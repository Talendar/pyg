""" Implements a graphic object representing a dot.
"""

from __future__ import annotations
from typing import Optional, Any

import numpy as np
import OpenGL.GL as gl

from pyg.objects.simple_graphic_object import SimpleGraphicObject
from pyg.enums.fill_mode import FillMode
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.utils import Coord2D, Coord3D, Color


class Dot(SimpleGraphicObject):
    """ Graphic object representing a dot.

    Wraps OpenGL's "POINTS" primitive.
    """

    def __init__(self,
                 pos: Coord2D | Coord3D | np.ndarray,
                 size: int = 1,
                 color: Optional[Color | np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL) -> None:
        """ Instantiates a new dot.

        Args:
            pos: The dot's coordinates.
            size: The dot's size. It will be capped at a maximum size specified
                by the current OpenGL's implementation.
            color: The point's color. If not provided, a default color will be
                used.
            fill_mode: Specifies how the object should be filled.
        """
        self._size = size
        super().__init__(
            vertices=[pos],
            primitive=PrimitiveShape.POINTS,
            color=color,
            fill_mode=fill_mode,
        )

    def draw(self, color_loc: Any) -> None:
        gl.glPointSize(self._size)
        super().draw(color_loc)
