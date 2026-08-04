"""Regression tests for the analytical curve definitions."""

from __future__ import annotations

import unittest

import numpy as np

from coinparadox import (
    aristotle_trajectories,
    epicycloid,
    hypocycloid,
    rotation_count,
)


class RouletteCurveTests(unittest.TestCase):
    def test_equal_coin_rotation_count_is_two(self) -> None:
        self.assertEqual(rotation_count(1.0, 1.0), 2.0)

    def test_epicycloid_starts_at_contact_and_closes_for_integer_ratio(self) -> None:
        theta = np.array([0.0, 2.0 * np.pi])
        x, y = epicycloid(theta, R=3.0, r=1.0)
        np.testing.assert_allclose(x, [3.0, 3.0], atol=1e-12)
        np.testing.assert_allclose(y, [0.0, 0.0], atol=1e-12)

    def test_hypocycloid_with_R_equal_2r_is_a_line_segment(self) -> None:
        theta = np.linspace(0.0, 2.0 * np.pi, 101)
        x, y = hypocycloid(theta, R=2.0, r=1.0)
        np.testing.assert_allclose(y, 0.0, atol=1e-12)
        self.assertAlmostEqual(float(x.max()), 2.0)
        self.assertAlmostEqual(float(x.min()), -2.0)

    def test_aristotle_points_share_the_outer_translation(self) -> None:
        theta = np.array([0.0, 2.0 * np.pi])
        x_outer, _, x_inner, _ = aristotle_trajectories(theta, R=2.0, r=1.0)
        expected_distance = 4.0 * np.pi
        self.assertAlmostEqual(float(x_outer[-1] - x_outer[0]), expected_distance)
        self.assertAlmostEqual(float(x_inner[-1] - x_inner[0]), expected_distance)

    def test_invalid_radii_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            rotation_count(1.0, 0.0)
        with self.assertRaises(ValueError):
            hypocycloid([0.0], R=1.0, r=1.0)
        with self.assertRaises(ValueError):
            aristotle_trajectories([0.0], R=1.0, r=2.0)


if __name__ == "__main__":
    unittest.main()
