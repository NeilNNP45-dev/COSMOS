"""
Provides energy calculations for physical systems.

Author: Neil
Project: COSMOS
"""

from engine.physics.body import Body
from engine.physics.constants import G


def calculate_kinetic_energy(body: Body) -> float:
    """
    Calculates the kinetic energy of a body.
    """

    # KE = 1/2 * m * v²
    ke = 0.5 * body.mass * body.speed ** 2

    return ke


def calculate_potential_energy(
    body1: Body,
    body2: Body,
) -> float:
    """
    Calculates the gravitational potential energy
    between two bodies.
    """

    # Calculate the distance between the two bodies.
    r = (body1.position - body2.position).length()

    # PE = -(G * m1 * m2) / r
    pe = -(G * body1.mass * body2.mass) / r

    return pe


def calculate_total_energy(bodies: list[Body]) -> float:
    """
    Calculates the total mechanical energy
    of the system.
    """

    total_ke = 0.0
    total_pe = 0.0

    # Add the kinetic energy of every body.
    for body in bodies:
        total_ke += calculate_kinetic_energy(body)

    # Calculate gravitational potential energy
    # for each unique pair of bodies.
    for i, body1 in enumerate(bodies):
        for body2 in bodies[i + 1:]:
            total_pe += calculate_potential_energy(
                body1,
                body2,
            )

    # Total mechanical energy is the sum of
    # kinetic and gravitational potential energy.
    total_energy = total_ke + total_pe

    return total_energy