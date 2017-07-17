import pkg_resources
import subprocess


def repository_name(repository_url):
    """Split the suffix from the URL.

    Positional arguments:
    repository_url -- the link to the repository to clone
    """
    name = repository_url.rsplit('/', 1)[-1]

    # remove the .git ending when given git repositories
    return name.replace('.git', '')


def retrieve_latest_commit(branch):
    """Retrieve the last commit made on the given branch."""
    subprocess.call(['git', 'rev-parse', branch])


def retrieve_updated_submodules(submodule='.'):
    """Retrieve a list of submodules that have been updated.

    Updated submodules' hashes start with '+' when the command
    git submodule status is run. The updated submodules are
    returned in a list with the '+' stripped from their hashes.
    """
    submodules = subprocess.check_output(['git', 'submodule', 'status',
                                         submodule], universal_newlines=True)

    return [submodule.lstrip('+') for submodule in submodules.splitlines()
            if submodule.startswith('+')]


def retrieve_submodule_commits(branch):
    """Retrieve the current submodule commit hashes for a specific branch."""
    return subprocess.check_output(['git', 'ls-tree', branch],
                                   universal_newlines=True).splitlines()


def retrieve_submodule_files_changed():
    diff_script = pkg_resources.resource_filename('conda_tracker',
                                                  'diff-script.sh')

    diff = subprocess.check_output(['bash', diff_script],
                                   universal_newlines=True).splitlines()

    submodule_changed_files = [line.split() for line in diff]

    submodules_with_recipe_changes = set()
    for submodule in submodule_changed_files:
        for file in submodule:
            if 'recipe/' in file:
                submodules_with_recipe_changes.add(submodule[0])

    return submodules_with_recipe_changes


def change_submodule_revision(submodule, revision):
    """Change the submodule commit reference to a different revision.

    Positional arguments:
    submodule -- the submodule to change
    revision -- the commit to point to
    """
    revision_script = pkg_resources.resource_filename('conda_tracker',
                                                      'change_revision.sh')

    subprocess.call(['bash', revision_script, submodule, revision])


def add_repository(repository_url):
    """Add a sub-repository to the aggregate repository.

    Positional arguments:
    repository_url -- the url to the repository to add

    Optional arguments:
    nested -- whether or not the subrepo is nested inside its own package
    """
    subprocess.call(['git', 'submodule', 'add', repository_url])


def update_submodules(submodule=''):
    """Update all of the submodules in the aggregate repository.

    Optional arguments:
    submodule -- the submodule to update
    """
    subprocess.call(['git', 'submodule', 'update', submodule])
