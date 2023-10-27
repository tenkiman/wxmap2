from tcVM import *
from vdVM import *
from w2base import w2Colors
from adCL import AdeckSources

class VD2AnlCmdLine(CmdLine):

    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            }
            
        self.defaults={
            'doupdate':0,
            # move from option to default -- not used? 'dobigbias':['B',0,1,'if ls of cases by tau; only print big bias'],
            'dobigbias':0,
            }


        self.options={
            'lsVD2cache':       ['A',0,1,'list all storms and aids in the cache'],
            'dssDir':           ['D:',None,'a','set base dir for DSs'],
            'tauopt':           ['a:','0-120','a','tauopt: 1) 0-72; 2) 24-120; 3) 48-72; 4) 72-120; 0-24,36,48,72,96,120,168'],
            'override':         ['O',0,1,'override'],
            'overrideVD':       ['o',0,1,'overrideVD unlink(kill) vdeck - start fresh'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'verbopt':          ['v:',-999,'i','verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'lsopt':            ['l:',3,'i','lsopt 0 - vdecks; 3|5|6 - with -p ls; 3 aid by aid ls; 5 - interaid ls; 6 csv output by aid'],
            'dohomo':           ['H',1,0,'do NOT do homo comp if set,default is to do homo comp'],
            'forcehomo':        ['h',0,1,'forcehomo = 1 does logical AND on two VDlists that are not the exact same size'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'pcase':            ['c:','pleaseset','a','pcase'],
            'pltcntvar':        ['C:',None,'a','plotcontrolVar=n1,n2,n3'],
            'ptype':            ['p:','pe','a',"""ptype:
       pe (position err) | vbias (intensity) | pod (prob of detect) | pod-line (pod with lines) | pof (prob of forecast) |
       pbias (pmin intensity)| gainxype (%%improve pe)| gainxyvmax (%%improve Vmax intensity) |
       pbetter (%% aid1 to N-1 better than aidN) | ct-ate (cross track/along track) | at-cte (along/cross)
       gainxyvbias (ratio of Vmax bias/abs Vmax error) | pe-line (pe with lines)| pe-frac (%% of by storm)
       fe (forecast err) | fe0 (forecast error IE=0) | fe-line (fe with lines) | gainxyfe(%%improve FE) | gainxyfe0(%%improve FE0) |
       te (track err) | gainxyte (%%improve te)
       spe (scaled pe - ratio of pe/best-track length)| nice (Net Intensity Change Error) | nicea abs(nice) 
       ls (listing) | ls.vmax (listing with bvmax and fvmax - experimental)
"""],
            'pdir':             ['I:','.','a',"""pdir = '.' default"""],
            'aidopt':           ['T:',None,'a','taid'],
            'toptitle1':        ['1:',None,'a','toplabel1'],
            'toptitle2':        ['2:',None,'a','toplabel2'],
#            'warn':            ['W',0,1,'warning'],
            'veriwarn':         ['w',None,2,'veriwarn'],
            'reloadFromPyp':    ['P',0,1,'reload state from pyp file'],
            'pypFile':          ['y:','','a','set name of pyp file'],
            'do9xNOT':          ['9',1,0,'if set dofilt9x=0; do9xrelab=0'],
            'dtgopt':           ['d:',None,'a','dtgopt'],
            'filterOpts':       ['f:',None,'a',"""filterOpt:
            
       tauTTT:             'tau072' -- only verify cases that have a tau072 verification
       synop time only:    'z0012'|'z00'|'z12' | 'z0618'
       be0:DDD | be12:DDD  filter out cases with big tau0 errors (be0) of DDD or big tau12 errors (be12)
       use comma delimited for multiple filterOpt, e.g., z0012,tau072
"""],
            'filterdtgopt':     ['g:',None,'a','filterdtgopt -- in getStats(), filter out dtgs outside the open interval dtgopt '],
            'stmidsByDtgsPath': ['G:',None,'a','path to file with select dtgs to verify for PoD'],
            'doplot':           ['X',0,1,'if set doplot=1 -- .show()'],
            'doxv':             ['x',1,0,'do NOT xv plot'],
            'doBystorm':        ['B',0,1,'output by storm'],
            'lsttau':           ['t:',-1,'i','lsttau -- tau to do an ls of cases'],
            'dobigbias':        ['b',0,1,'if ls of cases by tau; only print big bias'],
            'doplotBE':         ['e',0,1,'do track plots of big error cases when using filterOpt'], 
            'doErrBar':         ['E:',None,'i','for setting of the doErrBar from here vice from setVD2PlotVars() -- [None] | 1 | 0'], 
            'doshow':           ['s',0,1,'show() in pylab'],
            'doHistplot':       ['I:',-999,'i','do histogram for -I tau '],
            'phourSet':         ['u:',None,'i','set phour to verify'],
            'tableReverse':     ['R',0,1,'display errors by verifying dtg vice run dtg'],
            'printRunOnly':     ['r',0,1,"""for ptype='ls' output only bdtgs where the model is run, e.g., edet has run ddtg=12"""],
            'doland':           ['L',1,0,'remove over-land veri BT posits'],
            'doMetric':         ['M',0,1,'metric units'],
            'verirule':         ['3:','std','a',"""set verirule: 'std' :: NHC rule  or 'td':: any posit >= 25kt """],
            }


        self.purpose='''
analyze/create (as needed) vdeck2 from cache in dsbdirVD2/vdeck2_YYYY.pypdb'''

        self.examples='''
%s aliased in $W2/.w2alias as 'vd2a'

%s -S w.10 -T avno,edet -D 2010010100.2010072712 :: do stats on avno and edet aids before the gfs upgrade on 2010072712
%s -S 09w.12 -T avno -p ls -l3           # detailed ls of pe/vme by storm-model
%s -S 09w.12 -T avno -p ls -l3 -R        # as above except list errors by verifying dtg vice model run dtg
%s -S 09w.12 -T avno,hwrf -p ls -l4      # ls only cases where model is suppose to be run
%s -S 09w.12 -T avno,hwrf -p ls -l5      # intermodel comp of errors
%s -S 09w.12 -T avno,hwrf -p ls -l6      # output csv form for import to other plotting'''



class VdeckSAnl(DataSet):
    
    from WxMAP2 import W2
    w2=W2()
    
    lf=w2.SetLandFrac()
    
    def GetLF(self,lat,lon):
        landfrac=self.w2.GetLandFrac(self.lf,lat,lon)
        return(landfrac)        
    
    
class SumStats(MFutils):

    def __init__(self,
                 taids,
                 tstmids,
                 verivars,
                 ostats,
                 cases,
                 casedtgs,
                 ):


        self.taids=taids
        self.tstmids=tstmids
        self.verivars=verivars
        self.ostats=ostats
        self.cases=cases
        self.casedtgs=casedtgs

        self.initStorms()
        self.initAidStorms()


    def initStorms(self):

        vstmids=[]
        vdtgs=[]
        vvmaxs=[]
        kk=self.cases.keys()
        
        for k in kk:
            vstmids.append(self.cases[k][0])
            vdtgs.append(self.cases[k][1])
            vvmaxs.append(self.cases[k][2])

        self.vstmids=self.uniq(vstmids)
        self.vdtgs=self.uniq(vdtgs)
        self.vvmaxs=self.uniq(vvmaxs)

        
    def initAidStorms(self,verb=0):
        
        models=[]
        labaids=[]
        colaids=[]
        markaids=[]
        
        for taid in self.taids:
            ap=AidProp(taid)
            labaids.append(ap.label)
            colaids.append(ap.color)
            models.append(ap.oname)
            markaids.append(ap.mark)

        self.models=models
        self.labaids=labaids
        self.colaids=colaids
        self.markaids=markaids

        if(not(hasattr(self,'verivars'))): return

            
        # force specific marker for intensity plots
        #
        for n in range(0,len(markaids)):
            markaid=markaids[n]
            if(verb): print 'III(initAidStorms) ',self.verivars[0],markaid
            if(self.verivars[0] == 'vbias' and markaid != 'd'):
                markaid=markaid
            else:
                markaid='+'

            markaids[n]=markaid

        if(verb): print 'III(initAidSTorms) final markaids: ',markaids




class PodStats(SumStats):

    verikeyPod='pod'
    verikeyPoo='poo'

    def __init__(self,
                 taids,
                 tstmids,
                 counts,
                 verb=0,
                 verikey='pod',
                 ):


        self.taids=taids
        self.tstmids=tstmids
        self.counts=counts
        self.verb=verb

        self.initStorms()
        self.initAidStorms()
        self.makeStats()


    def initStorms(self):

        vstmids=[]

        kk=self.counts.keys()
        
        for k in kk:
            stmid=k[1]
            vstmids.append(stmid)

        self.vstmids=MF.uniq(vstmids)


    def makeStats(self):

        self.ostats={}
        self.ostatsB={}
        
        aids=[]
        taus=[]
        pods={}
        nveris={}
        nverifcs={}
        nverifcovers={}

        podsB={}
        nverisB={}
        nverifcsB={}
        nverifcoversB={}
       
        nveri=0
        nverifc=0
        nverifcover=0

        kk=self.counts.keys()
        stmids=[]

        for k in kk:

            aid=k[0]
            stmid=k[1]
            stmids.append(stmid)
            
            tau=k[2]

            aids.append(aid)
            taus.append(tau)
            
            cts= self.counts[k]

            try:
                nveris[aid,tau]=nveris[aid,tau]              + cts[0]
            except:
                nveris[aid,tau]=cts[0]
            

            try:
                nverifcs[aid,tau]=nverifcs[aid,tau]          + cts[1]
            except:
                nverifcs[aid,tau]=cts[1]

            try:
                nverifcovers[aid,tau]=nverifcovers[aid,tau]  + cts[2]
            except:
                nverifcovers[aid,tau]=cts[2]

            # -- By storms
            #
            try:
                nverisB[aid,stmid,tau]=nverisB[aid,tau]       + cts[0]
            except:
                nverisB[aid,stmid,tau]=cts[0]

            try:
                nverifcsB[aid,stmid,tau]=nverifcsB[aid,stmid,tau]          + cts[1]
            except:
                nverifcsB[aid,stmid,tau]=cts[1]

            try:
                nverifcoversB[aid,stmid,tau]=nverifcoversB[aid,stmid,tau]  + cts[2]
            except:
                nverifcoversB[aid,stmid,tau]=cts[2]


        # -- all stats
        #
        aids=MF.uniq(aids)
        taus=MF.uniq(taus)
        minv=ptl25=median=ptl75=ptl90=maxv=-999

        cardPods={}
        cardPoos={}
        omeanPods={}
        omeanPoos={}

        for aid in aids:
            
            for tau in taus:
                
                if(nveris[aid,tau] > 0):
                    pods[aid,tau]=(float(nverifcs[aid,tau])/float(nveris[aid,tau]))*100.0
                else:
                    pods[aid,tau]=-999

                pod=pods[aid,tau]

                try:    nveri=nveris[aid,tau]
                except: nveri=0

                try:    nverifc=nverifcs[aid,tau]
                except: nverifc=0

                try:    nverifcover=nverifcovers[aid,tau]
                except: nverifcover=0

                over=-999.
                if(nveri > 0):
                    over=(float(nverifcover)/float(nveri))*100.0

                    MF.appendDictList(omeanPods,aid,pod)
                    cardPods[aid,tau]='SSSSSHHHHH %18s %3d %10s'%(aid,tau,self.verikeyPod)+ \
                                       ' %10.1f N: %4d  Nfc:   %4d'%(pod,nveris[aid,tau],nverifcs[aid,tau])

                    MF.appendDictList(omeanPoos,aid,over)
                    cardPoos[aid,tau]='SSSSSHHHHH %18s %3d %10s'%(aid,tau,self.verikeyPoo) + \
                                       ' %10.1f N: %4d  Nover: %4d'%(over,nveris[aid,tau],nverifcovers[aid,tau])
                else:
                    #None
                    # -- output nothing...\
                    MF.appendDictList(omeanPods,aid,pod)
                    cardPods[aid,tau]='SSSSSHHHHH %18s %3d %10s -- nada'%(aid,tau,self.verikeyPod)
                    MF.appendDictList(omeanPoos,aid,over)
                    cardPoos[aid,tau]='SSSSSHHHHH %18s %3d %10s -- nada'%(aid,tau,self.verikeyPoo)
                    
                    
                #print 'aid: %s tau: %3d   pod: %6.1f  over: %6.1f   N: %4d  Nfc: %4d  Nover: %4d'%(aid,tau,pod,over,nveris[aid,tau],nverifcs[aid,tau],nverifcovers[aid,tau])

                ostat=(pod,nveri,minv,ptl25,median,ptl75,ptl90,maxv)
                self.ostats[aid,tau,'pod']=ostat

                ostat=(over,nverifcover,minv,ptl25,median,ptl75,ptl90,maxv)
                self.ostats[aid,tau,'over']=ostat



        Tcard="                    "
        for tau in taus:
            Tcard="%s  %03d  "%(Tcard,tau)

        Ncard="         #CASES      "
        for tau in taus:
            Ncard="%s %-4d  "%(Ncard,nveris[aids[0],tau])


        for tau in taus:
            for aid in aids:
                print cardPods[aid,tau]

        print
        print '   VERIKEY: ',self.verikeyPod.upper()

        print Tcard
        for aid in aids:
            ocard="  %13s   "%(aid.upper())
            for omean in omeanPods[aid]:
                ocard="%s %6.1f"%(ocard,omean)
            print ocard
        print Ncard
        print

        for tau in taus:
            for aid in aids:
                print cardPoos[aid,tau]
            
        print
        print '   VERIKEY: ',self.verikeyPoo.upper()

        print Tcard
        for aid in aids:
            ocard="  %13s   "%(aid.upper())
            for omean in omeanPoos[aid]:
                ocard="%s %6.1f"%(ocard,omean)
            print ocard
        print Ncard
        print

        # -- by storm stats
        #
        stmids=mf.uniq(stmids)

        for aid in aids:
            for stmid in stmids:
                if(self.verb and len(stmids) > 1): print
                
                for tau in taus:    
                
                    try: 
                        if(nverisB[aid,stmid,tau] > 0):
                            podsB[aid,stmid,tau]=(float(nverifcsB[aid,stmid,tau])/float(nverisB[aid,stmid,tau]))*100.0
                        else:
                            podsB[aid,stmid,tau]=-999
                    except:
                        podsB[aid,stmid,tau]=-999
    
                    pod=podsB[aid,stmid,tau]
    
                    try:    nveri=nverisB[aid,stmid,tau]
                    except: nveri=0
    
                    try:    nverifc=nverifcsB[aid,stmid,tau]
                    except: nverifc=0
    
                    try:    nverifcover=nverifcoversB[aid,stmid,tau]
                    except: nverifcover=0
    
                    over=-999.
                    if(nveri > 0):
                        over=(float(nverifcover)/float(nveri))*100.0
                    if(self.verb): print 'aid: %s stmid: %s tau: %3d   pod: %6.1f  over: %6.1f   N: %4d  Nfc: %4d  Nover: %4d'%(aid,stmid,tau,pod,over,\
                                                                                                                 nverisB[aid,stmid,tau],nverifcsB[aid,stmid,tau],nverifcoversB[aid,stmid,tau])
    
                    ostat=(pod,nveri)
                    self.ostatsB[aid,stmid,tau,'pod']=ostat
    
                    ostat=(over,nverifcover)
                    self.ostatsB[aid,stmid,tau,'over']=ostat
    


        


class SumStatsPlot(MFbase):


    def __init__(self,models,vstmids,
                 pcase,
                 ptype,
                 doland=1,
                 pdir='/tmp',
                 doMetric=0,
                 ):

        # -- 20190905 -- handle pcase with a directory
        #
        (ppdir,pfile)=os.path.split(pcase)
        
        if(len(ppdir) > 0): 
            pdir=ppdir
            pname="%s.%s"%(ptype,pfile)
        else:
            pname='%s.%s'%(ptype,pcase)
            
        self.models=models
        self.vstmids=vstmids
        self.pcase=pcase
        self.ptype=ptype
        self.doMetric=doMetric
        
        if(doland == 0):
            pname="%s-noland"%(pname)
            
        self.ppaths=[
            '%s/%s.png'%(pdir,pname),
            '%s/%s.eps'%(pdir,pname),
            '%s/%s.txt'%(pdir,pname),
            ]


        self.pvartagopt=None


    def reducestmids(self,stmids,filter9x=1):

        ostmids=[]
        for stmid in stmids:
            tt=stmid.split('.')
            stm3id=tt[0]
            stmnum=int(stm3id[0:2])
            if(filter9x and stmnum >= 90): continue
            stmyear=tt[1]
            ostmid="%s.%s"%(stm3id,stmyear[2:4])
            ostmids.append(ostmid)
            
        return(ostmids)


    def setPlottitles(self,
                      toptitle1=None,
                      toptitle2=None,
                      taus=None,
                      xlab=None,
                      ):

        models=self.models

        #
        # main title
        #
        if(toptitle1 == None):
            t1='please add using -1 command line option....'
        else:
            t1=toptitle1

        if(toptitle2 != None):
            t1=t1+'\n'+toptitle2


        #
        # subtitle
        #


        lmodel=models[-1]
        if(hasattr(self,'vstmids')):
            if(len(self.vstmids) > 0):
                ovstmids=self.reducestmids(self.vstmids)
            else:
                ovstmids=[]
        else:
            ovstmids=[]

        if(mf.find(self.ptype,'gainxype')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'
            
        if(mf.find(self.ptype,'gainxyte')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
                t2a=t2a+'\n'
                
        if(self.ptype == 'gainxyfe'):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
                t2a=t2a+'\n'
                
        if(self.ptype == 'gainxyfe0'):
            t2a="Gain [%%] FE(IE=0) Relative FE"

                    
        if(mf.find(self.ptype,'pbetter')):
            t2a="%% cases better Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            if(len(taus) == 1):
                t2a="%s tau= %s"%(t2a,taus[0])
            t2a=t2a+'\n'

        elif(mf.find(self.ptype,'gainxyvmax')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'

        elif(mf.find(self.ptype,'gainxyvbias')):
            t2a='Ratio of bias/mean(abs) [%]'
            for model in models[0:]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'

        else:
            t2a='Models: '
            for model in models:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'
            

        ns=len(ovstmids)
        nsmax=18
        if(ns > 0):
            t2b="Storms[N] [%d]: "%(ns)
        else:
            t2b=''

        if(ns > nsmax):
            n1b=0
            n1e=nsmax/2
            n2b=ns-nsmax/2
            n2e=ns

            for n in range(n1b,n1e):
                ovstmid=ovstmids[n]
                t2b="%s %s"%(t2b,ovstmid)

            t2b="%s ..."%(t2b)

            for n in range(n2b,n2e):
                ovstmid=ovstmids[n]
                t2b="%s %s"%(t2b,ovstmid)

        else:
            for n in range(0,ns):
                ovstmid=ovstmids[n]
                if(n%20 == 0 and n != 0): t2b=t2b+'\n'
                t2b="%s %s"%(t2b,ovstmid)


        if(self.ptype == 'pbetter'):
            t2=t2a+t2b
        else:
            t2=t2b

        if(self.ptype == 'pe' or self.ptype == 'pe-line'):
            ylab='PE [nm]'
            if(self.doMetric): ylab='PE [km]'

        if(self.ptype == 'pe-frac'):
            ylab='% PE '
            
        if(self.ptype == 'pe-pcnt'):
            ylab='% cases '

        if(self.ptype == 'pe-imp'):
            ylab='% PE Improve over Mean '
            
        if(self.ptype == 'pe-imps'):
            ylab='% PE Improve over Mean - Scaled by N '

        if(self.ptype == 'fe-imp'):
            ylab='% FE Improve over Mean '
            
        if(self.ptype == 'fe-imps'):
            ylab='% FE Improve over Mean - Scaled by N '

        if(self.ptype == 'fe' or self.ptype == 'fe-line'):
            ylab='FE [TJ]'
            if(self.doMetric): ylab='FE [TJ]'
        
        if(self.ptype == 'fe-norm'):
            ylab='FE normalized to [nmi]'
            if(self.doMetric): ylab='FE normalized to [nmi]'

        if(self.ptype == 'fe0'):
            ylab='FE0 [TJ]'
            if(self.doMetric): ylab='FE0 [TJ]'
        
        if(self.ptype == 'te'):
            ylab='TE [nm]'
            if(self.doMetric): ylab='TE [km]'
        
            
        if(self.ptype == 'pe-fe'):
            ylab='PE [nmi] FE [TJ]'
            if(self.doMetric): ylab='PE [km] FE [TJ]'

        if(self.ptype == 'spe'):
            ylab='PE scaled by length of track [%]'

        if(self.ptype == 'rmspe'):
            ylab='RMS PE [nm]'
            if(self.doMetric): ylab='RMS PE [km]'

        elif(self.ptype == 'vme'):
            ylab='VmaxE [kt]'
            if(self.doMetric): ylab='VmaxE [m/s]'

        elif(self.ptype == 'vbias'):
            ylab='Vmax MeanE(Bias)/AbsMeanE [kt]'
            if(self.doMetric): ylab='Vmax MeanE(Bias)/AbsMeanE [m/s]'

        elif(self.ptype == 'nice'):
            ylab='NICK MeanE(Bias)/AbsMeanE [kt]'
            if(self.doMetric): ylab='NICK MeanE(Bias)/AbsMeanE [m/s]'

        elif(self.ptype == 'pbias'):
            ylab='Pmin(Bias) [mb]'

        elif(self.ptype == 'pod-line'):
            ylab='POD (line) [%]'

        elif(self.ptype == 'pod'):
            ylab='POD (bar) ; POO (line) [%]'

        elif(self.ptype == 'pof'):
            ylab='POF (bar) ; POO (line) [%]'

        elif(self.ptype == 'gainxype'):
            ylab='Gain PE [%]'

        elif(self.ptype == 'gainxyte'):
            ylab='Gain TE [%]'

        elif(self.ptype == 'gainxyfe'):
            ylab='Gain FE [%]'

        elif(self.ptype == 'gainxyfe0'):
            ylab='Gain  [%]'

        elif(self.ptype == 'gainxyte'):
            ylab='Gain  [%]'


        elif(self.ptype == 'pbetter'):
            ylab='% better'
            if(len(taus) == 1):
                ylab="%s tau=%d"%(ylab,taus[0])

        elif(self.ptype == 'gainxyvmax'):
            ylab='Gain VmaxError [%]'

        elif(self.ptype == 'gainxyvbias'):
            ylab='Ratio abs(bias)/mean(abs) [%]'

        elif(self.ptype == 'ct-ate'):
            ylab='CT (track) bias [nm; line]; AT (speed) bias [nm; bar]'
            if(self.doMetric): ylab='CT (track) bias [km; line]; AT (speed) bias [km; bar]'
            
        elif(self.ptype == 'at-cte'):
            ylab='AT (speed) bias [nm; line]; CT (track) bias [nm; bar]'
            if(self.doMetric): ylab='AT (speed bias) [km; line]; CT (speed) bias [km; bar]'

        elif(self.ptype == 'r34e'):
            ylab='R34 fractional area error [%]'

        self.ptitles=(t1,t2,ylab)
        self.xlab=xlab




    def renamemodel(self,ol):

        rol='XXXX'

        if(ol == 'gfsn'): rol='GFS'
        if(ol == 'ecmo'): rol='ECMWF'
        if(ol == 'ukmo'): rol='UKMO'
        if(ol == 'ecmo'): rol='ECMWF'
        if(ol == 'ngps'): rol='NOGAPS'
        if(ol == 'gfdl'): rol='GFDL'
        if(ol == 'ofcl'): rol='OFCL'
        if(ol == 'bcon'): rol='BCON'
        if(ol == 'clip'): rol='CLIPER'
        if(ol == 'egrr'): rol='UKMO'

        return(rol)


    def isundef(self,val,undef=None):

        if(val == None):
            return(1)

        if(undef != None):
            undefs=[undef]
        else:
            undefs=[-999.,999.]
        rc=0
        for undef in undefs:
            if(val == undef): rc=1
        return(rc)


    def iszero(self,val):
        rc=0
        if(fabs(val) == 0): rc=1
        return(rc)


    def smooth(self,x,window_len=10,window='hanning'):
        """smooth the data using a window with requested size.

        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal 
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.

        input:
            x: the input signal 
            window_len: the dimension of the smoothing window
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                flat window will produce a moving average smoothing.

        output:
            the smoothed signal

        example:

        t=linspace(-2,2,0.1)
        x=sin(t)+randn(len(t))*0.1
        y=smooth(x)

        see also: 

        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
        scipy.signal.lfilter

        TODO: the window parameter could be the window itself if an array instead of a string   
        """

        import numpy

        if x.ndim != 1:
            raise ValueError, "smooth only accepts 1 dimension arrays."

        if x.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."


        if window_len<3:
            return x


        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


        s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
        #print(len(s))
        if window == 'flat': #moving average
            w=numpy.ones(window_len,'d')
        else:
            w=eval('numpy.'+window+'(window_len)')

        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len-1:-window_len+1]



    def setControls(self,controlsVar=None):
        
        if(self.ptype == 'pe'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)

        elif(self.ptype == 'pe-line'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,300.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)
        
        elif(self.ptype == 'fe-line'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,200.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)
        
        elif(self.ptype == 'pe-frac'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,30.0,5],lgndloc)

        elif(self.ptype == 'pe-pcnt'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,30.0,5],lgndloc)

        elif(self.ptype == 'pe-imp'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([-250,150,50],lgndloc)

        elif(self.ptype == 'pe-imps'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([-30,20,5],lgndloc)

        elif(self.ptype == 'fe-imp'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([-250,150,50],lgndloc)

        elif(self.ptype == 'fe-imps'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([-30,20,5],lgndloc)

        elif(self.ptype == 'fe-norm'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,700.0,100],lgndloc)

        elif(self.ptype == 'fe'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'te'):
            ptype1='te'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,1000.0,100],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'fe0'):
            ptype1='fe0'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)

        elif(self.ptype == 'pe-fe'):
            ptype1='pe'
            ptype2='fe'
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)
            if(self.doMetric): controls=([0.0,400.0,100],lgndloc)
            
        elif(self.ptype == 'spe'):
            ptype1='spe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,110.0,10],lgndloc)

        elif(self.ptype == 'rmspe'):
            ptype1='pe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)

        elif(self.ptype == 'vme'):
            ptype1='amvme'
            ptype2='mvme'
            lgndloc=0
            controls=([-50.0,50.0,10.0],lgndloc)

        elif(self.ptype == 'vbias'):
            ptype1='mvme'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)
            if(self.doMetric): controls=([-25.0,35.0,10.0],lgndloc)

        elif(self.ptype == 'nice'):
            ptype1='nice'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'pbias'):
            ptype1='pmin'
            ptype2=ptype1
            lgndloc=2
            controls=([-50.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'pod'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)
            
        elif(self.ptype == 'pod-line'):
            ptype1='pods'
            ptype2='pods'
            lgndloc=2
            controls=([0.0,125.0,25],lgndloc)
        

        elif(self.ptype == 'pof'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)

        elif(self.ptype == 'gainxype'):
            ptype1='gainxype'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)

        elif(self.ptype == 'gainxyte'):
            ptype1='gainxyte'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyte'):
            ptype1='gainxyte'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
            
        elif(self.ptype == 'gainxyfe0'):
            ptype1='gainxyfe0'
            ptype2=ptype1
            lgndloc=0
            controls=([-10.0,30.0,5.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
        
        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-50.0,50.0,10.0],lgndloc)
            if(self.doMetric): controls=([-60.0,90.0,15.0],lgndloc)
        
            
        elif(self.ptype == 'pbetter'):
            ptype1=self.ptype
            ptype2=ptype1
            lgndloc=0
            controls=([0.0,110.0,10.0],lgndloc)

        elif(self.ptype == 'gainxyvmax'):
            ptype1='gainxyvmax'
            ptype2=ptype1
            lgndloc=2
            controls=([-70.0,70.0,10.0],lgndloc)

        elif(self.ptype == 'gainxyvbias'):
            ptype1='gainxyvbias'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,120.0,10.0],lgndloc)

        elif(self.ptype == 'ct-ate'):
            ptype1='mcte'
            ptype2='mate'
            lgndloc=2
            controls=([-200.0,200.0,50.0],lgndloc)
            if(self.doMetric): controls=([-300.0,300.0,50.0],lgndloc)

        elif(self.ptype == 'at-cte'):
            ptype1='mate'
            ptype2='mcte'
            lgndloc=2
            controls=([-200.0,200.0,50.0],lgndloc)
            if(self.doMetric): controls=([-300.0,300.0,50.0],lgndloc)

        elif(self.ptype == 'r34e'):
            ptype1='r34e'
            ptype2='r34bt'
            lgndloc=0
            controls=([-200.0,200.0,25.0],lgndloc)

        else:
            print 'EEE invalid plot ptype in PlotsumStat: ',self.ptype
            sys.exit()

        if(controlsVar != None): controls=controlsVar
        self.controls=controls

    def setbarlineprops(self,n,np,pvartagopt=None):

        lstyle='-'
        wline=2.0

        if(pvartagopt == '00_12zv06_18z'):
            if(n%2 == 0):
                alphabar=alphaline=0.75
                lstyle='-'
            else:
                alphabar=alphaline=1.0
                lstyle=':'

        if(np >= 4):
            if(n%2 == 0):
                alphabar=alphaline=0.5
                lstyle=':'
            else:
                alphabar=alphaline=1.0
                lstyle='-'

        if(np == 4 and pvartagopt == '00_06_12_18z'):
            if(n == 3):
                alphabar=alphaline=0.25
                lstyle='-'
            elif(n == 2):
                alphabar=alphaline=0.5
                lstyle=':'
            elif(n == 1):
                alphabar=alphaline=0.75
                lstyle='-'
            elif(n == 0):
                alphabar=alphaline=1.0
                lstyle=':'

        if(pvartagopt == '00_12z'):
            if(n%2 == 0):
                alphabar=alphaline=1.0
                lstyle='-'
            else:
                alphabar=0.5
                alphaline=1.0
                lstyle=':'

        else:
            if(n%2 == 0):
                alphabar=alphaline=1.0
                lstyle='-'
            else:
                alphaline=1.0
                alphabar=1.0
                alphabar=0.85
                lstyle=':'
                lstyle='-'
                lstyle='--'


        return(lstyle,wline,alphabar,alphaline)


    def simpleplot2axis(self,
                        models,
                        dicts,
                        cnts,
                        labels,
                        irowc=None,
                        irowt=None,
                        irowl=None,
                        irowll=None,
                        do1stplot=1,
                        do2ndplot=0,
                        ilstyle=None,
                        ilwidth=None,
                        ilmarker=None,
                        ialphaline=None,
                        ialphabar=None,
                        reversedirection=0,
                        dopng=0,doeps=0,doxv=0,dopdf=0,
                        useroverride=0,
                        doshow=0,
                        verb=0,
                        dotable=1,
                        countonly=0,
                        docp=0,
                        domodelrename=0,
                        do2ndval=0,
                        doline=0,
                        doErrBar=1,
                        undef=-999,
                        ):
        
        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

        from WxMAP2 import W2
        w2=W2()

        self.do2ndval=do2ndval
        
        def ispvar1eqpvar2(taus,dict1,dict2):

            rc=0
            for nt in range(0,len(taus)):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]
                if(val1 != val2):
                    rc=1
                    break

            return(rc)


        def draw0line(lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0
            P.plot(x,y,color=lcol,linewidth=2.00)

        def drawCritline(critvalue,lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0 + critvalue
            P.plot(x,y,color=lcol,linewidth=2.00)


        def adjustxaxis(n,xaxis,barwidth,dxofffraction,center=0):

            pbarwidth=barwidth*dxofffraction
            dxoffplus=(pbarwidth-barwidth)*0.5

            if(center):
                xoff=0.0 - (barwidth*n) + dxoffplus
            else:
                xoff=0.5 - (barwidth*n) + dxoffplus

            for i in range(0,len( xaxis)):
                xaxis[i]=xaxis[i] - xoff + xshift - dxoffplus*0.5



        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # main def section
        #
        # -- force use of non-interactive backend
        #
        import matplotlib
        matplotlib.use('agg')

        from pylab import arange
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        from natsort import natsorted
        import matplotlib.patches as mpatch
        #
        C2hex=w2Colors().chex

        # setup input
        #

        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]
        

        (t1,t2,ylab)=self.ptitles
        xlab=self.xlab
        
        (ylim,lgndloc)=self.controls

        # -- 20221011 -- crude way to control yticks
        #
        if(len(ylim) == 3):
            yb=ylim[0]
            ye=ylim[1]
            dy=ylim[2]
            yts=arange(yb,ye,dy)
        else:
            yts=ylim[0:-1]
            yb=ylim[0]
            ye=ylim[-1]
        

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        taus=cnts[0].keys()
        
        # -- use natsort module to handle strings
        #
        taus=natsorted(taus)
        

        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy') and self.ptype != 'gainxyfe0'):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1


        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        xaxisTs=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]

        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            cnt=cnts[n]
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]
            xaxisT=[]

            nxpts=nts
            if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]
                if(verb): print 'nnn',nt,tau,val1,val2

                if(len(dict1[tau]) > 2):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=''
                    cval1=''
                else:
                    row1.append(val1)
                    xval1=0.5+(nt-1)
                    xaxis.append(xval1)
                    xaxisT.append(int(tau))

                if(self.isundef(val2) or nc == 0):
                    val2=''
                    cval2=''
                else:
                    row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            vals1.append(row1)
            vals2.append(row2)
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)
            xaxisTs.append(xaxisT)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        np=len(vals1)

        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        #  pylab 
        #

        params = {
            'axes.labelsize': 12,
            'font.size': 10,
            'legend.fontsize': 9,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }



        xydim=(10.5,8.25)
        fig, ax = plt.subplots(figsize = xydim)
        
        mpl.rcParams.update(params)
        ax2 = ax.twinx()
        
        lgndc=[]

        xtaus=[]
        ycnts=[]
        
        for tau in taus:
            if(mf.find(tau,'all')):  
                continue
            else:                    
                itau=int(tau)
                ycnt=cnts[0][tau]
                ycnts.append(ycnt)
                xtaus.append(itau)

        if(verb):
            print 'XXXTTT',xtaus
            print 'CCCCCC',ycnts

        for n in range(0,np):

            ys=vals1[n]
            xaxisT=copy.copy(xaxisTs[n])
            if(verb):
                print 'xxxx',n,xaxisT
                print 'yyyy',n,ys
                 
            rc=ax.plot(xaxisT,ys,
                       color=rowc[n],
                       linestyle=lstyle[n],
                       marker=lmarker[n],
                       linewidth=lwidth[n],
                       alpha=alphaline[n]
                       )

        rc=ax2.bar(xtaus,ycnts,
                   width=0.9,
                   color='grey',
                   )
        
        ax2.set_ylabel('N',fontsize=15)
        ax2.set_ylim(0,2000)
        ax2.set_yticks([0,50,100,200])
        ax2.grid()
        
        if(self.ptype == 'pe-line' or self.ptype == 'fe-line' or self.ptype == 'pod-line'):
                ax.legend(olabels, loc=lgndloc, shadow=True, markerscale=0.2)



        ax.set_xlim(xtaus[0]-0.7,xtaus[-1]+0.7)
        ax.set_ylim(yb,ye)
        ax.set_yticks(yts)

        fig.suptitle(t1,fontsize=13)
        ax.set_title(t2,size=8)

        ax.set_ylabel(ylab,fontsize=15)
        if(xlab != None): ax.set_xlabel(xlab,fontsize=15)

        ax.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            fig.savefig(pngpath)
            print 'PPP-pngpath: ',pngpath,doshow


        if(doeps):
            print 'EEE-epspath: ',epspath
            fig.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            P.savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng and w2.onKishou and w2.curuSer == 'fiorino'):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox/PLOTS'
            cmd="cp -p %s %s"%(pngpath,tdir)
            mf.runcmd(cmd,ropt)

    # -- plot method
    #

    def cformatVal(self,val1,val2,nc,diffv1v2=0,countonly=0):

        cval1=''
        
        if(val1 != ''):
            if(countonly):
                cval1="%d"%(nc)
            else:
                cval1="%4.0f[%d]"%(val1,nc)
                
        if(val1 != '' and val2 != '' and self.do2ndval != 0):
            if(countonly):
                cval1="%d"%(nc)
            else:
                if(self.do2ndval == -1):
                    cval1="%4.0f;%4.0f[%d]"%(val2,val1,nc)
                else:
                    cval1="%4.0f;%4.0f[%d]"%(val1,val2,nc)

        return(cval1)

    def simpleplot(self,
                   models,
                   dicts,
                   cnts,
                   labels,
                   irowc=None,
                   irowt=None,
                   irowl=None,
                   irowll=None,
                   do1stplot=1,
                   do2ndplot=0,
                   ilstyle=None,
                   ilwidth=None,
                   ilmarker=None,
                   ialphaline=None,
                   ialphabar=None,
                   reversedirection=0,
                   dopng=0,doeps=0,doxv=0,dopdf=0,
                   useroverride=0,
                   doshow=0,
                   verb=0,
                   dotable=1,
                   countonly=0,
                   docp=0,
                   domodelrename=0,
                   do2ndval=0,
                   doline=0,
                   doErrBar=1,
                   undef=-999,
                   ):

        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

        from WxMAP2 import W2
        w2=W2()

        self.do2ndval=do2ndval
        
        def ispvar1eqpvar2(taus,dict1,dict2):

            rc=0
            for nt in range(0,len(taus)):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]
                if(val1 != val2):
                    rc=1
                    break

            return(rc)


        def draw0line(lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0
            P.plot(x,y,color=lcol,linewidth=2.00)

        def drawCritline(critvalue,lcol='b'):
            minx, maxx = FP.get_xlim()
            x=P.arange(minx,maxx+1.0,1.0)
            y=x*0.0 + critvalue
            P.plot(x,y,color=lcol,linewidth=2.00)


        def adjustxaxis(n,xaxis,barwidth,dxofffraction,center=0):

            pbarwidth=barwidth*dxofffraction
            dxoffplus=(pbarwidth-barwidth)*0.5

            if(center):
                xoff=0.0 - (barwidth*n) + dxoffplus
            else:
                xoff=0.5 - (barwidth*n) + dxoffplus

            for i in range(0,len( xaxis)):
                xaxis[i]=xaxis[i] - xoff + xshift - dxoffplus*0.5



        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # main def section
        #
        # -- force use of non-interactive backend
        #
        import matplotlib
        matplotlib.use('agg')

        from pylab import arange
        import pylab as P
        from natsort import natsorted
        
        import matplotlib.patches as mpatch
        # -- moved to w2base.py from VT.py
        #
        C2hex=w2Colors().chex

        # setup input
        #

        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]
        

        (t1,t2,ylab)=self.ptitles
        xlab=self.xlab
        
        (ylim,lgndloc)=self.controls

        # -- 20221011 -- crude way to control yticks
        #
        if(len(ylim) == 3):
            yb=ylim[0]
            ye=ylim[1]
            dy=ylim[2]
            yts=arange(yb,ye,dy)
        else:
            yts=ylim[0:-1]
            yb=ylim[0]
            ye=ylim[-1]
        

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        taus=cnts[0].keys()
        
        # -- use natsort module to handle strings
        #
        taus=natsorted(taus)
        

        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy') and self.ptype != 'gainxyfe0'):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1


        vals1=[]
        vals2=[]
        
        v1mins=[]
        v2mins=[]
        
        v1ptl25s=[]
        v2ptl25s=[]
        
        v1medians=[]
        v2medians=[]
        
        v1ptl75s=[]
        v2ptl75s=[]

        v1ptl90s=[]
        v2ptl90s=[]

        v1maxs=[]
        v2maxs=[]

        xaxiss=[]
        cvals=[]
        rowc=[]
        
        if(irowt == None): rowt=[]
        if(irowl == None): rowl=[]
        if(irowll == None): rowll=[]
        if(ilstyle == None): lstyle=[]
        if(ilwidth == None): lwidth=[]
        if(ilmarker == None): lmarker=[]
        if(ialphaline == None): alphaline=[]
        if(ialphabar == None): alphabar=[]

        olabels=[]

        for n in range(0,nrows):

            (dict1,dict2)=dicts[n]
            
            cnt=cnts[n]
            
            ol=labels[n]

            if(domodelrename):
                nol=len(ol)
                if(ol[nol-2:nol] == '06'):
                    ol=ol[0:nol-2]
                ol=renamemodel(ol)

            olabels.append(ol)

            diffv1v2=ispvar1eqpvar2(taus,dict1,dict2)

            row1=[]
            row2=[]
            crow=[]
            
            row1minv=[]
            row2minv=[]
            
            row1ptl25=[]
            row2ptl25=[]

            row1median=[]
            row2median=[]
            
            row1ptl75=[]
            row2ptl75=[]
            
            row1ptl90=[]
            row2ptl90=[]
            
            row1maxv=[]
            row2maxv=[]
            
            nts=len(taus)

            xaxis=[]

            nxpts=nts
            if(doline): nxpts=nts-1
            
            for nt in range(0,nxpts):

                tau=taus[nt]

                val1=dict1[tau][0]
                val2=dict2[tau][0]

                if(len(dict1[tau]) > 2):

                    #doErrBar=0
                    v1min=dict1[tau][2]
                    v2min=dict1[tau][2]

                    v1ptl25=dict1[tau][3]
                    v2ptl25=dict1[tau][3]

                    v1median=dict1[tau][4]
                    v2median=dict1[tau][4]

                    v1ptl75=dict1[tau][5]
                    v2ptl75=dict1[tau][5]

                    v1ptl90=dict1[tau][6]
                    v2ptl90=dict1[tau][6]

                    v1max=dict1[tau][7]
                    v2max=dict1[tau][7]

                else:

                    v1min=undef
                    v2min=undef

                    v1ptl25=undef
                    v2ptl25=undef

                    v1median=undef
                    v2median=undef

                    v1ptl75=undef
                    v2ptl75=undef

                    v1ptl90=undef
                    v2ptl90=undef

                    v1max=undef
                    v2max=undef


                if(reversedirection):
                    val1=-val1
                    val2=-val2
                    v1min=-v1min
                    v2min=-v2min
                    v1ptl25=-v1ptl25
                    v2ptl25=-v2ptl25
                    v1med=-v1med
                    v2med=-v2med
                    v1ptl75=-v1ptl75
                    v2ptl75=-v2ptl75
                    v1ptl90=-v1ptl90
                    v2ptl90=-v2ptl90
                    v1max=-v1max
                    v2max=-v2max

                nc=cnt[tau]
                
                if(self.isundef(val1) or nc == 0):
                    val1=''
                    cval1=''
                else:
                    row1.append(val1)
                    xval1=0.5+(nt-1)
                    xaxis.append(xval1)

                if(self.isundef(val2) or nc == 0):
                    val2=''
                    cval2=''
                else:
                    row2.append(val2)

                cval1=self.cformatVal(val1,val2,nc)
                crow.append(cval1)
                
                row1minv.append(v1min)
                row2minv.append(v2min)

                row1ptl25.append(v1ptl25)
                row2ptl25.append(v2ptl25)
                
                row1median.append(v1median)
                row2median.append(v2median)
                
                row1ptl75.append(v1ptl75)
                row2ptl75.append(v2ptl75)
                
                row1ptl90.append(v1ptl90)
                row2ptl90.append(v2ptl90)

                row1maxv.append(v1max)
                row2maxv.append(v2max)
                

            vals1.append(row1)
            vals2.append(row2)
            
            v1mins.append(row1minv)
            v2mins.append(row2minv)

            v1ptl25s.append(row1ptl25)
            v2ptl25s.append(row2ptl25)

            v1medians.append(row1median)
            v2medians.append(row2median)

            v1ptl75s.append(row1ptl75)
            v2ptl75s.append(row2ptl75)

            v1ptl90s.append(row1ptl90)
            v2ptl90s.append(row2ptl90)

            v1maxs.append(row1maxv)
            v2maxs.append(row2maxv)

            cvals.append(crow)
            xaxiss.append(xaxis)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n].upper())
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            mcolt=C2hex['grey1']
            
            if(irowt == None): rowt.append(mcolt)

            (sline,wline,abar,aline)=self.setbarlineprops(n,nrows,self.pvartagopt)

            if(irowc == None): rowc.append(mcol)
            if(irowc != None):
                ccol=C2hex[irowc[n]]
                rowc.append(ccol)
            if(ilstyle == None): lstyle.append(sline)
            if(ilmarker == None): lmarker.append('d')
            if(ilwidth == None): lwidth.append(wline)
            if(ialphaline == None): alphaline.append(aline)
            if(ialphabar == None): alphabar.append(abar)




        ctaus=[]
        ctausblank=[]
        for tau in taus:
            if(type(tau) is IntType):
                ctaus.append("%3dh"%(tau))
            else:
                ctaus.append(tau.split('.')[0])
            ctausblank.append('')


        np=len(vals1)

        if(irowl != None): rowl=irowl
        if(ilstyle != None): lstyle=ilstyle
        if(ilmarker != None): lmarker=ilmarker
        if(ilwidth != None): lwidth=ilwidth
        if(ialphaline != None): alphaline=ialphaline
        if(ialphabar != None): alphabar=ialphabar


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        #  pylab 
        #

        params = {
            'axes.labelsize': 12,
            'font.size': 10,
            'legend.fontsize': 9,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }



        P.rcParams.update(params)


        xydim=(10.5,8.25)
        F=P.figure(figsize=xydim)

        leftsubplot=0.10
        bottomsubplot=0.15
        if(np > 6):
            bottomsubplot=0.20

        F.subplots_adjust(top=0.9,bottom=bottomsubplot,left=leftsubplot,right=0.95,wspace=0.0,hspace=0.0)

        FP=F.add_subplot(111)

        lgndc=[]

        #
        # setup bars
        #

        dxofffraction=1.0
        dxofffraction=1.25

        barscale=0.8

        if(np == 1):
            dxofffraction=1.0


        barwidth=barscale/np
        pbarwidth=barwidth*dxofffraction
        xshift=(1.0-barscale)*0.5
        boxbarwidth=pbarwidth*0.50
        errbarwidth=boxbarwidth*0.75
        errcapsize=errbarwidth*25

        if(dxofffraction >= 1.5):
            alphabar=0.75


        for n in range(0,np):

            ys=vals1[n]
            ymedian=v1medians[n]
                
            xaxisl=copy.copy(xaxiss[n])
            xaxisb=copy.copy(xaxiss[n])
            if(verb): print 'XXXLLL',xaxisl,ys
            
            if(do1stplot):
                #adjustxaxis(n,xaxisl,barwidth,dxofffraction,center=1)
                rc=FP.plot(xaxisl,ys,
                           color=rowc[n],
                           linestyle=lstyle[n],
                           marker=lmarker[n],
                           linewidth=lwidth[n],
                           alpha=alphaline[n]
                           )
                if(self.ptype == 'pe-line' or self.ptype == 'fe-line' or self.ptype == 'pod-line'):
                    FP.legend(olabels, loc=lgndloc, shadow=True, markerscale=0.2)


            if(do2ndplot > 0):

                if(do2ndplot == 2):
                    doline=1

                ys=vals2[n]
                for j in range(0,len(ymedian)):
                    ymedian[j]=v1medians[n][j]

                if(doline):
                    rc=FP.plot(xaxisl,ys,
                               color=rowc[n],
                               linestyle='--',
                               marker=lmarker[n],
                               linewidth=lwidth[n],
                               alpha=1.0
                               )
                else:

                    rcBB=None
                    
                    if(len(ys) != len(xaxisl)): doErrBar=0
                    adjustxaxis(n,xaxisb,barwidth,dxofffraction)
                    
                    if(doErrBar):

                        yBBbot=v2ptl25s[n]
                        yBBtop=v2ptl75s[n]
                        ymax=v2maxs[n]
                        ymin=v2mins[n]
                        ymed=v2medians[n]
                        
                        ysBBrange=[]
                        
                        yBoxMedian=[]
                        
                        yerrMM=[]
                        yerrCenter=[]

                        yboxCenter=[]
                        yboxMM=[]
                        
                        yerrLowCenter=[]
                        yerrLowMM=[]
                        
                        yerrUpCenter=[]
                        yerrUpMM=[]

                        xaxisBB=copy.copy(xaxisb)
                        xaxisEB=copy.copy(xaxisb)
                        xaxisBBrange=[]
                        
                        lenX=len(xaxisBB)
                        for j in range(0,lenX):
                            xBB=xaxisBB[j]
                            x0BB=xBB+(pbarwidth-boxbarwidth)*0.5
                            x1BB=boxbarwidth
                            xaxisBBrange.append((x0BB,x1BB))
                            xaxisEB[j]=xaxisEB[j]+pbarwidth*0.5
                            #print 'xBB',j,xBB,xaxisBBrange[j],xaxisEB[j]
                            
                        lenY=len(row1median)
                        
                        for j in range(0,lenY):
                            
                            if(ymin[j] != undef):
                                
                                y0BB=yBBbot[j]
                                y1BB=yBBtop[j]-yBBbot[j]   
                                
                                if(ymed[j] == -999):
                                    y0BB=undef
                                    y1BB=undef
                                
                                ysBBrange.append((y0BB,y1BB))
    
                                yboxL=y1BB*0.5
                                yboxC=y0BB+yboxL
                                
                                if(ymed[j] == -999):
                                    yboxC=undef
                                    yboxL=undef
                                
                                yboxCenter.append(yboxC)
                                yboxMM.append(yboxL)
                                
                                yerrL=(ymax[j]-ymin[j])*0.5
                                yerrC=ymin[j]+yerrL
                                
                                if(ymed[j] == -999):
                                    yerrC=undef
                                    yerrL=undef
                                
                                yerrCenter.append(yerrC)
                                yerrMM.append(yerrL)
    
                                yerrLowL=(y0BB-ymin[j])*0.5
                                yerrLowC=ymin[j]+yerrLowL

                                if(ymed[j] == -999):
                                    yerrLowC=undef
                                    yerrLowL=undef

                                yerrLowCenter.append(yerrLowC)
                                yerrLowMM.append(yerrLowL)
                                
                                yerrUpL=(ymax[j]-yBBtop[j])*0.5
                                yerrUpC=yBBtop[j]+yerrUpL
                                
                                if(ymed[j] == -999):
                                    yerrUpC=undef
                                    yerrUpL=undef
                                    
                                yerrUpCenter.append(yerrUpC)
                                yerrUpMM.append(yerrUpL)
                                
                                yBoxMedian.append(ymed[j])
                                
                        nBB=len(xaxisBBrange)
                        
                        for j in range(0,nBB):
                            xBBs=[xaxisBBrange[j]]
                            xBBs1=[(xaxisb[j],pbarwidth)]
                            yBB=ysBBrange[j]
                            rcBB=FP.broken_barh(xBBs1,(0,ys[j]),facecolor=rowc[n],alpha=alphabar[n])
                            rcBB2576=FP.broken_barh(xBBs,yBB,alpha=0.5,facecolor=rowc[n],edgecolor='black',linewidth=1.0)

                        #rc=FP.errorbar(xaxisEB,yerrCenter,yerr=yerrMM,linestyle='None',capthick=2,capsize=errcapsize,
                        #               elinewidth=0.5,alpha=0.75,
                        #               ecolor=rowc[n])
                        
                        rcEB=FP.errorbar(xaxisEB,yBoxMedian,xerr=boxbarwidth*0.5,linestyle='None',capthick=0,capsize=errcapsize,
                                       elinewidth=2,
                                       ecolor='black')

                        rcEB=FP.errorbar(xaxisEB,yerrLowCenter,yerr=yerrLowMM,linestyle='None',capthick=0.5,capsize=errcapsize,
                                       elinewidth=0.5,
                                       ecolor='black')

                        rcEB=FP.errorbar(xaxisEB,yerrUpCenter,yerr=yerrUpMM,linestyle='None',capthick=0.5,capsize=errcapsize,
                                       elinewidth=0.5,alpha=0.5,
                                       ecolor='black')

                        #rc=FP.errorbar(xaxisEB,yboxCenter,yerr=yboxMM,linestyle='None',capthick=0,capsize=errcapsize,
                        #               elinewidth=1,alpha=1.0,
                        #               ecolor=rowc[n])
                            
                        
                        barpatch = mpatch.Rectangle((0, 0), 1, 1, fc=rowc[n])
                        lgndc.append(barpatch)
               
                        if(n == np-1):
                            FP.legend(lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

                    else:

                        rc=FP.bar(xaxisb,ys,
                                  align='edge',
                                  color=rowc[n],
                                  width=pbarwidth,
                                  alpha=alphabar[n])

                        barpatch = mpatch.Rectangle((0, 0), 1, 1, fc=rowc[n])
                        lgndc.append(barpatch)
                        
                        if(n == np-1):
                            FP.legend(lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

        # -- table
        #
        if(dotable):

            if(verb):
                print 'rowl: ',rowl
                print 'rowc: ',rowc
                for  i in range(0,len(cvals)):
                    print 'cvals',i,cvals[i]

            TT=P.table(cellText=cvals,loc='bottom',
                       cellLoc='center',
                       rowLabels=rowll,rowColours=rowt,
                       colLabels=ctaus)

            TT.set_fontsize(8)

            P.xticks(xaxis,ctausblank)


        # -- lineplot labels
        else:

            xaxisp=[]
            ctausp=[]
            
            nxpts=len(xaxis)
            if(nxpts >= 40):
                xint=5
            elif(nxpts >=30 and nxpts < 40):
                xint=4
            elif(nxpts >= 20 and nxpts < 30):
                xint=3
            elif(nxpts >= 10 and nxpts < 20):
                xint=2
            elif(nxpts < 10):
                xint=1

            for i in range(0,nxpts,xint):
                xaxisp.append(xaxis[i])
                
                # -- the last point is 'allyears' set to penultimate point
                #
                #if(i == nxpts-1):
                #    i=nxpts-2
                ctausp.append(ctaus[i])
                
            P.xticks(xaxisp,ctausp)

        if(self.ptype == 'vme' or self.ptype == 'ct-ate' or self.ptype == 'at-cte' or \
           self.ptype == 'vbias' or self.ptype == 'pbias' or mf.find(self.ptype,'gainxy')):
            draw0line(lcol='k')

        if(self.ptype == 'pod' or self.ptype == 'pof'):
            drawCritline(100.0,lcol='k')

        elif(self.ptype == 'pbetter'):
            drawCritline(50.0,lcol='k')

        elif(self.ptype == 'pod-line'):
            None
            #drawCritline(100.0,lcol='k')
            #drawCritline(95.0,lcol='k')


        #P.xlim(-1.0,len(taus)-1)
        P.xlim(-1.0,nxpts-1)
        P.ylim(yb,ye)
        P.yticks(yts)

        P.suptitle(t1,fontsize=13)
        P.title(t2,size=8)

        P.ylabel(ylab,fontsize=15)
        if(xlab != None): P.xlabel(xlab,fontsize=15)

        P.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            P.savefig(pngpath)
            print 'PPP-pngpath: ',pngpath,doshow


        if(doeps):
            print 'EEE-epspath: ',epspath
            P.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            P.savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng and w2.onKishou and w2.curuSer == 'fiorino'):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox/PLOTS'
            cmd="cp -p %s %s"%(pngpath,tdir)
            mf.runcmd(cmd,ropt)

    # -- plot method
    #

    def cformatVal(self,val1,val2,nc,diffv1v2=0,countonly=0):

        cval1=''
        
        if(val1 != ''):
            if(countonly):
                cval1="%d"%(nc)
            else:
                cval1="%4.0f[%d]"%(val1,nc)
                
        if(val1 != '' and val2 != '' and self.do2ndval != 0):
            if(countonly):
                cval1="%d"%(nc)
            else:
                if(self.do2ndval == -1):
                    cval1="%4.0f;%4.0f[%d]"%(val2,val1,nc)
                else:
                    cval1="%4.0f;%4.0f[%d]"%(val1,val2,nc)

        return(cval1)


class Vdeck(MFutils):



    def __init__(self,etau=120,dtau=12,
                 verirule='std',
                 veritype='long',
                 ):

        from WxMAP2 import W2
        w2=W2()
        self.w2=w2

        self.veritype=veritype
        self.verirule=verirule
        self.HomoVDdics=HomoVDdics
        self.SimpleListStats=SimpleListStats


        self.undef=1e20
        self.etau=etau
        self.dtau=dtau
        
        self.bdtg={}
        self.vdtg={}

        self.pe={}
        self.cte={}
        self.ate={}
        self.vme={}
        self.pmine={}

        self.btYN={}
        self.tcYN={}
        self.warnYN={}
        self.cpacYN={}

        self.fcrunYN={}
        self.fctrkYN={}
        self.fcvmYN={}
        self.pod={}
        self.vflag={}

        self.blf={}
        self.flf={}
        self.tdo={}

        self.btr34={}
        self.btr50={}
        self.btlat={}
        self.btlon={}
        self.btvmax={}
        self.btpmin={}

        self.fcr34={}
        self.fcr50={}
        self.fclat={}
        self.fclon={}
        self.fcvmax={}
        self.fcpmin={}

        self.taus=range(0,etau+1,dtau)

        for tau in self.taus:

            self.bdtg[tau]=[]
            self.vdtg[tau]=[]

            self.pe[tau]=[]
            self.cte[tau]=[]
            self.ate[tau]=[]

            self.vme[tau]=[]
            self.pmine[tau]=[]

            self.blf[tau]=[]
            self.flf[tau]=[]

            self.btYN[tau]=[]
            self.tcYN[tau]=[]
            self.warnYN[tau]=[]

            self.fcrunYN[tau]=[]
            self.fctrkYN[tau]=[]
            self.fcvmYN[tau]=[]
            
            self.cpacYN[tau]=[]

            self.pod[tau]=[]
            self.vflag[tau]=[]

            self.tdo[tau]=[]

            self.btlat[tau]=[]
            self.btlon[tau]=[]
            self.btvmax[tau]=[]
            self.btpmin[tau]=[]
            self.btr34[tau]=[]
            self.btr50[tau]=[]

            self.fclat[tau]=[]
            self.fclon[tau]=[]
            self.fcvmax[tau]=[]
            self.fcpmin[tau]=[]
            self.fcr34[tau]=[]
            self.fcr50[tau]=[]


        self.lf=self.w2.SetLandFrac()


    def IsAidStarthh(self,hh,aidshh,aidsdt):
        aidhhs=range(aidshh,aidshh+24,aidsdt)
        for aidhh in aidhhs:
            if(aidhh == hh):
                return(1)
        return(0)

    def TcState(self,fldic,bvmax):

        if(bvmax == -99.9):
            istc=0
            iswarn=0
            isbt=0
            tsnum=-99
            tcstate='  '
            tcwarn='  '
            tcYN=' '

        else:
            tsnum=fldic[6]
            tcYN=fldic[0]
            tcstate=fldic[1]
            tcwarn=fldic[3]
            istc=IsTc(tcstate)
            # -- gooned up indicator from mdeck XX
            if(istc == -1):
                istc=IsTcWind(bvmax)
            iswarn=IsWarn(tcwarn)
            isbt=0
            if(tsnum != -1): isbt=1

        #
        # undef
        #
        return(istc,isbt,iswarn,tsnum,tcstate,tcwarn)

    def FcTrkState(self,flat):

        if(flat > -88.8 and flat < 88.8):
            rc=1 
        else:   
            rc=0    
        return(rc)
        

    def FcVmState(self,flat):

        if(flat > -88.8 and flat < 88.8):
            rc=1
        else:
            rc=0
        return(rc)
        

    def VmaxState(self,vmax,vmaxLim=180.0):

        if(vmax > 0.0 and vmax < vmaxLim):
            rc=1
        else:
            rc=0
        return(rc)
        

    def BtState(self,blat):

        if(blat > -88.8 and blat < 88.8):
            rc=1
        else:
            rc=0
        return(rc)
        

    def PodState(self,isfc,isveri,iswarn=None):
        """vflag below just tells if var should be included in mean
pod contains more... if should be verified and if the model made a forecast
total number of verifying positions is sum abs(rc) >= 1 or == 2 (veriwarn=1 or only verifying posits in warning) """
        
        rc=0
        if(isveri == 1 and isfc == 1): rc=1
        if(isveri == 1 and isfc != 1): rc=-1
        if(isveri != 1 and isfc == 1): rc=999
        if(isveri == 1 and isfc == 1 and (iswarn != None and iswarn == 1)): rc=2
        if(isveri == 1 and isfc != 1 and (iswarn != None and iswarn == 1)): rc=-2

        return(rc)

    def VflagState(self,isfc,isveri,iswarn=None):
        """vflag just tells if var should be included in mean... not too useful...
"""

        rc=0
        if(isveri == 1 and isfc == 1): rc=1
        if(isveri == 1 and isfc == 1 and (iswarn != None and iswarn == 1)): rc=2
        
        return(rc)

    def GetLF(self,lat,lon):
        
        landfrac=self.w2.GetLandFrac(self.lf,lat,lon)
        return(landfrac)

    def GetCpac(self,lat,lon):
        iscpac=0
        if(self.FcTrkState(lat) and (lat > 0.0) and (lon > 180.0 and lon <= 220.0)): iscpac=1
        return(iscpac)


    def PrintVar(self,hash,format='%3s'):
        taus=hash.keys()
        taus.sort()
        
        card="Bdtg\Taus:"
        if(mf.find(format,'f')):
            lovar=len(format%(0.0))
        else:
            lovar=len(format%(' '))

        otauformat=' %'+"%dd"%(lovar)
        for tau in taus:
            otau=otauformat%(tau)
            card="%s %s"%(card,otau)

        print card

        cards={}
        for tau in taus:
            lt=len(hash[tau])
            if(lt > 0):
                for i in range(0,lt):
                    if(tau == taus[0]):
                        ivar=hash[tau][i]
                        if(mf.find(format,'f')): ivar=float(ivar)
                        if(ivar == self.undef):
                            ovar=len(format%(0.0))*'*'
                        else:
                            ovar=format%(ivar)
                        cards[i]="%s %5s"%(self.bdtg[tau][i],ovar)
                    else:
                        try:
                            ivar=hash[tau][i]
                            if(mf.find(format,'f')): ivar=float(ivar)
                            if(ivar == self.undef):
                                ovar=len(format%(0.0))*'*'
                            else:
                                ovar=format%(ivar)
                            cards[i]="%5s  %s"%(cards[i],ovar)
                        except:
                            print 'bad ',tau,i


        kks=cards.keys()
        kks.sort()
        for kk in kks:
            print cards[kk]

    def GetVDVarlist(self,var,tau,verb=0):

        list=[]
        for i in range(0,self.ndtgs):

            rc=[]
            # 20130731 -- for times when trying to get tau > 120
            try:
                rc.append([self.vflag[tau][i],self.bdtg[tau][i],self.stmid,self.btvmax[tau][i]])
            except:
                continue
            
            if(var == 'pod'):
                rc.append(self.pod[tau][i])

            elif(var == 'bdtg'):
                rc.append(self.bdtg[tau][i])

            elif(var == 'btlat'):
                rc.append(self.btlat[tau][i])

            elif(var == 'btlon'):
                if(hasattr(self,'btlon')):
                    rc.append(self.btlon[tau][i])
                else:
                    btdtg=self.bdtg[tau][i]
                    vdtg=mf.dtginc(btdtg,tau)
                    print 'vvvvvv ',vdtg
                    rc.append(None)
                    #self.BT.ls()

            elif(var == 'fclat'):
                rc.append(self.fclat[tau][i])

            elif(var == 'fclon'):
                rc.append(self.fclon[tau][i])

            elif(var == 'pe'):
                rc.append(self.pe[tau][i])

            elif(var == 'fe'):
                rc.append(self.FE[tau][i])

            elif(var == 'fe0'):
                rc.append(self.FE0[tau][i])

            elif(var == 'te'):
                rc.append(self.TE[tau][i])

            elif(var == 'cte'):
                rc.append(self.cte[tau][i])

            elif(var == 'ate'):
                rc.append(self.ate[tau][i])

            elif(var == 'btvmax'):
                rc.append(self.btvmax[tau][i])

            elif(var == 'btpmin'):
                rc.append(self.btpmin[tau][i])

            elif(var == 'fcvmax'):
                rc.append(self.fcvmax[tau][i])

            elif(var == 'fcpmin'):
                rc.append(self.fcpmin[tau][i])

            elif(var == 'vme'):
                rc.append(self.vme[tau][i])

            elif(var == 'pmine'):
                rc.append(self.pmine[tau][i])

            list.append(rc)
            if(verb):
                print 'VDvar ',var,i,rc

        return(list)


    def lsFE(self,bdtgs,tau=72):

        print
        print 'lsFE ',self.aid,self.stmid,'tau: ',tau
        pes=self.pe[tau]
        n=0
        for pe in pes:
            bdtg=self.bdtg[tau][n]
            vdtg=mf.dtginc(bdtg,tau)
            if(vdtg in bdtgs):
                print bdtg,vdtg,pe
                
            n=n+1
            
class VdeckS(Vdeck):
    #SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
    # small version of vdeck
    #
    def __init__(self,etau=168,dtau=12,
                 verirule='std',
                 vdecktype='short',
                 veri9X=1,
                 ):

        self.vdecktype=vdecktype
        self.verirule=verirule
        self.veri9X=veri9X
        self.HomoVDdics=HomoVDdics
        self.SimpleListStats=SimpleListStats

        self.undef=1e20
        self.etau=etau
        self.dtau=dtau
        
        self.bdtg={}
        self.btvmax={}
        self.btpmin={}

        self.pe={}
        self.cte={}
        self.ate={}
        self.vme={}
        self.pmine={}

        self.pod={}
        self.vflag={}

        self.fcvmax={}
        self.fcpmin={}

        self.btnic={}
        self.fcnic={}

        self.btnicp={}
        self.fcnicp={}

        self.btnicn={}
        self.fcnicn={}

        self.nice={}
        self.niceb={}

        self.r34e={}
        self.r34bt={}
        self.r34fc={}

        # -- length of best track + scaled pe = pe/lenbt
        #
        self.btlen={}
        self.spe={}
        
        # -- length of bt for fc
        #
        self.btfclen={}
        self.fclen={}
        
        # -- ike FE
        
        self.ikeBT={}
        self.FE={}
        self.FE0={}
        
        self.TE={}

        self.taus=range(0,etau+1,dtau)

        for tau in self.taus:

            self.bdtg[tau]=[]
            self.btvmax[tau]=[]
            self.btpmin[tau]=[]

            self.pe[tau]=[]
            self.cte[tau]=[]
            self.ate[tau]=[]

            self.vme[tau]=[]
            self.pmine[tau]=[]

            self.pod[tau]=[]
            self.vflag[tau]=[]

            self.fcvmax[tau]=[]
            self.fcpmin[tau]=[]
            
            self.btnic[tau]=[]
            self.fcnic[tau]=[]

            self.btnicp[tau]=[]
            self.fcnicp[tau]=[]

            self.btnicn[tau]=[]
            self.fcnicn[tau]=[]

            self.nice[tau]=[]
            self.niceb[tau]=[]

            self.btlen[tau]=[]
            self.spe[tau]=[]

            self.btfclen[tau]=[]
            self.fclen[tau]=[]

            self.r34e[tau]=[]
            self.r34bt[tau]=[]
            self.r34fc[tau]=[]
            
            self.ikeBT[tau]=[]
            self.FE[tau]=[]
            self.FE0[tau]=[]

            self.TE[tau]=[]

    def GetVDVarlist(self,var,tau,verb=0,btoverride=1,warn=0):

        def getFromBT(tau,i,ndx):

            btdtg=self.bdtg[tau][i]
            vtdtg=mf.dtginc(btdtg,tau)
            btout=self.undef
            
            if(self.BT != None):
                try:
                    bttrk=self.BT.btrk[vtdtg]
                except:
                    bttrk=None
                    
                if(bttrk != None): btout=bttrk[ndx]
            
            if(hasattr(self,'btvmax') and ndx == 2 and bttrk == None):
                
                bdtgsTau=self.bdtg[tau]
                try:
                    vndx=bdtgsTau.index(vtdtg)
                except:
                    vndx=None
                    
                if(vndx != None):
                    btout=self.btvmax[tau][vndx]
                
                    
            return(btout)


        def getFromBTAll(tau,i,ndx):

            btouts=[]
            btdtgs=self.bdtg[tau]

            for btdtg in btdtgs:
                bttrk=self.BT.btrk[str(btdtg)]
                try:
                    bttrk=self.BT.btrk[str(btdtg)]
                except:
                    bttrk=self.undef
                
                btout=self.undef
                if(bttrk != self.undef): btout=bttrk[ndx]
                btouts.append(btout)

            return(btouts)


        def getFromBtcsTcflags(tau,i,ndx=4):

            btdtg=self.bdtg[tau][i]
            vdtg=mf.dtginc(btdtg,tau)
            
            try:
                bttcs=self.BT.btcs[vdtg]
            except:
                bttcs=None


            btout=None
            if(bttcs != None): 

                # -- new form
                #
                try:
                    (blat,blon,bvmax,bpmin,
                     cqdir,cqspd,
                     tccode,wncode,
                     bdir,bspd,cqdirtype,
                     b1id,tdo,ntrk,ndtgs,
                     r34m,r50m,alf,sname,
                     r34in,r50,depth)=bttcs
                    
                    # -- make 4-element fldic
                    #
                    istc=IsTc(tccode)
                    flgtc='NT'
                    if(istc):
                        tsnum=1
                        flgtc='TC'
                        
                    flgind=tccode
                    flgcq=cqdirtype
                    flgwn=wncode
                    btout="%s %s %s %s"%(flgtc,flgind,flgcq,flgwn)
                    
                # -- old form
                #
                except:
                    btout=bttcs[ndx]
                    btout="%s %s %s %s"%(btout[0],btout[1],btout[2],btout[3])

            if(btout == None):
                btout="NN NN NN NN"
            
            return(btout)


        list=[]
        for i in range(0,self.ndtgs):

            rc=[]
            try:
                obtvmax=getFromBT(tau,i,2)
            except:
                if(warn): print 'WWW(VdeckS.GetVDVarlist) tau: ',tau
                continue
            rc.append([self.vflag[tau][i],self.bdtg[tau][i],self.stmid,obtvmax])
            
            if(var == 'pod'):
                rc.append(self.pod[tau][i])

            elif(var == 'bdtg'):
                rc.append(self.bdtg[tau][i])

            elif(var == 'btpmin'):
                rc.append(self.btpmin[tau][i])

            elif(var == 'pe'):
                rc.append(self.pe[tau][i])

            elif(var == 'fe'):
                rc.append(self.FE[tau][i])

            elif(var == 'fe0'):
                rc.append(self.FE0[tau][i])

            elif(var == 'te'):
                rc.append(self.TE[tau][i])
                
            elif(var == 'cte'):
                rc.append(self.cte[tau][i])

            elif(var == 'ate'):
                rc.append(self.ate[tau][i])

            elif(var == 'vme'):
                rc.append(self.vme[tau][i])

            elif(var == 'pmine'):
                rc.append(self.pmine[tau][i])

            elif(var == 'fcvmax'):
                rc.append(self.fcvmax[tau][i])

            elif(var == 'vflag'):
                rc.append(self.vflag[tau][i])

            elif(var == 'fcpmin'):
                rc.append(self.fcpmin[tau][i])

            elif(var == 'nice'):
                rc.append(self.nice[tau][i])

            elif(var == 'nicf'):
                rc.append(self.nicf[tau][i])

            elif(var == 'nicfp'):
                rc.append(self.nicfp[tau][i])

            elif(var == 'nicfn'):
                rc.append(self.nicfn[tau][i])

            elif(var == 'nicbp'):
                rc.append(self.nicbp[tau][i])

            elif(var == 'nicbn'):
                rc.append(self.nicbn[tau][i])


            elif(var == 'niceb'):
                rc.append(self.niceb[tau][i])

            elif(var == 'btlen'):
                rc.append(self.btlen[tau][i])

            elif(var == 'btfclen'):
                rc.append(self.btfclen[tau][i])

            elif(var == 'fclen'):
                rc.append(self.fclen[tau][i])

            elif(var == 'spe'):
                rc.append(self.sfe[tau][i])

            elif(var == 'btlon'):
                if(hasattr(self,'btlon')):
                    obtlon=self.btlon[tau][i]
                else:
                    obtlon=getFromBT(tau,i,1)
                rc.append(obtlon)

            elif(var == 'tcflags'):
                if(hasattr(self,'tcflags')):
                    obtlon=self.tcflags[tau][i]
                else:
                    obtlon=getFromBtcsTcflags(tau,i)
                rc.append(obtlon)

            elif(var == 'btlat'):
                if(hasattr(self,'btlat')):
                    obtlat=self.btlat[tau][i]
                else:
                    obtlat=getFromBT(tau,i,0)
                rc.append(obtlat)

            elif(var == 'btvmax'):
                if(hasattr(self,'btvmax') and not(btoverride)):
                    obtvmax=self.btvmax[tau][i]
                else:
                    obtvmax=getFromBT(tau,i,2)
                rc.append(obtvmax)

            elif(var == 'r34e'):
                rc.append(self.r34e[tau][i])

            elif(var == 'r34bt'):
                rc.append(self.r34bt[tau][i])

            elif(var == 'r34fc'):
                rc.append(self.r34fc[tau][i])

            list.append(rc)
            if(verb):
                print 'VDvar ',var,i,rc

        return(list)

class cmpAdeckVdeck(MFbase):

    def __init__(self,
                 tdiffMin=1e20,
                 tdiffCrit=30.0,
                 doadtimeCheck=1,
                 verb=0,
                 ):

        self.verb=verb
        self.tdiffMin=tdiffMin
        self.tdiffCrit=tdiffCrit
        self.doadtimeCheck=doadtimeCheck
        

    def getADtime(self,taD):
        
        if(not(hasattr(taD,'updatedtghms'))):  adtime=taD.curdtghms[-1]
        else:  adtime=taD.updatedtghms

        adtimeAD=adtime
        taD.adtimeAD=adtimeAD

        
    
    def cmp(self,taid,tstmid,taD,tvD,verb=1):

        addtgs=taD.dtgs
        addtgs.sort()

        if(hasattr(tvD,'addtgsVD')):
            addtgsVD=tvD.addtgsVD
            addtgsVD.sort()
        else:
            addtgsVD=None
          
        try:
            vddtgs=tvD.bdtg[0]
            vddtgs.sort()
        except:
            vddtgs=[]

        addtgs.sort()
        vddtgs.sort()

        #print '00000000000000000000000 ',addtgsVD
        dtgcmpVD=-1
        if(addtgsVD != None):
            addtgsVD.sort()
            dtgcmpVD=0
            for addtg in addtgsVD:
                if(not(addtg in addtgsVD)):  dtgcmpVD=1

        #print 'aaaaaaaaaaaaaa ',addtgs
        #print 'vvvvvvvvvvvvvv ',vddtgs
        
        dtgcmp=0
        for addtg in addtgs:
            if(not(addtg in vddtgs)):  dtgcmp=1

        #print 'dddddddddddddddddd ',dtgcmp
        if(not(hasattr(taD,'adtimeAD'))):
            print 'getting in cmpAdeckVdeck.cmp adtimeAD'
            self.getADtime(taD)


        adtime=taD.adtimeAD
        vdtime=tvD.curdtghms[-1]

        if(hasattr(tvD,'adtimeVD')):
            if(tvD.adtimeVD != None):
                adtimeVD=tvD.adtimeVD
            else:
                adtimeVD=adtime
        else:
            adtimeVD=adtime

        MF=MFutils()
        tdiff=MF.DiffDtgHms(vdtime,adtime)
        ###print 'adtime: ',adtime,' adtimeVD: ',adtimeVD,' vdtime: ',vdtime,' tdiff: ',tdiff,dtgcmp,dtgcmpVD

        if(tdiff < self.tdiffMin): self.tdiffMin=tdiff

        update=0

        if(dtgcmp or dtgcmpVD > 0):
            update=1

            #print 'adtime: ',adtime,' adtimeVD: ',adtimeVD,' vdtime: ',vdtime,' dtgcmp: ',dtgcmp,' dtgcmpVD: ',dtgcmpVD
            # -- if adtime from vdeck = adtime from adeck, then already done, don't do again
            if(adtime == adtimeVD and self.doadtimeCheck): update=0

        # -- test if adeck *newer* than vdeck
        #
        if(tdiff > 0.0):
            update=2

        if(update > 0):
            tvD.adtimeVD=adtimeVD
            if(self.verb):
                if(update == 1):
                    print '11111111111111111 dtgcmp taid: ',taid,' tstmid: ',tstmid
                if(update == 2):
                    print '22222222222222222 tdiff  taid: ',taid,' tstmid: ',tstmid
            update=1

        return(update)


class SumStatMultiYear(MFbase):
    
    tausSR=[12,24]
    tausMR=[36,48]
    tausLR=[72,96,120]
    
    undef=-999.
    
    
    def __init__(self,byear,eyear,basin,setOpt,
                 baseModels,veriOpt,phrOpt,
                 veriStat,veriStatRead,
                 otau,
                 datDir='datTCstats',
                 verb=0,
                 ):

        self.byear=byear
        self.eyear=eyear
        self.years=range(byear,eyear+1)
        self.basin=basin
        self.setOpt=setOpt
        self.baseModels=baseModels
        self.datDir=datDir
        self.verb=verb
        
        if(veriOpt == '-H'):
            overrideOpt='-O'
            overrideOpt=''
            if(phrOpt == ''):  veriLabel='raw-hetero'
            elif(phrOpt == 0): veriLabel='phr00-raw-hetero'
            elif(phrOpt == 6): veriLabel='phr06-raw-hetero'
    
        if(veriOpt == ''):
            veriLabel='raw-homo'
            overrideOpt=''
            if(phrOpt == ''):  veriLabel='raw-homo'
            elif(phrOpt == 0): veriLabel='phr00-raw-homo'
            elif(phrOpt == 6): veriLabel='phr06-raw-homo'
            
        if(phrOpt == ''):
            models=self.baseModels
        elif(phrOpt == 0):
            models=[]
            for model in self.baseModels:
                model=model+'00'
                models.append(model)
        elif(phrOpt == 6):
            models=[]
            for model in self.baseModels:
                model=model+'06'
                models.append(model)
        
        self.phrOpt=phrOpt
        self.veriOpt=veriOpt
        self.veriStat=veriStat
        self.veriStatRead=veriStatRead
        self.veriLabel=veriLabel
        self.models=models
        self.otau=otau
        
        self.clipModel='clip5'
        self.navyModelG='gnav'
        self.ecmwfModel='tecmt'
        
        self.readStats()
        
        if(len(str(self.otau)) > 1 and str(self.otau)[1] == 'R'):
            if(self.otau == 'SR'): self.makeNetFe(self.tausSR,tauLabel=self.otau)
            if(self.otau == 'MR'): self.makeNetFe(self.tausMR,tauLabel=self.otau)
            if(self.otau == 'LR'): self.makeNetFe(self.tausLR,tauLabel=self.otau)
        
        if(self.veriStat == 'gainxype' or self.veriStat == 'gainxyfe' or self.veriStat == 'gainxyte'):
            self.models=self.baseModels
            self.makeGainxyFe(self.otau)
            
        self.makeYearStats(self.otau)
    
   
   
    def makeSingleYearStats(self,year):
        
        stype=self.veriStatRead
        
        for model in self.models:

            for tau in self.taus:
                try:
                    val=self.allStats[year,model,tau,stype]
                except:
                    val=(self.undef,0)
                    
                val2=val3=val4=val5=val6=self.undef

                if(val[0] != self.undef and len(val) == 2):
                    valR=val[0]
                    cntR=val[1]
                elif(len(val) == 7):
                    valR=val[0]
                    cntR=val[1]
                    valR2=val[2]
                    valR3=val[3]
                    valR4=val[4]
                    valR5=val[5]
                    valR6=val[6]
                                                                                
                self.yearStats[model,tau,stype]=oval
            
        


    def makeYearStats(self,tau):

        stype=self.veriStatRead

        modelMs=self.models
        if(self.veriStat == 'gainxyfe' or self.veriStat == 'gainxype' or self.veriStat == 'gainxyte'): modelMs=self.models[0:-1]
        
        for model in self.models:
            
            valSR=0.0
            cntSR=0
            val2=0.0
            val3=0.0
            val4=0.0
            val5=0.0
            val6=0.0
            val7=0.0
            
            for year in self.years:

                val=(self.undef,0)
                gotest=0
                for modelM in modelMs:
                    
                    try:
                        valM=self.allStats[year,modelM,tau,stype]
                    except:
                        valM=None
                
                    gotest=(valM == None or (valM != None and valM[0] == self.undef))        
                    if(gotest): break
                
                if(gotest): continue
                
                try:
                    val=self.allStats[year,model,tau,stype]
                except:
                    val=(self.undef,0)

                if(val[0] != self.undef and len(val) == 2):
                    valR=val[0]
                    cntR=val[1]
                    valSR=valSR+valR*cntR
                    cntSR=cntSR+cntR

                elif(len(val) == 8):
                    valR=val[0]
                    cntR=val[1]
                    valSR=valSR+valR*cntR
                    
                    valR2=val[2]
                    valR3=val[3]
                    valR4=val[4]
                    valR5=val[5]
                    valR6=val[6]
                    valR7=val[7]
                                                                            
                    val2=val2+valR2*cntR
                    val3=val3+valR3*cntR
                    val4=val4+valR4*cntR
                    val5=val5+valR5*cntR
                    val6=val6+valR6*cntR
                    val7=val7+valR7*cntR
                    
                    cntSR=cntSR+cntR
                    

            if(cntSR == 0 and len(val) == 2):
                valSR=self.undef
                oval=(valSR,cntSR)
                
            elif(cntSR == 0 and len(val) == 8):
                valSR=self.undef
                oval=(valSR,cntSR,val2,val3,val4,val5,val6,val7)
                
            elif(len(val) == 2):
                valSR=valSR/float(cntSR)
                oval=(valSR,cntSR)

            elif(len(val) == 8):
                valSR=valSR/float(cntSR)
                val2=val2/float(cntSR)
                val3=val3/float(cntSR)
                val4=val4/float(cntSR)
                val5=val5/float(cntSR)
                val6=val6/float(cntSR)
                val7=val7/float(cntSR)
                oval=(valSR,cntSR,val2,val3,val4,val5,val6,val7)

            self.yearStats[model,tau,stype]=oval
    
        
        
    
    def makeNetFe(self,tausSR,tauLabel='SR'):
        

        def doNetFe(tausSR,stype,tauLabel):
            
            for model in self.models:
                for year in self.years:
                    valSR=0.0
                    cntSR=0
                    val2=0.0
                    val3=0.0
                    val4=0.0
                    val5=0.0
                    val6=0.0
                    val7=0.0
                    
                    for tau in tausSR:
                        try:
                            val=self.allStats[year,model,tau,stype]
                        except:
                            val=(self.undef,0)
        
                        if(val[0] != self.undef and len(val) == 2):
                            valR=val[0]
                            cntR=val[1]
                            valSR=valSR+valR*cntR
                            cntSR=cntSR+cntR
                        elif(len(val) == 8):
                            valR=val[0]
                            cntR=val[1]
                            valSR=valSR+valR*cntR
                            
                            valR2=val[2]
                            valR3=val[3]
                            valR4=val[4]
                            valR5=val[5]
                            valR6=val[6]
                            valR7=val[7]
                                                                                    
                            val2=val2+valR2*cntR
                            val3=val3+valR3*cntR
                            val4=val4+valR4*cntR
                            val5=val5+valR5*cntR
                            val6=val6+valR6*cntR
                            val7=val7+valR7*cntR
                            
                            cntSR=cntSR+cntR
                            
        
                    if(cntSR == 0 and len(val) == 2):
                        valSR=self.undef
                        oval=(valSR,cntSR)
                        
                    elif(cntSR == 0 and len(val) == 7):
                        valSR=self.undef
                        oval=(valSR,cntSR,val2,val3,val4,val5,val6)
                        
                    elif(len(val) == 2):
                        valSR=valSR/float(cntSR)
                        oval=(valSR,cntSR)

                    elif(len(val) == 7):
                        valSR=valSR/float(cntSR)
                        val2=val2/float(cntSR)
                        val3=val3/float(cntSR)
                        val4=val4/float(cntSR)
                        val5=val5/float(cntSR)
                        val6=val6/float(cntSR)
                        val7=val7/float(cntSR)
                        oval=(valSR,cntSR,val2,val3,val4,val5,val6,val7)
        
                    self.allStats[year,model,tauLabel,stype]=oval
            
            

        stype=self.veriStatRead
        
        if(stype == 'pod'):
            doNetFe(tausSR,stype,tauLabel)
            doNetFe(tausSR,'poo',tauLabel)
        else:
            doNetFe(tausSR,stype,tauLabel)
            
    def makeGainxyFe(self,tau):
    
        tauLabel="%s-gainxyfe"%(str(tau))
    
        fixmodel=self.models[-1]
        for model in self.models[0:-1]:
            for year in self.years:
                valSR=0.0
                cntSR=0
                try:
                    val=self.allStats[year,model,tau,self.veriStatRead]
                except:
                    val=(self.undef,0)
                try:
                    valF=self.allStats[year,fixmodel,tau,self.veriStatRead]
                except:
                    valF=(self.undef,0)
    
                if(val[0] != self.undef and valF[0] != self.undef):
                    gainxy=((valF[0]-val[0])/valF[0])*100.0
                else:
                    gainxy=self.undef
                self.allStats[year,model,tauLabel,self.veriStatRead]=(gainxy,val[1])
                self.otauStats[year,model,tauLabel]=(gainxy,val[1])
                
        self.otau=tauLabel
    
    
    def readStats(self):
        
        self.allStats={}
        self.yearStats={}
        self.otauStats={}
        
        taus=[]
        
        for year in self.years:
            cyear=str(year)[-2:]
            ifile="%s/stats.%s-%s.%s.%s.%s.txt"%(self.datDir,self.basin,cyear,self.veriStatRead,self.veriLabel,self.setOpt)
            if(self.verb): print 'ifile:',ifile
            cards=MF.ReadFile2List(ifile)
            #allstats[taid,tau,verikey]=(ostat,mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)
            #SSSSSHHHHH               hwrf   0         pe        11.0 n: 294    m,a,s,mn,p25,med,p75,p90,mx:   11.0   11.0   15.9  Dist:    0.0    0.0  MD:    6.0   13.3   26.2  132.3
            #'SSSSSHHHHH', 'hwrf', '0', 'pe', '11.0', 'n:', '294', 'm,a,s,mn,p25,med,p75,p90,mx:', '11.0', '11.0', '15.9', 'Dist:', '0.0', '0.0', 'MD:', '6.0', '13.3', '26.2', '132.3']
            for card in cards:
                if(mf.find(card,'nada')):continue
                tt=card.split()
                #if(self.verb): print 'card:',tt
                n=1
                model=tt[n]        ; n=n+1
                tau=int(tt[n])     ; n=n+1  ; taus.append(tau)
                stype=tt[n]        ; n=n+1
                stat=float(tt[n])  ; n=n+2
                ncounts=int(tt[n])
                # -- relabel models
                #
                if(mf.find(model,'tecm')): model=self.ecmwfModel
                if( (self.basin == 'l' or self.basin == 'e') and model == 'clp5'): model=self.clipModel
                if( self.basin == 'w' and model == 'c120'):                        model=self.clipModel
                if(model == 'ngps' or model == 'nvgm'):                            model=self.navyModelG
                
                # -- full stat record
                
                if(len(tt) >= 19):
                    n=n+2
                    mean=float(tt[n])    ; n=n+1
                    amean=float(tt[n])   ; n=n+1
                    sigma=float(tt[n])   ; n=n+2
                    minv=float(tt[n])    ; n=n+1
                    ptl25=float(tt[n])   ; n=n+2
                    median=float(tt[n])  ; n=n+1
                    ptl75=float(tt[n])   ; n=n+1
                    ptl90=float(tt[n])   ; n=n+1
                    maxv=float(tt[n])    ; n=n+1
                    
                    ostat=(stat,ncounts,minv,ptl25,median,ptl75,ptl90,maxv)
                    self.allStats[year,model,tau,stype]=ostat
                    
                else:
                    ostat=(stat,ncounts)
                    self.allStats[year,model,tau,stype]=ostat
    
        taus=mf.uniq(taus)
        self.taus=taus






