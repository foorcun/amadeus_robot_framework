*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource
Resource            ../../resources/msc_keywords.resource

Suite Setup         Setup    applications=MSC
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001 Register then Unregister Alerts
    ${alert_list}    MSC V2 Get List Alert    max_no_of_alerts=3
    MSC V2 Post Register Alerts    alerts=${alert_list}
    ${registered_alerts}    MSC V2 Get Register Alerts
    MSC V2 Post Unregister Alerts    alerts=${registered_alerts}

002 Add and Remove Star from Message
    ${start}    Get Date    days=${-2}
    ${end}    Get Date
    ${filters}    Create Dictionary
    ...    startDate=${start}T00:00:00.000Z
    ...    endDate=${end}T23:59:59.000Z

    ${message_list}    MSC V3 Post List Message    filters=${filters}

    ${message_list_size}    Get Length    item=${message_list}
    IF    ${message_list_size} == 0    BuiltIn.Skip    msg=No messages to Star

    ${correlation_ids}    MSC V3 Message List Extract Correlation Ids    message_list=${message_list}

    MSC V2 Get Add Star    apt_correlation_ids=${correlation_ids}
    MSC V2 Get Remove Star    apt_correlation_ids=${correlation_ids}
