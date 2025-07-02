"""
Keywords for interacting with the SDS for airline-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import _sds_call, _sds_save, _find_match, _find_conflicting

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_get_airlines_by_iata(iata):
    """
    Get airlines by IATA code

    | *Arguments*                        | *Description*                                                     |
    | ``iata``                           | IATA code                                                         |

    === Usage: ===
    | Sds Get Airlines By Iata    6X
    """
    return _sds_call("GET", "airline", "4", f"/listByIataAndIcao?iataCode={iata}") or []


def sds_get_airlines_by_icao(icao):
    """
    Get airlines by ICAO code

    | *Arguments*                        | *Description*                                                     |
    | ``icao``                           | ICAO code                                                         |

    === Usage: ===
    | Sds Get Airlines By Icao    XYB
    """
    return _sds_call("GET", "airline", "4", f"/listByIataAndIcao?icaoCode={icao}") or []


def sds_get_airlines_by_iata_icao(iata, icao):
    """
    Get airlines by IATA and ICAO codes

    | *Arguments*                        | *Description*                                                     |
    | ``iata``                           | IATA code                                                         |
    | ``icao``                           | ICAO code                                                         |

    === Usage: ===
    | Sds Get Airlines By Iata Icao    iata=6X  icao=XYB
    """
    return (
        _sds_call(
            "GET", "airline", "4", f"/listByIataAndIcao?iataCode={iata}&icaoCode={icao}"
        )
        or []
    )


def sds_save_airline(iata, icao="ZZZ", force_creation=False):
    """
    Save airline

    | *Arguments*                        | *Description*                                                                                 |
    | ``iata``                           | IATA code of the airline                                                                      |
    | ``icao``                           | ICAO code of the airline                                                                      |
    | ``force_creation``                 | Force re-creation of airline if it already exists                                             |

    === Usage: ===
    | Sds Save Airline     iata=6X
    | Sds Save Airline     iata=6X  icao=XYB
    | Sds Save Airline     iata=6X  icao=XYB  force_creation=True
    """
    LOGGER.info("Save airline %s/%s", iata, icao)

    find_match = _find_match(sds_get_airlines_by_iata_icao, iata, icao)
    find_conflicting = _find_conflicting(
        (sds_get_airlines_by_iata, iata), (sds_get_airlines_by_icao, icao)
    )

    data = {
        "customerId": get_customer_id(),
        "name": "ROBOT AIRLINE",
        "iata": iata,
        "icao": icao,
    }
    return _sds_save("airline", data, find_match, find_conflicting, force_creation)
