import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)
from ams.data_model.common_libs.utils import generic_helpers as helpers
from ams.data_model.common_libs.utils.request_helpers import (
    _pre_process_payload_date_data,
)
from .input_builder import _update_leg_period_context


LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument, unused-variable, protected-access, too-many-locals


@RestInjector
def injector(kwargs, session_key):

    context_data = session_manager.sessions._get_session_context_data()

    payload_input_data = kwargs["leg_data"]
    _pre_process_payload_date_data(payload_input_data)

    LOGGER.debug("Payload input data for post leg periods is : %s", payload_input_data)

    gen_payload = PayloadGenerator(
        payload_input_data, "leg_period_manual.jinja", __file__
    )

    payload = gen_payload.construct_generic_payload()

    params = {
        "refAirport": context_data["test_context"]["generic_context"][
            "ref_airport_full"
        ]
    }

    rest_details = {
        "operation": "POST",
        "params": params,
        "path": context_data["end_points"]["vip"]["leg_periods_manual"],
        "data": payload,
        "expected_status_code": kwargs.get("expected_response_code", "200"),
        "verify": False,
    }

    LOGGER.debug("REST Details: %s", rest_details)

    return rest_details
