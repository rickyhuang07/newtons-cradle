import pytest
from vpython import vector, color, textures

import visualize_cradle_run as main
from tests.helpers.fake_objects import FakeBob

@pytest.mark.parametrize("pos1, omega1, m1, rad1, e1, \
                         pos2, omega2, m2, rad2, e2, \
                         expected_omega1, expected_omega2, \
                         reverse_expected_omega1, reverse_expected_omega2", [
    (vector(1,0,0), 1, 1, 0.5, 1,
     vector(0,0,0), 0.5, 2, 0.5, 0,
     0.3333333333333333, 0.8333333333333334,
     0.6666666666666666, 0.6666666666666666),
    (vector(1.05,0,0), 1, 1, 0.5, 1,
     vector(0,0,0), 0.5, 2, 0.5, 0,
     0.3333333333333333, 0.8333333333333334,
     0.6666666666666666, 0.6666666666666666),
    (vector(2, 1, 0.3), 0.1, 10, 1.5, 0.7,
     vector(0.5, 1.3, 0.7), 0.3, 2.7, 0.5,
     0.4, 0.17228346456692917, 0.03228346456692915,
     0.15952755905511815, 0.07952755905511813),
    # very close to condition - make sure your inequality is <= radius_sum * 1.05
    (vector(1.04, 0, 0), 1.4, 10, 0.25, 0.9,
     vector(0, 0, 0), 2.3, 2.7, 0.75, 0.1,
     1.7635433070866144, 0.9535433070866143,
     1.6104724409448818, 1.5204724409448822)
])
def test_handle_two_bobs_collision(pos1, omega1, m1, rad1, e1,
                         pos2, omega2, m2, rad2, e2,
                         expected_omega1, expected_omega2,
                         reverse_expected_omega1, reverse_expected_omega2):
    bob1 = FakeBob(pos1, rad1, color.white, textures.metal)
    pend1 = {
            "objects": (1, bob1, 1),
            "theta": 0.5, "omega": omega1, "mass": m1, "restitution_coeff": e1}
    
    bob2 = FakeBob(pos2, rad2, color.white, textures.metal)
    pend2 = {
            "objects": (1, bob2, 1),
            "theta": 0.1, "omega": omega2, "mass": m2, "restitution_coeff": e2
        }
    r1 = 1

    main.handle_two_bobs(pend1, pend2, r1)
    assert pytest.approx(expected_omega1, rel=0.01) == pend1["omega"], (
        'omega should change because collision should occur')
    assert pytest.approx(expected_omega2, rel=0.01) == pend2["omega"], (
        'second omega should change because collision should occur')

    # resetting the dictionary
    pend1["omega"] = omega1
    pend2["omega"] = omega2

    # here reverse is not necessarily symmetric because different e values
    main.handle_two_bobs(pend2, pend1, r1)
    assert pytest.approx(reverse_expected_omega1, rel=0.01) == pend1["omega"], (
        'the order of pendula in the collision matters because of the '
        'restitution coefficient chosen: make sure it is m1, m2')
    assert pytest.approx(reverse_expected_omega2, rel=0.01) == pend2["omega"], (
        'the order of pendula in the collision matters because of the '
        'restitution coefficient chosen: make sure it is m1, m2')


@pytest.mark.parametrize("omega1, omega2, rad1, rad2, pos1, pos2", [
    (1, 0.5, 0.5, 0.5, vector(1, 0, 0), vector(-1, 0, 0)),
    (2, 2.7, 0.3, 1, vector(1, 1.06, 2), vector(2, 1, 1)),
    (3, 3.25, 5, 3, vector(1, 7, 5), vector(7, 0.5, 3)),
    (0.1, 0.2, 0.69, 1.2, vector(-3.6, -2.7, -0.5), vector(-3, -4, -2))
])
def test_handle_two_bobs_no_collision(omega1, omega2, rad1, rad2, pos1, pos2):
    bob1 = FakeBob(pos1, rad1, color.white, textures.metal)
    pend1 = {
        "objects": (1, bob1, 1),
        "theta": 0.5, "omega": omega1, "mass": 1, "restitution_coeff": 1
    }

    bob2 = FakeBob(pos2, rad2, color.white, textures.metal)
    pend2 = {
        "objects": (1, bob2, 1),
        "theta": 0.1, "omega": omega2, "mass": 2, "restitution_coeff": 0
    }

    r1 = 1

    main.handle_two_bobs(pend1, pend2, r1)
    assert pytest.approx(omega1, rel=0.01) == pend1["omega"], (
        'omega should not change because no collision should occur')
    assert pytest.approx(omega2, rel=0.01) == pend2["omega"], (
        'second omega should not change because no collision should occur')

    # here reverse should be symmetric since there is no collision
    main.handle_two_bobs(pend2, pend1, r1)
    assert pytest.approx(omega1, rel=0.01) == pend1["omega"]
    assert pytest.approx(omega2, rel=0.01) == pend2["omega"]
