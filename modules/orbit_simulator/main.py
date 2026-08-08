"""
Orbit simulation module for COSMOS.

Uses the COSMOS engine for physics and graphics.

Author: Neil
Project: COSMOS
"""

import pygame

from engine.physics.body import Body
from engine.physics.integrators import VelocityVerletIntegrator

from engine.graphics.colors import SpaceColors
from engine.graphics.camera import Camera
from engine.graphics.hud import HUD
from engine.graphics.render import Renderer


# --------------------------------------------------
# Pygame Initialization
# --------------------------------------------------

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COSMOS - Orbit Simulator")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)


# --------------------------------------------------
# COSMOS Systems
# --------------------------------------------------

# Initialize the reusable COSMOS engine components.
camera = Camera(
    screen_size=(WIDTH, HEIGHT),
    position=pygame.Vector2(0, 0),
    zoom=1,
)

renderer = Renderer(
    screen=screen,
    camera=camera,
)

hud = HUD()

# Velocity Verlet is currently used for the orbital simulation.
integrator = VelocityVerletIntegrator()


# --------------------------------------------------
# Simulation Settings
# --------------------------------------------------

TIME_SCALE = 1
time_scale = TIME_SCALE

paused = False


# --------------------------------------------------
# Notifications
# --------------------------------------------------

current_notif = "UNIVERSE INITIATED"
notif_time = 2.0


def show_notif(message: str) -> None:
    """
    Displays a temporary Orbit Simulator notification.
    """

    global current_notif, notif_time

    current_notif = message
    notif_time = 2.0


# --------------------------------------------------
# Solar System
# --------------------------------------------------

def create_bodies() -> list[Body]:
    """
    Creates the initial Solar System configuration.

    Returns:
        list[Body]: Bodies used by the simulation.
    """

    return [
        # Central star
        Body(
            name="Sun",
            mass=332946.05,
            radius=25,
            position=pygame.Vector2(0, 0),
            velocity=pygame.Vector2(-0.00120529, -0.00004326),
            color=SpaceColors.YELLOW,
        ),

        # Inner planets
        Body(
            name="Mercury",
            mass=0.0553,
            radius=5,
            position=pygame.Vector2(43.6778, 15.8974),
            velocity=pygame.Vector2(-1.4455, 4.8405),
            color=SpaceColors.GRAY,
        ),

        Body(
            name="Venus",
            mass=0.815,
            radius=7,
            position=pygame.Vector2(27.9561, 104.3334),
            velocity=pygame.Vector2(-2.9228, 0.8037),
            color=SpaceColors.ORANGE,
        ),

        Body(
            name="Earth",
            mass=1,
            radius=8,
            position=pygame.Vector2(-116.0514, 97.3787),
            velocity=pygame.Vector2(-1.6544, -1.9286),
            color=SpaceColors.BLUE,
        ),

        Body(
            name="Mars",
            mass=0.107,
            radius=6,
            position=pygame.Vector2(-212.9156, -122.9269),
            velocity=pygame.Vector2(1.0469, -1.6178),
            color=SpaceColors.RED,
        ),

        # Outer planets
        Body(
            name="Jupiter",
            mass=317.828,
            radius=14,
            position=pygame.Vector2(-136.0132, -771.3689),
            velocity=pygame.Vector2(1.1123, -0.1409),
            color=SpaceColors.ORANGE,
        ),

        Body(
            name="Saturn",
            mass=95.159,
            radius=12,
            position=pygame.Vector2(970.5966, -970.5966),
            velocity=pygame.Vector2(0.5891, 0.6361),
            color=SpaceColors.GREEN,
        ),

        Body(
            name="Uranus",
            mass=14.536,
            radius=10,
            position=pygame.Vector2(2382.0946, 1375.3030),
            velocity=pygame.Vector2(-0.2942, 0.5369),
            color=SpaceColors.CYAN,
        ),

        Body(
            name="Neptune",
            mass=17.147,
            radius=10,
            position=pygame.Vector2(-4541.1308, 0),
            velocity=pygame.Vector2(0, -0.4649),
            color=SpaceColors.BLUE,
        ),
    ]


bodies = create_bodies()


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

running = True

while running:

    # ----------------------------------------------
    # Time
    # ----------------------------------------------

    # Convert real-time frame duration into simulation time.
    dt = clock.tick(60) / 1000
    sim_dt = dt * time_scale

    if notif_time > 0:
        notif_time -= dt


    # ----------------------------------------------
    # Events
    # ----------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Pause / resume simulation
            if event.key == pygame.K_SPACE:
                paused = not paused

                if paused:
                    show_notif(
                        "STAR PLATINUM: THE WORLD (TIME STOP)!!!"
                    )
                else:
                    show_notif(
                        "TIME MOVES AGAIN!!!"
                    )

            # Reset simulation to its initial state
            if event.key == pygame.K_r:
                bodies = create_bodies()
                camera.position.update(0, 0)
                camera.set_zoom(0.25)
                time_scale = TIME_SCALE

                show_notif(
                    "MADE IN HEAVEN: UNIVERSE RESET!!!"
                )

            # Increase simulation time scale
            if event.key == pygame.K_UP:
                time_scale += 10

                show_notif(
                    "MADE IN HEAVEN: TIME ACCELERATION!!!"
                )

            # Decrease simulation time scale
            if event.key == pygame.K_DOWN:
                time_scale = max(10, time_scale - 10)

                show_notif(
                    "MADE IN HEAVEN: TIME DECELERATION!!!"
                )

            # Quickly switch to a faster simulation speed
            if event.key == pygame.K_m:
                time_scale = 80

                show_notif(
                    "MADE IN HEAVEN: TIME FLIES!!!"
                )

            # Return to real-time simulation
            if event.key == pygame.K_n:
                time_scale = 1

                show_notif(
                    "MADE IN HEAVEN: TIME RETURNS!!!"
                )


    # ----------------------------------------------
    # Camera Controls
    # ----------------------------------------------

    keys = pygame.key.get_pressed()

    movement = pygame.Vector2()

    if keys[pygame.K_w]:
        movement.y -= 1

    if keys[pygame.K_s]:
        movement.y += 1

    if keys[pygame.K_a]:
        movement.x -= 1

    if keys[pygame.K_d]:
        movement.x += 1

    # Prevent diagonal movement from being faster.
    if movement.length_squared() > 0:
        movement = movement.normalize()

    camera.update(
        movement=movement,
        dt=dt,
        movement_speed=500,
    )


    # Zoom controls
    zoom_factor = 1.0

    if keys[pygame.K_o]:
        zoom_factor = 0.99

    if keys[pygame.K_i]:
        zoom_factor = 1.01

    if zoom_factor != 1.0:
        camera.update(
            movement=pygame.Vector2(),
            zoom_factor=zoom_factor,
            dt=dt,
        )


    # ----------------------------------------------
    # Physics
    # ----------------------------------------------

    # The integrator handles gravity, numerical integration,
    # and trail updates for the active bodies.
    if not paused:
        integrator.step(bodies, sim_dt)


    # ----------------------------------------------
    # Rendering
    # ----------------------------------------------

    screen.fill(SpaceColors.BLACK)

    renderer.render(bodies)


    # ----------------------------------------------
    # HUD
    # ----------------------------------------------

    # HUD data belongs to the Orbit Simulator module.
    # The HUD engine component only handles displaying it.
    hud.clear()

    hud.set("FPS", f"{clock.get_fps():.1f}")
    hud.set("Bodies", len(bodies))
    hud.set("Zoom", f"{camera.zoom:.2f}x")
    hud.set("Time Scale", f"{time_scale}x")
    hud.set(
        "State",
        "ZA WARUDO (Paused)" if paused else "Running",
    )
    hud.set("Integrator", "Velocity Verlet")

    renderer.draw_hud(
        hud.get_data(),
        font,
    )


    # ----------------------------------------------
    # Notifications
    # ----------------------------------------------

    if notif_time > 0:

        notif_surface = font.render(
            current_notif,
            True,
            SpaceColors.WHITE,
        )

        notif_width = notif_surface.get_width()

        notif_x = int(
            (WIDTH - notif_width) / 2
        )

        screen.blit(
            notif_surface,
            (notif_x, 30),
        )


    # ----------------------------------------------
    # Display
    # ----------------------------------------------

    pygame.display.flip()


pygame.quit()