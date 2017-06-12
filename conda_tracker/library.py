import subprocess

from conda_tracker import modifier


def repository_name(repository_url):
    """Split the suffix from the URL.

    Positional arguments:
    repository_url -- the link to the repository to clone
    """
    name = repository_url.rsplit('/', 1)[-1]

    # remove the .git ending when given git repositories
    return name.replace('.git', '')


def add_repository(repository_url):
    """Add a sub-repository to the aggregate repository."""

    repo_subdir = '{0}/{0}' .format(repository_name(repository_url))

    subprocess.call(['git', 'subrepo', 'clone', repository_url, repo_subdir])


def update_repository(repository, branch, all_repositories=False):
    """Update the sub-repository to the lastest branch or to a specific branch.

    Positional arguments:
    repository -- the name of the repository as given by the directory name

    Optional arguments:
    branch -- the name of the branch to pull from
    all_repositories -- update all repositorys located in the directory
    """
    cmd = ['git', 'subrepo', 'pull']

    if branch and repository:
        cmd.extend([repository, '-b', branch])

    elif repository:
        cmd.append(repository)

    elif all_repositories:
        cmd.append('--all')

    subprocess.call(cmd)


def patch_repository(repository, patch_file, nested=False):
    """Apply the given patch to the corresponding recipe in the directory.

    Positional arguments:
    repository -- the name of the repository as given by the directory name
    patch_file -- the path to the patch file

    Optional arguments:
    nested -- whether or not the subrepo is nested inside its own package
    """
    patch_file = modifier.modify_patch(patch_file, repository, nested)

    subprocess.call(['git', 'am', patch_file, '-3'])
