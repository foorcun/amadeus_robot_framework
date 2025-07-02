*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=SDS
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
SDS_SAVE_AIRCRAFT_TYPE
    Sds Save Aircraft Type    iata=720    icao=B720    force_creation=True

SDS_SAVE_AIRLINE
    Sds Save Airline    iata=ZZ    icao=ZZA    force_creation=True

SDS_SAVE_AIRPORT
    Sds Save Airport    iata=ZZZ    icao=ZZZA    force_creation=True

SDS_SAVE_NATURE_CODE
    Sds Save Nature Code
    ...    code=ADP
    ...    flight_activity=Arrival
    ...    flight_category=Domestic
    ...    flight_type=Passenger
    ...    iata_service_type=J

SDS_SAVE_TERMINAL
    Sds Save Terminal    code=T4

SDS_SAVE_BAGGAGE_BELT
    Sds Save Baggage Belt    name=BB1    terminal=T1    swing_belt=True

SDS_SAVE_BAGGAGE_CHUTE
    Sds Save Baggage Chute    name=MU22    terminal=T2

SDS_SAVE_RUNWAY
    Sds Save Runway    name=RWY5    direction_1=North    direction_2=East    default_usage=Arrival
