*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=CDS
Suite Teardown      No Operation


*** Test Cases ***
001_CDS_V1_GET_RULE_TEMPLATE_BY_ID
    ${response}    Cds V1 Get Rule Template By Id

002_CDS_V1_GET_RULE_TEMPLATES
    ${response}    Cds V1 Get Rule Templates

003_CDS_V1_GET_RULE_BY_ID
    ${response}    Cds V1 Get Rule By Id

004_CDS_V1_GET_RULES
    ${response}    Cds V1 Get Rules

005_CDS_V1_GET_RULES_FOM_TEMPLATE_ID
    ${response}    Cds V1 Get Rules For Template

006_CDS_V1_GET_RULE_GROUP_BY_ID
    ${response}    Cds V1 Get Rule Group By Id

007_CDS_V1_GET_RULE_GROUPS
    ${response}    Cds V1 Get Rule Groups

008_CDS_V1_GET_RULE_GROUPS_FOR_TEMPLATE
    ${response}    Cds V1 Get Rule Groups For Template

009_CDS_V1_GET_TAGS
    ${response}    Cds V1 Get Tags

010_CDS_V1_GET_TAGS_FOR_TEMPLATE
    ${response}    Cds V1 Get Tags For Template

011_CDS_V1_GET_STATISTICS
    ${response}    Cds V1 Get Statistics
