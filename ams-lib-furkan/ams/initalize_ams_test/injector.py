"""Injector module to handle creating an AMS Session"""

# pylint: disable=line-too-long, unused-argument
# pylint: disable = protected-access

import os
import logging
from protocols import session_manager
from ams.data_model.initialize_ams_test.create_ams_session import AMSSession
from ams.data_model.common_libs.utils.generic_helpers import initialize_test_context
from ams.initalize_ams_test.component_versions import (
    get_component_versions_from_json,
    get_esb_repo_versions_from_json,
)
from .input_builder import _get_active_configuration, _get_toggles_configuration
import requests
from ams.data_model.common_libs.utils.generic_helpers import initialize_context

LOGGER = logging.getLogger(__name__)


def open_generic_ams_session(protocol, current_directory, test_name=None, **kwargs):
    """
    Opens a generic AMS session.

    It has the capability to handle REST, Active MQ, FTP and other clients

    The name of the test for which the AMS session is being created.
    Use the robot variable ${TEST_NAME}
    Test Name and current directory is used to pick the test data file under
    data/${test_name}.py variable
    In the test data file add variables based on you test like so:
    Check file: tests/system_tests/AMS-XXX_SOME_FEATURE_NAME/data/
        001_AODB_PLANG_LEGPRD_CRUD_CREATE_FETCH_LEGPRD.py

    == Arguments ==
    | protocol
    | The protocol to be used for the AMS session.

    | current_directory
    | The current working directory where the test data is located.
    | Use the robot variable ${CURDIR}

    | test_name
    | The name of the test for which the AMS session is being created.
    | Use the robot variable ${TEST_NAME}

    Other parameters are passed as key=value through ``**kwargs`` (keyword arguments). Below the possible values:

    | ``context_file``           | data file name having the contextual data |
    | ``load_active_conf``       | Optional. If True, the function will call `_get_active_configuration` to load the active configuration. Defaults to False if not provided. |
    | ``load_toggles_conf``      | Optional. If True, the function will call `_get_toggles_configuration` to load the active 1A configuration for toggles. Defaults to False if not provided. |

    == Return value ==
    | None

    == Usage ==
    | Open Generic AMS Session   protocol=${protocol}
       current_directory=${current_directory}   test_name=${test_name}

    == Example ==
    | Open Generic Ams Session    protocol=REST
    current_directory=${CURDIR}    test_name=${TEST_NAME}   load_active_conf=True   load_toggles_conf=True
    | Open Generic Ams Session    protocol=REST
    current_directory=${CURDIR}    context_file=AODB_XXX_OPS_DATA
    """
    context_data_file = None
    if (
        "context_file" in kwargs
        and kwargs["context_file"]
        and kwargs["context_file"].strip() not in ["", "''", '""']
    ):
        context_data_file = f"{kwargs['context_file']}.py"
    elif test_name and test_name.strip():
        context_data_file = f"{test_name}.py"

    test_context = None
    if context_data_file:
        context_file_path = os.path.join(current_directory, "data", context_data_file)
        context = initialize_test_context(context_file_path)
        test_context = context.test_context
    else:
        test_context = initialize_context()

    session = AMSSession(
        protocol=protocol,
        test_context=test_context,
    )
    session.create_ams_session()

    # Parse load_active_conf to boolean
    load_active_conf = kwargs.get("load_active_conf", False)
    if isinstance(load_active_conf, str):
        load_active_conf = load_active_conf.lower() in ["true", "1", "yes"]

    # Check if load_active_conf is True
    if load_active_conf:
        LOGGER.info("Loading active configuration.")
        _get_active_configuration()
    else:
        LOGGER.info("Skipping loading active configuration.")

    # Parse load_active_conf to boolean
    load_toggles_conf = kwargs.get("load_toggles_conf", False)
    if isinstance(load_toggles_conf, str):
        load_toggles_conf = load_toggles_conf.lower() in ["true", "1", "yes"]

    # Check if load_toggles_conf is True
    if load_toggles_conf:
        LOGGER.info("Loading Release Toggles configuration.")
        _get_toggles_configuration()
    else:
        LOGGER.info("Skipping loading active configuration.")

    get_component_versions()


def get_component_versions(session_key="defaultKey", **kwargs):
    """
    Get the deployed versions of the components from the versions tool and place into the conext

    In context_data component_versions will contain the compoent's three letter code and its version
    ESB repos will also be set by the repo name.
    """
    LOGGER.info("Getting component versions")

    # Retrieve context_data
    context_data = session_manager.sessions._get_session_context_data()

    # Check if component_versions is already present
    if "component_versions" in context_data and context_data["component_versions"]:
        LOGGER.info(
            "Skipping getting compontent versions as it is already present in context_data."
        )
        return

    # user
    endpoint = "/versions/"
    server_url = (
        session_manager.sessions._get_session_context_data()
        .get("global_environment_context")
        .get("internal_server_url")
    )

    versions = {}
    try:
        compeont_versions = requests.get(
            server_url + endpoint,
            timeout=120,
            verify=False,
        )
        # Get the full response payload
        payload = compeont_versions.json()
        LOGGER.debug("returned versions %s", payload)
        # Parse the payload
        versions = get_component_versions_from_json(payload)
    except ValueError:
        # until /versions is deployed everywhere it will fail with 404
        LOGGER.info("ignore failure of the /versions call")

    # Get ESB repos
    endpoint = "/versions/deployments?apps=esb&pods=1"

    esb_versions = {}
    try:
        esb_repo_versions = requests.get(
            server_url + endpoint,
            timeout=60000,
            verify=False,
        )
        payload = esb_repo_versions.json()
        LOGGER.debug("returned esb versions %s", payload)
        # Parse the payload
        esb_versions = get_esb_repo_versions_from_json(payload)
    except ValueError:
        # until /versions is deployed everywhere it will fail with 404
        LOGGER.info("ignore failure of the /versions call")

    # lookup the overrides from
    overrides = (
        session_manager.sessions._get_session_context_data()
        .get("global_environment_context")
        .get("component_versions", {})
    )

    # Put versions in the context
    context_data["component_versions"] = {**versions, **esb_versions, **overrides}
