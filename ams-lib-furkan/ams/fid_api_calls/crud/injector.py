"""
This module contains the injector to fetch fids backend tables (controllers/layouts/rules)
"""

import logging
import protocols.broker
from protocols import session_manager
from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from .injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def fids_login(session_key="defaultKey", **kwargs):
    """
    Login to FIDS and set up session context.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | FIDS Login

    """
    kwargs["endpoint_type"] = "login"

    instance_id = Gad.generate_correlation_id(32)
    kwargs["headers"] = {"APT_AEP_INSTANCE_ID": instance_id}
    login_response = protocols.broker.injector(kwargs, session_key, rest_injector)

    # pylint: disable=protected-access
    rest_details = protocols.session_manager.sessions._get_security_context_details(
        session_key
    )

    fids_session_cookie = login_response.headers.get("Set-Cookie")

    context_data = protocols.session_manager.sessions._get_session_context_data()
    context_data["test_context"]["fids_session_cookie"] = fids_session_cookie
    context_data["test_context"]["web_sockets"] = []

    # Add the fids jsessionid to the cookie header for all requests
    if rest_details["header"]["Cookie"] is None:
        rest_details["header"]["Cookie"] = login_response.headers.get("Set-Cookie")
    else:
        rest_details["header"]["Cookie"] = (
            rest_details["header"]["Cookie"] + "; " + fids_session_cookie
        )

    # Add the fids tab instance id to the headers for all requests
    rest_details["header"]["APT_AEP_INSTANCE_ID"] = instance_id

    # Lookup which airport the fids server wants back
    kwargs["endpoint_type"] = "functions"
    functions_response = protocols.broker.injector(
        kwargs, session_key, rest_injector
    ).json()
    context_data["test_context"]["fids_home_airport"] = functions_response["results"][
        "ref_airport_icao"
    ]

    return login_response


def fids_get_home_airport():
    """Get from the context the home airport the FIDS will not reject"""
    # pylint: disable = protected-access
    context_data = protocols.session_manager.sessions._get_session_context_data()
    return context_data["test_context"]["fids_home_airport"]


def fids_logout(session_key="defaultKey", **kwargs):
    """this also logouts with AAA"""
    kwargs["endpoint_type"] = "logout"
    protocols.broker.injector(kwargs, session_key, rest_injector)

    # pylint: disable=protected-access
    rest_details = protocols.session_manager.sessions._get_security_context_details(
        session_key
    )

    context_data = protocols.session_manager.sessions._get_session_context_data()
    fids_session_cookie = context_data["test_context"]["fids_session_cookie"]

    # remove fids headers
    if rest_details["header"]["Cookie"] is not None:
        rest_details["header"]["Cookie"].replace(fids_session_cookie, "")

    rest_details["header"]["APT_AEP_INSTANCE_ID"] = None


def fids_get_ui_updates(session_key="defaultKey", **kwargs):
    """
    Fetch UI updates

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | FIDS Get UI Updates

    """
    kwargs["endpoint_type"] = "updates"
    return protocols.broker.injector(kwargs, session_key, rest_injector)


def fids_close_ui_updates(session_key="defaultKey", **kwargs):
    """
    Close the FIDS UI updates.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | FIDS Close UI Updates

    """
    kwargs["endpoint_type"] = "close"
    return protocols.broker.injector(kwargs, session_key, rest_injector)


def __base_get_data(view, fields, session_key="defaultKey", **kwargs):
    """
    Common get data processing used by most fids get calls
    """
    kwargs["endpoint_type"] = "read"
    kwargs["view"] = view
    kwargs["fields"] = fields
    return protocols.broker.injector(kwargs, session_key, rest_injector)


def __base_save_data(view, fields, entity, session_key="defaultKey", **kwargs):
    """
    Commone save data processing used by most fids save calls.
    This will include the entity in the auto clean up list unless "skip_clean_up" is True
    """
    kwargs["endpoint_type"] = "save"
    kwargs["view"] = view
    kwargs["fields"] = fields

    for field in fields:
        if field in kwargs:
            entity[field] = kwargs.get(field)

    kwargs["entity"] = entity

    response = protocols.broker.injector(kwargs, session_key, rest_injector)
    __add_to_automatic_clean_up(response=response, **kwargs)
    return response


def __add_to_automatic_clean_up(response, **kwargs):
    """
    Adds the response entity, if valid, to the auto clean up list for clean up before logout
    """
    result = fids_get_response_result(response)
    view_name = kwargs.get("view")
    fields = kwargs.get("fields")
    # add the entity to the clean up list if successful for auto clean up
    if result is not None and kwargs.get("skip_clean_up", False) is False:
        # pylint: disable = protected-access
        context_data = session_manager.sessions._get_session_context_data()
        data_to_clean_up = context_data["test_context"]["data_to_clean_up"]
        if data_to_clean_up.get("fids") is None:
            data_to_clean_up["fids"] = []
        data_to_clean_up["fids"].append(
            {
                "view": view_name,
                "fields": fields,
                "entity": result,
            }
        )


def __remove_data_from_clean_up(view, entity, **kwargs):
    """
    Removed the entity from the auto clean up.
    This allows tests that delete the data as part of the test to remove the auto clean up so it will not fail
    """
    # pylint: disable = protected-access
    context_data = session_manager.sessions._get_session_context_data()
    data_to_clean_up = context_data["test_context"]["data_to_clean_up"]
    if (
        data_to_clean_up.get("fids") is not None
        and kwargs.get("skip_clean_up", False) is False
    ):
        items_to_remove = []
        for item in data_to_clean_up["fids"]:
            # use first field as primary key
            primary_key = item["fields"][0]
            if item["view"] == view and item["entity"].get(primary_key) == entity.get(
                primary_key
            ):
                items_to_remove.append(item)
        for item in items_to_remove:
            data_to_clean_up["fids"].remove(item)


def __base_delete_data(view, fields, entity, session_key="defaultKey", **kwargs):
    """
    Commone delete processing
    """
    kwargs["endpoint_type"] = "delete"
    kwargs["view"] = view
    kwargs["fields"] = fields

    for field in fields:
        if field in kwargs:
            entity[field] = kwargs.get(field)

    kwargs["entity"] = entity
    response = protocols.broker.injector(kwargs, session_key, rest_injector)

    # remove from the clean up list if successful
    result = fids_get_response_result(response)
    if result is not None and kwargs.get("skip_clean_up", False) is False:
        __remove_data_from_clean_up(**kwargs)
    return response


def __base_execute_function(
    function_name, parameters, session_key="defaultKey", **kwargs
):
    """
    Common Execute Function processing
    """
    kwargs["endpoint_type"] = "execute_function"
    kwargs["function"] = function_name
    kwargs["parameters"] = parameters
    return protocols.broker.injector(kwargs, session_key, rest_injector)


def __integer_parameter(value):
    """
    Converts the given value to an aep integer for passing over query parameters
    """
    return str(value) + "L"


def fids_get_response_result(response_payload):
    """
    Extract the results a FIDS response.

    | *Arguments*         | *Description*                                                                |
    | ``response_payload``| The response object returned by the FIDS API call.                           |

    === Usage: ===
    | ${result}=    FIDS Get Response Result    response_payload=${response}

    """
    results = response_payload.json().get("results")
    if isinstance(results, list):
        return results[0] if len(results) > 0 else {}
    else:
        return results


def fids_get_updates_response_result(response_payload, store_id):
    """
    Extract updates for a specific store_id from a FIDS API updates response.

    | *Arguments*         | *Description*                                                                |
    | ``response_payload``| The response object returned by the FIDS API call.                           |
    | ``store_id``        | The store ID to extract updates for.                                         |

    === Usage: ===
    | ${updates}=    FIDS Get Updates Response Result    response_payload=${response}    store_id=store1

    """
    for item, updates in response_payload.json().get("results").items():
        if item == store_id:
            return updates[0]
    return {}


def web_socket_cleanup():
    """
    Ensure any web sockets are closed.

    | *Arguments* | *Description*         |
    | (none)      | No arguments needed.  |

    === Usage: ===
    | Web Socket Cleanup

    """
    # pylint: disable = protected-access
    context_data = protocols.session_manager.sessions._get_session_context_data()
    websockets = context_data["test_context"].get("web_sockets")
    if websockets is not None:
        for item in websockets:
            try:
                thread_name = item["thread"].name
                logging.info("Closing web socket %s", thread_name)
                item["ws"].close()
                item["thread"].join()
            except Exception as e:
                logging.error(
                    "Ignoring clean up Error closing web socket %s: %s",
                    thread_name,
                    e,
                )
