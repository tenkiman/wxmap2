import os,sys,posix

import mf
import w2


(NcepBaseInDat,NcepBaseOutDat,NcepBaseFlddb,NcepFldLiveBase)=w2.GetNcepBaseInOutDat()

def GetNcepPaths(dtg,model,tau,prcopt,
                 dofdb=1,override=0):

    verbdirchk=0
    verbdir1chk=0
    if(prcopt == 'g21'):
        verbdirchk=0
        verbdir1chk=1

    yymmdd=dtg[0:8]
    hh=dtg[8:10]

    og1ext='grb1'
    og2ext='grb2'
    
    if(model == 'gfs2'):

        imodel='gfs'
        datdir="%s/%s/prod/%s.%s"%(NcepBaseInDat,imodel,imodel,yymmdd)
        fdbdir="%s/%s/prod/%s.%s"%(NcepBaseFlddb,imodel,imodel,yymmdd)
        outdir2="%s/%s/prod/%s.%s"%(NcepBaseOutDat,imodel,imodel,yymmdd)
        outdir1="%s/ncep/gfs2/%s"%(NcepFldLiveBase,dtg)
        
        datpath="%s/gfs.t%sz.pgrb2f%02d"%(datdir,hh,tau)
        fdbpath="%s/gfs.t%sz.pgrb2f%02d.list.txt"%(fdbdir,hh,tau)
        g2outpath="%s/%s.%s.f%03d.%s"%(outdir2,model,dtg,tau,og2ext)
        g1outpath="%s/%s.%s.f%03d.%s"%(outdir1,model,dtg,tau,og1ext)
        g1ctlpath="%s/%s.%s.ctl"%(outdir1,model,dtg)


    else:
        print 'EEE invalid model: ',model

    dirdat=1
    if(mf.ChkDir(datdir,'quiet') == 0):
        if(verbdirchk): print "WWW datdir: ',datdir,' for model: %s  dtg: %s  tau: %s not there... "%(model,dtg,tau)
        dirdat=0
    else:
        datthere=mf.ChkPath(datpath,pathopt='noexit')


        
    dirfdb=1
    if(mf.ChkDir(fdbdir,'mkdir') == 0):
        print 'WWW unable to mkdir flddb path: ',fdbdir
        dirfdb=0
        sys.exit()
    else:
        fdbthere=mf.ChkPath(fdbpath,pathopt='noexit',verb=verbdirchk)

    dirout2=1
    if(mf.ChkDir(outdir2,'mkdir') == 0):
        print 'WWW unable to mkdir outdir2: ',outdir2
        dirout2=0
    else:
        g2outthere=mf.ChkPath(g2outpath,pathopt='noexit',verb=verbdirchk)

    dirout1=1
    if(mf.ChkDir(outdir1,'mkdir') == 0):
        print 'WWW unable to mkdir outdir1: ',outdir1
        dirout1=0
    else:
        g1outthere=mf.ChkPath(g1outpath,pathopt='noexit',verb=verbdir1chk)


    status=1

    if(mf.find(prcopt,'g21')):
        
        status=4
        
        if(dirout2 == 0):
            print 'EEE: do outdir2: ',outdir2
            sys.exit()
            
        if(g2outthere and dirout1):
            print 'III -- grb2 data there: ',g2outpath,' and dirout1 there ',dirout1
            status=2

        if(g1outthere and dirout1):
            print 'III -- grb1 data there: ',g1outpath,' and dirout1 there ',dirout1
            status=5
    
    elif(prcopt == 'dat' and g2outthere and not(override) ):
        status=3
    
    else:

        if(not(datthere)):
            print 'WWW -- no data: ',datpath
            status=-1

        elif(datthere and not(fdbthere)):
            print 'DDDDDDDDD there but fdb NOT...'
            if(dofdb):  MakeFdb2(datpath,fdbpath)

        elif(datthere and fdbthere):
            rc=open(fdbpath).readlines()
            if(len(rc) == 1):
                if(dofdb): MakeFdb2(datpath,fdbpath)

            if(override): MakeFdb2(datpath,fdbpath)
            status=0


    return(datpath,fdbpath,g2outpath,g1outpath,g1ctlpath,status)



def GetLatlonGrid2(model):


    if(model == 'gfs2'):
        
        nx=720
        ny=361
        
        blat=-90.0
        elat=90.0
        dlat=0.5
    
        blon=0.0
        elon=359.5
        dlon=0.5
        
        scanlon='WE'
        scanlat='NS'

    else:

        print 'EEE invalid model for getlatlongrid2: ',model
        sys.exit()
        
    grid=[nx,ny,blat,elat,dlat,blon,elon,dlon]

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
    dlatNest=0.1
    dlonNest=0.1

    dlatParent=0.5
    dlonParent=0.5

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
                            gridcode=tt[nb].split('=')[1]
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


                elif(mf.find(type,'latlon')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    blat=float(tt[2])
                    elat=float(tt[4])
                    dlat=float(tt[6])
                    nxny=int(tt[8])

                elif(mf.find(type,'long')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    blon=float(tt[1])
                    elon=float(tt[3])
                    dlon=float(tt[5].split(',')[0])

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
                gridcode,
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




def MakeFdb2(datpath,fdbpath,ropt=''):

    F=open(fdbpath,'w')
    F.writelines(datpath+'\n')
    F.close()

    cmd="wgrib2 -v2 %s >> %s"%(datpath,fdbpath)
    mf.runcmd(cmd,ropt)
    

def MakeFdb(datpath,fdbpath,ropt=''):

    F=open(fdbpath,'w')
    F.writelines(datpath+'\n')
    F.close()

    cmd="wgrib -V %s >> %s"%(datpath,fdbpath)
    mf.runcmd(cmd,ropt)
    


def GetFdb2(fdbpath):
    F=open(fdbpath)
    cards=F.readlines()
    F.close()
    return(cards)


def GetSizDataFile2(datpath):
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
    # if not one of these return none
    #
    else:
        tau=None

    return(tau)


def PrintWgribRecord(nrec,rec):


    (
        sizrecp1,
        gridcode,
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
    print '     gridcode: ',gridcode
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
            gridcode,
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
            vardescs[var,tau]=[vardesc]


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
            gridcode,
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
                    if(lev == rlev):
                        for rtau in rtaus:
                            if(rtau == tau):
                                print 'MMMMMMMMMMMMM ',	var,lev,tau,nrec,sizrecp1
                                ocard="%d:%d"%(nrec,sizrecp1)
                                ocard=ocard+'\n'
                                orecs.append(ocard)


    return(orecs)


def WgribFilter(orecs,inpath,outpath):

    wcmd="wgrib -i -grib -s %s -o %s"%(inpath,outpath)
    w=os.popen(wcmd,'w')
    w.writelines(orecs)
    w.close()

def CopygbNcep2Latlon(grid,inpath,outpath,ropt=''):

    nlpath='nlcopygbhwrf'

    [nx,ny,blat,elat,dlat,blon,elon,dlon]=grid

    print dlat,dlon,blat,blon,elat,elon
    dlatc=int(dlat*1000.0)
    dlonc=int(dlon*1000.0)
    blatc=int(blat*1000.0)
    elatc=int(elat*1000.0)
    blonc=int(blon*1000.0)
    elonc=int(elon*1000.0)
    
    gridopt="\"255 0 %d %d %d %d 136 %d %d %d %d 0\""%(nx,ny,blatc,blonc,elatc,elonc,dlonc,dlatc)
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
    

    
def SetFieldRequest(tau,spec='test0'):

    request={}

    if(spec == 'test0'):
        
        request['ugrd']=[10,850,700,500]
        request['vgrd']=request['ugrd']
    
        request['hgt']=[10,850,700,500]
    
        request['prmsl']=[0]
        request['apcp']=[0]
        request['acpcp']=[0]
        request['cprat']=[0]
        request['prate']=[0]

    else:
        
        request['ugrd']=[10,850,500,200]
        request['vgrd']=request['ugrd']
    
        request['tmp']=[850,500,200]
        request['rh']=request['tmp']
        request['hgt']=request['tmp']
    
        request['prmsl']=[0]
        request['apcp']=[0]
        request['acpcp']=[0]
        request['cprat']=[0]
        request['prate']=[0]
    
    request['taus']=[tau]

    return(request)



#222222222222222222222222222222222222222222222222222222222222222222
#
#  2 versions
#
#222222222222222222222222222222222222222222222222222222222222222222

def LevCode2Lev(lc1,lv1,lc2,lv2):
    levc=None
    if(lc1== 100):
        ld='mb'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 1):
        request['apcp']=[0]
        request['acpcp']=[0]
        request['cprat']=[0]
        request['prate']=[0]
    
    request['taus']=[tau]

    return(request)



#222222222222222222222222222222222222222222222222222222222222222222
#
#  2 versions
#
#222222222222222222222222222222222222222222222222222222222222222222

def LevCode2Lev(lc1,lv1,lc2,lv2):
    levc=None
    if(lc1== 100):
        ld='mb'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 1):
        ld='surface'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 4):
        ld='OC istotherm'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 6):
        ld='max wind'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 7):
        ld='tropopause'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 8):
        ld='top of atmosphere'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 101):
        ld='mean sea level'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 102):
        ld='m above mean sea level'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 103):
        ld='m above ground'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 104):
        ld='sigma layer'
        lv=lv1
        levc="%d.%g-%g"%(lc1,lv1,lv2)
    elif(lc1== 106):
        ld='m below ground (layer)'
        lv=lv1
        levc="%d.%d-%-d"%(lc1,int(lv1*0.01),int(lv2*0.01))
    elif(lc1== 108 and lc2 == 108):
        ld='mb layer above ground (layer)'
        lv=lv1
        levc="%d.%d-%-d"%(lc1,int(lv1*0.01),int(lv2*0.01))
    elif(lc1== 109):
        ld='reserved'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 244):
        ld='depth of atmos'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 234):
        ld='high cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 224):
        ld='mid cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 214):
        ld='low cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 211):
        ld='total cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(
        lc1 == 242 or lc1 == 243 or
        lc1 == 232 or lc1 == 233 or
        lc1 == 222 or lc1 == 223 or
        lc1 == 212 or lc1 == 213 or
        lc1 == 200 or
        lc1 == 204
        ):
        ld='NCEP level type %d'%(lc1)
        lv=float(lc1)
        levc="%d.%g"%(lc1,lv1)
    else:
        ld=None
        lv=None
        print 'NNNN ',lc1,lv1,lc2,lv2
        
    return(lv,ld,levc)
        
    
def ParseFdb2(cards,verb=0):


    def splitlevcodes(lvl):
        tt=lvl.split('=')
        lll=tt[1].split(',')
        lc=int(lll[0][1:])
        if(lc == 109 or lc == 104 or lc == 106):
            ll=float(lll[1][:-1])
        elif(lc == 100):
            ll=float(lll[1][:-1])*0.01
        else:
            ll=float(lll[1][:-1])
        return(lc,ll)
        
        
    ncards=len(cards)

    recsiz={}
    records={}

    #
    # the first card has the data path
    #

    nrec=0
    nc=1
    for nr in range(nc,ncards):

        card=cards[nr]
        tt=card.split(':')

        recnum=tt[0]
        sizrecp1=int(tt[1])

##        ['1', '0', '00Z07jun2007', 'HGT Geopotential Height [gpm]', 'lvl1=(100,100000) lvl2=(255,0)', '1000 mb', 'anl', '\n']

        var=tt[3].split()[0]
        vardesc=''
        for vt in tt[3].split()[1:]:
            vardesc="%s %s"%(vardesc,vt)
        vardesc=vardesc.lstrip()

        (lvl1,lvl2)=tt[4].split()
        (levcode1,lev1)=splitlevcodes(lvl1)
        (levcode2,lev2,)=splitlevcodes(lvl2)

        (lev,levd,levc)=LevCode2Lev(levcode1,lev1,levcode2,lev2)

        levdesc=tt[5]
        levdesc=levd
        timedesc=tt[6]

        rec=(
            recnum,
            sizrecp1,
            var,
            vardesc,
            lev,
            levc,
            levcode1,
            lev1,
            levcode2,
            lev2,
            levdesc,
            timedesc,
            )

        #print ' ',nrec,recnum,var,vardesc,levcode1,lev1,levcode2,lev2,levdesc,levc
        
        records[nrec]=rec
        recsiz[nrec]=sizrecp1
        nrec=nrec+1

    nrectot=ncards

    return(records,recsiz,nrectot)


def Wgrib2VarAnal(records,tau):

    nr=len(records)

    vars=[]
    taus=[]
    levs=[]
    levds={}
    
    vardescs={}
    varlevs={}

    for n in range(0,nr):
        
        (
            recnum,
            sizrecp1,
            var,
            vardesc,
            lev,
            levc,
            levcode1,
            lev1,
            levcode2,
            lev2,
            levdesc,
            timedesc,
            )=records[n]
    

        var=var.lower()
        vars.append(var)
        taus.append(tau)
        levs.append(levc)
        
        try:
            varlevs[levc,tau].append(var)
        except:
            varlevs[levc,tau]=[var]

        try:
            vardescs[var,tau].append(vardesc)
        except:
            vardescs[var,tau]=[vardesc]

        levds[levc]=levdesc


    vars=mf.uniq(vars)
    taus=mf.uniq(taus)
    levs=mf.uniq(levs)
    levs.sort()

    levsnp=[]
    levsp=[]

    for lev in levs:
        lc=lev.split('.')[0]
        if(lc == '100'):
            lv=lev.split('.')[1]
            levsp.append(int(lv))
        else:
            levsnp.append(lev)


    levsnp.sort()
    
    levs=[]
    for ll in levsnp:
        levs.append(ll)

    levsp.sort()
    for ll in levsp:
        levs.append("100.%d"%(ll))
                    

    print
    print "Var Inventory by Lev for Tau: ",tau
    print
    for tau in taus:
        for lev in levs:
            vcard="%-15s "%(lev)
            try:
                lvars=varlevs[lev,tau]
                lvars.sort()
                nlvars=len(lvars)
                for nlvar in range(0,nlvars):
                    lvar=lvars[nlvar]
                    vcard="%s %-6s"%(vcard,lvar)
                    if(nlvar > 0 and nlvar%12 == 0):
                        vcard=vcard+'\n '+15*' '
            except:
                vcard=vcard

            if(nlvars > 12):    print 
            print vcard
            if(nlvars > 12):    print 

        print
        print "Var desc:"
        print
        vars.sort()
        for var in vars:
            vv=vardescs[var,tau]
            vv=mf.uniq(vv)
            print "%-6s   %s"%(var,vv[0][:-1])


        print
        print "Lev desc:"
        print
        for lev in levs:
            print "%-15s  %s"%(lev,levds[lev])



def SetFieldRequest2(tau,spec='test0'):

    request={}

    if(spec == 'test0'):

        plevs=[1000,925,850,700,500,300,250,200,150,100]
        wapplevs=[850,700,500]

        #
        # sfc + ua versions
        #
        request['ugrd']=['103.10']
        request['vgrd']=['103.10']
        request['tmp']=['103.2']
        
        for plev in plevs:
            request['ugrd']=request['ugrd']+ ['100.%d'%(plev)]
            request['vgrd']=request['vgrd']+ ['100.%d'%(plev)]
            request['tmp']=request['tmp']+ ['100.%d'%(plev)]
        
        #
        # just ua
        #
        request['hgt']=[]
        request['rh']=[]
        
        for plev in plevs:
            request['hgt']=request['hgt']+ ['100.%d'%(plev)]
            request['rh']=request['rh']+ ['100.%d'%(plev)]
    
        request['vvel']=[]
        for wapplev in wapplevs:
            request['vvel']=request['vvel']+ ['100.%d'%(wapplev)]

        request['prmsl']=['101.0']
        request['apcp']=['1.0']
        request['acpcp']=['1.0']
        request['cprat']=['1.0']
        request['prate']=['1.0']

        request['ulwrf']=['8.0']
        request['tcdc']=['211.0','214.0','224.0','234.0','244.0']

        request['tmax']=['103.2']
        request['tmin']=['103.2']

        request['pwat']=['200.0']
        

    else:
        
        request['ugrd']=[10,850,500,200]
        request['vgrd']=request['ugrd']
    
        request['tmp']=[850,500,200]
        request['rh']=request['tmp']
        request['hgt']=request['tmp']
    
        request['prmsl']=[0]
        request['apcp']=[0]
        request['acpcp']=[0]
        request['cprat']=[0]
        request['prate']=[0]
    
    request['taus']=[tau]

    return(request)


def Wgrib2VarFilter(records,request,tau):

    nr=len(records)

    rtaus=request['taus']
    rtaus.sort()
    rvars=request.keys()
    rvars.sort()

   
    orecs=[]

    nrecs=records.keys()
    nrecs.sort()
    
    for nrec in nrecs:
        

        (
            recnum,
            sizrecp1,
            var,
            vardesc,
            lev,
            levc,
            levcode1,
            lev1,
            levcode2,
            lev2,
            levdesc,
            timedesc,
            )=records[nrec]
    

        var=var.lower()


        for rvar in rvars:
            if(var == rvar):
                rlevs=request[rvar]
                for rlev in rlevs:
                    if(levc == rlev):
                        for rtau in rtaus:
                            if(rtau == tau):
                                print 'MMMMMMMMMMMMM ',	var,lev,tau,nrec,sizrecp1
                                ocard="%s:%d"%(recnum,sizrecp1)
                                ocard=ocard+'\n'
                                orecs.append(ocard)


    return(orecs)


def Wgrib2Filter(orecs,inpath,outpath):

    wcmd="wgrib2 -i %s -grib %s"%(inpath,outpath)
    print wcmd

    w=os.popen(wcmd,'w')
    w.writelines(orecs)
    w.close()


def CnvgribG21(g2path,g1path,ropt=''):

    if(os.path.exists(g2path)):
        cmd="cnvgrib -g21 %s %s"%(g2path,g1path)
    else:
        print 'EEE g2path in CnvgribG21 not there ',g2path
        sys.exit()

    mf.runcmd(cmd,ropt)
    
    


def RemoteLocalRsync(dtg,model,ropt=''):

    yymmdd=dtg[0:8]
    hh=dtg[8:10]

    localcenter=w2.W2Center.lower()
    
    if(localcenter == 'nhc'):
        remotecenter='ncep'
    if(localcenter == 'ncep'):
        remotecenter='nhc'
    
    (NcepBaseInDat,sdir,dbdir,livdeir)=w2.GetNcepBaseInOutDat(remotecenter)
    (NcepBaseInDat,tdir,dbdir,livedir)=w2.GetNcepBaseInOutDat(localcenter)
    print 'ssssssss ',sdir
    print 'tttttttt ',tdir
    
    
    if(model == 'gfs2'):

        imodel='gfs'
        rsdir="%s/%s/prod/%s.%s"%(sdir,imodel,imodel,yymmdd)
        ltdir="%s/%s/prod/%s.%s"%(tdir,imodel,imodel,yymmdd)
        rexclude=''


    try:
        mf.ChkDir(ltdir,'mk')
    except:
        print 'EEE unable to make ltdir: ',ltdir

    print 'rrrsssssss ',rsdir
    print 'lllllttttt ',ltdir

    rsyncnceploc="--rsync-path=/usrx/local/bin/rsync"
    rsyncacct="tpcprd1@prodccs.ncep.noaa.gov"
    #rsyncacct="tpcprd1@devccs.ncep.noaa.gov"

    rsyncopt="-alv"
    if(rexclude != ''):
        rsyncopt="%s %s"%(rsyncopt,rexclude)
        
    rcmd="rsync %s %s \"%s:%s/*%s*\" \"%s/\""%(rsyncopt,rsyncnceploc,rsyncacct,rsdir,dtg,ltdir)
    mf.runcmd(rcmd,ropt)
    
#rsync -alv --rsync-path=/usrx/local/bin/rsync "tpcprd1@prodccs.ncep.noaa.gov:/tpc/noscrub/OUTDAT/gfs/prod/gfs.20070611/" /storage/dat/ncep/OUTDAT/gfs/prod/gfs.20070611/




def MakeNcepDcomDataCtl(dtg,ctlpath,model,domand=0,ropt=''):

    mdhh=dtg[4:10]+'00'
    
    gtime=mf.dtg2gtime(dtg)


    if(model == 'ecm2'):
        ctl="""dset ^ecens_DCD%s%%m2%%d2%%h2001
index ^ecmo.%s.gmp
undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
ydef 181 linear -90.000000 1
xdef 360 linear 0.000000 1.000000
tdef  41 linear %s 6hr
zdef 14 levels
1000 925 850 700 500 400 300 250 200 150 100 50 20 10 
vars 15
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       14 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      14 157,100,0 ** Relative humidity %%
ta       14 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars
###---  pr is accumluated in METERS
"""%(mdhh,dtg,gtime)

    elif(model == 'cmc2'):
        ctl="""dset ^cmc_%%iy4%%im2%%id2%%ih2f%%f3
index ^cmc.%s.gmp
undef 9.999E+20
title cmc_2007061412f012
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options template
ydef 181 linear -90.000000 1
xdef 360 linear 0.000000 1.000000
tdef  25 linear %s 6hr
zdef 7 levels
1000 925 850 700 500 250 200 
vars 11
vrta     7  41,100,0 ** Absolute vorticity [/s]
pr       0  61 , 1,0  ** Total precipitation [kg/m^2]
zg       7   7,100,0 ** Geopotential height [gpm]
psl      0   2,102,0  ** Pressure reduced to MSL [Pa]
hur      7  52,100,0 ** Relative humidity [%%]
ta       7  11,100,0 ** Temp. [K]
tas      0  11,119,10000  ** Temp. [K]
ua       7  33,100,0 ** u wind [m/s]
uas      0  33,119,10000  ** u wind [m/s]
va       7  34,100,0 ** v wind [m/s]
vas      0  34,119,10000  ** v wind [m/s]
endvars
###--- pr is accumulated precip in millimeters
"""%(dtg,gtime)


    elif(model == 'ngp2'):

        nlevs=21
        plevs='1000 950 925 900 850 800 750 700 650 600 550 500 450 400 350 300 250 200 150 100 70'
        gmpfile="ngp.%s.gmp"%(dtg)

        if(domand):
            pl=w2.MandatoryPressureLevels
            nlevs=len(pl)
            plevs=''
            for p in pl:
                plevs="%s %d"%(plevs,p)

            (dir,file)=os.path.split(ctlpath)
            tt=file.split('.')
            ntt=len(tt)
            nfile=''
            for n in range(0,ntt):
                if(n == ntt-1):
                    nfile=nfile+tt[n]
                elif(n == ntt-2):
                    nfile=nfile+tt[n]+'.mand.'
                else:
                    nfile=nfile+tt[n]+'.'

            ctlpath="%s/%s"%(dir,nfile)
            gmpfile="ngp.%s.mand.gmp"%(dtg)
        
        ctl="""dset ^nogaps_%%iy4%%im2%%id2%%ih2f%%f3
index ^%s
undef 9.999E+20
title nogaps_2007061412f012
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options template
ydef 181 linear -90.000000 1
xdef 360 linear 0.000000 1.000000
tdef  25 linear %s 6hr
zdef  %d levels
%s
vars 22
vrta     0  41,100,500  ** Absolute vorticity [/s]
prc      0  63,  1,0  ** Convective precipitation [kg/m^2]
pr       0  61,  1,0  ** Total precipitation [kg/m^2]
zg      %d   7,100,0 ** Geopotential height [gpm]
zg0      0   7,  6,0  ** Geopotential height [gpm]
pmxwnd   0   1,  6,0  ** Pressure [Pa]
ptrop    0   1,  7,0  ** Pressure [Pa]
psl      0   2,102,0  ** Pressure reduced to MSL [Pa]
hur     %d  52,100,0 ** Relative humidity [%%]
ta      %d  11,100,0 ** Temp. [K]
tamxwnd  0  11  ,6,0  ** Temp. [K]
tatrop   0  11,  7,0  ** Temp. [K]
ua      %d  33,100,0 ** u wind [m/s]
uas      0  33,105,10 ** u wind [m/s]
uamxwnd  0  33,  6,0  ** u wind [m/s]
va      %d  34,100,0 ** v wind [m/s]
vas      0  34,105,10 ** v wind [m/s]
vamxwnd  0  34,  6,0  ** v wind [m/s]
wap     %d  39,100,0 ** Pressure vertical velocity [Pa/s]
uas19    0  33,105,19  ** Wind speed [m/s]
vas19    0  34,105,19  ** Wind speed [m/s]
wspd19   0  32,105,19  ** Wind speed [m/s]
endvars
###--- pr is mm/6h *4 = mm/d

"""%(gmpfile,gtime,nlevs,plevs,nlevs,nlevs,nlevs,nlevs,nlevs,nlevs)

    
    mf.WriteCtl(ctl,ctlpath)

    dogribmap=1
    if(dogribmap):
        cmd="gribmap -E -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)






def MakeNcepComDataCtl(dtg,ctlpath,model,ropt=''):

    mdhh=dtg[4:10]+'00'
    
    gtime=mf.dtg2gtime(dtg)

    ctlpr=None

    (dir,file)=os.path.split(ctlpath)
    (base,ext)=os.path.splitext(file)
    ctlprfile="%s.pr%s"%(base,ext)
    ctlprpath="%s/%s"%(dir,ctlprfile)
    
    if(model == 'gfs2'):
        
        ctl="""dset ^gfs2.%s.f%%f3.grb1
index ^gfs2.%s.gmp
undef 1e+20
title gfs2.2007100112.f006.grb1
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5  
zdef 10 levels
1000 925 850 700 500 300 250 200 150 100 
tdef 27 linear %s 6hr
vars 23
prc      0  63  ,1,0   Convective precipitation [kg/m^2]
pr       0  61,  1,0   Total precipitation [kg/m^2]
prw      0  54,200,0   precip water [mm]
prcr     0 214,  1,0   Convective precip. rate [kg/m^2/s]
prr      0  59,  1,0   Precipitation rate [kg/m^2/s]
zg      10   7,100,0   Geopotential height [gpm]
psl      0   2,102,0   Pressure reduced to MSL [Pa]
hur     10  52,100,0   Relative humidity [%%]
clt      0  71,211,0   Total cloud cover [%%]
cll      0  71,214,0   Total cloud cover [%%]
clm      0  71,224,0   Total cloud cover [%%]
clh      0  71,234,0   Total cloud cover [%%]
cltc     0  71,244,0   Total cloud cover [%%]
tasmx    0  15,105,2   Max. temp. [K]
tasmn    0  16,105,2   Min. temp. [K]
tas      0  11,105,2   Temp. [K]
ua      10  33,100,0   u wind [m/s]
uas      0  33,105,10  u wind [m/s]
rlut     0 212,  8,0   Upward long wave flux [W/m^2]
va      10  34,100,0   v wind [m/s]
ta      10  11,100,0   air temperatrue [K]
vas      0  34,105,10  v wind [m/s]
wap     10  39,100,0   Pressure vertical velocity [Pa/s]
endvars"""%(dtg,dtg,gtime)

        ctlpr="""dset ^gfs2.%s.f%%f3.grb1
index ^gfs2.%s.pr.gmp
undef 1e+20
title gfs2.2007100112.f006.pr.grb1
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5  
zdef 10 levels
1000 925 850 700 500 300 250 200 150 100 
tdef 56 linear %s 3hr
vars 4
prc      0  63  ,1,0   Convective precipitation [kg/m^2]
pr       0  61,  1,0   Total precipitation [kg/m^2]
prcr     0 214,  1,0   Convective precip. rate [kg/m^2/s]
prr      0  59,  1,0   Precipitation rate [kg/m^2/s]
endvars"""%(dtg,dtg,gtime)

    elif(model == 'ngp'):
        print 'WWWW nogaps not implemented yet...'
        
    else:
        print 'nnnn'

    
    mf.WriteCtl(ctl,ctlpath)
    if(ctlpr != None):
        mf.WriteCtl(ctlpr,ctlprpath)
        

    dogribmap=1
    if(dogribmap):
        cmd="gribmap -E -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)

        if(ctlpr != None):
            cmd="gribmap -E -i %s"%(ctlprpath)
            mf.runcmd(cmd,ropt)





