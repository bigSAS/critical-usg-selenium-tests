from framework.action_framework import Page
from framework.conditions import XpathExists
from framework.selector import Selector, Using


class GitHubLogin(Page):
    url = "https://github.com"
    sign_in_button = Selector(Using.XPATH, "//a[@href='/login']")
    username_input = Selector(Using.NAME, "login")
    password_input = Selector(Using.NAME, "password")

    def goto_login_form(self):
        self.actions.click(self.sign_in_button)
        self.actions.wait_for(XpathExists("//div[@id='login']/form"))

    def login(self, username: str, password: str):
        self.actions.type_text(selector=self.username_input, text=username)
        self.actions.type_text(selector=self.password_input, text=password)
        self.actions.submit()
        self.actions.wait_for(XpathExists("//div[@id='dashboard']"))

