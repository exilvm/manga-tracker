# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    NewType as typing___NewType,
    Optional as typing___Optional,
    Text as typing___Text,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

ActionValue = typing___NewType('ActionValue', builtin___int)
type___ActionValue = ActionValue
Action: _Action
class _Action(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[ActionValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    DEFAULT = typing___cast(ActionValue, 0)
    UNAUTHORIZED = typing___cast(ActionValue, 1)
    MAINTENANCE = typing___cast(ActionValue, 2)
    GEOIP_BLOCKING = typing___cast(ActionValue, 3)
DEFAULT = typing___cast(ActionValue, 0)
UNAUTHORIZED = typing___cast(ActionValue, 1)
MAINTENANCE = typing___cast(ActionValue, 2)
GEOIP_BLOCKING = typing___cast(ActionValue, 3)
type___Action = Action

class Popup(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    subject: typing___Text = ...
    body: typing___Text = ...

    def __init__(self,
        *,
        subject : typing___Optional[typing___Text] = None,
        body : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"body",b"body",u"subject",b"subject"]) -> None: ...
type___Popup = Popup

class Title(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    LanguageValue = typing___NewType('LanguageValue', builtin___int)
    type___LanguageValue = LanguageValue
    Language: _Language
    class _Language(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[Title.LanguageValue]):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        ENGLISH = typing___cast(Title.LanguageValue, 0)
        SPANISH = typing___cast(Title.LanguageValue, 1)
    ENGLISH = typing___cast(Title.LanguageValue, 0)
    SPANISH = typing___cast(Title.LanguageValue, 1)
    type___Language = Language

    title_id: builtin___int = ...
    name: typing___Text = ...
    author: typing___Text = ...
    portrait_image_url: typing___Text = ...
    landscape_image_url: typing___Text = ...
    view_count: builtin___int = ...
    language: type___Title.LanguageValue = ...

    def __init__(self,
        *,
        title_id : typing___Optional[builtin___int] = None,
        name : typing___Optional[typing___Text] = None,
        author : typing___Optional[typing___Text] = None,
        portrait_image_url : typing___Optional[typing___Text] = None,
        landscape_image_url : typing___Optional[typing___Text] = None,
        view_count : typing___Optional[builtin___int] = None,
        language : typing___Optional[type___Title.LanguageValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"author",b"author",u"landscape_image_url",b"landscape_image_url",u"language",b"language",u"name",b"name",u"portrait_image_url",b"portrait_image_url",u"title_id",b"title_id",u"view_count",b"view_count"]) -> None: ...
type___Title = Title

class Chapter(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    title_id: builtin___int = ...
    chapter_id: builtin___int = ...
    name: typing___Text = ...
    sub_title: typing___Text = ...
    thumbnail_url: typing___Text = ...
    start_timestamp: builtin___int = ...
    end_timestamp: builtin___int = ...

    def __init__(self,
        *,
        title_id : typing___Optional[builtin___int] = None,
        chapter_id : typing___Optional[builtin___int] = None,
        name : typing___Optional[typing___Text] = None,
        sub_title : typing___Optional[typing___Text] = None,
        thumbnail_url : typing___Optional[typing___Text] = None,
        start_timestamp : typing___Optional[builtin___int] = None,
        end_timestamp : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"chapter_id",b"chapter_id",u"end_timestamp",b"end_timestamp",u"name",b"name",u"start_timestamp",b"start_timestamp",u"sub_title",b"sub_title",u"thumbnail_url",b"thumbnail_url",u"title_id",b"title_id"]) -> None: ...
type___Chapter = Chapter

class TitleDetailView(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    UpdateTimingValue = typing___NewType('UpdateTimingValue', builtin___int)
    type___UpdateTimingValue = UpdateTimingValue
    UpdateTiming: _UpdateTiming
    class _UpdateTiming(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[TitleDetailView.UpdateTimingValue]):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        NOT_REGULARLY = typing___cast(TitleDetailView.UpdateTimingValue, 0)
        MONDAY = typing___cast(TitleDetailView.UpdateTimingValue, 1)
        TUESDAY = typing___cast(TitleDetailView.UpdateTimingValue, 2)
        WEDNESDAY = typing___cast(TitleDetailView.UpdateTimingValue, 3)
        THURSDAY = typing___cast(TitleDetailView.UpdateTimingValue, 4)
        FRIDAY = typing___cast(TitleDetailView.UpdateTimingValue, 5)
        SATURDAY = typing___cast(TitleDetailView.UpdateTimingValue, 6)
        SUNDAY = typing___cast(TitleDetailView.UpdateTimingValue, 7)
        DAY = typing___cast(TitleDetailView.UpdateTimingValue, 8)
    NOT_REGULARLY = typing___cast(TitleDetailView.UpdateTimingValue, 0)
    MONDAY = typing___cast(TitleDetailView.UpdateTimingValue, 1)
    TUESDAY = typing___cast(TitleDetailView.UpdateTimingValue, 2)
    WEDNESDAY = typing___cast(TitleDetailView.UpdateTimingValue, 3)
    THURSDAY = typing___cast(TitleDetailView.UpdateTimingValue, 4)
    FRIDAY = typing___cast(TitleDetailView.UpdateTimingValue, 5)
    SATURDAY = typing___cast(TitleDetailView.UpdateTimingValue, 6)
    SUNDAY = typing___cast(TitleDetailView.UpdateTimingValue, 7)
    DAY = typing___cast(TitleDetailView.UpdateTimingValue, 8)
    type___UpdateTiming = UpdateTiming

    title_image_url: typing___Text = ...
    overview: typing___Text = ...
    background_image_url: typing___Text = ...
    next_timestamp: builtin___int = ...
    update_timing: type___TitleDetailView.UpdateTimingValue = ...
    viewing_period_description: typing___Text = ...
    non_appearance_info: typing___Text = ...
    is_simul_release: builtin___bool = ...
    chapters_descending: builtin___bool = ...

    @property
    def title(self) -> type___Title: ...

    @property
    def first_chapter_list(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___Chapter]: ...

    @property
    def last_chapter_list(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___Chapter]: ...

    @property
    def recommended_titles(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___Title]: ...

    def __init__(self,
        *,
        title : typing___Optional[type___Title] = None,
        title_image_url : typing___Optional[typing___Text] = None,
        overview : typing___Optional[typing___Text] = None,
        background_image_url : typing___Optional[typing___Text] = None,
        next_timestamp : typing___Optional[builtin___int] = None,
        update_timing : typing___Optional[type___TitleDetailView.UpdateTimingValue] = None,
        viewing_period_description : typing___Optional[typing___Text] = None,
        non_appearance_info : typing___Optional[typing___Text] = None,
        first_chapter_list : typing___Optional[typing___Iterable[type___Chapter]] = None,
        last_chapter_list : typing___Optional[typing___Iterable[type___Chapter]] = None,
        recommended_titles : typing___Optional[typing___Iterable[type___Title]] = None,
        is_simul_release : typing___Optional[builtin___bool] = None,
        chapters_descending : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"title",b"title"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"background_image_url",b"background_image_url",u"chapters_descending",b"chapters_descending",u"first_chapter_list",b"first_chapter_list",u"is_simul_release",b"is_simul_release",u"last_chapter_list",b"last_chapter_list",u"next_timestamp",b"next_timestamp",u"non_appearance_info",b"non_appearance_info",u"overview",b"overview",u"recommended_titles",b"recommended_titles",u"title",b"title",u"title_image_url",b"title_image_url",u"update_timing",b"update_timing",u"viewing_period_description",b"viewing_period_description"]) -> None: ...
type___TitleDetailView = TitleDetailView

class AllTitlesView(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def titles(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___Title]: ...

    def __init__(self,
        *,
        titles : typing___Optional[typing___Iterable[type___Title]] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"titles",b"titles"]) -> None: ...
type___AllTitlesView = AllTitlesView

class SuccessResult(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def titles(self) -> type___AllTitlesView: ...

    @property
    def title_detail(self) -> type___TitleDetailView: ...

    def __init__(self,
        *,
        titles : typing___Optional[type___AllTitlesView] = None,
        title_detail : typing___Optional[type___TitleDetailView] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"result",b"result",u"title_detail",b"title_detail",u"titles",b"titles"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"result",b"result",u"title_detail",b"title_detail",u"titles",b"titles"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"result",b"result"]) -> typing_extensions___Literal["titles","title_detail"]: ...
type___SuccessResult = SuccessResult

class ErrorResult(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    action: type___ActionValue = ...
    debug_info: typing___Text = ...

    @property
    def english_popup(self) -> type___Popup: ...

    @property
    def spanish_popup(self) -> type___Popup: ...

    def __init__(self,
        *,
        action : typing___Optional[type___ActionValue] = None,
        english_popup : typing___Optional[type___Popup] = None,
        spanish_popup : typing___Optional[type___Popup] = None,
        debug_info : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"english_popup",b"english_popup",u"spanish_popup",b"spanish_popup"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"action",b"action",u"debug_info",b"debug_info",u"english_popup",b"english_popup",u"spanish_popup",b"spanish_popup"]) -> None: ...
type___ErrorResult = ErrorResult

class Response(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def success_result(self) -> type___SuccessResult: ...

    @property
    def error_result(self) -> type___ErrorResult: ...

    def __init__(self,
        *,
        success_result : typing___Optional[type___SuccessResult] = None,
        error_result : typing___Optional[type___ErrorResult] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"error_result",b"error_result",u"success_result",b"success_result"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"error_result",b"error_result",u"success_result",b"success_result"]) -> None: ...
type___Response = Response
