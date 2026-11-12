"""Standard-library regression checks for ASTARTE V2 Mechanoron prototype."""
import unittest

from mechanoron_network import (
    CRITICAL_LOADS, SUPPLIES, edges, nominal_dc_model, pentakis_graph,
    reachable, resilience, ring_graph,
)


class MechanoronGraphTests(unittest.TestCase):
    def test_geometry_counts(self):
        graph = pentakis_graph()
        self.assertEqual(32, len(graph))
        self.assertEqual(90, len(edges(graph)))
        self.assertEqual(12, sum(len(n) == 5 for n in graph.values()))
        self.assertEqual(20, sum(len(n) == 6 for n in graph.values()))

    def test_all_single_edges_remain_connected_to_loads(self):
        graph = pentakis_graph()
        for edge in edges(graph):
            active = reachable(graph, failed_edges=[edge])
            self.assertTrue(set(CRITICAL_LOADS).issubset(active))

    def test_two_edge_failure_exhaustive(self):
        summary = resilience(pentakis_graph(), 2)
        self.assertEqual(4005, summary["cases"])
        self.assertEqual(1.0, summary["all_loads_supplied_rate"])
        self.assertLess(resilience(ring_graph(), 2)["all_loads_supplied_rate"], 1.0)

    def test_dc_voltage_and_nonnegative_dissipation(self):
        for graph in (pentakis_graph(), ring_graph()):
            output = nominal_dc_model(graph)
            self.assertGreater(output["minimum_critical_load_voltage_V"], 0)
            self.assertLess(output["minimum_critical_load_voltage_V"], 24)
            self.assertGreater(output["resistive_loss_W"], 0)
            self.assertAlmostEqual(output["source_current_A"], 0.8, places=7)


if __name__ == "__main__":
    unittest.main()
