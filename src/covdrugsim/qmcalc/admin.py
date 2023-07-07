from os import listdir, mkdir, rename
from os.path import isdir


def rmExtension(fileName):
    """Remove the extension of a file name."""
    if '.' in fileName:
        splitNames = fileName.split('.')
        newFileName = ''.join(splitNames[:-1])
    else:
        newFileName = fileName
    return newFileName


def makeDirForXYZs(dirPath):
    """Generate new directories with the same name as the existing xyz files"""
    xyzFiles = [f for f in listdir(dirPath) if not isdir(f"{dirPath}/{f}") and '.xyz' in f]
    for xyzFile in xyzFiles:
        mkdir(f"{dirPath}/{rmExtension(xyzFile)}")


def groupFilesIntoDir(dirPath, verbose=False):
    """Group files with same names (with extensions removed) into the same directories"""
    if verbose:
        print(f"\nGrouping molecules in {inputDirPath} into individual directory...")

    # Create a directory for each xyz file
    xyzDirs = [d for d in listdir(dirPath) if isdir(f"{dirPath}/{d}")]
    if len(xyzDirs) == 0:
        makeDirForXYZs(dirPath)
        xyzDirs = [d for d in listdir(dirPath) if isdir(f"{dirPath}/{d}")]

    # Move each file into the directory with the same name as the file with extension removed
    allFiles = [f for f in listdir(dirPath) if not isdir(f"{dirPath}/{f}")]
    for f in allFiles:
        filePath = f"{dirPath}/{f}"

        for xyzDir in xyzDirs:
            if rmExtension(f) == xyzDir:
                rename(filePath, filePath.replace(f"/{f}", f"/{xyzDir}/{f}"))


if __name__ == "__main__":
    inputDirPath = '/mnt/c/Users/ASUS/Documents/covdrugsim/src/covdrugsim/data/exampleXYZs'  # To be modified!
    groupFilesIntoDir(inputDirPath, verbose=True)


