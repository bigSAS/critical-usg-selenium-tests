from dataclasses import dataclass

import pytest, yaml, os

from framework.action_framework import Actions
from pages.git_hub.delete_repo import DeleteRepo
from pages.git_hub.login import GitHubLogin
from pages.git_hub.new_repo import GitHubNewRepo
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

from pages.repo_list import GitHubRepoList


def get_password(username: str) -> str:
    try:
        current_dir = os.path.dirname(__file__)
        filepath = current_dir + '\\github_passwords.yml'
        with open(filepath, mode='r', encoding='utf-8') as f:
            loaded: dict = yaml.load(f, Loader=yaml.FullLoader)
            password = loaded.get(username, None)
            if password is None: raise Exception(f'Password for user {username} not found :(')
            return password
    except Exception as e:
        raise Exception('Read password file failed ...\n' + repr(e))


@dataclass
class GitHubUser:
    username: str
    password: str


@dataclass
class GitHubRepo:
    name: str
    public: bool = True


class GitHubUserWithRepo:
    def __init__(self, user: GitHubUser, repo: GitHubRepo):
        self.user = user
        self.repo = repo


asia = GitHubUser('kolakowskajoanna', get_password('kolakowskajoanna'))
# sas = GitHubUser('bigSAS', get_password('bigSAS'))


@pytest.mark.learn
@pytest.mark.parametrize("github_user", [asia])
def test_login(actions: Actions, github_user: GitHubUser):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user.username,
        password=github_user.password
    )
    assert github_login_page.title == 'GitHub', "Tytul strony jest niepoprawny"


@pytest.mark.learn
@pytest.mark.parametrize("github_user_with_repo", [
    GitHubUserWithRepo(asia, GitHubRepo('yoloo')),
    GitHubUserWithRepo(asia, GitHubRepo('asd', False))

])
def test_new_repo(actions: Actions, github_user_with_repo: GitHubUserWithRepo):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_new_repo_form = GitHubNewRepo(actions)
    github_new_repo_form.goto_new_repo_form()
    github_new_repo_form.fill_form(public=github_user_with_repo.repo.public, reponame=github_user_with_repo.repo.name)
    github_new_repo_form.submit()
    assert github_new_repo_form.title == f'{github_user_with_repo.user.username}/{github_user_with_repo.repo.name}',\
        'repo nie powstalo'

@pytest.mark.learn
@pytest.mark.parametrize("github_user_with_repo", [
    GitHubUserWithRepo(asia, GitHubRepo('asd'))])
def test_delete_repo(actions: Actions, github_user_with_repo: GitHubUserWithRepo):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_delete_page = DeleteRepo(actions, github_user_with_repo)
    github_delete_page.open()
    github_delete_page.delete()
    github_delete_page.confirm()
    assert github_delete_page.title == 'GitHub', 'nie usunieto'


@pytest.mark.learn
@pytest.mark.parametrize("github_user", [asia])
def test_repo_list(actions: Actions,driver: WebDriver, github_user: GitHubUser):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user.username,
        password=github_user.password
    )
    github_repo_list_page = GitHubRepoList(actions, github_user)
    github_repo_list_page.open()
    repos = github_repo_list_page.get()
    print(repos)