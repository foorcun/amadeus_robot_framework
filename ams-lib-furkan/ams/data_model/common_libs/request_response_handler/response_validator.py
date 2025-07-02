"""Module to house all functions related to response validation"""

import json
import logging
import os
from json import JSONDecodeError
from jsonschema import validate, ValidationError
import jmespath

# pylint: disable=line-too-long

LOGGER = logging.getLogger()


def load_and_validate_response_schema(current_file, schema_name, response):
    """
    Load a JSON schema from a file and validate a given response against it.

    Args:
        current_file (str): The path to the current file, used to locate the schema file.
        schema_name (str): The name of the schema file to load.
        response (dict): The JSON response to validate against the loaded schema.

    Raises:
        AssertionError: If the response does not conform to the loaded schema, an AssertionError
            is raised with details of the validation error.

    Logs:
        Logs a message indicating whether the response is valid according to the loaded schema.
    """
    schema_file_paths = [
        os.path.join(os.path.dirname(current_file), schema_name),
        os.path.join(os.path.dirname(current_file), "schemas", schema_name),
    ]
    schema_file_path = next((p for p in schema_file_paths if os.path.isfile(p)), None)

    with open(schema_file_path, "r", encoding="utf-8") as schema_file:
        generated_schema = json.load(schema_file)
    try:
        validate(instance=response, schema=generated_schema)
        LOGGER.info(
            "The response is valid according to loaded schema for %s", schema_name
        )
    except ValidationError as e:
        raise AssertionError(
            "error found in path: " + e.json_path + "\n" + e.message
        ) from e


def _validate_json_response_schema(response, expected_schema):
    """
    Validates the JSON response against the expected schema.

    Args:
        response (requests.Response): The HTTP response object containing the JSON data.
        expected_schema (dict): The JSON schema to validate against.

    Raises:
        AssertionError: If the JSON response does not match the expected schema.
        JSONDecodeError: If the response does not contain a valid JSON object.

    Logs:
        Info: If the response is valid according to the loaded schema.
        Warning: If there is no JSON object in the response.
    """
    try:
        validate(instance=response.json(), schema=expected_schema)
        LOGGER.info("The response is valid according to expected schema")
    except JSONDecodeError as e:
        LOGGER.warning("There is no JSON object in the response: %s", e)
    except ValidationError as e:
        raise AssertionError(
            "error found in path: " + e.json_path + "\n" + e.message
        ) from e


def verify_response_status_code(
    rest_response_status_code: int, expected_status_code: str
) -> None:
    """
    Verifies that the actual response status code matches the expected status code.

    Args:
        rest_response_status_code (int): The actual status code received from the REST response.
        expected_status_code (str): The expected status code as a string.

    Raises:
        AssertionError: If the actual status code does not match the expected status code.

    Example:
        >>> verify_response_status_code(200, "200")
        # No exception raised

        >>> verify_response_status_code(404, "200")
        # AssertionError: Expected status:200.
        # Received status:404 and type is (<class 'str'>, <class 'int'>)
    """
    assert rest_response_status_code == int(
        expected_status_code
    ), f"Expected status:{expected_status_code}. Received status:{rest_response_status_code} and \
        type is {type(expected_status_code) , {type(rest_response_status_code)}}"


def search_jmespath(
    query, response, context_data=None, variable_name=None, context_key=None
):
    """Searches for a specified JMESPath query within a given response and optionally stores
     the result in a context.
    Args:
        query (str): The JMESPath query to search for in the response.
        response (dict): The response data to search within.
        context_data (dict, optional): The context data dictionary where the result
        can be stored. Defaults to None.
        variable_name (str, optional): The name of the variable to store the result under
        in the context data. Defaults to None.
        context_key (str, optional): The key within the context's test_context
        to store the result under. Defaults to None.
    Raises:
        ValidationError: If the query is not found in the response.
    Returns:
        None
    """
    query_output = jmespath.search(query, response)
    if not query_output:
        raise ValidationError(f"Unable to find {query} in {response}")

    if context_key is not None:
        LOGGER.debug(
            "Storing data in %s.%s under context.test_context",
            context_key,
            variable_name,
        )
        LOGGER.debug(context_data["test_context"][context_key])
        context_data["test_context"][context_key][variable_name] = query_output

    LOGGER.info("Validation has passed for %s in %s", query, response)


def execute_jmespath_queries(query_dict, response, context_data, context_key):
    """Executes JMESPath queries on the given response and stores the results in the
        context data.

    Args:
        query_dict (dict): A dictionary where keys are variable names and values are
        JMESPath queries.
        response (dict): The response data to be queried.
        context_data (dict): The context data where the results will be stored.
        context_key (str): The key under which the results will be stored in the
        context data.

    Returns:
        None
    """
    for key, query in query_dict.items():
        LOGGER.debug(
            "Executing jmespath query : %s, and adding variable %s in %s context.test_context",
            query,
            key,
            context_key,
        )
        search_jmespath(query, response, context_data, key, context_key)


def validate_general_processing(response, status="OK"):
    """
    Validates the general processing status present in the response for API calls.
    Arguments:
        response (requests.Response): The response object from API calls.
        status (str, optional): The expected general processing status. Defaults to "OK".
    Raises:
        ValueError: If the general processing status is not "OK" or there are general error details when status is "OK".
        ValueError: If the general processing status is not "ERROR" or there are no general error details when status is "ERROR".

    """
    general_processing_status = jmespath.search(
        "generalProcessingStatus", response.json()
    )
    general_error_details = jmespath.search(
        "generalErrorInformation[].{messageText: messageText, details: details}",
        response.json(),
    )

    match status:
        case "OK":
            if general_processing_status == "OK" and not general_error_details:
                LOGGER.debug(
                    "General processing status is OK and there are no general error details."
                )
            else:
                raise ValueError(
                    f"General processing status is not OK or there are general error details: {general_error_details}"
                )

        case "ERROR":
            if general_processing_status == "ERROR" and general_error_details:
                LOGGER.debug(
                    "General processing status is ERROR and there are general error details: %s",
                    general_error_details,
                )
            else:
                LOGGER.debug(
                    "General processing status is not ERROR or there are no general error details."
                )


def validate_response_all(current_file, schema_name, response, status):
    """
    This method to be extended further to validate all the response schema and general processing.

    Validates the response schema and performs general processing attribute validation.

    This function first loads and validates the response schema using the provided
    schema name and current file. It then validates the general processing of the
    response based on the given status.

    Args:
        current_file (str): The path to the current file containing the schema.
        schema_name (str): The name of the schema to validate against.
        response (dict): The response data to be validated.
        status (int): The status code of the response.

    Raises:
        SchemaValidationError: If the response schema validation fails.
        GeneralProcessingError: If the general processing validation fails.
    """

    load_and_validate_response_schema(current_file, schema_name, response)
    validate_general_processing(response, status)
