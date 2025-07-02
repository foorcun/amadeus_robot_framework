"""
REST injector
"""

import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.fom_api_calls.movement_api.create_inbound_outbound_flight.input_builder import (
    _update_create_flight_context,
)
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)
from ams.data_model.common_libs.utils import generic_helpers as helpers
from .input_builder import _update_payload


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
    jinja_template = "post_inbound_or_outbound_flight.jinja"

    LOGGER.debug("Context Data: %s", context_data)

    expected_response_code = kwargs.get("expected_response_code")
    endpoint_type = kwargs.get("endpoint_type", "adhoc")

    ref_airport = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("ref_airport_full", "")
    )

    _update_create_flight_context(ref_airport)

    additional_param = {"refAirport": ref_airport}

    query_param = helpers.build_query_param_string(
        kwargs.get("additional_params", additional_param), return_type="dict"
    )

    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("movements", {})
        .get(endpoint_type)
    )
    leg_type = kwargs.get("type", "ARRIVAL")

    LOGGER.debug("Endpoint identified as: %s", fom_endpoint)

    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("create_flight_context")
    )
    flight_info = _update_payload(payload_input_data, leg_type)

    LOGGER.debug(
        "Payload input data for Inbound or Outbound Flight is : %s", payload_input_data
    )
    gen_payload = PayloadGenerator(flight_info, jinja_template, __file__)
    payload = gen_payload.construct_generic_payload()

    rest_details = {
        "operation": "POST",
        "params": query_param,
        "path": fom_endpoint,
        "data": payload,
        "expected_status_code": expected_response_code,
        "verify": False,
    }

    LOGGER.debug("Create Inbound or Outbound Flight REST Details: %s", rest_details)

    return rest_details
