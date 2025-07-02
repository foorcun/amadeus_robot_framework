"""Injector module to handle GET http calls from MSC"""

import logging
from ams.data_model.common_libs.injectors.injector import _http_call
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def msc_v2_get_list_alert(
    last_updated_date_time="20250527T182238Z", max_no_of_alerts=3000, displayable="Y"
):
    """
    Executes a HTTP GET call to retrieve MSC v2 list alert.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/alert/listAlert.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``last_updated_date_time``       | Last updated date and time                                                            |
    | ``max_no_of_alerts``             | Max number of alerts returned by the request                                          |
    | ``displayable``                  | Displayable alerts                                                                    |

    === Usage: ===
    | ${response}   MSC V2 Get List Alert

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = "/messagestore/messagestoreService/rest/v2/alert/listAlert"

    kwargs = {
        "query_params": {
            "lastUpdatedDateTime": last_updated_date_time,
            "maxNoOfAlerts": max_no_of_alerts,
            "displayable": displayable,
        }
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_list_alert_count(
    last_updated_date_time="20250527T182238Z", displayable="Y"
):
    """
    Executes a HTTP GET call to retrieve MSC v2 list alert count.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/alert/listAlertCount.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``last_updated_date_time``       | Last updated date and time                                                            |
    | ``displayable``                  | Displayable alerts                                                                    |

    === Usage: ===
    | ${response}   MSC V2 Get List Alert Count

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = "/messagestore/messagestoreService/rest/v2/alert/listAlertCount"

    kwargs = {
        "query_params": {
            "lastUpdatedDateTime": last_updated_date_time,
            "displayable": displayable,
        }
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_label_list():
    """
    Executes a HTTP GET call to retrieve MSC v2 label list.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getLabelList.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments                                                      |

    === Usage: ===
    | ${response}   MSC V2 Get Label List

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getLabelList"
    )

    kwargs = {}

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_message_detail(apt_correlation_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 message detail.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getMessageDetail.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |

    === Usage: ===
    | ${response}   MSC V2 Get Message Detail

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getMessageDetail"
    )

    kwargs = {
        "query_params": {"aptCorrelationId": apt_correlation_id},
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_sub_message_detail(
    apt_correlation_id="TEST", sub_message_correlation_id="TEST"
):
    """
    Executes a HTTP GET call to retrieve MSC v2 sub message detail.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getSubMessageDetail.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |
    | ``sub_message_correlation_id``   | The unique identifier for a sub message in MSC                                        |

    === Usage: ===
    | ${response}   MSC V2 Get Sub Message Detail

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getSubMessageDetail"
    )

    kwargs = {
        "query_params": {
            "aptCorrelationId": apt_correlation_id,
            "subMessageCorrelationId": sub_message_correlation_id,
        },
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_error_list(
    apt_correlation_id="TEST", sub_message_correlation_id="TEST", archive_id="TEST"
):
    """
    Executes a HTTP GET call to retrieve MSC v2 error list.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getErrorList.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |
    | ``sub_message_correlation_id``   | The unique identifier for a sub message in MSC                                        |
    | ``archive_id``                   | The archive Id                                                                        |

    === Usage: ===
    | ${response}   MSC V2 Get Error List

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getErrorList"
    )

    kwargs = {
        "query_params": {
            "aptCorrelationId": apt_correlation_id,
            "subMessageCorrelationId": sub_message_correlation_id,
            "archiveId": archive_id,
        },
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_register_alerts():
    """
    Executes a HTTP GET call to retrieve MSC v2 register alerts.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getRegisterAlerts.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | None                             | This function takes no arguments                                                      |

    === Usage: ===
    | ${response}   MSC V2 Get Register Alerts

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getRegisterAlerts"
    )

    kwargs = {}

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_message_entity(
    apt_correlation_id="TEST", sub_message_correlation_id="TEST"
):
    """
    Executes a HTTP GET call to retrieve MSC v2 messgae entity.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getMessageEntity.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |
    | ``sub_message_correlation_id``   | The unique identifier for a sub message in MSC                                        |

    === Usage: ===
    | ${response}   MSC V2 Get Message Entity

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getMessageEntity"
    )

    kwargs = {
        "query_params": {
            "aptCorrelationId": apt_correlation_id,
            "subMessageCorrelationId": sub_message_correlation_id,
        },
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_message_label(apt_correlation_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 message label.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getMessageLabel.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |

    === Usage: ===
    | ${response}   MSC V2 Get Message Label

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getMessageLabel"
    )

    kwargs = {
        "query_params": {"aptCorrelationId": apt_correlation_id},
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_history(apt_correlation_id="TEST", sub_message_correlation_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 history.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getHistory.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |
    | ``sub_message_correlation_id``   | The unique identifier for a sub message in MSC                                        |

    === Usage: ===
    | ${response}   MSC V2 Get History

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = "/messagestore/messagestoreService/rest/v2/messageService/getHistory"

    kwargs = {
        "query_params": {
            "aptCorrelationId": apt_correlation_id,
            "subMessageCorrelationId": sub_message_correlation_id,
        },
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_sub_message_list(apt_correlation_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 sub message list

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getSubMessageList.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |

    === Usage: ===
    | ${response}   MSC V2 Get Sub Message List

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getSubMessageList"
    )

    kwargs = {
        "query_params": {"aptCorrelationId": apt_correlation_id},
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_alert_list(apt_correlation_id="TEST", sub_message_correlation_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 alert_list.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getAlertList.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |
    | ``sub_message_correlation_id``   | The unique identifier for a sub message in MSC                                        |

    === Usage: ===
    | ${response}   MSC V2 Get Alert List

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getAlertList"
    )

    kwargs = {
        "query_params": {
            "aptCorrelationId": apt_correlation_id,
            "subMessageCorrelationId": sub_message_correlation_id,
        },
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_message_archives(apt_correlation_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 message archives.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/messages/archives.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |

    === Usage: ===
    | ${response}   MSC V2 Get General Message

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/messages/archives"
    )

    kwargs = {
        "query_params": {"aptCorrelationId": apt_correlation_id},
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_history_message_meta(entity_id="TEST"):
    """
    Executes a HTTP GET call to retrieve MSC v2 history message meta.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/getHistoryMessageMeta.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``entity_id``                    | The entity Id                                                                         |

    === Usage: ===
    | ${response}   MSC V2 Get History Message Meta

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/getHistoryMessageMeta"
    )

    kwargs = {
        "query_params": {"entityId": entity_id},
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_structured_message(
    apt_correlation_id="TEST", sub_message_correlation_id="TEST"
):
    """
    Executes a HTTP GET call to retrieve MSC v2 structured_message.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/structuredMessage.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``apt_correlation_id``           | The unique identifier for a message in MSC                                            |
    | ``sub_message_correlation_id``   | The unique identifier for a sub message in MSC                                        |

    === Usage: ===
    | ${response}   MSC V2 Get Structured Message

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/structuredMessage"
    )

    kwargs = {
        "query_params": {
            "aptCorrelationId": apt_correlation_id,
            "subMessageCorrelationId": sub_message_correlation_id,
        },
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_post_register_alerts(alerts):
    """
    Executes a HTTP POST call to register a list of MSC alerts to the current user.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/registerAlerts.
    The function returns the string response from the API.

    | *Arguments*                      | *Description*                                                                                             |
    |----------------------------------|-----------------------------------------------------------------------------------------------------------|
    | ``alerts``                       | A list of dicts each containing the field 'alertId', or the response from keyword "Msc V2 Get List Alert" |

    === Usage: ===
    | ${response}   MSC V2 Post Register Alerts    alerts=${alert_list}

    === Returns: ===
    | string or None | The string response from the API, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/registerAlerts"
    )

    gen_payload = PayloadGenerator(
        alerts, "payloads/v2_register_alerts.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()

    kwargs = {
        "operation": "POST",
        "payload": payload,
        "json_response": False,
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_post_unregister_alerts(alerts):
    """
    Executes a HTTP POST call to unregister a list of MSC alerts from the current user.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/unregisterAlerts.
    The function returns the string response from the API.

    | *Arguments*                      | *Description*                                                                                             |
    |----------------------------------|-----------------------------------------------------------------------------------------------------------|
    | ``alerts``                       | A list of dicts each containing the field 'id', or the response from keyword "Msc V2 Get Register Alerts" |

    === Usage: ===
    | ${response}   MSC V2 Post Unregister Alerts    alerts=${registered_alerts}

    === Returns: ===
    | string or None | The string response from the API, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v2/messageService/unregisterAlerts"
    )

    gen_payload = PayloadGenerator(
        alerts, "payloads/v2_unregister_alerts.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()

    kwargs = {
        "operation": "POST",
        "payload": payload,
        "json_response": False,
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v3_post_list_message(filters):
    """
    Executes a HTTP POST call to retrieve the MSC v3 Message List corresponding to the Filters provided.

    This function calls the endpoint /messagestore/messagestoreService/rest/v3/messageServiceV3/listMessageByFilter.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                                         |
    |----------------------------------|---------------------------------------------------------------------------------------|
    | ``filters``                      | A dict containing the filter criteria                                                 |

    === Usage: ===
    | ${response}    MSC V3 Post List Message    filters=${filters}

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = (
        "/messagestore/messagestoreService/rest/v3/messageServiceV3/listMessageByFilter"
    )

    gen_payload = PayloadGenerator(
        filters, "payloads/v3_list_message_filter.jinja", __file__
    )
    payload = gen_payload.construct_generic_payload()

    kwargs = {"operation": "POST", "payload": payload}

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_add_star(apt_correlation_ids):
    """
    Executes a HTTP GET call to add a Star to the list of messages corresponding to the apt_correlation_ids provided.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/addStar.
    The function returns the string response from the API.

    | *Arguments*                      | *Description*                                                                                     |
    |----------------------------------|---------------------------------------------------------------------------------------------------|
    | ``apt_correlation_ids``          | A list of apt_correlation_id strings                                                              |

    === Usage: ===
    | ${response}   MSC V2 Get Add Star    apt_correlation_ids=${correlation_ids}

    === Returns: ===
    | string or None | The string response from the API, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = "/messagestore/messagestoreService/rest/v2/messageService/addStar"

    kwargs = {
        "query_params": {"aptCorrelationId": apt_correlation_ids},
        "json_response": False,
    }

    return _http_call(msc_endpoint, **kwargs)


def msc_v2_get_remove_star(apt_correlation_ids):
    """
    Executes a HTTP GET call to remove the Star from the list of messages corresponding to the apt_correlation_ids provided.

    This function calls the endpoint /messagestore/messagestoreService/rest/v2/messageService/removeStar.
    The function returns the string response from the API.

    | *Arguments*                      | *Description*                                                                                     |
    |----------------------------------|---------------------------------------------------------------------------------------------------|
    | ``apt_correlation_ids``          | A list of apt_correlation_id strings                                                              |

    === Usage: ===
    | ${response}   MSC V2 Get Remove Star    apt_correlation_ids=${correlation_ids}

    === Returns: ===
    | string or None | The string response from the API, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    msc_endpoint = "/messagestore/messagestoreService/rest/v2/messageService/removeStar"

    kwargs = {
        "query_params": {"aptCorrelationId": apt_correlation_ids},
        "json_response": False,
    }

    return _http_call(msc_endpoint, **kwargs)
