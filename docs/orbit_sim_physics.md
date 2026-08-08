# COSMOS Orbit Simulator Physics

## 1. Purpose

This document describes the physical model, units, equations, assumptions, and initial conditions used by the COSMOS Orbit Simulator.

The Orbit Simulator is a two-dimensional Newtonian **N-body simulation**. The Solar System is initialized from realistic orbital parameters, converted into position and velocity vectors, and then evolved by the COSMOS physics engine.

The current model contains the Sun and the eight planets, with the asteroid belt and other Solar System bodies intentionally excluded for now.

---

## 2. Physical Model

COSMOS treats every celestial object as a point mass for gravitational calculations.

Each `Body` stores mass, radius, position, velocity, and acceleration. The `Body` class does not calculate physics. Gravitational acceleration is calculated by `gravity.py`, while `integrators.py` advances the simulation.

The simulation uses **pairwise N-body gravity**, meaning every body gravitationally interacts with every other body.

Newton's law of universal gravitation is:

$$
F = G\frac{m_1m_2}{r^2}
$$

For the acceleration of one body caused by another:

$$
a = G\frac{m}{r^2}
$$

Each pair is processed once, with equal and opposite acceleration contributions.

---

## 3. COSMOS Unit System

| Quantity | COSMOS unit |
|---|---|
| Distance | million kilometres |
| Mass | Earth masses |
| Time | days |
| Velocity | million kilometres/day |
| Acceleration | million kilometres/day² |

The gravitational constant is scaled to match these units:

```python
G = 0.00297555
```

The Sun is represented as:

```text
M☉ = 332946.05 Earth masses
```

giving:

$$
\mu = GM_\odot \approx 990.70
$$

in COSMOS distance/time units.

---

## 4. Initial Orbital Conditions

The planets are initialized from **orbital elements**, rather than arbitrary distances and circular velocities.

The main parameters are:

- `a`: semi-major axis
- `e`: orbital eccentricity
- `ν`: true anomaly

The chosen true anomalies deliberately spread the planets around the system. They are **not** intended to reproduce the Solar System at a particular historical date.

### Orbital radius

The semi-latus rectum is:

$$
p=a(1-e^2)
$$

The instantaneous orbital distance is:

$$
r=\frac{a(1-e^2)}{1+e\cos\nu}
$$

### Orbital velocity

The radial component is:

$$
v_r = \sqrt{\frac{\mu}{p}}e\sin\nu
$$

The tangential component is:

$$
v_t = \sqrt{\frac{\mu}{p}}(1+e\cos\nu)
$$

The total speed is:

$$
v=\sqrt{v_r^2+v_t^2}
$$

The radial and tangential components are converted into Cartesian X/Y velocity components for `pygame.Vector2`.

---

## 5. Planetary Orbital Parameters

Distances are in million kilometres.

| Body | Semi-major axis `a` | Eccentricity `e` | True anomaly `ν` |
|---|---:|---:|---:|
| Mercury | 57.909 | 0.2056 | 20° |
| Venus | 108.209 | 0.0068 | 75° |
| Earth | 149.598 | 0.0167 | 140° |
| Mars | 227.956 | 0.0934 | 210° |
| Jupiter | 778.479 | 0.0489 | 260° |
| Saturn | 1432.041 | 0.0565 | 315° |
| Uranus | 2867.043 | 0.0463 | 30° |
| Neptune | 4498.396 | 0.0095 | 180° |

These parameters provide realistic orbital scales and eccentricities while keeping the initial arrangement reproducible.

---

## 6. Final Initial States

Masses are in Earth masses, positions are in million kilometres, and velocities are in million kilometres/day.

| Body | Mass | Position `(x, y)` | Velocity `(vx, vy)` |
|---|---:|---|---|
| Sun | 332946.05 | `(0, 0)` | `(-0.00120529, -0.00004326)` |
| Mercury | 0.0553 | `(43.6778, 15.8974)` | `(-1.4455, 4.8405)` |
| Venus | 0.815 | `(27.9561, 104.3334)` | `(-2.9228, 0.8037)` |
| Earth | 1.0 | `(-116.0514, 97.3787)` | `(-1.6544, -1.9286)` |
| Mars | 0.107 | `(-212.9156, -122.9269)` | `(1.0469, -1.6178)` |
| Jupiter | 317.828 | `(-136.0132, -771.3689)` | `(1.1123, -0.1409)` |
| Saturn | 95.159 | `(970.5966, -970.5966)` | `(0.5891, 0.6361)` |
| Uranus | 14.536 | `(2382.0946, 1375.3030)` | `(-0.2942, 0.5369)` |
| Neptune | 17.147 | `(-4541.1308, 0)` | `(0, -0.4649)` |

---

## 7. Solar Center-of-Mass Correction

The chosen planetary phases give the planets a non-zero total momentum.

Planetary momentum is:

$$
\vec P_{planets}=\sum_i m_i\vec v_i
$$

The Sun receives a compensating velocity:

$$
\vec v_\odot =
-\frac{\vec P_{planets}}{M_\odot}
$$

This produces the current initial solar velocity:

```text
(-0.00120529, -0.00004326)
```

The purpose is to begin approximately in the center-of-mass frame rather than artificially forcing the Sun to remain stationary.

---

## 8. N-Body Evolution

The orbital-element equations are used only to create the **initial state**.

Once the simulation starts, the engine does not force the planets to follow Keplerian ellipses.

Instead:

```text
Orbital elements
      ↓
Position + velocity
      ↓
Body objects
      ↓
Newtonian N-body gravity
      ↓
Velocity Verlet
      ↓
New positions and velocities
```

Every body responds to the gravitational field produced by every other body. Planetary perturbations can therefore naturally alter their motion.

---

## 9. Numerical Integration

The Orbit Simulator currently uses **Velocity Verlet**.

Each step:

1. Calculates current gravitational acceleration.
2. Saves the current accelerations.
3. Advances positions using velocity and acceleration.
4. Recalculates gravity.
5. Updates velocities using the old and new accelerations.

Velocity Verlet is substantially better suited to orbital mechanics than basic Euler integration because of its improved stability and long-term energy behaviour.

RK4 exists in the engine architecture but is currently a placeholder.

---

## 10. Simulation Time Scale

The default simulation time scale is:

```text
1×
```

This is the preferred reference/debug mode.

A convenience mode is also available:

```text
80×
```

The 80× mode does not alter gravity, masses, orbital parameters, or the integrator. It simply advances the simulation faster for visualization.

Therefore:

- **1×** = realistic/reference viewing speed
- **80×** = convenient accelerated viewing speed

---

## 11. Current Assumptions

### Included

- Sun
- Mercury
- Venus
- Earth
- Mars
- Jupiter
- Saturn
- Uranus
- Neptune
- Newtonian gravity
- N-body interactions
- 2D orbital motion
- Elliptical initial conditions
- Velocity Verlet integration

### Excluded for now

- Moon
- Asteroid belt
- Dwarf planets
- Comets
- Kuiper Belt objects
- 3D orbital inclination
- Relativistic corrections
- Solar radiation pressure
- Other non-gravitational forces

The purpose is to establish a stable and understandable Newtonian N-body foundation before increasing physical complexity.

---

## 12. Why This Is Not an Exact Historical Solar System

The current configuration is **physically motivated, but not a reconstruction of the Solar System at a specific date**.

Realistic orbital parameters are used for the planets, while the initial true anomalies are deliberately selected by COSMOS.

Therefore:

- orbital sizes are realistic;
- eccentricities are realistic;
- initial speeds are derived from orbital mechanics;
- the planets are not artificially forced into circular orbits;
- the starting configuration is not tied to a real astronomical epoch.

A future version could use real astronomical state vectors at a specified epoch to reproduce a particular Solar System configuration.

---

## 13. Future Physics Improvements

Potential future improvements include:

1. Add the Moon.
2. Add the asteroid belt.
3. Add dwarf planets and selected minor bodies.
4. Support 3D `Vector3` states.
5. Support real astronomical state vectors.
6. Add orbital inclination.
7. Investigate relativistic corrections.
8. Add energy and momentum conservation diagnostics.
9. Compare simulated orbital evolution against reference astronomical data.
10. Add configurable numerical-integration diagnostics.

---

## 14. Summary

> **Use realistic physics to create the initial Solar System, then let the N-body engine determine what happens next.**

The initial planetary states are derived from orbital elements rather than manually tuned positions and velocities.

After initialization, the system is governed by Newtonian gravity and advanced using Velocity Verlet.

This gives COSMOS a physically motivated 2D Solar System while leaving a clear path toward more sophisticated celestial mechanics.
