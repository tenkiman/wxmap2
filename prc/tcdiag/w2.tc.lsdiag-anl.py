#!/usr/bin/env python

from TCdiag import *  # imports tcbase

from M2 import setModel2

# -- top level vars
#
tbdir=w2.TcTcanalDatDir

if(w2.onKaze):
    tbdir='%s/tcdiag'%(w2.HfipProducts)
    tbdir='%s/jtdiag'%(w2.HfipProducts)
else:
    tbdir='/w21/dat/tc/tcdiag'
    tbdir='/w21/dat/tc/jtdiag'
    
jtdir='/w21/web/jtdiag'
prcdir='/w21/src-SAV/tcdiag'
prcdir='/w21/src/tcdiag'
prcdir=w2.PrcDirTcdiagW2
prcdirIships="%s/tclgem"%(w2.SrcBdirW2)


def makeJsNoLoad(jskey):
    
    jsno="""dtgStmDict['%s'] = [
[],
[], 
]
"""%(jskey)
    return(jsno)


class MyCmdLine(CmdLine):

    # -- set up here to put in an object
    #

    btau06=0
    etau06=48
    dtau06=6

    btau12=etau06+12
    etau12=168
    dtau12=12

    ttaus=range(btau06,etau06+1,dtau06)+range(btau12,etau12+1,dtau12)

    gaopt='-g 1024x768'

    def __init__(self,argv=sys.argv):



        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model|model1,model2|all|allgen'],
        }

        self.defaults={
            'doupdate':0,
            'doga':1,
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'TDoverride':       ['o:',None,'a','TDoverride invokes tests in lsDiagProc(): test-trkplot | test-htmlonly | test-plot-html'],
            'SSToverride':      ['z',0,1,'override just making oisst -- for old cases when grid changed'],
            'redoLsdiag':       ['R',0,1,'override just running the '],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'iVunlink':         ['v',0,1,'unlink invHash pypdb'],
            'quiet':            ['q',1,0,' turn OFF running GA in quiet mode'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doTcFlds':         ['F',0,1,'''doTcFlds -- make f77 input files for lsdiags.x only'''],
            'dowindow':         ['w',0,1,'1 - dowindow in GA.setGA()'],
            'doLgemOnly':       ['G',0,1,'doLgemOnly'],
            'dowebserver':      ['W',1,0,'do NOT 1 - dowebserver=1 write to webserver for plotonly '],
            'doxv':             ['X',0,1,'1 - xv the plot'],
            'doplot':           ['P',1,0,'0 - do NOT make diag plots'],
            'domandonly':       ['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':       ['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'getpYp':           ['Y',0,1,'1 - get from pyp'],
            'doclean':          ['k',0,1,'clean off files < dtgopt'],
            'docleanDpaths':    ['K',0,1,'clean off dpaths < dtgopt'],
            'dohtmlvars':       ['H',0,1,'do html for individual models'],
            'dothin':           ['t',0,1,'dothin -- reduce # of taus .dat files to reduce storage'],
            'lsInv':            ['i',0,1,'do html for individual models'],
            'doInv':            ['I',0,1,'do html for individual models'],
            'dols':             ['l',0,1,'do ls of TCs...'],
            'ndayback':         ['n:',25,'i','ndays back to do inventory from current dtg...'],
            'invtag':           ['g:',None,'a','tag to put on inventory file'],
            'zoomfact':         ['Z:',None,'a','zoomfact'],
            'dtype':            ['d:','w2flds','a','default source of fields'],
            'doall':            ['A',0,1,'do all processing for a dtg'],
            'doDiagOnly':       ['D',0,1,'do only diagfile processing'],
            'trkSource':        ['M:','mftrkN','a','tm|mftrk for trkSource'],
            'dotrkSource':      ['r',0,1,'run tracker to get track...'],
            'TRKoverride':      ['e',0,1,'set override=1 when running tracker to get track using -r option...'],
            'bypassRunChk':     ['y',0,1,'bypassRunChk track...'],
            'bmoverride':       ['B',1,0,'do NOT regen the basemaps'],
            'selectNN':         ['9',1,0,'default is 1 -- use NN, if 0 use 9X (more operational)'],
            'dobt':             ['b:',1,'i','do NOT use BT or working BT'],

        }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
%s cur-6 gfs2 -l -o test-plot-html  # ls and do plot track
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='all')

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tstmids=None

if(stmopt != None):

    MF.sTimer('gettD')
    tD=TcData(stmopt=stmopt)
    MF.dTimer('gettD')
    
    # -- use mdeck2 to make stmlist
    #
    tstmids=tD.makeStmListMdeck(stmopt,dobt=dobt)
    
    ostmids={}
    
    for tstmid in tstmids:

        dtgs=[]

        BTs=tD.getBT4Stmid(tstmid,dobt=dobt)
        BTs.ls()
        sys.exit()
        
        md2=tD.getDSsStm(tstmid,dobt=dobt)
        
        gendtgs=md2.gendtgs
        if(hasattr(md2,'stmid9x')):
            stmid9x=md2.stmid9x
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid9x,convert9x=1)
            stmid9x=stm1id
        else:
            stmid9x=tstmid
            
        ostmid=[tstmid,stmid9x]
        for gendtg in gendtgs:
            if(MF.is0012Z(gendtg)): dtgs.append(gendtg)

        dtgs=mf.uniq(dtgs)
        ostmids[tstmid]=(ostmid,dtgs)
        

    tstmids=ostmids.keys()
    tstmids.sort()
    
    for tstmid in tstmids:
        (ostmid,dtgs)=ostmids[tstmid]

        for dtg in dtgs:

            (mdtgs,modelsDiag)=getDtgsModels(CL,dtg,modelopt)
            
            for model in modelsDiag[dtg]:

                
                tGa=TcDiagAnl(dtg,model,
                              dols=dols,
                              wdir=tbdir,
                              dobt=dobt,
                              tD=tD,
                              verb=verb)

                tGa.prcdir=prcdir
                tGa.ls('diag')
                (Dtstmids,DlsdiagPaths)=tGa.getLsdiagPathsStmids(model)
                
                lsdiagPath=None
                fstmid=None
                if(ostmid[0] in Dtstmids):
                    fstmid=ostmid[0]
                elif(ostmid[1] in Dtstmids):
                    fstmid=ostmid[1]
                    
                if(fstmid != None):
                    lsdiagPath=DlsdiagPaths[fstmid]
                
                print 'oooooooooooo',Dtstmids,dtg,fstmid,lsdiagPath
                #tGa.lsDiag(ostmid,lsdiagpath=lsdiagPath)
                tGa.parseDiag(ostmid,lsdiagpath=lsdiagPath)
                
                #tGa.ls()
                
                cData=tGa.customData
                cLabels=tGa.customLabels
                
                sData=tGa.stmData
                sLabels=tGa.stmLabels
                
                
                cLndx=cLabels.keys()
                cLndx.sort()
                
                sLndx=sLabels.keys()
                sLndx.sort()
                
                otau=0
                cpsB=cData[otau,11]
                cpsVTl=cData[otau,12]
                cpsVTu=cData[otau,13]
                
                sVmax=sData[otau,3]
                sVTng=sData[otau,14]
                
                
                if(verb):
                    for cL in cLndx:
                        print 'CCC',cL,cLabels[cL],cData[otau,cL]
                
                    for sL in sLndx:
                        print 'SSS',sL,sLabels[sL],sData[otau,sL]
                    
                print 'CPS: ',cpsB,cpsVTl,cpsVTu
                print 'Stm: ',sVmax,sVTng
                #tGa.ls()
                

    sys.exit()
        
    

else:

    (dtgs,modelsDiag)=getDtgsModels(CL,dtgopt,modelopt)

    # -- do TcData topside
    #
    if(ropt != 'norun'):
    
        MF.sTimer('TcData')
        tD=TcData(dtgopt=dtgs[-1])
        MF.dTimer('TcData')
        
        
MF.ChangeDir(prcdir)

# -- by ddddddddddddddddtttttttttttttttttgggggggggggggggggggggssssssssssss
#

jsAll={}
jsAllDtgs=[]
jsAllModels=[]
jsAllStmidsDtgs={}
jsAllProds=[]

for dtg in dtgs:

    MF.sTimer('tcdiag-anl-%s'%(dtg))

    models=modelsDiag[dtg]

    for model in models:

        if(MF.is0618Z(dtg)): phrOpt='p06'
        if(MF.is0012Z(dtg)):
            phrOpt='p06'
            if(model == 'ecm4' or model == 'ukm2' or model == 'fv3g'): phrOpt='p12'
            
        print 'MMMMMMMMMMMM ',model,' DDDDDDDD',dtg,' PPPPPPPPPPP ',phrOpt
        dobail=0
        if(ropt == 'norun'): dobail=0

        tGa=TcDiagAnl(dtg,model,
                  dols=dols,
                  tbdir=tbdir,
                  wdir=tbdir,
                  dobt=dobt,
                  dobail=dobail,
                  tD=tD,
                  verb=verb)

        tGa.prcdir=prcdir
        
        (otstmids,olsdiagPaths)=tGa.getLsdiagPathsStmids(model)
            
        ostmids=olsdiagPaths.keys()
        ostmids.sort()
        
        for ostmid in ostmids:
            #tGa.lsDiag(ostmid,lsdiagpath=olsdiagPaths[ostmid])
            if(verb): print 'SSSSS: ',ostmid,olsdiagPaths[ostmid]
            tGa.parseDiag(ostmid,lsdiagpath=olsdiagPaths[ostmid])
            (allprods,js)=tGa.makeJsInv(phr=phrOpt)
            MF.appendDictList(jsAllStmidsDtgs, dtg, ostmid)
            jsAllProds=jsAllProds + allprods
            
            jskk=js.keys()
            jskk.sort()
            
            for jsk in jskk:
                jsAll[jsk]=js[jsk]
            
        jsAllDtgs.append(dtg)
        jsAllModels.append(model)

    MF.dTimer('tcdiag-anl-%s'%(dtg))
            
            

jsAllDtgs=mf.uniq(jsAllDtgs)
jsAllModels=mf.uniq(jsAllModels)
jsAllProds=mf.uniq(jsAllProds)

# -- reverse order of dtgs
#
jsAllDtgs.reverse()

MF.uniqDictList(jsAllStmidsDtgs)

modelLabels= {
'gfs2': 'ncep GFS',
'fv3g': 'esrl FV3-GF',
'ecm4': 'ecmwf HRES',
'ukm2': 'ukmo UM',
'navg': 'fnmoc NAVGEM',
}

jsmod="""
var allModels = [
"""

for model in jsAllModels:
    jsmod=jsmod+""" '%s',
"""%(model)
    
jsmod=jsmod+"""]

var modelLabels = [
"""

for model in jsAllModels:
    jsmod=jsmod+""" '%s',
"""%(modelLabels[model])
    
jsmod=jsmod+"""]
"""

jstaus="""
allTaus = [	
   '0',
   '6',
  '12',
  '18',
  '24',
  '30',
  '36',
  '42',
  '48',
  '60',
  '72',
  '84',
  '96',
 '108',
 '120',
]
"""

jsdtgs="""
var allDtgs = [
"""

for dtg in jsAllDtgs:
    jsdtgs=jsdtgs+""" '%s',
"""%(dtg)
    
jsdtgs=jsdtgs+"""]

var modelButton2Model = new Array()
var modelModel2Button = new Array()

modelModel2Button['ukm2']='UKM'
modelButton2Model['UKM']='ukm2'

modelModel2Button['navg']='NAVG'
modelButton2Model['NAVG']='navg'

modelModel2Button['gfs2']='GFS'
modelButton2Model['GFS']='gfs2'

modelModel2Button['fv3g']='FV3G'
modelButton2Model['FV3G']='fv3g'

modelModel2Button['ecm4']='ECM'
modelButton2Model['ECM']='ecm4'
"""

jsstmdtgs="""

allStmDtgDict=new Array()

allStmDtgDict = {
"""

for dtg in jsAllDtgs:
    jscard="""'%s':[
"""%(dtg)
    
    for jsstm in jsAllStmidsDtgs[dtg]:
        jscard=jscard+"""'%s',
"""%(jsstm)
        
    jscard=jscard+"""],
"""
    jsstmdtgs=jsstmdtgs+jscard
    
jsstmdtgs=jsstmdtgs+"""
}"""

# -- hard-wire for proper order
#jsvar="""
#for jvar in jsAllProds:
#    jsvar=jsvar+"""
#'%s',"""%(jvar)
#jsvar=jsvar+"""

jsvar="""

var allProds = [
  'max_wind',
  'shr_mag',
  'sst',
  '200dvrg',
]

var prodProd2Button = new Array()
var prodButton2Prod = new Array()

prodProd2Button['max_wind']='Vmax'
prodProd2Button['shr_mag']='VWS'
prodProd2Button['200dvrg']='D200'
prodProd2Button['sst']='SST'

prodButton2Prod['Vmax']='max_wind'
prodButton2Prod['VWS']='shr_mag'
prodButton2Prod['D200']='200dvrg'
prodButton2Prod['SST']='sst'

"""

# -- stm,dtg,prod taus,vals
#
jssdv="""
dtgStmDict = new Array()

"""
for jsdtg in jsAllDtgs: 
    for jsstm in jsAllStmidsDtgs[dtg]:
        for jsmodel in jsAllModels: 
            for jsprod in jsAllProds:
                jskey="%s-%s-%s-%s"%(jsmodel,jsstm,jsdtg,jsprod)
                try:
                    js=jsAll[jskey]
                except:
                    jsAll[jskey]=makeJsNoLoad(jskey)
                    js=jsAll[jskey]
                    
                #print 'jjj',jskey
                #print js
                jssdv=jssdv+js



#print jsmod              
#print jstaus
#print jsdtgs
#print jsstmdtgs
#print jsvar
#print jssdv

jsall=jsmod+jstaus+jsdtgs+jsstmdtgs+jsvar+jssdv

if(verb): print jsall

invpath="%s/inv-jtdiag.js"%(jtdir)
MF.WriteString2Path(jsall, invpath)

MF.dTimer(tag='all')
