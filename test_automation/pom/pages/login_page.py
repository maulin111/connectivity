import time
from selenium.webdriver.support.select import Select
from test_automation.pom.web_base_page import BasePage
from test_automation.utilities.ConfigParser import get_config_web_browser_url
from test_automation.utilities.log import logger


class LoginPage(BasePage):
    txt_username = None
    txt_password = None
    btn_signin = None
    txt_dashboard = None
    dashboard_hamburger_menu = None

    txt_email = None
    checkbox_check_out = None
    dropdown_gender = None
    radio_employment_status = None
    calendar_date_of_birth = None
    message_success = None

    def __init__(self, webdriver, locators, conf, message):
        webdriver.get(get_config_web_browser_url())
        self.message = message
        BasePage.__init__(self, webdriver, locators, conf, message)

        self.logo_whirlpool_path = 'self.locators.LOGIN_PAGE_WHIRLPOOL_LOGO_BY_XPATH'
        self.txt_username_path = 'self.locators.LOGIN_PAGE_USERNAME_INPUT_FIELD_BY_XPATH'
        self.txt_password_path = 'self.locators.LOGIN_PAGE_PASSWORD_INPUT_FIELD_BY_XPATH'
        self.btn_signin_path = 'self.locators.LOGIN_PAGE_SIGNIN_INPUT_FIELD_BY_XPATH'
        self.txt_dashboard_path = 'self.locators.DASHBOARD_PAGE_BY_XPATH'
        self.dropdown_env_path = 'self.locators.DASHBOARD_ENV_DROPDOWN_BY_XPATH'
        self.select_env_path = 'self.locators.DASHBOARD_SELECT_ENV_BY_XPATH'
        self.whirlpool_corp_logo_path = 'self.locators.WHIRLPOOL_CORP_LOGO_BY_XPATH'

        self.dashboard_hamburger_menu_path = 'self.locators.DASHBOARD_HAMBURGER_MENU_BY_XPATH'
        self.dashboard_tools_menu_path = 'self.locators.DASHBOARD_TOOLS_MENU_BY_XPATH'
        self.dashboard_debugging_tool_menu_path = 'self.locators.DASHBOARD_DEBUGGING_TOOL_MENU_BY_XPATH'
        self.tools_search_input_field_path = 'self.locators.TOOLS_SEARCH_INPUT_FIELD_MENU_BY_XPATH'
        self.tools_subscribe_button_path = 'self.locators.TOOLS_SUBSCRIBE_BUTTON_BY_XPATH'

        self.get_all_elements()

    def get_all_elements(self):
        LoginPage.txt_username = self.find_element(self.txt_username_path)
        LoginPage.txt_password = self.find_element(self.txt_password_path)
        LoginPage.btn_signin = self.find_element(self.btn_signin_path)
        LoginPage.txt_dashboard = self.find_element(self.txt_dashboard_path)
        LoginPage.dropdown_env = self.find_element(self.dropdown_env_path)
        LoginPage.select_env = self.find_element(self.select_env_path)

    def subscribe_device(self,device_id):
        try:
            if self.wait_until_element_visible(self.tools_search_input_field_path):
                time.sleep(2)
                LoginPage.tools_search_input_field = self.find_element(self.tools_search_input_field_path)
                self.tools_search_input_field.clear()
                self.tools_search_input_field.send_keys(device_id)
                time.sleep(2)
                LoginPage.tools_subscribe_button = self.find_element(self.tools_subscribe_button_path)
                self.tools_subscribe_button.click()
                time.sleep(2)
                logger.info(f"Clicked on the subscribe button")
                return True
        except Exception as error:
            logger.error('Unable to click on subscribe button')
            logger.error(repr(error))
        return False

    def click_on_debugging_tool_menu(self):
        try:
            if self.wait_until_element_visible(self.dashboard_tools_menu_path):
                time.sleep(2)
                LoginPage.dashboard_tools_menu = self.find_element(self.dashboard_tools_menu_path)
                self.dashboard_tools_menu.click()
                time.sleep(2)
                LoginPage.dashboard_debugging_tool_menu = self.find_element(self.dashboard_debugging_tool_menu_path)
                self.dashboard_debugging_tool_menu.click()
                logger.info(f"Clicked on the debugging tool menu button")
                return True
        except Exception as error:
            logger.error('Unable to click on debugging tool menu button')
            logger.error(repr(error))
        return False

    def open_hamburger_menu_dashboard_page(self):
        try:
            if self.wait_until_element_visible(self.dashboard_hamburger_menu_path):
                time.sleep(2)
                LoginPage.dashboard_hamburger_menu = self.find_element(self.dashboard_hamburger_menu_path)
                self.dashboard_hamburger_menu.click()
                # self.webdriver.execute_script("arguments[0].click();", self.dashboard_hamburger_menu)
                logger.info(f"Clicked on the hamburger menu page")
                return True
        except Exception as error:
            logger.error('Unable to click on hamburger menu page')
            logger.error(repr(error))
        return False

    def verify_qa_dashboard_page(self):
        try:
            if self.wait_until_element_visible(self.txt_dashboard_path):
                time.sleep(2)
                assert self.webdriver.current_url == 'https://portal.qa.aws.whrcloud.com/wcloud-portal-ui/dashboard'
                logger.info(f"User is on the QA dashboard page")
                return True
        except Exception as error:
            logger.error('Unable to redirect to QA dashboard page')
            logger.error(repr(error))
        return False


    def verify_whirlpool_corporation_page(self):
        try:
            window_before = self.webdriver.window_handles[0]
            window_after = self.webdriver.window_handles[1]
            self.webdriver.switch_to.window(window_after)
            if self.wait_until_element_visible(self.whirlpool_corp_logo_path):
                time.sleep(2)
                logger.info(f"User is on the whirlpool corporation page")
                return True
        except Exception as error:
            logger.error('Unable to redirect to to the whirlpool corporation page')
            logger.error(repr(error))
        return False

    def select_the_environment(self):
        try:
            if self.wait_until_element_visible(self.dropdown_env_path):
                time.sleep(2)
                self.dropdown_env.click()
                self.select_env.click()
                logger.info(f"Clicked on the given environment on home page")
                return True
        except Exception as error:
            logger.error('Unable to click on the given environment on home page')
            logger.error(repr(error))
        return False

    def verify_login_page(self):
        try:
            if not self.wait_until_element_visible(self.logo_whirlpool_path):
                time.sleep(2)
                self.webdriver.reload()
                time.sleep(2)
                logger.info(f"Reloading the page")
                return True
            elif self.wait_until_element_visible(self.logo_whirlpool_path):
                time.sleep(2)
                logger.info(f"Whirlpool logo is displayed on login page")
                return True
        except Exception as error:
            logger.error('Unable to found Whirlpool logo is displayed on login page')
            logger.error(repr(error))
        return False

    def set_username(self, username):
        try:
            if self.wait_until_element_visible(self.txt_username_path):
                self.txt_username.clear()
                time.sleep(2)
                self.txt_username.send_keys(username)
                logger.info(f"Username entered: {username}")
                return True
        except Exception as error:
            logger.error('Unable to found username text-box on Login page')
            logger.error(repr(error))
        return False

    def set_password(self, password):
        try:
            if self.wait_until_element_visible(self.txt_password_path):
                self.txt_password.clear()
                time.sleep(2)
                self.txt_password.send_keys(password)
                logger.info(f"Password entered: {password}")
                return True
        except Exception as error:
            logger.error('Unable to found password text-box on Login page')
            logger.error(repr(error))
        return False

    def signin_button(self):
        try:
            if self.wait_until_element_visible(self.btn_signin_path):
                self.btn_signin.click()
                time.sleep(2)
                logger.info("Successfully clicked on signin button")
                return True
        except Exception as error:
            logger.error("Unable to click on signin button")
            logger.error(repr(error))
        return False

    def verify_dashboard_page(self):
        try:
            if self.wait_until_element_visible(self.txt_dashboard_path):
                time.sleep(2)
                assert self.txt_dashboard.text.strip() == "Dashboard"
                logger.info(f"Dashboard label is displayed on home page")
                return True
        except Exception as error:
            logger.error('Unable to found Dashboard label is displayed on home page')
            logger.error(repr(error))
        return False



    # def verify_toast_message(self, expected_message):
    #     try:
    #         if self.wait_until_element_visible(self.message_success_path):
    #             actual_message = self.message_success.text
    #             assert expected_message in actual_message
    #             time.sleep(2)
    #             logger.info("Successfully verified success message")
    #             return True
    #     except Exception as error:
    #         logger.error(f"Actual message is {actual_message} not matched with {expected_message}")
    #         logger.error(repr(error))
    #     return False
