"""

python -m pytest -v .\test_automation\test_scripts\ -k test_home_page_tc_1_submit_the_login_page_details.py

"""

import pytest
import argparse
import os
import sys

# Append "Test_Automation" path in "sys.path" list variable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from test_automation.configuration import common_configuration as conf
from test_automation.utilities.ConfigParser import set_browser_type, set_report_html_file, set_config_web_browser_url, set_login_username, set_login_password

__docformat__ = 'restructuredtext en'
__author__ = 'test automation'


def main():

    test_path = ''
    print("Args are : ", str(sys.argv))
    print("Parsing the script arguments from the command line")
    print("If any argument names aren't correct, an exception will be thrown")

    try:
        # Pass the command line arguments in python (not in pytest)
        parser = argparse.ArgumentParser()
        parser.add_argument("--files", type=str,help="Name of Test Files to test is optional arguments")
        parser.add_argument("--functions", type=str,help="Name of Test Function  to test is optional arguments")
        parser.add_argument("--test_folder", type=str,default="test_suites",help="Name of Test Folder from which test can run is optional arguments")
        parser.add_argument('--report', default="report",help="Change the output XML and HTML report file names. Default='report'")
        parser.add_argument('--browser',default='chrome',help='Use to specify test automation browser environment like: chrome/ie/firefox')
        parser.add_argument('--web_url', default=conf.APP_URL,help=f"Use to specify test automation camera URL like: https://rahul.shetty.com, "f"Default={conf.APP_URL}")
        parser.add_argument('--username', default=conf.USER_NAME,help=f'Use to specify test automation camera username like:admin Default={conf.USER_NAME}')
        parser.add_argument('--password', default=conf.PASSWORD,help=f'Use to specify test automation camera password like:Test@12345 'f'Default={conf.PASSWORD}')

        # Get command line arguments in python (not in pytest)
        arg = parser.parse_args()
        FILES = arg.files
        FUNCTIONS = arg.functions
        TEST_FOLDER = arg.test_folder
        BROWSER= arg.browser
        WEB_URL = arg.web_url
        USERNAME = arg.username
        PASSWORD = arg.password

        # Set the command line input into the custom method
        set_config_web_browser_url(WEB_URL)
        set_login_username(USERNAME)
        set_login_password(PASSWORD)
        set_report_html_file(arg.report)
        set_browser_type(BROWSER)

        # Use the test_folder argument to figure out where to look for the test files.
        root_directory = os.path.dirname(os.path.abspath(__file__))
        test_script_directory = os.path.join(root_directory, TEST_FOLDER)
        assert os.path.isdir(test_script_directory), "Could not find test folder {!r} in the test_automation directory.Full path checked: {}".format(TEST_FOLDER, test_script_directory)

        # Collect the pytest arguments in a list form which will be passed in "pytest.main(pytest_arguments)" method
        pytest_arguments = ['--tb=short', '-v', test_script_directory]
        pytest_arguments.insert(0, '--html={}'.format(arg.report))
        pytest_arguments.insert(0, '--junitxml={}'.format(arg.report))
        pytest_arguments.insert(0, '--disable-warnings')
        pytest_arguments.insert(0, '--capture=tee-sys')
        pytest_arguments.insert(0, '--self-contained-html')

    except Exception as error:
        print(error)
        sys.exit(1)

    is_files_given = False
    is_functions_given = False

    if FILES != None:
        is_files_given = True
    if FUNCTIONS != None:
        is_functions_given = True

    if (is_files_given is True) and (is_functions_given is False):
        FILES = ''.join(map(str, FILES))
        FILES = FILES.replace(',', ' |')
        test_path = '-k ' + FILES

    elif(is_files_given is False) and (is_functions_given is True):
        FUNCTIONS = ''.join(map(str, FUNCTIONS))
        FUNCTIONS = FUNCTIONS.replace(',', ' |')
        test_path = '-k ' + FUNCTIONS

    else:
        print("Please enter valid command line arguments")

    pytest_arguments.append(test_path)

    # Call pytest from python code
    pytest.main(pytest_arguments) # python -m pytest -v .\test_automation\test_scripts\ -k test_home_page_tc_1_submit_the_login_page_details.py

if __name__ == '__main__':
    main()
