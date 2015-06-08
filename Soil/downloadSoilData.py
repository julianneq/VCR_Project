import ftplib
import datetime
import gzip
import os

def downloadSoilData(AggLevel, workingDir):
	'''Downloads all 250m AfSIS soil data from http://www.isric.org/content/african-soilgrids-250m-geotiffs \n
	and processes them at AggLevel = "Woreda" or "Kebele"'''

	#open a log file and write the current date to it
	fdLog = file(workingDir + '\\AfSISupdate.log','a')
	fdLog.write(str(datetime.datetime.today()) +'\n')
	fdLog.flush()

	#connect to the AfSIS FTP server and go to data directory
	ftp = ftplib.FTP('ftp.soilgrids.org')
	ftp.login('soilgrids','soilgrids')
	ftp.cwd('data/AF/recent/')

	#Get a list of files in the AfSIS data directory
	directoryList = []
	ftp.retrlines('LIST', directoryList.append)

	#Get a list of all of the tiff files for download
	tiffs = []
	for fileEntry in directoryList:
		if fileEntry.find(".tif.gz") > -1:
			tiffs.append(fileEntry)

	for i in range(len(tiffs)):
		#create a folder to store this soil characteristic, if one doesn't exist yet
		parts = tiffs[i].split()
		indices = []
		for k in range(len(parts[8])):
			if parts[8][k] == '_':
				indices.append(k)

		newDir = workingDir + "\\" + parts[8][(indices[0]+1):indices[1]] + "\\"
		if (os.path.exists(newDir)) == False:
			os.mkdir(newDir)

                #Download the tiffs
		ftp.retrbinary('RETR ' + parts[8], file(newDir + parts[8], 'wb').write)
		fdLog.write('downloaded ' + parts[8] + '\n')

		#uncompress the file
		inF = gzip.open(newDir + parts[8], 'rb')
		outF = open(newDir + parts[8][:-3],'wb')
		outF.write(inF.read())
		inF.close()
		outF.close()

	ftp.close()

	return None
