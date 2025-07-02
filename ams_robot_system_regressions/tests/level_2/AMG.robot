*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=AMG
Suite Teardown      No Operation


*** Test Cases ***
001_AMG_ENVIRONMENTS_CONFIG
    ${response}    Amg Environments Config

002_AMG_COMPONENTS_VERSION
    # Http Call And Check    path=/aodb/services/environment/components/version
    ${response}    Amg Components Version

003_AMG_ENVIRONMENT_SEASON
    # Http Call And Check    path=/aodb/services/environment/season
    ${response}    Amg Environment Season

004_AMG_COLUMN_CONFIG
    # Http Call And Check    path=/aodb/services/environment/config/columnConfig
    ${response}    Amg Column Config

005_AMG_MILESTONE
    # Http Call And Check    path=/aodb/services/configuration/lists/milestone
    ${response}    Amg Milestone
