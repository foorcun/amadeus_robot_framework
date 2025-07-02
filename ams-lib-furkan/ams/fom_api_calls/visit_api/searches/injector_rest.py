import logging
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.utils import generic_helpers as helpers

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access


@RestInjector
def injector(kwargs, session_key):
    context_data = session_manager.sessions._get_session_context_data()

    flight_number = kwargs["flight_number"]

    start_year = kwargs["start_date"][0]
    start_month = kwargs["start_date"][1]
    start_day = kwargs["start_date"][2]
    start_date = f"{start_year}{start_month}{start_day}T000000Z"

    end_year = kwargs["end_date"][0]
    end_month = kwargs["end_date"][1]
    end_day = kwargs["end_date"][2]
    end_date = f"{end_year}{end_month}{end_day}T000000Z"

    LOGGER.info(
        "Search flight number %s between %s and %s", flight_number, start_date, end_date
    )

    params = helpers.build_query_param_string(
        {
            "start-date": start_date,
            "end-date": end_date,
            "flight-number": flight_number,
            "best-time": "true",
            "ignore-pax-data": "true",
            "fetchSourceAttributes": "false",
            "fetchTowSourceAttributes": "false",
        }
    )

    rest_details = {
        "operation": "POST",
        "params": params,
        "path": context_data["end_points"]["fom"]["visits"]["searches"],
        "expected_status_code": kwargs.get("expected_response_code", "200"),
        "verify": False,
    }

    return rest_details
