"""
This module contains the functions to fetch airport details based on the response received.
"""

import jmespath

# pylint: disable=line-too-long


def get_airport_icao_code(response_json):
    """
    Get the ICAO code of an airport from the response JSON.

    | *Arguments*               | *Description*                                                   |

    | ``response_json``         | response object from call to 'Get Airport Details' keyword      |

    === Usage: ===
    | Get Airport Icao Code    response_json=${response_json}                                     |

    """
    query = "[0].icaoCode"
    result = jmespath.search(query, response_json)
    return result if result else "No ICAO code found in the response"
