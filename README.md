virtualenv -p /usr/bin/python ENV

in C:/Python27/ArcGIS10.5/arcpy_includes

cd c:/Python27/ArcGIS10.5
mkdir arcpy_includes
cd arcpy_includes
cp c:/Python27/ArcGIS10.5/Lib/site-packages/Desktop10.5.pth ./ 
ln -s c:/Python27/ArcGIS10.5/Lib/site-packages/numpy numpy 

Now we create a file called sitecustomize.py, in C:/Python27/ArcGIS10.5/Lib

import site

site.addsitedir('c:/Python27/ArcGIS10.5/arcpy_includes')


virtualenv --python C:/Python27/ArcGIS10.5/python.exe venv
source venv/Scripts/activate