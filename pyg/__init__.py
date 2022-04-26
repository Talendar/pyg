""" Starts `glfw` and defines the library's API.
"""

import glfw

# Start GLFW.
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


# API.
# pylint: disable=[C0413]
from pyg.window import Window
from pyg.enums.events import Key, KeyboardAction
from pyg.enums.fill_mode import FillMode
from pyg.enums.primitive_shape import PrimitiveShape
from pyg import objects
from pyg import utils
