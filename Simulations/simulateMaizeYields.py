import numpy as np
from readInData import readInData
import os

def simulateMaizeYields(model, numYears, FertScenario):
    '''Simulates numYears of maize yields under 0 kg fertilizer /ha and FertScenario; \
    model = 1, 2 or 3; numYears is the number of simulated years; and \
    FertScenario is a vector of modeled fertilizer application rates in kg/ha'''
    
    #Find the statistical model coefficients, matrix of predictor values
    #and statistical parameters for generating weather  
    #weather distribution is modeled as bivariate normal with mean seasonal temp
    #and log(total seasonal precip)
    modelCoeffs, simMatrix, WeatherParams, WIDs = readInData(model)
    
    #generate random weather and store in weatherRVs, an a x b x c matrix
    #where a = # of woredas, b = 2 (precip and temp), and c = numYears
    weatherRVs = np.zeros([np.shape(WeatherParams)[0],2,numYears])
    cov = np.zeros([2,2])
    for i in range(np.shape(WeatherParams)[0]):
        cov[0,0] = WeatherParams[i,1]**2
        cov[1,1] = WeatherParams[i,3]**2
        cov[0,1] = WeatherParams[i,4]*WeatherParams[i,1]*WeatherParams[i,3]
        cov[1,0] = cov[0,1]
        weatherRVs[i,:,:] = np.transpose(np.random.multivariate_normal([WeatherParams[i,0],WeatherParams[i,2]],\
        cov,numYears))
        weatherRVs[i,0,:] = np.exp(weatherRVs[i,0,:])
        
    #Calculate base case yields (with no fertilizer) in each woreda under each simulated year
    baseYield = simulateYield(numYears, simMatrix, weatherRVs, modelCoeffs, model)    
    
    #write generated rainfall, temperature, and base yields to separate csv's
    woredas = np.zeros([len(WIDs),1])
    for i in range(len(WIDs)):
        woredas[i,0] = WIDs[i]
        
    WIDs = woredas
    rainMatrix = weatherRVs[:,0,:]
    tempMatrix = weatherRVs[:,1,:]
    rainMatrix = np.concatenate((WIDs,rainMatrix),1)
    tempMatrix = np.concatenate((WIDs,tempMatrix),1)
    baseYield = np.concatenate((WIDs,baseYield),1)
    
    newDir = os.getcwd() + "\\Model" + str(model) + "\\"     
    writeCSVs(rainMatrix,newDir + 'simulatedRain.csv')
    writeCSVs(tempMatrix,newDir + 'simulateTemp.csv')
    writeCSVs(baseYield,newDir + 'simulated0kgYields.csv')
    
    #Calculate yields under FertScenarios
    for j in range(len(FertScenario)):
        for i in range(np.shape(simMatrix)[0]):
            if model == 1:
                simMatrix[i,9] = FertScenario[j] #ChemFert
                simMatrix[i,10] = FertScenario[j]**2 #ChemFert^2
            elif model == 2:
                simMatrix[i,16] = FertScenario[j] #ChemFert
                simMatrix[i,20] = FertScenario[j]*simMatrix[i,21] #ChemFert*Alum
            elif model == 3:
                simMatrix[i,15] = FertScenario[j] #ChemFert
                simMatrix[i,19] = FertScenario[j]*simMatrix[i,20] #ChemFert*Alum
        
        newYield = simulateYield(numYears, simMatrix, weatherRVs, modelCoeffs, model)
        newYield = np.concatenate((WIDs,newYield),1)
        writeCSVs(newYield,newDir + 'simulated'+ str(FertScenario[j]) + 'kgYields.csv')
    
    return None
        
def simulateYield(numYears, simMatrix, weatherRVs, modelCoeffs, model):
    simYield = np.zeros([np.shape(simMatrix)[0],numYears])
    for i in range(numYears):
        for j in range(np.shape(simMatrix)[0]):
            if model == 1:
                simMatrix[j,0] = weatherRVs[j,1,i] #Temp
                simMatrix[j,1] = weatherRVs[j,0,i] #Precip
                simMatrix[j,11] = simMatrix[j,9]*simMatrix[j,0] #ChemFert*Temp
                simMatrix[j,12] = simMatrix[j,11]*simMatrix[j,0] #ChemFert*Temp^2
            elif model == 2:
                simMatrix[j,7] = weatherRVs[j,1,i] #Temp
                simMatrix[j,8] = weatherRVs[j,0,i] #Precip
                simMatrix[j,17] = simMatrix[j,16]*simMatrix[j,7] #ChemFert*Temp
                simMatrix[j,18] = simMatrix[j,16]*simMatrix[j,8] #ChemFert*Precip
                simMatrix[j,19] = simMatrix[j,17]*simMatrix[j,8] #ChemFert*Temp*Precip
            elif model == 3:
                simMatrix[j,6] = weatherRVs[j,1,i] #Temp
                simMatrix[j,7] = weatherRVs[j,0,1] #Precip
                simMatrix[j,16] = simMatrix[j,15]*simMatrix[j,6] #ChemFert*Temp
                simMatrix[j,17] = simMatrix[j,15]*simMatrix[j,7] #ChemFert*Precip
                simMatrix[j,18] = simMatrix[j,17]*simMatrix[j,6] #ChemFert*Temp*Precip
                
        #simulate the yield
        simYield[:,i] = np.dot(simMatrix,modelCoeffs)
    
    #convert yield from quintal/ha to kg/ha
    simYield = simYield*100
    
    #replace all negative yields with 0
    for i in range(np.shape(simYield)[0]):
        for j in range(np.shape(simYield)[1]):
            if simYield[i,j] < 0:
                simYield[i,j] = 0
        
    return simYield
    
def writeCSVs(matrix, csvfile):
    f = open(csvfile,'w')
    f.write('WID,')
    for i in range(np.shape(matrix)[1]-2):
        f.write('Year' + str(i) + ',')
    f.write('Year' + str(np.shape(matrix)[1]-1) + '\n')
    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]-1):
            f.write(str(matrix[i,j]) + ',')
        f.write(str(matrix[i,-1]) + '\n')
        
    f.close()
    
    return None
