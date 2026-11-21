import pytest
from vpython import vector, color, textures

import visualize_cradle_run as main
from tests.helpers.fake_objects import FakePend

@pytest.mark.parametrize("pos1, theta1, omega1, m1, e1, \
                            pos2, theta2, omega2, m2, e2, \
                            pos3, theta3, omega3, m3, e3, \
                            r_param, dt, g, \
                            exp_omega1, exp_theta1, \
                            exp_omega2, exp_theta2, \
                            exp_omega3, exp_theta3", [
    ((vector(1, 0, 0), 1, 0.5, 2, 1,
      vector(0, 0, 0), 2, 0.5, 3, 0,
      vector(1.05, 0, 0), 1, 0.5, 2.5, 1,
      1, 0.01, 9.81,
      0.41745169639034535, 1.0041745169639034,
      0.41079792242840063, 2.004107979224284,
      0.41745169639034535, 1.0041745169639034)),
    (vector(1, 0, 0), 1, 1.5, 2, 1,
     vector(1.1, 0, 0), 2, 1.5, 3, 1,
     vector(1.05, 0, 0), 1, 1.5, 4.5, 1,
     0.5, 0.01, 10,
     1.3317058030384206, 1.0133170580303843,
     1.3181405146348637, 2.013181405146349,
     1.3317058030384206, 1.0133170580303843),
    (vector(0.5, 0.3, 2.2), 0.5, 0.1, 2, 0,
     vector(0.7, 0.2, 2.5), 2.2, 0, 2, 0,
     vector(1, 0.1, 3.3), 3.1, 1, 2, 0,
     1.5, 0.001, 5,
     0.09840191487131933, 0.5000984019148713,
     -0.002694988012731967, 2.1999973050119874,
     0.999861397791889, 3.100999861397792)
])

def test_newton_cradle_tick(pos1, theta1, omega1, m1, e1,
                            pos2, theta2, omega2, m2, e2,
                            pos3, theta3, omega3, m3, e3,
                            r_param, dt, g,
                            exp_omega1, exp_theta1,
                            exp_omega2, exp_theta2,
                            exp_omega3, exp_theta3):
    pend1 = {
            "objects": FakePend(pos1, r_param, theta1, color.white, textures.metal).pendulum,
            "theta": theta1, "omega": omega1, "mass": m1, "restitution_coeff": e1}
    
    pend2 = {
            "objects": FakePend(pos2, r_param, theta1, color.white, textures.metal).pendulum,
            "theta": theta2, "omega": omega2, "mass": m2, "restitution_coeff": e2
        }
    
    pend3 = {
            "objects": FakePend(pos3, r_param, theta1, color.white, textures.metal).pendulum,
            "theta": theta3, "omega": omega3, "mass": m3, "restitution_coeff": e3
        }

    pend_list = [pend1, pend2, pend3]

    main.newton_cradle_tick(pend_list, r_param, dt, g)
    assert pytest.approx(exp_omega1, rel=0.01) == pend1["omega"], (
        'first omega should be correctly updated as per dt tick')
    assert pytest.approx(exp_omega2, rel=0.01) == pend2["omega"], (
        'second omega should be correctly updated as per dt tick')
    assert pytest.approx(exp_omega3, rel=0.01) == pend3["omega"], (
        'third omega should be correctly updated as per dt tick')

    assert pytest.approx(exp_theta1, rel=0.01) == pend1["theta"], (
        'first theta should be correctly updated as per dt tick')
    assert pytest.approx(exp_theta2, rel=0.01) == pend2["theta"], (
        'second theta should be correctly updated as per dt tick')
    assert pytest.approx(exp_theta3, rel=0.01) == pend3["theta"], (
        'third theta should be correctly updated as per dt tick')
