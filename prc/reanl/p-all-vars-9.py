#!/usr/bin/env python

from WxMAP2 import *

# -- generated .ctls with var 9 using
# in /run/media/fiorino/USB3Ext4-09/nwp2/w2flds/dat/era5
# g vars 20??/*/*ua.ctl | g -v end | g -v 'vars 11' > vars-9-20.txt
# g vars 19??/*/*ua.ctl | g -v end | g -v 'vars 11' > vars-9-19.txt

vfiles=glob.glob("vars*")
vcmd='p-era5-ua-ctl-corr.py'

ropt='norun'
ropt=''

for vfile in vfiles:
    
    vcards=open(vfile).readlines()
    
    for vcard in vcards:
        tt=vcard.split('/')
        dtg=tt[1]
        cmd="%s %s"%(vcmd,dtg)
        mf.runcmd(cmd,ropt)
        
