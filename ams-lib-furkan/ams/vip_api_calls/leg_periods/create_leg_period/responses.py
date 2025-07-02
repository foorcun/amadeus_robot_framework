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


# def validate_create_leg_period_response_schema(response):
#     """
#     Validates the response schema of create leg period API call.

#     | *Arguments*                | *Description*                                                                  |

#     | ``response``               | response object from call to 'Create Manual Source Leg Period' keyword         |


#     === Usage: ===
#     | Validate Create Leg Period Response Schema    response=${response}

#     """
#     response_json = response.json()
#     schema_name = "create_leg_period_response_schema.json"

#     try:
#         load_and_validate_response_schema(__file__, schema_name, response_json)
#     except JSONDecodeError as e:
#         LOGGER.warning("There is no JSON object in the response: %s", e)


# def validate_create_leg_period_general_processing(response, status="OK"):
#     """
#     Validates the general processing status of create leg period API call.

#     | *Arguments*                | *Description*                                                                      |

#     | ``response``               | response object from call to 'Create Manual Source Leg Period' keyword             |
#     | ``status``                 | expected general processing status                                                 |


#     === Usage: ===
#     | Validate Create Leg Period General Processing    response=${response}                |
#     """
#     validate_general_processing(response, status)


# def validate_create_leg_period_response(response, status="OK"):
#     """
#     Validates the general processing status and the schema response of the create leg period API call.

#     | *Arguments*               | *Description*                                                                       |

#     | ``response``              | Response object from call to 'Create Manual Source Leg Period' keyword              |
#     | ``status``                | Expected general processing status. Default is "OK"                                 |


#     === Usage: ===
#     | Validate Create Leg Period Response       response=${response}        status=OK           |
#     | Validate Create Leg Period Response       response=${response}                            |
#     """
#     validate_create_leg_period_general_processing(response, status)
#     validate_create_leg_period_response_schema(response)
