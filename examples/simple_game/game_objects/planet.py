""" Implements the game object that represents a planet.
"""

import pyg

from .game_object import GameObject


class Planet(GameObject):
    """ Represents a planet. """

    def __init__(self,
                 initial_pos: pyg.utils.Coord2D = (-0.89, 0.89),
                 initial_scale: float = 1) -> None:
        super().__init__(
            initial_pos=initial_pos,
            initial_scale=initial_scale,
            all_graphics=[
                pyg.objects.Circle(
                    color=(0, 162/255, 205/255, 1),
                    center_pos=(0, 0),
                    radius=0.1,
                ),
                pyg.objects.Rectangle(
                    color=(79/255, 156/255, 6/255, 1),
                    top_left=(-0.04, 0.04),
                    size=(0.02, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.05, 0.05),
                    size=(0.02, 0.04),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.07, 0.03),
                    size=(0.03, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.065, 0.025),
                    size=(0.02, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.055, 0.015),
                    size=(0.02, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.05, 0.01),
                    size=(0.02, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.045, 0.05),
                    size=(0.0125, 0.05),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.045, -0.025),
                    size=(0.01, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(-0.06, 0.04),
                    size=(0.01, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(0.0175, 0.06),
                    size=(0.025, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(0.0225, 0.07),
                    size=(0.01, 0.01),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(0.03, 0.04),
                    size=(0.025, 0.02),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(0.04, -0.04),
                    size=(0.0075, 0.0075),
                ),
                pyg.objects.Rectangle(
                    color=(79 / 255, 156 / 255, 6 / 255, 1),
                    top_left=(0.01, -0.06),
                    size=(0.005, 0.005),
                ),
            ],
        )
