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


def makeDirForXYZs(inpDirPath, verbose=False):
    """Generate new directories with the same name as the existing xyz files"""
    if verbose:
        print(f"  Making directories for molecules in {inpDirPath}...")
    xyzFiles = [f for f in listdir(inpDirPath) if not isdir(f"{inpDirPath}/{f}") and '.xyz' in f]
    for xyzFile in xyzFiles:
        if verbose:
            print(f"    Making directory for {xyzFile}...")
        mkdir(f"{inpDirPath}/{rmExtension(xyzFile)}")
        if verbose:
            print(f"      Made directory for {xyzFile}!")
    if verbose:
        print(f"  DONE -- Made all directories!\n")


def groupFilesIntoDir(inpDirPath, verbose=False):
    """Group files with same names (with extensions removed) into the same directories"""
    if verbose:
        print(f"\nGrouping molecules in {inpDirPath} into individual directory...")

    # Make sure a directory is created for each xyz file
    xyzDirs = [d for d in listdir(inpDirPath) if isdir(f"{inpDirPath}/{d}")]
    if len(xyzDirs) == 0:
        makeDirForXYZs(inpDirPath, verbose=verbose)
        xyzDirs = [d for d in listdir(inpDirPath) if isdir(f"{inpDirPath}/{d}")]

    # Move each file into the directory with the same name as the file with extension removed
    if verbose:
        print(f"  Moving molecules in {inpDirPath} into individual directory...")
    allFiles = [f for f in listdir(inpDirPath) if not isdir(f"{inpDirPath}/{f}")]
    for f in allFiles:
        if verbose:
            print(f"    Processing {f}...")
        filePath = f"{inpDirPath}/{f}"

        for xyzDir in xyzDirs:
            if rmExtension(f) == xyzDir:
                rename(filePath, filePath.replace(f"/{f}", f"/{xyzDir}/{f}"))
                if verbose:
                    print(f"      Moved {f} to {xyzDir}!")
    if verbose:
        print(f"  DONE -- Moved all files!\n")
        print(f"DONE -- Grouped all molecules!\n")


if __name__ == "__main__":
    # Debugging
    inpDirPath = '/mnt/c/Users/ASUS/Documents/covdrugsim/src/covdrugsim/data/exampleXYZs'
    # makeDirForXYZs(inpDirPath, verbose=True)
    groupFilesIntoDir(inpDirPath, verbose=True)

