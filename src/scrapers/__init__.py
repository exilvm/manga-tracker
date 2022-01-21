from typing import TYPE_CHECKING, Dict, Type

from src.scrapers.comikey import Comikey
from src.scrapers.comixology import ComiXology
from src.scrapers.kireicake import KireiCake
from src.scrapers.mangadex import MangaDex
from src.scrapers.mangaplus import MangaPlus
from src.scrapers.reddit import Reddit

if TYPE_CHECKING:
    from src.scrapers.base_scraper import BaseScraper

SCRAPERS: Dict[str, Type['BaseScraper']] = {
    MangaDex.URL: MangaDex,
    MangaPlus.URL: MangaPlus,
    ComiXology.URL: ComiXology,
    Reddit.URL: Reddit,
    KireiCake.URL: KireiCake,
    Comikey.URL: Comikey
}

SCRAPERS_ID: Dict[int, Type['BaseScraper']] = {
    s.ID: s for s in SCRAPERS.values()
}
