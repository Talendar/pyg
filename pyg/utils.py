""" Utility types and functions.
"""

from __future__ import annotations

import abc
from typing import Optional

import numpy as np

from pyg.defaults import DEFAULT_COLOR


#: Represents a coordinate (x and y positions) in a plane.
Coord2D = tuple[float, float]

#: Represents a coordinate (x, y and z positions) in a 3D space.
Coord3D = tuple[float, float, float]

#: Represents a color (RGBA).
Color = tuple[float, float, float, float]


class Colored(abc.ABC):
    """ Represents a single-colored entity. """

    def __init__(self, color: Optional[Color | np.ndarray] = None):
        self.color = color

    @property
    def color(self) -> np.ndarray:
        """ NumPy array containing the RGBA values of the object's color. """
        return self._color

    @color.setter
    def color(self, new_color: Optional[Color | np.ndarray]) -> None:
        """ Sets the object's color.

        Args:
            new_color: Tuple or NumPy array with 4 floats specifying the RGBA
                values of the new color. If `None`, the object's color will be
                set to a default value.
        """
        if new_color is None:
            self._color = DEFAULT_COLOR
        else:
            new_color = np.array(new_color, dtype=np.float32)
            assert new_color.shape == (4,)
            self._color = new_color


def load_wavefront(pathname: str,
                   vertices_only: bool = False) -> dict | list[Coord3D]:
    """ Loads the contents of a Wavefront OBJ file. """
    material = None
    model = {"vertices": [], "texture": [], "faces": []}

    with open(pathname, "r") as file:
        for line in file:
            # Ignore comments.
            if line.startswith('#'):
                continue

            # Split the line on white spaces.
            values = line.split()
            if not values:
                continue

            # Extract vertices.
            if values[0] == "v":
                model["vertices"].append(values[1:4])
            # Extract texture coordinates.
            elif values[0] == "vt":
                model["texture"].append(values[1:3])
            # Extract faces.
            elif values[0] in ("usemtl", "usemat"):
                material = values[1]
            elif values[0] == "f":
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split("/")
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)
                model["faces"].append((face, face_texture, material))

    if not vertices_only:
        return model

    return [model["vertices"][vid - 1]
            for face in model["faces"] for vid in face[0]]
