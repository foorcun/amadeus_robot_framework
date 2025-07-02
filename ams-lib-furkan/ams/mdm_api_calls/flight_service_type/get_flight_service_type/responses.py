"""
This module contains the functions to fetch resource details based on the response received
"""

import jmespath

# pylint: disable=line-too-long


def get_service_type_code_by_operation_and_category(response, **kwargs):
    """
    Gets the relevant service type codes by passing the response from the get flight service type, the
    operational type and the category

    | *Arguments*               | *Description*                                                   |

    | ``response``              | response from call to 'Get Flight Service Type' keyword      |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*     | *Description*                   |

    | ``operation_type``        | type of operation     |
    | ``category``      | category of operation     |

    === Usage: ===
    | Get Service Type Code by Operation And Category       response=${response}        operation_type=Passenger        category=Scheduled
    | Get Service Type Code by Operation And Category       response=${response}        operation_type=Passenger
    | Get Service Type Code by Operation And Category       response=${response}        operation_type=Passenger        category=Charter
    | Get Service Type Code by Operation And Category       response=${response}        operation_type=Passenger        category=AdditionalFlights

    """
    response_json = response.json()
    if "operation_type" in kwargs and "category" in kwargs:
        operation_type = kwargs["operation_type"]
        category = kwargs["category"]
        query = f"[?value.operation.contains(@, '{operation_type}') && value.application=='{category}'].value.id"
        result = jmespath.search(query, response_json)
        return (
            result
            if result
            else [
                "No matching service type code found, please verify the operation type and category combination"
            ]
        )

    if "operation_type" in kwargs:
        operation_type = kwargs["operation_type"]
        query = f"[?value.operation.contains(@, '{operation_type}')].value.id"
        result = jmespath.search(query, response_json)
        return (
            result
            if result
            else [
                "No matching service type code found, please verify the operation type"
            ]
        )

    if "category" in kwargs:
        category = kwargs["category"]
        query = f"[?value.application=='{category}'].value.id"
        result = jmespath.search(query, response_json)
        return (
            result
            if result
            else ["No matching service type code found, please verify the category"]
        )

    raise ValueError(
        "Please provide either 'operation_type' or 'category' as a keyword argument."
    )
