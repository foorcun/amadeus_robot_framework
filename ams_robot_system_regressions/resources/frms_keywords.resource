*** Settings ***
Documentation       Resource File to define generic keywords for AMS system

Library             ams
Library             ams/commons.py


*** Keywords ***
Frms Find Visit By Plan Id
    [Arguments]    ${plan_id}    ${flight_id}
    
    ${frms_plan}    Frms Get Plan By Id    ${plan_id}
    Should Not Be Empty    ${frms_plan}
    ${frms_visit}    Frms Find Visit In Plan    plan=${frms_plan}    flight_id=${flight_id}
    Should Not Be Empty    ${frms_visit}
    RETURN    ${frms_visit}


