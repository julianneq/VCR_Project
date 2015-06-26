This directory contains all the code for simulating maize yields under different fertilizer scenarios.

Simulate them by calling simulateMaizeYields(model, numYears, FertScenario)

model = 1, 2, or 3 and corresponds to MaizeModel1.txt, MaizeModel2.txt and MaizeModel3.txt
numYears is the number of simulated years
FertScenario is a vector of fertilizer application scenarios, where each element is an application amount in kg/ha
You do not need to include 0 kg/ha in the FertScenario vector, as this will be modeled automatically as a base case.

simulateMaizeYields.py calls readInData.py to read in the necessary data, which include the soil parameters, weather generating
parameters and Harvest Choice AEZs by woreda. It also reads in the statistical crop yield model parameters.

The weather parameters were determined separately and written to a csv so that they did not need to be re-calculated each
time simulateMaizeYields.py is called. Instead, they are just read in. The weather parameters were calculated from the function
findWeatherParams.py, which fits a bivariate normal distribution to the natural log of total seasonal precipitation and
the mean seasonal temperature in each woreda.
