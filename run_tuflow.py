import os
import csv
import subprocess

def run_tuflow(NAME, run_number):
    runs_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/runs")
    model_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/model")
    bc_dbase_path=os.path.abspath("output_folder/" + NAME + "_tuflow/bc_dbase")
    material_file=os.path.join(model_folder,"materials.csv")
    tgc_file=os.path.join(model_folder, NAME + ".tgc")

    for i in range(int(run_number)):
        current_run = "00" + str(i+1)
        with open(os.path.join(runs_folder + "/" + current_run, NAME + ".tcf"), 'r+') as myfile:
            text = myfile.read().replace("Write Empty GIS Files ", "! Write Empty GIS Files ")
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()

        with open(os.path.join(bc_dbase_path + "/" + current_run, "2d_bc_" + NAME + ".csv" ), 'r+') as myfile:
            text = myfile.read().replace("NAME_bc_data", NAME+"_bc_data")
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()
        
        with open(os.path.join(runs_folder + "/" + current_run, NAME + "_TUFLOW.bat" ), 'r+') as myfile:
            text = myfile.read().replace("NAME", current_run + "\\" + NAME)
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()

    
    
    print("")
    print("Material manning's n options. Enter 1-4 to choose a pre-determined Manning's n or enter 5 to choose your own Manning's n")
    print("")
    print("1. gravel channel > 0.04")
    print("2. cobble boulder channel > 0.06 ")
    print("3. shrub > 0.01")
    print("4. dense vegetation > 0.3")
    print("5. enter your own manning's n")

    material_ID= raw_input("What is the Manning's n material ID? -> ")
    if material_ID=="5":
        mannings_n=raw_input("What is the Manning's n value? -> ")
        with open(material_file, 'r+') as myfile:
            text = myfile.read().replace("5,,,,!other", "5,{},,,!other".format(mannings_n))
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()
    with open(tgc_file, 'r+') as myfile:
        text = myfile.read().replace("Set Mat == 1", "Set Mat == {}".format(material_ID))
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()
    print ""
    print "NOTE: Running this code again will remove existing files and replace with new ones. To save files, copy the folder NAME_tuflow (within output_folder) and paste in a seperate location."    
    print ""
    print "REMINDER: Before running Tuflow, make sure the WSE (RPout) and flow (RPin) are added to the NAME_bc_data.csv spreadsheet located in NAME_Tuflow\ bc_dbase\RUN. This information will be different for each run."
    print ""
