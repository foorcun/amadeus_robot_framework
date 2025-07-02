*** Settings ***
Documentation       Resource File to define generic keywords for AMS system

Library             ams
Library             ams/commons.py
Library             jmespath


*** Keywords ***
MSC V3 Message List Extract Correlation Ids
    [Arguments]    ${message_list}
    
    ${search}    jmespath.Search    data=${message_list}    expression=mscMessageDTOList[].aptCorrelationId
    RETURN    ${search}
