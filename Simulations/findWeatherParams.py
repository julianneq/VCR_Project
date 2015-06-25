import numpy as np

def findWeatherParams(AEZmatrix, rainMatrix, tempMatrix, rainDates, tempDates):
    weatherMatrix = np.zeros([np.shape(rainMatrix)[1],2,14])
    yrs = np.arange(2001,2015,1)
    
    rainYrs = []
    rainMonths = []
    for i in range(len(rainDates)):
        rainMonths.append(rainDates[i].month)
        rainYrs.append(rainDates[i].year)
        
    tempYrs = []
    tempMonths = []
    for i in range(len(tempDates)):
        tempMonths.append(tempDates[i].month)
        tempYrs.append(tempDates[i].year)

    for i in range(len(yrs)):
        rainYrRows = [item for item in range(len(rainYrs)) if rainYrs[item] == yrs[i]]
        tempYrRows = [item for item in range(len(tempYrs)) if tempYrs[item] == yrs[i]]
        for j in range(np.shape(rainMatrix)[1]):
            months = np.arange(int(AEZmatrix[j+1][2]),int(AEZmatrix[j+1][3]),1)
            rainMonthRows = [item for item in range(len(rainMonths)) if rainMonths[item] in months]
            tempMonthRows = [item for item in range(len(tempMonths)) if tempMonths[item] in months]
            rainBothRows = list(set(rainYrRows) & set(rainMonthRows))
            tempBothRows = list(set(tempYrRows) & set(tempMonthRows))
            totalRain = 0
            avgTemp = 0
            for k in range(len(rainBothRows)):
                totalRain = totalRain + rainMatrix[rainBothRows[k],j]
                
            for k in range(len(tempBothRows)):
                avgTemp = avgTemp + tempMatrix[tempBothRows[k],j]
                
            avgTemp = avgTemp/len(tempBothRows)
            if totalRain == 0:
                weatherMatrix[j,0,i] = -5
            else:
                weatherMatrix[j,0,i] = np.log(totalRain)
            weatherMatrix[j,1,i] = avgTemp
    
    ParamMatrix = np.zeros([np.shape(weatherMatrix)[0],5])
    
    for i in range(np.shape(weatherMatrix)[0]):
        ParamMatrix[i,0] = np.mean(weatherMatrix[i,0,:])
        ParamMatrix[i,1] = np.std(weatherMatrix[i,0,:])
        ParamMatrix[i,2] = np.mean(weatherMatrix[i,1,:])
        ParamMatrix[i,3] = np.std(weatherMatrix[i,1,:])
        ParamMatrix[i,4] = np.corrcoef(weatherMatrix[i,0,:],weatherMatrix[i,1,:])[0,1]
        
    return ParamMatrix
    
