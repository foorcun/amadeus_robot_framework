"""
This module contains the injector to fetch the details of the countries present in the master data
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def get_country_details(session_key="defaultKey", **kwargs):
    """
    Get Country Details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                        | *Description*                                                                                         |

    | ``expected_response_code``         | expected response code from the api response defaults to 200                                          |
    | ``endpoint_type``                  | endpoint url to fetch the resource details                                                            |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed     |


    === Usage: ===
    | Get Country Details      expected_response_code=200    endpoint_type=list
    | Get Country Details      expected_response_code=200    endpoint_type=list    additional_params={"id": ["CNT_UM","CNT_PO","CNT_TY"]}
    | Get Country Details      expected_response_code=200    endpoint_type=count


    """
    return protocols.broker.injector(kwargs, session_key, rest_injector)
