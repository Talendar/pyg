""" Implements the game object that represents an asteroid.
"""

import random

import pyg

from .game_object import GameObject


class Asteroid(GameObject):
    """ Represents an asteroid. """

    def __init__(self) -> None:
        self._radius = random.uniform(0.025, 0.07)
        spawn_left = bool(random.getrandbits(1))
        super().__init__(
            initial_pos=(
                -1.1 if spawn_left else 1.1,
                random.uniform(-0.9, 0.75),
            ),
            all_graphics=[
                pyg.objects.Circle(
                    center_pos=(0, 0),
                    color=(158/255, 137/255, 120/255, 1),
                    radius=self._radius,
                    quality_level=random.randint(4, 9),
                ),
            ],
        )
        self._vel_x = (random.uniform(0.02, 0.35) if spawn_left
                       else random.uniform(-0.35, -0.02))
