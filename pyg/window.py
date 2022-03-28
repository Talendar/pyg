from __future__ import annotations
from typing import Optional
from types import TracebackType

import glfw
import OpenGL.GL as gl

from .drawer import Drawer


class Window:
    """ Represents a window in the application.

    In most scenarios, you will only need a single window for the app. Creating
    multiple windows in a single process might cause undefined behaviour. If
    multiple windows are needed, instantiate them in different processes (one
    window per process).
    """

    def __init__(self, width: int, height: int, name: str = "My app") -> None:
        self._name = name
        self._glfw_window = glfw.create_window(width, height, name, None, None)

        # Tell OpenGL the initial size of the window.
        gl.glViewport(0, 0, width, height)

        # Set up a callback to update OpenGL's viewport when the window is
        # resized.
        def win_resize_callback(_, new_width: int, new_height: int) -> None:
            gl.glViewport(0, 0, new_width, new_height)
            self.clear(tuple(gl.glGetFloatv(gl.GL_COLOR_CLEAR_VALUE)))
            self.update()

        glfw.set_framebuffer_size_callback(self._glfw_window,
                                           win_resize_callback)

        # Instantiate a drawer.
        self._drawer = Drawer(self)

    @property
    def size(self) -> tuple[int, int]:
        return glfw.get_window_size(self._glfw_window)

    @property
    def name(self) -> str:
        return self._name

    @property
    def draw(self) -> Drawer:
        return self._drawer

    @size.setter
    def size(self, new_size: tuple[int, int]) -> None:
        glfw.set_window_size(self._glfw_window, *new_size)

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name
        glfw.set_window_title(self._glfw_window, self._name)

    def __enter__(self) -> Window:
        """ Makes this window the current OpenGL context. """
        glfw.make_context_current(self._glfw_window)
        return self

    def __exit__(self,
                 exc_type: Optional[type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        """ Doesn't do anything.

        This method is only here for the sake of completeness.
        """

    def update(self) -> None:
        """ Updates the window.

        When drawing on the window inside a loop, this should be called in every
        iteration. When the window is resized, this method is automatically
        called.
        """
        glfw.swap_buffers(self._glfw_window)

    def show(self) -> None:
        """ Shows the window. """
        glfw.show_window(self._glfw_window)

    def destroy(self) -> None:
        """ Destroys the window. """
        glfw.destroy_window(self._glfw_window)
        self._glfw_window = None

    def should_close(self) -> bool:
        """ Returns `True` if the window has been instructed to close. """
        return glfw.window_should_close(self._glfw_window)

    def clear(self,
              color: tuple[int, int, int, int] = (0, 0, 0, 1)) -> None:
        """ Clears the screen using the given color. """
        with self:
            gl.glClearColor(*color)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
