"""ASTARTE V2: battery-constrained Mechanoron dispatch feasibility model.

Python 3.10+, standard library only. Requires mechanoron_network.py (V0.1) in
this directory. This does NOT model cell electrochemistry, I-V behavior,
converter transients, post-fault DC node voltages, or Venus-qualified hardware.
All battery ratings are illustrative, not measured LiSi/FeS specifications.

Run from the project root:
    python simulation/mechanoron_v02.py simulation/mechanoron_v02_results.csv
"""

from __future__ import annotations

import csv
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from mechanoron_network import CRITICAL_LOADS, SUPPLIES, pentakis_graph, ring_graph

DAYS = 60
BASE_POWER_W = 0.25
SCIENCE_POWER_W = 2.0
SCIENCE_HOURS = 0.5
COMMS_POWER_W = 10.0
COMMS_HOURS = 0.25
DRIVE_POWER_W = 75.0
DRIVE_HOURS = 1.0 / 6.0


@dataclass
class BatteryModule:
    name: str
    initial_wh: float = 1500.0  # hypothetical usable energy at mission start
    peak_input_w: float = 65.0  # hypothetical battery-side power limit
    energy_wh: float = 0.0
    failed: bool = False

    def __post_init__(self) -> None:
        if self.initial_wh <= 0 or self.peak_input_w <= 0:
            raise ValueError("Each module must have positive energy and power ratings")
        self.energy_wh = self.initial_wh


def network_reachable(graph, source_nodes, broken_edges=()):
    """Node accessibility given available source nodes and opened links."""
    blocked = {frozenset(e) for e in broken_edges}
    seen = set(source_nodes)
    queue = deque(source_nodes)
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in seen and frozenset((node, neighbor)) not in blocked:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen


def draw_energy(modules, demand_wh, duration_h, standby_w, efficiency, reserve_fraction):
    """Idealized dispatch limited by accessible energy and per-module peak power.

    For an incremental event, standby_w is already charged separately. We
    conservatively hold back enough power for the concurrent standby load.
    Power availability is approximate and does not replace a circuit solve.
    """
    if demand_wh == 0:
        return True
    if duration_h <= 0:
        raise ValueError("duration_h must be positive")
    caps = []
    for module in modules:
        remaining_above_reserve = max(0.0, module.energy_wh - reserve_fraction * module.initial_wh)
        incremental_power = max(0.0, module.peak_input_w - standby_w / efficiency)
        caps.append(min(remaining_above_reserve, incremental_power * duration_h))
    battery_demand = demand_wh / efficiency
    if sum(caps) + 1e-9 < battery_demand:
        return False
    # Proportional dispatch across the modules' constrained energy budgets.
    total_cap = sum(caps)
    for module, cap in zip(modules, caps):
        module.energy_wh -= battery_demand * cap / total_cap
    return True


def simulate(
    label: str,
    *,
    graph_name: str = "pentakis",
    lost_source: str | None = None,
    failure_day: int = 20,
    broken_edges=(),
    module_energy_wh: float = 1500.0,
    module_peak_w: float = 65.0,
    distribution_efficiency: float = 0.85,
    daily_self_discharge: float = 0.001,
    reserve_fraction: float = 0.20,
):
    """Run 60 daily time steps; report successful critical and mobility days."""
    if not (0 < distribution_efficiency <= 1):
        raise ValueError("distribution_efficiency must be in (0, 1]")
    if not (0 <= daily_self_discharge < 1):
        raise ValueError("daily_self_discharge must be in [0, 1)")
    if not (0 <= reserve_fraction < 1):
        raise ValueError("reserve_fraction must be in [0, 1)")
    if not 1 <= failure_day <= DAYS:
        raise ValueError("failure_day must be within the 60-day mission")
    if lost_source is not None and lost_source not in SUPPLIES:
        raise ValueError("lost_source must match a model supply node")

    graph = pentakis_graph() if graph_name == "pentakis" else ring_graph() if graph_name == "ring" else None
    if graph is None:
        raise ValueError("graph_name must be pentakis or ring")
    modules = {node: BatteryModule(node, module_energy_wh, module_peak_w) for node in SUPPLIES}
    rows = []
    critical_days = 0
    mobility_days = 0
    critical_event_failures = 0
    self_discharge_loss_wh = 0.0

    for day in range(1, DAYS + 1):
        if lost_source and day == failure_day:
            modules[lost_source].failed = True
        active_sources = [m for m in modules.values() if not m.failed]
        for module in active_sources:
            lost_wh = module.energy_wh * daily_self_discharge
            module.energy_wh -= lost_wh
            self_discharge_loss_wh += lost_wh

        reachable = network_reachable(graph, [m.name for m in active_sources], broken_edges)
        critical_connected = set(CRITICAL_LOADS).issubset(reachable)
        if critical_connected:
            baseline_ok = draw_energy(active_sources, BASE_POWER_W * 24.0, 24.0,
                                      0.0, distribution_efficiency, reserve_fraction)
            science_ok = baseline_ok and draw_energy(active_sources, SCIENCE_POWER_W * SCIENCE_HOURS,
                             SCIENCE_HOURS, BASE_POWER_W, distribution_efficiency, reserve_fraction)
            comms_ok = baseline_ok and draw_energy(active_sources, COMMS_POWER_W * COMMS_HOURS,
                             COMMS_HOURS, BASE_POWER_W, distribution_efficiency, reserve_fraction)
        else:
            baseline_ok = science_ok = comms_ok = False

        critical_ok = baseline_ok and science_ok and comms_ok
        if critical_ok:
            critical_days += 1
        else:
            critical_event_failures += 1

        mobility_ok = critical_ok and draw_energy(active_sources, DRIVE_POWER_W * DRIVE_HOURS,
                               DRIVE_HOURS, BASE_POWER_W, distribution_efficiency, reserve_fraction)
        if mobility_ok:
            mobility_days += 1

        rows.append({
            "scenario": label,
            "day": day,
            "active_sources": "+".join(m.name for m in active_sources) or "none",
            "critical_connected": int(critical_connected),
            "critical_operations_ok": int(critical_ok),
            "mobility_completed": int(mobility_ok),
            "accessible_energy_wh": round(sum(m.energy_wh for m in active_sources), 4),
        })

    return {
        "scenario": label,
        "critical_days": critical_days,
        "mobility_days": mobility_days,
        "critical_failures": critical_event_failures,
        "end_accessible_energy_wh": round(sum(m.energy_wh for m in modules.values() if not m.failed), 3),
        "self_discharge_loss_wh": round(self_discharge_loss_wh, 3),
        "rows": rows,
    }


def main() -> None:
    scenarios = [
        simulate("healthy_60d"),
        simulate("source_u5_fails_on_day20", lost_source="u5", failure_day=20),
    ]
    for case in scenarios:
        print(f"{case['scenario']}: critical days {case['critical_days']}/{DAYS}, "
              f"mobility days {case['mobility_days']}/{DAYS}, "
              f"end accessible energy {case['end_accessible_energy_wh']:.1f} Wh")
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        target.parent.mkdir(parents=True, exist_ok=True)
        rows = [row for scenario in scenarios for row in scenario["rows"]]
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved {target}")


if __name__ == "__main__":
    main()
