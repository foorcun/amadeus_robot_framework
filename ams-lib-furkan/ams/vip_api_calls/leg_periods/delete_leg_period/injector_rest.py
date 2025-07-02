import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.utils import generic_helpers as helpers


LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument, unused-variable, protected-access, too-many-locals


@RestInjector
def injector(kwargs, session_key):
    context_data = session_manager.sessions._get_session_context_data()

    leg_period_id = kwargs["leg_period_id"]

    endpoint = context_data["end_points"]["vip"]["leg_periods_delete"].replace(
        "{id}", leg_period_id
    )

    rest_details = {
        "operation": "DELETE",
        "path": endpoint,
        "expected_status_code": kwargs.get("expected_response_code", "200"),
        "verify": False,
    }

    LOGGER.debug("REST Details: %s", rest_details)

    return rest_details
