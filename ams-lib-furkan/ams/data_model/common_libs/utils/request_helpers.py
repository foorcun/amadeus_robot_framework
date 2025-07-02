"""Module handle any pre-processing before request payloads are generated"""

import logging

LOGGER = logging.getLogger(__name__)


def identify_day_of_ops(days: str):
    """
    Args:
        days: string of days of operation

    Returns:
        list of days of operation
    """
    day_map = {
        "1": "MON",
        "2": "TUE",
        "3": "WED",
        "4": "THU",
        "5": "FRI",
        "6": "SAT",
        "7": "SUN",
    }
    return [day_map[day] for day in days]


def generate_date_time_data(time_data: str):
    """
    Args:
        time_data: string of date and time in ISO format

    Returns:
        tuple: (list of date components, list of time components)
    """
    date_part, time_part = time_data.split("T")
    date_components = date_part.split("-")
    time_components = [int(part) for part in time_part.split(":")] + [0]
    return date_components, time_components


def _pre_process_payload_date_data(payload_input_data: dict):
    """
    Pre-processes the payload date data by updating specific keys with new period data.
    This method processes the payload input data by identifying days of
    operation and generating date and time data for specific period keys.
    It updates the payload input data with the processed information.
    The following keys are processed:
    - "depPeriodDaysOfOp"
    - "arrPeriodDaysOfOp"
    - "startOfDeparturePeriod"
    - "endOfDeparturePeriod"
    - "startOfArrivalPeriod"
    - "endOfArrivalPeriod"
    For "startOfDeparturePeriod" and "endOfDeparturePeriod",
    additional keys "departureTime" and "arrivalTime"
    are added to the payload input data respectively.
    Logs debug information about the processing steps and the types of the updated data.
    Returns:
        None
    """
    days_in_ops_keys = ("depPeriodDaysOfOp", "arrPeriodDaysOfOp")
    start_end_period_keys = (
        "startOfDeparturePeriod",
        "endOfDeparturePeriod",
        "startOfArrivalPeriod",
        "endOfArrivalPeriod",
    )
    LOGGER.debug("Pre-Processing Date Data for payload")

    for day_key in days_in_ops_keys:
        if day_key in payload_input_data.keys():
            days_in_ops = identify_day_of_ops(payload_input_data[day_key])
            payload_input_data[day_key] = days_in_ops

            LOGGER.debug(
                "Adding key %s to payload input data with new period data : %s and type is : %s",
                day_key,
                payload_input_data[day_key],
                type(payload_input_data[day_key]),
            )

    for period_key in start_end_period_keys:
        if period_key in payload_input_data.keys():
            date_data, time_data = generate_date_time_data(
                payload_input_data[period_key]
            )

            payload_input_data[period_key] = date_data
            LOGGER.debug(
                "Adding key %s to payload input data with new period data : %s and type is : %s",
                period_key,
                payload_input_data[period_key],
                type(payload_input_data[day_key]),
            )
            if period_key == "startOfDeparturePeriod":
                payload_input_data["departureTime"] = time_data
            elif period_key == "endOfDeparturePeriod":
                payload_input_data["arrivalTime"] = time_data
