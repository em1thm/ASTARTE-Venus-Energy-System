"""Physics, accounting and mission regression tests for ASTARTE V0.3."""
import unittest
from dataclasses import replace
from mechanoron_v03 import CellAssumptions,electrical_point,simulate,demonstration_cases

class TheveninTests(unittest.TestCase):
    def test_electrical_power_balance(self):
        p=CellAssumptions()
        x=electrical_point(p,0.75,30)
        self.assertIsNotNone(x)
        self.assertAlmostEqual(x['current_a']*x['terminal_v'],30,places=8)
        self.assertAlmostEqual(x['ohmic_w'],x['current_a']**2*p.pack_r_ohm,places=8)

    def test_zero_resistance_limit(self):
        p=CellAssumptions(resistance_ohm_per_cell=0)
        x=electrical_point(p,0.90,30)
        self.assertAlmostEqual(x['ohmic_w'],0)
        self.assertAlmostEqual(x['terminal_v'],p.source_ocv(.90))

    def test_current_ceiling_denies_high_power(self):
        p=CellAssumptions(max_current_a_per_string=.05)
        self.assertIsNone(electrical_point(p,.9,30))

    def test_infeasible_power_has_no_solution(self):
        p=CellAssumptions(resistance_ohm_per_cell=10.,
                          max_current_a_per_string=100)
        self.assertIsNone(electrical_point(p,.9,100))

    def test_temperature_parameter_increases_r(self):
        a=CellAssumptions(resistance_temp_slope_per_c=.005,temperature_c=465)
        b=replace(a,temperature_c=485)
        self.assertGreater(b.pack_r_ohm,a.pack_r_ohm)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            CellAssumptions(path_efficiency=0.)
        with self.assertRaises(ValueError):
            CellAssumptions(parallel_strings_per_source=0)

class MissionTests(unittest.TestCase):
    def test_60_day_rows(self):
        r=simulate('base',CellAssumptions())
        self.assertEqual(60,len(r['rows']))
        self.assertEqual(60,r['critical_days'])

    def test_increase_self_discharge_is_adverse(self):
        a=simulate('low',CellAssumptions(daily_self_discharge=0))
        b=simulate('high',CellAssumptions(daily_self_discharge=0.012))
        self.assertLessEqual(b['critical_days'],a['critical_days'])
        self.assertLessEqual(b['mobility_days'],a['mobility_days'])

    def test_low_current_cap_prevents_mobility(self):
        a=simulate('lowcap',CellAssumptions(max_current_a_per_string=.70))
        self.assertEqual(0,a['mobility_days'])
        self.assertEqual(60,a['critical_days'])

    def test_load_energy_accounting(self):
        r=simulate('large',CellAssumptions(parallel_strings_per_source=3,
                                            daily_self_discharge=0))
        self.assertEqual(60,r['mobility_days'])
        self.assertAlmostEqual(r['load_energy_wh'],1320.0,places=5)
        self.assertAlmostEqual(r['converter_path_loss_wh'],
            1320.0*(1/.85-1),places=2)

    def test_module_fault_and_no_drive_policy(self):
        r=simulate('fault',CellAssumptions(parallel_strings_per_source=3),
                   failed_source='u5',failure_day=20)
        self.assertTrue(all(x['mobility_ok']==0 for x in r['rows'][19:]))
        self.assertEqual('u0',r['rows'][19]['active_sources'])

    def test_disconnected_graph_reports_failure(self):
        from mechanoron_network import pentakis_graph
        g=pentakis_graph()
        isolated=[('f0',n) for n in g['f0']]
        r=simulate('cut',CellAssumptions(),broken_edges=isolated)
        self.assertEqual(0,r['critical_days'])

    def test_higher_r_increases_heat_for_fixed_small_load(self):
        a=electrical_point(CellAssumptions(resistance_ohm_per_cell=.1),.75,10)
        b=electrical_point(CellAssumptions(resistance_ohm_per_cell=.3),.75,10)
        self.assertGreater(b['ohmic_w'],a['ohmic_w'])

if __name__=='__main__':
    unittest.main()
