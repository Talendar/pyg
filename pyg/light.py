""" Definition of a light source.
"""

from dataclasses import dataclass


@dataclass
class Light:
    """ Represents a light source. """

    pos: tuple[float, float, float] = (0, 0, 0)
    color: tuple[float, float, float] = (1, 1, 1)
    ambient_strength: float = 0.1
    diffuse_strength: float = 1
    specular_strength: float = 0.5
    specular_exponent: float = 32
