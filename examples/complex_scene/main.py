""" Use `pyg` to draw a complex 3D scene.
"""

import time
from timeit import default_timer as timer

import pyg

CAMERA_MOV_SPEED = 1
MOUSE_SENSITIVITY = 0.2
SCROLL_SENSITIVITY = 2
DOG_SPEED = 500


def make_tree(x: float,
              y: float,
              z: float) -> pyg.objects.TexturizedGraphicObject:
    t = pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/tree/tree.obj",
        texture_img_path="objects/tree/tree.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    )
    t.transform.rotate(-90, axis="x")
    t.transform.scale(sx=0.00175, sy=0.00175, sz=0.00175)
    t.transform.translate(tx=x, ty=y, tz=z)
    return t


if __name__ == "__main__":
    # Create and show a new window.
    window = pyg.Window(1200, 800, depth_testing=True, use_textures=True)
    window.name = "Complex Scene"
    window.camera.movement_speed = CAMERA_MOV_SPEED
    window.camera.mouse_sensitivity = MOUSE_SENSITIVITY
    window.camera.move("backward", 1)
    window.show()

    objects = []

    # House.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/house/house.obj",
        texture_img_path="objects/house/house.png",
    ))
    objects[-1].transform.rotate(270, axis="y")
    objects[-1].transform.scale(sx=0.5, sy=0.5, sz=0.5)
    objects[-1].transform.translate(ty=-0.6, tz=-3)

    # Table.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/table/table.obj",
        texture_img_path="objects/table/table.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(270, axis="x")
    objects[-1].transform.rotate(270, axis="y")
    objects[-1].transform.scale(sx=0.00275, sy=0.00275, sz=0.00275)
    objects[-1].transform.translate(tz=-3, ty=-0.5)

    # Chair.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/chair/chair.obj",
        texture_img_path="objects/chair/chair.png",
        # primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.scale(sx=0.3, sy=0.3, sz=0.3)
    objects[-1].transform.translate(tz=-3.25, ty=-0.5)

    # Apple.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/apple/apple.obj",
        texture_img_path="objects/apple/apple.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.scale(sx=0.07, sy=0.07, sz=0.07)
    objects[-1].transform.translate(tz=-3, tx=-0.1, ty=-0.29)

    # Bread.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/bread/bread.obj",
        texture_img_path="objects/bread/bread.png",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(55, axis="y")
    objects[-1].transform.scale(sx=0.07, sy=0.07, sz=0.07)
    objects[-1].transform.translate(tz=-3, tx=0.1, ty=-0.29)

    # Trees.
    objects.append(make_tree(x=2, y=-0.65, z=0))
    objects.append(make_tree(x=-2, y=-0.65, z=0))
    objects.append(make_tree(x=-4, y=-0.65, z=-2))
    objects.append(make_tree(x=4, y=-0.65, z=-2))
    objects.append(make_tree(x=-3, y=-0.65, z=3.1))
    objects.append(make_tree(x=4.57, y=-0.65, z=3))
    objects.append(make_tree(x=3.25, y=-0.65, z=4))
    objects.append(make_tree(x=-1.7, y=-0.65, z=4.25))
    objects.append(make_tree(x=-1.9, y=-0.65, z=-4.25))
    objects.append(make_tree(x=2.5, y=-0.65, z=-4))

    # Dead trees.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/dead_tree/dead_tree.obj",
        texture_img_path="objects/dead_tree/dead_tree.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.scale(sx=0.03, sy=0.03, sz=0.03)
    objects[-1].transform.translate(tx=1.75, ty=-0.45, tz=2)

    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/dead_tree/dead_tree.obj",
        texture_img_path="objects/dead_tree/dead_tree.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.scale(sx=0.04, sy=0.04, sz=0.04)
    objects[-1].transform.translate(tx=-1.85, ty=-0.45, tz=1.4)

    # Flowers.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/flower/flower.obj",
        texture_img_path="objects/flower/flower.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(270, axis="x")
    objects[-1].transform.scale(sx=0.0032, sy=0.0032, sz=0.0032)
    objects[-1].transform.translate(tx=-0.05, ty=-0.56, tz=-1.32)

    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/flower/flower.obj",
        texture_img_path="objects/flower/flower.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(270, axis="x")
    objects[-1].transform.scale(sx=0.0032, sy=0.0032, sz=0.0032)
    objects[-1].transform.translate(tx=-0.25, ty=-0.56, tz=-1.32)

    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/flower/flower.obj",
        texture_img_path="objects/flower/flower.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(270, axis="x")
    objects[-1].transform.scale(sx=0.0032, sy=0.0032, sz=0.0032)
    objects[-1].transform.translate(tx=-0.45, ty=-0.56, tz=-1.32)

    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/flower/flower.obj",
        texture_img_path="objects/flower/flower.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(270, axis="x")
    objects[-1].transform.scale(sx=0.0032, sy=0.0032, sz=0.0032)
    objects[-1].transform.translate(tx=0.83, ty=-0.56, tz=-1.32)

    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/flower/flower.obj",
        texture_img_path="objects/flower/flower.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.rotate(270, axis="x")
    objects[-1].transform.scale(sx=0.0032, sy=0.0032, sz=0.0032)
    objects[-1].transform.translate(tx=1.03, ty=-0.56, tz=-1.32)

    # Dog.
    dog_z_pos = 0.0
    dog = pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/dog/dog.obj",
        texture_img_path="objects/dog/dog.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    )
    dog.transform.rotate(270, axis="x")
    dog.transform.scale(sx=0.01, sy=0.01, sz=0.01)
    dog.transform.translate(tx=0, ty=-0.6, tz=0)
    objects.append(dog)

    # Sun.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/sun/sun.obj",
        texture_img_path="objects/sun/sun.jpg",
        primitive=pyg.PrimitiveShape.TRIANGLE_STRIP,
    ))
    objects[-1].transform.scale(sx=0.0025, sy=0.0025, sz=0.0025)
    objects[-1].transform.translate(ty=20)

    # Grass.
    objects.append(pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/terrain.obj",
        texture_img_path="objects/grass.jpg",
    ))
    objects[-1].transform.translate(ty=-0.6)
    objects[-1].transform.scale(sx=6, sz=6)

    # Stone floor.
    objects.append((pyg.objects.TexturizedGraphicObject.from_file(
        file_path="objects/terrain.obj",
        texture_img_path="objects/stone_floor.jpg",
    )))
    objects[-1].transform.translate(tz=-2.3, ty=-0.59)
    objects[-1].transform.scale(sx=1.3, sz=1.3)
    for i in range(16):
        objects.append(pyg.objects.TexturizedGraphicObject.from_file(
            file_path="objects/terrain.obj",
            texture_img_path="objects/stone_floor.jpg",
        ))
        objects[-1].transform.translate(tx=1.7, tz=2 * i - 8, ty=-0.59)
        objects[-1].transform.scale(sx=0.25, sz=0.25)

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

            # Limit the camera's movement.
            window.camera._pos[0] = max(min(window.camera._pos[0], 5), -5)
            window.camera._pos[1] = max(min(window.camera._pos[1], 10), -0.5)
            window.camera._pos[2] = max(min(window.camera._pos[2], 5), -5)
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
        window.clear(color=(0.407, 0.612, 0.8, 1))

        # Move the dog.
        if dog_z_pos > 4.25 or dog_z_pos < -0.25:
            DOG_SPEED *= -1
            dog_tz = max(min(dog_z_pos, 4.25), -0.25) - dog_z_pos
        else:
            dog_tz = DOG_SPEED * (timer() - last_render)
        dog_z_pos += dog_tz
        dog.transform.translate(tz=dog_tz)

        # Draw the objects.
        for obj in objects:
            window.draw(obj)

        # Poll for events and update the window.
        window.poll_events()
        window.update()
        time.sleep(1 / 30)
        last_render = timer()
