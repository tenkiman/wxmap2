import os
import sys
import mf
import glob


def EcmwfCtl(dtg,ctlpath,ropt=''):

    ymdh=dtg[2:10]
    
    gtime=mf.dtg2gtime(dtg)

    ctl="""dset ^ecens_DCD%s%%m2%%d2%%h2001
index ^ecmo.%s.gmp
undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
ydef 181 linear -90.000000 1
xdef 360 linear 0.000000 1.000000
tdef  21 linear 00Z14jun2007 12hr
zdef 14 levels
1000 925 850 700 500 400 300 250 200 150 100 50 20 10 
vars 15
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       14 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      14 157,100,0 ** Relative humidity %%
ta       14 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars"""%(ymdh,dtg,gtime)
    
    mf.WriteCtl(ctl,ctlpath)

    dogribmap=1
    if(dogribmap):
        cmd="gribmap -E -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)


