""" Implements a class representing a texture in OpenGL.
"""

from collections.abc import Sequence

import numpy as np
import OpenGL.GL as gl
from PIL import Image

from pyg.utils import Coord2D


class Texture:
    """ Represents a texture in OpenGL. """

    def __init__(self, coordinates: Sequence[Coord2D], img_path: str) -> None:
        """ Creates a new texture.

        Ideally, this constructor should be called within the GL context of the
        window in which the texture will be drawn.

        Args:
            coordinates: Sequence with the 2D coordinates of the texture.
            img_path: Path to the file containing the image associated with the
                texture.
        """
        self._coordinates = np.array(coordinates, dtype=np.float32)
        assert len(self._coordinates.shape) == 2
        assert self._coordinates.shape[1] == 2

        self._img_path = img_path
        self._id = gl.glGenTextures(1)

        self.bind()

        # Set the texture's wrapping options.
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

        # Set the texture's filtering options.
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)

        # Load the texture's image and send it to the GPU.
        img = Image.open(img_path)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGB,
            img.size[0],
            img.size[1],
            0,
            gl.GL_RGB,
            gl.GL_UNSIGNED_BYTE,
            img.tobytes("raw", "RGB", 0, -1),
        )

    @property
    def coordinates(self) -> np.ndarray:
        """ NumPy array with the texture's coordinates. Shape: (n, 2). """
        return self._coordinates

    def bind(self) -> None:
        """ Binds the texture to the current OpenGL context. """
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._id)
