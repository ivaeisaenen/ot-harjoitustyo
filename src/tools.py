"""Tools like input / ouput and program logic between user input and calculations"""
import sys
# Import fatigue calculation criteria
from criteria import calculate_mises_sf
# from criteria import calculate_MMK_sf

# Import mean stress corrections
from mean_stress_correction import haigh_goodman
# from mean_stress_correction import haigh_cast_iron
# from mean_stress_correction import haigh_steel

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

    log.write(f"Stress read \"{input_dict['input_files']}\" lenght {len(stress_history)}")


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


def calculate(input_dict):
    """Calcualtes the results based on inputs

        Here will be logic to check if material inputs are valid for given criterion
        after multiple criteria and materials are implemented.

        Same logic should be also in GUI so that there should not be any miss matches,
        but for now progman is used from input file or actually for development phase
        from input dictionary, which will be later constructed using input/output tools
    """
    log = input_dict["log"]
    stress = input_dict["stress_history"]

    fat_str = input_dict["criterion"]
    mat_str = input_dict["material"]
    msc_str = input_dict["mean_stress_correction"]

    if fat_str == "mises":
        fatigue_solver = calculate_mises_sf
    # elif fat_str == "MMK":
        # fatigue_solver == calculate_MMK_sf
    else:
        log.write(f"calculate: Invalid fatigue solver name \"{fat_str}\" ...\n")
        log.close()
        sys.exit()

    if mat_str == "steel":
        mat = input_dict["material_dict"]["steel"]
    # elif mat_str == "cast_iron":
        # mat = cast_iron
    else:
        log.write(f"calculate: Invalid material name \"{mat_str}\" ...\n")
        log.close()
        sys.exit()

    if msc_str == "goodman":
        msc = haigh_goodman
    # elif msc_str == "haigh_cast_iron":
        # msc = haigh_cast_iron
    else:
        log.write(f"calculate: Invalid material name \"{mat_str}\" ...\n")
        log.close()
        sys.exit()


    log.write("Start running fatigue solver\n")
    results = fatigue_solver(stress, mat, msc)
    log.write("Done running fatigue solver\n")
    input_dict["results"] = results


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
