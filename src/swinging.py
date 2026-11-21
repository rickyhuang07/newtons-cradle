"""
Helper functions and implementation of a Newton's cradle simulation.
"""

from vpython import (  # type: ignore
    cos,  # type: ignore
    sin,  # type: ignore
    vector,  # type: ignore
)
from support.types import PendulumEntry


def angle_update(omega: float,
                 theta: float,
                 r_param: float,
                 dt: float,
                 g: float) -> tuple[float, float]:
    """
    Updates the angle and angular velocity of a pendulum system. 

    Args:
        omega (float): angular velocity of pendulum    
        theta (float): angle of pendulum 
        r_param (float): size parameter used to define pendulum components
        dt (float): time step of update
        g (float): gravitational acceleration

    Returns:
        (tuple[float, float]): time-updated omega, theta    
    """
    omegaf = omega + -g * sin(theta) * dt / r_param
    thetaf = theta + omegaf * dt
    return (omegaf, thetaf)


THETA = "theta"
OMEGA = "omega"
OBJECTS = "objects"


def swing_update(pend: PendulumEntry,
                 r_param: float,
                 dt: float,
                 g: float) -> None:
    """
    Updates the angle & position of the pendulum components in a single swing.

    Args:
        pend_dict (dict): represents attributes of the pendulum
        r_param (float): size parameter used to define pendulum components
        dt (float): time step of update
        g (float): gravitational acceleration
    """
    theta = pend[THETA]
    omega = pend[OMEGA]

    axle = pend[OBJECTS][0]
    bob = pend[OBJECTS][1]
    cord = pend[OBJECTS][2]
    temp = angle_update(omega, theta, r_param, dt, g)
    omega_new = temp[0]
    theta_new = temp[1]
    bob.pos = axle.pos + r_param * \
        vector(sin(theta_new), -cos(theta_new), 0)  # type: ignore
    cord.axis = bob.pos - axle.pos  # type: ignore

    pend[THETA] = theta_new
    pend[OMEGA] = omega_new


def full_swing_update(pend_list: list[PendulumEntry],
                      r_param: float,
                      dt: float,
                      g: float) -> None:
    """
    Updates the omegas for all the pendula in the cradle, updating each
    pendulum dictionary. 

    Args:
        pend_list (list): list of dictionaries, each dictionary representing a
                    pendulum, with keys as physical attributes
        r_param (float): size parameter used to define pendulum components
        dt (float): time step of update
        g (float): gravitational acceleration
    """
    for pend in pend_list:
        swing_update(pend, r_param, dt, g)
