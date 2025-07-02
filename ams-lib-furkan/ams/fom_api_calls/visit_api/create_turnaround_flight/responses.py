"""
Module contains function to verify the response schema of create leg period API call.
"""

# pylint: disable=line-too-long

from json import JSONDecodeError
import logging
from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
    validate_general_processing,
)

LOGGER = logging.getLogger(__name__)


def validate_turn_around_flight_response_schema(response):
    """
    Validates the response schema of Create Turnaround Flight API call.

    | *Arguments*                | *Description*                                                           |

    | ``response``               | response object from call to 'Create Turnaround Flight' keyword         |


    === Usage: ===
    | Validate Turn Around Flight Response Schema    response=${response}
    """
    response_json = response.json()
    schema_name = "turn_around_flight_response_schema.json"

    try:
        load_and_validate_response_schema(__file__, schema_name, response_json)
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)


def validate_turn_around_flight_general_processing(response, status="OK"):
    """
    Validates the general processing status of Create Turnaround Flight API call.

    | *Arguments*                | *Description*                                                               |

    | ``response``               | response object from call to 'Create Turnaround Flight' keyword             |
    | ``status``                 | expected general processing status                                          |


    === Usage: ===
    | Validate Turn Around Flight General Processing     response=${response}
    """
    validate_general_processing(response, status)
