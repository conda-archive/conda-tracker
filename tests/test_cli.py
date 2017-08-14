import os

from click.testing import CliRunner

from conda_tracker.cli import cli


def test_cli_workflow():
    runner = CliRunner()

    with runner.isolated_filesystem():
        runner.invoke(cli, ['create', 'my_agg_repo'])

        assert 'my_agg_repo' in os.listdir()

        runner.invoke(cli, ['add', 'conda', 'my_agg_repo', '--refine=^conda.*$'])

        conda_refined_repos = ['conda', 'conda-build', 'conda-docs', 'conda-ui']
        conda_omitted_repos = ['constructor', 'cookiecutter-conda-python', 'ci_test',
                               'libconda', 'kapsel', 'site', 'build_infrastructure',
                               'PyCommunity']

        assert all(repository in os.listdir('my_agg_repo') for repository in conda_refined_repos)
        assert all(repository not in os.listdir('my_agg_repo') for repository in conda_omitted_repos)

        update = runner.invoke(cli, ['update', 'my_agg_repo', '--remote'])

        assert update.exit_code == 0

        gather = runner.invoke(cli, ['gather', 'conda', 'my_agg_repo'])

        assert gather.exit_code == 0
