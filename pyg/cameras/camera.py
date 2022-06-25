""" Defines what a camera is.
"""

from __future__ import annotations

import abc
from typing import Literal, Optional, TYPE_CHECKING

import numpy as np
import glm

if TYPE_CHECKING:
    from pyg.window import Window
    from pyg.utils import Coord3D


class Camera(abc.ABC):
    """ Abstract class representing a camera. """

    def __init__(self,
                 pos: Coord3D = (0, 0, 2.5),
                 up: Coord3D = (0, 1, 0),
                 front: Coord3D = (0, 0, -1),
                 yaw: float = -90,
                 pitch: float = 0,
                 movement_speed: float = 5,
                 mouse_sensitivity: float = 0.1,
                 zoom: float = 45,
                 window: Optional[Window] = None) -> None:
        self._window: Optional[Window] = window
        self._pos = glm.vec3(*pos)
        self._world_up = glm.vec3(*up)
        self._front = glm.vec3(*front)
        self._yaw = yaw
        self._pitch = pitch
        self.movement_speed = movement_speed
        self.mouse_sensitivity = mouse_sensitivity
        self._fov = zoom
        self._right = glm.vec3(0, 0, 0)
        self._up = glm.vec3(0, 0, 0)
        self._update_vectors()

    @property
    def view_matrix(self) -> np.ndarray:
        return np.array(
            glm.lookAt(
                self._pos,                # eye
                self._pos + self._front,  # center
                self._up,                 # up
            ),
        )

    @property
    def projection_matrix(self) -> np.ndarray:
        if self._window is None:
            raise RuntimeError(
                "Attempt to build a projection matrix in a camera with no "
                "window!"
            )
        return np.array(
            glm.perspective(
                glm.radians(self._fov),
                self._window.size[0] / self._window.size[1],
                0.1,
                100,
            ),
        )

    def set_window(self, new_window: Window) -> None:
        self._window = new_window

    @abc.abstractmethod
    def move(self,
             direction: Literal["forward", "backward", "left", "right"],
             dT: float) -> None:
        """ Moves the camera. """

    @abc.abstractmethod
    def incline(self,
                x_offset: float,
                y_offset: float,
                constrain_pitch: bool = True) -> None:
        """ Inclines the camera. """

    @abc.abstractmethod
    def zoom(self, fov: float) -> None:
        """ Zooms the camera. """

    def _update_vectors(self) -> None:
        self._front = glm.normalize(glm.vec3(
            glm.cos(glm.radians(self._yaw)) * glm.cos(glm.radians(self._pitch)),
            glm.sin(glm.radians(self._pitch)),
            glm.sin(glm.radians(self._yaw)) * glm.cos(glm.radians(self._pitch)),
        ))
        self._right = glm.normalize(glm.cross(self._front, self._world_up))
        self._up = glm.normalize(glm.cross(self._right, self._front))
