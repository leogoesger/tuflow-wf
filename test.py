import arcpy
from time import sleep

fc = "C:/Users/jpablo/Desktop/tuflow-wf/ex-shp/Mexico_Ciudades.shp"
a = arcpy.Describe(fc).spatialReference

print a.Name
print("hello")