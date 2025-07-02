*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Library             DateTime
Resource            ../../../resources/generic_keywords.resource
Resource            ../../../resources/frms_keywords.resource
Resource            helpers.robot

Suite Setup         Setup    applications=SDS,VIP,FOM,SGA
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_PUBLISH_BELT_ALLOCATION
    [Documentation]    Publish belt allocation from FRMS to FOM

    # Initialize reference data
    ${customer_id}    ams.Get Customer Id
    ${ref_airport_id}    ams.Get Ref Airport Id
    ${airline}    Sds Save Airline    ZZ
    ${airport}    Sds Save Airport    ZZZ
    ${aircraft_type}    Sds Save Aircraft Type    720

    # Create demand rule for belts
    ${creation_time}    Get Date    date_format=%Y-%m-%dT%H:%M:%S
    ${rule_name}    Catenate    ROBOT RULE    ${creation_time}
    ${rule}    Frms Create Dedicated Demand Rule    resource_type=BAGGAGE_BELT    name=${rule_name}    offset_arr_before=-20    offset_arr_after=20
    Frms Change Rule Priority    rule_id=${rule["id"]}    priority=1

    # TODO VC: unhardcode belt id
    VAR    ${belt_id}    ABB000221

    # Create flight in FOM
    ${flight}    Helper Create Flight    type=ARRIVAL    airline=${airline}    airport=${airport}    aircraft_type=${aircraft_type}
    VAR    ${flight_id}    ${flight["id"]}
    ${onb}    Fom Find Timing    timings=${flight["operationTimeDuration"]}    time_type=SCT    qualifier=ONB

    # Initially, there is no belt allocations in FOM
    ${belt_allocations}    Fom Find Allocations In Flight    flight=${flight}    resource_type=BAGGAGE_BELT
    Should Be Empty    item=${belt_allocations}

    # Check flight has been propagated to FRMS
    ${plan_id}    Helper Check Flight Propagated to FRMS    flight_id=${flight_id}    resource_type=BAGGAGE_BELT

    # Initially, belt allocation should be unassigned in FRMS (since in critical window)
    ${frms_plan}    Frms Get Plan By Id    plan_id=${plan_id}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    ${belt_allocations}    Frms Get Allocations    ${frms_visit}    BAGGAGE_BELT
    Should Be Equal    first=${belt_allocations[0]["resourceId"]}    second=${None}

    # Move to belt
    Frms Move Allocation
    ...    plan_id=${plan_id}
    ...    allocation_id=${belt_allocations[0]["id"]}
    ...    resource_type=BAGGAGE_BELT
    ...    resource_id=${belt_id}

    # Check allocation has moved
    ${frms_plan}    Frms Get Plan By Id    plan_id=${plan_id}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    ${belt_allocations}    Frms Get Allocations    visit=${frms_visit}    resource_type=BAGGAGE_BELT
    Should Be Equal    first=${belt_allocations[0]["resourceId"]}    second=${belt_id}

    # Publish
    Frms Publish Visit    plan_id=${plan_id}    visit_id=${frms_visit["diffs"]["visitId"]}

    # Check belt allocation in FOM
    ${flight}    Fom V3 Movement By Id    movement_id=${flight_id}
    ${belt_allocations}    Fom Find Allocations In Flight    flight=${flight}    resource_type=BAGGAGE_BELT

    VAR    ${belt_allocation}    ${belt_allocations[0]["allocation"][0]}
    Should Be Equal    first=${belt_allocation["resourceId"]["id"]}    second=${belt_id}
    
    ${expected_alst}    Add Time To Date    date=${onb}    time=-20m    result_format=datetime
    ${actual_alst}    Fom Find Timing    timings=${belt_allocation["allocationTimings"]}    time_type=SCT    qualifier=ALST
    Should Be Equal    first=${expected_alst}    second=${actual_alst}

    ${expected_alet}    Add Time To Date    date=${onb}    time=20m    result_format=datetime
    ${actual_alet}    Fom Find Timing    timings=${belt_allocation["allocationTimings"]}    time_type=SCT    qualifier=ALET
    Should Be Equal    first=${expected_alet}    second=${actual_alet}
