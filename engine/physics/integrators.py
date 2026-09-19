"""
integrators.py
--------------

Provides numerical integration methods used to advance
a simulation through time.

Author: Neil
Project: COSMOS
"""

from abc import ABC, abstractmethod

from engine.physics.body import Body
from engine.physics.gravity import apply_gravity


class Integrator(ABC):
    """
    Abstract base class for all numerical integrators.
    """

    @abstractmethod
    def step(self, bodies: list[Body], dt: float) -> None:
        """
        Advances the simulation by one timestep.
        """
        raise NotImplementedError


class EulerIntegrator(Integrator):
    """
    First-order Euler integrator.
    """

    def step(self, bodies: list[Body], dt: float) -> None:

        apply_gravity(bodies)

        for body in bodies:
            body.velocity += body.acceleration * dt
            body.position += body.velocity * dt

            body.update_trail()


class VelocityVerletIntegrator(Integrator):
    """
    Second-order Velocity Verlet integrator.

    More accurate and stable than Euler for orbital mechanics.
    """

    def step(self, bodies: list[Body], dt: float) -> None:

        apply_gravity(bodies)

        previous_accelerations = [
            body.acceleration.copy()
            for body in bodies
        ]

        for body, previous in zip(bodies, previous_accelerations):
            body.position += (
                body.velocity * dt
                + 0.5 * previous * dt * dt
            )

        apply_gravity(bodies)

        for body, previous in zip(bodies, previous_accelerations):
            body.velocity += (
                0.5 * (previous + body.acceleration) * dt
            )

            body.update_trail()


class RK4Integrator(Integrator):
    """
    Fourth-order Runge-Kutta integrator.

    TODO:
    Implement once the mathematical foundations and
    architecture have been fully designed.
    """
 
    def step(self, bodies: list[Body], dt: float) -> None:
        """
        RK4 Algorithm

        1. Save the original simulation state.

        2. Compute k1 using the original state.

        3. Restore the original state.
           Create a temporary half-step state using k1.
           Compute k2.

        4. Restore the original state.
           Create another temporary half-step state using k2.
           Compute k3.

        5. Restore the original state.
           Create a temporary full-step state using k3.
           Compute k4.

        6. Restore the original state.

        7. Combine k1, k2, k3 and k4 using the
           Runge-Kutta weighted average.

        8. Apply the final position and velocity
           updates to the real bodies.

        Notes:
        - Temporary states are never rendered.
        - The real simulation state is modified only once.
        - This implementation will require a redesign
          of temporary state handling.
        """
        pass