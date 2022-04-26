""" Implements the game object that represents a black hole.
"""

from timeit import default_timer as timer

import pyg

from .game_object import GameObject


_MIN_SCALING_INTERVAL = 0.01
_SCALE_STEP_FACTOR = 1.02
_BLACK_HOLE_GRAVITY_FACTOR = 0.075


class BlackHole(GameObject):
    """ Represents a black hole. """

    def __init__(self,
                 initial_pos: pyg.utils.Coord2D = (0.82, 0.82),
                 initial_scale: float = 0.8) -> None:
        self._scaling_counter = 0
        self._reverse_scales = False
        self._last_scaling = 0

        super().__init__(
            initial_pos=initial_pos,
            initial_scale=initial_scale,
            all_graphics=[
                pyg.objects.Circle(
                    color=(r/140, r/120, r/100, 1),
                    fill_mode=(pyg.FillMode.POINT if r > 16
                               else pyg.FillMode.FILL),
                    center_pos=(0, 0),
                    radius=0.15 * r / 100,
                )
                for r in range(100)
            ],
        )

    def calc_gravitational_pull(self, obj: GameObject) -> tuple[float, float]:
        """ Calculates the gravitational pull the black hole exerts on the given
        object.
        """
        d = max(self.distance(obj), 1e-4)
        g = _BLACK_HOLE_GRAVITY_FACTOR / (d ** 2)

        gX = g * (self.x - obj.x) / d
        gY = g * (self.y - obj.y) / d
        return gX, gY

    def update(self, dT: float, *args, **kwargs) -> None:
        if (timer() - self._last_scaling) >= _MIN_SCALING_INTERVAL:
            sx = sy = (1 / _SCALE_STEP_FACTOR if self._reverse_scales
                       else _SCALE_STEP_FACTOR)

            self.scale(sx=sx, sy=sy)
            self._scaling_counter += 1
            self._last_scaling = timer()

            if self._scaling_counter >= 20:
                self._scaling_counter = 0
                self._reverse_scales = not self._reverse_scales

        self.rotate(angle=dT * 30, axis="z")
        super().update(dT, *args, **kwargs)
