from typing import List

import pytest, yaml, os

from data_classes.github import GitHubUser, GitHubUserWithRepo, GitHubRepo
from framework.action_framework import Actions
from framework.conditions import XpathExists
from pages.git_hub.branches import GitHubBranches
from pages.git_hub.delete_repo import DeleteRepo
from pages.git_hub.login import GitHubLogin
from pages.git_hub.merge import GitHubMerge
from pages.git_hub.new_file import GitHubNewCommit
from pages.git_hub.new_issue import GitHubNewIssue
from pages.git_hub.new_repo import GitHubNewRepo
from selenium.webdriver.remote.webdriver import WebDriver

from pages.git_hub.pull_request import GitHubNewPullRequest
from pages.git_hub.repo import GitHubRepoMain
from pages.repo_list import GitHubRepoList

AVOID_DELETION_REPOS = {
    'kolakowskajoanna': [
        'testowe',
        'TEST__jolo',
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
tester = GitHubUser('jtesterk', get_password('jtesterk'))


@pytest.mark.github
@pytest.mark.parametrize("github_user", [tester])
def test_login(actions: Actions, github_user: GitHubUser):
    """
    Logowanie

    1.otwórz formularza logowanie
    2.uzupełnij formularza logowania
    3.kliknij “ Sign in”

    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user.username,
        password=github_user.password
    )
    assert github_login_page.title == 'GitHub', "Tytul strony jest niepoprawny"


@pytest.mark.github
@pytest.mark.parametrize("github_user_with_repo", [
    GitHubUserWithRepo(tester, GitHubRepo('TEST__check'))
])
def test_new_repo(actions: Actions, github_user_with_repo: GitHubUserWithRepo):
    """
    Dodanie nowego repozytorium

    1.zaloguj się
    2.przejdź do formularza tworzenia nowego repozytorium
    3.uzupełnij formularz
    4.potwierdź poprzez “Create repository”
    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_new_repo_form = GitHubNewRepo(actions)
    github_new_repo_form.open()
    github_new_repo_form.fill_form(public=github_user_with_repo.repo.public, reponame=github_user_with_repo.repo.name)
    github_new_repo_form.submit()
    assert github_new_repo_form.title == f'{github_user_with_repo.user.username}/{github_user_with_repo.repo.name}', \
        'repo nie powstalo'


@pytest.mark.github
@pytest.mark.debugin
@pytest.mark.parametrize(
    "github_user, reponame, title, comment",
    [
        [tester, 'TEST__check', 'hajo error', 'dej fitke'],
    ]
)
def test_add_new_issue(actions: Actions, driver: WebDriver,
                       github_user: GitHubUser, reponame: str, title: str, comment: str):
    """
    Dodanie new issue

    1.zaloguj sie
    2.otwórz formularz zgłaszania
    3.uzupełnij formularz
    4.kliknij “Submit new issue”
    """
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
    # todo: add assert


@pytest.mark.github
@pytest.mark.test
@pytest.mark.parametrize(
    "github_user_with_repo, branchname",
    [
        [GitHubUserWithRepo(tester, GitHubRepo('TEST__check')), "best"]
    ]
)
def test_add_new_branch(actions: Actions, driver: WebDriver,
                        github_user_with_repo: GitHubUserWithRepo, branchname: str):
    """
    Stworzenie nowego brancha

    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_repo_page = GitHubRepoMain(actions, github_user_with_repo)
    github_repo_page.open()
    github_repo_page.add_branch(branchname=branchname)
    xpath_format = f'//span[@class="css-truncate-target" and contains(.,"{branchname}")]'
    assert XpathExists(xpath_format), 'nie powstało nowe repo'


@pytest.mark.github
@pytest.mark.test
@pytest.mark.parametrize(
    "github_user_with_repo, branchname, filename",
    [
        [GitHubUserWithRepo(tester, GitHubRepo('TEST__check')), "best", "test101"]
    ]
)
def test_add_new_commit(actions: Actions, driver: WebDriver,
                        github_user_with_repo: GitHubUserWithRepo, branchname: str, filename: str):
    """
    Dodoanie nowego commitu do nowego brancha
    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_new_commit_page = GitHubNewCommit(actions, github_user_with_repo, branchname)
    github_new_commit_page.open()
    github_new_commit_page.fill_form(
        filename=filename
    )
    github_new_commit_page.submit()
    # todo: add assertion


@pytest.mark.github
@pytest.mark.test
@pytest.mark.parametrize(
    "github_user_with_repo, branchname",
    [
        [GitHubUserWithRepo(tester, GitHubRepo('TEST__check')), "best"]
    ]
)
def test_create_pull_request(actions: Actions, driver: WebDriver,
                             github_user_with_repo: GitHubUserWithRepo, branchname: str):
    """
    Create pull request master <- new_branch
    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_new_pull_request_page = GitHubNewPullRequest(actions, github_user_with_repo, branchname)
    github_new_pull_request_page.open()
    github_new_pull_request_page.create()


@pytest.mark.github
@pytest.mark.test
@pytest.mark.parametrize(
    "github_user_with_repo", [GitHubUserWithRepo(tester, GitHubRepo('TEST__check'))])
def test_merge(actions: Actions, driver: WebDriver,
               github_user_with_repo: GitHubUserWithRepo):
    """
    Marge
    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_merge_page = GitHubMerge(actions, github_user_with_repo)
    github_merge_page.open()
    github_merge_page.pick_pull_requests()
    github_merge_page.create()

    # assert not XpathExists(github_merge_page.xpath_pull_request), "arono"


@pytest.mark.github
@pytest.mark.test
@pytest.mark.parametrize(
    "github_user_with_repo, branchname",
    [
        [GitHubUserWithRepo(tester, GitHubRepo('TEST__check')), "best"]
    ]
)
def test_delete_branch(actions: Actions, driver: WebDriver,
                       github_user_with_repo: GitHubUserWithRepo, branchname: str):
    """
    Usunięcie brancha

    """
    github_login_page = GitHubLogin(actions)
    github_login_page.open()
    github_login_page.goto_login_form()
    github_login_page.login(
        username=github_user_with_repo.user.username,
        password=github_user_with_repo.user.password
    )
    github_branches_page = GitHubBranches(actions, github_user_with_repo)
    github_branches_page.open()
    github_branches_page.delete_branch(branchname=branchname)
    xpath_format = f'//li//div[contains(.,"{branchname}") and contains(.,"Deleted just now by ")]'
    assert XpathExists(xpath_format), 'Nie usunięto repo'


@pytest.mark.deletion
@pytest.mark.parametrize("github_user_with_repo", [
    GitHubUserWithRepo(tester, GitHubRepo('INNE_cos'))])
def test_delete_repo(actions: Actions, github_user_with_repo: GitHubUserWithRepo):
    """
    Usunięcie danego repozytorium

    """
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


@pytest.mark.deletion
@pytest.mark.parametrize("github_user", [tester])
def test_delete_repos(actions: Actions, driver: WebDriver, github_user: GitHubUser):
    """
    Usunięcie repozytoriów spoza whitelist
    """
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
        assert github_delete_page.title == 'GitHub', 'nie usunieto'


@pytest.mark.github
@pytest.mark.parametrize("github_user", [tester])
def test_delete_repos_with_prefix(actions: Actions, driver: WebDriver, github_user: GitHubUser):
    """
    Usunięcie repozytoriów z prefixem 'TEST__'

    """
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
        assert github_delete_page.title == 'GitHub', 'nie usunieto'
