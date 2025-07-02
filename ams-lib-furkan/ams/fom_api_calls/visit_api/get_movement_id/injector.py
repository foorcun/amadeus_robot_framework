"""
This module contains the injector to get movement id details

"""

import protocols.broker
from .injector_rest import injector as rest_injector


# pylint: disable=line-too-long
def get_movement_id_details(session_key="defaultKey", **kwargs):
    """
    GET Movement id Details.
    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                       | *Description*                                                                                                  |

    | ``expected_response_code``         | expected response code from the api response                                                                  |
    | ``endpoint_type``                  | endpoint url to create the resource                                                                           |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed             |
    | ``path_param``                     | path parameter to be passed                                                                                   |


    === Usage: ===

    | GET Movement Id Details     expected_response_code=200      endpoint_type=visits_get     movement_id= C_XYB_1112__20250305_DEPARTURE_XYZA
    | GET Movement Id Details     expected_response_code=200      endpoint_type=visits_get

    """

    return protocols.broker.injector(kwargs, session_key, rest_injector)
