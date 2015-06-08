#Soil

This directory contains all of the codes used to process the AfSIS soil data at the woreda or kebele level. The user only needs
to call process.SoilData.py with one argument: AggLevel = "Woreda" or AggLevel = "Kebele".

processSoilData.py will call downloadSoilData.py to download the data. It will then calculate woreda or kebele level average
soil characteristics using ZonalStatisticsAsTable and store them in database files (.dbf). It will then call convertDBFtoCSV.py
to convert these to csv's, and lastly call joinSoilCSVs.py to combine all of the csv's for different soil characteristics into 
one file.
