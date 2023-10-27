#!/usr/bin/env python

from WxMAP2 import *

dtgs=['2021031312','2021031318','2021031400','2021031406']
dtgs=['2021031400','2021031406','2021031412']
dtgs=['2021031418']
ropt='norun'
ropt=''

for dtg in dtgs:
    models=['gfs2','ecm5','cgd2','navg','jgsm']
    if (dtg[8:10] == '18' or dtg[8:10] == '06'):
        models=['gfs2','navg','jgsm']
    elif(dtg == '2021031400'):
        models=['navg','jgsm']

    
    for model in models:
        cmd="do-%s.py %s"%(model,dtg)
        mf.runcmd(cmd,ropt)

    print
