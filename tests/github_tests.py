import pytest

from framework.action_framework import Actions
from pages.git_hub.login import GitHubLogin


@pytest.mark.learn
@pytest.mark.parametrize("usename, password", [
    ['bigSAS', '???'],
    ['kolakowskajoanna', 'asdas']
])
def test_login(actions: Actions, usename: str, password: str):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(usename, password)
    assert github_login_page.title == 'GitHub', "Tytul strony jest niepoprawny"
