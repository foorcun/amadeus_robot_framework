import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)
from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from ams.data_model.common_libs.utils import generic_helpers as helpers
from .input_builder import (
    _add_equipment_connection,
    _add_gate_connection,
    _add_security_level,
)

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access, line-too-long, too-many-locals


@RestInjector
def injector(kwargs, session_key):
    context_data = session_manager.sessions._get_session_context_data()
    create_stand_template = "create_stand.jinja"

    expected_response_code = kwargs.get("expected_response_code")
    endpoint_type = kwargs.get("endpoint_type", "stand")
    name = kwargs.get("name", f"ROBOT_Stand{Gad.generate_correlation_id(3)}")
    stand_type = kwargs.get("type")
    allowed_arrival_sec_level = kwargs.get("arrival_security_level")
    allowed_departure_sec_level = kwargs.get("departure_security_level")

    query_param = helpers.build_query_param_string(
        kwargs.get("additional_params", None)
    )

    endpoint = None
    stand_endpoints = context_data.get("end_points", {}).get("mdm").get("stand", {})
    endpoint = stand_endpoints.get(endpoint_type)

    LOGGER.debug("Endpoint identified as: %s", endpoint)

    # fetch customer_id from the context data

    customer_id = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id", "")
    )

    # fetch payload input data from the context data

    payload_input_data = context_data.get("test_context", {}).get(
        "create_stand_context"
    )

    # update customer id & payload input data with the values passed in the test

    payload_input_data["customer_id"] = customer_id
    payload_input_data.update(
        {
            key: value
            for key, value in {"name": name, "periods_type": stand_type}.items()
            if value
        }
    )

    # for allowed security level

    _add_security_level(
        payload_input_data,
        allowed_arrival_sec_level or None,
        allowed_departure_sec_level or None,
    )

    # sanitization of gate/equipment connections if passed any through data file

    for key in [
        "connections_gateDirectionalConnection",
        "connections_equipmentConnection",
    ]:
        payload_input_data.pop(key, None)

    # for gate connection

    if kwargs.get("gate_connection") == "YES":
        if not kwargs.get("gate_id"):
            raise ValueError(
                "If 'gate_connection' is 'YES', 'gate_id' must also be provided."
            )

        _add_gate_connection(payload_input_data, kwargs.get("gate_id"))

    # for equipment connection

    if kwargs.get("equipment_connection") == "YES":
        if not kwargs.get("equipment_type"):
            raise ValueError(
                "If 'equipment_connection' is 'YES', 'equipment_type' must also be provided."
            )
        _add_equipment_connection(payload_input_data, kwargs.get("equipment_type"))

    LOGGER.debug("Payload input data for create stand is : %s", payload_input_data)

    # payload generation

    gen_payload = PayloadGenerator(payload_input_data, create_stand_template, __file__)
    payload = gen_payload.construct_generic_payload()

    rest_details = {
        "operation": "POST",
        "params": query_param,
        "path": endpoint,
        "data": payload,
        "expected_status_code": expected_response_code,
        "verify": False,
    }

    LOGGER.debug("REST Details for create stand: %s", rest_details)

    return rest_details
