#!/usr/bin/env pythonw

from tcbase import *

def pltHist(lista,listi,listo,
            stmopt,basin,year,
            tlist=None,
            ptitle2=None,
            filttype='season',
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
            doAllOnly=0,
            tag='',
            doshow=1):

    import matplotlib.pyplot as plt
    from numpy import array,arange

    xa=array(lista)
    xi=array(listi)
    xo=array(listo)

    ymaxi=xi.max()
    try:
        ymaxi=x.max()
    except:
        ymaxi=undef
        
    try:
        ymaxo=xo.max()
    except:
        ymaxo=undef

    rca=SimpleListStats(lista,hasflag=0)
    rci=SimpleListStats(listi,hasflag=0)
    rco=SimpleListStats(listo,hasflag=0)
    
    meana=rca[0]
    mediana=rca[-3]
    sigmaa=rca[2]

    meani=rci[0]
    mediani=rci[-3]
    sigmai=rci[2]

    meano=rco[0]
    mediano=rco[-3]
    sigmao=rco[2]

    if(donorm):
        ymax=0.75
        yint=0.25

    if(docum):
        ymax=1.0
        yint=0.25


    if(xmax == None): xmax=15
    if(xmin == None): xmin=0
    if(xint == None): xint=1

    if(binint == None):
        nbins=(xmax/xint)
        nbins=nbins*5
    else:
        nbins=(xmax-xmin)/binint

    xa=lista

    hrange=[xmin,xmax]

    fc1='green'
    fc2='red'
    ptype='bar'
    ec1='black'
    ec2='black'


    if(donorm or docum):
        ylab='prob [%]'
    else:
        ylab='N'

    nbins=mf.nint(nbins)

    if(doAllOnly):

        (n1, bins, patches) = plt.hist(xa,bins=nbins,histtype='bar',range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=0.75,rwidth=1.0)

        print '1111111111111' ,n1,bins
        
        n2=n1
        
        


    elif(dostacked):

        ptype='barstacked'
        ptype='bar'

        xplot=(xi,xo)
    
        (n1, bins, patches) = plt.hist(xplot,nbins,histtype=ptype,range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       color=['green', 'red'],
                                       alpha=1.0,rwidth=1.0)

    else:

        (n1, bins, patches) = plt.hist(xi,nbins,histtype='bar',range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=0.75,rwidth=1.0)

        print '1111111111111' ,n1,bins
        
        (n2, bins, patches) = plt.hist(xo,nbins,histtype='bar',range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       facecolor=fc2,edgecolor=ec2,
                                       alpha=1.0,rwidth=0.50)
        print '22222222222222 ',n2,bins


    ymax1=n1.max()
    ymax2=n2.max()

    if(ymax1 > ymax2):
        maxy=ymax1
    else:
        maxy=ymax2

    if(maxy >= 100):
        yint=20
    elif(maxy >= 50 and maxy < 100):
        yint=10
        
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


    xlab='Nada'
    if(tlist == 'stmlife'):
        xlab='Storm Life [d]'

    elif(tlist == '9xlife'):
        xlab='pre-genesis 9X Life [d]'

    elif(tlist == 'latb'):
        xlab='Begin Latitude [deg]'

    elif(tlist == 'time2gen'):
        xlab='Time to Genesis [d]'

    plt.xlabel(xlab)
    plt.ylabel(ylab)

    if(ptitle2 == None):
        ptitle2="Stmopt: %s"%(stmopt)

    if(tlist == 'time2gen'):

        ptitle="N: %d  Mn: %3.1f $\sigma$: %3.1f  Median: %3.1f\n%s"%(
            len(lista),meana,sigmaa,mediana,
            stmopt)

    elif(mf.find(filttype,'dev')):

        ni=len(listi)
        no=len(listo)
        devratio=(float(ni)/float(no))*100.0
        ptitle="%s(G) N %d Mn %3.1f $\sigma$: %3.1f %s(R) N %d Mn: %3.1f $\sigma$: %3.1f %%: %3.0f\n%s"%(
            var1,ni,meani,sigmai,
            var2,no,meano,sigmao,
            devratio,
            ptitle2)

    elif(mf.find(filttype,'seas')):

        ptitle="%s(G)  N: %d Mn: %3.1f $\sigma$: %3.1f %s(R)  N: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(
            var1,len(listi),meani,sigmai,
            var2,len(listo),meano,sigmao,
            stmopt)


        
    #ptitle="$\sigma=$"
    plt.title(r"%s"%(ptitle),fontsize=12)
    

   
    plt.xlim(xmin,xmax)
    xaxis=arange(xmin,xmax+1,xint)
    plt.xticks(xaxis)

    if(ymax != None):
        plt.ylim(ymin,ymax)
        yaxis=arange(ymin,ymax+0.001,yint)
        plt.yticks(yaxis)

    plt.grid(True)

    if(pngpath == None):
        pngpath="/tmp/9x.%s.%s.png"%(basin,year)

    print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)
    
    doCp2Aori=0
    if(doCp2Aori):
        cmd="cp %s ~/pCloudDrive/AORI/TALKS/plt/"%(pngpath)
        mf.runcmd(cmd)

    if(doshow): plt.show()



def setFilter(filtopt,stmopt):

    tt=filtopt.split('.')
    if(len(tt) != 3):
        print """EEE improper form of filtopt
FF.TT.NN
FF: all|season|dev|CC|CC-bt|CC-9x
TT: latb|latmn|stmlife|9xlife
NN: 0 - counts; 1 - donorm=1; 2 donorm=1,docum=1
"""
        sys.exit()


    filtBySeason=0
    filtByDev=0
    filtByCC=0

    tlist='stmlife'

    ymax=None
    yint=None
    xmax=10
    xmin=0
    xint=1

    ftype=tt[0]
    tlist=tt[1]
    dtype=int(tt[2])
    binint=0.25

    ptitle2="Stmopt: %s"%(stmopt)
    
    if(mf.find(ftype,'sea')): filtBySeason=1
    if(mf.find(ftype,'dev')): filtByDev=1
    if(mf.find(ftype,'CC')):
        filtByCC=1
        ptitle2="CC TC+pTC (all); Stmopt: %s"%(stmopt)
        if(mf.find(ftype,'bt')):
            filtByCC=2
            ptitle2="CC  TC only (NN); Stmopt: %s"%(stmopt)
        elif(mf.find(ftype,'9x')):
            filtByCC=3
            ptitle2="CC pTC only (9X); Stmopt: %s"%(stmopt)
            

    if(tlist == '9xlife'):
        yint=5
        xmax=10
        xmin=0
        xint=1
        binint=0.5
        
    elif(tlist == 'stmlife' or tlist == 'time2gen'):
        yint=5
        xmax=10
        xmin=0
        xint=1
        binint=0.5
        if(tlist == 'time2gen'):
            ptitle2="Time to Genesis Stmopt: %s"%(stmopt)
        
    
    elif(tlist == 'latb'):
        yint=5
        xmax=45
        xmin=0
        xint=5
        binint=5

    donorm=0
    docum=0
    if(dtype == 1):donorm=1
    if(dtype == 2):donorm=1; docum=2

    return(filtBySeason,filtByDev,filtByCC,tlist,donorm,docum,
           ymax,yint,xmax,xmin,xint,binint,ptitle2)



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
            'dotcvitals':     ['v',0,1,'output tcvitals'],
            'tcvPath':        ['p:',None,'a','output path for tcvitals'],
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
            'doshow':         ['x',1,0,'do NOT show in pltHist'],
            'doWorkingBT':    ['W',0,1,'using working/b*.dat for bdecks vice ./b*.dat'],
            'oPath':          ['o:',None,'a','write output to oPath'],
            
            'doBdeck2':       ['2',0,1,'use bdeck in bdeck2/ vice bdeck/'],
            
            
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

# -- disable scp2jet
#
scp2jet=0

# -- dtgs
#
if(dtgopt != None):

    selectNN=1
    if(ls9x or doCARQonly): selectNN=0

    #tcD=TcData(dtgopt=dtgopt,verb=verb,cacheOverride=cacheOverride,keepPrevYears=keepPrevYears)
    tcD=TcData(dtgopt=dtgopt,md2tag=md2tag,doWorkingBT=doWorkingBT,doBdeck2=doBdeck2,verb=verb)
    dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)
    isRT=mf.isRealTime(dtgs,age=18.0)
    
    # -- tcbog by dtg
    #
    if(tcbogPath != None):
        
        for dtg in dtgs:
            tcV=tcD.getTCvDtg(dtg,dobt,dupchk=dupchk,selectNN=selectNN)
            tcbogcards=tcV.makeTCbogCards(tcbogPath=tcbogPath,verb=verb)

    # -- vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv -- tcvitals by dtg
    #
    if(dotcvitals):
        # -- force 9X into tcvitals -- important for non real-time
        #
        selectNN=0
        if(isRT): selectNN=1
        for dtg in dtgs:
            tcV=tcD.getTCvDtg(dtg,dobt,dupchk,selectNN=selectNN)

            if(tcV != None):
                if(verb): tcV.lsStms()
                # -- not putting to a specified path
                if(tcvPath == None):
                    tcvcards=tcV.makeTCvCards(override=override,verb=verb,
                                              writefile=1,scp2jet=scp2jet,scp2theia=scp2jet)
                else:
                    tcvcards=tcV.makeTCvCards(override=override,verb=verb,
                                              writefile=1,tcvPath=tcvPath,scp2jet=scp2jet,scp2theia=scp2jet)

    # -- llllllllllllllllllllllllllllllllllllllllllllllll -- ls TCs by dtg
    #
    tcD.lsDSsDtgs(dtgs,dobt=dobt,dupchk=dupchk,selectNN=selectNN,countsOnly=countsOnly,filtTCs=filtTCs)
    sys.exit()

    


# -- storms
#
if(stmopt != None):

    tcD=TcData(stmopt=stmopt,md2tag=md2tag,doWorkingBT=doWorkingBT,doBdeck2=doBdeck2,verb=verb)

    lstm=len(stmopt.split('.')[0])
    ltt1=len(stmopt.split(','))

    didold=0
    ostmids=[]
    dobtStms=0
    
    # -- detect if 9X stmopt
    #
    if(dobt or doBT and stmopt[0] != '9'): dobtStms=1
 
 
    # -- convert multiyear
 
    if(filtopt != None and mf.find(filtopt,'time2gen')):
        stmids=MakeStmList(stmopt) 
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
    
    #print 'qqqqqqqqqqqq23222222222222222222',stmids,dobt,dobtStms
    #sys.exit()
    
    # -- run track plotter ...
    #
    if(dotrkplot):
        btopt=''
        if(dobt): btopt='-b 1'
        overopt=''
        if(override): overopt='-O'
        drpboxopt=''
        if(w2.onKishou): drpboxopt='-D'
        for stmid in stmids:
            cmd="w2-tc-dss-md2-trkplot.py -S %s %s %s %s -X"%(stmid,drpboxopt,overopt,btopt)
            mf.runcmd(cmd,ropt)
        sys.exit()
        

    if(doanl):

        # -- RI in SCS
        #
        doRISCS=0
        if(doRISCS):
            tt=stmopt.split('.')
            year=tt[1]  
            basin=tt[0] 
            ocards=tcD.anlDSsStmRI(stmids,verb=verb)
            tdir='/w21/prj/tc/20130426_ri_south_china_sea'
            opath="%s/ri.%s.%s.txt"%(tdir,basin,year)
            MF.WriteList2Path(ocards,opath)
            sys.exit()
        
        n9X={}
        nNN={}
        years=[]
        b1ids=[]
        
        stmcards=[]
        
        for stmid in stmids:
            
            rc=getStmParams(stmid)
            b1id=rc[1]
            b1ids.append(b1id)
            year=rc[2]
            years.append(year)
            
            card=tcD.lsDSsStmCards(stmid,sumonly=1)
            
            if(len(card) == 0): continue
            
            print 'cccccccccccccc',stmid,b1id,card
            tt=card['summary'].split()

            if(Is9X(stmid)): 
                try:
                    n9X[year,b1id]=n9X[year,b1id]+1
                except:
                    try:
                        n9X[year,b1id]=1
                    except:
                        n9X[year,b1id]=1
            else:
                try:
                    nNN[year,b1id]=nNN[year,b1id]+1
                except:
                    try:
                        nNN[year,b1id]=1
                    except:
                        nNN[year,b1id]=1
                    
                    
        
        years=mf.uniq(years)
        b1ids=mf.uniq(b1ids)
        
        for year in years:
            for b1id in b1ids:
                try:
                    n9=n9X[year,b1id]
                except:
                    n9=0
                try:
                    nN=nNN[year,b1id]
                except:
                    nN=0
                    
                tcDevRatio=-999.
                if(n9 > 0 and nN > 0):
                    tcDevRatio=(nN*1./n9*1.)*100.0
                    
                print 'SSS b1id: ',b1id,' year: ',year,' 9X: %3d'%(n9),' NN: %3d'%(nN)," TCdevR: %3.0f%%"%(tcDevRatio)
            
            
    #
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
        
        
        tcD.stats=[]
        tcD.anlDSsStmSummary(stmids,dobt=dobt,set9xfirst=dobt,anltype='time2gen')
        tcD.statsGen=tcD.stats
        rc=SimpleListStats(tcD.stats,hasflag=0)

        tcD.stats=[]
        tcD.anlDSsStmSummary(stmids,dobt=dobt,set9xfirst=dobt,anltype='tclife')
        tcD.statsTc=tcD.stats
        rc=SimpleListStats(tcD.stats,hasflag=0)
        #print rc,tcD.stats

        tcD.stats=[]
        tcD.anlDSsStmSummary(stmids,dobt=dobt,set9xfirst=dobt,anltype='stmlife')
        tcD.statsStm=tcD.stats
        rc=SimpleListStats(tcD.stats,hasflag=0)
        print rc,tcD.stats

        #sys.exit()

    else:
        #llllllllllllllllllllllllllllllllllllllllllllllllll -- listing here
        #
        if(filtopt == None):

            writeCard=''
            writeCards=[]
            
            for stmid in stmids:
                
                # -- merge both 9x and real/final bdeck
                #
                set9xfirst=1

                # -- mechanism to output only 9x in TcData.lsDSsStm
                #
                if(ls9x or Is9X(stmid)): dobt=-1
                if(doBT): dobt=2 ; set9xfirst=1   # -- want to show 9X now that we merge WN posits from NN trk into final(default)
                (ocard,ocards)=tcD.lsDSsStm(stmid,dobt=dobt,
                                            set9xfirst=set9xfirst,
                                            convert9x=0,
                                            sumonly=sumonly,printdtgs=printdtgs,
                                            filtTCs=filtTCs,
                                            verb=verb)
                if(ocards == None):
                    writeCard=writeCard+ocard+'\n'
            
            if(oPath != None):
                if(ocards != None):
                    writeCards=[]
                    kk=ocards.keys()
                    kk.sort()
                    for k in kk:
                        writeCards.append(ocards[k])
                    writeCards.append(ocard)
                    MF.WriteList2Path(writeCards,oPath)
                else:
                    MF.WriteString2Path(writeCard,oPath)
                
    if(filtopt == None and doanl == 1):

        print 'ls for doanl = 1'
        
        for stmid in stmids:
            tcD.lsDSsStm(stmid,dobt=dobt,sumonly=sumonly,
                        set9xfirst=dobt,
                        printdtgs=printdtgs)
            
            
        sys.exit()
            
    if(filtopt != None):

        try:
            year=stmopt.split('.')[1]
        except:
            year=CL.curyear
            
        if(mf.find(stmopt.lower(),'l')): basin='LANT'
        if(mf.find(stmopt.lower(),'w')): basin='WPAC'
        if(mf.find(stmopt.lower(),'e')): basin='EPAC'
        if(mf.find(stmopt.lower(),'s')): basin='SHEM'

        (filtBySeason,filtByDev,filtByCC,tlist,donorm,docum,
         ymax,yint,xmax,xmin,xint,binint,ptitle2)=setFilter(filtopt,stmopt)

        pngpath="/ptmp/%s.%s.png"%(filtopt,stmopt)
        pngpath=pngpath.replace(',','-')
        print 'PPP(pngpath): ',pngpath
        
        if(tlist == 'time2gen'):
            
            (statAll,statIn,statOut)=tcD.filtStmSummaryBySeason(stmids,tlist=tlist,verb=0)

            pltHist(statAll,statIn,statOut,stmopt,basin=basin,year=year,
                    tlist=tlist,
                    ptitle2=None,
                    filttype=None,
                    donorm=donorm,
                    docum=docum,
                    ymax=ymax,yint=yint,
                    binint=binint,
                    dostacked=0,
                    var1='yesCC',
                    var2='nonCC',
                    pngpath=pngpath,
                    doAllOnly=1,
                    xmax=xmax,xmin=xmin,xint=xint,tag=tlist,
                    doshow=doshow)

        if(filtBySeason):
            
            (statAll,statIn,statOut)=tcD.filtStmSummaryBySeason(stmids,tlist=tlist,verb=0)

            pltHist(statAll,statIn,statOut,stmopt,basin=basin,year=year,
                    filttype='season',
                    donorm=donorm,
                    tlist=tlist,
                    ptitle2=ptitle2,
                    docum=docum,
                    ymax=ymax,yint=yint,
                    binint=binint,
                    dostacked=0,
                    var1='InSeason',
                    var2='OffSeason',
                    pngpath=pngpath,
                    xmax=xmax,xmin=xmin,xint=xint,tag=tlist,
                    doshow=doshow)

        elif(filtByDev):

            (statAll,statDev,statNonDev)=tcD.filtStmSummaryByDev(stmids,tlist=tlist,verb=0)
         
            pltHist(statAll,statDev,statNonDev,stmopt,basin=basin,year=year,
                    filttype='dev',
                    tlist=tlist,
                    ptitle2=ptitle2,
                    donorm=donorm,
                    docum=docum,
                    ymax=ymax,yint=yint,
                    binint=binint,
                    dostacked=0,
                    var1='Dev',
                    var2='NonDev',
                    pngpath=pngpath,
                    xmax=xmax,xmin=xmin,xint=xint,tag=tlist,doshow=doshow)

        elif(filtByCC != 0):

            if(filtByCC == 1): cctest='all'
            if(filtByCC == 2): cctest='bt'
            if(filtByCC == 3): cctest='9x'
            
            (statAll,statDev,statNonDev)=tcD.filtStmSummaryByCC(stmids,tlist=tlist,
                                                               cctest=cctest,
                                                               verb=0)

            pltHist(statAll,statDev,statNonDev,stmopt,basin=basin,year=year,
                    tlist=tlist,
                    ptitle2=ptitle2,
                    filttype='dev',
                    donorm=donorm,
                    docum=docum,
                    ymax=ymax,yint=yint,
                    binint=binint,
                    dostacked=0,
                    var1='yesCC',
                    var2='nonCC',
                    pngpath=pngpath,
                    xmax=xmax,xmin=xmin,xint=xint,tag=tlist,
                    doshow=doshow)
            

        sys.exit()
        
    if(doanl):
        
        print tcD.statsGen
        rc=SimpleListStats(tcD.statsGen,hasflag=0)
        (mean,amean,sigma,max,min,n)=rc[0:6]
        print 'meanGen: ',mean

        print tcD.statsTc
        rc=SimpleListStats(tcD.statsTc,hasflag=0)
        (mean,amean,sigma,max,min,n)=rc[0:6]
        print 'meanTc: ',mean

        year=stmids[0].split('.')[1]
        
        if(mf.find(stmopt,'l')): basin='LANT'
        if(mf.find(stmopt,'w')): basin='WPAC'
        
        rc=pltHist(tcD.stats,stmopt,basin,year)

        print 'rrrrrrrrrrrrrrrrrrrrrrrr',rc
        sys.exit()

    if(verb): MF.dTimer('all')
    sys.exit()


if(verb): MF.dTimer('all')
sys.exit()

# -- 9x count
#
if(ls9x):

    tcD=TcData(stmopt=stmopt,doBdeck2=doBdeck2,verb=verb)
    tcD.ls()
    sumonly=1
    dobt=0
    
    tcD.lsDSsStm(stmid,dobt=dobt,
                 set9xfirst=set9xfirst,
                 convert9x=0,
                 sumonly=sumonly,printdtgs=printdtgs,
                 filtTCs=filtTCs,
                 verb=verb)
    
    sys.exit()

    tag=' NN  9X  formrate[%]'
    print 'LANT',tag
    for year in years:
        print year,tcD.lsStmids(year,'al')
    sys.exit()

    print
    print 'WPAC',tag
    for year in years:
        print year,tcD.lsStmids(year,'wp')

    print
    print 'EPAC',tag
    for year in years:
        print year,tcD.lsStmids(year,'ep')
    sys.exit()



        
