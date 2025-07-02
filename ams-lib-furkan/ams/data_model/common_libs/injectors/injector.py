"""Injector module to handle generic calls"""

import logging
import protocols.broker
from ams.data_model.common_libs.injectors.injector_rest import injector as rest_injector


# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def _http_call(path, **kwargs):
    """
    Executes a HTTP call using the provided path.

    Args:
        path (str): The endpoint path for the API call.
        **kwargs: Additional options for the call. The following keys are supported:
            - path_params (dict): Dictionary of path parameters to replace placeholders in the path (e.g., {"id": 123} for /user/{id}).
            - query_params (dict): Dictionary of query parameters to be appended to the request.
            - operation (str): The HTTP operation to perform. Default is "GET".
            - json_response (bool): If the response should be automatically deserialized from Json. Default is True

    Returns:
        dict or None: The JSON response from the API if the call is successful and returns content,
                      None if the response status code is 204 (No Content).

    Raises:
        ValueError: If the response status code is not 200 or 204.

    Usage:
        Http Call    path=/configuration/admin/rest/v1/configuration/list
        Http Call    path=/configuration/admin/rest/v2/configuration/{conf_id}    path_params=${additional_params}
    """
    kwargs["path"] = f"{path}"
    response = protocols.broker.injector(kwargs, "defaultKey", rest_injector)

    LOGGER.debug(
        "HTTP Call: %s, Response: %s.",
        kwargs["path"],
        response.status_code,
    )

    if response.status_code != 200 and response.status_code != 204:
        raise ValueError(
            f"Call to {kwargs['path']} failed with status {response.status_code}"
        )

    if response.status_code == 204:
        return None

    if kwargs.get("json_response", True):
        return response.json()
    else:
        return response.text


def _http_call_and_check(path, field="generalProcessingStatus", value="OK", **kwargs):
    """
    Executes a HTTP call and validates the response with the given field and value.

    Args:
        path (str): The endpoint path for the API call.
        field (str): The response field to check for validation. Default is "generalProcessingStatus".
        value (Any): The expected value for the response field. Default is "OK".
        **kwargs: Additional options for the call. The following keys are supported:
            - path_params (dict): Dictionary of path parameters to replace placeholders in the path (e.g., {"id": 123} for /user/{id}).
            - query_params (dict): Dictionary of query parameters to be appended to the request.
            - operation (str): The HTTP operation to perform. Default is "GET".

    Returns:
        dict or None: The JSON response from the API if the call is:
                      - successful
                      - the value fo the provided field matches the provided value; by default generalProcessingStatus is "OK"
                      None if the response status code is 204 (No Content).

    Raises:
        ValueError: If the response status code is not 200 or 204,
                    or if generalProcessingStatus in the response is not "OK".

    Usage:
        ${response}=    Fom Http Call    /fom/rest-services/v3/movements/internal-id/{id}    path_params=${additional_params}
    """
    response_json = _http_call(path, **kwargs)
    if response_json is not None and response_json.get(field) != value:
        raise ValueError(
            f"Call failed: {field}={response_json.get(field)}, "
            f"errors={response_json.get('generalErrorInformation')}"
        )
    return response_json
