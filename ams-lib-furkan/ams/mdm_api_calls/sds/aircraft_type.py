"""
Keywords for interacting with the SDS for aircraft type-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import _sds_call, _sds_save, _find_match, _find_conflicting

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_get_aircraft_types_by_iata(iata):
    """
    Get aircraft types by IATA code

    | *Arguments*                        | *Description*                                                     |
    | ``iata``                           | IATA code                                                         |

    === Usage: ===
    | Sds Get Aircraft Types By Iata    720
    """
    return (
        _sds_call("GET", "aircraftType", "6", f"/listByIataAndIcao?iataCode={iata}")
        or []
    )


def sds_get_aircraft_types_by_icao(icao):
    """
    Get aircraft types by ICAO code

    | *Arguments*                        | *Description*                                                     |
    | ``icao``                           | ICAO code                                                         |

    === Usage: ===
    | Sds Get Aircraft Types By Icao    B720
    """
    return (
        _sds_call("GET", "aircraftType", "6", f"/listByIataAndIcao?icaoCode={icao}")
        or []
    )


def sds_get_aircraft_types_by_iata_icao(iata, icao):
    """
    Get aircraft types by IATA and ICAO codes

    | *Arguments*                        | *Description*                                                     |
    | ``iata``                           | IATA code                                                         |
    | ``icao``                           | ICAO code                                                         |

    === Usage: ===
    | Sds Get Aircraft Types By Iata Icao    iata=720  icao=B720
    """
    return (
        _sds_call(
            "GET",
            "aircraftType",
            "6",
            f"/listByIataAndIcao?iataCode={iata}&icaoCode={icao}",
        )
        or []
    )


def sds_save_aircraft_type(iata, icao="ZZZZ", force_creation=False):
    """
    Save aircraft type

    | *Arguments*                        | *Description*                                                                                 |
    | ``iata``                           | IATA code of the aircraft type                                                                      |
    | ``icao``                           | ICAO code of the aircraft type                                                                      |
    | ``force_creation``                 | Force re-creation of aircraft type if it already exists                                             |

    === Usage: ===
    | Sds Save Aircraft Type     iata=720
    | Sds Save Aircraft Type     iata=720  icao=B720
    | Sds Save Aircraft Type     iata=720  icao=B720  force_creation=True
    """
    LOGGER.info("Save aircraft type %s/%s", iata, icao)

    find_match = _find_match(sds_get_aircraft_types_by_iata_icao, iata, icao)
    find_conflicting = _find_conflicting(
        (sds_get_aircraft_types_by_iata, iata), (sds_get_aircraft_types_by_icao, icao)
    )

    data = {
        "customerId": get_customer_id(),
        "name": "ROBOT AIRCRAFT TYPE",
        "iata": iata,
        "icao": icao,
    }
    return _sds_save("aircraftType", data, find_match, find_conflicting, force_creation)
