import ftplib
import datetime
import os
import gzip

def downloadRainData():
    '''Downloads 0.5 degree monthly temperature data from ftp://ftp.cdc.noaa.gov/Datasets/ghcncams/ \n
    and processes them at AggLevel = "Woreda" or "Kebele"'''

    #open a log file and write the current date to it
    workingDir = os.getcwd()
    fdLog = file(workingDir + "\\" + 'NOAAupdate.log','a')
    fdLog.write(str(datetime.datetime.today()) + '\n')
    fdLog.flush()

    #connect to the GHCN FTP server and go to data directory
    ftp = ftplib.FTP('ftp.cpc.ncep.noaa.gov')
    ftp.login('','')
    ftp.cwd('fews/fewsdata/africa/rfe2/bin/')

    #download the temperature netCDF file
    directoryList = []
    ftp.retrlines('LIST', directoryList.append)
    rainFiles = []
    for fileEntry in directoryList:
        if fileEntry.find(".gz") > -1:
            rainFiles.append(fileEntry)

    for i in range(len(rainFiles)):
        parts = rainFiles[i].split()
        newFile = workingDir + "\\" + parts[8][0:12] + parts[8][16:25]
        if (os.path.exists(newFile)) == False:
            #Download the binary file if it hasn't yet been downloaded
            ftp.retrbinary('RETR ' + parts[8], file(workingDir + "\\" + parts[8], 'wb').write)
            fdLog.write('downloaded ' + parts[8] + '\n')

            #uncompress the file and delete the zipped file
            inF = gzip.open(workingDir + "\\" + parts[8], 'rb')
            outF = open(workingDir + "\\" + parts[8][:-3],'wb')
            outF.write(inF.read())
            inF.close()
            outF.close()
            os.remove(str(workingDir + "\\" + parts[8]))

    ftp.close()

    return None
