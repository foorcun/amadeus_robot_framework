import protocols.broker
from .injector_rest import injector as rest_injector


# pylint: disable=line-too-long
def delete_leg_period(leg_period_id):
    """
    Delete leg period by id

    | *Arguments*                        | *Description*                                                                                         |

    | ``leg_period_id``                  | leg period id                                                                                         |


    === Usage: ===
    | delete_leg_period     6X$1725$$APT_GYD$APT_XYZ$2025-04-29$2025-04-30$23$arrival$0

    """

    return protocols.broker.injector(
        {"leg_period_id": leg_period_id}, "defaultKey", rest_injector
    )
