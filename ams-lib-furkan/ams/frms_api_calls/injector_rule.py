from ams.data_model.common_libs.utils.generic_helpers import add_data_to_clean_up
from ams.frms_api_calls.common import _frms_call

# pylint: disable=line-too-long


def frms_get_rule_by_id(rule_id):
    """
    Get FRMS Rule By Id

    | *Arguments*                       | *Description*                                                        |
    | ``rule_id``                       | Rule id                                                              |

    === Usage: ===
    | Frms Get Rule By Id    rule_id=888e03b5-1016-4820-800a-88da2c8f84ba

    """
    return _frms_call("GET", f"/rules/find/{rule_id}")


def frms_create_allocation_rule(resource_type, name):
    """
    Create an FRMS allocation rule

    | *Arguments*                      | *Description*                                                   |
    | ``resource_type``                | Resource type (e.g., STAND)                                     |
    | ``name``                         | Name of the allocation rule                                     |

    === Usage: ===
    | Frms Create Allocation Rule    resource_type=STAND   name=MyRule

    """
    form_data = {
        "@type": "COMPATIBILITY",
        "activated": True,
        "conditions": [
            [
                {
                    "name": "OPERATIONAL_STATUS",
                    "resourceType": None,
                    "subCategory": None,
                    "value": ["DX"],
                    "operator": "EQUAL",
                    "visitSide": "EITHER",
                    "routing": "DIRECT",
                }
            ]
        ],
        "explanation": name,
        "importance": "HARDRULE",
        "name": name,
        "resourceType": resource_type.upper(),
        "showConflicts": True,
        "unbreakable": False,
    }
    return _save_rule(form_data)


def frms_create_dedicated_demand_rule(
    resource_type,
    name,
    offset_arr_before=-20,
    offset_arr_after=20,
    offset_dep_before=-20,
    offset_dep_after=20,
):
    """
    Create an FRMS demand rule

    | *Arguments*                      | *Description*                                                   |
    | ``resource_type``                | Resource type (e.g., GATE)                                     |
    | ``name``                         | Name of the demand rule                                         |

    === Usage: ===
    | Frms Create Demand Rule    resource_type=GATE   name=MyRule

    """
    form_data = {
        "@type": "DEDICATED_DEMAND",
        "activated": True,
        "allocationDemands": [
            {
                "deskType": "0",
                "direction": "ARRIVAL",
                "startMin": offset_arr_before,
                "endMin": offset_arr_after,
            },
            {
                "deskType": "0",
                "direction": "DEPARTURE",
                "startMin": offset_dep_before,
                "endMin": offset_dep_after,
            },
        ],
        "arrivalTimeQualifier": "ONB",
        "departureTimeQualifier": "OFB",
        "explanation": name,
        "fixedDemand": True,
        "name": name,
        "priority": 1,
        "resourceType": resource_type,
        "timeType": "BEST",
    }
    return _save_rule(form_data)


def frms_change_rule_priority(rule_id, priority):
    """
    Change the priority of an FRMS rule

    | *Arguments*                     | *Description*                                                |
    | ``rule_id``                     | Rule ID to change priority                                   |
    | ``priority``                    | New priority value (highest priority = 1)                    |

    === Usage: ===
    | Frms Change Rule Priority    rule_id=888e03b5-1016-4820-800a-88da2c8f84ba   priority=1

    """
    return _frms_call(
        "GET",
        f"/rules/update-priority/{rule_id}/{priority}",
    )


def frms_delete_rules(rule_ids):
    """
    Delete a list of FRMS rules

    | *Arguments*                     | *Description*                                                 |
    | ``rule_ids``                    | List of Rule IDs to delete                                    |

    === Usage: ===
    | Frms Delete Rules    rule_ids=[888e03b5-1016-4820-800a-88da2c8f84ba]

    """
    return _frms_call("POST", "/rules/delete", rule_ids)


def _save_rule(form_data):
    rule = _frms_call("POST", "/rules/save", form_data)
    add_data_to_clean_up("frms_rule", rule["id"])
    return rule
