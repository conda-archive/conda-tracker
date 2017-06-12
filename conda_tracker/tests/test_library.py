from conda_tracker import library


def test_repository_name():
    """Test that repository_name correctly splits the suffix from a URL."""
    link = 'https://github.com/conda/conda-tracker'
    git_https_link = 'https://github.com/conda/conda-tracker.git'
    git_ssh_link = 'git@github.com:conda/conda-tracker.git'

    assert library.repository_name(link) == 'conda-tracker'
    assert library.repository_name(git_https_link) == 'conda-tracker'
    assert library.repository_name(git_ssh_link) == 'conda-tracker'


def test_add_repository(mock_call, test_repo, test_repo_name):
    """Test that add_repository is called correctly."""
    library.add_repository(test_repo)

    mock_call.assert_called_once_with(['git', 'subrepo', 'clone', test_repo,
                                       test_repo_name])

    library.add_repository(test_repo, nested=True)

    mock_call.assert_called_with(['git', 'subrepo', 'clone', test_repo,
                                  '{0}/{0}' .format(test_repo_name)])


def test_update_repository(mock_call, test_repo_name):
    """Test that update_repository is called correctly."""
    library.update_repository(test_repo_name)

    mock_call.assert_called_once_with(['git', 'subrepo', 'pull',
                                      test_repo_name])


def test_update_repository_branch(mock_call, test_repo_name):
    """Test that update_repository is called correctly when given a branch."""
    library.update_repository(test_repo_name, 'fix')

    mock_call.assert_called_once_with(['git', 'subrepo', 'pull',
                                       test_repo_name, '-b', 'fix'])


def test_update_repository_all(mock_call):
    """Test that update_repository is called correctly with the all flag."""
    library.update_repository(all_repositories=True)

    mock_call.assert_called_once_with(['git', 'subrepo', 'pull', '--all'])


def test_patch_repository(mock_call, mocker, test_repo_name):
    """Test that patch_repository is called correctly."""
    mock_patch = mocker.patch('conda_tracker.modifier.modify_patch')

    library.patch_repository('0001-some-file.patch', test_repo_name, False)

    mock_patch.assert_called_once_with(test_repo_name, '0001-some-file.patch',
                                       False)
