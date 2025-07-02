"""
This module contains the functions to fetch resource details based on the response received
"""

import random
import jmespath
from robot.api.deco import not_keyword
from ams.data_model.common_libs.utils.date_handler import now_gmt


# pylint: disable=line-too-long


def get_valid_aircraft_type_period_details(response_json):
    """
    Get a list of dictionaries with all valid aircraft type period details along with aircraft type id, iata-icao code and name.

    | *Arguments*               | *Description*                                                         |

    | ``response_json``         | response object from call to 'Get Aircraft Type Details' keyword      |

    === Usage: ===
    | Get Valid Aircraft Type Period details    response_json=${response_json}

    """

    act_period_details = jmespath.search(
        f"[?periods[0].endDateTime == `null` || periods[0].endDateTime > `{now_gmt()}`] | [].{{id: id, iataCode: iataCode, icaoCode: icaoCode, name: periods[].name | [0], periodId: periods[].periodId | [0], startDateTime: periods[].startDateTime | [0], endDateTime: periods[].endDateTime | [0]}}",
        response_json,
    )

    valid_act_period_details = [
        act_period
        for act_period in act_period_details
        if act_period.get("iataCode") not in (None, "null")
        and act_period.get("icaoCode") not in (None, "null")
    ]

    return valid_act_period_details


@not_keyword
def get_aircraft_type_bind_label(response_json, act_iata_code):
    """
    Builds a value for param called aircraftTypeBindLabel (to be used during aircraft type creation) using aircraft type iata code, icao code and name.

    Returns the generated bind label e.g. '321, A321, Airbus A321-100/200'

    | *Arguments*               | *Description*                                                         |

    | ``response_json``         | response object from call to 'Get Aircraft Type Details' keyword      |
    | ``act_iata_code``         | aircraft type iata code e.g. 331, 321                                 |

    === Usage: ===
    | Get Aircraft Type Bind Label    response_json=${response_json}    act_iata_code=321

    """
    act_period_details_all = get_valid_aircraft_type_period_details(response_json)

    act_data = next(
        (act for act in act_period_details_all if act.get("iataCode") == act_iata_code),
        None,
    )

    return (
        "No matching valid aircraft data found"
        if not act_data
        else ", ".join(
            part
            for part in [
                act_data.get("iataCode"),
                act_data.get("icaoCode"),
                act_data.get("name"),
            ]
            if part and part != "null"
        )
    )


def get_valid_aircraft_registration_and_type_mapping(response_json):
    """
    Get a list of dictionaries with all valid aircraft registrations and their mapped aircraft types.

    | *Arguments*               | *Description*                                                    |

    | ``response_json``         | response object from call to 'Get Aircraft Details' keyword      |

    === Usage: ===
    | Get Valid Aircraft Registration And Type Mapping    response_json=${response_json}

    """

    aic_rego_type_map = jmespath.search(
        f"[?periods[?endDateTime == `null` || endDateTime > `{now_gmt()}`]].{{registrationId: registrationId, aircraftTypeId: periods[0].aircraftType.id, iataCode: periods[0].aircraftType.iataCode, icaoCode: periods[0].aircraftType.icaoCode}}",
        response_json,
    )

    valid_aic_rego_type_map = [
        aic_rego
        for aic_rego in aic_rego_type_map
        if all(
            aic_rego.get(key) not in (None, "null")
            for key in ("registrationId", "iataCode", "icaoCode")
        )
    ]

    return valid_aic_rego_type_map


def get_valid_aircraft_rego_and_type_mapping(response_json):
    """
    Get any random rego number and it's mapped aircraft type dict from the response.

    | *Arguments*               | *Description*                                                  |

    | ``response_json``         | response object from call to 'Get Aircraft Details' keyword    |

    === Usage: ===
    | Get Valid Aircraft Rego And Type Mapping    response_json=${response_json}

    """
    aic_rego_type_map_all = get_valid_aircraft_registration_and_type_mapping(
        response_json
    )

    return random.choice(aic_rego_type_map_all) if aic_rego_type_map_all else None
