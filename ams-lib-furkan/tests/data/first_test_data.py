from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from ams.data_model.common_libs.utils.date_handler import get_date


period_start = get_date(days=0, time_format="12:00", date_format="%Y-%m-%dT%H:%M:%S")
period_end = get_date(days=90, time_format="13:12", date_format="%Y-%m-%dT%H:%M:%S")

generic_context = {
    "customer_id": "AITA-GENR",
    "ref_airport": "XYZ",
    "ref_airport_full": "APT_CUST_XYZ",
    "apt_correlation_id": f"regression{Gad.generate_correlation_id(9)}",
}
leg_period_context = {
    "params": {"refAirport": generic_context.get("ref_airport_full")},
    "customerId": generic_context.get("customer_id"),
    "airlineCode": Gad.generate_airline_code("AB", 6),
    "flightNumber": Gad.generate_flight_number(4),
    "arrivalAirport": generic_context.get("ref_airport_full"),
    "aircraftType": "ACT002409",
    "departureAirport": "NDK",
    "depPeriodDaysOfOp": "1234567",
    "arrPeriodDaysOfOp": "1234567",
    "startOfDeparturePeriod": period_start,
    "endOfDeparturePeriod": period_end,
    "startOfArrivalPeriod": period_start,
    "endOfArrivalPeriod": period_end,
    "serviceType": "J",
}


test_context = {
    "token_type": "COOKIE",
    "generic_context": generic_context,
    "leg_period_context": leg_period_context,
    "user_context": {"mode": "local"},
}
