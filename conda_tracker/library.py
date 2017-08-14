import os
import re

import git
from github import Github

from conda_tracker.utils import remove_submodule


def create_aggregate_repository(repository_name, path='.'):
    """Create a new repository that will house all submodules.

    The repository will be created in the current working directory
    or at the given path. An initial commit with a README is created
    as submodules have buggy behavior in a bare repository.

    Parameters
    ----------
    repository_name: str
        The name of the repository to create.
    path: str
        The directory in which to create the repository.
        Default is the current working directory.

    Returns
    -------
    repository: git.Repo
        The newly created repository.

    """
    aggregate_repository = os.path.join(path, repository_name)
    git.Repo.init(aggregate_repository)
    new_repository = git.Repo(aggregate_repository)

    first_committed_file = os.path.abspath(os.path.join(aggregate_repository, 'README.rst'))

    with open(first_committed_file, 'w') as readme:
        readme.write('aggregate repository')

    new_repository.index.add([first_committed_file])
    new_repository.index.commit('Initial commit')

    return new_repository


def access_github_api(token=None):
    """Access the Github API with a personal access token.

    Parameters
    ----------
    token: str
        The Github personal access token.
        If no token is given, the environment is searched for
        the GITHUB_TOKEN environment variable.

    Returns
    -------
    response: github.Github
        A github.Github object with API access methods

    Raises
    ------
    RuntimeError
        When a token is not given and it is not found in the environment
    """
    if token is None:
        try:
            token = os.environ['GITHUB_TOKEN']
        except KeyError:
            raise RuntimeError('GITHUB_TOKEN environment variable not found. '
                               'Please export the GITHUB_TOKEN variable to '
                               'the environment or provide a '
                               'personal access token.')

    return Github(token)


def retrieve_organization_repositories(organization, token=None):
    """Retrieve all of the repositories from the organization.

    Parameters
    ----------
    organization: str
        The name of the organization to fetch repositories from.
    token: str
        The Github personal access token.
        If no token is given, the environment is searched for
        the GITHUB_TOKEN environment variable.

    Returns
    -------
    repositories: github.Github.PaginatedList
        An array_like structure that contains github.Github repo objects.
    """
    return access_github_api(token).get_organization(organization).get_repos()


def add_submodules(source_repository, aggregate_repository, refined_repositories=''):
    """Add submodules from the source_repository to the aggregate_repository.

    Parameters
    ----------
    source_repository: github.Github.PaginatedList
        The repositories obtained from the Github API.
    aggregate_repository: str
        The directory name of the aggregate_repository.
    refined_repositories: str
        A regular expression to match to repositories
        that should be downloaded.
        Defaults to ' '

    Returns
    -------
    None
    """
    aggregate_repository = git.Repo(aggregate_repository)

    refined_repositories = re.compile(refined_repositories)

    for repository in source_repository:
        if refined_repositories.match(repository.name):
            aggregate_repository.create_submodule(name=repository.name,
                                                  path=repository.name,
                                                  url=repository.clone_url)

    aggregate_repository.index.commit('Add submodules')


def update_submodules(aggregate_repository):
    """Update all of the submodules in the aggregate repository.

    Parameters
    ----------
    aggregate_repository: str
        The directory name of the aggregate repository.

    Returns
    -------
    None
    """
    aggregate_repository_repo = git.Repo(aggregate_repository)

    for submodule in aggregate_repository_repo.submodules:
        try:
            submodule.update()
        except git.exc.GitCommandError:
            print('Removing submodule {}' .format(submodule.name))
            remove_submodule(aggregate_repository, submodule.name)

    aggregate_repository_repo.index.commit('Updated all submodules')


def gather_submodules(source_repository, aggregate_repository):
    """Gather all of the submodules in the source_repository that are not in the aggregate_repository.

    Parameters
    ----------
    source_repository: github.Github.PaginatedList
        The repositories obtained from the Github API.
    aggregate_repository: str
        The directory name of the aggregate_repository.

    Returns
    -------
    None
    """
    aggregate_repository = git.Repo(aggregate_repository)
    aggregate_repository_submodules = [submodule.name for submodule
                                       in aggregate_repository.submodules]

    for repository in source_repository:
        if repository.name not in aggregate_repository_submodules:
            aggregate_repository.create_submodule(name=repository.name,
                                                  path=repository.name,
                                                  url=repository.clone_url)


def submit_submodules(aggregate_repository):
    """Push all of the commits in the aggregate repository to origin.

    Parameters
    ----------
    aggregate_repository: str
        The directory name of the aggregate_repository.

    Returns
    -------
    None
    """
    aggregate_repository = git.Repo(aggregate_repository)
    origin = aggregate_repository.remote(name='origin')
    origin.push()
