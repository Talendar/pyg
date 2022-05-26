""" Implements a cube.obj.
"""


from __future__ import annotations
from typing import Optional, Any

import numpy as np
import OpenGL.GL as gl  # noqa

from .graphic_object import GraphicObject
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.enums.fill_mode import FillMode
from pyg.utils import Color, Colored


class Cube(GraphicObject, Colored):
    """ Simple cube.obj. """

    def __init__(self,
                 color: Optional[Color | np.ndarray] = None,
                 diff_faces_colors: bool = True,
                 fill_mode: FillMode = FillMode.FILL,
                 initial_model: Optional[np.ndarray] = None) -> None:
        self.color = color
        self.diff_faces_colors = diff_faces_colors
        self.fill_mode = fill_mode
        super().__init__(
            initial_model=initial_model,
            vertices=[
                # Face 1
                (-0.2, -0.2, +0.2),
                (+0.2, -0.2, +0.2),
                (-0.2, +0.2, +0.2),
                (+0.2, +0.2, +0.2),

                # Face 2
                (+0.2, -0.2, +0.2),
                (+0.2, -0.2, -0.2),
                (+0.2, +0.2, +0.2),
                (+0.2, +0.2, -0.2),

                # Face 3
                (+0.2, -0.2, -0.2),
                (-0.2, -0.2, -0.2),
                (+0.2, +0.2, -0.2),
                (-0.2, +0.2, -0.2),

                # Face 4
                (-0.2, -0.2, -0.2),
                (-0.2, -0.2, +0.2),
                (-0.2, +0.2, -0.2),
                (-0.2, +0.2, +0.2),

                # Face 5
                (-0.2, -0.2, -0.2),
                (+0.2, -0.2, -0.2),
                (-0.2, -0.2, +0.2),
                (+0.2, -0.2, +0.2),

                # Face 6
                (-0.2, +0.2, +0.2),
                (+0.2, +0.2, +0.2),
                (-0.2, +0.2, -0.2),
                (+0.2, +0.2, -0.2),
            ],
        )

    def draw(self, color_loc: Any) -> None:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, self.fill_mode.value)
        for i in range(0, 24, 4):
            color = (
                ((24 - i) / 16) * self.color[:3]
                if self.diff_faces_colors else self.color[:3]
            )
            gl.glUniform4f(color_loc, *color, self.color[-1])
            gl.glDrawArrays(PrimitiveShape.TRIANGLE_STRIP.value, i, 4)
