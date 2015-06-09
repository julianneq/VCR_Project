import arcpy as ap
import os
from convertDBFtoCSV import convertDBFtoCSV

def intersectGrid(AggLevel, workingDir, variable):
    '''Intersects the GHCN temperature data grid with the AggLevel = "Woreda" or "Kebele" shapefile'''

    #create grid shapefile
    Grid = workingDir + "\\All" + variable + "Grid.shp"
    if(os.path.exists(Grid)==False):
        if variable == "Temp":
            origin_coord = "-180 -90"
            nrows = "360"
            ncols = "720"
            polygon_width = "0.5 degrees"
        else:
            origin_coord = "-20.05 -40.05"
            nrows = "801"
            ncols = "751"
            polygon_width = "0.1 degrees"
    
        polygon_height = polygon_width
        ap.GridIndexFeatures_cartography(Grid, "", "", "", "", polygon_width, polygon_height, origin_coord, nrows, ncols)
        ap.DefineProjection_management(Grid,coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',\
        SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
    
        #add 3 or 4 fields to grid shapefile: latitude (LAT), longitude (LONG) and
        #for precipitation, row (row) of text file corresponding to each grid in the shapefile;
        #for temperature, row (row) and column (col) of netCDF file corresponding to each grid in the shapefile
        ap.AddField_management(Grid, "LAT", "DOUBLE", 7, 2, "", "", "", "", "")
        ap.AddField_management(Grid, "LONG", "DOUBLE", 7, 2, "", "", "", "", "")
        ap.AddField_management(Grid, "row", "SHORT", 6, "", "", "", "", "", "")
        if variable == "Temp":
            ap.AddField_management(Grid, "col", "SHORT", 5, "", "", "", "", "", "")

        #calculate lat and long fields
        expression1 = "float(!SHAPE.CENTROID!.split()[0])"
        expression2 = "float(!SHAPE.CENTROID!.split()[1])"
        ap.CalculateField_management(Grid, "LONG", expression1, "PYTHON")
        ap.CalculateField_management(Grid, "LAT", expression2, "PYTHON")

        #calculate row and col fields
        if variable == "Temp":
            Grid = calcTempFields(Grid)
        else:
            Grid = calcRainFields(Grid)

    #clip the grid to Ethiopia and convert its .dbf to a .csv for later use
    GridClip = workingDir + "\\" + variable + "GridClip" + AggLevel + ".shp"
    if AggLevel == 'Woreda':
        EthiopiaBorders = workingDir[0:-13] + "EthiopiaPolitical\\WoredasAdindan.shp"
    elif AggLevel == 'Kebele':
        EthiopiaBorders = workingDir[0:-13] + "EthiopiaPolitical\\Ethiopia Kebeles without Somali region.shp"

    ap.Clip_analysis(Grid, EthiopiaBorders, GridClip)
    dbf = GridClip[0:-4] + ".dbf"
    GridCSV = convertDBFtoCSV(dbf)

    #intersect the clipped grid with the woreda or kebele shapefile and project to Adindan
    GridIntersect = workingDir + "\\" + variable + AggLevel + "Intersect.shp"
    ap.Intersect_analysis([GridClip, EthiopiaBorders],GridIntersect)
    GridIntersectProject = GridIntersect[0:-4] + "Project.shp"
    ap.Project_management(GridIntersect,GridIntersectProject,out_coor_system="PROJCS['Adindan_UTM_Zone_37N',GEOGCS['GCS_Adindan',\
    DATUM['D_Adindan',SPHEROID['Clarke_1880_RGS',6378249.145,293.465]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],\
    PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],\
    PARAMETER['Central_Meridian',39.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],\
    UNIT['Meter',1.0]]",transform_method="Adindan_To_WGS_1984_1",in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',\
    SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")

    #calculate area of intersection between grid and woreda or kebele shapefile after adding a field to store it
    ap.AddField_management(GridIntersectProject, "PartArea", "DOUBLE", 12, 6, "", "", "", "", "")
    expression = "float(!SHAPE.AREA@SQUAREKILOMETERS!)"
    ap.CalculateField_management(GridIntersectProject, "PartArea", expression, "PYTHON")

    #convert GridIntersect's .dbf to a .csv for later use
    dbf = GridIntersectProject[0:-4] + ".dbf"
    intersectCSV = convertDBFtoCSV(dbf)
    
    return intersectCSV, GridCSV

def calcTempFields(Grid):
    expression1 = "getCol(!LONG!)"
    code_block1 = """def getCol(long):
        if long > 0:
            return 2*(long+0.25)-1
        elif long < 0:
            return 2*(long-0.25)+720"""
    ap.CalculateField_management(Grid, "col", expression1, "PYTHON", code_block1)

    expression2 = "180-2*(!LAT!-0.25)-1"
    ap.CalculateField_management(Grid, "row", expression2, "PYTHON")
    
    return Grid

def calcRainFields(Grid):
    expression = "750*(10*(!LAT!+40))+10*(!LONG!+20)"
    ap.CalculateField_management(Grid, "row", expression, "PYTHON")
    
    return Grid
