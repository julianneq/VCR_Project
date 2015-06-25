import numpy as np
import pandas as pd
import csv
#from findWeatherParams import findWeatherParams
import itertools

def readInData(model):
    #Read in the soil data  in each woreda
    #Store in soilMatrix
    #1st row is the header, 1st column is the woreda IDs
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
    #rainMatrix, rainDates = readWeatherData('rain', WIDs)
    
    #Read in the monthly temperature record in each woreda
    #Store in tempMatrix
    #each row is a different woreda, identified by WIDs (in the same order)
    #each column is a different date, identified by header (in the same order)
    #tempMatrix, tempDates = readWeatherData('temp', WIDs)

    #Read in the FAO AEZ of each woreda, along with the planting and harvesting dates
    #Store in FAO_AEZ7_matrix
    #1st row is the header
    #1st column is woreda ID, 2nd is the corresponding AEZ7, 
    #3rd and 4th are the 1st and last months of the growing period (for weather)
    #5th and 6th are the 1st and last months of the harvest period (for prices)
    #reader = csv.reader(open('FAO_AEZworeda.csv','r'),delimiter = ',')
    #x = list(reader)
    #FAO_AEZ7_matrix = np.array(x)
    
    #Find statistical parameters for weather generation and store them in matrix WeatherParams
    #each row is a different woreda
    #1st column is mean(ln(totalSeasonalPrecip)), 2nd column is std(ln(totalSeasonalPrecip))
    #3rd column is mean(averageSeasonalTemp), 4th column is std(averageSeasonalTemp)
    #5th and last column is correl(ln(totalSeasonalPrecip),averageSeasonalTemp)
    #WeatherParams = findWeatherParams(FAO_AEZ7_matrix, rainMatrix, tempMatrix, rainDates, tempDates)
    #writeWeatherParams(WeatherParams,WIDs)    
    reader = csv.reader(open('WeatherParams.csv','r'),delimiter=',')
    x = list(reader)
    weatherMatrix = np.array(x)
    WeatherParams = np.zeros([len(WIDs),5])
    for i in range(len(WIDs)):
        WeatherParams[i,0] = weatherMatrix[i+1][1]
        WeatherParams[i,1] = weatherMatrix[i+1][2]
        WeatherParams[i,2] = weatherMatrix[i+1][3]
        WeatherParams[i,3] = weatherMatrix[i+1][4]
        WeatherParams[i,4] = weatherMatrix[i+1][5]

    #Read in the Harvest Choice AEZ8 classification of each woreda
    #Store in HC_AEZ8_matrix
    #first column is woreda ID, second column is corresponding AEZ8 string,
    #third column corresponding AEZ8 numerical code
    reader = csv.reader(open('WoredaAEZ8.csv','r'),delimiter = ',')
    x = list(reader)
    HC_AEZ8_matrix = np.array(x)
    
    #Read in price data for each woreda
    #Store in PriceMatrix
    #First row is the header
    #6th column is the month, 7th the year, 11th the price (in birr/kg) \
    #and last (12th) the Woreda ID
    #reader = csv.reader(open('MaizePrices.csv','rU'),delimiter = ',')
    #x = list(reader)
    #PriceMatrix = np.array(x)
    
    #read in statisical crop model parameters
    #store the predictor names in modelVars, and the coefficients in modelCoeffs
    if model == 1:
        reader = csv.reader(open('MaizeModel.txt','r'),delimiter=',')
    elif model == 2:
        reader = csv.reader(open('MaizeModel2.txt','r'),delimiter=',')
    elif model == 3:
        reader = csv.reader(open('MaizeModel3.txt','r'),delimiter=',')
    
    x = list(reader)    
    modelVars = []
    modelCoeffs = np.zeros(np.shape(x)[0]-1)
    for i in range(np.shape(x)[0]-1):
        modelVars.append(x[i+1][0])
        modelCoeffs[i] = x[i+1][1]
        
    simMatrix = np.zeros([len(WIDs),len(modelCoeffs)])
    for i in range(np.shape(simMatrix)[0]):
        if model == 1:
            simMatrix[i,4] = soilMatrix[i+1,29] #percent clay in each woreda
            simMatrix[i,5] = soilMatrix[i+1,37] #percent silt in each woreda
            simMatrix[i,6] = soilMatrix[i+1,91] #SOC in layer 1 in each woreda
        elif model == 2:
            if int(HC_AEZ8_matrix[i+1][2]) == 2:
                simMatrix[i,0] = 1 #AEZ2 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 3:
                simMatrix[i,1] = 1 #AEZ3 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 4:
                simMatrix[i,2] = 1 #AEZ4 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 5:
                simMatrix[i,3] = 1 #AEZ5 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 11:
                simMatrix[i,4] = 1 #AEZ11 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 12:
                simMatrix[i,5] = 1 #AEZ12 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 13:
                simMatrix[i,6] = 1 #AEZ13 dummy
            simMatrix[i,11] = soilMatrix[i+1,29] #percent clay in each woreda
            simMatrix[i,12] = soilMatrix[i+1,37] #percent silt in each woreda
            simMatrix[i,13] = soilMatrix[i+1,91] #SOC in layer 1 in each woreda
            simMatrix[i,21] = soilMatrix[i+1,86] #Al content in layer 1 in each woreda
        elif model == 3:
            if int(HC_AEZ8_matrix[i+1][2]) == 3:
                simMatrix[i,0] = 1 #AEZ3 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 4:
                simMatrix[i,1] = 1 #AEZ4 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 5:
                simMatrix[i,2] = 1 #AEZ5 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 11:
                simMatrix[i,3] = 1 #AEZ11 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 12:
                simMatrix[i,4] = 1 #AEZ12 dummy
            elif int(HC_AEZ8_matrix[i+1][2]) == 13:
                simMatrix[i,5] = 1 #AEZ13 dummy
            simMatrix[i,10] = soilMatrix[i+1,29] #percent clay in each woreda
            simMatrix[i,11] = soilMatrix[i+1,37] #percent silt in each woreda
            simMatrix[i,12] = soilMatrix[i+1,91] #SOC in layer 1 in each woreda
            simMatrix[i,20] = soilMatrix[i+1,86] #Al content in layer 1 in each woreda
            simMatrix[i,21] = soilMatrix[i+1,-2] #Acidity in layer 1 in each woreda
        
    return modelCoeffs, simMatrix, WeatherParams, WIDs#, PricePars
    
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
