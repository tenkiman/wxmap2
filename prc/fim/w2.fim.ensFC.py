#!/usr/bin/env python

import os,sys,time,copy
import getopt,glob
import cPickle as pickle

import mf
import w2
import FM

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#
    
test=1

if(test):
    dtgopt='2009112412.cur12-12'
    dtgopt='2009113000'
    bdtg='2009112412'
    model='rtfimy'
    model='rtfim'
    model='rtfimx'
    models=['rtfim','rtfimx','rtfimy']

    bdtg=None
    edtg='cur12'
    rootdtg=edtg
    models=['rtfim']
    
else:
    rc=FM.CmdLineEnsFc()



dsbdirlocal="%s/DSs"%(FM.lrootWjet)
dblocal="rtfim_local_%s.pypdb"%(dtg)
DSslocal=FM.DataSets(bdir=dsbdirlocal,name=dblocal,verb=1)
if(DSslocal == None): sys.exit()

for model in models:

    dskey="%s.%s"%(model,rootdtg)
    if(dslocal != None):
        FRl=dslocal.FR
    else:
        continue

    #FRl.EnsFcCtl(bdtg=bdtg,edtg=edtg,override=override,verb=verb)

sys.exit()

