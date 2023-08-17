"""
CovDrugSim Package
==================

Description

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided with the code, 
and a loose standing reference guide, available from 
`the CovDrugSim homepage <https://covdrugsim.readthedocs.io/en/latest/>`_.

Code snippets in docstrings are indicated by three greater-than signs::

  >>> x = 42
  >>> x = x + 1

Use the built-in ``help`` function to view a function's docstring::

  >>> import covdrugsim
  >>> help(covdrugsim.qmcalc.genScripts)
  ... # docstring: +SKIP

Utilities
---------
test (To be implemented)
    Run CovDrugSim tests.
__version__
    Return CovDrugSim version string.
"""
# Read version from installed package
from importlib.metadata import version
__version__ = version('covdrugsim')

# Populate package namespace
__all__ = ['mdsim', 'qmcalc']
from covdrugsim.datasets import genExampleXYZs, getExampleEnergyLevellerInputPath, getExampleChargePath
from covdrugsim.qmcalc.constants import keywordDict
from covdrugsim.qmcalc.genScripts import genAllScripts
from covdrugsim.qmcalc.admin import groupFilesIntoDir
from covdrugsim.qmcalc.tabulate import writeToExcel
from covdrugsim.qmcalc.unitConv import energyUnitsConversion, eyringEquation, timeUnitsConversion

from covdrugsim.mdsim import mdAnalyse
