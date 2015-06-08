# VCRproject
This repository contains all of the codes used to process the soil, weather and agroecological zone data used to develop 
a fertilizer profitability tool for Ethiopia.

The codes used to process the soil data are located in the "Soil" subdirectory. The soil data are 250 m resolution data from
AfSIS: http://www.isric.org/content/african-soilgrids-250m-geotiffs

The codes used to process the precipitation data are located in the "Rain" subdirectory. These are daily rainfall estimates from
satellites provided by NOAA at 0.1 degree resolution: ftp://ftp.cpc.ncep.noaa.gov/fews/fewsdata/africa/rfe2. More details on how
these data were processed can be found in the README.md within the "Rain" subdirectory.

The codes used to process the temperature data are located in the "Temp" subdirectory. These are monthly temperature estimates
from satellites provided by NOAA at 0.5 degree resolution: ftp://ftp.cdc.noaa.gov/Datasets/ghcncams/. More details on how these
data were processed can be found in the README.md within the "Temp" subdirectory.

The codes used to process the agroecological zone data are located in the "AEZ" subdirectory. These came from the Atlas of the
Ethiopian Rural Economy (https://books.google.cl/books?id=z6D2d0sBUqwC&lpg=PT7&ots=TkDqmbHta_&dq=Atlas%20of%20the%20Ethiopian%20Rural%20Economy&pg=PP1#v=onepage&q=Atlas%20of%20the%20Ethiopian%20Rural%20Economy&f=false) and were given to us by IFPRI. More details on how these data were processed can be found in the
README.md within the "AEZ" subdirectory.

The woreda and kebele shapefiles are located in the "Shapefiles" subdirectory. These were found from ArcGIS online.
