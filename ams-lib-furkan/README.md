[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![made-with-python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

`ams-lib` provides keywords for all AMS functionalities.

## Installation

Install the library from Amadeus Artifactory using the following command:

`pip install -i https://repository.rnd.amadeus.net/api/pypi/utopy-pypi-production-utopy/simple ams-lib`

## Keywords documentation

ams offers a wide set of keywords which can be found in the [Keywords documentation](https://static.forge.amadeus.net/utopy/ams-lib/ams-lib.html)

## Robot arguments

- `ENVIRONMENT`: target environment (e.g. `QCP2`) - list of supported values is defined in `environment.yaml`)
- `CUSTOMER_ID`: customer id (e.g. `AITA-TEST`)
- `AIRPORT`: IATA code of the airport (e.g. `XYZ`)
- `MODE`: login method:
  - `cyber_ark`: CyberArk
  - `mock`: dynamic mock user (`manage@<CUSTOMER_ID>[<AIRPORT>]`)
  - default behaviour:
    - if present, use Robot arguments `USER`, `PASSWD`, `ORG` containing credentials details (resp. user name, password, organization)
    - if one these arguments is not present, read content of `.ams_login` in the user's home directory

## Quick start

```robotframework
*** Settings ***
Library             protocols
Library             ams
Variables           data.py

Test Setup          Open Session    ${security_context_user_details_log}
Test Teardown       Close Session


*** Test Cases ***
My Test Case
    [Documentation]    Fetch Airport Terminal Details
    Open Generic Ams Session
    ...    protocol=REST
    ...    environment=QCP2
    ...    current_directory=${CURDIR}
    ...    test_name=${TEST_NAME}

    ${all_terminal_details}    Fetch Terminal Details    expected_response_code=200    endpoint_type=terminalList
    ${add_param}    Create Dictionary    code=T3
    Fetch Terminal Details
    ...    expected_response_code=200
    ...    endpoint_type=terminalByCode
    ...    additional_params=${add_param}

```

### How to contribute and create a new Python package

Python package is generated automatically via Utopy workflow.

Package is published in [Utopy Artifactory](https://repository.rnd.amadeus.net/ui/repos/tree/General/utopy-pypi-production-utopy-nce) as for all Utopy libraries.

Library documentation is generated and published in [static-forge](https://static.forge.amadeus.net/utopy) via Utopy workflow.

To generate a new release of the library follow these steps:

1. Fork the repository and clone it on your local machine
2. Create a new branch from master
3. Perform your changes
4. Run black module (code formatter) on ams-lib
5. Run pylint module (static code analysis) on ams-lib
6. Run robotidy (robotframework-tidy) on .robot test files
7. Create a PR from your branch to release branch with your Jira Id in the commit message **only release branch will trigger the worklow to generate the package and the documentation**
8. PR will be reviewed and merged by the owner of the repository
9. After PR merge, a new Python package will be available in [Utopy Artifactory](https://repository.rnd.amadeus.net/ui/repos/tree/General/utopy-pypi-production-utopy-nce)
10. Master branch will be rebased automatically to reflect the latest changes

Note: pytest, black and  pylint will be automatically executed as part of PR build.

Should the black formatter modify any file, if the pylint score falls below 9.0, or if any unit test fails, the build process will be deemed unsuccessful.

Complete documentation is available [here](https://rndwww.nce.amadeus.net/confluence/display/UTOPY/Contributing+to+Utopy+Libraries).