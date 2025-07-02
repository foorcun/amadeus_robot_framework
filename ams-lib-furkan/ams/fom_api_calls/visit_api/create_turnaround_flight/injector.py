"""
This module contains the injector to create turn around flight

"""

import protocols.broker
from .injector_rest import injector as rest_injector


# pylint: disable=line-too-long
def create_turnaround_flight(session_key="defaultKey", **kwargs):
    """
    Create turnaround Flight.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                 |

    | ``expected_response_code``         | expected response code from the api response                                                                  |
    | ``endpoint_type``                  | endpoint url to create the resource                                                                           |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed             |
    | ``path_param``                     | path parameter to be passed                                                                                   |


    === Usage: ===
    | Create turnaround Flight    expected_response_code=200   endpoint_type=visits_post


    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)
