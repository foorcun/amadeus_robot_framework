import logging

LOGGER = logging.getLogger(__name__)


def frms_find_visit_in_plan(plan, flight_id):
    """
    Finds a visit in the specified FRMS plan by flight ID.

    | *Arguments*                | *Description*                                                |
    | ``plan``                   | The FRMS plan object in which to search for the visit        |
    | ``flight_id``              | The flight ID to search for                                  |

    === Usage: ===
    | Frms Find Visit In Plan      plan=${plan}    flight_id=C_AIC_372__20250327_ARRIVAL_XYZA   |
    """
    visits = plan["dictionary"]["visitOperations"]

    visit = next(
        filter(
            lambda visit: (
                visit["inboundFlight"]
                and visit["inboundFlight"]["functionalId"] == flight_id
            )
            or (
                visit["outboundFlight"]
                and visit["outboundFlight"]["functionalId"] == flight_id
            ),
            visits.values(),
        ),
        None,
    )

    if visit is None:
        raise ValueError(f"Flight {flight_id} not found in FRMS plan {plan}")

    return visit


def frms_get_allocations(visit, resource_type):
    """
    Retrieves the allocations for a specific resource type from the FRMS visit.

    | *Arguments*                | *Description*                                                  |
    | ``visit``                  | The FRMS visit object from which to retrieve allocations       |
    | ``resource_type``          | The type of resource for which to retrieve allocations         |

        === Usage: ===
    | Frms Get Allocations      visit=${visit}    resource_type=STAND                                                 |
    """
    return visit["allocations"][resource_type]


def frms_find_operational_plan(plan_list, resource_type):
    """
    Finds an operational FRMS plan that contains the specified resource type.

    | *Arguments*                | *Description*                                                  |
    | ``plan_list``              | The list of FRMS plans to search through                       |
    | ``resource_type``          | The type of resource to search for in the plans                |

        === Usage: ===
    | Frms Find Operational Plan  plan_list=${plan_list}    resource_type=STAND                                                 |
    """
    plan = next(
        filter(
            lambda plan: plan["operational"] and resource_type in plan["resourceTypes"],
            plan_list,
        ),
        None,
    )

    if plan is None:
        raise ValueError(f"No FRMS operational plan with resource type {resource_type}")

    return plan
