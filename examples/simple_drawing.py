import pyg
import time


if __name__ == "__main__":
    window = pyg.Window(700, 700)
    window.show()

    time_count = 0
    while not window.should_close():
        window.name = f"Elapsed time: {time_count:.1f}s"

        # Draw arms.
        window.draw.line(((0, 0.5), (0.6, -0.1)),
                         line_width=12,
                         color=(0, 0, 1, 1))
        window.draw.line(((0, 0.5), (-0.6, -0.1)),
                         line_width=12,
                         color=(0, 0, 1, 1))

        # Draw body.
        window.draw.triangle((
            (0, 0.6),
            (-0.5, -0.4),
            (0.5, -0.4)
        ), color=(1, 0, 0, 1))

        # Draw head and eyes.
        window.draw.circle((0, 0.75), radius=0.25, color=(1, 1, 1, 1))
        window.draw.point((-0.1, 0.8), 12, color=(0, 0, 0, 1))
        window.draw.point((0.1, 0.8), 12, color=(0, 0, 0, 1))

        # Draw legs.
        window.draw.rect((-0.225, -0.4), (0.075, 0.5), color=(0, 1, 0, 1))
        window.draw.rect((0.075, -0.4), (0.075, 0.5), color=(0, 1, 0, 1))

        # Poll for events and update the window.
        pyg.poll_events()
        window.update()

        time.sleep(0.1)
        time_count += 0.1
