"""
REST injector
"""

import logging
from protocols.decorators import RestInjector

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access


@RestInjector
def injector(kwargs, session_key):

    rest_details = {
        "operation": kwargs["operation"],
        "params": kwargs.get("params", {}),
        "path": kwargs["path"],
        "data": kwargs.get("payload", None),
        "verify": False,
    }

    LOGGER.debug("REST Details: %s", rest_details)

    return rest_details
