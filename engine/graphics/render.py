"""
render.py
---------

Handles rendering of simulation bodies using Pygame.

The renderer is responsible only for visual representation.
It does not perform physics calculations or modify simulation state.

Author: Neil
Project: COSMOS
"""

import pygame

from engine.physics.body import Body
from engine.graphics.camera import Camera


class Renderer:
    """
    Renders COSMOS simulation objects onto a Pygame surface.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        camera: Camera,
    ) -> None:
        """
        Creates a renderer.

        Args:
            screen: Pygame surface used for rendering.
            camera: Camera used to transform world coordinates.
        """

        self.screen = screen
        self.camera = camera

    def draw_body(self, body: Body) -> None:
        """
        Draws a single body onto the screen.
        """

        screen_position = self.camera.world_to_screen(body.position)

        radius = max(1, int(body.radius * self.camera.zoom))

        pygame.draw.circle(
            self.screen,
            body.color,
            (int(screen_position.x), int(screen_position.y)),
            radius,
        )

    def draw_trail(self, body: Body) -> None:
        """
        Draws the stored trail of a body.
        """

        if len(body.trail) < 2:
            return

        screen_points = [
            self.camera.world_to_screen(point)
            for point in body.trail
        ]

        screen_points = [
            (int(point.x), int(point.y))
            for point in screen_points
        ]

        pygame.draw.lines(
            self.screen,
            body.color,
            False,
            screen_points,
            1,
        )

    def render_body(self, body: Body) -> None:
        """
        Draws a body's trail and body.
        """

        self.draw_trail(body)
        self.draw_body(body)

    def render(self, bodies: list[Body]) -> None:
        """
        Renders all bodies in the simulation.
        """

        for body in bodies:
            self.render_body(body)
    def draw_hud(
     self,
     hud_data: dict[str, object],
     font: pygame.font.Font,
     position: tuple[int, int] = (10, 10),
     ) -> None:
     """
     Draws HUD information onto the screen.

     Args:
        hud_data: Dictionary containing HUD labels and values.
        font: Font used to render the HUD text.
        position: Starting screen position of the HUD.
     """

     x, y = position

     for i, (label, value) in enumerate(hud_data.items()):
        text = f"{label}: {value}"

        text_surface = font.render(
            text,
            True,
            (255, 255, 255),
        )

        self.screen.blit(
            text_surface,
            (x, y + i * 30),
        )            