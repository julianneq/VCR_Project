import numpy as np
import csv

def findRainWeightMatrix(AggLevel, intersectCSV, gridCells):
    '''Calculates the weight of each NOAA grid cell in each woreda or kebele based on area'''

    #Read in the attribute table with the area of each intersected Rain grid cell
    #and woreda or kebele to determine weights for averaging temperature data
    reader = csv.reader(open(intersectCSV,'rb'),delimiter=',')
    x = list(reader)
    Rain_area = np.array(x)
    ID = []
    rowID = []

    #determine which columns of the file contain the row and column in which the data is stored in the netCDF file
    #and the ID of the woreda or kebele
    rowCol = 7
    if AggLevel == 'Woreda':
        IDcol = 13
    elif AggLevel == 'Kebele':
        IDcol = 26

    #Read in row IDs and woreda or kebele IDs
    for i in range(np.shape(Rain_area)[0]-1):
        rowID.append(Rain_area[i+1,rowCol])
        ID.append(Rain_area[i+1,IDcol])

    #Determine all unique woreda or kebele IDs
    allIDs = np.unique(ID[::-1])
    allIDs = list(allIDs)

    #Build a matrix, WeightMatrix, to store the weights (by area) of each grid cell in each woreda or kebele;
    #Each row is a different Temp grid cell and each column is a different woreda or kebele
    WeightMatrix = np.zeros([len(gridCells),len(allIDs)])
    if AggLevel == 'Woreda':
        areaCol = 20
    elif AggLevel == 'Kebele':
        areaCol = 29
    for i in range(np.shape(Rain_area)[0]-1):
        for j in range(len(gridCells)):
            if int(rowID[i]) == gridCells[j]:
                row = j
                col = allIDs.index(ID[i])
                WeightMatrix[row,col] = float(Rain_area[i+1,areaCol])

    AreaSums = np.sum(WeightMatrix,0)
    for j in range(np.shape(WeightMatrix)[0]):
        for i in range(np.shape(WeightMatrix)[1]):
            if AreaSums[i] > 0:
                WeightMatrix[j,i] = WeightMatrix[j,i]/AreaSums[i]
            else:
                WeightMatrix[j,i] = 0

    #Write WeightMatrix to a file
    f = open('Rain' + AggLevel + 'WeightMatrix.csv','w')
    f.write(',')
    for i in range(np.shape(WeightMatrix)[1]):
        f.write(str(allIDs[i])+',')

    f.write('\n')
    for i in range(np.shape(WeightMatrix)[0]):
        f.write(str(gridCells[i]) + ',')
        for j in range(np.shape(WeightMatrix)[1]):
            f.write(str(WeightMatrix[i,j]) + ',' )
        f.write('\n')
        
    f.close()
        
    return WeightMatrix
