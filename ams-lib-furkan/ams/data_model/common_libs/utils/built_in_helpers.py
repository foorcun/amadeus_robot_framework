"""
Helper methods that use Robot Framework's BuiltIn library.
"""

from robot.libraries.BuiltIn import BuiltIn


def skip(msg):
    """
    Skips the current test with the provided message using Robot Framework's BuiltIn library.

    Args:
        msg (str): The message to display when skipping the test.

    Usage:
        skip("This test is skipped.")
    """
    BuiltIn().skip(msg=msg)


def get_var_value(name):
    """
    Retrieves the value of a Robot Framework variable using BuiltIn().get_variable_value.

    Args:
        name (str): The name of the variable to retrieve (e.g., "${MY_VAR}").

    Returns:
        Any: The value of the variable.

    Usage:
        value = get_var_value("$MY_VAR")
    """
    return BuiltIn().get_variable_value(name)


def fail(msg):
    """
    Fails the current test with the provided message using Robot Framework's BuiltIn library.

    Args:
        msg (str): The message to display when failing the test.

    Usage:
        fail("This test failed due to an error.")
    """
    BuiltIn().fail(msg=msg)
