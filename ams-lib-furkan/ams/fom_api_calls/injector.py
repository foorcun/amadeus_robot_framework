"""Injector module to handle GET http calls from FOM"""

import logging
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call_and_check

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def fom_v3_movement_by_id(movement_id):
    """
    Executes a HTTP GET call to retrieve a FOM movement by ID and validates the response.

    This function calls the endpoint /fom/rest-services/v3/movements/{id} with a path parameter 'id'.
    The function checks that the response contains
    "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | movement_id                      | Movement id                                                                           |

    === Usage: ===
    | ${response}    Fom V3 Movements By Id     C_CPA_1400__20250424_ARRIVAL_XYZA

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("movements", {})
        .get("delete")
    )

    kwargs = {"path_params": {"id": movement_id}}

    response_json = _http_call_and_check(fom_endpoint, **kwargs)

    movement = None
    if "content" in response_json and len(response_json["content"]) > 0:
        movement = response_json["content"][0]

    return movement


def fom_v3_movements_internal_id():
    """
    Executes a HTTP GET call to retrieve a FOM movement by internal ID and validates the response.

    This function calls the endpoint /fom/rest-services/v3/movements/internal-id/{id} with a path parameter 'id'.
    The function checks that the response contains
    "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments                                                      |

    === Usage: ===
    | ${response}    Fom V3 Movements Internal Id

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("movements", {})
        .get("internal_id")
    )

    kwargs = {"path_params": {"id": "TEST"}}

    response_json = _http_call_and_check(fom_endpoint, **kwargs)
    return response_json


def fom_v3_visits_additional_sources():
    """
    Executes a HTTP GET call to retrieve additional sources for FOM visits and validates the response.

    This function calls the endpoint /fom/rest-services/v3/visits/additionalsources.
    The function checks that the response contains "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments.                                                     |

    === Usage: ===
    | ${response}    Fom V3 Visits Additional Sources

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("visits", {})
        .get("additional_sources")
    )

    kwargs = {}

    response_json = _http_call_and_check(fom_endpoint, **kwargs)
    return response_json


def fom_v4_visits_searches():
    """
    Executes a HTTP POST call to search for FOM visits using specified query parameters and validates the response.

    This function calls the endpoint /fom/rest-services/v4/visits/searches with the following query parameters:
        - start-date
        - end-date
        - flight_number
        - best-time
        - ignore-pax-data
        - fetchSourceAttributes
        - fetchTowSourceAttributes

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments. Query parameters are set within the function.       |

    === Usage: ===
    | ${response}    Fom V4 Visits Searches

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("visits", {})
        .get("searches")
    )

    kwargs = {
        "operation": "POST",
        "query_params": {
            "start-date": "20250523T184855Z",
            "end-date": "20250524T014855Z",
            "flight_number": "1234",
            "best-time": "true",
            "ignore-pax-data": "true",
            "fetchSourceAttributes": "false",
            "fetchTowSourceAttributes": "false",
        },
    }

    response_json = _http_call_and_check(fom_endpoint, **kwargs)
    return response_json
