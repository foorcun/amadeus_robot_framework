"""
Commons module contains common functions, variables used by the injectors
"""

# pylint: disable=line-too-long
# pylint: disable = protected-access

import logging
import random
import jmespath
import jmespath.exceptions
from protocols import session_manager
from ams.data_model.common_libs.utils.date_handler import now_gmt
from ams.data_model.common_libs.utils.generic_helpers import (
    find_matching_setting,
    find_matching_setting_with_criteria,
    validate_data_type_and_setting_value,
    check_value_in_array,
    parse_value_to_json,
    find_matching_toggle,
)
from ams.initalize_ams_test.component_versions import parse_version
from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from ams.data_model.common_libs.utils.date_handler import (
    get_date as date_handler_get_date,
)
from ams.data_model.common_libs.utils.built_in_helpers import skip, get_var_value

LOGGER = logging.getLogger(__name__)


def generate_flight_number(length):
    """
    Generate a random flight number consisting of digits.
    If generated flight number is less than 3 digits, it will be padded with 0s.

    Args:
        length (int): The length of the flight number to generate.

    Returns:
        str: The generated flight number as a string.
    """
    return Gad.generate_flight_number(length)


def get_date(**kwargs):
    """
    Get a date relative to the given date and format it to the given format.
      - date: the reference date and can have the following values:
        - None: use now in GMT time so all relative time (hours, minutes, seconds,
          microseconds) would be from current time
        - date/datetime string: it will try to convert it to a real date object through all
          DateFormat
        - lambda/function: call it, it should return a date or datetime object
        - today_gmt: will get the current date without current time so all relative time
        (hours, minutes, seconds, microseconds) would be from 00:00:00
        - date/datetime object: just use it
      - week_day: if not None, the reference date will become the next given week day
      after the reference date
      - years, months, weeks, days, hours, minutes, seconds, microseconds: positive or
      negative integer to give a relative date from the reference one
      - date_format: the format in which to format the date, can be the following values:
        - None: return a datetime object
        - str/lamda/function: use the given function to format
        - DateFormat: format following the given format
    Examples:
      Lets assume that current datetime is 2020-12-25 14:30:45
      get_date(hours=6) --> 2020-12-25
      get_date(years=-5, hours=-6, date_format=DateFormat.DATETIME) --> 2015-12-25T08:30:45Z
      get_date(hours=6, date_format=DateFormat.DATETIME) --> 2020-12-25T20:30:45Z
      get_date(hours=6, date=today_gmt, date_format=DateFormat.DATETIME) --> 2020-12-25T06:00:00Z
      get_date(hours=6, date='2020-12-25', date_format=DateFormat.DATETIME) -->
        2020-12-25T06:00:00Z
    """
    return date_handler_get_date(**kwargs)


def get_resource_id(response_json, return_type="list"):
    """
    Extracts the resource Id/s for any entity type from a JSON response.

    | *Arguments*               | *Description*                                                                             |

    | ``response_json``         | response object from any GET api call                                                     |
    | ``return_type``           | returns a list(default), comma separated string of resource Ids present in the response   |

    === Usage: ===
    | Get Resource Id    response_json=${response_json}    return_type=str  |

    """
    resource_id = jmespath.search(
        f"[?periods[?endDateTime == null || endDateTime > '{now_gmt()}']].id",
        response_json,
    )
    if return_type == "str":
        return ", ".join(resource_id)
    return resource_id


def get_random_resource_id(response_json):
    """
    Get any random resource id from the response.

    | *Arguments*               | *Description*                             |

    | ``response_json``         | response object from any GET api call     |

    === Usage: ===
    | Get Random Resource Id    response_json=${response_json}     |

    """
    resource_ids = get_resource_id(response_json)
    if not resource_ids:
        return None
    return random.choice(resource_ids)


def get_resource_name(response_json, return_type="list"):
    """
    Extracts the resource name/s for any entity from a JSON response.

    | *Arguments*               | *Description*                                                                                 |

    | ``response_json``         | response object from any GET api call                                                         |
    | ``return_type``           | returns a list(default), comma separated string of resource names present in the response     |

    === Usage: ===
    | Get Resource Name    response_json=${response_json}    return_type=str  |

    """
    resource_name = jmespath.search(
        f"[?periods[?endDateTime == null || endDateTime > '{now_gmt()}']].name",
        response_json,
    )
    if return_type == "str":
        return ", ".join(resource_name)
    return resource_name


def get_random_resource_name(response_json):
    """
    Extracts a random resource name from a JSON response.

    | *Arguments*               | *Description*                             |

    | ``response_json``         | response object from any GET api call     |

    === Usage: ===
    | Get Random Resource Name    response_json=${response_json}     |

    """
    resource_names = get_resource_name(response_json)
    if not resource_names:
        return None
    return random.choice(resource_names)


def get_resource_name_and_id(response_json):
    """
    Returns a list of dictionaries, each containing 'name' and 'id' of a resource entity from a JSON response.

    | *Arguments*               | *Description*                             |

    | ``response_json``         | response object from any GET api call     |

    === Usage: ===
    | Get Resource Name And Id    response_json=${response_json}     |

    """
    resource_name_id_list = jmespath.search(
        f"[?periods[?endDateTime == null || endDateTime > '{now_gmt()}']].{{name: name, id: id}}",
        response_json,
    )

    return resource_name_id_list


def get_resource_period_details(response_json, **kwargs):
    """
    Retrieve period details (periodId, startDateTime, and endDateTime) for any entity from a JSON response based on a given resource identifier.

    | ``response_json``                  | response object from any GET api call |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*                         | *Description*                                                                                         |

    | ``id``         | id of the resource       |
    | ``name``       | name of the resource     |

    """
    if "id" in kwargs:
        query = f"[?id=='{kwargs['id']}'].periods[].{{periodId: periodId, startDateTime: startDateTime, endDateTime: endDateTime}}"
    elif "name" in kwargs:
        query = f"[?name=='{kwargs['name']}'].periods[].{{periodId: periodId, startDateTime: startDateTime, endDateTime: endDateTime}}"
    else:
        raise ValueError(
            "Either 'id' or 'name' must be provided as a keyword argument."
        )

    period_details = jmespath.search(query, response_json)
    period_details_str = ", ".join(map(str, period_details))
    return period_details_str


def get_context():
    """
    Retrieves the current session context data.

    This function fetches the session context data from the session manager, which contains
    information about the current test session, such as active configurations, test context,
    and other session-specific details.

    === Usage: ===
    | ${context_data} =    Get Context

    === Example: ===
    | ${context_data} =    Get Context
    | Log    Active configuration: ${context_data["active_configuration"]}

    Returns:
        dict: A dictionary containing the session context data.
    """
    return session_manager.sessions._get_session_context_data()


def get_customer_id():
    """
    Retrieves the current customer id

    === Usage: ===
    | get_customer_id
    """
    return get_context()["test_context"]["generic_context"]["customer_id"]


def get_ref_airport_iata():
    """
    Retrieves the current reference airport IATA code
    """
    return get_context()["test_context"]["generic_context"]["ref_airport"]


def get_ref_airport_id():
    """
    Retrieves the current reference airport id
    """
    return get_context()["test_context"]["generic_context"]["ref_airport_full"]


def precondition_config_check(
    param_name,
    application_name,
    value,
    criteria=None,
    matching_setting=None,
    skip_when_not_found=True,
):
    """
    Retrieves a setting from the active configuration's settings list,
    compares its value with the input value based on the setting's data type,
    and skips the test is the values do not match.
    If the setting is not found the tests skips,
    but only if ``skip_when_not_found`` is True (default).
    Supported data types for this keyword are: BOOLEAN, INTEGER, and STRING.

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``param_name``            | The name of the parameter to search for in the settings list.                 |
    | ``application_name``      | The name of the application to match in the settings list.                    |
    | ``value``                 | The value to compare against the setting's value.                             |
    | ``criteria``              | The criteria to be used to look up the setting.                               |
    | ``matching_setting``      | Optional. A pre-fetched matching setting to use instead of finding one.       |
    | ``skip_when_not_found``   | If True (default), skips the test when no matching setting is found.          |

    === Usage: ===
    | Precondition Config Check    param_name=exampleParam    application_name=exampleApp    value=exampleValue |
    """

    # Find the matching setting
    if criteria:
        matching_setting = find_matching_setting_with_criteria(
            param_name, application_name, criteria, skip_when_not_found
        )
    elif not matching_setting:
        matching_setting = find_matching_setting(
            param_name, application_name, skip_when_not_found
        )

    # If no matching setting is found and the test is not skipped, return early
    if not matching_setting:
        LOGGER.warning(
            "No matching setting found for parameter '%s' and application '%s'. Test execution continues.",
            param_name,
            application_name,
        )
        return

    # Get the "value" of the setting or "defaultValue" if "value" is null
    setting_value = matching_setting.get("value") or matching_setting.get(
        "defaultValue"
    )

    # Get the "dataType" from the setting
    data_type = matching_setting.get("dataType", "").upper()

    # Compare the setting value with the input value based on the data type
    if data_type.upper() == "BOOLEAN":
        # Convert both values to boolean and compare
        try:
            setting_value = str(setting_value).lower()
            input_value = str(value).lower()
            if setting_value != input_value:
                skip(
                    msg=f"Precondition value [{input_value}] and parameter value [{setting_value}] do not match."
                )
        except ValueError:
            skip(msg="Error evaluating precondition.")

    elif data_type.upper() == "INTEGER":
        # Convert both values to integers and compare
        try:
            setting_value = int(setting_value)
            input_value = int(value)
            if setting_value != input_value:
                skip(
                    msg=f"Precondition value [{input_value}] and parameter value [{setting_value}] do not match."
                )
        except ValueError:
            skip(msg="Error evaluating precondition.")

    elif data_type.upper() == "STRING":
        # Compare both values as strings
        if str(setting_value) != str(value):
            skip(
                msg=f"Precondition value [{value}] and parameter value [{setting_value}] do not match."
            )

    else:
        # Unsupported data type
        raise ValueError(f"Unsupported data type: {data_type}")


def precondition_config_check_json(
    param_name,
    application_name,
    value_path,
    value,
    criteria=None,
    skip_when_not_found=True,
):
    """
    Retrieves a setting from the active configuration's settings list,
    validates that its value is a JSON object, and traverses the object using the given value_path
    to fetch a value for comparison. If the fetched value is an array, it checks if the array contains the input value.
    If the value does not match the test is skipped.
    If the setting is not found the tests skips,
    but only if ``skip_when_not_found`` is True (default).

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``param_name``            | The name of the parameter to search for in the settings list.                 |
    | ``application_name``      | The name of the application to match in the settings list.                    |
    | ``value_path``            | The path to traverse the JSON object to fetch the value for comparison.       |
    | ``value``                 | The value to compare against the fetched value from the JSON object.          |
    | ``criteria``              | The criteria to be used to look up the setting.                               |
    | ``skip_when_not_found``   | If True (default), skips the test when no matching setting is found.          |

    === Behavior: ===
    - If the fetched value is not an array, it is compared directly with the input value.
    - If the fetched value is an array:
        - For simple arrays (e.g., ["value1", "value2"]), the method checks if the input value exists in the array.
        - For arrays of JSON objects (e.g., [{"key": "value1"}, {"key": "value2"}]), the method checks if the input value matches any JSON object in the array.

    === Usage: ===
    | Precondition Config Check Json    param_name=exampleParam    application_name=exampleApp    value_path=path.to.value    value=expectedValue |

    === Examples: ===
    1. **Direct Comparison**:
       - Setting Value: {"encryption": {"expiryPlusMonths": 2}}
       - Input Value: {"expiryPlusMonths": 2}
       - Value Path: "encryption"
       - Result: Passes if the fetched value matches the input value.

    2. **Simple Array**:
       - Setting Value: {"encryption": ["AES", "RSA", "DES"]}
       - Input Value: "AES"
       - Value Path: "encryption"
       - Result: Passes if the input value exists in the array.

    3. **Array of JSON Objects**:
       - Setting Value: {"encryption": [{"expiryPlusMonths": 2}, {"expiryPlusMonths": 3}]}
       - Input Value: {"expiryPlusMonths": 2}
       - Value Path: "encryption"
       - Result: Passes if the input JSON object matches any object in the array.

    4. **Incompatible Types**:
       - Setting Value: {"encryption": [{"expiryPlusMonths": 2}, {"expiryPlusMonths": 3}]}
       - Input Value: "expiryPlusMonths"
       - Value Path: "encryption"
       - Result: Skips the test with a message indicating that the input value is not compatible with the array.

    === Notes: ===
    - If the input value is a string that looks like a JSON object (e.g., '{"key": "value"}'), the method attempts to parse it into a dictionary.
    """

    # Parse the value as JSON if applicable
    value = parse_value_to_json(value)

    # Find the matching setting
    if criteria:
        matching_setting = find_matching_setting_with_criteria(
            param_name, application_name, criteria, skip_when_not_found
        )
    else:
        matching_setting = find_matching_setting(
            param_name, application_name, skip_when_not_found
        )

    # If no matching setting is found and the test is not skipped, return early
    if not matching_setting:
        LOGGER.warning(
            "No matching setting found for parameter '%s' and application '%s'. Test execution continues.",
            param_name,
            application_name,
        )
        return

    # Get the "value" of the setting or "defaultValue" if "value" is null
    setting_value = matching_setting.get("value") or matching_setting.get(
        "defaultValue"
    )

    # Get the "dataType" from the setting
    data_type = matching_setting.get("dataType", "").upper()

    # Validate data type and setting value
    validate_data_type_and_setting_value(data_type, setting_value, dict, "JSON")

    # Traverse the JSON object using the value_path
    try:
        object_value = jmespath.search(value_path, setting_value)
    except jmespath.exceptions.JMESPathError as e:
        skip(
            msg=f"Precondition failed: Error traversing JSON object with path '{value_path}'. Error: {str(e)}"
        )

    # Check if the value was found
    if object_value is None:
        skip(
            msg=f"Precondition failed: Path '{value_path}' not found in JSON object. Object: {setting_value}"
        )

    # Handle cases where object_value is an array
    if isinstance(object_value, list):
        LOGGER.debug("Object value is an array: %s", object_value)
        check_value_in_array(object_value, value, f"at path '{value_path}'")
        return

    # If object value is not an array, convert both values to strings and compare
    if str(object_value).lower() != str(value).lower():
        skip(
            msg=f"Precondition failed: Value at path '{value_path}' ({object_value}) does not match expected value ({value})."
        )


def precondition_config_check_array(
    param_name, application_name, value, criteria=None, skip_when_not_found=True
):
    """
    Retrieves a setting from the active configuration's settings list,
    validates that its value is a JSON array, and checks if the array contains the input value.
    The method supports both simple strings and JSON objects as input values.
    If the value does not match or is not found, the test is skipped.
    If the setting is not found the tests skips,
    but only if ``skip_when_not_found`` is True (default).

    | *Arguments*               | *Description*                                                                      |
    |---------------------------|------------------------------------------------------------------------------------|
    | ``param_name``            | The name of the parameter to search for in the settings list.                      |
    | ``application_name``      | The name of the application to match in the settings list.                         |
    | ``value``                 | The value to check for in the JSON array. Can be a simple string or a JSON object. |
    | ``criteria``              | The criteria to be used to look up the setting.                                    |
    | ``skip_when_not_found``   | If True (default), skips the test when no matching setting is found.               |

    === Behavior: ===
    - If the setting value is a simple array (e.g., ["value1", "value2"]), the method checks if the input value exists in the array.
    - If the setting value is an array of JSON objects (e.g., [{"key": "value1"}, {"key": "value2"}]), the method checks if the input value matches any JSON object in the array.

    === Usage: ===
    | Precondition Config Check Array    param_name=exampleParam    application_name=exampleApp    value=exampleValue        |
    | Precondition Config Check Array    param_name=exampleParam    application_name=exampleApp    value={"key": "value"}    |

    === Examples: ===
    1. **Simple Array**:
       - Setting Value: ["Jet A-1", "Jet B", "Avgas 100 LL"]
       - Input Value: "Jet A-1"
       - Result: Passes - "Jet A-1" exists in the array.

    2. **Array of JSON Objects**:
       - Setting Value: [{"label": "J.seat", "value": "Jumpseat"}, {"label": "Infant", "value": "Infant"}]
       - Input Value: {"label": "J.seat", "value": "Jumpseat"}
       - Result: Passes - the input JSON object matches an object in the array.

    3. **Invalid Input**:
       - Setting Value: [{"label": "J.seat", "value": "Jumpseat"}]
       - Input Value: "Jumpseat"
       - Result: Skips the test with a message indicating that the input value is not compatible with the setting array.

    === Notes: ===
    - If the input value is a string that looks like a JSON object (e.g., '{"key": "value"}'), the method attempts to parse it into a dictionary.
    """

    # Parse the value as JSON if applicable
    value = parse_value_to_json(value)

    # Find the matching setting
    if criteria:
        matching_setting = find_matching_setting_with_criteria(
            param_name, application_name, criteria, skip_when_not_found
        )
    else:
        matching_setting = find_matching_setting(
            param_name, application_name, skip_when_not_found
        )

    # If no matching setting is found and the test is not skipped, return early
    if not matching_setting:
        LOGGER.warning(
            "No matching setting found for parameter '%s' and application '%s'. Test execution continues.",
            param_name,
            application_name,
        )
        return

    # Get the "value" of the setting or "defaultValue" if "value" is null
    setting_value = matching_setting.get("value") or matching_setting.get(
        "defaultValue"
    )

    # Get the "dataType" from the setting
    data_type = matching_setting.get("dataType", "").upper()

    # Validate data type and setting value
    validate_data_type_and_setting_value(data_type, setting_value, list, "JSON")

    # Look for the value in the setting array
    check_value_in_array(setting_value, value, "in setting array")


def precondition_toggle_check(
    toggle_name, application_name, value, skip_when_not_found=True
):
    """
    Retrieves a toggle from the toggles configuration,
    compares its value with the input value,
    and skips the test is the values do not match.
    If the toggle is not found the tests skips,
    but only if ``skip_when_not_found`` is True (default).

    | *Arguments*               | *Description*                                                         |
    |---------------------------|-----------------------------------------------------------------------|
    | ``toggle_name``           | The name of the toggle to search for.                                 |
    | ``application_name``      | The name of the application to match f or this toggle.                |
    | ``value``                 | The value to compare against the toggle's value.                      |
    | ``skip_when_not_found``   | If True (default), skips the test when no matching setting is found.  |

    === Usage: ===
    | Precondition Toggle Check    toggle_name=exampleToggle    application_name=exampleApp    value=exampleValue  |
    """

    # Find the matching toggle
    matching_toggle = find_matching_toggle(
        toggle_name, application_name, skip_when_not_found
    )

    # If no matching toggle is found and the test is not skipped, return early
    if not matching_toggle:
        LOGGER.warning(
            "No matching toggle found for toggle_name '%s' and application '%s'. Test execution continues.",
            toggle_name,
            application_name,
        )
        return

    # Use precondition_config_check with the matching toggle
    precondition_config_check(
        param_name=toggle_name,
        application_name=application_name,
        value=value,
        matching_setting=matching_toggle,
    )


def precondition_applications_deployed(applications):
    """
    Skips this test if the list of applications expected to be deployed in the environment the test
    is executed against does not contain all the applications this test requires to be deployed.

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``applications``          | A comma separated list of applications required to be deployed for this test  |

    === Usage: ===
    | Precondition Applications Deployed    applications=FOM, SDS, FRMS                                         |
    | Precondition Applications Deployed    FOM, SDS, FRMS                                                      |
    """

    deployed_applications_var = get_var_value("$DEPLOYED_APPLICATIONS")
    deployed_applications = (
        []
        if deployed_applications_var is None
        else [
            value.strip()
            for value in deployed_applications_var.split(",")
            if value.strip()
        ]
    )

    required_applications = [
        value.strip() for value in applications.split(",") if value.strip()
    ]

    not_deployed_applications = [
        required_application
        for required_application in required_applications
        if required_application not in deployed_applications
    ]

    if not_deployed_applications:
        skip(
            msg=f"Precondition failed: The following applications are not deployed: {','.join(not_deployed_applications)}"
        )


def precondition_esb_interfaces_deployed(interfaces):
    """
    Skips this test if the list of ESB interfaces expected to be deployed in the environment the test
    is executed against does not contain all the ESB interfaces this test requires to be deployed.

    | *Arguments*               | *Description*                                                                 |
    |---------------------------|-------------------------------------------------------------------------------|
    | ``interfaces``          | A comma separated list of ESB interfaces required to be deployed for this test  |

    === Usage: ===
    | Precondition Esb Interfaces Deployed    interfaces=FIDS, NOAA                                             |
    | Precondition Esb Interfaces Deployed    FIDS, NOAA                                                        |
    """

    deployed_interfaces_var = get_var_value("$DEPLOYED_ESB_INTERFACES")
    deployed_interfaces = (
        []
        if deployed_interfaces_var is None
        else [
            value.strip()
            for value in deployed_interfaces_var.split(",")
            if value.strip()
        ]
    )

    required_interfaces = [
        value.strip() for value in interfaces.split(",") if value.strip()
    ]

    not_deployed_interfaces = [
        required_interface
        for required_interface in required_interfaces
        if required_interface not in deployed_interfaces
    ]

    if not_deployed_interfaces:
        skip(
            msg=f"Precondition failed: The following ESB interfaces are not deployed: {','.join(not_deployed_interfaces)}"
        )


def precondition_component_version_check(component, version_min, version_max=None):
    """
    Precondition Component Version Check (component, version_min, and version_max) to skip a test if the component version is out of range
    version_max does not check equals, so if functionality is removed in 9.3.x then version_max should be sent in as 9.3 to skip the test if the component is 9.3 or higher

    | *Arguments*               | *Description*                                                         |
    |---------------------------|-----------------------------------------------------------------------|
    | ``component``             | short letter code of the component. e.g. FOM, FIDS       |
    | ``version_min``           | minimum version of the component                         |
    | ``version_max``           | optional maximum version of the component                |

    === Usage: ===
    | Precondition Component Version Check   component=FOM version_min=9.3.2
    """
    LOGGER.debug(
        "Performing component version check %s %s %s",
        component,
        version_min,
        version_max,
    )

    # get versions stored in the context
    context_data = session_manager.sessions._get_session_context_data()
    component_versions = context_data.get("component_versions", {})

    if component_versions.get(component) is None:
        skip(msg=f"Component {component} is not loaded in this environment")

    # convert to ComponentVersions
    component_version = parse_version(component_versions[component])
    version_min = parse_version(version_min)

    # check min version
    if component_version <= version_min:
        skip(
            msg=f"Component {component} with version {component_version} does not meet the min version {version_min}"
        )

    # check max version
    if version_max:
        version_max = parse_version(version_max)
        if component_version > version_max:
            skip(
                msg=f"Component {component} with version {component_version} exceeds the max version {version_max}"
            )
