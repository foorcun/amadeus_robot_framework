"""
Keywords for interacting with the SDS for terminal-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import sds_save, _sds_call, sds_get_by_code

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_get_terminal_by_code(code):
    """
    Get terminal by code

    | *Arguments*                        | *Description*                                                     |
    | ``code``                           | Terminal code                                                     |

    === Usage: ===
    | Sds Get Terminal By Code    T1
    """
    return sds_get_by_code("terminal", code) or []


def sds_get_terminal_by_external_id(external_id):
    """
    Get terminal by external id

    | *Arguments*                      | *Description*                                                 |
    | ``external_id``                  | External id of the terminal                                   |

    === Usage: ===
    | Sds Get Terminal By External Id    QCPAZU_TER000945
    """
    return _sds_call("GET", "terminal", "4", f"/externalId/{external_id}") or []


def sds_save_terminal(code):
    """
    Save terminal

    | *Arguments*                        | *Description*                                                        |
    | ``code``                           | Terminal code                                                        |

    === Usage: ===
    | Sds Save Terminal    code=T1
    """
    existing_terminal = sds_get_terminal_by_code(code)

    if len(existing_terminal) > 0:
        existing_terminal = existing_terminal[0]
        LOGGER.info("Terminal %s already exists, skipping creation", code)
        return existing_terminal

    LOGGER.info("Create terminal %s", code)
    data = {
        "customerId": get_customer_id(),
        "code": code,
        "name": f"AUTO TEST TERMINAL {code}",
    }

    return sds_save("terminal", data)
