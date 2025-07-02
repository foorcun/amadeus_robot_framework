"""
This module contains function to help building the input payload data for Update leg period API
"""

from protocols import session_manager
from ams.mdm_api_calls.aircraft.get_aircraft.responses import (
    get_valid_aircraft_rego_and_type_mapping,
)
from ams.mdm_api_calls.aircraft.get_aircraft.injector import get_aircraft_details

# pylint: disable=unused-argument, unused-variable, protected-access


@staticmethod
def _update_payload(payload_input_data, leg_type):
    """
    Update payload using the provided input data and type.
    Args:
        payload_input_data (dict): The input data for the payload.
        leg_type (str): Arrival or departure type.
    Returns:
        dict: The constructed generic payload.
    """
    context_data = session_manager.sessions._get_session_context_data()

    # Ensure the type key is updated correctly
    payload_input_data["type"] = leg_type

    match leg_type:
        case "ARRIVAL":
            payload_input_data.update(
                {
                    "arrivalAirport": context_data.get("test_context", {})
                    .get("generic_context", {})
                    .get("ref_airport_full", ""),
                    "departureAirport": "APT_HEL",
                }
            )
        case "DEPARTURE":
            payload_input_data.update(
                {
                    "arrivalAirport": "APT_HEL",
                    "departureAirport": context_data.get("test_context", {})
                    .get("generic_context", {})
                    .get("ref_airport_full", ""),
                }
            )

    return payload_input_data


def _update_create_flight_context(ref_airport):
    """
    Updates the arrivalAirport,refAirport, aircraftType and registration in Create Flight Context for FOM.

    Args:
        ref_airport : The ref airport from generic_context
    """
    context_data = session_manager.sessions._get_session_context_data()
    context_data["test_context"]["fom_context"]["create_flight_context"]["params"][
        "refAirport"
    ] = ref_airport
    context_data["test_context"]["fom_context"]["create_flight_context"][
        "arrivalAirport"
    ] = ref_airport

    all_aircraft_details_response = get_aircraft_details()
    response = get_valid_aircraft_rego_and_type_mapping(
        all_aircraft_details_response.json()
    )
    context_data["test_context"]["fom_context"]["create_flight_context"][
        "aircraftType"
    ] = response.get("aircraftTypeId")
    context_data["test_context"]["fom_context"]["create_flight_context"][
        "registration"
    ] = response.get("registrationId")
