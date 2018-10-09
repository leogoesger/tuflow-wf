import arcpy
import os

field = "gridcode"
field2 = "Id"
arcpy.CheckOutExtension("3D")


def update_attri_table(NAME):
    input_path = os.path.abspath(
        "output_folder/{}_tuflow/model/gis".format(NAME))

    # Example below
    """
    fc = os.path.join(input_path, "{}_bound_rec.shp".format(NAME))

    cursor = arcpy.UpdateCursor(fc)
    with arcpy.da.UpdateCursor(fc, [field, field2]) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
    """

    code_R_shp = os.path.join(input_path, "2d_code_{}_R.shp".format(NAME))
    po_P_shp = os.path.join(input_path, "2d_po_{}_P.shp".format(NAME))
    po_L_shp = os.path.join(input_path, "2d_po_{}_L.shp".format(NAME))
    loc_L_shp = os.path.join(input_path, "2d_loc_{}_L.shp".format(NAME))
    bc_HT_L_shp = os.path.join(input_path, "2d_bc_{}_HT_L.shp".format(NAME))
    sa_QT_shp = os.path.join(input_path, "2d_sa_{}_QT.shp".format(NAME))

    code_r_fields = ["code"]
    with arcpy.da.UpdateCursor(code_R_shp, code_r_fields) as cursor:
        for index, row in enumerate(cursor):
            row.setValue("code", 1)
            cursor.updateRow(row)
            # missing measure tool step

    po_P_fields = ["type"]
    with arcpy.da.UpdateCursor(po_P_shp, po_P_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
            row.setValue("type", "V_" + row.getValue("type"))
            # missing add a label for each point

    po_L_fields = ["type"]
    with arcpy.da.UpdateCursor(po_L_shp, po_L_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
            row.setValue("type", "Q_" + row.getValue("type"))
            # missing add a label for each point

    loc_L_fields = ["type"]
    with arcpy.da.UpdateCursor(loc_L_shp, loc_L_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()

    bc_HT_L_fields = ["type", "name"]
    with arcpy.da.UpdateCursor(bc_HT_L_shp, bc_HT_L_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
            row.setValue("type", "HT")
            row.setValue("name", "RPout")

    sa_QT_fields = ["name"]
    with arcpy.da.UpdateCursor(sa_QT_shp, sa_QT_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
            row.setValue("name", "Rpin")
