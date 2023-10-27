#!/usr/bin/env python

from WxMAP2 import *


def getStillOnDtgs(sdir,invpathwx2Local):

    dpaths=glob.glob('%s/??????????'%(sdir))
    dtgsDone={}

    for dpath in dpaths:
        grbs=glob.glob("%s/*sfc.grb2"%(dpath)) + glob.glob("%s/*ua.grb2"%(dpath))
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


class Ecm5CmdLine(CmdLine):

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
            'doByDtgs':            ['d',0,1,'do rsync by dtgs'],
            }

        self.purpose='''
rsync ecm5 from wxmap2.com to tenki7'''
        
        self.examples='''
%s -N'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Ecm5CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(doIt): ropt=''

sdirwx2='/home3/mfiorino/dat/nwp2/w2flds/dat/ecm5'
invfilewx2='inv-ecm5-wxmap2.txt'
invpathwx2="%s/%s"%(sdirwx2,invfilewx2)

sdir='/w21/dat/nwp2/w2flds/dat/ecm5'
invpath="%s/inv-ecm5-tenki7.txt"%(sdir)
invpathwx2Local="%s/%s"%(sdir,invfilewx2)

prcdirW2=os.getenv('W2_PRC_DIR')
prcdir="%s/reanl"%(prcdirW2)

# -- first run the inventory and put to wxmap2 -- really needed
#
#cmd='%s/p-inv-ecm5-tenki7.py -V'%(prcdir)
#rc=mf.runcmd2(cmd,ropt)

# -- get inv from wxmap2
#
rsyncOpt=""" -alv --exclude "*ua.grb" --exclude "*.ecm5*"  --rsh="ssh -p2222" """

cmd="""rsync %s mfiorino@wxmap2.com:%s %s/"""%(rsyncOpt,invpathwx2,sdir)
rc=mf.runcmd2(cmd,ropt)
if(rc < 0): print 'EEEE rsync error GGGEEETTTIING INVentory...bail...' ; sys.exit()
if(ropt != 'norun'): print '0000-ecm5-rc: ',rc


dtgsOn=getStillOnDtgs(sdir,invpathwx2Local)

if(len(dtgsOn) > 0):
    
    if(doByDtgs):
        for dtg in dtgsOn:
            cmd="""time rsync %s  mfiorino@wxmap2.com:%s/%s/ %s/%s/"""%(rsyncOpt,sdirwx2,dtg,sdir,dtg)
            rc=mf.runcmd2(cmd,ropt)
            if(rc != 1): print 'EEEE rsync error DATA...bail...' ; sys.exit()
            if(ropt != 'norun'): print '1111-rc: ',rc
        
    else:
        cmd="""time rsync %s  mfiorino@wxmap2.com:%s/ %s/"""%(rsyncOpt,sdirwx2,sdir)
        rc=mf.runcmd2(cmd,ropt)
        if(rc < 0): print 'EEEE rsync error DATA...bail...' ; sys.exit()
        if(ropt != 'norun'): print '1111-rc: ',rc
        
            

# -- now run the inventory
#
cmd='%s/p-inv-ecm5-tenki7.py -X -V'%(prcdir)
rc=mf.runcmd2(cmd,ropt)
if(rc < 0): print 'EEEE rsync error PPPUUUTTTIIING INVentory...bail...' ; sys.exit()
