*** Settings ***
Library             ams
Library             protocols
Resource            keywords.resource

Test Setup          Open Generic Ams Session    protocol=REST    environment=INT_XYZ
...                     current_directory=${CURDIR}    context_file=001_AODB_VIP_CREATE_GET_LEGPRD
Test Teardown       automatic_data_cleanup


*** Test Cases ***
001_AODB_VIP_CREATE_GET_LEGPRD
    ${leg_response}    Create Manual Source Leg Period
    ...    expected_response_code=200    endpoint_type=legPeriods

    Validate Create Leg Period Response Schema    ${leg_response}
    Validate Create Leg Period General Processing    status=OK    response=${leg_response}

    ${additional_params}    Create Dictionary    adhocFlag=MIXED
    ${response_all}    Get Leg Periods
    ...    expected_response_code=200
    ...    endpoint_type=all
    ...    default_params=flightNumber,customerId
    ...    additional_params=${additional_params}

    Validate Get Leg Period Response Schema Ok    ${response_all}

    ${response_orphan}    Get Leg Periods
    ...    expected_response_code=200
    ...    endpoint_type=orphans
    ...    default_params=flightNumber,customerId
    ...    additional_params=${additional_params}
    ${response_multiple}    Get Leg Periods
    ...    expected_response_code=200
    ...    endpoint_type=multipleFlights
    ...    default_params=customerId
    ...    additional_params=${additional_params}

    Validate Get Leg Period Response Schema Ok    ${response_multiple}
    Validate Leg Period Response And Create Movement Id    ${response_all}
