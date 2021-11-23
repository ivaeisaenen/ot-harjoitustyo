"""The main module"""
import time

from tools import calculate, read_stress, write_results

####################################################
# Development inputs beging later these are read from input file (produced by GUI)
#####################################################
steel = {"fR1": 200.0,  # Fatigue limit R=-1
         "fR0": 100.0,  # Fatigue limit R=0
         "Rm" : 500.0,   # Ultimate strengt
         "Rp02": 300.0,  # Rp02 limit for elasticity
         }

material_dict = {"steel": steel}

input_dict = {"material": "steel",
              "criterion": "mises",
              "mean_stress_correction": "goodman",
              "input_files": ["./data/stress_history1.txt","./data/stress_history2.txt"],
              "material_dict": material_dict
              }
##########################################################
# Developmnt inputs end
##########################################################
t1 = time.time()
log = open(input_dict["input_files"][0][:-4] + "_log.txt", "w", encoding='utf-8')
input_dict["log"] = log

# Write all inputs information to the log file
for key, value in input_dict.items():
    log.write(f"{key}:{value}\n")

# Read the stress history
read_stress(input_dict)

# calculate
calculate(input_dict)

write_results(input_dict)

t2 = time.time()
log.write(f"Finished calculation in {t2-t1} seconds\n")
log.close()
