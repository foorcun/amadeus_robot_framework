from ams.data_model.common_libs.utils.generic_helpers import add_data_to_clean_up
from ams.frms_api_calls.common import _frms_call

# pylint: disable=line-too-long


def frms_get_plans():
    """
    Get FRMS Plans
                                                    |

    === Usage: ===
    | Frms Get Plans

    """
    return _frms_call("GET", "/plans/list")


def frms_get_plan_by_id(plan_id):
    """
    Get FRMS Plan By Id

    | *Arguments*                       | *Description*                                                        |
    | ``plan_id``                       | plan id                                                              |

    === Usage: ===
    | Frms Get Plan By Id    plan_id=5940b6e8-63cd-42a4-9438-9e6445ae716a

    """
    return _frms_call("GET", f"/plans/find/{plan_id}")


def frms_create_plan(resource_type, name, start_date, end_date):
    """
    Create an FRMS plan

    | *Arguments*                      | *Description*                                                   |
    | ``resource_type``                | Resource type (e.g., STAND)                                     |
    | ``name``                         | Name of the plan                                                |

    === Usage: ===
    | Frms Create Plan    resource_type=STAND   name=MyPlan

    """
    if resource_type.upper() in ["STAND", "GATE"]:
        resource_types = ["STAND", "GATE"]
    else:
        resource_types = [resource_type.upper()]

    form_data = {
        "name": name,
        "resourceTypes": resource_types,
        "startDate": start_date,
        "endDate": end_date,
        "includeOnGroundFlights": "false",
    }

    plan = _frms_call(
        "POST",
        "/plans/create",
        form_data,
        "application/x-www-form-urlencoded",
    )

    add_data_to_clean_up("frms_plan", plan["id"])

    return plan


def frms_delete_plans(plan_ids):
    """
    Delete a list of FRMS plans

    | *Arguments*                     | *Description*                                                 |
    | ``plan_ids``                    | List of Plan IDs to delete                                    |

    === Usage: ===
    | Frms Delete Plans    plan_ids=[5940b6e8-63cd-42a4-9438-9e6445ae716a]

    """
    return _frms_call("POST", "/plans/delete/secure", plan_ids)
