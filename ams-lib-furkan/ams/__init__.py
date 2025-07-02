# pylint: disable=line-too-long
"""
ams-lib provides keywords for all AMS (Airport Management Systems) functionalities.

=== Table of contents ===
%TOC%

= Owners =
TRU-AOP-ENG-ADM-ADQ-BLR-APR

= Installation =
Install the library from Amadeus Artifactory using the following command:

``pip install -i https://repository.rnd.amadeus.net/api/pypi/utopy-pypi-production-utopy-nce ams-lib``

= Usage =
To use the library just import it as follow:
|   *** Settings ***
|   Library    ams

= Data Model =
Data model representing the product and functionality. It's stored in the `data_model` folder.

Refer to the files in this folder for the full documentation. Below an overview:

| ``myclass``        | Python class representing XXXX`` |
| ``myfunction``     | Python module containing useful functions to XXXX`` |
"""

import os
import pkgutil
from importlib import import_module as _import_module
from inspect import isfunction as _isfunction
from inspect import getmembers as _getmembers

# get PROTOCOL environment variable
protocol = os.environ.get("PROTOCOL", "EDIFACT")

# Discover and import automatically keywords
PACKAGE_NAME = __name__

# import package and discover list of functionality modules
mod = __import__(PACKAGE_NAME)
func_modules_list = [
    modname
    for importer, modname, ispkg in pkgutil.iter_modules(mod.__path__)
    if modname not in ["main", "commons", "data_model", "grammar", "version"]
]

# list of modules containing keywords at functionality level
modules_with_keywords = ["injector", "responses"]
# list of modules containing keywords at library level
extra_modules = []


# def _discover_keywords(current_functionality, directory=""):
#     """
#     Discover keywords in Python modules - functionality level
#     """
#     for module in modules_with_keywords:
#         keywords_list = []
#         try:
#             imported_module = _import_module(
#                 "%(package_name)s.%(functionality)s%(directory)s.%(module)s"
#                 % {
#                     "package_name": PACKAGE_NAME,
#                     "functionality": current_functionality,
#                     "directory": directory,
#                     "module": module,
#                 }
#             )
#         except ImportError:
#             # optional response module
#             if module == "responses" and not os.path.isfile(
#                 os.path.sep.join(
#                     [PACKAGE_NAME, directory, current_functionality, module, ".py"]
#                 )
#             ):
#                 continue
#             raise
#         # get list of keywords from the imported module
#         for function in _getmembers(imported_module, _isfunction):
#             if _isfunction(function[1]):
#                 keywords_list.append(function[0])

#         # create variables for every keyword discovered
#         for keyword in keywords_list:
#             globals()[keyword] = getattr(imported_module, keyword)


# pylint: disable=redefined-outer-name
def _discover_keywords(current_functionality, module, subfolder=""):
    """
    Discover keywords in Python modules
    """
    module_path = (
        f"{PACKAGE_NAME}.{current_functionality}.{subfolder}.{module}"
        if subfolder
        else f"{PACKAGE_NAME}.{current_functionality}.{module}"
    )
    try:
        imported_module = _import_module(module_path)
    except ImportError as e:
        print(f"Failed to import module {module_path}: {e}")
        raise

    # get list of keywords from the imported module
    keywords_list = [
        function
        for function in dir(imported_module)
        if callable(getattr(imported_module, function))
    ]
    # create variables for every keyword discovered
    for keyword in keywords_list:
        globals()[keyword] = getattr(imported_module, keyword)


def _discover_extra_keywords():
    """
    Discover extra keywords in Python modules - library level
    """
    for module in extra_modules:
        keywords_list = []
        imported_module = _import_module(
            "%(package_name)s.%(module)s"
            % {
                "package_name": PACKAGE_NAME,
                "module": module,
            }
        )
        # get list of keywords from the imported module
        for function in _getmembers(imported_module, _isfunction):
            if _isfunction(function[1]):
                keywords_list.append(function[0])

        # create variables for every keyword discovered
        for keyword in keywords_list:
            globals()[keyword] = getattr(imported_module, keyword)


for functionality in func_modules_list:
    # discover keywords for every functionality modules
    for root, directories, files in os.walk(mod.__path__[0] + os.sep + functionality):
        directories = [
            directory for directory in directories if "__pycache__" not in directory
        ]
        py_files = [file for file in files if file.endswith(".py")]
        for file in py_files:
            module = file.split(".")[0]
            subfolder = root.split(functionality)[1].strip(os.sep)
            if os.sep in subfolder:
                # in case subfolder has additional folders
                subfolder = subfolder.replace(os.sep, ".")
            _discover_keywords(functionality, module, subfolder)
# discover extra keywords
_discover_extra_keywords()
