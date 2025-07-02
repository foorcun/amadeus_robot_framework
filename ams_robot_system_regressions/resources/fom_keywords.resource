*** Settings ***
Documentation       Resource File to define generic keywords for AMS system

Library             ams
Library             ams/commons.py


*** Keywords ***
Fom Find Visit
    [Arguments]    ${airlineCode}    ${flightNumber}    ${period_start}    ${period_end}

    ${flights}    Fom Searches    flight_number=${flightNumber}    start_date=${period_start}    end_date=${period_end}
    Should Not Be Empty    ${flights}
    ${visit}    Fom Find Visit In Flights    flights=${flights}    airline_code=${airlineCode}    flight_number=${flightNumber}
    Should Not Be Empty    ${visit}
    RETURN    ${visit}
