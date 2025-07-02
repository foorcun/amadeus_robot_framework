"""This module provides a class `PayloadGenerator` to generate payloads for
requests using Jinja2 templates."""

import os
import logging
from jinja2 import Environment
from ams.data_model.common_libs.utils.airport_data_generator import (
    GenerateAirportData as GaD,
)

LOGGER = logging.getLogger(__name__)


class PayloadGenerator:
    """
    A class to generate payloads for requests using Jinja2 templates.
    Attributes:
        input_data (dict): The input data to be used in the template.
        filename (str): The name of the template file.
        current_file (str): The current file path.
    Methods:
        read_template(_filename, _current_file):
            Reads the template file and returns its content as a string.
        construct_generic_payload():
            Constructs a payload by rendering the template with the input data.
    """

    def __init__(self, input_data, filename, current_file):
        self.input_data = input_data
        self.filename = filename
        self.current_file = current_file
        self.function_dict = {
            "generate_flight_number": GaD.generate_flight_number,
            "generate_airline_code": GaD.get_iata_airline_code,
        }

    @staticmethod
    def read_template(_filename, _current_file):
        """
        Reads the content of a template file.

        Args:
            _filename (str): The name of the template file to read.
            _current_file (str): The path of the current file to determine the
                directory of the template file.

        Returns:
            str: The content of the template file as a string.

        Raises:
            FileNotFoundError: If the template file does not exist at the specified path.
        """
        paths = [
            os.path.join(os.path.dirname(_current_file), "template_files", _filename),
            os.path.join(os.path.dirname(_current_file), _filename),
        ]

        path = next((p for p in paths if os.path.isfile(p)), None)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The following path does not exist: {path}")
        with open(path, "r", encoding="utf-8") as template_file:
            return template_file.read().strip()

    def construct_generic_payload(self):
        """
        Constructs a generic payload by rendering a Jinja2 template with the provided input data.
        This method reads a template file, processes it using Jinja2 with the given input data,
        and returns the generated payload as a string. The payload is formatted to replace
        single quotes with double quotes.
        Returns:
            str: The generated payload string.
        """
        jinja_env = Environment(trim_blocks=True, lstrip_blocks=True)
        jinja_env.globals.update(self.function_dict)
        template_file_data = self.read_template(self.filename, self.current_file)
        template = jinja_env.from_string(template_file_data)
        LOGGER.debug(
            "Attempting to construct payload from template using input data : %s",
            self.input_data,
        )
        request_str = "".join(
            map(str.strip, template.render(data=self.input_data).splitlines())
        )
        LOGGER.debug("Generated payload is :%s", request_str)
        request_str = request_str.replace("'", '"')

        return request_str
