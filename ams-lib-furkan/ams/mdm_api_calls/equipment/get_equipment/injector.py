"""
This module contains the injector to fetch the equipment type details
"""

import protocols.broker
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def get_equipment_type_details(session_key="defaultKey", **kwargs):
    """
    Get Equipment Type entity details.

    | ``session_key``                  | session alias. If no value specified, default key "defaultKey" is used |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                        | *Description*                                                                                        |

    | ``expected_response_code``         | expected response code from the api response                                                         |
    | ``endpoint_type``                  | endpoint url to fetch the resource details                                                           |
    | ``additional_params``              | dictionary. Values can be either a single value or a list of values. query parameter to be passed    |
    | ``equipmentTypeId``                | path parameter. Id of the equipment type to be passed                                                |

    === Usage: ===
    | Get Equipment Type Details    expected_response_code=200    endpoint_type=equipmentType
    | Get Equipment Type Details    expected_response_code=200    endpoint_type=equipmentType    equipmentTypeId=EQT000081

    """
    return protocols.broker.injector(kwargs, session_key, rest_injector)
