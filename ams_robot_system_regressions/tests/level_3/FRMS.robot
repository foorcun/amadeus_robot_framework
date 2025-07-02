*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=SGA
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_FRMS_CREATE_PLAN
    ${creation_time}    Get Date    date_format=%Y-%m-%dT%H:%M:%S
    ${plan_start_date}    Get Date    days=${1}    date_format=%Y-%m-%d
    ${plan_end_date}    Get Date    days=${2}    date_format=%Y-%m-%d
    ${plan_name}    Catenate    ROBOT PLAN    ${creation_time}

    # Create plan
    ${created_frms_plan}    Frms Create Plan
    ...    resource_type=STAND
    ...    name=${plan_name}
    ...    start_date=${plan_start_date}
    ...    end_date=${plan_end_date}
    ${fetched_frms_plan}    Frms Get Plan By Id    ${created_frms_plan["id"]}
    Should Be Equal    first=${fetched_frms_plan["id"]}    second=${created_frms_plan["id"]}

002_FRMS_CREATE_RULE
    ${creation_time}    Get Date    date_format=%Y-%m-%dT%H:%M:%S
    ${rule_name}    Catenate    ROBOT RULE    ${creation_time}

    # Create rule
    ${created_frms_rule}    Frms Create Allocation Rule    resource_type=STAND    name=${rule_name}
    ${fetched_frms_rule}    Frms Get Rule By Id    ${created_frms_rule["id"]}
    Should Be Equal    first=${fetched_frms_rule["id"]}    second=${created_frms_rule["id"]}
