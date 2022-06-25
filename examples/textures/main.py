""" Use `pyg` to load and display Wavefront objects with textures.
"""

import time
from timeit import default_timer as timer

import pyg


CAMERA_MOV_SPEED = 25
MOUSE_SENSITIVITY = 0.2
SCROLL_SENSITIVITY = 2


if __name__ == "__main__":
    # Create and show a new window.
    window = pyg.Window(1200, 800, depth_testing=True, use_textures=True)
    window.name = "Textures"
    window.camera.movement_speed = CAMERA_MOV_SPEED
    window.camera.mouse_sensitivity = MOUSE_SENSITIVITY
    window.show()

    # Loading objects.
    box = pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objs/box.obj",
        texture_img_path="objs/box.jpg",
    )
    box.transform.scale(sx=0.5, sy=0.5, sz=0.5)
    box.transform.translate(tz=-1)

    terrain = pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objs/terrain.obj",
        texture_img_path="objs/terrain.jpg",
    )
    terrain.transform.scale(sx=20, sy=20, sz=20)
    terrain.transform.translate(ty=-0.51)

    house = pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objs/house.obj",
        texture_img_path="objs/house.jpg",
    )
    house.transform.translate(ty=-0.5)

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
        window.draw(box)
        window.draw(terrain)
        window.draw(house)

        # Poll for events and update the window.
        window.poll_events()
        window.update()
        time.sleep(1 / 30)
        last_render = timer()
