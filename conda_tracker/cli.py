import os
import subprocess

import click

from conda_tracker import modifier


@click.group()
def cli():
    """Link git repositories and patches into an aggregate repository.


    conda-tracker includes multiple subcommands to assist in repo tracking:
    $  conda-tracker add [OPTIONS] RECIPE_URL
    $  conda-tracker update [OPTIONS] [RECIPE] [BRANCH]
    $  conda-tracker patch [OPTIONS] RECIPE PATCH_FILE

    To see more information regarding each subcommand, type:
    $ conda-tracker subcommand --help
    """


@cli.command()
@click.argument('recipe_url')
def add(recipe_url):
    """Add a repository to the aggregate repository.

    conda-tracker add requires the url of the repository as an argument.
    This url can be either a link to the repo on a git hosting service,
    or a git repository itself.

    Example:
    $ conda-tracker add https://github.com/conda/conda-tracker.git
    """
    recipe_name = recipe_url.rsplit('/', 1)[-1]

    # if recipe_url is a git repository, remove the .git ending
    recipe_name = recipe_name.replace('.git', '')

    recipe_subdir = '{0}/{0}' .format(recipe_name)

    subprocess.call(['git', 'subrepo', 'clone', recipe_url, recipe_subdir])


@cli.command()
@click.argument('recipe', required=False)
@click.argument('branch', required=False)
@click.option('--all-recipes', is_flag=True)
def update(recipe, branch, all_recipes):
    """Update a repository to a specific branch or to the master branch.

    conda-tracker update takes either the name of the repository or the
    --all-recipes command line flag. If the name of the repository is
    given a branch can also be given to update to a specific branch.

    Examples:
    $  conda-tracker update some_repository
    $  conda-tracker update some_repository some_branch
    $  conda-tracker update --all-recipes
    """
    cmd = ['git', 'subrepo', 'pull']

    if branch and recipe:
        cmd.extend([recipe, '-b', branch])

    elif recipe:
        cmd.append(recipe)

    elif all_recipes:
        cmd.append('--all')

    subprocess.call(cmd)


@cli.command()
@click.argument('recipe')
@click.argument('patch_file', type=click.Path(exists=True))
@click.option('--remove', is_flag=True)
def patch(recipe, patch_file, remove):
    """Apply a patch to the corresponding repository in the directory.

    conda-tracker patch requires as positional arguments the name of the
    repository to be patched as well as the file path to the patch file.
    Optionally, the --remove flag can be used to delete the patch file
    from the directory.

    Examples:
    $  conda-tracker my_sub_repository 0001-remove-file.patch
    $  conda-tracker my_sub_repository 0001-remove-file.patch --remove
    """
    patch_file = modifier.modify_patch(patch_file, recipe)

    if remove:
        if click.confirm('Are you sure you want to remove {}?'.format(patch_file)):
            os.remove(patch_file)

    else:
        subprocess.call(['git', 'am', patch_file, '-3'])
