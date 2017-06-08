import os
import subprocess

import click

from conda_tracker import modifier


@click.group()
def cli():
    """Manage conda recipes."""


@cli.command()
@click.argument('recipe_url')
def add(recipe_url):
    """Add the given recipe to the repository.

    Positional arguments:
    recipe_url -- the url to the repository containing the conda recipe
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
    """Update the given recipe.

    Positional arguments:
    recipe -- the name of the recipe as given by the directory name

    Optional arguments:
    branch -- the name of the branch to pull from
    all_recipes -- update all recipes located in the directory
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
    """Apply the given patch to the corresponding recipe in the directory.

    Positional arguments:
    recipe -- the name of the recipe as given by the directory name
    patch_file -- the path to the patch file

    Optional arguments:
    remove -- delete the patch file from the directory
    """
    patch_file = modifier.modify_patch(patch_file, recipe)

    if remove:
        if click.confirm('Are you sure you want to remove {}?'.format(patch_file)):
            os.remove(patch_file)

    else:
        subprocess.call(['git', 'am', patch_file, '-3'])
