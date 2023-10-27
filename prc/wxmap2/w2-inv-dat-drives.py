#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
from M import MFutils
MF=MFutils()
import mf

from M2 import setModel2

modelsW2=['gfs2','cgd2','navg','ecmt','ecm5','jgsm']
modelsNwp2=['goes']
modelsAll=modelsW2+modelsNwp2

modelsW20012=modelsW2
modelsW20618=['gfs2','jgsm']

datDirs={
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
}

nfldsMinMax={
'gfs2':(68,71),
'goes':(4,64),
'ecm5':(8,8),
'cgd2':(40,69),
'ecmt':(1,86),
'ecm5':(3,9),
'jgsm':(3,6),
'navg':(51,72),
}

def makeTFlabels(falseDtgs,ltype='false',verb=0):
    
    fBdtgs=falseDtgs.keys()
    fBdtgs.sort()
    
    fRlabels={}

    if(verb):
        if(ltype == 'false'):
            print 'fff',fBdtgs
        else:
            print 'ttt',fBdtgs
        
    flabels=[]

    for fbdtg in fBdtgs:
        fdtgs=falseDtgs[fbdtg]
        f0dtg=fdtgs[0]
        f1dtg=fdtgs[-1]
        if(len(fdtgs) == 1):
            flab=f0dtg
        else:
            flab="%s-%s"%(f0dtg,f1dtg)
        fRlabels[f0dtg]=flab

        if(verb):
            if(ltype == 'false'):
                print 'FFF',flab
            else:
                print 'TTT',flab
                
    return(fRlabels)

def lsZipFile(zipPath,lstype='sum'):
    
    try:
        AZ=zipfile.ZipFile(zipPath)
    except:
        print 'bad zipfile: ',zipPath,' return -1'
        return(-1)

    zls=AZ.namelist()
    adpaths={}
    adAllpaths={}
    
    zls.reverse()
    for zl in zls:
        
        
        if(mf.find(zl,lstype)):
            zc=AZ.open(zl).readlines()
        else:
            continue

        print 'ZZZZZ',zl
        for z in zc:
            print z[:-1]
        return(1)
        continue
        
        # -- 20211222 -- find the .txt file with all trackers
        #
        if(mf.find(zl,dtg)):
            lzl=len(zl.split('.'))
            if(stype == 'atcf' and lzl == 5 and mf.find(zl,afileMask)):
                zi=AZ.getinfo(zl)
                zt=zi.date_time
                zs=zi.file_size
                zc=AZ.open(zl).readlines()
                zrc=(zs,zt,zc)
                adAllpaths[zl]=zrc
    rc=1
    return(rc)
        

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class w2CmdLine(CmdLine):
    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['datDrive',  'drive to check'],
            2:['modopt',    'models mm1,mm2,mm3...'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'override':             ['O',0,1,'override for models'],
            'doKlean':              ['K',0,1,'rm -r 0 len and incomplete dirs'],
            'doLsOnly':             ['l',0,1,'rm -r 0 len and incomplete dirs'],
            'doLsOnlyLong':         ['L',0,1,'rm -r 0 len and incomplete dirs'],
            'doZip':                ['Z',1,0,'do NOT do zip of output'],
            'ropt':                 ['N','','norun',' norun is norun'],
        }

        self.purpose='''
inventory a USB3 drive in /dat?? 
(c) 2009-%s Michael Fiorino, mfiorino@gmu.edu'''%(w2.curyear)

        self.examples='''
%s dat81 all'''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(modopt == 'all'):
    models=modelsAll
else:
    models=modopt.split(',')

ddatDrive=datDrive
if(datDrive == 'dat2'): ddatDrive='dat2-orig'
datDF=''
cmd="df -h /%s"%(ddatDrive)
rc=mf.runcmd2(cmd,verb=0,lsopt='q')

if(rc[0]):
    datDF=rc[1][-2]
    datDF=datDF[-40:]

datDocDir="%s/doc"%(w2.W2_BDIRDAT)
invSumPath="%s/inv-sum-%s-%s.txt"%(datDocDir,datDrive,curdtg)
invAllPath="%s/inv-all-%s-%s.txt"%(datDocDir,datDrive,curdtg)
zipAllPath="%s/inv-%s.zip"%(datDocDir,datDrive)

lstype='sum'
if(doLsOnlyLong):
    doLsOnly=1
    lstype='all'
    
if(doLsOnly):
    
    rc=lsZipFile(zipAllPath,lstype=lstype)
    
    sys.exit()

ocards=[]
acards=[]
card='AAA--Drive: %s df: %s'%(datDrive,datDF)
if(verb): print card
ocards.append(card)
acards.append(card)

drvSiz=0

for model in models:
    m=setModel2(model)
    if(hasattr(m,'w2fldsSrcDir') and model != 'goes'):
        mbdir=m.w2fldsSrcDir
    else:
        mbdir=m.bddir
        
    try:
        (nfmin,nfmax)=nfldsMinMax[model]
    except:
        print 'EEE no nfmin/max for model: ',model
        sys.exit()
    
    isW2=0
    if(model in modelsW2):
        isW2=1
        mbdir=m.w2fldsSrcDir
        
    try:
        dbdir=datDirs[datDrive]
    except:
        print 'EEE datDrive: ',datDrive,'not in datDirs...sayounara'
        sys.exit()
        
    mdtgInc=m.modelDdtg

    dd=dbdir.split('/')
    mm=mbdir.split('/')
    
    if(isW2):
        sbdir="%s/%s/%s/%s"%(dbdir,mm[-3],mm[-2],mm[-1])
    else:
        sbdir="%s/%s/%s"%(dbdir,mm[-2],mm[-1])
        
    if(model == 'ecm5' or model == 'jgsm'):
        smask="%s/????/??????????"%(sbdir)
    else:
        smask="%s/??????????"%(sbdir)
        
    rc=MF.ChkDir(sbdir)
    if(rc == 0):
        print 'III -- no data on ',datDrive,'for model: ',model
        continue
    
    hasDataDirs=[]
    zeroDataDirs=[]
    allDataDirs={}
    allDataDtgs={}
    
    allSiz=0
    
    ddirs=glob.glob(smask)
    ddirs.sort()
    for ddir in ddirs:
        dfiles=glob.glob("%s/*"%(ddir))
        lfile=len(dfiles)
        if(lfile == 0):
            zeroDataDirs.append(ddir)
        else:
            hasDataDirs.append(ddir)
        (tdir,tdtg)=os.path.split(ddir)
        asiz=MF.GetDirFilesSiz(ddir)
        if(asiz == None): asiz=0
        allDataDirs[ddir]=lfile
        allSiz=allSiz+asiz
        allDataDtgs[tdtg]=(ddir,lfile,asiz)

        
    adirs=allDataDirs.keys()
    adirs.sort()
    
    # -- bail if no data
    #
    if(len(adirs) == 0):
        print 'WWW no data in smask: ',smask,' press ...'
        continue

    bdatDir=None
    for adir in adirs:
        if(allDataDirs[adir] != 0 and bdatDir == None): bdatDir=adir
    
    adirs.reverse()
    
    edatDir=None
    for adir in adirs:
        if(allDataDirs[adir] != 0 and edatDir == None): edatDir=adir
        
    
    (bdir,bdtg)=os.path.split(bdatDir)
    (edir,edtg)=os.path.split(edatDir)

    #print 'bbb',bdatDir,bdtg
    #print 'eee',edatDir,edtg

    #ddtgs=allDataDtgs.keys()
    #ddtgs.sort()
    ddtgs=mf.dtgrange(bdtg,edtg,mdtgInc)
    
    trueDtgs={}
    falseDtgs={}
    trueBdtg=None
    falseBdtg=None
    
    for ddtg in ddtgs:
        agebdtg=mf.dtgdiff(bdtg,ddtg)
        ageedtg=mf.dtgdiff(ddtg,edtg)
        try:
            rc=allDataDtgs[ddtg]
        except:
            if(verb): print 'III no data for dtg: ',ddtg
            if(falseBdtg == None):
                falseBdtg=ddtg
                trueBdtg=None
            MF.appendDictList(falseDtgs, falseBdtg, ddtg)
            continue
        
        nfld=rc[-2]
        nsiz=rc[-1]
        nfchk=( (nfld >= nfmin and nfld <= nfmax) )
        if(agebdtg >= 0.0 and ageedtg >= 0.0):
            if(nfchk):
                if(trueBdtg == None): 
                    trueBdtg=ddtg
                    falseBdtg=None
                MF.appendDictList(trueDtgs, trueBdtg, ddtg)
            else:
                if(falseBdtg == None):
                    falseBdtg=ddtg
                    trueBdtg=None
                MF.appendDictList(falseDtgs, falseBdtg, ddtg)

            if(verb): print 'dddd',ddtg,'%6.0f %6.0f %3d'%(agebdtg,ageedtg,nfld),nfchk
                
        if(verb): print 'nnnn',ddtg,'nfld: ',nfld,nfchk,nsiz
            
    tBdtgs=trueDtgs.keys()
    tBdtgs.sort()
    
    fBdtgs=falseDtgs.keys()
    fBdtgs.sort()

    fLabs=makeTFlabels(falseDtgs,ltype='false')
    tLabs=makeTFlabels(trueDtgs,ltype='true')
    
    aLabDtgs=fLabs.keys()+tLabs.keys()
    aLabDtgs.sort()
    
    nTrue=0
    nFalse=0
    aDtgs=[]
    for alab in aLabDtgs:
        try:
            flab=fLabs[alab]
        except:
            flab=None
        try:
            tlab=tLabs[alab]

        except:
            tlab=None
            
        if(tlab != None):
            olab=tlab.replace('-','.')
            if(len(olab) == 10): 
                dtgopt=olab
                olab=tlab
            else:
                dtgopt="%s.%s"%(olab,mdtgInc)
            odtgs=mf.dtg_dtgopt_prc(dtgopt)
            aDtgs=aDtgs+odtgs
            nTrue=nTrue+len(odtgs)
            card='TTT--%s: %4d  %s'%(model,len(odtgs),tlab)
            if(verb): print card
            ocards.append(card)
            
        elif(flab != None):
            olab=flab.replace('-','.')
            if(len(olab) == 10):
                dtgopt=olab
            else:
                dtgopt="%s.%s"%(olab,mdtgInc)
            odtgs=mf.dtg_dtgopt_prc(dtgopt)
            aDtgs=aDtgs+odtgs
            nFalse=nFalse+len(odtgs)
            card='FFF--%s: %4d  %s'%(model,len(odtgs),flab)
            if(verb): print card
            ocards.append(card)


    # -- clean off 0 or incomplete dtgs
    #
    if(doKlean):
        
        fKillDtgs=[]
        fKillDirs=[]
        for kk in fLabs.keys():
            dtgopt=fLabs[kk]
            if(len(dtgopt) != 10):
                dtgopt=dtgopt.replace('-','.')+'.%d'%(mdtgInc)
                
            fKillDtgs=fKillDtgs+mf.dtg_dtgopt_prc(dtgopt)
            
        fKillDtgs.sort()
        
        for fkk in fKillDtgs:
            try:
                kDir=allDataDtgs[fkk][0]
                fKillDirs.append(kDir)
            except:
                kDir=None
            print 'ff',fkk,kDir
            
        kleanAllDirs=zeroDataDirs+fKillDirs
        kleanAllDirs=mf.uniq(kleanAllDirs)
        for kdir in kleanAllDirs:
            cmd="rm -r %s"%(kdir)
            mf.runcmd(cmd,ropt)
        
    aDtgs.sort()
    abdtg=aDtgs[0]
    aedtg=aDtgs[-1]
            
    allGB=(allSiz*1.0/(1024*1024*1024))
    drvSiz=drvSiz+allGB
    allGB="%5.0f"%(allGB)
    allGB=int(allGB)
    rc=mf.PrintCurrency('test',5,allGB,quiet=1)
    tt=rc.split()
    aGB=tt[-1]
    
    #acards.append(' ')
    card='AAA--Model: %s  %s-%s'%(model,abdtg,aedtg)+'  nGood: %4d nBad: %4d'%(nTrue,nFalse)+'  total: %6s GB'%(aGB)
    if(verb): print card
    ocards.append(card)
    acards.append(card)
    ocards.append(' ')
    acards.append(' ')
    
    
drvSiz="%6.0f"%(drvSiz)
drvSiz=int(drvSiz)
rc=mf.PrintCurrency('test',5,drvSiz,quiet=1)
tt=rc.split()
dSiz=tt[-1]
card='AAA--Size:                                                               --------'
if(verb): print card
ocards.append(card)
acards.append(card)
card='AAA--Size:                                                              %6s GB'%(dSiz)
if(verb): print card
ocards.append(card)
acards.append(card)

rc=MF.WriteList2Path(ocards, invAllPath)
rc=MF.WriteList2Path(acards, invSumPath)

for card in acards:
    print card
        
#mf.runcmd('git add %s'%(invAllPath))
#mf.runcmd('git add %s'%(invSumPath))

if(doZip):
    mf.runcmd('zip -u -m %s %s'%(zipAllPath,invAllPath))
    mf.runcmd('zip -u -m %s %s'%(zipAllPath,invSumPath))

sys.exit()
