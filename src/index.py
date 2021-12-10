"""The main module"""

# General modules import
import time
import json

# Program's own modules import
from tools import tools
from inpout import inpout

# Read inputs
with open("./data/input.json", "r", encoding='utf-8') as inputfile:
    input_dict = json.load(inputfile)

# Open log file
t1 = time.time()
log = open(input_dict["input_files"][0][:-4] + "_log.txt", "w", encoding='utf-8')  # pylint: disable=R1732
input_dict["log"] = log

# Read material library
inpout.read_materials(input_dict)

# Read the stress history
inpout.read_stress(input_dict)

# Calculate
tools.calculate(input_dict)

# Write results to a file
inpout.write_results(input_dict)

# Close log file
t2 = time.time()
log.write(f"Finished calculation in {t2-t1} seconds\n")
log.close()
