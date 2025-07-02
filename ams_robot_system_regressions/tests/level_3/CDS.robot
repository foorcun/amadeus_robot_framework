*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=CDS
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_V1_CDS_CREATE_RULE
    ${rule}    Cds V1 Create Rule

    # Validate Rule Creation
    Should Not Be Empty    ${rule}
    Should Contain    ${rule}    uuid
    Should Contain    ${rule}    name
    Should Contain    ${rule}    rawContent
    Should Contain    ${rule}    whenClause
    Should Contain    ${rule}    thenClause
