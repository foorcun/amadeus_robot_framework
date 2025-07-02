"""This module is to be used for defining functions that are required for generating the context
test data for AMS"""

__author__ = "Sayantan Roy"
__maintainer__ = "Sayantan Roy"

import random
import string
import uuid


class GenerateAirportData:
    """A utility class for generating various types of airport-related data.
    Methods
    -------
    generate_airline_code(prefix, length):
        Generates an airline code with the given prefix and length of digits.
    generate_flight_number(length):
        Generates a flight number with the specified length of digits.
    generate_correlation_id(size=50, chars=string.ascii_uppercase +
    string.digits + string.ascii_lowercase):
        Generates a correlation ID for AMS with the specified size and character set.
    generate_uuid():
        Generates a UUID v4 string.
    identify_day_of_ops(days: str):
        Identifies the days of operation from a string of days."""

    @staticmethod
    def generate_airline_code(prefix, length):
        """
        Generate an airline code with a given prefix and a specified number of digits.

        Args:
            prefix (str): The prefix for the airline code.
            length (int): The number of digits to generate for the airline code.

        Returns:
            str: The generated airline code consisting of the prefix followed by
            the specified number of digits.
        """
        digits = "".join(random.choices("0123456789", k=length))
        return f"{prefix}{digits}"

    @staticmethod
    def get_iata_airline_code():
        """
        Get a random airline code.

        Returns:
            str: A random airline iata code.
        """
        arl_prefix = "ARL_"
        airline_iata_codes = [
            "6E",
            "6X",
            "AI",
            "LX",
            "UK",
            "AA",
            "MA",
            "ME",
            "EK",
            "SQ",
        ]
        return f"{arl_prefix}{random.choice(airline_iata_codes)}"

    @staticmethod
    def generate_flight_number(length):
        """
        Generate a random flight number consisting of digits.
        If generated flight number is less than 3 digits, it will be padded with 0s.

        Args:
            length (int): The length of the flight number to generate.

        Returns:
            str: A string representing the generated flight number.
        """
        if length == 0:
            return ""

        first_digit = random.choice("123456789")
        remaining_digits = "".join(random.choices("0123456789", k=length - 1))
        digits = first_digit + remaining_digits
        if len(digits) < 3:
            digits = "0" * (3 - len(digits)) + digits

        return digits

    @staticmethod
    def generate_correlation_id(
        size=50, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
    ):
        """
        Generates a correlation ID for AMS.

        Args:
            size (int, optional): The length of the correlation ID to generate. Defaults to 50.
            chars (str, optional): The characters to use for generating the correlation ID.
                                   Defaults to uppercase letters, digits, and lowercase letters.

        Returns:
            str: A randomly generated correlation ID.
        """
        return "".join(random.choice(chars) for _ in range(size))

    @staticmethod
    def generate_uuid():
        """
        Generate UUID v4
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_random_string():
        """
        Generates a random string of 50 characters consisting of lowercase letters and digits.

        This function creates a string by randomly selecting characters from the set of
        lowercase ASCII letters and digits. The resulting string is 50 characters long.

        Returns:
            str: A random string of 50 characters.
        """
        characters = string.ascii_lowercase + string.digits
        random_string = "".join(random.choice(characters) for _ in range(50))
        return random_string
