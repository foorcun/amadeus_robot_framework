"""
This module contains the injector to create inbound or outbound flight

"""

import logging
import protocols.broker
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call_and_check
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)
from ams.data_model.common_libs.utils.generic_helpers import add_data_to_clean_up
from .responses import get_flight_details_from_json
from .injector_rest import injector as rest_injector

LOGGER = logging.getLogger(__name__)


# pylint: disable=line-too-long, protected-access
def create_inbound_or_outbound_flight(session_key="defaultKey", **kwargs):
    """
    Create Inbound or Outbound Flight.

     | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


     Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

     | *Arguments*                       | *Description*                                                                                                 |

     | ``expected_response_code``         | expected response code from the api response                                                                  |
     | ``endpoint_type``                  | endpoint url to create the resource                                                                           |
     | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed             |
     | ``default_params``                 | The default parameters to include in the request. Default is "type"                                                                                                                                                                |


     === Usage: ===
     | Create Inbound or Outbound Flight  type=DEPARTURE    expected_response_code=200      endpoint_type=movements_post


    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def fom_v3_create_movement(flight_data):
    """
    Creates an inbound or outbound flight using the FOM v3 mevements API with the provided flight data.

    This function builds the required payload from the given flight_data dictionary and sends a POST request
    to /fom/rest-services/v3/movements/adhoc endpoint. All required fields must be present in flight_data.

    | *Arguments*      | *Description*                                                                 |
    |------------------|-------------------------------------------------------------------------------|
    | ``flight_data``  | Dictionary containing flight details. Must include:                           |
    |                  |   - airline (dict with "id")                                                  |
    |                  |   - airport (dict with "id")                                                  |
    |                  |   - aircraftType (dict with "id")                                             |
    |                  |   - flightNumber                                                              |
    |                  |   - type ("ARRIVAL" or "DEPARTURE")                                           |
    |                  |   - time (ISO 8601 string)                                                    |

    === Usage: ===
    | ${response}    Fom V3 Create Movement    ${flight_data}

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If required fields are missing in flight_data or if ref_airport is not set in the test context.
    """
    context_data = session_manager.sessions._get_session_context_data()
    fom_endpoint = (
        context_data.get("end_points", {})
        .get("fom", {})
        .get("movements", {})
        .get("adhoc")
    )

    ref_airport = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("ref_airport_full", None)
    )

    if ref_airport is None:
        raise ValueError("ref_airport is not set in the test context.")

    airline = flight_data.get("airline")
    airport = flight_data.get("airport")
    aircraft_type = flight_data.get("aircraftType")
    flight_number = flight_data.get("flightNumber")
    flight_type = flight_data.get("type")
    time = flight_data.get("time")

    missing_fields = []
    if not airline:
        missing_fields.append("airline")
    if not airport:
        missing_fields.append("airport")
    if not aircraft_type:
        missing_fields.append("aircraftType")
    if not flight_number:
        missing_fields.append("flightNumber")
    if not flight_type:
        missing_fields.append("type")
    if not time:
        missing_fields.append("time")
    if missing_fields:
        raise ValueError(
            f"Missing required fields in flight_data: {', '.join(missing_fields)}"
        )

    op_qualifier = "ONB" if flight_type == "ARRIVAL" else "OFB"
    arrival_airport = ref_airport if flight_type == "ARRIVAL" else airport.get("id")
    departure_airport = airport.get("id") if flight_type == "ARRIVAL" else ref_airport

    payload_data = {
        "airline": airline.get("id"),
        "flightNumber": flight_number,
        "departureAirport": departure_airport,
        "arrivalAirport": arrival_airport,
        "type": flight_type,
        "operationTimeDuration": [
            {
                "timeType": "SCT",
                "operationQualifier": op_qualifier,
                "value": {"time": time},
            }
        ],
        "aircraftType": aircraft_type.get("id"),
        "operationalStatus": "OP",
        "serviceType": "J",
    }

    gen_payload = PayloadGenerator(
        payload_data, "post_inbound_or_outbound_flight.jinja", __file__
    )
    entity = gen_payload.construct_generic_payload()

    kwargs = {"operation": "POST", "payload": entity}

    response = _http_call_and_check(fom_endpoint, **kwargs)

    flight_id = get_flight_details_from_json(response.get("content"), "id")

    add_data_to_clean_up("movement", flight_id)

    return response
