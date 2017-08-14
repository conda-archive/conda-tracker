import os
import shutil


def remove_submodule(repository, submodule):
    """Remove a submodule from a repository.

    Because git does not currently include a command to remove
    submodules, we have to edit the git files and remove the
    submodule directory ourselves.

    Parameters
    ----------
    repository: str
        the path to the aggregate directory
    submodule: str
        the name of the submodule to remove

    Returns
    -------
    None
    """
    submodule_path = os.path.join(os.path.abspath(repository), submodule)
    gitmodules_path = os.path.join(os.path.abspath(repository), '.gitmodules')
    config_path = os.path.join(os.path.abspath(repository), os.path.join('.git', 'config'))

    with open(gitmodules_path) as gitmodules_file:
        gitmodules = gitmodules_file.read().splitlines()

    with open(config_path) as config_file:
        config = config_file.read().splitlines()

    with open(gitmodules_path, 'w') as gitmodules_file:
        for line in gitmodules:
            if submodule not in line:
                gitmodules_file.write(line + '\n')

    with open(config_path, 'w') as config_file:
        for line in config:
            if submodule not in line:
                config_file.write(line + '\n')

    shutil.rmtree(submodule_path)
