"""
This module contains the HTTP calls for VIP application

"""

import logging
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call
from ams.data_model.common_libs.injectors.injector import _http_call_and_check

LOGGER = logging.getLogger(__name__)


# pylint: disable=line-too-long
def vip_v1_legperiods_all(flight_number=None):
    """
    VIP V1 leg periods list

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``flight_number``                | (optional) flight number                                                              |

    === Usage: ===
    | VIP V1 Legperiods All
    | VIP V1 Legperiods All     flight_number=123

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {})
        .get("vip", {})
        .get("v1", {})
        .get("legperiods_all")
    )

    rest_details = {
        "query_params": {},
    }
    if flight_number is not None:
        rest_details["query_params"]["flightNumber"] = flight_number

    return _http_call_and_check(endpoint, **rest_details)


def vip_v1_seasons():
    """
    VIP V1 Seasons

    === Usage: ===
    | VIP V1 Seasons

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {}).get("vip", {}).get("v1", {}).get("seasons")
    )

    return _http_call_and_check(endpoint)


def vip_v1_exports():
    """
    VIP V1 exports

    === Usage: ===
    | VIP V1 Exports

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {}).get("vip", {}).get("v1", {}).get("exports")
    )

    return _http_call_and_check(endpoint)


def vip_v1_cannedmessages():
    """
    VIP V1 cannedmessages

    === Usage: ===
    | VIP V1 Cannedmessages

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {})
        .get("vip", {})
        .get("v1", {})
        .get("cannedmessages")
    )

    return _http_call(endpoint)


def vip_v1_messages_statsbatches(recon_source):
    """
    VIP V1 Messages Statsbatches

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``recon_source``                 | recon source                                                                          |

    === Usage: ===
    | VIP V1 Messages Statsbatches  recon_source=AMGUIRecon

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {})
        .get("vip", {})
        .get("v1", {})
        .get("statsbatches")
    )

    rest_details = {
        "query_params": {"reconSource": recon_source},
    }

    return _http_call_and_check(endpoint, **rest_details)
