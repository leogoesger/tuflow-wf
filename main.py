import os
from generate_file_structure import generate_file_structure
from create_boundary import create_boundary
from update_attri_table import update_attri_table
from run_tuflow import run_tuflow


print ""
NAME = raw_input("Enter the file name (e.g. Eastfork) -> ")
print ""
meter = raw_input("Enter buffer distance [m] (e.g. -2 to buffer DEM boundary in by 2 meters) -> ")
print ""
run_number = raw_input("How many runs do you want for this channel type (1 run per unique discharge)?  -> ")

create_boundary(NAME, meter)
generate_file_structure(NAME,run_number)
update_attri_table(NAME)
run_tuflow(NAME, run_number)
