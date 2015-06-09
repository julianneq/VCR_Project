      PROGRAM convert_rfe_bin2asc

c cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c  Program: convert_rfe2.f
c
c  Description: This program reads in a daily RFE (rainfall estimate) file
c              (version 2) in .bin format and creates an ascii integer
c              file.  Each file contains rfe coordinate data ordered by rows.
c              Rainfall resolution is 0.1 degree with a domain of
c              20W-55E, 40S-40N.
c
c  Inputs: 'input_file' = the binary precip file to be converted
c
c  Output: 'output.txt' = the output ascii converted text file
c
c  Modified: July, 2010 by Nick Novella (nicholas.novella@noaa.gov)
c
c cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      REAL*4 rfe(751,801),arr(3,601551)
      real*4 lat,lon
      INTEGER:: i,j,ind
      character*48:: input_file
      character*48:: output_file

c #####  CHANGE FILE NAME BELOW TO INPUT FILE  #####

      CALL getarg(1,input_file)
      CALL getarg(2,output_file)

c ##################################################

c #####  Initialize the arrays  #####
      do i = 1,751 
      do j = 1,801 
        rfe (i,j) = -999
      end do
      end do

c #####  Read in the input rainfall data  #####
      open (unit=22,file=input_file,access="direct",
     1	convert='big_endian',status="old",recl=751*801*4)
      read  (22, rec=1) rfe 

c #####  Open the output file  #####
      open (88,file=output_file,access='sequential',
     1	status='unknown',form='formatted')

c #####  The next code converts the input rainfall data. Each row is then written
c        to the output file.

      ind=1 
      lat= -40.0
      lon= -20.0  
      do j=1,801
      do i=1,751
          arr(1,ind)=lat
          arr(2,ind)=lon
          arr(3,ind)=rfe(i,j)

      write (88,499) arr(1,ind), arr(2,ind), arr(3,ind)
 499	format(1X,f6.2,1X,f6.2,1X,f8.2)

      ind=ind+1
      lon=lon+0.1
      end do
          lat=lat+0.1
          lon=-20.0
      end do





      END PROGRAM
