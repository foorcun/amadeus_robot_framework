"""Injector module to handle GET http calls from ESB agent"""

import logging
import random
from protocols import session_manager
from ams.data_model.common_libs.injectors.injector import _http_call_and_check

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def esb_agent_node_status():
    """
    Executes a HTTP GET call to retrieve ESB Agent Node Status.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Node Status

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("status")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_node_details():
    """
    Executes a HTTP GET call to retrieve ESB Agent Node Details.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Node Details

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("details")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_cluster_summary():
    """
    Executes a HTTP GET call to retrieve ESB Agent Cluster Summary.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Cluster Summary

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("cluster_summary")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_cluster_validate():
    """
    Executes a HTTP GET call to validate the ESB Agent Cluster Summary.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Cluster Validate

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("cluster_validate")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_cluster_registry():
    """
    Executes a HTTP GET call to retrieve ESB Agent Cluster Service Registry.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Cluster Registry

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("cluster_registry")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_queues_metrics():
    """
    Executes a HTTP GET call to retrieve ESB Agent ActiveMQ Queue Metrics.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Queues Metrics

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("queues_metrics")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_routing_rules():
    """
    Executes a HTTP GET call to retrieve ESB Agent Routing Rules.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Routing Rules

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = context_data.get("end_points", {}).get("esb", {}).get("routing_rules")

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_interfaces_descriptor():
    """
    Executes a HTTP GET call to retrieve ESB Agent Cluster Interfaces Descriptor.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Interfaces Descriptor

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {}).get("esb", {}).get("interfaces_descriptor")
    )

    kwargs = {}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_node_interface_metrics(node, interface="list"):
    """
    Executes a HTTP GET call to retrieve ESB interface metrics for a specific ESB node.

    | *Arguments*                      | *Description*                                                           |
    |----------------------------------|-------------------------------------------------------------------------|
    | node                             | Which node to retrieve the metrics from                                 |
    | interface                        | (optional) If provided, will return only properties for that interface. |

    === Usage: ===
    | ${response}    Esb Agent Interface Metrics    node=${node}
    | ${response}    Esb Agent Interface Metrics    node=${node}    interface=FOM

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {}).get("esb", {}).get("interface_metrics")
    )

    kwargs = {"path_params": {"node": node, "interface": interface}}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_interface_properties(interface=""):
    """
    Executes a HTTP GET call to retrieve ESB interface properties.

    | *Arguments*                      | *Description*                                                           |
    |----------------------------------|-------------------------------------------------------------------------|
    | interface                        | (optional) If provided, will return only properties for that interface. |

    === Usage: ===
    | ${response}    Esb Agent Interface Properties
    | ${response}    Esb Agent Interface Properties     interface=FOM

    === Returns: ===
    | dict    | The JSON response from the API if the call is successful.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    context_data = session_manager.sessions._get_session_context_data()
    endpoint = (
        context_data.get("end_points", {}).get("esb", {}).get("interface_properties")
    )

    kwargs = {"path_params": {"interface": interface}}

    response_json = _http_call_and_check(
        path=endpoint, field="success", value=True, **kwargs
    )
    return response_json


def esb_agent_find_node_running_interface(interface, node_selector="any"):
    """
    Executes a HTTP GET call to find which node(s) are running the specified interface.

    | *Arguments*                      | *Description*                                                               |
    |----------------------------------|-----------------------------------------------------------------------------|
    | interface                        | The specified interface.                                                    |
    | node_selector                    | (optional) Which node(s) to return: "any" (default), "first", "last", "all" |

    === Usage: ===
    | ${node}   Esb Agent Find Node Running Interface      interface=FOM
    | ${nodes}  Esb Agent Find Node Running Interface      interface=FOM   node_selector=all

    === Returns: ===
    | string or list    | The node or list of nodes, depending on the node_selector.

    === Raises: ===
    | ValueError | If the response status code is not 200 or the "success" field is not True.
    """
    interfaces_descriptor = esb_agent_interfaces_descriptor()
    interface_descriptor = [
        desc
        for desc in interfaces_descriptor["data"]["descriptors"]
        if desc["serviceName"] == interface
    ]
    if not interface_descriptor:
        raise ValueError("Could not find interface in descriptor")

    deployments = [
        deployment
        for deployment in interface_descriptor[0]["deployments"]
        if deployment["deployed"]
    ]
    if not deployments:
        return None

    if node_selector == "any":
        return random.choice(deployments)["node"]
    elif node_selector == "first":
        return deployments[0]["node"]
    elif node_selector == "last":
        return deployments[len(deployments) - 1]["node"]
    elif node_selector == "all":
        return [node["node"] for node in deployments]
    else:
        raise ValueError("Uknown node_selector parameter")


def esb_agent_find_running_nodes():
    """
    Executes a HTTP GET call to retrieve a list of running ESB nodes.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Esb Agent Find Running Nodes

    === Returns: ===
    | list    | The list of running ESB nodes.

    === Raises: ===
    | ValueError | If there is an error when retrieving the list of running ESB nodes.
    """
    registry = esb_agent_cluster_registry()

    return [node for node in registry["data"] if registry["data"][node]]
