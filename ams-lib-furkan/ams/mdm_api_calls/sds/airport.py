"""
Keywords for interacting with the SDS for airport-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import _sds_call, _sds_save, _find_match, _find_conflicting

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_get_airports_by_iata(iata):
    """
    Get airports by IATA code

    | *Arguments*                        | *Description*                                                     |
    | ``iata``                           | IATA code                                                         |

    === Usage: ===
    | Sds Get Airports By Iata    NCE
    """
    return _sds_call("GET", "airport", "5", f"/listByIataAndIcao?iataCode={iata}") or []


def sds_get_airports_by_icao(icao):
    """
    Get airports by ICAO code

    | *Arguments*                        | *Description*                                                     |
    | ``icao``                           | ICAO code                                                         |

    === Usage: ===
    | Sds Get Airports By Icao    LFMN
    """
    return _sds_call("GET", "airport", "5", f"/listByIataAndIcao?icaoCode={icao}") or []


def sds_get_airports_by_iata_icao(iata, icao):
    """
    Get airports by IATA and ICAO codes

    | *Arguments*                        | *Description*                                                     |
    | ``iata``                           | IATA code                                                         |
    | ``icao``                           | ICAO code                                                         |

    === Usage: ===
    | Sds Get Airports By Iata Icao    iata=NCE  icao=LFMN
    """
    return (
        _sds_call(
            "GET", "airport", "5", f"/listByIataAndIcao?iataCode={iata}&icaoCode={icao}"
        )
        or []
    )


def sds_save_airport(iata, icao="ZZZZ", force_creation=False):
    """
    Save airport

    | *Arguments*                        | *Description*                                                                                 |                                                                                      |
    | ``iata``                           | IATA code of the airport                                                                        |
    | ``icao``                           | ICAO code of the airport                                                                        |
    | ``force_creation``                 | Force re-creation of airport if it already exists                                             |

    === Usage: ===
    | Sds Save Airport     iata=NCE
    | Sds Save Airport     iata=NCE  icao=LFMN
    | Sds Save Airport     iata=NCE  icao=LFMN  force_creation=True
    """
    LOGGER.info("Save airport %s/%s", iata, icao)

    find_match = _find_match(sds_get_airports_by_iata_icao, iata, icao)
    find_conflicting = _find_conflicting(
        (sds_get_airports_by_iata, iata), (sds_get_airports_by_icao, icao)
    )

    data = {
        "customerId": get_customer_id(),
        "name": "ROBOT AIRPORT",
        "iata": iata,
        "icao": icao,
    }
    return _sds_save("airport", data, find_match, find_conflicting, force_creation)
