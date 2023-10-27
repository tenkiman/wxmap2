#!/usr/bin/env python

from vdVM import *
from VT import *
from scipy import integrate

class PlotXYs(MFbase):

    import w2colors as W2C

    cols=[]
    namecols=['red','navy','gold','black','green','purple']

    for ncol in namecols:
        cols.append(W2C.Color2Hex[ncol])

    lstys=[]
    lstys.append('-')
    lstys.append('-')
    lstys.append('--')
    lstys.append(':')
    lstys.append('-.')
    lstys.append('-')

    lwids=[]

    lwids.append(2.0)
    lwids.append(1.0)
    lwids.append(2.0)
    lwids.append(1.0)
    lwids.append(2.0)
    lwids.append(1.0)

    def __init__(self,XYs):


        import numpy
        yss=[]
        xss=[]
        zeros=[]

        for XY in XYs:
            
            xss.append(XY.x)
            yss.append(XY.y)
            zeros.append(numpy.zeros(XY.np))

        self.yss=yss
        self.xss=xss
        self.zeros=zeros
        self.xunits=XYs[0].xunits


    def pdiff(self):

        oyss=[]
        oxss=[]
        ny=len(self.yss)
        if(ny>1):

            ymean=self.zeros
            for n in range(0,ny):
                ymean=ymean+self.yss[n]

            ymean=ymean/ny

            for n in range(1,ny):
                ydiff=self.yss[n] - self.yss[n-1]
                ymean=(self.yss[n] + self.yss[n-1])*0.5
                pdiff=(ydiff/ymean)*100.0
                oyss.append(pdiff)
                oxss.append(self.xss[n-1])

                for i in range(0,len(pdiff)):
                    print 'i ',i,pdiff[i]
                
            self.yss=oyss
            self.xss=oxss
            self.t2='Percent Difference from Mean of'


            
            


    def plot(self,pngpath=None,doshow=0,
             yb=None,
             ye=None,
             ):

        def setxlab(xunits):
            if(xunits == 'h'):
                xlab="time [%s]"%(xunits)
            else:
                xlab=''
            return(xlab)


        MF.sTimer('pylab')
        
        import matplotlib as mpl
        from dateutils import datetohrs
        from matplotlib import pylab as P
        from numpy import arange
        MF.dTimer('pylab')

        Params = {
            'axes.labelsize': 12,
            'text.fontsize': 12,
            'legend.fontsize': 14,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            }
        


        try:
            t1=self.t1
        except:
            t1=''

        try:
            t2=self.t2
        except:
            t2=''

        P.rcParams.update(Params)
        
        xydim=(10.5,8.25)
        F=P.figure(figsize=xydim)
        
        leftsubplot=0.10
        bottomsubplot=0.15
        
        F.subplots_adjust(top=0.9,bottom=bottomsubplot,left=leftsubplot,right=0.95,wspace=0.0,hspace=0.0)
        
        FP=F.add_subplot(111)

        xmaxA=-1e20
        xminA=1e20
        
        for n in range(0,len(self.yss)):
            ys=self.yss[n]
            xs=self.xss[n]
            ymax=ys.max()
            ymin=ys.min()
            xmax=xs.max()
            xmin=xs.min()
            xmaxA=max(xmax,xmaxA)
            xminA=min(ymin,xminA)
            
        dx=24.0
        xb=0.0
        xe=xmaxA
        xts=arange(xb,xe,dx)

        nyss=len(self.yss)

        ys1=None
        if(nyss == 3):
            ys0=self.yss[1]
            ys1=self.yss[2]

        if(nyss == 6):
            ys0a=self.yss[1]
            ys1a=self.yss[2]

            ys0b=self.yss[4]
            ys1b=self.yss[5]

        self.lwids[2]=0
        self.lwids[1]=4.0
        self.lwids[0]=2.0
        
        self.lwids[5]=0
        self.lwids[4]=4.0
        self.lwids[3]=2.0

        self.lstys[3]='-'
        self.lstys[4]='-'
        self.lstys[5]='-'
        
        self.cols[0]='black'
        self.cols[1]='red'
        self.cols[2]='red'
        self.cols[3]='green'
        self.cols[4]='green'
        self.cols[5]='red'
        
        
        for n in range(0,len(self.yss)):
            
            ys=self.yss[n]
            xs=self.xss[n]

            rc=FP.plot(xs,ys,
                       color=self.cols[n],
                       linestyle=self.lstys[n],
                       marker='',
                       linewidth=self.lwids[n],
                       alpha=1.0,
                       )

            if(ys1a != None and n == 2):
                P.fill_between(xs, ys0a, ys1a, where=ys1a>=ys0a,  facecolor='red', alpha=0.5,linewidth=0)
                P.fill_between(xs, ys0a, ys1a, where=ys1a<=ys0a,  facecolor='blue', alpha=0.5,linewidth=0)
        
            elif(ys1b != None and n == 5):
                P.fill_between(xs, ys0b, ys1b, where=ys1b>ys0b,  facecolor='green', alpha=0.5,linewidth=0)
                P.fill_between(xs, ys0b, ys1b, where=ys1b<=ys0b,  facecolor='yellow', alpha=0.5,linewidth=0)
        
        if(yb != None and ye != None):
            P.ylim(yb,ye)

        P.xlim(xb,xe)
        P.xticks(xts)
        
        xlab=setxlab(self.xunits)
        P.xlabel(xlab)
        P.ylabel('Vmax [kt]')

        if(len(t1)>0):
            P.suptitle(t1,fontsize=14)
        if(len(t2)>0):
            P.title(t2,size=12)
            
        P.grid(True)

    
        
        if(pngpath != None):
            P.savefig(pngpath)
            print 'qqqqqqqqqqqqqqqqqqqq pngpath: ',pngpath
            
        if(doshow):
            P.show()
            print 'qqqqqqqqqqqqqqqqqqqq do show'


class tsPlot(PlotXYs):


    def __init__(self,hash):

        import numpy
        
        xl=[]
        yl=[]
        kk=hash.keys()
        kk.sort()
        for k in kk:
            xl.append(k)
            yl.append(hash[k])

        x=numpy.array(xl)
        y=numpy.array(yl)

        self.x=x
        self.y=y
        self.np=len(x)
        self.dx=(x[-1]-x[-2])
        self.xunits='h'



        




def getVdFromDSss(DSss,taid,tstmid,verb=0):

    kk=DSss.keys()
    for k in kk:
        vDS=DSss[k]
        if(verb):
            print 'trying to get taid, tstmid: ',taid,tstmid
        vd=GetVdsFromDSs(vDS,taid,tstmid,returnlist=1)
        if(vd != None):
            return(vd)


def getVdsFromDSss(DSss,taids,tstmids):

    kk=DSss.keys()

    vds={}
    for taid in taids:
        gtaid=taid
        for tstmid in tstmids:
            # -- handle bcon
            #
            if(taid == 'bcon'):
                gtaid=getBcon4Stmid(tstmid)

            if(taid == 'hfip'):
                vds[taid,tstmid]=None
            else:
                vds[taid,tstmid]=getVdFromDSss(DSss,gtaid,tstmid,verb=0)

    return(vds)

        
def lsCases(taids,cases,casedtgs,verivars,ttau=72,dobigbias=0):

    try:
        tdtgs=casedtgs[ttau,verivars[0][0]]
    except:
        print 'WWW no cases for ttau: ',ttau
        return
    
    kk=cases.keys()
    kk.sort()

    ovars={}
    ocards={}
    ostmids={}
        
    for tdtg in tdtgs:

        for k in kk:

            (aid,stmid,dtg,tau,verikey)=k
                
            if(dtg == tdtg):
                    
                for taid in taids:
                    if(aid == taid and tau == ttau):
                        
                        (stmid,vmax,vvar)=cases[k]
                        MF.loadDictList(ostmids,dtg,stmid)
                        try:
                            ocards[taid,stmid,dtg]
                        except:
                            ocards[taid,stmid,dtg]=''
                                
                        if(len(ocards[taid,stmid,dtg]) > 0):
                            #print 'tttttttt ',taid,stmid,dtg,ocards[taid,stmid,dtg]
                            ocards[taid,stmid,dtg]="%10s %6s %6.1f"%(ocards[taid,stmid,dtg],verikey,vvar)
                            #print 'tttttttt ',ocards[taid,stmid,dtg]
                        else:
                            #print 'eeeeeee ',taid,stmid,dtg
                            ocards[taid,stmid,dtg]="%10s %s %d %s %3d %6s %6.1f"%(taid,dtg,ttau,stmid,vmax,verikey,vvar)
                            MF.loadDictList(ovars,taid,vvar)

    MF.uniqDictList(ostmids)
    
    for tdtg in tdtgs:
        
        tstmids=ostmids[tdtg]
        
        for tstmid in tstmids:

            vvars=[]
            naids=len(taids)
            for n in range(0,naids):
                taid=taids[n]

                try:
                    ocard=ocards[taid,tstmid,tdtg]
                except:
                    ocard=None

                if(ocard == None): continue
                
                tt=ocard.split()
                fcvmx=float(tt[6])
                try:
                    fcvbias=float(tt[8])
                except:
                    fcvbias=-999

                vvars.append(fcvmx)

                #fcvbiasmax=5.0
                if(len(tt) > 0):

                    #if(dobigbias and fcvbias != -999 and (fcvbias > fcvbiasmax) ):
                    #    print ocard
                    #elif(dobigbias == 0):
                    #    print ocard

                    if(n == naids-1 and naids >= 2):
                        ocard="%s %6.1f"%(ocard,vvars[n]-vvars[0])

                    print ocard
        
        if(len(taids) > 1): print

    return(ovars)



    
#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local methods
#

def getStats(ptype,taus,taids,tstmids,vds,
             filterdtgopt=None):
    
    if(ptype == 'fe'):
        verivars=[
            ('fe','mean','fe'),
            ]
    elif(ptype == 'gainxyfe'):
        verivars=[
            ('fe','gainxy','fe'),
            ]
    elif(ptype == 'gainxyfe'):
        verivars=[
            ('fe','gainxy','fe'),
            ]
    elif(ptype == 'gainxyvmax'):
        verivars=[
            ('vme','gainxyvmax','vme'),
            ]
    elif(ptype == 'vbias'):
        verivars=[
            ('vme','mean','vbias'),
            ('vme','amean','vme'),
            ('fcvmax','mean','fcvm'),
            ]
        
    elif(ptype == 'nice'):
        verivars=[
            ('nice','amean','nice'),
            ('niceb','mean','niceb'),
            ]
        
    elif(ptype == 'pbias'):
        verivars=[
            ('pmine','mean','pbias'),
            ('pmine','amean','pmine'),
            ('fcpmin','mean','fcpmin'),
            ('btpmin','mean','btpmin'),
            ]

    elif(ptype == 'gainxyvbias'):
        verivars=[
            ('vme','gainxyvbias','vbias'),
            ('vme','gainxyvbias','vme'),
            ]

    elif(ptype == 'vmxmn'):
        verivars=[
            ('fcvmax','mean','fcvm'),
            ('btvmax','mean','btvm'),
            ]

    ostats={}
    allstats={}
    cases={}
    casedtgs={}

    # -- take taids and copy to itaids so we can override with the hfipBase dic later
    # forces calc using first model
    #
    
    itaids=copy.deepcopy(taids)

    for n in range(0,len(verivars)):

        vv=verivars[n]
        
        verivar=vv[0]
        veristat=vv[1]
        verikey=vv[2]

        lists={}
        stats={}

        bdtg0='2011082300'
        tau0=120.0

        # collect lists of verivars
        #
        MF.sTime('make lists')
        for tau in taus:
            fes={}
            
            for taid in itaids:

                for tstmid in tstmids:

                    vd=vds[taid,tstmid]
                    if(vd == None):
                        print 'NNNNNNNNNN from DSs for ',taid,tstmid,tau
                        sys.exit()

                    #vd.ls()

                    vd.AT.ls()
                    vd.BT.ls()

                    btrk=vd.BT.btrk
                    atrk=vd.AT.atrks

                    adtgs=atrk.keys()
                    adtgs.sort()

                    bdtgs=btrk.keys()
                    bdtgs.sort()

                    xy={}
                    xy0={}
                    xy1={}
                    xy2={}
                    xy2p={}
                    xy2n={}
                    xys=[]

                    axy={}
                    axy0={}
                    axy1={}
                    axy2={}
                    axy2p={}
                    axy2n={}
                    axys=[]

                    try:
                        ays=atrk[bdtg0]
                    except:
                        ays={}

                    for bdtg in bdtgs:

                        x=mf.dtgdiff(bdtgs[0],bdtg)
                        y=btrk[bdtg][2]
                        xy[x]=y
                        axy[x]=None

                        print 'bbb ',bdtg,btrk[bdtg][2]

                        tau=mf.dtgdiff(bdtg0,bdtg)
                        y0=btrk[bdtg0][2]

                        if(tau == 0.0): x0=x

                        if(tau >= 0.0):
                            
                            if(tau <= tau0):

                                if(tau == tau0):
                                    yFC=ays[tau0][2]
                                    yBT=btrk[bdtg][2]
                                    vme=yFC-yBT
                                    vmeABS=abs(vme)
                                
                                try:
                                    ay=ays[tau][2]
                                except:
                                    ay=0.0

                                axy[x]=ay
                        
                                if(tau == 0): ay0=ays[tau][2]
                                    
                                print 'tau: ',tau,'b: ',y0,'ay0: ',ay0,'ay: ',ay
                                
                                # -- bt
                                #
                                
                                xy0[x]=y0
                                xy1[x]=y

                                y2=y-y0
                                x2=x-x0
                                print 'yyy2222 ',x2,y2
                                xy2[x2]=y2

                                xy2p[x2]=0.0
                                xy2n[x2]=0.0
                                
                                if(y2 > 0.0):
                                    xy2p[x2]=y2
                                elif(y2 < 0.0):
                                    xy2n[x2]=y2

                                    
                                # -- atrk
                                #
                                axy0[x]=ay0
                                axy1[x]=ay

                                ay2=ay-ay0
                                axy2[x2]=ay2
                                print 'yyy2222 ',x2,ay2

                                axy2p[x2]=0.0
                                axy2n[x2]=0.0
                                
                                if(ay2 > 0.0):
                                    axy2p[x2]=ay2
                                elif(ay2 < 0.0):
                                    axy2n[x2]=ay2
                                    

                                
                            #else:
                            #    xy0[y]=x

                    tS=tsPlot(xy)
                    tS0=tsPlot(xy0)
                    tS1=tsPlot(xy1)
                    tS2=tsPlot(xy2)
                    tS2p=tsPlot(xy2p)
                    tS2n=tsPlot(xy2n)

                    nicb=integrate.simps(tS2.y,tS2.x)/tau0
                    nicbp=integrate.simps(tS2p.y,tS2p.x)/tau0
                    nicbn=integrate.simps(tS2n.y,tS2n.x)/tau0
                    print 'bbbb nicb:',nicb,'p: ',nicbp,' n: ',nicbn

                    xys.append(tS)
                    xys.append(tS0)
                    xys.append(tS1)

                    #xyP=PlotXYs(xys)
                    #xyP.plot(doshow=0,
                    #pngpath='/tmp/t.png',
                    #         yb=0.0,
                    #        ye=150.0,
                    #         )
                    
                    atS=tsPlot(axy)
                    atS0=tsPlot(axy0)
                    atS1=tsPlot(axy1)
                    atS2=tsPlot(axy2)
                    atS2p=tsPlot(axy2p)
                    atS2n=tsPlot(axy2n)


                    xys.append(atS)
                    xys.append(atS0)
                    xys.append(atS1)
                    xyP=PlotXYs(xys)
                    
                    nicf=integrate.simps(atS2.y,atS2.x)/tau0
                    nicfp=integrate.simps(atS2p.y,atS2p.x)/tau0
                    nicfn=integrate.simps(atS2n.y,atS2n.x)/tau0
                    print 'ffff nicf:',nicf,'p: ',nicfp,' n: ',nicfn

                    print 'VVVVVVVVVVVVVVVVVV ',yFC,yBT
                    xyP.t1='Net Intensity Change Knots (NICK) for IRENE %s tau=%03d h\nAid: %s'%(bdtg0,tau0,taid.upper())
                    xyP.t2='BT: %4.1f Aid: %4.1f nickERR: %4.1f  VMAXerr: %4.1f'%(nicb,nicf,nicf-nicb,vme)

                    xyP.plot(doshow=1,
                             pngpath='/tmp/t.png',
                             yb=0.0,
                             ye=150.0,
                             )
                    
                    sys.exit()
                    
                    dlist=vd.GetVDVarlist(verivar,tau)
                    vd.addList2DictList(fes,taid,dlist)

            if(len(itaids) > 1 and dohomo):
                fes=vd.HomoVDdics(fes,itaids,tstmid,tau,forcehomo=forcehomo,verb=verb)

            for taid in itaids:
                dlist=fes[taid]
                lists[taid,tau,verikey]=dlist
        MF.dTime('make lists')


        # make list of cases by tau
        #
        dofilt=0
        if(dofilt):
            rc=filterListsbyTau(lists,taus,taids,verikey,fixtau=120)
        
        if(filterdtgopt != None):
            rc=filterListsbyDtgs(lists,filterdtgopt,taids,taus,verikey)
        
        #(taids,lists,taus)=lagListsbyTau(lists,taids,verikey)
        #taus=[24]

        # do the stats on the lists
        #
        stime=timer()
        for tau in taus:
            fixtaid=taids[-1]
            
            if(fixtaid == 'hfip'):
                (mean,n)=hfipBase[verikey][tau]
                (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix)=(mean,mean,0.0,mean,mean,n)
            else:
                listfix=lists[fixtaid,tau,verikey]
                rc=vd.SimpleListStats(listfix,verb=0,undef=-999)
                (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix)=rc
                rc=vd.SimpleListStats(listfix,verb=0,undef=-999)
                
            for taid in taids:
                if(taid == 'hfip'):
                    (mean,n)=hfipBase[verikey][tau]
                    (mean,amean,sigma,max,min,n)=(mean,mean,0.0,mean,mean,n)
                else:
                    dlist=lists[taid,tau,verikey]
                    rc=vd.SimpleListStats(dlist,verb=0,undef=-999)
                    (mean,amean,sigma,max,min,n)=rc
                    
                stats[taid,tau]=(mean,amean,sigma,n)
                
                if(veristat == 'mean'):    ostat=(mean,n)
                elif(veristat == 'amean'): ostat=(amean,n)
                elif(veristat == 'sigma'): ostat=(sigma,n)
                elif(veristat == 'gainxy'):
                    gain=((meanfix-mean)/meanfix)*100.0
                    if(tau == 0): gain=0.0
                    ostat=(gain,n)
                elif(veristat == 'gainxyvbias'):
                    gain=(abs(mean)/amean)*100.0
                    if(tau == 0): gain=0.0
                    ostat=(gain,n)
                elif(veristat == 'gainxyvmax'):
                    gain=((ameanfix-amean)/ameanfix)*100.0
                    if(tau == 0): gain=0.0
                    ostat=(gain,n)
                print 'SSSSSHHHHH %15s %3d %10s:'%(taid,tau,verikey),' %10.1f n: %3d'%(ostat[0],ostat[1]),\
                      '   m,a,s,mx,mn,n: %6.1f %6.1f %6.1f %6.1f %6.1f %d'%(mean,amean,sigma,max,min,n)
                allstats[taid,tau,verikey]=(ostat,mean,amean,sigma,max,min,n)
                ostats[taid,tau,verikey]=ostat
        mf.Timer('stats from listsL ---- ',stime)

        # collect cases
        #
        for taid in itaids:
            for tau in taus:
                ll=lists[taid,tau,verikey]
                ll.sort()

                for l in ll:
                    if(l[0][0] == 1):
                        dtg=l[0][1]
                        stmid=l[0][2]
                        vmax=l[0][3]
                        vvar=l[1]
                        try:
                            casedtgs[tau,verikey].append(dtg)
                        except:
                            casedtgs[tau,verikey]=[]
                            casedtgs[tau,verikey].append(dtg)

                        cases[taid,stmid,dtg,tau,verikey]=(stmid,vmax,vvar)

        for tau in taus:
            try:    casedtgs[tau,verikey]=mf.uniq(casedtgs[tau,verikey])
            except: continue


        ss=SumStats(taids,tstmids,
                    verivars,ostats,
                    cases,casedtgs)

        rc=(ss,verivars,ostats,allstats,cases,casedtgs)

    return(rc)

    

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
            }


        self.options={
            'yearopt':['y:',None,'a','year'],
            'endTau':['E:',120,'i','last tau to output stats'],
            'override':['O',0,1,'override'],
            'overrideNL':['o',0,1,'overrideNL -- force making of adeck noloads'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'dols':['l',0,1,'1 - list'],
            'dohomo':['H',1,0,'do NOT do homo comp if set,default is to do homo comp'],
            'forcehomo':['h',0,1,'forcehomo = 1 does logical AND on two VDlists that are not the exact same size'],
            'stmopt':['S:',None,'a','stmopt'],
            'pcase':['c:','pleaseset','a','pcase'],
            'ptype':['p:','fe','a','ptype = fe (tracke fe) | vbias (intensity) | pod (prob of detect) | pbias'],
            'pdir':['D:','.','a','pdir = . default'],
            'aidopt':['T:',None,'a','taid'],
            'toptitle1':['1:',None,'a','toplabel1'],
            'toptitle2':['2:',None,'a','toplabel2'],
            'warn':['W',0,1,'warning'],
            'reloadFromPyp':['P',0,1,'relocad state from pyp'],
            'do9xNOT':['9',1,0,'if set dofilt9x=0; do9xrelab=0'],
            'dtgopt':['d:',None,'a','dtgopt'],
            'filterdtgopt':['D:',None,'a','filterdtgopt -- in getStats(), filter out dtgs outside the open interval dtgopt '],
            'doplot':['X',0,1,'if set doplot=1 -- .show()'],
            'lsttau':['t:',-1,'i','lsttau -- tau to do an ls of cases'],
            'dobigbias':['B',0,1,'if ls of cases by tau; only print big bias'],
            'doshow':['s',0,1,'show() in pylab'],
            'doHistplot':['I',0,1,'do histogram for a dtau'],
            }


        self.purpose='''
purpose -- analyze vdecks by year(s) source(s)

sources: %s'''%(self.sources)
        self.examples='''
%s rtfim -T fim8 -S e.9,l.9 -y 2009
%s ncep,ecmwf -S w -T avno,edet -D 2010010100.2010072712 :: do stats on avno and edet aids before the gfs upgrade on 2010072712
'''


    def ChkSource(self):

        iok=0
        for iss in self.sourceopt.split(','):
            for s in self.sources:
                if(iss == s): iok=1 ; break

        return(iok)


def getAllTaus(endTau):

    if(endTau == 48):
        taus=[0,12,24,36,48]
    elif(endTau == 72):
        taus=[0,12,24,36,48,72]
    elif(endTau == 96):
        taus=[0,12,24,36,48,72,96]
    else:
        taus=[0,12,24,36,48,72,96,120]

    return(taus)
        
        

    

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer('all')
argstr="pyfile 2009,2010 rtfim,rtfimy -T fim8,f8cy -S 07l.9 -W"

argv=argstr.split()
argv=sys.argv

CL=AdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

iyearopt=yearopt
if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear

taus=getAllTaus(endTau)


pyppath='/tmp/vda.pyp'

if(reloadFromPyp):

    PS=open(pyppath)
    pyp=pickle.load(PS)

    if(ptype == 'pod'):
        (taus,sources,years,
         taids,tstmids,ss)=pyp

    else:
        (taus,verivars,
         sources,years,
         taids,tstmids,
         ostats,allstats,
         cases,casedtgs,
         ss)=pyp


    verikeys=[]
    kks=ostats.keys()
    for kk in kks:
        verikeys.append(kk[2])

    verikeys=mf.uniq(verikeys)
    if(ptype == 'vbias'):
        verikeys=['vme','vbias']

    if(ptype == 'nice'):
        verikeys=['nicea','nice']

    for verikey in verikeys:
        for tau in taus:
            for taid in taids:
                (ostat,mean,amean,sigma,max,min,n)=allstats[taid,tau,verikey]
                print 'SSSSSHHHHH %15s %3d %10s'%(taid,tau,verikey),' %10.1f n: %3d'%(ostat[0],ostat[1]),\
                      '   m,a,s,mx,mn,n: %6.1f %6.1f %6.1f %6.1f %6.1f %d'%(mean,amean,sigma,max,min,n)
        print
    MF.dTimer('all')

else:
    
    PS=open(pyppath,'w')

    if(not(CL.ChkSource())):
        print 'WWW not a standard sourceopt:',sourceopt,' try using adeck from AD.AdeckSource class...'


    if(stmopt != None): getstms=MakeStmList(stmopt,verb=0,dofilt9x=do9xNOT)
    else: getstms=None

    if(aidopt != None): getaids=aidopt.split(',')
    else: getaids=None
    
    if(dtgopt != None): dtgs=mf.dtg_dtgopt_prc(dtgopt)
    else: dtgs=None
    
    stime=timer()
    DSss={}
    dsbdir="%s/DSs"%(TcDataBdir)
    dbtype='vdeck'
    sources=sourceopt.split(',')
    years=yearopt.split(',')

    if(getstms != None and iyearopt == None):
        years=getYearsFromStmids(getstms)
        
    noDSs=DataSets(bdir=dsbdir,name='NoLoad_vdeck.pypdb',dtype='noloads',verb=verb)

    mDs={}
    tstmids=taids=[]

    for year in years:
        for source in sources:
            dbname="%s_%s_%s"%(dbtype,source,year)
            dbfile="%s.pypdb"%(dbname)
            DSss[source,year]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=1)
            
            (aids,stmids)=GetAidsStormsFromDss(DSss[source,year],getaids,getstms,dofilt9x=do9xNOT)
            tstmids=tstmids+stmids
            taids=taids+aids
            print 'ssssssssssss ',source,year,aids

    mf.Timer('getDSs ---- ',stime)


    tstmids=mf.uniq(tstmids)
    taids=mf.uniq(taids)


    if(len(taids) > maxTaids):
        print 'EEE too many aids to vda; N: ',len(taids)
        sys.exit()

    if(getaids != None):
        taids=getaids

    if(dols):
        print 'DDDD #DSss: ',len(DSss)
        for k in DSss.keys():
            vDS=DSss[k]
            print 'DDDDDDDDD ',k
            LsAidsStormsDss(DSss[k],None,None,dofilt9x=do9xNOT)
        sys.exit()

    else:
        print 'WWWWWWWWWWWWW working tstmids: ',tstmids
        print 'WWWWWWWWWWWWW working   taids: ',taids


    # get vd dict
    #
    stime=timer()
    if(dtgs != None):
        tcD=TcData(dtgopt=dtgs[-1])
        for dtg in dtgs:
            (tstmids)=tcD.getStmidDtg(dtg)
        tstmids=mf.uniq(tstmids)
        vds=getVdsFromDSss(DSss,taids,tstmids)
        mf.Timer('getvds dtgs ---- ',stime)
    else:
        vds=getVdsFromDSss(DSss,taids,tstmids)
        mf.Timer('getvds  ALL ---- ',stime)


    if(ptype == 'pod'):
        # -- counts analysis
        #
        stime=timer()
        counts=getCountsVds(vds,taus,verb=verb)
        ss=PodStats(taids,tstmids,counts)
        mf.Timer('PodStats    ---- ',stime)

        # -- pickle current state
        #
        pyp=(taus,sources,years,
             taids,tstmids,ss)


    
    else:

        rc=getStats(ptype,taus,taids,tstmids,vds,filterdtgopt)
        (ss,verivars,ostats,allstats,cases,casedtgs)=rc        
        # -- pickle current state
        #
        pyp=(taus,verivars,
             sources,years,
             taids,tstmids,
             ostats,allstats,
             cases,casedtgs,
             ss)
        

    pickle.dump(pyp,PS)
    PS.close()


if(lsttau >= 0):
    ovars=lsCases(taids,cases,casedtgs,verivars,ttau=lsttau,dobigbias=dobigbias)

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


        rc=pltHist(list0,list1,list2,
                   stmopt,
                   xlab='forecast error [nm]',
                   var1=var1,
                   var2=var2,
                   tag0=tag0,
                   donorm=1,
                   docum=1,
    #               xmax=400.0,xmin=0.0,xint=50.0,
    #               ymax=50,   ymin=0,  yint=10,
    #               ymax=1,   ymin=0,  yint=0.1,
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

    elif(ptype == 'gainxyfe'):
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        
    elif(ptype == 'gainxyvmax'):
        pverikey='vme'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        

    elif(ptype == 'vbias'):
        pverikey='vbias'
        pverikey1='vme'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(mf.find(pcase,'ens')):
            toptitle1='HFIP 2009 Summer Demo Period -- Hi-Res Ensemble Systems -- Mean v Spread'
        else:
            if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'nice'):
        pverikey='nice'
        pverikey1='nicea'
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
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Prob Of Detection [POD;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        ostats=ss.ostats

    elif(ptype == 'gainxyvbias'):
        pverikey='vbias'
        pverikey1='vbias'
        do1stplot=0
        do2ndplot=1

        toptitle2='Ratio abs(bias)/mean(abs) Intensity Error [%] :: percentage of Error from bias'


    sdicts=[]
    ndicts=[]

    for n in range(0,len(taids)):
        taid=taids[n]
        sdict1={}
        sdict={}
        ndict={}

        for tau in taus:
            sdict1[tau]=ostats[taid,tau,pverikey1][0]
            sdict[tau]=ostats[taid,tau,pverikey][0]
            ndict[tau]=ostats[taid,tau,pverikey][1]

        if( (pcase == 'ens.eemn' or pcase == 'ens.f8mn') and (n == len(taids)-1) ):
            ss.models=ss.models[0:-1]
            continue

        sdicts.append((sdict1,sdict))
        ndicts.append(ndict)


    pss=SumStatsPlot(ss,pcase,ptype,pdir=pdir)
    if(verb): pss.ls()

    pss.setPlottitles(toptitle1,toptitle2)
    pss.setControls()
    pss.simpleplot(ss.models,sdicts,ndicts,ss.labaids,ss.colaids,
                   ilmarker=ss.markaids,
                   do1stplot=do1stplot,
                   do2ndplot=do2ndplot,
                   dopng=1,
                   do2ndval=do2ndval,
                   doline=0,
                   doshow=doshow)
    


MF.dTimer('all')


sys.exit()
