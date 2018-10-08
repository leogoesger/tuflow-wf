import os

import arcpy
from shutil import rmtree


arcpy.CheckOutExtension("spatial")

def create_boundary(NAME):

    input_path = os.path.abspath("input_folder")
    output_path = os.path.abspath("output_folder/shp_files")

    if os.path.isdir("output_folder/shp_files"):
        rmtree('output_folder/shp_files')
    else:
        os.mkdir("output_folder/shp_files")


    asc_file_path = os.path.join(input_path, NAME+"_dem.3.asc")

    sfe3_boundary_shp= os.path.join(output_path, "sfe3_boundary_shp.shp")
    sfe3_bound_neg2m_shp = os.path.join(output_path, "sfe3_bound_neg2m_shp.shp")
    sfe3_bound_rec_shp = os.path.join(output_path, "sfe3_bound_rec_shp.shp")

    sfe3_1 = arcpy.sa.Reclassify(asc_file_path, "VALUE", "101.102745 105.156837 1;105.156837 108.940979 1")
    arcpy.RasterToPolygon_conversion(sfe3_1, sfe3_boundary_shp, "NO_SIMPLIFY", "VALUE", "SINGLE_OUTER_PART", "")
    arcpy.Buffer_analysis(sfe3_boundary_shp, sfe3_bound_neg2m_shp, "-2 Meters", "FULL", "ROUND", "NONE", "", "PLANAR") # require user input for meters
    arcpy.MinimumBoundingGeometry_management(sfe3_bound_neg2m_shp, sfe3_bound_rec_shp, "RECTANGLE_BY_AREA", "NONE", "", "NO_MBG_FIELDS")