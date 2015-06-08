import os
import arcpy as ap
from convertDBFtoCSV import convertDBFtoCSV
from joinSoilCSVs import joinSoilCSVs
from downloadSoilData import downloadSoilData

def processSoilData(AggLevel):
    '''Calculates average soil characteristics at AggLevel = "Woreda" or "Kebele" and outputs them to WoredaSoilData.csv or KebeleSoilData.csv'''

    #set the working directory
    workingDir = os.getcwd()

    #Download all of the soil data
    downloadSoilData(AggLevel, workingDir)

    #Turn on Spatial Statistics package and define field over which ZonalStatisticsAsTable will be calculated (Woreda or Kebele ID)
    ap.CheckOutExtension("Spatial")
    if AggLevel == 'Kebele':
        in_zone_data = os.path.dirname(workingDir) + "\\Shapefiles\\Ethiopia Kebeles without Somali region.shp"
        in_template_dataset = in_zone_data
        zone_field = "KebeleID"
    elif AggLevel == 'Woreda':
        in_zone_data = os.path.dirname(workingDir) + "\\Shapefiles\\WoredasWGS1984.shp"
        in_template_dataset = in_zone_data
        zone_field = "WOREDANO_"

    #Define the projection and change the working directory to the directory with all of the soil data folders
    latLongRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"
    os.chdir(workingDir)
    directories = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) == False]

    for i in range(len(directories)):
        #Find all the tiffs with soil data in each soil characteristic folder
        os.chdir(workingDir + "\\" + directories[i])
        filelist = os.listdir(os.getcwd())
        tiffs = []
        clipTiffs = []
        for j in range(len(filelist)):
            name = filelist[j]
            if name[-8::] == '250m.tif':
                tiffs.append(name)
            elif name[-9::] == '_Clip.tif':
                clipTiffs.append(name)

        for j in range(len(clipTiffs)):
            clipTiffs[j] = os.getcwd() + "\\" + clipTiffs[j]
            
        for j in range(len(tiffs)):
            in_raster = os.getcwd() + "\\" + tiffs[j]
            out_raster = os.getcwd() + "\\" + tiffs[j][0:-4] + "_Clip.tif"
            #Clip the tiffs to Ethiopia if they haven't been already
            if out_raster not in clipTiffs:
                ap.Clip_management(in_raster, "#", out_raster, in_template_dataset, "#", 1)

            #Calculate Zonal Statistics of soil data at AggLevel
            in_value_raster = out_raster
            out_table = os.getcwd() + "\\" + tiffs[j][0:-4] + AggLevel + ".dbf"
            ap.sa.ZonalStatisticsAsTable(in_zone_data, zone_field, in_value_raster, out_table)

    #Convert the DBFs with all the AggLevel soil data to CSVs
    #Change the working directory to the directory with all the soil data folders
    os.chdir(workingDir)
    directories = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) == False]

    for i in range(len(directories)):
        #Find all the DBFs with soil data in each soil characteristic folder
        os.chdir(workingDir + "\\" + directories[i])
        filelist = os.listdir(os.getcwd())
        DBFs = []
        for j in range(len(filelist)):
            name = filelist[j]
            if name[-10::] == AggLevel + '.dbf':
                DBFs.append(name)

        #Convert the DBF to a CSV
        for j in range(len(DBFs)):
            convertDBFtoCSV(os.getcwd() + "\\" + DBFs[j])

    #Join the CSVs with all the AggLevel soil data into one CSV titled "WoredaSoilData.csv" or "KebeleSoilData.csv" depending on the AggLevel
    joinSoilCSVs(AggLevel, workingDir)
            
    return None
