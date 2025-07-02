"""
Keywords for interacting with the SDS for arrival baggage belt-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import sds_save, sds_get, _sds_call, _get_version
from .terminal import sds_get_terminal_by_code

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_get_baggage_belt_by_terminal_and_name(terminal, name):
    """
    Get baggage belt by terminal and name

    | *Arguments*                        | *Description*                                           |
    | ``terminal``                       | terminal code or id                                     |
    | ``name``                           | Name of the baggage belt                                |

    === Usage: ===
    | Sds Get Baggage Belt By Terminal And Name    T1    B6
    | Sds Get Baggage Belt By Terminal And Name    TER000441    B6
    """
    version = _get_version("arrivalBaggageBelt", version_str="latest")

    return (
        _sds_call("GET", "arrivalBaggageBelt", version, f"/name/{terminal}/{name}")
        or []
    )


def sds_save_baggage_belt(name, terminal, swing_belt=False):
    """
    Save baggage belt

    | *Arguments*                        | *Description*                                            |
    | ``name``                           | Name of the baggage belt                                 |
    | ``terminal``                       | Code of the terminal where the baggage belt is located   |
    | ``swing_belt``                     | Whether the baggage belt is a swing belt                 |

    === Usage: ===
    | Sds Save Baggage Belt    B6    T1    True
    """
    # Check if baggage belt already exists

    all_belt_list = sds_get("arrivalBaggageBelt")
    existing_belt = [belt for belt in all_belt_list if belt["name"] == name]

    existing_baggage_belt_in_terminal = sds_get_baggage_belt_by_terminal_and_name(
        terminal, name
    )

    if len(existing_baggage_belt_in_terminal) > 0 or existing_belt:
        LOGGER.info("Baggage belt %s already exists, skipping creation", name)
        return existing_belt

    LOGGER.info("Create baggage belt %s for terminal %s", name, terminal)
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
        "swingBelt": swing_belt,
    }
    return sds_save("arrivalBaggageBelt", data)
