# conda-tracker

[![Build Status](https://travis-ci.org/conda/conda-tracker.svg?branch=master)](https://travis-ci.org/conda/conda-tracker)

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

### Command Line Application

conda-tracker provides a CLI wrapped around a library. The CLI may be invoked
as follows:

    usage: conda-tracker [OPTIONS] COMMAND [ARGS]...
    
    commands:
      add           Add a repository to the aggregate repository
      update        Update a linked repository to the master branch
      patch         Apply a patch to the corresponding repository in the directory
    
    positional arguments:
      repository    The repository to link to the aggregate repository
      patch-file    The patch file to add to the linked repository
    
    optional arguments:
      branch        The specific branch to link to
      all-recipes   Updates all linked repositories in the aggregate repository
      remove        Remove a patch file from the linked repository

The `add` and `update` commands take a repository URL as a positional argument whereas
the `patch` command takes the file path to the patch file as a positional argument.

The `branch` optional argument may be used with either the `add` or `update` command,
the `all-recipes` optional argument may be used with the `update` command, and the
`remove` optional argument may be used with the `patch` command.

### Library

conda-tracker may be imported as a module as well. An example follows:

```python
import conda_tracker


def add_many_repositories(list_of_repositories):
    for repository in list_of_repositories:
        conda_tracker.add_repository(repository)

```

## Example 

First the aggregate repository must be a git initialized repository. Here we use
a directory named `aggregate`.

```bash
$  user:aggregate user$ git init
$  user:aggregate user$ touch README.rst
$  user:aggregate user$ echo "This is a README" >> README.rst
$  user:aggregate user$ git add README.rst
$  user:aggregate user$ git commit -m "Added an exciting README"
[master (root-commit) abcd1234] Added an exciting README
 1 file changed, 1 insertion(+)
 create mode 100644 README.rst
```

Next, let's add two repositories to our aggregate repository. Here we will be using
the attrs repository's master branch and the click repository's 6.x-maintenance branch:

```bash
$  user:aggregate user$ conda-tracker add https://github.com/python-attrs/attrs.git
Subrepo 'https://github.com/python-attrs/attrs.git' (master) cloned into 'attrs/attrs'.
  
$  user:aggregate user$ conda-tracker add https://github.com/pallets/click.git 6.x-maintenance
Subrepo 'https://github.com/pallets/click.git' (6.x-maintenance) cloned into 'click/click'.
```

If we want to update click to the master branch, all that's needed is:

```bash
$  user:aggregate user$ conda-tracker update click/click master
Subrepo 'click/click' pulled from 'https://github.com/pallets/click.git' (master).
```

Now, let's say we want to create a patch for one of the linked repositories. The linked
repository works in the same way as any git repository, and its changes will be tracked
by the aggregate repository.

```bash
$  user:aggregate user$ cd attrs/attrs
$  user:aggregate user$ git checkout -b new-branch
$  user:aggregate user$ rm -f tox.ini
$  user:aggregate user$ git add tox.ini 
$  user:aggregate user$ git commit -m "Removed tox.ini for some reason"
[new-branch abcd1234] Removed tox.ini for some reason
 1 file changed, 62 deletions(-)
 delete mode 100644 attrs/attrs/tox.ini
$  user:aggregate user$ git format-patch master
0001-Removed-tox.ini-for-some-reason.patch
```

If we change directories back to the aggregate repository and call git status, the
new patch in the linked repository will show as an untracked file in the aggregate repository:
```bash
$  user:aggregate user$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

  attrs/attrs/0001-Removed-tox.ini-for-some-reason.patch
```

We can remove the patch using the `remove` flag on the `patch` command:

```bash
$  user:aggregate user$ conda-tracker patch attrs --remove attrs/attrs/0001-Removed-tox.ini-for-some-reason.patch
Are you sure you want to remove attrs/attrs/0001-Removed-tox.ini-for-some-reason.patch? [y/N]: y
attrs/attrs/0001-Removed-tox.ini-for-some-reason.patch successfully removed.
```

conda-tracker also allows users to apply patches to the linked repositories:

```bash
$  user:aggregate user$ conda-tracker patch click click/0001-Remove-Makefile.patch 
Applying: Remove Makefile
```