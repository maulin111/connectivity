from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

LOCATOR_MAP = {'css': By.CSS_SELECTOR,
               'id': By.ID,
               'name': By.NAME,
               'xpath': By.XPATH,
               'link_text': By.LINK_TEXT,
               'partial_link_text': By.PARTIAL_LINK_TEXT,
               'tag_name': By.TAG_NAME,
               'class_name': By.CLASS_NAME,
               }


class BasePageObject(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver


class BasePageElement(object):
    def __init__(self, context=False, **kwargs):
        self.has_context = None
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        key, value = next(iter(kwargs.items()))
        self.locator = (LOCATOR_MAP[key], value)
        self.has_context = bool(context)

    def find(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None
        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)
        if not context:
            context = instance.webdriver
        return self.find(context)


class BaseMultiPageElement(BasePageElement):
    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []
