import numpy as np
import csv

def findTempWeightMatrix(AggLevel, intersectCSV, gridCells):
    '''Finds the weights of each GHCN grid cell in each AggLevel = "Woreda" or "Kebele"'''

    #Read in the attribute table with the area of each intersected Temp grid cell
    #and woreda or kebele to determine weights for averaging temperature data
    reader = csv.reader(open(intersectCSV),delimiter=',')
    x = list(reader)
    Temp_area = np.array(x)
    ID = []
    cellID = []
    
    #determine which columns of the file contain the row and column in which the data is stored in the netCDF file
    #and the ID of the woreda or kebele
    rowCol = 7
    colCol = 8
    if AggLevel == 'Woreda':
        IDcol = 14
    elif AggLevel == 'Kebele':
        IDcol = 27
        
    #concatenate row and column strings to find unique gridCell identifier
    for i in range(np.shape(Temp_area)[0]-1):
        if len(Temp_area[i+1,rowCol]) == 1:
            row = '00' + Temp_area[i+1,rowCol]
        elif len(Temp_area[i+1,rowCol]) == 2:
            row = '0' + Temp_area[i+1,rowCol]
        else:
            row = Temp_area[i+1,rowCol]
        if len(Temp_area[i+1,colCol]) == 1:
            col = '00' + Temp_area[i+1,colCol]
        elif len(Temp_area[i+1,colCol]) == 2:
            col = '0' + Temp_area[i+1,colCol]
        else:
            col = Temp_area[i+1,colCol]
        cellID.append(row+col)
        ID.append(Temp_area[i+1,IDcol])
        
    #Determine all unique grid cell locations
    allCellIDs = np.unique(cellID[::-1])
    allCellIDs = list(allCellIDs)

    #Determine all unique woreda or kebele IDs
    allIDs = np.unique(ID[::-1])
    allIDs = list(allIDs)

    #Build a matrix, WeightMatrix, to store the weights (by area) of each grid cell in each woreda or kebele;
    #Each row is a different Temp grid cell and each column is a different woreda or kebele
    WeightMatrix = np.zeros([len(allCellIDs),len(allIDs)])
    if AggLevel == 'Woreda':
        areaCol = 21
    elif AggLevel == 'Kebele':
        areaCol = 30
    for i in range(np.shape(Temp_area)[0]-1):
        for j in range(len(gridCells)):
            if cellID[i] == gridCells[j]:
                row = j
                col = allIDs.index(ID[i])
                WeightMatrix[row,col] = float(Temp_area[i+1,areaCol])
        
    AreaSums = np.sum(WeightMatrix,0)
    for j in range(np.shape(WeightMatrix)[0]):
        for i in range(np.shape(WeightMatrix)[1]):
            if AreaSums[i] > 0:
                WeightMatrix[j,i] = WeightMatrix[j,i]/AreaSums[i]
            else:
                WeightMatrix[j,i] = 0

    #Write WeightMatrix to a file
    f = open('Temp' + AggLevel + 'WeightMatrix.txt','w')
    f.write(',')
    for i in range(np.shape(WeightMatrix)[1]):
        f.write(str(allIDs[i])+',')

    f.write('\n')
    for i in range(np.shape(WeightMatrix)[0]):
        f.write(gridCells[i] + ',')
        for j in range(np.shape(WeightMatrix)[1]):
            f.write(str(WeightMatrix[i,j]) + ',' )
        f.write('\n')
        
    f.close()
        
    return WeightMatrix, allIDs
