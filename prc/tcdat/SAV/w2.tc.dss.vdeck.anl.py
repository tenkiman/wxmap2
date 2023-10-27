#!/usr/bin/env python

#from M import *
#MF=MFutils()

diag=0

from tcbase import * # imports tcVM tcCL adVM adCL
from vdVM import *  
from vdCL import *   # imports vdVM

from w2methods import SimpleListStats




#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class AdeckCmdLine(CmdLine,AdeckSources):

    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['sourceopt',  'source or source1,source2,...,sourceN'],
            }
            
        self.defaults={
            'doupdate':0,
            # move from option to default -- not used? 'dobigbias':['B',0,1,'if ls of cases by tau; only print big bias'],
            'dobigbias':0,
            }


        self.options={
            'yearopt':         ['y:',None,'a','year'],
            'tauopt':          ['a:','0-120','a','tauopt'],
            'override':        ['O',0,1,'override'],
            'overrideNL':      ['o',0,1,'overrideNL -- force making of adeck noloads'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'verbopt':         ['v:',-999,'i','verb=1 is verbose'],
            'ropt':            ['N','','norun',' norun is norun'],
            'ropt':            ['N','','norun',' norun is norun'],
            'lsopt':           ['l:',3,'i','lsopt 0 - vdecks; 3|5|6 - with -p ls; 3 aid by aid ls; 5 - interaid ls; 6 csv output by aid'],
            'dohomo':          ['H',1,0,'do NOT do homo comp if set,default is to do homo comp'],
            'forcehomo':       ['h',0,1,'forcehomo = 1 does logical AND on two VDlists that are not the exact same size'],
            'stmopt':          ['S:',None,'a','stmopt'],
            'pcase':           ['c:','pleaseset','a','pcase'],
            'ptype':           ['p:','fe','a',"""ptype:
            
       fe (position fe) | vbias (intensity) | pod (prob of detect) | pof (prob of forecast) |
       pbias (pmin intensity)| gainxyfe (%%improve fe)| gainxyvmax (%%improve Vmax intensity) |
       pbetter (%% aid1 to N-1 better than aidN) |
       gainxyvbias (ratio of Vmax bias/abs Vmax error) | fe-line (fe with lines)| 
       sfe (scaled fe - ratio of fe/best-track length)| nice (Net Intensity Change Error) | nicea abs(nice) 
       ls (listing)
"""],
            'pdir':            ['D:','.','a','pdir = . default'],
            'aidopt':          ['T:',None,'a','taid'],
            'toptitle1':       ['1:',None,'a','toplabel1'],
            'toptitle2':       ['2:',None,'a','toplabel2'],
#            'warn':            ['W',0,1,'warning'],
            'veriwarn':        ['w',None,2,'veriwarn'],
            'newVdeck2':       ['n',0,1,'use vdeck2 form'],
            'reloadFromPyp':   ['P',0,1,'relocad state from pyp'],
            'do9xNOT':         ['9',1,0,'if set dofilt9x=0; do9xrelab=0'],
            'dtgopt':          ['d:',None,'a','dtgopt'],
            'filterOpt':       ['f:',None,'a',"""filterOpt:
            
       tauTTT:             'tau072' -- only verify cases that have a tau072 verification
       synop time only:    'z0012'|'z00'|'z12' | 'z0618'
       be0:DDD | be12:DDD  filter out cases with big tau0 errors (be0) of DDD or big tau12 errors (be12)
"""],
            'filterdtgopt':    ['g:',None,'a','filterdtgopt -- in getStats(), filter out dtgs outside the open interval dtgopt '],
            'doplot':          ['X',0,1,'if set doplot=1 -- .show()'],
            'doxv':            ['x',1,0,'do NOT xv plot'],
            'doBystorm':       ['B',0,1,'output by storm'],
            'lsttau':          ['t:',-1,'i','lsttau -- tau to do an ls of cases'],
            'dobigbias':       ['b',0,1,'if ls of cases by tau; only print big bias'],
            'doplotBE':        ['e',0,1,'do track plots of big error cases when using filterOpt'], 
            'doshow':          ['s',0,1,'show() in pylab'],
            'doHistplot':      ['I',0,1,'do histogram for a dtau'],
            'phourSet':        ['u:',None,'i','set phour to verify'],
            'tableReverse':    ['R',0,1,'display errors by verifying dtg vice run dtg'],
            'printRunOnly':    ['r',0,1,"""for ptype='ls' output only bdtgs where the model is run, e.g., edet has run ddtg=12"""],
            'doland':          ['L',1,0,'remove over-land veri BT posits'],
            }


        self.purpose='''
analyze vdecks by source(s), year(s), storm(s)

sources: %s'''%(self.sources)
        self.examples='''
%s rtfim -T fim8 -S e.9,l.9 -y 2009
%s ncep,ecmwf -S w -T avno,edet -D 2010010100.2010072712 :: do stats on avno and edet aids before the gfs upgrade on 2010072712

%s jtwc -S 09w.12 -T avno -p ls -l3           # detailed ls of fe/vme by storm-model
%s jtwc -S 09w.12 -T avno -p ls -l3 -R        # as above except list errors by verifying dtg vice model run dtg
%s jtwc -S 09w.12 -T avno,hwrf -p ls -l4      # ls only cases where model is suppose to be run
%s jtwc -S 09w.12 -T avno,hwrf -p ls -l5      # intermodel comp of errors
%s jtwc -S 09w.12 -T avno,hwrf -p ls -l6      # output csv form for import to other plotting'''

    def ChkSource(self):

        iok=0
        for iss in self.sourceopt.split(','):
            for s in self.sources:
                if(iss == s): iok=1 ; break

        return(iok)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer('all')
CL=AdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verbopt != -999): verb=verbopt
if(verb): print CL.estr

if(ptype == 'ls'): filterOpt=None

iyearopt=yearopt
if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear


taus=getAllTaus(tauopt)

pyppath='/tmp/vda.pyp'

if(reloadFromPyp):

    PS=open(pyppath)
    pyp=pickle.load(PS)

    if(ptype == 'pod' or ptype == 'pof'):
        (taus,sources,years,
         taids,tstmids,ss)=pyp

    else:
        (taus,verivars,
         sources,years,
         taids,tstmids,
         ostats,allstats,
         ostatsB,allstatsB,
         cases,casedtgs,
         sourceUsed)=pyp


    MF.dTimer('all')

else:
    
    MF.sTimer('getDSs ---- ')
    PS=open(pyppath,'w')

    if(not(CL.ChkSource()) and verb):
        print 'WWW not a standard sourceopt:',sourceopt,' try using adeck from AD.AdeckSource class...'


    if(stmopt != None): getstms=MakeStmList(stmopt,verb=verb,dofilt9x=do9xNOT)
    else: getstms=None

    if(aidopt != None): getaids=aidopt.split(',')
    else: getaids=None

    if(dtgopt != None): dtgs=mf.dtg_dtgopt_prc(dtgopt)
    else: dtgs=None
    
    DSss={}
    dsbdir="%s/DSs"%(TcDataBdir)

    dbtype='vdeck'
    if(newVdeck2): dbtype='vdeck2'
    
    sources=sourceopt.split(',')
    years=yearopt.split(',')


    if(getstms != None and iyearopt == None):
        years=getYearsFromStmids(getstms)
        
    noDSs=DataSets(bdir=dsbdir,name='NoLoad_vdeck.pypdb',dtype='noloads',verb=verb,doDSsWrite=1)

    # -- get source-year by aid
    #
    aidSources={}

    tgetaids=copy.deepcopy(getaids)
    igetaids=[]
    
    if(tgetaids == None): tgetaids=[]
    for getaid in tgetaids:
        tt=getaid.split('.')
        igetaid=tt[-1]
        aidSources[igetaid]=[]
        if(len(tt) > 1): aidSources[igetaid]=tt[0:-1]
        igetaids.append(igetaid)

    getaids=igetaids
    
    # -- get aids and relabel
    #
    tstmids=taids=[]

    # -- set phour
    #
    if(getaids != None and phourSet != None):
        ogetaids=[]
        for taid in getaids:
            ogetaids.append("%s%02d"%(taid,phourSet))
        getaids=ogetaids

        print 'HHHHHHHHHHHHHHHHHH ',phourSet,getaids

    (getaidsFinal,taidsFinal,taidsRelabel,aidSources)=getFinalAidsByRelabel(getaids,aidSources)
    
    # -- case where we want to output all aids
    #
    if(len(getaidsFinal) == 0): getaidsFinal=None

    # -- dict with source used for aid
    sourceUsed={}
    # -- loop by years, sources go DSss hash
    #
    for year in years:
        for source in sources:
            dbname="%s_%s_%s"%(dbtype,source,year)
            dbfile="%s.pypdb"%(dbname)
            print 'sssssssssssss',year,source,dbfile
            DSss[source,year]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)
            (aids,stmids)=GetAidsStormsFromDss(DSss[source,year],getaidsFinal,getstms,dofilt9x=do9xNOT)
            tstmids=tstmids+stmids
            taids=taids+aids
            for aid in aids:
                MF.appendDictList(sourceUsed,aid,source)

    
    for getaid in getaids:
        ssyys=aidSources[getaid]
        
        if(len(ssyys) > 0):
            for ssyy in ssyys:
                try:
                    (source,year)=ssyy.split('-')
                except:
                    print 'EEE invalid form of setting source-year for aids...was:  ',ssyy,'should be: SSS-YYYY'
                    sys.exit()
                if(verb): print 'GGG getting source,year: ',source,year,' for getaid: ',getaid
                dbname="%s_%s_%s"%(dbtype,source,year)
                dbfile="%s.pypdb"%(dbname)
                
                if(not( (source,year) in DSss.keys())):
                    DSss[source,year,getaid]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)
                else:
                    DSss[source,year,getaid]=DSss[source,year]
                    if(verb): print 'III already got DSss[%s,%s] continue...'%(source,year)
                    
                (aids,stmids)=GetAidsStormsFromDss(DSss[source,year,getaid],getaidsFinal,getstms,dofilt9x=do9xNOT)

                for aid in aids:
                    MF.appendDictList(sourceUsed,aid,source)
                    
                tstmids=tstmids+stmids
                taids=taids+aids

    MF.dTimer('getDSs ---- ')

    tstmids=mf.uniq(tstmids)
    taids=mf.uniq(taids)

    if(len(taids) > maxTaids):
        print 'EEE too many aids to vda; N: ',len(taids)
        sys.exit()


    if(lsopt == 0):
        print 'DDDD #DSss: ',len(DSss)
        for k in DSss.keys():
            vDS=DSss[k]
            print 'DDDDDDDDD ',k
            if(vDS != None):
                LsAidsStormsDss(vDS,None,None,dofilt9x=do9xNOT)
        sys.exit()

    else:
        print 'IIIIII--- working tstmids: %s'%(str(tstmids))[0:140],'...'
        print 'IIIIII--- working   taids: ',taids

    # -- check if we got anything
    #
    if(len(taids) == 0):
        print 'EEE(w2.tc.dssvdeck.anl.py) no taids ... if 9X try -9 option'
        sys.exit()
        


    # get vd dict
    #
    MF.sTimer('getvds dtgs ---- ')
    MF.sTimer('getvds ALL ---- ')

    if(dtgs != None):
        tcD=TcData(dtgopt=dtgs[-1])
        for dtg in dtgs:
            (tstmids)=tcD.getStmidDtg(dtg)
        tstmids=mf.uniq(tstmids)
        (vds,taids,tstmids)=getVdsFromDSss(DSss,taids,tstmids,taidsRelabel,aidSources,verb=verb)
        MF.dTimer('getvds dtgs ---- ')
    else:
        (vds,taids,tstmids)=getVdsFromDSss(DSss,taids,tstmids,taidsRelabel,aidSources,verb=verb)
        MF.dTimer('getvds ALL ---- ')

    # -- if no taidsFinal set to taids from the DSs
    #
    if(len(taidsFinal) == 0): taidsFinal=taids
    
    # -- order the output aids by the input, but include only aids in the vdecks
    #
    otaids=[]
    for ftaid in taidsFinal:
        for otaid in taids:
            if( (otaid == ftaid and not(otaid in otaids)) or 
                (ftaid == 'hfip' and not(ftaid in otaids)) or
                (ftaid == 'hfipj' and not(ftaid in otaids)) or
                (ftaid == 'hclp' and not(ftaid in otaids)) or
                (ftaid == 'hfip20' and not(ftaid in otaids)) 
                ): otaids.append(ftaid)


    # -- uniq sorts...turned for for some reason...20130410 -- uncomment for this case:
    # vda rtfim9,rtfim_r2220intfc150g9 -S e.11,l.11,e.12,l.12 -T fr2220g9:fim9,fim9
    # -- 20130503 -- added code to handle dups in getFinalAidsByRelabel() when relabeling
    #
    if(len(taidsFinal) != len(otaids)):
        print 'EEEE error outputing the aids in order of input...taids: ',taids,' otaids: ',otaids
        sys.exit()

    if(verb): print 'OOOO final otaids: ',otaids
    
    taids=otaids

    if(len(taids) == 0):
        print 'EEE(%s) no aids in '%(pyfile),DSss.keys(),'for getaids: ',getaids
        sys.exit()

    # -- POD by analyzing counts
    #
    if(ptype == 'pod' or ptype == 'pof'):
        
        filtPof=0
        if(ptype == 'pof'): filtPof=1

        filt0012=0
        filt0618=0
        filt00=0
        filt12=0

        if(filterOpt != None):
            if(filterOpt.upper() == 'Z0012'): filt0012=1
            if(filterOpt.upper() == 'Z0618'): filt0618=1
            if(filterOpt.upper() == 'Z00'):   filt00=1
            if(filterOpt.upper() == 'Z12'):   filt12=1
            
        
        # -- counts analysis
        #
        MF.sTimer('PodStats    ---- ')
        
        counts=getCountsVds(vds,taus,
                            filt0012=filt0012,
                            filt00=filt00,
                            filt12=filt12,
                            filt0618=filt0618,
                            filtPof=filtPof,verb=verb,
                            veriwarn=veriwarn,
                            )
        
        ss=PodStats(taids,tstmids,counts,verb=verb)
        MF.dTimer('PodStats    ---- ')

        # -- pickle current state
        #
        pyp=(taus,sources,years,aidSources,
             taids,tstmids)


    
    else:


##         kk=vds.keys()

##         print 'kkkkkkkkkkkkkkkkk ',kk

##         vstmids={}

##         for taid in taids:
##             vstmids[taid]=tstmids

##         for k in kk:
##             vd=vds[k]
##             print k,vd
##             veriopts=None
##             tau00filtopt='tc'
##             stmoptall=None
##             tauls=0
##             lsopt=0
##             dohomo=0
##             vopts=(veriopts,tau00filtopt,stmopt,stmoptall,tauls,dohomo)

##             filtdtgs=None
##             if(filterdtgopt != None):  filtdtgs=mf.dtg_dtgopt_prc(filterdtgopt)

##             rc=StmStatAnal(taids,vstmids,taus,vds,
##                            vopts,verb=verb,lsopt=lsopt,
##                            filtdtgs=filtdtgs)

##             (stats,imstats,counts,countsmask,fevmerpt)=rc
##             print stats

            

##         sys.exit()

    
##         rc=StmStatAnal(imodels,vstmids,taus,vd,
##                        vopts,verb=verb,lsopt=lsopt,
##                        filtdtgs=filtdtgs)
        
##         (stats,imstats,counts,countsmask,fevmerpt)=rc

        rc=getStats(ptype,taus,taids,tstmids,vds,noDSs,filterdtgopt,
                    doland=doland,
                    tableReverse=tableReverse,
                    filterOpt=filterOpt,
                    overrideNL=overrideNL,
                    lsopt=lsopt,
                    doBystorm=doBystorm,
                    dohomo=dohomo,
                    forcehomo=forcehomo,
                    printRunOnly=printRunOnly,
                    veriwarn=veriwarn,
                    sourceUsed=sourceUsed,
                    w2=w2,
                    diag=diag,
                    verb=verb)

        (ss,verivars,ostats,ostatsB,allstats,allstatsB,cases,casedtgs)=rc
        

        ## for verikey in verikeys:
        ##     ocards={}
        ##     for taid in taids:
        ##         print 'vvvvvvvvvvvvvvvvvvvvvvvv',taid,taids.index(taid)
        ##         if(taids.index(taid) == len(taids)):
        ##             Ncard="  #CASES   "
        ##             for tau in taus:
        ##                 (ostat,mean,amean,sigma,max,min,n)=allstats[taid,tau,verikey]
        ##                 Ncard="%s %-4d"%(Ncard,n)
        ##             print 'NNNNNNNNNNNNNNN ',Ncard
                
        ##     for tau in taus:
        ##         (ostat,mean,amean,sigma,max,min,n)=allstats[taid,tau,verikey]
        ##         mean=ostat[0]
        ##         printOstat(allstats,taid,tau,verikey)

        # -- pickle current state
        #
        pyp=(ss,taus,verivars,
             sources,years,
             taids,tstmids,
             ostats,allstats,
             ostatsB,allstatsB,
             cases,casedtgs,
             sourceUsed)
        

    pickle.dump(pyp,PS)
    PS.close()


if(lsttau >= 0):
    ovars=lsCases(taids,cases,casedtgs,verivars,ttau=lsttau,dobigbias=dobigbias,filterOpt=filterOpt,veriwarn=veriwarn,doplot=doplot)
    if(len(ovars) > 0): print 'ooooooooooooooo -- ovars ',ovars.keys()
    
    
    # -- hhhhhhh histograms
    #
    if(doHistplot):
        list0=None
        if(len(taids) == 1):
            list1=ovars[taids[0]]
            list2=None
            tag0=taids[0]
            var1=taids[0]
            var2=''
        elif(len(taids) == 2):
            list1=ovars[taids[0]]
            list2=ovars[taids[1]]
            tag0="%s_%s"%(taids[0],taids[1])
            var1=taids[0]
            var2=taids[1]

        elif(len(taids) == 3):
            list1=ovars[taids[-2]]
            list2=ovars[taids[-1]]
            tag0="%s_%s"%(taids[-2],taids[-1])
            var1=taids[-2]
            var2=taids[-1]



        xint=50.0
        yint=2
        ymin=0.0
        xmin=0.0
        
        if(lsttau == 120):
            xmax=1000.0
            xint=100.0
            ymax=12
        elif(lsttau == 72):
            xmax=500.0
            xint=50.0
            ymax=15
            
        elif(lsttau == 48):
            xmax=400.0
            xint=50.0
            ymax=20
            
        elif(lsttau == 24):
            xmax=300.0
            xint=25.0
            ymax=30
            
        elif(lsttau == 0):
            xmax=150.0
            xint=10.0
            ymax=50

        htag2="tau%03d"%(lsttau)
        if(pcase != None): htag2="tau%03d-%s"%(lsttau,pcase)

        rc=pltHist(list0,list1,list2,
                   stmopt,
                   #xlab='Intensity error [kt]',
                   xlab='FE [nm]',
                   var1=var1,
                   var2=var2,
                   tag0=tag0,
                   donorm=0,
                   docum=0,
                   doxv=1,
                   doshow=0,
                   title1="%s v %s %d-h %s"%(var1,var2,lsttau,ptype),
                   tag1=ptype,tag2=htag2,
                   #xmax=1000.0,xmin=0.0,xint=100.0,
                   xmax=xmax,xmin=xmin,xint=xint,
                   ymax=ymax,ymin=ymin,yint=yint,
                   #ymax=1,   ymin=0,  yint=0.1,
    #               ymax=10,   ymin=0,  yint=1,
                   )

#pppppppppppppppppppppppppppppppppppppppppppppppppp
# plotting


if(doplot):

    do2ndval=0
    dohfiptitle=0
    
    if(ptype == 'fe' or ptype == 'gainxyfe'):
        pverikey='fe'
        pverikey1=pverikey
        if(mf.find(pcase,'ens') and dohfiptitle ):
            do1stplot=1
            do2ndplot=0
            toptitle1='HFIP 2009 Summer Demo Period -- Hi-Res Ensemble Systems -- Mean v Spread'
        else:
            do1stplot=0
            do2ndplot=1
            if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

        if(dohfiptitle):
            if(pcase == 'ens.f8mn'):
                toptitle2='21 Member FIM G8 (30 km) using EnKF perturbation'
            elif(pcase == 'ens.gkmn'):
                toptitle2='21 Member GFS (T382) using EnKF'
            elif(pcase == 'ens.eemn'):
                toptitle2='51 Member ECMWF EPS (T399) using tropical SVs'
            else:
                toptitle2=None
                
    elif(ptype == 'fe-line'):
        ptype='fe'
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'sfe'):
        pverikey='sfe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        
    elif(ptype == 'gainxyvmax'):
        pverikey='vme'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        
    elif(ptype == 'pbetter'):
        pverikey=ptype
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        
    elif(ptype == 'vbias'):
        pverikey='vbias'
        pverikey1='vme'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'rmsfe'):
        pverikey='fe'
        pverikey1='rmsfe'
        do1stplot=1
        do2ndplot=1
        do2ndval=-1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='RMS -- line ; Error = bar'

    elif(ptype == 'nice'):
        pverikey='niceb'
        pverikey1='nice'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pbias'):
        pverikey='pbias'
        pverikey1='pmine'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pod'):
        pverikey='pod'
        pverikey1='over'
        #pverikey='over'
        #pverikey1='pod'

        do1stplot=1
        do2ndplot=1
        do2ndval=-1 # have pod 1st in table cells

        toptitle2='Prob Of Detection [POD;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        ostats=ss.ostats
        ostatsB=ss.ostatsB

    elif(ptype == 'pof'):
        pverikey='pod'
        pverikey1='over'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Prob Of Forecast [POF;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        ostats=ss.ostats

    elif(ptype == 'gainxyvbias'):
        pverikey='vbias'
        pverikey1='vbias'
        do1stplot=0
        do2ndplot=1

        toptitle2='Ratio abs(bias)/mean(abs) Intensity Error [%] :: percentage of Error from bias'

    elif(ptype == 'r34e'):
        pverikey='r34e'
        pverikey1='r34bt'
        do1stplot=1
        do2ndplot=1
        do2ndval=1
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)    

    sdicts=[]
    ndicts=[]

    for n in range(0,len(taids)):
        taid=taids[n]
        sdict1={}
        sdict={}
        ndict={}

        if(doBystorm):
	
            nstms=len(tstmids)
            nstmids=1
            if(nstms > 0): nstmids=nstms
            for ns in range(0,nstmids):
                stmid=tstmids[ns]
                fixtau=taus[0]
                for tau in taus:
                    sdict1[stmid]=ostatsB[taid,stmid,fixtau,pverikey1][0]
                    sdict[stmid]=ostatsB[taid,stmid,fixtau,pverikey][0]
                    ndict[stmid]=ostatsB[taid,stmid,fixtau,pverikey][1]

        else:
        
            for tau in taus:
                sdict1[tau]=ostats[taid,tau,pverikey1][0]
                sdict[tau]=ostats[taid,tau,pverikey][0]
                ndict[tau]=ostats[taid,tau,pverikey][1]
                
        if( (pcase == 'ens.eemn' or pcase == 'ens.f8mn') and (n == len(taids)-1) ):
            ss.models=ss.models[0:-1]
            continue

        sdicts.append((sdict1,sdict))
        ndicts.append(ndict)


    pss=SumStatsPlot(ss,pcase,ptype,pdir=pdir,doland=doland)
    if(verb): pss.ls()

    # see c.w2.pt 20120308*/p.vda.py for tuned version to do 'skill'
    #
    
    ilstyle=ilwidth=None
    
    pss.setPlottitles(toptitle1,toptitle2,taus)
    plotcontrolVar=None
    #plotcontrolVar=([0.0,800.0,100],2)  -- big d+7 errors
    #plotcontrolVar=([0.0,100.0,10],2) -- skill space
    #plotcontrolVar=([-70.0,70.0,10],2) # gainxyfe for hfip
    #plotcontrolVar=([-60.0,50.0,10],2) # gainxyfe for hfip
    #plotcontrolVar=([0.0,600.0,50],2)  #-- big d+7 errors
    #plotcontrolVar=([0.0,200.0,20],2) #-- pod/poo

    pss.setControls(controlsVar=plotcontrolVar)
    pss.simpleplot(ss.models,sdicts,ndicts,ss.labaids,ss.colaids,
                   ilmarker=ss.markaids,
                   do1stplot=do1stplot,
                   do2ndplot=do2ndplot,
                   dopng=1,
                   ilstyle=ilstyle,
                   ilwidth=ilwidth,
                   do2ndval=do2ndval,
                   doline=0,
                   doxv=doxv,
                   docp=1,
                   verb=verb,
                   doshow=doshow)
    


MF.dTimer('all')


sys.exit()
