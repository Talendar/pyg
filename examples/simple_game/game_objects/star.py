""" Implements the game object that represents a star.
"""

import random

import pyg

from .game_object import GameObject


class Star(GameObject):
    """ Represents a start. """

    def __init__(self) -> None:
        super().__init__(
            initial_pos=(random.uniform(-1, 1), random.uniform(-1, 1)),
            initial_scale=random.uniform(0.001, 0.02),
            all_graphics=[
                pyg.objects.Circle(
                    center_pos=(0, 0),
                    color=(1, 1, 1, 1),
                    radius=0.04,
                ),
                *[
                    pyg.objects.Circle(
                        center_pos=(0, 0),
                        color=(140 / 255, 195 / 255, 205 / 255, 1),
                        radius=0.04 + 0.01 * r,
                        fill_mode=pyg.FillMode.POINT,
                    )
                    for r in range(1, 4)
                ],
            ],
        )
