"""
Module contains function to verify the response schema of create leg period API call.
"""

import logging
from json import JSONDecodeError
import jmespath
from protocols import session_manager

# pylint: disable=line-too-long

from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
    validate_general_processing,
)

# pylint: disable = protected-access
LOGGER = logging.getLogger(__name__)


def validate_inbound_or_outbound_flight_response_schema(response):
    """
    Validates the response schema of Create Inbound Or Outbound Flight API call.

    | *Arguments*                | *Description*                                                                  |

    | ``response``               | response object from call to 'Create Inbound Or Outbound Flight' keyword       |


    === Usage: ===
    | Validate Inbound or Outbound Flight Response Schema    response=${response}
    """
    response_json = response.json()
    schema_name = "inbound_or_outbound_flight_response_schema.json"

    try:
        load_and_validate_response_schema(__file__, schema_name, response_json)
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)


def validate_inbound_or_outbound_flight_general_processing(response, status="OK"):
    """
    Validates the general processing status of Create Inbound Or Outbound Flight API call.

    | *Arguments*                | *Description*                                                                      |

    | ``response``               | response object from call to 'Create Inbound Or Outbound Flight' keyword           |
    | ``status``                 | expected general processing status                                                 |


    === Usage: ===
    | Validate Inbound or Bound Flight General Processing    response=${response}
    """
    validate_general_processing(response, status)


def get_flight_details(response, key):
    """
    Get flight details from the given response based on the provided key.

    |  *Arguments*                | *Description*                                       |
    |  ``response``               | The response dictionary containing flight details.  |
    |  ``key``                    | The key to check in the response.                   |

    === Usage: ===
    |  Get Flight Details    response_json=${response_json}   key=${key}
    """
    response_json = response.json()
    results = []
    expressions = [
        f"content[].content[].inboundMovement.{key}",
        f"content[].content[].outboundMovement.{key}",
        f"content[0].content[].{key}",
        f"content[].{key}",
    ]

    context_data = session_manager.sessions._get_session_context_data()
    for expression in expressions:
        result = jmespath.search(expression, response_json)
        if result:
            results.extend(result)

    if key == "id":
        context_data["test_context"]["fom_context"]["movement_context"][
            "movement_ids"
        ] = results

    return results


def get_flight_details_from_json(response, key):
    """
    Get the value for the given key from the response object

    This function supports both list and dict response formats:
      - If the response is a list, it expects the first element to have a "content" key.
      - If the response is a dict, it expects a "content" key at the top level.

    |  *Arguments*                | *Description*                                       |
    |  ``response``               | The response (list or dict) containing flight details.|
    |  ``key``                    | The key to extract from the first content object.   |

    === Usage: ===
    |  Get Flight Details From Json    response=${response}   key=${key}

    === Returns: ===
    | Any | The value for the given key from the first object in the content list, or None if not found.
    """
    # Handle list response
    if isinstance(response, list) and response and "content" in response[0]:
        content_list = response[0]["content"]
        if content_list and isinstance(content_list, list):
            return content_list[0].get(key)
    # Handle dict response
    elif isinstance(response, dict) and "content" in response:
        content_list = response["content"]
        if content_list and isinstance(content_list, list):
            return content_list[0].get(key)
    return None
