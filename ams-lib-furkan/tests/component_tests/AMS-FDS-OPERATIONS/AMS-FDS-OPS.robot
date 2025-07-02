*** Settings ***
Library             ams
Library             protocols

Test Setup          Open Generic Ams Session    protocol=REST    environment=INT_XYZ
...                     current_directory=${CURDIR}    test_name=${TEST_NAME}
Test Teardown       No Operation


*** Test Cases ***
001_AODB_FDS_GET_OPS
    ${history_response}    Get Flight History
    ...    endpoint_type=deltaMovements    movement_id=C_TAM_1114__20250327_ARRIVAL_XYZA
    Log    ${history_response.json()}
