import arcpy
import os

class Toolbox(object):
    def __init__(self):
        self.label = "Toolbox"
        self.alias = ""
        self.tools = [BuildingProximity]


class BuildingProximity(object):
    def __init__(self):
        self.label = "Building Proximity"
        self.description = "Determine which buildings are near garages"
        self.canRunInBackground = False

    def getParameterInfo(self):

        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdbFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="gdbName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garageCSV",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="garageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="campusGDB",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="bufferDistance",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )

        return [param0, param1, param2, param3, param4, param5]

    def execute(self, parameters, messages):

        arcpy.env.overwriteOutput = True

        folder_path = parameters[0].valueAsText
        gdb_name_in = parameters[1].valueAsText
        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        campus_gdb = parameters[4].valueAsText
        buffer_distance = int(parameters[5].value)

       
        gdb_base = gdb_name_in
        if gdb_base.lower().endswith(".gdb"):
            gdb_base = gdb_base[:-4]

        gdb_path = os.path.join(folder_path, gdb_base + ".gdb")

        
        if not arcpy.Exists(gdb_path):
            arcpy.management.CreateFileGDB(folder_path, gdb_base)

      
        arcpy.management.MakeXYEventLayer(csv_path, "X", "Y", garage_layer_name)

        garage_points_fc = os.path.join(gdb_path, garage_layer_name)
        arcpy.management.CopyFeatures(garage_layer_name, garage_points_fc)

       
        structures_fc = os.path.join(campus_gdb, "Structures")
        buildings_fc = os.path.join(gdb_path, "Buildings")

        arcpy.AddMessage("Campus GDB selected: " + campus_gdb)
        arcpy.AddMessage("Looking for Structures at: " + structures_fc)

        if not arcpy.Exists(structures_fc):
            raise Exception("ERROR: Structures not found at: " + structures_fc +
                            "\nYou probably selected the wrong Campus.gdb in the tool.")

        arcpy.management.CopyFeatures(structures_fc, buildings_fc)

        spatial_ref = arcpy.Describe(buildings_fc).spatialReference

        garage_projected = os.path.join(gdb_path, "Garage_Points_projected")
        arcpy.management.Project(garage_points_fc, garage_projected, spatial_ref)

      
        garage_buffer = os.path.join(gdb_path, "Garage_Buffer")
        arcpy.analysis.Buffer(garage_projected, garage_buffer, buffer_distance)

    
        intersection_fc = os.path.join(gdb_path, "Garage_Building_Intersection")
        arcpy.analysis.Intersect([garage_buffer, buildings_fc], intersection_fc)

        
