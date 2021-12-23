"""input / ouput for stress history and materials"""

import sys
import json
import h5py


def read_stress(input_dict):
    """Read stress history from ascii or HDF5 file, defined in input_dict"""
    input_filenames = input_dict["input_files"]
    log = input_dict["log"]
    if len(input_filenames) == 1 and input_filenames[0].split(".")[-1] == "hdf5":
        read_stress_h5(input_dict)
    elif len(input_filenames) > 0:
        read_stress_ascii(input_dict)
    else:
        log.write(f"Failed to read {len(input_filenames)} input files {str(input_filenames)} \
            and  stopping ...")
        log.close()
        sys.exit(123)


def read_stress_h5(input_dict):
    """Read stress from HDF5 file, defined in input_dict"""

    log = input_dict["log"]
    input_filename = input_dict["input_files"][0]
    with h5py.File(input_filename, "r") as h5file:
        ids_ = list(h5file["nodes"]["ids"])
        stress_history = []
        for timestepname in h5file['nodes']['stress'].keys():
            stress_tensor_group = h5file['nodes']['stress'][timestepname]

            tensor_ = [[0]*6 for _ in range(len(ids_))]
            for i, s_str in enumerate(["S11", "S22", "S33", "S23", "S13", "S12"]):
                for k in range(len(ids_)):
                    tensor_[k][i] = list(stress_tensor_group[s_str])[k]
            stress_history.append(tensor_)

        stress_history_dict_ = {}
        for i in range(len(stress_history)):
            for node_idx in range(len(ids_)):
                if ids_[node_idx] not in stress_history_dict_:
                    stress_history_dict_[ids_[node_idx]] = []
                stress_history_dict_[ids_[node_idx]].append(list(stress_history[i][node_idx]))
    input_dict["stress_history"] = stress_history_dict_
    log.write(f"Read h5 \"{input_dict['input_files']}\" len {len(stress_history)}\n")


def read_stress_ascii(input_dict):
    """Read stress history from ascii file, defined in input_dict"""

    log = input_dict["log"]
    input_files = input_dict["input_files"]
    datas = []
    for input_file in input_files:
        log.write(f"Reading file \"{input_file}\"\n")
        data = []
        id_ = []
        with open(input_file, "r", encoding='utf-8') as fil:
            for i, line in enumerate(fil.readlines()):
                line_splitted = line.split(",")
                if len(line_splitted) != 7:
                    log.write(f"Failed read file \"{input_file}\" line {i} \"{line}\" ...\n")
                    log.close()
                    sys.exit(44)
                try:
                    id_ = int(line_splitted[0])
                except ValueError:
                    log.write(f"Failed read file \"{input_file}\" line {i} \"{line}\" ...\n")
                    log.close()
                    sys.exit(55)

                stress = []
                for stress_component in line_splitted[1:]:
                    try:
                        stress.append(float(stress_component))
                    except ValueError:
                        log.write(f"Failed read file \"{input_file}\" line {i} \"{line}\" ...\n")
                        log.close()
                        sys.exit(66)

                data.append([id_, stress])
            datas.append(data)

    stress_history = reoder_stress_data(datas)
    input_dict["stress_history"] = stress_history

    log.write(f"Read ascii file \"{input_dict['input_files']}\" len {len(stress_history)}\n")

def reoder_stress_data(datas):
    """Reorder stress history from time steps including data for all nodes
        to node including all time steps
    """
    stress_history = {}
    for step_data in datas:
        for node_data in step_data:
            id_ = node_data[0]
            stress = node_data[1]
            if id_ in stress_history:
                stress_history[id_].append(stress)
            else:
                stress_history[id_] = [stress]
    return stress_history

def write_results_ascii(input_dict):
    """Write results as csv"""
    output_filename = input_dict["input_files"][0][:-4] + "_result.txt"
    with open(output_filename, "w", encoding='utf-8') as fil:
        tmp = input_dict["results"][list(input_dict["results"].keys())[0]].keys()
        header = "id, " + ", ".join(tmp)  + "\n"
        fil.write(header)
        for id_, results in input_dict["results"].items():
            values = results.values()
            values = [str(v) for v in values]
            values_str = ", ".join(values)
            fil.write(f"{id_}, {values_str}\n")


def write_results_h5(input_dict):
    """Write results to input hdf5 file"""
    fatigue_result_dict = input_dict["results"]
    filename = input_dict["input_files"][0]
    with h5py.File(filename, 'r+') as f:
        # node_ids = list(f["nodes"]["ids"])
        node_ids = list(fatigue_result_dict.keys())
        results_list = list(fatigue_result_dict.values())
        g = f["nodes"]
        gf = g.create_group("fatigue_results")

        # check out the keys
        keys_list = []
        for res_dict in results_list:
            for key in res_dict.keys():
                keys_list.append(key)
        keys_list = list(set(keys_list))
        # and create datasets
        dset_dict = {}
        for key_ in keys_list:
            dset = gf.create_dataset(key_, shape=((len(node_ids),)), dtype="float64")
            dset_dict[key_] = dset.ref
        # save values in datasets
        for i, res_dict in enumerate(results_list):
            keys_ = res_dict.keys()
            for key in keys_:
                gf[dset_dict[key]][i] = res_dict[key]


def write_results(input_dict):
    """Write fatigue results"""
    input_filenames = input_dict["input_files"]
    log = input_dict["log"]
    if len(input_filenames) == 1 and input_filenames[0].split(".")[-1] == "hdf5":
        write_results_h5(input_dict)
    elif len(input_filenames) > 0:
        write_results_ascii(input_dict)
    else:
        log.write(f"Failed to write {len(input_filenames)} input files {str(input_filenames)} \
            and  stopping ...")
        log.close()
        sys.exit(1234)


def read_materials(input_dict):
    """Read materials json file"""
    log = input_dict["log"]
    # Read material library
    if "materials" in input_dict:
        with open(input_dict["materials"], "r", encoding='utf-8') as matfile:
            material_dict = json.load(matfile)
        log.write("Available materials:\n")
        for key in material_dict.keys():
            log.write(f"{key}\n")
        input_dict["material_dict"] = material_dict
    else:
        log.write("Error! Material file has not been specified!")
        log.close()
        sys.exit(77)
