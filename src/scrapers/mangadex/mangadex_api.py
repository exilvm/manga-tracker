import logging
from datetime import datetime
from enum import Enum
from typing import Optional, List, Union, Dict, Iterable, Literal, TypeVar, \
    Type, TypedDict, Generic

import requests
from pydantic import BaseModel, Field, validator, ValidationError, \
    root_validator
from pydantic.generics import GenericModel
from ratelimit import rate_limited, sleep_and_retry

from src.enums import Status as MangaStatus

logger = logging.getLogger('debug')

SortDirection = Literal['asc', 'desc']
DataT = TypeVar('DataT')

SortColumns = TypedDict('SortColumns', {
    'createdAt': SortDirection,
    'updatedAt': SortDirection,
    'publishAt': SortDirection,
    'volume': SortDirection,
    'chapter': SortDirection,
}, total=False)


class MangadexResultStatus(Enum):
    ok = 'ok'
    error = 'error'


class Relationship(BaseModel):
    id: str
    type: str


class Links(BaseModel):
    al: Optional[str]
    ap: Optional[str]
    bw: Optional[str]
    mu: Optional[str]
    nu: Optional[str]
    kt: Optional[str]
    amz: Optional[str]
    ebj: Optional[str]
    mal: Optional[str]
    raw: Optional[str]
    engtl: Optional[str]


class Status(Enum):
    ongoing = 'ongoing'
    completed = 'completed'
    hiatus = 'hiatus'
    cancelled = 'cancelled'

    def to_int(self) -> int:
        d: Dict[Status, int] = {
            self.ongoing: MangaStatus.ONGOING.value,        # type: ignore[dict-item]
            self.completed: MangaStatus.COMPLETED.value,    # type: ignore[dict-item]
            self.hiatus: MangaStatus.HIATUS.value,          # type: ignore[dict-item]
            self.cancelled: MangaStatus.DROPPED.value,      # type: ignore[dict-item]
        }

        return d[self]


class MangadexData(GenericModel, Generic[DataT]):
    id: str
    attributes: DataT


class MangadexResult(GenericModel, Generic[DataT]):
    result: MangadexResultStatus
    data: MangadexData[DataT]
    relationships: List[Relationship]


class ChapterAttributes(BaseModel):
    volume: Optional[str]
    chapter: Optional[str]
    title: Optional[str]
    publish_at: datetime = Field(..., alias='publishAt')


class ScanlationGroupAttributes(BaseModel):
    name: str


class ChapterResult(MangadexResult[ChapterAttributes]):
    group: Optional[MangadexData[ScanlationGroupAttributes]]

    @property
    def ok(self) -> bool:
        return self.result == MangadexResultStatus.ok

    @root_validator(pre=True)
    def restructure_data(cls, data):
        """
        Maps data for reference expanded objects
        """
        if 'relationships' not in data:
            return data

        for r in data['relationships']:
            if 'attributes' not in r:
                continue

            rtype = r['type']
            if rtype == 'scanlation_group':
                # Support only a single group per chapter for now
                data['group'] = r
                break

        return data

    @property
    def manga_id(self) -> str:
        for relationship in self.relationships:
            if relationship.type == 'manga':
                return relationship.id

        raise ValueError(f'Manga id not found for {self}')

    @property
    def group_id(self) -> str:
        for relationship in self.relationships:
            if relationship.type == 'scanlation_group':
                return relationship.id

        raise ValueError(f'Scanlation group id not found for {self}')


class MangaAttributes(BaseModel):
    title: str
    links: Links
    status: Status

    @validator('title', pre=True)
    def validate_title(cls, v):
        return v['en']

    @validator('links', pre=True)
    def validate_links(cls, v):
        if v is None:
            return Links()
        return v


class AuthorAttributes(BaseModel):
    name: str


class CoverAttributes(BaseModel):
    file_name: str = Field(..., alias='fileName')


class MangaResult(MangadexResult[MangaAttributes]):
    # We need to redefine this here as mypy is too stupid to understand
    # nested generics
    data: MangadexData[MangaAttributes]
    authors: Optional[List[MangadexData[AuthorAttributes]]]
    artists: Optional[List[MangadexData[AuthorAttributes]]]
    cover: Optional[MangadexData[CoverAttributes]]

    @root_validator(pre=True)
    def restructure_data(cls, data):
        """
        Maps data for reference expanded objects
        """
        if 'relationships' not in data:
            return data

        authors = []
        artists = []
        for r in data['relationships']:
            if 'attributes' not in r:
                continue

            rtype = r['type']
            if rtype == 'cover_art':
                data['cover'] = r
            elif rtype == 'artist':
                artists.append(r)
            elif rtype == 'author':
                authors.append(r)

        if authors:
            data['authors'] = authors
        if artists:
            data['artists'] = artists

        return data

    def author_relationships(self) -> Iterable[Relationship]:
        for relationship in self.relationships:
            if relationship.type == 'author':
                yield relationship

    def artist_relationships(self) -> Iterable[Relationship]:
        for relationship in self.relationships:
            if relationship.type == 'artist':
                yield relationship

    def cover_id(self) -> Optional[str]:
        for relationship in self.relationships:
            if relationship.type == 'cover_art':
                return relationship.id

        return None


class AuthorResult(MangadexResult[AuthorAttributes]):
    data: MangadexData[AuthorAttributes]


class CoverResult(MangadexResult[CoverAttributes]):
    data: MangadexData[CoverAttributes]


class ScanlationGroupResult(MangadexResult[ScanlationGroupAttributes]):
    data: MangadexData[ScanlationGroupAttributes]


def handle_response(r: requests.Response) -> Dict:
    if not r.ok:
        raise ValueError(f'Failed to fetch {r.url}', r)

    return try_parse_result(r)


def try_parse_result(r: requests.Response) -> Dict:
    data = r.json()

    if 'results' not in data:
        raise ValueError('Results not found in response', data)

    return data


# This does not work correctly and consistently when bound=MangadexResult
GenericResults = TypeVar('GenericResults', bound=BaseModel)
GenericMangadexResults = TypeVar('GenericMangadexResults', bound=MangadexResult)


# noinspection PyPep8Naming
def request_to_model(r: requests.Response, Model: Type[GenericResults]) -> Iterable[GenericResults]:
    for result in handle_response(r)['results']:
        try:
            yield Model(**result)
        except ValidationError:
            logger.warning(f'Failed to parse result for model {Model.__name__} {result}', exc_info=True)


api_rate_limiter = rate_limited(5, 1)


class MangadexAPI:
    def __init__(self, url='https://api.mangadex.org'):
        self.base_url = url

    @staticmethod
    def join_array(ids: List[str], key: str):
        key = key + '[]'
        return f'{key}={f"&{key}=".join(ids)}'

    @sleep_and_retry
    @api_rate_limiter
    def get_manga(self, manga_ids: Union[str, List[str]], include_authors: bool = True,
                  include_artists: bool = True, include_cover: bool = True) -> Iterable[MangaResult]:
        if isinstance(manga_ids, str):
            manga_ids = [manga_ids]
        if len(manga_ids) > 100:
            raise ValueError('Max 100 manga can be fetched at a time')

        includes = []
        if include_authors:
            includes.append('author')
        if include_artists:
            includes.append('artist')
        if include_cover:
            includes.append('cover_art')

        params = [self.join_array(manga_ids, "ids")]

        if includes:
            params.append(self.join_array(includes, 'includes'))

        params.append(f'limit={len(manga_ids)}')

        r = requests.get(f'{self.base_url}/manga?{"&".join(params)}')

        return request_to_model(r, MangaResult)

    @sleep_and_retry
    @api_rate_limiter
    def get_chapters(self, sort_by: SortColumns, *, languages: List[str],
                     manga_id: str = None, limit: int = 100,
                     include_groups: bool = True) -> Iterable[ChapterResult]:
        params = []
        order = []
        for k, v in sort_by.items():
            order.append(f'order[{k}]={v}')

        params.append('&'.join(order))

        if languages:
            params.append(self.join_array(languages, 'translatedLanguage'))

        if manga_id:
            params.append(f'manga={manga_id}')

        if limit:
            params.append(f'limit={limit}')

        if include_groups:
            params.append('includes[]=scanlation_group')

        r = requests.get(f'{self.base_url}/chapter?{"&".join(params)}')

        return request_to_model(r, ChapterResult)

    # Commented out as it's not required after reference expansion was introduced
    # def fetch_chunked(self, api_path: str, ids: List[str], model: Type[GenericMangadexResults]) -> Dict[str, GenericMangadexResults]:
    #     if not ids:
    #         return {}
    #
    #     chunk_size = 100
    #     ids = list(set(ids))
    #     results: Dict[str, GenericMangadexResults] = {}
    #
    #     # Inner function to get rate limits for each request
    #     @sleep_and_retry
    #     @api_rate_limiter
    #     def fetch_data(chunk):
    #         r = requests.get(f'{self.base_url}/{api_path}?limit={len(chunk)}&{self.join_array(chunk, "ids")}')
    #         for m in request_to_model(r, model):
    #             results[m.data.id] = m
    #
    #     for i in range(0, len(ids), chunk_size):
    #         fetch_data(ids[i:i + chunk_size])
    #
    #     return results
    #
    # def get_authors(self, author_ids: List[str]) -> Dict[str, AuthorResult]:
    #     return self.fetch_chunked('author', author_ids, AuthorResult)
    #
    # def get_covers(self, cover_ids: List[str]) -> Dict[str, CoverResult]:
    #     return self.fetch_chunked('cover', cover_ids, CoverResult)
    #
    # def get_scanlation_groups(self, group_ids: List[str]) -> Dict[str, ScanlationGroupResult]:
    #     return self.fetch_chunked('group', group_ids, ScanlationGroupResult)
