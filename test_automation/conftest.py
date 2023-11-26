import os
from sys import platform
import sys
import time
import pytest
from test_automation.utilities.ConfigParser import get_browser_type, get_config_web_browser_download_path, \
    get_base_log_folder
from test_automation.configuration import common_configuration as conf

if sys.platform == 'win32':
    HOME = 'USERPROFILE'
else:
    HOME = 'HOME'
pytest.driver = None


@pytest.yield_fixture(scope='function')
def web_driver(request):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

    # get browser name
    selected = get_browser_type()
    print("Selected Browser: ", selected)

    # get the path of WebDriverServer
    dir_path = os.path.dirname(__file__)
    driver_path = str(dir_path + os.sep + "library" + os.sep + "selenium")
    curr_platform = None
    if platform in ("linux", "linux2"):
        curr_platform = "Linux"
    elif platform in ("win32"):
        curr_platform = "Windows"
    else:
        curr_platform = "Mac"
    chrome_driver_path = str(driver_path + os.sep + curr_platform + os.sep + "chromedriver")

    # Define browser's service log directory
    log_dir = get_base_log_folder()

    # Browser service log path
    log_path = os.path.join(
        log_dir,
        str(selected) + '.log '
    )

    # Invoke browser
    if selected is None:
        print("None of the browser is selected so setting default browser as firefox")
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.dir", conf.DOWNLOAD_PATH)
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.helperApps.neverAsk.openFile", False)
        fp.set_preference("browser.helperApps.neverAsk.openFile",
                          "application/pdf,text/plain,application/octet-stream,application/x-pdf,application/vnd.pdf,application/vnd.openxmlformats-officedocument.spreadsheethtml,text/csv,text/html,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "application/pdf,text/plain,application/octet-stream,application/x-pdf,application/vnd.pdf,application/vnd.openxmlformats-officedocument.spreadsheethtml,text/csv,text/html,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel")
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        opts = Options()
        opts.profile = fp
        firefox_driver_path = str(driver_path + os.sep + curr_platform + os.sep + "geckodriver")
        web_driver = webdriver.Firefox(executable_path=firefox_driver_path, service_log_path=log_path, options=opts)
    else:
        # setting run time web driver environment
        if "chrome" in selected.lower():
            options = webdriver.ChromeOptions()
            options.add_argument('ignore-certificate-errors')
            # options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-dev-shm-usage')
            prefs = {'download.default_directory': get_config_web_browser_download_path()}
            options.add_experimental_option('prefs', prefs)
            web_driver = webdriver.Chrome(executable_path=chrome_driver_path, service_log_path=log_path,options=options)
        elif "firefox" in selected.lower():
            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.dir", get_config_web_browser_download_path())
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.helperApps.neverAsk.openFile", False)
            fp.set_preference("browser.helperApps.neverAsk.openFile",
                              "application/pdf,text/plain,application/octet-stream,application/x-pdf,application/vnd.pdf,application/vnd.openxmlformats-officedocument.spreadsheethtml,text/csv,text/html,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel")
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                              "application/pdf,text/plain,application/octet-stream,application/x-pdf,application/vnd.pdf,application/vnd.openxmlformats-officedocument.spreadsheethtml,text/csv,text/html,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel")
            fp.set_preference("browser.helperApps.alwaysAsk.force", False)
            opts = Options()
            opts.profile = fp
            firefox_driver_path = str(driver_path + os.sep + curr_platform + os.sep + "geckodriver")
            web_driver = webdriver.Firefox(executable_path=firefox_driver_path, service_log_path=log_path, options=opts)
        elif "ie" in selected.lower():
            ie_options = webdriver.IeOptions()
            ie_options.set_capability("nativeEvents", False)
            ie_options.set_capability("unexpectedAlertBehaviour", "accept")
            ie_options.set_capability("ignoreProtectedModeSettings", True)
            ie_options.set_capability("disable-popup-blocking", True)
            ie_options.set_capability("enablePersistentHover", True)
            ie_options.set_capability("ignoreZoomSetting", True)
            ie_driver_path = driver_path + os.sep + curr_platform + os.sep + "IEDriverServer"
            web_driver = webdriver.Ie(executable_path=ie_driver_path, service_log_path=log_path, options=ie_options)
        else:
            print("Please enter valid browser like: chrome/IE/firefox")
            return False
    web_driver.maximize_window()

    # Return driver object-Declare the driver object as class variable so we can access using self keyword or class name [ie. self.driver, ClassName.driver]
    request.cls.driver = web_driver
    pytest.driver = web_driver
    yield web_driver # Return the driver object so we can access using method name [ie. web_driver]
    time.sleep(5)
    # web_driver.close()
    web_driver.quit()
