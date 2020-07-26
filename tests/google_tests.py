from time import sleep

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from framework.action_framework import Actions
from framework.conditions import XpathExists
from framework.configuration import Config
from framework.selector import Selector, Using
from pages.google.pages_google import Search


@pytest.mark.selenium
def test_google_search(actions: Actions):
    """
    Szukaj z uzyciem samych actions'ow
    Mozesz dodawac funkcje jakie dusza zapragnie i wywolywac selenium poprzez actions,
    tam jest pod spodem duzo ogarniete
    czyli robisz np:
    actions.click(selector)
    actions.type_text(selector, text)
    actions.submit()
    itd. omowimy se to
    """
    driver = actions.element_provider.driver
    search_text = 'dr dissrespect'  # tekst do wpisania
    actions.element_provider.driver.get('https://google.pl')  # otworz gugle
    search_input_selector = Selector(Using.NAME, 'q')  # definiujesz kontrolke (to se omowic bardziej mozemy)
    actions.type_text(search_input_selector, search_text)  # wpisz text
    actions.submit()  # submit formularza
    search_result_exist_xpath = "//div[@class='g']"  # xpath do poczekania
    actions.wait_for(XpathExists(search_result_exist_xpath))  # jesli ten xpath istnieje to kolejny ekran sie zaladowal

    title = driver.title  # odczytaj tytul stronki
    assert search_text in title, f"tytul strony powinien zawierac: {search_text}"  # asercja


@pytest.mark.selenium
def test_google_search_with_page_object(actions: Actions):
    """
    Szukaj z uzyciem page objecta - to se pokminisz z czasem - prosty patern
    """
    search_text = 'dr dissrespect'
    search_page = Search(actions)  # tworze obiekt pagea
    search_page.search_for(search_text)  # wywoluje na nim metode szukaj
    driver = actions.element_provider.driver
    title = driver.title  # odczytaj tytul stronki
    assert search_text in title, f"tytul strony powinien zawierac: {search_text}"  # asercja


@pytest.mark.learn
@pytest.mark.parametrize("test_input", ["adin", "dwa", "tri"])
def test_foo( test_input,driver: WebDriver):
    user = "kolakowskajoanna"
    driver.get('https://github.com')
    sleep(2)
    login_button = driver.find_element_by_xpath("//a[@href='/login']")
    login_button.click()
    sleep(2)
    #driver.find_element_by_class_name("HeaderMenu-link no-underline mr-3").click()
    driver.find_element_by_name("login").send_keys(user)

    driver.find_element_by_name("password").send_keys("???")
    driver.find_element_by_name("commit").click()
    try:
        driver.find_element_by_xpath("//a[@href='/new' and contains(@class, 'btn-sm')]")
        button_exists = True
    except:
        button_exists = False
    assert button_exists, "przycisk New powinien istniec"
    sleep(4)
    assert (driver.title == 'GitHub'), "tytul strony powinien byc: 'github'"
    button_new = driver.find_element_by_xpath("//a[@href='/new' and contains(@class, 'btn-sm')]")
    button_new.click()
    driver.find_element_by_name('repository[name]').send_keys(test_input)
    sleep(2)
    btn_submit = driver.find_element_by_xpath("//div[@class='js-with-permission-fields']//button[@type='submit']")
    btn_submit.click()
    sleep(3)
    assert (driver.title == f"{user}/{test_input}"), "nie ma repo:c"

