import os
import csv
import subprocess

def run_tuflow(NAME, RUN):
    runs_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/runs")
    model_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/model")
    bat_file_path = os.path.join(
        runs_folder, NAME + "_" + RUN + "_TUFLOW.bat")
    bc_dbase_path=os.path.abspath("output_folder/" + NAME + "_tuflow/bc_dbase")
    bc_2d_bc_filepath=os.path.join(bc_dbase_path,"2d_bc_" + NAME + ".csv")
    bc_data=os.path.join(bc_dbase_path, NAME + "_bc_data.csv")
    material_file=os.path.join(model_folder,"materials.csv")
    tgc_file=os.path.join(model_folder, NAME +"_"+ RUN + ".tgc")

    with open(os.path.join(runs_folder, NAME + "_" + RUN + ".tcf"), 'r+') as myfile:
        text = myfile.read().replace("Write Empty GIS Files == ..\model\gis\empty | SHP", "! Write Empty GIS Files == ..\model\gis\empty | SHP")
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    with open(bc_2d_bc_filepath, 'r+') as myfile:
        text = myfile.read().replace("NAME_bc_data", NAME+"_bc_data")
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()
    

    is_asking_flow_parameters = True
    bc_data_inputs = [["Time","RPin","RPout"]]

    while is_asking_flow_parameters: 
        print ""
        timing=raw_input("what is time equal to ()? -> ")
        RPin=raw_input("what is flow? -> ")
        RPout=raw_input("what is the water surface elevation? -> ")
        addition=raw_input("Do you want to add another (y/n)? -> ")
        if addition=="n":
            is_asking_flow_parameters=False
        bc_data_inputs.append([timing, RPin, RPout])
    
    with open(bc_data, "w") as output:
        writer = csv.writer(output, delimiter=",", lineterminator="\n")
        for dataset in bc_data_inputs:
            writer.writerow(dataset)
    
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

    # subprocess.Popen(bat_file_path, shell=True, stdout=subprocess.PIPE)
