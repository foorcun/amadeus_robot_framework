import logging
from ams.commons import get_customer_id
from .injector import _sds_call, _sds_save, _find_match


LOGGER = logging.getLogger(__name__)


def sds_get_stand_by_name(name):
    """
    Get stand by name

    | *Arguments*                        | *Description*                                                     |
    | ``name``                           | Name of the stand                                                  |

    === Usage: ===
    | Sds Get Stand By Name    STD01
    """
    return _sds_call("GET", "stand", "4", f"/name?name={name}") or []


def sds_save_stand(name, force_creation=False):
    """
    Save stand

    | *Arguments*                        | *Description*                                                     |
    | ``name``                           | Name of the stand                                                  |
    | ``force_creation``                | Force re-creation of the stand if it already exists (default: False) |

    === Usage: ===
    | Sds Save Stand    STD01   force_creation=True
    | Sds Save Stand    STD01
    """
    find_match = _find_match(sds_get_stand_by_name, name)
    data = {
        "customerId": get_customer_id(),
        "name": name,
    }
    return _sds_save("stand", data, find_match, find_match, force_creation)
