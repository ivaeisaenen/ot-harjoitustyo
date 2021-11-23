"""Mean stress correction test module"""
import unittest
from mean_stress_correction import haigh_goodman

class TestMeanStressCorrection(unittest.TestCase):
    """Test mean stress correction methods"""


    def test_haigh_goodman1(self):
        """Goodman mean stress correction tests part 1"""
        material_dict = {"fR1": 100,
                         "Rm": 300}

        stress_amplitude1 = 0
        mean_stress1 = 0
        stress_amplitudef1 = haigh_goodman(stress_amplitude1,mean_stress1, material_dict)

        stress_amplitude2 = 55
        mean_stress2 = 0
        stress_amplitudef2 = haigh_goodman(stress_amplitude2,mean_stress2, material_dict)

        self.assertEqual(stress_amplitudef1, 100.0)
        self.assertEqual(stress_amplitudef2, 100.0)


    def test_haigh_goodman2(self):
        """Goodman mean stress correction tests part 2"""
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = 200
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 100.0)


    def test_haigh_goodman3(self):
        """Goodman mean stress correction tests part 3"""
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = -200
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 100.0)


    def test_haigh_goodman4(self):
        """Goodman mean stress correction tests part 4"""
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = -500
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 0.0)


    def test_haigh_goodman5(self):
        """Goodman mean stress correction tests part 5"""
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = 500
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 0.0)
