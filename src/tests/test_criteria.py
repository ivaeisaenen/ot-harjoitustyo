"""Criteria test module"""
import unittest
from criteria import _mises, calculate_equivalent_mises, calculate_mises_sf, \
                    _tresca, calculate_equivalent_tresca, calculate_tresca_sf
from mean_stress_correction import haigh_goodman, haigh_none

class TestCriteria(unittest.TestCase):
    """Tests for criteria.py

        Currently only for Von Mises and using Goodman mean stress correction
        when the mean stress correction is needed.
    """


    def test_tresca(self):
        """Tresca stress calculation test"""
        stress1 = [ 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        stress2 = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        stress3 = [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        stress4 = [ 6.0, 0.0, 2.0, 12.0, 0.0, 0.0]

        self.assertEqual(_tresca(stress1), 0.5)
        self.assertEqual(_tresca(stress2), 1.5)
        self.assertEqual(_tresca(stress3), 8.366025403784441)
        self.assertEqual(_tresca(stress4), 12.041594578792296)


    def test_calculate_equivalent_tresca(self):
        """Tresca equivalent stress calculation test"""

        # First
        stress_history = [[ 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [   0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        stress_amplitude, mean_stress = calculate_equivalent_tresca(stress_history)
        self.assertEqual(stress_amplitude, 50.0)
        self.assertEqual(mean_stress, 25.0)

        # Second
        stress_history = [[ 12.0, 0.0, 4.0, 24.0, 0.0, 0.0],
                          [-2.0, 0.0, -30.0, 8.0, 0.0, 6.0]]
        self.assertEqual(stress_amplitude, 50.0)
        self.assertEqual(mean_stress, 25.0)

    def test_calculate_tresca_sf(self):
        """Tresca safety factor calculation test"""

        material_dict = {"tR1": 57.735026919}

        stress_history_dict = {1: [[ 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                   [-100.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               2: [[   0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                   [-200.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               3: [[ 200.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                   [-200.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               4: [[ 12.0, 0.0, 4.0, 24.0, 0.0, 0.0],
                                  [ -2.0, 0.0, -30.0, 8.0, 0.0, 6.0]],
                               5: [[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                  [  0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               6: [[ 150.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                  [  150.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
                              }

        result_dict = calculate_tresca_sf(stress_history_dict, material_dict, msc=haigh_none)
        self.assertAlmostEqual(result_dict[1]["SF"], 1.15470053838)
        self.assertAlmostEqual(result_dict[1]["Saf"], 57.735026919)
        self.assertAlmostEqual(result_dict[1]["Sa"], 50.0)
        self.assertAlmostEqual(result_dict[1]["Sm"], 50.0)

        self.assertAlmostEqual(result_dict[2]["SF"], 0.57735026919)
        self.assertAlmostEqual(result_dict[2]["Saf"],  57.735026919)
        self.assertAlmostEqual(result_dict[2]["Sa"],  100.0)
        self.assertAlmostEqual(result_dict[2]["Sm"],   50.0)

        self.assertAlmostEqual(result_dict[3]["SF"],  0.57735026919)
        self.assertAlmostEqual(result_dict[3]["Saf"],  57.735026919)
        self.assertAlmostEqual(result_dict[3]["Sa"], 100.0)
        self.assertAlmostEqual(result_dict[3]["Sm"], 100.0)

        self.assertAlmostEqual(result_dict[4]["SF"], 2.3973165074284744)
        self.assertAlmostEqual(result_dict[4]["Saf"],  57.735026919)
        self.assertAlmostEqual(result_dict[4]["Sa"], 24.08318915758459)
        self.assertAlmostEqual(result_dict[4]["Sm"],   21.603211961447478)

        self.assertAlmostEqual(result_dict[5]["SF"],  57735026918.99999)
        self.assertAlmostEqual(result_dict[5]["Saf"],  57.735026919)
        self.assertAlmostEqual(result_dict[5]["Sa"],  0.0)
        self.assertAlmostEqual(result_dict[5]["Sm"],  0.0)

        self.assertAlmostEqual(result_dict[6]["SF"], 0.76980035892)
        self.assertAlmostEqual(result_dict[6]["Saf"],  57.735026919)
        self.assertAlmostEqual(result_dict[6]["Sa"], 75.0)
        self.assertAlmostEqual(result_dict[6]["Sm"], 75.0)


    def test_mises(self):
        """Von Mises stress calculation test"""
        stress1 = [ 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        stress2 = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        stress3 = [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        stress4 = [ 6.0, 0.0, 2.0, 12.0, 0.0, 0.0]

        self.assertEqual(_mises(stress1), 1.0)
        self.assertEqual(_mises(stress2), 3.0)
        self.assertEqual(_mises(stress3), 15.297058540778355)
        self.assertEqual(_mises(stress4), 21.447610589527216)


    def test_calculate_equivalent_mises(self):
        """Von Mises equivalent stress calculation test"""

        # First
        stress_history = [[ 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [   0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        stress_amplitude, mean_stress = calculate_equivalent_mises(stress_history)
        self.assertEqual(stress_amplitude, 50.0)
        self.assertEqual(mean_stress, 50.0)

        # second
        stress_history = [[ 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                          [-100.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        stress_amplitude, mean_stress = calculate_equivalent_mises(stress_history)
        self.assertEqual(stress_amplitude, 100.0)
        self.assertEqual(mean_stress,   0.0)


        # third
        stress_history = [[ 12.0, 0.0, 4.0, 24.0, 0.0, 0.0],
                          [-2.0, 0.0, -30.0, 8.0, 0.0, 6.0]]
        stress_amplitude, mean_stress = calculate_equivalent_mises(stress_history)
        self.assertEqual(stress_amplitude, 38.35914511481498)
        self.assertEqual(mean_stress, 4.536076064239452)

        # fourth
        stress_history = [[ 1.0, 2.0, 3.0, 1.0, 5.0, 9.0]]
        stress_amplitude, mean_stress = calculate_equivalent_mises(stress_history)
        self.assertEqual(stress_amplitude, 9.0)
        self.assertEqual(mean_stress, 9.0)


    def test_calculate_mises_sf(self):
        """Von Mises safety factor calculation test"""

        material_dict = {"fR1": 100,
                         "Rm": 300}

        stress_history_dict = {1: [[ 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                   [-100.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               2: [[   0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                   [-200.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               3: [[ 200.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                   [-200.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               4: [[ 12.0, 0.0, 4.0, 24.0, 0.0, 0.0],
                                  [ -2.0, 0.0, -30.0, 8.0, 0.0, 6.0]],
                               5: [[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                  [  0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                               6: [[ 150.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                  [  150.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
                              }

        result_dict = calculate_mises_sf(stress_history_dict, material_dict, haigh_goodman)
        self.assertAlmostEqual(result_dict[1]["SF"], 1.0)
        self.assertAlmostEqual(result_dict[1]["Saf"], 100.0)
        self.assertAlmostEqual(result_dict[1]["Sa"], 100.0)
        self.assertAlmostEqual(result_dict[1]["Sm"], 0.0)

        self.assertAlmostEqual(result_dict[2]["SF"], 2/3)
        self.assertAlmostEqual(result_dict[2]["Saf"], 200.0/3)
        self.assertAlmostEqual(result_dict[2]["Sa"],  100.0)
        self.assertAlmostEqual(result_dict[2]["Sm"], -100.0)

        self.assertAlmostEqual(result_dict[3]["SF"],  0.5)
        self.assertAlmostEqual(result_dict[3]["Saf"], 100.0)
        self.assertAlmostEqual(result_dict[3]["Sa"], 200.0)
        self.assertAlmostEqual(result_dict[3]["Sm"],  0.0)

        self.assertAlmostEqual(result_dict[4]["SF"], 2.5675226689871073)
        self.assertAlmostEqual(result_dict[4]["Saf"], 98.48797464525352)
        self.assertAlmostEqual(result_dict[4]["Sa"], 38.35914511481498)
        self.assertAlmostEqual(result_dict[4]["Sm"],  4.536076064239452)

        self.assertAlmostEqual(result_dict[5]["SF"],  1e11)
        self.assertAlmostEqual(result_dict[5]["Saf"], 100.0)
        self.assertAlmostEqual(result_dict[5]["Sa"],  0.0)
        self.assertAlmostEqual(result_dict[5]["Sm"],  0.0)

        self.assertAlmostEqual(result_dict[6]["SF"], 5e10)
        self.assertAlmostEqual(result_dict[6]["Saf"], 50.0)
        self.assertAlmostEqual(result_dict[6]["Sa"],  0.0)
        self.assertAlmostEqual(result_dict[6]["Sm"], 150.0)
