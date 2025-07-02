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
    endpoint_type = kwargs.get("endpoint_type", "list")

    query_param = helpers.build_query_param_string(
        kwargs.get("additional_params", None)
    )

    endpoint = None

    delay_endpoint = context_data.get("end_points", {}).get("mdm", {}).get("delay", {})
    endpoint = delay_endpoint.get(endpoint_type)

    LOGGER.debug("Endpoint identified as: %s", endpoint)

    rest_details = {
        "operation": "GET",
        "params": query_param,
        "path": endpoint,
        "expected_status_code": expected_response_code,
        "verify": False,
    }

    LOGGER.debug("REST Details for Delay: %s", rest_details)

    return rest_details
