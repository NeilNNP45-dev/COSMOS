"""
body.py
-------

Defines the Body class used throughout the COSMOS Engine.

A Body represents any physical object that exists within a simulation.

It stores only the physical properties of the object and does not
perform physics calculations or rendering.

Author: Neil
Project: COSMOS
"""

from dataclasses import dataclass, field
import pygame


@dataclass(slots=True)
class Body:
    """
    Represents a physical body in a simulation.
   
    A Body stores only its physical state. It does not perform
    physics calculations or rendering.
    """

    # Identification
    name: str

    # Physical Properties
    mass: float
    radius: float

    # Motion
    position: pygame.Vector2
    velocity: pygame.Vector2
    acceleration: pygame.Vector2 = field(default_factory=pygame.Vector2)

    # Visuals
    color: tuple[int, int, int]

    # Rendering
    trail: list[pygame.Vector2] = field(default_factory=list)
    max_trail_length: int = 500

    @property
    def speed(self) -> float:
        """Returns the current speed of the body."""
        return self.velocity.length()

    
    def add_trail_point(self) -> None:
        """
        Adds the current position to the body's trail.
        """

        self.trail.append(self.position.copy())

        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)


    def clear_trail(self) -> None:
        """
        Removes all stored trail points.
        """

        self.trail.clear()


    def reset_acceleration(self) -> None:
        """
        Resets the body's acceleration to zero.
        """

        self.acceleration.update(0, 0)                