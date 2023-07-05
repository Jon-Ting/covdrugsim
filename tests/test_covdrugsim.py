from os.path import exists, isdir, isfile
from shutil import rmtree

import numpy as np
from pytest import approx, fixture, mark

from covdrugsim.qmcalc.unitConv.unitConv import E_unit_conv


def test_E_unit_conv():
    assert E_unit_conv(100, None) == approx((100, 418.40000000000003))


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

