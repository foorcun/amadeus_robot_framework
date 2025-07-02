*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=CFG
Suite Teardown      No Operation


*** Test Cases ***
001_CFG_V1_GET_CONFIGURATIONS
    ${response}    Cfg V1 Get Configurations

002_CFG_V1_GET_CONFIGURATION
    ${response}    Cfg V1 Get Configuration

003_CFG_V2_GET_CONFIGURATION
    ${additional_params}    Create Dictionary    conf_id=1A
    ${response}    Cfg V2 Get Configuration

004_CFG_V2_GET_FEATURES
    ${response}    Cfg V2 Get Features

005_CFG_V2_GET_CONFIGURATION_APPLICATION
    ${response}    Cfg V2 Get Configuration Application
