import os
import errno
import subprocess
from shutil import rmtree, copyfile, copy2, copytree, copy

file_names = ["2d_bc_empty_L", "2d_code_empty_R", "2d_loc_empty_L",
              "2d_mat_empty_R", "2d_po_empty_L", "2d_po_empty_P", "2d_sa_empty_R"]


def generate_file_structure():
    NAME = raw_input("What is the NAME for files? -> ")
    RUN = raw_input("What is the RUN for files? -> ")
    # NAME = "VanillaC4"
    # RUN = "002"
    output_folder = os.path.abspath("output_folder/" + NAME + "_tuflow")
    bc_dbase_folder = os.path.abspath(
        "output_folder/" + NAME + "_tuflow/bc_dbase")
    model_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/model")
    runs_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/runs")

    if os.path.isdir("output_folder"):
        rmtree('output_folder')

    # step 2.3
    copytree("template/init", output_folder)

    os.rename(os.path.join(bc_dbase_folder, "2d_bc_NAME.csv"),
              os.path.join(bc_dbase_folder, "2d_bc_"+NAME+".csv"))
    os.rename(os.path.join(bc_dbase_folder, "NAME_bc_data.csv"),
              os.path.join(bc_dbase_folder, NAME+"_bc_data.csv"))
    os.rename(os.path.join(model_folder, "NAME_001.tbc"),
              os.path.join(model_folder, NAME + "_" + RUN + ".tbc"))
    os.rename(os.path.join(model_folder, "NAME_001.tgc"),
              os.path.join(model_folder, NAME + "_" + RUN + ".tgc"))
    os.rename(os.path.join(runs_folder, "NAME_run_001_TUFLOW.bat"),
              os.path.join(runs_folder, NAME + "_run_" + RUN + "_TUFLOW.bat"))

    # step 2.5
    copyfile("inputFiles/" + NAME + "_boundary.prj",
             model_folder + "/gis/Project.prj")

    # step 2.6
    # filepath = "D:/path/to/batch/myBatch.bat"
    # subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE)

    # step 2.8
    os.makedirs(model_folder + "/gis/empty")

    # next 4 lines are to replace step 2.6 above
    for f in file_names:
        file_path = os.path.join(model_folder + "/gis/empty", f)
        k = open(file_path, "w+")
        k.close()

    for f in os.listdir(model_folder + "/gis/empty"):
        file_path = os.path.join(model_folder + "/gis/empty", f)
        des_path = os.path.join(
            model_folder + "/gis", f.replace("_empty_", "_"+NAME+"_"))
        copyfile(file_path, des_path)

    # step 4.1, 4.2
    os.rename(runs_folder + "/Name_001.tcf",
              runs_folder + "/" + NAME + "_" + RUN + ".tcf")

    iwl = raw_input("IWL(7.3) -> ") or "7.3"
    cell_depth = raw_input("Cell Wet/Dry Depth(0.1) -> ") or "0.1"
    end_time = raw_input("End Time(2) -> ") or "2"
    timestep = raw_input("Time Step(2.5) -> ") or "2.5"
    mapOutput = raw_input("Start Map Output(0) -> ") or "0"
    mapOutputInterval = raw_input("Map Output Interval(600) -> ") or "600"
    tsOutputInterval = raw_input(
        "Time Series Output Interval(60)  -> ") or "60"

    f = open(os.path.join(runs_folder, NAME + "_" + RUN + ".tcf"), "a")
    f.write("\n! Demo Model == ON" +
            "\nUnits == US Customary" +
            "\nGeometry Control File  ==  ..\\model\\" + NAME + "_" + RUN + ".tgc" +
            "\nBC Control File == ..\\model\\" + NAME + "_" + RUN + ".tbc" +
            "\nBC Database == ..\\bc_dbase\\2d_bc_" + NAME + ".csv" +
            "\nRead Materials File == ..\\model\\" + NAME + "_materials.csv" +
            "\nRead GIS PO == ..\\model\\gis\\2d_po_" + NAME + "_P.shp" +
            "\nRead GIS PO ==..\\model\\gis\\2d_po_" + NAME + "_L.shp" +
            "\nViscosity Formulation == SMAGORINSKY" +
            "\nViscosity Coefficients == 0.5, 0.005" +
            "\nSET IWL == " + iwl +
            "\nCell Wet/Dry Depth == " + cell_depth +
            "\nStart Time == 0" +
            "\nEnd Time == " + end_time +
            "\nTime Step == " + timestep +
            "\nLog Folder == Log" +
            "\nOutput Folder == ..\\results\\RUN\\" +
            "\nWrite Check Files == ..\\check\\RUN\\" +
            "\nMap Output Format == GRID XMDF" +
            "\nMap Output Data Types == h d n V BSS" +
            "\nStart Map Output == " + mapOutput +
            "\nMap Output Interval == " + mapOutputInterval +
            "\nGRID Map Output Data Types == h d n V BSS" +
            "\nTime Series Output Interval  == " + tsOutputInterval
            )

    # Steps 5.1, 5.2
    with open(os.path.join(model_folder, NAME + "_" + RUN + ".tbc"), 'r+') as myfile:
        text = myfile.read().replace("NAME", NAME)
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    with open(os.path.join(model_folder, NAME + "_" + RUN + ".tgc"), 'r+') as myfile:

        cell_size = raw_input("Cell Size(3) -> ") or "3"
        grid_size = raw_input("Grid Size(18247,6926)-> ") or "18247,6926"
        z_pts = raw_input("Zpts(1500) -> ") or "1500"
        mat = raw_input("Material Id(1) -> ") or "1"

        text = myfile.read().replace("NAME", NAME)
        text = text.replace("Cell Size == 3", "Cell Size == " + cell_size)
        text = text.replace("Grid Size (X,Y) == 18247,6926",
                            "Grid Size (X,Y) == " + grid_size)
        text = text.replace("Set Zpts == 1500", "Set Zpts == " + z_pts)
        text = text.replace("Set Mat == 1", "Set Mat == " + mat)

        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    # Step 7.1
    with open(os.path.join(runs_folder, NAME + "_run_" + RUN + "_TUFLOW.bat"), 'r+') as myfile:

        text = myfile.read().replace("%RUN% \"NAME_001.tcf\" ",
                                     "%RUN% \"" + NAME + "_" + RUN + ".tcf\"")
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()
