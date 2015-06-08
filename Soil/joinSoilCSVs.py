import os
import csv
import numpy as np

def joinSoilCSVs(AggLevel, workingDir):
    '''Joins all of the CSVs with the average AggLevel soil data across all soil characteristics and layers'''

    #Change the working directory to the directory with all the soil data folders
    os.chdir(workingDir)
    directories = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f) == False]
    if AggLevel == 'Woreda':
        headers = ['WID']
    else:
        headers = ['KebeleID']
    
    for i in range(len(directories)):
        #Find all the CSVs with the soil data in each soil characteristic folder
        os.chdir(workingDir +"\\" + directories[i])
        filelist = os.listdir(os.getcwd())
        CSVs = []
        for j in range(len(filelist)):
            name = filelist[j]
            if name[-10::] == AggLevel + '.csv':
                CSVs.append(name)

        for j in range(len(CSVs)):
            #determine the soil characteristic and soil layer to use as a header field
            if CSVs[j][-18:-16] == 'sd' or CSVs[j][-18:-16] == 'xd':
                layer = CSVs[j][-18:-15]
            else:
                layer = ''
            indices = []

            for k in range(len(CSVs[j])):
                if CSVs[j][k] == '_':
                    indices.append(k)

            headers.append(CSVs[j][(indices[0]+1):indices[1]]+layer)

            #open the CSV and read in the mean soil data
            reader = csv.reader(open(CSVs[j],'rb'),delimiter = ",")
            x = list(reader)
            data = np.array(x)
            row = -1
            if i == 0 and j == 0:
                WIDs = []
                for k in range(len(data[1:,1])):
                    if data[k+1,1] != ' ':
                        WIDs.append(data[k+1,1])
                    else:
                        row = k+1
                joinedTable = np.zeros([len(WIDs),1])
                joinedTable[:,0] = WIDs

            joinedTable = np.concatenate((joinedTable,np.zeros([len(WIDs),1])),1)
            for k in range(len(data[0,:])):
                if data[0,k] == 'MEAN':
                    col = k

            #add the mean soil data to joinedTable, which stores the mean soil data for every layer and soil characteristic
            if row != -1:
                for k in range(len(WIDs)+1):
                    if k < row:
                        joinedTable[k,-1] = data[k+1,col]
                    elif k > row:
                        joinedTable[k-1,-1] = data[k+1,col]
            else:
                for k in range(len(WIDs)):
                    joinedTable[k,-1] = data[k+1,col]

    #change the directory to where the soil data csv will be stored
    os.chdir(workingDir)

    #write the soil data csv
    f = open(AggLevel + "SoilData.csv",'w')
    for i in range(len(headers)):
        if i != (len(headers)-1):
            f.write(headers[i] + ',')
        else:
            f.write(headers[i] + '\n')
                           
    for i in range(np.shape(joinedTable)[0]):
        for j in range(np.shape(joinedTable)[1]):
            if j != (np.shape(joinedTable)[1]-1):
                f.write(str(joinedTable[i,j]) + ',')
            else:
                f.write(str(joinedTable[i,j]) + '\n')

    f.close()

    return joinedTable
