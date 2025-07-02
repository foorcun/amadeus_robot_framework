*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=CFG
Suite Teardown      Automatic Data Cleanup


*** Test Cases ***
001_V1_CFG_UPDATE_PARAMETER
    Precondition Applications Deployed    applications=CFG
    # Find the parameter to update
    ${param_to_update}    Cfg V2 Get Parameter In Configuration
    ...    component=COMMON
    ...    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD
    # Record the original value and increment it
    ${original_value}    Set Variable    ${param_to_update['value']}
    ${incremented_value}    Evaluate    ${original_value} + 1
    # Update the parameter with the new value
    ${updated_param}    Cfg V1 Update Parameter
    ...    component=COMMON
    ...    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD
    ...    value=${incremented_value}
    # Publish the configuration to apply the changes
    Cfg V2 Publish Configuration
    ...    configuration=${updated_param['configurationName']}
    ...    revision=${updated_param['revision']}
    # Retrieve the updated parameter to verify the change
    ${updated_param_check}    Cfg V2 Get Parameter In Configuration
    ...    component=COMMON
    ...    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD
    # Verify the parameter has been updated to the new value
    Should Be Equal    ${updated_param_check['value']}    ${incremented_value}
    # Change the value back to the original for cleanup
    ${rolled_back_param}    Cfg V1 Update Parameter
    ...    component=COMMON
    ...    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD
    ...    value=${original_value}
    # Publish the configuration again to apply the cleanup change
    Cfg V2 Publish Configuration
    ...    configuration=${rolled_back_param['configurationName']}
    ...    revision=${rolled_back_param['revision']}
    # Verify the parameter is back to the original value
    ${rolled_back_param_check}    Cfg V2 Get Parameter In Configuration
    ...    component=COMMON
    ...    param=RELEASE_TOGGLES_DAYS_OVERDUE_THRESHOLD
    Should Be Equal    ${rolled_back_param_check['value']}    ${original_value}
