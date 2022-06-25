""" Implements a class that represents a simple graphic object.
"""

from __future__ import annotations

from typing import Optional, Any
from collections.abc import Sequence

import numpy as np
import OpenGL.GL as gl  # noqa

from pyg.utils import Coord2D, Coord3D, Color, Colored
from pyg.enums.fill_mode import FillMode
from pyg.enums.primitive_shape import PrimitiveShape
from .graphic_object import GraphicObject


class SimpleGraphicObject(GraphicObject, Colored):
    """ Represents a simple drawable graphic object, with some pre-defined
    behaviour.
    """

    def __init__(self,
                 vertices: Sequence[Coord2D] | Sequence[Coord3D],
                 primitive: PrimitiveShape,
                 color: Optional[Color | np.ndarray] = None,
                 initial_model: Optional[np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL) -> None:
        """ Instantiates a new graphic object.

        Args:
            vertices: Coordinates of the object's vertices.
            primitive: The OpenGL
                [primitive](https://www.khronos.org/opengl/wiki/Primitive) to be
                used to connect the object's vertices.
            color: Optional color for the whole object. If not provided, a
                default color will be used.
            initial_model: Optional initial value for the object's model matrix.
                If provided, it must be a 4x4 NumPy array. If not provided, an
                identity matrix is used.
            fill_mode: Specifies how the object should be filled.
        """
        super().__init__(vertices=vertices, initial_model=initial_model)
        self.primitive = primitive
        self.color = color
        self.fill_mode = fill_mode

    def draw(self,
             color_loc: Optional[Any] = None,
             texture_coord_loc: Optional[Any] = None) -> None:
        assert color_loc is not None
        gl.glUniform4f(color_loc, *self.color)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, self.fill_mode.value)
        gl.glDrawArrays(self.primitive.value, 0, len(self.vertices))
