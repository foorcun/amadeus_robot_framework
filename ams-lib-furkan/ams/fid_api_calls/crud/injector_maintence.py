"""FIDS Injector Maintenance and Monitoring keywords"""

import json
from ams.fid_api_calls.crud.injector import (
    __base_get_data,
    __base_execute_function,
    fids_get_home_airport,
)

# pylint: disable=line-too-long


def fids_send_controller_command(
    command, controller=None, controller_ids=None, session_key="defaultKey", **kwargs
):
    """
    Send a command to one or more FIDS controllers.

    | *Arguments*        | *Description*                                                                 |
    | ``command``        | Command string to send.                                                       |
    | ``controller``     | (Optional) Controller entity dictionary. Must contain key ``fcoId``.          |
    | ``controller_ids`` | (Optional) List of controller IDs.                                            |
    | ``session_key``    | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Send Controller Command    command=REBOOT    controller=${controller}
    | Send Controller Command    command=REBOOT    controller_ids=[1,2,3]

    """
    if controller is not None:
        controllers = [{"controllerId": controller["fcoId"]}]
    else:
        controllers = []
        for controler_id in controller_ids:
            controllers.append({"controllerId": controler_id})

    parameters = [
        command,
        fids_get_home_airport(),
        "{}",
        json.dumps(controllers),
    ]
    return __base_execute_function(
        "FidDelegateBean.buildClientCommand", parameters, session_key, **kwargs
    )


FIDS_ALL_DEVICES_VIEW_NAME = "RefDelegateBean.AllDevices"
FIDS_ALL_DEVICES_FIELDS = [
    "deviceId",
    "deviceIdentification",
    "deviceStatus",
    "deviceType",
    "deviceName",
    "deviceDescription",
    "deviceHomeAirport",
    "deviceControllerId",
    "deviceControllerType",
    "deviceAdminStatus",
]


def fids_all_devices_get(session_key="defaultKey", **kwargs):
    """
    Get all FIDS devices, this is the Maintence and Monitoring 'All Devices' tab

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get All Devices

    """
    return __base_get_data(
        FIDS_ALL_DEVICES_VIEW_NAME, FIDS_ALL_DEVICES_FIELDS, session_key, **kwargs
    )
