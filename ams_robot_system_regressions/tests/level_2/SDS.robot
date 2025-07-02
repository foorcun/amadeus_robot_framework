*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=SDS
Suite Teardown      No Operation


*** Test Cases ***
001_SDS_READ_ENDPOINTS
    Sds Test All Read Endpoints
