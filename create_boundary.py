import os

import arcpy
from shutil import rmtree


arcpy.CheckOutExtension("spatial")


def create_boundary(NAME, meter):

    input_path = os.path.abspath("input_folder")
    output_path = os.path.abspath("output_folder/shp_files")

    if os.path.isdir("output_folder/"):
        rmtree('output_folder/')
        os.mkdir("output_folder/")
        os.mkdir("output_folder/shp_files")
    else:
        os.mkdir("output_folder/")
        os.mkdir("output_folder/shp_files")

    asc_file_path = os.path.join(input_path, NAME + ".asc")
    prj_file_path = os.path.join(input_path, NAME + ".prj")
    boundary = os.path.join(output_path, "{}_boundary.shp".format(NAME))
    bound_neg2m = os.path.join(
        output_path, "{}_bound_neg2m.shp".format(NAME))
    bound_rec = os.path.join(output_path, "{}_bound_rec.shp".format(NAME))

    arcpy.DefineProjection_management(asc_file_path, prj_file_path)

    reclassified = arcpy.sa.Reclassify(
        asc_file_path, "VALUE", "0 10000 1") #"101.102745 105.156837 1;105.156837 108.940979 1")
    arcpy.RasterToPolygon_conversion(reclassified, boundary, "NO_SIMPLIFY")
    arcpy.Buffer_analysis(boundary, bound_neg2m, "{} Meters".format(meter),
                          "FULL", "ROUND", "NONE", "", "PLANAR")  # require user input for meters
    arcpy.MinimumBoundingGeometry_management(
        bound_neg2m, bound_rec, "RECTANGLE_BY_AREA", "NONE", "", "NO_MBG_FIELDS")
