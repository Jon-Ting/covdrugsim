"""
CovDrugSim
==========

Provides
    1. Representation of surface of 3D complex objects consisting of spherical entities as 

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
  >>> help(covdrugsim.qmcalc.unitConv.unitConv)
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
from covdrugsim.mdsim import mdAnalyse
from covdrugsim.qmcalc.unitConv.unitConv import exp_time
