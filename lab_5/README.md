import arcpy

import os



class Toolbox(object):

&nbsp;   def \_\_init\_\_(self):

&nbsp;       self.label = "Toolbox"

&nbsp;       self.alias = ""

&nbsp;       self.tools = \[BuildingProximity]





class BuildingProximity(object):

&nbsp;   def \_\_init\_\_(self):

&nbsp;       self.label = "Building Proximity"

&nbsp;       self.description = "Determine which buildings are near garages"

&nbsp;       self.canRunInBackground = False



&nbsp;   def getParameterInfo(self):



&nbsp;       param0 = arcpy.Parameter(

&nbsp;           displayName="GDB Folder",

&nbsp;           name="gdbFolder",

&nbsp;           datatype="DEFolder",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       param1 = arcpy.Parameter(

&nbsp;           displayName="GDB Name",

&nbsp;           name="gdbName",

&nbsp;           datatype="GPString",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       param2 = arcpy.Parameter(

&nbsp;           displayName="Garage CSV File",

&nbsp;           name="garageCSV",

&nbsp;           datatype="DEFile",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       param3 = arcpy.Parameter(

&nbsp;           displayName="Garage Layer Name",

&nbsp;           name="garageLayerName",

&nbsp;           datatype="GPString",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       param4 = arcpy.Parameter(

&nbsp;           displayName="Campus GDB",

&nbsp;           name="campusGDB",

&nbsp;           datatype="DEWorkspace",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       param5 = arcpy.Parameter(

&nbsp;           displayName="Buffer Distance",

&nbsp;           name="bufferDistance",

&nbsp;           datatype="GPLong",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       return \[param0, param1, param2, param3, param4, param5]



&nbsp;   def execute(self, parameters, messages):



&nbsp;       arcpy.env.overwriteOutput = True



&nbsp;       folder\_path = parameters\[0].valueAsText

&nbsp;       gdb\_name\_in = parameters\[1].valueAsText

&nbsp;       csv\_path = parameters\[2].valueAsText

&nbsp;       garage\_layer\_name = parameters\[3].valueAsText

&nbsp;       campus\_gdb = parameters\[4].valueAsText

&nbsp;       buffer\_distance = int(parameters\[5].value)



&nbsp;      

&nbsp;       gdb\_base = gdb\_name\_in

&nbsp;       if gdb\_base.lower().endswith(".gdb"):

&nbsp;           gdb\_base = gdb\_base\[:-4]



&nbsp;       gdb\_path = os.path.join(folder\_path, gdb\_base + ".gdb")



&nbsp;       

&nbsp;       if not arcpy.Exists(gdb\_path):

&nbsp;           arcpy.management.CreateFileGDB(folder\_path, gdb\_base)



&nbsp;     

&nbsp;       arcpy.management.MakeXYEventLayer(csv\_path, "X", "Y", garage\_layer\_name)



&nbsp;       garage\_points\_fc = os.path.join(gdb\_path, garage\_layer\_name)

&nbsp;       arcpy.management.CopyFeatures(garage\_layer\_name, garage\_points\_fc)



&nbsp;      

&nbsp;       structures\_fc = os.path.join(campus\_gdb, "Structures")

&nbsp;       buildings\_fc = os.path.join(gdb\_path, "Buildings")



&nbsp;       arcpy.AddMessage("Campus GDB selected: " + campus\_gdb)

&nbsp;       arcpy.AddMessage("Looking for Structures at: " + structures\_fc)



&nbsp;       if not arcpy.Exists(structures\_fc):

&nbsp;           raise Exception("ERROR: Structures not found at: " + structures\_fc +

&nbsp;                           "\\nYou probably selected the wrong Campus.gdb in the tool.")



&nbsp;       arcpy.management.CopyFeatures(structures\_fc, buildings\_fc)



&nbsp;       spatial\_ref = arcpy.Describe(buildings\_fc).spatialReference



&nbsp;       garage\_projected = os.path.join(gdb\_path, "Garage\_Points\_projected")

&nbsp;       arcpy.management.Project(garage\_points\_fc, garage\_projected, spatial\_ref)



&nbsp;     

&nbsp;       garage\_buffer = os.path.join(gdb\_path, "Garage\_Buffer")

&nbsp;       arcpy.analysis.Buffer(garage\_projected, garage\_buffer, buffer\_distance)



&nbsp;   

&nbsp;       intersection\_fc = os.path.join(gdb\_path, "Garage\_Building\_Intersection")

&nbsp;       arcpy.analysis.Intersect(\[garage\_buffer, buildings\_fc], intersection\_fc)



&nbsp;       



