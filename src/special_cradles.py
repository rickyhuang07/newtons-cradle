"""
Helper functions and implementation of a Newton's cradle simulation.
"""


from src.pds_helper import extract_and_convert
from vpython import vector  # type: ignore
from support.constants import *
from support.pendulum import make_objects_of_pendulum  # type: ignore
from support.types import PendulumEntry
MASS = "mass"
RES = "restitution_coeff"
THETA = "theta"
OMEGA = "omega"
COLOR = "color"
TEXTURE = "texture"
OBJECTS = "objects"


def uniform_mass_newton_cradle(relative_filepath: str,
                               mass: float) -> list[PendulumEntry]:
    """
    Creates a list of pendula and updates them to have the same mass.

    Args:
        relative_filepath (str): filepath to access CSV with pendula data
        mass (float): mass to be uniformly applied to each pendulum

    Returns:
        (list[dict]): list of dictionaries, each dictionary corresponding to
        a pendulum, with keys as physical attributes
    """

    res = extract_and_convert(relative_filepath)
    for d in res:
        d[MASS] = mass
    return res


def uniform_e_newton_cradle(relative_filepath: str,
                            e_val: float) -> list[PendulumEntry]:
    """
    Creates a list of pendula and updates them to have the same coefficient of
    restitution.

    Args:
        relative_filepath (str): filepath to access CSV with pendula data
        e_val (float): coefficient of restitution to be uniformly applied to each
        pendulum

    Returns:
        (list[dict]): list of dictionaries, each dictionary corresponding to
        a pendulum, with keys as physical attributes
    """

    res = extract_and_convert(relative_filepath)
    for d in res:
        d[RES] = e_val
    return res


def elastic_newton_cradle(relative_filepath: str) -> list[PendulumEntry]:
    """
    Creates a list of pendula and updates them to have perfectly elastic
    collisions with each other.

    Args:
        relative_filepath (str): filepath to access CSV with pendula data

    Returns:
        (list[dict]): list of dictionaries, each dictionary corresponding to
        a pendulum, with keys as physical attributes
    """

    return uniform_e_newton_cradle(relative_filepath, 1)


def inelastic_newton_cradle(relative_filepath: str) -> list[PendulumEntry]:
    """
    Creates a list of pendula and updates them to have perfectly inelastic
    collisions with each other.

    Args:
        relative_filepath (str): filepath to access CSV with pendula data

    Returns:
        (list[dict]): list of dictionaries, each dictionary corresponding to
        a pendulum, with keys as physical attributes
    """
    return uniform_e_newton_cradle(relative_filepath, 0)


CONST1 = -0.1
CONST2 = 4
CONST3 = 5


def make_newton_cradle(relative_filepath: str,
                       r_param: float,
                       theta_init: float) -> list[PendulumEntry]:
    """
    Uses information from a specific CSV file to make a list of
    dictionaries representing each pendula and their physical attributes.

    Args:
        relative_filepath (str): relative filepath of the CSV file
        r_param (float): size parameter used to define pendulum components
        theta_init (float): initial angle of the first pendulum (in radians)

    Returns:
        (list[dict]): list of dictionaries, each dictionary corresponding
        to each pendulum, with keys representing physical attributes
    """

    pend_list = extract_and_convert(relative_filepath)
    for i in range(len(pend_list)):
        if i == 0:
            pend_list[i][THETA] = theta_init
        else:
            pend_list[i][THETA] = 0
        pend_list[i][OMEGA] = 0
        axle_pos = vector((CONST1 + r_param / CONST2 * i), r_param / CONST3, 0)
        pend_list[i][OBJECTS] = make_objects_of_pendulum(
            axle_pos, r_param, pend_list[i][THETA], COLOR_MAP[pend_list[i][COLOR]], TEXTURE_MAP[pend_list[i][TEXTURE]])
    return pend_list
