"""The main module"""
import time

from tools import calculate, read_stress, write_results
import json

####################################################
# Development inputs beging later these are read from input file (produced by GUI)
#####################################################
# steel = {"fR1": 200.0,  # Fatigue limit R=-1
#          "fR0": 100.0,  # Fatigue limit R=0
#          "Rm" : 500.0,   # Ultimate strengt
#          "Rp02": 300.0,  # Rp02 limit for elasticity
#          }

# material_dict = {"steel": steel}

# input_dict = {"material": "steel",
#               "criterion": "mises",
#               "mean_stress_correction": "goodman",
#               "input_files": ["./data/stress_history1.txt","./data/stress_history2.txt"],
#               "material_dict": material_dict,
#               "material": "steel"
#               }
# with open("steel.json", "w") as outputfile:
#     json.dump(steel, outputfile)
# with open("material.json", "w") as outputfile:
#     json.dump(material_dict, outputfile)
# with open("input.json", "w") as outputfile:
#     json.dump(input_dict, outputfile)

# Read inputs
with open("./data/input.json", "r") as inputfile:
    input_dict = json.load(inputfile)

##########################################################
# Developmnt inputs ends
##########################################################

# Open log file
t1 = time.time()
log = open(input_dict["input_files"][0][:-4] + "_log.txt", "w", encoding='utf-8')
input_dict["log"] = log

# Read material library
with open(input_dict["materials"], "r") as matfile:
    material_dict = json.load(matfile)
log.write(f"Available materials:\n")
for key in material_dict.keys():
    log.write(f"{key}\n")
input_dict["material_dict"] = material_dict


# Write all inputs information to the log file
for key, value in input_dict.items():
    if key != "log":
       log.write(f"{key}:{value}\n")

# Read the stress history
read_stress(input_dict)

# Calculate
calculate(input_dict)

# Write results to a file
write_results(input_dict)

t2 = time.time()
log.write(f"Finished calculation in {t2-t1} seconds\n")
log.close()
