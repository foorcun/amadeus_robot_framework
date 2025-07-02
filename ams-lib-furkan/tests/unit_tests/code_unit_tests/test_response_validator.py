import pytest
from jsonschema import ValidationError
import os
import json

from ams.data_model.common_libs.request_response_handler.response_validator import (
    load_and_validate_response_schema,
    verify_response_status_code,
    search_jmespath,
    execute_jmespath_queries,
)


# Mocking the logger
class MockLogger:
    @staticmethod
    def info(msg):
        print(f"INFO: {msg}")

    @staticmethod
    def debug(msg):
        print(f"DEBUG: {msg}")


log = MockLogger()

# Test data
current_file = __file__
schema_name = "test_schema.json"
response = {"key": "value"}
invalid_response = {"invalid_key": "value"}
schema_content = {
    "type": "object",
    "properties": {"key": {"type": "string"}},
    "required": ["key"],
}


# Helper function to create a temporary schema file
def create_temp_schema_file(schema_content):
    schema_file_path = os.path.join(
        os.path.dirname(current_file), "schemas", schema_name
    )
    os.makedirs(os.path.dirname(schema_file_path), exist_ok=True)
    with open(schema_file_path, "w", encoding="utf-8") as schema_file:
        json.dump(schema_content, schema_file)
    return schema_file_path


# Tests
def test_load_and_validate_response_schema_valid():
    schema_file_path = create_temp_schema_file(schema_content)
    try:
        load_and_validate_response_schema(current_file, schema_name, response)
    except AssertionError:
        pytest.fail("Unexpected AssertionError raised")


def test_load_and_validate_response_schema_invalid():
    schema_file_path = create_temp_schema_file(schema_content)
    with pytest.raises(AssertionError):
        load_and_validate_response_schema(current_file, schema_name, invalid_response)


def test_verify_response_status_code_valid():
    try:
        verify_response_status_code(200, "200")
    except AssertionError:
        pytest.fail("Unexpected AssertionError raised")


def test_verify_response_status_code_invalid():
    with pytest.raises(AssertionError):
        verify_response_status_code(404, "200")


def test_search_jmespath_valid():
    response = {"key": "value"}
    query = "key"
    context_data = {"test_context": {"key": {}}}
    search_jmespath(query, response, context_data, "variable_name", "key")
    assert context_data["test_context"]["key"]["variable_name"] == "value"


def test_search_jmespath_invalid():
    response = {"key": "value"}
    query = "invalid_key"
    with pytest.raises(ValidationError):
        search_jmespath(query, response)


def test_execute_jmespath_queries():
    response = {"customerId": "value"}
    query_dict = {"customerId": "customerId"}
    context_data = {"test_context": {"some_context": {}}}
    execute_jmespath_queries(query_dict, response, context_data, "some_context")
    assert context_data["test_context"]["some_context"]["customerId"] == "value"
