import pytest
from selenium import webdriver
from framework.action_framework import Actions
from framework.configuration import Config
from framework.element_provider import BasicWebElementProvider


@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver

    driver.quit()


@pytest.fixture(scope='function')
def actions(driver, conf):
    actions = Actions(BasicWebElementProvider(driver, config=conf))
    yield actions


@pytest.fixture(scope='session')
def conf():
    cfg = Config.from_file()
    return cfg
