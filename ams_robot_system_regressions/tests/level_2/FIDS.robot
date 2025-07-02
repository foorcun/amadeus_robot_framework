*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            keywords.resource

Test Setup          Setup
Test Teardown       Tear Down

*** Keywords ***
Setup
    Open Generic Ams Session   protocol=REST    current_directory=${CURDIR}
    Precondition Applications Deployed   applications=FID
    Precondition Component Version Check   component=fid    version_min="2.0.27"
    Fids Login

Tear Down
    Automatic Data Cleanup
    Fids Logout

*** Test Cases ***
# Level 2 Simualte Opening the different FIDS screens in the UI
FIDS_CONTROLLERS
    Fids Controllers Get
    Fids Device Types Get
    Fids File Layouts Get
    Fids Controller Monitor Tags Get
    Fids Selection Rules Get

FIDS_MONITORS
    Fids Controller Monitor Tags Get
    Fids Layouts Hopo Get
    Fids Controllers Get
    Fids Monitors Get

FIDS_LAYOUTS
    Fids Layouts Get
    Fids Monitors Get

FIDS_RULES
    Fids Display Rules Get
    Fids Selection Rules Get

FIDS_MEDIA
    Fids Media Get
    Fids Media Compaign Tags Get
    Fids Media Deleted Get
    Fids External Media Get
    Fids External Media Deleted Get

FIDS_CAMPAIGNS
    Fids Media Compaign Tags Get
    Fids Campaigns Get

FIDS_TRANSLATIONS
    Fids Languages Get
    Fids Codes Get
    Fids Airport Translations Get
    Fids Airline Translations Get

FIDS_PARAMETERS
    Fids System Parameters Get
    Fids Controller Parameters Get
    Fids Monitor Parameters Get

FIDS_MAINTENCE_AND_MONITORING
    Fids System Parameters Get
    Fids Monitors Get
    Fids Controllers Get
    Fids All Devices Get

FIDS_DEGRADED
    Fids Arrival Metadata Get
    Fids Departure Metadata Get
    Fids Degraded Airlines Get
    Fids Degraded Airports Get
    Fids Degraded Arrivals Get
    Fids Degraded Departures Get
    Fids Degraded Common Allocations Get

FIDS_REPORTS
    Fids Client Report Get
    Fids System Report Get

FIDS_SCHEDULED_TASKS
    Fids Controller Monitor Tags Get
    Fids Scheduled Tasks Get

FIDS_MESSSAGING
    Fids Controller Monitor Tags Get
    Fids View Languages Get
    Fids Monitor Zones Get
    Fids Message Languages Get
    Fids Message Template Lanaguages Get
    Fids Message Templates Get
    Fids Messages Get
