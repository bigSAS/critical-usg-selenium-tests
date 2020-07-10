from framework.action_framework import Page, Actions
from framework.selector import Selector, Using


class GitHubRepoList(Page):
    url = 'https://github.com/{username}?tab=repositories'

    def __init__(self, actions: Actions, github_user):
        super().__init__(actions)
        self.github_user = github_user

    def open(self, url: str = None):
        if url is not None: super().open(url)
        else:
            uri = self.url.format(username=self.github_user.username)
            super().open(uri)

    def get(self):
        a = Selector(Using.XPATH, '//h3[@class="wb-break-all" and contains(itemprop, name)]')
        elems = self.actions.get_elements_text(a)
        repos = []
        for elem in elems:
            item = elem.replace(' Private', '')
            repos.append(item)
        return repos

