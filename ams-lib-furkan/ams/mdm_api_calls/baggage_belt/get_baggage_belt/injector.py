"""
This module contains the injector to fetch the baggage belt details
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def get_baggage_belt_details(session_key="defaultKey", **kwargs):
    """
    Get Baggage Belt entity details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                        | *Description*                                                                                         |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``endpoint_type``                  | endpoint url to fetch the resource details                                                            |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``path_param``                     | path parameter to be passed                                                                           |


    === Usage: ===
    | Get Baggage Belt Details    expected_response_code=200      endpoint_type=baggageBeltList
    | Get Baggage Belt Details    expected_response_code=200      endpoint_type=baggageBeltCount     path_param=${beltName}
    | Get Baggage Belt Details    expected_response_code=200      endpoint_type=baggageBeltGroup     additional_params=${beltName}

    """
    return protocols.broker.injector(kwargs, session_key, rest_injector)
