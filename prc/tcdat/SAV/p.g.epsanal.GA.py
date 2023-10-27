#!/usr/bin/env python

from tcbase import *
from ATCF import *
from vdVM import *
from ga2 import setGA,GradsEnv

def getTrksFromVds(dtg,taus,bts,ads,aids,stmid,verb=0):

    trks={}
    otrks={}
    if(type(aids) is not(ListType)):
        aids=[aids]


    for aid in aids:
        try:
            trk=ads[aid,stmid].getAidTrk().atrks[dtg]
        except:
            trk=None
            
        trks[aid]=trk

        
    for aid in aids:
        
        trk=trks[aid]
        otrk={}
        
        for tau in taus:
            
            if(trk != None):

                try:
                    lat=trk[tau][0]
                    lon=trk[tau][1]
                    vmax=trk[tau][2]
                    pmin=trk[tau][3]

                except:
                    lat=None
                    lon=None
                    vmax=None
                    pmin=None

            else:
                lat=None
                lon=None
                vmax=None
                pmin=None

            otrk[tau]=(lat,lon,vmax,pmin)

        otrks[aid]=otrk

    return(otrks)





def getEnsPlotTrks(dtg,taus,bts,ads,eaids,stmid,pMin=40.0,verb=0):

    def listbar(list,n):
        sum=0.0
        for l in list:
            sum=sum+l
        return(sum/float(n))
        
    trks={}
    otrks={}
    mvmaxs={}
    mlats={}
    mlons={}
    mpmins={}

    for eaid in eaids:
        try:
            trk=ads[eaid,stmid].getAidTrk().atrks[dtg]
        except:
            trk=None
            
        trks[eaid]=trk

    ntrks=len(eaids)
    
    for tau in taus:
        
        lats=[]
        lons=[]
        vmaxs=[]
        pmins=[]
        
        for eaid in eaids:
            trk=trks[eaid]
            if(trk != None):
                try:
                    lat=trk[tau][0]
                    lon=trk[tau][1]
                    vmax=trk[tau][2]
                    pmin=trk[tau][3]
                except:
                    lat=lon=vmax=pmin=None

                if(lat != None):   lats.append(lat)
                if(lon != None):   lons.append(lon)
                if(vmax != None):  vmaxs.append(vmax)
                if(pmin != None):  pmins.append(pmin)

        n=len(lats)
        pn=(float(n)/float(ntrks))*100.0

        if(pn > pMin):
            mvmax=listbar(vmaxs,n)
            mlat=listbar(lats,n)
            mlon=listbar(lons,n)
            mpmin=listbar(pmins,n)
        else:
            mlat=None
            mlon=None
            mvmax=None
            mpmin=None

        mlats[tau]=mlat
        mlons[tau]=mlon
        mvmaxs[tau]=mvmax
        mpmins[tau]=mpmin


    for eaid in eaids:
        trk=trks[eaid]
        otrk={}
        for tau in taus:

            mvmax=mvmaxs[tau]
            
            if(trk != None):

                try:
                    lat=trk[tau][0]
                    lon=trk[tau][1]
                    vmax=trk[tau][2]
                    pmin=trk[tau][3]
                except:
                    lat=lon=vmax=pmin=dvmax=None
                    
                if(mvmax != None and vmax != None):
                    dvmax=vmax-mvmax
                else:
                    dvmax=None

            else:
                lat=lon=vmax=pmin=dvmax=None

            otrk[tau]=(lat,lon,vmax,pmin,dvmax)

        otrks[eaid]=otrk

    # find spread -- dist from mean -> ensemble member
    #

    mfound={}
    mdists={}
    for tau in taus:
        dists=[]
        mlat=mlats[tau]
        mlon=mlons[tau]
        neaids=0
        for eaid in eaids:
            lat=otrks[eaid][tau][0]
            lon=otrks[eaid][tau][1]
            if(lat > -90.0 and mlat != None):
                dist=gc_dist(lat,lon,mlat,mlon)
                dists.append(dist)
            elif(lat > -90.0):
                neaids=neaids+1
                
        n=len(dists)
        pn=(float(n)/float(ntrks))*100.0

        if(pn > pMin):
            mdist=listbar(dists,n)
        else:
            mdist=None

        mdists[tau]=mdist
        mfound[tau]=(neaids,ntrks)
            

    # find top 25% and bottom 25% of intensity change from mean
    #
    
    ftrks={}
    for tau in taus:
        otrkdvmax={}
        dvmaxs=[]
        for eaid in eaids:
            dvmax=otrks[eaid][tau][4]
            if(dvmax != None):
                dvkey=(eaid,dvmax)
                dvmaxs.append(dvkey)
                otrkdvmax[dvkey]=(tau,otrks[eaid][tau])
            
        import operator
        map(operator.itemgetter(1), dvmaxs)
        dvmaxs=sorted(dvmaxs, key=operator.itemgetter(1))

        top25=0.75*len(dvmaxs)
        bot25=0.25*len(dvmaxs)
        top25=int(top25+0.5)
        bot25=int(bot25)
        for n in range(0,len(dvmaxs)):
            dvmax=dvmaxs[n]
            if(n >= top25): dvflg=1
            if(n > bot25 and n < top25): dvflg=0
            if(n <= bot25): dvflg=-1
            eaid=dvmax[0]
            tau=otrkdvmax[dvmax][0]
            tt=otrkdvmax[dvmax][1]
            i=0
            lat=tt[i] ; i=i+1
            lon=tt[i] ; i=i+1
            vmax=tt[i] ; i=i+1
            pmin=tt[i] ; i=i+1
            dvmax=tt[i] ; i=i+1
            
            ftrks[eaid,tau]=(lat,lon,vmax,pmin,dvmax,dvflg)
            if(verb): print '111 ',eaid,tau,ftrks[eaid,tau],'nnnnnnnnn ',n,top25,bot25

    # reorg for otrks
    #
    for eaid in eaids:
        otrk={}
        for tau in taus:
            try:
                (lat,lon,vmax,pmin,dvmax,dvflg)=ftrks[eaid,tau]
                otrk[tau]=(lat,lon,vmax,pmin,dvmax,dvflg)
            except:
                None
                
        otrks[eaid]=otrk


    mtrk={}
    
    for tau in taus:
        mlat=mlats[tau]
        mlon=mlons[tau]
        mvmax=mvmaxs[tau]
        mpmin=mpmins[tau]
        mdist=mdists[tau]
        vdtg=mf.dtginc(dtg,tau)
        try:
            btlat=bts[vdtg][0]
            btlon=bts[vdtg][1]
            fe=gc_dist(mlat,mlon,btlat,btlon)
        except:
            fe=None
            
        
        # make 5th element None for plotTcFt class to signal
        mtrk[tau]=(mlat,mlon,mvmax,mpmin,None,mdist,fe)
        
            
    return(otrks,mtrk,mfound)
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
from M  import CmdLine
from adCL import AdeckSources

class AdeckCmdLine(CmdLine,AdeckSources):
    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['year',    'no default'],
            2:['source',  'no default'],
            3:['dtg',     'no default'],
            }
            
        self.defaults={
            'doupdate':0,
            }


        self.options={
            'override':  ['O',0,1,'override'],
            'verb':      ['V',0,1,'verb=1 is verbose'],
            'ropt':      ['N','','norun',' norun is norun'],
            'otau':      ['t:','48','a','otau'],
            'stmopt':    ['S:',None,'a','stmopt'],
            'dospread':  ['s',0,1,'dospread'],
            'dofehalo':  ['h',0,1,'dofehalo'],
            'doveribt':  ['v',0,1,'doveribt'],
            'dodaid':    ['d',0,1,'doveribt'],
            'dowindow':  ['W',1,0,'dowindow'],
            'doalltaus': ['A',1,0,'doalltaus=1 (default) -- plot taus 0,etau(=120),12; otherwise 0,otau,12'],
            'zoomfact':  ['Z:',None,'a','zoomfact'],
            'ftlcol':    ['F:','15','a','ftlcol -- colorize ft tracks if == -1'],
            'mftlcol':   ['M:','3','a','ftlcol -- colorize ft tracks if == -1'],
            'doxv':      ['X',0,1,'doxv'],
            'quiet':     ['q',0,1,'quiet=1 in ga.cmd() -- turn off all output from grads'],
            }

        self.purpose='''
purpose -- plot colorized tracks from eps trackers'''
        self.examples='''
%s test
'''


    def ChkSource(self):

        iok=0
        for iss in self.source.split(','):
            for s in self.sources:
                if(iss == s): iok=1 ; break

        return(iok)

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):

    if(option == 'stmopt'):
        print 'EEE must specify a stmopt using -S stmopt... '
    elif(option == 'source'):
        print 'EEE bad source: ',source
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main


argstr="pyfile 2009 gfsenkf 2009090800 -S 07l.9 -V -Z 1.0 "
argstr="pyfile 2009 ncep    2009090800 -S 07l.9 -V -Z 1.0 "
argstr="pyfile 2009 ecmwf   2009090800 -S 07l.9 -V -Z 1.0 "
argv=argstr.split()
argv=sys.argv
CL=AdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)

(btau,etau,dtau)=(0,120,12)
if(not(doalltaus)): etau=int(otau)
taus=range(btau,etau+1,dtau)

MF.sTimer(tag='ALL')

# qc cmd line input
#
if(not(CL.ChkSource())): errAD('source')
if(stmopt == None):      errAD('stmopt')
if(verb): print CL.estr

otau=int(otau)
ftlcol=int(ftlcol)
mftlcol=int(mftlcol)
if(doxv): dowindow=0



#ooooooooooooooooooooooooooooooooo  opaths
#

opaths=['/tmp/ttspread.png',
        '/tmp/ttfe.png',
        '/tmp/tt2.png',
        '/tmp/tt3.png',
        ]

# clear before making plots
#
for opath in opaths:
    try:    os.unlink(opath)
    except: continue
    
opathcirc=opaths[0]
opathfehalo=opaths[1]
opathbase=opaths[2]
opathfinal=opaths[3]

# -- get list of storms
#
tstms=MakeStmList(stmopt,verb=0)
stmid=tstms[0]

# -- ensemble aid properties
#
ep=EaidProperties(source)

# -- init TcData object to get TC stuff...
#
tD=TcData(dtgopt=dtg)
bts=tD.getBtLatLonVmax(stmid)

# -- get adecks with ensemble aids and det aid
#
dbtype='adeck'
dbname="%s_%s_%s"%(dbtype,source,year)
dbfile="%s.pypdb"%(dbname)
dsbdir="%s/DSs"%(TcDataBdir)

aDS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)
(eaids,estmids)=GetAidsStormsFromDss(aDS,taids=None,tstms=stmid)
ads=GetVdsFromDSs(aDS,eaids,estmids,donone=1,verb=verb)
(eaids,daid,dsource)=FilterEaids(eaids,source,year)

if(dodaid):
    if(source != dsource):
        dbname="%s_%s_%s"%(dbtype,dsource,year)
        dbfile="%s.pypdb"%(dbname)
        vDS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)
    
    add={}
    add=GetVdsFromDSs(aDS,daid,estmids,add,donone=1,verb=1)
    dtrks=getTrksFromVds(dtg,taus,bts,add,daid,stmid,verb=0)
    print 'dtrks: ',dtrks

# get tracks and calc mean track and spread and fe
#
(otrks,mtrk,mfound)=getEnsPlotTrks(dtg,taus,bts,ads,eaids,stmid,verb=verb)

# get reftrks and lat/lon bounds
#
(alats,alons,refaid,reftau,reftrk)=GetOpsRefTrk(dtg,stmid,override=0,verb=0)
(lat1,lat2,lon1,lon2)=LatLonOpsPlotBounds(alats,alons,verb=verb)


# zoom in for demo purposes
#
if(zoomfact != None):

    zoom=float(zoomfact)
    
    dlon=30.0/zoom
    dlat=20.0/zoom
    dint=2.5
    
    rlat=mtrk[otau][0]
    rlon=mtrk[otau][1]
    if(rlat == None):
        vdtg=mf.dtginc(dtg,otau)
        bt=bts[vdtg]
        rlat=bt[0]
        rlon=bt[1]

    lat1=rlat-dlat*0.65
    lat1=int(lat1/dint+1)*dint
    lat2=lat1+dlat

    lon1=rlon-dlon*0.35
    lon1=int(lon1/dint+1)*dint
    lon2=lon1+dlon

    
    print 'zzzzzzzzzzzzz ',rlat,rlon
    print 'ddddddddddddd ',lat1,lat2,lon1,lon2

        
#(lat1,lat2,lon1,lon2)=(5,40,280,340)
#(lat1,lat2,lon1,lon2)=(10,35,285,325)
#(lat1,lat2,lon1,lon2)=(10,25,360-40,360-20)


# -- grads obeject
#
ctl='dum.ctl'
gaopt='-g 1024x768'
ga=setGA(Window=dowindow,Opts=gaopt,Quiet=quiet)
ga.fh=ga.open(ctl)

# -- grads env object from ga
#
ge=ga.ge

# -- grads plot obj from ga
#
gp=ga.gp

ge.lat1=lat1
ge.lat2=lat2
ge.lon1=lon1
ge.lon2=lon2

ge.pareaxl=1.15
ge.pareaxr=9.75
ge.pareayb=1.0
ge.pareayt=8.0
#ge.pngmethod='gxyat'


# set up canvas
#
ge.clear()
ge.mapcol=0
ge.setMap()
ge.grid='off'
ge.setGrid()
ge.setLatLon()
ge.setXylint()
ge.setParea()
ge.setPlotScale()


#  -- haloes
#
if(dospread):
    clat=mtrk[otau][0]
    clon=mtrk[otau][1]
    spread=mtrk[otau][5]

    spread0=mtrk[0][5]
    clat0=mtrk[0][0]
    clon0=mtrk[0][1]

    if(clat0 == None or
       (clat0 < lat1 or clat0 > lat2 or clon0 < lon1 or clon0 > lon2)
       ):
        print "WWW can't make tau0 spread circle"
        spread0=-999.
    else:
        pcirc0=gp.polyCircle
        pcirc0.set(clat0,clon0,spread0)
        pcirc0.fill(lcol=7)
        pcirc0.border(lcol=1,lthk=4)
        
        ge.makePng(opathcirc)
        ge.makePngTransparent(opathcirc)

    if(clat == None):
        print "WWW can't make spread circle"
        spread=-999.
    else:
        pcirc=gp.polyCircle
        pcirc.set(clat,clon,spread)
        pcirc.fill(lcol=7)
        pcirc.border(lcol=1,lthk=4)

    if(clat0 != None or clat != None):
        ge.makePng(opathcirc)
        ge.makePngTransparent(opathcirc)

if(dofehalo):
    ge.clear()
    ge.mapcol=0
    ge.grid='off'
    ge.setGrid()
    ge.setXylint()
    ge.setParea()
    ge.setPlotScale()
    
    clat=mtrk[otau][0]
    clon=mtrk[otau][1]
    if(clat == None):
        print "WWW can't make fe halo"
        fe=-999.
    else:
        fe=mtrk[otau][6]
        pcirc=gp.polyCircle
        pcirc.set(clat,clon,fe)
        pcirc.fill(lcol=2)
        pcirc.border(lcol=1,lthk=6)
        ge.makePng(opathfehalo)
        ge.makePngTransparent(opathfehalo)

# -- main plot
#
ge.clear()
ge.mapcol=15
ge.grid='on'
ge.setMap()
ge.setGrid()
ge.setLatLon()
ge.setXylint()
ge.setParea()
ge.setPlotScale()
ge.setColorTable()

# -- best track and mean ensemble plot objects
#
mftlsty=3
if(mftlcol == -1): mftlsty=3

pbt=gp.plotTcBt
pbt.set(bts,dtg,nhbak=72,nhfor=etau)

pftm=gp.plotTcFtVmax
pftm.set(mtrk,lcol=mftlcol,lsty=mftlsty,lthk=15,doland=1)

pfte=gp.plotTcFt
pfte.set(mtrk,lcol=3,lsty=3,lthk=15)

if(dodaid):
    pftd=gp.plotTcFt
    pftd.set(dtrks[daid],lcol=2,lsty=1,lthk=15,doland=1)

bm=gp.basemap2
bm.draw()

ge.setPlotScale()

pbt.dline(times=pbt.otimesbak,lcol=7,lthk=10)
pbt.dwxsym(times=pbt.otimesbak)
pbt.legend(ge,times=pbt.otimesbak)

pfts={}
for eaid in eaids:
    pft=gp.plotTcFt # -- colorize by dVmax
    #pft=gp.plotTcFtVmax # -- colorize by Vmax
    pft.set(otrks[eaid],lcol=ftlcol,doland=1)
    
    if(ftlcol == -2):
        pft.dline(lcol=15)
    else:
        pft.dline()
    pfts[eaid]=pft
    
for eaid in eaids:
    pft=pfts[eaid]
    if(ftlcol == -2):
        try:
            vmcol=pft.lineprop[otau][0]
        except:
            continue

        if(vmcol != 75):
            pft.dmark(times=[otau],mkcol=vmcol,mksiz=0.20)
            pft.dmark(times=[otau],mksiz=0.05)
        else:
            pft.dmark(times=[otau])
    else:
        pft.dmark(times=[otau])
    

        
# plot det aids
#
bott2=None
if(dodaid):
    pftd.dline(lcol=0,lthk=20)
    pftd.dline(lcol=2,lthk=10)
    pftd.dmark(times=[otau],mkcol=2,mksiz=0.15)
    pftd.dmark(times=[otau],mkcol=1,mksiz=0.05)
    bott2='Red: Det Fc Track'


pftm.dline(lcol=0,lsty=1,lthk=15)
pftm.dline()
pftm.dmark(times=[otau],mkcol=3,mksiz=0.15)
pftm.dmark(times=[otau],mkcol=1,mksiz=0.05)

if(mftlcol == -1): 
    pcbarnM=gp.cbarn
    #pcbarnM.draw(vert=1,sf=0.65,side='left')
    

ttl=gp.title
ttl.set(scale=0.85)

vdtg=mf.dtginc(dtg,otau)
nf=mfound[otau][0]
nt=mfound[otau][1]
nm=nt-nf
stmname=GetTCName(stmid)
t1='%s TC: %s[%s] V`bmax`n: %3dkt bdtg: %s at `3t`0= %03d'%(ep.modeltitle,stmid,stmname,int(bts[dtg][2]),dtg,int(otau))
t2='valid dtg: %s  N`bfound`n:%d N`bmissed`n: %d N`bMEMBERS`n: %d'%(vdtg,nf,nm,nt)
if(dospread):
    t2='%s Spread:%4.0f nm  Spread `3t`0=0 %3.0f nm'%(t2,spread,spread0)
if(dofehalo):
    t2='%s FE: %4.0f nm'%(t2,fe)
    
ttl.top(t1,t2)
bott1='Green: Ens Mean track'
ttl.t1col=3
ttl.t2col=2
ttl.scale=1.0
ttl.bottom(bott1,bott2,sopt='left')

if(doveribt):
    pbt.dline(times=pbt.otimesfor,lcol=1)
    pbt.dwxsym(times=pbt.otimesfor,wxcol=1,wxthk=4)
    pbt.legend(ge,times=pbt.otimesfor,btcol=1)

if(ftlcol == -1 or ftlcol == -2):
    pcbarnF=gp.cbarn
    pcbarnF.draw(vert=0,sf=0.65)


dodis=0
ge.makePng(opathbase)
if(dospread):
    ge.makePngDissolve(opathcirc,opathbase,opathfinal,disolvfrc=50)
    dodis=1

if(dofehalo):
    obase=opathfinal
    if(dospread == 0): obase=opathbase
    ge.makePngDissolve(opathfehalo,obase,opathfinal)
    dodis=1

if(dodis == 0): mf.runcmd("mv %s %s"%(opathbase,opathfinal),ropt)

if(doxv):       mf.runcmd("xv %s"%(opathfinal),ropt)

MF.dTimer(tag='ALL')

sys.exit()
