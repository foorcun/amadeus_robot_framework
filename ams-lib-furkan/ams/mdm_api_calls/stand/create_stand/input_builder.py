# pylint:disable=line-too-long

"""
This module contains function to help building the input payload data for stand creation API POST call
"""

import json
import logging
from ams.mdm_api_calls.gate.get_gate.injector import get_gate_details
from ams.mdm_api_calls.equipment.get_equipment.injector import (
    get_equipment_type_details,
)
from ams.commons import get_resource_period_details

LOGGER = logging.getLogger(__name__)


def _add_security_level(payload_input_data, arr_security_level, dep_security_level):
    """
    Add security level to the payload input data

    Args:
        payload_input_data (dict): The payload input data
        arrival_security_level (list): The arrival security level
        departure_security_level (list): The departure security level

    Returns:
        dict: The updated payload input data with allowed security level details
    """

    security_level = {
        "DOMESTIC": 0,
        "SCHENGEN": 1,
        "EU": 2,
        "INTERNATIONAL": 3,
        "CRITICAL": 4,
        "EUSAFE": 5,
        "NONEUSAFE": 6,
    }

    arrival_security_level = (
        [security_level.get(level, 0) for level in arr_security_level.split(", ")]
        if arr_security_level
        else []
    )
    departure_security_level = (
        [security_level.get(level, 0) for level in dep_security_level.split(", ")]
        if dep_security_level
        else []
    )

    payload_input_data["periods_allowedSecurityLevelArrival"] = arrival_security_level
    payload_input_data["periods_allowedSecurityLevelDeparture"] = (
        departure_security_level
    )

    return payload_input_data


def _add_gate_connection(payload_input_data, gate_id):
    """
    Add gate connections to the payload input data

    Args:
        payload_input_data (dict): The payload input data
        gate_id (str): The id for gate resource

    Returns:
        dict: The updated payload input data with gate connection details
    """
    gate_details = get_gate_details(endpoint_type="gateList", path_param=gate_id)
    gate_details_json = gate_details.json()

    start_date_time = (
        gate_details_json.get("periods", [{}])[0].get("startDateTime") or "null"
    )
    end_date_time = (
        gate_details_json.get("periods", [{}])[0].get("endDateTime") or "null"
    )
    allowed_direction = gate_details_json.get("periods", [{}])[0].get(
        "allowedDirection"
    )

    gate_connections = [
        {
            "targetResource": {"id": gate_id, "dataType": "GAT"},
            "startDateTime": start_date_time,
            "endDateTime": end_date_time,
            "direction": allowed_direction,
        }
    ]

    payload_input_data["connections_gateDirectionalConnection"] = gate_connections
    return payload_input_data


def _add_equipment_connection(payload_input_data, equipment_type):
    """
    Add equipment connection to the payload input data

    Args:
        payload_input_data (dict): The payload input data
        equipment_type (str): The type(name) of the equipment

    Returns:
        dict: The updated payload input data with equipment connection details
    """

    all_equipment_details = get_equipment_type_details(endpoint_type="equipmentType")
    all_equipment_details_json = all_equipment_details.json()

    equipment_period_details = get_resource_period_details(
        all_equipment_details_json, name=equipment_type
    )

    period_details = json.loads(
        equipment_period_details.replace("'", '"').replace("None", "null")
    )

    start_date_time = period_details.get("startDateTime") or "null"
    end_date_time = period_details.get("endDateTime") or "null"

    equipment_connections = [
        {
            "targetResource": {
                "type": equipment_type,
                "name": f"{equipment_type}_{payload_input_data.get('name')}",
            },
            "startDateTime": start_date_time,
            "endDateTime": end_date_time,
        }
    ]

    payload_input_data["connections_equipmentConnection"] = equipment_connections
    return payload_input_data
