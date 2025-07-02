"""
This module contains the functions to fetch resource details based on the response received
"""

import jmespath

# pylint: disable=line-too-long


def get_baggage_belt_name_or_id(response_json, **kwargs):
    """
    Get baggage belt name by id or vice versa.

    | ``response_json``                  | response object from call to 'Get Baggage Belt Details' keyword |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*      | *Description*                     |

    | ``name``         | name of the baggage belt entity   |
    | ``id``           | id of the baggage belt entity     |

    === Usage: ===
    | Get Baggage Belt Name or ID    response_json=${response}    name=${beltName}
    | Get Baggage Belt Name or ID    response_json=${response}    id=${beltId}

    """
    if "name" in kwargs:
        bb_name = kwargs["name"]
        bb_id = jmespath.search(f"[?name=='{bb_name}'].id | [0]", response_json)
        return bb_id
    if "id" in kwargs:
        bb_id = kwargs["id"]
        bb_name = jmespath.search(f"[?id=='{bb_id}'].name | [0]", response_json)
        return bb_name

    return "Please provide either 'id' or 'name' as a keyword argument."


def get_baggage_belt_gate_connection(response_json, **kwargs):
    """
    Get the details of Gate connection for any baggage belt.

    | ``response_json``                  | response object from call to 'Get Baggage Belt Details' keyword |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*     | *Description*                      |

    | ``name``         | name of the baggage belt entity   |
    | ``id``           | id of the baggage belt entity     |

    === Usage: ===
    | Get Baggage Belt Gate Connection    response_json=${response}    name=${beltName}
    | Get Baggage Belt Gate Connection    response_json=${response}    id=${beltId}

    """
    if "id" in kwargs:
        query = f"[?id=='{kwargs['id']}'].connections.gateConnection[].targetResource.{{id: id, name: name}}"
    elif "name" in kwargs:
        query = f"[?name=='{kwargs['name']}'].connections.gateConnection[].targetResource.{{id: id, name: name}}"
    else:
        return "Please provide either 'id' or 'name' as a keyword argument."

    gate_con = jmespath.search(query, response_json)
    gate_con_str = ", ".join(map(str, gate_con))
    return gate_con_str


def get_arrival_baggage_belt_connection(response_json, **kwargs):
    """
    Get adjacent belt details for any baggage belt.

    | ``response_json``                  | response object from call to 'Get Baggage Belt Details' keyword |


    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*     | *Description*                      |

    | ``name``         | name of the baggage belt entity   |
    | ``id``           | id of the baggage belt entity     |

    === Usage: ===
    | Get Arrival Baggage Belt Connection    response_json=${response}    name=${beltName}
    | Get Arrival Baggage Belt Connection    response_json=${response}    id=${beltId}

    """
    if "id" in kwargs:
        query = f"[?id=='{kwargs['id']}'].connections.arrivalBaggageBeltConnection[].targetResource.{{id: id, name: name}}"
    elif "name" in kwargs:
        query = f"[?name=='{kwargs['name']}'].connections.arrivalBaggageBeltConnection[].targetResource.{{id: id, name: name}}"
    else:
        return "Please provide either 'id' or 'name' as a keyword argument."

    baggage_belt_con = jmespath.search(query, response_json)
    baggage_belt_con_str = ", ".join(map(str, baggage_belt_con))
    return baggage_belt_con_str
