#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M import *
MF=MFutils()


def getStillOnDtgs(sdir,invpathwx2Local,gsizMin=770.,verb=0):
    
    """ failed on 2023110500 because mike3 inv only found sfc.grb vice ua&sfc.grb
    and that was because the rsync from wxmap2.com
"""
    dpaths=glob.glob('%s/????/??????????'%(sdir))
    dtgsDoneT7={}

    for dpath in dpaths:
        grbs=glob.glob("%s/*sfc.grb2"%(dpath)) + glob.glob("%s/*ua.grb2"%(dpath))
        
        if(len(grbs) == 2):
            gsiz1=MF.GetPathSiz(grbs[0])
            gsiz2=MF.GetPathSiz(grbs[1])
        elif(len(grbs) == 1):
            gsiz1=MF.GetPathSiz(grbs[0])
            gsiz2=0
        else:
            gsiz1=gsiz2=0
            
        gsizAll=gsiz1+gsiz2
        gsizAll=gsizAll/(1024*1024)
        gsizAll=int(gsizAll)*1.0
        (ddir,dtg)=os.path.split(dpath)
    
        stat=0
        if(len(grbs) == 2 and gsizAll >= gsizMin):  stat=1
        dtgsDoneT7[dtg]=(stat,gsizAll)
    
    dtgsT7=dtgsDoneT7.keys()
    dtgsT7.sort()
    
    if(verb):
        for dtg in dtgsT7:
            print 'on  T7: ',dtg,dtgsDoneT7[dtg]
    
    
    dtgsDoneWx2={}
    
    cardswx2=MF.ReadFile2List(invpathwx2Local)

    for card in cardswx2:
        (dtg,stat,gsiz)=card.split()
        stat=int(stat)

        if(stat == 1):
            if(verb): print 'on WX2: ',dtg,stat,gsiz
            dtgsDoneWx2[dtg]=stat

    dtgsWx2=dtgsDoneWx2.keys()
    dtgsWx2.sort()
    
    dtgsStillOnWx2={}
    
    for dtg in dtgsWx2:
        dtgNot=1
        try:
            (dtgNot,gsiz)=dtgsDoneT7[dtg]
        except:
            dtgNot=0
            gsiz=-999
            
        if(gsiz != -999 and verb):
            print 'dtgNot: ',dtg,dtgNot,gsiz
            

        # -- if not(dtgNot) -- still on wx2
        #
        if(dtgNot == 0):
            dtgsStillOnWx2[dtg]=1


    dtgs=dtgsStillOnWx2.keys()
    dtgs.sort()

    return(dtgs,dtgsWx2,dtgsT7)

def getEcm5Ready(dtg,model='ecm5',override=0,verb=0):
    
    l2opt='-W'
    card=w2.getL2ModelStatus(model,l2opt,dtg,override=override,verb=verb)
    tt=card.split()
    sdtg=tt[1]
    sfields=int(tt[4])
    #print 'stat card: ',card
    #print 'SSS',sdtg,sfields
    ecm5Ready=0
    if(sfields > 50): ecm5Ready=1
    return(ecm5Ready)



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
            'doTCs':               ['t',0,1,'only do TCs here if running -ALL.py'],
            'doCycle':             ['C',0,0,'disable cycling'],
            'doWxmap2Inv':         ['2',1,0,'do NOT get wxmap2 inv'],
            'byPassWxmap2Inv':     ['B',0,1,'do byPass the wxmap2.com inv chk, e.g., cron broken'],
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

# -- superbt
#

sdirwx2='/home4/superbt1/dat/nwp2/w2flds/dat/%s'%(model)
invfilewx2='inv-%s-superbt.txt'%(model)
invpathwx2="%s/%s"%(sdirwx2,invfilewx2)
bddir=os.getenv('W2_BDIRDAT')

hsRsa="~/.ssh/id_rsa-SBT"
hsuser="superbt1@superbt.org"
tdir="%s/nwp2/w2flds/dat/%s"%(bddir,model)

prcdirW2=os.getenv('W2_PRC_DIR')
prcdir="%s/flddat"%(prcdirW2)
prcdirReanl="%s/reanl"%(prcdirW2)
prcdirTcTrk="%s/tctrk"%(prcdirW2)

# -- make local inventory -- first ... this also pull over wxmap2 inv
#
verbOpt=''
if(verb): verbOpt='-V'

cmd="%s/p-inv-%s-tenki7.py -X %s"%(prcdirReanl,model,verbOpt)
rcI7=MF.loopCmd2(cmd)
if(verb): print 'III---rcI7: ',rcI7

#  get the inventory from wxmap2 -- always
#
rsyncOpt=""" -alv --exclude "*ua.grb" --exclude "*.%s*"  --rsh="ssh -p2222 -i %s" """%(model,hsRsa)

if(doWxmap2Inv and not(byPassWxmap2Inv)):
    cmd="""rsync %s %s:%s %s/"""%(rsyncOpt,hsuser,invpathwx2,tdir)
    rcIW=MF.loopCmd2(cmd)
    if(verb): print 'III---rcIW: ',rcIW

invpathwx2Local="%s/%s"%(tdir,invfilewx2)
(dtgsOn,dtgsWx2,dtgsT7)=getStillOnDtgs(tdir,invpathwx2Local,verb=verb)

if(verb):
    print 'dtgsOn: ',dtgsOn
    print 'dtgsWx2: ',dtgsWx2

# -- case when either already on tenki7 or not available
if(len(dtgsOn) == 0):
    if(not(byPassWxmap2Inv)):
        print 'WWW---ecm5 NOT on wxmap2 (or allready on tenki7)...press...'
        sys.exit()
    else:
        print 'WWW-byPassWxmap2Inv...trying to get anyway...'
        
    
# -- do all the ones still on
#
if(mf.find(dtgopt,'wx2')):
    dtgsGet=dtgsOn
else:
    dtgsGet=mf.dtg_dtgopt_prc(dtgopt)

pycmd="%s/%s"%(pydir,pyfile)

# -- DON'T cycle here ... cycle in -ALL.py
#
#if(doCycle and len(dtgsGet) > 1):
    
    #for dtg in dtgsGet:
        #MF.sTimer('ECM5-Cycle-%s'%(dtg))
        #cmd="%s %s"%(pycmd,dtg)
        #for o,a in CL.opts:
            #cmd="%s %s %s"%(cmd,o,a)
        #mf.runcmd(cmd,ropt)
        #MF.dTimer('ECM5-Cycle-%s'%(dtg))
        
    #sys.exit()
    
if(len(dtgsOn) > 0 or byPassWxmap2Inv):

    for dtg in dtgsGet:
        
        if(verb): print 'DDD: ',dtg,'dtgsOn: ',dtgsOn

        if(dtg in dtgsOn or override or byPassWxmap2Inv):
            
            tyear=dtg[0:4]
            tdiryy="%s/%s"%(tdir,tyear)
            MF.ChkDir(tdiryy,'mk')
            
            cmd="""time rsync %s  %s:%s/%s/%s/ %s/%s/"""%(rsyncOpt,hsuser,sdirwx2,tyear,dtg,tdiryy,dtg)
            if(doIt):
                rc=MF.loopCmd2(cmd,nLoop=2,sLoop=30,verb=1)
            else:
                rc=mf.runcmd2(cmd,ropt)
                
            orc=rc
            if(len(rc) > 0): orc=rc[0] ; rc=orc
            
            if(rc == 0):
                print '1111-rc: ',rc,"""ropt is 'norun'"""
            elif(rc == 1):
                print 'FFF-good to go...press'
            elif(rc != 1): 
                print 'EEEE rsync error DATA...bail...' ; sys.exit()
            else:
                print 'EEEEE-rc: ',rc; sys.exit()
        
        cmd="%s/p-inv-%s-tenki7.py -V -X"%(prcdirReanl,model)
        if(doIt):
            rcI7END=MF.loopCmd2(cmd,nLoop=0)
            if(verb): print 'III--rcI7END: ',rcI7END
        else:
            mf.runcmd(cmd,ropt)
        
        ecm5Ready=getEcm5Ready(dtg)
        
        

            
