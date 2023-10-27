#!/usr/bin/env python
from WxMAP2 import *

from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()


def retErai(dtg,ropt='norun',override=0):

    bdate="%s-%s-%s"%(dtg[0:4],dtg[4:6],dtg[6:8])
    bhour="%s:00:00"%(dtg[8:10])

    tdir='/w21/dat/reanl/erai/fc/%s'%(dtg)

    tpathFinal="%s/erai.%s.grb"%(tdir,dtg)
    sizF=MF.getPathSiz(tpathFinal)

    if(ropt == 'norun'):
        print 'retErai tdir: ',tdir
        return(-1)
    
    if(sizF > 0):
        print 'III final grb: ',tpathFinal,' already done...press'
        return(0)


    if(ropt == ''):
        MF.ChkDir(tdir,'mk')

        tpathSfcAN="%s/erai.%s.sfc.an.grb"%(tdir,dtg)
        tpathSfcFC="%s/erai.%s.sfc.fc.grb"%(tdir,dtg)
        
        tpathuaAN="%s/erai.%s.ua.an.grb"%(tdir,dtg)
        tpathuaFC="%s/erai.%s.ua.fc.grb"%(tdir,dtg)
        
        sizsAN=MF.getPathSiz(tpathSfcAN)
        sizsFC=MF.getPathSiz(tpathSfcFC)
        sizuAN=MF.getPathSiz(tpathuaAN)
        sizuFC=MF.getPathSiz(tpathuaFC)
    else:
        print 'III will do retErai(%s)...'%(dtg)
        return(0)

    if(sizsAN > 0 and sizsFC > 0 and sizuAN > 0 and sizuFC > 0):
        print 'already done for dtg: ',dtg
        print tpathSfcAN
        print tpathSfcFC
        print tpathuaAN
        print tpathuaFC
        return(0)
    
    reqSfcAN={
        "class": "ei",
        "dataset": "interim",
        "date": "%s"%(bdate),
        "expver": "1",
        "grid": "0.75/0.75",
        "levtype": "sfc",
        "param": "151.128/165.128/166.128/137.128",
        "step": "0",
        "stream": "oper",
        "time": "%s"%(bhour),
        "type": "an",
        "target": "%s/erai.%s.sfc.an.grb"%(tdir,dtg),
        }
    
    reqSfcFC={
        "class": "ei",
        "dataset": "interim",
        "date": "%s"%(bdate),
        "expver": "1",
        "grid": "0.75/0.75",
        "levtype": "sfc",
        "param": "143.128/228.128/137.128/151.128/165.128/166.128",
        "step": "all",
        "stream": "oper",
        "time": "%s"%(bhour),
        "type": "fc",
        "target": "%s/erai.%s.sfc.fc.grb"%(tdir,dtg),
        }
    
    requaAN={
        "class": "ei",
        "dataset": "interim",
        "date": "%s"%(bdate),
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": "100/200/300/400/500/700/850/925/1000",
        "levtype": "pl",
        "param": "129.128/130.128/131.128/132.128/157.128",
        "step": "0",
        "stream": "oper",
        "time": "%s"%(bhour),
        "type": "an",
        "target": "%s/erai.%s.ua.an.grb"%(tdir,dtg),
        }
    
    requaFC={
        "class": "ei",
        "dataset": "interim",
        "date": "%s"%(bdate),
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": "100/200/300/400/500/700/850/925/1000",
        "levtype": "pl",
        "param": "129.128/130.128/131.128/132.128/157.128",
        #    "step": "6/12/18/24/30/36/48/60/72/84/96/108/120/132/144/156/168/180/192/204/216/228/240",
        "step": "all",
        "stream": "oper",
        "time": "%s"%(bhour),
        "type": "fc",
        "target": "%s/erai.%s.ua.fc.grb"%(tdir,dtg),
        }


    if(ropt == ''):
        
        server.retrieve(reqSfcAN)
        server.retrieve(reqSfcFC)
        
        server.retrieve(requaAN)
        server.retrieve(requaFC)
        rc=1
    else:
        rc=0

    return(rc)



class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.options={
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            }

        self.purpose='''
mars rtetrieve ERAI and run tracker'''
        
        self.examples='''
%s 1983081512'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


dtgs=mf.dtg_dtgopt_prc(dtgopt)


for dtg in dtgs:
    print '..........................working: ',dtg
    rc=retErai(dtg,ropt=ropt,override=override)
    if(rc):
        cmd="p.tmtrkS.py %s"%(dtg)
        mf.runcmd(cmd,ropt)
    elif(rc == 0):
        print 'AAA already done ...'
        
    
sys.exit()
