*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=FOM
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_FOM_V3_MOVEMENTS_CRUD_INBOUND_FLIGHT
    # Prepare reference data for flight creation
    ${airline}    Sds Save Airline    iata=AF    icao=AFR
    ${airport}    Sds Save Airport    iata=MIA    icao=KMIA
    ${aircraft_type}    Sds Save Aircraft Type    iata=TST    icao=TTST
    ${aircraft_type_2}    Sds Save Aircraft Type    iata=TS2    icao=TTS2
    ${flight_number}    Generate Flight Number    length=${3}
    ${onb}    Get Date    hours=${0}    date_format=%Y-%m-%dT%H:%M:%S
    ${flight_data}    Create Dictionary
    ...    airline=${airline}
    ...    airport=${airport}
    ...    aircraftType=${aircraft_type}
    ...    flightNumber=${flight_number}
    ...    type=ARRIVAL
    ...    time=${onb}

    # Create inbound flight
    ${response}    Fom V3 Create Movement    flight_data=${flight_data}

    # Capture flight id from response
    ${flight_id}    Get Flight Details From Json    response=${response['content']}    key=id

    # Validate flight data
    ${flight_number_value}    Get Flight Details From Json    response=${response['content']}    key=flightNumber
    ${flight_number_str}    Convert To String    ${flight_number_value['value']}
    ${flight_airline}    Get Flight Details From Json    response=${response['content']}    key=airline
    ${departure_airport}    Get Flight Details From Json    response=${response['content']}    key=departureAirport
    ${flight_aircraft_type}    Get Flight Details From Json    response=${response['content']}    key=aircraftType
    Should Be Equal    ${flight_number_str}    ${flight_number}
    Should Be Equal    ${flight_airline['value']}    ${airline['id']}
    Should Be Equal    ${departure_airport['value']}    ${airport['id']}
    Should Be Equal    ${flight_aircraft_type['value']}    ${aircraft_type['id']}

    # Update flight
    ${flight_data}    Create Dictionary    aircraftType=${aircraft_type_2}
    ${response}    Fom V3 Movements Update Aircraft Type    flight_id=${flight_id}    flight_data=${flight_data}

    # Validate flight data
    ${flight_aircraft_type}    Get Flight Details From Json    response=${response}    key=aircraftType
    Should Be Equal    ${flight_aircraft_type['value']}    ${aircraft_type_2['id']}

002_FOM_V3_MOVEMENTS_CRUD_OUTBOUND_FLIGHT
    # Prepare reference data for flight creation
    ${airline}    Sds Save Airline    iata=AF    icao=AFR
    ${airport}    Sds Save Airport    iata=MIA    icao=KMIA
    ${aircraft_type}    Sds Save Aircraft Type    iata=TST    icao=TTST
    ${aircraft_type_2}    Sds Save Aircraft Type    iata=TS2    icao=TTS2
    ${flight_number}    Generate Flight Number    length=${3}
    ${ofb}    Get Date    hours=${0}    date_format=%Y-%m-%dT%H:%M:%S
    ${flight_data}    Create Dictionary
    ...    airline=${airline}
    ...    airport=${airport}
    ...    aircraftType=${aircraft_type}
    ...    flightNumber=${flight_number}
    ...    type=DEPARTURE
    ...    time=${ofb}

    # Create outbound flight
    ${response}    Fom V3 Create Movement    flight_data=${flight_data}

    # Capture flight id from response
    ${flight_id}    Get Flight Details From Json    response=${response['content']}    key=id

    # Validate flight data
    ${flight_number_value}    Get Flight Details From Json    response=${response['content']}    key=flightNumber
    ${flight_number_str}    Convert To String    ${flight_number_value['value']}
    ${flight_airline}    Get Flight Details From Json    response=${response['content']}    key=airline
    ${arrival_airport}    Get Flight Details From Json    response=${response['content']}    key=arrivalAirport
    ${flight_aircraft_type}    Get Flight Details From Json    response=${response['content']}    key=aircraftType
    Should Be Equal    ${flight_number_str}    ${flight_number}
    Should Be Equal    ${flight_airline['value']}    ${airline['id']}
    Should Be Equal    ${arrival_airport['value']}    ${airport['id']}
    Should Be Equal    ${flight_aircraft_type['value']}    ${aircraft_type['id']}

    # Update flight
    ${flight_data}    Create Dictionary    aircraftType=${aircraft_type_2}
    ${response}    Fom V3 Movements Update Aircraft Type    flight_id=${flight_id}    flight_data=${flight_data}

    # Validate flight data
    ${flight_aircraft_type}    Get Flight Details From Json    response=${response}    key=aircraftType
    Should Be Equal    ${flight_aircraft_type['value']}    ${aircraft_type_2['id']}
