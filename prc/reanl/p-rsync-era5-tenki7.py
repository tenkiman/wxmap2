#!/usr/bin/env python

from WxMAP2 import *

def getDtgsOnWxmap2Rsync(sdir,invpathwx2Local,verb=0):

    dtgsDone={}
    dtgs2Rsync=[]
    
    dtgsDoneWx2={}
    cardswx2=MF.ReadFile2List(invpathwx2Local)

    for card in cardswx2:
        (dtg,stat)=card.split()
        istat=int(stat)
        if(istat == 1):
            dtgsDoneWx2[dtg]=istat
            
    dtgs=dtgsDoneWx2.keys()
    dtgs.sort()

    for dtg in dtgs:
        syear=dtg[0:4]
        sdirDtg="%s/%s/%s"%(sdir,syear,dtg)
        grbs=glob.glob("%s/*sfc.grb"%(sdirDtg)) + glob.glob("%s/*ua.grb2"%(sdirDtg))
        stat=0
        if(len(grbs) == 2):  stat=1
        if(stat):
            dtgsDone[dtg]=stat
        else:
            if(verb): print 'GGGGGGGGGGGGGGGGGetThisDtg: ',dtg
            dtgs2Rsync.append(dtg)

    dtgs=dtgs2Rsync

    return(dtgs)


def getStillOnDtgs(sdir,invpathwx2Local):

    dpaths=glob.glob('%s/??????????'%(sdir))

    dtgsDone={}

    for dpath in dpaths:
        grbs=glob.glob("%s/*sfc.grb"%(dpath)) + glob.glob("%s/*ua.grb2"%(dpath))
        (ddir,dtg)=os.path.split(dpath)
    
        stat=0
        if(len(grbs) == 2):  stat=1
    
        dtgsDone[dtg]=stat
    
    dtgs=dtgsDone.keys()
    dtgs.sort()


    dtgsDoneWx2={}
    cardswx2=MF.ReadFile2List(invpathwx2Local)

    for card in cardswx2:
        (dtg,stat)=card.split()
        stat=int(stat)

        if(stat == 1):
            dtgsDoneWx2[dtg]=stat

    dtgs=dtgsDoneWx2.keys()
    dtgs.sort()

    dtgsStillOnWx2={}
    
    for dtg in dtgs:
        dtgNot=0
        try:
            dtgstat=dtgsDone[dtg]
        except:
            dtgNot=1


        if(dtgNot == 1):
            dtgsStillOnWx2[dtg]=1


    dtgs=dtgsStillOnWx2.keys()
    dtgs.sort()

    return(dtgs)


class Era5CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):


        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
#            1:['year',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','norun','norun','must use -X to run'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            'doByDtgs':            ['d',1,0,'do NOT do rsync by dtgs'],
            }

        self.purpose='''
rsync era5 from wxmap2.com to tenki7'''
        
        self.examples='''
%s -N'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Era5CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(doIt): ropt=''

sdirwx2='/home3/mfiorino/dat/nwp2/w2flds/dat/era5'
invfilewx2='inv-era5-wxmap2.txt'
invpathwx2="%s/%s"%(sdirwx2,invfilewx2)

sdir='/w21/dat/nwp2/w2flds/dat/era5'
invpath="%s/inv-era5-tenki7.txt"%(sdir)
invpathwx2Local="%s/%s"%(sdir,invfilewx2)

prcdirW2=os.getenv('W2_PRC_DIR')
prcdir="%s/reanl"%(prcdirW2)

# -- first run the inventory and put to wxmap2 -- really needed -- yes!
#
cmd='%s/p-inv-era5-tenki7.py -X -V'%(prcdir)
rc=mf.runcmd2(cmd,ropt)

# -- get inv from wxmap2
#
rsyncOpt=""" -alv --exclude "*ua.grb" --exclude "*.era5*"  --rsh="ssh -p2222" """

cmd="""rsync %s mfiorino@wxmap2.com:%s %s/"""%(rsyncOpt,invpathwx2,sdir)
rc=mf.runcmd2(cmd,ropt)
if(rc < 0): print 'EEEE rsync error GGGEEETTTIING INVentory...bail...' ; sys.exit()
if(ropt != 'norun'): print '0000-era5-rc: ',rc


if(doByDtgs):
    dtgsOn=getDtgsOnWxmap2Rsync(sdir,invpathwx2Local,verb=verb)
else:
    dtgsOn=getStillOnDtgs(sdir,invpathwx2Local)

if(len(dtgsOn) > 0):
    
    if(doByDtgs):
        for dtg in dtgsOn:
            MF.sTimer('ERA5-pull-%s'%(dtg))
            year=dtg[0:4]
            cmd="""time rsync %s  mfiorino@wxmap2.com:%s/%s/%s/ %s/%s/%s/"""%(rsyncOpt,sdirwx2,year,dtg,sdir,year,dtg)
            rc=mf.runcmd2(cmd,ropt)
            MF.dTimer('ERA5-pull-%s'%(dtg))
            
            if(rc[0] != 1): print 'EEEE rsync error DATA...bail... rc: ',rc[0] ; sys.exit()
            if(ropt != 'norun'): 
                if(len(rc) == 2): print '1111-rc-bydtg-22: ',rc[0]
                else:             print '1111-rc-bydtg-11: ',rc
        
    else:
        cmd="""time rsync %s  mfiorino@wxmap2.com:%s/ %s/"""%(rsyncOpt,sdirwx2,sdir)
        rc=mf.runcmd2(cmd,ropt)
        if(rc < 0): print 'EEEE rsync error DATA...bail...rc: ',rc ; sys.exit()
        if(ropt != 'norun'): 
            if(len(rc) == 2): print '1111-rc-22: ',rc[0]
            else:             print '1111-rc-11: ',rc
        
            

# -- now run the inventory
#
cmd='%s/p-inv-era5-tenki7.py -V'%(prcdir)
rc=mf.runcmd2(cmd,ropt)
if(rc < 0): print 'EEEE rsync error PPPUUUTTTIIING INVentory...bail...' ; sys.exit()
