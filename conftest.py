import pytest, os, logging
from selenium import webdriver

from framework.action_framework import Actions
from framework.configuration import Config
from framework.element_provider import BasicWebElementProvider

DRIVER_SCOPE = 'session'
CONFIG_PATH = os.environ.get('SELENIUM_CONFIG_PATH', None)
if not CONFIG_PATH:
    logging.warning('SELENIUM_CONFIG_PATH not set! using default selenium_config.yml')
    CONFIG_PATH = 'selenium_config.yml'


@pytest.fixture(scope=DRIVER_SCOPE)
def driver(conf):
    if conf.wd_hub_url:
        caps = {
            "browser_name": conf.browser,
            "version": str(conf.browser_version),
            "enableVNC": True,
            "enableVideo": False,
            "acceptInsecureCerts": True
        }
        options = webdriver.ChromeOptions()
        options.headless = conf.headless
        options.add_argument('--start-maximized')
        driver = webdriver.Remote(
            command_executor=conf.wd_hub_url,
            desired_capabilities=caps,
            options=options
        )
    else:
        driver = webdriver.Chrome()

    yield driver
    driver.quit()


@pytest.fixture(scope=DRIVER_SCOPE)
def actions(driver, conf):
    actions = Actions(BasicWebElementProvider(driver, conf))
    return actions


@pytest.fixture(scope='session')
def conf():
    cfg = Config.from_file(CONFIG_PATH)
    return cfg
