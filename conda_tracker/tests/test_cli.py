import subprocess

from click.testing import CliRunner

from conda_tracker import cli


def repo_name(repository_url):
    return repository_url.rsplit('/', 1)[-1]


def test_add_cli(capfd, test_dir, test_repo):
    """Test the add subcommand of the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['add', test_repo])

    output, _ = capfd.readouterr()

    assert result.exit_code == 0

    assert "Subrepo '{0}' (master) cloned into '{1}/{1}'" .format(
        test_repo, repo_name(test_repo)) in output


def test_update_cli(capfd, test_dir, test_repo):
    """Test the update subcommand of the CLI."""
    subprocess.call(['git', 'subrepo', 'clone', test_repo])

    runner = CliRunner()
    result = runner.invoke(cli.cli, ['update', repo_name(test_repo)])

    output, _ = capfd.readouterr()

    assert result.exit_code == 0

    assert "Subrepo '{}' is up to date." .format(repo_name(test_repo)) in output


def test_update_cli_all_recipes(capfd, test_dir, test_repo, another_test_repo):
    """Test the update subcommand of the CLI."""
    subprocess.call(['git', 'subrepo', 'clone', test_repo])
    subprocess.call(['git', 'subrepo', 'clone', another_test_repo])

    runner = CliRunner()
    result = runner.invoke(cli.cli, ['update', '--all-recipes'])

    output, _ = capfd.readouterr()

    assert result.exit_code == 0

    assert "Subrepo '{}' is up to date." .format(repo_name(test_repo)) in output
    assert "Subrepo '{}' is up to date." .format(repo_name(another_test_repo)) in output


def test_patch_cli(test_subrepo):
    """Test the patch subcommand of the CLI."""

    runner = CliRunner()
    result = runner.invoke(cli.cli, ['patch', 'test_subrepo',
                                     '0001-removed-readme-file.patch'])

    assert result.exit_code == 0


def test_patch_cli_remove(test_subrepo):
    """Test the patch subcommand of the CLI."""

    runner = CliRunner()
    result = runner.invoke(cli.cli, ['patch', 'test_subrepo',
                                     '0001-removed-readme-file.patch',
                                     '--remove'], input='y')

    assert result.exit_code == 0
