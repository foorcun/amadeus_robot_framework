import logging
from protocols.decorators import RestInjector

LOGGER = logging.getLogger(__name__)


# pylint: disable=unused-argument, unused-variable, protected-access


@RestInjector
def injector(kwargs, session_key):

    is_form_url_encoded = (
        kwargs.get("headers", {}).get("Content-Type", None)
        == "application/x-www-form-urlencoded"
    )

    rest_details = {
        "operation": kwargs["operation"],
        "headers": kwargs.get("headers", {}),
        "params": kwargs.get("params", {}),
        "path": kwargs["path"],
        "json": kwargs.get("payload", None) if not is_form_url_encoded else None,
        "data": kwargs.get("payload", None) if is_form_url_encoded else None,
        "verify": False,
    }

    LOGGER.debug("REST Details: %s", rest_details)

    return rest_details
