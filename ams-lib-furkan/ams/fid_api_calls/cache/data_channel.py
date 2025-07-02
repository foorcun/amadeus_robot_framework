"""This is the data channel for FIDS data cache via web socket"""

import logging
import threading
import ssl
import time
import copy
import json
import base64
from ams.data_model.common_libs.clients.web_socket_client import WebSocketWrapper
from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)

# pylint: disable=line-too-long


class FidsDataChannelWebSocket(WebSocketWrapper):
    """
    This class acts as the data service in Rendering Engine
    Because of the different in list handling between Python and JavaScript there are changes to how the instruction sets are applied
    The test class for this class uses the same data and flow to test the final snapshot equals what the data service would return
    """

    def __init__(
        self,
        url,
        home_airport,
        monitor_id,
        cli_id,
        headers=None,
        logging_trace=True,
        data_poll_interval=5,
        sslopt=None,
    ):
        if sslopt is None:
            sslopt = {"cert_reqs": ssl.CERT_NONE}
        url = url + "/fids/ng/cli/ws/data"
        super().__init__(url, headers, logging_trace, sslopt)
        self.data_poll_interval = data_poll_interval
        self.home_airport = home_airport
        self.monitor_id = monitor_id
        self.cli_id = cli_id
        self.poll_thread = None
        self.data_request_full = True
        self.initial_data_received = False

        self.condition = threading.Condition()

        self.snapshots = {}
        self.rule_context = {}
        self.metadata = {}
        self.register_views = {}
        self.tables = {}
        self.banks = {}

    def start(self):
        """
        Starts the data polling thread unless disabled and calls the parent class to start (blocking this thread)
        """
        logging.info("Starting web socket")
        self.__schedule_data_poll()
        super().start()

    def wait_for_data(self, view_name, condition, timeout=120):
        """
        Wait for data to be received for a specific view name.
        This method will block until data is received or the timeout is reached.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.condition:
                if view_name in self.snapshots:
                    filter_data = list(filter(condition, self.snapshots[view_name]))
                    if filter_data is not None and len(filter_data) > 0:
                        return copy.copy(filter_data)  # return copy
                self.condition.wait(timeout=1)
        return None

    def wait_for_empty_data(self, view_name, timeout=120):
        """
        Wait for data to be received for a specific view name.
        This method will block until data is received or the timeout is reached.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.condition:
                if view_name in self.snapshots:
                    if len(self.snapshots[view_name]) == 0:
                        return []  # return copy
                self.condition.wait(timeout=1)
        return None

    def wait_for_initial_data(self, timeout=120):
        """
        Wait for initial data to be received for a specific view name.
        This method will block until data is received or the timeout is reached.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.condition:
                if self.initial_data_received:
                    return True
                self.condition.wait(timeout=1)
        return False

    def __schedule_data_poll(self):
        """ "
        Schedule the next data poll unless disabled
        """
        if self.data_poll_interval > 0:
            logging.info("scheduling poll fetch %s", self.data_poll_interval)
            self.poll_thread = threading.Timer(
                self.data_poll_interval, self.__send_data_poll
            )
            self.poll_thread.start()

    def __send_data_poll(self):
        """
        Send a data poll message to the web socket
        """
        if self.ws.sock and self.ws.sock.connected:
            message = {
                "type": "Data",
                "APT_FID_MON_ID": self.monitor_id,
                "APT_CORRELATION_ID": Gad.generate_correlation_id(32),
                "metaData": "true",
                "full": "true" if self.data_request_full else "false",
            }
            self.data_request_full = False
            self.ws.send(json.dumps(message))
            logging.info("Data poll message sent")
            self.__schedule_data_poll()
        else:
            logging.error("Web socket is not connected, cannot send data poll message")

    def close(self):
        """
        Close the web socket connection and cancel the poll thread
        """
        if self.poll_thread is not None and self.poll_thread.is_alive():
            self.poll_thread.cancel()
        super().close()
        logging.info("Web Socket Closed and Poll Thread Cancelled")

    def on_open(self, ws):
        """
        When a new connection is made send the register message as configured
        """
        super().on_open(ws)
        payload = self.__register_payload()
        logging.info("Registering views with payload: %s", payload)
        ws.send(payload)

    def get_snapshot(self, view_name):
        """
        Returns a copy of the current snapshot as it has been processed from incoming instruction sets
        """
        return (
            self.snapshots.get(view_name).copy() if view_name in self.snapshots else []
        )

    def register_view(self, view_name, selection_rule):
        """
        Register a view with the selection rule, will be sent when the web socket is opened.
        """
        self.register_views[view_name] = base64.b64encode(
            selection_rule.encode("utf-8")
        ).decode("ascii")
        logging.info(
            "Registering view: %s with selection rule: %s",
            view_name,
            self.register_views[view_name],
        )
        self.snapshots[view_name] = []

    def register_context(self, context):
        """
        Register the given context, will be sent when the web socket is opened
        The context include parameters that are used in the selection rules,
        like the Monitor.resourceName parameter in xMIDS selection rules
        or the counter/belt/gate field.
        """
        self.rule_context = {**self.rule_context, **context}

    def register_table(self, table_name, view_name, data_row_count, table_row_cout):
        """register table to an existing view"""
        self.tables[table_name] = {
            "selectionId": view_name,
            "definedDataRowCount": data_row_count,
            "definedTableRowCount": table_row_cout,
        }

    def register_bank(
        self, bank_name, view_name, data_row_count, table_row_cout, defined_position
    ):
        """register bank to an existing view"""
        self.snapshots["bankStates"] = []
        self.banks[bank_name] = {
            "selectionId": view_name,
            "definedDataRowCount": data_row_count,
            "definedTableRowCount": table_row_cout,
            "definedPosition": defined_position,
        }

    def __register_payload(self):
        return json.dumps(
            {
                "type": "Register",
                "APT_FID_CLI_ID": self.cli_id,
                "APT_FID_MON_ID": self.monitor_id,
                "APT_FID_HOPO": self.home_airport,
                "APT_FID_EMMM": "false",
                "APT_CORRELATION_ID": Gad.generate_correlation_id(32),
                "payload": {
                    "views": self.register_views,
                    "banks": self.banks,
                    "tables": self.tables,
                    "context": self.rule_context,
                },
            }
        )

    def on_message(self, ws, message):
        """
        For data messages, apply the updates to the snapshots.
        """
        super().on_message(ws, message)
        msg = json.loads(message)
        if msg.get("type") == "Data":
            self.apply_updates(msg.get("payload", {}))

    def apply_updates(self, payload):
        """
        Process instruction set messages as the rendering engine would
        """
        if payload.get("metaData") is not None:
            self.metadata = payload.get("metaData", {})
        with self.condition:
            for view in payload.get("data", []).keys():
                current_data = self.snapshots.get(view)
                for iset in payload["data"][view]:
                    self.__apply_deletes(current_data, iset)
                    self.__apply_moves(current_data, iset)
                    self.__apply_adds(current_data, iset)
                    self.__apply_updates(current_data, iset)
                    self.__apply_post_process(current_data)
            if self.initial_data_received is False:
                self.initial_data_received = True
            self.condition.notify_all()

    def __apply_post_process(self, current_data):
        """Remove any None values from the list"""
        while None in current_data:
            current_data.remove(None)

    def __apply_deletes(self, current_data, iset):
        deletes = iset.get("D", None)
        if deletes is not None:
            for key in deletes:
                idx = int(key)
                if 0 <= idx < len(current_data):
                    current_data[idx] = None

    def __apply_moves(self, current_data, iset):
        moves = iset.get("M", None)
        if moves is not None:
            for new_index, old_index in moves.items():
                value = current_data[old_index]
                current_data[old_index] = None
                self.__list_insert(current_data, int(new_index), value)

    def __apply_adds(self, current_data, iset):
        adds = iset.get("N", None)
        if adds is not None:
            for index in adds:
                self.__list_insert(current_data, int(index), adds[index])

    def __apply_updates(self, current_data, iset):
        updates = iset.get("U", None)
        if updates is not None:
            if isinstance(updates, list):  # on full requests its a list
                for index, item in enumerate(updates):
                    self.__list_insert(current_data, index, item)
            else:
                for index in updates:
                    self.__list_insert(current_data, int(index), updates[index])

    def __list_insert(self, lst, index, value):
        """
        Insert a value into a list at a specific index
        """
        if len(lst) <= index:
            # If the index is greater than the length of the list, extend the list
            lst.extend([None] * ((index + 1) - len(lst)))
        lst[index] = value
