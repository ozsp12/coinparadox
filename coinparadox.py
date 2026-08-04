"""Parametric models for roulette curves and rolling-wheel paradoxes.

The functions implement the conventions used in Santos-Pereira (2025).
Angles are measured in radians, and all radii must use the same length unit.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _positive_radius(value: float, name: str) -> float:
    """Return a finite positive radius or raise ``ValueError``."""
    radius = float(value)
    if not np.isfinite(radius) or radius <= 0.0:
        raise ValueError(f"{name} must be a finite positive number.")
    return radius


def _angles(theta: ArrayLike) -> FloatArray:
    """Convert an angle-like input to a finite NumPy array."""
    angles = np.asarray(theta, dtype=float)
    if not np.isfinite(angles).all():
        raise ValueError("theta must contain only finite values.")
    return angles


def rotation_count(R: float, r: float, *, internal: bool = False) -> float:
    """Return the rolling circle's rotations per circuit.

    For external rolling the count is ``(R + r) / r``. For internal rolling
    it is ``(R - r) / r`` and requires ``R > r``.
    """
    fixed_radius = _positive_radius(R, "R")
    rolling_radius = _positive_radius(r, "r")
    if internal:
        if fixed_radius <= rolling_radius:
            raise ValueError("Internal rolling requires R > r.")
        return (fixed_radius - rolling_radius) / rolling_radius
    return (fixed_radius + rolling_radius) / rolling_radius


def epicycloid(theta: ArrayLike, R: float, r: float) -> tuple[FloatArray, FloatArray]:
    """Coordinates of a point on a circle rolling outside a fixed circle."""
    angles = _angles(theta)
    fixed_radius = _positive_radius(R, "R")
    rolling_radius = _positive_radius(r, "r")
    frequency = rotation_count(fixed_radius, rolling_radius)
    x = (fixed_radius + rolling_radius) * np.cos(angles) - rolling_radius * np.cos(frequency * angles)
    y = (fixed_radius + rolling_radius) * np.sin(angles) - rolling_radius * np.sin(frequency * angles)
    return x, y


def hypocycloid(theta: ArrayLike, R: float, r: float) -> tuple[FloatArray, FloatArray]:
    """Coordinates of a point on a circle rolling inside a fixed circle."""
    angles = _angles(theta)
    fixed_radius = _positive_radius(R, "R")
    rolling_radius = _positive_radius(r, "r")
    frequency = rotation_count(fixed_radius, rolling_radius, internal=True)
    x = (fixed_radius - rolling_radius) * np.cos(angles) + rolling_radius * np.cos(frequency * angles)
    y = (fixed_radius - rolling_radius) * np.sin(angles) - rolling_radius * np.sin(frequency * angles)
    return x, y


def aristotle_trajectories(
    theta: ArrayLike, R: float, r: float
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Return trajectories of points on concentric radii ``R`` and ``r``.

    The outer circle rolls without slipping along a straight line. Both
    material points share the same angular displacement because the circles
    are rigidly connected. The outer point traces a cycloid; the inner point
    traces a curtate cycloid.
    """
    angles = _angles(theta)
    outer_radius = _positive_radius(R, "R")
    inner_radius = _positive_radius(r, "r")
    if inner_radius >= outer_radius:
        raise ValueError("Aristotle's wheel requires 0 < r < R.")

    translation = outer_radius * angles
    x_outer = translation + outer_radius * np.sin(angles)
    y_outer = outer_radius + outer_radius * np.cos(angles)
    x_inner = translation + inner_radius * np.sin(angles)
    y_inner = outer_radius + inner_radius * np.cos(angles)
    return x_outer, y_outer, x_inner, y_inner


__all__: Iterable[str] = (
    "aristotle_trajectories",
    "epicycloid",
    "hypocycloid",
    "rotation_count",
)
