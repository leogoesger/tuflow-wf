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
            text = myfile.read().replace("Write Empty GIS Files == ..\model\gis\empty | SHP", "! Write Empty GIS Files == ..\model\gis\empty | SHP")
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()

        with open(os.path.join(bc_dbase_path + "/" + current_run, "2d_bc_" + NAME + ".csv" ), 'r+') as myfile:
            text = myfile.read().replace("NAME_bc_data", NAME+"_bc_data")
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()
        
        with open(os.path.join(runs_folder + "/" + current_run, NAME + "_TUFLOW.bat" ), 'r+') as myfile:
            text = myfile.read().replace("runs\\" + NAME, current_run + "\\" + NAME)
            myfile.seek(0)
            myfile.write(text)
            myfile.truncate()

    
    
    print("")
    print("material manning's n options")
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

