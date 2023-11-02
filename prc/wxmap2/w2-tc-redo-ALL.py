#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcbase import *

modelsW20012=w2.Nwp2ModelsActW20012
modelsW20618=w2.Nwp2ModelsActW20618


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
            'forceOverride':       ['F',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','norun','norun','must use -X to run'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            'doTCs':               ['t',1,0,'do NOT do the TC tracker'],
            'modOpt':              ['m:',None,'a','model opt'],
            'bypassRunChk':        ['y',0,1,'bypassRunChk in lsdiag...'],
            
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

prcdirTD=w2.PrcDirTcdiagW2
prcdirTT=w2.PrcDirTctrkW2
prcdirTG=w2.PrcDirTcgenW2

cmdTT="w2-tc-runTrks.py"
cmdTD="w2-tc-lsdiag.py"
cmdTG="w2-tc-tcgen2.py"

tcddir="%s/tcdiagDAT"%(w2.HfipWebBdir)  # rsync'd from tcdiag/2020 -> tcdiagDAT/2020
#tcddir="%s/tcdiag"%(w2.W2BaseDirWebConfig)
tctdir="%s"%(w2.TcDatDirTMtrkN)

if(doIt): ropt=''

models=['ecm5']
if(modOpt != None):
    models=modOpt.split(',')

maxAgeDtg=10.0

dtgs=mf.dtg_dtgopt_prc(dtgopt)

tD=TcData(dtgopt=dtgopt)
overrideW2=0

for dtg in dtgs:

    ageDtg=mf.dtgdiff(curdtg,dtg)
    ageDtg=-1*ageDtg/24.0
    maxAgeDtg=10.0
    
    oldDtg=mf.dtginc(curdtg,-maxAgeDtg)

    doTCD=doTCG=1
    if(ageDtg > maxAgeDtg):
        doTCD=0
        doTCG=0
        print 'WWWWW----WWWWW this dtg:',dtg,' is older than oldest saved for wxmap2.com: ',oldDtg    
    

    allMissing=0
    
    stmids=tD.getStmidDtg(dtg)
    nstmids=len(stmids)

    if(nstmids > 0):
        print
        print 'SSSTTTMMMMSSSS --dtg: ',dtg,' nstmids: ',nstmids
    else:
        print ''
        print 'NnnnnOooooSTMS --dtg: ',dtg
        print ''
        
    tCTsizMin=257
    w2Status={}

    tCTstatus={}
    tCGstatus={}
    tCDstatus={}
    tcGPlotStatus={}
    
    if(MF.is0012Z(dtg)): 
        tcdModels=modelsW20012
    else:
        tcdModels=modelsW20618
        
    if(modOpt != None):
        tcdModels=models
    
    ntcdModels=0
    for model in tcdModels:
        tCTstatus[model]=0
        tCGstatus[model]=0
        card=w2.getL2ModelStatus(model,'-W',dtg,override=overrideW2,verb=verb)
        ntaus=int(card.split()[4])
        if(ntaus > 0): 
            ntcdModels=ntcdModels+1
            w2Status[model]=1
        else:
            w2Status[model]=0
            

    allMissing=0
    returnAd2=1
    tcA=TcAidTrkAd2Bd2(dtgopt=dtg,verb=verb,quiet=1)
    rcA=tcA.getStatus(modelChk=None, doPrint=0,returnAd2=returnAd2)
    
    if(verb):
        if(returnAd2):
            print ' rcT: ',rcA[0]
            print ' rcG: ',rcA[1]
            try:
                print 'rcTA: ',rcA[2]
            except:
                None
            
            try:
                print 'rcTS: ',rcA[3]
            except:
                None
        
    if(rcA != None): 
        rcT=rcA[0]
        rcG=rcA[1]
        try:
            rcTA=rcA[2]
        except:
            rcTA=None
        try:
            rcTS=rcA[3]
        except:
            rcTS=None
    else:
        if(nstmids > 0):
            print 'WWW -- no rcA for dtg: ',dtg,' AND nstms > 0'
            allMissing=1
        elif(nstmids == 0):
            print 'WWW -- no rcA for dtg: ',dtg,' BECAUSE NO STMS!'
            
        print
            
    if(allMissing):    
        
        for model in tcdModels:
            tCTstatus[model]=0
            tCDstatus[model]=0
            tCGstatus[model]=0
            tcGPlotStatus[model]=0
            
    elif(forceOverride):

        tCTstatus[model]=0
        tCDstatus[model]=0
        tCGstatus[model]=0
        tcGPlotStatus[model]=0
            
    elif(allMissing == -1):

        for model in tcdModels:
            tCTstatus[model]=-1
            tCDstatus[model]=-1
            tCGstatus[model]=-1
            tcGPlotStatus[model]=-1
        
    else:

        modtcd={}
        if(rcT == -1 or len(rcT) == 0):
            doTCD=0
            for model in tcdModels:
                tCTstatus[model]=-1

        else:

            # -- scan tmtrkN tracker files for individual storms
            #
            for r in rcT:
                tt=r[0]
                stms=r[1]
                rmodel=tt.split()[0]
                rnstms=len(stms)
                if(nstmids > 0): 
                    tCTstatus[rmodel]=1
             
            # -- scan tmtrkN total tracker file to detect if ran but had 0 length output
            #
            if(rcTA != None):
                for r in rcTA:
                    model=r[0].split()[0]
                    rcAm=tcA.getStatus(modelChk=model, doPrint=0,returnAd2=3,verb=0)
                    # -- 20230916 -- case of no trackers
                    #
                    if(rcAm == 2):
                        #stmSiz=modtctTrk[model]
                        #rcS=getStmSiz(stmSiz)
                        tCTstatus[model]=-1
                        # -- set the stmids in modtcd to stmid.siz list
                        #
                        #if(rcS[0] == -2):
                        #    modtcd[model]=rcS[1]
                        modtcd[model]=-1
                    
                    else:
                        (modtctGen,modtctTrk,modtctTrkStdout,modtctAllTrk)=rcAm
                        stmSiz=modtctTrk[model]
                        rcS=getStmSiz(stmSiz)
                        tCTstatus[model]=rcS[0]
                        # -- set the stmids in modtcd to stmid.siz list
                        #
                        if(rcS[0] == -2):
                            modtcd[model]=rcS[1]
                    
                    
                    #siz=r[1][0].split('.')[-1]
                    #siz=int(siz)
                    #print 'qqq',model,siz
                    #if(nstmids > 0):
                        #if(siz > tCTsizMin):
                            #tCTstatus[model]=1
                        #else:
                            #tCTstatus[model]=-2
                        
        # -- tcgen
        #
        if(rcG != None):
            
            for r in rcG:
                tt=r[0]
                stms=r[1]
                rmodel=tt.split()[0]
                rnstms=len(stms)
                tCGstatus[rmodel]=1
            
        
        # -- scan tcdiag output -- even if no tmtrkN, could use mftrkN
        #
        year=dtg[0:4]
        dmask='%s/%s/%s/DIAGFILES/tcdiag.*.txt'%(tcddir,year,dtg)
        tcdfiles=glob.glob(dmask)
        
        ntcdfiles=len(tcdfiles)
        for tcdfile in tcdfiles:
            (ddir,dfile)=os.path.split(tcdfile)
            tt=dfile.split('.')
            model=tt[1]
            tracker=tt[-2].split('-')[-1][0:2]
            stmid="%s.%s-%s"%(tt[-4],tt[-3],tracker)
            if(verb): print 'ttccddd--',model,stmid,tCTstatus[model]
            MF.appendDictList(modtcd, model, stmid)
    
    
    # -- now check if gtc actually ran and made plots
    #
    year=dtg[0:4]
    w2tcgenDATDir="%s/tcgenDAT/%s"%(w2.HfipWebBdir,year)  # non-real time
    #w2tcgenDATDir="%s/tcgen/%s"%(w2.W2BaseDirWebConfig,year)  #  real-time < 10 day from curdtg
    
    for model in tcdModels:
        if(doTCG):
            tcGPlotStatus[model]=9
        else:
            tcGPlotStatus[model]=0
            
        gmask='%s/%s/*%s*.120.wpac.*prp.fcst.*'%(w2tcgenDATDir,dtg,model) 
        # -- 20220721 -- tmp because of grib2 coding bug in navgem precip
        gmask='%s/%s/*%s*.120.wpac.*uas.fcst.*'%(w2tcgenDATDir,dtg,model) 
        if(verb): print 'III-%s tcG mask: %s'%(pyfile,gmask)
        tcgfiles=glob.glob(gmask)
        if(len(tcgfiles) > 0):
            tcGPlotStatus[model]=1
            
        if(MF.is0618Z(dtg)): tcGPlotStatus[model]=-1


    redoPrcs={}
    
    for model in tcdModels:
        try:
            stms=modtcd[model]
            nstms=len(stms)
        except:
            nstms=0
            
        if(nstms > 0):
            tCDstatus[model]=1
        else:
            #print 'ddd',model,doTCD,tCTstatus[model]
            if(doTCD and (tCTstatus[model] == 1) ):
                tCDstatus[model]=0
            else:
                tCDstatus[model]=-1
                

        if(model == 'ecmt'):
            tCDstatus[model]=-1
            tCGstatus[model]=-1
            tcGPlotStatus[model]=-1
            
        postStr=''
        if(tCTstatus[model] == -2): postStr='NOOOLOOOAD'
        print 'model: ',model,'W2: ',w2Status[model],' TCT: %2d'%(tCTstatus[model]),\
              ' TCG: %2d'%(tCGstatus[model]),\
              ' TCD: %2d'%(tCDstatus[model]),\
              ' TCG(plot): %2d %s'%(tcGPlotStatus[model],postStr)

    print
    
    # -- reruns
    #
    for model in tcdModels:

        # -- rerun TC
        #
        if(w2Status[model] == 1 and (tCTstatus[model] == 0 or (tCTstatus[model] == -1 and nstmids > 0) ) ):
            # -- override always
            #
            overOptTT='-O'
            cmd="%s/%s %s %s %s"%(prcdirTT,cmdTT,dtg,model,overOptTT)
            mf.runcmd(cmd,ropt)
            
            # -- if tcTrack = 0 then need to override TD
            #
            overOptTD='-O'
            cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,overOptTD)
            mf.runcmd(cmd,ropt)

            if(MF.is0012Z(dtg)):
                overOptTG='-O'
                cmd="%s/%s %s %s %s"%(prcdirTG,cmdTG,dtg,model,overOptTG)
                mf.runcmd(cmd,ropt)
             
        if(w2Status[model] == 1 and tCDstatus[model] == 0 and tCTstatus[model] == 1 and model != 'ecmt'):
            
            # -- always override
            #
            overOpt='-O'
            if(override): overOpt='-O'
            # -- the default in lsdiag is to BYPASS run check
            #
            #if(bypassRunChk): overOpt="%s -y"%(overOpt)
            cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,overOpt)
            mf.runcmd(cmd,ropt)
            #print 'RRR',model,' TT: ',cmdTT,' DD: ',cmdTD,' GG: ',cmdTG
            
            # -- also do track plot
            #
            trkOpt='-l -o test-trkplot'
            cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,trkOpt)
            mf.runcmd(cmd,ropt)
        
        if(w2Status[model] == 1 and 
           tCTstatus[model] == 1 and
           (tcGPlotStatus[model] == 0 or tcGPlotStatus[model] == 9) and 
           ##tCTstatus[model] == 1 and 
           model != 'ecmt' and
           MF.is0012Z(dtg)
           ):
            
            overOpt=''
            if(override or tcGPlotStatus[model] == 9): overOpt='-O'
            cmd="%s/%s %s %s %s"%(prcdirTG,cmdTG,dtg,model,overOpt)
            mf.runcmd(cmd,ropt)
            
print   
            
        
    