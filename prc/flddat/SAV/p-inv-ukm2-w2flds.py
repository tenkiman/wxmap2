#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
from M2 import setModel2

model='ukm2'
bdtg='2019062000'
edtg='2019070412'

alltaus00_12=range(0,72+1,6)+range(84,168+1,12)
alltaus06_18=range(0,66+1,6)

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
        }

        self.options={
            'verb':              ['V',0,1,'verb=1 is verbose'],
            'ropt':              ['X','norun','',""" default is ropt='norun'"""],
            'override':          ['O',0,1,'1 - '],
            'onlyMissing':       ['M',0,1,'1 - '],
        }

        self.purpose='''
inventory ukm2 w2flds by dtg
(c) 2009-%s Michael Fiorino,NOAA ESRL'''%(w2.curyear)

        self.examples='''
%s cur12-12'''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#
argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

m2=setModel2(model)
sdir=m2.w2fldsSrcDir

dtgs=mf.dtg_dtgopt_prc(dtgopt)

misstaus={}
for dtg in dtgs:

    gtaus=[]
    hh=dtg[8:10]
    ataus=alltaus00_12
    alltaus00_12=range(0,72+1,6)+range(84,168+1,12)    
    if(hh == '06' or hh == '18'): ataus=alltaus06_18
    
    grbs=glob.glob("%s/%s/*.grb1"%(sdir,dtg))
    for grb in grbs:
        tt=grb.split('.')
        tau=tt[-2][1:]
        gtau=int(tau)
        gtaus.append(gtau)


    gtaus.sort()
    mtaus=[]
    for atau in ataus:
        if(not(atau in gtaus)):
            if(verb): print 'missing in dtg: ',dtg,' run tau: ',atau
            mtaus.append(atau)

    misstaus[dtg]=mtaus

prcdir=w2.PrcDirWxmap2W2
mdtgs=misstaus.keys()
mdtgs.sort()
cmds=[]
for mdtg in mdtgs:
    mtaus=misstaus[mdtg]
    if(len(mtaus) > 0):
        # -- check in /public/data/grids/ukmet
        #
        for mtau in mtaus:
            mask="/public/data/grids/ukmet/%s_%03d*"%(mdtg,int(mtau))
            bfs=glob.glob(mask)
            nthere=len(bfs)
        print 'MMM dtg: ',mdtg,' #/public: %2d'%(nthere),' missing taus: ',mtaus
        if(nthere > 0):
            cmd='%s/w2.nwp2.py %s ukm2 -t'%(prcdir,mdtg)
            cmds.append(cmd)
            
    elif(onlyMissing == 0):
        print 'CCC dtg: ',mdtg,' ........ no missing taus ...........'
        
        
if(not(onlyMissing)):
    for cmd in cmds:
        mf.runcmd(cmd,ropt)
        


