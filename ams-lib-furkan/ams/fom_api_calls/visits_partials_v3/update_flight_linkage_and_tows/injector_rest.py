"""
REST injector
"""

import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.utils import generic_helpers as helpers
from ams.data_model.common_libs.request_response_handler.request_generator import (
    LOGGER,
    PayloadGenerator,
)
from ams.fom_api_calls.visits_partials_v3.update_flight_linkage_and_tows.input_builder import (
    _add_link,
    _add_tows_operation,
    _unlink_operation,
)

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
    expected_response_code = kwargs.get("expected_response_code")
    endpoint_type = kwargs.get("endpoint_type", "partials")

    query_param = helpers.build_query_param_string(kwargs.get("additional_params"))

    movement_id = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("movement_id")
        if context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("movement_id")
        else kwargs.get("movement_id")
    )
    if not movement_id:
        LOGGER.debug("Movement ID not present")
        raise ValueError("Movement ID neither present in context nor given by user.")

    LOGGER.debug("Movement %s", movement_id)
    op_type = kwargs.get("op_type")
    endpoint = None
    movement_endpoints = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("visits", {})
        .get(endpoint_type)
    )
    endpoint = movement_endpoints + "-" + movement_id
    payload = None

    match op_type:
        case "link":
            payload = _add_link(kwargs, context_data, PayloadGenerator)
        case "unlink":
            payload = _unlink_operation(kwargs, context_data, PayloadGenerator)
        case "update_flight_tows":
            payload = _add_tows_operation(kwargs, context_data, PayloadGenerator)

    rest_details = {
        "operation": "PUT",
        "params": query_param,
        "path": endpoint,
        "data": payload,
        "expected_status_code": expected_response_code,
        "verify": False,
    }

    LOGGER.debug("Update Flight REST Details: %s", rest_details)
    return rest_details
