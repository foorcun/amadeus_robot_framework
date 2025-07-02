"""
Module contains function to verify the general processsing status of delete leg period API call.
"""

from ams.data_model.common_libs.request_response_handler.response_validator import (
    validate_general_processing,
)


def validate_delete_leg_period_general_processing(response, status="OK"):
    """
    Validates the general processing status of delete leg period API call.

    | *Arguments*                | *Description*                                                                      |

    | ``response``               | response object from call to 'Delete Leg Period' keyword                            |
    | ``status``                 | expected general processing status                                                 |


    === Usage: ===
    | Validate Delete Leg Period General Processing    response=${response}

    """
    validate_general_processing(response, status)
