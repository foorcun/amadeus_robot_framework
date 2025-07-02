*** Settings ***
Documentation       Combine injectors using keywords

Library             ams
Library             ams/commons.py
Library             jmespath
Library             ams.data_model.common_libs.utils.date_handler


*** Variables ***
${context}      Evaluate    get_context()


*** Keywords ***
Create and Verify Flight in Visit Planner
    [Documentation]    This keyword helps in creating a flight in the visit planner and verifying if the flight has been successfully created.
    ...    It utilizes the `create_manual_source_leg_period` keyword to create a flight and then verify its existence in the visit planner
    ...    using `get_leg_periods` keyword.
    ...    === Usage: ===
    ...    Create and Verify Flight in Visit Planner

    create_manual_source_leg_period    ${context["test_context"]["leg_period_context"]}
    ${leg_periods}    get_leg_periods    ${flightNumber}

Search for flight in Flight Operations
    [Documentation]    This keyword helps verify if the flight created in the visit planner is present in flight operations.
    ...
    ...    === Usage: ===
    ...    Search for flight in Flight Operations

    ${flights}    Fom Searches
    ...    ${flightNumber}
    ...    ${context["test_context"]["leg_period_context"]["startOfArrivalPeriod"]}
    ...    ${context["test_context"]["leg_period_context"]["endOfArrivalPeriod"]}

    ${visit}    fom_find_visit_in_flights    ${flights}    ${airline}    ${flightNumber}

Search for flight in Fixed Resource Management System
    [Documentation]    This keyword verifies whether a flight created in the visit planner is present in the Fixed Resource Management System (FRMS).
    ...    === Usage: ===
    ...    Search for flight in Fixed Resource Management System

    ${flights}    Fom Searches
    ...    ${flightNumber}
    ...    ${context["test_context"]["leg_period_context"]["startOfArrivalPeriod"]}
    ...    ${context["test_context"]["leg_period_context"]["endOfArrivalPeriod"]}

    ${visit}    fom_find_visit_in_flights    ${flights}    ${airline}    ${flightNumber}

    ${frms_plans}    get_frms_plans

    ${stand_gate_plan}    find_operational_plan    ${frms_plans}    STAND

    Sleep    10s

    ${frms_plan}    get_frms_plan_by_id    ${stand_gate_plan["id"]}

    find_visit_in_plan    ${frms_plan}    ${visit["inboundMovement"]["id"]}

Update Resource Type
    [Documentation]    Updates the resource type for a flight movement.
    ...    Args:
    ...    ${resource_type} (str): Type of resource (e.g., "STAND", "GATE").
    ...    ${movement_id} (str): Flight movement ID.
    ...    Returns:
    ...    ${response} (dict): Response from the update operation.
    [Arguments]    ${resource_type}    ${movement_id}

    IF    ${resource_type} == "STAND"
        ${all_stand_details}    Get Stand Details
        ${get_random_id}    Get Random Resource Id    response_json=${all_stand_details.json()}
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=STAND
        ...    departure_or_arrival=Arrival
        ...    resourceId=${get_random_id}
    ELSE IF    ${resource_type} == "AIRCRAFT_TERMINAL"
        ${all_terminal_details}    Get Terminal Details    endpoint_type=terminalList
        ${get_random_id}    Get Random Resource Id    response_json=${all_terminal_details.json()}
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=AIRCRAFT_TERMINAL
        ...    departure_or_arrival=Arrival
        ...    resourceId=${get_random_id}
    ELSE IF    ${resource_type} == "PUBLIC_TERMINAL"
        ${all_terminal_details}    Get Terminal Details    endpoint_type=terminalList
        ${get_random_id}    Get Random Resource Id    response_json=${all_terminal_details.json()}
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=PUBLIC_TERMINAL
        ...    departure_or_arrival=Arrival
        ...    resourceId=${get_random_id}
    ELSE IF    ${resource_type} == "GATE"
        ${response_gate}    Get Gate Details    endpoint_type=gateList
        ${get_random_id}    Get Random Resource Id    response_json=${response_gate.json()}
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=PASSENGER_GATE
        ...    departure_or_arrival=Arrival
        ...    resourceId=${get_random_id}
    ELSE IF    ${resource_type} == "BAGGAGE_BELT"
        ${response_bb}    Get Baggage Belt Details    endpoint_type=baggageBeltList
        ${get_random_id}    Get Random Resource Id    response_json=${response_bb.json()}
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=BAGGAGE_BELT
        ...    departure_or_arrival=Arrival
        ...    resourceId=${get_random_id}
    ELSE IF    ${resource_type} == "FOLLOW_ME_REQUESTED"
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=FOLLOW_ME_REQUEST
        ...    departure_or_arrival=Arrival
        ...    resourceId=true
    ELSE IF    ${resource_type} == "MARSHALLER_REQUESTED"
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=MARSHALLER
        ...    departure_or_arrival=Arrival
        ...    resourceId=true
    ELSE IF    ${resource_type} == "BUS_NEED"
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=PASSENGER_BUS
        ...    departure_or_arrival=Arrival
        ...    resourceId=true
    ELSE IF    ${resource_type} == "SID"
        ${response}    Update Flight Resources
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=STANDARD_INSTRUMENT_DEPARTURE
        ...    departure_or_arrival=Arrival
        ...    resourceId=test
    ELSE IF    ${resource_type} == "STAR"
        ${response}    Update Flight Resources
        ...    endpoint_type=movements-put
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_resources
        ...    resource_type=STANDARD_TERMINAL_ARR_ROUTE
        ...    departure_or_arrival=Arrival
        ...    resourceId=test
    END
    RETURN    ${response}

ADD DIVERSION
    [Documentation]    Adds a diversion event for a flight movement.
    ...    Returns:
    ...    ${response} (dict): Response from the diversion update operation.
    [Arguments]    ${EVENT_TYPE}    ${movement_id}    ${time}    ${divert_time}
    IF    str(${EVENT_TYPE}) == 'divert' or ${EVENT_TYPE} == 'go_around'
        Update Flight Time
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_time
        ...    leg_type=inbound
        ...    timing_type=ALDT
        ...    time=${time}
        ${response}    Update Flight Diverion
        ...    movement_id=${movement_id}
        ...    op_type=disruption
        ...    event_type=${EVENT_TYPE}
        ...    divert_time=${divert_time}
    ELSE IF    ${EVENT_TYPE} == "air_return"
        Update Flight Time
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_time
        ...    leg_type=outbound
        ...    timing_type=ATOT
        ...    time=${time}
        ${response}    Update Flight Diverion
        ...    movement_id=${movement_id}
        ...    op_type=disruption
        ...    event_type=${EVENT_TYPE}
        ...    divert_time=${divert_time}
    ELSE IF    ${EVENT_TYPE} == "ground_return"
        Update Flight Time
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_time
        ...    leg_type=outbound
        ...    timing_type=EOBT
        ...    time=${time}
        Update Flight Time
        ...    movement_id=${movement_id}
        ...    op_type=update_flight_time
        ...    leg_type=outbound
        ...    timing_type=AOBT
        ...    time=${time}
        ${response}    Update Flight Diverion
        ...    movement_id=${movement_id}
        ...    op_type=disruption
        ...    event_type=${EVENT_TYPE}
        ...    divert_time=${divert_time}
    ELSE
        ${response}    Update Flight Diverion
        ...    movement_id=${movement_id}
        ...    op_type=disruption
        ...    event_type=${EVENT_TYPE}
        ...    divert_time=${divert_time}
    END
    RETURN    ${response}

Get Time
    [Documentation]    Adds the specified number of hours to the current time and returns the result in ISO 8601 format.
    ...    | Arguments | Description |
    ...    | `hours` (int) | Number of hours to add to the current time |
    ...
    ...    | Returns | Description |
    ...    | `time` (str) | The calculated date and time in the format `YYYY-MM-DDTHH:MM:SSZ` |
    ...    === Usage: ===
    ...    | Get Time | hours=5 |
    [Arguments]    ${hours}

    ${time}    Get Date    hours=${hours}    date_format=%Y-%m-%dT%H:%M:%SZ
    RETURN    ${time}
