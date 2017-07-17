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
def add(recipe_url):
    """Add a repository to the aggregate repository.

    conda-tracker add requires the url of the repository as an argument.
    This url can be either a link to the repo on a git hosting service,
    or a git repository itself.

    Example:
    $ conda-tracker add https://github.com/conda/conda-tracker.git
    """
    library.add_repository(recipe_url)


@cli.command()
@click.argument('recipe', required=False)
def update(recipe):
    """Update a repository to a specific branch or to the master branch.

    conda-tracker update takes either the name of the repository or the
    --all-recipes command line flag. If the name of the repository is
    given a branch can also be given to update to a specific branch.

    Examples:
    $  conda-tracker update
    $  conda-tracker update some_repository
    """
    library.update_repository(recipe)
