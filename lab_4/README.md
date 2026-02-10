

\# create a gdb and garage feature

import arcpy



arcpy.env.workspace = r"D:\\GEOG676\\New\_Folder\\Lab4"

folder\_path = r'D:\\GEOG676\\New\_Folder\\Lab4'

gdb\_name = 'Test.gdb'

gdb\_path = folder\_path + '\\\\' + gdb\_name

arcpy.CreateFileGDB\_management(folder\_path, gdb\_name)



csv\_path = r'D:\\GEOG676\\New\_Folder\\Lab4\\garages.csv'

garage\_layer\_name = 'Garage\_Points'

garages = arcpy.MakeXYEventLayer\_management(csv\_path, 'X', 'Y', garage\_layer\_name)



input\_layer = garages

arcpy.FeatureClassToGeodatabase\_conversion(input\_layer, gdb\_path)

garage\_points = gdb\_path + '\\\\' + garage\_layer\_name



\# open campus gdb, copy building feature to our gdb

campus = r'D:\\GEOG676\\New\_Folder\\Lab4\\Campus.gdb'

buildings\_campus = campus + r'\\Structures'

buildings = gdb\_path + '\\\\' + 'Buildings'



arcpy.Copy\_management(buildings\_campus, buildings)



\# Re-Projection

spatial\_ref = arcpy.Describe(buildings).spatialReference

arcpy.Project\_management(garage\_points, gdb\_path + '\\Garage\_Points\_reprojected', spatial\_ref)



\# buffer the garages

garageBuffered = arcpy.Buffer\_analysis(gdb\_path + '\\Garage\_Points\_reprojected', gdb\_path + '\\Garage\_Points\_buffered', 150)



\# Intersect our buffer with the buildings

arcpy.Intersect\_analysis(\[garageBuffered, buildings], gdb\_path + r'\\Garage\_Building\_Intersection', 'ALL')



arcpy.TableToTable\_conversion(gdb\_path + r'\\Garage\_Building\_Intersection', r'D:\\GEOG676\\New\_Folder\\Lab4', 'nearbyBuildings.csv')







