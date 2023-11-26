import pytest
from test_automation.configuration import common_configuration as conf
from test_automation.resources import web_page_message_constant as const
from test_automation.pom.pages.login_page import LoginPage
from test_automation.resources import web_page_element_locators as locators
from test_automation.resources import web_page_message_constant as message
from test_automation.utilities.ConfigParser import set_current_test_file_case_name, log_test_data, CONFIG, \
    take_screenshot
from test_automation.utilities.log import logger
from test_automation.utilities.script_helper import test_step as steps


@pytest.mark.usefixtures("web_driver")
class TestHomePageTC1:
    driver = None
    login_page = None

    @pytest.fixture(autouse=True)
    def set_up(self, request, web_driver):
        self.driver = web_driver
        set_current_test_file_case_name(request)
        self.login_page = LoginPage(self.driver, locators, conf, message)
        yield
        log_test_data()

    def test_verify_home_page_screen(self):
        logger.debug_test_case_start(CONFIG.current_test_name)
        try:
            steps(1, "Enter user name on Login page")
            assert self.login_page.verify_login_page(), "Unable to find whirlpool logo on the login page"
            logger.info_step_verification(1, "Successfully verified whirlpool logo on login page")

            steps(2, "Enter username on Login page")
            assert self.login_page.set_username(conf.USER_NAME), "Unable to enter username"
            logger.info_step_verification(2, "Successfully entered username")

            steps(3, "Enter password on Login page")
            assert self.login_page.set_password(conf.PASSWORD), "Unable to enter password"
            logger.info_step_verification(3, "Successfully entered password")

            steps(4, "Click on signin button on Login page")
            assert self.login_page.signin_button(), "Unable to click on signin button"
            logger.info_step_verification(4, "Successfully clicked on signin button")

            steps(5, "Verify the Dashboard page")
            assert self.login_page.verify_dashboard_page(), "Unable to find Dahsboard page on the home page"
            logger.info_step_verification(5, "Successfully verified Dashboard page")

            steps(6, "Click on QA environment")
            assert self.login_page.select_the_environment(), "Unable to find the given environment on the home page"
            logger.info_step_verification(6, "Successfully Clicked on QA option")

            steps(7, "Verify the Whirlpool Corporation logo on new window")
            assert self.login_page.verify_whirlpool_corporation_page(), "Unable to found whirlpool corporation page"
            logger.info_step_verification(7, "Successfully verified Whirlpool Corporation page")

            steps(8, "Enter username on Login page")
            assert self.login_page.set_username(conf.USER_NAME), "Unable to enter username address"
            logger.info_step_verification(8, "Successfully entered username")

            steps(9, "Enter password on Login page")
            assert self.login_page.set_password(conf.PASSWORD), "Unable to enter password"
            logger.info_step_verification(3, "Successfully entered password")

            steps(10, "Click on signin button on Login page")
            assert self.login_page.signin_button(), "Unable to click on signin button"
            logger.info_step_verification(10, "Successfully clicked on signin button")

            steps(11, "Verify the QA Dashboard")
            assert self.login_page.verify_qa_dashboard_page(), "Unable to find QA dashboard home page"
            logger.info_step_verification(11, "Successfully verified QA Dashboard page")

            steps(12, "Click on hamburger menu")
            assert self.login_page.open_hamburger_menu_dashboard_page(), "Unable to find hamburger menu"
            logger.info_step_verification(12, "Successfully clicked on hamburger button")

            steps(13, "Click on debugging tool menu")
            assert self.login_page.click_on_debugging_tool_menu(), "Unable to click on debugging tool menu"
            logger.info_step_verification(13, "Successfully clicked on debugging tool menu")

            steps(14, "Search and subscribe the device")
            assert self.login_page.subscribe_device(conf.DEVICE_ID), "Unable to Search and subscribe the device"
            logger.info_step_verification(14, "Successfully Search and subscribe the device")

        except Exception as error:
            take_screenshot(self.driver, "test_home_page_tc_1_submit_the_login_page_details")
            raise error
        finally:
            # self.login_page.click_on_logout_button()
            logger.info_test_case_end(CONFIG.current_test_name)
