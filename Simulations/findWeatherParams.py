import numpy as np
import itertools
import pandas as pd
import csv

def findWeatherParams():
    '''Fits a bivariate normal distribution to ln(Total Seasonal Precipitation) and \
    Mean Seasonal Temperature by woreda and writes the parameters to WeatherParams.csv'''
    
    #Read in the woreda IDs
    reader = csv.reader(open('WoredaSoilData.csv','r'),delimiter=',')
    x = list(reader)
    soilMatrix = np.array(x)
    WIDs = np.zeros([np.shape(soilMatrix)[0]-1])
    for i in range(len(WIDs)):
        WIDs[i] = int(soilMatrix[i+1,0])
    
    #Read in the daily precipitation record in each woreda
    #Store in rainMatrix
    #each row is a different woreda, identified by WIDs (in the same order)
    #each column is a different date, identified by header (in the same order)
    rainMatrix, rainDates = readWeatherData('rain', WIDs)
    
    #Read in the monthly temperature record in each woreda
    #Store in tempMatrix
    #each row is a different woreda, identified by WIDs (in the same order)
    #each column is a different date, identified by header (in the same order)
    tempMatrix, tempDates = readWeatherData('temp', WIDs)

    #Read in the FAO AEZ of each woreda, along with the planting and harvesting dates
    #Store in FAO_AEZ7_matrix
    #1st row is the header
    #1st column is woreda ID, 2nd is the corresponding AEZ7, 
    #3rd and 4th are the 1st and last months of the growing period (for weather)
    #5th and 6th are the 1st and last months of the harvest period (for prices)
    reader = csv.reader(open('FAO_AEZworeda.csv','r'),delimiter = ',')
    x = list(reader)
    FAO_AEZ7_matrix = np.array(x)
    
    #Find statistical parameters for weather generation and store them in matrix WeatherParams
    #each row is a different woreda
    #1st column is mean(ln(totalSeasonalPrecip)), 2nd column is std(ln(totalSeasonalPrecip))
    #3rd column is mean(averageSeasonalTemp), 4th column is std(averageSeasonalTemp)
    #5th and last column is correl(ln(totalSeasonalPrecip),averageSeasonalTemp)   
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
            months = np.arange(int(FAO_AEZ7_matrix[j+1][2]),int(FAO_AEZ7_matrix[j+1][3]),1)
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
        
    writeWeatherParams(ParamMatrix,WIDs) 
        
    return None
    
def readWeatherData(variable, WIDs):
    if variable == 'rain':
        reader = csv.reader(open('WoredaRainDBF.csv','r'),delimiter=',')
    else:
        reader = csv.reader(open('WoredaTempDBF.csv','r'),delimiter=',')
    
    x = list(reader)
    allDates = []
    for i in range(np.shape(x)[0]-1):
        year = int(x[i+1][2])
        month = int(x[i+1][3])
        if variable == 'rain':
            day = int(x[i+1][4])
            allDates.append(pd.datetime(year, month, day))
        else:
            allDates.append(pd.datetime(year, month,1))
        
    uniqueDates = list(np.unique(allDates))
    yrs = np.arange(2001,2015)
    seasonalDates = []
    for i in range(len(yrs)):
        if variable == 'rain':
            seasonalDates.append(pd.date_range(pd.datetime(yrs[i],4,1),pd.datetime(yrs[i],9,30)))
        else:
            for j in np.arange(4,10):
                seasonalDates.append(pd.datetime(yrs[i],j,1))
        
    if variable == 'rain':
        seasonalDates = list(itertools.chain(*seasonalDates))
        
    keepRows = [uniqueDates.index(z) if z in uniqueDates else None for z in seasonalDates]
    if variable == 'rain':
        del keepRows[keepRows.index(None)]

    for j in range(len(keepRows)):
        keepRows[j] = keepRows[j] + 1
        
    weatherMatrix = np.zeros([len(keepRows),len(WIDs)])
    for i in range(len(WIDs)):
        for j in range(len(keepRows)):
            weatherMatrix[j,i] = x[keepRows[j]][-1]
        for j in range(len(keepRows)):
            keepRows[j] = keepRows[j] + len(uniqueDates)
            
    return weatherMatrix, seasonalDates
    
def writeWeatherParams(WeatherParams,WIDs):
    f = open('WeatherParams.csv','w')
    f.write('WID,mu_lnP,std_lnP,mu_T,std_T,rho\n')
    for i in range(len(WIDs)):
        f.write(str(int(WIDs[i])) + ',' + str(WeatherParams[i,0]) + ',' + str(WeatherParams[i,1]) + ',' \
        + str(WeatherParams[i,2]) + ',' + str(WeatherParams[i,3]) + ',' + str(WeatherParams[i,4]) + '\n')
        
    f.close()
    
    return None
