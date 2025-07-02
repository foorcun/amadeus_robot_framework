import logging
from datetime import datetime

LOGGER = logging.getLogger(__name__)


def fom_find_visit_in_flights(flights, airline_code, flight_number):

    # TODO VC: check date, arrival/departure

    flight = next(
        filter(
            lambda flight: flight["inboundMovement"]["airline"]["value"] == airline_code
            and str(flights[0]["inboundMovement"]["flightNumber"]["value"])
            == flight_number,
            flights,
        ),
        None,
    )

    if flight is None:
        raise ValueError(
            f"Flight {airline_code} {flight_number} not found in list of flights {flights}"
        )

    LOGGER.info("Flight: %s", flight)

    return flight


def fom_find_allocations_in_flight(flight, resource_type):
    """
    Finds all allocations for a given flight and resource type.

    | *Arguments*                      | *Description*                                                 |
    | ``flight``                       | The flight data containing allocations                        |
    | ``resource_type``                | The type of the resource to find (e.g., 'STAND', 'GATE'...)   |

    === Usage: ===
    | fom_find_allocations    flight={flight}  resource_type=STAND
    """
    if resource_type == "GATE":
        resource_type = "PASSENGER_GATE"

    return list(
        filter(
            lambda allocation: allocation.get("resourceType") == resource_type,
            flight.get("resource", []),
        )
    )


def fom_find_timing(timings, time_type, qualifier):
    """
    Finds a specific timing in a list of timings based on type and qualifier.

    | *Arguments*                      | *Description*                                                 |
    | ``timings``                      | List of timing objects                                        |
    | ``time_type``                    | Type of the timing (e.g., 'SCT', 'EST')                       |
    | ``qualifier``                    | Qualifier for the timing (e.g., 'ONB', 'OFB', 'ALST', 'ALET') |

    === Usage: ===
    | fom_find_timing    timings={timings}  time_type=SCT  qualifier=ALST
    """
    timing = next(
        filter(
            lambda timing: timing.get("timeType") == time_type
            and timing.get("operationQualifier", timing.get("qualifier")) == qualifier,
            timings,
        ),
        None,
    )
    if timing:
        if isinstance(timing["value"], str):
            value = timing["value"]
        else:
            value = timing["value"]["time"]
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    return None
