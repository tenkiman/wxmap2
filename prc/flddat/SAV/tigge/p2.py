from ecmwf import ECMWFDataServer

server = ECMWFDataServer(
       'http://tigge-portal.ecmwf.int/d/dataserver/',
       'd907f75cd718ed40eff12e8bdd115f8b',
       'michael.fiorino@noaa.gov'
    )

server.retrieve({
    'dataset' : "tigge",
    'step'    : "24/to/120/by/24",
    'number'  : "all",
    'levtype' : "sl",
    'date'    : "20071001/to/20071003",
    'time'    : "00/12",
    'origin'  : "all",
    'type'    : "pf",
    'param'   : "tp",
    'area'    : "70/-130/30/-60",
    'grid'    : "2/2",
    'target'  : "data.grib"
    })

