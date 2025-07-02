*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=MSC
Suite Teardown      No Operation


*** Test Cases ***
001_MSC_V2_GET_LIST_ALERT
    MSC V2 Get List Alert

002_MSC_V2_GET_LIST_ALERT_COUNT
    MSC V2 Get List Alert Count

003_MSC_V2_GET_LABEL_LIST
    MSC V2 Get Label List

004_MSC_V2_GET_MESSAGE_DETAIL
    MSC V2 Get Message Detail

005_MSC_V2_GET_SUB_MESSAGE_DETAIL
    MSC V2 Get Sub Message Detail

006_MSC_V2_GET_ERROR_LIST
    MSC V2 Get Error List

007_MSC_V2_GET_REGISTER_ALERTS
    MSC V2 Get Register Alerts

008_MSC_V2_GET_MESSAGE_ENTITY
    MSC V2 Get Message Entity

009_MSC_V2_GET_MESSAGE_LABEL
    MSC V2 Get Message Label

010_MSC_V2_GET_HISTORY
    MSC V2 Get History

011_MSC_V2_GET_SUB_MESSAGE_LIST
    MSC V2 Get Sub Message List

012_MSC_V2_GET_ALERT_LIST
    MSC V2 Get Alert List

013_MSC_V2_GET_MESSAGE_ARCHIVES
    MSC V2 Get Message Archives

014_MSC_V2_GET_HISTORY_MESSAGE_META
    MSC V2 Get History Message Meta

015_MSC_V2_GET_STRUCTURED_MESSAGE
    MSC V2 Get Structured Message

016_MSC_V3_POST_LIST_MESSAGE
    ${today}    Get Date
    ${filters}    Create Dictionary
    ...    startDate=${today}T00:00:00.000Z
    ...    endDate=${today}T23:59:59.000Z

    MSC V3 Post List Message    filters=${filters}
