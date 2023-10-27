#!/usr/bin/env python

from M import *
MF=MFutils()

class Rsync(MFbase):
    
    server='fiorino@kishou.fsl.noaa.gov'
    sbase='/dat2'
    sbase='/FWV2/dat2/nwp2/w2flds/dat'
    #sbase='/dat4/nwp2/w2flds/dat'
    tbase='/USB3V1/kishou/dat/nwp2/w2flds/dat'
    pdir='/w21/etc'

    def __init__(self,dtg,model,
                 sbase=sbase,
                 tbase=tbase,
                 ):



        self.tdir="%s/%s/%s"%(self.tbase,model,dtg)
        self.sdir="%s/%s/%s"%(self.sbase,model,dtg)

    def doRsync(self,
                dodelete=0,
                doupdate=0,
                ropt='norun'
                ):

        ruopt=''
        rnopt=''
        delopt=''
        if(doupdate):      rupopt='-u'
        if(ropt != ''):    rnopt='-n'
        if(dodelete):      delopt='--delete'

        MF.ChkDir(self.tdir,'mk')
        self.rsyncopt="%s %s %s -alv --exclude-from=%s/ex-w21.txt"%(delopt,ruopt,rnopt,self.pdir)
        cmd="rsync %s %s:%s/ %s/"%(self.rsyncopt,self.server,self.sdir,self.tdir)
        mf.runcmd(cmd,'')





#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            2:['modelopt',  '''model - gfs2,ecm2,fim8,fimx,ukm2,ngp2,cmc2'''],
            }

        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'doit':['X',0,1,' run...'],
            'doupdate':['u',0,1,' update in rsync'],
            }

        self.purpose='''
purpose -- rsync from kishou to local tc data sets
%s -N -V -u 
'''
        self.examples='''
%s -V -N
'''
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

argv=sys.argv
CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(modelopt == 'all'):
    models=['gfs2','ecm2','ukm2','ngpc','fim8','cmc2']
else:
    models=modelopt.split(',')

dtgs=mf.dtg_dtgopt_prc(dtgopt)
for dtg in dtgs:
    for model in models:
        rS=Rsync(dtg,model)
        rS.doRsync(ropt=ropt)

sys.exit()


