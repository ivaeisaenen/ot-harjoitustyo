"""Input/Output test module"""
import unittest

from inpout import inpout
import random
import os
import sys
import shutil
import h5py

class LogOpen:
    """Class to emulate open log file"""
    def __init__(self):
        self.list_of_strings = []
    def write(self, string_):
        """Append string to list of strings"""
        string_ = str(string_)
        self.list_of_strings.append(string_)
    def close(self):
        """Print out list of strings"""
        # print(self.list_of_strings)
        pass


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


    def test_read_stress0(self):
        """Testing invalid inputs"""

        input_dict = {}
        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = []

        with self.assertRaises(SystemExit) as cm:
            inpout.read_stress(input_dict)
            self.assertEqual(cm.exception.code, 123)


    def test_read_stress_h5_example1(self):
        """Test read stress function with correct inputs"""
        input_dict = {}
        stress_history_dict_ = {1: [[ 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/example1.hdf5"]
        inpout.read_stress(input_dict)
        stress_history_dict = input_dict["stress_history"]
        self.assertEqual(stress_history_dict, stress_history_dict_)


    def test_read_stress_h5_example2(self):
        """Test read stress function with correct inputs"""
        input_dict = {}
        stress_history_dict_ = {555:[[1.0,2.0,3.0,4.0,5.0,6.0],
                                       [100.0,110.0,120.0,130.0,140.0,150.0]],
                                666:[[0.0,0.0,0.0,0.0,0.0,0.0],
                                       [300.0,100.0,500.0,200.0,100.0,100.0]] }

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/example2.hdf5"]
        inpout.read_stress(input_dict)
        stress_history_dict = input_dict["stress_history"]
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
        """Test read stress function with wrong lenght of stress tensor (Voigt notation)"""
        input_dict = {}

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1_erronous_data_for_testing1.txt",
                                     "./data/stress_history2.txt"]

        with self.assertRaises(SystemExit) as cm:
            inpout.read_stress(input_dict)
            self.assertEqual(cm.exception.code, 44)

    def test_read_stress3(self):
        """Test read stress function with stress tensor has alphabet u instead of number"""
        input_dict = {}

        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1_erronous_data_for_testing2.txt",
                                     "./data/stress_history2.txt"]

        with self.assertRaises(SystemExit) as cm:
            self.assertRaises(ValueError, inpout.read_stress(input_dict))
            self.assertEqual(cm.exception.code, 66)


    def test_read_stress4(self):
        """Test read stress function with node value is abc instead of number"""
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


    def test_write_results_ascii(self):
        """test ascii result writing"""

        input_dict = {}
        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/stress_history1.txt",
                                     "./data/stress_history2.txt"]
        inpout.read_stress(input_dict)

        # Read the stress history and node ids from file to generate fatigue results
        inpout.read_stress(input_dict)
        ids_ = list(input_dict["stress_history"].keys())
        fatigue_result_dict = {}
        for id_ in ids_:
            result_dict = {"SF": random.random()*10,
                        "Saf": random.random()*100,
                        "Sa": random.random()*50,
                        "Sm": random.random()*10}
            fatigue_result_dict[id_] = result_dict

        input_dict["results"] = fatigue_result_dict

        # Write fatigue results
        input_dict["input_files"] = ["./data/temp/stress_history1_temp_for_unittesting.txt",
                                     "./data/temp/stress_history2_temp_for_unittesting.txt"]
        inpout.write_results(input_dict)

        # Now read the file confirm the writing correct
        output_filename = input_dict["input_files"][0][:-4] + "_result.txt"
        with open(output_filename, "r") as file_handle:
            lines = file_handle.readlines()
            for k, line in enumerate(lines):
                line_splitted = line.split(",")
                if k == 0:
                    header = line_splitted
                    for idx, str_ in enumerate(header):
                        header[idx] = str_.strip()
                    res_ = [[0]*(len(header)-1) for _ in range(len(lines)-1)]
                else:
                    for i in range(len(header)-1):
                        # if len(line_splitted) == len(header)-1:
                        if len(line_splitted) > 0:
                            res_[k-1][i] = float(line_splitted[i+1])

            fatigue_result_dict_ = {}
            for node_idx in range(len(ids_)):
                if ids_[node_idx] not in fatigue_result_dict_:
                    fatigue_result_dict_[ids_[node_idx]] = {}
                for i, key_ in enumerate(header[1:]):
                    fatigue_result_dict_[ids_[node_idx]][key_] = res_[node_idx][i]

        self.assertEqual(fatigue_result_dict, fatigue_result_dict_)



    def test_write_results_h5(self):
        """test h5 result writing"""

        # Copy example file to temporary file
        shutil.copy("./data/example2.hdf5", "./data/temp/example2_temp_for_unittesting.hdf5")

        input_dict = {}
        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = ["./data/temp/example2_temp_for_unittesting.hdf5"]

        # Read the stress history and node ids from file to generate fatigue results
        inpout.read_stress(input_dict)
        ids_ = input_dict["stress_history"].keys()
        fatigue_result_dict = {}
        for id_ in ids_:
            result_dict = {"SF": random.random()*10,
                        "Saf": random.random()*100,
                        "Sa": random.random()*50,
                        "Sm": random.random()*10}
            fatigue_result_dict[id_] = result_dict

        input_dict["results"] = fatigue_result_dict

        # Write fatigue results
        inpout.write_results(input_dict)

        # Now read the file confirm the writing correct
        with h5py.File(input_dict["input_files"][0], "r") as h5file:
            ids_ = list(h5file["nodes"]["ids"])
            fr_group = h5file['nodes']['fatigue_results']
            fat_keys = list(fr_group.keys())
            res_ = [[0]*(len(fat_keys)) for _ in range(len(ids_))]
            for i, s_str in enumerate(fat_keys):
                for k in range(len(ids_)):
                    res_[k][i] = list(fr_group[s_str])[k]

            fatigue_result_dict_ = {}
            for node_idx in range(len(ids_)):
                if ids_[node_idx] not in fatigue_result_dict_:
                    fatigue_result_dict_[ids_[node_idx]] = {}
                for i, key_ in enumerate(fat_keys):
                    fatigue_result_dict_[ids_[node_idx]][key_] = res_[node_idx][i]

        self.assertEqual(fatigue_result_dict, fatigue_result_dict_)


    def test_write_results(self):
        """Testing invalid inputs"""

        input_dict = {}
        log = LogOpen()
        input_dict["log"] = log
        input_dict["input_files"] = []

        with self.assertRaises(SystemExit) as cm:
            inpout.write_results(input_dict)
            self.assertEqual(cm.exception.code, 1234)