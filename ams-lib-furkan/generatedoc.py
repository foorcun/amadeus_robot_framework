"""
Generate library documentation to aggregate both Python and Robot Framework keywords
"""

import json
import os
import pathlib
from robot.libdoc import libdoc
from bs4 import BeautifulSoup

LIBRARY_NAME = "ams-lib"
LIBRARY_ROOT_DIR = os.getcwd() + os.sep
LIBRARY_PACKAGE_PATH = LIBRARY_ROOT_DIR + "ams"
LIBRARY_RESOURCES_PATH = LIBRARY_PACKAGE_PATH + os.sep + "keywords.resource"
DOC_FOLDER = LIBRARY_ROOT_DIR + "doc" + os.sep
PYTHON_KEYWORD_DOC_PATH = DOC_FOLDER + "python-keywords.html"
RESOURCES_KEYWORDS_DOC_PATH = DOC_FOLDER + "robot-keywords.html"
LIBRARY_DOC_PATH = DOC_FOLDER + LIBRARY_NAME + ".html"
MACRO_FUNCTIONALITIES = []

# extract version from VERSION file
with open(LIBRARY_ROOT_DIR + "VERSION", encoding="utf-8") as version_file:
    version = version_file.read().strip()

# generate Python keywords documentation
libdoc(
    LIBRARY_PACKAGE_PATH,
    PYTHON_KEYWORD_DOC_PATH,
    name=LIBRARY_NAME,
    format="HTML",
    docformat="ROBOT",
    version=version,
)

# generate Robot Framework resources keywords documentation
if MACRO_FUNCTIONALITIES:
    # if macro functionalities are defined (= more .keywords.resource file)
    for functionality in MACRO_FUNCTIONALITIES:
        LIBRARY_RESOURCES_PATH = (
            LIBRARY_PACKAGE_PATH + os.sep + functionality + os.sep + "keywords.resource"
        )
        RESOURCES_KEYWORDS_DOC_PATH = (
            LIBRARY_ROOT_DIR
            + "doc"
            + os.sep
            + "robot-keywords-"
            + functionality
            + ".html"
        )

        libdoc(
            LIBRARY_RESOURCES_PATH,
            RESOURCES_KEYWORDS_DOC_PATH,
            name=LIBRARY_NAME,
            format="HTML",
            docformat="ROBOT",
            version=version,
        )
else:
    # standard case
    libdoc(
        LIBRARY_RESOURCES_PATH,
        RESOURCES_KEYWORDS_DOC_PATH,
        name=LIBRARY_NAME,
        format="HTML",
        docformat="ROBOT",
        version=version,
    )


def extract_robot_framework_keywords(resources_keywords_doc_path):
    """
    Look for keywords in Robot Framework resources files
    """
    # check if Robot Framework resources file exists
    if pathlib.Path(resources_keywords_doc_path).is_file():
        with open(resources_keywords_doc_path, encoding="utf-8") as robot_keywords_file:
            soup = BeautifulSoup(robot_keywords_file, "html.parser")
            for tag in soup.head.find_all("script"):
                if "libdoc" in tag.contents[0]:
                    string_libdoc = tag.string.strip().replace("libdoc = ", "")
                    json_libdoc = json.loads(string_libdoc)
                    # retrieve list of keywords
                    return json_libdoc["keywords"]
    return []


def add_link_to_robot_framework_keywords(json_libdoc):
    """
    Add link to Robot Framework keywords and return updated documentation
    """

    soup = BeautifulSoup(json_libdoc["doc"], "html.parser")

    for tag in soup.find_all("table"):
        for td_tag in tag.find_all("td"):
            # explore all data cell under td tag
            try:
                if "class" in td_tag.contents[0].attrs.keys():
                    if "href" in td_tag.contents[0].attrs.keys():
                        # print("Keyword link aleady present")
                        continue

                    # print("No keyword link, adding link")
                    keyword_name = td_tag.string
                    keyword_name_no_spaces = keyword_name.replace(" ", "%20")
                    # Add link attribute
                    td_tag.contents[0]["href"] = f"#{keyword_name_no_spaces}"
                    # Rename tag from span to a
                    td_tag.contents[0].name = "a"
            except BaseException:  # pylint: disable=bare-except
                # print("No class")
                continue

    # Recreate doc string with updated links
    child_list = []
    for child in soup.children:
        child_list.append(str(child))
    new_doc = "".join(child_list)
    return new_doc


def extract_python_keywords(python_keyword_doc_path, library_doc_path, robot_keywords):
    """
    Look for keywords in Python files
    """
    with open(python_keyword_doc_path, encoding="utf-8") as python_keywords_file:
        soup = BeautifulSoup(python_keywords_file, "html.parser")
        for tag in soup.head.find_all("script"):
            if "libdoc" in tag.contents[0]:
                string_libdoc = tag.string.strip().replace("libdoc = ", "")
                json_libdoc = json.loads(string_libdoc)
                # retrieve list of keywords
                python_keywords = json_libdoc["keywords"]

                # merge Robot Framework and Python keywords
                json_libdoc["keywords"] = robot_keywords + python_keywords
                # sort json
                json_libdoc["keywords"].sort(key=lambda x: x["name"])

                # recreate link for Robot Framework keywords
                new_doc = add_link_to_robot_framework_keywords(json_libdoc)
                json_libdoc["doc"] = new_doc
                new_string_libdoc = json.dumps(json_libdoc)
                # recreate libdoc string
                tag.string = "libdoc = " + new_string_libdoc

                # Generate new documentation file
                with open(library_doc_path, "w", encoding="utf-8") as library_file:
                    library_file.write(str(soup))


# Extract Robot Framework resources keyword
robot_keywords_list = []
if MACRO_FUNCTIONALITIES:
    # if macro functionalities are defined (= more .keywords.robot file)
    for functionality in MACRO_FUNCTIONALITIES:
        RESOURCES_KEYWORDS_DOC_PATH = (
            LIBRARY_ROOT_DIR
            + "doc"
            + os.sep
            + "robot-keywords-"
            + functionality
            + ".html"
        )
        robot_keywords_list.extend(
            extract_robot_framework_keywords(RESOURCES_KEYWORDS_DOC_PATH)
        )
else:
    # standard case
    robot_keywords_list.extend(
        extract_robot_framework_keywords(RESOURCES_KEYWORDS_DOC_PATH)
    )

# extract Python keywords
extract_python_keywords(PYTHON_KEYWORD_DOC_PATH, LIBRARY_DOC_PATH, robot_keywords_list)


# Remove temporary files
if MACRO_FUNCTIONALITIES:
    # if macro functionalities are defined (= more .keywords.robot file)
    for functionality in MACRO_FUNCTIONALITIES:
        RESOURCES_KEYWORDS_DOC_PATH = (
            LIBRARY_ROOT_DIR
            + "doc"
            + os.sep
            + "robot-keywords-"
            + functionality
            + ".html"
        )
        os.remove(RESOURCES_KEYWORDS_DOC_PATH)
else:
    # check if Robot Framework resources file exists
    if pathlib.Path(RESOURCES_KEYWORDS_DOC_PATH).is_file():
        os.remove(RESOURCES_KEYWORDS_DOC_PATH)

os.remove(PYTHON_KEYWORD_DOC_PATH)
