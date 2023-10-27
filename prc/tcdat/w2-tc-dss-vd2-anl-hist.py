#!/usr/bin/env pythonw

diag=0
from tcbase import * # imports tcVM tcCL adVM adCL
from vdVM import *  
from vdCL import *   # imports vdVM
from ATCF import aidDescTechList
#from w2methods import SimpleListStats

def pltScatter(list0,
               list1,
               stmopt,
               listc=None,
               xmin=None,
               xmax=None,
               ymin=None,
               ymax=None,
               xlab=None,
               ylab=None,
               toptitle=None,
               pngpath=None):

    import matplotlib.pyplot as plt

    plt.scatter(list0, list1, s=listc, c=listc, marker=None, cmap=None, norm=None, 
               vmin=None, vmax=None, alpha=0.5, 
               linewidths=None, verts=None, edgecolors=None, 
               hold=None, data=None)
    
    if(xmin != None and xmax != None):
        plt.xlim(xmin,xmax)   
        
    if(ymin != None and ymax != None):
        plt.ylim(ymin,ymax)   

    if(pngpath == None):
        pngpath="/ptmp/scat.%s.png"%(stmopt)

    if(xlab != None): plt.xlabel(xlab)
    if(ylab != None): plt.ylabel(ylab)

    if(toptitle != None): plt.title(r"%s"%(toptitle),fontsize=12)

    print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)

    plt.show()
    return







def pltHist(lista,
            stmopt,
            listb=None,
            listc=None,
            tlist=None,
            ptitle2=None,
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


    rca=SimpleListStats(lista,hasflag=0)
    
    meana=rca[0]
    sigmaa=rca[2]
    xmaxa=rca[3]
    xmina=rca[4]
    mediana=rca[-2]
    
    print 'ssss AAAA',meana,sigmaa,xmaxa,xmina,mediana
    
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
        
    if(donorm):
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
                                       alpha=1.0,rwidth=0.65)
        
    if(listc != None):
        xa=listc
        
        (n1, bins, patches) = plt.hist(xa,nbins,histtype='bar',range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       facecolor=fc3,edgecolor=ec3,
                                       alpha=1.0,rwidth=0.35)
        


    ymax1=n1.max()

    maxy=ymax1

    print 'yyyyyyyymmmmmmm',ymax
    
    if(ymin == None):
        ymin=0.
        
    if(ymax == None and yint != None):
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

    
    ptitle=" tau   0  N: %3d Mn: %4.1f Md: %4.1f $\sigma$: %4.1f"%(
        len(lista),meana,mediana,sigmaa)
    
    if(listb != None):
        ptitle="%s\ntau  72  N: %3d Mn: %4.1f Md: %4.1f $\sigma$: %4.1f"%(
            ptitle,len(listb),meanb,medianb,sigmab)

    if(listc != None):
        ptitle="%s  tau 120  N: %3d Mn: %4.1f Md: %4.1f $\sigma$: %4.1f"%(
            ptitle,len(listc),meanc,medianc,sigmac)

    ptitle=ptitle+"\n%s"%(ptitle2)

    plt.title(r"%s"%(ptitle),fontsize=9)
    
    plt.xlim(xmin,xmax)
    xaxis=arange(xmin,xmax+1,xint)
    plt.xticks(xaxis)

    ymax=None
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



def plotVD2Hist(ovars,taids,lstau):

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

    rc=pltHist(lista,
               stmopt,
               listb,
               #xlab='Intensity error [kt]',
               xlab='PE [nm]',
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


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup in vdCL.py

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

MF.sTimer('all')
CL=VD2AnlCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verbopt != -999): verb=verbopt
if(verb): print CL.estr

dobt=1
if(not(do9xNOT)): dobt=0

if(filterOpts != None):  
    filterOpts=filterOpts.split(',')
else:
    filterOpts=[]

taus=getAllTaus(tauopt)

# -- if doing metric, always override unless -O
#
if(doMetric): 
    tcunits='metric'
    if(override): override=0
    else:         override=1

if(verirule != 'std' and verirule != 'td'):
    print 'VVVEEERRRIII rule invalid: ',verirule,"""must be either 'std' or 'td' -- sayounara"""
    sys.exit()

MF.sTimer('getDSs ---- ')

# -- setup the dsbdir and dsbdirVD2
#
if(dssDir != None):
    dsbdir=dssDir
    dsbdirVD2=dssDir
else:
    dsbdir="%s/DSs"%(TcDataBdir)
    dsbdirVD2="%s/DSs-VD2"%(TcDataBdir)

    # -- local for DSs or DSs-local in .
    #
    dsbdir="%s/DSs"%(TcDataBdir)
    localDSs=os.path.abspath('./DSs')
    localDSsLocal=os.path.abspath('./DSs-local')

    if(os.path.exists(localDSs)):
        dsbdir=localDSs
        dsbdirVD2=dsbdir

    elif(os.path.exists(localDSsLocal)):
        dsbdir=localDSsLocal
        dsbdirVD2=dsbdir

# -- stmopt/dtg processing
#
if(stmopt != None and ( mf.find(stmopt,'all') or mf.find(stmopt,'nh') or mf.find(stmopt,'sh') ) ):
    stmopt=getAllStmopt(stmopt)

if(stmopt != None): 
    tD=TcData(stmopt=stmopt)
    getstms=tD.makeStmListMdeck(stmopt,dobt=dobt,cnvSubbasin=1,verb=verb)

dtgs=None
if(dtgopt != None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    tD=TcData(dtgopt=dtgopt)
    getstms=tD.getStmidDtgs(dtgs,dobt=dobt)

if(dtgopt == None and stmopt == None and not(lsVD2cache)):
    print 'EEE vd2a -- must set -S stmopt OR -d dtgopt '; sys.exit()

# -- aidopt
#
if(aidopt != None): getaids=aidopt.split(',')
else: getaids=None

# -- set the filterdtgopt to dtgopt, unless overriden
#
if(dtgopt != None and filterdtgopt == None): filterdtgopt=dtgopt

# -- lllllllllllllllllllllllllllllllll -- list the cache
#
if(lsVD2cache): rc=lsVD2_Cache(dsbdirVD2)

# -- set up AD2 and BD2s for use in make VD2
#
A2DSs={}
B2DSs={}

years=getYearsFromStmids(getstms)

tstmids=getstms
taids=getaids

basins=getBasinsFromStmids(tstmids)

# -- loop by years, get A2 and B2 DSss hash
#
for year in years:
    for basin in basins:
        dbtype=AD2dbname
        if(not(do9xNOT)): dbtype="%s-9X"%(dbtype)
        dbname="%s-%s-%s"%(dbtype,basin,year)
        dbfile="%s.pypdb"%(dbname)
        A2DSs[basin,year]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)

# -- get bdeck2
#
dbtype=BD2dbname
for year in years:
    dbfile="%s-%s.pypdb"%(dbtype,year)
    B2DS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)
    B2DSs[year]=B2DS

MF.dTimer('getDSs ---- ')


if(len(taids) > maxTaids):
    print 'EEE too many aids to vda; N: ',len(taids)
    sys.exit()

print 'IIIIII--- working tstmids: %s'%(str(tstmids))[0:140],'...'
print 'IIIIII--- working   taids: ',taids


# -- setup pyp cache file for big stat calcs
#
pyppath='/tmp/vd2.pyp'
if(pypFile != ''): pyppath='/tmp/vd2-%s.pyp'%(pypFile)

if(reloadFromPyp):

    MF.sTimer('LOAD vars from pyp')
    PS=open(pyppath)
    pyp=pickle.load(PS)

    (ss,verivars,ostats,ostatsB,allstats,allstatsB,cases,casedtgs,
     filtStorms,filtCases,filtDtgs,filtTauErrs)=pyp

    for n in range(0,len(verivars)):
        verikey=verivars[n][2]
        allstats['curkey']=verikey

        for tau in taus:        
            for taid in taids:  
                printOstat(allstats, taid, tau, verikey)

        rc=printStats(taids,taus,allstats,ptype,
                      w2=w2,
                      doplotBE=doplotBE,
                      override=override)
    MF.dTimer('LOAD vars from pyp')

else:

    # -- MMMMMMMMMMMMMMMMMMMMMMMMMMM -- main processing loop
    #
    PS=open(pyppath,'w')

    if(dtgs != None): MF.sTimer('getvds dtgs ---- ')
    else:             MF.sTimer('getvds ALL ---- ')

    # -- get/make VD2s
    #
    (vds,vtaids,tstmids)=makeVdsFromAB2DSs(A2DSs,B2DSs,years,dsbdirVD2,overrideVD,
                                           taids,tstmids,
                                           tcunits=tcunits,
                                           verirule=verirule,
                                           override=override,
                                           verb=verb)

    if(dtgs != None): MF.dTimer('getvds dtgs ---- ')
    else:             MF.dTimer('getvds ALL ---- ')

    # -- get final taids list
    #
    taids=getFinalTaidsVD2(getaids,vtaids,verb=verb)

    # -- LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLlll 00000 listing -- still in dev mode
    #
    if(lsopt == 0):
        print 'DDDD #DSss: ',len(DSss)
        for k in vds.keys():
            vDS=DSss[k]
            print 'DDDDDDDDD ',k
            if(vDS != None):
                LsAidsStormsDss(vDS,None,None,dofilt9x=do9xNOT)
                sys.exit()


    # -- PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP - POD by analyzing counts
    #
    if(ptype == 'pod' or ptype == 'pof'):
        if(stmidsByDtgsPath != None):
            PS=open(stmidsByDtgsPath)
            stmidsByDtgs=pickle.load(PS)
        else:
            stmidsByDtgs=None

        (filtPof,filt0012,filt0618,filt00,filt12)=getPodFiltOpts(ptype,filterOpts)
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
                            stmidsByDtgs=stmidsByDtgs,
                            )

        ssPOD=PodStats(taids,tstmids,counts,verb=verb)
        verivars=[
            ('pod','mean','pod'),
        ]

        ostats=ssPOD.ostats
        cases={}
        casedtgs={}

        ss=SumStats(taids,tstmids,
                    verivars,ostats,
                    cases,casedtgs)

        MF.dTimer('PodStats    ---- ')

    # -- SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS - statistical analysis and storm 'ls'
    #
    if(not(ptype == 'pod' or ptype == 'pof')):

        MF.sTimer('getStats')

        rc=getStats(ptype,taus,taids,tstmids,vds,filterdtgopt=filterdtgopt,
                    doland=doland,
                    tableReverse=tableReverse,
                    filterOpts=filterOpts,
                    lsopt=lsopt,
                    doBystorm=doBystorm,
                    dohomo=dohomo,
                    forcehomo=forcehomo,
                    printRunOnly=printRunOnly,
                    veriwarn=veriwarn,
                    w2=w2,
                    diag=diag,
                    verb=verb)

        (ss,verivars,ostats,ostatsB,allstats,allstatsB,cases,casedtgs,
         filtStorms,filtCases,filtDtgs,filtTauErrs)=rc

        MF.dTimer('getStats')

        MF.sTimer('DUMP vars TO pyp')
        pyp=(ss,verivars,ostats,ostatsB,allstats,allstatsB,cases,casedtgs,
             filtStorms,filtCases,filtDtgs,filtTauErrs) 
        pickle.dump(pyp,PS)
        PS.close()
        MF.dTimer('DUMP vars TO pyp')

# -- ls by tau
#
if(lsttau >= 0):
    (ovars,ovars2)=lsCases(taids,cases,casedtgs,verivars,ttau=lsttau,dobigbias=dobigbias,filterOpts=filterOpts,veriwarn=veriwarn,doplot=doplot)
    if(len(ovars) > 0 and verb): print 'ooooooooooooooo -- ovars ',ovars.keys()

# -- hhhhhhh histograms
#
if(doHistplot != -999):
    
    print 'vvvvvv',verivarss
    ovars2=getOvars4Cases(taids,cases,casedtgs,verivars,ttau=doHistplot,dobigbias=dobigbias,filterOpts=filterOpts,veriwarn=veriwarn,doplot=doplot)
    
    print ovars2
    
    taid=ovars2.keys()[0]
    lista=ovars2[taid]['pe']
    listb=ovars2[taid]['fe']
    
    if(taid == 'avno'): model='GFS'
    if(taid == 'tecm4'): model='ECMWF'
    
    list0=[]
    list1=[]
    vmax0=[]
    for ll in lista:
        list0.append(ll[0])
        vmax0.append(ll[1])
    
    for ll in listb:
        list1.append(ll[0])
        
    ptype='pe-vmax0'
    ptype='fe-vmax0'
    ptype='fe-pe'
    
    if(ptype == 'pe-vmax0'):
        
        xmin=-10    
        xmax=600
        ymin=-10
        ymax=200
        
        lista=list0
        listb=vmax0
        listc=vmax0
        xlab='PE [nm]'
        ylab='Vmax [kts]'
        toptitle='%s 72-h PE v Vmax\nLANT 2017'%(model)
        
    elif(ptype == 'fe-vmax0'):
        
        xmin=-10    
        xmax=600
        ymin=-10
        ymax=200
        
        lista=list0
        listb=list1
        listc=vmax0
        xlab='FE [TJ]'
        ylab='Vmax [kts]'
        toptitle='%s 72-h FE v Vmax\nLANT 2017'%(model)
        
    elif(ptype == 'fe-pe'):
        
        xmin=-10    
        xmax=300
        ymin=-10
        ymax=300
        
        lista=list1
        listb=vmax0
        listc=vmax0
        xlab='PE [nmi]'
        ylab='FE [TJ]'
        toptitle='%s 72-h FE v PE\nLANT 2017'%(model)
        

    ptitle2="scat-fe-%s-%03d-%s-%s"%(taid,doHistplot,stmopt,ptype)
    pngpath="/ptmp/%s.png"%(ptitle2)

    rc=pltScatter(lista,listb,stmopt,listc,
                  xmin,xmax,ymin,ymax,
                  xlab=xlab,
                  ylab=ylab,
                  toptitle=toptitle,
                  pngpath=pngpath)
    
    sys.exit()

    ymax=500
    ymin=0
    yint=50
    ymax=ymin=yint=None

    var='pe-fe'
    ptitle2="%s-%03d-%s"%(var,lsttau,stmopt)
    pngpath="/ptmp/%s.png"%(ptitle2)

    rc=pltHist(lista, stmopt, listb, 
               tlist=None, ptitle2=ptitle2, donorm=0, 
               docum=0, xmax=None, xmin=None, xint=None, 
               ymax=ymax, ymin=ymin, yint=yint, binint=None, 
               dostacked=0, var1='Dev', var2='NonDev', 
               pngpath=pngpath, tag='')
    
    
    
    #rc=plotVD2Hist(ovars,taids,lsttau)
    

# -- PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP x-y plotting
#

if(doplot):

    if(ptype == 'gainxyfe' or ptype == 'pod'): doErrBar=0  # haven't figured out how to do box/whiskers for gainxy plots

    # -- plot controls in vdVM.py
    #
    rc=setVD2PlotVars(ptype,pcase,toptitle1=toptitle1,toptitle2=toptitle2)
    (pverikey,pverikey1,do1stplot,do2ndplot,do2ndval,doErrBar,optitle1,toptitle2)=rc


    # -- set up the dictionaries to pass to plotter sdicts - stats ndicts - counts
    #
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
                    sdict1[stmid]=ostatsB[taid,stmid,fixtau,pverikey1]
                    sdict[stmid]=ostatsB[taid,stmid,fixtau,pverikey]
                    ndict[stmid]=ostatsB[taid,stmid,fixtau,pverikey][1]

        else:

            for tau in taus:
                sdict1[tau]=ostats[taid,tau,pverikey1]
                sdict[tau]=ostats[taid,tau,pverikey]
                ndict[tau]=ostats[taid,tau,pverikey][1]

        if( (pcase == 'ens.eemn' or pcase == 'ens.f8mn') and (n == len(taids)-1) ):
            ss.models=ss.models[0:-1]
            continue

        sdicts.append((sdict1,sdict))
        ndicts.append(ndict)


    # -- put the plot to pdir = /tmp if not me
    #
    if(w2.curuSer != 'fiorino'): pdir='/tmp'
    pss=SumStatsPlot(ss.models,ss.vstmids,pcase,ptype,pdir=pdir,doland=doland)
    if(verb): pss.ls()

    ilstyle=ilwidth=None	
    pss.setPlottitles(toptitle1,toptitle2,taus)
    plotcontrolVar=None

    #plotcontrolVar=([0.0,800.0,100],2)  -- big d+7 errors
    #plotcontrolVar=([0.0,100.0,10],2) -- skill space
    #plotcontrolVar=([-70.0,70.0,10],2) # gainxyfe for hfip
    #plotcontrolVar=([-60.0,50.0,10],2) # gainxyfe for hfip
    #plotcontrolVar=([0.0,600.0,50],2)  #-- big d+7 errors
    #plotcontrolVar=([0.0,200.0,20],2) #-- pod/poo

    if(pltcntvar != None):
        tt=pltcntvar.split(',')
        plotcontrolVar=([float(tt[0]),float(tt[1]),float(tt[2])],2)

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
                   doErrBar=doErrBar,
                   doshow=doshow)


MF.dTimer('all')

sys.exit()