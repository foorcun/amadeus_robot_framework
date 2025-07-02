import protocols.broker

from ams.data_model.common_libs.utils.generic_helpers import add_data_to_clean_up
from ams.vip_api_calls.leg_periods.get_leg_period.injector import (
    find_leg_period,
    get_leg_periods,
)
from .injector_rest import injector as rest_injector

from json import JSONDecodeError
import logging
from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
    validate_general_processing,
)

LOGGER = logging.getLogger(__name__)


# pylint: disable=line-too-long
def create_manual_source_leg_period(leg_data):
    """
    Create leg period

    === Usage: ===
    | create_manual_source_leg_period

    """

    # create leg period
    args = {"leg_data": leg_data}
    response = protocols.broker.injector(args, "defaultKey", rest_injector)

    validate_general_processing(response, "OK")

    response_json = response.json()
    schema_name = "create_leg_period_response_schema.json"

    try:
        load_and_validate_response_schema(__file__, schema_name, response_json)
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)

    # check leg period has been created
    airline_code = leg_data["airlineCode"]
    flight_number = leg_data["flightNumber"]

    leg_periods = get_leg_periods(airline_code, flight_number)
    leg_period = find_leg_period(leg_periods, airline_code, flight_number)

    # cleanup
    add_data_to_clean_up("leg_period", leg_period["id"])

    return leg_period
