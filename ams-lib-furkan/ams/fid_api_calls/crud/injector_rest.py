"""
REST injector for FIDS CRUD calls
"""

import logging
import json
from protocols.decorators import RestInjector
from protocols import session_manager
from ams.data_model.common_libs.utils import generic_helpers as helpers

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access

# All endpoints handled by the injector
FIDS_ENDPOINTS = {
    "read": "/fids/api/data/",
    "save": "/fids/api/putdata",
    "delete": "/fids/api/putdata",
    "login": "/fids/api/login",
    "functions": "/fids/api/functions",
    "logout": "/fids/api/logout",
    "media_upload": "/fids/ng/media",
    "updates": "/fids/api/updates",
    "close": "/fids/api/closedata",
    "execute_function": "/fids/api/executefunction",
    "download_template": "/fids/ng/customerData/downloadTemplate",
    "export": "/fids/ng/transfer/export",
    "import_template": "/fids/ng/customerData/uploadValidateAndImportTemplateAsync",
    "import": "/fids/ng/transfer/import",
    "import_poll": "/fids/ng/customerData/poll",
}


@RestInjector
def injector(kwargs, session_key="defaultKey"):
    """
    REST injector

    # arguments can be passed from the main injector.py
    arg1 = kwargs["args1"]
    arg2 = kwargs["args2"]
    """

    context_data = session_manager.sessions._get_session_context_data()

    expected_response_code = kwargs.get("expected_response_code", "200")
    endpoint_type = kwargs.get("endpoint_type")

    # Login call (goes to AAA)
    if endpoint_type == "login":
        return {
            "operation": "POST",
            "path": f"{FIDS_ENDPOINTS.get('login')}",
            "expected_status_code": expected_response_code,
            "verify": False,
            "headers": kwargs.get("headers", {}),
        }
    # Logout call (goes to AAA)
    elif endpoint_type == "logout":
        return {
            "operation": "GET",
            "path": f"{FIDS_ENDPOINTS.get('logout')}",
            "expected_status_code": expected_response_code,
            "verify": False,
            "headers": kwargs.get("headers", {}),
        }

    view = {}

    # setup url query parameters when in kwargs
    if kwargs.get("view") is not None:
        view["view"] = kwargs.get("view")
    if kwargs.get("fields") is not None:
        view["fields"] = kwargs.get("fields")
    if kwargs.get("where") is not None:
        view["where"] = kwargs.get("where")
    if kwargs.get("parameters") is not None:
        view["parameters"] = kwargs.get("parameters")
    if kwargs.get("order_by") is not None:
        view["order_by"] = kwargs.get("order_by")
    if kwargs.get("store_id") is not None:
        view["storeId"] = kwargs.get("store_id")
    if kwargs.get("function") is not None:
        view["function"] = kwargs.get("function")

    query_param = helpers.build_query_param_string(
        {
            **{
                "hopoICAO": context_data.get("test_context", {})
                .get("generic_context", {})
                .get("ref_airport")
            },
            **(kwargs.get("additional_params", {}) or {}),
            **view,
        }
    )

    endpoint = f"{FIDS_ENDPOINTS.get(endpoint_type)}"

    # setup final rest details for the endpoint_type
    headers = kwargs.get("headers", {})
    payload = None
    files = None
    if endpoint_type == "save":
        operation = "POST"
        payload = json.dumps({"action": "U", "payload": kwargs.get("entity")})
    elif (
        endpoint_type == "media_upload"
        or endpoint_type == "import"
        or endpoint_type == "import_template"
    ):
        # upload media and import files in using the form data
        operation = "POST"
        headers["Content-Type"] = None  # it will set to json otherwise
        files = {
            "file": (
                kwargs.get("file_name"),
                kwargs.get("payload"),
                kwargs.get("content_type"),
            )
        }
    elif endpoint_type == "delete":
        operation = "POST"
        payload = json.dumps({"action": "D", "payload": kwargs.get("entity")})
    elif endpoint_type == "close" or endpoint_type == "execute_function":
        operation = "POST"
    else:
        operation = "GET"

    rest_details = {
        "operation": operation,
        "params": query_param,
        "path": endpoint,
        "expected_status_code": expected_response_code,
        "verify": False,
        "headers": headers,
        "data": payload,
        "files": files,
    }

    LOGGER.debug("REST Details for the FIDS call: %s", rest_details)

    return rest_details
