from ams.frms_api_calls.common import _frms_call

# pylint: disable=line-too-long


def frms_move_allocation(plan_id, allocation_id, resource_type, resource_id):
    """
    Move an allocation to a different resource in the FRMS plan.

    | *Arguments*                      | *Description*                                                      |
    | ``plan_id``                      | The ID of the FRMS plan where the allocation exists                |
    | ``allocation_id``                | The ID of the allocation to be moved                               |
    | ``resource_type``                | The type of the resource to which the allocation will be moved    |
    | ``resource_id``                  | The ID of the resource to which the allocation will be moved       |

    === Usage: ===
    | Frms Move Allocation    plan_id=5940b6e8-63cd-42a4-9438-9e6445ae716a  allocation_id=99f92b9b-d9a7-49d5-abb4-84f0e09d4dc3  resource_type=STAND  resource_id=STD000123
    """
    path_key = _get_path_key(resource_type)

    return _frms_call(
        "POST",
        f"/{path_key}/multi-moves/{plan_id}",  # TODO VC: fix me for belts, desk, generic resource type
        {"multiMoves": [{"allocationId": allocation_id, "resourceId": resource_id}]},
    )


def _get_path_key(resource_type):
    if resource_type == "BAGGAGE_BELT":
        path_key = "baggagebelt"
    elif resource_type == "CHECK_IN_DESK":
        path_key = "checkindesk"
    else:
        path_key = resource_type.lower()
    # TODO VC: generic resource type
    return f"{path_key}-allocations"
