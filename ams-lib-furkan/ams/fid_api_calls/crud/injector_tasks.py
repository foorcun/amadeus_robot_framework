"""Injector for FIDS Scheduled Tasks keywords"""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_SCHEUDLED_TASKS_VIEW_NAME = "FidDelegateBean.ScheduledTasks"
FIDS_SCHEUDLED_TASKS_FIELDS = [
    "fstId",
    "fstHomeAirport",
    "fstName",
    "fstType",
    "fstCommand",
    "fstDescription",
    "fstClearDescription",
    "fstTags",
    "fstStartTime",
    "fstEndTime",
    "fstRecurrenceType",
    "fstRecurrences",
    "fstRecurrenceDays",
    "fstLastRunTime",
    "fstNextRunTime",
    "fstCreateTime",
    "fstCreateUser",
    "fstUpdateTime",
    "fstUpdateUser",
]


def fids_scheduled_tasks_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS scheduled tasks.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Scheduled Tasks

    """
    return __base_get_data(
        FIDS_SCHEUDLED_TASKS_VIEW_NAME,
        FIDS_SCHEUDLED_TASKS_FIELDS,
        session_key,
        **kwargs,
    )
