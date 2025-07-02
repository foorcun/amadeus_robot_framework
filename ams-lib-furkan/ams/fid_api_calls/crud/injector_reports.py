"""Injector FIDS reports keywords."""

import datetime
from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_CLIENT_REPORT_VIEW_NAME = "FidDelegateBean.AuditClientReport"
FIDS_CLIENT_REPORT_FIELDS = [
    "facId",
    "facTimestamp",
    "facDeviceId",
    "facSeverity",
    "facEventType",
    "facDescription",
]


def fids_client_report_get(
    time_window_start=-24,
    time_window_end=0,
    device_id=None,
    event_type=None,
    event_description=None,
    severity=None,
    session_key="defaultKey",
    **kwargs,
):
    """
    Get FIDS client reports within a time window.

    | *Arguments*           | *Description*                                                                |
    | ``time_window_start`` | (Optional) Start of the time window (hours). Default is -24.                 |
    | ``time_window_end``   | (Optional) End of the time window (hours). Default is 0.                     |
    | ``device_id``         | (Optional) Filter by device ID.                                              |
    | ``event_type``        | (Optional) Filter by event type.                                             |
    | ``event_description`` | (Optional) Filter by event description.                                      |
    | ``severity``          | (Optional) Filter by severity.                                               |
    | ``session_key``       | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Client Report    time_window_start=-24    time_window_end=0    device_id=123

    """
    kwargs["where"] = "facTimestamp>=? AND facTimestamp<=?"
    now = datetime.datetime.now().replace(microsecond=0)
    start = now + datetime.timedelta(hours=time_window_start)
    end = now + datetime.timedelta(hours=time_window_end)
    kwargs["parameters"] = [start.isoformat(), end.isoformat()]

    if device_id is not None:
        kwargs["where"] = (
            kwargs["where"] + f" AND (UPPER(facDeviceId) LIKE '{device_id.upper()}%')"
        )
    if event_description is not None:
        kwargs["where"] = (
            kwargs["where"]
            + f" AND (UPPER(facDescription) LIKE '{event_description.upper()}%')"
        )
    if severity is not None:
        kwargs["where"] = (
            kwargs["where"] + f" AND (UPPER(facSeverity) LIKE '{severity.upper()}%')"
        )
    if event_type is not None:
        kwargs["where"] = (
            kwargs["where"] + f" AND (UPPER(facEventType) LIKE '{event_type.upper()}%')"
        )

    return __base_get_data(
        FIDS_CLIENT_REPORT_VIEW_NAME, FIDS_CLIENT_REPORT_FIELDS, session_key, **kwargs
    )


FIDS_SYSTEM_REPORT_VIEW_NAME = "FidDelegateBean.AuditSystemReport"
FIDS_SYSTEM_REPORT_FIELDS = [
    "fasId",
    "fasNodeName",
    "fasHomeAirport",
    "fasTimestamp",
    "fasCustomerId",
    "fasSeverity",
    "fasCorrelationId",
    "fasEventType",
    "fasDescription",
    "fasCreateTime",
    "fasUpdateTime",
    "fasUpdateUser",
]


def fids_system_report_get(
    time_window_start=-24,
    time_window_end=0,
    event_type=None,
    severity=None,
    session_key="defaultKey",
    **kwargs,
):
    """
    Get FIDS system reports within a time window

    | *Arguments*           | *Description*                                                                |
    | ``time_window_start`` | (Optional) Start of the time window (hours). Default is -24.                 |
    | ``time_window_end``   | (Optional) End of the time window (hours). Default is 0.                     |
    | ``event_type``        | (Optional) Filter by event type.                                             |
    | ``severity``          | (Optional) Filter by severity.                                               |
    | ``session_key``       | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS System Report    time_window_start=-24    time_window_end=0

    """
    kwargs["where"] = "fasTimestamp>=? AND fasTimestamp<=?"
    now = datetime.datetime.now().replace(microsecond=0)
    start = now + datetime.timedelta(hours=time_window_start)
    end = now + datetime.timedelta(hours=time_window_end)
    kwargs["parameters"] = [start.isoformat(), end.isoformat()]

    if severity is not None:
        kwargs["where"] = (
            kwargs["where"] + f" AND (UPPER(fasSeverity) LIKE '{severity.upper()}%')"
        )
    if event_type is not None:
        kwargs["where"] = (
            kwargs["where"] + f" AND (UPPER(fasEventType) LIKE '{event_type.upper()}%')"
        )

    return __base_get_data(
        FIDS_SYSTEM_REPORT_VIEW_NAME, FIDS_SYSTEM_REPORT_FIELDS, session_key, **kwargs
    )
