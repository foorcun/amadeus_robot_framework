# pylint:disable=line-too-long

"""
This module contains function to help building the input payload data for create leg period API POST call
"""

import logging
import random
from protocols import session_manager
from ams.mdm_api_calls.aircraft.get_aircraft.injector import get_aircraft_type_details
from ams.mdm_api_calls.aircraft.get_aircraft.responses import (
    get_valid_aircraft_type_period_details,
)

LOGGER = logging.getLogger(__name__)


def _update_leg_period_context(ref_airport):
    """
    Updates the arrivalAirport, customerId and refAirport in VIP leg period context
    """
    context_data = session_manager.sessions._get_session_context_data()
    context_data["test_context"]["vip_context"]["leg_period_context"]["params"][
        "refAirport"
    ] = ref_airport
    context_data["test_context"]["vip_context"]["leg_period_context"][
        "arrivalAirport"
    ] = ref_airport
    context_data["test_context"]["vip_context"]["leg_period_context"]["customerId"] = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id")
    )

    all_aircraft_details_response = get_aircraft_type_details(
        endpoint_type="aircraftType"
    )
    all_valid_aircraft_period_details = get_valid_aircraft_type_period_details(
        all_aircraft_details_response.json()
    )
    context_data["test_context"]["vip_context"]["leg_period_context"][
        "aircraftType"
    ] = random.choice(all_valid_aircraft_period_details)["id"]
