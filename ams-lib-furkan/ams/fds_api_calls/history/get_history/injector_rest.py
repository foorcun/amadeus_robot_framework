"""
REST injector
"""

import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.utils import generic_helpers as helpers

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access


@RestInjector
def injector(kwargs, session_key="defaultKey"):
    """
    REST injector

    # arguments can be passed from the main injector.py
    arg1 = kwargs["args1"]
    arg2 = kwargs["args2"]
    """

    context_data = session_manager.sessions._get_session_context_data()
    expected_response_code = kwargs.get("expected_response_code", "200")
    endpoint_type = kwargs.get("endpoint_type", "deltaMovements")
    movement_id = kwargs.get("movement_id")
    query_param = helpers.build_query_param_string(
        {
            **{
                "customerId": context_data.get("test_context", {})
                .get("generic_context", {})
                .get("customer_id")
            },
            **(kwargs.get("additional_params", {}) or {}),
        }
    )
    LOGGER.debug("The query param for history ops is : %s", query_param)
    endpoint = None

    fds_endpoints = context_data.get("end_points", {}).get("fds")
    endpoint = f"{fds_endpoints.get(endpoint_type)}/{movement_id}"

    LOGGER.debug("Endpoint identified for history as: %s", endpoint)

    rest_details = {
        "operation": "GET",
        "params": query_param,
        "path": endpoint,
        "expected_status_code": expected_response_code,
        "verify": False,
    }

    LOGGER.debug("REST Details for the FDS history call: %s", rest_details)

    return rest_details
