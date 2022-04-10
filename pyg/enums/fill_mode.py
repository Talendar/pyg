from enum import Enum

import OpenGL.GL as gl


class FillMode(Enum):
    """ Represents a polygon fill mode in OpenGL.

    See:
        https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glPolygonMode.xhtml
    """

    POINT = gl.GL_POINT
    LINE = gl.GL_LINE
    FILL = gl.GL_FILL
