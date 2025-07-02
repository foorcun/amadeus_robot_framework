"""Module to construct movement ID from VIP response"""

import logging
from protocols import session_manager
from ams.mdm_api_calls.airport.get_airport.injector import get_airport_details
from ams.mdm_api_calls.airline.get_airline.injector import get_airline_details
from ams.mdm_api_calls.airport.get_airport.responses import get_airport_icao_code
from ams.mdm_api_calls.airline.get_airline.responses import get_airline_icao_code

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long,protected-access


def _get_icao_codes():
    """
    This function retrieves the ICAO codes of our airline and airport
    """
    context_data = session_manager.sessions._get_session_context_data()
    airport_code = (
        context_data.get("test_context").get("generic_context").get("ref_airport")
    )

    arl_code = (
        context_data.get("test_context")
        .get("vip_context")
        .get("leg_period_context")
        .get("airlineCode")
    )

    airport_details = get_airport_details(
        endpoint_type="byCode",
        additional_params={"code": airport_code},
    )

    airline_details = get_airline_details(endpoint_type="list")

    airline_icao = get_airline_icao_code(airline_details.json(), iata_code=arl_code)
    airport_icao = get_airport_icao_code(airport_details.json())

    context_data["test_context"]["sds_context"]["airline_context"][
        "airline_icao_code"
    ] = airline_icao
    context_data["test_context"]["sds_context"]["airport_context"][
        "airport_icao_code"
    ] = airport_icao


def create_movement_id():
    """
    This function constructs the valid movement ids and stores inside the context file.

    === Usage:  ===
    | Create Movement Id                                                    |

    """
    context_data = session_manager.sessions._get_session_context_data()
    movement_ids = []
    _get_icao_codes()

    airline_icao = (
        context_data.get("test_context", {})
        .get("sds_context", {})
        .get("airline_context", {})
        .get("airline_icao_code")
    )
    airport_icao = (
        context_data.get("test_context", {})
        .get("sds_context", {})
        .get("airport_context", {})
        .get("airport_icao_code")
    )
    flight_num = (
        context_data.get("test_context", {})
        .get("vip_context", {})
        .get("leg_period_context", {})
        .get("flightNumber")
    )

    op_dates = context_data["test_context"]["vip_context"]["leg_period_context"][
        "op_dates"
    ]
    leg_type = context_data["test_context"]["vip_context"]["leg_period_context"][
        "leg_type"
    ]

    LOGGER.debug(op_dates)

    for date_of_operation in op_dates:
        movement_id = f"C_{airline_icao}_{flight_num}__{date_of_operation}_{leg_type}_{airport_icao}"
        movement_ids.append(movement_id)
    context_data["test_context"]["fom_context"]["movement_context"][
        "movement_ids"
    ] = movement_ids
