from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from test_automation.utilities.log import logger
from .web_base_page_object import BasePageObject, BasePageElement, BaseMultiPageElement
from .web_base_page_object import LOCATOR_MAP

LOCATOR_MAP_TO_CONSTANT = {'CSS': 'css',
                           'ID': 'id',
                           'NAME': 'name',
                           'XPATH': 'xpath',
                           'LINKTEXT': 'link_text',
                           'PARTIALLINKTEXT': 'partial_link_text',
                           'TAGNAME': 'tag_name',
                           'CLASSNAME': 'class_name',
                           }


class BasePage(BasePageObject):

    def __init__(self, webdriver, locators, conf, message):

        BasePageObject.__init__(self, webdriver)
        self.locators = locators
        self.conf = conf
        self.message = message
        self.get_elements()

    def get_elements(self):
        pass

    def resolve_locator_value(self, locator_str):

        locator_value = eval(locator_str)
        locator_method = locator_str.split('BY_')[1]
        bool_data = locator_method in LOCATOR_MAP_TO_CONSTANT.keys()

        if not bool_data:
            raise ElementNotVisibleException(
                'Element method has to be one from {0}'.format(
                    LOCATOR_MAP_TO_CONSTANT.keys()))

        locator_method = LOCATOR_MAP_TO_CONSTANT[locator_method]
        return locator_method, locator_value

    def find_element(self, locator_str, postfix_str=''):
        locator_method, locator_value = self.resolve_locator_value(locator_str)
        return eval('BasePageElement(' + locator_method + '=\'' +
                    locator_value.format(postfix_str) + '\')')

    def find_elements(self, locator_str, postfix_str=''):
        locator_method, locator_value = self.resolve_locator_value(locator_str)
        return eval('BaseMultiPageElement(' +
                    locator_method + '=\'' + locator_value.format(postfix_str) + '\')')

    def fetch_element_locator(self, locator_str, postfix_str=''):
        locator_method, locator_value = self.resolve_locator_value(locator_str)
        locator_value = locator_value.format(postfix_str)
        return LOCATOR_MAP[locator_method], locator_value

    def wait_until_element_visible(self, locator_str, timeout=60, pollfrequency=1, postfix_str='', log=True):
        try:
            self.wait_until_page_is_loaded()
            web_driver_wait = WebDriverWait(self.webdriver, timeout, poll_frequency=pollfrequency,
                                            ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,
                                                                ElementNotSelectableException])
            locator_method, locator_value = self.fetch_element_locator(locator_str, postfix_str)
            web_driver_wait.until(EC.visibility_of_element_located((locator_method, locator_value)))
        except:
            if log:
                logger.error(f"Unable to get webdriver :{locator_method, locator_value} ")
            return False
        return True

    def wait_until_page_is_loaded(self):
        is_jquery_status = False
        try:
            is_jquery_status = WebDriverWait(self.webdriver, 60, poll_frequency=1).until(
                lambda webdriver: self.webdriver.execute_script('return document.readyState == "complete";'))
            logger.debug("JQuery readyState status:: {0}".format(is_jquery_status))
        except Exception as ae:
            logger.info("exception while running jquery ::: {0}".format(ae))
        return is_jquery_status
