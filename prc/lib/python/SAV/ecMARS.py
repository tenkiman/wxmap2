import sys
import mf
import w2

class MARS():

    from ecmwf import ECMWFDataServer

## servertigge = ECMWFDataServer(
##        'http://tigge-portal.ecmwf.int/d/dataserver/',
##        'd907f75cd718ed40eff12e8bdd115f8b',
##        'michael.fiorino@noaa.gov'
##     )
## server.retrieve({
##     'dataset' : "tigge",
##     'step'    : "24/to/120/by/24",
##     'number'  : "all",
##     'levtype' : "sl",
##     'date'    : "20091001/to/20091001",
##     'time'    : "00",
##     'origin'  : "all",
##     'type'    : "fc",
##     'param'   : "tp",
##     'area'    : "70/-130/30/-60",
##     'grid'    : "2/2",
##     'target'  : "data.grib"
##     })


    yotc = ECMWFDataServer(
        'http://data-portal.ecmwf.int/data/d/dataserver/',
        'd907f75cd718ed40eff12e8bdd115f8b',
        'michael.fiorino@noaa.gov'
        )
    
class Req():
    
    plevs='200/300/500/700/850/925/1000'
    param=None
    type='an'
    tdir="%s/ecmwf/yotc"%(w2.Nwp2DataBdir)
    step='0'
    area='global'
    grid='0.5/0.5'
    levtype='pl'
    dataset='yotc_od'
    otype=None
    
    def __init__(self,dtg,type=type,step=step):

        ymd=dtg[0:8]
        hh=dtg[8:10]

        self.type=type
        self.step=step
        odir="%s/%s"%(self.tdir,dtg)
        mf.ChkDir(odir,'mk')
        
        self.req={
            'dataset'  : "%s"%(self.dataset),
            'step'     : "%s"%(self.step),
            'levtype'  : "%s"%(self.levtype),
            'date'     : "%s/to/%s"%(ymd,ymd),
            'time'     : "%s"%(hh),
            'type'     : "%s"%(self.type),
            'param'    : "%s"%(self.param),
            'levelist' : "%s"%(self.plevs),
            'area'     : "%s"%(self.area),
            'grid'     : "%s"%(self.grid),
            'expect'   : 'any',
            'target'   : "%s/%s.%s.%s.%s.grb1"%(odir,self.dataset,self.otype,self.type,dtg),
            }

class uaReq(Req):

    grid='1.0/1.0'
    uavars='u/v/t/z/r'
    param=uavars
    otype='ua'

class sfcReq(Req):

    sfcvars='10u/10v/cp/tp/msl'
    param=sfcvars
    levtype='sfc'
    plevs='0'
    otype='sfc'
    

