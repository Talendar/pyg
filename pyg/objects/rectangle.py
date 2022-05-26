""" Implements a graphic object representing a rectangle.
"""

from __future__ import annotations
from typing import Optional

import numpy as np

from pyg.objects.simple_graphic_object import SimpleGraphicObject
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.enums.fill_mode import FillMode
from pyg.utils import Coord2D, Coord3D, Color


class Rectangle(SimpleGraphicObject):
    """ Graphic object representing a rectangle. """

    def __init__(self,
                 top_left: Coord2D | Coord3D | np.ndarray,
                 size: tuple[float, float] | np.ndarray,
                 color: Optional[Color | np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL) -> None:
        """ Instantiates a new rectangle.

        Args:
            top_left: The coordinates of the rectangle's top-left vertex.
            size: The rectangle's width and height relative to, respectively,
                the window's width and height. Example: passing (0.5, 0.5) to
                this parameter will draw a rectangle with width and height equal
                to, respectively, half of the window's width and height.
            color: The rectangle's color. If not provided, a default color will
                be used.
            fill_mode: Specifies how the object should be filled.
        """
        size = np.array(size) * 2
        top_left = np.array(top_left, dtype=np.float32)
        other_vertices = np.array([
            (top_left[0], top_left[1] - size[1]),  # bottom-left
            (top_left[0] + size[0], top_left[1]),  # top-right
            (top_left[0] + size[0], top_left[1] - size[1]),  # bottom-right
        ], dtype=np.float32)

        if len(top_left) == 3:
            other_vertices = np.hstack([
                other_vertices,
                np.full([other_vertices.shape[0], 1],
                        top_left[-1],
                        dtype=np.float32),
            ])

        super().__init__(
            vertices=np.vstack([top_left, other_vertices]),
            primitive=PrimitiveShape.TRIANGLE_STRIP,
            color=color,
            fill_mode=fill_mode,
        )
