import glfw


def poll_events() -> None:
    """ Processes the events that are already in the event queue and then
    returns immediately.

    Processing events will cause the window and input callbacks associated with
    those events to be called.
    """
    glfw.poll_events()
