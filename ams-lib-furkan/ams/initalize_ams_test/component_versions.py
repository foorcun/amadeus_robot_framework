"""Component Versions class and parsing"""

# pylint: disable=line-too-long
# pylint: disable = protected-access

import logging
import re

LOGGER = logging.getLogger(__name__)


class ComponentVersion:
    """Represents the version of an apt component by major, minor, patch and build"""

    def __init__(self, major, minor=None, patch=None, build=None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.build = build

    def __str__(self):
        s = ""
        if self.major:
            s = s + str(self.major)
        if self.minor:
            s = s + "." + str(self.minor)
        if self.patch:
            s = s + "." + str(self.patch)
        if self.build:
            s = s + "." + str(self.build)
        return s

    def __repr__(self):
        s = "("
        if self.major:
            s = s + str(self.major)
        if self.minor:
            s = s + "," + str(self.minor)
        if self.patch:
            s = s + "," + str(self.patch)
        if self.build:
            s = s + "," + str(self.build)
        return s + ")"

    def __eq__(self, other):
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.build == other.build
        )

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.major, self.minor, self.patch, self.build))

    def __lt__(self, other):
        if self.major < other.major:
            return True
        if self.major > other.major:
            return False
        # major is equal
        if self.minor < other.minor:
            return True
        if self.minor > other.minor:
            return False
        # minor is equal
        if self.patch < other.patch:
            return True
        if self.patch > other.patch:
            return False
        # patch is equal
        if self.build < other.build:
            return True
        if self.build > other.build:
            return False
        # self and other are equal
        return False

    def __gt__(self, other):
        return not self < other

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other


def parse_version(version):
    """
    Parses the given version into a ComponentVersion Class otherwise raises ValueError
    Valid version strings
        9.10.1.5
        9.10.1-5
        9.10.1-a
        9.10.1a
        202412120021
    """
    major = None
    minor = None
    patch = None
    build = None

    if version is None:
        raise ValueError(f"Invalid version {version}")

    # break into pieces on .
    periods = version.split(".")
    if len(periods) == 2:
        major = periods[0]
        minor = periods[1]  # 9.2
    elif len(periods) == 3:
        major = periods[0]
        minor = periods[1]
        if periods[2].isdigit():
            patch = periods[2]  # 9.3.1
        else:
            # check for - in the third position, anything after the - goes into build field
            matcher = re.search(r"(.)+-(.)+", periods[2])
            if matcher:
                patch = matcher.group(1)
                build = matcher.group(2)  # 9.4.2-1 or 9.4.2-a
            else:
                patch = periods[2]  # 9.4.2a
    elif len(periods) == 4:
        major = periods[0]
        minor = periods[1]
        patch = periods[2]
        build = periods[3]  # 9.10.1.5
    else:
        # esb versioning
        matcher = re.search(r"[\d]{12}", version)
        if matcher:
            major = version[0:4]
            minor = version[4:6]
            patch = version[6:8]
            build = version[8:12]  # 202504041825
        else:
            # not in a known format, assume the version can be compared with just one part
            major = version  # 10

    return ComponentVersion(
        __private_convert_to_number(major),
        __private_convert_to_number(minor),
        __private_convert_to_number(patch),
        __private_convert_to_number(build),
    )


def __private_convert_to_number(s):
    """
    Attempts to convert the string to a number, if failed returns the string
    """
    if s is None or s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return s


def get_component_versions_from_json(versions_json):
    """
    Create dictionary of component, version from the /version call json
    """
    # Find the image for each deployment and parses the version from it
    # path: deployments.<deployment_name>.containers.image
    versions = {}
    for deployment_name in versions_json.get("deployments"):
        # deployments are in the formt: aptams-<component>-<environment>
        matcher = re.search(r"aptams-(\w+)-\w+", deployment_name)
        if matcher:
            component = matcher.group(1)
            deployment = versions_json.get("deployments").get(deployment_name)
            if (
                deployment.get("containers")
                and deployment.get("containers").get(deployment_name)
                and deployment.get("containers").get(deployment_name).get("image")
            ):
                image = deployment.get("containers").get(deployment_name).get("image")
                # images are in the format: <docker_url>/aptams/<component>:<version>
                matcher = re.search(r":(.*)", image)
                if matcher:
                    version = matcher.group(1)
                    versions[component] = version
                    LOGGER.info("Found version: %s %s", component, version)
                else:
                    LOGGER.info(
                        "Component version not found from image: %s %s",
                        component,
                        version,
                    )
    return versions


def get_esb_repo_versions_from_json(versions_esb):
    """
    Create dictionary of repo, version from the /version call json
    """
    # Find the interface array in the payload
    # path: deployments.<esb_deployment_name>.pods.<pod_name>.interfaces
    interfaces = []
    for deployment_name in versions_esb.get("deployments"):
        if "esb" in deployment_name:
            deployment = versions_esb.get("deployments").get(deployment_name)
            if deployment.get("pods"):
                for pod_name in deployment.get("pods"):
                    pod = deployment.get("pods").get(pod_name)
                    if pod.get("interfaces"):
                        interfaces = pod.get("interfaces")
                        break

    # parse the repo version from the string
    # example formats "altea-core-repo-1.1.16.zip" "finavia-repo-1.1.12.5.zip"
    versions = {}
    for repo in interfaces:
        matcher = re.search(r"([\w\\\-]+)-([\d+\\\.]*)\.zip", repo)
        if matcher:
            repo_name = matcher.group(1)
            version = matcher.group(2)
            versions[repo_name] = version
            LOGGER.info("Found repo: %s %s", repo_name, version)
        else:
            LOGGER.info("Repo stringdid not match: %s %s", repo_name, version)

    return versions
