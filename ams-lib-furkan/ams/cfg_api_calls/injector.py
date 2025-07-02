"""Injector module to handle GET http calls from CFG"""

import logging
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def cfg_v1_get_configurations():
    """
    Executes a HTTP GET call to retrieve CFG v1 configurations.

    This function calls the endpoint /configuration/admin/rest/v1/configuration/list.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cfg V1 Get Configurations

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cfg_endpoint = "/configuration/admin/rest/v1/configuration/list"

    kwargs = {}

    response_json = _http_call(cfg_endpoint, **kwargs)
    return response_json


def cfg_v1_get_configuration():
    """
    Executes a HTTP GET call to retrieve CFG v1 configuration.

    This function calls the endpoint /configuration/admin/rest/v1/configuration.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cfg V1 Get Configuration

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cfg_endpoint = "/configuration/admin/rest/v1/configuration"

    kwargs = {}

    response_json = _http_call(cfg_endpoint, **kwargs)
    return response_json


def cfg_v2_get_configuration():
    """
    Executes a HTTP GET call to retrieve CFG v2 configuration.

    This function calls the endpoint /configuration/admin/rest/v2/configuration/{conf_id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cfg V2 Get Configuration

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    context_data = session_manager.sessions._get_session_context_data()
    cfg_endpoint = "/configuration/admin/rest/v2/configuration/{conf_id}"

    customer_id = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id", "")
    )

    kwargs = {"path_params": {"conf_id": customer_id}}

    response_json = _http_call(cfg_endpoint, **kwargs)
    return response_json


def cfg_v2_get_features():
    """
    Executes a HTTP GET call to retrieve CFG v2 features.

    This function calls the endpoint /configuration/admin/rest/v2/features.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cfg V2 Get Features

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cfg_endpoint = "/configuration/admin/rest/v2/features"

    kwargs = {}

    response_json = _http_call(cfg_endpoint, **kwargs)
    return response_json


def cfg_v2_get_configuration_application(component="COMMON", revision="-1"):
    """
    Executes a HTTP GET call to retrieve CFG v2 configuration application.

    This function calls the endpoint /configuration/admin/rest/v2/configuration-application/{configuration}/{component}/{revision}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cfg V2 Get Configuration Application

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    context_data = session_manager.sessions._get_session_context_data()
    cfg_endpoint = "/configuration/admin/rest/v2/configuration-application/{configuration}/{component}/{revision}"

    customer_id = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id", "")
    )

    kwargs = {
        "path_params": {
            "configuration": customer_id,
            "component": component,
            "revision": revision,
        }
    }

    response_json = _http_call(cfg_endpoint, **kwargs)
    return response_json


def cfg_v2_get_parameter_in_configuration(component, param):
    """
    Retrieves a specific parameter/setting from the CFG v2 configuration application for the given component.

    This function calls cfg_v2_get_configuration_application to get the configuration for the specified component,
    then searches for the setting with the given parameter name.

    | *Arguments*      | *Description*                                                       |
    |------------------|---------------------------------------------------------------------|
    | ``component``    | The component name to search in the configuration (e.g., "COMMON")  |
    | ``param``        | The parameter name to find in the settings                          |

    === Usage: ===
    | ${setting}    Cfg V2 Get Parameter In Configuration    component=COMMON    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD

    === Returns: ===
    | dict | The setting dictionary for the specified parameter if found.

    === Raises: ===
    | ValueError | If no configuration is found for the customer or if the parameter is not found.
    """
    context_data = session_manager.sessions._get_session_context_data()
    # Get the working configuration for customer_id and component
    customer_id = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id", "")
    )
    configuration_for_customer = cfg_v2_get_configuration_application(component)
    if configuration_for_customer is None:
        raise ValueError(f"No configurations found for customer_id: {customer_id}")

    # Find the parameter in the configuration
    settings = configuration_for_customer.get("settings", [])
    target_setting = next(
        (s for s in settings if s.get("parameterName") == param), None
    )
    if target_setting is None:
        raise ValueError(f"Could not find parameter: {param}")

    LOGGER.info("Found setting: %s", target_setting)
    return target_setting


def cfg_v1_update_parameter(component, param, value):
    """
    Updates a specific parameter/setting in the CFG v1 configuration.

    This function finds the current setting for the given component and parameter,
    prepares an updated payload with the new value, and sends a POST request to update the setting
    by calling endpoint /configuration/admin/rest/v1/setting/{configurationName}/{applicationName}/{settingName}.save

    | *Arguments*      | *Description*                                                       |
    |------------------|---------------------------------------------------------------------|
    | ``component``    | The component name to update in the configuration (e.g., "COMMON")  |
    | ``param``        | The parameter name to update in the settings                        |
    | ``value``        | The new value to set for the parameter                              |

    === Usage: ===
    | ${response}    Cfg V1 Update Parameter    component=COMMON    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD    value=17

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the parameter is not found or if the response status code is not 200 or 204.
    """
    context_data = session_manager.sessions._get_session_context_data()
    cfg_endpoint = "/configuration/admin/rest/v1/setting/{configurationName}/{applicationName}/{settingName}.save"
    customer_id = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id", "")
    )

    # Find the parameter to update
    target_setting = cfg_v2_get_parameter_in_configuration(component, param)

    LOGGER.info("Updating setting: %s", target_setting)

    # Prepare the payload for the update
    payload = {
        "configuration": customer_id,
        "component": component,
        "parameterName": target_setting.get("parameterName"),
        "value": value,
        "revision": target_setting.get("revision"),
    }
    gen_payload = PayloadGenerator(payload, "payloads/setting.jinja", __file__)
    entity = gen_payload.construct_generic_payload()

    kwargs = {
        "operation": "POST",
        "path_params": {
            "configurationName": customer_id,
            "applicationName": component,
            "settingName": param,
        },
        "payload": entity,
    }

    return _http_call(cfg_endpoint, **kwargs)


def cfg_v2_publish_configuration(configuration, revision):
    """
    Publishes a CFG v2 configuration with a specific revision.

    This function calls the endpoint /configuration/admin/rest/v2/configuration/{configurationName}/{revision}/activate
    to publish the specified configuration with the working revision.

    | *Arguments*         | *Description*                                                        |
    |---------------------|----------------------------------------------------------------------|
    | ``configuration``   | The configuration name to publish                                    |
    | ``revision``        | The revision number of the configuration to publish                  |

    === Usage: ===
    | ${response}    Cfg V2 Publish Configuration    configuration=1A    revision=8

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cfg_endpoint = "/configuration/admin/rest/v2/configuration/{configurationName}/{revision}/activate"

    kwargs = {
        "operation": "POST",
        "path_params": {"configurationName": configuration, "revision": revision},
    }

    return _http_call(cfg_endpoint, **kwargs)
