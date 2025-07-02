*** Settings ***
Library             ams
Resource            keywords.resource

Test Setup          Open Generic Ams Session    protocol=REST    environment=INT_XYZ
...                     current_directory=${CURDIR}    context_file=AODB_FOM_OPS
Test Teardown       No Operation


*** Variables ***
${EVENT_TYPE}       "divert_cancel"


*** Test Cases ***
001_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_TIME
    ${time}    Get Time    ${2}
    ${response}    Update Flight Time
    ...    expected_response_code=200
    ...    movement_id=C_UAE_2166__20250412_ARRIVAL_XYZA
    ...    op_type=update_flight_time
    ...    leg_type=inbound
    ...    timing_type=AIBT
    ...    time=${time}
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

002_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_DIVERSION
    ${time}    Get Time    ${2}
    ${divert_time}    Get Time    ${3}
    ${response}    ADD DIVERSION    ${EVENT_TYPE}    C_UAE_9392__20250412_DEPARTURE_XYZA    ${time}    ${divert_time}
    Get Flight Details    ${response}    key=event
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

003_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_ALERT
    ${response}    Update Flight Alert
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_alert
    ...    alert_code=neo11
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

004_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_OP_STATUS
    ${time}    Get Time    ${2}
    ${response}    Update Flight Op Status
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_op_status
    ...    update_type=reinstantiate
    ...    time=${time}
    Get Flight Details    ${response}    key=event
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

005_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_DELAY
    ${response}    Update Flight Delay
    ...    expected_response_code=200
    ...    movement_id=C_UAE_2166__20250412_ARRIVAL_XYZA
    ...    op_type=update_flight_delay
    ...    delay_type=subdelay
    ...    departure_or_arrival=Arrival
    ...    alpha_code=AAA
    ...    subdelay_alphacode=Aaa
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

006_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_REMARKS
    ${response}    Update Flight Remarks
    ...    expected_response_code=200
    ...    movement_id=C_UAE_2166__20250412_ARRIVAL_XYZA
    ...    op_type=update_flight_remarks
    ...    remark_type=CKD
    ...    remarks=test2
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

007_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_RESOURCES
    ${response}    Update Resource Type    "STAND"    C_UAE_2166__20250412_ARRIVAL_XYZA
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

008_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_TASKS
    ${response}    Update Flight Tasks
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_tasks
    ...    task_type=FuelUplift
    ...    value=15
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

009_AODB_FOM_PUT_VISITS_UPDATE_FLIGHT_LINK
    ${response}    Flight Linkage Operation
    ...    expected_response_code=200
    ...    movement_id=C_UAE_2166__20250412_ARRIVAL_XYZA
    ...    outbound_movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=link
    Validate Visits Partial Response Schema    ${response}
    Validate Visits Partial General Processing    ${response}    status=OK

010_AODB_FOM_PUT_VISITS_FLIGHT_UNLINK
    ${response}    Flight Linkage Operation
    ...    expected_response_code=200
    ...    movement_id=C_UAE_2166__20250412_ARRIVAL_XYZA
    ...    op_type=unlink
    Validate Visits Partial Response Schema    ${response}
    Validate Visits Partial General Processing    ${response}    status=OK

011_AODB_FOM_PUT_VISITS_UPDATE_FLIGHT_TOWS
    ${sobt_time}    Get Time    ${2}
    ${sibt_time}    Get Time    ${3}

    ${all_stand_details}    Get Stand Details    expected_response_code=200
    ${get_random_id}    Get Random Resource Id    response_json=${all_stand_details.json()}
    ${response}    Update Flight Tows
    ...    expected_response_code=200
    ...    movement_id=C_UAE_2166__20250412_ARRIVAL_XYZA
    ...    op_type=update_flight_tows
    ...    resourceId=${get_random_id}
    ...    sobt_time=${sobt_time}
    ...    sibt_time=${sibt_time}

    Validate Visits Partial Response Schema    ${response}
    Validate Visits Partial General Processing    ${response}    status=OK

012_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_HANDLING_AGENT
    ${response}    Update Flight Handling Agent
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_handling_agent
    ...    handling_task=Cleaning
    ...    value=SH07
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

013_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_FIDS_DETAILS
    ${response}    Update Flight Fids Details
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_fids_details
    ...    display_type=EVERYWHERE
    ...    airline=6X
    ...    flight_number=1234
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

014_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_LOAD_DETAILS
    ${response}    Update Flight Load Details
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_load_details
    ...    load_type=C
    ...    count_qualifier=Loaded
    ...    count_value=12
    ...    weight_value=11
    ...    cabin=W
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

015_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_PAX_DETAILS
    ${response}    Update Flight Pax Details
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_pax_details
    ...    cabin_class=F
    ...    count=20
    ...    pax_count_qualifier=Booked
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK

016_AODB_FOM_PUT_MOVEMENT_UPDATE_FLIGHT_AIRCRAFT_DETAILS
    ${registration_id}    Get Aircraft Details    expected_response_code=200
    ${rand_aic_reg_id}    Get Valid Aircraft Registration And Type Mapping    response_json=${registration_id.json()}
    ${response}    Update Flight Aircraft Details
    ...    expected_response_code=200
    ...    movement_id=C_UAE_9392__20250412_DEPARTURE_XYZA
    ...    op_type=update_flight_aircraft_details
    ...    registration=${rand_aic_reg_id["registrationId"]}
    ...    aircraft_type=320
    Validate Movement Partial Response Schema    ${response}
    Validate Movement Partial General Processing    ${response}    status=OK
