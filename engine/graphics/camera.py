"""
camera.py
---------

Provides the Camera class used by the COSMOS rendering system.

The Camera converts between simulation/world coordinates and
screen coordinates while supporting camera movement and zoom.

Author: Neil
Project: COSMOS
"""

import pygame


class Camera:
    """
    Represents the viewport into the simulation world.
    """

    def __init__(
        self,
        screen_size: tuple[int, int],
        position: pygame.Vector2 | None = None,
        zoom: float = 1.0,
    ) -> None:
        """
        Creates a camera.

        Args:
            screen_size: Width and height of the screen in pixels.
            position: Camera position in world coordinates.
            zoom: Initial zoom level.
        """

        self.screen_width, self.screen_height = screen_size

        self.position = position.copy() if position else pygame.Vector2()
        self.zoom = zoom

    def world_to_screen(self, world_position: pygame.Vector2) -> pygame.Vector2:
        """
        Converts a world position into a screen position.
        """

        offset = world_position - self.position
        screen_center = pygame.Vector2(
            self.screen_width / 2,
            self.screen_height / 2,
        )

        return screen_center + offset * self.zoom

    def screen_to_world(self, screen_position: pygame.Vector2) -> pygame.Vector2:
        """
        Converts a screen position into a world position.
        """

        screen_center = pygame.Vector2(
            self.screen_width / 2,
            self.screen_height / 2,
        )

        return self.position + (screen_position - screen_center) / self.zoom

    def move(self, offset: pygame.Vector2) -> None:
        """
        Moves the camera by a world-space offset.
        """

        self.position += offset

    def set_zoom(self, zoom: float) -> None:
        """
        Sets the camera zoom level.

        Zoom must be greater than zero.
        """

        if zoom <= 0:
            raise ValueError("Zoom must be greater than zero.")

        self.zoom = zoom
    def update(
     self,
     movement: pygame.Vector2,
     zoom_factor: float = 1.0,
     dt: float = 1 / 60,
     movement_speed: float = 500.0,
     ) -> None:
     """
     Updates the camera position and zoom.

     Args:
        movement: Normalized movement direction.
        zoom_factor: Multiplicative zoom factor.
        dt: Delta time in seconds.
        movement_speed: Camera movement speed in world units per second.
     """

     self.move(movement * movement_speed * dt)

     if zoom_factor != 1.0:
        self.set_zoom(self.zoom * zoom_factor)    