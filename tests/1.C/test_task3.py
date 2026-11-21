from vpython import vector, color, textures
import pytest

from tests.helpers.fake_objects import FakePend
import src.swinging as main

@pytest.mark.parametrize("theta1, omega1, theta2, omega2, r_param, dt, g, \
                         expected_omega1, expected_theta1, expected_omega2, \
                         expected_theta2, expected_bob_pos1, expected_bob_pos2, \
                         expected_axis_pos1, expected_axis_pos2", [
    # base case
    (0, 0, 0, 0, 100, 0.01, 0, 0.0, 0.0, 0.0, 0.0, (0.0, -99.0, 0.0),
     (0.0, -98.0, 0.0), (0.0, -100.0, 0.0), (0.0, -100.0, 0.0)),

    (0.5, 1, 0.1, 0, 1, 1, 1, 0.520574461395797, 1.020574461395797,
     -0.09983341664682815, 0.0001665833531718508, (0.852409, 0.477124, 0.0),
     (0.000166583, 1.0, 0.0), (0.852409, -0.522876, 0.0), (0.000166583, -1.0, 0.0)),

    (0.1, 0.2, 0.3, 0.4, 1, 0.01, 9.81, 0.19020634182694618, 0.10190206341826946,
     0.3710094677265226, 0.30371009467726523,
     (0.10172579593859243, 0.005187523982203013, 0.0),
     (0.2990625534670365, 1.0457664913063596, 0.0),
     (0.10172579593859243, -0.994812476017797, 0.0),
     (0.2990625534670365, -0.9542335086936404, 0.0)),

    (6.28, 1, -6.28, 1, 1.5, 1, 10, 1.0212353452875866, 7.301235345287587,
     0.9787646547124134, -5.301235345287587,
     (1.2766287883935794, 0.21246019996146148, 0.0),
     (1.2473729454328544, 1.1668969241431375, 0.0),
     (1.2766287883935794, -0.7875398000385385, 0.0),
     (1.2473729454328544, -0.8331030758568625, 0.0)),

    (1.1, 0, 1.2, 0, 5, 0.001, 2, -0.00035648294402457415, 1.099999643517056,
     -0.00037281563438689054, 1.1999996271843656,
     (4.45603599181049, -1.2679821956288597, 0.0),
     (4.660194754372627, 0.18820949022304223, 0.0),
     (4.45603599181049, -2.2679821956288597, 0.0),
     (4.660194754372627, -1.8117905097769578, 0.0))
    ])

def test_full_swing_update(theta1, omega1, theta2, omega2, r_param, dt, g,
                           expected_omega1, expected_theta1, expected_omega2,
                           expected_theta2, expected_bob_pos1, expected_bob_pos2,
                           expected_axis_pos1, expected_axis_pos2):
    pend1 = {"objects": FakePend(vector(0, 1, 0), 1, theta1, color.white, textures.metal).pendulum,
             "theta": theta1, "omega": omega1}
    
    pend2 = {"objects": FakePend(vector(0, 2, 0), 1, theta2, color.cyan, textures.earth).pendulum,
             "theta": theta2, "omega": omega2}
    
    pend_list = [pend1, pend2]

    main.full_swing_update(pend_list, r_param, dt, g)
    
    assert pytest.approx(expected_omega1, rel=0.01) == pend1["omega"], (
        'omega should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_theta1, rel=0.01) == pend1["theta"], (
        'theta should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_omega2, rel=0.01) == pend2["omega"], (
        'omega should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_theta2, rel=0.01) == pend2["theta"], (
        'theta should be updated correctly for given arguments, not hardcoded arguments')
    
    bob_pos1 = pend1["objects"][1].pos
    assert pytest.approx(expected_bob_pos1[0], rel=0.01) == bob_pos1.x, (
        'bob position (x) should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_bob_pos1[1], rel=0.01) == bob_pos1.y, (
        'bob position (y) should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_bob_pos1[2], rel=0.01) == bob_pos1.z, (
        'bob position (z) should be updated correctly for given arguments, not hardcoded arguments')

    bob_pos2 = pend2["objects"][1].pos
    assert pytest.approx(expected_bob_pos2[0], rel=0.01) == bob_pos2.x, (
        'second bob position (x) should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_bob_pos2[1], rel=0.01) == bob_pos2.y, (
        'second bob position (y) should be updated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_bob_pos2[2], rel=0.01) == bob_pos2.z, (
        'second bob position (z) should be updated correctly for given arguments, not hardcoded arguments')

    axis_pos1 = pend1["objects"][2].axis
    assert pytest.approx(expected_axis_pos1[0], rel=0.01) == axis_pos1.x, (
        'cord axis (x) should be updated correctly with given parameters')
    assert pytest.approx(expected_axis_pos1[1], rel=0.01) == axis_pos1.y, (
        'cord axis (y) should be updated correctly with given parameters')
    assert pytest.approx(expected_axis_pos1[2], rel=0.01) == axis_pos1.z, (
        'cord axis (z) should be updated correctly with given parameters')
    
    axis_pos2 = pend2["objects"][2].axis
    assert  pytest.approx(expected_axis_pos2[0], rel=0.01) == axis_pos2.x, (
        'second cord axis (x) should be updated correctly with given parameters')
    assert pytest.approx(expected_axis_pos2[1], rel=0.01) == axis_pos2.y, (
        'second cord axis (y) should be updated correctly with given parameters')
    assert pytest.approx(expected_axis_pos2[2], rel=0.01) == axis_pos2.z, (
        'second cord axis (z) should be updated correctly with given parameters')