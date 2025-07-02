"""
This module contains the functions to fetch resource details based on the response received
"""

import jmespath

# pylint: disable=line-too-long


def get_airline_icao_code(response_json, **kwargs):
    """
    Get the icao code of any airline by providing iata code or name.

    | *Arguments*               | *Description*                                                   |

    | ``response_json``         | response object from call to 'Get Airline Details' keyword      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | *Arguments*     | *Description*                   |

    | ``iata_code``      | iata code of the airline     |
    | ``name``           | name of the airline          |

    === Usage: ===
    | Get Airline Icao Code    response_json=${response_json}    iata_code=6X
    | Get Airline Icao Code    response_json=${response_json}    name=Laker Airways
    | Get Airline Icao Code    response_json=${response_json}    iata_code=TS    name=Top Sky International

    """
    if "iata_code" in kwargs and "name" in kwargs:
        iata_code = kwargs["iata_code"]
        name = kwargs["name"]
        query = f"[?iataCode=='{iata_code}' && name=='{name}'].icaoCode | [0]"
        result = jmespath.search(query, response_json)
        return (
            result
            if result
            else "No mapping icao found, please verify the iata code and name combination"
        )
    if "iata_code" in kwargs:
        iata_code = kwargs["iata_code"]
        query = f"[?iataCode=='{iata_code}'].icaoCode | [0]"
        result = jmespath.search(query, response_json)
        return (
            result if result else "No mapping icao found, please verify the iata code"
        )
    if "name" in kwargs:
        name = kwargs["name"]
        query = f"[?name=='{name}'].icaoCode | [0]"
        result = jmespath.search(query, response_json)
        return result if result else "No mapping icao found, please verify the name"

    raise ValueError(
        "Please provide either 'iata_code' or 'name' as a keyword argument."
    )


def get_callsign_for_flight(response_json, airline_iata_code, flight_number):
    """
    Get the callsign of a flight by providing the airline iata code and flight number.
    This method to be enhanced further to check the callsign rule in SDS.

    | *Arguments*                   | *Description*                                                     |

    | ``response_json``             | response object from call to 'Get Airline Details' keyword        |
    | ``airline_iata_code``         | airline iata code such as 6X or 6E                                |
    | ``flight_number``             | flight number                                                     |


    === Usage: ===
    | Get Callsign For Flight    response_json=${response_json}    airline_iata_code=6X    flight_number=1011

    """

    airline_icao = get_airline_icao_code(response_json, iata_code=airline_iata_code)
    return f"{airline_icao}{flight_number}"
