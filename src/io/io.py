"""input / ouput for stress history"""
import sys
import json

def read_stress(input_dict):
    """Read stress history from file defined in input_dict"""

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
                    sys.exit()
                try:
                    id_ = int(line_splitted[0])
                    stress = []
                    for stress_component in line_splitted[1:]:
                        stress.append(float(stress_component))
                except TypeError:
                    log.write(f"Failed read file \"{input_file}\" line {i} \"{line}\" ...\n")
                    log.close()
                    sys.exit()
                data.append([id_, stress])
            datas.append(data)

    stress_history = reoder_stress_data(datas)
    input_dict["stress_history"] = stress_history

    log.write(f"Stress read \"{input_dict['input_files']}\" lenght {len(stress_history)}\n")

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

def write_results(input_dict):
    """Write results as csv"""
    output_filename = input_dict["input_files"][0][:-4] + "_result.txt"
    with open(output_filename, "w", encoding='utf-8') as fil:
        tmp = input_dict["results"][list(input_dict["results"].keys())[0]].keys()
        header = "id " + ", ".join(tmp)  + "\n"
        fil.write(header)
        for id_, results in input_dict["results"].items():
            values = results.values()
            values = [str(v) for v in values]
            values_str = ", ".join(values)
            fil.write(f"{id_}, {values_str}\n")

def read_materials(input_dict):
    log = input_dict("log")
    # Read material library
    if "materials" in input_dict:
        with open(input_dict["materials"], "r") as matfile:
            material_dict = json.load(matfile)
        log.write(f"Available materials:\n")
        for key in material_dict.keys():
            log.write(f"{key}\n")
        input_dict["material_dict"] = material_dict
    else:
        log.write("Error! Input have to spesicifed input file")
