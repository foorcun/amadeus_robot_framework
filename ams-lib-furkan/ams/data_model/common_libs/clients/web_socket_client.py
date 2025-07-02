"""Base class for web sockets, child classes can override the call backs"""

import ssl
import logging
import websocket


class WebSocketWrapper:
    """Base class for web sockets, child classes can override the call backs"""

    def on_ping(self, _ws, message):
        """Call back for ping messages"""
        logging.info("Ping received %s", message)

    def on_open(self, _ws):
        """Call back for connection opened"""
        logging.info("Web Socket Opened")
        self.connnected = True

    def on_message(self, _ws, message):
        """Call back for message recieved"""
        logging.info("Web Socket Message received %s", message)

    def on_error(self, _ws, error):
        """Call back for error"""
        logging.error("Web Socket Error %s", error)
        self.connnected = False

    def on_close(self, _ws):
        """Call back for connection closed"""
        logging.info("Web Socket Closed")
        self.connnected = False

    #
    def __init__(
        self,
        url,
        headers=None,
        logging_trace=True,
        sslopt=None,
    ):
        if sslopt is None:
            sslopt = {"cert_reqs": ssl.CERT_NONE}
        self.connnected = False
        websocket.enableTrace(logging_trace)
        self.sslopt = sslopt
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_ping=self.on_ping,
            header=headers,
        )

    def start(self):
        """Starts the web socket, blocking the thread."""
        self.ws.run_forever(sslopt=self.sslopt)

    def is_connected(self):
        """Returns is the socket is connected"""
        return self.connnected

    def close(self):
        """Closes the web socket"""
        self.ws.close()
