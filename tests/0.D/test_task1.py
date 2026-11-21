
import subprocess
import sys
import pandas as pd

try:
    from vpython import box, cylinder, pi, sphere
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'vpython'])
finally:
    from vpython import box, cylinder, pi, sphere

import pytest

from support.constants import DF1_FP, DF2_FP, DF3_FP, NC_FP, R, THETA_INIT
from tests.helpers.constants_for_testing import VPYTHON_COLOR_MAP

from src.pds_helper import extract_and_convert

import src.special_cradles as main

@pytest.mark.parametrize(
    "filepath", 
    [DF1_FP, DF2_FP, DF3_FP, NC_FP]
    )
def test_extract_and_convert(filepath):
    pend_list = pd.DataFrame.from_dict(extract_and_convert(filepath))
    correct_pend_list = pd.DataFrame.from_dict(pd.read_csv(filepath).to_dict(orient="index"), orient="index")
    assert correct_pend_list.size == pend_list.size, 'Size of lists are not the same'
    assert pd.DataFrame.equals(pend_list, correct_pend_list), 'Values in list are not equal'

@pytest.mark.parametrize(
    "mass", 
    [(5), (2), (1)]
    )
def test_uniform_mass_newton_cradle(mass):
    pend_list = main.uniform_mass_newton_cradle(DF1_FP, mass)
    for pend in pend_list:
        assert mass == float(pend["mass"]), 'all masses must be the same'


@pytest.mark.parametrize(
    "e", 
    [(0.3), (0.5), (0.8)]
    )
def test_uniform_e_newton_cradle(e):
    pend_list = main.uniform_e_newton_cradle(DF1_FP, e)
    for pend in pend_list:
        assert e == float(pend["restitution_coeff"]), 'all restitution coefficients must be the same'


def test_elastic_newton_cradle():
    pend_list = main.elastic_newton_cradle(DF1_FP)
    for pend in pend_list:
        assert 1 == float(pend["restitution_coeff"]), (
            'all restitution coefficients should be elastic')
        

def test_inelastic_newton_cradle():
    pend_list = main.inelastic_newton_cradle(DF1_FP)
    for pend in pend_list:
        assert 0 == float(pend["restitution_coeff"]), (
            'all restitution coefficients should be inelastic')


def test_make_newton_cradle_pendulum():
    pend_list = main.make_newton_cradle(NC_FP, R, THETA_INIT)
    for pend in pend_list:
        pendulum = pend["objects"]
        assert isinstance(pendulum[0], box), 'axle should be a box'
        assert isinstance(pendulum[1], sphere), 'bob should be a sphere'
        assert isinstance(pendulum[2], cylinder), 'cord should be a string'


def test_make_newton_cradle_attributes():
    pend_data = main.make_newton_cradle(NC_FP, 0.4, -20 * pi / 180)
    pend_correct = extract_and_convert(NC_FP)

    for i in range(len(pend_correct)):
        pend_dict = pend_data[i]
        sheet_pend_dict = pend_data[i]

        bob = pend_dict["objects"][1]
        assert VPYTHON_COLOR_MAP[sheet_pend_dict["color"]
                                 ] == bob.color, 'bob color should not be modified'
        
        texture = sheet_pend_dict["texture"]
        assert f":{texture}_texture.jpg" == bob.texture, 'bob texture should not be modified'

        axle_pos = pend_dict["objects"][0].pos
        assert pytest.approx(0.1 * i - 0.1, rel=0.01) == axle_pos.x, (
            'axle position calculation should be correct')
        assert pytest.approx(0.08, rel=0.01) == axle_pos.y, (
            'axle position calculation should be correct')
        assert pytest.approx(0.0, rel=0.01) == axle_pos.z, (
            'axle position calculation should be correct')

        assert (-20 * pi / 180 if i == 0 else 0) == pend_dict["theta"], (
            'theta should be initialised to theta_init only for the first pendulum, and 0 for the others')
        assert 0 == pend_dict["omega"], 'omega should be initialised to 0 for all pendula'

        assert sheet_pend_dict["mass"] == pend_dict["mass"], 'mass should not be modified'
        assert sheet_pend_dict["restitution_coeff"] == pend_dict["restitution_coeff"], (
             'restitution coefficient should not be modified')