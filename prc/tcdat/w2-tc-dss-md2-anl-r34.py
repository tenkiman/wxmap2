#!/usr/bin/env pythonw

from tcbase import *

def parsePcard(pcard):

    if(pcard == None):
        return(pcard)
    tt=pcard.split()
    # 00 - '2017110912', 
    # 01 - '19L.2017', 
    # 02 - '040', 
    # 03 - '998', 
    # 04 - '45.5N', 
    # 05 - '47.0W', 
    # 06 - '130',
    # 07 - '---', 
    # 08 - '18.6',
    # 09 - '21.6',
    # 10 - 'B',
    # 11 - 'LO',
    # 12 - 'WN',
    # 13 - 'ESB',
    # 14 - '23/23',
    # 15 - 'lf:',
    # 16 - '0.00',
    # 17 - 'RINA']
    dtg=tt[0]
    
    vmax=float(tt[2])
    pmin=-9999.
    if(tt[3] != '----'): pmin=float(tt[3])
    
    clat=tt[4]
    clon=tt[5]
    r34=-999.
    if(tt[6] != '---'): r34=float(tt[6])
    tcState=tt[11]
    flgtc=IsTc(tcState)
    
    rc=(dtg,vmax,pmin,clat,clon,r34,flgtc)
    return(rc)
    
def makeWarnCard(stmid,dtg,flgtc,clat,vmax,pmin,r34):
    
    wcard=None
    if(r34 > 0.):
        if(flgtc == 1):
            if(r34 > r34max): wflg='WWW-TTT(R34-TC)'
        elif(flgtc == 3):
            if(r34 > r34max): wflg='WWW-SSS(R34-SS)'
        elif(flgtc == 3):
            if(r34 > r34max): wflg='WWW-XXX(R34-XT)'
        wcard='%s: %s %s %d %s %s %3.0f %4.0f  %4.0f'%(wflg,stmid,dtg,flgtc,clat,vmax,pmin,r34)
        
    return(wcard)
        
    
def compStmCards(stmid,dtg,tau,pcard0,pcardfc):
    
    def getR34(rc0,rcfc):
        
        r340=rc0[-2]
        flgtc0=rc0[-1]
        
        r34fc=-999.
        flgtcfc=999
        
        #print ' rrr0',rc0
        #print 'rrrfc',rcfc
        
        if(rcfc != None): r34fc=rcfc[-2] ; flgtcfc=rcfc[-1] ; vmaxfc=rcfc[1]
        #print '33333',r34fc,flgtc0,flgtcfc
        
        r34o=-999.
        vmaxo=-99.
        if(r34fc > 0.0 and flgtc0 == 1 and flgtcfc == 1 ):
            r34o=r34fc
            vmaxo=vmaxfc
            
        #print 'fffff',r34o,vmaxo
        return(r34o,vmaxo)
        
        
    rc0=parsePcard(pcard0)
    rcfc=parsePcard(pcardfc)
    
    (r34o,vmaxo)=getR34(rc0, rcfc)
    
    return(r34o,vmaxo)

def anlStmDtgs(stmdtgs,warn=1,r34max=200,verb=0):
 
    r34Vmaxs={}
    
    stmids=stmdtgs.keys()
    stmids.sort()
    taus=[0,12,24,36,48,72,96,120]
    
    for stmid in stmids:
        dtgs=stmdtgs[stmid].keys()
        dtgs.sort()
        
        for dtg in dtgs:
            dtg0=dtg
            
            for tau in taus:

                dtgfc=mf.dtginc(dtg0,tau)
                pcard0=stmdtgs[stmid][dtg0]
                
                try:
                    pcardfc=stmdtgs[stmid][dtgfc]
                except:
                    pcardfc=None
                    
                (r34tau,vmaxtau)=compStmCards(stmid,dtg,tau,pcard0,pcardfc)
                
                if(r34tau > 0. and vmaxtau > 0.):
                    #MF.append2TupleKeyDictList(r34Vmaxs, tau, 'r34', r34tau)
                    #MF.append2TupleKeyDictList(r34Vmaxs, tau, 'vmax', vmaxtau)
                    MF.append2KeyDictList(r34Vmaxs, tau, 'r34', r34tau)
                    MF.append2KeyDictList(r34Vmaxs, tau, 'vmax', vmaxtau)
                    

    return(r34Vmaxs)
    
    
def pltHist(lista,
            stmopt,
            listb=None,
            listc=None,
            list0=None,
            tlist=None,
            ptitle1=None,
            ptitle2=None,
            ptaus=None,
            pcnttaus=None,
            donorm=1,
            docum=1,
            xmax=None,
            xmin=None,
            xint=None,
            ymax=None,
            ymin=0,
            yint=5,
            binint=None,
            dostacked=0,
            var1='Dev',
            var2='NonDev',
            pngpath=None,
            tag=''):

    import matplotlib.pyplot as plt
    from numpy import array,arange

    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=9)    # fontsize of the tick labels

    median0=mediana=medianb=medianc=None
        
    rca=SimpleListStats(lista,hasflag=0)
    
    meana=rca[0]
    sigmaa=rca[2]
    xmaxa=rca[3]
    xmina=rca[4]
    mediana=rca[-2]
    
    
    if(listb != None):
        rcb=SimpleListStats(listb,hasflag=0)
        meanb=rcb[0]
        sigmab=rcb[2]
        xmaxb=rcb[3]
        xminb=rcb[4]
        medianb=rcb[-2]
        
    if(listc != None):
        rcc=SimpleListStats(listc,hasflag=0)
        meanc=rcc[0]
        sigmac=rcc[2]
        xmaxc=rcc[3]
        xminc=rcc[4]
        medianc=rcc[-2]
        
    if(list0!= None):
        rc0=SimpleListStats(list0,hasflag=0)
        mean0=rc0[0]
        sigma0=rc0[2]
        xmax0=rc0[3]
        xmin0=rc0[4]
        median0=rc0[-2]
        

    if(donorm and ymax == None):
        ymax=0.75
        yint=0.25

    if(docum):
        ymax=1.0
        yint=0.25


    xmax=450
    xmin=0
    xint=25
    
    if(xmax == None): xmax=xmaxa
    if(xmin == None): xmin=xmina
    if(xint == None): xint=10
    
    binint=xint
    nbins=mf.nint((xmax-xmin)/xint)	

    hrange=[xmin,xmax]

    fc1='green'
    fc2='red'
    fc3='blue'
    ptype='bar'
    ec1='black'
    ec2='black'
    ec3='black'

    if(donorm or docum):
        ylab='prob [0-1]'
    else:
        ylab='N'

    xa=lista

    (n1, bins, patches) = plt.hist(xa,nbins,histtype='bar',range=hrange,\
                                   normed=donorm,cumulative=docum,
                                   facecolor=fc1,edgecolor=ec1,
                                   alpha=1.0,rwidth=1.0)

    if(listb != None):
        xa=listb

        (n1, bins, patches) = plt.hist(xa,nbins,histtype='bar',range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       facecolor=fc2,edgecolor=ec2,
                                       alpha=1.0,rwidth=0.75)
        
    if(listc != None):
        xa=listc
        
        (n1, bins, patches) = plt.hist(xa,nbins,histtype='bar',range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       facecolor=fc3,edgecolor=ec3,
                                       alpha=1.0,rwidth=0.35)
        


    ymax1=n1.max()

    maxy=ymax1

    print 'yyyyyyyymmmmmmm',ymax
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

    xlab='R34 [nmi]'
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    print 'pppppppp',ptitle2
    if(ptitle2 == None):
        ptitle2="Stmopt: %s"%(stmopt)

    
    ptau0=None
    ntau0=None
    if(ptaus != None):
        if(len(ptaus) == 4):
            
            ptau0=ptaus[0]
            ptaua=ptaus[1]
            ptaub=ptaus[2]
            ptauc=ptaus[3]
            
            ntau0=pcnttaus[0][0]
            ntaua=pcnttaus[ptaua][0]
            ntaub=pcnttaus[ptaub][0]
            ntauc=pcnttaus[ptauc][0]
            
            pcn0=pcnttaus[0][1]

            
        else:

            ptaua=ptaus[0]
            ptaub=ptaus[1]
            ptauc=ptaus[2]

            ntaua=len(lista)
            ntaub=len(listb)
            ntauc=len(listc)
        
        pcna=pcnttaus[ptaua][1]
        pcnb=pcnttaus[ptaub][1]
        pcnc=pcnttaus[ptauc][1]
        


    if(pcnttaus != None):
        
        if(median0 != None): md0=median0
        
        if(ptau0 != None):
            
            if(median0 != None and mediana != None):
                ptitle=" tau0 N: %3d FC: %3.0f%% MD: %3.0f   tau%-3d  N: %3d FC: %3.0f%%  MD: %3.0f"%\
                    (ntau0,pcn0,median0,ptaua,ntaua,pcna,mediana)
            else:
                ptitle=" tau0 N: %3d FC: %3.0f%%   tau%-3d  N: %3d FC: %3.0f%%"%(ntau0,pcn0,ptaua,ntaua,pcna)
            
        else:
            ptitle="tau%-3d  N: %3d FC: %3.0f%%"%(ptaua,ntaua,pcna)
        
        if(listb != None):
            if(medianb != None):
                ptitle="%s\n  tau%-3d N: %4d FC: %3.0f%% MD: %3.0f"%(
                    ptitle,ptaub,ntaub,pcnb,medianb)
            else:
                ptitle="%s\n  tau%-3d  N: %4d FC: %3.0f%%"%(
                    ptitle,ptaub,ntaub,pcnb)
    
        if(listc != None):
            if(medianc != None):
                ptitle="%s  tau%-3d  N: %3d FC: %3.0f%% MD: %3.0f"%(
                    ptitle,ptauc,ntauc,pcnc,medianc)
            else:
                ptitle="%s  tau%-3d  N: %3d FC: %3.0f%%"%(
                    ptitle,ptauc,ntauc,pcnc)
        
    else:
        
        ptitle=" tau   %-3d  N: %3d Mn: %4.1f Md: %4.1f $\sigma$: %4.1f"%(ptaua,
            len(lista),meana,mediana,sigmaa)
        
        if(listb != None):
            ptitle="%s\ntau  %-3d  N: %3d Mn: %4.1f Md: %4.1f $\sigma$: %4.1f"%(
                ptitle,ptaub,len(listb),meanb,medianb,sigmab)
    
        if(listc != None):
            ptitle="%s  tau %-3d  N: %3d Mn: %4.1f Md: %4.1f $\sigma$: %4.1f"%(
                ptitle,ptauc,len(listc),meanc,medianc,sigmac)


    if(ptitle1 != None):
        ptitle=ptitle1+"\n%s"%(ptitle)
    else:
        ptitle=ptitle+"\n%s"%(ptitle2)

    plt.title("%s"%(ptitle),fontsize=9)
    
    plt.xlim(xmin,xmax)
    xaxis=arange(xmin,xmax+1,xint)
    plt.xticks(xaxis)

    #ymax=None
    if(ymax != None):
        plt.ylim(ymin,ymax)
        yaxis=arange(ymin,ymax+0.001,yint)
        plt.yticks(yaxis)
            
    plt.grid(True)

    if(pngpath == None):
        pngpath="/tmp/r34.%s.png"%(stmopt)

    print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)

    plt.show()


def errMD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()



class MdeckCmdLine(CmdLine):

    otags=getMd2DSsTags()
    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'md2tag':         ['t:',None,'a','year'],
            'filtTCs':        ['T',0,1,'only print out TCs'],
            'printdtgs':      ['D',0,1,'ls all storms in the dtgs of a single stmid'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'doCARQonly':     ['C',1,0,'do NOT do ops = use 9X ids always'],
            'sumonly':        ['s',0,1,'list storm stats only'],
            'scp2jet':        ['J',1,0,'do NOT scp to jet/theia'],
            'dotcvitals':     ['v',0,1,'output tcvitals'],
            'tcvPath':        ['p:',None,'a','output path for tcvitals'],
            'ptitle1':        ['1:',None,'a',' set top title'],
            'dupchk':         ['R',1,0,'do NOT remove dups from list'],
            'ls9x':           ['9',0,1,'ls stats on 9x'],
            'doanl':          ['a',0,1,'analyze stm liftime histogram'],
            'countsOnly':     ['K',0,1,'output counts by dtg'],
            #'cacheOverride':  ['c',0,1,'override or reset the /ptmp/mdecks2-all.pypdb cache'],
            #'keepPrevYears':  ['k',1,0,'do NOT keep prev years in the /ptmp/mdecks2-all.pypdb cache'],
            'filtopt':        ['f:',None,'a',"""
            
FF.TT.NN
FF: all|season|dev|CC|CC-bt|CC-9x
TT: latb|latmn|stmlife|9xlife
NN: 0 - counts; 1 - donorm=1; 2 donorm=1,docum=1          
"""],
            'tcbogPath':      ['P:',None,'a','output tcbog intput'],
            'dotrkplot':      ['X',0,1,'rsync to jet/theia'],
            'doWorkingBT':    ['W',0,1,'using working/b*.dat for bdecks vice ./b*.dat'],
            
            }

        self.purpose='''
analyze mdecks2'''
        
        self.purpose=self.purpose+'''
-t tags: %s'''%(self.otags)
        
        self.examples='''
%s -d cur12
%s -S l.13 -s -b # summary based on final BT bdeck (may have early 9X clipped as at NHC)
%s -S l.13 -s -C # summary based on operational merged a/bdeck'''


    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


# -- control output of storm listing by dtg
#
doBT=0
if(not(dobt)):  doBT=1  # default dobt=0 doBT=1  -- replace all 
if(doCARQonly): doBT=0  # ops     dobt=0 doBT=0  -- pure ops  : picks available from CARQ (adeck) first then bdeck (?)


# -- dddddddddddddddddddddddddddddddddddddddddddddddddddd -- dtgs
#
if(dtgopt != None):

    selectNN=1
    if(ls9x or doCARQonly): selectNN=0

    tcD=TcData(dtgopt=dtgopt,md2tag=md2tag,doWorkingBT=doWorkingBT,verb=verb)
    dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)
    
    # -- llllllllllllllllllllllllllllllllllllllllllllllll -- ls TCs by dtg
    #
    tcD.lsDSsDtgs(dtgs,dobt=dobt,dupchk=dupchk,selectNN=selectNN,countsOnly=countsOnly,filtTCs=filtTCs)
    sys.exit()


# -- sssssssssssssssssssssssssssssssssssssssssssssssssss -- storms
#
if(stmopt != None):

    tcD=TcData(stmopt=stmopt,md2tag=md2tag,doWorkingBT=doWorkingBT,verb=verb)

    lstm=len(stmopt.split('.')[0])
    ltt1=len(stmopt.split(','))

    didold=0
    ostmids=[]
    dobtStms=0
    
    # -- detect if 9X stmopt
    #
    if(dobt or doBT and stmopt[0] != '9'): dobtStms=1
 
    if(lstm == 1 or lstm == 3 or mf.find(stmopt,'cc') or ltt1 > 1 ):
        # -- main stmlist
        stmids=tcD.makeStmListMdeck(stmopt,dobt=dobtStms,cnvSubbasin=0,verb=verb)
    else:
        didold=1
        ostmids=MakeStmList(stmopt)
        
    # -- if used old stm lister, put through new one that uses the stmids keys; 
    # -- needed for 9X=> [a-z][0-9]

    if(didold):
        print 'III(md2a.didold)...stmopt: ',stmopt
        stmids=[]
        for ostmid in ostmids:
            stmids=stmids+tcD.makeStmListMdeck(ostmid,dobt=dobt,cnvSubbasin=0)

    stmids.sort()
    
    #  0 yyyy
    #  1 stm,
    #  2 tctype
    #  3 sname[0:9]
    #  4 ovmax
    #  5 tclife
    #  6 stmlife
    #  7 latb,
    #  8 lonb,
    #  9 bdtg,
    # 10 edtg,
    # 11 latmn
    # 12 latmx
    # 13 lonmn
    # 14 lonmx,
    # 15 stcd
    # 16 oACE
    # 17 nED
    # 18 nRW
    # 19 RIstatus
    # 20 timeGen
    # 21 stm9x
    # 22 ogendtg
        
    #llllllllllllllllllllllllllllllllllllllllllllllllll -- listing here
    #
    stmdtgs={}
    stmsums={}
    MF.sTimer('stmdtgs: %s'%(stmopt))
    for stmid in stmids:
        
        # -- merge both 9x and real/final bdeck
        #
        set9xfirst=1

        # -- mechanism to output only 9x in TcData.lsDSsStm
        #
        if(ls9x or Is9X(stmid)): dobt=-1
        if(doBT): dobt=2 ; set9xfirst=1   # -- want to show 9X now that we merge WN posits from NN trk into final(default)
        
        rc=tcD.getDSsStmCards(stmid,dobt=dobt,
                     set9xfirst=set9xfirst,
                     convert9x=0,
                     verb=verb)
        
        stmdtgs[stmid]=rc[0]
        stmsums[stmid]=rc[1]
        
    MF.dTimer('stmdtgs: %s'%(stmopt))

    MF.sTimer('stmdtgs-anl: %s'%(stmopt))
    r34Vmaxs=anlStmDtgs(stmdtgs,verb=verb)
    
    taus=r34Vmaxs.keys()
    
    taus.sort()
    
    pcnttaus={}
    ntau0=len(r34Vmaxs[0]['r34'])
    for tau in taus:
        listtau=r34Vmaxs[tau]['r34']
        ntau=len(listtau)
        ptau=(ntau*1.0/ntau0)*100.
        pcnttaus[tau]=(ntau,ptau)
        #print 'tttttttttttttt %03d N: %5d'%(tau,len(listtau)),'prcnt: %3.0f'%(ptau)
    
    kk=pcnttaus.keys()
    kk.sort()
    for k in kk:
        print 'ttt',k,' % ',pcnttaus[k]
    
    var='r34'
    tau=0
    tau=72
    #tau=120
    ptitle2="%s-%03d-%s"%(var,tau,stmopt)
    pngpath="/ptmp/%s.png"%(ptitle2)

    ptaus=[0,24,72,120]

    list0=r34Vmaxs[0][var]    
    list24=r34Vmaxs[24][var]    
    list72=r34Vmaxs[72][var]
    list120=r34Vmaxs[120][var]
    
    
    ymax=700
    ymax=1100
    ymin=0
    yint=100
    
    #ymax=0.10
    #ymin=0
    #yint=0.001
    
    
    rc=pltHist(list24, stmopt, listb=list72, listc=list120, list0=list0,
               ptaus=ptaus,pcnttaus=pcnttaus,
               tlist=None, ptitle1=ptitle1, ptitle2=ptitle2, donorm=0, 
               docum=0, xmax=None, xmin=None, xint=None, 
               ymax=ymax, ymin=ymin, yint=yint, binint=None, 
               dostacked=0, var1='Dev', var2='NonDev', 
               pngpath=pngpath, tag='')
    
    MF.dTimer('stmdtgs-anl: %s'%(stmopt))
        
        
        

MF.dTimer('all')
sys.exit()