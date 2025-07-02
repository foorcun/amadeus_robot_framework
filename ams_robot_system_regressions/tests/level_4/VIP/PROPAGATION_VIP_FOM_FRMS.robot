*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource
Resource            ../../resources/fom_keywords.resource
Resource            ../../resources/frms_keywords.resource

Suite Setup         Setup    applications=SDS,VIP,FOM,SGA
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_PROPAGATION_VIP_FOM_FRMS
    [Documentation]    Check propagation from VIP to FOM, and FOM to FRMS

    # Initialize reference data
    ${customer_id}    ams.Get Customer Id
    ${ref_airport_id}    ams.Get Ref Airport Id
    ${airline}    Sds Save Airline    ZZ
    ${airport}    Sds Save Airport    ZZZ
    ${aircraft_type}    Sds Save Aircraft Type    720

    # Initialize flight data
    ${flightNumber}    Generate Flight Number    ${4}

    ${period_start}    Get Date    days=${0}    time_format=12:00    date_format=%Y-%m-%dT%H:%M:%S
    ${period_end}    Get Date    days=${1}    time_format=13:12    date_format=%Y-%m-%dT%H:%M:%S

    ${leg_period_data_params}    Create Dictionary    refAirport=${ref_airport_id}
    ${leg_period_data}    Create Dictionary
...    params=&{leg_period_data_params}
...    customerId=${customer_id}
...    airlineCode=${airline["iataCode"]}
...    flightNumber=${flightNumber}
...    arrivalAirport=${ref_airport_id}
...    aircraftType=${aircraft_type["id"]}
...    departureAirport=${airport["id"]}
...    depPeriodDaysOfOp=1234567
...    arrPeriodDaysOfOp=1234567
...    startOfDeparturePeriod=${period_start}
...    endOfDeparturePeriod=${period_end}
...    startOfArrivalPeriod=${period_start}
...    endOfArrivalPeriod=${period_end}
...    serviceType=J

    # Create leg period in VIP
    ${leg_period}    Create Manual Source Leg Period    leg_data=${leg_period_data}

    # Retry for visit creation in FOM (wait for specific visit)
    ${visit}    Wait Until AMS Keyword Succeeds
    ...    FOM Find Visit
    ...    ${airline["iataCode"]}
    ...    ${flightNumber}
    ...    ${period_start}
    ...    ${period_end}

    # Check flight has been propagated to FRMS
    ${frms_plans}    Frms Get Plans
    ${stand_gate_plan}    Frms Find Operational Plan    plan_list=${frms_plans}    resource_type=STAND

    # Retry for FRMS plan availability and visit presence
    ${frms_plan}    Wait Until AMS Keyword Succeeds
    ...    Frms Find Visit By Plan Id
    ...    ${stand_gate_plan["id"]}
    ...    ${visit["inboundMovement"]["id"]}
