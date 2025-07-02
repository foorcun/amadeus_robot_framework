"""
This module contains the injector to update flight details
"""

import protocols.broker
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long, protected-access


def update_flight_time(session_key="defaultKey", **kwargs):
    """
    Update Flight Time.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |
    | ``leg_type``                       | leg type to be passed                                                                                 |
    | ``timing_type``                    | timing type to be passed                                                                              |


    === Usage: ===
    | Update Flight Time     expected_response_code=200     movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_time    leg_type=inbound    timing_type=AIBT
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_diverion(session_key="defaultKey", **kwargs):
    """
    Update Flight Diversion.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |
    | ``event_type``                     | event type to be passed                                                                               |


    === Usage: ===
    | Update Flight Diversion     expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=disruption    event_type=${event_type}
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_alert(session_key="defaultKey", **kwargs):
    """
    Update Flight Alert.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |
    | ``alert_code``                     | alert code to be passed                                                                               |


    === Usage: ===
    | Update Flight Alert     expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_alert    alert_code=neo11
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_op_status(session_key="defaultKey", **kwargs):
    """
    Update Flight Op Status.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |
    | ``update_type``                    | update type to be passed                                                                              |


    === Usage: ===
    | Update Flight Op Status     expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_op_status    update_type=cancel_flight
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_delay(session_key="defaultKey", **kwargs):
    """
    Update Flight Delay.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |
    | ``delay_type``                     | delay type to be passed                                                                               |


    === Usage: ===
    | Update Flight Delay     expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_delay    delay_type=subdelay
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_remarks(session_key="defaultKey", **kwargs):
    """
    Update Flight Remarks.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |
    | ``remark_type``                    | remark type to be passed                                                                              |
    | ``remarks``                        | remarks to be passed                                                                                  |


    === Usage: ===
    | Update Flight Remarks     expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_remarks    remark_type=CKD    remarks=test
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_resources(session_key="defaultKey", **kwargs):
    """
    Update Flight Resources.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                  |

    | ``expected_response_code``         | expected response code from the api response                                                                  |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed             |
    | ``movement_id``                    | movement id to be passed                                                                                      |
    | ``op_type``                        | operation type to be passed                                                                                   |
    | ``resource_type``                  | resource type to be passed                                                                                    |


    === Usage: ===
    | Update Flight Resources     expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_resources    resource_type=STAND    departure_or_arrival=Arrival    resourceId=${resourceId}
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_tasks(session_key="defaultKey", **kwargs):
    """
    Update Flight Tasks.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                |

    | ``expected_response_code``         | expected response code from the api response                                                                |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed           |
    | ``movement_id``                    | movement id to be passed                                                                                    |
    | ``op_type``                        | operation type to be passed                                                                                 |
    | ``task_type``                      | task type to be passed                                                                                      |
    | ``value``                          | value to be passed                                                                                          |


    === Usage: ===
    | Update Flight Tasks    expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_tasks    task_type=FuelUplift    value=13
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_handling_agent(session_key="defaultKey", **kwargs):
    """
    Update Flight Handling Agent.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                |

    | ``expected_response_code``         | expected response code from the api response                                                                |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed           |
    | ``movement_id``                    | movement id to be passed                                                                                    |
    | ``op_type``                        | operation type to be passed                                                                                 |
    | ``handling_task``                  | handling task to be passed                                                                                  |
    | ``value``                          | value to be passed                                                                                          |


    === Usage: ===
    | Update Flight Handling Agent    expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_handling_agent    handling_task=PRI    value=SH07
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_fids_details(session_key="defaultKey", **kwargs):
    """
    Update Flight Fids Details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                |

    | ``expected_response_code``         | expected response code from the api response                                                                |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed           |
    | ``movement_id``                    | movement id to be passed                                                                                    |
    | ``op_type``                        | operation type to be passed                                                                                 |
    | ``display type``                   | display type to be passed                                                                                   |
    | ``airline``                        | airline to be passed                                                                                        |
    | ``flight number``                  | flight number to be passed                                                                                  |


    === Usage: ===
    | Update Flight Fids Details    expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_fids_details    display_type="STAFF"    airline=6X    flight_number=1212
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_load_details(session_key="defaultKey", **kwargs):
    """
    Update Flight Load Details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                |

    | ``expected_response_code``         | expected response code from the api response                                                                |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed           |
    | ``movement_id``                    | movement id to be passed                                                                                    |
    | ``op_type``                        | operation type to be passed                                                                                 |
    | ``load_type``                      | load type to be passed                                                                                      |
    | ``count_qualifier``                | count_qualifier to be passed                                                                                |
    | ``count_value``                    | count_value to be passed                                                                                    |
    | ``weight_value``                   | weight_value to be passed                                                                                   |
    | ``cabin``                          | cabin to be passed                                                                                          |


    === Usage: ===
    | Update Flight Load Details    expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_load_details    load_type=C    count_qualifier=Accepted    count_value=16     weight_value=12    cabin=F
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_pax_details(session_key="defaultKey", **kwargs):
    """
    Update Flight Pax Details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                |

    | ``expected_response_code``         | expected response code from the api response                                                                |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed           |
    | ``movement_id``                    | movement id to be passed                                                                                    |
    | ``op_type``                        | operation type to be passed                                                                                 |
    | ``cabin_class``                    | cabin class to be passed                                                                                    |
    | ``count``                          | count to be passed                                                                                          |
    | ``pax_count_qualifier``            | pax_count_qualifier to be passed                                                                            |


    === Usage: ===
    | Update Flight Pax Details    expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_pax_details    cabin_class=F    count=10    pax_count_qualifier=Booked
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_aircraft_details(session_key="defaultKey", **kwargs):
    """
    Update Flight Aircraft Details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                |

    | ``expected_response_code``         | expected response code from the api response                                                                |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed           |
    | ``movement_id``                    | movement id to be passed                                                                                    |
    | ``op_type``                        | operation type to be passed                                                                                 |
    | ``registration``                   | registration to be passed                                                                                   |
    | ``aircraft_type``                  | aircraft_type to be passed                                                                                  |


    === Usage: ===
    | Update Flight Aircraft Details    expected_response_code=200      movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_aircraft_details    registration=BLAC    aircraft_type=773
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def fom_v3_movements_update_aircraft_type(flight_id, flight_data):
    """
    Updates the aircraft type of a movement using the FOM v3 mevements API with the provided flight ID and flight data.

    This function builds the required payload with the given flight_id and new aircraft type,
    and sends a PUT request to the /fom/rest-services/v3/movements/partials/{id} endpoint.

    | *Arguments*      | *Description*                                   |
    |------------------|-------------------------------------------------|
    | ``flight_id``    | The ID of the flight/movement to update.        |
    | ``flight_data``  | Dictionary containing the new aircraftType (dict with "id"). |

    === Usage: ===
    | ${response}    Fom V3 Movements Update Aircraft Type    ${flight_id}    ${flight_data}

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

    aircraft_type = flight_data.get("aircraftType")
    if not aircraft_type:
        raise ValueError("Missing required field: aircraftType in flight_data.")

    payload_data = {"id": flight_id, "aircraftType": aircraft_type.get("id")}

    gen_payload = PayloadGenerator(
        payload_data,
        "jinja_templates/movement_put_update_aircraft_type.jinja",
        __file__,
    )
    entity = gen_payload.construct_generic_payload()

    kwargs = {"path_params": {"id": flight_id}, "operation": "PUT", "payload": entity}

    return _http_call(fom_endpoint, **kwargs)
