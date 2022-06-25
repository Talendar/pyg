""" Implements a simple camera.
"""

from __future__ import annotations
from typing import Literal

from .camera import Camera


class SimpleCamera(Camera):
    """ A simple camera. """

    def move(self,
             direction: Literal["forward", "backward", "left", "right"],
             dT: float) -> None:
        vel = self.movement_speed * dT
        if direction == "forward":
            self._pos += self._front * vel
        elif direction == "backward":
            self._pos -= self._front * vel
        elif direction == "left":
            self._pos -= self._right * vel
        elif direction == "right":
            self._pos += self._right * vel
        else:
            raise ValueError(f"Invalid movement direction \"{direction}\".")

    def incline(self,
                x_offset: float,
                y_offset: float,
                constrain_pitch: bool = True) -> None:
        self._yaw += x_offset * self.mouse_sensitivity
        self._pitch -= y_offset * self.mouse_sensitivity
        if constrain_pitch:
            self._pitch = max(min(self._pitch, 90), -90)
        self._update_vectors()

    def zoom(self, fov: float) -> None:
        self._fov = max(min(fov, 45), 1)
