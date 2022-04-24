""" Implementation of a utility class that abstracts the interaction with a
transformation matrix.
"""

from typing import Optional, Literal

import numpy as np


class TransformationHandler:
    """ Abstracts the interaction with a transformation matrix.

    A transformation matrix represents a sequence of transformations that can be
    applied to individual vertices (vectors).
    """

    def __init__(self, initial_matrix: Optional[np.ndarray] = None) -> None:
        """ Instantiates a new transformation handler.

        Args:
            initial_matrix: Optional 4x4 NumPy array representing the initial
                transformation matrix. If not provided, the initial matrix will
                be an identity matrix.
        """
        if initial_matrix is not None:
            assert initial_matrix.shape == (4, 4)
            self._matrix = initial_matrix.astype(np.float32)
        else:
            self._matrix = np.eye(4, dtype=np.float32)
        self._initial_matrix: np.ndarray = self._matrix.copy()

    @property
    def matrix(self) -> np.ndarray:
        """ The current transformation matrix. """
        return self._matrix

    @matrix.setter
    def matrix(self, new_matrix: np.ndarray) -> None:
        """ Manually sets the transformation matrix. """
        assert new_matrix.shape == (4, 4)
        self._matrix = new_matrix

    def reset(self) -> None:
        """ Resets the transformation matrix to its initial value.

        If no initial value was provided when instantiating the transformation
        handler, the new matrix will be an identity matrix.
        """
        self._matrix = self._initial_matrix.copy()

    def __call__(self, transformation: np.ndarray) -> None:
        """ Applies the transformation specified by the provided matrix.

        This method will update the internal transformation matrix of this
        handler.
        """
        assert transformation.shape == (4, 4)
        self._matrix = np.matmul(transformation,
                                 self._matrix).astype(np.float32)

    def translate(self,
                  tx: float = 0.0,
                  ty: float = 0.0,
                  tz: float = 0.0) -> None:
        """ Applies a translation using the provided offsets.

        Args:
            tx: Offset in the x-axis' direction. Defaults to 0.
            ty: Offset in the y-axis' direction. Defaults to 0.
            tz: Offset in the z-axis' direction. Defaults to 0.
        """
        self(np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0,  1],
        ]))

    def rotate(self, angle: float, axis: Literal["x", "y", "z"] = "x") -> None:
        """ Applies a rotation.

        Args:
            angle: The rotation angle, in degrees.
            axis: The rotation axis ("x", "y" or "z"). Defaults to "x".

        Raises:
            ValueError: If `axis` contains an invalid value.
        """
        angle = np.pi * (angle / 180)
        cos, sin = np.cos(angle), np.sin(angle)

        if axis == "x":
            self(np.array([
                [1,  0,    0,     0],
                [0,  cos,  -sin,  0],
                [0,  sin,  cos,   0],
                [0,  0,    0,     1],
            ]))
        elif axis == "y":
            self(np.array([
                [cos,   0,   sin,  0],
                [0,     1,   0,    0],
                [-sin,  0,   cos,  0],
                [0,     0,   0,    1],
            ]))
        elif axis == "z":
            self(np.array([
                [cos,  -sin,  0,  0],
                [sin,  cos,   0,  0],
                [0,    0,     1,  0],
                [0,    0,     0,  1],
            ]))
        else:
            raise ValueError(f"Invalid rotation axis \"{axis}\"!")

    def scale(self,
              sx: float = 1.0,
              sy: float = 1.0,
              sz: float = 1.0) -> None:
        """ Applies a scaling transformation.

        Args:
            sx: Scaling factor along the x-axis' direction. Defaults to 1.
            sy: Scaling factor along the y-axis' direction. Defaults to 1.
            sz: Scaling factor along the z-axis' direction. Defaults to 1.
        """
        self(np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0,  1],
        ]))
