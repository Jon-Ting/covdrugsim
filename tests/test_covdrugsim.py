import pytest
from covdrugsim.qmcalc.unitConv.unitConv import E_unit_conv


# TODO: More tests to be developed


def test_E_unit_conv():
    assert E_unit_conv(100, None) == pytest.approx((100, 418.40000000000003))


