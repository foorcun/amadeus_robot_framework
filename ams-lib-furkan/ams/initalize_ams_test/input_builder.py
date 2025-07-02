# pylint:disable=line-too-long
# pylint: disable = protected-access

"""
This module contains helper functions used for ams tests initialization
"""
import logging
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call

LOGGER = logging.getLogger(__name__)


def _get_configuration(
    customer_id,
    conf_endpoint,
    context_key="active_configuration",
):
    """
    Retrieves the configuration for a customer based on the provided customer_id.

    This function makes API calls to retrieve the configuration for the given customer_id
    and stores it in the context data.

    == Arguments ==
    | customer_id (str)
    | The customer ID for which the configuration is to be retrieved.

    | session_key (str)
    | The session key to use for the API calls. Defaults to "defaultKey".

    == Return value ==
    | None
    | The function does not return any value. It updates the context data with the
    | configuration if it is successfully retrieved.

    == Dependencies ==
    | `context_data`
    | Context data must be available to store the configuration.
    """

    LOGGER.info("Getting active configuration")

    # Retrieve context_data
    context_data = session_manager.sessions._get_session_context_data()

    # Initialize kwargs
    kwargs = {"path_params": {"conf_id": customer_id}}

    configurations_for_customer_endpoint = (
        "/configuration/admin/rest/v2/configuration/{conf_id}"
    )

    # Get the full response payload
    payload = _http_call(configurations_for_customer_endpoint, **kwargs)

    # Extract the list of revisions
    revisions = payload.get("revisions", [])

    # Find the object where "active": true
    active_revision = next(
        (rev for rev in revisions if rev.get("active") is True), None
    )
    if active_revision:
        # Extract the 'id' from the active revision
        active_revision_id = active_revision.get("id")

        # Update kwargs for the next call
        kwargs = {
            "path_params": {"conf_id": customer_id, "revision_id": active_revision_id}
        }

        # Make another call to get the active configuration
        active_configuration = _http_call(conf_endpoint, **kwargs)

        if active_configuration:
            # Store the active configuration in context_data
            context_data[context_key] = active_configuration
            LOGGER.info("Active configuration stored in context_data.")

        else:
            LOGGER.warning(
                "Failed to retrieve active configuration. Status code: %s",
                active_configuration.status_code,
            )

    else:
        LOGGER.warning("No active revision found.")


def _get_active_configuration():
    """
    Retrieves the active configuration for a customer based on the context data.

    This function checks if the `active_configuration` is already present in the context data.
    If it is present, the function skips execution and logs that the active configuration
    is already available. Otherwise, it retrieves the active configuration by making API calls
    and stores it in the context data.

    == Arguments ==
    | session_key (str)
    | The session key to use for the API calls. Defaults to "defaultKey".

    == Return value ==
    | None
    | The function does not return any value. It updates the context data with the
    | active configuration if it is successfully retrieved.
    """
    LOGGER.info("Getting active configuration")

    # Retrieve context_data
    context_data = session_manager.sessions._get_session_context_data()

    # Check if active_configuration is already present
    if context_data.get("active_configuration"):
        LOGGER.info(
            "Skipping getting active configuration as it is already present in context_data."
        )
        return

    # Get the customer_id from context_data
    customer_id = (
        context_data.get("test_context", {})
        .get("generic_context", {})
        .get("customer_id", "")
    )

    # Call the shared _get_configuration function
    active_configuration_endpoint = "/configuration/admin/rest/v2/configuration-without-application/{conf_id}/{revision_id}"
    _get_configuration(customer_id, active_configuration_endpoint)


def _get_toggles_configuration():
    """
    Retrieves the toggles configuration for customer ID "1A".
    This function checks if the `toggles_configuration` is already present in the context data.
    If it is present, the function skips.

    == Arguments ==
    | session_key (str)
    | The session key to use for the API calls. Defaults to "defaultKey".

    == Return value ==
    | None
    | The function does not return any value. It updates the context data with the
    | toggles configuration if it is successfully retrieved.
    """
    LOGGER.info("Getting toggles configuration for customer_id: '1A'")

    # Retrieve context_data
    context_data = session_manager.sessions._get_session_context_data()

    # Check if toggles_configuration is already present
    if context_data.get("toggles_configuration"):
        LOGGER.info(
            "Skipping getting toggles configuration as it is already present in context_data."
        )
        return

    # Use customer_id "1A"
    customer_id = "1A"

    # Use the endpoint to fetch toggles configuration
    toggles_conf_endpoint = "/configuration/admin/rest/v2/configuration-without-application-for-toggles/{conf_id}/{revision_id}"

    # Use a different context_key to store the toggles in the context data
    context_key = "toggles_configuration"

    # Call the shared _get_configuration function
    _get_configuration(customer_id, toggles_conf_endpoint, context_key)
