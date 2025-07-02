"""Injector module to handle GET http calls from AMG"""

import logging
from ams.data_model.common_libs.injectors.injector import _http_call_and_check

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def amg_environments_config():
    """
    Executes a HTTP GET call to retrieve AMG environment configuration and validates the response.

    This function calls the endpoint /aodb/services/environment/config.
    The function checks that the response contains "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments.                                                     |

    === Usage: ===
    | ${response}    Amg Environments Config

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    amg_endpoint = "/aodb/services/environment/config"

    kwargs = {}

    response_json = _http_call_and_check(amg_endpoint, **kwargs)
    return response_json


def amg_components_version():
    """
    Executes a HTTP GET call to retrieve AMG components version and validates the response.

    This function calls the endpoint /aodb/services/environment/components/version.
    The function checks that the response contains "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments.                                                     |

    === Usage: ===
    | ${response}    Amg Environments Config

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    amg_endpoint = "/aodb/services/environment/components/version"

    kwargs = {}

    response_json = _http_call_and_check(amg_endpoint, **kwargs)
    return response_json


def amg_environment_season():
    """
    Executes a HTTP GET call to retrieve AMG environment season and validates the response.

    This function calls the endpoint /aodb/services/environment/season.
    The function checks that the response contains "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments.                                                     |

    === Usage: ===
    | ${response}    Amg Environments Config

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    amg_endpoint = "/aodb/services/environment/season"

    kwargs = {}

    response_json = _http_call_and_check(amg_endpoint, **kwargs)
    return response_json


def amg_column_config():
    """
    Executes a HTTP GET call to retrieve AMG column config and validates the response.

    This function calls the endpoint /aodb/services/environment/config/columnConfig.
    The function checks that the response contains "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments.                                                     |

    === Usage: ===
    | ${response}    Amg Environments Config

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    amg_endpoint = "/aodb/services/environment/config/columnConfig"

    kwargs = {}

    response_json = _http_call_and_check(amg_endpoint, **kwargs)
    return response_json


def amg_milestone():
    """
    Executes a HTTP GET call to retrieve AMG milestones and validates the response.

    This function calls the endpoint /aodb/services/configuration/lists/milestone.
    The function checks that the response contains "generalProcessingStatus" equal to "OK". If not, it raises a ValueError.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments.                                                     |

    === Usage: ===
    | ${response}    Amg Environments Config

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful and generalProcessingStatus is "OK", or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204, or if generalProcessingStatus in the response is not "OK".
    """
    amg_endpoint = "/aodb/services/configuration/lists/milestone"

    kwargs = {}

    response_json = _http_call_and_check(amg_endpoint, **kwargs)
    return response_json
