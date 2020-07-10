from framework.action_framework import Page
from framework.conditions import XpathExists
from framework.selector import Selector, Using


class GitHubNewRepo(Page):
    new_repo_button = Selector(Using.XPATH, "//a[@href='/new' and contains(@class, 'btn-sm')]")
    new_repo_name_input = Selector(Using.NAME, 'repository[name]')
    new_repo_descrip_input = Selector(Using.ID,'repository_description')
    visibility_public_check = Selector(Using.ID, 'repository_visibility_public')
    visibility_private_check = Selector(Using.ID, 'repository_visibility_private')
    submit_button = Selector(Using.XPATH, "//div[@class='js-with-permission-fields']//button[@type='submit']")

    def goto_new_repo_form(self):
        self.actions.click(self.new_repo_button)
        self.actions.wait_for(XpathExists("//form[@id='new_repository']"))

    def fill_form(self, reponame: str, public=True):
        self.actions.type_text(self.new_repo_name_input, reponame)
        # self.actions.wait_for(XpathExists("//dd[@class='success']"))
        if public: self.actions.click(self.visibility_public_check)
        else: self.actions.click(self.visibility_private_check)

    def submit(self):
        self.actions.click(self.submit_button)