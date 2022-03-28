from __future__ import annotations

import ctypes
import math
from typing import TYPE_CHECKING, Final, Any, Optional, Callable

import OpenGL.GL as gl
import OpenGL.GL.shaders

from .utils import *

if TYPE_CHECKING:
    from .window import Window


#: Default color of the objects.
_DEFAULT_COLOR = np.array([1, 0.5, 0.2, 1])


#: Source code for the vertex shader.
_VERTEX_SHADER_SRC: Final[str] = """
    #version 330 core
    attribute vec2 pos;
    
    void main() {
        gl_Position = vec4(pos.x, pos.y, 0, 1.0);
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
    """ Abstracts the drawing of basic shapes in a window. """

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

    def _draw_primitive(
        self,
        vertices: tuple[Coord2D, ...] | np.ndarray,
        primitive: Any,
        color: Optional[Color | np.ndarray] = None,
        before_draw: Optional[Callable[[], None]] = None,
    ):
        """ Draws a set of vertices using an OpenGL primitive.

        Args:
            vertices: The vertices of the object to be drawn.
            primitive: The OpenGL [primitive](https://www.khronos.org/opengl/wiki/Primitive)
                to be used as a reference to connect the vertices.
            color: The color of the object.
            before_draw: Callback fired just before the actual drawing occurs.
        """
        vertices = normalize_array(vertices)
        color = color if color is not None else _DEFAULT_COLOR

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
                vertices.nbytes,
                vertices,
                gl.GL_DYNAMIC_DRAW,
            )

            # Set our vertex attributes pointers. We're telling OpenGL how it
            # should interpret the vertex data.
            pos_attr_loc = gl.glGetAttribLocation(self._shader_program, "pos")
            gl.glEnableVertexAttribArray(pos_attr_loc)
            gl.glVertexAttribPointer(
                pos_attr_loc,
                2,
                gl.GL_FLOAT,
                False,
                vertices.strides[0],
                ctypes.c_void_p(0),
            )

            # Set the color of our object.
            color_attr_loc = gl.glGetUniformLocation(self._shader_program,
                                                     "color")
            gl.glUniform4f(color_attr_loc, *color)

            # Draw.
            if before_draw is not None:
                before_draw()
            gl.glDrawArrays(primitive, 0, len(vertices))

            # Clean up.
            gl.glDisableVertexAttribArray(pos_attr_loc)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glUseProgram(0)

    def point(self,
              pos: Coord2D | np.ndarray,
              point_size: int = 1,
              color: Optional[Color | np.ndarray] = None) -> None:
        """ Draws a single point at the given position.

        Args:
            pos: The point's coordinates.
            point_size: The point's size. It will be capped at a maximum size
                specified by the current OpenGL's implementation.
            color: The point's color.
        """
        self._draw_primitive(
            vertices=tuple([pos]),
            primitive=gl.GL_POINTS,
            color=color,
            before_draw=lambda: gl.glPointSize(point_size),
        )

    def line(self,
             pos: tuple[Coord2D, Coord2D] | np.ndarray,
             line_width: int = 1,
             color: Optional[Color | np.ndarray] = None) -> None:
        """ Draws a line.

        Args:
            pos: Tuple or numpy array containing the coordinates of two points
                in the line.
            line_width: The width of the line. It will be capped at a maximum
                size specified by the current OpenGL's implementation.
            color: The line's color.
        """
        self._draw_primitive(
            vertices=pos,
            primitive=gl.GL_LINES,
            color=color,
            before_draw=lambda: gl.glLineWidth(line_width),
        )

    def triangle(self,
                 vertices: tuple[Coord2D, Coord2D, Coord2D] | np.ndarray,
                 color: Optional[Color | np.ndarray] = None) -> None:
        """ Draws a triangle from its vertices coordinates.

        Args:
            vertices: The coordinates of the 3 vertices of the triangle.
            color: The triangle's color.
        """
        self._draw_primitive(vertices, gl.GL_TRIANGLES, color)

    def rect(self,
             top_left: Coord2D | np.ndarray,
             size: tuple[float, float],
             color: Optional[Color | np.ndarray] = None) -> None:
        """ Draws a rectangle.

        Args:
            top_left: The coordinates of the rectangle's top-left vertex.
            size: The rectangle's width and height relative to, respectively,
                the window's width and height. Example: passing (0.5, 0.5) to
                this parameter will draw a rectangle with width and height equal
                to, respectively, half of the window's width and height.
            color: The rectangle's color.
        """
        size = np.array(size) * 2
        top_right = (top_left[0] + size[0], top_left[1])
        bottom_right = (top_left[0] + size[0], top_left[1] - size[1])
        bottom_left = (top_left[0], top_left[1] - size[1])

        self._draw_primitive(
            vertices=(
                top_left,
                bottom_left,
                top_right,
                bottom_right,
            ),
            primitive=gl.GL_TRIANGLE_STRIP,
            color=color,
        )

    def circle(self,
               center_pos: Coord2D | np.ndarray,
               radius: float,
               color: Optional[Color | np.ndarray] = None,
               quality_level: int = 64) -> None:
        """ Draws a circle.

        Args:
            center_pos: The coordinates of the circle's center.
            radius: The circle's radius.
            color: The circle's color.
            quality_level: An integer related to the quality of the drawn
                circle. Greater values mean higher quality.
        """
        vertices = []
        inc = 2 * math.pi / quality_level
        for i in range(quality_level):
            angle = i * inc
            x = math.cos(angle) * radius + center_pos[0]
            y = math.sin(angle) * radius + center_pos[1]
            vertices.append((x, y))

        self._draw_primitive(
            vertices=np.array(vertices),
            primitive=gl.GL_TRIANGLE_FAN,
            color=color,
        )
