import os,sys,posix,glob

import mf
import ncep

# ------- 20070823 -- cut over to new snap drive 
HwrfBaseInDat='/storage2/nwp2/ncep/hwrf'
HwrfBaseInDat='/storage3/nwp2/ncep/hwrf'

HwrfBaseOutDat='/storage/dat/hwrf/OUTDAT'
HwrfBaseFlddb='/storage2/nwp2/ncep/FLDDB'
HwrfBaseFlddb='/storage3/nwp2/ncep/FLDDB'

GfdlBaseInDat='/storage2/nwp2/ncep/gfdl'
GfdlBaseInDat='/storage3/nwp2/ncep/gfdl'

dlatParent=0.5
dlonParent=0.5
dlatNest=0.1
dlonNest=0.1


HwrfType='COUPLED_FCST'

def ChkHgrid(hgrid):
    hmask=''
    hrun=HwrfType

    if(mf.find(hgrid.lower(),'ne')):
        hgrid='NEST'
    elif(mf.find(hgrid.lower(),'par')):
        hgrid='PARENT'
    elif(mf.find(hgrid.lower(),'vit')):
        hrun='ATMOS'
        hgrid=''
        hmask="tcvitals*"
    elif(mf.find(hgrid.lower(),'trk')):
        hgrid='COMBINE'
        hmask="*atcf*"
    elif(mf.find(hgrid.lower(),'cou')):
        hgrid='COUPLED'
    else:
        print 'EEE invalid hgrid: ',hgrid
        sys.exit()

    return(hgrid,hmask,hrun)



def GetHwrfPaths(stmid,dtg,htype,hgrid,tau,
                 dofdb=1,override=0):

    datdir="%s/hwrf.%s"%(HwrfBaseInDat,dtg)
    fdbdir="%s/hwrf.%s"%(HwrfBaseFlddb,dtg)
    outdir=datdir
    
    if(mf.ChkDir(datdir) == 0):
        print 'EEEEEEEEEEEEE hwrf dat dir not there... '
        sys.exit()

    if(mf.ChkDir(fdbdir,'mkdir') == 0):
        print 'EEEEEEEEEEEEE unable to mkdir flddb path... '
        sys.exit()

    if(mf.ChkDir(outdir,'mkdir') == 0):
        print 'EEEEEEEEEEEEE unable to mkdir out dat path... '
        sys.exit()
        

    if(htype == 'grb2'):
        hbase='hwrfprs'
        gbase='grb2'
        
    elif(htype == 'egrd'):
        hbase='hwrfeprs'
        gbase='grb'


    mask="%s/*%s.%s.%s_%s*%sf%02d"%(datdir,stmid,dtg,hbase,hgrid,gbase,tau)
    print 'mmm ',mask
        
    tt=glob.glob(mask)

    if(len(tt) == 1):
        datpath=tt[0]
        igoutpath=datpath
        (dir,file)=os.path.split(datpath)
        (obase,ext)=os.path.splitext(file)
        fdbpath="%s/hwrf.%s.list.txt"%(fdbdir,obase)

    else:
        print 'EEE no data or two or more files for mask: ',mask


    datthere=mf.ChkPath(datpath)
    fdbthere=mf.ChkPath(fdbpath,pathopt='noexit')
    if(not(datthere)):
         print 'EEEEEEEEEEEE data NOT there: ',datpath
         sys.exit()

    elif(datthere and not(fdbthere)):
        print 'DDDDDDDDD there but fdb NOT...'
        if(dofdb):
            if(htype == 'grb2'):
                ncep.MakeFdb2(datpath,fdbpath)
            else:
                MakeFdb(datpath,fdbpath)
            

    elif(datthere and fdbthere):
        rc=open(fdbpath).readlines()
        if(len(rc) == 1):
            if(dofdb):
                if(htype == 'grb2'):
                    ncep.MakeFdb2(datpath,fdbpath)
                else:
                    MakeFdb(datpath,fdbpath)

        if(override):
                if(htype == 'grb2'):
                    ncep.MakeFdb2(datpath,fdbpath)
                else:
                    MakeFdb(datpath,fdbpath)


    if(htype == 'grb2'):
        (nx,ny,blat,elat,dlat,blon,elon,dlon,gridnum)=GetLatlonGrid(datpath,fdbpath,htype,hgrid)
        dlatgrid=int(dlat*100.0)

    if(hgrid == 'p'):

        if(htype == 'egrd'): dlatgrid=int(dlatParent*100.0)

        obase="%s.%s.%s.dx%03d.f%03d"%(stmid,dtg,hgrid,dlatgrid,tau)
        ogoutpath="%s/hwrf.%s.grb1"%(outdir,obase)
        noutpath="%s/hwrf.%s.gpk"%(outdir,obase)
        
    elif(hgrid == 'n'):

        if(htype == 'egrd'): dlatgrid=int(dlatNest*100.0)

        obase="%s.%s.%s.dx%03d.f%03d"%(stmid,dtg,hgrid,dlatgrid,tau)
        ogoutpath="%s/hwrf.%s.grb1"%(outdir,obase)
        noutpath="%s/hwrf.%s.gpk"%(outdir,obase)

    else:
        print 'EEE' ; sys.exit()
    


    return(datpath,fdbpath,
           igoutpath,ogoutpath,
           noutpath)

def GetLatlonGrid(datpath,fdbpath,htype,hgrid):

    #
    # use the combined grid used in the ncep post processor for track
    #


    if(htype == 'grb2'):

        cmd="wgrib2 -grid -d 1 %s"%(datpath)
        cards=os.popen(cmd).readlines()

        #
        # get the gds grid number
        #
        cmd="wgrib2 -Sec3 -d 1 %s"%(datpath)
        gcards=os.popen(cmd).readlines()

        gcard=gcards[0]
        tt=gcard.split()
        gridnum=int(tt[3].split('=')[1])
        
        
        #for card in cards:
        #    print card[:-1]

        card1=cards[1]
        if(mf.find(card1,'lat-lon grid')):
            nx=card1.split('(')[1].split(' ')[0]
            ny=card1.split('(')[1].split(' ')[2].split(')')[0]

            nx=int(nx.strip())
            ny=int(ny.strip())

        card2=cards[2]
        if(mf.find(card2,'lat')):
            tt=card2.split()
            lat1=float(tt[1])
            lat2=float(tt[3])
            dlat=float(tt[5])
                       
            if(lat1 > lat2):
                blat=lat2
                elat=lat1
            else:
                blat=lat1
                elat=lat2
                
                
        card3=cards[3]
        if(mf.find(card3,'lon')):
            tt=card3.split()
            lon1=float(tt[1])
            lon2=float(tt[3])
            dlon=float(tt[5])

            #
            # shift to deg W (deg)
            #
        
            if(lon1 > lon2):
                blon=lon2
                elon=lon1
            else:
                blon=lon1
                elon=lon2
                
            if(blon > 180.0):
                
                blon=blon-360.0
                elon=elon-360.0
                
                

    else:
        cards=GetFdb(fdbpath)
        (records,recsiz,nrectot)=ParseFdb(cards)

        grid=None
    
        (
            sizrecp1,
            gridnum,
            nx,
            ny,
            nxny,
            ndef,
            nundef,
            blat,
            elat,
            dlat,
            blon,
            elon,
            dlon,
            timecode,
            timedesc,
            timerangeind,
            timerangep1,
            timerangep2,
            timeunits,
            tau,
            varcode,
            var,
            vardesc,
            levcode,
            lev,
            levcode2,
            levdesc,
            gridvalmin,
            gridvalmax,
            nbits,
            bdsref,
            decscale,
            binscale
            )=records[1]


    grid=[nx,ny,blat,elat,dlat,blon,elon,dlon,gridnum]

    return(grid)


def nearestinc(input,dinc):
    out=mf.nint(input/dinc)*dinc
    out=float(out)
    return(out)
              

    

def ReduceLatlonGrid(grid,hgrid):

    (nx,ny,blat,elat,dlat,blon,elon,dlon)=grid
    
    dinc=5.0
    latlen=blat-elat
    clat=elat+latlen*0.5

    
    lonlen=elon-blon
    clon=blon+lonlen*0.5


    rclat=nearestinc(clat,dinc)
    rclon=nearestinc(clon,dinc)

    print 'qqqqqq ',clat,clon,rclat,rclon
    print 'qqqqqq ',latlen,lonlen


    SlatborderNest=10.0
    NlatborderNest=25.0
    ElonborderNest=15.0
    WlonborderNest=35.0

    if(mf.find(hgrid.lower(),'nest')):

        rblat=rclat-SlatborderNest
        relat=rclat+NlatborderNest
        rblon=rclon-WlonborderNest
        relon=rclon+ElonborderNest
        rdlat=dlatNest
        rdlon=dlonNest



    elif(mf.find(hgrid.lower(),'par')):

        #
        # ncep grib N->S so blat = elat
        #
        rblat=nearestinc(elat,dinc)
        relat=nearestinc(blat,dinc)

        print 'pppp ',elat,blat
        print 'pppp ',rblat,relat
        if(elat < rblat):
            rblat=rblat-dinc
        if(blat > relat):
            relat=relat+dinc

        rblon=nearestinc(blon,dinc)
        relon=nearestinc(elon,dinc)
        
        if(blon < rblon):
            rblon=rblon+dinc
        if(elon > relon):
            relon=relon+dinc
            
        rdlat=dlatParent
        rdlon=dlonParent

        print 'ppplll ',blon,elon
        print 'ppplll ',rblon,relon


    elif(mf.find(hgrid.lower(),'comb')):
        print 'qq'
        
    else:
        print 'EEEEE invalid hgrid: ',hgrid
        sys.exit()
        
    rny=int((relat-rblat)/rdlat)+1
    rnx=int((relon-rblon)/rdlon)+1

    #
    # sway the lats because in ncep grib N->S
    #
    rgrid=(rnx,rny,relat,rblat,rdlat,rblon,relon,rdlon)

    return(rgrid)
              
    


def ParseFdb(cards,verb=0):

    ncards=len(cards)

    recsiz={}
    records={}

    #
    # the first card has the data path
    #

    nc=1
    nrc=0
    while (nc < ncards):

        card=cards[nc]
        lcard=len(card)
        rcards=[]

        if(card[0:3] == 'rec'):

            while(lcard > 1):
                lcard=len(cards[nc])
                if(lcard > 1):
                    rcards.append(cards[nc])
                nc=nc+1

            #
            # initialize
            #
            nxny=0
            blat=blon=elat=elon=dlat=dlon=-999.9

            for n in range(0,len(rcards)):
                rcard=rcards[n]
                type=rcard.split()[0]

                if(type == 'rec'):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()

                    #    0         1                2            3       4
                    #['rec', '5:5513228:date', '2006091800', 'UGRD', 'kpds5=33',
                    #    5            6               7               8        9     10    11        12 
                    # 'kpds6=100', 'kpds7=850', 'levels=(3,82)', 'grid=255', '850', 'mb', 'anl:', 'bitmap:',
                    #    13       14
                    # '344664', 'undef']

                    ttt=tt[1].split(':')
                    nrec=int(ttt[0])
                    sizrecp1=int(ttt[1])

                    var=tt[3]
                    varcode=tt[4].split('=')[1]
                    levcode=tt[5].split('=')[1]
                    lev=tt[6].split('=')[1]
                    lev=int(lev)
                    levcode2=tt[7].split('=')[1]

                    nbitmap=0
                    nre=len(tt)


                    if(nre >=14):
                        if(tt[nre-3] == 'bitmap:'):
                            nbitmap=int(tt[nre-2])
                            timecode=tt[nre-4].split(':')[0]
                            timedesc=tt[nre-5]
                        else:
                            timecode=tt[nre-1].split(':')[0]
                            timedesc=tt[nre-2]

                    else:
                        timecode=tt[nre-1].split(':')[0]
                        timedesc=tt[nre-2]


                    nb=0
                    for n in range(0,nre):
                        if(mf.find(tt[n],'grid=')):
                            nb=n
                            gridnum=int(tt[nb].split('=')[1])
                            break

                    ne=0
                    for n in range(nb,nre):
                        if(mf.find(tt[n],':')):
                            ne=n
                            break

                    if(timecode != 'anl'):
                        ne=ne-1
                    else:
                        timedesc=0

                    levdesc=''
                    for n in range(nb+1,ne):
                        levdesc=levdesc+' '+tt[n]

                    if(timecode == 'anl'):
                        time=0

                elif(mf.find(type,'=')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split('=')
                    vardesc=tt[1]

                elif(mf.find(type,'timerange')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    timerangeind=int(tt[1])
                    timerangep1=int(tt[3])
                    timerangep2=int(tt[5])
                    timeunits=int(tt[7])
                    nx=int(tt[9])
                    ny=int(tt[11])
                    gridnum=int(tt[14])

                elif(mf.find(type,'center')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    centernum=int(tt[1])
                    subcenternum=int(tt[3])
                    processnum=int(tt[5])
                    gribtablenum=int(tt[7])


#  LRGHR=Large scale condensation heating [K/s]
#  timerange 3 P1 0 P2 0 TimeU 1  nx 215 ny 431 GDS grid 203 num_in_ave 0 missing 0
#  center 7 subcenter 0 process 89 Table 2 scan: WE:SN winds(grid) 
#  Semi-staggered Arakawa E-Grid (2D): lat0 -25.893000 lon0 -156.703000 nxny 92665
#    dLat 0.180000 dLon 0.180000 (tlm0d -123.813000 tph0d 15.700000) scan 64 mode 136
#  min/max data 0 0  num bits 0  BDS_Ref 0  DecScale 0 BinScale 0

                elif(mf.find(rcard,'Semi-staggered Arakawa E-Grid')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    blat=float(tt[5])
                    blon=float(tt[7])
                    nxny=int(tt[9])

                elif(mf.find(type,'long')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    blon=float(tt[1])
                    elon=float(tt[3])
                    dlon=float(tt[5].split(',')[0])

                elif(mf.find(rcard,'tlm0d')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    dlat=float(tt[1])
                    dlon=float(tt[3])
                    elat=blat+nx*dlon
                    elon=blon+nx*dlon

                elif(mf.find(type,'min/max')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    gridvalmin=float(tt[2])
                    gridvalmax=float(tt[3])
                    nbits=int(tt[6])
                    bdsref=float(tt[8])
                    decscale=int(tt[10])
                    binscale=int(tt[12])




            if(nxny == 0 and nx != 0 and ny != 0): nxny=nx*ny
            ndef=nxny-nbitmap
            nundef=nxny-ndef

            tau=GribTime2Tau(timerangeind,timerangep1,timerangep2)

            rec=(
                sizrecp1,
                gridnum,
                nx,
                ny,
                nxny,
                ndef,
                nundef,
                blat,
                elat,
                dlat,
                blon,
                elon,
                dlon,
                timecode,
                timedesc,
                timerangeind,
                timerangep1,
                timerangep2,
                timeunits,
                tau,
                varcode,
                var,
                vardesc,
                levcode,
                lev,
                levcode2,
                levdesc,
                gridvalmin,
                gridvalmax,
                nbits,
                bdsref,
                decscale,
                binscale
                )

            records[nrec]=rec
            recsiz[nrec]=sizrecp1

            #hwrf.PrintWgribRecord(nrec,rec)

            nrectot=nrec

    return(records,recsiz,nrectot)









def MakeFdb(datpath,fdbpath,ropt=''):
    F=open(fdbpath,'w')
    F.writelines(datpath+'\n')
    F.close()

    cmd="wgrib -V %s >> %s"%(datpath,fdbpath)
    mf.runcmd(cmd,ropt)
    


def GetFdb(fdbpath):
    F=open(fdbpath)
    cards=F.readlines()
    F.close()
    return(cards)


def GetSizDataFile(datpath):
    dsiz=os.path.getsize(datpath)
    return(dsiz)



def GribTime2Tau(timerangeind,timerangep1,timerangep2):
    #
    # instantaneous
    #
    if(timerangeind == 0):
        tau=timerangep1
    #
    # accumulated - put tau at end of interval
    #
    elif(timerangeind == 4):
        tau=timerangep2
    #
    # average - put tau at end of interval
    #
    elif(timerangeind == 3):
        tau=timerangep2
    #
    # valid time occupies p1 and p2
    #
    elif(timerangeind == 10):
        tau=timerangep1*256*256+timerangep2
    #
    # valid time between p1 and p2 set to p2
    #
    elif(timerangeind == 2):
        tau=timerangep2

    #
    # if not one of these return none
    #
    else:
        print 'NNNNNNNNNNNNNNNNNNN ',timerangeind,timerangep1,timerangep2
        tau=None

    return(tau)


def PrintWgribRecord(nrec,rec):


    (
        sizrecp1,
        gridnum,
        nx,
        ny,
        nxny,
        ndef,
        nundef,
        blat,
        elat,
        dlat,
        blon,
        elon,
        dlon,
        timecode,
        timedesc,
        timerangeind,
        timerangep1,
        timerangep2,
        timeunits,
        tau,
        varcode,
        var,
        vardesc,
        levcode,
        lev,
        levcode2,
        levdesc,
        gridvalmin,
        gridvalmax,
        nbits,
        bdsref,
        decscale,
        binscale
        )=rec
    
    
    print
    print 'FFF Record: '
    print '         nrec: ',nrec
    print '     sizrecp1: ',sizrecp1
    print
    print 'FFF Grid: '
    print '      gridnum: ',gridnum
    print '           nx: ',nx
    print '           ny: ',ny
    print '         nxny: ',nxny
    print '         ndef: ',ndef
    print '       nundef: ',nundef
    print
    print '         blat: ',blat
    print '         elat: ',elat
    print '         dlat: ',dlat
    print 
    print '         blon: ',blon
    print '         elon: ',elon
    print '         dlon: ',dlon
    print
    print 'FFF Time: '
    print '     timecode: ',timecode
    print '     timedesc: ',timedesc
    print ' timerangeind: ',timerangeind
    print '  timerangep1: ',timerangep1
    print '  timerangep2: ',timerangep2
    print '    timeunits: ',timeunits
    print '          tau: ',tau
    print
    print 'FFF Var: '
    print '      varcode: ',varcode
    print '          var: ',var
    print '      vardesc: ',vardesc
    print
    print 'FFF Level: '
    print '      levcode: ',levcode
    print '          lev: ',lev
    print '     levcode2: ',levcode2
    print '      levdesc: ',levdesc
    print
    print 'FFF Grid Values: '
    print '   gridvalmin: ',gridvalmin
    print '   gridvalmax: ',gridvalmax
    print
    finalcard="%-8s %s  %-8s  %-10s  %-16s"%(var,vardesc[0:-1],timecode,timedesc,levdesc)
    #finalcard=var,vardesc,timecode,timedesc,levdesc
    #finalcard="%s | %s | %s | "%(var,timecode,levdesc)


    print 'FFF GRIB packing: '
    print '        nbits: ',nbits
    print '       bdsref: ',finalcard,bdsref,gridvalmin,nbits,decscale,binscale
    print '     decscale: ',decscale
    print '     binscale: ',binscale


def WgribVarAnal(records):

    nr=len(records)

    vars=[]
    taus=[]
    levs=[]
    
    vardescs={}
    varlevs={}

    for n in range(1,nr+1):
        
        (
            sizrecp1,
            gridnum,
            nx,
            ny,
            nxny,
            ndef,
            nundef,
            blat,
            elat,
            dlat,
            blon,
            elon,
            dlon,
            timecode,
            timedesc,
            timerangeind,
            timerangep1,
            timerangep2,
            timeunits,
            tau,
            varcode,
            var,
            vardesc,
            levcode,
            lev,
            levcode2,
            levdesc,
            gridvalmin,
            gridvalmax,
            nbits,
            bdsref,
            decscale,
            binscale
            )=records[n]

        var=var.lower()
        vars.append(var)
        taus.append(tau)
        levs.append(lev)

        
        try:
            varlevs[lev,tau].append(var)
        except:
            varlevs[lev,tau]=[var]

        try:
            vardescs[var,tau].append(vardesc)
        except:
            vardescs[var,tau]=[]
            vardescs[var,tau].append(vardesc)

    vars=mf.uniq(vars)
    taus=mf.uniq(taus)
    levs=mf.uniq(levs)
    levs.sort()

    for tau in taus:
        for lev in levs:
            vcard="%-5d "%(lev)
            try:
                lvars=varlevs[lev,tau]
                lvars.sort()
                for lvar in lvars:
                    vcard="%s %-6s"%(vcard,lvar)
            except:
                vcard=vcard

            print vcard

        print
        print "Var desc:"
        print
        vars.sort()
        for var in vars:
            vv=vardescs[var,tau]
            vv=mf.uniq(vv)
            print "%-6s   %s"%(var,vv[0][:-1])


def WgribVarFilter(records,request):

    nr=len(records)

    rtaus=request['taus']
    rtaus.sort()
    rvars=request.keys()
    rvars.sort()

    print 'rrrrrrrrrrrrrr ',rvars
    print 'rrrrrrrrrrrrrr ',rtaus 

    
    orecs=[]

    nrecs=records.keys()
    nrecs.sort()
    
    for nrec in nrecs:
        
        (
            sizrecp1,
            gridnum,
            nx,
            ny,
            nxny,
            ndef,
            nundef,
            blat,
            elat,
            dlat,
            blon,
            elon,
            dlon,
            timecode,
            timedesc,
            timerangeind,
            timerangep1,
            timerangep2,
            timeunits,
            tau,
            varcode,
            var,
            vardesc,
            levcode,
            lev,
            levcode2,
            levdesc,
            gridvalmin,
            gridvalmax,
            nbits,
            bdsref,
            decscale,
            binscale
            )=records[nrec]

        var=var.lower()


        for rvar in rvars:
            if(var == rvar):
                rlevs=request[rvar]
                
                for rlev in rlevs:
                    slev=rlev.split('.')
                    reqlev=slev[0]
                    reqlevcode=slev[1]

                    #print 'lllllllllllllllll ',lev,reqlev,' rrrrrrrrrrrrrrrrrrrrr',levcode,reqlevcode
                    if(int(lev) == int(reqlev) and int(levcode) == int(reqlevcode)):
                        for rtau in rtaus:
                            if(rtau == tau):
                                print 'MMMMMMMMMMMMM ',	var,lev,nrec,sizrecp1,' LLL ',lev,levcode
                                ocard="%d:%d"%(nrec,sizrecp1)
                                ocard=ocard+'\n'
                                orecs.append(ocard)


    return(orecs)


def WgribFilter(orecs,inpath,outpath):

    wcmd="wgrib -i -grib -s %s -o %s"%(inpath,outpath)
    w=os.popen(wcmd,'w')
    w.writelines(orecs)
    w.close()


def CopygbHwrf2Latlon(grid,inpath,outpath,ropt='norun'):

    nlpath='nlcopygbhwrf'

    [nx,ny,blat,elat,dlat,blon,elon,dlon,gridnum]=grid

    dlatc=int(dlat*1000.0)
    dlonc=int(dlon*1000.0)
    blatc=int(blat*1000.0)
    elatc=int(elat*1000.0)
    blonc=int(blon*1000.0)
    elonc=int(elon*1000.0)

    gridopt="\"255 0 %d %d %d %d %d %d %d %d %d 0\""%(nx,ny,blatc,blonc,gridnum,elatc,elonc,dlonc,dlatc)
    cmd="time copygb.x -N %s -g%s -x %s %s"%(nlpath,gridopt,inpath,outpath)
    
    mf.runcmd(cmd,ropt)


def NagribLatlon2Gempak(grid,inpath,outpath,curdir):

    ropt='norun'
    ropt=''

    [nx,ny,blat,elat,dlat,blon,elon,dlon]=grid

    (idir,ifile)=os.path.split(inpath)
    (odir,ofile)=os.path.split(outpath)

    blonn=blon
    elonn=elon
    #if(blonn > 180.0): blonn=blonn-360.0
    #if(elonn > 180.0): elonn=elonn-360.0
    
    garea="%6.1f;%6.1f;%6.1f;%6.1f"%(elat,blonn,blat,elonn)
    grdarea="%6.1f;%6.1f;%6.1f;%6.1f"%(elat,blon,blat,elon)

    ngarea=''
    for char in garea:
        if(char != ' '): ngarea=ngarea+char

    ngrdarea=''
    for char in grdarea:
        if(char != ' '): ngrdarea=ngrdarea+char


    kxky="#%4.2f;%4.2f"%(dlon,dlat)

    nkxky=''
    for char in kxky:
        if(char != ' '): nkxky=nkxky+char


    os.chdir(idir)
    
    ngs="""CPYFIL  = gds
MAXGRD  = 3999
PROJ    = ced
OUTPUT  = T
GBFILE  = %s
GAREA   = %s
GRDAREA = %s
GBTBLS  =  
GBDIAG  =  
PDSEXT  = NO
OVERWR  = YES
KXKY    = %s
GDOUTF  = %s

run
"""%(ifile,ngarea,ngrdarea,nkxky,ofile)

    #
    # blow away previous file, gets gempak confused...
    #
    if(os.path.exists(ofile)): posix.unlink(ofile)
    
    if(ropt == ''):
        ncmd="time nagrib"
        n=os.popen(ncmd,'w')
        n.writelines(ngs)
        n.close()

        n=os.system('gpend')
        
    os.chdir(curdir)
    

    
def SetFieldRequest(hgrid,tau,spec='test0'):

    request={}

    if(spec == 'test0'):
        
        request['ugrd']=[10,850,700,500]
        request['vgrd']=request['ugrd']
    
        request['hgt']=[10,850,700,500]
    
        request['prmsl']=[0]
        request['apcp']=[0]
        request['acpcp']=[0]

    else:
        
        request['ugrd']=[10,850,500,200]
        request['vgrd']=request['ugrd']
    
        request['tmp']=[850,500,200]
        request['rh']=request['tmp']
        request['hgt']=request['tmp']
    
        request['prmsl']=[0]
        request['apcp']=[0]
        request['acpcp']=[0]
    
    request['taus']=[tau]

    return(request)

