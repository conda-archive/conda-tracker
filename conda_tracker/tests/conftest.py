import subprocess

import pytest


@pytest.fixture(scope='function')
def gitdir(tmpdir):
    """Create a git initialized directory for tests."""
    testdir = tmpdir.mkdir('test')
    testfile = testdir.join('readme.txt')

    testfile.write('This is a test.')
    testdir.chdir()

    # initialize a git repo and add a readme so the repo isn't empty
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', 'readme.txt'])
    subprocess.call(['git', 'commit', '-m', "'added readme'"])

    return testdir


@pytest.fixture(scope='function')
def test_dir(gitdir):
    """Create a git initialized directory for tests."""

    # create a branch and remove the readme in order to create a patch
    subprocess.call(['git', 'checkout', '-b', 'test_branch'])
    subprocess.call(['rm', 'readme.txt'])
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'removed readme'])
    subprocess.call(['git', 'format-patch', 'master'])
    subprocess.call(['git', 'checkout', 'master'])


@pytest.fixture(scope='function')
def test_subrepo(gitdir, another_test_repo):
    """Create a subrepo inside a repo and patch the subrepo."""

    repo_name = another_test_repo.rsplit('/', 1)[-1]

    subprocess.call(['git', 'clone', another_test_repo])
    subprocess.call(['git', 'subrepo', 'clone', another_test_repo,
                     'test_subrepo/test_subrepo/'])

    repodir = gitdir.join(repo_name)
    repodir.chdir()

    subprocess.call(['git', 'checkout', '-b', 'test_some_branch'])
    subprocess.call(['rm', 'README.md'])
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'removed readme file'])
    subprocess.call(['git', 'format-patch', 'master'])
    subprocess.call(['git', 'checkout', 'master'])

    patch_file = repodir.join('0001-removed-readme-file.patch')
    subrepodir = gitdir.join('test_subrepo')

    subprocess.call(['cp', str(patch_file), str(subrepodir)])

    subrepodir.chdir()


@pytest.fixture
def test_repo():
    return 'https://github.com/conda/conda-docs'


@pytest.fixture
def another_test_repo():
    return 'https://github.com/conda/cookiecutter-conda-python'
