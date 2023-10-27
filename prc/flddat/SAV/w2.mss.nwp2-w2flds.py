#!/usr/bin/env python

diagmss=0
if(diagmss):
    from M import MFutils
    MFm=MFutils()
    
if(diagmss): MFm.sTimer('load-mss')

from nwp import *
from M2 import setModel2
from FM import rtfimRuns

if(diagmss):
    MFm.dTimer('load-mss')

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            2:['modelopt',  'no default'],
            }

        self.defaults={
            'model':'gfs2',
            }

        self.options={
            'invoverride':   ['I',0,1,'force new inventory of local/mss and set dolsonly=1'],
            'invoverrideL':  ['i',0,1,'force new inventory of local and set dolsonly=1'],
            'invoverrideM':  ['M',0,1,'force new inventory of mss and set dolsonly=1'],

            'dolsonly':      ['l',0,1,'ls on local/mss'],
            'dolsmssonly':   ['m',0,1,'only list mss data'],
            'override':      ['O',0,1,'override'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doKlean':       ['K',1,0,'do NOT clean local'],
            'doRmLocal':     ['r',0,1,'clean off local dir'],
            'doput':         ['P',0,1,'put to mss'],
            'mv2dat5':       ['5',0,1,'move to dat5'],
            'mv2dat6':       ['6',0,1,'move to dat6'],
            'mv2dat7':       ['7',0,1,'move to dat5 to dat6'],
            'doget':         ['G',0,1,'get from mss'],
            'fulltaus':      ['F',0,1,'ls on local/mss'],
            'bdir':          ['b:',None,'a','set bdir dat0: /data/amb... ; dat4: /dat4/'],
            'dojet':         ['J',0,1,'rsync or prestage over to jet; then do mss'],
            'dow2flds':      ['W',0,1,'w2flds vice nwp2'],
            'dortfim':       ['R',0,1,'rtfim vice nwp2'],
            'doremoteRsync': ['y',1,0,'do NOT do rsync of remote mss pypdb'],
            }

        self.purpose='''
purpose -- manage w2flds local and mss
%s cur modelopt '''
        self.examples='''
%s all all-2-jet -W -5 -P -J
%s all all-2-mss'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

MF.sTimer(tag='mss-all')
CL=MssCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#jobopt=None
#killjob=1
#MF.sTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
#rc=MF.chkIfJobIsRunning(pyfile,killjob=killjob,verb=verb,nminWait=1,timesleep=5)
#MF.dTimer('chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))

onLocal=(w2.onKishou or w2.onKaze)
onHpcc=(w2.onWjet or w2.onTheia)

if(w2.onKishou):

    # -- doing dat5/dat6 mv dat6todat5
    #
    mv2dat=(mv2dat5 or mv2dat6 or mv2dat7)

    # -- mv 5 to jet
    if( (dow2flds or dortfim) and mv2dat5 and doput and dojet ):                       bdir='dat5'

    # -- mv 5 to 6 by using -5 -6 -P for -W or -R
    elif((dow2flds or dortfim) and (mv2dat5 and mv2dat6) and bdir == None and doput):  bdir='dat5'

    # -- mv 6 to 5 by using -7 -P for -W or -R
    elif((dow2flds or dortfim) and (mv2dat7) and bdir == None and doput):              bdir='dat6'

    # -- mv dat4 to dat5 or dat6 by using (-5 -P) or (-6 -P)         and -W or -R
    elif((dow2flds or dortfim) and (mv2dat5 or mv2dat6) and bdir == None and doput):   bdir='dat4'
    
    # -- location of w2flds/rtfim fields on kishou
    elif(dow2flds and not(mv2dat) and bdir == None):                                    bdir='dat4'

    # -- location of nwp2 fields on kishou
    #elif(dortfim  and bdir == None and not(mv2dat)):                                    bdir='dat2'
    elif(dortfim  and bdir == None and not(mv2dat)):                                    bdir='datg'
    
    # -- ls dat5
    elif( (dow2flds or dortfim) and mv2dat5 and bdir == None and not(doput)):           bdir='dat5'
    
    # -- ls dat6
    elif(dow2flds and mv2dat6      and bdir == None and not(doput)):                    bdir='dat6'
    elif(dortfim  and mv2dat6      and bdir == None and not(doput)):                    bdir='dat6'
    
    #elif(not(dow2flds) and bdir == None):                                               bdir='dat2'
    #elif(not(dow2flds) and bdir == None):                                               bdir='datg'
    elif(not(dow2flds) and bdir == None):                                               bdir='datr'
    
    else:
        print 'EEE %s unable to set bdir'%(CL.pyfile)
        sys.exit()
    if(doget): dojet=1


elif(onHpcc):
    if(dortfim  and bdir == None):       bdir='datjr'
    if(dow2flds and bdir == None):       bdir='datj2'
    if(not(dow2flds) and bdir == None):  bdir='datj2'

elif(w2.onKaze):
    if(dortfim  and bdir == None):       bdir='dat0'
    if(dow2flds and bdir == None):       bdir='dat0'
    if(not(dow2flds) and bdir == None):  bdir='dat0'

doinv=0
if(invoverride or invoverrideL): invoverrideL=1  ; doinv=1
if(invoverride or invoverrideM): invoverrideM=1  ; doinv=1

if(doinv): MF.sTimer(tag='make n2 with inventory')
if(dow2flds):    
    sdiroptJet='datj2'
    n2=  Nwp2DataW2flds(sdiropt=bdir,overrideL=invoverrideL,overrideM=invoverrideM,verb=verb,doremoteRsync=doremoteRsync,dojet=0)
    if(not(onHpcc)): n2J= Nwp2DataW2flds(sdiropt=sdiroptJet,overrideL=0,overrideM=0,verb=verb,doremoteRsync=0,dojet=1)
elif(dortfim):  
    sdiroptJet='datjr'
    n2=  Nwp2DataRtfim(sdiropt=bdir,overrideL=invoverrideL,overrideM=invoverrideM,verb=verb,doremoteRsync=doremoteRsync,dojet=0)
    if(not(onHpcc)): 
        n2J= Nwp2DataRtfim(sdiropt=sdiroptJet,overrideL=0,overrideM=0,verb=verb,doremoteRsync=0,dojet=1)
else:
    sdiroptJet='datj2'
    n2=  Nwp2Data(sdiropt=bdir,overrideL=invoverrideL,overrideM=invoverrideM,verb=verb,doremoteRsync=doremoteRsync,dojet=0)
    if(not(onHpcc)): n2J= Nwp2Data(sdiropt=sdiroptJet,overrideL=0,overrideM=0,verb=verb,doremoteRsync=0,dojet=1)
    
if(doinv): MF.dTimer(tag='make n2 with inventory')
if(doinv): print "III just doing inventory...bdir: ",bdir ; sys.exit()

if( onLocal and (dojet and not(doget) and not(doput)) ):
    print 'III settting n2 to n2J...'
    n2=n2J

if(not(mf.find(modelopt,'all'))):
    models=modelopt.split(',')
elif(modelopt == 'all-2-jet'):
    models=['gfsc','cgd2','fim8','jmac','ngpj','ocn','ohc','ww3','ukmc']
elif(modelopt == 'all-2-mss'):
    models=[
'ngpc',       
'ecmt',      
#'fimens_g7'
#'navg',      
'fim7',      
'fim8',      
'fim9',      
'fim9h',     
'ngpj',      
'ohc',       
'fimens',    
'fim7h',     
#'gfsenkf_t25',
'gfsk',      
#'gfs2',      
#'ecm4',      
#'ecm2',      
'ukmc',     
#'cmc2',      
#'fim7xh',    
'ww3',       
'fimx',      
'fim8h',     
'ngp2',      
'cgd6',      
'cgd2',      
#'ukm2',      
'ocn',      
'jmac',      
'ecmn',      
'ecmg',      
'gfsc',      
'rtfim9',    
]        
else:
    models=n2.allmodels
    if(onLocal and hasattr(n2,'allmodelsLocal')): models=n2.allmodelsLocal
    
ntot=0
for model in models:

    rmodel=None
    if(type(model) is ListType): model=model[1]
    if(not(dortfim)):
        m=setModel2(model)
        if(m != None and hasattr(m,'rundtginc')): rundtginc=m.rundtginc
        pmodel=model
        rmodel=model
    else:
        rundtginc=6
        fr=rtfimRuns()
        fimrun=fr.getRmodel(model)
        if(fimrun == None):
            print 'EEE could not find: ',model,' in fr.runs fimrun: ',fimrun
            continue
        pmodel=fimrun
        rmodel=model

    if(mf.find(dtgopt,'all')):
        tdtgs=dtgopt
    else:
        tdtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=rundtginc)
        rcSynHour=MF.isSynopticHour(tdtgs[0],12)[0]
        if(rundtginc == 12 and rcSynHour == 0):
            bdtg=mf.dtginc(tdtgs[0],-6)
            edtg=mf.dtginc(tdtgs[-1],+6)
            tdtgs=mf.dtgrange(bdtg,edtg,rundtginc)

    n2.lsAllLocalDtgs(pmodel,rmodel=rmodel,verb=verb)
    n2.lsAllMssDtgs(pmodel,rmodel=rmodel)
    
    # -- get local dtgs
    #
    ldtgs=n2.getDtgs4localModelDtgs(pmodel,tdtgs)

    if(type(tdtgs) != ListType and mf.find(tdtgs,'all')):
        if(dolsmssonly): tdtgs=None
        if(dolsonly):    tdtgs=ldtgs
    
    if(doRmLocal):
        n2.rmLocalDtgDirs(pmodel,tdtgs,rmodel=rmodel,ropt=ropt)
        continue
        
    if(dolsonly):
        n2.lsLocalDtgDirs(pmodel,tdtgs,rmodel=rmodel,fulltaus=fulltaus)
        continue
    
    elif(dolsmssonly):
        n2.lsMssDtgDirs(pmodel,tdtgs)
        continue
    
    if(doput):

        if(dojet):
            n2.putLocal2JetModelDtgs(pmodel,ldtgs,ropt=ropt,doKlean=doKlean,override=override,verb=verb)
            
        # -- mv dat4(local) to dat5
        elif(mv2dat5 and not(mv2dat6)):
            n2.putLocal2Dat5ModelDtgs(pmodel,ldtgs,ropt=ropt,doKlean=doKlean,override=override,verb=verb)
        
        # -- mv dat4(local) to dat6
        elif(mv2dat6 and not(mv2dat5)):
            n2.putLocal2Dat6ModelDtgs(pmodel,ldtgs,ropt=ropt,doKlean=doKlean,override=override,verb=verb)
            
        # -- mv dat5 to dat6
        elif(mv2dat6 and mv2dat5):
            n2.putLocal2Dat6ModelDtgs(pmodel,ldtgs,ropt=ropt,doKlean=doKlean,override=override,verb=verb)
            
        # -- mv dat6 to dat5
        elif(mv2dat7):
            n2.putLocal2Dat5ModelDtgs(pmodel,ldtgs,ropt=ropt,doKlean=doKlean,override=override,verb=verb)
            
        else:
            n2.putLocal2HpssModelDtgs(pmodel,ldtgs,ropt=ropt,doKlean=doKlean,override=override)
            
    if(doget):

        if(dojet):
            # -- do inv for Jet and get dtgs on Jet
            n2J.lsAllLocalDtgs(pmodel,rmodel=rmodel)
            ldtgs=n2J.getDtgs4localModelDtgs(pmodel,tdtgs)

            # -- do inv to set up the target dir
            n2.lsLocalDtgDirs(pmodel,ldtgs)
            
            # -- not get from Jet
            n2.getJet2LocalModelDtgs(pmodel,ldtgs,ropt=ropt)

        else:
            # -- make the center_model.dtgs hash for this model only, to override the dsL.center_model_dtgs hash
            #    i.e., check if local data there before doing the hsi get
            #
            n2.invLocalSingle(pmodel,verb=verb)
            n2.lsLocalDtgDirs(pmodel,tdtgs)
            n2.getHpss2LocalModelDtgs(pmodel,tdtgs,ropt=ropt,override=override)


MF.dTimer(tag='mss-all')

