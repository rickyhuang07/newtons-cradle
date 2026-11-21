"""
Constants required for a Newton's cradle simulation.
"""
from vpython import color, pi, textures, vector  # type: ignore

from support.types import VPythonColor, VPythonTexture

import pandas as pd

GRAV: float = 9.81  # gravitational acceleration in m/s^2
R: float = 0.2  # cord length in meters, functions as size parameter for whole system
THETA_INIT: float = -30 * pi / 180  # initial angle of 1st pendulum in radians

DT: float = 0.005  # timestep (between 0.000005 [slo-mo] and 0.01 [normal])

DF1_FP = "support/DF1.csv"
DF2_FP = "support/DF2.csv"
DF3_FP = "support/DF3.csv"
NC_FP = "src/newton_cradle_pends.csv"

# Define color and texture dictionaries that map strings -> VPython attributes
COLOR_MAP: dict[str, VPythonColor] = {
    "red": color.red,
    "green": color.green,
    "blue": color.blue,
    "yellow": color.yellow,
    "orange": color.orange,
    "cyan": color.cyan,
    "magenta": color.magenta,
    "white": color.white,
    "black": color.black,
    "gray": color.gray(0.5),  # type: ignore
}

TEXTURE_MAP: dict[str, VPythonTexture] = {
    "earth": textures.earth,
    "flower": textures.flower,
    "granite": textures.granite,
    "gravel": textures.gravel,
    "metal": textures.metal,
    "rock": textures.rock,
    "rough": textures.rough,
    "rug": textures.rug,
    "stones": textures.stones,
    "stucco": textures.stucco,
    "wood": textures.wood,
    "wood_old": textures.wood_old,
}