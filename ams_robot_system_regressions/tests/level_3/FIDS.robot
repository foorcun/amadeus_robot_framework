*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            keywords.resource

Test Setup          Setup
Test Teardown       tear down

*** Keywords ***
Setup
    Open Generic Ams Session    protocol=REST    current_directory=${CURDIR}
    Precondition Applications Deployed   applications=FID
    Precondition Component Version Check   component=fid    version_min="2.0.27"
    Fids Login

tear down
    Automatic Data Cleanup
    Web Socket Cleanup
    Fids Logout

*** Test Cases ***
FIDS_MEDIA_CRUD
    # This test covers uploading an image, soft deleting it and then deleting it.
    
    # Open a live update processing
    Fids Media Get   store_id=Media_CRUD
    Fids Media Deleted Get    store_id=DeletedMedia_CRUD

    # Upload new media
    ${response}   Fids Media Upload   file_path=data/level_3/FIDS   file_name=one_pixel.png   content_type=image/png
    ${media}    Fids Get Response Result   ${response}
    
    # Validate the media fields as we would expect from the uploaded file.
    Should Be Equal   ${media['fmeMetadata']}   image/png
    Should Be Equal   ${media['fmeDimensions']}   1x1
    Should Be Equal   ${media['fmeExternalInd']}   ${False}
    Should Be Equal   ${media['fmeDeletedInd']}   ${False}
    Should Be Equal   ${media['fmeName']}   one_pixel

    # Validate the media live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Media_CRUD
    Should Be Equal   ${update['action']}    N
    Should Be Equal   ${media['fmeId']}    ${update['payload']['fmeId']}
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=DeletedMedia_CRUD
    Should Be Empty   ${update}

    # check the media get endpoint as a controller would

    # 'Delete' Media on the screen moves to the delete table (not used by the controllers)
    ${media}[fmeDeletedInd]  Set Variable    ${True}
    ${response}   Fids Media Save   ${media}
    ${media}    Fids Get Response Result   ${response}
    Should Be Equal   ${media['fmeDeletedInd']}   ${True}

    # Validate the media live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Media_CRUD
    Should Be Equal   ${update['action']}    D
    Should Be Equal   ${media['fmeId']}    ${update['payload']['fmeId']}
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=DeletedMedia_CRUD
    Should Be Equal   ${update['action']}    U
    Should Be Equal   ${media['fmeId']}    ${update['payload']['fmeId']}

    # Delete media as a user would from the UI
    ${response}   Fids Media Delete   ${media}
    ${deleted_media}    Fids Get Response Result   ${response}
    Should Be Empty   ${deleted_media}

    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Media_CRUD
    # two 'deletes' because the backend does not keep a list of entities only what this session is interested in
    Should Be Equal   ${update['action']}    D
    Should Be Equal   ${media['fmeId']}    ${update['payload']['fmeId']}
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=DeletedMedia_CRUD
    Should Be Equal   ${update['action']}    D
    Should Be Equal   ${media['fmeId']}    ${update['payload']['fmeId']}

    # Close live update processing
    Fids Close Ui Updates   store_id=Media_CRUD
    Fids Close Ui Updates   store_id=DeletedMedia_CRUD

FIDS_CAMPAIGNS_CRUD
    # This tests creates a campaign, adds a schedule and media to it, then deletes the campaign.

    # Open live update processing
    Fids Campaigns Get   store_id=Campaigns_CRUD

    # Create a campaign
    ${response}   Fids Campaigns Save   name=Test   priority=10
    ${campaign}   Fids Get Response Result   ${response}

    # Validate the campaign
    Should Be Equal As Integers  ${campaign['fcnPriority']}   10
    Should Be True    ${campaign['fcnId']}
    
    # Validate the live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Campaigns_CRUD
    Should Be Equal   ${update['action']}    N
    Should Be Equal   ${campaign['fcnId']}    ${update['payload']['fcnId']}

    # Add schedule to the campaign
    ${response}   Fids Camapigns Schedules Save    ${campaign}   effective_days=234   start_time=00:00   end_time=12:00
    ${campaign_schedule}   Fids Get Response Result   ${response}

    # Validate the campaign schedule
    Should Be Equal  ${campaign_schedule['fcsEffectiveDays']}   234
    Should Be Equal  ${campaign_schedule['fcsEffectiveStartTime']}   00:00
    Should Be Equal  ${campaign_schedule['fcsEffectiveEndTime']}   12:00
    Should Be True  ${campaign_schedule['fcsId']}

    # Upload new media
    ${response}   Fids Media Upload   file_path=data/level_3/FIDS/data   file_name=one_pixel.png   content_type=image/png
    ${media}    Fids Get Response Result   ${response}

    # Add media to the campaign
    ${response}   Fids Campaigns Media Save   ${campaign}   ${media}   duration=200
    ${campaign_media}   Fids Get Response Result   ${response}

    # Validate the campaign media
    Should Be Equal As Integers   ${campaign_media['fccDuration']}   200
    Should Be Equal  ${campaign_media['fccFcnId']}   ${campaign['fcnId']}
    Should Be Equal  ${campaign_media['fccFmeId']}   ${media['fmeId']}

    # Delete the campaign
    ${response}   Fids Campaigns Delete   ${campaign}
    ${deleted_campaign}    Fids Get Response Result   ${response}
    Should Be Empty   ${deleted_campaign}

    # Media should be deletable now that the campaign is deleted
    Fids Media Delete   ${media}

    # Validate the live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Campaigns_CRUD
    Should Be Equal   ${update['action']}    D
    Should Be Equal   ${campaign['fcnId']}    ${update['payload']['fcnId']}

    # Close live update processing
    Fids Close Ui Updates   store_id=Campaigns_CRUD

FIDS_CAMPAIGN_DATA_CHANNEL
    # Monitors that display campaigns will get the campaigns on the data channel

    # Open data web socket with the campaign selection rule
    ${selection_rules}   Create Dictionary   campaign_test=SELECT CAMPAIGNS WHERE ($fcnEffectiveStart IS NOT SET OR $fcnEffectiveStart <= NOW) AND ($fcnEffectiveEnd IS NOT SET OR $fcnEffectiveEnd >= NOW)
    ${campaigns_ws}   Fids Open Data Channel   controller_name="DEVBOX"   monitor_name="DEVBOX"   selection_rules=${selection_rules}
    ${opened_websocket}   Fids Data Channel Wait For Initial Data   ${campaigns_ws}   timeout=60
    Should Be True    ${opened_websocket}

    # Create a campaign
    ${response}   Fids Campaigns Save   name=TestDataChannel
    ${campaign}   Fids Get Response Result   ${response}

    ${data}   Fids Data Channel Find   ${campaigns_ws}    campaign_test    field=fcnId    value=${campaign['fcnId']}   timeout=60
    Should Not Be Empty    ${data}

    # Update the end time to the past
    ${response}   Fids Campaigns Save   name=TestDataChannel   fcnId=${campaign['fcnId']}   fcnEffectiveEnd=2000-01-01T00:00:00.000Z
    ${campaign}   Fids Get Response Result   ${response}

    
    ${data}   Fids Data Channel Empty   ${campaigns_ws}    campaign_test   timeout=60
    Should Be Empty    ${data}

    # Remove the end time
    ${response}   Fids Campaigns Save   name=TestDataChannel   fcnId=${campaign['fcnId']}   fcnEffectiveEnd=${None}
    ${campaign}   Fids Get Response Result   ${response}

    ${data}   Fids Data Channel Find   ${campaigns_ws}    campaign_test    field=fcnId    value=${campaign['fcnId']}   timeout=60
    Should Not Be Empty    ${data}

    # Delete the campaign
    Fids Campaigns Delete   ${campaign}
    
    # Campaign is removed from data channel
    ${data}   Fids Data Channel Find   ${campaigns_ws}    campaign_test    field=fcnId    value=${campaign['fcnId']}   timeout=60
    Should Not Be Empty    ${data}

    # Close web socket
    Fids Close Data Channel   ${campaigns_ws}

FIDS_CONTROLLERS_CRUD
    # This test covers creating a controller, updating it, deleting it and validating the live updates sent.

     # Open live update processing
    Fids Controllers Get   store_id=Controllers_CRUD

    # Create controller
    ${response}   Fids Controllers Save   name=ROBOT   identification=ROBOT_CONTROLLER
    ${controller}   Fids Get Response Result   ${response}

    Should Be Equal    ${controller['fcoCustomerId']}   ROBOT_CONTROLLER
    Should Be Equal    ${controller['fcoName']}   ROBOT

    # Validate the live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Controllers_CRUD
    Should Be Equal   ${update['action']}    N
    Should Be Equal   ${controller['fcoId']}    ${update['payload']['fcoId']}
    
    # Look up the controller by id and confirm it returns the same data
    ${response}   Fids Controllers Get By Id    ${controller['fcoId']}
    ${controller_get}   Fids Get Response Result   ${response}

    Should Not Be Empty   ${controller_get}
    Should Be Equal    ${controller['fcoCustomerId']}   ${controller_get['fcoCustomerId']}
    Should Be Equal    ${controller['fcoName']}   ${controller_get['fcoName']}

    # Update the controller
    ${response}   Fids Controllers Save   name=ROBOT_UPDATED  identification=${controller['fcoCustomerId']}  fcoId=${controller['fcoId']}
    ${controller}   Fids Get Response Result   ${response}
    Should Be Equal    ${controller['fcoName']}   ROBOT_UPDATED
    Should Be Equal    ${controller['fcoCustomerId']}   ROBOT_CONTROLLER

    # Validate the live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Controllers_CRUD
    Should Be Equal   ${update['action']}    U
    Should Be Equal   ${controller['fcoId']}    ${update['payload']['fcoId']}

    # Delete the controller
    ${response}   Fids Controllers Delete   ${controller}
    ${controller_delete}   Fids Get Response Result   ${response}
    Should Be Empty   ${controller_delete}

    # Validate the live update was sent
    ${response}   Fids Get Ui Updates
    ${update}    Fids Get Updates Response Result   response_payload=${response}   store_id=Controllers_CRUD
    Should Be Equal   ${update['action']}    D
    Should Be Equal   ${controller['fcoId']}    ${update['payload']['fcoId']}

    # close ui update processing
    Fids Close Ui Updates   store_id=Controllers_CRUD


FIDS_CONTROLLER_COMMAND_CHANEL
    # This test covers creating a controller, opening a command channel, sending a command and validating the command was received.

    # Create controller
    ${response}   Fids Controllers Save   name=ROBOT_CMD1   identification=ROBOT_CMD1
    ${controller}   Fids Get Response Result   ${response}

    # open a command channel for it
    ${command_ws}   Fids Open Command Channel   ROBOT_CMD1
    ${connected}    Fids Command Channel Wait Connected   ${command_ws}   timeout=30
    Should Be True   ${connected}

    # Create Command
    ${response}   Fids Send Controller Command   "CONFIG_UPDATE"   ${controller}
    ${task}   Fids Get Response Result   ${response}

    # Check task was created
    Should Be Equal    ${task['fstCommand']}   CONFIG_UPDATE
    Should Be True    ${task['fstId']}

    # Get the command when it is sent
    ${command}   Fids Comamnd Channel Wait Command   ${command_ws}    timeout=120
    Should Not Be Empty   ${command}

    # Delete controller
    Fids Controllers Delete   ${controller}

    # Close web socket
    Fids Close Command Channel   ${command_ws}


# xMIDS tests are to check the rules are loaded and valid
XMIDS_COUTNER_ALLOCTIONS

    ${allocations}   Fids Cmid Alloctions Get   C04
    Should Not Be Empty    ${allocations}

XMIDS_BELT_ALLOCTIONS
    ${allocations}   Fids Bmid Alloctions Get   BGB01
    Should Not Be Empty    ${allocations}

XMIDS_GATE_ALLOCTIONS
    ${allocations}   Fids Gmid Alloctions Get   D1
    Should Not Be Empty    ${allocations}

XMIDS_ARRIVAL_FLIGHTS
    ${arrivals}   Fids Xmids Arrivals Get
    Should Not Be Empty    ${arrivals}

XMIDS_DEPARTURE_FLIGHTS
    ${departures}   Fids Xmids Departures Get
    Should Not Be Empty    ${departures}


FIDS_DOWNLOAD_TEMPLATE
    Precondition Component Version Check   component=fid    version_min="3.2"
    ${file}   Fids Download Template
    Should Be Equal    ${file.headers['Content-Disposition']}   attachment; filename=TPL-IMP-AMS-MASTER_DATA-FIDS.xlsx

FIDS_EXPORT
    Precondition Component Version Check   component=fid    version_min="3.2"
    ${file}   Fids Export   FidControllers,FidMonitors
    Should Be Equal    ${file.headers['Content-Disposition']}   inline; filename=fids-export.zip

FIDS_IMPORT_TEMPLATE
    Precondition Component Version Check   component=fid    version_min="3.2"
    ${response}   Fids Import Template   data\\level_3\\FIDS   TPL-IMP-AMS-MASTER_DATA-FIDS.xlsx
    Should Not Be Empty    ${response.content}

    ${response}   Fids Import Poll   ${response.content}

FIDS_IMPORT_EXPORT
    Precondition Component Version Check   component=fid    version_min="3.2"
    ${response}   Fids Import From Another System  data\\level_3\\FIDS   export.zip
    Should Not Be Empty    ${response.content}

    ${response}   Fids Import Poll   ${response.content}