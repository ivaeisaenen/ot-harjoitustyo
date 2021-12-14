"""Tools like calculations"""
import sys
# Import fatigue calculation criteria
from criteria import calculate_mises_sf
# from criteria import calculate_MMK_sf

# Import mean stress corrections
from mean_stress_correction import haigh_goodman
# from mean_stress_correction import haigh_cast_iron
# from mean_stress_correction import haigh_steel

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
        input_dict["error"] = True
        log.write(f"calculate: Invalid fatigue solver name {fat_str} ...\n")
        log.close()
        sys.exit(11)

    if input_dict["material_name"] in input_dict["material_dict"].keys():
        mat = input_dict["material_dict"][input_dict["material_name"]]
    else:
        input_dict["error"] = True
        log.write(f"calculate: Invalid material name \"{mat_str}\" ...\n")
        log.close()
        sys.exit(22)

    if msc_str == "goodman":
        msc = haigh_goodman
    # elif msc_str == "haigh_cast_iron":
        # msc = haigh_cast_iron
    else:
        input_dict["error"] = True
        log.write(f"calculate: Invalid msc name \"{msc_str}\" ...\n")
        log.close()
        sys.exit(33)


    log.write("Start running fatigue solver\n")
    results = fatigue_solver(stress, mat, msc)
    log.write("Done running fatigue solver\n")
    input_dict["results"] = results
