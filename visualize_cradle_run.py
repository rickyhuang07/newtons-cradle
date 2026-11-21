"""
Helper functions and implementation of a Newton's cradle simulation.
"""

from vpython import mag, scene, rate

from support.types import PendulumEntry
from support.constants import NC_FP, DT, GRAV, R, THETA_INIT
from src.pds_helper import write_to_csv
from src.special_cradles import uniform_mass_newton_cradle, uniform_e_newton_cradle, elastic_newton_cradle, inelastic_newton_cradle, make_newton_cradle
from src.swinging import full_swing_update

scene.title = "Newton's cradle"


def handle_collision(e: float,
                     omega1: float,
                     omega2: float,
                     m1: float,
                     m2: float,
                     r_param: float) -> tuple[float, float]:
    """
    In case two bobs collide, handles the physics (momentum conservation).

    Args:
        e (float): coefficient of restitution for collision
        omega1 (float): angular velocity of first pendulum
        omega2 (float): angular velocity of second pendulum
        m1 (float): mass of first pendulum
        m2 (float): mass of second pendulum
        r_param (float): size parameter used to define pendulum components

    Returns:
        (tuple[float, float]): post-collision omegas of 1st, 2nd pendula
    """

    v1 = omega1 * r_param
    v2 = omega2 * r_param
    v1new = (m1 * v1 + m2 * v2 - m2 * e * (v1 - v2)) / (m1 + m2)
    v2new = (m1 * v1 + m2 * v2 + m1 * e * (v1 - v2)) / (m1 + m2)
    omegaf1 = v1new / r_param
    omegaf2 = v2new / r_param
    return (omegaf1, omegaf2)


MASS = "mass"
OMEGA = "omega"
OBJECTS = "objects"
RES = "restitution_coeff"
CONST = 1.05


def handle_two_bobs(pend1: PendulumEntry,
                    pend2: PendulumEntry,
                    r_param: float) -> None:
    """
    Handles the collisions and updates of 2 pendula in the cradle.

    Args:
        pend1 (PendulumEntry): dictionary representing 1st pendulum, 
                        with keys as physical attributes
        pend2 (PendulumEntry): dictionary representing 2nd pendulum, 
                        with keys as physical attributes
        r_param (float): size parameter used to define pendulum components
    """
    m1 = pend1[MASS]
    av1 = pend1[OMEGA]
    bob1 = pend1[OBJECTS][1]
    m2 = pend2[MASS]
    av2 = pend2[OMEGA]
    bob2 = pend2[OBJECTS][1]
    e1 = pend1[RES]
    if mag(bob1.pos - bob2.pos) <= CONST * (bob1.radius + bob2.radius):
        new = handle_collision(e1, av1, av2, m1, m2, r_param)
        pend1[OMEGA] = new[0]
        pend2[OMEGA] = new[1]


def newton_cradle_tick(pend_list: list[PendulumEntry],
                       r_param: float,
                       dt: float,
                       g: float) -> None:
    """
    Performs one 'tick' of the entire Newton's cradle (propagates any
    motion throughout all the pendula).

    Args:
        pend_list (list[PendulumEntry]): list of pendulum dictionaries, 
                        with keys as physical attributes
        r_param (float): size parameter used to define pendulum components
        dt (float): time step of update
        g (float): gravitational acceleration
    """
    full_swing_update(pend_list, r_param, dt, g)
    for i in range(len(pend_list) - 1):
        handle_two_bobs(pend_list[i], pend_list[i + 1], r_param)


if __name__ == "__main__":
    pend_list = make_newton_cradle(NC_FP, R, THETA_INIT)

    done = False
    while not done:
        rate(1 / DT)  # The rate to be included in the animation

        newton_cradle_tick(pend_list, R, DT, GRAV)
