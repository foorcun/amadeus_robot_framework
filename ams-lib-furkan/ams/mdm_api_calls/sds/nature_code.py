"""
Keywords for interacting with the SDS for nature code-related operations.
"""

import logging
from ams.commons import get_customer_id
from .injector import sds_save, sds_list

# pylint: disable=line-too-long

LOGGER = logging.getLogger(__name__)


def sds_save_nature_code(
    code, flight_activity, flight_category, flight_type, iata_service_type=None
):
    """
    Save nature code

    | *Arguments*                        | *Description*                                               |
    | ``code``                           | 3 characters code                                           |
    | ``flight_activity``                | Flight activity                                             |
    | ``flight_category``                | Flight category                                             |
    | ``flight_type``                    | Flight type                                                 |
    | ``iata_service_type``              | IATA service type e.g. A, J, G                              |

    === Usage: ===
    | Sds Save Nature Code    code=AAA    flight_activity=Arrival    flight_category=Domestic    flight_type=Passenger    iata_service_type=G
    """

    all_nature_code_details = sds_list("extendedServiceType")

    existing_nature_code_details = [
        nature_code
        for nature_code in all_nature_code_details
        if nature_code["code"] == code
    ]

    if existing_nature_code_details:
        LOGGER.info("Nature code %s already exists, skipping creation", code)
        return existing_nature_code_details

    LOGGER.info("Create nature code %s", code)
    data = {
        "customerId": get_customer_id(),
        "code": code,
        "flightActivity": flight_activity,
        "flightCategory": flight_category,
        "flightType": flight_type,
        "iataServiceTypeId": iata_service_type,
    }

    return sds_save("extendedServiceType", data)
