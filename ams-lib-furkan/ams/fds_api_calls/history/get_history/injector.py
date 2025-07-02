"""
This module contains the injector to fetch the history details of a given flight from the Flight operations history tab
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def get_flight_history(session_key="defaultKey", **kwargs):
    """
    Get Flight History details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                        | *Description*                                                                                         |

    | ``expected_response_code``         | expected response code from the api response                                                          |
    | ``endpoint_type``                  | endpoint url to fetch the history details                                                             |
    | ``movement_id``                    | movement id for which the history details need to be fetched                                          |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |


    === Usage: ===
    | Get Flight History     expected_response_code=200    endpoint_type=deltaMovements     movement_id=C_AIC_372__20250327_ARRIVAL_XYZA

    """
    return protocols.broker.injector(kwargs, session_key, rest_injector)
