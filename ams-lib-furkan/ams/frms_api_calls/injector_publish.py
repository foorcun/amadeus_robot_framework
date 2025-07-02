from ams.frms_api_calls.common import _frms_call

# pylint: disable=line-too-long


def frms_publish_visit(plan_id, visit_id):
    """
    Publishes the specified visit to FOM.

    | *Arguments*                | *Description*                                                |
    | ``plan_id``                | The ID of the FRMS plan in which the visit exists            |
    | ``visit_id``               | The ID of the visit to be published                          |

    === Usage: ===
    | Frms Publish Visit          plan_id=5940b6e8-63cd-42a4-9438-9e6445ae716a  visit_id=C_ZZZ_4253__20250612_ARRIVAL_XYZA:C_ZZZ_4254__20250612_DEPARTURE_XYZA   |
    """
    return _frms_call(
        "POST",
        f"/plan/publish/changes/{plan_id}",
        {"visitIds": [visit_id]},
        "application/x-www-form-urlencoded",
    )
