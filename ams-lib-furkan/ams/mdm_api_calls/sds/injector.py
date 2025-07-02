"""
This module contain the injectors for SDS operations
"""

import logging
import protocols.broker


from ams.commons import get_customer_id, get_ref_airport_id
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)
from ams.data_model.common_libs.utils.generic_helpers import add_data_to_clean_up
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)

DEFAULT_ENDPOINTS = {
    "get": "/{id}",
    "list": "",
    "save": "/save",
    "delete": "/delete/{id}",
}

ENTITIES = {
    "aircraft": {
        2: {"get": "/get/{id}", "list": "/list"},
        3: {},
        4: {},
        5: {},
        6: {},
    },
    "aircraftType": {
        2: {"get": "/{customerId}/{id}", "list": "/list/{customerId}"},
        3: {"get": "/get/{id}", "list": "/list"},
        4: {},
        5: {},
        6: {"save": "", "delete": "?id={id}"},
    },
    "airline": {
        1: {},
        2: {"get": "/build?customerId={customerId}&dataId={id}", "list": "/list"},
        3: {"get": "/build?id={id}", "list": "/list"},
        4: {"list": "/list"},
    },
    "airport": {
        2: {},
        3: {"get": "/build?customerId={customerId}&dataId={id}", "list": "/list"},
        4: {"get": "/build?id={id}", "list": "/list"},
        5: {"get": "/build?id={id}", "list": "/list"},
    },
    "arrivalBaggageBelt": {
        2: {"get": "", "list": "/list/{airportId}", "count": "/count/{airportId}"},
        3: {"get": "", "list": "/list/{airportId}", "count": "/count/{airportId}"},
        4: {"get": ["", "/{id}"], "count": "/count", "save": "", "delete": "?id={id}"},
    },
    "departureBaggageCarousel": {
        2: {"get": "", "list": "/list/{airportId}", "count": "/count/{airportId}"},
        3: {"get": "", "list": "/list/{airportId}", "count": "/count/{airportId}"},
        4: {"get": ["", "/{id}"], "count": "/count", "save": "", "delete": "?id={id}"},
    },
    "extendedServiceType": {
        1: {},
        2: {},
        3: {"list": "/list", "count": "/count", "delete": "/delete?id={id}"},
    },
    "flightServiceType": {
        1: {},
        2: {},
        3: {
            "code": "/listByCode?code={code}",
            "list": "/list",
            "delete": "/delete?id={id}",
        },
    },
    "gate": {
        3: {"get": "/{airportId}/{id}", "list": "/list/{airportId}"},
        4: {"save": "", "delete": "?id={id}"},
    },
    "runway": {
        1: {},
        2: {},
        3: {
            "get": "/{airportId}/{id}",
            "list": "/list/{airportId}",
            "count": "/count/{airportId}",
            "save": "/save/{airportId}",
            "delete": "/delete/{airportId}?id={id}",
        },
    },
    "stand": {
        2: {"get": "/{customerId}/{airportId}/{id}", "list": "/list/{airportId}"},
        3: {"get": "/{airportId}/{id}", "list": "/list/{airportId}"},
        4: {"save": "", "delete": "?id={id}"},
    },
    "terminal": {
        1: {},
        2: {},
        4: {
            "get": ["", "/{id}"],
            "count": "/count",
            "code": "/code?code={code}",
            "save": "",
            "delete": "?id={id}",
        },
    },
}


##
# Generic services
##


def sds_get(entity_type, version="latest", get_by_id=False, entity_id=None):
    """
    Get SDS entity details

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |
    | ``get_by_id``                      | if True, tries to use endpoint with {id} placeholder                                                  |
    | ``entity_id``                      | entity id to use if get_by_id is True                                                                 |

    === Usage: ===
    | sds_get     stand
    | sds_get     stand  4
    | sds_get     stand  True  STD000123
    """

    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "get")
    if isinstance(endpoint, list):
        if get_by_id and entity_id is not None:
            endpoint_with_id = next(
                (ep for ep in endpoint if "{id}" in ep), endpoint[0]
            )
            endpoint = endpoint_with_id.replace("{id}", entity_id)
            return _sds_call("GET", entity_type, version, endpoint)
        # If not get_by_id or entity_id is None, use the first endpoint
        endpoint = endpoint[0]
    elif isinstance(endpoint, str):
        if get_by_id and entity_id is not None:
            return sds_get_by_id(entity_type, entity_id, version)

    return _sds_call("GET", entity_type, version, endpoint)


def sds_get_by_id(entity_type, entity_id, version="latest"):
    """
    Get SDS entity by id

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``entity_id``                      | entity id                                                                                             |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |

    === Usage: ===
    | sds_get_by_id     stand  STD000123
    | sds_get_by_id     stand  STD000123  3
    """
    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "get").replace("{id}", entity_id)
    return _sds_call("GET", entity_type, version, endpoint)


def sds_get_by_code(entity_type, entity_code, version="latest"):
    """
    Get SDS entity by code

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``entity_code``                    | entity code                                                                                           |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |

    === Usage: ===
    | sds_get_by_code     terminal  T2
    | sds_get_by_code     terminal  T2  4
    """
    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "code").replace(
        "{code}", entity_code
    )
    return _sds_call("GET", entity_type, version, endpoint)


def sds_count(entity_type, version="latest"):
    """
    Get total count of records present

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |

    === Usage: ===
    | sds_count     gate
    | sds_count     gate  4
    """
    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "count")
    return _sds_call("GET", entity_type, version, endpoint)


def sds_list(entity_type, version="latest"):
    """
    List SDS entities

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |

    === Usage: ===
    | sds_list     stand
    | sds_list     stand  3
    """
    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "list")
    return _sds_call("GET", entity_type, version, endpoint)


def _sds_save(entity_type, data, find_match, find_conflicting, force_creation=False):
    # find_match and find_conflicting are now values, not functions
    entity = find_match
    conflicting_entities = find_conflicting
    if not force_creation:
        if entity:
            return entity
    if conflicting_entities:
        for entity_id in conflicting_entities:
            sds_delete(entity_type, entity_id)
    return sds_save(entity_type, data)


def _find_match(get_func, *args, **kwargs):
    """
    Find a matching entity using the provided get function.
    """
    entities = get_func(*args, **kwargs)
    return entities[0] if entities else None


def _find_conflicting(*get_fun_arg):
    """
    Find conflicting entities using (function, argument) tuples.
    Usage: _find_conflicting((func1, arg1), (func2, arg2), ...)
    """
    ids = set()
    for func, arg in get_fun_arg:
        ids.update(e["id"] for e in func(arg))
    return ids


def sds_save(entity_type, data, version="latest"):
    """
    Save SDS entity

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``data``                           | data used to populate Jinja template                                                                  |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |

    === Usage: ===
    | sds_save     stand  {name: "S12", ...}
    """
    LOGGER.info("Save entity '%s': %s", entity_type, data)
    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "save")

    gen_payload = PayloadGenerator(data, f"payloads/{entity_type}.jinja", __file__)
    entity = gen_payload.construct_generic_payload()

    saved_entity = _sds_call("POST", entity_type, version, endpoint, entity)

    assert (
        saved_entity is not None and saved_entity["id"] is not None
    ), f"Failed to create entity {entity_type}"

    LOGGER.info("Entity '%s' saved: %s", entity_type, saved_entity["id"])

    add_data_to_clean_up(entity_type, saved_entity["id"])

    return saved_entity


def sds_delete(entity_type, entity_id, version="latest"):
    """
    Delete SDS entity

    | *Arguments*                        | *Description*                                                                                         |
    | ``entity_type``                    | entity type ("aircraft", "aircraftType", "stand", "gate"...)                                          |
    | ``entity_id``                      | entity id                                                                                             |
    | ``version``                        | version of the REST service (by default, call latest version)                                         |

    === Usage: ===
    | sds_delete     stand  STD000123
    | sds_delete     stand  STD000123  3
    """
    LOGGER.info("Delete entity '%s': %s", entity_type, entity_id)

    version = _get_version(entity_type, version)
    endpoint = _get_endpoint(entity_type, version, "delete").replace("{id}", entity_id)

    response = _sds_call("DELETE", entity_type, version, endpoint)

    LOGGER.info("Entity '%s' deleted: %s", entity_type, entity_id)

    return response


##
# Test keywords
##
def sds_test_all_read_endpoints():
    """
    Test all available read-only SDS endpoints

    === Usage: ===
    | sds_test_all_read_endpoints
    """
    for entity_key, entity in ENTITIES.items():
        for version in entity.keys():
            LOGGER.info("Call - Get %s v%s", entity_key, str(version))
            sds_get_by_id(entity_key, "DUMMY", version)

            LOGGER.info("Call - List %s v%s", entity_key, str(version))
            sds_list(entity_key, version)


##
# Helpers
##
def _get_version(entity_type, version_str):
    if version_str == "latest":
        return max(ENTITIES[entity_type].keys())
    return int(version_str)


def _get_endpoint(entity_type, version, service_type):
    """
    Get the endpoint for a given entity type, version, and service type.
    """
    endpoint = ENTITIES[entity_type][version].get(service_type, None)

    if endpoint is None:
        endpoint = DEFAULT_ENDPOINTS[service_type]

    if isinstance(endpoint, list):
        return [
            ep.replace("{airportId}", get_ref_airport_id()).replace(
                "{customerId}", get_customer_id()
            )
            for ep in endpoint
        ]

    return endpoint.replace("{airportId}", get_ref_airport_id()).replace(
        "{customerId}", get_customer_id()
    )


def _sds_call(operation, entity_type, version, endpoint, payload=None):
    args = {
        "operation": operation,
        "path": f"/sds/data/v{version}/{entity_type}{endpoint}",
        "payload": payload,
    }
    response = protocols.broker.injector(args, "defaultKey", rest_injector)

    if response.status_code != 200 and response.status_code != 204:
        raise ValueError(f"Call to {args} failed with status {response.status_code}")

    if response.status_code == 204:
        return None

    response_json = response.json()
    return response_json
