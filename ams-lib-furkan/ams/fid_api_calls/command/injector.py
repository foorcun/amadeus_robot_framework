"""Injector for command keywords for controller commands in FIDS"""

import threading
import protocols.broker
from ams.fid_api_calls.command.cmd_channel import FidsCommandChannelWebSocket
from ams.fid_api_calls.crud.injector import fids_get_home_airport


def fids_close_command_channel(ws):
    """
    Close the FIDS command channel WebSocket connection.

    | *Arguments*      | *Description*                                              |
    | ``ws``           | The FidsCommandChannelWebSocket instance to close.         |

    === Usage: ===
    | Close FIDS Command Channel    ${cmd_socket}

    """
    ws.close()


def fids_open_command_channel(controller_name):
    """
    Open a FIDS command channel WebSocket connection.

    | *Arguments*         | *Description*                                         |
    | ``controller_name`` | Controller/client identifier.                         |

    === Usage: ===
    | Open FIDS Command Channel    RobotTestController

    """
    # pylint: disable = protected-access
    server_url = (
        protocols.session_manager.sessions._get_session_context_data()
        .get("global_environment_context")
        .get("server_url")
    )

    server_url = server_url.replace("https://", "wss://")
    home_airport = fids_get_home_airport()

    ws = FidsCommandChannelWebSocket(
        url=server_url,
        home_airport=home_airport,
        cli_id=controller_name,
    )

    thread = threading.Thread(
        target=ws.start, name=f"FidsDataChannel-{controller_name}"
    )

    context_data = protocols.session_manager.sessions._get_session_context_data()

    context_data["test_context"]["web_sockets"].append({"thread": thread, "ws": ws})

    thread.start()

    return ws


def fids_command_channel_wait_connected(ws, timeout=120):
    """
    Wait for the FIDS command channel WebSocket to be connected.

    | *Arguments*      | *Description*                                              |
    | ``ws``           | The FidsCommandChannelWebSocket instance.                  |
    | ``timeout``      | (Optional) Timeout in seconds. Default is 120.             |

    === Usage: ===
    | Wait For Command Channel Connected    ${data_socket}

    """
    return ws.wait_for_connected(timeout)


def fids_comamnd_channel_wait_command(ws, timeout=120):
    """
    Wait for a command on the FIDS command channel WebSocket.

    | *Arguments*      | *Description*                                              |
    | ``ws``           | The FidsCommandChannelWebSocket instance.                  |
    | ``timeout``      | (Optional) Timeout in seconds. Default is 120.             |

    === Usage: ===
    | Wait For Command Channel Command    ${data_socket}

    """
    return ws.wait_for_command(timeout)
