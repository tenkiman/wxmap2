####!/usr/bin/env python

import os,sys,glob
import mf
import AD
import BD
import cPickle as pickle

from types import ListType
from types import DictType


def MakeVds(Adps,Bdps,taids=None,stmopt=None,doadeckonly=0):

    adpaths=Adps.paths
    
    bts={}
    ats={}
    vds={}

    A=AD.Adeck(adpaths)
    #return(bts,ats,vds,A,Adps,Bdps)

    if(Bdps == None):
        stmids=mf.uniq(A.stmids.values())
        Bdps=BD.Bdeck(stmopt=stmids,verb=0)

    if(doadeckonly):
        return(bts,ats,vds,A,Adps,Bdps)

    #
    #  get taids from A
    #
    if(taids == None):
        taids=A.aids

    for taid in taids:

        stm2ids=A.aidstms[taid]
        stm1ids=A.GetAidStmids(taid)

        for stm1id in stm1ids:
            
            # get the best track from the bdeck
            #
            bts[stm1id]=A.GetBestTrk(stm1id)

            # bail if no best track
            if(bts[stm1id] == None): continue

            # get the aid track from the adeck
            #
            ats[taid,stm1id]=A.GetAidTrk(taid,stm1id)

            # make the vdeck
            #
            vd=AD.MakeVdeck(bts[stm1id],ats[taid,stm1id],verb=0)
            
            # decorate vdeck with more adeck properties
            #
            vd.acards=A.GetAidCards(taid,stm1id)
            vd.stm1id=stm1id

            # now paths
            #
            vd.Bdps=Bdps
            vd.Adps=Adps

            # make the key
            #
            vdkey="%s_%s"%(taid,stm1id)
            vds[vdkey]=vd

    return(bts,ats,vds,A,Adps,Bdps)


def PutVds2DataSets(vds,DSs):

    dskeys=vds.keys()

    from M import DataSet
    dsk=DataSet(name='dskeys',dtype='hash')
    dsk.data=dskeys
    
    DSs.putDataSet(dsk,'keys')

    for dskey  in dskeys:
        ds=vds[dskey]
        DSs.putDataSet(ds,dskey)



        
def GetAidsStorms(DSs,tstms=None,taids=None,dofilt9x=0):

    aids=[]
    stms=[]
    dskeys=DSs.db['keys'].getData()
    dskeys.sort()

    for dskey in dskeys:

        aid=dskey.split('_')[0]
        stm=dskey.split('_')[1]

        doaid=1
        dostm=1
        stmnum=int(stm[0:2])
        if(dofilt9x and stmnum >= 90 and stmnum <= 99): dostm=0

        if(tstms != None):
            dostm=0
            if(type(tstms) != ListType): tstms=[tstms]
            for tstm in tstms:
                if(mf.find(stm,tstm.upper())): dostm=1

        if(taids != None):
            doaid=0
            if(type(taids) != ListType): taids=[taids]
            for taid in taids:
                if(mf.find(aid,taid.lower())): doaid=1

        
                


            
        
        if(doaid): aids.append(aid)
        if(dostm): stms.append(stm)
                        
    aids=mf.uniq(aids)
    stms=mf.uniq(stms)

    aids.sort()
    stms.sort()

    return(aids,stms)


def getVdsFromDSs(DSs,taids,tstmids):

    if(type(tstmids) is not(ListType)):
        tstmids=[tstmids]

    if(type(taids) is not(ListType)):
        taids=[taids]

    vds={}
    for taid in taids:
        for tstmid in tstmids:
            print 'getting: ',taid,tstmid
            try:
                vd=DSs.db["%s_%s"%(taid,tstmid)]
            except:
                vd=None

        vds[taid,tstmid]=vd

    return(vds)
    

def getEaidsTrks(vds,eaids,stmid):

    trks={}
    dtgs=[]
    for eaid in eaids:
        trks[eaid]=vds[eaid,stmid].AT.trks
        dtgs=dtgs+trks[eaid].keys()
        
        for dtg in trks[eaid].keys():
            taus=trks[eaid][dtg].keys()

            for tau in taus:
                trks[eaid,dtg,tau]=trks[eaid][dtg][tau]
        


    dtgs=mf.uniq(dtgs)
    return(trks,dtgs)

    

def SetMeanTrk(trks,stmid,dtgs,taus,eaids,omodel=None,percentMin=40.0,verb=1):

    #
    # ensemble mean track + member tracks
    #

    nmembers=len(eaids)
    
    emtrk={}
    acards={}

    for dtg in dtgs:
        
        for tau in taus:
            
            lats=[]
            lons=[]
            pmins=[]
            vmaxs=[]
            iok=0
            
            for eaid in eaids:

                try:
                    (lat,lon,vmax,pmin)=trks[eaid,dtg,tau]
                    lats.append(lat)
                    lons.append(lon)
                    if(vmax <= 0.0):
                        vmax=-999.0
                    if(pmin < 0.0):
                        pmin=-999.0
                    vmaxs.append(vmax)
                    pmins.append(pmin)
                    iok=1
                except:
                    if(verb >= 1): print 'NNNN no tracks for ',eaid,dtg,tau


                if(verb):
                    print 'qqq ',eaid,dtg,tau,lat
                    

            if(iok):
                mlat=0.0
                mlon=0.0
                mpmin=0.0
                mvmax=0.0
                nll=0
                nvm=0
                npm=0

                for n in range(0,len(lats)):
                    mlat=mlat+lats[n]
                    mlon=mlon+lons[n]
                    if(pmins[n] > 0.0):
                        mpmin=mpmin+pmins[n]
                        npm=npm+1
                    if(vmaxs[n] > 0.0):
                        mvmax=mvmax+vmaxs[n]
                        nvm=nvm+1

                    nll=nll+1

                pnll=(float(nll)/float(nmembers))*100.0

                if(nll > 0 and pnll >= percentMin):
                    mlat=mlat/float(nll)
                    mlon=mlon/float(nll)

                    if(nvm > 0):
                        mvmax=mvmax/float(nvm)

                    if(npm > 0):
                        mpmin=mpmin/float(npm)

                    if(verb): print 'nll---- ',"%4.1f"%(pnll),nmembers,nll,tau,mlat,mlon,' nvm ',nvm,mvmax,' npm ',npm,mpmin

                    try:
                        emtrk[dtg][tau]=(mlat,mlon,mvmax,mpmin,None,None,None,pnll)
                    except:
                        emtrk[dtg]={}
                        emtrk[dtg][tau]=(mlat,mlon,mvmax,mpmin,None,None,None,pnll)

        trk=emtrk[dtg]
        acards[dtg]=AD.MakeAdeckCards(omodel,dtg,trk,stmid,verb=verb)

    return(emtrk,acards)

    


    
    



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

year=2009
source='gfsenkf'
sdir="%s/esrl/%s/%s"%(AD.AdeckBaseDir,year,source)

admasks=[
#    "%s/track*20090907*"%(sdir),
    "%s/track*%s*"%(sdir,year),
    ]

dsbdir="%s/DSs"%(AD.TcDataBdir)
dbtype='vdeck'
dbname="%s_%s_%s"%(dbtype,source,year)
dbname=dbtype

# datasets setup
#
dbfile="%s.pypdb"%(dbname)
DSs=AD.DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=1)

dovdecks=0
doputdss=0

if(dovdecks):
    adecks=[]
    for admask in admasks:
        adecks=adecks+glob.glob(admask)

    Adps=AD.AtcfAdeckPaths(adecks=adecks)
    Bdps=None

    (bts,ats,vds,A,Adps,Bdps)=MakeVds(Adps,Bdps)

if(doputdss):
    PutVds2DataSets(vds,DSs)

# get aids and storms from shelve
#

taids=None
tstms='03l'
omodel='gemn'
(eaids,tstmids)=GetAidsStorms(DSs,tstms,taids)
print eaids,tstmids

doemean=0

if(doemean):
    etau=120
    dtau=12

    taus=range(0,etau+1,dtau)

    emtrks={}
    vds=getVdsFromDSs(DSs,eaids,tstmids)


    (etrks,dtgs)=getEaidsTrks(vds,eaids,tstmids[0])
    for tstmid in tstmids:

        (emtrks[tstmid],acards)=SetMeanTrk(etrks,tstmid,dtgs,taus,eaids,omodel,percentMin=40.0,verb=0)
        Am=AD.AdeckAcardsDtgHash(acards)

        bts=Am.GetBestTrk(tstmid)
        if(bts == None): continue

        ats=Am.GetAidTrk(omodel,tstmid)

        vd=AD.MakeVdeck(bts,ats,verb=0)
        vd.acards=Am.GetAidCards(omodel,tstmid)
        vd.stm1id=tstmid

        vdkey="%s_%s"%(omodel,tstmid)
        DSs.putDataSet(vd,vdkey)

    

taus=[0,24,48,72,96,120]
taids=['gemn']
tstmids=['03L.2009']

vds=getVdsFromDSs(DSs,taids,tstmids)

verivar='fe'
lists={}
stats={}

for tau in taus:
    fes={}
    for taid in taids:
        for tstmid in tstmids:
            
            vd=vds[taid,tstmid]
            if(vd == None):
                print 'MMMMMMMMMMMMMMMMMMMM making noload vd for ',taid,tstmid
                bt=bts[tstmid]
                at=A.GetAidTrk(taid,tstmid)
                vd=AD.MakeVdeck(bt,at,verb=0)

            list=vd.GetVDVarlist(verivar,tau)
            vd.addList2DictList(fes,taid,list)

    if(len(taids) > 1 and dohomo):
        fes=vd.HomoVDdics(fes,taids,verb=0)
        
    for taid in taids:
        list=fes[taid]
        (mean,amean,sigma,n)=vd.SimpleListStats(list,verb=0,undef=vd.undef)
        stats[taid,tau]=(mean,amean,sigma,n)
        lists[taid,tau]=list
        print 'SSSSSHHHHH ',taid,tau,n,mean,amean,sigma




ttau=120
for taid in taids:
    
    ll=lists[taid,ttau]
    ll.sort()

    for l in ll:
        if(l[0][0] == 1):
            dtg=l[0][1]
            stmid=l[0][2]
            fe=l[1]
            print taid,dtg,stmid,"%6.1f"%(fe)

        
sys.exit()


cards=[]
card0='taus'
for tau in taus:
    card0="%s, %s"%(card0,tau)

cards.append(card0)

print 'CCC ',card0

for taid in taids:
    card1=taid
    card1a=taid
    card2=taid
    for tau in taus:
        (mean,amean,sigma,n)=stats[taid,tau]
        card1="%s, %8.1f"%(card1,mean)
        card1a="%s, %8.1f"%(card1a,amean)
        card2="%s, %8d"%(card2,n)

    cards.append(card1)
    cards.append(card1a)

cards.append(card2)

cardspath='/ptmp/hfip.stat.txt'
mf.WriteList(cards,cardspath)

        


