"""
gravity.py
----------

Handles Newtonian gravitational interactions between bodies.

This module calculates the gravitational acceleration acting on
each Body in a simulation. It does not update positions or
velocities; that responsibility belongs to the integrators.

Author: Neil
Project: COSMOS
"""

from engine.physics.body import Body
from engine.physics.constants import G


def apply_gravity(bodies: list[Body]) -> None:
    """
    Calculates and applies gravitational acceleration between all
    bodies in the simulation.

    Accelerations are reset before calculation. Each pair of bodies
    is processed only once using Newton's Third Law.
    """

    # Reset accelerations
    for body in bodies:
        body.reset_acceleration()

    # Apply gravitational acceleration
    for i in range(len(bodies)):
        body_a = bodies[i]

        for j in range(i + 1, len(bodies)):
            body_b = bodies[j]

            offset = body_b.position - body_a.position
            distance_squared = offset.length_squared()

            # Prevent division by zero
            if distance_squared == 0:
                continue

            direction = offset.normalize()

            acceleration_a = direction * (G * body_b.mass / distance_squared)
            acceleration_b = direction * (G * body_a.mass / distance_squared)

            body_a.acceleration += acceleration_a
            body_b.acceleration -= acceleration_b