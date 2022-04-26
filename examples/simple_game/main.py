""" Simple space exploration game using `pyg`.
"""

import time
from timeit import default_timer as timer

import pyg

import ascii_arts
from game_objects import Spaceship, BlackHole, Planet, Star, Asteroid


_MAX_FPS = 60
_WINDOW_SIZE = (1600, 1000)
_NUM_STARS = 50
_ASTEROID_SPAWN_TIME = 1.5


if __name__ == "__main__":
    # Create and show a new window.
    window = pyg.Window(*_WINDOW_SIZE)
    window.name = "Space exploration"
    window.show()

    # Game objects.
    spaceship = Spaceship()
    black_hole = BlackHole()
    planet = Planet()
    stars = [Star() for _ in range(_NUM_STARS)]
    asteroids = [Asteroid()]

    # Function to handle keyboard events.
    def handle_controls() -> None:
        if window.get_key_state(pyg.Key.RIGHT):
            spaceship.anticlockwise_rotation_engines_on = True
        if window.get_key_state(pyg.Key.LEFT):
            spaceship.clockwise_rotation_engines_on = True
        if window.get_key_state(pyg.Key.UP):
            spaceship.lower_engines_on = True
        if window.get_key_state(pyg.Key.DOWN):
            spaceship.upper_engines_on = True

    # Time references.
    last_update_time = timer()
    last_asteroid_time = timer()

    # Main loop.
    is_game_over = False
    while not window.should_close() and not is_game_over:
        loop_start_time = timer()

        # Handle controls.
        spaceship.shut_down_engines()
        window.poll_events()
        handle_controls()

        # Clear the window.
        window.clear()

        # Update the objects.
        dT = timer() - last_update_time
        spaceship.update(dT, *black_hole.calc_gravitational_pull(spaceship))
        black_hole.update(dT)
        for asteroid in asteroids:
            asteroid.update(dT, *black_hole.calc_gravitational_pull(asteroid))
        last_update_time = timer()

        # Draw the game's objects.
        for star in stars:
            star.render(window)
        for asteroid in asteroids:
            asteroid.render(window)
        planet.render(window)
        black_hole.render(window)
        spaceship.render(window)

        # Handle collisions between asteroids.
        asteroids_indices_to_delete = set()
        for i in range(len(asteroids)):
            if (asteroids[i].is_colliding_with(black_hole)
                    or abs(asteroids[i].x) > 1.1
                    or abs(asteroids[i].y) > 1.1):
                asteroids_indices_to_delete.add(i)
            else:
                for j in range(i + 1, len(asteroids)):
                    if asteroids[i].is_colliding_with(asteroids[j]):
                        asteroids[i].vel_x = -asteroids[i].vel_x
                        asteroids[i].vel_y = -asteroids[i].vel_y
                        asteroids[j].vel_x = -asteroids[j].vel_x
                        asteroids[j].vel_y = -asteroids[j].vel_y
        asteroids = [a for i, a in enumerate(asteroids)
                     if i not in asteroids_indices_to_delete]

        # Check if the spaceship has left the viewport.
        if abs(spaceship.x) > 1.3 or abs(spaceship.y) > 1.3:
            is_game_over = True
            print(f"{ascii_arts.LOSE_ASCII}\n"
                  f"{ascii_arts.SPACE_ASCII}\n\n"
                  "You got lost in space.")
            continue

        # Check if the spaceship reached the planet.
        if spaceship.is_colliding_with(planet):
            is_game_over = True
            if ((spaceship.vel_x**2 + spaceship.vel_y**2) ** 0.5) >= 0.3:
                print(f"{ascii_arts.LOSE_ASCII}\n\n"
                      f"{ascii_arts.EXPLOSION_ASCII}\n\n"
                      "You've reached an habitable planet in Alpha Centauri, "
                      "but you were too fast and didn't survive the landing.")
                continue
            print(f"{ascii_arts.WIN_ASCII}\n\n"
                  f"{ascii_arts.PLANET_ASCII}\n\n"
                  "You've reached an habitable planet in Alpha Centauri!")
            continue

        # Check if the spaceship entered the black hole.
        if spaceship.is_colliding_with(black_hole):
            is_game_over = True
            print(f"{ascii_arts.LOSE_ASCII}\n"
                  f"{ascii_arts.BLACK_HOLE_ASCII}\n"
                  "Your spaceship was lost in a black hole.")
            continue

        # Check if the spaceship collided with an asteroid.
        for asteroid in asteroids:
            if spaceship.is_colliding_with(asteroid):
                is_game_over = True
        if is_game_over:
            print(f"{ascii_arts.LOSE_ASCII}\n"
                  f"{ascii_arts.ASTEROID_ASCII}\n"
                  "Your spaceship collided with an asteroid.")
            continue

        # Spawn new asteroids.
        if (timer() - last_asteroid_time) >= _ASTEROID_SPAWN_TIME:
            asteroids.append(Asteroid())
            last_asteroid_time = timer()

        # Update the window.
        window.update()

        # Enforce the FPS limit.
        loop_dT = timer() - loop_start_time
        waiting_time = (1 / _MAX_FPS) - loop_dT
        time.sleep(max(waiting_time, 0))

        # Display FPS.
        window.name = (f"FPS: "
                       f"{_MAX_FPS if waiting_time > 0 else (1 / loop_dT):.1f}")
