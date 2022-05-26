""" Implements a graphic object representing a line.
"""

from __future__ import annotations
from typing import Optional, Any

import numpy as np
import OpenGL.GL as gl

from pyg.objects.simple_graphic_object import SimpleGraphicObject
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.utils import Coord2D, Coord3D, Color
from pyg.enums.fill_mode import FillMode


class Line(SimpleGraphicObject):
    """ Graphic object representing a line.

    Wraps OpenGL's "LINES" primitive.
    """

    def __init__(self,
                 pos: (tuple[Coord2D, Coord2D] |
                       tuple[Coord3D, Coord3D] |
                       np.ndarray),
                 line_width: int = 1,
                 color: Optional[Color | np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL) -> None:
        """ Instantiates a new line.

        Args:
            pos: Tuple or numpy array containing the coordinates of two points
                in the line.
            line_width: The width of the line. It will be capped at a maximum
                size specified by the current OpenGL's implementation.
            color: The line's color. If not provided, a default color will be
                used.
            fill_mode: Specifies how the object should be filled.
        """
        self._width = line_width
        super().__init__(
            vertices=pos,
            primitive=PrimitiveShape.LINES,
            color=color,
            fill_mode=fill_mode,
        )

    def draw(self, color_loc: Any) -> None:
        gl.glLineWidth(self._width)
        super().draw(color_loc)
