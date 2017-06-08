from conda_tracker import modifier


def test_modify_patch_without_recipe(test_dir, test_repo):
    """Test that modify_patch correctly modifies the patch file."""
    modifier.modify_patch('0001-removed-readme.patch')

    with open('0001-removed-readme.patch') as patch_file:
        patch = patch_file.readlines()

    lines = []
    for line in patch:
        if 'a/' in line or 'b/' in line:
            lines.append(line)

    assert 'diff --git a/readme.txt b/readme.txt\n' in lines
    assert '--- a/readme.txt\n' in lines


def test_modify_patch_with_recipe_unnested(test_dir, test_repo):
    """Test that modify_patch correctly modifies the patch file.

    This function tests in an unnested directory hierarchy.
    """
    modifier.modify_patch('0001-removed-readme.patch', 'package', nested=False)

    with open('0001-removed-readme.patch') as patch_file:
        patch = patch_file.readlines()

    lines = []
    for line in patch:
        if 'a/' in line or 'b/' in line:
            lines.append(line)

    assert 'diff --git a/package/readme.txt b/package/readme.txt\n' in lines
    assert '--- a/package/readme.txt\n' in lines


def test_modify_patch_with_recipe_nested(test_dir, test_repo):
    """Test that modify_patch correctly modifies the patch file.

    This function tests in a nested directory hierarchy.
    """
    modifier.modify_patch('0001-removed-readme.patch', 'package', nested=True)

    with open('0001-removed-readme.patch') as patch_file:
        patch = patch_file.readlines()

    lines = []
    for line in patch:
        if 'a/' in line or 'b/' in line:
            lines.append(line)

    assert 'diff --git a/package/package/readme.txt b/package/package/readme.txt\n' in lines
    assert '--- a/package/package/readme.txt\n' in lines
