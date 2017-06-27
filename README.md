# conda-tracker

conda-tracker is a tool that links git repositories and patches into an aggregate 
repository. By grouping repositories and patches into a single repository, tasks
such as updating conda recipes prior to submitting to conda-concourse-ci become
much easier.

## Installation

To install conda-tracker with conda:

    $  conda install conda-tracker

To install conda-tracker from source:

    $  git clone https://github.com/conda/conda-tracker.git
    $  cd conda-tracker
    $  python setup.py install

## Usage

conda-tracker provides a CLI wrapped around a library. The CLI may be invoked
as follows:

    usage: conda-tracker [OPTIONS] COMMAND [ARGS]...
    
    commands:
      add           Add a repository to the aggregate repository
      patch         Apply a patch to the corresponding repository in the directory
      update        Update a repository to a specific branch or to the master branch
    
    positional arguments:
      repository    The repository to link to the aggregate repository
      branch        The specific branch to link to
      patch-file    The patch file to add to the linked repository
    
    optional arguments:
      all-recipes   Updates all linked repositories in the aggregate repository
      remove        Remove a patch file from the linked repository

conda-tracker may be imported as a module as well. An example follows:

```python
import conda_tracker


def add_many_repositories(list_of_repositories):
    for repository in list_of_repositories:
        conda_tracker.add_repository(repository)

```