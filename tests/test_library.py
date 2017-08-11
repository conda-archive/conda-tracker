import os

import git

from conda_tracker import library


def test_create_repository(tmpdir):
    library.create_aggregate_repository('test_aggregate_repo', tmpdir)
    aggregate_repository = os.path.join(tmpdir, 'test_aggregate_repo')

    assert os.path.isdir(aggregate_repository)
    assert git.repo.fun.is_git_dir(os.path.join(aggregate_repository, '.git'))


def test_access_github_api(capfd):
    response = library.access_github_api().get_api_status()

    assert response.status == 'good'


def test_retrieve_organization_repositories():
    repositories = library.retrieve_organization_repositories('conda')
    repository_names = [repository.name for repository in repositories]

    conda = ['conda', 'conda-build', 'conda-docs', 'conda-ui']

    assert all(repository in repository_names for repository in conda)


def test_add_submodules(tmpdir):
    library.create_aggregate_repository('test_aggregate_repo', tmpdir)
    aggregate_repository = os.path.join(tmpdir, 'test_aggregate_repo')
    aggregate_repository_repo = git.Repo(aggregate_repository)
    conda_repositories = library.retrieve_organization_repositories('conda')

    library.add_submodules(conda_repositories, aggregate_repository)

    conda = ['conda', 'conda-build', 'conda-docs', 'conda-ui']

    assert all(repository in os.listdir(aggregate_repository) for repository in conda)
    assert all((repository, 0) in aggregate_repository_repo.index.entries for repository in conda)
    assert not aggregate_repository_repo.is_dirty()
    assert len(aggregate_repository_repo.untracked_files) == 0
    assert aggregate_repository_repo.head.commit.message == 'Add submodules'


def test_update_submodules(tmpdir):
    library.create_aggregate_repository('test_aggregate_repo', tmpdir)
    aggregate_repository = os.path.join(tmpdir, 'test_aggregate_repo')
    aggregate_repository_repo = git.Repo(aggregate_repository)

    aggregate_repository_repo.create_submodule(name='conda-ui',
                                               path='conda-ui',
                                               url='https://github.com/conda/conda-ui.git')

    conda_ui_submodule = aggregate_repository_repo.submodules[0]
    conda_ui_path = os.path.join(aggregate_repository, conda_ui_submodule.name)

    conda_ui_git = git.Git(conda_ui_path)
    conda_ui_git.execute(['git', 'checkout', '9d6b31f0868fef1dc4f4e2e4b56df84f7729fc07'])
    aggregate_repository_git = git.Git(aggregate_repository)

    assert '9d6b31f0868fef1dc4f4e2e4b56df84f7729fc07' in aggregate_repository_git.execute(['git', 'submodule'])

    library.update_submodules(aggregate_repository)

    assert 'c272ad7f5a018495a8d60c05919c2ca396e7296f' in aggregate_repository_git.execute(['git', 'submodule'])


def test_gather_submodules(tmpdir):
    library.create_aggregate_repository('test_aggregate_repo', tmpdir)
    aggregate_repository = os.path.join(tmpdir, 'test_aggregate_repo')
    aggregate_repository_repo = git.Repo(aggregate_repository)

    aggregate_repository_repo.create_submodule(name='conda-ui',
                                               path='conda-ui',
                                               url='https://github.com/conda/conda-ui.git')

    conda = ['conda', 'conda-build', 'conda-docs']

    assert 'conda-ui' in os.listdir(aggregate_repository)
    assert not all(repository in os.listdir(aggregate_repository) for repository in conda)

    conda_repositories = library.retrieve_organization_repositories('conda')
    library.gather_submodules(conda_repositories, aggregate_repository)

    assert all(repository in os.listdir(aggregate_repository) for repository in conda)
