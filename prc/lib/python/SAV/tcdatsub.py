
import TCw2 as TC
import mf
import os,sys
import atcf

from math import sqrt

dTau=12


def SetFtpServer(pushcenter):
    
    if(pushcenter == 'llnl'):
        server='sprite.llnl.gov'
        ftpdirput='/var/ftp/pub/fiorino/npmoc'
    
    elif(pushcenter == 'npmoc'):
        server='blackgbs.npmoc.navy.mil'
        server='199.10.200.38'
        ftpdirput='/comms_dir/llnl/ecmwf'

    return(server,ftpdirput)



def PingFtpServer(server):

    tt=server.split('.')
    if(len(tt) == 3):
        servercheck=tt[0]
    elif(len(tt) == 4 and tt[0].isdigit()):
        servercheck=server
    else:
        servercheck=server

    dsec=5
    nsec=1
    nsecmax=nsec+2*dsec

    verb=0
    while(nsec<=nsecmax):
        cmd='ping -w %s %s'%(nsec,server)
        #
        # uset popen4 because stdout and stderr go to O
        #
        (I,O)=os.popen4(cmd)
        try:
            cards=O.readlines()
        except:
            cards=[]

        status=1
        for card in cards:
            if(verb): print server,'ccc',card
            if(mf.find(card,'0 received')):
                status=0
            elif(mf.find(card,'unknown host')):
                status=-1

        if(status==1):
            break

        elif(status == -1):
            print "unknown host: %s; bail"%(server)
            status=0
            break
            
        else:
            nsec=nsec+5
            print "bump ping wait to: %d ; try again"%(nsec)
        
        
    return(status)

def CheckFtpServer(server):

    tt=server.split('.')
    if(len(tt) == 3):
        servercheck=tt[0]
    elif(len(tt) == 4):
        servercheck=server
        
    verb=1
    cmd='traceroute %s'%(server)
    cards=os.popen(cmd).readlines()
    status=0
    for card in cards:
        if(verb): print server,card
        if(card.find(servercheck) != -1): status=1
    return(status)

def RegionalCtl(dtg,ni,nj,blat,dlat,blon,dlon,undef,taus):

    nt=len(taus)
    dt=12
    gtime=mf.dtg2gtime(dtg)
    
    ctl="""dset ^t.dat
title test
undef %s
xdef %3d linear %5.1f  %5.1f
ydef %3d linear %5.1f  %5.1f
zdef   1 levels 1013
tdef %3d linear %s %dhr
vars 1
n 0 0 # of ensembles per grid box and tau [nd] 
endvars"""%(str(undef),
            ni,blon,dlon,
            nj,blat,dlat,
            nt,gtime,dt)

    #print ctl

    cpath='/tmp/t.ctl'
    c=open(cpath,'w')
    c.writelines(ctl)
    c.close()

    return(cpath)
                          
    
def ParseEcmwfTracksMsl(cards,bdtg,stmid,source):

    """
    parse psl ecmwf tracks (msl in ec terms)

    """

    verb=1
    members=[]
    increments={}
    etrk={}

    if(source == 'msl'):
        ib=4
    elif(source == 'eps'):
        ib=2

    n=len(cards)

    i=ib
    while(i<n):
        
        tt=cards[i].split()

        lat=float(tt[0])
        lon=float(tt[1])
        #
        # convert to deg E
        #
        if(lon < 0.0): lon=360.0+lon
        member=int(tt[2])

        
        if(source == 'msl' or source == 'eps'):
            if(member == 52):
                dtaumsl=6.0
            else:
                dtaumsl=12.0
        
        members.append(member)
        yyyymmdd=tt[3]
        hh=int(tt[4])/100

        taudtg=yyyymmdd+"%02d"%(hh)
        
        pmin=float(tt[5])

        #
        # bad pmin...
        #
        if(pmin < 800.0):
            pmin=0
            vmax=0
        else:
            vmax=TC.HolidayAtkinsonPsl2Vmax(pmin)
        #
        # boost max wind and round to nearest 5
        #
        EcmwfVmaxAliasFactor=1.25
        vmax=vmax*EcmwfVmaxAliasFactor
        #vmax=int((vmax/5.0)+0.5)*5.0

        tau=mf.dtgdiff(bdtg,taudtg)
        tau=int(tau)
        tcparms=(lat,lon,pmin,vmax,tau)
        try:
            etrk[member].append(tcparms)
        except:
            etrk[member]=[]
            etrk[member].append(tcparms)
            
        increments[member]=dtaumsl

        i=i+1


    nmembers=mf.uniq(members)
    
    return(nmembers,increments,etrk)


def ParseEcmwfTracks(cards,obsflg,verb=0):

    members=[]
    increments={}
    etrk={}

    stmid=cards[1].split()[2]
    stmname=cards[2].split()[2]

    ib=4
    if(obsflg): ib=6
    n=len(cards)

    if(verb):
        i=ib
        while(i<n):
            print 'ccc ',i,cards[i][:-1]
            i=i+1

    i=ib
    while(i<n):
        if(verb): print 'ccc ',i,cards[i][:-1]
        member=int(float(cards[i].split()[1]))
        members.append(member)
        i=i+1
        increment=float(cards[i].split()[1])
        i=i+1
        nsteps=int(float(cards[i].split()[3]))
        if(verb): print 'nnn ',member,nsteps,increment

        increments[member]=increment
        i=i+1
        trk=[]
        for j in range(0,nsteps):
            tt=cards[i].split()
            lat=float(tt[0])
            lon=float(tt[1])
            tau=j*increment
            #
            # convert to deg E
            #
            if(lon < 0.0): lon=360.0+lon
            pmin=float(tt[2])
            vmax=float(tt[3])*TC.ms2knots
            if(verb): print i,j,i,lat,lon,pmin,vmax
            tcparms=(lat,lon,pmin,vmax,tau)
            trk.append(tcparms)
            i=i+1
        etrk[member]=trk
            

    return(members,increments,etrk)


#
#  move ecmwf files to data dir
#

def RegionalGrid(blat,elat,dlat,blon,elon,dlon,undef,taus):

    InitialValue=0.0

    latsiz=elat-blat
    lonsiz=elon-blon
    
    grid={}
    ni=int(lonsiz/dlon)+1
    nj=int(latsiz/dlat)+1
    nij=ni*nj

    Initial=0.0

    for tau in taus:
        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                grid[ii,tau]=InitialValue
    
            
    return(ni,nj,nij,grid)

def GlobalGrid(dlon,dlat,undef,taus):

    grid={}
    ni=int(360.0/dlon)
    nj=int(180.0/dlat)+1
    nij=ni*nj

    InitialGrid=0.0

    for tau in taus:
        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                grid[ii,tau]=InitialGrid
    
            
    return(ni,nj,nij,grid)


def ll2i(lon,lat,dlon,dlat,lon0,lat0,ni,nj):

    i=(lon - lon0)/dlon + 0.5 
    j=(lat - lat0)/dlon + 0.5 

    if(i<=0): i=ni+i
    if(i>=ni): i=i-ni

    i=int(i+1.0)
    j=int(j+1.0)

    ii=(j-1)*ni + i

    return(ii)

def LatLonBounds(lats,lons):

    latinc=loninc=5.0
    
    latbuff=10.0
    lonbuff=15.0

    latmaxplot=50.0
    lonmaxplot=80.0

    maxlat=maxlon=-999.9
    minlat=minlon=999.9

    for lat in lats:
        if(lat < minlat): minlat=lat
        if(lat > maxlat): maxlat=lat

    for lon in lons:
        if(lon < minlon): minlon=lon
        if(lon > maxlon): maxlon=lon

    latbar=(minlat+maxlat)*0.5
    lonbar=(minlon+maxlon)*0.5

    nj1=int( minlat/latinc+0.5 )
    nj2=int( maxlat/latinc+0.5 )
    nj3=int( minlon/loninc+0.5 )
    nj4=int( maxlon/loninc+0.5 )

    j1=nj1*latinc
    j2=nj2*latinc
    j3=nj3*loninc
    j4=nj4*loninc

    latplotmin=j1-latbuff
    latplotmax=j2+latbuff
    lonplotmin=j3-lonbuff
    lonplotmax=j4+lonbuff
    
    return(latplotmin,latplotmax,lonplotmin,lonplotmax)
                                
    latplotmin=int( (latbar - (latmaxplot/2) )/latinc + 0.5)*latinc
    latplotmax=latplotmin + latmaxplot

    lonplotmin=int( (lonbar - (latmaxplot/2) )/loninc + 0.5)*loninc
    lonplotmax=lonplotmin + lonmaxplot
    
    return(latplotmin,latplotmax,lonplotmin,lonplotmax)


def MakeTauTrack(ectrack,bdtg,taus,inctau,alltaus):
    
    track={}
    ttau=0

    if(alltaus):
        for e in ectrack:
            etau=e[4]
            track[etau]=e[0:4]

    else:
        for e in ectrack:
            for tau in taus:
                if(ttau == tau):
                    track[ttau]=e
            ttau=ttau+inctau

    return(track)

    
def MakeAdeck(model,ostmid,dtg,adeckdir,ectrack,server=None,ftpdirput=None,
              trktype='all',doftp=0,verb=0):

    taus=ectrack.keys()
    taus.sort()
    
    stmnum=ostmid[0:2]
    basin1=ostmid[2:3]
    basin2=TC.Basin1toBasin2[basin1]
    adeckname=atcf.ModelNametoAdeckName[model]
    adecknum=atcf.ModelNametoAdeckNum[model]
    r34ne=r34se=r34sw=r34nw=0
    adum=0

    if(trktype == 'all'):
        adeckfile="wxmap.%s.%s.%s"%(model,dtg,ostmid)
    else:
        adeckfile="wxmap.MSL.%s.%s.%s"%(model,dtg,ostmid)

    apath="%s/%s"%(adeckdir,adeckfile)

    if(verb):
        print 'AAAAA making adeck to: ',apath
    a=open(apath,'w')

    for tau in taus:

        itau=int(tau)
        (lat,lon,pmin,vmax)=ectrack[tau]

        ivmax=mf.nint(vmax)
        ipmin=mf.nint(pmin)

        (clat,clon,ilat,ilon,hemns,hemew)=TC.Rlatlon2Clatlon(lat,lon)

        acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,dtg,adecknum,adeckname,itau)

        acard1=" %3d%1s, %4d%1s, %3d, %4d, XX,  34, NEQ, %4d, %4d, %4d, %4d,"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw)

        acard=acard0+acard1
        if(verb): print acard
        a.writelines(acard+'\n')

    a.close()

    if(doftp):
        
        #
        # ftp put adeck
        #
        mf.doFTPsimple(server,adeckdir,ftpdirput,adeckfile)

    return(apath)

def AnalyzeMembers2Grid(members,increments,etrk,dlat,dlon,undef,taus,dtg):

    verb=0
    
    lats=[]
    lons=[]

    for member in members:
        trk=etrk[member]
        for t in trk:
            (lat,lon,pmin,vmax)=t
            lats.append(lat)
            lons.append(lon)

    (blat,elat,blon,elon)=LatLonBounds(lats,lons)
    (ni,nj,nij,grid)=RegionalGrid(blat,elat,dlat,blon,elon,dlon,undef,taus)

    cpath=RegionalCtl(dtg,ni,nj,blat,dlat,blon,dlon,undef,taus)

    ntau={}
    for tau in taus:
        ntau[tau]=0.0

    for member in members:
        dt=increments[member]
        trk=etrk[member]
        rtau=0.0

        for t in trk:
            (lat,lon,pmin,vmax)=t
            itau=int(rtau)

            ii=ll2i(lon,lat,dlon,dlat,blon,blat,ni,nj)
            for tau in taus:
                if(itau == tau):
                    ##print 'iiiii increment ',tau,ii
                    grid[ii-1,tau]=grid[ii-1,tau]+1.0
                    ntau[tau]=ntau[tau]+1.0

            rtau=rtau+dt


    if(verb):
        for tau in taus:
            print 'tau = ',tau,ntau[tau]
    
    import array

    g=array.array('f')

    (dir,file)=os.path.split(cpath)
    (base,ext)=os.path.splitext(file)

    dpath="%s/%s.dat"%(dir,base)

    o=open(dpath,'wb')

    ngrid=[]

    for tau in taus:

        if(tau == 0):
            for i in range(0,ni):
                for j in range(0,nj):
                    ii=j*ni + i
                    ngrid.append(0.0)


        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                #print 'BBBBBBBBB ',ii,tau,grid[ii,tau]
                if(grid[ii,tau] > 0.0):
                    ngrid[ii]=grid[ii,tau]
                    if(verb): print 'BBBBBBBBB ',ii,tau,ngrid[ii]
                if(grid[ii,tau] == 0.0):
                    ngrid[ii]=undef


        #print 'writing tau = ',tau
        g.fromlist(ngrid)

    g.tofile(o)

    o.close()

    return(cpath)


def GetEcmwfEpsTcs(paths,source='msl',verb=0):

    paths.sort()

#    paths=[
#        '/pcmdi/ftp_incoming/fiorino/tracks_06L_2004082600.fm',
#        '/pcmdi/chico_dat/wxmap2/dat/tc/fc/ecmwf/eps/tracks_22W_2004082400.fm',
#        '/pcmdi/ftp_incoming/fiorino/tracks_06L_2004082512.fm',
#        ]

    etcs=[]
    trktypes=[]
    for path in paths:
        if(verb): print 'ECTC path       : ',path
        (dir,filePext)=os.path.split(path)
        (file,ext)=os.path.splitext(filePext)

        tt=file.split('_')

        if(len(tt) == 4 and source == 'arch'):
            trktype='all'
            dtg=tt[3]
            istmid=tt[1]
        elif(len(tt) == 5):
            if(tt[1] == 'det'): trktype='ecmo'
            if(tt[1] == 'eps'): trktype='ecme'
            dtg=tt[4]
            istmid=tt[3]
        elif(len(tt) == 3 and source == 'arch' and tt[0] != 'msl'):
            trktype='all'
            dtg=tt[2]
            istmid=[1]
        elif(len(tt) == 3 and tt[0] == 'msl'):
            trktype='eps'
            dtg=tt[2]
            istmid=[1]

        elif(source == 'arch'):
            trktype='all'
            dtg=tt[2]
            istmid=tt[1]
        

        
        #
        # set mincards to > no trackers...
        #
        if(trktype == 'ecme'):
            mincards=163
        elif(trktype == 'ecmo'):
            mincards=10
        elif(trktype == 'eps'):
            mincards=50
        elif(trktype == 'all'):
            mincards=163

        tcs=TC.findtcs(dtg,srcopt='bt.ops')

        ecards=open(path).readlines()
        necards=len(ecards)

        if(verb):
            for tc in tcs:
                print 'ECTC obs tc: ',tc
            print 'ECTC file,istmid,dtg : ',file,istmid,dtg
            print 'ECTD necards,trktype : ',necards,trktype
            
            for ecard in ecards:
                print ecard[:-1]


        if(necards > mincards):

            obsflg=0
            if(trktype == 'all'):
                
                istmid=ecards[1].split()[2]
                istmname=ecards[2].split()[2]

                #
                # search for a member with initial position -- the first one might not have one...
                #
                #
                # 20040902 new format may have obs lat/lon
                #

                ichk=6

                obslat=obslon=None
                obsflg=0
                
                testlat=ecards[3].split()
                testlon=ecards[4].split()

                if(testlat[1] == 'lat:'):
                    obslat=float(testlat[2])
                    
                if(testlon[1] == 'lon:'):
                    obslon=float(testlon[2])

                if(obslat and obslon):
                    print "OOOOOOOOOOOOO obslat: %5.1f %6.1f"%(obslat,obslon)
                    ichk=8
                    obsflg=1

                
                #print 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq ',path
                #for i in range(0,len(ecards)):
                #    if(i < 20):
                #        print i,ecards[i][:-1]

                print 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq ',ecards[ichk].split()
                nmember=int(float(ecards[ichk].split()[3]))

                
                if(nmember != 0):
                    print 'qqqqqqqqq ',nmember
                    ilatlon=ichk+1
                else:
                    ninter=0
                    while(nmember == 0 and ninter < 52):
                        ichk=ichk+3
                        try:
                            nmember=int(float(ecards[ichk].split()[3]))
                            if(verb): print '000000 ',ecards[ichk],ninter,nmember
                            ninter=ninter+1
                        except:
                            print 'WWWWWWWWWWWWWWWWWWW no trackers at all..........'
                            print 'in GetEcmwfEpsTcs: ',path
                            sys.exit()

                    ilatlon=ichk+1

            elif(trktype == 'ecmo'):
                ilatlon=4
                nmember=1
                
            elif(trktype == 'ecme'):
                ilatlon=4
                nmember=51

            elif(trktype == 'eps'):
                ilatlon=2
                nmember=52

            ee=ecards[ilatlon].split()
            
            istmlat=float(ee[0])
            istmlon=float(ee[1])
            if(verb): print 'nnnnnnnnnnnnnnnnn ',nmember,ilatlon,istmlat,istmlon

            distmin=1e20
            distmin=300.0
            i=0
            imin=-999
            for tc in tcs:
                tcid=tc.split()[1]
                tclat=float(tc.split()[4])
                tclon=float(tc.split()[5])
                dist=TC.gc_dist(tclat,tclon,istmlat,istmlon)
                if(dist < distmin):
                    distmin=dist
                    imin=i
                #print '11 ',dist,' 222 ',tcid,tclon,istmlat,istmlon
                i=i+1

            #
            # no match
            #
            if(imin<0):
                tcard=(None,path,dtg,None,None)
            else:
                ostmid=tcs[imin].split()[1]
                print 'qqq ',trktype,ostmid,obsflg
                tcard=(ostmid,path,dtg,trktype,obsflg)
                
            etcs.append(tcard)

            trktypes.append(trktype)
            
    return(etcs,trktypes)

#
# verification TCs by dtg, Must BE >= 20 kts!!!!!
#

def FindTcsBtMoFinal(dtg):

    vmaxmin=20.0
    
    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(TC.BtDir,yyyy,yyyymm)

    try:
        b=open(btmopath)
    except:
        print 'EEEE unable to open ',btmopath
        sys.exit()

    cmd="grep -s -h %s %s"%(dtg,btmopath)
    cards=os.popen(cmd).readlines()

    tcs=[]
    for card in cards:
        tt=card.split()
        vmax=float(tt[2])

        if(vmax >= vmaxmin):
            tcs.append(card[:-1])
        
    return(tcs)


def ReadBtMoFinal(dtg):

    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(TC.BtDir,yyyy,yyyymm)

    try:
        b=open(btmopath)
    except:
        print 'EEEE unable to open ',btmopath
        sys.exit()


    cards=b.readlines()
    b.close()

    btcs={}
    btstmids={}
    btcstms={}
    
    for card in cards:
        tt=card.split()
        dtg=tt[0]
        stmid=tt[1]
        vmax=int(tt[2])
        pmin=int(tt[3])
        lat=float(tt[4])
        lon=float(tt[5])
        dir=float(tt[8])
        spd=float(tt[9])
        btdata=(lat,lon,vmax,pmin,dir,spd)
        btdatadtg=(dtg,lat,lon,vmax,pmin,dir,spd)
        btcs[dtg,stmid]=btdata
        try:
            btstmids[dtg].append(stmid)
        except:
            btstmids[dtg]=[stmid]

        try:
            btcstms[stmid].append(btdatadtg)
        except:
            btcstms[stmid]=[btdatadtg]
            

    return(btcs,btstmids,btcstms)

def MakeBtMoFinal(dtg,verb=0):

    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(TC.BtDir,yyyy,yyyymm)

    print 'btmopath ',btmopath

    b=open(btmopath,'w')

    ddtg=6
    bdtg=yyyymm+'0100'
    edtg=yyyymmp1+'2100'

    vdtgs=mf.dtgrange(bdtg,edtg,ddtg)

    for vdtg in vdtgs:
        if(verb): print 
        tcs=TC.findtcs(vdtg)
        for tc in tcs:
            if(verb): print tc
            b.writelines(tc+'\n')

    b.close()


    return()


def ParseAdeckCards(dtg,cards):

    verb=0

    stms=[]
    ftcs={}
    ftcstruct={}

    taumax=120

    for card in cards:
        
        if(verb):
            print card[:-1]
            
        tt=card.split(',')

        bid2=tt[0][0:2]
        bid1=TC.Basin2toBasin1[bid2]

        stmnum=int(tt[1])
        stm="%02d%s"%(stmnum,bid1)

        stms.append(stm)

        tau=int(tt[5])
        clat=tt[6]
        clon=tt[7]
        
        try:
            vmax=int(tt[8])
        except:
            vmax=-88.8
            
        try:
            pmin=int(tt[9])
        except:
            pmin=-888.8

        (rlat,rlon,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(clat,clon)
        #print 'bbb ',bid2,bid1,stmnum,stm,tau,clat,clon,rlat,rlon

        if(tau == 0):
            wlat=rlat
            wlon=rlon
            ftcs[stm]=[(wlat,wlon)]
        
        sdtgm12=mf.dtginc(dtg,tau-12);
        sdtgp12=mf.dtginc(dtg,tau+12);
        sdtg=mf.dtginc(dtg,tau);
        lat=rlat
        lon=rlon
        ccirc='CC'

        ftcstruct[stm,tau,'spdmax','val']=vmax
        ft=(tau,sdtg,sdtgm12,sdtgp12,lat,lon,ccirc)
        #print 'ffff ',ft
        try:
            ftcs[stm].append(ft)
        except:
            print 'EEE bad ft in ftcs',stm,ft
            sys.exit()
            
    stms=mf.uniq(stms)
    #for stm in stms:
    #    print 'sssss ',stm,ftcs[stm]


    for stm in stms:
        
        np=len(ftcs[stm])
        if(np == 1):
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)
            
    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dTau+1
            sdtg=fsdtg
            tau=ftau+dTau
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dTau)
                sdtgm12=mf.dtginc(sdtg,-dTau)
                sdtgp12=mf.dtginc(sdtg,+dTau)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dTau
                



    return(ftcs,ftcstruct)


def NoLoadFtCards(dtg,tcs):

    ftcs={}
    stms=[]
    btlat={}
    btlon={}

    taumax=120
    
    for tc in tcs:
        stmid=tc.split()[1]
        stmid=stmid.split('.')[0]

        btlat[stmid]=float(tc.split()[4])
        btlon[stmid]=float(tc.split()[5])
        
        stms.append(stmid)
        
    for stm in stms:

        wtlat=btlat[stm]
        wtlon=btlon[stm]
        
        ftcs[stm]=[(wtlat,wtlon)]
        ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
        ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dTau+1
            sdtg=fsdtg
            tau=ftau+dTau
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dTau)
                sdtgm12=mf.dtginc(sdtg,-dTau)
                sdtgp12=mf.dtginc(sdtg,+dTau)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dTau
                



    return(ftcs)


def ParseFtCards(dtg,cards):

    verb=0
    
    stms=[]
    ftcs={}

    #
    # for older tracking files check if cyclones
    #
    if(cards[0].find('NO CY') != -1):
        print 'WWWW \'NO CYCLONES TO TRACK\' message in track file...'
        return(ftcs)

    
    nstms=int(cards[0].split()[0])

    if(verb):
        print 'nnnn ',nstms,cards[nstms+2]

    n=-1
    for card in cards:
        
        n=n+1
        if(n < nstms+2): continue
        if(verb): print card[:-1]
        tt=card.split()

        if( ( tt[0] == '***') or ( tt[0] != 'LOST' and tt[0] != 'FINISHED') ):

            #
            # new style storm from tracker SSS.YYYY
            #

            try:
                ss=tt[1].split('.')
                stm=ss[0]
            except:
                stm=tt[1]
            
            stms.append(stm)
            
            if( tt[0] == '***'):
                latwarn=float(tt[2])
                lonwarn=float(tt[3])
                ftcs[stm]=[(latwarn,lonwarn)]
            
            else:
                tau=int(tt[0])
                sdtgm12=mf.dtginc(dtg,tau-12);
                sdtgp12=mf.dtginc(dtg,tau+12);
                sdtg=mf.dtginc(dtg,tau);
                lat=float(tt[2])
                lon=float(tt[3])
                ccirc='CC'
                if(float(tt[6]) < 0): ccirc='VM'

                ft=(tau,sdtg,sdtgm12,sdtgp12,lat,lon,ccirc)

                try:
                    ftcs[stm].append(ft)
                except:
                    print 'EEEEEEEEE no warning posit for: ',stm
                    sys.exit()

   
    #
    # extend fc track to taumax (120) with 999 to for force detection of
    # bt for POD purposes
    #

    taumax=120
    
    stms=mf.uniq(stms)
    #
    # check for an fc with no posits
    # add a noload
    #
    donoload=0
    for stm in stms:
        
        np=len(ftcs[stm])
        if(np == 1):
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)
            
        if(donoload):
            (latwarn,lonwarn)=ftcs[stm][0]
            ftcs[stm]=[(latwarn,lonwarn)]
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dTau+1
            sdtg=fsdtg
            tau=ftau+dTau
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dTau)
                sdtgm12=mf.dtginc(sdtg,-dTau)
                sdtgp12=mf.dtginc(sdtg,+dTau)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dTau
                

    return(ftcs)

def TcClass(vmax):

    if(vmax < 30): tcclass='nt'
    if(vmax >=30 and vmax < 35): tcclass='td'
    if(vmax >=35 and vmax < 65): tcclass='ts'
    if(vmax >=65 and vmax < 130): tcclass='ty'
    if(vmax >=130): tcclass='st'
    #
    # case where vmax missing...
    #
    if(vmax == 999): tcclass='nt'

    return(tcclass)
    

def AnalyzeBtCards(cards,stmname):

    verb=0
    btsummary=''
    gdtg35='1776070400'
    glat35=-99.9
    glon35=-999.9

    nnt=0
    ntd=0
    nts=0
    nty=0
    nst=0
    nt=0
    ng=0

    ng35=0
    gflg=0
    gflg35=0
    eflg=0

    tcvmax=0.0

    tccs=[]
    dtgs=[]

    for card in cards[1:]:
        #print card.strip()
        tt=card.split()
        dtg=tt[0]
        stmid=tt[1]
        vmax=int(tt[2])
        rlat=float(tt[4])
        rlon=float(tt[5])

        if(vmax > tcvmax): tcvmax=vmax

        tcc=TcClass(vmax)

        tccs.append(tcc)
        dtgs.append(dtg)
        
        if(tcc == 'nt'): nnt=nnt+1
        if(tcc == 'td'): ntd=ntd+1
        if(tcc == 'ts'): nts=nts+1
        if(tcc == 'ty'): nty=nty+1
        if(tcc == 'st'): nst=nst+1
        
        #
        # genesis point
        #
        
        if(ntd == 1 and nts == 0 and nty == 0 and nst == 0):
            if(verb): print 'GGGG at TD'
            ng=1
        if(ntd == 0 and nts == 1 and nty == 0 and nst == 0):
            if(verb): print 'GGGGSSSS at TS'
            ng=2
        if(ntd == 0 and nts == 0 and nty == 1 and nst == 0):
            if(verb): print 'GGGGTTTTTTTTT at TY!!!!'
            ng=3
        if(ntd == 0 and nts == 0 and nty == 0 and nst == 1):
            if(verb): print 'GGGGTTTTTTTTTSSSSSSSSSSSSSS  at STY!!!!'
            ng=4
        

        #
        # 35 kt genesis point
        #
        
        if(nts == 1):
            if(verb): print 'GGGG at TD'
            ng35=1
            
        if(ng > 0 and gflg == 0):
            gdtg=dtg
            glat=rlat
            glon=rlon
            if(verb): print 'GGGGGG at: ',gdtg
            gflg=1
            
        if(ng35 > 0 and gflg35 == 0):
            gdtg35=dtg
            glat35=rlat
            glon35=rlon
            if(verb): print 'GGGGGG33333555555 at: ',gdtg35
            gflg35=1
            
            
        if(verb): print "%s %s %3d %5.1f %6.1f :: %s"%(dtg,stmid,vmax,rlat,rlon,tcc)

        nt=nt+1


    #
    # work backword for endpoint
    #

    nc=len(tccs)

    edtg=dtgs[nt-1]
    for n in range(nc-1,0,-1):
        if(eflg == 0 and tccs[n] != 'nt'):
            eflg=1
            edtg=dtgs[n]

    #
    # case of NO posit >= 30 kt
    #

    if(nt > 0 and gflg == 0):
        gdtg='9999999999'
        edtg=gdtg
        tclifetime=-99.99
        glat=-99.9
        glon=-99.9
    else:
        tclifetime=(mf.dtgdiff(gdtg,edtg)+6.0)/24.0

    
    sumcard="%s %s :: %12s :: %s %s %6.2f :: %5.1f %6.1f :: %5.1f"%\
             (gdtg[0:4],stmid,stmname,gdtg,edtg,tclifetime,glat,glon,tcvmax)
    #sumcard="%s ::  nt:  %3d  :: nnt: %2d  ntd: %2d  nts: %2d  nty: %2d  nst: %2d"%\
    sumcard="%s ::  %3d  :: %2d  %2d  %2d  %2d %2d"%\
             (sumcard,nt,nnt,ntd,nts,nty,nst)

    sumcard="%s ::  gdtg35: %s :: %5.1f %6.1f"%\
             (sumcard,gdtg35,glat35,glon35)

    print sumcard
    return(sumcard)
    

def StripList(list):
    nlist=[]
    for tt in list:
        ttt=tt.strip()
        nlist.append(ttt)
    return(nlist)
    

def GrepTcVeriSum(veridir,veritype,verirule,model,tau,area,areaid,undef,years):

    sumdata={}

    noload=[]
    
    ns=7
    for i in range(0,ns):
        noload.append(undef)
        
    noload=tuple(noload)
    
    for year in years:
        sumdata[year]=(noload)

    vmask="%s/tc.veri.sum.%s.????.%s.txt"%(veridir,veritype,verirule)

    cmd="grep -s -h \' %s, \' %s | grep -s  \' %s, \' | grep -s \' %s, \' | grep -s \' %s, \' "%\
         (model,vmask,tau,area,areaid)

    cards=os.popen(cmd).readlines()

    print 'vvvvvvvvvv ',model,verirule,tau,area
    
    for card in cards:
        
        tt=card.split(',')
        ttt=StripList(tt)
        yyyy=int(ttt[0].split('.')[1])
        tt=tuple(ttt[6:13])
        (nbt,nfc,pod,fe,impclp,ate,cte)=tt
        #print yyyy,model,nbt,nfc,pod,fe,impclp,ate,cte
        sumdata[yyyy]=(tt)

    print

    return(sumdata)
        

def VarTcVeriSum(varopt,sumdata,undef,years):

    ovar=[]

    for year in years:
        (nbt,nfc,pod,fe,impclp,ate,cte)=sumdata[year]
        if(float(pod) == 0.0):
            pod=undef
            fe=undef
            impclp=undef
            
        if(varopt == 'pod'):
            print 'ssss ',year,nbt,nfc,pod,varopt
            ovar.append(float(pod))
        elif(varopt == 'fe'):
            print 'ssss ',year,fe,varopt
            ovar.append(float(fe))
        elif(varopt == 'impclp'):
            print 'ssss ',year,impclp,varopt
            ovar.append(float(impclp))
        elif(varopt == 'nbt'):
            print 'ssss ',year,impclp,varopt
            ovar.append(float(nbt))
        elif(varopt == 'nfc'):
            print 'ssss ',year,impclp,varopt
            ovar.append(float(nfc))
        else:
            print 'EEE invalid varopt in VarTcVerSum: %s'%(varopt)

    return(ovar)

def AreaName(area,areaid):
    
    varaeid='99'
    if(area == 'hemi'):
        if(areaid == 'W'): vareaid='WESTPAC'
        if(areaid == 'EP'): vareaid='EASTPAC'
        if(areaid == 'N'): vareaid='NHEM'
        if(areaid == 'S'): vareaid='SHEM'
    
    if(area == 'basin'):
        if(areaid == 'W'): vareaid='WESTPAC'
        if(areaid == 'E'): vareaid='EASTPAC'
        if(areaid == 'L'): vareaid='LANT'
        if(areaid == 'S'): vareaid='SHEM'

    return(vareaid)


def VarOptName(varopt):

    if(varopt == 'impclp'):
        tvaropt='% improve over CLP'
    elif(varopt == 'fe'):
        tvaropt='FE (nm)'
    elif(varopt == 'pod'):
        tvaropt='POD [%]'
    elif(varopt == 'nbt'):
        tvaropt='N (BT) [#]'
    elif(varopt == 'nfc'):
        tvaropt='N (fc) [#]'

    return(tvaropt)


def VeriRuleName(vr):
    
    tt=vr.split('.')

    if(tt[1] == 'hetero'): vtype="Hetero"
    if(len(tt) >= 3):
        if(tt[2] == 'hetero'): vtype="Hetero"

    if(tt[1] == 'homo'): vtype="Homogeneous %s:%s"%(tt[2],tt[3])

    if(len(tt) >= 3):
        if(tt[2] == 'homo'): vtype="Homogeneous %s:%s"%(tt[3],tt[4])

    if(vr.find('nhc.pure') != -1): veriname="%s %s"%(vtype,'NHC')
    if(vr.find('jtwc') != -1): veriname="%s %s"%(vtype,'JTWC')
    if(vr.find('jtwc.mod') != -1): veriname="%s %s"%(vtype,'JTWC(mod)')
    if(vr.find('td30') != -1): veriname="%s %s"%(vtype,'>= TD')
    if(vr.find('nhc.wind') != -1): veriname="%s %s"%(vtype,'>= TS')
    
    return(veriname)



def ModelName(model):
    
    if(model == 'e40'): modelname="ERA-40"
    elif(model == 'ifs'): modelname="ECMWF IFS"
    elif(model == 'clp'): modelname="CLIPER"
    elif(model == 'clp'): modelname="CLIPER"
    elif(model == 'ngp'): modelname="NOGAPS"
    
    return(modelname)




def VarCardTcVeriSum(varopt,verirule,model,tau,area,areaid,nv,nt):

    vtau="%03d"%(int(tau))
    vtau="%d"%(int(tau))

    tvaropt=VarOptName(varopt)
    vareaid=AreaName(area,areaid)
    veriname=VeriRuleName(verirule)
    modelname=ModelName(model)
    
    vardesc="%s(%s) : `3t`0=%s : %s : %s : %s"%(modelname,model,vtau,tvaropt,veriname,vareaid)
    varname="v%s"%(nv)
    varcard="%s 0 -1,20,%s   %s"%(varname,nt,vardesc)

    return(varname,vardesc,varcard)

#--------------------------------------------------
#
# title - veri rules
#
#--------------------------------------------------

def TitleVeriRules(verirules):

    title='Veri Rules: '
    nvr=len(verirules)

    if(nvr>1): title=title+' 1) '

    for i in range(0,nvr):

        vr=verirules[i]
        
        veriname=VeriRuleName(vr)

        title=title+veriname

        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def TitleModels(models):

    title='Models: '
    nvr=len(models)

    if(nvr>1): title=title+'1) '
    
    for i in range(0,nvr):
        model=models[i]
        modelname=ModelName(model)
        title=title+"%s(%s)"%(modelname,model)

        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def TitleTaus(taus):

    title='Taus: '

    nvr=len(taus)
    if(nvr>1): title=title+' 1) '
    
    for i in range(0,nvr):
        tau=int(taus[i])
        title=title+"%d"%(tau)
        
        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def TitleAreas(areas):

    title='Basins: '

    nvr=len(areas)
    if(nvr>1): title=title+' 1) '
    
    for i in range(0,nvr):
        vr=areas[i]
        tt=vr.split('.')
        area=tt[0]
        areaid=tt[1]
        areaname=AreaName(area,areaid)
        title=title+"%s"%(areaname)
        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        
def TitleVarOpts(varopts):

    title=''

    nvr=len(varopts)
    if(nvr>1): title=title+' 1) '
    
    for i in range(0,nvr):
        vr=varopts[i]
        varoptname=VarOptName(vr)
        title=title+"%s"%(varoptname)
        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def OrderTcPlotVars(verirules,models,areas,taus,varopts,igvars):

    nvr=len(verirules)
    nvo=len(varopts)
    na=len(areas)
    nm=len(models)
    nt=len(taus)

    verirules=verirules
    models=models
    areas=areas
    taus=taus
    varopts=varopts
    
    ogvars=[]

    fastest='models'
    if(nvr > 1 and nvr >= nm): fastest='verirules'
    if(nm > 1 and nm >=nvr): fastest='models'
    if(nm == 3 and nm >= nvr): fastest='verirules'

    altcol=1

    if(fastest=='verirules'):
        
        altcol=nvr
        for varopt in varopts:
            for model in models:
                for area  in areas:
                    for tau in taus:
                        for v1 in verirules:
                            (vn,vd)=igvars[varopt,tau,area,model,v1]
                            ogvars.append([vn,vd])

    elif(fastest=='models'):
        
        altcol=nm
        for varopt in varopts:
            for area  in areas:
                for tau in taus:
                    for v1 in verirules:
                        for model in models:
                            (vn,vd)=igvars[varopt,tau,area,model,v1]
                            ogvars.append([vn,vd])

    else:
        for v1 in verirules:
            for model in models:
                for area  in areas:
                    for tau in taus:
                        for varopt in varopts:
                            (vn,vd)=igvars[varopt,tau,area,model,v1]
                            ogvars.append([vn,vd])
            

    return(altcol,ogvars)



def SetHomoRule(hiopt):
    
    #
    # homo opts
    #

    homorule='hetero'
    homomodel1=''
    homomodel2=''
    dohomo=0

    if(hiopt != 'null' and hiopt != 'hetero'):

        hh=hiopt.split('.')
        if(len(hh) == 2):
            dohomo=1
            homomodel1=hh[0]
            homomodel2=hh[1]
            homorule='homo.%s.%s'%(homomodel1,homomodel2)
        else:
            print "EEE invalid homo compare options: %s"%(hiopt)
            sys.exit()
            
    return(homorule,homomodel1,homomodel2,dohomo)


def GetTcStatsDic(TCS,basinopt,modelopt):

    if(basinopt == 'NHS'):
        try:
            statsdic=TCS.tcfcNHS
        except:
            statsdic=None

    elif(basinopt == 'SHS'):
        try:
            statsdic=TCS.tcfcSHS
        except:
            statsdic=None
    
    elif(basinopt == 'LTS'):
        try:
            statsdic=TCS.tcfcLTS
        except:
            statsdic=None

    elif(basinopt == 'WPS'):
        try:
            statsdic=TCS.tcfcWPS
        except:
            statsdic=None

    elif(basinopt == 'EPS'):
        try:
            statsdic=TCS.tcfcEPS
        except:
            statsdic=None

    elif(basinopt == 'NIS'):
        try:
            statsdic=TCS.tcfcNIS
        except:
            statsdic=None

    elif(len(basinopt) == 1):
        try:
            statsdic=TCS.tcfcbasin[basinopt]
        except:
            statsdic=None

    models=modelopt.split('.')

    if(statsdic):
        sk=statsdic.keys()
        sk.sort()
    else:
        return(None,None,None)


    stats={}
    taus=[]
    
    for model in models:

        for k in sk:

            tmodel=k.split('.')[0]
            tau=k.split('.')[1]
            taus.append(tau)
            if(tmodel == model):
                try:
                    stats[model,tau].append(statsdic[k])
                except:
                    stats[model,tau]=[]
                    stats[model,tau].append(statsdic[k])
    taus=mf.uniq(taus)
    taus.sort()

    return(models,taus,stats)


    
def ParseFtMfCards(dtg,cards):


    #
    # 20041007: handle bad data
    #
    
    def splitfc(cards,i,undef):

        try:
            scard=cards[i]
        except:
            scard='undef '

        try:
            tt=scard.split()
            tlon=float(tt[1])
            tlat=float(tt[2])
            tval=float(tt[3])
            tdist=TC.gc_dist(flat,flon,tlat,tlon)
        except:
            tdist=tval=tlon=tlat=undef
            
        return(tdist,tval,tlon,tlat)

    def splittau(cards,i):
        tt=cards[i].split()
        type=tt[0]
        tau=int(float(tt[2]))
        stmid=tt[4]
        flon=float(tt[5])
        flat=float(tt[6])
        #print type,tau,stmid,flon,flat
        i=i+1

        tt=cards[i].split()
        #print i,tt
        nhi=int(tt[0])
        nlo=int(tt[1])
        i=i+1

        return(type,tau,stmid,flon,flat,nhi,nlo,i)


    verb=0

    undef=1e20
    
    dcrit={}
    dcrit['SPD','H']=400.0
    dcrit['SPD','L']=200.0
    dcrit['VRT','H']=400.0
    dcrit['VRT','L']=200.0

    ftcstruct={}

    stms=[]
    ftcs={}

    ncards=len(cards)

    for i in range(0,ncards):

        if(mf.find(cards[i],'tau:')):
           
           (type,tau,stmid,flon,flat,nhi,nlo,i)=splittau(cards,i)

           tdcrit=dcrit[type,'H']
           tdmin=undef
           for j in range(0,nhi):
               (tdist,tval,tlon,tlat)=splitfc(cards,i,undef)
               if(tdist < tdcrit and tdist < tdmin):
                   tdmin=tdist
                   tvalcrit=tval
               if(verb): print 'hi ',i,tdcrit,tdist,tlon,tlat,tval,ncards
               i=i+1

           if(type == 'SPD'): typeout='spdmax'
           if(type == 'VRT'): typeout='vrtmax'
           if(tdmin == undef):
               tdmin=-888.8
               tvalcrit=-88.8
           ftcstruct[stmid,tau,typeout,'dist']=tdmin
           ftcstruct[stmid,tau,typeout,'val']=tvalcrit
         
           if(verb):
               print "hhhhhhhhhhh stm: %s tau: %03d type: %s ::  %7.1f  %7.2f"%\
                     (stmid,tau,type,tdmin,tvalcrit)


           tdcrit=dcrit[type,'L']
           tdmin=undef
           for j in range(0,nlo):
               (tdist,tval,tlon,tlat)=splitfc(cards,i,undef)
               if(tdist < tdcrit and tdist < tdmin):
                   tdmin=tdist
                   tvalcrit=tval
               if(verb): print 'lo ',i,tdist,tlon,tlat,tval
               i=i+1
               
           if(type == 'SPD'): typeout='spdmin'
           if(type == 'VRT'): typeout='vrtmin'
           if(tdmin == undef):
               tdmin=-888.8
               tvalcrit=-88.8
           ftcstruct[stmid,tau,typeout,'dist']=tdmin
           ftcstruct[stmid,tau,typeout,'val']=tvalcrit
         

           if(verb):
               print "lllllllllll stm: %s tau: %03d type: %s ::  %7.1f  %7.2f"%\
                     (stmid,tau,type,tdmin,tvalcrit)

           #print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ',i

            


    return(ftcstruct)
        

def GetftcstrucParms(ftcstruct,fcid,tau):
    
    try:
        fmaxspd=ftcstruct[fcid,tau,'spdmax','val']
    except:
        fmaxspd=-88.8

    try:
        fminspd=ftcstruct[fcid,tau,'spdmin','val']
    except:
        fminspd=-88.8

    try:
        fmaxvrt=ftcstruct[fcid,tau,'vrtmax','val']
    except:
        fmaxvrt=-88.8

    try:
        fminvrt=ftcstruct[fcid,tau,'vrtmin','val']
    except:
        fminvrt=-88.8

    try:
        fmaxspddist=ftcstruct[fcid,tau,'spdmax','dist']
    except:
        fmaxspddist=-888.8

    try:
        fminspddist=ftcstruct[fcid,tau,'spdmin','dist']
    except:
        fminspddist=-888.8

    try:
        fmaxvrtdist=ftcstruct[fcid,tau,'vrtmax','dist']
    except:
        fmaxvrtdist=-888.8

    try:
        fminvrtdist=ftcstruct[fcid,tau,'vrtmin','dist']
    except:
        fminvrtdist=-888.8

    return(fmaxspddist,fminspd,fminspddist,fmaxvrt,fmaxvrtdist,fmaxspd)

def FilterHemiTcs(tcs,hemi):
    btcs=[]
    for tc in tcs:
        tt=tc.split()
        tcbasin=tt[1].split('.')[0][2:3]
        tchemi=TC.Basin1toHemi3[tcbasin]
        if(tchemi == hemi):
            btcs.append(tc)
            
    tcs=btcs
    return(tcs)
    

def FilterBasinTcs(tcs,basin):
    btcs=[]
    for tc in tcs:
        tt=tc.split()
        tcbasin=tt[1].split('.')[0][2:3]
        if(tcbasin == basin):
            btcs.append(tc)
            
    tcs=btcs
    return(tcs)
    

def GetTcFcCards(dtg,imodel):

    ftmfcards=None
    ftcards=None
    
    #EcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwf
    #
    # ecmwf trackers
    #
    #EcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwfEcMwf

    if(imodel == 'ecmo' or imodel == 'ecme'):

        ftdir=TC.AdeckDirEcmwf
        ftype='adeck'

        ftmaskops='%s/wxmap.%s.%s.*'%(ftdir,imodel,dtg)
        ftpathsops=glob.glob(ftmaskops)

        ftmaskmsl='%s/wxmap.MSL.%s.%s.*'%(ftdir,imodel,dtg)
        ftpathsmsl=glob.glob(ftmaskmsl)

        if(len(ftpathsmsl) == 0 and len(ftpathsops) != 0):
            ftpaths=ftpathsops
            if(verb): print 'FFFFFFFFF ecmwf: using OPS paths only ',ftpaths

        elif(len(ftpathsmsl) != 0 and len(ftpathsops) == 0):
            ftpaths=ftpathsmsl
            if(verb): print 'FFFFFFFFF ecmwf: using MSL paths only'

        else:
            ftpaths=ftpathsmsl+ftpathsops


        if(verb): print ftpaths

        ftcards=[]    
        for ftpath in ftpaths:
            cards=open(ftpath).readlines()
            for card in cards:
                ftcards.append(card)

    elif(imodel == 'fv4' or imodel == 'fv5'):

        ftdir1=TC.AdeckDirNasa
        ftype='adeck'

        ftmask1='%s/????/wxmap/wxmap.%s.%s.*'%(ftdir1,imodel,dtg)
        if(verb): print 'ADECK ftmask1: ',ftmask1
        ftpaths1=glob.glob(ftmask1)

        ftpaths=ftpaths1

        if(verb):
            print 'adeck data for : ',imodel,' ftpaths: ',ftpaths

        ftcards=[]    
        for ftpath in ftpaths:
            (d,f)=os.path.split(ftpath)
            print 'ooooooooooooo ',f
            cards=open(ftpath).readlines()
            for card in cards:
                ftcards.append(card)

    elif(imodel == 'fg4' or imodel == 'fg5'):

        ftdir1=TC.TcanalDatDir
        ftype='adeck'

        ftmask1='%s/%s/trk/wxmap.%s.%s.*'%(ftdir1,dtg,imodel,dtg)
        if(verb): print 'ADECK ftmask1: ',ftmask1
        ftpaths1=glob.glob(ftmask1)

        ftpaths=ftpaths1

        if(verb):
            print 'adeck data for : ',imodel,' ftpaths: ',ftpaths

        ftcards=[]    
        for ftpath in ftpaths:
            (d,f)=os.path.split(ftpath)
            print 'ooooooooooooo ',f
            cards=open(ftpath).readlines()
            for card in cards:
                ftcards.append(card)

    elif(imodel == 'ofc' or imodel == 'con'):

        ftdir1=TC.AdeckDirJtwc
        ftdir2=TC.AdeckDirNhc
        ftype='adeck'

        ftmask1='%s/????/wxmap/wxmap.%s.%s.*'%(ftdir1,imodel,dtg)
        if(verb): print 'ADECK ftmask1: ',ftmask1
        ftpaths1=glob.glob(ftmask1)


        ftmask2='%s/????/wxmap/wxmap.%s.%s.*'%(ftdir2,imodel,dtg)
        if(verb): print 'ADECK ftmask2: ',ftmask2
        ftpaths2=glob.glob(ftmask2)

        ftpaths=ftpaths1+ftpaths2

        if(verb):
            print 'adeck data for : ',imodel,' ftpaths: ',ftpaths

        ftcards=[]    
        for ftpath in ftpaths:
            (d,f)=os.path.split(ftpath)
            print 'ooooooooooooo ',f
            cards=open(ftpath).readlines()
            for card in cards:
                ftcards.append(card)

    else:

        #ffffffffffffffffffffffffffffffffffffffffffffff
        #
        # mf/fnmoc trackers
        #
        #ffffffffffffffffffffffffffffffffffffffffffffff

        ftype='mf'

        if(prcopt == 'ops'):
            ftdir=TC.ModelFcDir(imodel,mopt='ops')
        else:
            ftdir=TC.ModelFcDir(imodel)

        if(imodel == 'eclp'): imodel='clp'

        ftfile="tc.%s.%s.tracks.txt"%(imodel,dtg)
        ftfilemf="tc.%s.%s.tracks.mf.txt"%(imodel,dtg)

        ftdpath="%s/%s"%(ftdir,ftfile)
        ftdpathmf="%s/%s"%(ftdir,ftfilemf)

        if(verb):
            print 'FFFF paths ',ftdpath,ftdpathmf

        try:
            ftcards=open(ftdpath).readlines()
        except:
            if(verb): print "EEE unable to read/open: %s"%(ftdpath)
            #
            # close to make 0 length
            #
            ftcards=None

        try:
            ftmfcards=open(ftdpathmf).readlines()
        except:
            ftmfcards=None

    return(ftcards,ftmfcards)

def goodid(b1id,source):
    rc=0
    #
    # handle case where both jt and cpc do the same storm
    #
    if(source == 'jtwc'):
        if(b1id == 'W' or b1id == 'S' or b1id == 'P' or b1id == 'A' or b1id == 'I' or b1id == 'B'  or b1id == 'C'): rc=1
        #### forces to do all: rc=1
    elif(source == 'nhc' or source == 'ncep'):
        if(b1id == 'L' or b1id == 'E' or b1id == 'C'): rc=1

    #
    # tpc adecks come from /com/tpc tc trackers for all models; globally
    #
    elif(source == 'tpc' or source == 'gsd' or source == 'hrd' or source == 'local'):
        rc=1

    elif(source == 'nasa'):
        if(b1id == 'L' or b1id == 'E' or b1id == 'C'): rc=1

    return(rc)

def ofcid(b1id):
    #
    # don't override for cpc storms, jt might have the storm
    #
    if(b1id == 'W' or b1id == 'S' or b1id == 'P' or b1id == 'A' or b1id == 'B' or b1id == 'I'): ofc='JTWC'
    if(b1id == 'L' or b1id == 'E' or b1id == 'C'): ofc='OFCL'

    return(ofc)

def radid(source,omodel):

    if(source == 'nhc' or source == 'local'):
        critrad=atcf.CritRadAdeckParserNhc[omodel]

    elif(source == 'jtwc'):
        critrad=atcf.CritRadAdeckParserJtwc[omodel]

    elif(source == 'ncep' or source == 'tpc' or source == 'gsd' or source == 'hrd' or source == 'ecmwf'):
        critrad=atcf.CritRadAdeckParserNhc[omodel]

    return(critrad)

    

def goodsnum(snum,do9x):
    rc=0
    if(snum > 0 and snum <= 50): rc=1
    if(do9x and (snum >= 90 and snum <= 99)): rc=1
    return(rc)


def Adeck2TmpDeck(adeck,imodel,omodel,source,snum,b1id,dtgmask,ropt='',verb=1):

    #
    # add sort | uniq to kill off dups in tpc decks
    # bad idea...except really need to to tpc decks -- only for tpc
    #
    
    tmpdeck="/tmp/adeck.%s.%02d%s.txt"%(omodel,snum,b1id)

    sortopt=''
    if(source == 'tpc'):
        sortopt=' sort +5 | '

        
    gmodel=imodel
    if((imodel == 'JTWC' or imodel == 'OFCL') and (b1id != 'C')):
        gmodel=ofcid(b1id)

    if(len(gmodel) == 3):
       gmodel="' %s,'"%(gmodel)

    #
    # special case for STIP-> ST10 or STID for, NEVER use the id
    #
    if(imodel == 'STIP' and int(dtgmask[0:4]) >= 2006 ):
        
        if(len(dtgmask) == 4 and (b1id == 'P' or b1id == 'S') ):
            dtgmask1=str(int(dtgmask)-1)
            years=[dtgmask1,dtgmask]
        else:
            dtgmask1=dtgmask
            years=[dtgmask1]

        if(len(dtgmask) == 4):
            
            for year in years:
                if(year == dtgmask1):
                    cmd="grep -h %s %s | grep %s |  uniq > %s"%(year,adeck,'STID',sortopt,tmpdeck)
                    mf.runcmd(cmd,ropt)
                    if(os.path.getsize(tmpdeck) == 0):
                        cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(year,adeck,'ST10',sortopt,tmpdeck)
                        mf.runcmd(cmd,ropt)
                    if(os.path.getsize(tmpdeck) == 0):
                        cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(year,adeck,'ST11',sortopt,tmpdeck)
                        mf.runcmd(cmd,ropt)
            
                else:
                    if(os.path.getsize(tmpdeck) == 0):
                        cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(year,adeck,'STID',sortopt,tmpdeck)
                        mf.runcmd(cmd,ropt)
                    if(os.path.getsize(tmpdeck) == 0):
                        cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(year,adeck,'ST10',sortopt,tmpdeck)
                        mf.runcmd(cmd,ropt)
                    if(os.path.getsize(tmpdeck) == 0):
                        cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(year,adeck,'ST11',sortopt,tmpdeck)
                        mf.runcmd(cmd,ropt)
            

        else:
            cmd="grep -h %s %s | grep %s | %s uniq > %s"%(dtgmask,adeck,'STID',sortopt,tmpdeck)
            mf.runcmd(cmd,ropt)
            if(os.path.getsize(tmpdeck) == 0):
                cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(dtgmask,adeck,'ST10',sortopt,tmpdeck)
                mf.runcmd(cmd,ropt)

            if(os.path.getsize(tmpdeck) == 0):
                cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(dtgmask,adeck,'ST11',sortopt,tmpdeck)
                mf.runcmd(cmd,ropt)
    #
    # shem
    # 
    elif(len(dtgmask) == 4 and (b1id == 'P' or b1id == 'S') ):
        
        dtgmask1=str(int(dtgmask)-1)
        years=[dtgmask1,dtgmask]

        for year in years:
            if(year == dtgmask1):
                cmd="grep -h %s %s | grep %s | %s uniq > %s"%(year,adeck,gmodel,sortopt,tmpdeck)
                mf.runcmd(cmd,ropt)
            else:
                cmd="grep -h %s %s | grep %s | %s uniq >> %s"%(year,adeck,gmodel,sortopt,tmpdeck)
                mf.runcmd(cmd,ropt)
            

    else:
        
        cmd="grep -h %s %s | grep %s | %s uniq > %s"%(dtgmask,adeck,gmodel,sortopt,tmpdeck)
        mf.runcmd(cmd,ropt)
        

    if(not(os.path.exists(tmpdeck))):
        print "EEE unable to open tmpdeck: %s"%(tmpdeck)
        cards=None
        return(cards)

    if(os.path.getsize(tmpdeck) == 0):
        print "EEE tmpdeck: %s has 0 length..."%(tmpdeck)
        os.remove(tmpdeck)
        cards=None
        return(cards)

    cards=open(tmpdeck).readlines()
    print 'tmpdeck: ',tmpdeck
    
    os.remove(tmpdeck)

    return(cards)



def Adeck2WxmapDeck(cards,tdir,omodel,stid,critrad,verb=0,override=0):

    stmids=[]
    
    dtgs=[]
    acards={}

    for card in cards:
        bdtg=card[8:18]
        dtgs.append(bdtg)
        try:
            acards[bdtg].append(card)
        except:
            acards[bdtg]=[]
            acards[bdtg].append(card)

    dtgs=mf.uniq(dtgs)


    for dtg in dtgs:

        cards=acards[dtg]


        fc={}
        fc50={}
        fc64={}
        taus=[]

        for card in cards:
            card=card[:-1]
            tt=card.split(',')
            nflds=len(tt)

            tau=int(tt[5])

            try:
                ilat=int(tt[6][0:4])
                ilon=int(tt[7][0:5])
            except:
                print 'WWW missing lat, lon in card: ',card
                continue

            #print 'qqqqqqqqqqqqqqq ',ilat,ilon
            try:
                crad=tt[11].strip()
            except:
                crad=''

            #print 'ttt ',tt[11],' card: ',card
            
            if(len(crad) == 0):
                rad=-99
            else:
                rad=int(crad)
                
            lcard=len(tt)

            #
            # test for bad/funky adeck card...
            #
            if(lcard != 18 and lcard != 23 and lcard != 28):

                fcard=''
                tt=card.split(',')

                lend=lcard-1
                lstart=0
                if(lcard == 30):
                    lstart=0
                    lend=lcard-3

                if(lcard >= 34):
                    lstart=0
                    lend=17
                    
                for i in range(lstart,lend+1):
                    ttt=tt[i]
                    if(i==0):
                        fcard="%s"%(ttt)
                    else:
                        fcard="%s,%s"%(fcard,ttt)

                fcard=fcard+','
                if(verb): print 'bbbbbNNNNN %2d %s'%(lcard,fcard)
                card=fcard

            #-----------------------------------------------------------
            #
            # OK adeck card
            #
            #-----------------------------------------------------------

            tt=card.split(',')
            tau=int(tt[5])

            #
            # filter out bad taus:
            #
    
            if(tau == 7):
                print'77777777777777777777777777777'
                continue

            try:
                crad=tt[11].strip()
            except:
                crad=''
                
            if(len(crad) == 0):
                rad=-99
            else:
                rad=int(crad)


            #
            # pull the r50 data out
            #
            if(rad == 50):
                fccard=''
                for n in range (11,17):
                    fccard=fccard+"%s,"%(tt[n])
                fc50[tau]=fccard

            #
            # pull the r64 data out
            #
            if(rad == 64):
                fccard=''
                for n in range (11,17):
                    fccard=fccard+"%s,"%(tt[n])
                fc64[tau]=fccard

            #
            # the raw adecks from tim's tracker can be very bare, add noloads
            #
            adecknoload='   0,    0,   ,   0,    ,    0,    0,    0,    0,'
            if(nflds == 8):
                card=card+adecknoload
            
            #
            # filter out tau=3 and go for either 0 or 3 (bug in encoder for jma) critrad for pulling tau fc
            #
            # filter out lat/lon = 0 (undef for ships, but not for icon)
            #
            zerolat=(ilat == 0 and ilon == 0)
            norad=(rad == -99)
            rad35=(critrad == 34 and rad == 35)
            goodtau=(tau != 3 and tau != 4 and tau != 1)
            #
            # bad hand decode of by jtwc of rmsc tokyo
            #
            goodtaurjtd=(tau == 0 or tau == 24 or tau == 48 or tau == 72)

            if(omodel == 'rjtd' and not(goodtaurjtd)):
                continue
            elif(
                ( (rad == critrad or rad == 0 or rad == 3 or norad or rad35) and goodtau) and
                (not(zerolat) and not(atcf.IsVmaxOnlyModel(omodel))) or
                (zerolat and atcf.IsVmaxOnlyModel(omodel))
                ):
                fc[tau]=card
                taus.append(tau)

        stmid="%s.%s"%(stid,dtg[0:4])
        stmids.append(stmids)
        wxfile="wxmap.%s.%s.%s"%(omodel,dtg,stid)
        wxpath="%s/%s"%(tdir,wxfile)
        
        dowrite=0
        if(not(mf.ChkPath(wxpath)) or override):
            print 'wxpath: ',wxpath
            A=open(wxpath,'w')
            dowrite=1
        else:
            print 'AAAA wxpath already done: ',wxpath

        if(dowrite):
            for tau in taus:
                try:
                    cfc50=fc50[tau]
                except:
                    cfc50=''
                try:
                    cfc64=fc64[tau]
                except:
                    cfc64=''

                #print 'fc50 ',cfc50
                #print 'fc64 ',cfc64
                #print 'fc   ',fc[tau]
                cfc=fc[tau]+cfc50+cfc64
                ###print cfc
                acard=cfc
                if(verb): print tau,acard[0:100]
                A.writelines(acard+'\n')

            A.close()

    stmids=mf.uniq(stmids)

    return(stmids)

def WxmapAdeck2StormAdeck(tdir,omodel,stmid,ropt='',verb=0):

    stid=stmid.split('.')[0]
    syear=stmid.split('.')[1]
    b1id=stid[2:3]
    b2id=TC.Basin1toBasin2[b1id]
    snum=stid[0:2]
    cmd="cat %s/wxmap.%s.*.%s > %s/a%s%s%s.%s.dat"%(tdir,omodel,stid,tdir,b2id.lower(),snum,syear,omodel)
    mf.runcmd(cmd,ropt)
    


def NasaAdeck2TmpDeck(adeck,verb=0):

    cards=open(adeck).readlines()
    scards={}
    s21=TC.Basin2toBasin1

    print 'AAAAAAAAAAAA ',adeck
    
    for card in cards:
        if(verb): print card[:-1]
        tt=card.split(',')
        try:
            bid=s21[tt[0]]
        except:
            scards={}
            print 'BBBBBBBBBBBBBBBBBBBBB bad data from nasa in adeck: ',adeck
            return(None)
        
        snum=tt[1].strip()
        stid=snum+bid
        imodel=tt[3].strip()
        tau=tt[4].strip()
        if(verb): print bid,stid,imodel,tau
        try:
            scards[stid].append(card)
        except:
            scards[stid]=[]
            scards[stid].append(card)
                
    if(verb):
        stids=scards.keys()
        for stid in stids:
            print 'sss ',stid
            for scard in scards[stid]:
                print 'aaa ',scard[:-1]
    
    return(scards)

def EcmwfBufrAdeckDupChk(cards,stmid):
    
    ocards=[]

    for card in cards:
        tt=card.split(',')
        tau=int(tt[5].strip())
    
        duptau=0
        try:
            for gtau in gottaus:
                if(tau == gtau):
                    print 'DDDDDDDDDDDDDDDDDDDDDD dup tau for: ',stmid,' tau: ',tau
                    duptau=1
        except:
            gottaus=[]

        gottaus.append(tau)

        if(not(duptau)):
            ocards.append(card)

    return(ocards)
        
            



def EcmwfBufrAdeck2TmpDeck(adeck,imodel,verb=0):

    cards=open(adeck).readlines()
    scards={}
    s21=TC.Basin2toBasin1

    print 'AAAAAAAAAAAA ',adeck,imodel

    otau=None
    orlat=None
    orlon=None

    #
    # code for bad bufr -- only add card if no dups in tau, if dup
    # then add no other taus...
    #

    curstid=None

    for card in cards:
        if(verb): print 'AAEE ',card[:-1]
        tt=card.split(',')
        try:
            bid=s21[tt[0]]
        except:
            continue
            scards={}
            print 'BBBBBBBBBBBBBBBBBBBBB bad data from nasa in adeck: ',adeck
            return(None)
        
        snum=tt[1].strip()
        sdtg=tt[2].strip()
        smodel=tt[4].strip()

        #
        # check for unnumbered storm; set to 99
        #
        if(len(snum) == 0):
            snum='99'

        hemi=TC.Basin1toHemi4[bid]

        if(hemi == 'shem'):
            syear=TC.GetShemYear(sdtg)
        else:
            syear=sdtg[0:4]

        stmid="%s%s.%s"%(snum,bid,syear)

        if(smodel == imodel):
            
            tau=int(tt[5].strip())
            clat=tt[6].strip()
            clon=tt[7].strip()
            (rlat,rlon,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(clat,clon)

            addcard=1
            if(tau == 0):
                otau=tau
                orlat=rlat
                orlon=rlon
            #
            # dup taus = lost tracker
            #
            elif(otau == tau):
                print 'EEEEEEE  duppppppp!!!',otau,tau,snum,stmid,smodel
                addcard=0

            if(verb): print bid,stmid,smodel,imodel,tau

            if(addcard):
                try:
                    scards[stmid].append(card)
                except:
                    scards[stmid]=[]
                    scards[stmid].append(card)

                    
            otau=tau
            orlat=rlat
            orlon=rlon


    #
    #  now check for big change
    #

    scards1={}

    stids=scards.keys()
    for stid in stids:
        addcard=1
        for scard in scards[stid]:
            tt=scard.split(',')
            
            tau=int(tt[5].strip())
            clat=tt[6].strip()
            clon=tt[7].strip()
            (rlat,rlon,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(clat,clon)

            if(tau == 0):
                otau=tau
                orlat=rlat
                orlon=rlon
                
            dlat=(orlat-rlat)
            dlon=(orlon-rlon)
            ddist=sqrt(dlat*dlat+dlon*dlon)

            if(ddist > 10.0):
                print 'EEEEEEE  big dist change!!!',ddist,tau,snum,stid,smodel
                addcard=0

            if(addcard):
                try:
                    scards1[stid].append(scard)
                except:
                    scards1[stid]=[]
                    scards1[stid].append(scard)

            otau=tau
            orlat=rlat
            orlon=rlon

                
    if(verb):
        stids=scards1.keys()
        for stid in stids:
            print 'sss ',stid
            for scard in scards1[stid]:
                print 'FFFFFFFFFFFF ',scard[:-1]


    return(scards1)

