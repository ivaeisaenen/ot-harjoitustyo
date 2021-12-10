"""The main module"""
import time
import json

from tools import tools
from io import io
# from io import read_stress, write_results


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
io.read_materials(input_dict)

# Read the stress history
io.read_stress(input_dict)

# Calculate
tools.calculate(input_dict)

# Write results to a file
io.write_results(input_dict)

t2 = time.time()
log.write(f"Finished calculation in {t2-t1} seconds\n")
log.close()
