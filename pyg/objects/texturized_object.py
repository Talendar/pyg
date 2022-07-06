""" Implements a graphic object that has a texture.
"""

from __future__ import annotations

import ctypes
from typing import Optional, Any
from collections.abc import Sequence

import numpy as np
import OpenGL.GL as gl

from pyg.utils import Coord2D, Coord3D, load_wavefront
from pyg.texture import Texture
from pyg.enums.primitive_shape import PrimitiveShape
from .graphic_object import GraphicObject


class TexturizedGraphicObject(GraphicObject):
    """ Represents a graphic object that has a texture. """

    def __init__(self,
                 vertices: Sequence[Coord2D] | Sequence[Coord3D],
                 texture: Texture,
                 initial_model: Optional[np.ndarray] = None,
                 primitive: PrimitiveShape = PrimitiveShape.TRIANGLES) -> None:
        self._texture = texture
        self._primitive = primitive
        super().__init__(vertices=vertices, initial_model=initial_model)

    def draw(self,
             *,
             color_loc: Optional[Any] = None,
             texture_coord_loc: Optional[Any] = None) -> None:
        # Send the texture's coordinates to the buffer. The buffer is expected
        # to have already been bound.
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self._texture.coordinates.nbytes,
            self._texture.coordinates,
            gl.GL_DYNAMIC_DRAW,
        )

        # Associate the texture's coordinates with the appropriate attribute.
        gl.glEnableVertexAttribArray(texture_coord_loc)
        gl.glVertexAttribPointer(
            texture_coord_loc,
            2,
            gl.GL_FLOAT,
            False,
            self._texture.coordinates.strides[0],
            ctypes.c_void_p(0),
        )

        # Bind the texture and draw the object.
        self._texture.bind()
        gl.glDrawArrays(self._primitive.value, 0, len(self.vertices))

    @staticmethod
    def from_file(
        file_path: str,
        texture_img_path: str,
        primitive: PrimitiveShape = PrimitiveShape.TRIANGLES,
    ) -> TexturizedGraphicObject:
        """ Loads a texturized graphic object from a file.

        Args:
            file_path: Path to the object's file. Currently, only Wavefront
                files are supported.
            texture_img_path: Path to the image associated with the object's
                texture.

        Returns:
            The built object.
        """
        obj_data = load_wavefront(file_path)
        vertices, texture_coords = [], []
        for face in obj_data["faces"]:
            vertices += [obj_data["vertices"][vid - 1] for vid in face[0]]
            texture_coords += [obj_data["texture"][tid - 1] for tid in face[1]]

        assert len(vertices) == len(texture_coords)
        return TexturizedGraphicObject(
            vertices=vertices,
            texture=Texture(
                coordinates=texture_coords,
                img_path=texture_img_path,
            ),
            primitive=primitive,
        )
