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


#: Source code for the vertex shader.
_VERTEX_SHADER_SRC: Final[str] = """
    #version 330 core
    
    attribute vec3 pos;
    uniform mat4 transform;
    
    void main() {
        gl_Position = transform * vec4(pos, 1.0);
    }
"""

#: Source code for the fragment shader.
_FRAGMENT_SHADER_SRC: Final[str] = """
    #version 330 core
    uniform vec4 color;
    
    void main() {
        gl_FragColor = color;
    } 
"""


class Drawer:
    """ Abstracts the drawing of basic shapes in a :class:`Window`. """

    def __init__(self, window: Window) -> None:
        self._window = window
        with self._window:
            # Vertex buffer and array objects.
            self._vbo = gl.glGenBuffers(1)
            self._vao = gl.glGenVertexArrays(1)

            # Compile the vertex shader.
            self._vertex_shader = gl.shaders.compileShader(
                _VERTEX_SHADER_SRC,
                gl.GL_VERTEX_SHADER,
            )

            # Compile the fragment shader.
            self._fragment_shader = gl.shaders.compileShader(
                _FRAGMENT_SHADER_SRC,
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
            pos_attr_loc = gl.glGetAttribLocation(self._shader_program, "pos")
            gl.glEnableVertexAttribArray(pos_attr_loc)
            gl.glVertexAttribPointer(
                pos_attr_loc,
                3,
                gl.GL_FLOAT,
                False,
                obj.vertices.strides[0],
                ctypes.c_void_p(0),
            )

            # Set the transformation matrix.
            transform_attr_loc = gl.glGetUniformLocation(self._shader_program,
                                                         "transform")
            gl.glUniformMatrix4fv(
                transform_attr_loc, 1, gl.GL_TRUE, obj.transform.matrix,
            )

            # Set the color of our object.
            color_attr_loc = gl.glGetUniformLocation(self._shader_program,
                                                     "color")
            gl.glUniform4f(color_attr_loc, *obj.color)

            # Specify how the object should be filled.
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, obj.fill_mode.value)

            # Draw.
            if obj.on_draw is not None:
                obj.on_draw()
            gl.glDrawArrays(obj.primitive.value, 0, len(obj.vertices))

            # Clean up.
            gl.glDisableVertexAttribArray(pos_attr_loc)
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
