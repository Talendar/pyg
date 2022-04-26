""" Implements the game object that represents the spaceship controlled by the
player.
"""

import math

import pyg

from .game_object import GameObject


_VERTICAL_ENGINES_ACCELERATION = 0.07
_ROTATION_ENGINES_ACCELERATION = 90


class Spaceship(GameObject):
    """ Represents the spaceship controlled by the player.

    Attributes:
        upper_engines_on(bool): Whether the upper engines are on.
        lower_engines_on(bool): Whether the lower engines are on.
        clockwise_rotation_engines_on(bool): Whether the "clockwise rotation"
            engines are on.
        anticlockwise_rotation_engines_on(bool): Whether the "anti-clockwise
            rotation" engines are on.
    """

    def __init__(self,
                 initial_pos: pyg.utils.Coord2D = (0.75, -0.9),
                 initial_scale: float = 1.0) -> None:
        self.upper_engines_on = False
        self.lower_engines_on = False
        self.clockwise_rotation_engines_on = False
        self.anticlockwise_rotation_engines_on = False

        # Specify the graphics for the spaceship's body.
        self._spaceship_graphics = [
            # Bottom-left turbine
            pyg.objects.Triangle(
                color=(0.65, 0.65, 0.65, 1),
                vertices=(
                    (-0.01, -0.02),
                    (-0.02, -0.07),
                    (-0.005, -0.07),
                ),
            ),
            # Bottom-right turbine
            pyg.objects.Triangle(
                color=(0.65, 0.65, 0.65, 1),
                vertices=(
                    (0.01, -0.02),
                    (0.005, -0.07),
                    (0.02, -0.07),
                ),
            ),
            # Top-left turbine
            pyg.objects.Triangle(
                color=(0.65, 0.65, 0.65, 1),
                vertices=(
                    (-0.005, 0),
                    (-0.012, 0.015),
                    (-0.0175, -0.005),
                ),
            ),
            # Top-right turbine
            pyg.objects.Triangle(
                color=(0.65, 0.65, 0.65, 1),
                vertices=(
                    (0.005, 0),
                    (0.012, 0.015),
                    (0.0175, -0.005),
                ),
            ),
            # Body
            pyg.objects.Triangle(
                color=(1, 0.815, 0.137, 1),
                vertices=(
                    (0, 0.05),
                    (-0.025, -0.05),
                    (0.025, -0.05),
                ),
            ),
        ]

        # Specify the graphics for the "combustion flames" of the lower engines.
        self._lower_combustion_graphics = [
            # Bottom-left turbine flame
            pyg.objects.Triangle(
                color=(1, 0, 0, 1),
                vertices=(
                    (-0.0125, -0.09),
                    (-0.0175, -0.07),
                    (-0.0075, -0.07),
                ),
            ),
            # Bottom-right turbine flame
            pyg.objects.Triangle(
                color=(1, 0, 0, 1),
                vertices=(
                    (0.0125, -0.09),
                    (0.0175, -0.07),
                    (0.0075, -0.07),
                ),
            ),
        ]

        # Specify the graphics for the "combustion flames" of the upper engines.
        self._upper_combustion_graphics = [
            # Top-left turbine flame
            pyg.objects.Triangle(
                color=(1, 0, 0, 1),
                vertices=(
                    (-0.015, 0),
                    (-0.025, 0.0175),
                    (0, 0),
                ),
            ),
            # Top-right turbine flame
            pyg.objects.Triangle(
                color=(1, 0, 0, 1),
                vertices=(
                    (0.015, 0),
                    (0.025, 0.0175),
                    (0, 0),
                ),
            ),
        ]

        # Specify the graphics for the "combustion flames" of the "clockwise
        # rotation" engines.
        self._clockwise_rotation_graphics = [
            # Top-right rotation turbine flame
            pyg.objects.Triangle(
                color=(0.2, 0.4, 1, 1),
                vertices=(
                    (0.005, 0.03),
                    (0, 0.04),
                    (0.0125, 0.045),
                ),
            ),
            # Bottom-left rotation turbine flame
            pyg.objects.Triangle(
                color=(0.2, 0.4, 1, 1),
                vertices=(
                    (-0.031, -0.03),
                    (0.021, -0.04),
                    (-0.021, -0.045),
                ),
            ),
        ]

        # Specify the graphics for the "combustion flames" of the
        # "anti-clockwise rotation" engines.
        self._anticlockwise_rotation_graphics = [
            # Top-left rotation turbine flame
            pyg.objects.Triangle(
                color=(0.2, 0.4, 1, 1),
                vertices=(
                    (-0.005, 0.03),
                    (0, 0.04),
                    (-0.0125, 0.045),
                ),
            ),
            # Bottom-right rotation turbine flame
            pyg.objects.Triangle(
                color=(0.2, 0.4, 1, 1),
                vertices=(
                    (0.031, -0.03),
                    (-0.021, -0.04),
                    (0.021, -0.045),
                ),
            ),
        ]

        # Call the constructor of the parent class.
        super().__init__(
            initial_pos=initial_pos,
            initial_scale=initial_scale,
            all_graphics=[
                *self._lower_combustion_graphics,
                *self._upper_combustion_graphics,
                *self._clockwise_rotation_graphics,
                *self._anticlockwise_rotation_graphics,
                *self._spaceship_graphics,
            ],
        )

    @property
    def graphics(self) -> list[pyg.objects.GraphicObject]:
        """ List with all the graphic objects associated with this game object
        that should be rendered.
        """
        comb_graphics = []

        if self.lower_engines_on:
            comb_graphics += self._lower_combustion_graphics
        if self.upper_engines_on:
            comb_graphics += self._upper_combustion_graphics

        if self.clockwise_rotation_engines_on:
            comb_graphics += self._clockwise_rotation_graphics
        if self.anticlockwise_rotation_engines_on:
            comb_graphics += self._anticlockwise_rotation_graphics

        return comb_graphics + self._spaceship_graphics

    def shut_down_engines(self) -> None:
        """ Shuts down all the spaceship's engines. """
        self.lower_engines_on = False
        self.upper_engines_on = False
        self.clockwise_rotation_engines_on = False
        self.anticlockwise_rotation_engines_on = False

    def update(self,
               dT: float,
               gX: float = 0.0,
               gY: float = 0.0,
               *args, **kwargs) -> None:
        """ Updates the spaceship's internal state.

        Args:
            dT: Time elapsed, in seconds, since the last update.
            gX: The spaceship's acceleration in the x-axis due to gravitational
                pull.
            gY: The spaceship's acceleration in the y-axis due to gravitational
                pull.
        """
        # Calculate the spaceship's translational acceleration.
        a = 0
        if self.lower_engines_on:
            a -= _VERTICAL_ENGINES_ACCELERATION
        if self.upper_engines_on:
            a += _VERTICAL_ENGINES_ACCELERATION

        angle_rads = math.pi * (self._angle / 180)
        aX = gX - a * math.cos(angle_rads)
        aY = gY - a * math.sin(angle_rads)

        # Calculate the spaceship's rotational acceleration around the z-axis.
        rot_accel_z = 0
        if self.clockwise_rotation_engines_on:
            rot_accel_z += _ROTATION_ENGINES_ACCELERATION
        if self.anticlockwise_rotation_engines_on:
            rot_accel_z -= _ROTATION_ENGINES_ACCELERATION

        # Update the spaceship.
        super().update(dT=dT, aX=aX, aY=aY, rot_accel_z=rot_accel_z)
