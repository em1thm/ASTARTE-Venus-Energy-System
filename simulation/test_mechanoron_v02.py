"""Repeatable checks for the ASTARTE V0.2 energy-dispatch abstraction."""
import unittest

from mechanoron_network import CRITICAL_LOADS, ring_graph
from mechanoron_v02 import network_reachable, simulate


class BatteryAwareTests(unittest.TestCase):
    def test_nominal_mission(self):
        report = simulate("healthy", daily_self_discharge=0.001)
        self.assertEqual(report["critical_days"], 60)
        self.assertEqual(report["mobility_days"], 60)
        self.assertGreater(report["end_accessible_energy_wh"], 0)

    def test_source_failure_preserves_critical_loads(self):
        report = simulate("failure", lost_source="u5", failure_day=20)
        self.assertEqual(report["critical_days"], 60)
        self.assertEqual(report["mobility_days"], 19)
        self.assertEqual(report["rows"][19]["active_sources"], "u0")

    def test_losing_one_source_immediately_suspends_driving(self):
        report = simulate("early_failure", lost_source="u5", failure_day=1)
        self.assertEqual(report["critical_days"], 60)
        self.assertEqual(report["mobility_days"], 0)

    def test_disconnect_critical_node_detected(self):
        graph = ring_graph()
        nbrs = sorted(graph["f0"])
        isolated = [("f0", nbr) for nbr in nbrs]
        self.assertNotIn("f0", network_reachable(graph, ["u0", "u5"], isolated))
        report = simulate("cut", graph_name="ring", broken_edges=isolated)
        self.assertLess(report["critical_days"], 60)

    def test_more_self_discharge_means_less_energy(self):
        a = simulate("no_leak", daily_self_discharge=0.0)
        b = simulate("leak", daily_self_discharge=0.01)
        self.assertLess(b["end_accessible_energy_wh"], a["end_accessible_energy_wh"])


if __name__ == "__main__":
    unittest.main()
