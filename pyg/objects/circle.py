""" Implements a graphic object representing a circle.
"""

from __future__ import annotations
from typing import Optional

import numpy as np

from pyg.objects.graphic_object import GraphicObject
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.enums.fill_mode import FillMode
from pyg.utils import Coord2D, Coord3D, Color


class Circle(GraphicObject):
    """ Graphic object representing a circle. """

    def __init__(self,
                 center_pos: Coord2D | Coord3D | np.ndarray,
                 radius: float,
                 color: Optional[Color | np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL,
                 quality_level: int = 64) -> None:
        """ Instantiates a new circle.

        Args:
            center_pos: The coordinates of the circle's center.
            radius: The circle's radius.
            color: The circle's color. If not provided, a default color will be
                used.
            fill_mode: Specifies how the object should be filled.
            quality_level: An integer related to the quality of the drawn
                circle. Greater values mean higher quality.
        """
        vertices = []
        inc = 2 * np.pi / quality_level
        for i in range(quality_level):
            angle = i * inc
            x = np.cos(angle) * radius + center_pos[0]
            y = np.sin(angle) * radius + center_pos[1]
            vertices.append((x, y))

        vertices = np.array(vertices, dtype=np.float32)
        if len(center_pos) == 3:
            vertices = np.hstack([
                vertices,
                np.full([vertices.shape[0], 1],
                        center_pos[-1],
                        dtype=np.float32),
            ])

        super().__init__(
            vertices=vertices,
            primitive=PrimitiveShape.TRIANGLE_FAN,
            color=color,
            fill_mode=fill_mode,
        )
