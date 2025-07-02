*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=FOM
Suite Teardown      No Operation


*** Test Cases ***
001_FOM_V3_MOVEMENTS_BY_ID
    ${response}    Fom V3 Movement By Id    movement_id=TEST

002_FOM_V3_MOVEMENTS_INTERNAL_ID
    ${response}    Fom V3 Movements Internal Id

003_FOM_V3_VISITS_ADDITIONAL_SOURCES
    ${response}    Fom V3 Visits Additional Sources

004_FOM_V4_VISITS_SEARCHES
    ${response}    Fom V4 Visits Searches
