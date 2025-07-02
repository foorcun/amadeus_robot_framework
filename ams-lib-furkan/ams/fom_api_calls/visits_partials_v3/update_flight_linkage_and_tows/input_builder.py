"""
This module contains function to help building the input payload data for Update flight details API
"""

from ams.data_model.common_libs.utils.airport_data_generator import GenerateAirportData


def _add_link(kwargs, context_data, PayloadGenerator):
    """
    Constructs a payload for linking inbound and outbound movements using the provided context data and payload generator.

    Args:
        kwargs (dict): A dictionary containing the movement IDs.
        context_data (dict): A dictionary containing the context data.
        PayloadGenerator (class): A class used to generate the payload.

    Returns:
        dict: The constructed payload for linking the movements.
    """
    inbound_movement_id = kwargs.get("movement_id")
    outbound_movement_id = kwargs.get("outbound_movement_id")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("visit_context", {})
        .get("add_link")
    )
    payload_input_data["inboundMovementId"] = inbound_movement_id
    payload_input_data["outboundMovementId"] = outbound_movement_id
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/visits_put_add_link.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()
    return payload


def _unlink_operation(kwargs, context_data, PayloadGenerator):
    """
    Handles the 'unlink' operation by constructing the necessary payload.

    Args:
        kwargs (dict): A dictionary containing additional parameters, e.g., 'movement_id'.
        context_data (dict): A dictionary containing context data.

    Returns:
        dict: The constructed payload for the unlink operation.
    """

    inbound_movement_id = kwargs.get("movement_id")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("visit_context", {})
        .get("unlink")
    )
    payload_input_data["inboundMovementId"] = inbound_movement_id
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/visits_put_unlink.jinja", __file__
    )
    return gen_payload.construct_generic_payload()


def _add_tows_operation(kwargs, context_data, PayloadGenerator):
    """
    Handles the 'add_tows' operation by constructing the necessary payload.

    Args:
        kwargs (dict): A dictionary containing additional parameters, e.g., 'movement_id', 'resourceId', 'sobt_time', 'sibt_time'.
        context_data (dict): A dictionary containing context data.

    Returns:
        dict: The constructed payload for the add_tows operation.
    """
    movement_id = kwargs.get("movement_id")
    resource_id = kwargs.get("resourceId")
    sobt_time = kwargs.get("sobt_time")
    sibt_time = kwargs.get("sibt_time")
    payload_input_data = (
        context_data.get("test_context", {})
        .get("fom_context", {})
        .get("visit_context", {})
        .get("update_tows")
    )
    payload_input_data["id"] = movement_id
    payload_input_data["time"] = sobt_time
    payload_input_data["time1"] = sibt_time
    payload_input_data["identifier"] = GenerateAirportData.generate_random_string()
    payload_input_data["resourceId"] = resource_id
    gen_payload = PayloadGenerator(
        payload_input_data, "jinja_templates/visits_put_add_tows.jinja", __file__
    )
    return gen_payload.construct_generic_payload()
