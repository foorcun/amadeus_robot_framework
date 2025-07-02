"""
Usage:
Run this script directly to initialize the AMS session and perform the API calls.
"""

import os
from ams.initalize_ams_test.injector import open_generic_ams_session
from ams.vip_api_calls.leg_periods.get_leg_period.injector import (
    fetch_leg_periods,
)
from ams.vip_api_calls.leg_periods.create_leg_period.injector import (
    create_manual_source_leg_period,
)
from tests.data.first_test_data import test_context


if __name__ == "__main__":
    print(test_context)
    open_generic_ams_session(
        protocol="REST",
        environment="INT",
        current_directory=os.curdir,
        test_name="first_test_data",
    )
    post_response = create_manual_source_leg_period(
        expected_response_code=200,
        params={"refAirport": "APT_CUST_XYZ"},
    )
    get_response = fetch_leg_periods(
        expected_response_code=200,
        default_params="flightNumber,customerId",
        additional_params={"adhocFlag": "MIXED"},
        type="all",
    )
