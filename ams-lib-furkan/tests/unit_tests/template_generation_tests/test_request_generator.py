"""
Unit tests for the PayloadGenerator class.
"""

import os
import pytest
from unittest.mock import patch, mock_open
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)


@pytest.fixture
def payload_generator():
    input_data = {"key": "value"}
    filename = "test_template.j2"
    current_file = __file__
    return PayloadGenerator(input_data, filename, current_file)


@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.os.path.isfile",
    return_value=True,
)
@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.open",
    new_callable=mock_open,
    read_data="template content",
)
def test_read_template(mock_open, mock_isfile, payload_generator):
    result = payload_generator.read_template(
        payload_generator.filename, payload_generator.current_file
    )
    expected_path = os.path.join(
        os.path.dirname(__file__), "template_files", payload_generator.filename
    )
    assert result == "template content"
    mock_open.assert_called_once_with(
        expected_path,
        "r",
        encoding="utf-8",
    )


@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.os.path.isfile",
    return_value=False,
)
def test_read_template_file_not_found(mock_isfile, payload_generator):
    with pytest.raises(FileNotFoundError):
        payload_generator.read_template(
            payload_generator.filename, payload_generator.current_file
        )


@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.GaD.generate_airline_code",
    return_value="Hello {{ data.key }}",
)
@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.PayloadGenerator.read_template",
    return_value="Hello {{ data.key }}",
)
@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.LOGGER.debug"
)
def test_construct_generic_payload(
    mock_log_debug,
    mock_generate_airline_code,
    mock_read_template,
    payload_generator,
):
    """Test constructing a generic payload."""
    result = payload_generator.construct_generic_payload()
    expected_payload = "Hello value"
    assert result == expected_payload


@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.GaD.generate_flight_number",
    return_value="1246",
)
@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.GaD.generate_airline_code",
    return_value="ARL_",
)
@patch(
    "ams.data_model.common_libs.request_response_handler.request_generator.LOGGER.debug"
)
def test_payload_generation_without_mock(
    mock_log_debug,
    mock_generate_airline_code,
    mock_generate_flight_number,
    payload_generator,
):
    """Test payload generation without using mocks."""
    data = {"customerId": "value", "airlineCode": "ARL_"}
    template_name = "template.jinja"
    plg = PayloadGenerator(
        input_data=data, filename=template_name, current_file=__file__
    )
    generated_payload = plg.construct_generic_payload()
    assert (
        generated_payload
        == """{"flight": {"customerId": "value","airlineCode": "ARL_" ,"flightNumber": "1246" ,"operationalSuffix": ""},}"""
    )
