"""
Helper functions to make a pendulum.
"""

from vpython import (  # type: ignore
    box,  # type: ignore
    color,  # type: ignore
    cos,  # type: ignore
    cylinder,  # type: ignore
    vector,  # type: ignore
    sin,  # type: ignore
    sphere,  # type: ignore
    textures,  # type: ignore
)

from support.types import Pendulum, VPythonColor, VPythonTexture


def make_objects_of_pendulum(axle_pos: vector,
                  r_param: float,
                  theta: float,
                  bob_color: VPythonColor = color.white,
                  bob_texture: VPythonTexture = textures.metal,
                  ) -> Pendulum:
    """
    Builds a pendulum with a bob, axle and cord. 
    
    Args:
        axle_pos (VPython vector): position of center of axle
        r_param (float): size parameter used to define pendulum components
        theta (float); angle of the bob with respect to the axle
        bob_color (optional, VPython color): color of bob, defaults to white
        bob_texture (optional, VPython texture): texture of bob, defaults to wood

    Returns:
        (VPython box, VPython sphere, VPython cylinder): pendulum axle, bob, cord
    """
    axle = make_axle(axle_pos, r_param)

    bob_pos = axle.pos + r_param * vector(sin(theta), -cos(theta), 0)
    bob = make_bob(bob_pos, r_param, bob_color, bob_texture)
    
    cord_axis = bob.pos - axle.pos
    cord = make_cord(axle.pos, cord_axis, r_param)

    return axle, bob, cord


def make_bob(bob_pos: vector,
             r_param: float,
             clr: VPythonColor,
             texture: VPythonTexture,
             ) -> sphere:
    """
    Makes a spherical bob for the pendulum given certain parameters. 

    Args:
        bob_pos (VPython vector): position of center of bob
        r_param (float): size parameter used to define pendulum components
        clr (VPython color): color of bob
        texture (VPython texture): texture of bob

    Returns:
        (VPython sphere): sphere representing pendulum bob
    """
    return sphere(pos=bob_pos, radius=r_param/15, color=clr,
                texture=texture)


def make_axle(axle_pos: vector,
              r_param: float,
              clr: VPythonColor = color.green,
              ) -> box:
    """
    Makes a cuboidal axle/support for the pendulum given certain parameters. 

    Args:
        axle_pos (VPython vector): position of center of axle
        r_param (float): size parameter used to define pendulum components
        clr (optional, VPython color): color of axle, defaults to green

    Returns:
        (VPython box): box representing pendulum axle
    """
    return box(pos=axle_pos, size=vector(r_param/2, r_param/9, r_param/2), 
                color=clr, texture=textures.wood)


def make_cord(cord_pos: vector,
              axis: vector,
              r_param: float,
              clr: VPythonColor = color.white,
              ) -> cylinder:
    """
    Makes a cylindrical cord/string for the pendulum given certain parameters. 

    Args:
        cord_pos (VPython vector): position of center of cord
        axis (VPython vector): orientation of cord
        r_param (float): size parameter used to define pendulum components
        clr (optional, VPython color): color of cord, defaults to white

    Returns:
        (VPython cylinder): cylinder representing pendulum cord
    """
    return cylinder(pos=cord_pos, axis=axis, radius=r_param/50, color=clr)
