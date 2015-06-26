This directory contains all the code for simulating maize yields under different fertilizer scenarios. Simulate them by calling simulateMaizeYields(model, numYears, FertScenario).

model = 1, 2, or 3 and corresponds to MaizeModel1.txt, MaizeModel2.txt and MaizeModel3.txt;
numYears is the number of simulated years;
and FertScenario is a vector of fertilizer application scenarios, where each element is an application amount in kg/ha.
You do not need to include 0 kg/ha in the FertScenario vector, as this will be modeled automatically as a base case.

Model results are written to simulated0kgYields.csv, simulated*kgYields.csv where "*" corresponds to the amounts in FertScenario, simulatedRain.csv, and simulatedTemp.csv. Simulated yields are point estimates from the statistical crop model.
Errors by woreda were subsequently added to these simulated yields.

simulateMaizeYields.py calls readInData.py to read in the necessary data, which include:
the soil parameters (from WoredaSoilData.csv), 
weather generating parameters (from WeatherParams.csv)
and Harvest Choice AEZs by woreda (from WoredaAEZ8.csv).
It also reads in the statistical crop yield model parameters from MaizeModel1.txt, MaizeModel2.txt or MaizeModel3.txt.

The weather parameters were determined separately and written to WeatherParams.csv so that they do not need to be re-calculated each time simulateMaizeYields.py is called; instead, they are just read in from WeatherParams.csv.
The weather parameters were calculated from the function findWeatherParams.py, which fits a bivariate normal distribution to the natural log of total seasonal precipitation and the mean seasonal temperature in each woreda.

The woreda-level rainfall data is read in from WoredaRainDBF.csv; 
the woreda-level temperature is read in from WoredaTempDBF.csv,
and the maize growing seasons for each woreda are determined by the FAO AEZ, given in FAO_AEZworeda.csv.
