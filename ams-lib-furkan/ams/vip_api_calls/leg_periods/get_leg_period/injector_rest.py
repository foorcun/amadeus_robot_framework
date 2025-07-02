"""
REST injector
"""

import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.utils import generic_helpers as helpers
from ams.data_model.common_libs.utils.generic_helpers import (
    construct_default_params,
    construct_attributes,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument, unused-variable, protected-access, too-many-locals


@RestInjector
def injector(kwargs, session_key="defaultKey"):

    context_data = session_manager.sessions._get_session_context_data()

    airline_code = kwargs["airline_code"]
    flight_number = kwargs["flight_number"]

    rest_details = {
        "operation": "GET",
        "params": {"airlineCode": airline_code, "flightNumber": flight_number},
        "path": context_data["end_points"]["vip"]["leg_periods_all"],
        "expected_status_code": kwargs.get("expected_response_code", "200"),
        "verify": False,
    }

    LOGGER.debug("REST Details: %s", rest_details)

    return rest_details
