"""
This module contains the injector to get movement id details

"""

import protocols.broker
from .injector_rest import injector as rest_injector


# pylint: disable=line-too-long
def fom_searches(flight_number, start_date, end_date):
    """
    Search visits

    | *Arguments*                       | *Description*                                                        |
    | ``flight_number``                 | flight number                                                        |
    | ``start_date``                    | start date for the search in YYYY-MM-DD format                       |
    | ``end_date``                      | end date for the search in YYYY-MM-DD format                         |

    === Usage: ===
    | Fom Searches     flight_number=123      start_date=2025-04-01      end_date=2025-04-10
    """

    response = protocols.broker.injector(
        {
            "flight_number": flight_number,
            "start_date": start_date,
            "end_date": end_date,
        },
        "defaultKey",
        rest_injector,
    )

    # TODO VC: review date format of start_date/end_date

    # TODO VC: put code in helper class

    response_json = response.json()

    if response_json.get("generalProcessingStatus", "") == "Error":
        message = "-"
        if len(response_json.get("generalErrorInformation", [])) > 0:
            message = response_json["generalErrorInformation"][0].get(
                "messageText", "-"
            )
        raise ValueError(f"Error in response from FOM: {message}")

    return response.json()["content"]
