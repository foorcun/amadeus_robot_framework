*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../../resources/generic_keywords.resource
Resource            ../../../resources/frms_keywords.resource
Resource            helpers.robot

Suite Setup         Setup    applications=SDS,VIP,FOM,SGA
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_PUBLISH_STAND_ALLOCATION
    [Documentation]    Publish stand allocation from FRMS to FOM

    # Initialize reference data
    ${customer_id}    ams.Get Customer Id
    ${ref_airport_id}    ams.Get Ref Airport Id
    ${airline}    Sds Save Airline    ZZ
    ${airport}    Sds Save Airport    ZZZ
    ${aircraft_type}    Sds Save Aircraft Type    720

    # TODO VC: unhardcode stand id
    VAR    ${stand_id}    STD000129

    # Create flight in FOM
    ${flight}    Helper Create Flight    type=ARRIVAL    airline=${airline}    airport=${airport}    aircraft_type=${aircraft_type}
    VAR    ${flight_id}    ${flight["id"]}

    # Initially, there is no stand allocations in FOM
    ${stand_allocations}    Fom Find Allocations In Flight    flight=${flight}    resource_type=STAND
    Should Be Empty    item=${stand_allocations}

    # Check flight has been propagated to FRMS
    ${plan_id}    Helper Check Flight Propagated to FRMS    flight_id=${flight_id}    resource_type=STAND

    # Initially, stand allocation should be unassigned in FRMS (since in critical window)
    ${frms_plan}    Frms Get Plan By Id    plan_id=${plan_id}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    ${stand_allocations}    Frms Get Allocations    ${frms_visit}    STAND
    Should Be Equal    first=${stand_allocations[0]["resourceId"]}    second=${None}

    # Move to stand
    Frms Move Allocation
    ...    plan_id=${plan_id}
    ...    allocation_id=${stand_allocations[0]["id"]}
    ...    resource_type=STAND
    ...    resource_id=${stand_id}

    # Check allocation has moved
    ${frms_plan}    Frms Get Plan By Id    plan_id=${plan_id}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    ${stand_allocations}    Frms Get Allocations    visit=${frms_visit}    resource_type=STAND
    Should Be Equal    first=${stand_allocations[0]["resourceId"]}    second=${stand_id}

    # Publish
    Frms Publish Visit    plan_id=${plan_id}    visit_id=${frms_visit["diffs"]["visitId"]}

    # Check stand allocation in FOM
    ${flight}    Fom V3 Movement By Id    movement_id=${flight_id}
    ${stand_allocations}    Fom Find Allocations In Flight    flight=${flight}    resource_type=STAND
   
    VAR    ${stand_allocation}    ${stand_allocations[0]["allocation"][0]}
    Should Be Equal    first=${stand_allocation["resourceId"]["id"]}    second=${stand_id}
