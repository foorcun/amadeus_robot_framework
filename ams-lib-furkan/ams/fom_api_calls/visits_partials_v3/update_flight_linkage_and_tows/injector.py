"""
This module contains the injector to update flight details
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def flight_linkage_operation(session_key="defaultKey", **kwargs):
    """
    Flight Linkage Operation.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``outbound_movement_id``           | outbound movement id to be passed                                                                     |
    | ``op_type``                        | operation type to be passed                                                                           |


    === Usage: ===
    | Flight Linkage Operation     expected_response_code=200     movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    outbound_movement_id=C_SWR_9211__20250315_DEPARTURE_XYZA      op_type=link
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)


def update_flight_tows(session_key="defaultKey", **kwargs):
    """
    Update Flight Tows.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                          |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``movement_id``                    | movement id to be passed                                                                              |
    | ``op_type``                        | operation type to be passed                                                                           |


    === Usage: ===
    | Update Flight Tows     expected_response_code=200     movement_id=C_CPA_100_20240111_ARRIVAL_XYZA    op_type=update_flight_tows
    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)
