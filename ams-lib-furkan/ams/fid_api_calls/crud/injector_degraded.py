"""Injector for FIDS degraded keywords"""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

FIDS_DEGRADED_AIRLINES_VIEW_NAME = "CHDelegateBean.Airlines"
FIDS_DEGRADED_AIRLINES_FIELDS = ["code", "iata", "icao", "language"]


def fids_degraded_airlines_get(session_key="defaultKey", **kwargs):
    """
    Get degraded airlines from the cache.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Degraded Airlines

    """
    return __base_get_data(
        FIDS_DEGRADED_AIRLINES_VIEW_NAME,
        FIDS_DEGRADED_AIRLINES_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_DEGRADED_AIRPORTS_VIEW_NAME = "CHDelegateBean.Airports"
FIDS_DEGRADED_AIRPORTS_FIELDS = ["code", "iata", "icao", "language"]


def fids_degraded_airports_get(session_key="defaultKey", **kwargs):
    """
    Get degraded airports from the cache.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Degraded Airports

    """
    return __base_get_data(
        FIDS_DEGRADED_AIRPORTS_VIEW_NAME,
        FIDS_DEGRADED_AIRPORTS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_DATASET_PROCESSORS_VIEW_NAME = "FCDelegateBean.BatchProcessors"
FIDS_DATASET_PROCESSORS_FIELDS = [
    "fdpId",
    "fdpName",
    "fdpDegraded",
    "fdpFdbId",
    "fdpOrder",
    "fdpRequired",
    "fdpDataTtl",
    "fdpRscFetch",
    "fdpRscInterested",
    "fdpRscMap",
    "fdpRscEnrich",
    "fdpRscPersist",
]


def fids_dataset_processors_get(session_key="defaultKey", **kwargs):
    """
    Get dataset processors

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Dataset Processors

    """
    return __base_get_data(
        FIDS_DATASET_PROCESSORS_VIEW_NAME,
        FIDS_DATASET_PROCESSORS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_ARRIVAL_METADATA_VIEW_NAME = "RefDelegateBean.MetadataFlatTreeByName"
FIDS_ARRIVAL_METADATA_FIELDS = ["path", "value", "displayName"]


def fids_arrival_metadata_get(session_key="defaultKey", **kwargs):
    """
    Get arrival metadata.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Arrival Metadata

    """
    kwargs["where"] = "sources.mdsName = 'arrivalTimings'"
    return __base_get_data(
        FIDS_ARRIVAL_METADATA_VIEW_NAME,
        FIDS_ARRIVAL_METADATA_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_DEGRADED_ARRIVALS_VIEW_NAME = "CHDelegateBean.ArrivalFlights"
FIDS_DEGRADED_ARRIVALS_FIELDS = [
    "acType3lc",
    "acType5lc",
    "aircraftTerminal",
    "airline",
    "beltList",
    "beltRange",
    "belts",
    "boardedPax",
    "bookedPax",
    "callsign",
    "codeshareList",
    "direction",
    "displayCode",
    "flightKey",
    "gateList",
    "gateRange",
    "gates",
    "iataFlightNumber",
    "icaoFlightNumber",
    "publicFlightNumber",
    "publicTerminal",
    "registration",
    "remarks",
    "routings",
    "runway",
    "securityLevel",
    "serviceType",
    "specialEmphasis",
    "standList",
    "stands",
    "statuses",
    "suffix",
    "timings",
    "trafficType",
    "tripNumber",
    "_name",
]


def fids_degraded_arrivals_get(
    time_window_start=-1, time_window_end=6, session_key="defaultKey", **kwargs
):
    """
    Get degraded arrivals from the cache.

    | *Arguments*          | *Description*                                                                 |
    | ``time_window_start``| (Optional) Start of the time window (hours). Default is -1.                   |
    | ``time_window_end``  | (Optional) End of the time window (hours). Default is 6.                      |
    | ``session_key``      | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Degraded Arrivals    time_window_start=-1    time_window_end=6

    """
    kwargs["where"] = (
        f"($timings.AONB >= (NOW + {time_window_end}H) AND $timings.AONB <= (NOW + {time_window_start}H)) OR ($timings.AONB IS NOT SET AND "
        + f"(($timings.EONB >= (NOW + {time_window_end}H) AND $timings.EONB <= (NOW + {time_window_start}H)) OR ($timings.EONB IS NOT SET AND "
        + f"($timings.SONB >= (NOW + {time_window_end}H) AND $timings.SONB <= (NOW + {time_window_start}H)))))"
    )
    return __base_get_data(
        FIDS_DEGRADED_ARRIVALS_VIEW_NAME,
        FIDS_DEGRADED_ARRIVALS_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_DEPARTURE_METADATA_VIEW_NAME = "RefDelegateBean.MetadataFlatTreeByName"
FIDS_DEPARTURE_METADATA_FIELDS = ["path", "value", "displayName"]


def fids_departure_metadata_get(session_key="defaultKey", **kwargs):
    """
    Get departure metadata.

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Departure Metadata

    """
    kwargs["where"] = "sources.mdsName = 'departureTimings'"

    return __base_get_data(
        FIDS_DEPARTURE_METADATA_VIEW_NAME,
        FIDS_DEPARTURE_METADATA_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_DEGRADED_DEPARTURES_VIEW_NAME = "CHDelegateBean.DepartureFlights"
FIDS_DEGRADED_DEPARTURES_FIELDS = [
    "acType3lc",
    "acType5lc",
    "aircraftTerminal",
    "airline",
    "boardedPax",
    "bookedPax",
    "callsign",
    "chuteList",
    "chuteRange",
    "chutes",
    "codeshareList",
    "commonCounterList",
    "commonCounterRanges",
    "counterList",
    "counterRange",
    "counterRanges",
    "counters",
    "direction",
    "displayCode",
    "durations",
    "flightKey",
    "gateList",
    "gateRange",
    "gates",
    "iataFlightNumber",
    "icaoFlightNumber",
    "publicFlightNumber",
    "publicTerminal",
    "registration",
    "runway",
    "remarks",
    "routings",
    "securityLevel",
    "serviceType",
    "specialEmphasis",
    "standList",
    "stands",
    "statuses",
    "suffix",
    "timings",
    "trafficType",
    "tripNumber",
    "_name",
]


def fids_degraded_departures_get(
    time_window_start=-1, time_window_end=6, session_key="defaultKey", **kwargs
):
    """
    Get degraded departures from the cache.

    | *Arguments*          | *Description*                                                                 |
    | ``time_window_start``| (Optional) Start of the time window (hours). Default is -1.                   |
    | ``time_window_end``  | (Optional) End of the time window (hours). Default is 6.                      |
    | ``session_key``      | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Degraded Departures    time_window_start=-1    time_window_end=6

    """
    kwargs["where"] = (
        f"($timings.AOFB >= (NOW + {time_window_end}H) AND $timings.AOFB <= (NOW + {time_window_start}H)) OR ($timings.AOFB IS NOT SET AND (($timings.EOFB >= (NOW + {time_window_end}H) AND $timings.EOFB <= (NOW + {time_window_start}H)) OR ($timings.EOFB IS NOT SET AND ($timings.SOFB >= (NOW + {time_window_end}H) AND $timings.SOFB <= (NOW + {time_window_start}H)))))"
    )

    return __base_get_data(
        FIDS_DEGRADED_DEPARTURES_VIEW_NAME,
        FIDS_DEGRADED_DEPARTURES_FIELDS,
        session_key,
        **kwargs,
    )


FIDS_DEGRADED_COMMON_ALLOCATIONS_VIEW_NAME = "CHDelegateBean.CommonAllocations"
FIDS_DEGRADED_COMMON_ALLOCATIONS_FIELDS = [
    "airlineCodes",
    "airlineList",
    "allocationKey",
    "footerText",
    "freeText",
    "name",
    "paxClass",
    "previous",
    "previousCode",
    "previousChangeTime",
    "remarkFreeText",
    "remarks",
    "resource",
    "resourceSubType",
    "resourceType",
    "serviceId",
    "serviceName",
    "subTypes",
    "timings",
    "webContent",
    "_name",
]


def fids_degraded_common_allocations_get(
    time_window_start=-12, time_window_end=12, session_key="defaultKey", **kwargs
):
    """
    Get degraded common allocations from the cache.

    | *Arguments*          | *Description*                                                                 |
    | ``time_window_start``| (Optional) Start of the time window (hours). Default is -12.                  |
    | ``time_window_end``  | (Optional) End of the time window (hours). Default is 12.                     |
    | ``session_key``      | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Degraded Common Allocations    time_window_start=-12    time_window_end=12

    """
    kwargs["where"] = (
        "$timings.planStart IS NOT SET OR "
        + f"($timings.planStart >= (NOW + {time_window_end}H) AND $timings.planStart <= (NOW + {time_window_start}H))"
    )
    return __base_get_data(
        FIDS_DEGRADED_COMMON_ALLOCATIONS_VIEW_NAME,
        FIDS_DEGRADED_COMMON_ALLOCATIONS_FIELDS,
        session_key,
        **kwargs,
    )
