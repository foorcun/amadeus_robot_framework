"""
This module contains function to help building the input payload data for Update flight details API
"""

from ams.data_model.data_store.inbound_data_for_updating_time import inbound_data
from ams.data_model.data_store.outbound_data_for_updating_time import outbound_data


def _update_and_process_data(leg_type, payload, timing_type):
    """
    Update payload and process data according to the type and timingType.

    Parameters:
    type (str): The type of data, either 'inbound' or 'outbound'.
    inbound_data (dict): The data for inbound operations.
    outbound_data (dict): The data for outbound operations.
    payload (dict): The payload to be updated.
    timingType (str): The timing type to be used for updating the payload.

    Returns:
    dict: The updated payload.

    Raises:
    ValueError: If the type is not 'inbound' or 'outbound'.
    """
    data = None
    if leg_type == "inbound":
        data = inbound_data
    elif leg_type == "outbound":
        data = outbound_data
    else:
        raise ValueError("Invalid type. Must be 'inbound' or 'outbound'.")

    if timing_type in data:
        time_type = data[timing_type]["timeType"]
        operation_qualifier = data[timing_type]["operationQualifier"]
        payload["timeType"] = time_type
        payload["operationQualifier"] = operation_qualifier
    return payload


def _update_flight_op_status(update_type, payload):
    """
    Update payload according to the flight status type.

    Parameters:
    type (str): The type of flight status update, e.g., 'cancel_flight', 'reinstantate', 'nop',
    'delete'. payload (dict): The payload to be updated.

    Returns:
    dict: The updated payload.
    """
    match update_type:
        case "cancel_flight":
            payload["operationalStatus"] = "DX"
        case "reinstantiate":
            payload["operationalStatus"] = "OP"
        case "nop":
            payload["operationalStatus"] = "NOP"
        case "delete":
            payload["operationalStatus"] = "DEL"
    return payload


def _update_divert_type(event_type, payload):
    """
    Update payload according to the divert event type.

    Parameters:
    event_type (str): The type of divert event, e.g., 'divert', 'go_around',
    'ground_return', 'air_return', 'divert_cancel'.
    payload (dict): The payload to be updated.

    Returns:
    dict: The updated payload.
    """
    match event_type:
        case '"divert"':
            payload["type"] = "DIVERT_CONTINUE"
        case '"go_around"':
            payload["type"] = "GO_AROUND"
        case '"ground_return"':
            payload["type"] = "RETURN_TO_RAMP_AND_CREATE"
        case '"air_return"':
            payload["type"] = "RETURN_FROM_AIRBORNE_AND_CREATE"
        case '"divert_cancel"':
            payload["type"] = "DIVERT_CANCEL"
    return payload


def _get_handling_task_value(handling_task):
    """
    Returns the corresponding code for a given handling task.

    Args:
        handling_task (str): The name of the handling task.

    Returns:
        str: The code corresponding to the handling task, or None if the task is not found.
    """
    handling_task_mapping = {
        "Primary": "PRI",
        "Deicing": "ICE",
        "Catering": "CAT",
        "Cleaning": "CLN",
        "Ramp": "PLT",
        "Bus": "BUS",
        "Cargo": "FRT",
        "Baggage": "BAG",
        "Disembarkation": "DIS",
        "Towing": "TOW",
        "TOBT": "TOB",
        "Fueling": "FUE",
        "Check-in": "CHK",
        "Boarding": "BRD",
        "Load Control": "LCT",
        "Loading": "LOD",
        "Crew Activities": "CAC",
        "Push Back": "PUB",
        "Security Check": "SCP",
    }
    return handling_task_mapping.get(handling_task, None)


def _update_timing(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates the timing information of a movement.

    Args:
        op_type (str): The operation type (e.g., "update_time").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated timing information.
    """
    time = kwargs.get("time")
    timing_type = kwargs.get("timing_type")
    leg_type = kwargs.get("leg_type")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("timing_update")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["time"] = time
    updated_payload = _update_and_process_data(
        leg_type, payload_input_data, timing_type
    )
    gen_payload = PayloadGenerator(
        updated_payload, "jinja_templates/movement_put_update_time.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_disruption(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates the disruption information of a movement.

    Args:
        op_type (str): The operation type (e.g., "disruption").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated disruption information.
    """
    divert_time = kwargs.get("divert_time")
    event_type = kwargs.get("event_type")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("event_update")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["time"] = divert_time
    payload_input_data["occurrenceTime"] = divert_time

    updated_payload = _update_divert_type(event_type, payload_input_data)
    gen_payload = PayloadGenerator(
        updated_payload, "jinja_templates/movement_put_divert.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_alert(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Adds an alert to a movement.

    Args:
        op_type (str): The operation type (e.g., "add_alert").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with the added alert.
    """
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("alert_update")
    )
    alert_code = kwargs.get("alert_code")
    payload_input_data["code"] = alert_code
    payload_input_data["id"] = movement_id
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_alert.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_flight_op(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates the flight operation status for a movement.

    Args:
        op_type (str): The operation type (e.g., "flight_op_status_update").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated flight operation status.
    """
    time = kwargs.get("time")
    update_type = kwargs.get("update_type")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context")
        .get("movement_context")
        .get("flight_op_status_update")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["time"] = time
    updated_payload = _update_flight_op_status(update_type, payload_input_data)
    gen_payload = PayloadGenerator(
        updated_payload, "jinja_templates/movement_put_flight_op_status.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_delay(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Adds a delay or subdelay to a movement.

    Args:
        op_type (str): The operation type (e.g., "add_delay").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with the delay or subdelay added.
    """
    payload = None
    departure_or_arrival = kwargs.get("departure_or_arrival")
    delay_type = kwargs.get("delay_type")
    alpha_code = kwargs.get("alpha_code")
    subdelay_alphacode = kwargs.get("subdelay_alphacode")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_delay")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["departureOrArrival"] = departure_or_arrival
    payload_input_data["alphaCode"] = alpha_code
    if delay_type == "delay":
        gen_payload = PayloadGenerator(
            payload_input_data, "jinja_templates/movement_put_add_delay.jinja", __file__
        )
        payload = gen_payload.construct_generic_payload()
    elif delay_type == "subdelay":
        payload_input_data["subDelays"] = subdelay_alphacode
        gen_payload = PayloadGenerator(
            payload_input_data,
            "jinja_templates/movement_put_add_subdelay.jinja",
            __file__,
        )
        payload = gen_payload.construct_generic_payload()
    return payload


def _update_remarks(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Adds remarks to a movement.

    Args:
        op_type (str): The operation type (e.g., "add_remarks").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with the added remarks.
    """
    remark_type = kwargs.get("remark_type")
    remarks = kwargs.get("remarks")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_remarks")
    )
    payload_input_data["qualifier"] = remark_type
    payload_input_data["text"] = remarks
    payload_input_data["id"] = movement_id
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_remarks.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_resources(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Adds resources to a movement.

    Args:
        op_type (str): The operation type (e.g., "add_resources").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with the added resources.
    """
    resource_type = kwargs.get("resource_type")
    departure_or_arrival = kwargs.get("departure_or_arrival")
    resourceid = kwargs.get("resourceId")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_resources")
    )
    payload_input_data["resourceType"] = resource_type
    payload_input_data["departureOrArrival"] = departure_or_arrival
    payload_input_data["resourceId"] = resourceid
    payload_input_data["id"] = movement_id
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_resources.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_tasks(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Adds tasks to a movement.

    Args:
        op_type (str): The operation type (e.g., "add_tasks").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with the added tasks.
    """
    task_type = kwargs.get("task_type")
    value = kwargs.get("value")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_tasks")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["qualifier"] = task_type
    payload_input_data["measurement"] = value
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_tasks.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_handling_agent(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Adds a handling agent to a movement.

    Args:
        op_type (str): The operation type (e.g., "add_handling_agent").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with the added handling agent.
    """
    handling_task = kwargs.get("handling_task")
    handling_task_value = _get_handling_task_value(handling_task)
    value = kwargs.get("value")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_handling_agent")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["handlingTask"] = handling_task_value
    payload_input_data["value"] = value
    gen_payload = PayloadGenerator(
        payload_input_data,
        "jinja_templates/movement_put_handling_agent.jinja",
        __file__,
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_fids(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates FIDS (Flight Information Display System) information for a movement.

    Args:
        op_type (str): The operation type (e.g., "update_fids").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated FIDS information.
    """
    display_type = kwargs.get("display_type")
    airline = kwargs.get("airline")
    flight_number = kwargs.get("flight_number")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_fids")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["displayType"] = display_type
    payload_input_data["airline"] = airline
    payload_input_data["flightNumber"] = flight_number
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_update_fids.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_load(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates load information for a movement.

    Args:
        op_type (str): The operation type (e.g., "update_load").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated load information.
    """
    load_type = kwargs.get("load_type")
    count_qualifier = kwargs.get("count_qualifier")
    count_value = kwargs.get("count_value")
    weight_value = kwargs.get("weight_value")
    cabin = kwargs.get("cabin")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_load")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["type"] = load_type
    payload_input_data["countQualifier"] = count_qualifier
    payload_input_data["countValue"] = count_value
    payload_input_data["weightValue"] = weight_value
    payload_input_data["cabin"] = cabin
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_update_load.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_pax(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates passenger (PAX) information for a movement.

    Args:
        op_type (str): The operation type (e.g., "update_pax").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated passenger information.
    """
    pax_count_qualifier = kwargs.get("pax_count_qualifier")
    cabin_class = kwargs.get("cabin_class")
    count = kwargs.get("count")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_pax")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["class"] = cabin_class
    payload_input_data["paxCount"] = count
    payload_input_data["paxCountQualifier"] = pax_count_qualifier
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/movement_put_update_pax.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _update_aircraft_details(kwargs, context_data, movement_id, PayloadGenerator):
    """
    Updates aircraft details for a movement.

    Args:
        op_type (str): The operation type (e.g., "update_aircraft_details").
        kwargs (dict): The keyword arguments containing operation-specific data.
        context_data (dict): The context data for the movement.
        movement_id (str): The unique identifier for the movement.
        PayloadGenerator (class): The class used to generate payloads.

    Returns:
        dict: The constructed payload with updated aircraft details.
    """
    movement_id = kwargs.get("movement_id")
    registration = kwargs.get("registration")
    aircraft_type = kwargs.get("aircraft_type")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("movement_context", {})
        .get("update_aircraft_details")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["registration"] = registration
    payload_input_data["aircraftType"] = aircraft_type
    gen_payload = PayloadGenerator(
        payload_input_data,
        "jinja_templates/movement_put_update_aircraft_details.jinja",
        __file__,
    )
    payload = gen_payload.construct_generic_payload()
    return payload
