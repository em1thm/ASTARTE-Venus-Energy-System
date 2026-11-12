"""ASTARTE V2 | Mechanoron candidate graph and illustrative DC network.

Python 3.10+; standard library only.
This is a topology-and-resistance feasibility experiment, not a qualified
battery, high-temperature switching design, or Venus mission simulation.

Usage: python simulation/mechanoron_network.py [optional_results.csv]
"""
from __future__ import annotations

import csv
import itertools
import random
import sys
from collections import Counter, deque
from pathlib import Path

N = 10
SUPPLIES = ("u0", "u5")
CRITICAL_LOADS = ("f0", "f3", "f6", "f9")
SUPPLY_VOLTAGE_V = 24.0        # illustrative ideal voltage sources
LOAD_CURRENT_A = 0.20         # constant-current load at each critical node
EDGE_RESISTANCE_OHM = 0.05    # same resistance per link; NOT a Venus-rated part
SEED = 2026
TRIALS = 2000


def add_edge(graph: dict[str, set[str]], a: str, b: str) -> None:
    if a == b:
        raise ValueError("Self edge")
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)


def pentakis_graph() -> dict[str, set[str]]:
    """Dodecahedral G(10,2) graph, with a 5-link center in each face.

    20 dodecahedron vertices (u0..u9,v0..v9), 12 face centers
    (f0..f9,f_even,f_odd). Total: V=32, E=90, F=60.
    """
    graph: dict[str, set[str]] = {}
    for i in range(N):
        add_edge(graph, f"u{i}", f"u{(i + 1) % N}")
        add_edge(graph, f"u{i}", f"v{i}")
        add_edge(graph, f"v{i}", f"v{(i + 2) % N}")

    faces = [
        [f"u{i}", f"u{(i + 1) % N}", f"u{(i + 2) % N}",
         f"v{(i + 2) % N}", f"v{i}"]
        for i in range(N)
    ]
    faces.extend([
        [f"v{i}" for i in range(0, N, 2)],
        [f"v{i}" for i in range(1, N, 2)],
    ])
    for k, face in enumerate(faces):
        face_id = f"f{k}" if k < N else ("f_even" if k == N else "f_odd")
        for vertex in face:
            add_edge(graph, face_id, vertex)

    validate_pentakis_graph(graph)
    return graph


def ring_graph() -> dict[str, set[str]]:
    """32-node, 32-edge topological reference; physical lengths are unknown."""
    nodes = ([f"u{i}" for i in range(N)] +
             [f"v{i}" for i in range(N)] +
             [f"f{i}" for i in range(N)] + ["f_even", "f_odd"])
    g: dict[str, set[str]] = {}
    for a, b in zip(nodes, nodes[1:] + nodes[:1]):
        add_edge(g, a, b)
    return g


def edges(graph: dict[str, set[str]]) -> list[tuple[str, str]]:
    return sorted((min(a, b), max(a, b)) for a, ns in graph.items() for b in ns if a < b)


def reachable(graph: dict[str, set[str]], failed_edges=(), failed_nodes=()) -> set[str]:
    blocked = {frozenset(x) for x in failed_edges}
    disabled = set(failed_nodes)
    starts = [x for x in SUPPLIES if x in graph and x not in disabled]
    found = set(starts)
    queue = deque(starts)
    while queue:
        a = queue.popleft()
        for b in graph[a]:
            if b in disabled or b in found or frozenset((a, b)) in blocked:
                continue
            found.add(b)
            queue.append(b)
    return found


def validate_pentakis_graph(graph: dict[str, set[str]]) -> None:
    degrees = Counter(len(n) for n in graph.values())
    assert len(graph) == 32, f"Wrong vertex count: {len(graph)}"
    assert len(edges(graph)) == 90, f"Wrong edge count: {len(edges(graph))}"
    assert degrees == {6: 20, 5: 12}, f"Wrong degree distribution: {degrees}"
    assert len(reachable(graph)) == 32, "Graph is not connected"
    assert len(graph) - len(edges(graph)) + 60 == 2, "Euler invariant failed"


def service_fraction(graph: dict[str, set[str]], removed_edges=()) -> float:
    active = reachable(graph, failed_edges=removed_edges)
    return sum(node in active for node in CRITICAL_LOADS) / len(CRITICAL_LOADS)


def resilience(graph: dict[str, set[str]], failures: int, *, trials: int = TRIALS):
    link_list = edges(graph)
    if failures <= 3:
        cases = itertools.combinations(link_list, failures)
        method = "exact enumeration"
    else:
        rng = random.Random(SEED)
        cases = (rng.sample(link_list, failures) for _ in range(trials))
        method = f"Monte Carlo, seed={SEED}, {trials} trials"
    count = 0
    all_supplied = 0
    total_fraction = 0.0
    for removed in cases:
        fraction = service_fraction(graph, removed)
        count += 1
        total_fraction += fraction
        all_supplied += fraction == 1.0
    return {"failure_count": failures, "cases": count, "method": method,
            "all_loads_supplied_rate": all_supplied / count,
            "average_service_fraction": total_fraction / count}


def solve_linear(A: list[list[float]], b: list[float]) -> list[float]:
    """Small dense system with partial pivoting; standard library only."""
    n = len(b)
    a = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda i: abs(a[i][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError("Electrical network singular or disconnected")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= scale
        for row in range(col + 1, n):
            factor = a[row][col]
            for j in range(col, n + 1):
                a[row][j] -= factor * a[col][j]
    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = a[i][n] - sum(a[i][j] * solution[j] for j in range(i + 1, n))
    return solution


def nominal_dc_model(graph: dict[str, set[str]]) -> dict[str, float]:
    """Ideal 24-V clamps, resistive links, fixed 0.2-A current sinks.

    Not a battery cell IV model, converter or switching design.
    """
    fixed = set(SUPPLIES)
    unknowns = sorted(set(graph) - fixed)
    idx = {node: i for i, node in enumerate(unknowns)}
    n = len(unknowns)
    conductance = 1 / EDGE_RESISTANCE_OHM
    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    for node, i in idx.items():
        b[i] = -LOAD_CURRENT_A if node in CRITICAL_LOADS else 0.0
        for nbr in graph[node]:
            A[i][i] += conductance
            if nbr in idx:
                A[i][idx[nbr]] -= conductance
            else:
                b[i] += conductance * SUPPLY_VOLTAGE_V
    sol = solve_linear(A, b)
    voltages = {node: SUPPLY_VOLTAGE_V for node in fixed}
    voltages.update({node: sol[i] for node, i in idx.items()})
    dissipated_w = sum((voltages[a] - voltages[b]) ** 2 / EDGE_RESISTANCE_OHM
                       for a, b in edges(graph))
    source_current = sum(sum((voltages[s] - voltages[j]) / EDGE_RESISTANCE_OHM
                             for j in graph[s]) for s in fixed)
    assert abs(source_current - len(CRITICAL_LOADS) * LOAD_CURRENT_A) < 1e-7
    lowest_load = min(voltages[node] for node in CRITICAL_LOADS)
    return {"minimum_critical_load_voltage_V": lowest_load,
            "resistive_loss_W": dissipated_w,
            "source_current_A": source_current}


def summarize() -> list[dict[str, str | int | float]]:
    rows = []
    for title, graph in (("pentakis", pentakis_graph()), ("ring", ring_graph())):
        dc = nominal_dc_model(graph)
        print(f"\n{title}: {len(graph)} nodes, {len(edges(graph))} links")
        print(f"  DC: minimum critical-load voltage = {dc['minimum_critical_load_voltage_V']:.6f} V;"
              f" link dissipation = {dc['resistive_loss_W']:.6f} W")
        for k in (0, 1, 2, 3):
            summary = resilience(graph, k)
            print(f"  {k} link fault(s): full service = "
                  f"{summary['all_loads_supplied_rate']:.4%}, mean load service = "
                  f"{summary['average_service_fraction']:.4%} "
                  f"[{summary['cases']} cases, {summary['method']}]")
            rows.append({"topology": title, "nodes": len(graph), "links": len(edges(graph)),
                         "failed_links": k, "sample_count": summary["cases"],
                         "method": summary["method"],
                         "all_loads_supplied_rate": round(summary["all_loads_supplied_rate"], 6),
                         "average_service_fraction": round(summary["average_service_fraction"], 6),
                         "minimum_nominal_load_voltage_V": round(dc["minimum_critical_load_voltage_V"], 6),
                         "nominal_link_loss_W": round(dc["resistive_loss_W"], 6)})
    return rows


def main():
    rows = summarize()
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
