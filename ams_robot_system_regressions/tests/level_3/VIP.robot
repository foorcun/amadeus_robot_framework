*** Settings ***
Library             ams
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=VIP
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001 VIP Create and Delete Arrival Manual Legperiod
    ${customer_id}    ams.Get Customer Id
    ${ref_airport}    ams.Get Ref Airport Id

    ${airline}    Sds Save Airline    iata=ZZ    icao=ZZZ
    ${airport}    Sds Save Airport    iata=ZZZ    icao=ZZZZ
    ${aircraft_type}    Sds Save Aircraft Type    iata=ZZA    icao=ZZZA    force_creation=True

    ${period_start}    Get Date    days=${-14}    time_format=12:00    date_format=%Y-%m-%dT%H:%M:%S
    ${period_end}    Get Date    days=${14}    time_format=13:12    date_format=%Y-%m-%dT%H:%M:%S

    ${params}    Create Dictionary    refAirport=${ref_airport}
    ${legdata}    Create Dictionary
    ...    params=${params}
    ...    customerId=${customer_id}
    ...    airlineCode=${airline['id']}
    ...    flightNumber=999
    ...    departureAirport=${airport['id']}
    ...    arrivalAirport=${ref_airport}
    ...    aircraftType=${aircraft_type['id']}
    ...    depPeriodDaysOfOp=1234567
    ...    arrPeriodDaysOfOp=1234567
    ...    startOfDeparturePeriod=${period_start}
    ...    endOfDeparturePeriod=${period_end}
    ...    startOfArrivalPeriod=${period_start}
    ...    endOfArrivalPeriod=${period_end}
    ...    serviceType=J

    ${response}    Create Manual Source Leg Period    leg_data=${legdata}

002 VIP Create and Delete Departure Manual Legperiod
    ${customer_id}    ams.Get Customer Id
    ${ref_airport}    ams.Get Ref Airport Id

    ${airline}    Sds Save Airline    iata=ZZ    icao=ZZZ
    ${airport}    Sds Save Airport    iata=ZZZ    icao=ZZZZ
    ${aircraft_type}    Sds Save Aircraft Type    iata=ZZB    icao=ZZZB    force_creation=True

    ${period_start}    Get Date    days=${-14}    time_format=12:00    date_format=%Y-%m-%dT%H:%M:%S
    ${period_end}    Get Date    days=${14}    time_format=13:12    date_format=%Y-%m-%dT%H:%M:%S

    ${params}    Create Dictionary    refAirport=${ref_airport}
    ${legdata}    Create Dictionary
    ...    params=${params}
    ...    customerId=${customer_id}
    ...    airlineCode=${airline['id']}
    ...    flightNumber=998
    ...    departureAirport=${ref_airport}
    ...    arrivalAirport=${airport['id']}
    ...    aircraftType=${aircraft_type['id']}
    ...    depPeriodDaysOfOp=1234567
    ...    arrPeriodDaysOfOp=1234567
    ...    startOfDeparturePeriod=${period_start}
    ...    endOfDeparturePeriod=${period_end}
    ...    startOfArrivalPeriod=${period_start}
    ...    endOfArrivalPeriod=${period_end}
    ...    serviceType=J

    ${response}    Create Manual Source Leg Period    leg_data=${legdata}
