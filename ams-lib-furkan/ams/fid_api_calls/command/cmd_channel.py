"""This is the command channel for FIDS controller commands via web socket"""

import ssl
import threading

import json
import logging
import time
from ams.data_model.common_libs.clients.web_socket_client import WebSocketWrapper
from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)


class FidsCommandChannelWebSocket(WebSocketWrapper):
    """
    This class acts as the command service in controller
    """

    def __init__(
        self,
        url,
        cli_id,
        home_airport,
        cmd_poll_interval=20,
        headers=None,
        logging_trace=True,
        sslopt=None,
    ):
        if sslopt is None:
            sslopt = {"cert_reqs": ssl.CERT_NONE}
        url = url + "/fids/ng/cli/ws/cmd"
        super().__init__(url, headers, logging_trace, sslopt)
        self.commands = []
        self.cli_id = cli_id
        self.home_airport = home_airport
        self.cmd_poll_interval = cmd_poll_interval
        self.poll_thread = None
        self.condition = threading.Condition()

    def start(self):
        """
        Starts the web socket and schedules the command poll unless disabled.
        """
        self.__schedule_cmd_poll()
        return super().start()

    def on_message(self, ws, message):
        """
        Handle incoming messages from the web socket.
        """
        super().on_message(ws, message)
        msg = json.loads(message)
        if "payload" in msg:
            with self.condition:
                self.commands.append(msg["payload"])
                self.condition.notify_all()

    def on_close(self, ws):
        if self.poll_thread is not None and self.poll_thread.is_alive():
            self.poll_thread.cancel()
        return super().on_close(ws)

    def wait_for_connected(self, timeout=120):
        """
        Waits for a command connected to the server
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.condition:
                if self.connnected:
                    return True
                self.condition.wait(timeout=1)
        return None

    def wait_for_command(self, timeout=120):
        """
        Waits for a command to be received from the web socket.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.condition:
                if len(self.commands) > 0:
                    commands = self.commands
                    self.commands = []  # reset
                    return commands
                self.condition.wait(timeout=1)
        return None

    def __schedule_cmd_poll(self):
        if self.cmd_poll_interval > 0:
            logging.info("scheduling poll fetch %s", self.cmd_poll_interval)
            self.poll_thread = threading.Timer(
                self.cmd_poll_interval, self.__send_cmd_poll
            )
            self.poll_thread.start()

    def __build_poll_message(self):
        """
        Build the command poll message to be sent to the web socket
        """
        return {
            "type": "COMMAND",
            "APT_CORRELATION_ID": Gad.generate_correlation_id(32),
            "FIDS_CLIENT_HA": self.home_airport,
            "FIDS_CLIENT_ID": self.cli_id,
            "FIDS_CLIENT_VERSION": "ROBOT",
        }

    def __send_cmd_poll(self):
        """
        Send a data poll message to the web socket
        """
        if self.ws.sock and self.ws.sock.connected:
            message = self.__build_poll_message()
            self.ws.send(json.dumps(message))
            logging.info("CMD poll message sent")
            self.__schedule_cmd_poll()
        else:
            logging.error("Web socket is not connected, cannot send cmd poll message")
