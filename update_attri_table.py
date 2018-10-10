import arcpy
import os

arcpy.CheckOutExtension("3D")


def update_attri_table(NAME):
    input_path = os.path.abspath(
        "output_folder/{}_tuflow/model/gis".format(NAME))

    code_R_shp = os.path.join(input_path, "2d_code_{}_R.shp".format(NAME))
    po_P_shp = os.path.join(input_path, "2d_po_{}_P.shp".format(NAME))
    po_L_shp = os.path.join(input_path, "2d_po_{}_L.shp".format(NAME))
    loc_L_shp = os.path.join(input_path, "2d_loc_{}_L.shp".format(NAME))
    bc_HT_L_shp = os.path.join(input_path, "2d_bc_{}_HT_L.shp".format(NAME))
    sa_QT_shp = os.path.join(input_path, "2d_sa_{}_QT_R.shp".format(NAME))

    code_r_fields = ["code"]
    with arcpy.da.UpdateCursor(code_R_shp, code_r_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
                continue
            row[0] = 1
            cursor.updateRow(row)

    po_P_fields = ["type", "label"]
    with arcpy.da.UpdateCursor(po_P_shp, po_P_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
                continue
            row[0] = "V_" + row[0]
            row[1] = index
            cursor.updateRow(row)

    po_L_fields = ["type", "label"]
    with arcpy.da.UpdateCursor(po_L_shp, po_L_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
                continue
            row[0] = "Q_" + row[0]
            row[1] = index
            cursor.updateRow(row)

    loc_L_fields = ["comment"]
    with arcpy.da.UpdateCursor(loc_L_shp, loc_L_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
                continue

    bc_HT_L_fields = ["type", "name"]
    with arcpy.da.UpdateCursor(bc_HT_L_shp, bc_HT_L_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
                continue
            row[0] = "HT"
            row[1] = "RPout"
            cursor.updateRow(row)

    sa_QT_fields = ["name"]
    with arcpy.da.UpdateCursor(sa_QT_shp, sa_QT_fields) as cursor:
        for index, row in enumerate(cursor):
            if index == 0:
                cursor.deleteRow()
                continue
            row[0] = "RPin"
            cursor.updateRow(row)
