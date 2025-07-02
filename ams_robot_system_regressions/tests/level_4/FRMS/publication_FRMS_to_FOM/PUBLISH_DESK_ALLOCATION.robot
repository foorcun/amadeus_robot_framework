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
001_PUBLISH_DESK_ALLOCATION
    [Documentation]    Publish desk allocation from FRMS to FOM

    # Initialize reference data
    ${customer_id}    ams.Get Customer Id
    ${ref_airport_id}    ams.Get Ref Airport Id
    ${airline}    Sds Save Airline    ZZ
    ${airport}    Sds Save Airport    ZZZ
    ${aircraft_type}    Sds Save Aircraft Type    720

    # Create demand rule for desks
    ${creation_time}    Get Date    date_format=%Y-%m-%dT%H:%M:%S
    ${rule_name}    Catenate    ROBOT RULE    ${creation_time}
    ${rule}    Frms Create Dedicated Demand Rule    resource_type=CHECK_IN_DESK    name=${rule_name}    offset_dep_before=-20    offset_dep_after=20
    Frms Change Rule Priority    rule_id=${rule["id"]}    priority=1

    # TODO VC: unhardcode desk id
    VAR    ${desk_id}    CKD000061

    # Create flight in FOM
    ${flight}    Helper Create Flight    type=DEPARTURE    airline=${airline}    airport=${airport}    aircraft_type=${aircraft_type}
    VAR    ${flight_id}    ${flight["id"]}
    ${ofb}    Fom Find Timing    timings=${flight["operationTimeDuration"]}    time_type=SCT    qualifier=OFB

    # Initially, there is no desk allocations in FOM
    ${desk_allocations}    Fom Find Allocations In Flight    flight=${flight}    resource_type=CHECK_IN_DESK
    Should Be Empty    item=${desk_allocations}

    # Check flight has been propagated to FRMS
    ${plan_id}    Helper Check Flight Propagated to FRMS    flight_id=${flight_id}    resource_type=CHECK_IN_DESK

    # Initially, desk allocation should be unassigned in FRMS (since in critical window)
    ${frms_plan}    Frms Get Plan By Id    plan_id=${plan_id}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    ${desk_allocations}    Frms Get Allocations    ${frms_visit}    CHECK_IN_DESK
    Should Be Equal    first=${desk_allocations[0]["resourceId"]}    second=${None}

    # Move to desk
    Frms Move Allocation
    ...    plan_id=${plan_id}
    ...    allocation_id=${desk_allocations[0]["id"]}
    ...    resource_type=CHECK_IN_DESK
    ...    resource_id=${desk_id}

    # Check allocation has moved
    ${frms_plan}    Frms Get Plan By Id    plan_id=${plan_id}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    ${desk_allocations}    Frms Get Allocations    visit=${frms_visit}    resource_type=CHECK_IN_DESK
    Should Be Equal    first=${desk_allocations[0]["resourceId"]}    second=${desk_id}

    # Publish
    Frms Publish Visit    plan_id=${plan_id}    visit_id=${frms_visit["diffs"]["visitId"]}

    # Check desk allocation in FOM
    ${flight}    Fom V3 Movement By Id    movement_id=${flight_id}
    ${desk_allocations}    Fom Find Allocations In Flight    flight=${flight}    resource_type=CHECK_IN_DESK

    VAR    ${desk_allocation}    ${desk_allocations[0]["allocation"][0]}
    Should Be Equal    first=${desk_allocation["resourceId"]["id"]}    second=${desk_id}
    
    ${expected_alst}    Add Time To Date    date=${ofb}    time=-20m    result_format=datetime
    ${actual_alst}    Fom Find Timing    timings=${desk_allocation["allocationTimings"]}    time_type=SCT    qualifier=ALST
    Should Be Equal    first=${expected_alst}    second=${actual_alst}

    ${expected_alet}    Add Time To Date    date=${ofb}    time=20m    result_format=datetime
    ${actual_alet}    Fom Find Timing    timings=${desk_allocation["allocationTimings"]}    time_type=SCT    qualifier=ALET
    Should Be Equal    first=${expected_alet}    second=${actual_alet}
