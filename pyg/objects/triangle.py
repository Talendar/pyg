""" Implements a graphic object representing a triangle.
"""

from __future__ import annotations
from typing import Optional

import numpy as np

from pyg.objects.graphic_object import GraphicObject
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.enums.fill_mode import FillMode
from pyg.utils import Coord2D, Coord3D, Color


class Triangle(GraphicObject):
    """ Graphic object representing a triangle.

    Wraps OpenGL's "TRIANGLES" primitive.
    """

    def __init__(self,
                 vertices: (tuple[Coord2D, Coord2D, Coord2D] |
                            tuple[Coord3D, Coord3D, Coord3D] |
                            np.ndarray),
                 color: Optional[Color | np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL) -> None:
        """ Instantiates a new triangle.

        Args:
            vertices: The coordinates of the 3 vertices of the triangle.
            color: The triangle's color. If not provided, a default color will
                be used.
            fill_mode: Specifies how the object should be filled.
        """
        super().__init__(
            vertices=vertices,
            primitive=PrimitiveShape.TRIANGLES,
            fill_mode=fill_mode,
            color=color,
        )
