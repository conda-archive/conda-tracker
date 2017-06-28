import os

import click

from conda_tracker import library


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
@click.argument('branch', default='master')
def add(recipe_url, branch):
    """Add a repository to the aggregate repository.

    conda-tracker add requires the url of the repository as an argument.
    This url can be either a link to the repo on a git hosting service,
    or a git repository itself.

    Example:
    $ conda-tracker add https://github.com/conda/conda-tracker.git
    """

    library.add_repository(recipe_url, branch, nested=True)


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
    library.update_repository(recipe, branch, all_recipes)


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
    if remove:
        if click.confirm('Are you sure you want to remove {}?'.format(patch_file)):
            try:
                os.remove(patch_file)
                print('{} successfully removed.' .format(patch_file))
            except OSError:
                print('Unable to remove {}.' .format(patch_file))

    else:
        library.patch_repository(recipe, patch_file, nested=True)
