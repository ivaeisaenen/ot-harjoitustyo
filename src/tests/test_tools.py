"""Tools test module"""
import unittest
# from criteria import _mises, calculate_equivalent_mises, calculate_mises_sf
# from mean_stress_correction import haigh_goodman
from tools import tools

class LogOpen:
    """Class to emulate open log file"""
    def __init__(self):
        self.list_of_strings = []
    def write(self, s):
        s = str(s)
        self.list_of_strings.append(s)
    def close(self):
        pass

class TestTools(unittest.TestCase):

    def test_calculate1(self):
        input_dict = {}

        log = LogOpen()
        input_dict["log"] = log

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

        steel_dict = {"fR1":100.0, "Rm":300}
        material_dict = {"steel":steel_dict}
        input_dict["material_dict"] = material_dict
        input_dict["material_name"] = "steel"
        input_dict["material"] = "steel"
        input_dict["stress_history"] = stress_history_dict
        input_dict["criterion"] = "mises"
        input_dict["material"] = "steel"
        input_dict["mean_stress_correction"] = "goodman"
        input_dict["Error"] = False


        tools.calculate(input_dict)
        result_dict = input_dict["results"]
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


    def test_calculate2(self):
        """Wrong criterion name"""
        fat_str = "umppalumppa"

        input_dict = {}
        input_dict["error"] = False

        log = LogOpen()
        input_dict["log"] = log

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

        steel_dict = {"fR1":100.0, "Rm":300}
        material_dict = {"steel":steel_dict}
        input_dict["material_dict"] = material_dict
        input_dict["material_name"] = "steel"
        input_dict["material"] = "steel"
        input_dict["stress_history"] = stress_history_dict
        input_dict["criterion"] = fat_str
        input_dict["material"] = "steel"
        input_dict["mean_stress_correction"] = "goodman"

        with self.assertRaises(SystemExit) as cm:
            tools.calculate(input_dict)
            self.assertEqual(cm.exception.code, 11)

        test_passed = False
        for s in input_dict["log"].list_of_strings:
            print(f"s11={s}")
            if "calculate: Invalid fatigue solver name umppalumppa ..." in s:
                test_passed = True
        self.assertTrue(test_passed == True)
        self.assertTrue(input_dict["error"] == True)

    def test_calculate3(self):
        """Wrong material name"""
        mat_str = "umppalumppa"
        input_dict = {}
        input_dict["error"] = False

        log = LogOpen()
        input_dict["log"] = log

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

        steel_dict = {"fR1":100.0, "Rm":300}
        material_dict = {"steel":steel_dict}
        input_dict["material_dict"] = material_dict
        input_dict["material_name"] = mat_str
        input_dict["material"] = "steel"
        input_dict["stress_history"] = stress_history_dict
        input_dict["criterion"] = "mises"
        input_dict["material"] = mat_str
        input_dict["mean_stress_correction"] = "goodman"

        with self.assertRaises(SystemExit) as cm:
            tools.calculate(input_dict)
            self.assertEqual(cm.exception.code, 22)

        test_passed = False
        for s in input_dict["log"].list_of_strings:
            print(f"s22={s}")
            if f"calculate: Invalid material name \"{mat_str}\"" in s:
                test_passed = True
        self.assertTrue(test_passed)
        self.assertTrue(input_dict["error"] == True)


    def test_calculate4(self):
        """Wrong mean stress correction name"""
        msc_str = "umppalumppa"
        input_dict = {}
        input_dict["error"] = False

        log = LogOpen()
        input_dict["log"] = log

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

        steel_dict = {"fR1":100.0, "Rm":300}
        material_dict = {"steel":steel_dict}
        input_dict["material_dict"] = material_dict
        input_dict["material_name"] = "steel"
        input_dict["material"] = "steel"
        input_dict["stress_history"] = stress_history_dict
        input_dict["criterion"] = "mises"
        input_dict["material"] = "steel"
        input_dict["mean_stress_correction"] = msc_str

        with self.assertRaises(SystemExit) as cm:
            tools.calculate(input_dict)
            self.assertEqual(cm.exception.code, 33)

        test_passed = False
        for s in input_dict["log"].list_of_strings:
            print(f"s={s}")
            if f"calculate: Invalid msc name \"{msc_str}\" ..." in s:
                test_passed = True
        self.assertTrue(test_passed == True)
        self.assertTrue(input_dict["error"] == True)