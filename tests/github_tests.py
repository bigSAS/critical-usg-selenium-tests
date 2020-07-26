from typing import List

import pytest, yaml, os

from data_classes.github import GitHubUser, GitHubUserWithRepo, GitHubRepo
from framework.action_framework import Actions
from pages.git_hub.delete_repo import DeleteRepo
from pages.git_hub.login import GitHubLogin
from pages.git_hub.new_issue import GitHubNewIssue
from pages.git_hub.new_repo import GitHubNewRepo
from selenium.webdriver.remote.webdriver import WebDriver

from pages.repo_list import GitHubRepoList

AVOID_DELETION_REPOS = {
    'kolakowskajoanna': [
        'praca_dyplomowa',
        'zadanie_fakultet',
        'fakultet',
        'PSIK',
        'product-mvc-app'
    ]
}


def get_avoided_repos(username: str) -> List[str]:
    repos = AVOID_DELETION_REPOS.get(username, None)
    if repos is None: raise Exception(f'{username} not found :(')
    return repos


def get_password(username: str) -> str:
    try:
        path = os.environ.get('GITHUB_PASSWORDZ_PATH', None)
        current_dir = os.path.dirname(__file__)
        filepath = path if path else current_dir + '\\github_passwords.yml'
        with open(filepath, mode='r', encoding='utf-8') as f:
            loaded: dict = yaml.load(f, Loader=yaml.FullLoader)
            password = loaded.get(username, None)
            if password is None: raise Exception(f'Password for user {username} not found :(')
            return password
    except Exception as e:
        raise Exception('Read password file failed ...\n' + repr(e))


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
    GitHubUserWithRepo(asia, GitHubRepo('TEST__jolo')),
    GitHubUserWithRepo(asia, GitHubRepo('INNE_cos', False))

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
@pytest.mark.debugin
@pytest.mark.parametrize(
    "github_user, reponame, title, comment",
    [
        [asia, 'INNE_cos', 'hajo error', 'dej fitke'],
    ]
)
def test_add_new_issue(actions: Actions, driver: WebDriver,
                       github_user: GitHubUser, reponame: str, title: str, comment: str):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user.username,
        password=github_user.password
    )
    github_add_new_issue_page = GitHubNewIssue(
        actions=actions,
        github_user=github_user,
        reponame=reponame
    )
    github_add_new_issue_page.open()
    github_add_new_issue_page.fill_form(
        title=title,
        comment=comment
    )
    github_add_new_issue_page.submit()


@pytest.mark.learn
@pytest.mark.parametrize("github_user_with_repo", [
    GitHubUserWithRepo(asia, GitHubRepo('INNE_cos'))])
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
def test_delete_repos(actions: Actions, driver: WebDriver, github_user: GitHubUser):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user.username,
        password=github_user.password
    )
    github_repo_list_page = GitHubRepoList(actions, github_user)
    github_repo_list_page.open()
    repos_for_deletion = github_repo_list_page.get_names(get_avoided_repos(github_user.username))
    for repo_name in repos_for_deletion:
        github_user_with_repo = GitHubUserWithRepo(
            user=github_user,
            repo=GitHubRepo(name=repo_name)
        )
        github_delete_page = DeleteRepo(actions, github_user_with_repo)
        github_delete_page.open()
        github_delete_page.delete()
        github_delete_page.confirm()


@pytest.mark.learn
@pytest.mark.parametrize("github_user", [asia])
def test_delete_repos_with_prefix(actions: Actions, driver: WebDriver, github_user: GitHubUser):
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user.username,
        password=github_user.password
    )
    github_repo_list_page = GitHubRepoList(actions, github_user)
    github_repo_list_page.open()
    repos_for_deletion = github_repo_list_page.get_names_with_prefix()
    for repo_name in repos_for_deletion:
        github_user_with_repo = GitHubUserWithRepo(
            user=github_user,
            repo=GitHubRepo(name=repo_name)
        )
        github_delete_page = DeleteRepo(actions, github_user_with_repo)
        github_delete_page.open()
        github_delete_page.delete()
        github_delete_page.confirm()


