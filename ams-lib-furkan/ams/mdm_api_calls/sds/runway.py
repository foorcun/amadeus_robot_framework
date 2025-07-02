"""
Keywords for interacting with the SDS for runway-related operations.
"""

import logging
from ams.commons import get_customer_id, get_ref_airport_iata
from .injector import sds_list, sds_save
from .airport import sds_get_airports_by_iata

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_save_runway(name, direction_1=None, direction_2=None, default_usage=None):
    """
    Save runway

    | *Arguments*                        | *Description*                                            |
    | ``name``                           | Name of the runway                                       |
    | ``direction1``                     | Direction 1 of the runway                                |
    | ``direction2``                     | Direction 2 of the runway                                |

    === Usage: ===
    | Sds Save Runway    R3    south    east
    """
    # Check if the runway already exists

    runway_list = sds_list("runway")

    existing_runway = [runway for runway in runway_list if runway["name"] == name]

    if existing_runway:
        LOGGER.info("Runway %s already exists, skipping creation", name)
        return existing_runway

    # get airport by IATA code to ensure the runway is associated with an airport

    airport_details_list = sds_get_airports_by_iata(get_ref_airport_iata())
    airport_details = airport_details_list[0] if airport_details_list else {}

    LOGGER.info("Create runway %s", name)
    data = {
        "customerId": get_customer_id(),
        "airport_id": airport_details.get("id"),
        "airport_iataCode": airport_details.get("iataCode"),
        "airport_icaoCode": airport_details.get("icaoCode"),
        "airport_timezone": (
            airport_details.get("periods")[0].get("timeZoneId")
            if airport_details.get("periods")
            else None
        ),
        "airport_name": airport_details.get("name"),
        "name": name,
        "direction1": direction_1,
        "direction2": direction_2,
        "defaultUsage": default_usage,
    }
    return sds_save("runway", data)
