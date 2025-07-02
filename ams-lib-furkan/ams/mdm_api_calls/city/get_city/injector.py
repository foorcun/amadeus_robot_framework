"""
This module contains the injector to fetch the details of the cities present in the master data
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def get_city_details(session_key="defaultKey", **kwargs):
    """
    Get City Details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                        | *Description*                                                                                         |

    | ``expected_response_code``         | expected response code from the api response defaults to 200                                          |
    | ``endpoint_type``                  | endpoint url to fetch the resource details                                                            |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |


    === Usage: ===
    | Get City Details      expected_response_code=200    endpoint_type=list
    | Get City Details      expected_response_code=200    endpoint_type=list    additional_params={"id": ["CIT_MKV","CIT_POL","CIT_TRY"]}
    | Get City Details      expected_response_code=200    endpoint_type=count


    """
    return protocols.broker.injector(kwargs, session_key, rest_injector)
