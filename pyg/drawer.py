""" Implementation of a drawer, which abstracts the drawing of basic shapes in a
:class:`Window`.
"""

from __future__ import annotations

import ctypes
from typing import TYPE_CHECKING, Final

import OpenGL.GL as gl  # noqa
import OpenGL.GL.shaders  # pylint: disable=[W0611]

from .objects import GraphicObject, Dot, Line, Triangle, Rectangle, Circle

if TYPE_CHECKING:
    from .window import Window


#: Source code for the vertex shader, without support for textures.
_VERTEX_SHADER_SRC: Final[str] = """
    #version 330 core
    
    attribute vec3 aPos;
    
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main() {
        gl_Position = projection * view * model * vec4(aPos, 1.0);
    }
"""

#: Source code for the vertex shader, WITH support for textures.
_VERTEX_SHADER_TEXTURE_SRC: Final[str] = """
    #version 330 core

    attribute vec3 aPos;
    attribute vec2 aTextureCoord;
    
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    
    out vec2 textureCoord;

    void main() {
        gl_Position = projection * view * model * vec4(aPos, 1.0);
        textureCoord = aTextureCoord;
    }
"""

#: Source code for the fragment shader, without support for textures.
_FRAGMENT_SHADER_SRC: Final[str] = """
    #version 330 core
    
    uniform vec4 color;
    
    void main() {
        gl_FragColor = color;
    } 
"""

#: Source code for the fragment shader, WITH support for textures.
_FRAGMENT_SHADER_TEXTURE_SRC: Final[str] = """
    #version 330 core
    
    in vec2 textureCoord;
    uniform sampler2D samplerTexture;

    void main() {
        gl_FragColor = texture2D(samplerTexture, textureCoord);
    } 
"""


class Drawer:
    """ Abstracts the drawing of basic shapes in a :class:`Window`. """

    def __init__(self, window: Window, use_textures: bool = False) -> None:
        self._window = window
        self._use_textures = use_textures

        with self._window:
            # Create buffers.
            buffer = gl.glGenBuffers(2 if use_textures else 1)

            # Vertex buffer and array objects.
            self._vbo = buffer[0] if use_textures else buffer
            self._vao = gl.glGenVertexArrays(1)

            # Buffer for the coordinates of textures.
            self._texture_buffer = buffer[1] if use_textures else None

            # Source code for the shaders.
            vertex_src, frag_src = (
                (_VERTEX_SHADER_TEXTURE_SRC, _FRAGMENT_SHADER_TEXTURE_SRC)
                if use_textures else (_VERTEX_SHADER_SRC, _FRAGMENT_SHADER_SRC)
            )

            # Compile the vertex shader.
            self._vertex_shader = gl.shaders.compileShader(
                vertex_src,
                gl.GL_VERTEX_SHADER,
            )

            # Compile the fragment shader.
            self._fragment_shader = gl.shaders.compileShader(
                frag_src,
                gl.GL_FRAGMENT_SHADER,
            )

            # Start a shader program.
            self._shader_program = gl.shaders.compileProgram(
                self._vertex_shader,
                self._fragment_shader,
            )

    def __call__(self, obj: GraphicObject) -> None:
        """ Draws a graphic object in the drawer's window. """
        with self._window:
            # Activate the shader program.
            gl.glUseProgram(self._shader_program)

            # Bind our vertex array object.
            gl.glBindVertexArray(self._vao)

            # Bind our vertex buffer and set its data (send our data to the
            # GPU).
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
            gl.glBufferData(
                gl.GL_ARRAY_BUFFER,
                obj.vertices.nbytes,
                obj.vertices,
                gl.GL_DYNAMIC_DRAW,
            )

            # Set our vertex attributes pointers. We're telling OpenGL how it
            # should interpret the vertex data.
            pos_attr_loc = gl.glGetAttribLocation(self._shader_program, "aPos")
            gl.glEnableVertexAttribArray(pos_attr_loc)
            gl.glVertexAttribPointer(
                pos_attr_loc,
                3,
                gl.GL_FLOAT,
                False,
                obj.vertices.strides[0],
                ctypes.c_void_p(0),
            )

            # Set the object's model matrix.
            gl.glUniformMatrix4fv(
                gl.glGetUniformLocation(self._shader_program, "model"),
                1,
                gl.GL_TRUE,
                obj.model_matrix,
            )

            # Set the window's view matrix.
            gl.glUniformMatrix4fv(
                gl.glGetUniformLocation(self._shader_program, "view"),
                1,
                gl.GL_TRUE,
                self._window.camera.view_matrix,
            )

            # Set the window's projection matrix.
            gl.glUniformMatrix4fv(
                gl.glGetUniformLocation(self._shader_program, "projection"),
                1,
                gl.GL_TRUE,
                self._window.camera.projection_matrix,
            )

            # Draw.
            if self._use_textures:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._texture_buffer)
                obj.draw(
                    texture_coord_loc=gl.glGetAttribLocation(
                        self._shader_program, "aTextureCoord",
                    ),
                )
            else:
                obj.draw(
                    color_loc=gl.glGetUniformLocation(
                        self._shader_program, "color",
                    ),
                )

            # Clean up.
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glUseProgram(0)

    def dot(self, *args, **kwargs) -> None:
        """ Draws a dot at the given position.

        This method has the same parameters as `__init__()` method of
        :class:`Dot`.
        """
        self(Dot(*args, **kwargs))

    def line(self, *args, **kwargs) -> None:
        """ Draws a line.

        This method has the same parameters as `__init__()` method of
        :class:`Line`.
        """
        self(Line(*args, **kwargs))

    def triangle(self, *args, **kwargs) -> None:
        """ Draws a triangle.

        This method has the same parameters as `__init__()` method of
        :class:`Triangle`.
        """
        self(Triangle(*args, **kwargs))

    def rect(self, *args, **kwargs) -> None:
        """ Draws a rectangle.

        This method has the same parameters as `__init__()` method of
        :class:`Rectangle`.
        """
        self(Rectangle(*args, **kwargs))

    def circle(self, *args, **kwargs) -> None:
        """ Draws a circle.

        This method has the same parameters as `__init__()` method of
        :class:`Circle`.
        """
        self(Circle(*args, **kwargs))
