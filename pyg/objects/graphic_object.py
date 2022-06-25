""" Implements an abstract class that represents a generic graphic object.
"""

from __future__ import annotations

import abc
from typing import Optional, Any
from collections.abc import Sequence

import numpy as np
import OpenGL.GL as gl  # noqa

from pyg.utils import Coord2D, Coord3D
from pyg.transformation_handler import TransformationHandler


class GraphicObject(abc.ABC):
    """ Abstract class representing a generic drawable graphic object. """

    def __init__(self,
                 vertices: Sequence[Coord2D] | Sequence[Coord3D],
                 initial_model: Optional[np.ndarray] = None) -> None:
        """ Instantiates a new graphic object.

        Args:
            vertices: Coordinates of the object's vertices.
            initial_model: Optional initial value for the object's model matrix.
                If provided, it must be a 4x4 NumPy array. If not provided, an
                identity matrix is used.
        """
        self.vertices = vertices  # type: ignore[assignment]
        self._transformation_handler = TransformationHandler(
            initial_matrix=initial_model,
        )

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
    def transform(self) -> TransformationHandler:
        """ Transformation handler (instance of `TransformationHandler`) that
        handles transformations in this object's model matrix.

        Use the returned object to apply transformations to this object's
        model matrix.
        """
        return self._transformation_handler

    @property
    def model_matrix(self) -> np.ndarray:
        """ The object's model matrix. """
        return self._transformation_handler.matrix

    @abc.abstractmethod
    def draw(self,
             *,
             color_loc: Optional[Any] = None,
             texture_coord_loc: Optional[Any] = None) -> None:
        """ Draws the object in the current OpenGL window.

        When this method is called, the object's vertices must already be in the
        GPU. This method is responsible for specifying the object's color and
        its fill mode or its texture, as well as drawing its vertices.

        If textures are being used, then, when this method is called, the
        current bound OpenGL buffer can be safely used to store the coordinates
        of the object's texture.

        Args:
            color_loc: Location of the `color` attribute in the vertex shader.
                This argument is only provided by the drawer if using textures
                is disabled.
            texture_coord_loc: Location of the vertex attribute associated with
                the texture's coordinate. This argument is only provided by th
                 drawer if using textures is enabled.
        """
