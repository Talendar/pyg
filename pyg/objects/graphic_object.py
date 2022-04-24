""" Implements a class that represents a graphic object.
"""

from __future__ import annotations

from typing import Optional
from collections.abc import Sequence, Callable

import numpy as np

from pyg.utils import Coord2D, Coord3D, Color
from pyg.enums.fill_mode import FillMode
from pyg.enums.primitive_shape import PrimitiveShape
from pyg.transformation_handler import TransformationHandler
from pyg.defaults import DEFAULT_COLOR


class GraphicObject:
    """ Represents a drawable graphic object. """

    def __init__(self,
                 vertices: Sequence[Coord2D] | Sequence[Coord3D],
                 primitive: PrimitiveShape,
                 color: Optional[Color | np.ndarray] = None,
                 initial_transformation: Optional[np.ndarray] = None,
                 fill_mode: FillMode = FillMode.FILL,
                 on_draw: Optional[Callable[[], None]] = None) -> None:
        """ Instantiates a new graphic object.

        Args:
            vertices: Coordinates of the object's vertices.
            primitive: The OpenGL
                [primitive](https://www.khronos.org/opengl/wiki/Primitive) to be
                used to connect the object's vertices.
            color: Optional color for the whole object. If not provided, a
                default color will be used.
            initial_transformation: Optional initial value for the object's
                transformation matrix. If provided, it must be a 4x4 NumPy
                array. If not provided, an identity matrix is used.
            fill_mode: Specifies how the object should be filled.
            on_draw: Optional callback fired right before the object is drawn.
                It's useful when you need to tweak OpenGL's state before the
                object is drawn.
        """
        self.vertices = vertices  # type: ignore[assignment]
        self.primitive = primitive
        self.color = color  # type: ignore[assignment]
        self._transformation_handler = TransformationHandler(
            initial_matrix=initial_transformation,
        )
        self.fill_mode = fill_mode
        self.on_draw = on_draw

    @property
    def vertices(self) -> np.ndarray:
        """ NumPy array of shape `(n, 3)` containing the raw/untransformed
        coordinates (x, y and z) of the object's `n` vertices.
        """
        return self._vertices

    @vertices.setter
    def vertices(
        self,
        new_vertices: Sequence[Coord2D] | Sequence[Coord3D] | np.ndarray,
    ) -> None:
        """ Sets the coordinates of all the object's vertices. """
        # Convert the vertices to a NumPy array.
        new_vertices = np.array(new_vertices, dtype=np.float32)

        # Check if the vertices have the correct shapes.
        assert len(new_vertices.shape) == 2
        assert new_vertices.shape[1] in (2, 3)

        # Convert 2D vertices to 3D, if necessary.
        if new_vertices.shape[1] == 2:
            new_vertices = np.hstack([
                new_vertices,
                np.zeros((new_vertices.shape[0], 1), dtype=np.float32),
            ])

        # Update the current vertices.
        self._vertices = new_vertices

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

    @property
    def transform(self) -> TransformationHandler:
        """ Returns this object's transformation handler (instance of
        `TransformationHandler`).
        """
        return self._transformation_handler
