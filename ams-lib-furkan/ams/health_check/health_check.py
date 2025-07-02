"""health check of AMS components"""

from ams.health_check.injector import get_health_status
from ams.data_model.common_libs.utils.built_in_helpers import fail


def health_check(component_name):
    """
    Calls get_health_status from the injector module, checks if the result is "OK",
    and fails the test if it is not.

    == Arguments ==
    | component_name (str)
    | The name of the component to check the health status. Defaults to "aaa".

    == Return value ==
    | str/bool: Status "OK" or True given by the readiness endpoint, or the test fails otherwise.

    == Usage ==
    |  Health Check   component_name=aaa
    """
    # Get the health status
    health_status = get_health_status(component_name)

    # Fail if health_status is not "OK" or not True
    if health_status != "OK" and health_status is not True:
        fail(
            f"Health check failed for component '{component_name}'. Status: {health_status}"
        )

    return health_status
