import os
import errno
import subprocess
from shutil import rmtree, copyfile, copy2, copytree, copy


def generate_file_structure(NAME, RUN):

    output_folder = os.path.abspath("output_folder/" + NAME + "_tuflow")
    bc_dbase_folder = os.path.abspath(
        "output_folder/" + NAME + "_tuflow/bc_dbase")
    model_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/model")
    runs_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/runs")

    if os.path.isdir("output_folder/" + NAME + "_tuflow"):
        rmtree("output_folder/" + NAME + "_tuflow")

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
    copyfile("output_folder/shp_files/" + NAME + "_bound_rec.prj",
             model_folder + "/gis/Projection.prj")

    # step 4.1, 4.2
    os.rename(runs_folder + "/Name_001.tcf",
              runs_folder + "/" + NAME + "_" + RUN + ".tcf")

    # edit NAME to actual name in tuflow.bat
    bat_file_path = os.path.join(
        runs_folder, NAME + "_run_" + RUN + "_TUFLOW.bat")

    with open(os.path.join(bat_file_path), 'r+') as myfile:
        text = myfile.read().replace("NAME", NAME).replace(
            "RUNN", RUN)  # RUN exists in two places in bat file
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    # run tuflow sub process
    p = subprocess.Popen(bat_file_path, shell=True, stdout=subprocess.PIPE)
    p.communicate()

    desired_files = ["2d_code_empty_R", "2d_loc_empty_L",
                     "2d_mat_empty_R", "2d_po_empty_L", "2d_po_empty_P"]

    for f in os.listdir(model_folder + "/gis/empty"):
        file_path = os.path.join(model_folder + "/gis/empty", f)

        if f.split(".")[0] == '2d_sa_empty_R':
            des_path = os.path.join(
                model_folder + "/gis", f.replace("_empty_", "_"+NAME+"_QT_"))
        elif f.split(".")[0] == '2d_bc_empty_L':
            des_path = os.path.join(
                model_folder + "/gis", f.replace("_empty_", "_"+NAME+"_HT_"))
        elif f.split(".")[0] in desired_files:
            des_path = os.path.join(
                model_folder + "/gis", f.replace("_empty_", "_"+NAME+"_"))
        else:
            continue

        copyfile(file_path, des_path)

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
