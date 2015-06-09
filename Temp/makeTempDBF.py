import os
import numpy as np
from downloadTempData import downloadTempData
from intersectGrid import intersectGrid
from readTempData import readTempData
from findTempWeightMatrix import findTempWeightMatrix

def makeTempDBF(AggLevel):
    '''Calculates weighted average monthly temperature at AggLevel = "Woreda" or "Kebele"'''

    #Set the working directory
    workingDir = os.getcwd()

    #Download the monthly temperature data from NOAA GHCN CAMS
    DataFile = downloadTempData(workingDir)

    #Intersect the GHCN grid with the Woreda or Kebele shapefile and convert the .dbf to a .csv
    intersectCSV, GridCSV = intersectGrid(AggLevel, workingDir, "Temp")

    #Read in raw monthly temperature data at every GHCN grid cell and store it in the matrix 'allData'
    #dimensions are a x b x c where a = # of gridcells, b = 5 (lat, long, yr, mo, temp), 
    #and c = # of months
    allData, gridCells = readTempData(DataFile, GridCSV)
     
    #Read in weights of each data point to each woreda or kebele
    WeightMatrix, ID = findTempWeightMatrix(AggLevel, intersectCSV, gridCells)
    Year = allData[0,2,:]
    Month = allData[0,3,:]

    #Calculate area-weighted average temperature data in each woreda or kebele
    Temp = np.dot(np.transpose(WeightMatrix),allData[:,4,:])

    #Write the data to 'WoredaTempDBF.csv' or 'KebeleTempDBF.csv'
    writeFiles(AggLevel, Temp, ID, Year, Month) 

    return None
    
def writeFiles(AggLevel, Temp, ID, Year, Month):
    if AggLevel == 'Kebele':
        f = open('KebeleTempDBF.csv','w')
        f.write('AggLevel,RK_CODE,Year,Month,Temp\n')
    elif AggLevel == 'Woreda':
        f = open('WoredaTempDBF.csv','w')
        f.write('AggLevel,WID,Year,Month,Temp\n')
    
    for i in range(np.shape(Temp)[0]):
        for j in range(np.shape(Temp)[1]):
            if AggLevel == 'Woreda':
                f.write('W,'+ str(ID[i]) + ',' + str(int(Year[j])) + ',' + str(int(Month[j])) + ',')
            elif AggLevel == 'Kebele':
                f.write('K,'+ str(ID[i]) + ',' + str(int(Year[j])) + ',' + str(int(Month[j])) + ',')
            f.write(str(Temp[i,j]))
            f.write('\n')
        
    f.close()
        
    return None
