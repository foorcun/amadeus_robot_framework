"""
This module contains the injector to fetch the terminal details
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def get_terminal_details(session_key="defaultKey", **kwargs):
    """
    Get Terminal entity details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:
    Below the possible values:

    | *Arguments*                       | *Description*                                                                                         |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``endpoint_type``                  | endpoint url to fetch the resource details                                                            |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |
    | ``path_param``                     | path parameter to be passed                                                                           |


    === Usage: ===
    | Get Terminal Details    expected_response_code=200      endpoint_type=terminalCount
    | Get Terminal Details    expected_response_code=200      endpoint_type=terminalCount     path_param=${terminalCode}
    | Get Terminal Details    expected_response_code=200      endpoint_type=terminalByCode     additional_params=${terminalCode}

    """
    return protocols.broker.injector(kwargs, session_key, rest_injector)
