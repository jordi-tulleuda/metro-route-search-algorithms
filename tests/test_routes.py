"""Small independent portfolio smoke tests (not the university test suite)."""
import unittest

from demo import load_map
from SearchAlgorithm import (
    Astar, Astar_improved, breadth_first_search, depth_first_search,
    uniform_cost_search, calculate_cost,
)
from SubwayMap import Map, Path


class MetroSearchSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lyon = load_map("lyon")
        cls.barcelona = load_map("barcelona")

    def test_datasets_load(self):
        self.assertEqual(len(self.lyon.stations), 14)
        self.assertEqual(len(self.barcelona.stations), 25)

    def test_depth_first_search(self):
        self.assertEqual(depth_first_search(2, 7, self.lyon).route, [2, 5, 6, 7])

    def test_breadth_first_search(self):
        self.assertEqual(breadth_first_search(5, 12, self.lyon).route, [5, 10, 11, 12])

    def test_ucs_and_astar_agree_on_sample(self):
        ucs = uniform_cost_search(1, 25, self.barcelona, 1)
        astar = Astar(1, 25, self.barcelona, 1)
        self.assertEqual(ucs.route, astar.route)
        self.assertAlmostEqual(ucs.g, astar.g)

    def test_coordinate_routing(self):
        route = Astar_improved([80, 100], [100, 240], self.lyon)
        self.assertEqual(route.route, [0, 11, 12, -1])
        self.assertAlmostEqual(route.f, 18.417006, places=6)

    def test_transfer_cost(self):
        # An inter-line edge should contribute one transfer.
        subway = Map()
        subway.add_station(1, "First", 1, 0, 0)
        subway.add_station(2, "Second", 2, 2, 0)
        subway.add_connection({1: {2: 1.0}})
        subway.add_velocity([10, 10])
        self.assertEqual(calculate_cost([Path([1, 2])], subway, 3)[0].g, 1)

    def test_unreachable_astar_returns_none(self):
        subway = Map()
        subway.add_station(1, "First", 1, 0, 0)
        subway.add_station(2, "Unreachable", 1, 2, 0)
        subway.add_connection({1: {}, 2: {}})
        subway.add_velocity([10])
        self.assertIsNone(Astar(1, 2, subway, 1))


if __name__ == "__main__":
    unittest.main()
