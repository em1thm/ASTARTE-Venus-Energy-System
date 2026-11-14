"""ASTARTE V2 | V0.3 physics-aware battery dispatch *sensitivity* model.

Python 3.10+, standard library only. All assumed cell ratings are illustrative,
NOT measurements of LiSi/FeS cells and NOT a Venus-qualified architecture.

Run from repository root:
    python simulation/mechanoron_v03.py simulation/mechanoron_v03_results.csv

Assumes two independently regulated source modules feeding reachable critical loads.
The model does not solve post-fault network voltages, converter dynamics, RC
polarization, temperature evolution, electrochemical ageing or cell imbalances.
"""
from __future__ import annotations

import csv
import math
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from mechanoron_network import CRITICAL_LOADS, SUPPLIES, pentakis_graph

DAYS = 60
HOUSEKEEPING_W = 0.25
SCIENCE_EXTRA_W = 2.0
COMMS_EXTRA_W = 10.0
MOBILITY_EXTRA_W = 75.0
SCIENCE_H = 0.5
COMMS_H = 0.25
MOBILITY_H = 1.0/6.0
IDLE_H = 24.0 - SCIENCE_H - COMMS_H - MOBILITY_H


@dataclass(frozen=True)
class CellAssumptions:
    series_cells: int = 19
    parallel_strings_per_source: int = 2
    capacity_ah_per_cell: float = 20.0
    plateau_reference_v: float = 1.32   # NASA LiSi/FeS reported discharge plateau;
    ocv_soc_slope_v: float = 0.10      # HYPOTHETICAL OCV profile, not measured
    resistance_ohm_per_cell: float = 0.10  # HYPOTHETICAL, temperature reference
    resistance_temp_slope_per_c: float = 0.0 # HYPOTHETICAL sensitivity
    temperature_c: float = 465.0
    max_current_a_per_string: float = 2.0  # HYPOTHETICAL continuous/pulse cap
    min_terminal_v_per_cell: float = 1.00  # HYPOTHETICAL cutoff
    reserve_soc: float = 0.20
    daily_self_discharge: float = 0.001  # HYPOTHETICAL fraction of remaining Ah
    path_efficiency: float = 0.85      # does NOT include cell I^2R losses

    def __post_init__(self):
        if self.series_cells < 1 or self.parallel_strings_per_source < 1:
            raise ValueError('Cell counts must be positive')
        if min(self.capacity_ah_per_cell,self.plateau_reference_v,
               self.max_current_a_per_string) <= 0:
            raise ValueError('Capacity, plateau voltage and current limits must be positive')
        if self.resistance_ohm_per_cell < 0 or self.ocv_soc_slope_v < 0:
            raise ValueError('Resistance and OCV slope must be nonnegative')
        if not 0 <= self.reserve_soc < 1 or not 0 <= self.daily_self_discharge < 1:
            raise ValueError('Reserve and self-discharge must be fractions in [0, 1)')
        if not 0 < self.path_efficiency <= 1:
            raise ValueError('Efficiency must be in (0, 1]')
        if self.min_terminal_v_per_cell <= 0:
            raise ValueError('Minimum cell voltage must be positive')
        if 1 + self.resistance_temp_slope_per_c*(self.temperature_c - 465) <= 0:
            raise ValueError('Resistance temperature factor must be positive')

    @property
    def pack_r_ohm(self):
        return (self.series_cells*self.resistance_ohm_per_cell /
                self.parallel_strings_per_source *
                (1 + self.resistance_temp_slope_per_c*(self.temperature_c-465)))

    @property
    def source_capacity_ah(self):
        return self.parallel_strings_per_source*self.capacity_ah_per_cell

    def source_ocv(self,soc):
        # The 1.32 V paper reports a loaded LiSi plateau, NOT OCV vs SOC.
        # The following synthetic law is for parameter sensitivity ONLY.
        return self.series_cells*(self.plateau_reference_v +
                self.ocv_soc_slope_v*(soc-0.5))


def electrical_point(p: CellAssumptions, soc: float, requested_terminal_w: float):
    """Solve P=I(Voc-I R) on the low-current branch; None if limits violated.

    Returns terminal voltage, source current and cell ohmic dissipation.
    Cell current is pack current / parallel_strings_per_source.
    """
    if requested_terminal_w < 0 or not 0 <= soc <= 1:
        raise ValueError('Power and SOC outside model bounds')
    voc = p.source_ocv(soc)
    r = p.pack_r_ohm
    if requested_terminal_w == 0:
        return {'current_a':0.0,'terminal_v':voc,'ohmic_w':0.0,
                'terminal_w':0.0}
    if r == 0:
        current = requested_terminal_w/voc
    else:
        disc = voc*voc - 4*r*requested_terminal_w
        if disc < 0:
            return None
        # Stable expression avoids subtraction cancellation.
        current = (2*requested_terminal_w)/(voc+math.sqrt(max(0.0,disc)))
    voltage = voc-current*r
    if (current/p.parallel_strings_per_source > p.max_current_a_per_string + 1e-9
        or voltage/p.series_cells < p.min_terminal_v_per_cell-1e-9):
        return None
    return {'current_a':current,'terminal_v':voltage,
            'ohmic_w':current*current*r,'terminal_w':current*voltage}


def reachable_from_active(active_sources, broken_edges=()):
    graph = pentakis_graph()
    failed = {frozenset(e) for e in broken_edges}
    seen = set(active_sources)
    q = deque(active_sources)
    while q:
        v = q.popleft()
        for n in graph[v]:
            if n not in seen and frozenset((v,n)) not in failed:
                seen.add(n)
                q.append(n)
    return set(CRITICAL_LOADS).issubset(seen)


def simulate(label: str, p: CellAssumptions, *, failed_source=None,
             failure_day=20, broken_edges=(), suspend_mobility_after_failure=True):
    """Daily energy scheduling with transactional electrical feasibility checks.

    Two modules at nodes u0,u5, each with Ns x Np cells. Equal power share among
    active modules, treated as independently regulated sources. No postfault DC
    network solve; reachability is a gate only.
    """
    if failed_source not in (None, *SUPPLIES):
        raise ValueError('Unknown source node')
    if not 1 <= failure_day <= DAYS:
        raise ValueError('Failure day outside mission')
    soc = {name:1.0 for name in SUPPLIES}
    active = list(SUPPLIES)
    rows=[]
    critical_days=mobility_days=0
    failure_reasons={}
    cumulative_ohmic_wh=cumulative_load_wh=cumulative_path_loss_wh=0.0

    def dispatch(load_power_w, duration_h, *, protect_critical_days=0):
        """Returns (success, min_v, joule_heating_wh, reason). Commit only if feasible."""
        if not active:
            return False, None, 0.0, 'no_source'
        if not reachable_from_active(active,broken_edges):
            return False, None, 0.0, 'disconnected'
        battery_terminal_w = load_power_w/p.path_efficiency
        per_source_w = battery_terminal_w/len(active)
        snapshots=[]
        for name in active:
            sol = electrical_point(p,soc[name],per_source_w)
            if sol is None:
                return False,None,0.0,'electrical_limit'
            soc_after=soc[name]-sol['current_a']*duration_h/p.source_capacity_ah
            if soc_after < p.reserve_soc-1e-10:
                return False,None,0.0,'reserve_exhaustion'
            if protect_critical_days:
                # Conservative screening only: assume future science energy is
                # delivered at the *assumed* lower cell-voltage cutoff, with
                # equal splitting among available sources and no new faults.
                # Actual mission planning needs cell discharge curves.
                future_day_wh = (HOUSEKEEPING_W*24 + SCIENCE_EXTRA_W*SCIENCE_H
                                 + COMMS_EXTRA_W*COMMS_H)
                required_ah_each = (protect_critical_days*future_day_wh /
                    (p.path_efficiency*len(active)*p.series_cells*
                     p.min_terminal_v_per_cell))
                estimated_end_soc=(soc_after*(1-p.daily_self_discharge)**protect_critical_days
                                   - required_ah_each/p.source_capacity_ah)
                if estimated_end_soc < p.reserve_soc - 1e-10:
                    return False,None,0.0,'future_critical_reserve'
            snapshots.append((name,sol,soc_after))
        for name,sol,new_soc in snapshots:
            soc[name]=new_soc
        min_v=min(s['terminal_v'] for _,s,_ in snapshots)
        heat_wh=sum(s['ohmic_w']*duration_h for _,s,_ in snapshots)
        return True,min_v,heat_wh,'ok'

    for day in range(1,DAYS+1):
        if failed_source is not None and day==failure_day:
            active.remove(failed_source)
        # Fractional calendar self-discharge on remaining SOC; not a fitted chemistry rate.
        for name in active:
            soc[name] *= (1-p.daily_self_discharge)
        daily_ohmic=0.0
        daily_load=0.0
        daily_min_v=[]
        daily_reason='ok'
        critical_ok=True
        for w,t in ((HOUSEKEEPING_W,IDLE_H),
                    (HOUSEKEEPING_W+SCIENCE_EXTRA_W,SCIENCE_H),
                    (HOUSEKEEPING_W+COMMS_EXTRA_W,COMMS_H)):
            ok,v,h,why=dispatch(w,t)
            if ok:
                daily_ohmic+=h
                daily_load+=w*t
                daily_min_v.append(v)
            else:
                critical_ok=False
                if daily_reason=='ok':
                    daily_reason=why
        if critical_ok:
            critical_days+=1
        # Final 10-min slot: drive if feasible; otherwise stand by during that slot.
        can_drive=critical_ok and not (failed_source is not None and
                      failed_source not in active and suspend_mobility_after_failure)
        drive_ok=False
        if can_drive:
            drive_ok,v,h,why=dispatch(HOUSEKEEPING_W+MOBILITY_EXTRA_W,MOBILITY_H,
                                      protect_critical_days=DAYS-day)
            if drive_ok:
                daily_ohmic+=h
                daily_load+=(HOUSEKEEPING_W+MOBILITY_EXTRA_W)*MOBILITY_H
                daily_min_v.append(v)
                mobility_days+=1
            elif daily_reason=='ok':
                daily_reason=why
        elif critical_ok and daily_reason=='ok':
            daily_reason='fault_policy'
        if not drive_ok:
            idle_ok,v,h,why=dispatch(HOUSEKEEPING_W,MOBILITY_H)
            if idle_ok:
                daily_ohmic+=h
                daily_load+=HOUSEKEEPING_W*MOBILITY_H
                daily_min_v.append(v)
            elif daily_reason=='ok':
                daily_reason=why
        if daily_reason!='ok':
            failure_reasons[daily_reason]=failure_reasons.get(daily_reason,0)+1
        cumulative_ohmic_wh+=daily_ohmic
        cumulative_load_wh+=daily_load
        # Path loss = electrical energy at source terminals - delivered load energy.
        cumulative_path_loss_wh+=daily_load*(1/p.path_efficiency-1)
        rows.append({'scenario':label,'day':day,'active_sources':'+'.join(active) or 'none',
          'critical_ok':int(critical_ok),'mobility_ok':int(drive_ok),
          'min_terminal_v':round(min(daily_min_v),4) if daily_min_v else '',
          'soc_u0':round(soc['u0'],5),'soc_u5':round(soc['u5'],5) if 'u5' in active else '',
          'load_energy_wh':round(daily_load,5),
          'cell_ohmic_heat_wh':round(daily_ohmic,5),
          'reason':daily_reason})
    return {'scenario':label,'critical_days':critical_days,
            'mobility_days':mobility_days,
            'min_soc_active':min(soc[n] for n in active) if active else None,
            'cell_ohmic_heat_wh':round(cumulative_ohmic_wh,3),
            'load_energy_wh':round(cumulative_load_wh,3),
            'converter_path_loss_wh':round(cumulative_path_loss_wh,3),
            'failure_reasons':failure_reasons,'rows':rows}


def demonstration_cases():
    # All cell capacity/current/resistance parameters: synthetic sensitivity cases.
    baseline = CellAssumptions()
    return [
      simulate('19S4P_cap2A',baseline),
      simulate('19S4P_cap0p7A',CellAssumptions(max_current_a_per_string=0.70)),
      simulate('19S6P_cap2A',CellAssumptions(parallel_strings_per_source=3)),
      simulate('19S6P_u5fails_day20',CellAssumptions(parallel_strings_per_source=3),
               failed_source='u5',failure_day=20),
      simulate('19S6P_higherR',CellAssumptions(parallel_strings_per_source=3,
                                            resistance_ohm_per_cell=0.35))
    ]


def main():
    results=demonstration_cases()
    for r in results:
        print(f"{r['scenario']}: critical={r['critical_days']}/60, "
              f"mobility={r['mobility_days']}/60, "
              f"heat={r['cell_ohmic_heat_wh']:.2f} Wh; "
              f"end min active SOC={r['min_soc_active']:.3f}; "
              f"flags={r['failure_reasons']}")
    if len(sys.argv)>1:
        out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
        rows=[day for scenario in results for day in scenario['rows']]
        with out.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        print('Saved',out)

if __name__=='__main__':
    main()
