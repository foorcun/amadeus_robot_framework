"""
Commons module contains common functions, variables used by the injectors
"""

import os
import sys
import logging
import json
from importlib import import_module
from urllib.parse import urlencode
from protocols import session_manager

from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from ams.data_model.common_libs.utils.built_in_helpers import skip, get_var_value

# pylint: disable=line-too-long
# pylint: disable = protected-access

LOGGER = logging.getLogger(__name__)


def get_variable_value(var_name, default=None):
    """
    Retrieve a variable's value from Robot Framework if available, otherwise from the OS environment, or use a default.

    This function is designed for hybrid codebases that may run under Robot Framework or as standalone Python scripts.
    It first attempts to fetch the variable from Robot Framework's variable store (using BuiltIn). If Robot is not running,
    or the variable is not set in Robot, it falls back to the OS environment variable. If neither is set, it returns the provided default value.

    Args:
        var_name (str): The name of the variable to retrieve (without the $ sign). For example, 'ENVIRONMENT'.
        default (Any, optional): The value to return if the variable is not found in either Robot or the environment. Defaults to None.

    Returns:
        Any: The value of the variable from Robot Framework, the OS environment, or the default if not found.

    Example:
        >>> In Robot Framework, if ENVIRONMENT is set to 'dev', this will return 'dev'.
        >>> In plain Python, if ENVIRONMENT is set in the OS environment, this will return its value.
        >>> If neither is set, returns 'default_env'.
        >>> env = get_variable_value('ENVIRONMENT', 'default_env')

    Notes:
        - If running under Robot Framework and the variable is not set, the function will check the OS environment.
        - If neither Robot nor the OS environment has the variable, the default is returned.
        - This function is safe to use in both Robot Framework and plain Python contexts.
    """
    try:
        value = get_var_value(f"${var_name}")
        if value is None:
            return os.environ.get(var_name, default)
        return value
    except Exception:
        return os.environ.get(var_name, default)


def initialize_context():
    return {
        "generic_context": {
            "customer_id": get_variable_value("CUSTOMER_ID"),
            "ref_airport": get_variable_value("AIRPORT"),
            "ref_airport_full": "APT_" + str(get_variable_value("AIRPORT")),
            "apt_correlation_id": f"regression{Gad.generate_correlation_id(9)}",
        },
        "data_to_clean_up": {},
    }


def add_data_to_clean_up(entity_type, entity_id):
    context_data = session_manager.sessions._get_session_context_data()
    if entity_type not in context_data["test_context"]["data_to_clean_up"]:
        context_data["test_context"]["data_to_clean_up"][entity_type] = []

    context_data["test_context"]["data_to_clean_up"][entity_type].append(entity_id)


def initialize_variables(self):
    """
    Initializes instance variables based on the request_data dictionary.

    This method iterates over the items in the request_data dictionary and sets
    instance attributes with the corresponding key-value pairs. If the key is
    "params" and the value is not present, it attempts to retrieve the "params"
    value from the context_data dictionary using the context_data_key.

    Attributes:
        self.request_data (dict): Dictionary containing request data.
        self.context_data (dict): Dictionary containing context data.
        self.context_data_key (str): Key to access specific context data.

    Logs:
        Logs the setting of the "params" attribute if it is updated.
        Logs the setting of each attribute with its corresponding value.
    """
    for key, value in self.request_data.items():
        if key == "params" and not self.request_data.get("params"):
            self.request_data[key] = (
                self.context_data.get("test_context", {})
                .get(self.context_data_key, {})
                .get("params")
            )
            LOGGER.debug("params is set as : %s ", self.request_data[key])
        setattr(self, key, value)
        LOGGER.debug(
            "Attempting to set Constructor attribute: %s = %s", key, getattr(self, key)
        )


def construct_default_params(default_params, test_context_keys, test_context):
    """
    Constructs a dictionary of parameters based on the provided default parameters and test context.

    Args:
        default_params (str): A comma-separated string of default parameter names.
        test_context_keys (list): A list of keys to look up in the test context.
        test_context (dict): A dictionary containing the test context data.

    Returns:
        dict: A dictionary containing the constructed parameters.
    """
    params = {}
    default_param_list = default_params.split(",")
    LOGGER.debug("default_param_list is %s", default_param_list)
    for param in default_param_list:
        for key in test_context_keys:
            if param in test_context[key].keys():
                params[param] = test_context[key][param]
    return params


def construct_attributes(attributes):
    """
    Constructs a dictionary of attributes from a comma-separated string.

    Args:
        attributes (str): A comma-separated string of attributes.

    Returns:
        dict: A dictionary where each attribute from the input string is
        added with the key "attribute".
    """
    attribute_params = {}
    attribute_list = attributes.split(",")
    for attribute in attribute_list:
        attribute_params["attribute"] = attribute
    return attribute_params


def initialize_test_context(test_data_file_path):
    """
    Initializes the test context by loading the configuration from the specified test data file.

    This function checks if the provided test data file path exists.
    If it does, it loads the context
    configuration from the file, imports the module, and
    returns the context. If the file does not exist,
    it raises an exception.

    Args:
        test_data_file_path (str): The file path to the test data context file.

    Returns:
        module: The imported module containing the test context.

    Raises:
        Exception: If the test data context file does not exist.

    Example:
        context = initialize_test_context('/path/to/test_data.py')
        print(context.test_context)
    """
    if os.path.exists(test_data_file_path):
        LOGGER.debug("Loading context config from %s", test_data_file_path)
        context_dir = os.path.dirname(test_data_file_path)
        sys.path.insert(0, context_dir)
        context_module_name = os.path.splitext(os.path.basename(test_data_file_path))[0]
        py_context = import_module(context_module_name)
        sys.path.remove(context_dir)
        LOGGER.debug("Context is loaded for the test: %s", py_context.test_context)
        return py_context
    raise FileNotFoundError(
        f'Test Data context file "{test_data_file_path}" does not exist'
    )


def build_query_param_string(additional_param: dict, return_type: str = "string"):
    """
    Builds a query parameter string from a dictionary of additional parameters.
    Args:
        additional_param (dict): A dictionary where keys are parameter names and values are parameter values.
                                 Values can be either a single value or a list of values.
        return_type (str): The type of the return value, either "string" or "dict". Default is "string".
    Returns:
        str: A URL-encoded query parameter string. If the input dictionary is empty or an error occurs,
             an empty string is returned.
    Raises:
        TypeError: If the input dictionary contains non-string keys or values.
        ValueError: If the input dictionary contains values that cannot be URL-encoded.
    """
    if not additional_param:
        return "" if return_type == "string" else {}

    query_params = []

    try:
        for key, value in additional_param.items():
            if isinstance(value, list):
                for item in value:
                    query_params.append((key, item))
            else:
                query_params.append((key, value))

        if return_type not in {"string", "dict"}:
            raise ValueError("Invalid return type specified. Use 'string' or 'dict'.")
        return (
            urlencode(query_params) if return_type == "string" else dict(query_params)
        )
    except (TypeError, ValueError) as e:
        print(f"Error building query string: {e}")
        return "" if return_type == "string" else {}


def generate_json_to_jinja_template(data):
    """
    Generates a Jinja template from the given data structure.

    This function takes a nested data structure (dictionary or list) and converts it into a Jinja template format.
    It recursively processes the data to replace values with Jinja template placeholders.

    Args:
        data (dict or list): The input data structure to be converted into a Jinja template.

    Returns:
        dict or list: The formatted Jinja template with placeholders.

    Example:
        input_data = {
            "name": "John",
            "age": "null",
            "address": {
                "city": "New York",
                "zip": "null"
            },
            "hobbies": ["reading", "travelling"]
        }

        template = generate_jinja_template(input_data)
        # Output:
        # {
        #     "name": "{{ data['name'] }}",
        #     "age": "{{ data['age'] }} : {% if data['age'] %} \"{{ data['age'] }}\" {% else %} null {% endif %}",
        #     "address": {
        #         "city": "{{ data['city'] }}",
        #         "zip": "{{ data['zip'] }} : {% if data['zip'] %} \"{{ data['zip'] }}\" {% else %} null {% endif %}"
        #     },
        #     "hobbies": ["{{ data['hobbies'][0] }}", "{{ data['hobbies'][1] }}"]
        # }
    """

    def create_template(data):
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    if "value" in value:
                        result[key] = {"value": f'{{{{ data["{key}"] }}}}'}
                    else:
                        result[key] = create_template(value)
                elif isinstance(value, list):
                    result[key] = [create_template(item) for item in value]
                else:
                    if value is "null":
                        result[key] = (
                            f'{{{{ data["{key}"] }}}} : {{% if data["{key}"] %}} "{{{{ data["{key}"] }}}}" {{% else %}} null {{% endif %}}'
                        )
                    else:
                        result[key] = f'{{{{ data["{key}"] }}}}'
            return result
        elif isinstance(data, list):
            return [create_template(item) for item in data]
        return data

    jinja_template = create_template(data)

    def format_template(template):
        if isinstance(template, dict):
            return {key: format_template(value) for key, value in template.items()}
        elif isinstance(template, list):
            return [format_template(item) for item in template]
        elif isinstance(template, str):
            return template
        return template

    formatted_template = format_template(jinja_template)
    return formatted_template


def find_matching_setting(param_name, application_name, skip_when_not_found=True):
    """
    Finds a setting in the settings list from the active configuration
    where 'parameterName' matches the given param_name
    and 'applicationName' matches the given application_name.

    Args:
        param_name (str): The name of the parameter to search for.
        application_name (str): The name of the application to match.
        skip_when_not_found (bool): If True (default), skips the test when no matching setting is found.
                                    If False, returns None when no matching setting is found.

    Returns:
        dict: The matching setting if found, otherwise test exection is interrupted.
    """

    # Retrieve the active configuration from context_data
    context_data = session_manager.sessions._get_session_context_data()
    active_configuration = context_data.get("active_configuration", {})

    # Get the list of settings
    settings = active_configuration.get("settings", [])

    matching_setting = next(
        (
            setting
            for setting in settings
            if setting.get("parameterName") == param_name
            and setting.get("applicationName") == application_name
        ),
        None,
    )

    if not matching_setting:
        if skip_when_not_found:
            skip(
                msg=f"Error evaluating precondition: no matching setting found for parameter '{param_name}' and application '{application_name}'."
            )
        return None

    return matching_setting


def validate_data_type_and_setting_value(
    data_type, setting_value, expected_type, expected_data_type
):
    """
    Validates the data type and setting value.

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``data_type``             | The actual data type of the setting (e.g., "JSON").                           |
    | ``setting_value``         | The value of the setting to validate.                                         |
    | ``expected_type``         | The expected Python type of the setting value (e.g., dict, list).             |
    | ``expected_data_type``    | The expected data type of the setting (e.g., "JSON", "STRING").               |

    === Behavior: ===
    - If the data type does not match the expected data type, the test is skipped.
    - If the setting value does not match the expected Python type, the test is skipped.

    Raises:
        skip: If the data type or setting value is invalid.
    """
    # Validate data type
    if data_type != expected_data_type:
        skip(
            msg=f"Precondition failed: Expected data type '{expected_data_type}', but got '{data_type}'."
        )

    # Validate setting value type
    if not isinstance(setting_value, expected_type):
        skip(
            msg=f"Precondition failed: Setting value is not of type '{expected_type.__name__}'. Value: {setting_value}"
        )


def check_value_in_array(object_value, value, context_message=""):
    """
    Checks if the given value exists in the object_value array.

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``object_value``          | The array to search in.                                                      |
    | ``value``                 | The value to search for in the array.                                         |
    | ``context_message``       | Additional context for error messages (e.g., "at path 'value_path'").         |

    === Behavior: ===
    - If the array is a simple array (e.g., ["value1", "value2"]), it checks if the value exists.
    - If the array is an array of JSON objects (e.g., [{"key": "value1"}, {"key": "value2"}]), it checks if the value matches any JSON object in the array.

    Raises:
        skip: If the value is not found in the array or is incompatible with the array.
    """
    LOGGER.debug("Checking if value '%s' exists in array: %s", value, object_value)

    # Handle simple arrays (e.g., ["value1", "value2"])
    if all(not isinstance(item, dict) for item in object_value):
        if value not in object_value:
            skip(
                msg=f"Precondition failed: Value '{value}' not found in array {context_message}. Array: {object_value}"
            )
        return

    # Handle arrays of JSON objects (e.g., [{"key": "value1"}, {"key": "value2"}])
    if isinstance(value, dict):
        match_found = any(
            all(value.get(k) == item.get(k) for k in value.keys())
            for item in object_value
            if isinstance(item, dict)
        )
        if not match_found:
            skip(
                msg=f"Precondition failed: JSON object '{value}' not found in array {context_message}. Array: {object_value}"
            )
    else:
        skip(
            msg=f"Precondition failed: Value '{value}' is not compatible with the array {context_message}. Array: {object_value}"
        )


def parse_value_to_json(value):
    """
    Attempts to parse the given value as JSON if it looks like a JSON object.

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``value``                 | The value to parse.                                                          |

    === Behavior: ===
    - If the value is a string that starts with '{', it attempts to parse it as a JSON object.
    - If parsing is successful, the parsed dictionary is returned.
    - If parsing fails or the value is not a JSON string, the original value is returned.

    Returns:
        The parsed dictionary if the value is a valid JSON string, otherwise the original value.
    """
    if isinstance(value, str) and value.startswith("{"):
        try:
            parsed_value = json.loads(value)
            LOGGER.debug("Parsed value into dictionary: %s", parsed_value)
            return parsed_value
        except json.JSONDecodeError:
            LOGGER.debug("Value is not a valid JSON string: %s", value)
    return value


def find_matching_setting_with_criteria(
    param_name, application_name, criteria, skip_when_not_found=True
):
    """
    Finds a setting in the settings list from the active configuration
    where 'parameterName' matches the given param_name,
    'applicationName' matches the given application_name,
    and the 'criteria' matches the input criteria exactly.

    Args:
        param_name (str): The name of the parameter to search for.
        application_name (str): The name of the application to match.
        criteria (array):  list of criteria to match exactly.
        skip_when_not_found (bool): If True (default), skips the test when no matching setting is found.
                                    If False, returns None when no matching setting is found.

    Returns:
        dict: The matching setting if found, otherwise raises an error.
    """

    # Parse the input criteria if it is a JSON-like string
    if isinstance(criteria, str):
        try:
            criteria = json.loads(criteria)
            LOGGER.debug("Parsed input criteria into list: %s", criteria)
        except json.JSONDecodeError:
            LOGGER.debug("Input criteria is not a valid JSON string: %s", criteria)

    # Retrieve the active configuration from context_data
    context_data = session_manager.sessions._get_session_context_data()
    active_configuration = context_data.get("active_configuration", {})

    # Get the list of settings
    settings = active_configuration.get("settings", [])

    # Find the top-level matching setting
    matching_setting = next(
        (
            setting
            for setting in settings
            if setting.get("parameterName") == param_name
            and setting.get("applicationName") == application_name
        ),
        None,
    )

    if not matching_setting:
        if skip_when_not_found:
            skip(
                msg=f"Error evaluating precondition: no matching setting found for parameter '{param_name}' and application '{application_name}'."
            )
        return None

    # Drill down into children to find the setting with matching criteria
    def find_in_children(setting, criteria):
        if setting.get("criteria") == criteria:
            return setting
        for child in setting.get("children", []):
            result = find_in_children(child, criteria)
            if result:
                return result
        return None

    # At this point, matching_setting is guaranteed to be found and we can begin to evaluate the criteria
    result = find_in_children(matching_setting, criteria)
    if not result:
        if skip_when_not_found:
            skip(
                msg=f"Error evaluating precondition: no matching setting found for parameter '{param_name}', application '{application_name}', and criteria {criteria}"
            )
        return None

    return result


def find_matching_toggle(toggle_name, application_name, skip_when_not_found=True):
    """
    Finds a toggle in the toggles configuration
    where 'applicationName' matches the given application_name and
    'parameterName' matches the given toggle_name.

    Args:
        toggle_name (str): The name of the toggle to search for.
        application_name (str): The name of the application to match.
        skip_when_not_found (bool): If True (default), skips the test when no matching setting is found.
                                    If False, returns None when no matching setting is found.

    Returns:
        dict: The matching toggle if found, otherwise test execution is interrupted.
    """

    # Retrieve the toggles configuration from context_data
    context_data = session_manager.sessions._get_session_context_data()
    toggles_configuration = context_data.get("toggles_configuration", {})

    # Get the list of settings
    settings = toggles_configuration.get("settings", [])

    # Find the matching setting by application_name
    matching_setting = next(
        (
            setting
            for setting in settings
            if setting.get("applicationName") == application_name
        ),
        None,
    )

    if not matching_setting:
        if skip_when_not_found:
            skip(
                msg=f"Precondition failed: No matching toggles found for application '{application_name}'."
            )
        return None

    # Find the toggle in the children of the matching setting
    matching_toggle = next(
        (
            child
            for child in matching_setting.get("children", [])
            if child.get("parameterName") == toggle_name
        ),
        None,
    )

    if not matching_toggle:
        if skip_when_not_found:
            skip(
                msg=f"Precondition failed: No matching toggle found for toggle_name '{toggle_name}' in application '{application_name}'."
            )
        return None

    return matching_toggle
