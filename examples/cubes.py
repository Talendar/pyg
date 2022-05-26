""" View some cubes in a 3D space.
"""

import time
from timeit import default_timer as timer

import pyg


CAMERA_MOV_SPEED = 10
MOUSE_SENSITIVITY = 0.1
SCROLL_SENSITIVITY = 2


if __name__ == "__main__":
    # Create and show a new window.
    window = pyg.Window(1200, 800, depth_testing=True)
    window.name = "Cubes"
    window.camera.movement_speed = CAMERA_MOV_SPEED
    window.camera.mouse_sensitivity = MOUSE_SENSITIVITY
    window.show()

    # Creating the cubes.
    cubes = [
        pyg.objects.Cube(color=(0.1, 0.2, 0.2, 1)),
        pyg.objects.Cube(color=(0.2, 0.2, 0.2, 1)),
        pyg.objects.Cube(color=(0.5, 0.2, 0.25, 1)),
    ]

    # Transforming the cubes.
    cubes[0].transform.scale(sx=2, sy=2, sz=2)
    cubes[1].transform.scale(sx=2, sy=2, sz=2)
    cubes[1].transform.translate(tx=1, tz=-1)
    cubes[2].transform.translate(tx=-1, tz=-0.5)

    # Point in time in which the last frame was rendered.
    last_render = timer()

    # Last recorded position of the mouse's cursor.
    last_cursor_pos = (None, None)

    # Current zoom level of the camera.
    zoom_level = 45

    # Callback to handle keyboard events.
    def handle_key_event(key: pyg.Key, action: pyg.KeyboardAction) -> None:
        if action not in (pyg.KeyboardAction.PRESS, pyg.KeyboardAction.REPEAT):
            return

        try:
            direction = {
                pyg.Key.W: "forward",
                pyg.Key.S: "backward",
                pyg.Key.A: "left",
                pyg.Key.D: "right",
            }[key]
            window.camera.move(direction, dT=timer() - last_render)
        except KeyError:
            pass

    # Callback to handle changes in the cursor's position.
    def handle_cursor_pos_event(x_pos: float, y_pos: float) -> None:
        global last_cursor_pos
        if last_cursor_pos == (None, None):
            last_cursor_pos = (x_pos, y_pos)

        window.camera.incline(x_offset=x_pos - last_cursor_pos[0],
                              y_offset=y_pos - last_cursor_pos[1])
        last_cursor_pos = (x_pos, y_pos)

    # Callback to handle changes in the mouse's scrolling wheel.
    def handle_scroll_event(y_pos: float) -> None:
        global zoom_level
        zoom_level += y_pos * SCROLL_SENSITIVITY
        zoom_level = min(max(zoom_level, 1), 45)
        window.camera.zoom(zoom_level)

    # Add the callbacks.
    window.set_key_callback(handle_key_event)
    window.set_cursor_pos_callback(handle_cursor_pos_event)
    window.set_scroll_callback(handle_scroll_event)

    # Main loop.
    while not window.should_close():
        # Clear the window.
        window.clear(color=(1, 1, 1, 1))

        # Draw the cubes.
        for cube in cubes:
            window.draw(cube)

        # Poll for events and update the window.
        window.poll_events()
        window.update()
        time.sleep(1 / 30)
        last_render = timer()
