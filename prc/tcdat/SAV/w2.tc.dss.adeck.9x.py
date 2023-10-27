#!/usr/bin/env python

from tcbase import *

from ATCF import AidProp

class Adeck9x(Adeck):

    dynamicalModels=['avno','ecm2','gfs2','javn','ukm2','jukm','ngps','jngp']

    def __init__(self,stmdtgs,
                 stmid=None,stmid9=None,
                 inV=None,
                 override=0,warn=1,verb=0):

        self.initVars()
        self.inputstmdtgs=stmdtgs
        self.mD=None
        self.skipcarq=1
        self.aliases={}
        self.taids=None
        self.undef=-999
        self.stmid=stmid
        self.stmid9=stmid9

        self.override=override
        self.warn=warn
        self.verb=verb
        self.inV=inV
        self.chkModelStats()


    def initAcards(self,acards):
        self.cards=acards
        self.initAdeck()
    

    def chkModelStats(self):

        self.dostats=0
        if(self.inV != None):
            try:
                (percentHit,life,meanlasttau,meannmods)=self.inV[self.stmid]
                print 'PPP--hash percentHit(%s): %3.0f life: %4.1f [d]  meanlasttau: %3.0f meannmods: %3.1f'%(self.stmid,percentHit,life,meanlasttau,meannmods)
            except:
                percentHit=None

        if(self.override or percentHit == None): self.dostats=1


    def getModelStats(self,verb=0):

        if(self.inV != None):
            try:
                (percentHit,life,meanlasttau,meannmods)=self.inV[self.stmid]
                if(verb): print 'PPP--hash percentHit(%s): %3.0f life: %4.1f [d]  meanlasttau: %3.0f meannmods: %3.1f'%(self.stmid,percentHit,life,meanlasttau,meannmods)
            except:
                print 'not there...',self.stmid
                percentHit=None

        if(not(self.override or percentHit == None)): return
        
        life=float(len(stmdtgs))*0.25
        nmodels={}

        if(len(self.stm2ids) == 0):
            print 'WWW no trackers for:  ',self.stmid,stmdtgs
            if(self.inV != None):  self.inV[self.stmid]=(0.0,life,0.0,0.0)
            return
            
        stm2id=self.stm2ids[0]
        for stmdtg in stmdtgs:
            if(self.verb): print 'SSSSSSSSSS stmdtg: ',stmdtg
            for model in self.dynamicalModels:
                try:
                    taus=self.aidtaus[model,stm2id,stmdtg]
                    taus=mf.uniq(taus)
                except:
                    taus=None

                if(taus != None):
                    if(self.verb): print 'MMM taus for model: ',model,' stm2id: ',stm2id,' taus: ',taus
                    MF.appendDictList(nmodels,stmdtg,(model,taus))
                    
            if(self.verb): print

        ntot=0
        meannmods=0

        meanlasttau=0

        for stmdtg in stmdtgs:

            meanltmod=0
            
            try:
                nm=nmodels[stmdtg]
            except:
                nm=[]

            nmods=0
            lasttau=0
            meanltmod=0
            
            if(len(nm) > 0):
                ntot=ntot+1

                for m in nm:
                    nmods=nmods+1
                    lasttau=m[1][-1]
                    meanltmod=meanltmod+float(lasttau)
                    
                # -- mean # of models
                #
                meannmods=meannmods+len(nm)
                meanltmod=meanltmod/len(nm)

                meanlasttau=meanlasttau+meanltmod

                    
                
            #print stmdtg,nm

        if(ntot > 0):
            meanlasttau=meanlasttau/float(ntot)
            meannmods=meannmods/float(ntot)
        percentHit=(float(ntot)/float(len(stmdtgs)))*100.0

        print 'PPP percentHit(%s): %3.0f life: %4.1f [d]  meanlasttau: %3.0f meannmods: %3.1f'%(self.stmid,percentHit,life,meanlasttau,meannmods)
        
        if(self.inV != None):  self.inV[self.stmid]=(percentHit,life,meanlasttau,meannmods)


def getModelStats(inV,stmid):

    if(inV != None):
        try:
            (percentHit,life,meanlasttau,meannmods)=inV[stmid]
            print 'PPP--hash percentHit(%s): %3.0f life: %4.1f [d]  meanlasttau: %3.0f meannmods: %3.1f'%(stmid,percentHit,life,meanlasttau,meannmods)
        except:
            percentHit=life=meanlasttau=meannmods=None

    return(percentHit,life,meanlasttau,meannmods)



        
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
            var1='var1',
            var2='var2',
            pngpath=None,
            tag=''):

    import matplotlib.pyplot as plt
    from numpy import array,arange

    xa=array(lista)
    xi=array(listi)
    xo=array(listo)

    ymaxi=xi.max()
    ymaxo=xo.max()

    rca=SimpleListStats(lista,hasflag=0)
    rci=SimpleListStats(listi,hasflag=0)
    rco=SimpleListStats(listo,hasflag=0)
    
    meana=rca[0]
    sigmaa=rca[2]

    meani=rci[0]
    sigmai=rci[2]

    meano=rco[0]
    sigmao=rco[2]

    if(donorm):
        ymax=0.75
        yint=0.25
        ymax=0.25
        yint=0.05

    if(docum):
        ymax=1.0
        yint=0.25


    if(xmax == None): xmax=15
    if(xmin == None): xmin=0
    if(xint == None): xint=1

    print 'xxxxxxxxxxxxx ',xint

    if(binint == None):
        nbins=(xmax/xint)
        nbins=nbins*5
    else:
        nbins=(xmax-xmin)/binint

    xa=lista

    hrange=[xmin,xmax]
    print'hhhhhhhhh',hrange,nbins

    fc1='green'
    fc2='red'
    ptype='bar'
    ec1='black'
    ec2='black'


    if(donorm or docum):
        ylab='prob [%]'
    else:
        ylab='N'

    if(dostacked):

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
        
        ## (n2, bins, patches) = plt.hist(xo,nbins,histtype='bar',range=hrange,\
        ##                                normed=donorm,cumulative=docum,
        ##                                facecolor=fc2,edgecolor=ec2,
        ##                                alpha=1.0,rwidth=0.50)
        ## print '22222222222222 ',n2,bins


    #ymax2=n2.max()

    ymax2=1e20
    ymax1=n1.max()
    if(ymax1 > ymax2):
        maxy=ymax1
    else:
        maxy=ymax2

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

    plt.xlabel(xlab)
    plt.ylabel(ylab)

    if(ptitle2 == None):
        ptitle2="Stmopt: %s"%(stmopt)

    if(mf.find(filttype,'dev')):

        ni=len(listi)
        no=len(listo)
        devratio=(float(ni)/float(ni+no))*100.0
        ptitle="%s(G) N %d Mn %3.1f $\sigma$: %3.1f %s(R) N %d Mn: %3.1f $\sigma$: %3.1f %%: %3.0f\n%s"%(
            var1,ni,meani,sigmai,
            var2,no,meano,sigmao,
            devratio,
            ptitle2)

    if(mf.find(filttype,'seas')):

        ptitle="%s(G)  N: %d Mn: %3.1f $\sigma$: %3.1f %s(R)  N: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(
            var1,len(listi),meani,sigmai,
            var2,len(listo),meano,sigmao,
            stmopt)

        
    #ptitle="$\sigma=$"
    plt.title(r"%s"%(ptitle),fontsize=12)
    

   
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
        pngpath="/tmp/9x.%s.%s.png"%(basin,year)

    print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)

    plt.show()


def pltScatHist(x=None,y=None,basin='wpac',
                year=2010,
                pngpath=None):
    
    import numpy as np
    from pylab import xlabel,ylabel
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter

    # the random data
    if(x == None):
        x = np.random.randn(1000)
        y = np.random.randn(1000)
    else:
        x=np.array(x)
        y=np.array(y)


    nullfmt   = NullFormatter()         # no labels
    font = "sans-serif"

    xlim0=0.0
    xlim1=100.0
    xbinwidth=5.0
    
    ylim0=0.0
    ylim1=10.0
    ybinwidth=0.5

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left+width+0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(1, figsize=(8,8))

    ylab='lifetime [d]'
    xlab='Percent of lifetime with model tracker [%]'

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    #axHistx.xaxis.set_major_formatter(nullfmt)
    #axHisty.yaxis.set_major_formatter(nullfmt)

    hxlab="Histogram of %s"%(xlab)
    hylab="Histogram of %s"%(ylab)
    axHistx.text(50,20, hxlab, ha="center",
                 family=font, size=12)

    axHisty.text(15,6, hylab, ha="center", rotation='vertical',
                 family=font, size=12)


    # the scatter plot:
    axScatter.scatter(x, y,label=ylab)

    axScatter.text(50,-0.75, xlab, ha="center",
                   family=font, size=14)
    
    axScatter.text(-5,6, ylab, ha="center",rotation='vertical',
                   family=font, size=14)

    slab="%s %s"%(basin.upper(),str(year))
    axScatter.text(50,9, slab, ha="center",
                   family=font, size=16)

    #plt.xlabel(xlab)
    #plt.ylabel(ylab)

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
    lim = ( int(xymax/binwidth) + 1) * binwidth

    #axScatter.set_xlim( (-lim, lim) )
    #axScatter.set_ylim( (-lim, lim) )

    
    axScatter.set_xlim( (xlim0,xlim1) )
    axScatter.set_ylim( (ylim0,ylim1) )

    xbins = np.arange(xlim0, xlim1 + xbinwidth, xbinwidth)
    ybins = np.arange(ylim0, ylim1 + ybinwidth, ybinwidth)
    axHistx.hist(x, bins=xbins)
    axHisty.hist(y, bins=ybins, orientation='horizontal')

    axHistx.set_xlim( axScatter.get_xlim() )
    axHisty.set_ylim( axScatter.get_ylim() )

    if(pngpath == None):
        pngpath="/tmp/9x.%s.%s.png"%(basin,year)

    print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)


    plt.show()    

def filterAcardsByDtgs(acards,dtgs,verb=0):

    oacards=[]

    for acard in acards:
        tt=acard.split(',')
        try:
            adtg=tt[2].strip()
        except:
            adtg=None

        if(adtg != None and adtg in dtgs):
            if(verb): print 'filterAcardsByDtgs adtg: ',adtg,acard
            oacards.append(acard)

    return(oacards)


def getLocalAdecks(stmdtgs,stmid=None,verb=0):

    sdir="%s"%(w2.TcDatDirTMtrkN)
    tstmid=None
    if(stmid != None): tstmid=stmid.split('.')[0].lower()

    adecks=[]
    acards=[]
    for stmdtg in stmdtgs:
        mask="%s/%s/????/tctrk.atcf.%s.????.txt"%(sdir,stmdtg,stmdtg)
        if(verb): print 'MMM localadecks(mask): ',mask
        if(tstmid != None):
            mask="%s/%s/????/tctrk.atcf.%s.????.%s.txt"%(sdir,stmdtg,stmdtg,tstmid)
        adecks=adecks+glob.glob(mask)
        for adeck in adecks:
            acards=acards+open(adeck).readlines()

    if(verb):
        print adecks
        for acard in acards:
            print acard[0:-1]

    return(acards)

                               

def getLocalAdecksEsrl(stmdtgs,stmid=None,verb=0):

    sdir="%s"%(w2.TcAdecksEsrlDir)
    tstmid=None
    if(stmid != None):
        tstmid=stmid.split('.')[0].lower()
        t2basin=Basin1toBasin2[tstmid[2].upper()]


    adecks=[]
    acards=[]
    oacards=[]
    
    for stmdtg in stmdtgs:
        mask="%s/%s/w2flds/tctrk.atcf.%s.????.txt"%(sdir,stmdtg[0:4],stmdtg)
        if(verb): print 'MMM localadecksEsrl(mask): ',mask
        adecks=adecks+glob.glob(mask)
        for adeck in adecks:
            acards=acards+open(adeck).readlines()

    for acard in acards:
        tt=acard.split(',')
        astmid=tt[1].strip()
        a2basin=tt[0].strip()
        if(stmid != None and astmid == stmid[0:2] and a2basin == t2basin):
            oacards.append(acard)
        
            

    if(verb):
        print adecks
        for acard in oacards:
            print acard[0:-1]

    return(oacards)

                               

    


    
        

        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class AdeckCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            'dorsync2kaze':0,
            }

        self.options={
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'doplot':         ['P',0,1,'do histogram plot'],
            }

        self.purpose='''
parse and create adeck card data shelves
sources: %s'''%(self.sourcesAll)
        self.examples='''
%s -u -y cur'''

    def ChkSource(self,year=None):

        if(year != None):
            self.getSourcesbyYear(year)
            
        iok=0
        for s in self.sources:
            if(self.source == s): iok=1 ; break

        return(iok)

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' in: ',CL.pyfile
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

CL=AdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)

MF.sTimer('all')

sources=source.split(',')
if(stmopt == None): errAD('tstmids')

MF.sTimer('tcD')
tcD=TcData(stmopt=stmopt,verb=verb)
MF.dTimer('tcD')

tstmids=tcD.makeStmListMdeck(stmopt)
if(len(tstmids) == 0):
    fstmids=[]
    tstmids=MakeStmList(stmopt)
    for tstmid in tstmids:
        fstmids=fstmids+tcD.makeStmListMdeck(tstmid)
    tstmids=fstmids

if(len(tstmids) == 0): errAD('tstmids')

years=getYearsFromStmids(tstmids)
year=years[0]

if(mf.find(source,'jtwc')): source='jtwc9x'
if(mf.find(source,'nhc')):  source='nhc9x'

dsbdir="%s/DSs"%(TcDataBdir)
dbtype='adeck'
dbname="%s_%s_%s"%(dbtype,source,year)
dbfile="%s.pypdb"%(dbname)
backup=0
chkifopen=0
doclean=0
DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,backup=backup,unlink=doclean,chkifopen=chkifopen)

# -- inventory
#
tbdir=w2.TcDatDirDSs
dbname='inv_9x'
iV=InvHash(dbname,tbdir=tbdir,diag=1,verb=1)
inV=iV.hash

if(doplot):

    listi=[]
    listo=[]
    lista=[]
    for tstmid in tstmids:
        (percentHit,life,meanlasttau,meannmods)=getModelStats(inV,tstmid)
        if(percentHit != None):
            listi.append(percentHit)
            listo.append(life)

    print listi
    print listo

    basin='wpac'
    year=tstmid.split('.')[1]
    pltScatHist(listi,listo,'wpac',year)
    sys.exit()

    binint=xint=5

    docum=1
    donorm=1
    
    xmin=0
    xmax=100
    xint=20
    ymax=50
    ymin=0
    yint=5
    binint=xint=5

    if(docum or donorm):
        #donorm=0
        ymax=None
        ymin=None
        yint=None

    pltHist(listi,listi,listo,stmopt,basin='wpac',year=2010,
            filttype='season',
            donorm=donorm,
            ptitle2='ptitle2',
            docum=docum,
            ymax=ymax,yint=yint,
            binint=binint,
            dostacked=0,
            var1='InSeason',
            var2='OffSeason',
            pngpath='./test.png',
            xmax=xmax,xmin=xmin,xint=xint,tag='test')

    sys.exit()


    


for tstmid in tstmids:

    MF.sTimer('gettaus: %s'%(tstmid))
    # -- first get full mdeck2 object for tstmid
    #
    dds=tcD.getDSsFullStm(tstmid,dobt=0)
    stmdtgs=dds.dtgs

    # -- locate the appropriate adeck in the uniq.zip archive
    #
    
    zstmid=tstmid
    if(zstmid[0].isalpha()): zstmid="9%s"%(tstmid[1:])

    # -- make the 9X adeck
    #
    aD=Adeck9x(stmdtgs,stmid=tstmid,stmid9=zstmid,inV=inV,
               override=override,
               warn=0,verb=verb)

    if(not(aD.dostats or override)): continue

    stm2id=stm1idTostm2id(zstmid)
    b2id=stm2id[0:2]
    snum=stm2id[2:4]
    byear=stm2id.split('.')[1]

    if(IsJtwcBasin(b2id)):
        abdir=TcAdecksJtwcDir
        bbdir=TcBdecksJtwcDir

    # -- set nhc if cross basin
    #
    if(IsNhcBasin(b2id)):
        abdir=TcAdecksNhcDir
        bbdir=TcBdecksNhcDir

    adeckfile='a%s%s%s.dat'%(b2id,snum,byear)
    adsdir="%s/%s"%(abdir,byear)
    adarchdir="%s/archive"%(adsdir)
    adarchzippath="%s/%s.zip"%(adarchdir,adeckfile)
    aduniqzippath="%s/%s.uniq.zip"%(adarchdir,adeckfile)

    acards=[]
    AZ=zipfile.ZipFile(aduniqzippath)
    afiles=AZ.namelist()
    for afile in afiles:
        cards=AZ.read(afile)
        acards=acards+cards.split('\n')

    # -- pull cards in the stmdtgs
    #
    acards=filterAcardsByDtgs(acards,stmdtgs,verb=verb)

    # -- get local adecks
    #

    year=int(tstmid.split('.')[1])
    
    if(year == 2012):
        acards=acards+getLocalAdecks(stmdtgs,zstmid,verb=verb)
    elif(year == 2010):
        acards=acards+getLocalAdecksEsrl(stmdtgs,zstmid,verb=verb)
    else:
        acards=acards+getLocalAdecksEsrl(stmdtgs,zstmid,verb=verb)
    
    #aD.ls('aid')

    aD.initAcards(acards)
    aD.getModelStats()
    MF.dTimer('gettaus: %s'%(tstmid))

    #abcards=get9xABuniq(aduniqzippath,bduniqzippath)
    #print abcards
    #dds.ls()
    
MF.dTimer('all')
iV.put()



sys.exit()
        


