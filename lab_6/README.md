import arcpy

import time

import os



class Toolbox(object):

&nbsp;   def \_\_init\_\_(self):

&nbsp;       self.label = "Toolbox"

&nbsp;       self.alias = ""

&nbsp;       self.tools = \[GraduatedColorsRenderer]



class GraduatedColorsRenderer(object):

&nbsp;   def \_\_init\_\_(self):

&nbsp;       self.label = "graduatedcolor"

&nbsp;       self.description = "create a graduated colored map based on a specific attribute of a layer"

&nbsp;       self.canRunInBackground = False

&nbsp;       self.category = "MapTools"



&nbsp;   def getParameterInfo(self):



&nbsp;       # Input ArcGIS Pro Project

&nbsp;       param0 = arcpy.Parameter(

&nbsp;           displayName="Input ArcGIS Pro Project Name",

&nbsp;           name="aprxInputName",

&nbsp;           datatype="DEFile",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       # Layer to classify

&nbsp;       param1 = arcpy.Parameter(

&nbsp;           displayName="Layer to Classify",

&nbsp;           name="LayerToClassify",

&nbsp;           datatype="GPLayer",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       # Output folder

&nbsp;       param2 = arcpy.Parameter(

&nbsp;           displayName="Output Location",

&nbsp;           name="OutputLocation",

&nbsp;           datatype="DEFolder",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       # Output project name

&nbsp;       param3 = arcpy.Parameter(

&nbsp;           displayName="Output Project Name",

&nbsp;           name="OutputProjectName",

&nbsp;           datatype="GPString",

&nbsp;           parameterType="Required",

&nbsp;           direction="Input"

&nbsp;       )



&nbsp;       return \[param0, param1, param2, param3]



&nbsp;   def isLicensed(self):

&nbsp;       return True



&nbsp;   def updateParameters(self, parameters):

&nbsp;       return



&nbsp;   def updateMessages(self, parameters):

&nbsp;       return



&nbsp;   def execute(self, parameters, messages):



&nbsp;       readTime = 3

&nbsp;       start = 0

&nbsp;       max\_range = 100

&nbsp;       step = 33



&nbsp;       # Setup Progressor

&nbsp;       arcpy.SetProgressor("step", "Validating Project File...", start, max\_range, step)

&nbsp;       time.sleep(readTime)

&nbsp;       arcpy.AddMessage("Validating Project File...")



&nbsp;       # Open project

&nbsp;       project = arcpy.mp.ArcGISProject(parameters\[0].valueAsText)



&nbsp;       # Get first map (safer than listMaps('Map')\[0])

&nbsp;       campus = project.listMaps("Map")\[0]



&nbsp;       # Increment progressor

&nbsp;       arcpy.SetProgressorPosition(start + step)

&nbsp;       arcpy.SetProgressorLabel("Finding your map layer...")

&nbsp;       time.sleep(readTime)

&nbsp;       arcpy.AddMessage("Finding your map layer...")



&nbsp;       # Loop through layers

&nbsp;       for layer in campus.listLayers():



&nbsp;           if layer.isFeatureLayer:



&nbsp;               symbology = layer.symbology



&nbsp;               if hasattr(symbology, 'renderer'):



&nbsp;                   if layer.name == parameters\[1].value.name:



&nbsp;                       # Progress

&nbsp;                       arcpy.SetProgressorPosition(start + step \* 2)

&nbsp;                       arcpy.SetProgressorLabel("Calculating and classifying...")

&nbsp;                       time.sleep(readTime)

&nbsp;                       arcpy.AddMessage("Calculating and classifying...")



&nbsp;                       # Apply Graduated Colors Renderer

&nbsp;                       symbology.updateRenderer('GraduatedColorsRenderer')



&nbsp;                       # IMPORTANT FIX (video correction)

&nbsp;                       symbology.renderer.classificationField = "Shape\_Area"



&nbsp;                       # Set number of classes

&nbsp;                       symbology.renderer.breakCount = 5



&nbsp;                       # Set color ramp

&nbsp;                       symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')\[0]



&nbsp;                       # Apply symbology

&nbsp;                       layer.symbology = symbology



&nbsp;                       arcpy.AddMessage("Finish Generating Layer...")



&nbsp;       # Final progress

&nbsp;       arcpy.SetProgressorPosition(start + step \* 3)

&nbsp;       arcpy.SetProgressorLabel("Saving...")

&nbsp;       time.sleep(readTime)

&nbsp;       arcpy.AddMessage("Saving...")



&nbsp;       # Save copy

&nbsp;       output\_path = os.path.join(parameters\[2].valueAsText,

&nbsp;                                  parameters\[3].valueAsText + ".aprx")



&nbsp;       project.saveACopy(output\_path)



&nbsp;       return

