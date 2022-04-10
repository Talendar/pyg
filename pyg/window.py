from __future__ import annotations

from typing import Optional, Any
from types import TracebackType
from collections.abc import Callable

import glfw
import OpenGL.GL as gl

from .drawer import Drawer
from pyg.enums.events import Key, KeyboardAction


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

    def poll_events(self) -> None:
        """ Processes the events that are already in the event queue, then
        returns immediately.

        This method is the best choice when rendering continuously, like most
        games do. Processing events will cause the window and input callbacks
        associated with those events to be called.
        """
        with self:
            glfw.poll_events()

    def wait_events(self) -> None:
        """ Puts the current thread to sleep until at least one event has been
        received, then processes all received events.

        If you only need to update the contents of the window when you receive
        new input, this method is a better choice than `Window.poll_events()`.
        This method saves a great deal of CPU cycles and is useful for, for
        example, editing tools.
        """
        with self:
            glfw.wait_events()

    def wait_events_timeout(self, timeout: float) -> None:
        """ Puts the current thread to sleep until at least one event has been
        received or until the specified number of seconds have elapsed. It then
        processes any received events.

        If you want to wait for events but have UI elements or other tasks that
        need periodic updates, this method lets you specify a timeout.

        Args:
            timeout: The maximum waiting time, in seconds.
        """
        with self:
            glfw.wait_events_timeout(timeout)

    def post_empty_event(self) -> None:
        """ Posts an empty event to wake up a thread put to sleep by
        `Window.wait_events()` or `Window.wait_events_timeout()`
        """
        with self:
            glfw.post_empty_event()

    def set_key_callback(
            self,
            callback: Callable[[Key, KeyboardAction], None],
    ) -> None:
        """ Set up a callback to be fired when a physical key is pressed or
        released or when it repeats.
        """
        def callback_wrapper(glfw_window: Any,
                             key: int,
                             scancode: int,
                             action: int,
                             mods: int) -> None:
            callback(Key(key), KeyboardAction(action))

        glfw.set_key_callback(self._glfw_window, callback_wrapper)
