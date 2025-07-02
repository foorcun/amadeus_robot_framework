"""Injector for FIDS messages keywords"""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_VIEW_LANGUAGES_VIEW_NAME = "RefDelegateBean.ViewLanguages"
FIDS_VIEW_LANGUAGES_FIELDS = ["slaId", "slaLanguageCode", "slaName"]


def fids_view_languages_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS view languages.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS View Languages

    """
    return __base_get_data(
        FIDS_VIEW_LANGUAGES_VIEW_NAME, FIDS_VIEW_LANGUAGES_FIELDS, session_key, **kwargs
    )


FIDS_MONITOR_ZONES_VIEW_NAME = "RefDelegateBean.MonitorPropsZone"
FIDS_MONITOR_ZONES_FIELDS = ["fmpValue"]


def fids_monitor_zones_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS monitor zones.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Monitor Zones

    """
    return __base_get_data(
        FIDS_MONITOR_ZONES_VIEW_NAME, FIDS_MONITOR_ZONES_FIELDS, session_key, **kwargs
    )


FIDS_MESSAGE_TEMPLATES_VIEW_NAME = "FidDelegateBean.SysMsgTemplates"
FIDS_MESSAGE_TEMPLATES_FIELDS = [
    "smtId",
    "smtCode",
    "smtCreateTime",
    "smtCreateUser",
    "smtUpdateTime",
    "smtUpdateUser",
    "smtHomeAirport",
]


def fids_message_templates_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS message templates.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Message Templates

    """
    return __base_get_data(
        FIDS_MESSAGE_TEMPLATES_VIEW_NAME,
        FIDS_MESSAGE_TEMPLATES_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_MESSAGE_LANUGAGES_VIEW_NAME = "FidDelegateBean.RelSgmSla"
FIDS_MESSAGE_LANUGAGES_FIELDS = [
    "sgmSlaId",
    "sgmSlaClearMessage",
    "sgmSlaSgm",
    "sgmSlaSla",
]


def fids_message_languages_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS message languages.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Message Languages

    """
    return __base_get_data(
        FIDS_MESSAGE_LANUGAGES_VIEW_NAME,
        FIDS_MESSAGE_LANUGAGES_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_MESSAGE_TEMPLATE_LANGUAGES_VIEW_NAME = "FidDelegateBean.RelSmtSla"
FIDS_MESSAGE_TEMPLATE_LANGUAGES_FIELDS = [
    "smtSlaId",
    "smtSlaClearMessage",
    "smtSlaSmt",
    "smtSlaSla",
]


def fids_message_template_lanaguages_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS message template languages.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Message Template Languages

    """
    return __base_get_data(
        FIDS_MESSAGE_TEMPLATE_LANGUAGES_VIEW_NAME,
        FIDS_MESSAGE_TEMPLATE_LANGUAGES_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_MESSAGES_VIEW_NAME = "FidDelegateBean.SysGenMessages"
FIDS_MESSAGES_FIELDS = [
    "sgmId",
    "sgmHomeAirport",
    "sgmPriority",
    "sgmExternalId",
    "sgmSource",
    "sgmMessage1",
    "sgmMessage2",
    "sgmMessage3",
    "sgmZones",
    "sgmStartTime",
    "sgmEndTime",
    "sgmTemplateId",
    "sgmCreateTime",
    "sgmCreateUser",
    "sgmUpdateTime",
    "sgmUpdateUser",
    "sgmRelUpdateTime",
]


def fids_messages_get(
    time_window_start=-12, time_window_end=12, session_key="defaultKey", **kwargs
):
    """
    Get FIDS messages within a time window.

    | *Arguments*          | *Description*                                                                |
    | ``time_window_start``| (Optional) Start of the time window (hours). Default is -12.                 |
    | ``time_window_end``  | (Optional) End of the time window (hours). Default is 12.                    |
    | ``session_key``      | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Messages    time_window_start=-12    time_window_end=12

    """
    kwargs["parameters"] = [time_window_start, time_window_end]
    return __base_get_data(
        FIDS_MESSAGES_VIEW_NAME, FIDS_MESSAGES_FIELDS, session_key, **kwargs
    )
