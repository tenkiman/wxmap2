#!/usr/bin/env python

from WxMAP2 import *


def getStillOnDtgs(sdir,invpathwx2Local):

    dpaths=glob.glob('%s/????/??????????'%(sdir))
    dtgsDoneT7={}

    for dpath in dpaths:
        grbs=glob.glob("%s/*sfc.grb2"%(dpath)) + glob.glob("%s/*ua.grb2"%(dpath))
        (ddir,dtg)=os.path.split(dpath)
    
        stat=0
        if(len(grbs) == 2):  stat=1
    
        dtgsDoneT7[dtg]=stat
    
    dtgsT7=dtgsDoneT7.keys()
    dtgsT7.sort()
    
    dtgsDoneWx2={}
    
    cardswx2=MF.ReadFile2List(invpathwx2Local)

    for card in cardswx2:
        (dtg,stat)=card.split()
        stat=int(stat)

        if(stat == 1):
            dtgsDoneWx2[dtg]=stat

    dtgsWx2=dtgsDoneWx2.keys()
    dtgsWx2.sort()
    
    dtgsStillOnWx2={}
    
    for dtg in dtgsWx2:
        dtgNot=0
        try:
            dtgstat=dtgsDoneT7[dtg]
        except:
            dtgNot=1

        # -- if not(dtgNot) -- still on wx2
        #
        if(dtgNot == 1):
            dtgsStillOnWx2[dtg]=1


    dtgs=dtgsStillOnWx2.keys()
    dtgs.sort()

    return(dtgs,dtgsWx2,dtgsT7)



class Ecm5CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):


        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  '''pull ecm5 from wxmap2 '''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','norun','norun','must use -X to run'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            'doTCs':               ['t',1,0,'do NOT do the TC tracker'],
            'doCycle':             ['C',1,0,'do NOT cycle by dtgs'],
            'doWxmap2Inv':         ['2',1,0,'do NOT get wxmap2 inv'],
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

model='ecm5'
sdirwx2='/home3/mfiorino/dat/nwp2/w2flds/dat/%s'%(model)
invfilewx2='inv-%s-wxmap2.txt'%(model)
invpathwx2="%s/%s"%(sdirwx2,invfilewx2)

bddir=os.getenv('W2_BDIRDAT')

tdir="%s/nwp2/w2flds/dat/%s"%(bddir,model)

prcdirW2=os.getenv('W2_PRC_DIR')
prcdir="%s/flddat"%(prcdirW2)
prcdirReanl="%s/reanl"%(prcdirW2)
prcdirTcTrk="%s/tctrk"%(prcdirW2)

# -- make local inventory -- always -- first
#
#cmd="%s/p-inv-%s-tenki7.py"%(prcdirReanl,model)
#rcI7=MF.loopCmd2(cmd)
#print 'III-77777 for %  rcI7: %d'%(pyfile,rcI7)

rsyncOpt=""" -alv --exclude "*ua.grb" --exclude "*.%s*"  --rsh="ssh -p2222" """%(model)

#  get the inventory from wxmap2 -- always
#
cmd="""rsync %s mfiorino@wxmap2.com:%s %s/"""%(rsyncOpt,invpathwx2,tdir)
rcIW=MF.loopCmd2(cmd,nLoop=0)
print 'III-WWW222 for: %  rcIW: %d'%(pyfile,rcIW)
#rc=mf.runcmd2(cmd,ropt='')


invpathwx2Local="%s/%s"%(tdir,invfilewx2)
(dtgsOn,dtgsWx2,dtgsT7)=getStillOnDtgs(tdir,invpathwx2Local)

if(verb):
    print 'dtgsOn:  ',dtgsOn
    print 'dtgsWx2: ',dtgsWx2
    #print 'dtgsT7:  ',dtgsT7


# -- do all the ones still on
#
if(mf.find(dtgopt,'wx2')):
    dtgsGet=dtgsOn
else:
    dtgsGet=mf.dtg_dtgopt_prc(dtgopt)

pycmd="%s/%s"%(pydir,pyfile)
pycmdRun=pycmd.replace('-ALL','')

# -- cycle here ...
#
if(doCycle and len(dtgsGet) > 0):

    MF.sTimer('ALL-ECM5-Cycle')
    
    for dtg in dtgsGet:
        MF.sTimer('ECM5-Cycle-%s'%(dtg))
        
        # -- if running inside -ALL do NOT get the inv from wxmap2
        #
        if(doTCs):
            cmd="%s %s -t -2"%(pycmdRun,dtg)
        else:
            cmd="%s %s -2"%(pycmdRun,dtg)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
        MF.dTimer('ECM5-Cycle-%s'%(dtg))
        
    MF.dTimer('ALL-ECM5-Cycle')
    sys.exit()
    
