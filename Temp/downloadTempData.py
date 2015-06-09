import ftplib
import datetime

def downloadTempData(workingDir):
    '''Downloads 0.5 degree monthly temperature data from ftp://ftp.cdc.noaa.gov/Datasets/ghcncams/ \n
    and processes them at AggLevel = "Woreda" or "Kebele"'''

    #open a log file and write the current date to it
    fdLog = file(workingDir + '\\TempUpdate.log','a')
    fdLog.write(str(datetime.datetime.today()) + '\n')
    fdLog.flush()

    #connect to the GHCN FTP server and go to data directory
    ftp = ftplib.FTP('ftp.cdc.noaa.gov')
    ftp.login('','')
    ftp.cwd('Datasets/ghcncams/')

    #download the temperature netCDF file
    directoryList = []
    ftp.retrlines('LIST', directoryList.append)
    for fileEntry in directoryList:
        if fileEntry.find(".nc") > -1:
            TempFile = fileEntry

    parts = TempFile.split()
    DataFile = workingDir + "\\" + parts[8]
    ftp.retrbinary('RETR ' + parts[8], file(DataFile, 'wb').write)
    fdLog.write('downloaded ' + parts[8] + '\n')

    return DataFile
