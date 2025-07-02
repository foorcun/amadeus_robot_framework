"""
REST injector for generic calls
"""

import logging
from protocols.decorators import RestInjector
from ams.data_model.common_libs.utils import generic_helpers as helpers

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access


@RestInjector
def injector(kwargs, session_key):
    path_params = kwargs.get("path_params", {})
    if path_params:
        for key, value in path_params.items():
            kwargs["path"] = kwargs["path"].replace(f"{{{key}}}", str(value))

    query_params = helpers.build_query_param_string(
        kwargs.get("query_params", {}), return_type="dict"
    )

    rest_details = {
        "operation": kwargs.get("operation", "GET"),
        "params": query_params,
        "path": kwargs["path"],
        "data": kwargs.get("payload", None),
        "verify": False,
    }

    LOGGER.debug("REST Details: %s", rest_details)

    return rest_details
