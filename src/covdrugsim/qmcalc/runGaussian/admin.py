import os
from os.path import isdir


def makeDirForFiles(dirPath):
    """Generate new directories with the same name as the existing file"""
    fileList = [f for f in os.listdir(dirPath) if not isdir('{0}/{1}'.format(dirPath, f)) and '.xyz' in f]
    for i, file in enumerate(fileList):
        newDirPath = '{0}/{1}'.format(dirPath, rmExtension(file))
        os.mkdir(newDirPath)


def groupFiles(dirPath):
    """Group files with similar names (with extensions removed) into same directories"""
    group_list = [g for g in os.listdir(dirPath) if isdir('{0}/{1}'.format(dirPath, g))]
    if len(group_list) == 0:
        makeDirForFiles(dirPath)
        group_list = [g for g in os.listdir(dirPath) if isdir('{0}/{1}'.format(dirPath, g))]
    fileList = [f for f in os.listdir(dirPath) if not isdir('{0}/{1}'.format(dirPath, f))]
    for i, file in enumerate(fileList):
        filePath = '{0}/{1}'.format(dirPath, file)
        for j, group in enumerate(group_list):
            if rmExtension(file) == group:
                old_str, new_str = '/{0}'.format(file), '/{0}/{1}'.format(group, file)
                os.rename(filePath, filePath.replace(old_str, new_str))


def rmExtension(file_name):
    """Remove extension of a file name"""
    if '.' in file_name:
        split_names = file_name.split('.')
        newFileName = ''.join(split_names[:-1])
    else:
        newFileName = file_name
    return newFileName


if __name__ == "__main__":

    # Change this!
    inputDir = "/User/kahochow/Desktop/Li_mechanism/Li_work/Reactant"

    dircs = [f for f in os.listdir(inputDir) if isdir('{0}/{1}'.format(inputDir, f))]
    print("\n# Directory:\n", inputDir)
    print("Grouping conformers into individual dir...")
    groupFiles(inputDir)


