# Read version from installed package
from importlib.metadata import version
__version__ = version('covdrugsim')

# Populate package namespace
from covdrugsim.mdsim import mdAnalyse
from covdrugsim.qmcalc.unitConv.unitConv import exp_time
