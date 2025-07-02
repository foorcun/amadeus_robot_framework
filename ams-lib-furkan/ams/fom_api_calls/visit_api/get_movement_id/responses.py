from json import JSONDecodeError
import logging
import jmespath
from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
)


LOGGER = logging.getLogger(__name__)


def validate_visit_movement_response(response):
    """
    Validates the response schema of Get Movement ID call.

    | *Arguments*                | *Description*                                                  |

    | ``response``               | response object from call to 'Get Movement ID Details' keyword         |


    === Usage: ===
    | Validate Visit Movement Response      response=${response}                   |
    """

    message_text = jmespath.search(
        "generalErrorInformation[0].messageText", response.json()
    )
    if message_text == "No Visit found.":
        raise ValueError(
            "No visits found. Enter a movement ID present in the flight operations"
        )

    response_json = response.json()
    schema_name = "get_movement_response_schema.json"

    try:
        load_and_validate_response_schema(__file__, schema_name, response_json)
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)
