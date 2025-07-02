#!/bin/bash
#
# Jenkins executor script for Robot Framework tests
#

# Exit immediately if a command exits with a non-zero status
# set -e

echo "======= Environment Setup ======="

# Remove any existing virtual environment
rm -rf ../.venv

# Uncomment if system packages need to be updated
# apt update
# apt install python3.10 -y

# Check Python version
python3 --version

echo "======= Dependencies Installation ======="
echo "Installing requirements from requirements.txt..."
ls -al
ls "$WORKSPACE"
ls -al requirements.txt

# Install dependencies
pip install -r requirements.txt --no-cache-dir

# Verify installed packages
echo "======= Installed Packages ======="
pip list

# Verify Robot Framework and Pabot installation
robot --version
pip3 show robotframework-pabot

echo "======= Running Tests ======="

command_line_args="-x xunit.xml -L ${logLevel} -P ${libPath} \
-v DEPLOYED_APPLICATIONS:${deployedApplications} \
-v ENVIRONMENT:${environment} \
-v CUSTOMER_ID:${customerId} \
-v AIRPORT:${airport} \
-v USER:${robotUser} \
-v PASSWD:${robotPwd} \
-v ORG:${org} \
-v MODE:${mode} \
"

echo "robot args: ${command_line_args}"

for i in $(seq 1 ${maxLevel});
do
	robot ${command_line_args} -d ./reports/level_$i tests/level_$i
	status=$?
	if [ $status -ne 0 ] && [ $i -lt $maxLevel ]; then
		echo "Will not move on to next Level as tests at Level ${i} have failed."
		break
	fi
done
