"""
Injector for keywords that will get data from the FIDS cache
"""

# pylint: disable=line-too-long

import threading
import protocols.broker

from ams.fid_api_calls.cache.data_channel import FidsDataChannelWebSocket
from ams.fid_api_calls.crud.injector import fids_get_home_airport


def fids_close_data_channel(ws):
    """
    Close the FIDS data channel WebSocket connection.

    | *Arguments*      | *Description*                                   |
    | ``ws``           | The FidsDataChannelWebSocket instance to close. |

    === Usage: ===
    | Close FIDS Data Channel    ${data_socket}

    """
    # pylint: disable = protected-access
    context_data = protocols.session_manager.sessions._get_session_context_data()
    for item in context_data["test_context"]["web_sockets"]:
        if item["ws"] == ws:
            ws.close()
            item["thread"].join()
            context_data["test_context"]["web_sockets"].remove(item)
            break


def fids_open_data_channel(
    controller_name,
    monitor_name,
    selection_rules,
    context=None,
    tables=None,
):
    """
    Open a FIDS data channel WebSocket and register views, tables, and context.

    | *Arguments*         | *Description*                                                       |
    | ``controller_name`` | Controller/client identifier.                                       |
    | ``monitor_name``    | Monitor identifier.                                                 |
    | ``selection_rules`` | Dictionary mapping view names to selection rules.                   |
    | ``context``         | (Optional) Additional context to register.                          |
    | ``tables``          | (Optional) List of table objects to register.                       |
    | ``session_key``     | (Optional) Session key for the connection. Default is "defaultKey". |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Open FIDS Data Channel    RobotDataChannelTest    monitor_name=RobotDataChannelMonitor    selection_rules={"arrivals": "select Arrivals where $airline.code == 'WN'"}

    """
    # pylint: disable = protected-access
    server_url = (
        protocols.session_manager.sessions._get_session_context_data()
        .get("global_environment_context")
        .get("server_url")
    )

    server_url = server_url.replace("https://", "wss://")
    home_airport = fids_get_home_airport()

    ws = FidsDataChannelWebSocket(
        url=server_url,
        cli_id=controller_name,
        home_airport=home_airport,
        monitor_id=monitor_name,
    )

    for view_name, rule in selection_rules.items():
        ws.register_view(view_name, rule)

    if tables is not None:
        for table in tables:
            ws.register_table(
                table.name, table.view_name, table.data_row_count, table.table_row_count
            )

    if context is not None:
        ws.register_context(context)

    thread = threading.Thread(
        target=ws.start, name=f"FidsDataChannel-{controller_name}-{monitor_name}"
    )

    context_data = protocols.session_manager.sessions._get_session_context_data()
    context_data["test_context"]["web_sockets"].append({"thread": thread, "ws": ws})

    thread.start()

    return ws


def fids_data_channel_find(ws, selection_rule_name, field, value, timeout=120):
    """
    Wait for and return the first data item matching the field and value.

    | *Arguments*            | *Description*                                  |
    | ``ws``                 | The FidsDataChannelWebSocket instance.         |
    | ``selection_rule_name``| Name of the selection rule/view.               |
    | ``field``              | Field to match in the data.                    |
    | ``value``              | Value to match for the field.                  |
    | ``timeout``            | (Optional) Timeout in seconds. Default is 120. |

    === Usage: ===
    | Find Data Channel Item    ${data_socket}    selection_rule_name=arrivals    field=flightKey    value=XYZA_1234_DEPARTURE

    """
    return ws.wait_for_data(
        selection_rule_name, lambda item: item.get(field) == value, timeout
    )


def fids_data_channel_empty(ws, selection_rule_name, timeout=120):
    """
    Wait until the data for the given selection rule is empty.

    | *Arguments*            | *Description*                                  |
    | ``ws``                 | The FidsDataChannelWebSocket instance.         |
    | ``selection_rule_name``| Name of the selection rule/view.               |
    | ``timeout``            | (Optional) Timeout in seconds. Default is 120. |

    === Usage: ===
    | Wait For Empty Data Channel    ${data_socket}    selection_rule_name=arrivals

    """
    return ws.wait_for_empty_data(selection_rule_name, timeout)


def fids_data_channel_get_snapshot(ws, selection_rule_name):
    """
    Return the current snapshot of data for the given selection rule.

    | *Arguments*            | *Description*                          |
    | ``ws``                 | The FidsDataChannelWebSocket instance. |
    | ``selection_rule_name``| Name of the selection rule/view.       |

    === Usage: ===
    | Get Data Channel Snapshot    ws=websocket_instance    selection_rule_name=rule

    """
    return ws.get_snapshot(selection_rule_name)


def fids_data_channel_wait_for_initial_data(ws, timeout=120):
    """
    Wait for the initial data to be received on the data channel.

    | *Arguments*      | *Description*                                  |
    | ``ws``           | The FidsDataChannelWebSocket instance.         |
    | ``timeout``      | (Optional) Timeout in seconds. Default is 120. |

    === Usage: ===
    | Wait For Initial Data Channel    ws=websocket_instance

    """
    return ws.wait_for_initial_data(timeout)
