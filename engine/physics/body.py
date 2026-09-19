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

    # Visuals
    color: tuple[int, int, int]

    # Acceleration
    acceleration: pygame.Vector2 = field(default_factory=pygame.Vector2)

    

    # Rendering
    trail: list[pygame.Vector2] = field(default_factory=list)
    # Trail distances are measured in million kilometres.
    trail_spacing: float = 0.1
    max_trail_distance: float = 100.0
    # Total physical distance currently represented by the trail.
    trail_distance: float = 0.0

    @property
    def speed(self) -> float:
        """Returns the current speed of the body."""
        return self.velocity.length()

    
    def update_trail(self) -> None:
     """
     Updates the body's trail using physical distance.
     """

     if not self.trail:
        self.trail.append(self.position.copy())
        return

     distance = self.position.distance_to(self.trail[-1])

     if distance < self.trail_spacing:
        return

     self.trail.append(self.position.copy())
     self.trail_distance += distance

     while self.trail_distance > self.max_trail_distance:
           removed_distance = self.trail[0].distance_to(self.trail[1])

           self.trail_distance -= removed_distance

           self.trail.pop(0)

    def clear_trail(self) -> None:
        """
        Removes all stored trail points.
        """

        self.trail.clear()
        self.trail_distance = 0.0

    def reset_acceleration(self) -> None:
        """
        Resets the body's acceleration to zero.
        """

        self.acceleration.update(0, 0)                