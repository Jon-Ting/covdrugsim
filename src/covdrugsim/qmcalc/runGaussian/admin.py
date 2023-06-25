import os
from os.path import isdir


def make_dir_for_files(dir_path):
    """Generate new directories with the same name as the existing file"""
    file_list = [f for f in os.listdir(dir_path) if not isdir('{0}/{1}'.format(dir_path, f)) and '.xyz' in f]
    for i, file in enumerate(file_list):
        new_dir_path = '{0}/{1}'.format(dir_path, rid_ext(file))
        os.mkdir(new_dir_path)


def group_files(dir_path):
    """Group files with similar names (with extensions removed) into same directories"""
    group_list = [g for g in os.listdir(dir_path) if isdir('{0}/{1}'.format(dir_path, g))]
    if len(group_list) == 0:
        make_dir_for_files(dir_path)
        group_list = [g for g in os.listdir(dir_path) if isdir('{0}/{1}'.format(dir_path, g))]
    file_list = [f for f in os.listdir(dir_path) if not isdir('{0}/{1}'.format(dir_path, f))]
    for i, file in enumerate(file_list):
        file_path = '{0}/{1}'.format(dir_path, file)
        for j, group in enumerate(group_list):
            if rid_ext(file) == group:
                old_str, new_str = '/{0}'.format(file), '/{0}/{1}'.format(group, file)
                os.rename(file_path, file_path.replace(old_str, new_str))


def rid_ext(file_name):
    """Remove extension of a file name"""
    if '.' in file_name:
        split_names = file_name.split('.')
        new_file_name = ''.join(split_names[:-1])
    else:
        new_file_name = file_name
    return new_file_name


if __name__ == "__main__":

    # Change this!
    input_dir = "/User/kahochow/Desktop/Li_mechanism/Li_work/Reactant"

    dircs = [f for f in os.listdir(input_dir) if isdir('{0}/{1}'.format(input_dir, f))]
    print("\n# Directory:\n", input_dir)
    print("Grouping conformers into individual dir...")
    group_files(input_dir)


