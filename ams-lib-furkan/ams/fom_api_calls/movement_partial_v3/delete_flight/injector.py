"""
This module contains the injector to delete movements
"""

import logging
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def fom_v3_movements_delete(flight_id):
    """
    Deletes a movement using the FOM v3 mevements API with the provided flight ID.

    This function builds the required payload with the given flight_id and sends a PUT request
    to the /fom/rest-services/v3/movements/partials/{id} endpoint to mark the movement as deleted.

    | *Arguments*      | *Description*                                   |
    |------------------|-------------------------------------------------|
    | ``flight_id``    | The ID of the flight/movement to be deleted.    |

    === Usage: ===
    | ${response}    Fom V3 Movements Delete    ${flight_id}

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    context_data = session_manager.sessions._get_session_context_data()
    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("movements", {})
        .get("partial_update")
    )

    payload_data = {"id": flight_id}

    gen_payload = PayloadGenerator(
        payload_data, "movement_put_partial_delete.jinja", __file__
    )
    entity = gen_payload.construct_generic_payload()

    kwargs = {"path_params": {"id": flight_id}, "operation": "PUT", "payload": entity}

    response = _http_call(fom_endpoint, **kwargs)

    LOGGER.info("Flight deleted: %s", flight_id)

    return response
