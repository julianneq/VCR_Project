import numpy as np
import csv
import os

def readRainData(workingDir, GridCSV):
    '''Reads in all of the daily rain data from the Ethiopia grid cells and stores it in the matrix allData'''
    
    #make a list of all of the precipitation data files
    filelist = os.listdir(workingDir)
    data = []
    for i in range(len(filelist)):
        if filelist[i][0:12] == 'all_products':
            data.append(filelist[i])

    #determine which rows of the precipitation data files need to be read in
    Grid = csv.reader(open(GridCSV), delimiter = ",")
    Grid = np.array(list(Grid))
    rowString = Grid[1::,6]
    numGridPts = len(rowString)
    row = []
    for i in range(len(rowString)):
        row.append(int(rowString[i]))
    
    #create matrix 'allData' to store all of the data
    #dimensions are a x b x c where a = # of gridcells, b = 6 (lat, long, ppt, yr, mo, day),
    #and c = # of days
    allData = np.zeros([numGridPts,6,len(data)])
    for i in range(len(data)):
        f = open(data[i],'r')
        y = []
        for line in f.readlines():
            value = [value for value in line.split()]
            y.append(value)
            
        f.close()
        for j in range(np.shape(y)[0]):
            #replace no-data values with a string that can be converted to a floating point number
            if y[j][2] == '********':
                y[j][2] = '-99.99'
        dailyGridData = np.array(y).astype('float')
        #only include the rows corresponding to points in Ethiopia
        dailyData = dailyGridData[row,:]
        dailyData = np.concatenate((dailyData,np.tile(int(data[i+1][17:21]),[np.shape(dailyData)[0],1])),axis=1)
        dailyData = np.concatenate((dailyData,np.tile(int(data[i+1][21:23]),[np.shape(dailyData)[0],1])),axis=1)
        dailyData = np.concatenate((dailyData,np.tile(int(data[i+1][23:25]),[np.shape(dailyData)[0],1])),axis=1)
        allData[:,:,i] = dailyData
        
    return allData, row
