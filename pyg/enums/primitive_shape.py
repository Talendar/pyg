from enum import Enum

import OpenGL.GL as gl


class PrimitiveShape(Enum):
    """ Encapsulation of a OpenGL primitive shape.

    See:
        https://www.khronos.org/opengl/wiki/Primitive
    """

    #: This will cause OpenGL to interpret each individual vertex in the stream
    #: as a point.
    POINTS = gl.GL_POINTS

    #: Vertices 0 and 1 are considered a line. Vertices 2 and 3 are considered a
    #: line. And so on.
    LINES = gl.GL_LINES

    #: The adjacent vertices are considered lines. Thus, if you pass n vertices,
    #: you will get n-1 lines. If the user only specifies 1 vertex, the drawing
    #: command is ignored.
    LINE_STRIP = gl.GL_LINE_STRIP

    #: As line strips, except that the first and last vertices are also used as
    #: a line. Thus, you get n lines for n input vertices. If the user only
    #: specifies 1 vertex, the drawing command is ignored. The line between the
    #: first and last vertices happens after all of the previous lines in the
    #: sequence.
    LINE_LOOP = gl.GL_LINE_LOOP

    #: Vertices 0, 1, and 2 form a triangle. Vertices 3, 4, and 5 form a
    #: triangle. And so on.
    TRIANGLES = gl.GL_TRIANGLES

    #: Every group of 3 adjacent vertices forms a triangle. The face direction
    #: of the strip is determined by the winding of the first triangle. Each
    #: successive triangle will have its effective face order reversed, so the
    #: system compensates for that by testing it in the opposite way. A vertex
    #: stream of n length will generate n-2 triangles.
    TRIANGLE_STRIP = gl.GL_TRIANGLE_STRIP

    #: The first vertex is always held fixed. From there on, every group of 2
    #: adjacent vertices form a triangle with the first. So with a vertex
    #: stream, you get a list of triangles like so: (0, 1, 2) (0, 2, 3),
    #: (0, 3, 4), etc. A vertex stream of n length will generate n-2 triangles.
    TRIANGLE_FAN = gl.GL_TRIANGLE_FAN
