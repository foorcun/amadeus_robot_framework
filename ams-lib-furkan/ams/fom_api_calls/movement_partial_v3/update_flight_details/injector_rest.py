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


from .input_builder import (
    _update_aircraft_details,
    _update_alert,
    _update_delay,
    _update_disruption,
    _update_fids,
    _update_flight_op,
    _update_handling_agent,
    _update_load,
    _update_pax,
    _update_remarks,
    _update_resources,
    _update_tasks,
    _update_timing,
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
        .get("movements", {})
        .get(endpoint_type)
    )
    endpoint = movement_endpoints + "/" + movement_id
    payload = None

    match op_type:
        case "update_flight_time":
            payload = _update_timing(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case "disruption":
            payload = _update_disruption(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case "update_flight_alert":
            payload = _update_alert(kwargs, context_data, movement_id, PayloadGenerator)
        case "update_flight_op_status":
            payload = _update_flight_op(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case "update_flight_delay":
            payload = _update_delay(kwargs, context_data, movement_id, PayloadGenerator)
        case "update_flight_remarks":
            payload = _update_remarks(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case "update_flight_resources":
            payload = _update_resources(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case "update_flight_tasks":
            payload = _update_tasks(kwargs, context_data, movement_id, PayloadGenerator)
        case "update_flight_handling_agent":
            payload = _update_handling_agent(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case "update_flight_fids_details":
            payload = _update_fids(kwargs, context_data, movement_id, PayloadGenerator)
        case "update_flight_load_details":
            payload = _update_load(kwargs, context_data, movement_id, PayloadGenerator)
        case "update_flight_pax_details":
            payload = _update_pax(kwargs, context_data, movement_id, PayloadGenerator)
        case "update_flight_aircraft_details":
            payload = _update_aircraft_details(
                kwargs, context_data, movement_id, PayloadGenerator
            )
        case _:
            payload = None

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
