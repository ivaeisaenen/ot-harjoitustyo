"""Mean stress correction test module"""
import unittest
from mean_stress_correction import haigh_goodman, haigh_soderberg, haigh_gerbel, haigh_none

class TestMeanStressCorrection(unittest.TestCase):
    """Test mean stress correction methods"""

    def test_haigh_none(self):
        """Test none mean stress correction"""
        material_dict = {"fR1": 100}
        vals = [[532,4234],[423,4324],[0,4324],[323,0],[43,-3132]]
        for val in vals:
            stress_amplitude1 = val[0]
            mean_stress1 = val[1]
            stress_amplitudef1 = haigh_none(stress_amplitude1, mean_stress1, material_dict)
            self.assertEqual(stress_amplitudef1, material_dict["fR1"])


    def test_haigh_goodman1(self):
        """Goodman mean stress correction tests part 1

            Zero mean stress tests
        """
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
        """Goodman mean stress correction tests part 2

            Positive mean stress less than ultimate limit
        """
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = 200
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 100.0)


    def test_haigh_goodman3(self):
        """Goodman mean stress correction tests part 3

            Negative mean stress less than ultimate limit
        """
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = -200
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 100.0)


    def test_haigh_goodman4(self):
        """Goodman mean stress correction tests part 4

            Negative mean stress more than ultimate limit
        """
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = -500
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 0.0)


    def test_haigh_goodman5(self):
        """Goodman mean stress correction tests part 5

            Positive mean stress more than ultimate limit
        """
        material_dict = {"fR1": 200,
                         "Rm": 400}
        stress_amplitude = 100
        mean_stress = 500
        stress_amplitudef = haigh_goodman(stress_amplitude,mean_stress, material_dict)
        self.assertEqual(stress_amplitudef, 0.0)


    def test_haigh_goodman6(self):
        """Test Goodman mean stress correction"""

        vals = [{"fR1":200, "Rm":400, "amplitude": 100, "mean": 0, "saf":200},
                {"fR1":200, "Rm":400, "amplitude": 100, "mean": 200, "saf":100},
                {"fR1":200, "Rm":400, "amplitude": 100, "mean": -200, "saf":100},
                {"fR1":200, "Rm":400, "amplitude": 100, "mean": 500, "saf":0},
                {"fR1":200, "Rm":400, "amplitude": 100, "mean": -500, "saf":0},
                {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": 0, "saf":200},
                {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": 200, "saf":100},
                {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": -400, "saf":100},
                {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": 500, "saf":0},
                {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": -900, "saf":0}]

        for dict_ in vals:
            material_dict = {"fR1": dict_["fR1"],
                             "Rm": dict_["Rm"]}
            if "Rmc" in dict_:
                material_dict["Rmc"] = dict_["Rmc"]
            stress_amplitudef = haigh_goodman(dict_["amplitude"], dict_["mean"], material_dict)
            self.assertEqual(stress_amplitudef, dict_["saf"])

    def test_haigh_soderberg(self):
        """Test Soderberg mean stress correction"""

        vals = [{"fR1":200, "Rp02":400, "amplitude": 100, "mean": 0, "saf":200},
                {"fR1":200, "Rp02":400, "amplitude": 100, "mean": 200, "saf":100},
                {"fR1":200, "Rp02":400, "amplitude": 100, "mean": -200, "saf":100},
                {"fR1":200, "Rp02":400, "amplitude": 100, "mean": 500, "saf":0},
                {"fR1":200, "Rp02":400, "amplitude": 100, "mean": -500, "saf":0},
                {"fR1":200, "Rp02":400, "Rpc02":-800, "amplitude": 100, "mean": 0, "saf":200},
                {"fR1":200, "Rp02":400, "Rpc02":-800, "amplitude": 100, "mean": 200, "saf":100},
                {"fR1":200, "Rp02":400, "Rpc02":-800, "amplitude": 100, "mean": -400, "saf":100},
                {"fR1":200, "Rp02":400, "Rpc02":-800, "amplitude": 100, "mean": 500, "saf":0},
                {"fR1":200, "Rp02":400, "Rpc02":-800, "amplitude": 100, "mean": -900, "saf":0}]

        for dict_ in vals:
            material_dict = {"fR1": dict_["fR1"],
                             "Rp02": dict_["Rp02"]}
            if "Rpc02" in dict_:
                material_dict["Rpc02"] = dict_["Rpc02"]
            stress_amplitudef = haigh_soderberg(dict_["amplitude"], dict_["mean"], material_dict)
            self.assertEqual(stress_amplitudef, dict_["saf"])


    def test_haigh_gerbel(self):
        """Test Soderberg mean stress correction"""

        test_values = [{"fR1":200, "Rm":400, "amplitude": 100, "mean": 0, "saf":200},
                       {"fR1":200, "Rm":400, "amplitude": 100, "mean": 200, "saf":150},
                       {"fR1":200, "Rm":400, "amplitude": 100, "mean": -200, "saf":150},
                       {"fR1":200, "Rm":400, "amplitude": 100, "mean": 500, "saf":0},
                       {"fR1":200, "Rm":400, "amplitude": 100, "mean": -500, "saf":0},
                       {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": 0, "saf":200},
                       {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": 200, "saf":150},
                       {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": -400, "saf":150},
                       {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": 500, "saf":0},
                       {"fR1":200, "Rm":400, "Rmc":-800, "amplitude": 100, "mean": -900, "saf":0}]

        for dict_ in test_values:
            material_dict = {"fR1": dict_["fR1"],
                             "Rm": dict_["Rm"]}
            if "Rmc" in dict_:
                material_dict["Rmc"] = dict_["Rmc"]
            stress_amplitudef = haigh_gerbel(dict_["amplitude"], dict_["mean"], material_dict)
            self.assertEqual(stress_amplitudef, dict_["saf"])
