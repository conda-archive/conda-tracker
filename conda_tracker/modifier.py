def modify_patch(patch_file, recipe=None, nested=True):
    """Modify the contents of the patch file to find the subrepo.

    Positional arguments:
    recipe -- the name of the recipe as given by the directory name
    patch_file -- the path to the patch file

    Keyword arguments:
    nested -- whether or not the subrepo is nested inside its own package
    """
    if recipe is not None:
        if nested:
            subdir = '{0}/{0}/' .format(recipe)
        else:
            subdir = '{}/' .format(recipe)
    else:
        subdir = ''

    with open(patch_file, 'r') as file:
        patch = file.readlines()

    lines = []
    for line in patch:
        replacement_a = 'a/{}' .format(subdir)
        replacement_b = 'b/{}' .format(subdir)

        if 'a/' in line and replacement_a not in line:
            line = line.replace('a/', replacement_a)

        if 'b/' in line and replacement_b not in line:
            line = line.replace('b/', replacement_b)

        lines.append(line)

    with open(patch_file, 'w') as file:
        for line in lines:
            file.write(line)

    return patch_file