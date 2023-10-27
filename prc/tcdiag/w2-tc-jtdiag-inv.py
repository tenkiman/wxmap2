#!/usr/bin/env python

from TCdiag import *  # imports tcbase

from M2 import setModel2

if(w2.onKaze or w2.onTenki or w2.onGmu):
    tbdir='%s/tcdiag'%(w2.HfipProducts)
    tbdir='%s/jtdiag'%(w2.HfipProducts)
    jtdir='%s/jtdiag'%(w2.HfipProducts)
else:
    tbdir='/w21/dat/tc/tcdiag'
    tbdir='/w21/dat/tc/jtdiag'
    tbdir='/w21/web/jtdiag'
    jtdir='/w21/web/jtdiag'


prcdir=w2.PrcDirTcdiagW2

def makeJsNoLoad(jskey):
    
    jsno="""dtgStmDict['%s'] = [
[],
[], 
]
"""%(jskey)
    return(jsno)

def makeJsNoLoadTrk(jskey):
    
    jsno="""dtgStmTrkDict['%s'] = [   '', ]
"""%(jskey)
    return(jsno)

allModelsJtdiag=jtdiagModels  # -- set in TCdiag.py

getVars=['precip','shr_mag','max_wind','sst','200dvrg','tpw','850vort']
getStmVars=['shr_mag','max_wind','sst','200dvrg','tpw','850vort']
getCusVars=['precip']


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
            1:['dtgopt',    'run dtgs'],
            2:['modelopt',  'model|model1,model2|alljt'],
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
jsAllTrkStmidsDtgs={}
jsAllProds=[]

for dtg in dtgs:

    MF.sTimer('tcdiag-anl-%s'%(dtg))

    models=modelsDiag[dtg]
    
    if(modelopt == 'alljt'):
        models=allModelsJtdiag  # -- use the list from above

    for model in models:

        if(MF.is0618Z(dtg)): phrOpt='p06'
        if(MF.is0012Z(dtg)):
            phrOpt='p06'
            if(model == 'ecm4' or model == 'ecm5' or model == 'ukm2' or model == 'fv3g'): phrOpt='p12'
            
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
            
            trkpath="%s/trkplt.%s.%s.png"%(tGa.pngdir,ostmid,model)
            if(MF.getPathSiz(trkpath) > 0):
                (trkdir,trkfile)=os.path.split(trkpath)
                urltrkpath="%s/%s/%s"%(dtg[0:4],dtg,trkfile)
                #print 'TTT - there: ',urltrkpath
            else:
                urltrkpath=''
                #print 'III - no trkapth: ',trkpath
                
            
            jskeytrk="%s-%s-%s"%(model,ostmid,dtg)
            #print 'TTT ',jskeytrk
            
            jstrk="""dtgStmTrkDict['%s'] =[  '%s' , ]
"""%(jskeytrk,urltrkpath)
            
            jsAllTrkStmidsDtgs[jskeytrk]=jstrk

            #tGa.lsDiag(ostmid,lsdiagpath=olsdiagPaths[ostmid])
            if(verb): print 'SSSSS: ',ostmid,olsdiagPaths[ostmid]
            tGa.parseDiag(ostmid,lsdiagpath=olsdiagPaths[ostmid])
            (allprods,js)=tGa.makeJsInv(getStmVars,getCusVars,phr=phrOpt,stmid=ostmid)
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
'cgd2': 'cmc GDPS',
'ecm4': 'ecmwf HRES',
'ecm5': 'ecmwf HRES',
'jgsm': 'JMA GSM',
'ukm2': 'ukmo UM',
'fv3g': 'esrl FV3-GF',
'navg': 'fnmoc NAVGEM',
}

jsmod="""
var allModels = [
"""

# -- use the model list and labels here vice from parsing the inventory
#
for model in allModelsJtdiag:
    jsmod=jsmod+""" '%s',
"""%(model)
    
jsmod=jsmod+"""]

var modelLabels = [
"""

for model in allModelsJtdiag:
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

    try:
        jstest=jsAllStmidsDtgs[dtg]
    except:
        print 'WWW-JJJ-ALLDTGS ... no js for dtg: ',dtg,' press...'
        continue
    
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


modelModel2Button['cgd2']='CMC'
modelButton2Model['CMC']='cgd2'

modelModel2Button['fv3g']='FV3G'
modelButton2Model['FV3G']='fv3g'

modelModel2Button['ecm5']='ECM'
modelButton2Model['ECM']='ecm5'
"""

jsstmdtgs="""

allStmDtgDict=new Array()

allStmDtgDict = {
"""

for dtg in jsAllDtgs:
    jscard="""'%s':[
"""%(dtg)
    
    try:
        jstest=jsAllStmidsDtgs[dtg]
    except:
        continue
    
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
"""
for gvar in getVars:
    jsvar=jsvar+ """  '%s',
"""%(gvar)
    
jsvar=jsvar+"""
]
var prodProd2Button = new Array()
var prodButton2Prod = new Array()

prodProd2Button['precip']='SLP'
prodProd2Button['max_wind']='Vmax'
prodProd2Button['precip']='SLP'
prodProd2Button['shr_mag']='VWS'
prodProd2Button['200dvrg']='D200'
prodProd2Button['sst']='SST'
prodProd2Button['tpw']='TPW'
prodProd2Button['850vort']='VRT8'

prodButton2Prod['SLP']='precip'
prodButton2Prod['Vmax']='max_wind'
prodButton2Prod['SLP']='precip'
prodButton2Prod['VWS']='shr_mag'
prodButton2Prod['D200']='200dvrg'
prodButton2Prod['SST']='sst'
prodButton2Prod['TPW']='tpw'
prodButton2Prod['VRT8']='850vort'

"""

# -- trk plots
#
jssdv="""
dtgStmTrkDict = new Array()

"""

for jsdtg in jsAllDtgs:
    try:
        jstest=jsAllStmidsDtgs[jsdtg]
    except:
        continue
    
    for jsstm in jsAllStmidsDtgs[jsdtg]:
        for jsmodel in jsAllModels: 
            jskey="%s-%s-%s"%(jsmodel,jsstm,jsdtg)
            if(verb): print 'TTT---',jskey
            try:
                js=jsAllTrkStmidsDtgs[jskey]
            except:
                jsAllTrkStmidsDtgs[jskey]=makeJsNoLoadTrk(jskey)
                
            js=jsAllTrkStmidsDtgs[jskey]
            jssdv=jssdv+js


# -- stm,dtg,prod taus,vals
#
jssdv=jssdv+"""
dtgStmDict = new Array()

"""
for jsdtg in jsAllDtgs: 


    try:
        jstest=jsAllStmidsDtgs[jsdtg]
    except:
        continue

    for jsstm in jsAllStmidsDtgs[jsdtg]:
        for jsmodel in jsAllModels: 
            for jsprod in jsAllProds:
                jskey="%s-%s-%s-%s"%(jsmodel,jsstm,jsdtg,jsprod)
                try:
                    js=jsAll[jskey]
                except:
                    jsAll[jskey]=makeJsNoLoad(jskey)
                    js=jsAll[jskey]
                    
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

# -- 20200317 -- now rsync to wxmap2
#
if(not(dols)):
    rc=rsync2Wxmap2('jtdiag')

MF.dTimer(tag='all')
