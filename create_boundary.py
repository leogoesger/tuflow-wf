import arcpy
import os

def create_boundary(NAME):

    input_path = os.path.abspath("input_folder")

    asc_file_path = os.path.join(input_path, NAME+"_dem_1m.asc")
    print arcpy.RasterToPolygon_conversion(asc_file_path)