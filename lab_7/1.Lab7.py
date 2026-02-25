import arcpy
import os

source = r"D:\GEOG676\Lab\Lab7"

arcpy.env.workspace = source
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# --- Use EXACT filenames shown in VS Code ---
band1 = arcpy.sa.Raster("band1.TIF")   # blue
band2 = arcpy.sa.Raster("band2.TIF")   # green
band3 = arcpy.sa.Raster("band3.TIF")   # red
band4 = arcpy.sa.Raster("band4.TIF")   # NIR

# Composite (4-band)
arcpy.management.CompositeBands([band1, band2, band3, band4], "output_combined.tif")

# Hillshade (DEM file is DEM.tif)
arcpy.ddd.HillShade("DEM.tif", "output_Hillshade.tif", 315, 45, "NO_SHADOWS", 1)

# Slope
arcpy.ddd.Slope("DEM.tif", "output_Slope.tif", "DEGREE", 1)

print("success!")
