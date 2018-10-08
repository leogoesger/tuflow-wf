import arcpy
import os

field = "gridcode"
field2 = "Id"
arcpy.CheckOutExtension("3D")

def update_attri_table():
    input_path = os.path.abspath("input_folder")
    fc = os.path.join(input_path, "sfe3_bound_rec_shp.shp")

    cursor = arcpy.UpdateCursor(fc)
    with arcpy.da.UpdateCursor(fc, [field, field2]) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()