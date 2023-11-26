import importlib
import os
import pathlib
import sys
from datetime import datetime
from os.path import join, isfile
from shutil import copyfile
from test_automation.configuration.common_configuration import TEST_LOGS_BASE
from test_automation.utilities import log
from test_automation.utilities.log import logger


if sys.platform == 'win32':
    home = 'USERPROFILE'
else:
    home = 'HOME'

CONFIG = None

try:
    CONFIG = importlib.import_module('common_configuration')
except ImportError:
    print("locate config.py file in {}".format(os.getcwd()))
    import test_automation.configuration.common_configuration as CONFIG

def set_browser_type(browser):
    print(f"Set Browser to: {browser}")
    CONFIG.BROWSER = browser

def set_report_html_file(report):
    CONFIG.REPORT_FILE_NAME = report
    print(CONFIG.REPORT_FILE_NAME)


def set_config_web_browser_url(url):
    CONFIG.APP_URL = url
    print(f"Web App URL :: {CONFIG.APP_URL}")

def set_login_username(login_uname):
    CONFIG.USER_NAME = login_uname

def set_login_password(login_pwd):
    CONFIG.PASSWORD = login_pwd


def get_browser_type():
    return CONFIG.BROWSER

def get_base_log_folder():
    return os.path.join(
        os.environ[home],
        TEST_LOGS_BASE,
        log.LOG_FOLDER_NAME
    )

def get_config_web_browser_download_path():
    return CONFIG.DOWNLOAD_PATH

def get_config_web_browser_url():
    logger.info(f"::Get Browser URL::{CONFIG.APP_URL}")
    return CONFIG.APP_URL

def set_current_test_file_case_name(node_path):
    print(node_path)
    CONFIG.current_test_name = ''
    CONFIG.current_test_name = str(node_path.node._nodeid)
    # index = CONFIG.current_test_name.split('/')[1]
    index = CONFIG.current_test_name
    CONFIG.current_test_name = node_path.node.name
    CONFIG.test_file_name = index.split('.py')[0]
    print(CONFIG.test_file_name)
    print(CONFIG.current_test_name)

def log_test_data():
    log_folder = get_current_test_log_directory()
    pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

    log_files = [f for f in os.listdir(get_base_log_folder()) if isfile(join(get_base_log_folder(), f))]
    for log_file in log_files:
        try:
            source = get_base_log_folder() + "/" + log_file
            destination = log_folder + "/" + log_file
            copyfile(source, destination)

            if log_file.startswith("project_"):
                destination = os.path.join(get_base_log_folder(), log_file)
                with open(destination, "a") as fo:
                    fo.write("===================================\r\n")
                    with open(source, 'r') as fi:
                        fo.write(fi.read())

            open(source, 'w').close()
        except Exception as e:
            print("Error while copying log file. {}".format(e))
    return True

def get_current_test_log_directory():
    test_file, test_case = get_current_test_file_case_name()
    return os.path.join(get_base_log_folder(),test_file,test_case)

def get_current_test_file_case_name():
    if not hasattr(CONFIG, 'current_test_name') and not hasattr(CONFIG, 'test_file_name'):
        return ""
    print(CONFIG.current_test_name)
    return CONFIG.test_file_name, CONFIG.current_test_name

def take_screenshot(driver, file_name):
    try:
        HOME = 'USERPROFILE' if sys.platform == 'win32' else 'HOME'
        if not os.path.exists(os.environ[HOME] + '/test_logs/ScreenShots'):
            os.makedirs(os.environ[HOME] + '/test_logs/ScreenShots')
        scrn_name = os.environ[HOME] + '/test_logs/ScreenShots/{0}_{1}.png'.format(
            file_name, str(datetime.now().strftime("%m%d%Y_%H%M%S")))
        set_test_screenshot_name(scrn_name)
        driver.save_screenshot(scrn_name)
    except Exception as ex:
        logger.error(ex)
        raise ex

def set_test_screenshot_name(screenshot_name):
    CONFIG.SCREENSHOT_NAME = screenshot_name
