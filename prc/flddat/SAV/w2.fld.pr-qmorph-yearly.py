#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  local defs
#
            
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yearopt',    'no default'],
            }


        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'source':           ['S:',None,'a',' [qmorph]|cmorph'],
            'ropt':             ['N','','norun',' norun is norun'],
            }

        self.purpose='''
reorg cpc c|qmorph by year'''

        self.examples="""
%s 2018"""

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


MF.sTimer('all')
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#   main loop
#

if(not(w2.onKaze)):
    print 'EEE only run this on Kaze!!!'
    sys.exit()

pdir=w2.PrcDirFlddatW2
sources=['qmorph','cmorph']

yy=yearopt.split('.')
if(len(yy) == 2):
    byear=yy[0]
    eyear=yy[1]
    years=mf.yyyyrange(2013,2018)
    
else:
    years=[yearopt]

if(source == None):
    
    for year in years:
        for source in sources:
            cmd="%s %s"%(pypath,year)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)
        
            cmd="%s -S %s"%(cmd,source)
            mf.runcmd(cmd,ropt)

    sys.exit()
    
else:
    None



if(source == 'qmorph'):
    sdir=w2.NhcQmorphFinalLocal
    sdirl=w2.NhcFtpTargetDirQmorph
    grbdir=w2.NhcQmorphProductsGrib
    prodpre="pr%s"%(source[0])
    
elif(source == 'cmorph'):
    sdir=w2.NhcCmorphFinalLocal
    sdirl=w2.NhcFtpTargetDirCmorph
    grbdir=w2.NhcCmorphProductsGrib
    prodpre="pr%s"%(source[0])


MF.sTimer('glob')
pmask="%s/*%s*.grb"%(grbdir,yearopt)
imask="%s/C*%s*"%(sdirl,yearopt)
smask="%s/*.%s*.grb*"%(sdir,yearopt)

grbPrdPaths=glob.glob(pmask)
grbSrcPaths=glob.glob(smask)
grbIncPaths=glob.glob(imask)
MF.dTimer('glob')

grbPrdPaths.sort()

print 'PPPPPPPPPP: ',pmask
for gpath in grbPrdPaths:
    (gdir,gfile)=os.path.split(gpath)
    (base,ext)=os.path.splitext(gfile)
    tt=base.split('_')
    dtg=tt[-1]
    yyyymm=dtg[0:6]
    
    tdir="%s/%s"%(grbdir,yyyymm)
    MF.ChkDir(tdir,'mk')
    
    cmd="mv %s %s/%s"%(gpath,tdir,gfile)
    mf.runcmd(cmd,ropt)
    
    #print 'ppppp: ',yyyymm,dtg,gpath
            

grbIncPaths.sort()
print 'IIIIIIIIII: ',imask
for ipath in grbIncPaths:
    (idir,ifile)=os.path.split(ipath)
    (base,ext)=os.path.splitext(ifile)
    tt=base.split('_')
    dtg=tt[-1]
    if(mf.find(dtg,'RT2')): dtg=dtg.split('.')[0]
    yyyymm=dtg[0:6]

    tdir="%s/%s"%(sdirl,yyyymm)
    MF.ChkDir(tdir,'mk')
    
    cmd="mv %s %s/%s"%(ipath,tdir,ifile)
    mf.runcmd(cmd,ropt)
    

grbSrcPaths.sort()
print 'SSSSSSSSSS: ',smask
for spath in grbSrcPaths:
    (sdir,sfile)=os.path.split(spath)
    (base,ext)=os.path.splitext(sfile)
    if(mf.find(spath,'.idx')): continue
    tt=base.split('.')
    if(len(tt) == 1): continue
    dtg=tt[-1]
    yyyymm=dtg[0:6]

    tdir="%s/%s"%(sdir,yyyymm)
    MF.ChkDir(tdir,'mk')
    
    cmd="mv %s %s/%s"%(spath,tdir,sfile)
    mf.runcmd(cmd,ropt)
    
sys.exit()

            
            

MF.dTimer('all')
sys.exit()    

