import csv
import arcpy as ap

def convertDBFtoCSV(dbf):
    '''Converts database file to a csv'''
    table = dbf
    outfile = dbf[0:-4] + ".csv"

    fields = ap.ListFields(table)
    field_names = [field.name for field in fields]
    with open(outfile,'wb') as f:
        dw = csv.DictWriter(f,field_names)
        dw.writeheader()

        with ap.da.SearchCursor(table,field_names) as cursor:
            for row in cursor:
                dw.writerow(dict(zip(field_names,row)))

    return None
