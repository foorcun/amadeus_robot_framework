*** Settings ***
Library             ams
Library             protocols
Resource            keywords.resource

Test Setup          Open Generic Ams Session    protocol=REST    environment=INT_XYZ
...                     current_directory=${CURDIR}    context_file=AODB_FOM_OPS
Test Teardown       Cleanup Flight Data In Ops


*** Variables ***
${MOVEMENT_ID}      movement_id


*** Test Cases ***
001_AODB_FOM_CREATE_INBOUND_OUTBOUND_FLIGHT
    ${response}    Create Inbound Or Outbound Flight    type=DEPARTURE
    ...    expected_response_code=200    endpoint_type=adhoc
    Validate Inbound Or Outbound Flight Response Schema    ${response}
    Validate Inbound Or Outbound Flight General Processing    response=${response}
    ${id_details}    Get Flight Details    ${response}    key=id
    ${movement_id}    Set Variable    ${id_details}
    Log    Flight ID: ${movement_id}

002_AODB_FOM_CREATE_TURNAROUND_FLIGHT
    ${response}    Create Turnaround Flight
    ...    expected_response_code=200    endpoint_type=adhoc
    Validate Turn Around Flight Response Schema    ${response}
    Validate Turn Around Flight General Processing    response=${response}
    ${id_details}    Get Flight Details    ${response}    key=id
    ${movement_id}    Set Variable    ${id_details}
    Log    Flight ID: ${movement_id}

003_AODB_FOM_GET_MOVEMENT_ID
    Get Movement Id Details    movement_id= ${MOVEMENT_ID}
