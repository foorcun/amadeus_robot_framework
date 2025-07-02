"""
Module contains function to verify the response schema of get leg period API call.
"""

from json import JSONDecodeError
import logging
import jmespath
from protocols import session_manager
from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
)
from ams.fom_api_calls.visit_api.get_movement_id.input_builder import create_movement_id

from ams.data_model.common_libs.utils.date_handler import get_dates_between

LOGGER = logging.getLogger(__name__)


# def validate_get_leg_period_response_schema_ok(response):
#     """
#     Validates the response schema of get leg period API call.

#     | *Arguments*                | *Description*                                                  |

#     | ``response``               | response object from call to 'Get Leg Periods' keyword         |


#     === Usage: ===
#     | Validate Get Leg Period Response Schema    response=${response}

#     """
#     response_json = response.json()
#     schema_name = "get_leg_period_response_schema.json"

#     try:
#         load_and_validate_response_schema(__file__, schema_name, response_json)
#     except JSONDecodeError as e:
#         LOGGER.warning("There is no JSON object in the response: %s", e)


# def _update_leg_period_details(response):
#     """

#     Updates the context file from details in the Get Legperiods response.
#     Stores legtype,dates of operations and id(eg: "ARL_MA$2454$$APT_GYD$APT_XYZ$2025-03-20$2025-03-30$1234567$arrival$0").

#     | *Arguments*                | *Description*                                                  |

#     | ``response``               | response object from call to 'Get Leg Periods' keyword         |

#     === Usage: ===
#     |    _Update_Leg_Period_Details       response=${response}        |


#     """
#      context_data = session_manager.sessions._get_session_context_data()
# id_value = jmespath.search("content[0].id", response)

# if (
#     not context_data.get("test_context", {})
#     .get("vip_context", {})
#     .get("leg_period_context", {})
#     .get("id_list")
# ):
#     context_data["test_context"]["vip_context"]["leg_period_context"][
#         "id_list"
#     ] = []

# context_data["test_context"]["vip_context"]["leg_period_context"]["id_list"].append(
#     id_value
# )

# LOGGER.debug(
#     "The stored ID is : %s",
#     context_data.get("test_context", {})
#     .get("vip_context", {})
#     .get("leg_period_context", {})
#     .get("id_list"),
# )
#     parts = id_value.split("$")
#     leg_type = parts[-2].upper()
#     context_data["test_context"]["vip_context"]["leg_period_context"][
#         "leg_type"
#     ] = leg_type
#     start_date = parts[5].replace("-", "")
#     end_date = parts[6].replace("-", "")
#     op_dates = get_dates_between(start_date, end_date)
#     context_data["test_context"]["vip_context"]["leg_period_context"][
#         "op_dates"
#     ] = op_dates


# def validate_leg_period_response_and_create_movement_id(response):
#     """
#     Validates the Get leg period response and constructs the movement ID

#     | *Arguments*                | *Description*                                                  |

#     | ``response``               | response object from call to 'Get Leg Periods' keyword         |

#     === Usage: ===
#         Validate Leg Period Response And Retrieve Movement Id       response=${response}        |
#     """
#     validate_get_leg_period_response_schema_ok(response)
#     _update_leg_period_details(response.json())
#     create_movement_id()
