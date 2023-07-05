from importlib.resources import files


def getExampleChargePath():
    """Get path to chargesExample.txt.

    Returns
    -------
    str
        Path to file.
    """
    return str(files('covdrugsim.data').joinpath('chargesExample.txt'))


def getExampleEnergyLevellerInputPath():
    """Get path to energyLevellerExample.inp.

    Returns
    -------
    str
        Path to file.
    """
    return str(files('covdrugsim.data').joinpath('energyLevellerExample.inp'))

