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

    LOGGER.debug("The context data is : %s", context_data)

    expected_response_code = kwargs.get("expected_response_code", "200")
    endpoint_type = kwargs.get("endpoint_type", "movement")
    query_param = helpers.build_query_param_string(kwargs.get("additional_params"))

    movement_id = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("movement_ids")[0]
        if context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("movement_ids")
        else kwargs.get("movement_id")
    )

    if not movement_id:
        LOGGER.debug("Movement ID not present")
        raise ValueError(
            "Movement ID neither given by user nor present in the context file"
        )

    endpoint = None

    movement_endpoints = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("visits", {})
        .get(endpoint_type)
    )
    endpoint = movement_endpoints.replace(" ", "") + "-" + movement_id.replace(" ", "")
    print(endpoint)

    LOGGER.debug("Endpoint identified as: %s", endpoint)

    rest_details = {
        "operation": "GET",
        "params": query_param,
        "path": endpoint,
        "expected_status_code": expected_response_code,
        "verify": False,
    }

    LOGGER.debug("Get Movement Id REST Details: %s", rest_details)

    return rest_details
