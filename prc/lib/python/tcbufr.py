from tcbase import *
import json

def makeAdeckCard(stmid,aid,dtg,tau,rlat,rlon,pmin,vmax,rmax,radVal,radii):
    
    (snum,b1id,year,b2id,tstm2id,tstm1id)=getStmParams(stmid)
    
    adecknum=98
    adeckname=aid

    (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(rlat,rlon)
    
    ipmin=mf.nint(pmin)
    ivmax=mf.nint(vmax)
    irmax=mf.nint(rmax)
    
    r34ne=r34se=r34sw=r34nw=0
    
    (r34ne,r34se,r34sw,r34nw)=radii
    
    ipoci=0
    iroci=0

    acard1=''
    acard2=''
    acard3=''

    acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(b2id,str(snum),dtg,adecknum,adeckname,tau)

    oextra=" %4d, %4d, %3d"%(ipoci,iroci,irmax)

    # add \n at end of card to be consistent with real adecks
    #
    acard1=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  %2d, NEQ, %4d, %4d, %4d, %4d,%s\n"%\
        (ilat,hemns,ilon,hemew,ivmax,ipmin,radVal,r34ne,r34se,r34sw,r34nw,oextra)
    
    return(acard1)
     

def getBTlatlons(dtg,tD,dupchk=0,selectNN=1):

    btlatlons={}
    (bstmids,btcs)=tD.getStmidBtcsDtg(dtg,dupchk=dupchk,selectNN=selectNN)

    for bstmid in bstmids:
        rc=btcs[bstmid]
        btlatlons[bstmid]=rc[0:2]
        
    return(btlatlons)
     
def comp2BTstmids(rlat,rlon,btlatlons,
                  tolNN,tol9X,
                  aid,
                  verb=0):

    rc=None
    odist=None
    for stmid in btlatlons.keys():
        btlat=btlatlons[stmid][0]
        btlon=btlatlons[stmid][1]
        if(IsNN(stmid)): tol=tolNN
        else:            tol=tol9X
        
        dist=gc_dist(rlat, rlon, btlat, btlon)
        if(verb): print ('CCC-comp2BTstmids: ',stmid,aid,btlat,btlon,'bufr: ',rlat,rlon,' dist: ',dist,' tol: ',tol)
        if(dist < tol): 
            odist=dist
            rc=stmid
            return(rc,odist)
        
    return(rc,odist)


def getAid(nm):
    if(nm == 52):
        aid="emdt"
    elif(nm == 51):
        aid="emcn"
    else:
        aid="em%02d"%(nm)
    aid=aid.upper()
    return(aid)

def getR34(radii,m,vmax,nEns):
    
    if(nEns == 1 or not(type(radii[0]) is ListType)):
        r0=radii[0]
    else:
        r0=radii[0][m]

    if(nEns == 1 or not(type(radii[1]) is ListType)):
        r1=radii[1]
    else:
        r1=radii[1][m]
        
    if(nEns == 1 or not(type(radii[2]) is ListType)):
        r2=radii[2]
    else:
        r2=radii[2][m]
        
    if(nEns == 1 or not(type(radii[3]) is ListType)):
        r3=radii[3]
    else:
        r3=radii[3][m]
    
    rNone=0
    if(r0 == None): r0=0. ; rNone=1
    if(r1 == None): r1=0. ; rNone=1
    if(r2 == None): r2=0. ; rNone=1
    if(r3 == None): r3=0. ; rNone=1

    if(vmax >= 34. and rNone):
        r0=r1=r2=r3=-1.
    
    r0=setR34(r0)
    r1=setR34(r1)
    r2=setR34(r2)
    r3=setR34(r3)

    r34=(r0,r1,r2,r3)
    meanR34=(r0+r1+r2+r3)*0.25

    c34="%3.0f %3.0f %3.0f %3.0f"%(r0,r1,r2,r3)
    
    return(r34,c34,meanR34)
    
def setR34(r0):
    if(r0 > 0.0):
        r0=r0*0.001*km2nm
    else:
        r0=0.0
    return(r0)

def setR50(r0):
    if(r0 > 0.0):
        r0=r0*0.001*km2nm
    else:
        r0=-2.0
    return(r0)
    
def setR64(r0):
    if(r0 > 0.0):
        r0=r0*0.001*km2nm
    else:
        r0=-3.0
    return(r0)
    
def finalRXX(r0,r1,r2,r3):
    
    if(r0 < 0.0): r0=0.0
    if(r1 < 0.0): r1=0.0
    if(r2 < 0.0): r2=0.0
    if(r3 < 0.0): r3=0.0
    
    return(r0,r1,r2,r3)


def getR50(radii,m,vmax,nEns):

    r0=r1=r2=r3=-2.0
    
    if(nEns == 1 or not(type(radii[4]) is ListType)):
        r0=radii[4]
    else:
        r0=radii[4][m]
        
    if(nEns == 1 or not(type(radii[5]) is ListType)):
        r1=radii[5]
    else:
        r1=radii[5][m]
        
    if(nEns == 1 or not(type(radii[6]) is ListType)):
        r2=radii[6]
    else:
        r1=radii[6][m]

    if(nEns == 1 or not(type(radii[7]) is ListType)):
        r3=radii[7]
    else:
        r3=radii[7][m]
    
    rNone=0
    if(r0 == None): r0=-2. ; rNone=1
    if(r1 == None): r1=-2. ; rNone=1
    if(r2 == None): r2=-2. ; rNone=1
    if(r3 == None): r3=-2. ; rNone=1

    # -- set r to -1 if == 0.0 otherwise convert to nmi
    #
    r0=setR50(r0)
    r1=setR50(r1)
    r2=setR50(r2)
    r3=setR50(r3)
    
    if(vmax > 50. and rNone):
        r0=r1=r2=r3=-2.

    meanR50=(r0+r1+r2+r3)*0.25
    (r0,r1,r2,r3)=finalRXX(r0, r1, r2, r3)
    
    r50=(r0,r1,r2,r3)

    c50="%3.0f %3.0f %3.0f %3.0f"%(r0,r1,r2,r3)

    return(r50,c50,meanR50)
    
def getR64(radii,m,vmax,nEns):

    r0=r1=r2=r3=-3.

    if(nEns == 1 or not(type(radii[8]) is ListType)):
        r0=radii[8]
    else:
        r0=radii[8][m]
        
    if(nEns == 1 or not(type(radii[9]) is ListType)):
        r1=radii[9]
    else:
        r1=radii[9][m]
    
    if(nEns == 1 or not(type(radii[10]) is ListType)):
        r2=radii[10]
    else:
        r2=radii[10][m]
        
    if(nEns == 1 or not(type(radii[11]) is ListType)):
        r3=radii[11]
    else:
        r3=radii[11][m]
    
    if(r0 == None): r0=-3.
    if(r1 == None): r1=-3.
    if(r2 == None): r2=-3.
    if(r3 == None): r3=-3.

    # -- set r to -3 if == 0.0 otherwise convert to nmi
    #
    r0=setR64(r0)
    r1=setR64(r1)
    r2=setR64(r2)
    r3=setR64(r3)
    
    if(vmax < 64.):
        r0=r1=r2=r3=-3.
    
    meanR64=(r0+r1+r2+r3)*0.25
    (r0,r1,r2,r3)=finalRXX(r0, r1, r2, r3)
    
    r64=(r0,r1,r2,r3)

    c64="%3.0f %3.0f %3.0f %3.0f"%(r0,r1,r2,r3)

    return(r64,c64,meanR64)

def crackJson(bpath,btlatlons,dtg,acards,tol=180.0,ropt='',verb=0,warn=0):
    
    # -- check if track has 0,6,12 posits and near btlatlons...
    #

    def getrlat(rlats,m):
        
        if(type(rlats) is ListType):
            rlat=rlats[m]
        else:
            rlat=rlats
            
        return(rlat)
        

    def chkTrkTau0(m,posit,btlatlons,verb=0):

        def getRlatlon(tau):

            # -- 20200709 -- checks on rlats/rlons
            rc=-1
            rlat=rlon=None

            ptaus=posit.keys()
            # -- case where the tau is not in the posit taus!  e.g., tau12 when only 0,6 taus
            #
            if(not(tau in ptaus)):
                print 'WWW no tau: ',tau,' in posit taus...press...for: ',bpath,'siz: ',MF.getPathSiz(bpath)
                return(rc)
                
            (rlats,rlons,rlatMs,rlonMs,pmins,vmaxs,radii)=posit[tau]
            
            # -- 20200709 -- checks on rlats/rlons
            rc=-1
            rlat=rlon=None
            
            if(rlats != None): 
                if(type(rlats) is ListType):
                    rlat=rlats[m]
                else:
                    rlat=rlats

            if(rlons != None):
                if(type(rlons) is ListType):
                    rlon=rlons[m]
                else:
                    rlon=rlons

            if(rlat != None):
                btdist=gc_dist(rlat,rlon,btlat,btlon)
                if(btdist <= tol):
                    rc=tau
                else:
                    rc=-2
                        
            return(rc)
            
            
        stmids=btlatlons.keys()
        stmids.sort()
        rc=-1
        for stmid in stmids:
            
            (btlat,btlon)=btlatlons[stmid]

            rc0=getRlatlon(0)
            rc6=getRlatlon(6)
            rc12=getRlatlon(12)
        
            if(rc0 == 0): rc=0
            elif(rc6 == 6 and rc0 != -2): rc=1
            elif(rc12 == 12 and rc6 != -2 and rc0 != -2 ): rc=2

            # -- got a hit
            #
            if(rc >= 0): 
                if(verb): print 'stmid/dtg: %s %s'%(stmid,dtg),'rc:',rc0,rc6,rc12,' final rc: ',rc
                return(rc,stmid)
                
        
        #print 'gggrrr rc0: ',rc0,' rc6: ',rc6,' rc12: ',rc12,' rc: ',rc
        
        return(rc,'99X.9999')
        
    
    # -- convert to json
    #
    tauType=0
    roptB='quiet'
    jpath='/tmp/json.txt'
    cmd='bufr_dump -jf %s > %s'%(bpath,jpath)
    mf.runcmd(cmd,roptB)
    
    x=open(jpath,'r').read().replace('\n','')
    y=json.loads(x)
    
    z=y['messages']
    
    ckeys=['code','key','value']
    
    bCode={}
    bDict={}
    
    for zz in z:
        #print zz
        code=key=val=None
        zkeys=zz.keys()
        #print zz.keys()
    
        if(ckeys[0] in zkeys):
            code=zz[ckeys[0]]
    
        if(ckeys[1] in zkeys):
            key=zz[ckeys[1]]
    
        if(ckeys[2] in zkeys):
            val=zz[ckeys[2]]
            
        lval=0
        if(type(val) is ListType):
            lval=len(val)
    
        #print 'code: ',code,'key: ',key,'val: ',val,'lval: ',lval
        if(code == '004024' and lval != 0): tauType=52
        if(code != None):
            MF.appendDictList(bDict, code, val)
            bCode[code]=key
            
    cc=bDict.keys()
    cc=mf.uniq(cc)
    bKeys=cc
    
    for c in cc:
        dstr=str(bDict[c])
        if(len(dstr) > 180):
            ostr=dstr[0:90]+'...'+dstr[-90:]
        else:
            ostr=dstr
        if(verb): print 'cc: %s %-183s %s'%(c,ostr,bCode[c])
    
    
    (bdir,bfile)=os.path.split(bpath)
    bsiz=MF.GetPathSiz(bpath)
    if(tauType != 0):
        print 'BBB bailing path: ',bfile,' bsiz: ',bsiz
        rc=-1
        return(rc)
        

    tauKey='004024'
    if(not(tauKey in bKeys)):
        print 'WWWW -- no taus...bail'
        rc=-1
        return(rc)

    taus=[0]+bDict['004024']
    
    
    # -- turn ensemble list to single list
    #
    nens=bDict['001091']
    
    try:
        nn=nens[0][0]
        nens=nens[0]
    except:
        None
        
    nens.sort()
    
    nTau=len(taus)
    nEns=len(nens)
        
    posit={}
    
    n=0
    np=0
    nr=0
    dr=9
    dr=12
    n0=1
    
    radCode='019004'
    #print 'TTTTTTTTTTttttt-------------',nens,'ttt',taus
    for tau in taus:
        if(tau == 0):
            rlat=bDict['005002'][n0]
            rlon=bDict['006002'][n0]
            rlatM=bDict['005002'][n0+1]
            rlonM=bDict['006002'][n0+1]
            n=n0+2
        else:
            rlat=bDict['005002'][n]
            rlon=bDict['006002'][n]
            rlatM=bDict['005002'][n+1]
            rlonM=bDict['006002'][n+1]
            n=n+2
    
        pmin=bDict['010051'][np]
        vmax=bDict['011012'][np]

        if(radCode in bKeys):
            radii=bDict['019004'][nr:nr+dr]
        else:
            radii=None
    
        if(nEns == 1):
            rlat=[rlat]
            rlon=[rlon]
            rlatM=[rlatM]
            rlonM=[rlonM]
            pmin=[pmin]
            vmax=[vmax]
            
        nr=nr+dr
            
        np=np+1
    
        #print 'TTT',tau
        #print 'Posit: ',rlat
        #rlon,'Rmax: ',rlatM,rlonM,'pmin: ',pmin,'vmax: ',vmax
        posit[tau]=(rlat,rlon,rlatM,rlonM,pmin,vmax,radii)
            
    
    
    
    mSkip=0
    for m in range(0,nEns):    
        
        aid=getAid(nens[m])
        (rc,stmid)=chkTrkTau0(m,posit,btlatlons)
        if(verb): print 'NNN ensemble: %2d stmid: %s rc: %d'%(nens[m],stmid,rc)
        
        # -- skip tracks that are:
        #
        #    -1 -- taus 0,6,12 are not close to best track initial posit
        #     0 -- tau0 matches
        #     1 -- tau6 matches
        #     2 -- tau12 matches
        
        if(rc == -1):
            
            if(warn):  print 'WWW--skipping m=',m
            mSkip=mSkip+1
            continue
        
        for n in range(0,nTau):
            tau=taus[n]
            (rlats,rlons,rlatMs,rlonMs,pmins,vmaxs,radii)=posit[tau]

            if(rlats == None): 
                if(warn): print 'WWW--crackJson no lats for tau: ',tau,' ensemble: ',m
                continue

            #rlat=rlats[m]
            #rlon=rlons[m]
            
            #rlatM=rlatMs[m]
            #rlonM=rlonMs[m]
            
            rlat=getrlat(rlats,m)
            rlon=getrlat(rlons,m)
            
            rlatM=getrlat(rlatMs,m)
            rlonM=getrlat(rlonMs,m)
            
            if(rlat == None):
                rlat=-999.
            if(rlon == None):
                rlon=-999.
            if(rlatM == None):
                rlatM=-999.
            if(rlonM == None):
                rlonM=-999.
            
            rmax=-999.
            if(rlat != -999. and rlatM != -999.):
                rmax=gc_dist(rlat,rlon,rlatM,rlonM)
                
            try:
                pmin=pmins[m]
            except:
                print 'WWW--crackJson pmin failed...set to None'
                pmin=None
                
            if(pmin == None):
                pmin=-999.
            else:
                pmin=pmins[m]*0.01
            try:
                vmax=vmaxs[m]
            except:
                vmax=-999
                
            if(vmax == None):
                vmax=-999.
            else:
                vmax=vmax*ms2knots
    
            if(radii != None):
                (r34,c34,meanR34)=getR34(radii, m, vmax,nEns)
                (r50,c50,meanR50)=getR50(radii, m, vmax,nEns)
                (r64,c65,meanR64)=getR64(radii, m, vmax,nEns)
            else:
                r0=r1=r2=r3=0.0
                r34=(r0,r1,r2,r3)
                meanR34=(r0+r1+r2+r3)*0.25
                c34="%3.0f %3.0f %3.0f %3.0f"%(r0,r1,r2,r3)
                meanR50=meanR64=-999.0
                
            #print 'RRRMMM: ',meanR34,meanR50,meanR64
            
            #print 'TTT %03d'%(tau),'Posit: %6.1f %7.1f'%(rlat,rlon),'RmaxLL: %6.1f %7.1f  rmax: %3.0f'%(rlatM,rlonM,rmax),'pmin: %6.1f'%(pmin),'vmax: %5.0f '%(vmax),'r34: ',c34,'r50: ',c50
            # -- always make the R34 card
            if(rlat != -999.):
                acard=makeAdeckCard(stmid,aid,dtg,tau,rlat,rlon,pmin,vmax,rmax,34,r34)
                if(verb): print acard.strip()
                MF.append2KeyDictList(acards, stmid, aid, acard)

                # -- make the R50 card if radii
                #
                if(meanR50 > 0.0):
                    acard=makeAdeckCard(stmid,aid,dtg,tau,rlat,rlon,pmin,vmax,rmax,50,r50)
                    print 'DDD-555 R50 Card: %s  meanR50: %3.0f (%3.0f %3.0f %3.0f %3.0f)'%(acard[0:-1],meanR50,\
                                                                                        r50[0],r50[1],r50[2],r50[3])
                    
                    if(verb): print acard.strip()
                    MF.append2KeyDictList(acards, stmid, aid, acard)
                    
                # -- make the R64 card if radii
                #
                if(meanR64 > 0.0):
                    acard=makeAdeckCard(stmid,aid,dtg,tau,rlat,rlon,pmin,vmax,rmax,64,r64)
                    print 'DDD-666 R64 Card: %s  meanR64: %3.0f (%3.0f %3.0f %3.0f %3.0f) <---666'%(acard[0:-1],meanR64,\
                                                                                        r64[0],r64[1],r64[2],r64[3])
                    
                    
                    if(verb): print acard.strip()
                    MF.append2KeyDictList(acards, stmid, aid, acard)
                    
                    
    pSkip=(float(mSkip)/float(nEns))*100.
    
    if(pSkip == 100.):
        if(verb): print 'OOO-- Skip ALL for: ',bfile,' bsiz: ',bsiz
    else:
        print 'OOO-- nEns: ',nEns,' mSkip: ',mSkip,' pSkip: %3.0f%%'%(pSkip),'for: ',bfile,' bsiz: ',bsiz
                 
    rc=1   
    return(rc)
            
def removeDups(acards,verb=0):
    """ the R50/R64 can be different in different .bufr...
    remove but filling dict
"""    
    
    for kk in acards.keys():
        ss=acards[kk].keys()
        if(verb): print 'kk:',kk,'ss:',ss
        
        for s in ss:
            if(verb): print 'ss: ',s
            
            ocards=acards[kk][s]
            ncards=[]
            ncardsD={}
            taus=[]
            arads=[]
            rads={}
            
            for ocard in ocards:
                tt=ocard.split(',')
                basin=tt[0].strip()
                stmnum=tt[1].strip()
                tau=int(tt[5])
                rad=int(tt[11])
                taus.append(tau)
                arads.append(rad)
                ncardsD[(tau,rad)]=ocard
                MF.append2KeyDictList(rads, tau, rad, rad)
                
            taus=mf.uniq(taus)
            arads=mf.uniq(arads)
            
            for tau in taus:
                
                for arad in arads:
                    
                    try:
                        ndup=len(rads[tau][arad])
                        ncard=ncardsD[(tau,arad)]
                        ncards.append(ncard)
                        if(ndup > 1):
                            print 'WWW--removeDups aid: %7s tau: %3d  rad: %3d  basin: %s snum: %s'\
                                  %(s,tau,arad,basin,stmnum)
                            
                    except:
                        None

            if(verb):
                for ncard in ncards:
                    print 'nnn',ncard.strip()
                
            acards[kk][s]=ncards
            
    return(acards)
    
    
    