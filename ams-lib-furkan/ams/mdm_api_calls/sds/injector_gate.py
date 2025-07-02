import logging
from ams.commons import get_customer_id
from .injector import _sds_call, _sds_save, _find_match
import os
import json


LOGGER = logging.getLogger(__name__)


def sds_get_gate_by_name(name):
    """
    Get gate by name

    | *Arguments*                        | *Description*                                                     |
    | ``name``                           | Name of the gate                                                  |

    === Usage: ===
    | Sds Get gate By Name    STD01
    """
    return _sds_call("GET", "gate", "4", f"/name?name={name}") or []


def sds_save_gate(name, payload={}, force_creation=False):
    """
    Save gate

    | *Arguments*                        | *Description*                                                     |
    | ``name``                           | Name of the gate                                                  |
    | ``force_creation``                | Force re-creation of the gate if it already exists (default: False) |

    === Usage: ===
    | Sds Save gate    STD01 force_creation=True
    | Sds Save gate    STD01
    """
    find_match = _find_match(sds_get_gate_by_name, name)
    data = {
        "customerId": get_customer_id(),
        "name": name,
    }
    data.update(payload)
    response =_sds_save("gate", data, find_match, find_match, force_creation)
    #define the schema file path
    schema_path = os.path.join("schemas", "schema.json")

    #load  the json schema
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    
    try:
        validate(instance=response, schema=schema)
        print("Validation successful: The response is valid.")
    except: ValidationError as e:
    print("Validation error: ", e.message)
    # return _sds_save("gate", data, find_match, find_match, force_creation)
    return response
