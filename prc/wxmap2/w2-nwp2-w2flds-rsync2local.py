#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
from M2 import setModel2

models2Chk=['gfs2','goes','ecm4','ecm5','ecmt','ukm2','jgsm']
modelsW2=['gfs2','ecm4','ecmt','ukm2','ecm5','jgsm','era5']
modelsW20012=modelsW2
modelsW20618=['gfs2','ukm2','jgsm']
modelsNwp2=['goes']
modelsExtra=['ecmt']
reducedTaus=range(0,126+1,6)

srcUrl={
    'dat0':'/dat0/dat',
    'dat1':'/dat1/nwp2',
    'dat2':'/dat2-orig/dat/nwp2',
    'dat16':'/dat2/dat/nwp2',
    'dat3':'/dat3/nwp2',
    'dat4':'/dat4/nwp2',
    'dat5':'/dat5/nwp2',
    'dat6':'/dat5/nwp2',
    'dat7':'/dat7/nwp2',
    'dat9':'/dat9/nwp2',
    'dat10':'/dat10/dat/nwp2',
    'dat11':'/dat11/nwp2',
    'dat12':'/dat12/dat/nwp2',
    'dat13':'/dat13/nwp2',
    'dat14':'/dat14/nwp2',
    'dat15':'/dat15/nwp2',
    'dat20':'/dat20/dat/nwp2',
    'dat80':'/dat80/dat/nwp2',
    'dat81':'/dat81/dat/nwp2',
    'dat82':'/dat82/dat/nwp2',
    'dat83':'/dat83/dat/nwp2',
    'ssd1':'/ssd1/dat/nwp2',
    'ssd4':'/ssd4/dat/nwp2',
    
    'wxmap2':'mfiorino@wxmap2.com:/home3/mfiorino/dat/nwp2',
    'kishou':'fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2',
    #'hwrf':'fiorino@kishou.fsl.noaa.gov:$W2_HFIP../w21/dat/nwp2',
}

srcTypes2Move=['dat1','dat2','dat3','dat4','dat5','dat9','dat10','dat11','dat13','dat14','dat15','dat16','dat80','dat81','dat82']


def getRsyncCmd(model,dtg,dmodelType,
                srcType=None,trgType=None,stmopt=None,
                doClean=0,doCleanDat0=0,
                doCleanLocal=0,doCleanTarget=0,
                reverse=0,doLs=0,thinTaus=-999,doRsync=0,
                hwrfTaus=0,
                ropt='',verb=0,override=0):
    
    lsext=''
    doarchive=0
    m=setModel2(model)
    m.dtype=dmodelType
    
    #if(dmodelType != None):         m.bddir="%s/%s/dat/%s"%(w2.Nwp2DataBdir,'w2flds',model)
    if(hasattr(m,'setxwgribNwp2')): m.setxwgrib=m.setxwgribNwp2
    fm=m.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,doDATage=1)
    #fm.ls()
    #fd=fm.GetDataStatus(dtg)
    #fd.ls()
    rsopt="-alv -P"
    rsopt='-alv --size-only'
    if(srcType == 'hwrf' and stmopt != None):
        rsopt='''%s --include "*%s*" --exclude "*"'''%(rsopt,stmopt)
    elif(srcType == 'wxmap2'):
        rsopt='-alv --size-only -p2222'
        
    ddtg=fm.modelDdtg
    tdir=fm.dbasedir
    tt=tdir.split('/')
    
    if(ddtg == 12 and not(MF.is0012Z(dtg))):
        print 'WWW no data for model: ',model,' dtg: ',dtg,' return None'
        return(None)

    srcTypes=srcUrl.keys()
    srcTypes.sort()
    
    if(srcType != None and not(srcType in srcTypes)):
        print 'EEE--getRsyncCmd: invalid srcType: ',srcType,' not in: ',srcTypes
        sys.exit()
        
    if(srcType != None):
        sbdir=srcUrl[srcType]
    else:
        sbdir='/w21/dat'

    if(trgType != None and not(trgType in srcTypes)):
        print 'EEE--getRsyncCmd: invalid trgType: ',trgType,' not in: ',trgTypes
        sys.exit()
        
    bb=[]
    if(trgType != None):
        tbdir=srcUrl[trgType]
        bb=tbdir.split('/')

    prcdir=w2.PrcDirFlddatW2
    l2opt=''
    if(dmodelType == 'w2flds'):  l2opt='-W'


    # -- SSSSSS -- set sdir here based on sbdir and fm.dbasedir
    #
    nb=-4
    if(dmodelType == 'w2flds' and len(tt) == 10): nb=-5
    if(dmodelType == 'w2flds' and len(tt) == 9): nb=-4
    if(dmodelType == 'nwp2'): nb=-3
    sdir=sbdir
    
    for t in tt[nb:]:
        sdir="%s/%s"%(sdir,t)
        
    # -- TTTTTT -- set tdir here if trgType is set 
    #
    if(len(bb) > 0):
        tdir=tbdir
        nb=-4
        #print 'qqqqqqqqqq',len(tt),tt,len(bb),'bb',bb
        if(dmodelType == 'w2flds' and len(bb) == 3 and len(tt) == 9): nb=-4
        elif(dmodelType == 'w2flds' and (len(bb) == 4 and len(tt) == 10)): nb=-5
        elif(dmodelType == 'w2flds' and (len(bb) == 3 and len(tt) == 10)): nb=-5
        
        if(dmodelType == 'nwp2' and len(bb) >= 3): nb=-3

        #print 'qqqqq',nb
        for t in tt[nb:]:
            tdir="%s/%s"%(tdir,t)
        

    
    # -- reverse if cleaning local...
    #
    localTdir=tdir
    if((reverse or (doClean or doCleanLocal) or thinTaus > 0) and trgType == None):
        ss=sdir
        tt=tdir
        tdir=ss
        sdir=tt
        
    bdir2=None
    if(doCleanDat0 or srcType != None): bdir2=sbdir
    card=w2.getL2ModelStatus(model,l2opt,dtg,bdir2=bdir2,override=override,verb=verb)
    if(verb):
        print 'bbb',bdir2
        print 'ccc',card
 

    # -- do rsync and then thin...
    #
    testRsync=(doRsync or (doClean and not(doCleanLocal) and not(doCleanTarget)))
 
    sdirThere=MF.ChkDir(sdir, diropt='quiet')
    tdirThere=MF.ChkDir(tdir, diropt='quiet')
    ldirThere=MF.ChkDir(localTdir, diropt='quiet')
         
    if(verb):
        print 'ttt: ',testRsync
        print 'SSS: ',sdir,sdirThere
        print 'TTT: ',tdir,tdirThere
        print 'LLL: ',localTdir,ldirThere
        
    dat0There=0
    if(doCleanDat0):
        if(not(mf.find(card,'N-'))): dat0There=1
    else:
        iok=0
        mkTest=( (mf.find(card,'N-') and not(doLs) and ropt != 'norun') or
                 (testRsync and sdirThere and ropt != 'norun') )
        if(mkTest and not(doCleanLocal)): iok=1
        if(iok):  
            MF.ChkDir(tdir,'mk')	
    

 
    if(testRsync):
        
        if(ropt != 'norun'): MF.sTimer("rsync-%s-%s"%(model,dtg))
        
        didRsync=1
        if(hwrfTaus):
            for htau in reducedTaus:
                cmd='''rsync %s "%s/*f%03d*grb*" %s/'''%(rsopt,sdir,htau,tdir)
                mf.runcmd(cmd,ropt)
        else:
            if(sdirThere):
                # -- use runcmd2 to make sure it worked
                #
                cmd='rsync %s %s/ %s/'%(rsopt,sdir,tdir)
                rc=mf.runcmd2(cmd,ropt,ostdout=0)

                if(ropt != 'norun'): MF.dTimer("rsync-%s-%s"%(model,dtg))
                if(rc != 1 and ropt != 'norun'):
                    print 'EEEEEEEE--getRsyncCmd: ',cmd,' failed!!!  set didRsync=0'
                    didRsync=0
            else:
                print 'WWW-------sdir : ',sdir,' not there...no rsync...'
                didRsync=0

        if(doRsync and not(doCleanTarget)): return(None)
        
    if(doClean or doCleanLocal):
        if(testRsync and didRsync == 0):
            print 'WWW---testRsync: ',testRsync,' but no data...do NOT do the rm -r...'
            cmd=None
        elif(not(ldirThere)):
            print 'LLL---localTdir not there...no rm -r'
            cmd=None
        elif(testRsync):
            cmd='rm -r %s/'%(localTdir)
        else:
            print 'EEE clean failed because testRsync: ',testRsync,' before rm -r %s/...'%(localTdir)
            cmd=None
        
    elif(doCleanDat0):
        if(dat0There):
            cmd='rm -r %s/'%(sdir)
        else:
            print 'DDDAAATTT000:',sdir,' not there...return None'
            cmd=None
            
    elif(doCleanTarget):
        if(sdirThere):
            cmd='rm -r %s/'%(sdir)
        else:
            if(verb): print 'DDDSSSSSS:',sdir,' to doCleanTarget -- not there...return None'
            cmd=None
        
    elif(doLs):
        if(reverse):
            bdir2=srcUrl['dat0']
            card=w2.getL2ModelStatus(model,l2opt,dtg,bdir2=bdir2,override=override,verb=verb)
            print 'RRR: ',card
            return(None)
        else:
            if(bdir2 != None):
                print card
                return(None)
            else:
                cmd='%s/l2.py %s %s %s'%(prcdir,dtg,model,l2opt)
            
            
    elif(thinTaus > 0):

        prcdir=w2.PrcDirFlddatW2

        # -- thin
        #
        grbs=glob.glob("%s/*grb*"%(localTdir))
        for grb in grbs:
            tau=grb.split('.')[-2][1:]
            tau=int(tau)
            if(tau > thinTaus):
                cmd="rm %s"%(grb)
                mf.runcmd(cmd,ropt)
        cmd='%s/l2.py %s %s %s -l'%(prcdir,dtg,model,l2opt)
        
    else:
        cmd='rsync %s %s/ %s/'%(rsopt,sdir,tdir)
        
    return(cmd)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class w2CmdLine(CmdLine):

    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            2:['modopt',    'models mm1,mm2,mm3...'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'override':             ['O',0,1,'override for models'],
            'ropt':                 ['N','','norun',' norun is norun'],
            'nhback':               ['b:',0,'i','N hours back...'],
            'srcType':              ['s:',None,'a','source type: dat0|kishou(vpn)|hwrf...'],
            'stmopt':               ['S:',None,'a',' for srcType=hwrf...go for this storm NNB ...'],
            'donwp2':               ['2',0,1,'do nwp2'],
            'doClean':              ['k',0,1,'rsync to dat0 and clean off on local hd'],
            'doCleanDat0':          ['K',0,1,'clean off on dat0'],
            'doCleanLocal':         ['C',0,1,'ONLY clean local hd'],
            'reverse':              ['r',0,1,'reverse tdir -> sdir'],
            'doLs':                 ['l',0,1,'list local files'],
            'thinTaus':             ['T:',-999,'i','thin taus > thinTaus'],
            'hwrfTaus':             ['H',0,1,'pull in only HWRF taus 0.126.6'],
            'doMove':               ['M:',None,'a','move to srcType: dat0,dat3'],
            'doRsync':              ['R',0,1,'rsync firsts, if thinTaus > 0...'],
        }

        self.purpose='''
rsync w2flds from source to local targe
(c) 2009-%s Michael Fiorino, CIRES@ESRL.NOAA'''%(w2.curyear)

        self.examples='''
%s cur12-12 gfs2,ecm4   # default is to d w2fields -2 flag changes to nwp2'''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.sTimer('all')

idtgopt=dtgopt
dtgs=mf.dtg_dtgopt_prc(dtgopt)

prcdir=os.getenv('W2_PRC_DIR')
if(prcdir == None): print 'bad env var' ; sys.exit()

models=modopt.split(',')

# -- MMMMMMMMMMMMOOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLSSSSSSSSSSSSSSS
#
dmodelType='w2flds'
if(donwp2): dmodelType='nwp2'

# -- cleaning dat0 or cleaning tenki7-Mike2
#
if(doCleanDat0 or doClean):
    srcType='dat0'
    
if(hwrfTaus):
    doRsync=1

# -- move from local to dat0|dat3 or dat3-dat0 ...
#
trgType=None
doCleanTarget=0

if(doMove != None):
    dd=doMove.split('-')
    if(len(dd) == 2):
        srcType=dd[0]
        trgType=dd[1]
        doRsync=1
        doCleanTarget=1
    else:
        if(doMove in srcTypes2Move):
            srcType=doMove
            reverse=1
            doClean=1
        else:
            print 'EEE---w2-nwp2-w2flds-rsync2local.py -- trying to move to an invalid srcType: ',doMove
            sys.exit()
    
MF.sTimer('all')
for dtg in dtgs:
    
    if(modopt == 'all' and dmodelType == 'w2flds'):
        if(MF.is0012Z(dtg)):
            models=w2.Nwp2ModelsActW20012
        elif(MF.is0618Z(dtg)):
            models=w2.Nwp2ModelsActW20618

    for model in models:
        if(model in modelsW2): dmodelType='w2flds'
        if(model in modelsNwp2): dmodelType='nwp2'
        cmd=getRsyncCmd(model,dtg,dmodelType,srcType=srcType,trgType=trgType,
                        reverse=reverse,
                        stmopt=stmopt,
                        doClean=doClean,doCleanDat0=doCleanDat0,
                        doCleanLocal=doCleanLocal,doCleanTarget=doCleanTarget,
                        doLs=doLs,thinTaus=thinTaus,
                        doRsync=doRsync,
                        hwrfTaus=hwrfTaus,
                        ropt=ropt,
                        verb=verb,
                        )
        if(cmd != None):
            if(not(doLs)): MF.sTimer('rsync2local-%s-%s-%s'%(dmodelType,model,dtg))
            qopt=''
            if(doLs): qopt='q'
            if(cmd != None): MF.runcmd(cmd,ropt,lsopt=qopt)
            if(not(doLs)): MF.dTimer('rsync2local-%s-%s-%s'%(dmodelType,model,dtg))
            
MF.dTimer('all')

