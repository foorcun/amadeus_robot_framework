*** Settings ***
Documentation       Resource File to define generic keywords for AMS system

Library             ams
Library             ams/commons.py
Resource            global_variables.resource

*** Keywords ***
Setup
    [Arguments]    ${applications}    ${protocol}=REST    ${current_directory}=${CURDIR}

    Precondition Applications Deployed    applications=${applications}
    Open Generic Ams Session    protocol=${protocol}    current_directory=${current_directory}


Wait Until AMS Keyword Succeeds
    [Arguments]    ${keyword}    @{args}    ${retry_count}=${RETRY_COUNT}    ${retry_interval}=${RETRY_INTERVAL}

    ${result}=    Wait Until Keyword Succeeds    ${retry_count}x    ${retry_interval}    ${keyword}    @{args}
    RETURN    ${result}