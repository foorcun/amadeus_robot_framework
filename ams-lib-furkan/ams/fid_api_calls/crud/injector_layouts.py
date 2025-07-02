"""Injector for FIDS Layouts keywords"""

from ams.fid_api_calls.crud.injector import __base_get_data

FIDS_LAYOUT_VIEW_NAME = "DMDelegateBean.Layout"
FIDS_LAYOUT_FIELDS = [
    "flyId",
    "flyName",
    "flyHomeAirport",
    "flyRemark",
    "flyTags",
    "flyDisplayName",
    "flyOobInd",
    "flyUpdateUser",
    "flyUpdateTime",
    "flyCreateUser",
    "flyCreateTime",
]


def fids_layouts_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS layouts.

    | *Arguments*      | *Description*                                                           |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Layouts

    """
    return __base_get_data(
        FIDS_LAYOUT_VIEW_NAME, FIDS_LAYOUT_FIELDS, session_key, **kwargs
    )
