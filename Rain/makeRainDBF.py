import os
import sys
import numpy as np
from intersectGrid import intersectGrid
from readRainData import readRainData
from findRainWeightMatrix import findRainWeightMatrix

first_arg = sys.argv[1]

def makeRainDBF(AggLevel=first_arg):
    '''Makes a .csv database file with average daily rainfall at AggLevel = "Woreda" or "Kebele"'''
    
    #Set the working directory
    workingDir = os.getcwd()

    #Intersect the NOAA grid with the Woreda or Kebele shapefile and convert the .dbf to a .csv
    intersectCSV, GridCSV = intersectGrid(AggLevel, workingDir, "Rain")

    #Read in raw monthly temperature data at every GHCN grid cell and store it in the matrix 'allData'
    #dimensions are a x b x c where a = # of gridcells, b = 5 (lat, long, yr, mo, temp), 
    #and c = # of months
    allData, gridCells = readRainData(workingDir,GridCSV)
    
    #Calculate and read in weights of each data point to each woreda or kebele
    WeightMatrix, ID = findRainWeightMatrix(AggLevel, intersectCSV, gridCells)
    Year = allData[0,3,:]
    Month = allData[0,4,:]
    Day = allData[0,5,:]

    #Calculate area-averaged rainfall data in each woreda or kebele
    Rain = np.dot(np.transpose(WeightMatrix),allData[:,2,:])

    #Write the data to WoredaRainDBF.csv or KebeleRainDBF.csv
    writeFiles(AggLevel, Rain, ID, Year, Month, Day) 

    return None
    
def writeFiles(AggLevel, Rain, ID, Year, Month, Day):
    if AggLevel == 'Kebele':
        f = open('KebeleRainDBF.csv','w')
    elif AggLevel == 'Woreda':
        f = open('WoredaRainDBF.csv','w')

    f.write('AggLevel,ID,Year,Month,Day,Precip\n')
    for i in range(np.shape(Rain)[0]):
        for j in range(np.shape(Rain)[1]):
            if AggLevel == 'Kebele':
                f.write('K,'+ ID[i] + ',' + str(int(Year[j])) + ',' + str(int(Month[j])) + ',' + str(int(Day[j])) + ',')
            elif AggLevel == 'Woreda':
                f.write('W,'+ ID[i] + ',' + str(int(Year[j])) + ',' + str(int(Month[j])) + ',' + str(int(Day[j])) + ',')
            f.write(str(Rain[i,j]))
            f.write('\n')
        
    f.close()
        
    return None

if __name__ == "__main__":
    makeRainDBF()
