"""Injector for FIDS translations keywords."""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_LANGUAGES_VIEW_NAME = "RefDelegateBean.WebUIViewLanguages"
FIDS_LANGUAGES_FIELDS = [
    "slaId",
    "slaName",
    "slaLanguageCode",
    "slaUpdateUser",
    "slaUpdateTime",
    "slaActiveInd",
    "slaHomeAirport",
    "slaCreateUser",
    "slaCreateTime",
]


def fids_languages_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS languages.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Languages

    """
    kwargs["order_by"] = "slaLanguageCode"
    return __base_get_data(
        FIDS_LANGUAGES_VIEW_NAME, FIDS_LANGUAGES_FIELDS, session_key, **kwargs
    )


FIDS_CODES_VIEW_NAME = "RefDelegateBean.ActiveLanguageCodes"
FIDS_CODES_FIELDS = [
    "id",
    "code",
    "description",
    "systemCode",
    "modifiedBy",
    "modifiedTime",
    "createdBy",
    "createdTime",
    "languageCodes",
    "languageNames",
    "languageValues",
]


def fids_codes_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS active language codes.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Codes

    """
    return __base_get_data(
        FIDS_CODES_VIEW_NAME, FIDS_CODES_FIELDS, session_key, **kwargs
    )


FIDS_AIRLINE_TRANSLATIONS_VIEW_NAME = "RefDelegateBean.LanguagesAirline"
FIDS_AIRLINE_TRANSLATIONS_FIELDS = [
    "rlgId",
    "rlgHomeAirport",
    "rlgDatatype",
    "rlgLanguageCode",
    "rlgKey",
    "rlgAltKey",
    "rlgFieldName",
    "rlgClearFieldValue",
    "rlgCreateTime",
    "rlgCreateUser",
    "rlgUpdateTime",
    "rlgUpdateUser",
]


def fids_airline_translations_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS airline translations.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Airline Translations

    """
    return __base_get_data(
        FIDS_AIRLINE_TRANSLATIONS_VIEW_NAME,
        FIDS_AIRLINE_TRANSLATIONS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_AIRPORT_TRANSLATIONS_VIEW_NAME = "RefDelegateBean.LanguagesAirport"
FIDS_AIRPORT_TRANSLATIONS_FIELDS = [
    "rlgId",
    "rlgHomeAirport",
    "rlgDatatype",
    "rlgLanguageCode",
    "rlgKey",
    "rlgAltKey",
    "rlgFieldName",
    "rlgClearFieldValue",
    "rlgCreateTime",
    "rlgCreateUser",
    "rlgUpdateTime",
    "rlgUpdateUser",
]


def fids_airport_translations_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS airport translations.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Airport Translations

    """
    return __base_get_data(
        FIDS_AIRPORT_TRANSLATIONS_VIEW_NAME,
        FIDS_AIRLINE_TRANSLATIONS_FIELDS,
        session_key,
        **kwargs,
    )
