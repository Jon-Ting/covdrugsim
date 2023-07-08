from os import listdir
from os.path import exists, isdir, isfile
from shutil import rmtree

import numpy as np
from pytest import approx, fixture, mark

from covdrugsim.datasets import genExampleXYZs, getExampleEnergyLevellerInputPath, getExampleChargePath
from covdrugsim.qmcalc.constants import keywordDict
from covdrugsim.qmcalc.genScripts import genAllScripts
from covdrugsim.qmcalc.admin import groupFilesIntoDir
from covdrugsim.qmcalc.tabulate import writeToExcel
from covdrugsim.qmcalc.unitConv import energyUnitsConversion, eyringEquation, timeUnitsConversion
from covdrugsim.mdsim import mdAnalyse

targetDirPath = 'tests/exampleXYZs'
exampleXYZname = 'example1'
exampleXYZdirPath = f"{targetDirPath}/{exampleXYZname}"


def test_genExampleXYZs():
    """Unit test for genExampleXYZs()."""
    genExampleXYZs(targetDirPath)
    assert exists(targetDirPath), f"{targetDirPath} not found"
    assert isdir(targetDirPath), f"{targetDirPath} not a directory"
    assert len(listdir(targetDirPath)) == 3, f"Incorrect number of xyz files in {targetDirPath}"


def test_getExampleEnergyLevellerInputPath():
    """Unit test for genExampleEnergyLevellerInputPath()."""
    energyLevellerInputPathAct = getExampleEnergyLevellerInputPath()
    assert isinstance(energyLevellerInputPathAct, str), 'Path not a string'


def test_getExampleChargePath():
    """Unit test for genExampleChargePath()."""
    chargePathAct = getExampleChargePath()
    assert isinstance(chargePathAct, str), 'Path not a string'


def test_groupFilesIntoDir():
    """Unit test for groupFilesIntoDir()."""
    groupFilesIntoDir(targetDirPath)

    assert exists(exampleXYZdirPath), f"{exampleXYZdirPath} not found"
    assert isdir(exampleXYZdirPath), f"{exampleXYZdirPath} not a directory"

    assert exists(f"{exampleXYZdirPath}/{exampleXYZname}.xyz"), f"{exampleXYZname}.xyz not found"
    assert isfile(f"{exampleXYZdirPath}/{exampleXYZname}.xyz"), f"{exampleXYZname}.xyz not a file"

    assert len(listdir(targetDirPath)) == 3, f"Incorrect number of files in {exampleXYZdirPath}"

    if isdir(targetDirPath):
        rmtree(targetDirPath)


def test_genAllScripts():
    """Unit test for genAllScripts()."""
    genExampleXYZs(targetDirPath)
    genAllScripts(targetDirPath, verbose=True)
    assert exists(f"{exampleXYZdirPath}/{exampleXYZname}.xyz"), f"{exampleXYZname}.xyz not found"
    assert isfile(f"{exampleXYZdirPath}/{exampleXYZname}.xyz"), f"{exampleXYZname}.xyz not a file"
    assert exists(f"{exampleXYZdirPath}/{exampleXYZname}.inp"), f"{exampleXYZname}.inp not found"
    assert isfile(f"{exampleXYZdirPath}/{exampleXYZname}.inp"), f"{exampleXYZname}.inp not a file"
    assert exists(f"{exampleXYZdirPath}/{exampleXYZname}.sh"), f"{exampleXYZname}.sh not found"
    assert isfile(f"{exampleXYZdirPath}/{exampleXYZname}.sh"), f"{exampleXYZname}.sh not a file"
    if isdir(targetDirPath):
        rmtree(targetDirPath)


def test_energyUnitsConversion():
    assert energyUnitsConversion(100, None) == approx((100, 418.40000000000003))


#def test_vis():
#    assert exists('tests/outputs/betaCarbonCharges.png'), 'betaCarbonCharges.png not found'
#    assert isfile('tests/outputs/betaCarbonCharges.png'), 'betaCarbonCharges.png is not a file'
#    assert exists('tests/outputs/distortionInteractionAnalysis.png'), 'distortionInteractionAnalysis.png not found'
#    assert isfile('tests/outputs/distortionInteractionAnalysis.png'), 'distortionInteractionAnalysis.png is not a file'
#    assert exists('test/outputs/ligandLUMOenergy.png'), 'ligandLUMOenergy.png not found'
#    assert isfile('tests/outputs/ligandLUMOenergy.png'), 'ligandLUMOenergy.png is not a file'
#    assert exists('test/outputs/example.pdf'), 'example.pdf not found'
#    assert isfile('tests/outputs/example.pdf'), 'example.pdf is not a file'
#    if isdir('tests/outputs'):
#        rmtree('tests/outputs')

