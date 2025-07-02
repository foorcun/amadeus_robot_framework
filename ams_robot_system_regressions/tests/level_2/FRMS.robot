*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=SGA
Suite Teardown      No Operation


*** Test Cases ***
001_FRMS_GET_PLAN_BY_ID
    ${frms_plans}    Frms Get Plans
    ${stand_gate_plan}    Frms Find Operational Plan    ${frms_plans}    STAND
    ${frms_plan}    Frms Get Plan By Id    ${stand_gate_plan["id"]}
