"""
Module contains function to verify the response schema of create stand API call.
"""

from json import JSONDecodeError
import logging
from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
)

LOGGER = logging.getLogger(__name__)


def validate_create_stand_response_schema(response):
    """
    Validates the response schema of get leg period API call.

    | *Arguments*                | *Description*                                               |

    | ``response``               | response object from call to 'Create Stand' keyword         |


    === Usage: ===
    | Validate Create Stand Response Schema    response=${response}

    """
    response_json = response.json()
    schema_name = "create_stand_response_schema.json"

    try:
        load_and_validate_response_schema(__file__, schema_name, response_json)
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)
