import TCw2 as TC
import mf
import os,sys
import glob
import copy

dLatLonEcmwfEPSAnalysis=1.0

dTau12=12


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
                          
    
def ParseEcmwfTracksMsl(cards,stmid,trktype):

    """
    parse psl ecmwf tracks (msl in ec terms)

    """

    verb=0
    members=[]
    increments={}
    etrk={}

    if(trktype == 'eco'):
        dtaumsl=6.0
    elif(trktype == 'ece'):
        dtaumsl=12.0

    ib=4
    n=len(cards)
    if(verb): print 'MSL ',n

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
        
        if(trktype == 'msl'):
            if(member == 52):
                dtaumsl=6.0
            else:
                dtaumsl=12.0
        
        members.append(member)
        yyyymmdd=tt[3]
        hh=int(tt[4])/100
        pmin=float(tt[5])
        vmax=TC.HolidayAtkinsonPsl2Vmax(pmin)
        #
        # boost max wind and round to nearest 5
        #
        EcmwfVmaxAliasFactor=1.25
        vmax=vmax*EcmwfVmaxAliasFactor
        vmax=int((vmax/5.0)+0.5)*5.0

        
        tcparms=(lat,lon,pmin,vmax)
        try:
            etrk[member].append(tcparms)
        except:
            etrk[member]=[]
            etrk[member].append(tcparms)
            
        increments[member]=dtaumsl

        i=i+1


    nmembers=mf.uniq(members)
    
    return(nmembers,increments,etrk)

def ParseEcmwfTracks(cards,obsflg):

    verb=0
    members=[]
    increments={}
    etrk={}
    
    stmid=cards[1].split()[2]
    stmname=cards[2].split()[2]

    print stmid
    print stmname

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
            #
            # convert to deg E
            #
            if(lon < 0.0): lon=360.0+lon
            pmin=float(tt[2])
            vmax=float(tt[3])*TC.ms2knots
            if(verb): print i,j,i,lat,lon,pmin,vmax
            tcparms=(lat,lon,pmin,vmax)
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


def MakeTauTrack(ectrack,taus,inctau):
    
    track={}
    ttau=0
    for e in ectrack:
        for tau in taus:
            if(ttau == tau):
                track[ttau]=e
        ttau=ttau+inctau

    return(track)

    
def MakeAdeck(model,ostmid,dtg,adeckdir,ectrack,server,ftpdirput,
              trktype='all',doftp=1,verb=0):

    taus=ectrack.keys()
    taus.sort()
    
    stmnum=ostmid[0:2]
    basin1=ostmid[2:3]
    basin2=TC.Basin1toBasin2[basin1]
    adeckname=TC.ModelNametoAdeckName[model]
    adecknum=TC.ModelNametoAdeckNum[model]
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

        ivmax=int(vmax)
        ipmin=int(pmin)

        (ilat,ilon,hemns,hemew)=TC.Rlatlon2Clatlon(lat,lon)

        acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,dtg,adecknum,adeckname,itau)

        acard1=" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

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


def GetEcmwfEpsTcs(paths,verb=0):

    paths.sort()

#    paths=[
#        '/pcmdi/ftp_incoming/fiorino/tracks_06L_2004082600.fm',
#        '/pcmdi/chico_dat/wxmap2/dat/tc/fc/ecmwf/eps/tracks_22W_2004082400.fm',
#        '/pcmdi/ftp_incoming/fiorino/tracks_06L_2004082512.fm',
#        ]

    etcs=[]
    for path in paths:
        if(verb): print 'ECTC path       : ',path
        (dir,filePext)=os.path.split(path)
        (file,ext)=os.path.splitext(filePext)

        trktype='all'
        
        tt=file.split('_')

        if(len(tt) == 5):
            if(tt[1] == 'det'): trktype='eco'
            if(tt[1] == 'eps'): trktype='ece'
            dtg=tt[4]
            istmid=tt[3]
        elif(len(tt) == 3 and tt[0] != 'msl'):
            dtg=tt[2]
            istmid=[1]
        elif(len(tt) == 3 and tt[0] == 'msl'):
            trktype='msl'
            dtg=tt[2]
            istmid=[1]

        #
        # check for case with no tracks
        #
        if(trktype == 'eco'):
            mincards=4
        elif(trktype == 'ece'):
            mincards=100
        elif(trktype == 'all' or trktype == 'msl'):
            mincards=200

        tcs=TC.findtc(dtg)

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
                #print 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq ',ecards[ichk].split()
                
                nmember=int(float(ecards[ichk].split()[3]))

                if(nmember != 0):
                    ilatlon=ichk+1
                else:
                    while(nmember == 0):
                        ichk=ichk+3
                        nmember=int(float(ecards[ichk].split()[3]))
                        if(verb): print '000000 ',ichk,nmember

                    ilatlon=ichk+1

            elif(trktype == 'eco'):
                ilatlon=4
                nmember=52
                
            elif(trktype == 'ece'):
                ilatlon=4
                nmember=51

            elif(trktype == 'msl'):
                ilatlon=3
                nmember=52

            ee=ecards[ilatlon].split()
            
            if(verb): print 'nnnn ',nmember,ilatlon
            istmlat=float(ee[0])
            istmlon=float(ee[1])

            distmin=1e20
            distmin=250.0
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
                tcard=(ostmid,path,dtg,trktype,obsflg)
                
            etcs.append(tcard)

    return(etcs)

#
# verification TCs by dtg, Must BE >= 20 kts!!!!!
#

def FindTcsBtMoFinal(dtg,verb=0):

    vmaxmin=20.0
    
    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(TC.BtDir,yyyy,yyyymm)

    if(verb):
        print 'btmopath: ',btmopath

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
        tcs=TC.findtc(vdtg)
        for tc in tcs:
            b.writelines(tc+'\n')
            if(verb): print tc

    b.close()


    return()


def ParseAdeckCards(dtg,cards,dtautracker,verb=0):

    def ParseTcs(tcs,stm):
        
        olat=-99.9
        olon=-999.9
        odir=-999.9
        ospd=-99.9
        otype=None


        for tc in tcs:
            tt=tc.split()
            stmid=tt[1]
            stmid3=stmid.split('.')[0]

            if(stm == stmid3):

                bvmax=float(tt[2])
                blat=float(tt[4])
                blon=float(tt[5])
                bdir=float(tt[8])
                bspd=float(tt[9])

                clat=float(tt[21])
                clon=float(tt[22])
                cvmax=float(tt[23])
                cdir=float(tt[24])
                cspd=float(tt[25])

                if(clat > -89.0):
                    olat=clat
                    olon=clon
                    odir=cdir
                    ospd=cspd
                    ovmax=cvmax
                    otype='carq'
                else:
                    olat=blat
                    olon=blon
                    odir=bdir
                    ospd=bspd
                    ovmax=bvmax
                    otype='bt'


        #print 'qqqqqooooooo ',otype,olat,olon,odir,ospd

        return(olat,olon,odir,ospd,ovmax,otype)


    stms=[]
    ftcs={}
    ftcstruct={}

    taumax=120

    settau0=0
    curstm=None
    curtau=-999

    for card in cards:
        
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

        #
        # 20070620 -- code to handle wind radii
        #
        
        try:
            wrad=int(tt[11])
        except:
            wrad=None
            wrad1=wrad2=wrad3=wrad4=None

        if(wrad == 34 or wrad == 50 or wrad == 64):
            try:
                wrad1=int(tt[13])
                wrad2=int(tt[14])
                wrad3=int(tt[15])
                wrad4=int(tt[16])
            except:
                wrad1=-999.
                wrad2=-999.
                wrad3=-999.
                wrad4=-999.

        #
        # 20070620 -- hwrf is the first model tracker i've hit that outputs wind radii
        # until we add wind radii to the ft=() detect dup and fill only one ft / tau
        #
        #print 'tttttttttttttttt ',dtg,tau,curtau,wrad
        
        if(curtau == tau):
            continue
        else:
            curtau=tau
        
        if(verb):
            print 'CC: ',card[:-1]
            

        (rlat,rlon,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(clat,clon)
        #print 'bbb ',bid2,bid1,stmnum,stm,tau,clat,clon,rlat,rlon


        sdtgm12=mf.dtginc(dtg,tau-12)
        sdtgp12=mf.dtginc(dtg,tau+12)
        sdtg=mf.dtginc(dtg,tau)
        
        lat=rlat
        lon=rlon
        ccirc='CC'

        if(pmin > 0.0 and vmax <= 0.0):
            vmax=TC.HolidayAtkinsonPsl2Vmax(pmin)


        ftcstruct[stm,tau,'spdmax','val']=vmax
        ft=(tau,sdtg,sdtgm12,sdtgp12,lat,lon,ccirc)

        
        if(curstm != stm):
            curstm=stm
            settau0=0

        if(tau == 0 and settau0 == 0):
            
            wlat=rlat
            wlon=rlon
            ftcs[stm]=[(wlat,wlon)]
            settau0=1

        elif( (tau == 6 or tau == 12) and settau0 == 0):
            
            print 'WWWWW no initial posit: ',stm,dtg,tau
            tcs=TC.findtcs(dtg)
            (olat,olon,odir,ospd,ovmax,otype)=ParseTcs(tcs,stm)

            tau0=0
            sdtgm12=mf.dtginc(dtg,tau0-12);
            sdtgp12=mf.dtginc(dtg,tau0+12);
            sdtg=mf.dtginc(dtg,tau0);
            
            ft00=(tau0,sdtg,sdtgm12,sdtgp12,olat,olon,ccirc)
            ftcs[stm]=[(olat,olon)]
            ftcs[stm].append(ft00)

            #
            # set the initial wind for intensity verification
            #
            ftcstruct[stm,tau0,'spdmax','val']=ovmax

            settau0=1

        if(tau > 0 and settau0 == 0):
            print 'EEE---- unable to set tau 0, sayounara'
            sys.exit()


 
        try:
            ftcs[stm].append(ft)
        except:
            print 'EEE---- bad ft in ftcs',stm,tau,' ft: ',ft
            sys.exit()
            
    stms=mf.uniq(stms)
    
    for stm in stms:
        
        np=len(ftcs[stm])
        if(np == 1):
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)
            
    
    for stm in stms:

        np=len(ftcs[stm])-1

        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dtautracker+1
            sdtg=fsdtg
            tau=ftau+dtautracker
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dtautracker)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dtautracker
                



    return(ftcs,ftcstruct)


def NoLoadFtCards(dtg,tcs,dtautracker):

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
        ft=(0,dtg,dtg,dtg,91.9,911.9,'CC')
        ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dtautracker+1
            sdtg=fsdtg
            tau=ftau+dtautracker
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dtautracker)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                alat=91.9
                alon=911.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dtautracker
                



    return(ftcs)


def NoShowFtCards(dtg,tcs,dtautracker):

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
        ft=(0,dtg,dtg,dtg,95.9,955.9,'CC')
        ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dtautracker+1
            sdtg=fsdtg
            tau=ftau+dtautracker
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dtautracker)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                alat=95.9
                alon=955.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dtautracker

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
            npall=taumax/dTau12+1
            sdtg=fsdtg
            tau=ftau+dTau12
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dTau12)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dTau12
                

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
    
#--------------------------------------------------
#
#  load w2 adecks into dic
#
#--------------------------------------------------

def LoadW2TcFcCards(stmopt,year,phr,imodel,amodel,verb=0):

    ftmfcards=None
    ftcards=None
    
    ftdir=TC.AdeckDirW2
    ftype='adeck'

    ftmask='%s/%s/w2.adeck.%s.%s.*'%(ftdir,year,imodel,stmopt)
    if(verb): print 'W2 ADECK ftmask: ',ftmask
    ftpaths=glob.glob(ftmask)
    
    if(verb):
        print 'adeck data for : ',imodel,' ftpaths: ',ftpaths
        for ftpath in ftpaths:
            print 'ffff ',ftpath

    ftcards=[]    
    for ftpath in ftpaths:
        (d,f)=os.path.split(ftpath)
        cards=open(ftpath).readlines()
        for card in cards:
            ftcards.append(card)

    aftcards={}
    
    tamodel="%s%02d"%(amodel,int(phr))
    for ftcard in ftcards:
        tt=ftcard.split(',')
        dtg=tt[2].strip()
        iamodel=tt[4].strip()
        if(iamodel == tamodel):
            try:
                aftcards[dtg].append(ftcard)
            except:
                aftcards[dtg]=[]
                aftcards[dtg].append(ftcard)

    return(aftcards)

        

def ParseVdeck2Fcs(cards):
    
    fcs={}
    dtgs=[]
    
    for card in cards:
        tt=card.split()
        tau=int(tt[1])
        bdtg=tt[3]
        
        bdir=float(tt[21])
        bspd=float(tt[22])
        
        blat=float(tt[24])
        blon=float(tt[25])
        
        fvmax=float(tt[38])
        flat=float(tt[33])
        flon=float(tt[34])

        cqlat=float(tt[27])
        cqlon=float(tt[28])

        if(tau == 0):
            fcs[bdtg,'mot']=[bdir,bspd]
            fcs[bdtg,'bt']=[blat,blon]
            fcs[bdtg,'cq']=[cqlat,cqlon]
        fcs[bdtg,tau]=[flat,flon,fvmax]
        
        dtgs.append(bdtg)

    dtgs=mf.uniq(dtgs)

    return(dtgs,fcs)

# 0   1     2         3          4        5     6     7  8  9 10 11 12   13  14  15     16   17    18    19 
#ofc 000 12L.2005 2005082318 2005082318 FLG: BTC_Fee TC TD CQ WN CQ WN  TDO: SRS FE:    8.2  LF:  0.03  0.03
#
# 20     21     22  23    24     25  26    27     28  29    30    31   32    33    34   35    36  37    38 
#Bmot:   75.4  11.9 BP:  28.3  317.8 CP: -99.9 -999.9 WP: -99.9 -999.9 FP:  91.9  911.9 BW:  35.0 FW: -88.8
#
#39     40  41    42   43    44      45    46     47     48    49  50   51          52      53
#CW: -999.0 WW: -999.0 FS: -888.8  -88.8 -888.8  -88.8 -888.8  CT: CC CT_AT(nm):  9999.9  9999.9
#
# 54    55  56    57   58   59   60   61   62
#BVd: -999 FVd: -999 -999 -999 -999 -999 -999


def TrackBtBiasCorr(itrk,taus,bdir,bspd,verb=0):

    otrk=copy.deepcopy(itrk)
                   
    #
    # find fc taus
    #
    
    ftaus=[]

    for tau in taus:
        flat=otrk[tau][0]
        if(flat > -90.0 and flat < 88.0):
            ftaus.append(tau)

    #
    # check for noshow/noload
    #
    ntaus=len(ftaus)
    if(ntaus == 0 or ntaus == 1): return(otrk)

    #
    # save target taus and replace input taus with forecast taus
    #
    
    itaus=taus
    taus=ftaus
    
    ntau=len(taus)
    etau=taus[ntau-1]

    #
    # check if 36-h fc; if not the set to 24 and then 12 ... because # taus handled below
    #

    if(etau >= 36):
        taubc=36
    elif(etau == 24):
        taubc=24
    elif(etau == 12):
        taubc=12

    if(verb): print 'EEEEEEEEEEE etau: ',etau

    
    try:
        tau00=taus[0]
        flat00=otrk[0][0]
        flon00=otrk[0][1]
        flat36=otrk[taubc][0]
        flon36=otrk[taubc][1]
        (fdir36,fspd36,fiumot36,fivmot36)=TC.rumhdsp(flat00,flon00,flat36,flon36,36)
    except:
        fspd36=-99.9


    if(fspd36 > 0.0 and verb):
        print '36  ',flat00,flon00,flat36,flon36
        print '36  ',fdir36,fspd36
        
            
    bc12hr=0
    bc24hr=0

    i=0
    while(i< ntau):
        tau0=taus[i]
        flat0=otrk[tau0][0]
        flon0=otrk[tau0][1]
        i=i+1
        if(i == ntau): break

    
    i=0
    while(i< ntau):

        tau0=taus[i]
        tau1=taus[i+1]

        if(tau0 == etau):
            tau0=taus[i-1]
            tau1=taus[i]
            
        dtau=tau1-tau0
        
        flat0=otrk[tau0][0]
        flon0=otrk[tau0][1]
        fvmax0=otrk[tau0][2]

        flat1=otrk[tau1][0]
        flon1=otrk[tau1][1]
        fvmax1=otrk[tau1][2]


        (fdir,fspd,fiumot,fivmot)=TC.rumhdsp(flat0,flon0,flat1,flon1,dtau)
        
        if(verb):
            print
            print '--- ',i,tau0,tau1,dtau,fspd36
            print '000 ',flat0,flon0,fvmax0
            print '111 ',flat1,flon1,fvmax1
            print 'bc: ',bdir,bspd,' fc: ',fdir,fspd,fiumot,fivmot

        if(fspd36 > 0.0 and tau1 <= 24):
            dtau36=tau1-tau00
            (flat36bc,flon36bc)=TC.rumltlg(fdir36,fspd36,dtau36,flat00,flon00)

            if(tau1 == 12):
                perwght12=0.67
                (flatbt,flonbt)=TC.rumltlg(bdir,bspd,dtau,flat00,flon00)
                flat1bc=flat36bc*(1.0-perwght12) + flatbt*perwght12
                flon1bc=flon36bc*(1.0-perwght12) + flonbt*perwght12
                otrk[tau1][0]=flat1bc
                otrk[tau1][1]=flon1bc
                bc12hr=1

            if(tau1 == 24):
                perwght24=0.50
                (flatbt,flonbt)=TC.rumltlg(fdir,fspd,dtau,flat0,flon0)
                flat1bc=flat36bc*(1.0-perwght24) + flatbt*perwght24
                flon1bc=flon36bc*(1.0-perwght24) + flonbt*perwght24
                otrk[tau1][0]=flat1bc
                otrk[tau1][1]=flon1bc
                bc24hr=1

        else:
            flat36bc=-99.9
            flon36bc=-999.9
            flatbt=-99.9
            flonbt=-999.9
            dtau36=-99.9

        if(flat36bc > -90 and verb):
            print 'b36 -- ',flat36bc,flon36bc,dtau36
            print 'b36 bt ',flatbt,flonbt,dtau,flat00,flon00
            
            
        (rlat1,rlon1)=TC.rumltlg(fdir,fspd,dtau,flat0,flon0)
        if(verb): print 'LLL ',rlat1,rlon1,fvmax1,flat1bc,flon1bc

        i=i+1

        if(i == ntau-1): break

    if(verb):
        i=0
        while(i< ntau):
            tau0=taus[i]
            olat0=otrk[tau0][0]
            olon0=otrk[tau0][1]
            ilat0=itrk[tau0][0]
            ilon0=itrk[tau0][1]
            print "AAA-------- %03i in: %5.1f %6.1f  out: %5.1f %6.1f"%(tau0,ilat0,ilon0,olat0,olon0)
            i=i+1
            if(i == ntau): break


    return(otrk)

#--------------------------------------------------
#
#  track extrap using motion
#
#--------------------------------------------------

def TrackBtCqExtrap(itrk,taus,blat,blon,cqlat,cqlon,verb=0):

    otrk=copy.deepcopy(itrk)
                   
    #
    # find fc taus
    #
    
    ftaus=[]

    for tau in taus:
        flat=otrk[tau][0]
        if(flat > -90.0 and flat < 88.0 ):
            ftaus.append(tau)

    #
    # check for noshow/noload
    #
    ntaus=len(ftaus)
    if(ntaus == 0 or ntaus == 1): return(otrk)

    #
    # save target taus and replace input taus with forecast taus
    #
    
    taus=ftaus
    
    ntau=len(taus)
    etau=taus[ntau-1]

    
    i=0
    while(i< ntau):

        tau0=taus[i]
        tau1=taus[i+1]

        if(tau0 == etau):
            tau0=taus[i-1]
            tau1=taus[i]


            
        dtau=tau1-tau0
        
        flat0=itrk[tau0][0]
        flon0=itrk[tau0][1]
        fvmax0=itrk[tau0][2]

        flat1=itrk[tau1][0]
        flon1=itrk[tau1][1]
        fvmax1=itrk[tau1][2]

        (fdir,fspd,fiumot,fivmot)=TC.rumhdsp(flat0,flon0,flat1,flon1,dtau)

        if(tau0 == 0):
            
            if(cqlat > -90.0 and cqlat < 88.0):
                otrk[tau0][0]=cqlat
                otrk[tau0][1]=cqlon
            else:
                otrk[tau0][0]=blat
                otrk[tau0][1]=blon
                
            otrk[tau0][2]=fvmax0
            
        eflat0=otrk[tau0][0]
        eflon0=otrk[tau0][1]

        (eflat1,eflon1)=TC.rumltlg(fdir,fspd,dtau,eflat0,eflon0)
                
        otrk[tau1][0]=eflat1
        otrk[tau1][1]=eflon1
        
        
        if(verb):
            print
            print '--- ',i,tau0,tau1,dtau
            print '000 ',flat0,flon0
            print '111 ',eflat1,eflon1
            print 'fc: ',fdir,fspd,fiumot,fivmot

        i=i+1

        if(i == ntau-1): break

    if(verb):
        i=0
        while(i< ntau):
            tau0=taus[i]
            olat0=otrk[tau0][0]
            olon0=otrk[tau0][1]
            ilat0=itrk[tau0][0]
            ilon0=itrk[tau0][1]
            print "AAA-------- %03i in: %5.1f %6.1f  out: %5.1f %6.1f"%(tau0,ilat0,ilon0,olat0,olon0)
            i=i+1
            if(i == ntau): break


    return(otrk)



def MakeAdeckCards(model,ostmid,dtg,fctrk,phr='',verb=0):

    taus=fctrk.keys()
    taus.sort()
    
    stmnum=ostmid[0:2]
    basin1=ostmid[2:3]
    basin2=TC.Basin1toBasin2[basin1]
    adeckname=TC.ModelNametoAdeckName[model]
    adecknum=TC.ModelNametoAdeckNum[model]

    if(phr != ''): adeckname=adeckname+phr
    
    r34ne=r34se=r34sw=r34nw=0
    adum=0

    acards=[]
    
    for tau in taus:

        itau=int(tau)
        (lat,lon,vmax)=fctrk[tau]

        if(lat < -90.0 or lat > 88.0): continue

        ivmax=int(vmax)
        ipmin=0

        (clat,clon,ilat,ilon,hemns,hemew)=TC.Rlatlon2Clatlon(lat,lon)

        adextra=''
        if(len(adeckname) == 4): adextra='  '
        acard0="%2s, %2s, %10s, %2s, %4s, %s%3d,"%(basin2,stmnum,dtg,adecknum,adeckname,adextra,itau)

        acard1=" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

        acard=acard0+acard1
        if(verb): print acard
        acards.append(acard)

    return(acards)


def PrintInOutTrk(taus,itrk,otrk):
    ntaus=len(taus)
    i=0
    while(i< ntaus):
        tau0=taus[i]
        olat0=otrk[tau0][0]
        olon0=otrk[tau0][1]
        ilat0=itrk[tau0][0]
        ilon0=itrk[tau0][1]
        print "AAA-------- %03i in: %5.1f %6.1f  out: %5.1f %6.1f"%(tau0,ilat0,ilon0,olat0,olon0)
        i=i+1
        if(i == ntaus): break

    return
