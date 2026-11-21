
from vpython import box, cylinder, sphere, vector
from pandas import DataFrame, read_csv
from typing import Any, TypedDict

VPythonColor = vector
VPythonTexture = str
Pendulum = tuple[box, sphere, cylinder]

class PendulumEntry(TypedDict):
    mass: float
    restitution_coeff: float
    color: str
    texture: str
    objects: Pendulum
    theta: float
    omega: float
    