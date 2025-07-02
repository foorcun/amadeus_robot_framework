"""Injector module to handle health check of AMS components"""

import logging
from ams.data_model.common_libs.injectors.injector import _http_call

LOGGER = logging.getLogger(__name__)

# Health endpoints mapping
HEALTH_ENDPOINTS = {
    "aaa": "/authentication/agent/monitor/health/readiness",
    "afv": "/afv/agent/monitor/health/readiness",
    "amg": "/aodb/agent/monitor/health/readiness",
    "amo": "/aptMonitoring/aptMonitoringApp/agent/monitor/health/readiness",
    "cds": "/cds/agent/monitor/health/readiness",
    "cfg": "/configuration/agent/monitor/health/readiness",
    "csv": "/coreServices/agent/monitor/health/readiness",
    "dfib": "/dfib/agent/monitor/health/readiness",
    "esb": "/esb4/api/node/cluster/summary/validate",
    "fds": "/fds/agent/monitor/health/readiness",
    "fid": "/fids/admin/health/readiness",
    "fom": "/fom/agent/monitor/health/readiness",
    "lcx": "/lcx/agent/monitor/health/readiness",
    "mb": "/mb/agent/monitor/health/readiness",
    "mbl": "/mbl/agent/monitor/health/readiness",
    "msc": "/msc/agent/monitor/health/readiness",
    "prw": "/propworks/agent/monitor/health/readiness",
    "psa": "/psa/agent/monitor/health/readiness",
    "sds": "/sds/agent/monitor/health/readiness",
    "sga": "/rm/agent/monitor/health/readiness",
    "tam": "/tam/agent/monitor/health/readiness",
    "vip": "/vip/agent/monitor/health/readiness",
}


def get_health_status(component_name):
    """
    Get the health status of a component by calling the readiness endpoint.

    == Arguments ==
    | component_name (str)
    | The name of the component to check the health status. Defaults to "aaa".

    == Return value ==
    | str: The status of the compoent given by the rediness endpoint.

    == Usage ==
    | Get Health Status   component_name=aaa
    """

    # Initialize kwargs
    kwargs = {}

    # Get the health endpoint for the component
    try:
        health_endpoint = get_health_endpoint(component_name)
    except ValueError as e:
        LOGGER.error("Error getting health endpoint: %s", e)
        return None

    # Get the full response payload
    payload = _http_call(health_endpoint, **kwargs)

    # Special handling for FID component
    if component_name == "fid":
        app_status = payload.get("application")
        LOGGER.debug("App name: fid, App status: %s", app_status)
        return app_status

    # Special handling for ESB component
    if component_name.lower() == "esb":
        success = payload.get("success")
        LOGGER.debug("App name: esb, Success: %s", success)
        return success

    # Handling for all other AMS cmponents
    # Extract applicationStatuses
    application_statuses = payload.get("applicationStatuses", {})

    # Get appStatus
    for app_name, app_data in application_statuses.items():
        app_status = app_data.get("appStatus")
        LOGGER.debug("App name: %s, App status: %s", app_name, app_status)
        return app_status

    # If no appStatus is found, return None
    LOGGER.warning("Could not determine the health status for this component.")
    return None


def get_health_endpoint(component_name):
    """
    Get the health endpoint URL for a given component.

    Args:
        component_name (str): Name of the component (e.g. 'aaa', 'fom', etc.)

    Returns:
        str: The endpoint URL for the component's health check

    Raises:
        ValueError: If the component name is not found in HEALTH_ENDPOINTS
    """
    endpoint = HEALTH_ENDPOINTS.get(component_name.lower())
    if not endpoint:
        raise ValueError(f"No health endpoint found for component: {component_name}")
    return endpoint
