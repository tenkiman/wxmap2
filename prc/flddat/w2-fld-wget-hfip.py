#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

hModels=['hwrf','fv7e','fv7g']

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
            2:['model',     'model: hwrf|fv7g|fv7e'],
        }

        self.options={
            'verb':                 ['V',0,1,'verbose'],
            'doTar':                ['T',1,0,'do tarball since dir scan for web server disabled on 20190903'],
            'override':             ['O',0,1,'1 - '],
            'ropt':                 ['N','','norun','ropt'],
        }


        self.purpose='''pull %s fields on $W2_HFIP
(c) 1992-%s Michael Fiorino,NOAA ESRL CIRES'''%(str(hModels),w2.curyear)

        self.examples='''
%s 2019030912 hwrf'''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

if(not(model in hModels)):
    print 'EEE model: ',model,' not a valid hfip-w2flds...!= ',hModels
    sys.exit()
    
    
sbDir='https://ruc.noaa.gov/hfip/w21/dat/nwp2/w2flds/dat/%s'%(model)
tbDir="%s/w2flds/dat/%s"%(w2.Nwp2DataBdir,model)

for dtg in dtgs:

    tdir="%s/%s"%(tbDir,dtg)
    sdir="%s/%s"%(sbDir,dtg)
    
    if(ropt != 'norun'):
        MF.ChkDir(tdir, 'mk')
    else:
        print 'target Dir: ',tdir
    
    gotDown=0
    gotDone=0
        
    source='%s/'%(sdir)
    if(doTar and (model == 'hwrf' or model == 'fv7g' or model == 'fv7e')):
        MF.ChangeDir(tbDir)
        sourceFile="%s-%s.tgz"%(model,dtg)
        source="%s/%s"%(sbDir,sourceFile)
        logThere=glob.glob("log-%s-%s*"%(model,dtg))
        isThere=len(logThere)
        if(isThere): gotDown=gotDone=1
        
    else:
        MF.ChangeDir(tdir)
        
    if(not(isThere)):
        
        cmd='time wget -nd -m -nH -np %s'%(source)
        runlog=MF.runcmdLog(cmd, ropt)
    
        for r in runlog:
            if(mf.find(r,'Downloaded')): gotDown=1
            if(mf.find(r,'no newer than local')): gotDone=1
    
    logTime=mf.dtg('dtg_hms')
    print 'Down: ',gotDown,' Done: ',gotDone
    
    if(gotDown or gotDone and not(isThere)):
        logDone='log-%s-%s-done-%s.txt'%(model,dtg,logTime)
        print 'LLL: ',logDone
        cmd="touch %s"%(logDone)
        mf.runcmd(cmd,ropt)
        isThere=1
        
    # -- untar and del
    #
    if(isThere and doTar):
        cmd="tar -xzvf %s"%(sourceFile)
        mf.runcmd(cmd,ropt)
        
        cmd="rm %s"%(sourceFile)
        mf.runcmd(cmd,ropt)
        
    