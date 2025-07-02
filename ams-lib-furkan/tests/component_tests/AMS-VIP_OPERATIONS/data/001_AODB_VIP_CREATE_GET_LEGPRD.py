# pylint: disable="line-too-long"

"""
This script sets up the context for testing the creation and retrieval of leg period details from the AODB VIP system.
Modules:
    ams.data_model.common_libs.utils.airport_data_generator: Provides utilities for generating airport data.
    ams.data_model.common_libs.utils.date_handler: Provides utilities for handling dates.
Variables:
    period_start (str): The start date and time for the period in the format "%Y-%m-%dT%H:%M:%S".
    period_end (str): The end date and time for the period in the format "%Y-%m-%dT%H:%M:%S".
    generic_context (dict): Contains generic context information for the test, including:
        - customer_id (str): The customer identifier.
        - ref_airport (str): The reference airport code.
        - ref_airport_full (str): The full reference airport identifier.
        - apt_correlation_id (str): A unique correlation identifier generated for the test.
    leg_period_context (dict): Contains the context specific to the leg period, including:
        - params (dict): Parameters for the leg period, including the reference airport.
        - customerId (str): The customer identifier.
        - airlineCode (str): The airline code.
        - flightNumber (str): The flight number.
        - arrivalAirport (str): The arrival airport code.
        - aircraftType (str): The aircraft type.
        - departureAirport (str): The departure airport code.
        - depPeriodDaysOfOp (str): Days of operation for the departure period.
        - arrPeriodDaysOfOp (str): Days of operation for the arrival period.
        - startOfDeparturePeriod (str): The start date and time for the departure period.
        - endOfDeparturePeriod (str): The end date and time for the departure period.
        - startOfArrivalPeriod (str): The start date and time for the arrival period.
        - endOfArrivalPeriod (str): The end date and time for the arrival period.
        - serviceType (str): The service type.
    test_context (dict): Contains the test-specific context, including:
        - token_type (str): The type of token used for authentication.
        - generic_context (dict): The generic context information.
        - leg_period_context (dict): The leg period context information.
        - user_context (dict): The user-specific context, including the mode of operation.
"""

from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from ams.data_model.common_libs.utils.date_handler import get_date


period_start = get_date(days=0, time_format="12:00", date_format="%Y-%m-%dT%H:%M:%S")
period_end = get_date(days=1, time_format="13:12", date_format="%Y-%m-%dT%H:%M:%S")

generic_context = {
    "customer_id": None,
    "ref_airport": None,
    "ref_airport_full": None,
    "apt_correlation_id": f"regression{Gad.generate_correlation_id(9)}",
}
leg_period_context = {
    "params": {"refAirport": None},
    "customerId": None,
    "airlineCode": Gad.get_iata_airline_code(),
    "flightNumber": Gad.generate_flight_number(4),
    "arrivalAirport": None,
    "aircraftType": None,
    "departureAirport": "APT_GYD",
    "depPeriodDaysOfOp": "1234567",
    "arrPeriodDaysOfOp": "1234567",
    "startOfDeparturePeriod": period_start,
    "endOfDeparturePeriod": period_end,
    "startOfArrivalPeriod": period_start,
    "endOfArrivalPeriod": period_end,
    "serviceType": "J",
}

movement_context = {
    "flight_op_status_update": {
        "timeType": "ACT",
        "operationQualifier": "CNL",
        "time": "time",
        "value": "DX",
        "dataElement": [],
    },
}

# VIP context configuration
vip_context = {"leg_period_context": leg_period_context}

# FOM context configuration
fom_context = {"movement_context": movement_context}

# Airline context configuration
airline_context = {}

# Airport context configuration
airport_context = {}

# SDS context configuration
sds_context = {"airline_context": airline_context, "airport_context": airport_context}

# Test context configuration
test_context = {
    "token_type": "COOKIE",
    "generic_context": generic_context,
    "vip_context": vip_context,
    "fom_context": fom_context,
    "sds_context": sds_context,
    "user_context": {"mode": "local"},
}
