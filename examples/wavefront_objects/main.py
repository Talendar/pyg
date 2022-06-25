""" Load and display Wavefront objects using `pyg`.
"""

import time
from timeit import default_timer as timer

import pyg


CAMERA_MOV_SPEED = 10
MOUSE_SENSITIVITY = 0.2
SCROLL_SENSITIVITY = 2


if __name__ == "__main__":
    # Create and show a new window.
    window = pyg.Window(1200, 800, depth_testing=True)
    window.name = "Wavefront OBJs"
    window.camera.movement_speed = CAMERA_MOV_SPEED
    window.camera.mouse_sensitivity = MOUSE_SENSITIVITY
    window.show()

    # Loading the objects.
    cube = pyg.objects.SimpleGraphicObject(
        vertices=pyg.utils.load_wavefront("objs/cube.obj", vertices_only=True),
        primitive=pyg.PrimitiveShape.TRIANGLES,
        color=(0, 0, 0, 0),
    )
    cube.transform.scale(sx=0.1, sy=0.1, sz=0.1)
    cube.transform.translate(tx=-0.5)

    dragon = pyg.objects.SimpleGraphicObject(
        vertices=pyg.utils.load_wavefront("objs/dragon.obj",
                                          vertices_only=True),
        primitive=pyg.PrimitiveShape.TRIANGLES,
        color=(0.7, 0.1, 0.1, 1),
    )
    dragon.transform.scale(sx=0.16, sy=0.16, sz=0.16)
    dragon.transform.translate(tz=-2)

    male = pyg.objects.SimpleGraphicObject(
        vertices=pyg.utils.load_wavefront("objs/male.obj",
                                          vertices_only=True),
        primitive=pyg.PrimitiveShape.TRIANGLES,
        color=(0.33, 0.33, 0.25, 1),
    )
    male.transform.scale(sx=0.02, sy=0.02, sz=0.02)
    male.transform.rotate(angle=180, axis="y")

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
            last_cursor_pos = (window.size[0] / 2, window.size[1] / 2)

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

        # Draw the objects.
        window.draw(cube)
        window.draw(dragon)
        window.draw(male)

        # Poll for events and update the window.
        window.poll_events()
        window.update()
        time.sleep(1 / 30)
        last_render = timer()
