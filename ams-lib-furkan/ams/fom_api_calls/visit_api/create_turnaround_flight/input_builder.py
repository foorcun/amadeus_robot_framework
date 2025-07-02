"""
This module contains function to help building the input payload data for Create Turnaround Flight Call
"""

import random
from protocols import session_manager
from ams.mdm_api_calls.aircraft.get_aircraft.injector import get_aircraft_type_details
from ams.mdm_api_calls.aircraft.get_aircraft.responses import (
    get_valid_aircraft_type_period_details,
)


# pylint:disable=protected-access,line-too-long
def _update_create_turnaround_flight_context(ref_airport):
    """
    Updates the arrivalAirport,refAirport, aircraftType and registration in Create Turnaround Flight Context for FOM.

    Args:
        ref_airport : The ref airport from generic_context
    """
    context_data = session_manager.sessions._get_session_context_data()
    context_data["test_context"]["fom_context"]["create_turnaround_flight_context"][
        "InarrivalAirport"
    ] = ref_airport
    context_data["test_context"]["fom_context"]["create_turnaround_flight_context"][
        "OutdepartureAirport"
    ] = ref_airport

    all_aircraft_details_response = get_aircraft_type_details(
        endpoint_type="aircraftType"
    )
    all_valid_aircraft_period_details = get_valid_aircraft_type_period_details(
        all_aircraft_details_response.json()
    )
    context_data["test_context"]["fom_context"]["create_turnaround_flight_context"][
        "InaircraftType"
    ] = random.choice(all_valid_aircraft_period_details)["id"]
