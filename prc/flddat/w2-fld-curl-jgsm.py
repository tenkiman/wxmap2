#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

from M2 import setModel2

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
        }

        self.options={
            'verb':                 ['V',0,1,'verbose'],
            'override':             ['O',0,1,'1 - '],
            'ropt':                 ['N','','norun','ropt'],
        }


        self.purpose='''pull global GSM fields from JMA
(c) 1992-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s ops6'''


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

model='jgsm'

dtgs=mf.dtg_dtgopt_prc(dtgopt)

sbDir='https://www.wis-jma.go.jp/d/o/RJTD/GRIB/Global_Spectral_Model/Latitude_Longitude/1.25_1.25/90.0_-90.0_0.0_358.75/Upper_air_layers'
sbFile1='W_jp-JMA-tokyo,MODEL,JMA+gsm+gpv,C_RJTD'
sbFile2='GSM_GPV_Rgl_Gll1p25deg_L-all_FD0000-0512_grib2.bin'

tbDir="%s/w2flds/dat/%s"%(w2.Nwp2DataBdir,model)

maxTime=60
maxTime=maxTime*60*60

connTime=2
connTime=connTime*60*60

#curlOpt='--max-time %d --connect-timeout %d --progress-bar'%(maxTime,connTime)
curlOpt='-k -S -s --max-time %d --connect-timeout %d'%(maxTime,connTime)

tsizMin=145603973
tsizMin=140000000

m2=setModel2(model)


for dtg in dtgs:

    cyear=dtg[0:4]
    ymd=dtg[0:8]
    hh=dtg[8:10]+'0000'
    tdir="%s/%s/%s"%(tbDir,cyear,dtg)
    tfile="%s.w2flds.%s.grb2"%(model,dtg)
    sdir="%s/%s/%s"%(sbDir,ymd,hh)
    sfile='%s_%s%s_%s'%(sbFile1,ymd,hh,sbFile2)
    
    spath="%s/%s"%(sdir,sfile)
    tpath="%s/%s"%(tdir,tfile)
    
    if(ropt != 'norun'):
        MF.ChkDir(tdir, 'mk')
    else:
        print 'target Dir: ',tdir
    
    tsiz=MF.GetPathSiz(tpath)
    
    if(tsiz < tsizMin or override):
        cmd="time curl %s %s -o %s"%(curlOpt,spath,tpath)
        mf.runcmd(cmd,ropt)
        tsiz=MF.GetPathSiz(tpath)
    else:
        print 'WWW-already done...tsiz: ',tsiz
        
    if(tsiz > tsizMin):
        
        m2.setDbase(dtg)
        m2.setGrib(verb=verb)
        
        
        
    
    