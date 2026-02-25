import arcpy
import time
import os

class Toolbox(object):
    def __init__(self):
        self.label = "Toolbox"
        self.alias = ""
        self.tools = [GraduatedColorsRenderer]

class GraduatedColorsRenderer(object):
    def __init__(self):
        self.label = "graduatedcolor"
        self.description = "create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):

        # Input ArcGIS Pro Project
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        # Layer to classify
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayerToClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        # Output folder
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        # Output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        return [param0, param1, param2, param3]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):

        readTime = 3
        start = 0
        max_range = 100
        step = 33

        # Setup Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max_range, step)
        time.sleep(readTime)
        arcpy.AddMessage("Validating Project File...")

        # Open project
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        # Get first map (safer than listMaps('Map')[0])
        campus = project.listMaps("Map")[0]

        # Increment progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        # Loop through layers
        for layer in campus.listLayers():

            if layer.isFeatureLayer:

                symbology = layer.symbology

                if hasattr(symbology, 'renderer'):

                    if layer.name == parameters[1].value.name:

                        # Progress
                        arcpy.SetProgressorPosition(start + step * 2)
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        # Apply Graduated Colors Renderer
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        # IMPORTANT FIX (video correction)
                        symbology.renderer.classificationField = "Shape_Area"

                        # Set number of classes
                        symbology.renderer.breakCount = 5

                        # Set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                        # Apply symbology
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")

        # Final progress
        arcpy.SetProgressorPosition(start + step * 3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        # Save copy
        output_path = os.path.join(parameters[2].valueAsText,
                                   parameters[3].valueAsText + ".aprx")

        project.saveACopy(output_path)


        return
