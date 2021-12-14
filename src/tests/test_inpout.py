"""Input/Output test module"""
import unittest

from inpout import inpout

class LogOpen:
    """Class to emulate open log file"""
    def __init__(self):
        self.list_of_strings = []
    def write(self, s):
        s = str(s)
        self.list_of_strings.append(s)
    def close(self):
        print(self.list_of_strings)


class TestInputOutput(unittest.TestCase):
    """Test input and output module"""
    def test_reorder_stress_data(self):
        """Test reorder stress data function"""
        stress_history_dict_ = {555:[[1,2,3,4,5,6],
                                     [100,110,120,130,140,150]],
                                666:[[0,0,0,0,0,0],
                                     [300,100,500,200,100,100]] }

        datas = [[[555,[1,2,3,4,5,6]], [666,[0,0,0,0,0,0]]],
                 [[555,[100,110,120,130,140,150]], [666,[300,100,500,200,100,100]]]]
        stress_history_dict = inpout.reoder_stress_data(datas)

        self.assertEqual(stress_history_dict, stress_history_dict_)


    def test_read_stress(self):
        """Test read stress function with correct inputs"""
        input_dict = {}
        stress_history_dict_ = {555:[[1,2,3,4,5,6],
                                       [100,110,120,130,140,150]],
                                666:[[0,0,0,0,0,0],
                                       [300,100,500,200,100,100]] }

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1.txt",
                                     "./data/stress_history2.txt"]
        inpout.read_stress(input_dict)
        stress_history_dict = input_dict["stress_history"]
        self.assertEqual(stress_history_dict, stress_history_dict_)


    def test_read_stress2(self):
        """Test read stress function with wrong lenght of stress tensor (Voigt notation)
        """
        input_dict = {}

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1_erronous_data_for_testing1.txt",
                                     "./data/stress_history2.txt"]

        with self.assertRaises(SystemExit) as cm:
            inpout.read_stress(input_dict)
            self.assertEqual(cm.exception.code, 44)

    def test_read_stress3(self):
        """Test read stress function with stress tensor has alphabet u instead of number
        """
        input_dict = {}

        class LogOpen:
            def __init__(self):
                self.list_of_strings = []
            def write(self, s):
                s = str(s)
                self.list_of_strings.append(s)
            def close(self):
                print(self.list_of_strings)

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1_erronous_data_for_testing2.txt",
                                     "./data/stress_history2.txt"]

        with self.assertRaises(SystemExit) as cm:
            self.assertRaises(ValueError, inpout.read_stress(input_dict))
            self.assertEqual(cm.exception.code, 66)


    def test_read_stress4(self):
        """Test read stress function with node value is abc instead of number
        """
        input_dict = {}

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1_erronous_data_for_testing3.txt",
                                     "./data/stress_history2.txt"]

        with self.assertRaises(SystemExit) as cm:
            self.assertRaises(ValueError, inpout.read_stress(input_dict))
            self.assertEqual(cm.exception.code, 55)


    def test_read_materials(self):
        """Test read materials function with correct inputs"""

        material_dict_ = {"steel": {"fR1": 200.0, "fR0": 100.0, "Rm": 500.0, "Rp02": 300.0},
                          "cast_iron":{"fR1":90.0,"fR0":45.0,"Rm":100,"Rmc":350}}

        input_dict = {}


        log = LogOpen()
        input_dict["log"] = log
        input_dict["materials"] = "./data/materials.json"

        inpout.read_materials(input_dict)
        material_dict = input_dict["material_dict"]
        self.assertEqual(material_dict_, material_dict)


    def test_read_materials1(self):
        """Test read materials function with erronous inputs"""
        input_dict = {}

        log = LogOpen()
        input_dict["log"] = log

        with self.assertRaises(SystemExit) as cm:
            inpout.read_materials(input_dict)
            self.assertEqual(cm.exception.code, 77)
