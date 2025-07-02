"""
This module contains the injector to fetch fids backend tables (controllers/layouts/rules)
"""

import locale
from functools import cmp_to_key
from ams.fid_api_calls.cache.injector import (
    fids_open_data_channel,
    fids_close_data_channel,
)
from ams.fid_api_calls.crud.injector_rules import fids_selection_rule_get_by_name

# pylint: disable=line-too-long


def __fids_xmids_query_cache_by_selection_rule_name(
    rule_name, context, session_key, **kwargs
):
    response = fids_selection_rule_get_by_name(rule_name, session_key, **kwargs)
    # if there is an error here the selection rule is not in the system
    flights_selection = response.json()["results"][0]["fdrClearRule"]

    selection_rules = {"robot_rule": flights_selection}
    # use the selection rules to query the cache
    ws = fids_open_data_channel(
        controller_name="ROBOT",
        monitor_name="ROBOT_XMIDS",
        selection_rules=selection_rules,
        context=context,
    )
    ws.wait_for_initial_data()
    fids_close_data_channel(ws)
    return ws.get_snapshot("robot_rule")


def fids_cmid_alloctions_get(counter, session_key="defaultKey", **kwargs):
    """
    Get all CMID allocations (dedicated and common) for a counter.

    | *Arguments*      | *Description*                                                                |
    | ``counter``      | Counter resource name.                                                       |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get CMID Allocations    counter=COUNTER1

    """
    dedicated = __fids_xmids_query_cache_by_selection_rule_name(
        "xMIDS Counter Flights",
        {"MONITOR.resourceName": counter},
        session_key,
        **kwargs
    )
    common = __fids_xmids_query_cache_by_selection_rule_name(
        "xMIDS Counter Common Allocations",
        {"MONITOR.resourceName": counter},
        session_key,
        **kwargs
    )

    # combine the lists for sorting as cmids does
    combined = []
    combined.extend(dedicated)
    combined.extend(common)

    def alloction_compare(o1, o2):
        d1 = o1["timings"]["planEnd"]
        d2 = o2["timings"]["planEnd"]

        if d1 is None and d2 is not None:
            return 1
        if d2 is None and d1 is not NotImplemented:
            return -1
        if d1 is None and d2 is None:
            return 0
        if d1 == d2:
            return 0
        # the dates are strings but in sortable format
        return locale.strcoll(d2, d1)

    return sorted(combined, key=cmp_to_key(alloction_compare))


def fids_bmid_alloctions_get(belt, session_key="defaultKey", **kwargs):
    """
    Get all BMID allocations for a belt.

    | *Arguments*      | *Description*                                                                |
    | ``belt``         | Belt resource name.                                                          |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get BMID Allocations    belt=BELT1

    """
    return __fids_xmids_query_cache_by_selection_rule_name(
        "xMIDS Belt Flights", {"MONITOR.resourceName": belt}, session_key, **kwargs
    )


def fids_gmid_alloctions_get(gate, session_key="defaultKey", **kwargs):
    """
    Get all GMID allocations for a gate.

    | *Arguments*      | *Description*                                                                |
    | ``gate``         | Gate resource name.                                                          |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get GMID Allocations    gate=GATE1

    """
    return __fids_xmids_query_cache_by_selection_rule_name(
        "xMIDS Gate Flights", {"MONITOR.resourceName": gate}, session_key, **kwargs
    )


def fids_xmids_arrivals_get(session_key="defaultKey", **kwargs):
    """
    Get all xMIDS arrival flights.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get xMIDS Arrivals

    """
    return __fids_xmids_query_cache_by_selection_rule_name(
        "xMIDS Arrival Flights", {}, session_key, **kwargs
    )


def fids_xmids_departures_get(session_key="defaultKey", **kwargs):
    """
    Get all xMIDS departure flights.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get xMIDS Departures

    """
    return __fids_xmids_query_cache_by_selection_rule_name(
        "xMIDS Departure Flights", {}, session_key, **kwargs
    )
