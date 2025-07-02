"""
This module contains the injector to get flight leg periods

"""

import protocols.broker
from .injector_rest import injector as rest_injector
import logging
from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
)
from json import JSONDecodeError

LOGGER = logging.getLogger(__name__)


# pylint: disable=line-too-long
def get_leg_periods(airline_code, flight_number):
    """
    Get leg periods

    | *Arguments*                       | *Description*                                                               |
    | ``airline_code``                  | airline code                                                                |
    | ``flight_number``                 | flight number                                                               |

    === Usage: ===
    | get_leg_periods    6X  123

    """

    response = protocols.broker.injector(
        {"airline_code": airline_code, "flight_number": flight_number},
        "defaultKey",
        rest_injector,
    )

    response_json = response.json()
    schema_name = "get_leg_period_response_schema.json"

    try:
        load_and_validate_response_schema(__file__, schema_name, response_json)
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)

    return response_json["content"]


def find_leg_period(leg_periods, airline_code, flight_number):

    leg_period = next(
        filter(
            lambda leg_period: leg_period["flight"]["airlineCode"] == airline_code
            and str(leg_period["flight"]["flightNumber"]) == flight_number,
            leg_periods,
        ),
        None,
    )

    if leg_period is None:
        raise ValueError(
            f"Leg period for flight {airline_code} {flight_number} not found in leg periods {leg_periods}"
        )

    return leg_period
