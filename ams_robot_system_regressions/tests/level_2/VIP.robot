*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=VIP
Suite Teardown      No Operation


*** Test Cases ***
VIP_V1_legperiods_all
    vip_v1_legperiods_all

VIP_V1_legperiods_all with flightNumber
    vip_v1_legperiods_all    flight_number=0

VIP_V1_seasons
    vip_v1_seasons

VIP_V1_exports
    vip_v1_exports

VIP_V1_cannedmessages
    vip_v1_cannedmessages

VIP_V1_messages_statsbatches
    vip_v1_messages_statsbatches    recon_source=AMGUIRecon
