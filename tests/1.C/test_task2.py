import pytest

import src.swinging as main

# Test cases for the angle_update function
@pytest.mark.parametrize("omega, theta, r_param, dt, g, expected_omega, expected_theta", [
    (0, 0, 0.2, 0.1, 9.81, 0.0, 0.0),             # base case
    (0, 0.1, 1, 0.1, 9.81, -0.09793658173053843, 0.09020634182694616),    # omega 0, non-zero theta
    (1, 0, 0.2, 0.1, 9.81, 1.0, 0.1),             # theta 0, non-zero omega
    (1, 0.5, 2, 0.05, 9.81, 0.8824208866573192, 0.544121044332866),  # non-zero theta and omega
    (1, 0.5, 2, 0.05, 0.1, 0.9988014361534895, 0.5499400718076745),  # different g
    (1, 3.14, 0.2, 0.1, 0.5, 0.9996018367708783, 3.239960183677088),  
    (5, 6, 1, 1, 1, 5.279415498198926, 11.279415498198926)
])

def test_angle_update(omega, theta, r_param, dt, g, expected_omega, expected_theta):
    omega_new, theta_new = main.angle_update(omega, theta, r_param, dt, g)
    assert pytest.approx(expected_omega, rel=0.001) == omega_new, (
        'omega should be calculated correctly for given arguments, not hardcoded arguments')
    assert pytest.approx(expected_theta, rel=0.001) == theta_new, (
        'theta should be calculated correctly for given arguments, not hardcoded arguments')
