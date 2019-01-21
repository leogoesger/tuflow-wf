import os
import errno
import subprocess
from shutil import rmtree, copyfile, copy2, copytree, copy


def generate_file_structure(NAME, run_number):

    output_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/")
    bc_dbase_folder_init = os.path.abspath(
        "output_folder/" + NAME + "_tuflow/bc_dbase/init")
    bc_dbase_folder = os.path.abspath(
        "output_folder/" + NAME + "_tuflow/bc_dbase/")
    model_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/model/")
    runs_folder_init = os.path.abspath("output_folder/" + NAME + "_tuflow/runs/init/")
    runs_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/runs/")
    check_folder_init = os.path.abspath("output_folder/" + NAME + "_tuflow/check/init/")
    results_folder_init = os.path.abspath("output_folder/" + NAME + "_tuflow/results/init/")
    check_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/check/")
    results_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/results/")
    grid_folder = os.path.abspath("output_folder/" + NAME + "_tuflow/model/grid/") 

    # edit NAME to actual name in tuflow.bat
    bat_file_path = os.path.join(
        runs_folder_init, NAME + "_TUFLOW.bat")

    if os.path.isdir("output_folder/" + NAME + "_tuflow"):
        rmtree("output_folder/" + NAME + "_tuflow")
    

    # copy everything from template folder to output folder
    copytree("template", output_folder)
    copyfile("input_folder/" + NAME + ".asc", os.path.join(grid_folder, NAME + ".asc"))
    copyfile("input_folder/" + NAME + ".prj", os.path.join(grid_folder, NAME + ".prj"))

    os.rename(os.path.join(bc_dbase_folder_init, "2d_bc_NAME.csv"),
              os.path.join(bc_dbase_folder_init, "2d_bc_"+NAME+".csv"))
    os.rename(os.path.join(bc_dbase_folder_init, "NAME_bc_data.csv"),
              os.path.join(bc_dbase_folder_init, NAME+"_bc_data.csv"))
    os.rename(os.path.join(model_folder, "NAME.tbc"),
              os.path.join(model_folder, NAME + ".tbc"))
    os.rename(os.path.join(model_folder, "NAME.tgc"),
              os.path.join(model_folder, NAME + ".tgc"))
    os.rename(os.path.join(runs_folder_init, "NAME_TUFLOW.bat"),
              os.path.join(runs_folder_init, NAME + "_TUFLOW.bat"))
    os.rename(runs_folder_init + "/NAME.tcf",
              runs_folder_init + "/" + NAME + ".tcf")
    
    with open(os.path.join(bat_file_path), 'r+') as myfile:
        text = myfile.read().replace("TUFLOW_OUTPUT_FOLDER", output_folder)
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    
    for num in range(int(run_number)):
        copytree(bc_dbase_folder_init, bc_dbase_folder + "/00" + str(num+1))
        copytree(runs_folder_init, runs_folder + "/00" + str(num+1))
        copytree(check_folder_init, check_folder + "/00" + str(num+1))
        copytree(results_folder_init, results_folder + "/00" + str(num+1))

    # step 2.5
    copyfile("output_folder/shp_files/" + NAME + "_bound_rec.prj",
             model_folder + "/gis/Projection.prj")


    

    with open(os.path.join(bat_file_path), 'r+') as myfile:
        text = myfile.read().replace("runs\NAME", "runs\init\\" + NAME).replace("NAME", NAME)
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    # run tuflow sub process
    p = subprocess.Popen(bat_file_path, shell=True, stdout=subprocess.PIPE)
    print("\nAfter empty template GIS files are created, hit Enter to continue...\n")
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
    print "STOP! Go to ArcGIS and edit GIS files in model/gis. When finished in Arc, resume by entering a value for DS water surface elevation..."
    iwl = raw_input("Downstream water surface elevation [m] (e.g. 1003.432) -> ") #or "1003.432"
    print ""
    print "Values inside the parenthesis are default values. Hit enter to accept default value or update with new value by typing in value and hitting enter."
    cell_depth = raw_input("Cell Wet/Dry Depth(0.1 m) -> ") or "0.1"
    end_time = raw_input("End Time(2 hrs) -> ") or "2"
    timestep = raw_input("Time Step(2.5 s) NOTE: use timestep that is 1/4 of grid size in meters -> ") or "2.5"
    mapOutput = raw_input("Start Map Output(0 s) -> ") or "0"
    mapOutputInterval = raw_input("Map Output Interval(600 s) -> ") or "600"
    tsOutputInterval = raw_input(
        "Time Series Output Interval(60 s)  -> ") or "60"

    for i in range(int(run_number)):
        current_run = "00" + str(i+1)
        f = open(os.path.join(runs_folder + "/" +current_run, NAME + ".tcf"), "a")
        f.write("\nDemo Model == ON" +
                "\n" +
                # "\nUnits == US Customary" +
                "\nGeometry Control File  ==  ..\\..\\model\\" + NAME + ".tgc" +
                "\nBC Control File == ..\\..\\model\\" + NAME + ".tbc" +
                "\nBC Database == ..\\..\\bc_dbase\\" + current_run +"\\2d_bc_" + NAME + ".csv" +
                "\nRead Materials File == ..\\..\\model\\materials.csv" + "     ! This provides the link between the material ID defined in the .tgc and the Manning's roughess" +
                "\nRead GIS PO == ..\\..\\model\\gis\\2d_po_" + NAME + "_P.shp" + "     ! velocity monitoring point locations" +
                "\nRead GIS PO == ..\\..\\model\\gis\\2d_po_" + NAME + "_L.shp" + "     ! flow monitoring xs lines" +
                "\n" +
                "\nViscosity Formulation == SMAGORINSKY" +
                "\nViscosity Coefficients == 0.5, 0.005" +
                "\nSET IWL == " + iwl + "   ! matches the downstream WSE" +
                "\nCell Wet/Dry Depth == " + cell_depth + "     ! Forces cells to be dry if their depth is < 0.1 m" +
                "\n" +
                "\nStart Time == 0" + "     ! Start Simulation at 0 hours" +
                "\nEnd Time == " + end_time + "     ! End Simulation (hrs)" +
                "\nTimestep == " + timestep + "     ! Use a 2D time step that is ~1/4 of the grid size in m (10 m * 0.25 -> 2.5 s)" +
                "\n" +
                "\nLog Folder == Log" + "   ! Redirects log output (eg. .tlf and _messages GIS layers to the folder log" +
                "\nOutput Folder == ..\\..\\results\\" + current_run + "\\" + "     ! Redirects results files to TUFLOW\Results\RUN" +
                "\nWrite Check Files == ..\\..\\check\\" + current_run + "\\" + "   ! Specifies check files to be written to TUFLOW\check\RUN" +
                "\nMap Output Format == GRID XMDF" + "  ! Output directly to GIS (grid) as well as SMS (xmdf compact) format" +
                "\nMap Output Data Types == h d n V BSS" + "    ! wse depth Manning's n velocity bed shear stress" +
                "\nStart Map Output == " + mapOutput + "    ! Start map output at 0 hours" +
                "\nMap Output Interval == " + mapOutputInterval + "     ! Output every 600 seconds (10 minutes)" +
                "\nGRID Map Output Data Types == h d n V BSS" +
                "\nTime Series Output Interval  == " + tsOutputInterval + "     ! time interval of output in seconds"
                )

    # Steps 5.1, 5.2
    with open(os.path.join(model_folder, NAME + ".tbc"), 'r+') as myfile:
        text = myfile.read().replace("NAME", NAME)
        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()

    with open(os.path.join(model_folder, NAME + ".tgc"), 'r+') as myfile:

        print ""
        print "If you haven't done so already, use the measure tool in ArcGIS to obtain the x,y dimension (m) of the code area polygon..."
        print ""
        cell_size = raw_input("Cell Size of code area polygon(10 m)-> ") or "10"
        grid_size = raw_input("Grid Size [m] (x,y dimension of the code area polygon rounded to be divisible by the cell size, e.g. 770,150)-> ") #or "770,150"
        z_pts = raw_input("Zpts(10000 m) (any elevation notably higher than project max z) -> ") or "10000"

        text = myfile.read().replace("NAME", NAME)
        text = text.replace("Cell Size == 10", "Cell Size == " + cell_size)
        text = text.replace("Grid Size (X,Y) == ", #770,150",
                            "Grid Size (X,Y) == " + grid_size)                    
        text = text.replace("Set Zpts == 10000", "Set Zpts == " + z_pts)

        myfile.seek(0)
        myfile.write(text)
        myfile.truncate()
