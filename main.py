import os
from generate_file_structure import generate_file_structure
from create_boundary import create_boundary
from update_attri_table import update_attri_table
from run_tuflow import run_tuflow


NAME = raw_input("Enter the file name -> ")
meter = raw_input("Enter buffer distance -> ")
RUN = raw_input("What is the RUN for files? -> ")

create_boundary(NAME, meter)
generate_file_structure(NAME,RUN)
update_attri_table(NAME)
run_tuflow(NAME, RUN)
