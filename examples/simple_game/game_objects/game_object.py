""" Implements an abstract class that represents an object in the game.
"""

from __future__ import annotations

import math
from typing import Literal, Optional
from abc import ABC
from dataclasses import dataclass

import pyg
import numpy as np


_MAX_VEL = 0.5


class GameObject(ABC):
    """ Abstract class representing an object in the game. """

    def __init__(self,
                 all_graphics: list[pyg.objects.SimpleGraphicObject],
                 initial_pos: pyg.utils.Coord2D = (0, 0),
                 initial_scale: float = 1.0) -> None:
        self._x, self._y = (0.0, 0.0)
        self.vel_x = self.vel_y = 0.0
        self._angle = 90.0
        self._vel_angular = 0.0
        self._scale_x = self._scale_y = 1.0

        self._bounding_box: Optional[BoundingBox] = None
        self._all_graphics = all_graphics

        if initial_pos != (0, 0):
            self.translate(*initial_pos)
        if initial_scale != 1:
            self.scale(sx=initial_scale, sy=initial_scale)

    @property
    def x(self) -> float:
        """ The object's position in the x-axis. """
        return self._x

    @property
    def y(self) -> float:
        """ The object's position in the y-axis. """
        return self._y

    @property
    def graphics(self) -> list[pyg.objects.SimpleGraphicObject]:
        """ List with the graphic objects that compose this object. """
        return self._all_graphics

    @property
    def bounding_box(self) -> BoundingBox:
        """ The object's bounding box. """
        if self._bounding_box is not None:
            return self._bounding_box

        min_x = min_y = float("inf")
        max_x = max_y = -float("inf")
        for graphic_object in self.graphics:
            vertices = graphic_object.vertices
            vertices = np.matmul(
                graphic_object.transform.matrix,
                np.append(vertices, np.ones((vertices.shape[0], 1)), axis=1).T,
            )
            for x, y, _, _ in vertices.T:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

        return BoundingBox(
            x=min_x,
            y=max_y,
            width=max_x - min_x,
            height=max_y - min_y,
        )

    def is_colliding_with(self, other: GameObject) -> bool:
        """ Checks if this object is colliding with the given object. """
        b1, b2 = self.bounding_box, other.bounding_box
        return (
            b1.x < (b2.x + b2.width) and
            (b1.x + b1.width) > b2.x and
            b1.y > (b2.y - b2.height) and
            (b1.y - b1.height) < b2.y
        )

    def render(self, window: pyg.Window) -> None:
        """ Renders the object in the given window. """
        for graphic_object in self.graphics:
            window.draw(graphic_object)

    def distance(self, other: GameObject) -> float:
        """ Calculates the euclidean distance between this object and the given
        object, in OpenGL window coordinates.

        Args:
            other: The other object.

        Returns:
            The euclidean distance between the objects' centers, in OpenGL
            window coordinates.
        """
        return math.sqrt(
            ((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)
        )

    def update(self,
               dT: float,
               aX: float = 0.0,
               aY: float = 0.0,
               rot_accel_z: float = 0.0) -> None:
        """ Updates the current object's internal state.

        Args:
            dT: Time elapsed, in seconds, since the last update.
            aX: The object's resulting acceleration in the x-axis.
            aY: The object's resulting acceleration in the y-axis.
            rot_accel_z: Resulting rotational acceleration of the object around
                the z-axis, in degrees/s^2.
        """
        # Handle translational movement.
        if abs(self.vel_x) >= 1e-5 or abs(self.vel_y) >= 1e-5:
            self.translate(tx=self.vel_x * dT,
                           ty=self.vel_y * dT)

        # Handle rotational movement.
        if abs(self._vel_angular) >= 1e-3:
            self.rotate(angle=self._vel_angular * dT,
                        axis="z")

        # Handle translational acceleration.
        self.vel_x += aX * dT
        self.vel_y += aY * dT

        self.vel_x = max(min(self.vel_x, _MAX_VEL), -_MAX_VEL)
        self.vel_y = max(min(self.vel_y, _MAX_VEL), -_MAX_VEL)

        # Handle rotational acceleration.
        self._vel_angular += rot_accel_z * dT

    def translate(self, tx: float = 0.0, ty: float = 0.0) -> None:
        """ Translates the object by the given offset. """
        self._bounding_box = None
        self._x += tx
        self._y += ty
        for graphic_object in self._all_graphics:
            graphic_object.transform.translate(tx, ty)

    def rotate(self, angle: float, axis: Literal["x", "y", "z"] = "z") -> None:
        """ Rotates the object around the given axis.

        The center of rotation is the object's position.

        Args:
            angle: Angle of rotation, in degrees.
            axis: The axis around which the object will rotate. Defaults to the
                z-axis.
        """
        self._bounding_box = None
        self._angle = (self._angle + angle) % 360
        for graphic_object in self._all_graphics:
            # To rotate the object around its center, we must apply some
            # translations. See:
            # https://math.stackexchange.com/questions/2093314/rotation-matrix-of-rotation-around-a-point-other-than-the-origin  # noqa
            graphic_object.transform.translate(tx=-self._x, ty=-self._y)
            graphic_object.transform.rotate(angle, axis)
            graphic_object.transform.translate(tx=self._x, ty=self._y)

    def scale(self, sx: float = 1.0, sy: float = 1.0) -> None:
        """ Scales the object.

        Args:
            sx: Scale factor for the x-axis.
            sy: Scale factor for the y-axis.
        """
        self._bounding_box = None
        self._scale_x *= sx
        self._scale_y *= sy
        for graphic_object in self._all_graphics:
            # To scale the object without moving its center, we must apply some
            # translations. See:
            # https://math.stackexchange.com/questions/2093314/rotation-matrix-of-rotation-around-a-point-other-than-the-origin  # noqa
            graphic_object.transform.translate(tx=-self._x, ty=-self._y)
            graphic_object.transform.scale(sx=sx, sy=sy)
            graphic_object.transform.translate(tx=self._x, ty=self._y)


@dataclass(frozen=True)
class BoundingBox:
    x: float
    y: float
    width: float
    height: float
