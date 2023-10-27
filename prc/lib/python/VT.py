""" VT -- verification of TCs using vdecks
"""

from tcbase import *
from ATCF import AidProp

MF=MFutils()

# -- moved AidProp class to ATCF together with class Aid()

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
            if(verb): print 'III(initAidStorms) ',self.verivars[0][2],markaid
            if(self.verivars[0][2] == 'vbias' and markaid != 'd'):
                markaid=markaid
            else:
                markaid='+'

            markaids[n]=markaid

        if(verb): print 'III(initAidSTorms) final markaids: ',markaids




class PodStats(SumStats):

    def __init__(self,
                 taids,
                 tstmids,
                 counts,
                 verb=0,
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
                print 'aid: %s tau: %3d   pod: %6.1f  over: %6.1f   N: %4d  Nfc: %4d  Nover: %4d'%(aid,tau,pod,over,nveris[aid,tau],nverifcs[aid,tau],nverifcovers[aid,tau])

                ostat=(pod,nveri)
                self.ostats[aid,tau,'pod']=ostat

                ostat=(over,nverifcover)
                self.ostats[aid,tau,'over']=ostat

        # -- by storm stats
        #
        stmids=mf.uniq(stmids)

        for aid in aids:
            for stmid in stmids:
                if(self.verb and len(stmids) > 1): print
                
                for tau in taus:    
                
                    if(nverisB[aid,stmid,tau] > 0):
                        podsB[aid,stmid,tau]=(float(nverifcsB[aid,stmid,tau])/float(nverisB[aid,stmid,tau]))*100.0
                    else:
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

    def __init__(self,ss,
                 pcase,
                 ptype,
                 doland=1,
                 pdir='/tmp',
                 ):

        pname='%s.%s'%(ptype,pcase)
        self.ss=ss
        self.pcase=pcase
        self.ptype=ptype
        
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
                      ):

        models=self.ss.models

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
        if(hasattr(self.ss,'vstmids')):
            ovstmids=self.reducestmids(self.ss.vstmids)
        else:
            ovstmids=[]

        if(mf.find(self.ptype,'gainxyfe')):
            t2a="Gain [%%] Relative to: %s  of: "%(lmodel)
            for model in models[0:-1]:
                t2a="%s %s"%(t2a,model)
            t2a=t2a+'\n'

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
        nsmax=20
        t2b="Storms[N] [%d]: "%(ns)

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

        if(self.ptype == 'fe'):
            ylab='FE [nm]'

        if(self.ptype == 'sfe'):
            ylab='FE scaled by length of track [%]'

        if(self.ptype == 'rmsfe'):
            ylab='FE [nm]'

        elif(self.ptype == 'vme'):
            ylab='VmaxE [kt]'

        elif(self.ptype == 'vbias'):
            ylab='Vmax MeanE(Bias)/AbsMeanE [kt]'

        elif(self.ptype == 'pbias'):
            ylab='Pmin(Bias) [mb]'

        elif(self.ptype == 'pod'):
            ylab='POD (bar) ; POO (line) [%]'

        elif(self.ptype == 'pof'):
            ylab='POF (bar) ; POO (line) [%]'

        elif(self.ptype == 'gainxyfe'):
            ylab='Gain FE [%]'

        elif(self.ptype == 'pbetter'):
            ylab='% better'
            if(len(taus) == 1):
                ylab="%s tau=%d"%(ylab,taus[0])

        elif(self.ptype == 'gainxyvmax'):
            ylab='Gain VmaxError [%]'

        elif(self.ptype == 'gainxyvbias'):
            ylab='Ratio abs(bias)/mean(abs) [%]'

        elif(self.ptype == 'ctate'):
            ylab='XT (track) bias [nm; line]; AT (speed) bias [nm; bar]'

        self.ptitles=(t1,t2,ylab)




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

    def setpvartag(self,npvartag,pvartagopt=None):

        if(pvartagopt == '00_12z'):
            if(npvartag == 1):
                pvartag='_00z'
            elif(npvartag == 2):
                pvartag='_12z'

        elif(pvartagopt == '00z'):
            pvartag='_00z'

        elif(pvartagopt == '00_12v06_18z'):
            if(npvartag == 1):
                pvartag='_00/12z'
            elif(npvartag == 2):
                pvartag='_06/18z'
        else:
            pvartag=''

        return(pvartag)


    def putpvar(pvar,npvartag,pvartag,model,var,lab,cnt,type='fe'):

        lab=lab+'%s'%(pvartag)
        pvar[model,npvartag,type+'var']=var
        pvar[model,npvartag,type+'lab']=lab
        pvar[model,npvartag,type+'cnt']=cnt




    def getpvar(pvar,npvartag,model,type='fe'):

        var=pvar[model,npvartag,type+'var']
        lab=pvar[model,npvartag,type+'lab']
        cnt=pvar[model,npvartag,type+'cnt']

        return(var,lab,cnt)



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
        
        if(self.ptype == 'fe'):
            ptype1='fe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,400.0,50],lgndloc)

        elif(self.ptype == 'sfe'):
            ptype1='sfe'
            ptype2=ptype1
            lgndloc=2
            controls=([0.0,110.0,10],lgndloc)

        elif(self.ptype == 'rmsfe'):
            ptype1='fe'
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

        elif(self.ptype == 'pof'):
            ptype1='pods'
            ptype2='povr'
            lgndloc=0
            controls=([0.0,120.0,20.0],lgndloc)

        elif(self.ptype == 'gainxyfe'):
            ptype1='gainxyfe'
            ptype2=ptype1
            lgndloc=0
            controls=([-40.0,60.0,10.0],lgndloc)
            controls=([-30.0,70.0,10.0],lgndloc)

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

        elif(self.ptype == 'ctate'):
            ptype1='mcte'
            ptype2='mate'
            lgndloc=2
            controls=([-400.0,400.0,50.0],lgndloc)

        else:
            print 'EEE invalid plot ptype in PlotsumStat: ',ptype
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
                   ):

        #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #
        # internal defs
        #

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

        from pylab import arange
        import pylab as P

        # -- moved to w2base.py from VT.py
        #
        C2hex=w2Colors().chex

        # setup input
        #

        pngpath=self.ppaths[0]
        epspath=self.ppaths[1]
        rptpath=self.ppaths[2]

        (t1,t2,ylab)=self.ptitles
        (ylim,lgndloc)=self.controls

        yb=ylim[0]
        ye=ylim[1]
        dy=ylim[2]

        tt1=t1.split('|')
        if(len(tt1)==2):
            t1="%s\n%s"%(tt1[0],tt1[1])

        taus=cnts[0].keys()
        taus.sort()


        nrows=len(dicts)

        if(mf.find(self.ptype,'gainxy')):
            if(useroverride):
                nrows=nrows/2
            else:
                nrows=nrows-1


        vals1=[]
        vals2=[]
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
            nts=len(taus)

            xaxis=[]

            for nt in range(0,nts):
                tau=taus[nt]

                val1=dict1[tau]
                val2=dict2[tau]

                if(reversedirection):
                    val1=-val1
                    val2=-val2

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

            vals1.append(row1)
            vals2.append(row2)

            cvals.append(crow)
            xaxiss.append(xaxis)

            rlabel=olabels[n]

            if(irowll == None):
                rowll.append(models[n])
                
            if(irowl == None):
                rowl.append(rlabel)

            mcol=C2hex['navy']
            
            mcolt=C2hex['grey']
            
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

        yts=arange(yb,ye,dy)

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
            'text.fontsize': 10,
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

        if(dxofffraction >= 1.5):
            alphabar=0.75


        for n in range(0,np):

            ys=vals1[n]
            xaxisl=copy.copy(xaxiss[n])
            xaxisb=copy.copy(xaxiss[n])

            if(do1stplot):
                #adjustxaxis(n,xaxisl,barwidth,dxofffraction,center=1)
                rc=FP.plot(xaxisl,ys,
                           color=rowc[n],
                           linestyle=lstyle[n],
                           marker=lmarker[n],
                           linewidth=lwidth[n],
                           alpha=alphaline[n]
                           )


            if(do2ndplot > 0):

                if(do2ndplot == 2):
                    doline=1

                ys=vals2[n]

                if(doline):
                    rc=FP.plot(xaxisl,ys,
                               color='k',
                               linestyle='-',
                               marker=lmarker[n],
                               linewidth=lwidth[n],
                               alpha=1.0
                               )
                else:

                    adjustxaxis(n,xaxisb,barwidth,dxofffraction)
                    rc=FP.bar(xaxisb,ys,
                              align='edge',
                              color=rowc[n],
                              width=pbarwidth,
                              alpha=alphabar[n])


            if(len(rc) != 0):
                lgndc.append(rc[0])



        FP.legend( lgndc, rowl, loc=lgndloc, shadow=True, markerscale=0.2)

        if(dotable):

            if(verb):
                print 'rowl: ',rowl
                print 'rowc: ',rowc
                for  i in range(0,len(cvals)):
                    print 'cvals',i,cvals[i]

            TT=P.table(cellText=cvals,loc='bottom',
                       rowLabels=rowll,rowColours=rowt,
                       colLabels=ctaus)

            TT.set_fontsize(8)

            P.xticks(xaxis,ctausblank)


        else:
            P.xticks(xaxis,ctaus)

        if(self.ptype == 'vme' or self.ptype == 'ctate' or self.ptype == 'vbias' or self.ptype == 'pbias' or mf.find(self.ptype,'gainxy')):
            draw0line(lcol='k')

        if(self.ptype == 'pod' or self.ptype == 'pof'):
            drawCritline(100.0,lcol='k')

        elif(self.ptype == 'pbetter'):
            drawCritline(50.0,lcol='k')


        P.xlim(-1.0,len(taus)-1)
        P.ylim(yb,ye)
        P.yticks(yts)

        P.suptitle(t1,fontsize=13)
        P.title(t2,size=8)

        P.ylabel(ylab)

        P.grid()


        (path,ext)=os.path.splitext(pngpath)
        pdfpath="%s.pdf"%(path)
        
        if(dopng):
            P.savefig(pngpath)
            print 'pppppppppppp: ',pngpath,doshow


        if(doeps):
            print 'eeeeeeeeeeee ',epspath
            P.savefig(epspath,orientation='landscape')

        if(dopdf):
            print 'pdfpdfpdfpdf ',pdfpath
            P.savefig(pdfpath,orientation='landscape')


        if(doshow):  P.show()


        ropt=''
        if(doxv and dopng):
            cmd="xv %s &"%(pngpath)
            mf.runcmd(cmd,ropt)

        if(docp and dopng):
            tdir='/Users/fiorino/DropboxNOAA/Dropbox'
            tdir='/Users/fiorino/Dropbox'
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

    


    

        


#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods
#


def RemoveNonBtAcards(ac,stmid,btdtgs,verb=0):

    oacards={}
    odtgs=[]

    stmnum=stmid[0:2]
    for dtg in ac.dtgs:

        iokbt=0
        for btdtg in btdtgs:
            if(dtg == btdtg):
                iokbt=1
                break
        
        if(iokbt):
            ocards=[]
            for card in ac.acards[dtg]:
                ocards.append(card)
            oacards[dtg]=ocards
            odtgs.append(dtg)

    odtgs=mf.uniq(odtgs)

    ac.acards=oacards
    ac.dtgs=odtgs
    
    return(ac)


        
def pltHist(list0,list1,list2,
            stmopt='stmopt',
            tag0='tag0',
            tag1='tag1',
            tag2='tag2',
            donorm=1,
            docum=1,
            filttype='season',
            xlab='x',
            xmax=None,
            xmin=None,
            xint=None,
            ymax=None,
            ymin=0,
            yint=None,
            binint=None,
            dostacked=0,
            var1='var1',
            var2='var2',
            title1='',
            doxv=0,
            doshow=0,
            ):

    import matplotlib.pyplot as plt
    from numpy import array,arange

    if(list0 != None):
        x0=array(list0)
        xmax0=x0.max()
        rc0=SimpleListStats(list0,hasflag=0)
        mean0=rc0[0]
        sigma0=rc0[2]
        
    if(list1 != None):
        x1=array(list1)
        xmax1=x1.max()
        rc1=SimpleListStats(list1,hasflag=0)
        mean1=rc1[0]
        sigma1=rc1[2]
        
    if(list2 != None):
        x2=array(list2)
        xmax2=x2.max()
        rc2=SimpleListStats(list2,hasflag=0)
        mean2=rc2[0]
        sigma2=rc2[2]

    else:
        xmax2=xmax1


    print '1111111111111 ',list2

    #if(donorm):
    #    ymax=0.75
    #    yint=0.25

    if(docum):
        ymin=0
        ymax=1.0
        yint=0.10


    if(xmin == None): xmin=0


    if(xmax1 > xmax2):
        maxx=xmax1
    else:
        maxx=xmax2
        
    if(xint == None):
        xint=int(maxx/10.0)

    if(xmax == None):
        xmax=int((float(maxx)/float(xint))+0.5 + 1)*float(xint)


    nbins=int((xmax-xmin)/xint)
    nbins=(xmax-xmin)/xint
    nbins=nbins*5

    print 'xxxxxxxxxxxxxxxx ',maxx,xmax,xmin,xint,nbins

    x0=list0

    hrange=[xmin,xmax]
    hrange=None

    fc1='green'
    fc2='red'
    ptype='bar'
    ec1='black'
    ec2='black'


    if(donorm or docum):
        ylab='prob [fraction]'
        if(docum): ylab="cumulative %s"%(ylab)
    else:
        ylab='N'


    if(dostacked):

        ptype='barstacked'
        ptype='bar'

        xplot=(x1,x2)
    
        (n1, bins, patches) = plt.hist(xplot,nbins,histtype=ptype,range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       color=['green', 'red'],
                                       alpha=1.0,rwidth=1.0)

    else:

        ptype='bar'
        #ptype='step'
        (n1, bins, patches) = plt.hist(x1,nbins,histtype=ptype,range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=1.0,rwidth=1.0)


        
        ymax1=n1.max()
        maxy=ymax1
        maxx=xmax1
        print '1111111111111' ,n1,bins
        if(list2 != None):
            (n2, bins, patches) = plt.hist(x2,nbins,histtype='bar',range=hrange,\
                                           normed=donorm,cumulative=docum,
                                           facecolor=fc2,edgecolor=ec2,
                                           alpha=0.5,rwidth=1.0)
            print '22222222222222 ',n2,bins
            ymax2=n2.max()

            if(ymax1 > ymax2):
                maxy=ymax1
            else:
                maxy=ymax2
                
                

    if(yint == None):
        yint=int(maxy/10.0)
        yint=maxy/10.0
        if(yint == 0.0): yint=1

    if(ymax == None):
        ymax=int((float(maxy)/float(yint))+0.5 + 1)*float(yint)
    
        
    xs=[]
    for i in range(0,len(bins)-1):
        xs.append( (bins[i]+bins[i+1])*0.5 )

    def zerolt0(ys):
        oys=[]
        for y in ys:
            if(y < 0.0):
                oys.append(0.0)
            else:
                oys.append(y)
        return(oys)


    plt.xlabel(xlab)
    plt.ylabel(ylab)

    if(mf.find(filttype,'dev')):
        
        ptitle="%s(G)  N: %d Mn: %3.1f $\sigma$: %3.1f %s(R)  N: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(
            var1,len(list1),mean1,sigma1,
            var2,len(list2),mean2,sigma2,
            stmopt)

    if(mf.find(filttype,'seas')):

        if(list2 != None):
            ptitle="%s\n%s(G) N: %d Mn: %3.1f $\sigma$: %3.1f     %s(R)  N: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(title1,
                var1,len(list1),mean1,sigma1,
                var2,len(list2),mean2,sigma2,
                stmopt)

        else:
            ptitle="%s\n%s(G)  N: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(title1,
                                                                     var1,len(list1),mean1,sigma1,
                                                                     stmopt)

            print 'ppppppppppppppppppppppp ',ptitle

        
    #ptitle="$\sigma=$"
    plt.title(r"%s"%(ptitle),fontsize=11)
    

    print 'xxxxxxxxxxxxxxxxxxxxxxxxx ',xmax,xmin,xint
    plt.xlim(xmin,xmax)
    xaxis=arange(xmin,xmax+1,xint)
    plt.xticks(xaxis)

    print 'yyyyyyyyyyyyyyyyyyyyyyyyy ',ymax,ymin,yint
    plt.ylim(ymin,ymax)
    yaxis=arange(ymin,ymax+0.001,yint)
    plt.yticks(yaxis)

    plt.grid(True)

    if(donorm): tag1='norm'
    if(docum):  tag2='cumul'

    tagf='counts'
    
    if(tag1 != 'tag1' and tag2 != 'tag2'):
        tagf="%s-%s"%(tag1,tag2)
    elif(tag1 != 'tag1'):
        tagf=tag1
    elif(tag1 != 'tag2'):
        tagf=tag2
    

    tdir='/tmp'
    tdir='/Users/fiorino/Dropbox'
    pngpath="%s/%s.%s.%s.png"%(tdir,tag0,stmopt,tagf)

    print 'PPP(pngpath): ',pngpath
    
    plt.savefig(pngpath)

    if(doxv):
        cmd="xv %s"%(pngpath)
        mf.runcmd(cmd)

    if(doshow): plt.show()


        
                
