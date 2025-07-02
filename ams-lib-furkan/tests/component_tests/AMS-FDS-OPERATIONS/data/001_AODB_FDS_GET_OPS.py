from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)

generic_context = {
    "customer_id": None,
    "ref_airport": None,
    "ref_airport_full": None,
    "apt_correlation_id": f"regression{Gad.generate_correlation_id(9)}",
}


test_context = {
    "token_type": "COOKIE",
    "generic_context": generic_context,
    "user_context": {"mode": "local"},
}
