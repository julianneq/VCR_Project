#Temp

This directory contains all of the codes used to process the NOAA monthly temperature data at the woreda or kebele level. 
The user only needs to call makeTempDBF.py with one argument: AggLevel = "Woreda" or AggLevel = "Kebele".

makeTempDBF.py will call downloadTempData.py to download the data. Next, it will call intersectGrid.py to determine the 
percentage of each woreda's or kebele's area occupied by each NOAA grid cell. Then it calls readTempData.py to read in all of
the data from the points in Ethiopia and store them in the matrix allData. makeTempDBF.py then calls findTempWeightMatrix.py to
determine the weights of each grid cell to apply to each woreda or kebele when calculating area-weighted average precipitation,
and stores them in WeightMatrix. Finally, it finds the dot product of allData and WeightMatrix to determine these area-weighted
averages.
