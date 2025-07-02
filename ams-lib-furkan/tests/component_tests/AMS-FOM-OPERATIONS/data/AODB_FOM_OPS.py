"""
Data File for FOM Operations
"""

from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as Gad,
)
from ams.data_model.common_libs.utils.date_handler import get_date

sobt = get_date(days=1, time_format="05:40", date_format="%Y-%m-%dT%H:%M:%S")
sibt = get_date(days=1, time_format="09:40", date_format="%Y-%m-%dT%H:%M:%S")

generic_context = {
    "customer_id": None,
    "ref_airport": None,
    "ref_airport_full": None,
    "apt_correlation_id": f"regression{Gad.generate_correlation_id(9)}",
}

create_flight_context = {
    "params": {"refAirport": None},
    "airline": Gad.get_iata_airline_code(),
    "flightNumber": Gad.generate_flight_number(4),
    "departureAirport": "APT_NYC",
    "arrivalAirport": None,
    "registration": None,
    "callsign": "OSNT1400",
    "type": "DEPARTURE",
    "operationTimeDuration": [
        {
            "timeType": "SCT",
            "operationQualifier": "OFB",
            "value": {"time": sobt},
        },
        {
            "timeType": "SCT",
            "operationQualifier": "ONB",
            "value": {"time": sibt},
        },
    ],
    "aircraftType": None,
    "operationalStatus": "OP",
    "serviceType": "J",
    "dataElement": [],
}

create_turnaround_flight_context = {
    "Inairline": Gad.get_iata_airline_code(),
    "InflightNumber": Gad.generate_flight_number(4),
    "IndepartureAirport": "APT_NYC",
    "InarrivalAirport": None,
    "Intype": "ARRIVAL",
    "InoperationTimeDuration": [
        {
            "timeType": "SCT",
            "operationQualifier": "ONB",
            "value": {"time": sobt},
        },
        {
            "timeType": "SCT",
            "operationQualifier": "OFB",
            "value": {"time": sibt},
        },
    ],
    "InaircraftType": None,
    "IndataElement": [],
    "InserviceType": "J",
    "OutflightNumber": Gad.generate_flight_number(4),
    "OutdepartureAirport": None,
    "OutarrivalAirport": "APT_NYC",
    "Outtype": "DEPARTURE",
    "OutoperationTimeDuration": [
        {
            "timeType": "SCT",
            "operationQualifier": "ONB",
            "value": {"time": sobt},
        },
        {
            "timeType": "SCT",
            "operationQualifier": "OFB",
            "value": {"time": sibt},
        },
    ],
}

visit_context = {
    "add_link": {
        "inboundMovementId": "C_ING_1515__20250408_ARRIVAL_XYZA",
        "outboundMovementId": "C_ING_1616__20250409_DEPARTURE_XYZA",
    },
    "unlink": {"inboundMovementId": "C_ING_1515__20250408_ARRIVAL_XYZA"},
    "update_tows": {
        "id": "",
        "dataElement": [],
        "identifier": "wfmf6aywwa7mamaydmaoomfaam6wdmdoydl6o76y6lma76y8mg",
        "timeType": "SCT",
        "operationQualifier": "OFB",
        "time": "2025-03-18T18:00:00.000Z",
        "timeType1": "SCT",
        "operationQualifier1": "ONB",
        "time1": "2025-03-18T18:00:00.000Z",
        "resourceType": "STAND",
        "departureOrArrival": "Arrival",
        "resourceId": "STD000585",
        "order": 1,
        "text": "adding stand",
        "qualifier": "SGA",
    },
}

movement_context = {
    "flight_op_status_update": {
        "timeType": "ACT",
        "operationQualifier": "CNL",
        "time": "time",
        "value": "DX",
        "dataElement": [],
    },
    "timing_update": {
        "timeType": "ACT",
        "operationQualifier": "ONB",
        "dataElement": [],
    },
    "event_update": {
        "type": "DIVERT_CONTINUE",
        "occurrenceTime": "time",
        "timeType": "SCT",
        "operationQualifier": "ONB",
        "time": "time",
        "copyDisruptionDataGroup": ["COPY_FLT_PLAN_DATA"],
        "departureAirport": "APT_HYD",
        "arrOperationalSuffix": "A",
        "dataElement": [],
    },
    "alert_update": {
        "code": "neo11",
        "dataElement": [],
    },
    "update_delay": {
        "departureOrArrival": "Departure",
        "reasonCode": "23",
        "category": "TEST DELAY",
        "alphaCode": "AAA",
        "priority": 1,
        "subDelays": "",
        "freeTextObject": "delay remark",
        "durationObject": "PT12M",
        "dataElement": [],
    },
    "update_remarks": {
        "qualifier": "STAFF",
        "text": "Test1",
        "order": 1,
        "dataElement": [],
    },
    "update_resources": {
        "resourceType": "STAND",
        "departureOrArrival": "Arrival",
        "resourceId": "STD000585",
        "dataElement": [],
    },
    "update_tasks": {
        "qualifier": "FuelUplift",
        "measurement": "13",
        "measurementUnit": "Kilogram",
        "dataElement": [],
    },
    "update_handling_agent": {
        "handlingTask": "TOW",
        "departureOrArrival": "Arrival",
        "value": "SH07",
        "type": "AGENT",
        "dataElement": [],
    },
    "update_fids": {
        "dataElement": [],
        "displayType": "STAFF",
        "airline": "6E",
        "flightNumber": "1213",
    },
    "update_load": {
        "type": "C",
        "destinationType": "ALL",
        "countQualifier": "Accepted",
        "countValue": "11",
        "weightValue": "14",
        "measurementUnit": "Kilogram",
        "cabin": "F",
        "destination": "ALL",
        "dataElement": [],
    },
    "update_pax": {
        "class": "F",
        "paxCount": 10,
        "paxCountQualifier": "Booked",
        "SSRType": "ALL",
        "destinationType": "ALL",
        "dataElement": [],
    },
    "update_aircraft_details": {
        "registration": "AIC004815",
        "aircraftType": "ACT000873",
        "dataElement": [],
    },
}

fom_context = {
    "create_flight_context": create_flight_context,
    "create_turnaround_flight_context": create_turnaround_flight_context,
    "movement_context": movement_context,
    "visit_context": visit_context,
}

test_context = {
    "token_type": "COOKIE",
    "generic_context": generic_context,
    "fom_context": fom_context,
    "user_context": {"mode": "local"},
}
