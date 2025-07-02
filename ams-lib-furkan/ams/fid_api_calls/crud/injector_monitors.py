"""Injector for FIDS Monitors keywords."""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_MONITORS_VIEW_NAME = "RefDelegateBean.Monitors"
FIDS_MONITORS_FIELDS = [
    "fmoId",
    "fmoHomeAirport",
    "fmoName",
    "fmoAdminStatus",
    "fmoDisplayName",
    "fmoRemark",
    "fmoTags",
    "fmoLeft",
    "fmoTop",
    "fmoHeight",
    "fmoWidth",
    "fmoFcoId",
    "fmoNearestNode",
    "fmoFacing",
    "fmoLayoutName",
    "fmoCreateUser",
    "fmoCreateTime",
    "fmoUpdateUser",
    "fmoUpdateTime",
    "fmoFlyId",
    "fmoLayoutParameters",
]


def fids_monitors_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS monitors.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Monitors

    """
    return __base_get_data(
        FIDS_MONITORS_VIEW_NAME, FIDS_MONITORS_FIELDS, session_key, **kwargs
    )
