import click

from conda_tracker import library


@click.group()
def cli():
    """Link git repositories and patches into an aggregate repository.


    conda-tracker includes multiple subcommands to assist in repo tracking:
    \b $  conda-tracker create REPOSITORY

    \b $  conda-tracker add ORGANIZATION REPOSITORY

    \b $  conda-tracker update REPOSITORY

    \b $  conda-tracker gather ORGANIZATION REPOSITORY

    \b $  conda-tracker submit REPOSITORY

    To see more information regarding each subcommand, type:
    $ conda-tracker subcommand --help
    """


@cli.command()
@click.argument('repository_name')
def create(repository_name):
    """Create an aggregate repository that will house all submodules.

    Example:
    $  conda-tracker create aggregate_repo
    """
    library.create_aggregate_repository(repository_name)


@cli.command()
@click.argument('organization')
@click.argument('aggregate_repository')
@click.argument('token', required=False, default=None)
@click.option('--refine', default='')
def add(organization, aggregate_repository, token, refine):
    """Add all of the repositories of an organization into the aggregate repository.

    Example:
    $  conda-tracker add conda my_aggregate_repo
    """
    organization_repositories = library.retrieve_organization_repositories(organization, token)
    library.add_submodules(organization_repositories, aggregate_repository, refine)


@cli.command()
@click.argument('repository')
def update(repository):
    """Update all submodules inside the given aggregate repository.

    Example:
    $  conda-tracker update
    """
    library.update_submodules(repository)


@cli.command()
@click.argument('organization')
@click.argument('aggregate_repository')
@click.argument('token', required=False, default=None)
def gather(organization, aggregate_repository, token):
    """Gather new organization repositories into an aggregate repository.

    Example:
    $  conda-tracker gather conda my_aggregate_repository
    """
    organization_repositories = library.retrieve_organization_repositories(organization, token)
    library.gather_submodules(organization_repositories, aggregate_repository)


@cli.command()
@click.argument('aggregate_repository')
def submit(aggregate_repository):
    """Submit all changes to the origin remote.

    Example:
    $  conda-tracker submit my_aggregate_repository
    """
    library.submit_submodules(aggregate_repository)
