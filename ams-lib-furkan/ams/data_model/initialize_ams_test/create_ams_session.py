# pylint: disable=line-too-long

"""Module to handle the background work for creating an ams session"""

import os
import logging
import yaml
from protocols import open_session, session_manager
from ams.data_model.common_libs.utils.generic_helpers import get_variable_value


LOGGER = logging.getLogger(__name__)


class AMSSession:
    """Class to handle all functionalities to create an ams session"""

    def __init__(self, protocol, test_context):
        """
        Initialize a new AMS session.

        Args:
            protocol (str): The protocol to be used (e.g., 'http', 'https').
            test_context (dict): The context for the test being executed.
            user_context (dict, optional): Additional user-specific context.
            Defaults to None.

        Attributes:
            security_context (None): Placeholder for security context,
            initialized to None.
            protocol (str): The protocol to be used.
            environment (str): The environment in which the session is created.
            context_data (dict): Dictionary containing the test context.
            user_context (dict or None): Additional user-specific context.
            environment_context (dict): Dictionary for environment-specific
            context,
            initialized to an empty dictionary.
        """
        self.security_context = None
        self.protocol = protocol
        self.environment = get_variable_value("ENVIRONMENT")
        self.context_data = {"test_context": test_context}
        self.environment_context = {}

    @staticmethod
    def load_yaml_file(file_path):
        """
        Load and parse a YAML file.

        Args:
            file_path (str): The path to the YAML file to be loaded.

        Returns:
            dict: The parsed data from the YAML file.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data

    @staticmethod
    def load_and_replace_yaml(file_path, environment, replacements):
        """
        Load a YAML file, replace placeholders with provided values, and
        construct the referer URL.
        Args:
            file_path (str): The path to the YAML file.
            environment (str): The environment key to look for in the YAML data.
            replacements (dict): A dictionary of placeholder replacements where the
             key is the placeholder
                                 and the value is the replacement string.
        Returns:
            dict: The modified environment data from the YAML file.
        Raises:
            ValueError: If the specified environment is not found in the YAML file.
        """

        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        def replace_placeholders(obj, replacements_):
            if isinstance(obj, dict):
                return {
                    k: replace_placeholders(v, replacements_) for k, v in obj.items()
                }
            if isinstance(obj, list):
                return [replace_placeholders(i, replacements_) for i in obj]
            if isinstance(obj, str):
                for key, value in replacements_.items():
                    obj = obj.replace(f"{{{key}}}", value)
                return obj
            return obj

        def construct_referer(obj):
            obj["generic_headers"]["referer"] = (
                f"{obj.get('server_url')}"
                f"{obj.get('generic_headers', {}).get('referer')}"
            )

        if environment in data:
            data[environment] = replace_placeholders(data[environment], replacements)
            construct_referer(data[environment])
        else:
            raise ValueError(f"Environment '{environment}' not found in the YAML file.")

        return data[environment]

    def load_configs(self):
        """
        Loads configuration files for endpoints and JMESPath queries into the context data.

        This method constructs the file paths for the 'end_points.yml' and 'jmespath_queries.yml'
        configuration files relative to the current file's directory. It then loads the contents
        of these YAML files and stores them in the 'context_data' dictionary under the keys
        'end_points' and 'jmespath_queries', respectively.

        Raises:
            FileNotFoundError: If any of the configuration files are not found.
            yaml.YAMLError: If there is an error while parsing the YAML files.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        end_points = os.path.join(base_path, "../data_store/end_points.yml")
        jmespath_queries = os.path.join(base_path, "../data_store/jmespath_queries.yml")
        self.context_data["end_points"] = self.load_yaml_file(end_points)
        self.context_data["jmespath_queries"] = self.load_yaml_file(jmespath_queries)

    def create_environment_context(self):
        """
        Creates the environment context for the AMS session.

        This method constructs the file path to the environment YAML file,
        loads and replaces the YAML content with the current environment and
        generic context data, and then assigns the resulting context to the
        `environment_context` attribute. It also updates the `global_environment_context`
        in the `context_data` dictionary.

        The method performs the following steps:
        1. Determines the base path of the current file.
        2. Constructs the path to the environment YAML file.
        3. Loads and replaces the YAML content with the current environment and
        generic context data.
        4. Prints the generic context data for debugging purposes.
        5. Updates the `global_environment_context` in the `context_data` dictionary.

        Returns:
            None
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        yaml_file_path = os.path.join(base_path, "../data_store/environment.yml")
        self.environment_context = self.load_and_replace_yaml(
            yaml_file_path,
            self.environment,
            self.context_data.get("test_context", {}).get("generic_context"),
        )
        self.context_data["global_environment_context"] = self.environment_context

    def generate_security_context(self):
        """
        Generates the security context for the AMS session.

        This method constructs a dictionary containing the server URL, authentication token details,
        and headers required for the AMS session. The authentication token includes the token type,
        username, password, organization, and the authentication endpoint path.

        The security context is stored in the `self.security_context` attribute.

        Returns:
            None
        """
        self.security_context = {
            "server_url": self.environment_context.get("server_url"),
            "auth_token": {
                "token_type": self.context_data.get("test_context", {}).get(
                    "token_type", "COOKIE"
                ),
                "username_key": "apt_username",
                "username": self.context_data.get("test_context", {})
                .get("user_context", {})
                .get("username"),
                "password_key": "apt_password",
                "password": self.context_data.get("test_context", {})
                .get("user_context", {})
                .get("password"),
                "organization_key": "apt_companyId",
                "organization": (
                    self.context_data.get("test_context", {})
                    .get("user_context", {})
                    .get("organization")
                    if self.context_data.get("test_context", {})
                    .get("user_context", {})
                    .get("organization")
                    else "1A"
                ),
                "path": self.environment_context.get("authentication_end_point"),
            },
            "header": self.environment_context.get("auth_headers"),
        }

    def pick_sign_details(self):
        """
        Reads login details from environment variables if available else picks from a local file and updates the user context.

        This method looks for a file named ".ams_login" in the user's home directory.
        If the file exists, it reads the file line by line to extract the username,
        password, and organization details. These details are then stored in the
        `self.user_context` dictionary.

        The expected format of the ".ams_login" file is:
        user <username>
        password <password>
        organization <organization>

        Raises:
            FileNotFoundError: If the ".ams_login" file does not exist.
        """
        username = get_variable_value("USER")
        password = get_variable_value("PASSWD")
        organization = get_variable_value("ORG", "1A")
        self.context_data["test_context"]["user_context"] = {}
        if username and password and organization:
            self.context_data["test_context"]["user_context"]["username"] = username
            self.context_data["test_context"]["user_context"]["password"] = password
            self.context_data["test_context"]["user_context"][
                "organization"
            ] = organization
            LOGGER.debug(
                "Picked user context from robot environment variables or OS environment"
            )
        else:
            login_file = os.path.join(os.path.expanduser("~"), ".ams_login")
            if os.path.exists(login_file):
                with open(login_file, "r", encoding="utf-8") as fl:
                    for line in fl.readlines():
                        if line.startswith("user "):
                            self.context_data["test_context"]["user_context"][
                                "username"
                            ] = line[len("user ") :].strip()
                        elif line.startswith("password "):
                            self.context_data["test_context"]["user_context"][
                                "password"
                            ] = line[len("password ") :].strip()
                        elif line.startswith("organization "):
                            self.context_data["test_context"]["user_context"][
                                "organization"
                            ] = line[len("organization ") :].strip()
            LOGGER.debug("Picked user context from .ams_login file")

    def fetch_user_context_from_cyber_ark(self):
        """TODO document why this method is empty"""
        print("Inside fetch_user_context_from_cyber_ark")

    def set_mock_user(self):
        customer_id = self.context_data["test_context"]["generic_context"][
            "customer_id"
        ]
        airport = self.context_data["test_context"]["generic_context"]["ref_airport"]

        self.context_data["test_context"]["user_context"] = {}
        self.context_data["test_context"]["user_context"][
            "username"
        ] = f"manage@{customer_id}[{airport}]"
        LOGGER.info(
            "Login with mock user: %s",
            self.context_data["test_context"]["user_context"]["username"],
        )

    def construct_user_context(self):
        """
        Constructs the user context based on the mode specified in the user context.

        This method checks the "mode" key in the user context dictionary and performs
        actions accordingly:
        - If the mode is "cyber_ark", it fetches the user context from CyberArk.
        - If the mode is "local", it picks sign details from local storage and
        prints the user context.

        Returns:
            None
        """
        mode = get_variable_value("MODE")
        if mode == "cyber_ark":
            self.fetch_user_context_from_cyber_ark()
        if mode == "mock":
            self.set_mock_user()
        else:
            self.pick_sign_details()
        LOGGER.debug(
            "User context : %s",
            self.context_data.get("test_context", {}).get("user_context"),
        )

    def update_headers_after_cookie(self, orginal_cookie):
        """
        Updates the headers in the security context details with the generic
        headers from the environment context.

        This method retrieves the current security context details from the
        session manager and updates its headers
        with the generic headers specified in the environment context.

        Returns:
            None
        """
        # pylint: disable=protected-access
        rest_headers = session_manager.sessions._get_security_context_details()

        for key, value in self.environment_context.get("generic_headers").items():
            rest_headers["header"][key] = value

        if rest_headers["header"]["Cookie"] is None:
            rest_headers["header"]["Cookie"] = orginal_cookie
        else:
            rest_headers["header"]["Cookie"] = (
                rest_headers["header"]["Cookie"] + ";" + orginal_cookie
            )
        print(rest_headers["header"]["Cookie"])

    def create_ams_session(self):
        """
        Creates an AMS session by initializing the necessary contexts and configurations
        based on the specified protocol.
        This method performs the following steps:
        1. Creates the environment context.
        2. Constructs the user context.
        3. Generates the security context.
        4. Loads the necessary configurations.
        Depending on the protocol specified, it will handle the session creation as follows:
        - "REST": Opens a session with the security context, protocol, and context data,
          then updates headers after setting the cookie.
        - "ACTIVE MQ": Placeholder for future implementation.
        - "SOAP": Placeholder for future implementation.
        - "FTP": Placeholder for future implementation.
        """
        self.create_environment_context()
        self.construct_user_context()
        self.generate_security_context()
        self.load_configs()

        match self.protocol:
            case "REST":
                orginal_cookies = self.environment_context.get("auth_headers").get(
                    "Cookie"
                )
                open_session(
                    self.security_context,
                    protocol=self.protocol,
                    context_data=self.context_data,
                )
                self.update_headers_after_cookie(orginal_cookies)
            case "ACTIVE MQ":
                print("ACTIVE MQ")
            case "SOAP":
                print("SOAP")
            case "FTP":
                print("FTP")
