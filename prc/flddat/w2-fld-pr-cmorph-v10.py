#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['yyyymm',    'no default'],
            }

        self.defaults={
            }
        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doit':             ['X',0,1,' execute'],
        }

        self.purpose='''
convert cpc qmorph from compressed binary to grib'''

        self.examples="""
%s 201809"""


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  local defs
#

def makeprctl(tmpdir,dtg):

        
    ctlpath="%s/pr.ctl"%(tmpdir)
    gtime=mf.dtg2gtime(dtg)

    dsetcard="dset ^CMORPH_V1.0_ADJ_8km-30min_%s"%(dtg)
    optioncard='options little_endian'
            
    prctl="""%s
%s
UNDEF  -999.0
TITLE  Precipitation estimates
XDEF 4948 LINEAR   0.036378335 0.072756669
YDEF 1649 LINEAR -59.963614    0.072771377
ZDEF   1 LEVELS 1
TDEF   2 LINEAR  %s 30mn
VARS 1
pr   1  99  hourly cmorph [ mm/hr ]
ENDVARS"""%(dsetcard,optioncard,gtime)

    C=open(ctlpath,'w')
    C.writelines(prctl)
    C.close()
    return(ctlpath)

xgrads=setXgrads(useStandard=0, useX11=1, returnBoth=0)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#   main loop

MF.sTimer('all')

bbdir=w2.PrCV10DatRoot

tbdir=bbdir

bym=201905
eym=201912

bym=201812
eym=201812
bym=201601
eym=201601
yyyymms=mf.yyyymmrange(bym,eym)

for yyyymm in yyyymms:
    
    year=yyyymm[0:4]
    mm=yyyymm[4:]
    
    sbdir="%s/incoming/%s"%(bbdir,year)
    sdir="%s/%s"%(sbdir,yyyymm)
    mf.ChkDir(sdir,'mk')
    
    tdir="%s/grib/%s/%s"%(tbdir,year,yyyymm)
    mf.ChkDir(tdir,'mk')
    
    tmpdir="%s/tmp"%(sbdir)
    mf.ChkDir(tmpdir,'mk')
    
    prcdir=w2.PrcDirFlddatW2
    
    MF.sTimer('cmorph-v10-%s'%(yyyymm))
    
    tt=glob.glob("%s/*%s*.tar"%(sbdir,yyyymm))
    tarball=tt[0]
    
    cmd="tar -C %s -xvf %s"%(sbdir,tarball)
    mf.runcmd(cmd,ropt)
    
    dpaths=glob.glob("%s/*.bz2"%(sdir))
    dpaths.sort()
    for dpath in dpaths:
        print 'ddd',dpath
        (ddir,dfile)=os.path.split(dpath)
        (dbase,dext)=os.path.splitext(dfile)
        tt=dbase.split('_')
        dtg=tt[-1]
        
        tpath="%s/%s"%(tmpdir,dfile)
        cmd="mv %s %s"%(dpath,tpath)
        mf.runcmd(cmd,ropt)
        
        cmd="bzip2 -d %s"%(tpath)
        mf.runcmd(cmd,ropt)
        
        latsctlpath=makeprctl(tmpdir,dtg)
    
        latsgrbpath="%s/cmorph-v10.%s"%(tdir,dtg)
        latsgrbpath="%s/cmorph-v10.%s.grb"%(tdir,dtg)
    
        cmd="%s -lbc \"run %s/w2-fld-pr-cmorph-8km-lats.gs %s %s\""%(xgrads,prcdir,latsctlpath,latsgrbpath)
        mf.runcmd(cmd,ropt)
    
        cmd="rm %s/*"%(tmpdir)
        mf.runcmd(cmd,ropt)
    
    MF.dTimer('cmorph-v10-%s'%(yyyymm))

sys.exit()

