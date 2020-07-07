import logging
from abc import ABC

from selenium.webdriver.support.wait import WebDriverWait

from framework.selector import Selector, Using
from framework.element_provider import WebElementProvider


class Actions:
    def __init__(self, element_provider: WebElementProvider):
        self.__element_provider = element_provider
    
    @property
    def element_provider(self) -> WebElementProvider:
        return self.__element_provider
    
    def click(self, selector: Selector, timeout: int = None):
        logging.info(f'click: {selector}')
        self.element_provider.find_element(selector, timeout).click()
        
    def type_text(self, selector: Selector, text: str, timeout: int = None):
        logging.info(f'type text: {selector}')
        self.element_provider.find_element(selector, timeout).send_keys(text)
    
    def submit(self, selector: Selector = None, timeout: int = None):
        s = selector if selector else Selector(Using.XPATH, '//form')
        logging.info(f'submit: {s}')
        self.element_provider.find_element(s, timeout).submit()

    def wait_for(self, condition, timeout: int = None):
        logging.info(f'wait for: {condition}')
        tout = timeout if timeout is not None else self.element_provider.config\
            .action_framework.timeout_wait_for_condition_sec
        return WebDriverWait(self.element_provider.driver, tout) \
            .until(condition)

    def get_attribute(self, selector: Selector, attr: str, timeout: int = None) -> str:
        logging.info(f'get attribute: {selector} [{attr}]')
        return self.element_provider.find_element(selector, timeout)\
            .get_attribute(attr)

    def get_text(self, selector: Selector, timeout: int = None) -> str:
        return self.get_attribute(selector, 'innerText', timeout)
    
    def execute_js(self, js_script: str) -> str:
        logging.info(f'execute js:\n{js_script}')
        return str(self.element_provider.driver.execute_script(js_script))


class Page(ABC):
    def __init__(self, actions: Actions):
        self.__actions = actions
    
    @property
    def actions(self) -> Actions:
        return self.__actions

    def open(self, url: str):
        logging.info(f'open: "{url}"')
        self.actions.element_provider.driver.get(url)
