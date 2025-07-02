"""Injector for controller keywords for controllers in FIDS"""

# pylint: disable=line-too-long

from ams.fid_api_calls.crud.injector import (
    __base_get_data,
    __base_save_data,
    __base_delete_data,
    __integer_parameter,
    fids_get_home_airport,
)


FIDS_CONTROLLERS_VIEW_NAME = "DMDelegateBean.Controller"
FIDS_CONTROLLERS_FIELDS = [
    "fcoId",
    "fcoHomeAirport",
    "fcoCustomerId",
    "fcoName",
    "fcoDisplayName",
    "fcoRemark",
    "fcoTags",
    "fcoRdeInternalcode",
    "fcoAdminStatus",
    "fcoCreateTime",
    "fcoCreateUser",
    "fcoUpdateTime",
    "fcoUpdateUser",
    "fcoLedLayout",
    "fcoLedFdrId",
    "fcoClientVersion",
]


def fids_controllers_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS controllers.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                 | *Description*                                                                                      |
    | ``expected_response_code``  | Expected response code from the API response.                                                      |
    | ``endpoint_type``           | Endpoint URL to fetch the history details.                                                         |
    | ``additional_params``       | Dictionary. Values can be either a single value or a list of values. Query parameter to be passed. |

    === Usage: ===
    | Get Fids Controllers

    """
    return __base_get_data(
        FIDS_CONTROLLERS_VIEW_NAME, FIDS_CONTROLLERS_FIELDS, session_key, **kwargs
    )


def fids_controllers_get_by_id(controller_id, session_key="defaultKey", **kwargs):
    """
    Get a FIDS controller by its ID.

    | *Arguments*         | *Description*                                                                      |
    | ``controller_id``   | Controller ID.                                                                     |
    | ``session_key``     | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Fids Controller By Id    123

    """
    kwargs["where"] = "fcoId = ?"
    kwargs["additional_params"] = {"parameters": [__integer_parameter(controller_id)]}
    return __base_get_data(
        FIDS_CONTROLLERS_VIEW_NAME, FIDS_CONTROLLERS_FIELDS, session_key, **kwargs
    )


def fids_controllers_save(
    name,
    identification,
    controller_type="NET-2",
    admin_status="ACTIVE",
    session_key="defaultKey",
    **kwargs,
):
    """
    Save a FIDS controller.

    | *Arguments*         | *Description*                                                                 |
    | ``name``            | Controller name.                                                              |
    | ``identification``  | Customer identification.                                                      |
    | ``controller_type`` | (Optional) Controller type. Default is "NET-2".                               |
    | ``admin_status``    | (Optional) Admin status. Default is "ACTIVE".                                 |
    | ``session_key``     | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Save Fids Controller    name=MyController    identification=123

    """
    entity = {
        "fcoAdminStatus": admin_status,
        "fcoCustomerId": identification,
        "fcoName": name,
        "fcoRdeInternalcode": controller_type,
        "fcoHomeAirport": fids_get_home_airport(),
    }

    return __base_save_data(
        FIDS_CONTROLLERS_VIEW_NAME,
        FIDS_CONTROLLERS_FIELDS,
        entity,
        session_key,
        **kwargs,
    )


def fids_controllers_delete(controller, session_key="defaultKey", **kwargs):
    """
    Delete a FIDS controller.

    | *Arguments*      | *Description*                                                                 |
    | ``controller``   | Controller entity dictionary. Must contain key ``fcoId``.                     |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Delete Fids Controller    ${controller}

    """
    entity = {"fcoId": controller["fcoId"]}

    return __base_delete_data(
        FIDS_CONTROLLERS_VIEW_NAME,
        FIDS_CONTROLLERS_FIELDS,
        entity,
        session_key,
        **kwargs,
    )


FIDS_DEVICE_TYPES_VIEW_NAME = "RefDelegateBean.RefDeviceTypes"
FIDS_DEVICE_TYPES_FIELDS = ["rdeInternalcode", "rdeName"]


def fids_device_types_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS device types.

    | *Arguments*      | *Description*                                                                      |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Fids Device Types

    """
    return __base_get_data(
        FIDS_DEVICE_TYPES_VIEW_NAME, FIDS_DEVICE_TYPES_FIELDS, session_key, **kwargs
    )


FIDS_FILE_LAYOUTS_VIEW_NAME = "LedDelegateBean.FileLayouts"
FIDS_FILE_LAYOUTS_FIELDS = ["layoutFileName"]


def fids_file_layouts_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS file layouts.

    | *Arguments*      | *Description*                                                                      |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Fids File Layouts

    """
    kwargs["parameters"] = "daktronics"
    return __base_get_data(
        FIDS_FILE_LAYOUTS_VIEW_NAME, FIDS_FILE_LAYOUTS_FIELDS, session_key, **kwargs
    )


FIDS_CONTROLLER_MONITOR_TAGS_VIEW_NAME = "DMDelegateBean.MonitorControllerTags"
FIDS_CONTROLLER_MONITOR_TAGS_FIELDS = ["uniqueId", "tag"]


def fids_controller_monitor_tags_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS controller monitor tags.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Fids Controller Monitor Tags

    """
    return __base_get_data(
        FIDS_CONTROLLER_MONITOR_TAGS_VIEW_NAME,
        FIDS_CONTROLLER_MONITOR_TAGS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_LAYOUT_HOPO_VIEW_NAME = "DMDelegateBean.LayoutsByHOPO"
FIDS_LAYOUT_HOPO_FIELDS = ["flyId", "flyName", "flyDisplayName"]


def fids_layouts_hopo_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS layouts by HOPO.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Fids Layouts HOPO

    """
    return __base_get_data(
        FIDS_LAYOUT_HOPO_VIEW_NAME, FIDS_LAYOUT_HOPO_FIELDS, session_key, **kwargs
    )
