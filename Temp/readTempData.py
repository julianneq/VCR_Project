import csv
import pylab
import numpy as np
from netCDF4 import Dataset

def readTempData(DataFile, GridCSV):
    '''Reads the GHCN netCDF file and stores all of the Ethiopia data in a matrix allData. \n
    Also makes a temperature heat map with the Ethiopia points overlaid'''
    
    #read in the temperature data
    tempData = Dataset(DataFile)
    lat = tempData.variables['lat'][:]
    lon = tempData.variables['lon'][:]
    temp = tempData.variables['air'][:]
    
    #determine the data length and create vectors of the month ('mon') and year ('yr') of each data point
    numMonths = len(temp[:,0,0])
    numFullYears = np.floor(numMonths/12)
    additionalMonths = np.mod(numMonths,12)
    mon = np.tile(np.arange(1,13),numFullYears)
    mon = np.append(mon,(np.arange(1,additionalMonths+1)))
    yr = np.arange(1948,1948+numFullYears)
    yr = np.repeat(yr,12)
    yr = np.append(yr,np.repeat(1948+numFullYears,additionalMonths))
    
    #read in GridCSV, which gives the rows and columns of 'temp' that are in Ethiopia
    Grid = csv.reader(open(GridCSV), delimiter = ",")
    Grid = np.array(list(Grid))
    col = Grid[1::,7]
    row = Grid[1::,6]
    numGridPts = len(col)
    
    #make a global temperature heatmap with the Ethiopia points overlaid
    #plotTempMap(lat, lon, temp, col, row)
    
    #create matrix 'allData' to store all of the data
    #dimensions are a x b x c where a = # of gridcells, b = 5 (lat, long, yr, mo, temp), 
    #and c = # of months
    allData = np.zeros([numGridPts,5,numMonths])
    for i in range(numGridPts):
        for j in range(numMonths):
            allData[i,0,j] = lat[int(row[i])]
            allData[i,1,j] = lon[int(col[i])]
            allData[i,2,j] = yr[j]
            allData[i,3,j] = mon[j]
            allData[i,4,j] = temp[j,int(row[i]),int(col[i])]-273.15 #temperature in degrees Celsius

    #define a grid cell ID by concatenating the row and col
    gridCells = []
    for i in range(len(col)):
        if len(row[i]) == 1:
            first3 = '00' + row[i]
        elif len(row[i]) == 2:
            first3 = '0' + row[i]
        else:
            first3 = row[i]
        if len(col[i]) == 1:
            last3 = '00' + col[i]
        elif len(col[i]) == 2:
            last3 = '0' + col[i]
        else:
            last3 = col[i]
        gridCells.append(first3 + last3)
    
    return allData, gridCells
    
def plotTempMap(lat, lon, temp, col, row):
    
    x, y = pylab.meshgrid(lon, lat)
    z = temp[0,:,:]
    
    xPts = np.zeros(len(col))
    yPts = np.zeros(len(row))
    for i in range(len(xPts)):
        xPts[i] = x[0,int(col[i])]
        yPts[i] = y[int(row[i]),0]
        
    pylab.pcolor(x,y,z)
    pylab.colorbar()
    pylab.scatter(xPts, yPts)
    pylab.savefig('TempHeatMap.png')
    pylab.close()
    
    return None
