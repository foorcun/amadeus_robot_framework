"""Injector for FIDS parameters keywords."""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_SYSTEM_PARAMETERS_VIEW_NAME = "RefDelegateBean.RefParamsSystemProperties"
FIDS_SYSTEM_PARAMETERS_FIELDS = [
    "rpaId",
    "rpaHomeAirport",
    "rpaType",
    "rpaKey",
    "rpaValue",
    "rpaDescription",
    "rpaUpdateUser",
    "rpaUpdateTime",
    "rpaCreateUser",
    "rpaCreateTime",
]


def fids_system_parameters_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS system parameters.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS System Parameters

    """
    return __base_get_data(
        FIDS_SYSTEM_PARAMETERS_VIEW_NAME,
        FIDS_SYSTEM_PARAMETERS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_CONTROLLER_PARAMETERS_VIEW_NAME = "RefDelegateBean.RefParamsControllerProperties"
FIDS_CONTROLLER_PARAMETERS_FIELDS = [
    "rpaId",
    "rpaHomeAirport",
    "rpaType",
    "rpaKey",
    "rpaValue",
    "rpaDescription",
    "rpaUpdateUser",
    "rpaUpdateTime",
    "rpaCreateUser",
    "rpaCreateTime",
]


def fids_controller_parameters_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS controller parameters.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Controller Parameters

    """
    return __base_get_data(
        FIDS_CONTROLLER_PARAMETERS_VIEW_NAME,
        FIDS_CONTROLLER_PARAMETERS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_MONITOR_PARAMETERS_VIEW_NAME = "RefDelegateBean.RefParamsMonitorProperties"
FIDS_MONITOR_PARAMETERS_FIELDS = [
    "rpaId",
    "rpaHomeAirport",
    "rpaType",
    "rpaKey",
    "rpaValue",
    "rpaDescription",
    "rpaUpdateUser",
    "rpaUpdateTime",
    "rpaCreateUser",
    "rpaCreateTime",
]


def fids_monitor_parameters_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS monitor parameters.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Monitor Parameters

    """
    return __base_get_data(
        FIDS_MONITOR_PARAMETERS_VIEW_NAME,
        FIDS_MONITOR_PARAMETERS_FIELDS,
        session_key,
        **kwargs,
    )
