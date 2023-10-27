#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

dtg='2013031200'
dtg='2012071800'

model='ecmt'
m2=setModel2(model)

m2.setDtgTdirCtl(dtg)
m2.getFieldsTigge()
m2.makeCtl()

sys.exit()


# ----------------------- old version

server = ECMWFDataServer(
       'http://tigge-portal.ecmwf.int/d/dataserver/',
       'd907f75cd718ed40eff12e8bdd115f8b',
       'michael.fiorino@noaa.gov'
    )


dtg='2012102200'

ymd=dtg[0:8]
hh=dtg[8:10]
bymd=ymd
eymd=ymd

btau=0
etau=btau
etau=12
dtau=12

mf.ChangeDir(w2.ptmpBaseDir)

sfile="sfc.%s.f%03d.grb2"%(dtg,btau)
sfile="sfc.%s.grb2"%(dtg)
sfile="sfc.grb2"
sparam='59/121/122/134/136/146/147/151/165/166/167/168/172/176/177/179/189/235/228002/228039/228139/228141/228144/228164/228228'
sparam='cape/d2m/psfc/pmsl/sdsfc/sfsfc/sktsfc/slhfsfc/sm0_20cm/sshfsfc/ssrsfc/st0_20cm/sundsfc/tmax2m/tmin2m/t2m/tcc/tpsfc/ttrsfc/ttrtoa/u10m/v10m'
sparam='msl/10u/10v'


#param=130/131/132/133/156,
#levelist=200/300/500/700/850/925/1000

server = ECMWFDataServer(
       'http://tigge-portal.ecmwf.int/d/dataserver/',
       'd907f75cd718ed40eff12e8bdd115f8b',
       'michael.fiorino@noaa.gov'
    )


request={
    'dataset' : "tigge",
    'step'    : "%d/to/%d/by/%d"%(btau,etau,dtau),
    'number'  : "all",
    'levtype' : "sl",
    'date'    : "%s"%(ymd),
    'time'    : "%s"%(hh),
    'origin'  : "all",
    'type'    : "pf",
    'area'    : "global",
    'grid'    : "1.0/1.0",
    'target'  : "%s"%(sfile)
    }

request={
    'dataset' : "tigge",
    'step'    : "%d/to/%d/by/%d"%(btau,etau,dtau),
    'number'  : "all",
    'levtype' : "sl",
    'date'    : "%s/to/%s"%(bymd,eymd),
    'time'    : "%s"%(hh),
    'origin'  : "all",
    'type'    : "fc",
    'param'   : "%s"%(sparam),
    'area'    : "80/0/-10/360",
    'grid'    : "0.15/0.15",
    'target'  : "%s"%(sfile)
    }

# -- eps
request={
    'dataset' : "tigge",
    'step'    : "%d/to/%d/by/%d"%(btau,etau,dtau),
    'number'  : "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50",
    'levtype' : "sl",
    'expver'  : "prod",
    'date'    : "%s/to/%s"%(bymd,eymd),
    'time'    : "%s"%(hh),
    'origin'  : "ecmf",
    'type'    : "pf",
    'param'   : "%s"%(sparam),
    'area'    : "90/120/0/360",
    'grid'    : "1.0/1.0",
    'target'  : "%s"%(sfile)
    }

print request
server.retrieve(request)


##server.retrieve({
##    'dataset' : "tigge",
##    'step'    : "24/to/120/by/24",
##    'number'  : "all",
##    'levtype' : "sl",
##    'date'    : "20091001/to/20091001",
##    'time'    : "00",
##    'origin'  : "all",
##    'type'    : "fc",
##    'param'   : "tp",
##    'area'    : "70/-130/30/-60",
##    'grid'    : "2/2",
##    'target'  : "data.grib"
##    })

#server.retrieve({
#    'dataset' : "tigge",
#    'step'    : "%d/to/%d/by/%d"%(btau,etau,dtau),
#    'number'  : "all",
#    'levtype' : "sl",
#    'date'    : "%s"%(ymd),
#    'time'    : "%s"%(hh),
#    'origin'  : "all",
#    'type'    : "fc",
#    'area'    : "global",
#    'grid'    : "1.0/1.0"
#    })





##dset ^sfc.2009100100.grb2
##index ^sfc.2009100100.grb2.idx
##undef 9.999E+20
##title sfc.2009100100.grb2
##*  produced by g2ctl v0.0.4m
##* griddef=1:0:(360 x 181):grid_template=0: lat-lon grid:(360 x 181) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 1.000000 lon 0.000000 to 359.000000 by 1.000000 #points=65160:winds(N/S)
##dtype grib2
##ydef 181 linear -90.000000 1
##xdef 360 linear 0.000000 1.000000
##tdef 1 linear 12Z01oct2009 1mo
##zdef 1 linear 1 1
##vars 23
##cape  0,1,,,8   0,7,6 ** atmos col Convective_available_potential_energy [J/kg]
##d2m   0,103,2   0,0,6 ** 2 m above ground dew_point_temperature [K]
##psfc  0,1   0,3,0 ** surface pressure [Pa]
##pmsl  0,101   0,3,0 ** mean sea level pressure [Pa]
##sdsfc  0,1   0,1,60 ** surface snow_depth_water_equivalent [kg/m^2]
##sfsfc  0,1   0,1,53,1 ** surface snow_fall_water_equivalent [kg/m^2]
##sktsfc  0,1   0,0,17 ** surface skin_temperature [K]
##slhfsfc  0,1   0,0,10,1 ** surface time_integrated_surface_latent_heat_flux [W/m^2 s]
##sm0_20cm  0,106,0,0.2   2,0,22 ** 0-0.2 m below ground soil_moisture [kg/m^3]
##sshfsfc  0,1   0,0,11,1 ** surface time_integrated_surface_sensible_heat_flux [W/m^2 s]
##ssrsfc  0,1   0,4,9,1 ** surface time_integrated_surface_net_solar_radiation [W/m^2 s]
##st0_20cm  0,106,0,0.2   2,0,2 ** 0-0.2 m below ground soil_temperature [K]
##sundsfc  0,1   0,6,24,1 ** surface sunshine_duration [s]
##tmax2m  0,103,2   0,0,0,2 ** 2 m above ground temperature [K]
##tmin2m  0,103,2   0,0,0,3 ** 2 m above ground temperature [K]
##t2m  0,103,2   0,0,0 ** 2 m above ground temperature [K]
##tcc  0,1,,,8   0,6,1 ** atmos col total_cloud_cover [%]
##tcw  0,1,,,8   0,1,51 ** atmos col total_column_water [kg/m^2]
##tpsfc  0,1   0,1,52,1 ** surface total_precipitation [kg/m^2]
##ttrsfc  0,1   0,5,5,1 ** surface time_integrated_outgoing_long_wave_radiation [W/m^2 s]
##ttrtoa  0,8   0,5,5,1 ** top of atmosphere time_integrated_outgoing_long_wave_radiation [W/m^2 s]
##u10m   0,103,10   0,2,2 ** 10 m above ground u_velocity [m/s]
##v10m   0,103,10   0,2,3 ** 10 m above ground v_velocity [m/s]
##ENDVARS
