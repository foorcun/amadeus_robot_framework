"""
Keywords for interacting with the SDS for departure baggage carousel-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import sds_save, sds_get, _sds_call, _get_version
from .terminal import sds_get_terminal_by_code

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_get_baggage_chute_by_external_id(external_id):
    """
    Get baggage chute by external id

    | *Arguments*                      | *Description*                                                 |
    | ``external_id``                  | External id of the baggage chute                              |

    === Usage: ===
    | Sds Get Baggage Chute By External Id    QCPAZU_CAR000201
    """
    return (
        _sds_call("GET", "departureBaggageCarousel", "4", f"/externalId/{external_id}")
        or []
    )


def sds_get_baggage_chute_by_terminal_and_name(terminal, name):
    """
    Get baggage chute by terminal code and name

    | *Arguments*                        | *Description*                                                |
    | ``terminal``                       | Terminal code or id                                          |
    | ``name``                           | Name of the baggage chute                                    |

    === Usage: ===
    | Sds Get Baggage Chute By Terminal And Name    T1    Baggage Chute 1
    | Sds Get Baggage Chute By Terminal And Name    TER000441    Baggage Chute 2
    """
    version = _get_version("departureBaggageCarousel", version_str="latest")

    return (
        _sds_call(
            "GET", "departureBaggageCarousel", version, f"/name/{terminal}/{name}"
        )
        or []
    )


def sds_save_baggage_chute(name, terminal):
    """
    Save baggage chute

    | *Arguments*                        | *Description*                                            |
    | ``name``                           | Name of the baggage chute                                |
    | ``terminal``                       | Terminal code id of the baggage chute                    |

    === Usage: ===
    | Sds Save Baggage Chute    Baggage Chute 1    T1
    """
    all_baggage_chute_list = sds_get("departureBaggageCarousel")
    existing_baggage_chute = [
        chute for chute in all_baggage_chute_list if chute["name"] == name
    ]

    existing_baggage_chute_in_terminal = sds_get_baggage_chute_by_terminal_and_name(
        terminal, name
    )

    if len(existing_baggage_chute_in_terminal) > 0 or existing_baggage_chute:
        LOGGER.info("Baggage chute %s already exists, skipping creation", name)
        return existing_baggage_chute

    LOGGER.info("Create baggage chute %s for terminal %s", name, terminal)
    terminal_info = sds_get_terminal_by_code(terminal)
    terminal_id = (
        terminal_info[0]["id"]
        if isinstance(terminal_info, list) and terminal_info
        else terminal_info["id"]
    )
    data = {
        "customerId": get_customer_id(),
        "name": name,
        "terminalId": terminal_id,
    }
    return sds_save("departureBaggageCarousel", data)
