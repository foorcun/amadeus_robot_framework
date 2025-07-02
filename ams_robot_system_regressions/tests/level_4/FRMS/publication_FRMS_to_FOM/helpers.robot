*** Settings ***
Library             ams
Library             ams/commons.py
Resource            ../../../resources/generic_keywords.resource


*** Keywords ***
Helper Create Flight
    [Arguments]    ${type}    ${airline}    ${airport}    ${aircraft_type}    

    ${flight_number}    Generate Flight Number    length=${4}
    ${onb}    Get Date    hours=${0}    date_format=%Y-%m-%dT%H:%M:%S
    ${flight_data}    Create Dictionary
    ...    airline=${airline}
    ...    airport=${airport}
    ...    aircraftType=${aircraft_type}
    ...    flightNumber=${flight_number}
    ...    type=${type}
    ...    time=${onb}
    ${response}    Fom V3 Create Movement    flight_data=${flight_data}

    RETURN    ${response["content"][0]["content"][0]}


Helper Check Flight Propagated to FRMS
    [Arguments]    ${flight_id}    ${resource_type}
    
    ${frms_plans}    Frms Get Plans
    ${plan_container}    Frms Find Operational Plan    plan_list=${frms_plans}    resource_type=${resource_type}

    Wait Until AMS Keyword Succeeds
    ...    Frms Find Visit By Plan Id
    ...    ${plan_container["id"]}
    ...    ${flight_id}

    RETURN    ${plan_container["id"]}

