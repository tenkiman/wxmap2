import os,sys,glob
import cPickle as pickle
import mf
from M import *
MF=MFutils()


class Wgrib1Rec(MFbase):

    def __init__(self,rec):

        (
            centernum,
            subcenternum,
            processnum,
            gribtablenum,
            sizrecp1,
            gridcode,
            nx,
            ny,
            gridnum,
            nxny,
            ndef,
            nundef,
            blat,
            elat,
            dlat,
            blon,
            elon,
            dlon,
            scan,
            mode,
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
        
        
        self.centernum=centernum
        self.subcenternum=subcenternum
        self.processnum=processnum
        self.gribtablenum=gribtablenum
        self.sizrecp1=sizrecp1
        self.gridcode=gridcode
        self.nx=nx
        self.ny=ny
        self.gridnum=gridnum
        self.nxny=nxny
        self.ndef=ndef
        self.nundef=nundef
        self.blat=blat
        self.elat=elat
        self.dlat=dlat
        self.blon=blon
        self.elon=elon
        self.dlon=dlon
        self.scan=scan
        self.mode=mode
        self.timecode=timecode
        self.timedesc=timedesc
        self.timerangeind=timerangeind
        self.timerangep1=timerangep2
        self.timerangep2=timerangep2
        self.timeunits=timeunits
        self.tau=tau
        self.varcode=varcode
        self.var=var
        self.vardesc=vardesc
        self.levcode=levcode
        self.lev=lev
        self.levcode2=levdesc
        self.levdesc=gridvalmin
        self.gridvalmin=gridvalmin
        self.gridvalmax=gridvalmax
        self.nbits=nbits
        self.bdsref=bdsref
        self.decscale=decscale
        self.binscale=binscale




class Wgrib2Rec():


    def __init__(self,rec):

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
            timedesc
            )=rec

        
        self.recnum=recnum
        self.sizrecp1=sizrecp1
        self.var=var
        self.vardesc=vardesc
        self.lev=lev
        self.levc=levc
        self.levcode1=levcode1
        self.levcode=levcode1
        self.lev1=lev1
        self.levcode2=levcode2
        self.lev2=lev2
        self.levdesc=levdesc
        self.timedesc=timedesc





class Grib(MFbase):


    def WriteFdbCards(self,cards,cardpath,verb=0):

        try:
            c=open(cardpath,'w')
        except:
            print "EEE unable to open: %s"%(cardpath)
            return

        if(verb): print "CCCC creating .card: %s"%(cardpath)
        c.writelines(cards)
        c.close()
        
        return
    
    def GetFdb(self,tau):

        try:
            F=open(self.fdbpaths[tau])
            cards=F.readlines()
            F.close()
        except:
            cards=None
            
        return(cards)



    def GetLatlonGrid(self,tau):

        htype=self.gribtype
        datpath=self.tdatpaths[tau]

        #
        # use the combined grid used in the ncep post processor for track
        #


        if(htype == 'grb2'):

            datSiz=MF.getPathSiz(datpath)
            
            if(datSiz <= 0):
                return(None)

            cmd="%s -grid -d 1 %s"%(self.xwgrib,datpath)
            cards=os.popen(cmd).readlines()

            #
            # get the gds grid number
            #
            cmd="%s -Sec3 -d 1 %s"%(self.xwgrib,datpath)
            gcards=os.popen(cmd).readlines()

            #
            # get scan mode
            #
            cmd="%s -scan -d 1 %s"%(self.xwgrib,datpath)
            scards=os.popen(cmd).readlines()

            if(len(cards) == 0):
                return(None)
            
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


            scan=scards[0].split(':')[2].split('=')[1].split()[0]
            mode=-999
            gridnum=-999
            grid=[nx,ny,blat,elat,dlat,blon,elon,dlon,scan,mode,gridnum]

        else:

            cards=self.MakeFdb1Cards(datpath)
            (records,recsiz,nrectot)=self.ParseFdb1(cards=cards)

            if(len(records) == 0):
                return(None)
            grid=None
            W=records[1]
            grid=[W.nx,W.ny,W.blat,W.elat,W.dlat,W.blon,W.elon,W.dlon,W.scan,W.mode,W.gridnum]

        return(grid)




class Grib1(Grib):

    def MakeFdb1Cards(self,datpath):

        cards=[]
        cards.append(datpath+'\n')
        
        wcards=os.popen("%s -V %s "%(self.xwgrib,datpath)).readlines()
        cards=cards+wcards

        return(cards)
            

    def ParseFdb1(self,cards=None,ttau=None,verb=0,override=0):

        if(cards == None and ttau != None):
            cards=self.GetFdb(ttau)
            

        recsiz={}
        records={}
        nrectot=0

        try:
            ncards=len(cards)
        except:
            return(records,recsiz,nrectot)
            

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
                        vardesc=tt[1].strip()

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
                        #long 0.000000 to -1.000000 by 1.000000, (360 x 181) scan 0 mode 136 bdsgrid 1
                        if(verb): print 'CCC ',n,rcard[:-1]
                        tt=rcard.split()
                        blon=float(tt[1])
                        elon=float(tt[3])
                        dlon=float(tt[5].split(',')[0])
                        scan=int(tt[10])
                        mode=int(tt[12])
                                 

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

                tau=self.Grib1Time2Tau(timerangeind,timerangep1,timerangep2)

                rec=(
                    centernum,
                    subcenternum,
                    processnum,
                    gribtablenum,
                    sizrecp1,
                    gridcode,
                    nx,
                    ny,
                    gridnum,
                    nxny,
                    ndef,
                    nundef,
                    blat,
                    elat,
                    dlat,
                    blon,
                    elon,
                    dlon,
                    scan,
                    mode,
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

                WG=Wgrib1Rec(rec)

                records[nrec]=WG
                recsiz[nrec]=sizrecp1

                nrectot=nrec

            
        return(records,recsiz,nrectot)




    def Grib1Time2Tau(self,timerangeind,timerangep1,timerangep2):

        # instantaneous
        #
        if(timerangeind == 0):
            tau=timerangep1

        # average(?) - put tau at end of interval
        #
        elif(timerangeind == 2):
            tau=timerangep2

        # accumulated - put tau at end of interval
        #
        elif(timerangeind == 4):
            tau=timerangep2

        # average - put tau at end of interval
        #
        elif(timerangeind == 3):
            tau=timerangep2
            
        # tau occupies both p1 and p2
        
        elif(timerangeind == 10):
            tau=timerangep1*256 + timerangep2

        #
        # if not one of these return none
        #
        else:
            print 'tttttttt problem in Grib1.Grib1Time2Tau: ',timerangeind,timerangep1,timerangep2
            tau=None

        return(tau)


    def GetTauGrib1File(self,file):
        tau=file[-3:]
        tau=int(tau)
        return(tau)

    def MakeFdb1(self,ropt='',override=0,verb=0,ttau=None):

        self.taus=[]
        self.fdbpaths={}
        self.sdatpaths={}
        self.sdatpathAges={}
        self.tdatpaths={}

        curdtg=mf.dtg()

        gribfiles=glob.glob(self.gmask)
        gribfiles.sort()

        
        if(len(gribfiles) == 0):
            print 'WWW no source grib1111 files for gmask ',self.gmask
            
        for sdatpath in gribfiles:
            (dir,file)=os.path.split(sdatpath)
            agecur=MF.PathCreateTimeDtgdiff(curdtg,sdatpath)

            tau=self.GetTauGrib1File(file)
            fdbpath="%s/%s.wgrib1.txt"%(self.tDir,file)
            tdatpath="%s.f%03d.%s"%(self.tdatbase,tau,self.gribtype)

            if(ttau != None and tau != ttau): continue
            self.taus.append(tau)
            
            #
            # req override = 2 vice the more normal =1 since this is expensive...
            #

            if( ((override == 2) or not(os.path.exists(fdbpath))) or (ttau != None and tau == ttau) ):
                F=open(fdbpath,'w')
                F.writelines(sdatpath+'\n')
                F.close()
                cmd="%s -V %s >> %s"%(self.xwgrib,sdatpath,fdbpath)
                mf.runcmd(cmd,ropt)

            self.fdbpaths[tau]=fdbpath
            self.sdatpaths[tau]=sdatpath
            self.sdatpathAges[tau]=agecur
            self.tdatpaths[tau]=tdatpath


        tdatmask="%s.f%%f3.%s"%(self.tbase,self.gribtype)

        #
        #if no source files...look for target output
        #
        if(len(self.tdatpaths) == 0):
            tpathmask="%s.f???.%s"%(self.tdatbase,self.gribtype)
            gribs=glob.glob(tpathmask)
            gribs.sort()
            
            for grib in gribs:
                (dir,file)=os.path.split(grib)
                tau=int(file.split('.')[2][1:])
                self.taus.append(tau)
                self.tdatpaths[tau]=grib

        else:
            self.taus.sort()
        
        self.tdatmask=tdatmask


    def Wgrib1VarCtl(self,records,verb=1):

        nr=len(records)

        uavars=[]
        sfcvars=[]
        ualevs=[]

        vardescs={}
        varlevs={}
        varcodes={}

        uvs=[]

        if(hasattr(self,'sfcvars')):
            reqsfcvars=self.sfcvars
        else:
            reqsfcvars=self.FQ.sfcvars
            
        ovarsfcs=reqsfcvars.keys()
        ovarsfcs.sort()

        #
        # find # ua levs
        #
        nsfc=0
        for n in range(1,nr+1):
            
            W=records[n]
            
            lvar=W.var.lower()

            if(int(W.levcode) == 100):
                ualevs.append(W.lev)
                uvs.append(W.var.lower())


        ualevs=mf.uniq(ualevs)
        ualevs.reverse()

        uvs=mf.uniq(uvs)

        nualevs=len(ualevs)
        
        for n in range(1,nr+1):

            W=records[n]

            ilevcode=int(W.levcode)
            ilevreq="%d.%d"%(int(ilevcode),int(W.lev))
            ivar=W.var.lower()
            
            if(ilevcode == 100):
                olev='%3d,  0'%(ilevcode)
                
                if(hasattr(self,'I2Ouavar')):
                    ovar="%s"%(self.I2Ouavar(ivar))
                else:
                    ovar="%s"%(self.FQ.I2Ouavar(ivar))
                    
                uavar="%-8s %3d %3d,%s  %s"%(ovar,nualevs,int(W.varcode),olev,W.vardesc)
                uavars.append(uavar)

            else:

                for ovarsfc in ovarsfcs:

                    tt=reqsfcvars[ovarsfc]
                    rsfcvar=tt[0]
                    rlevreq=tt[1]
                    
                    # check for match based on name and levcode
                    # request used '105.1' form but wgrib outputs '105,1' so do replace in FQ.I2Osfcvar
                    #
                    if(ivar == rsfcvar and ilevreq == rlevreq):
                
                        olev='%3d,%3d'%(int(ilevcode),int(W.lev))
                        ovar=ovarsfc
                           
                        sfcvar="%-8s %3d %3d,%s  %s"%(ovar,0,int(W.varcode),olev,W.vardesc)
                        sfcvars.append(sfcvar)


        if(nualevs > 0):
            zdef="zdef %3d levels"%(nualevs)
            for l in ualevs:
                zdef="%s %4d"%(zdef,l)

        else:
            zdef="zdef 1 levels 1013"

                
        uavars=mf.uniq(uavars)
        sfcvars=mf.uniq(sfcvars)
        
        return(zdef,sfcvars,uavars)


    def Wgrib1VarFilter(self,records,request,verb=0):

        nr=len(records)

        rtaus=request['taus']
        rtaus.sort()
        rvars=request.keys()
        rvars.sort()

        orecs=[]

        nrecs=records.keys()
        nrecs.sort()

        for nrec in nrecs:

            W=records[nrec]

            var=W.var.lower()
            clev="%s.%s"%(W.levcode,W.lev)


            for rvar in rvars:

                if(var == rvar):

                    rlevs=request[rvar]
                    for rlev in rlevs:
                        if(clev == rlev):
                            for rtau in rtaus:
                                if(rtau == W.tau):
                                    if(verb): print 'MMMMMMMMMMMMM ',	W.var,clev,W.tau,nrec,W.sizrecp1
                                    ocard="%d:%d"%(nrec,W.sizrecp1)
                                    ocard=ocard+'\n'
                                    orecs.append(ocard)


        return(orecs)


    def Wgrib1Filter(self,orecs,inpath,outpath):

        wcmd="%s -s -i -grib -s %s -o %s"%(self.xwgrib,inpath,outpath)
        print 'WWW111--- ',wcmd
        w=os.popen(wcmd,'w')
        w.writelines(orecs)
        w.close()


    def MakeCtl(self,verb=0,ropt='',override=0,usedataTaus=0):


        if(hasattr(self,'usedataTaus')): usedataTaus=self.usedataTaus

        
        ctl=[]
        if(self.gribtype == 'grb1'):
            if(len(self.taus) > 1):
                tau=self.taus[1]
            else:
                tau=self.taus[0]
            datfile=self.tdatpaths[tau]
            cards=[]
            cards.append(datfile+'\n')
            wcards=os.popen("%s -V %s "%(self.xwgrib,datfile)).readlines()
            cards=cards+wcards
            (records,recsiz,nrectot)=self.ParseFdb1(cards=cards)
            (zdef,sfcvars,uavars)=self.Wgrib1VarCtl(records)

        elif(self.gribtype == 'grb2'):
            tau=self.taus[0]
            datpath=self.tdatpaths[tau]
            cards=self.MakeFdb2Cards(datpath)
            (records,recsiz,nrectot)=self.ParseFdb2(cards=cards)
            (zdef,sfcvars,uavars)=self.Wgrib2VarCtl(records)


        else:
            print 'EEE only grib1 and grib2 allowed...'
            sys.exit()


        # -- case where no data -- 0 length file
        #
        for n in range(0,len(self.taus)):
            grid=self.GetLatlonGrid(self.taus[n])
            if(grid != None): break

        if(grid == None): 
            print 'WWW(GRIB.Grib1.MakeCtl): non data -- return'
            return
            
        (nx,ny,blat,elat,dlat,blon,elon,dlon,scan,mode,gridnum)=grid

        dset="dset ^%s"%(self.tdatmask)
        ctl.append(dset)
        title="title test"
        ctl.append(title)

        undef='undef 9.999E+20'
        ctl.append(undef)

        gmpfile="index ^%s"%(self.gmpfile)
        ctl.append(gmpfile)

        if(self.gribtype == 'grb1'): 
            dtype='dtype grib 255'
            ctl.append(dtype)
        elif(self.gribtype == 'grb2'):
            dtype='dtype grib2'
            ctl.append(dtype)
        
        options="options template"
        if(blat > elat or mode == 136):
            options="%s yrev"%(options)
            blat=elat

        if(self.gribtype == 'grb2'):
            options="%s pascals"%(options)
            
            
        ctl.append(options)


        xdef="xdef %4d linear %6.2f %6.2f"%(nx,blon,dlon)
        ydef="ydef %4d linear %6.2f %6.2f"%(ny,blat,dlat)

        ctl.append(xdef)
        ctl.append(ydef)
        ctl.append(zdef)

        #
        # use target taus (ttaus) vice data taus
        #
        if(usedataTaus):
            nt=len(self.taus)
            dtau=self.taus[1]-self.taus[0]
        else:
            nt=len(self.ttaus)
            dtau=self.ttaus[1]-self.ttaus[0]

        tdef="tdef %3d linear %s %dhr"%(nt,self.gtime,dtau)
        ctl.append(tdef)

        nvars=len(uavars)+len(sfcvars)
        varcard="vars %d"%(nvars)
        ctl.append(varcard)

        for uavar in uavars:
            ctl.append(uavar)

        for sfcvar in sfcvars:
            ctl.append(sfcvar)

        endvarcard='endvars'

        ctl.append(endvarcard)

        mf.WriteList(ctl,self.ctlpath)
        print 'ccccccccccccccccc ',self.ctlpath

        #
        # now do the gribmap
        #

        if(verb):
            cmd="%s -v -i %s"%(self.xgribmap,self.ctlpath)
        else:
            cmd="%s -i %s"%(self.xgribmap,self.ctlpath)
            
        mf.runcmd(cmd,ropt)

        if(verb):
            for card in ctl:
                print card
        
        

    def PrintWgrib1Record(self,nrec,W):

        print
        print 'FFF Record: '
        print '         nrec: ',nrec
        print '     sizrecp1: ',W.sizrecp1
        print
        print 'FFF Grid: '
        print '     gridcode: ',W.gridcode
        print '           nx: ',W.nx
        print '           ny: ',W.ny
        print '         nxny: ',W.nxny
        print '         ndef: ',W.ndef
        print '       nundef: ',W.nundef
        print
        print '         blat: ',W.blat
        print '         elat: ',W.elat
        print '         dlat: ',W.dlat
        print 
        print '         blon: ',W.blon
        print '         elon: ',W.elon
        print '         dlon: ',W.dlon
        print
        print 'FFF Time: '
        print '     timecode: ',W.timecode
        print '     timedesc: ',W.timedesc
        print ' timerangeind: ',W.timerangeind
        print '  timerangep1: ',W.timerangep1
        print '  timerangep2: ',W.timerangep2
        print '    timeunits: ',W.timeunits
        print '          tau: ',W.tau
        print
        print 'FFF Var: '
        print '      varcode: ',W.varcode
        print '          var: ',W.var
        print '      vardesc: ',W.vardesc
        print
        print 'FFF Level: '
        print '      levcode: ',W.levcode
        print '          lev: ',W.lev
        print '     levcode2: ',W.levcode2
        print '      levdesc: ',W.levdesc
        print
        print 'FFF Grid Values: '
        print '   gridvalmin: ',W.gridvalmin
        print '   gridvalmax: ',W.gridvalmax
        print
        finalcard="%-8s %s  %-8s  %-10s  %-16s"%(W.var,W.vardesc[0:-1],W.timecode,W.timedesc,W.levdesc)


        print 'FFF GRIB packing: '
        print '        nbits: ',W.nbits
        print '       bdsref: ',finalcard,W.bdsref,W.gridvalmin,W.nbits,W.decscale,W.binscale
        print '     decscale: ',W.decscale
        print '     binscale: ',W.binscale


    def Wgrib1VarAnal(self,records):

        nr=len(records)

        vars=[]
        taus=[]
        levs=[]

        vardescs={}
        varlevs={}
        varcodes={}

        for n in range(1,nr+1):

            W=records[n]

            var=W.var.lower()
            vars.append(var)
            taus.append(W.tau)
            olev='%s.%s'%(W.levcode,W.lev)
            levs.append(olev)

            try:
                varlevs[olev,W.tau].append(var)
            except:
                varlevs[olev,W.tau]=[var]

            try:
                vardescs[var,W.tau].append(W.vardesc)
            except:
                vardescs[var,W.tau]=[W.vardesc]

            try:
                varcodes[var].append(W.varcode)
            except:
                varcodes[var]=[W.varcode]


        vars=mf.uniq(vars)
        taus=mf.uniq(taus)
        levs=mf.uniq(levs)
        levs.sort()

        for tau in taus:
            for lev in levs:
                vcard="%-8s "%(lev)
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
                vc=varcodes[var]
                print "%-6s  %3s  %s "%(var,vc[0],vv[0][:-1])



class Grib2(Grib):

    def MakeFdb2Cards(self,datpath):

        cards=[]
        cards.append(datpath+'\n')

        wg2opt='-v2'
        cards1=os.popen("%s %s %s"%(self.xwgrib,wg2opt,datpath)).readlines()

        wg2opt='-t -ftime -var -varX -lev0 -ctl_inv -stats' # -stats is VERY expensive; needed?
        wg2opt='-t -ftime -var -varX -lev0 -ctl_inv '
        
        cards2=os.popen("%s %s %s"%(self.xwgrib,wg2opt,datpath)).readlines()

        for n in range(0,len(cards1)):
            cards.append(cards1[n])
            cards.append(cards2[n])


        return(cards)
            
    
    def MakeFdb2(self,ropt='',override=0,ttau=None):

        self.taus=[]
        self.fdbpaths={}
        self.sdatpaths={}
        self.sdatpathAges={}
        self.tdatpaths={}

        MF.sTimer('GRIB-Grib2-MakeFdb2')
        curdtg=mf.dtg()

        if(hasattr(self,'grbpaths')):
            gribfiles=self.grbpaths
        else:
            gribfiles=glob.glob(self.gmask)

        if(hasattr(self,'dbasedir')):
            self.tDir=self.dbasedir

        if(hasattr(self,'dbase')):
            self.tdatbase=self.dbase
            
        gribfiles.sort()

        
        if(len(gribfiles) == 0):
            print 'WWW no source grib2222 files for gmask ',self.gmask
            return(0)
            
        for sdatpath in gribfiles:
            
            (dir,file)=os.path.split(sdatpath)
            agecur=self.PathCreateTimeDtgdiff(curdtg,sdatpath)
            tau=self.GetTauGrib1File(file)

            
            fdbpath="%s/%s.wgrib2.txt"%(self.tDir,file)
            tdatpath="%s.f%03d.%s"%(self.tdatbase,tau,self.gribtype)
            
            self.taus.append(tau)

            # req override = 2 vice the more normal =1 since this is expensive...
            #
            if( ((override == 2) or not(os.path.exists(fdbpath))) or (ttau != None and tau == ttau) ):
                print 'GG22 ',fdbpath
                cards=self.MakeFdb2Cards(sdatpath)
                self.WriteFdbCards(cards,fdbpath)
        
            self.fdbpaths[tau]=fdbpath
            self.sdatpaths[tau]=sdatpath
            self.sdatpathAges[tau]=agecur
            self.tdatpaths[tau]=tdatpath

        tdatmask="%s.f%%f3.%s"%(self.tbase,self.gribtype)

        self.taus.sort()
        self.tdatmask=tdatmask
        MF.dTimer('GRIB-Grib2-MakeFdb2')
        


    def Wgrib2VarCtl(self,records,verb=0):
        """ FQ is the FieldRequest object
        that should be dangled off self (FimRun object)
        """
        nr=len(records)

        isfcvars=[]
        isfcvarcodes={}

        iuavars=[]
        iualevs=[]
        iuavarcodes={}
        
        ouavars=[]
        osfcvars=[]

        vardescs={}
        varlevs={}
        
        
        #
        # find # ua levs
        #
        nsfc=0
        for n in range(1,nr+1):

            W=records[n]

            lvar=W.var.lower()
            levvar=int(W.varlev.split(',')[1])

            if(int(W.levcode1) == 100):
                iuavars.append(lvar)
                iualevs.append(levvar)
                iuavarcodes[lvar]=W.varlev + ' ' + W.varunits
            else:
                # make sfc var key = name + levcode, e.g.,
                # tas = tmp.105.1
                # ts  = tmp.1.0
                # variable name the same, but levcodes different
                nsfc=nsfc+1
                skey="%s.%s"%(lvar,W.varlev)
                isfcvars.append(skey)
                isfcvarcodes[skey]=W.varlev + ' ' + W.varunits

        iuavars=mf.uniq(iuavars)
        iualevs=mf.uniq(iualevs)

        iualevs=mf.uniq(iualevs)
        iualevs.reverse()

        niualevs=len(iualevs)
        
        for n in range(1,nr+1):

            W=records[n]

            ilevcode=int(W.levcode)
            if(ilevcode == 100):
                for iuavar in iuavars:
                    if(W.var.lower() == iuavar):
                        if(hasattr(self,'I2Ouavar')):
                            ovar="%s"%(self.I2Ouavar(iuavar))
                        else:
                            ovar="%s"%(self.FQ.I2Ouavar(iuavar))
                        ouavar="%-8s %3d,%-10d %-10s  %-s"%(ovar,niualevs,ilevcode,W.varunits,W.vardesc)
                        ouavars.append(ouavar)

            else:
                
                for skey in isfcvars:

                    isfcvar=skey.split('.')[0]
                    ilevcode=skey.split('.')[1]
                    iunitscode=isfcvarcodes[skey].split()[1]
                    
                    # check for match based on name and levcode
                    # request used '105.1' form but wgrib outputs '105,1' so do replace in FQ.I2Osfcvar
                    #
                    if(W.var.lower() == isfcvar and W.varlev == ilevcode):

                        if(hasattr(self,'I2Osfcvar')):
                            ovar="%s"%(self.I2Osfcvar(isfcvar,ilevcode))
                        else:
                            ovar="%s"%(self.FQ.I2Osfcvar(isfcvar,ilevcode))
                        osfcvar="%-8s %3d,%-10s %-10s  %-s"%(ovar,0,ilevcode,iunitscode,W.vardesc)
                        osfcvars.append(osfcvar)


        if(niualevs > 0):
            zdef="zdef %3d levels"%(niualevs)
            for l in iualevs:
                zdef="%s %4d"%(zdef,l)

        else:
            zdef="zdef 1 levels 1013"

                
        ouavars=mf.uniq(ouavars)
        osfcvars=mf.uniq(osfcvars)

        if(verb):
            for ouavar in ouavars:
                print 'ouavar  ',ouavar
        
            for osfcvar in osfcvars:
                print 'osfcvar ',osfcvar
        
        return(zdef,osfcvars,ouavars)

                

    def LevCode2Lev2(self,lc1,lv1,lc2,lv2):
        
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
        elif(lc1== 105):
            ld='hybrid layer'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
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

        return(lv,ld,levc)


    def ParseFdb2(self,cards=None,ttau=None,verb=0):

        if(cards == None and ttau != None):
            cards=self.GetFdb(ttau)


        def splitlevcodes(lvl):
            tt=lvl.split('=')
            lll=tt[1].split(',')
            lc=int(lll[0][1:])
            ll2=lll[1][:-1]
            if(lc == 255 or lc == 109 or lc == 104 or lc == 106  or lc == 108):
                if(ll2 == 'missing'):
                    ll=-999.
                else:
                    ll=float(ll2)
                    
            #
            # new parameter from ncep for gfs when lc=103 changes on 2009121512
            #
            elif(lc == 103):
                if(ll2 == 'missing'):
                    ll=-999.
                else:
                    ll=float(ll2)
                    
            elif(lc == 100):
                ll=float(ll2)*0.01
            elif(lc == 255):
                ll=-999.
            else:
                ll=float(ll2)
            return(lc,ll,ll2)


        if(cards == None):
            return(None,None,None)

        ncards=len(cards)

        recsiz={}
        records={}

        #
        # the first card has the data path
        #

        nrec=1
        nc=1
        
        for nr in range(nc,ncards,2):

            #11111111111111111111111111111111111111111111111111111111111111111111111111111111111111
            # first card is -v2
            #
            #  tt  0 1
            #  tt  1 0
            #  tt  2 12Z02dec2009
            #  tt  3 HGT Geopotential Height [gpm]
            #  tt  4 lvl1=(100,100000) lvl2=(255,missing)
            #  tt  5 1000 mb
            #  tt  6 anl

            card=cards[nr]
            tt=card.split(':')
            recnum=tt[0]
            sizrecp1=int(tt[1])

            var=tt[3].split()[0]
            vardesc=''
            for vt in tt[3].split()[1:]:
                vardesc="%s %s"%(vardesc,vt)
            vardesc=vardesc.lstrip()

            tt4=tt[4].split()
            if(len(tt4) == 4):
                lvl1=tt4[2]
                lvl2=tt4[3]
            else:
                lvl1=tt4[0]
                lvl2=tt4[1]

            (levcode1,lev1,lev1full)=splitlevcodes(lvl1)
            (levcode2,lev2,lev2full)=splitlevcodes(lvl2)

            (lev,levd,levc)=self.LevCode2Lev2(levcode1,lev1,levcode2,lev2)

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


            WG=Wgrib2Rec(rec)
            
            #print ' ',nrec,recnum,var,vardesc,levcode1,lev1,levcode2,lev2,levdesc,levc

            #2222222222222222222222222222222222222222222222222222222222222222222222222222222222222
            # second card
            #
            card=cards[nr+1]
            
            tt=card.split(':')
            #for t in tt: print 'tt ',t
            WG.bdtg=tt[2][2:]
            WG.vartime=tt[3]
            WG.varlev=tt[4]
            WG.varfull=tt[5]
            
            WG.varlevsmall=tt[6]
            varctl=tt[7].strip()
            ttt=varctl.split()
            #for t in ttt: print 'ttt ',t
            WG.varctl=varctl
            WG.varlev=ttt[1]
            WG.varunits=ttt[2]
                
            records[nrec]=WG
            
            recsiz[nrec]=sizrecp1
            nrec=nrec+1

        nrectot=nrec

        return(records,recsiz,nrectot)



    def Wgrib2VarFilter(self,records,request,tau,verb=1):

        orecs=[]
        if(records == None): return(orecs)
        nr=len(records)

        rtaus=request['taus']
        rtaus.sort()
        rvars=request.keys()
        rvars.sort()


        nrecs=records.keys()
        nrecs.sort()

        for nrec in nrecs:
            W=records[nrec]

            var=W.var.lower()

            for rvar in rvars:
                if(var == rvar):
                    rlevs=request[rvar]
                    runits=request[rvar,'units']
                    
                    #
                    # units check
                    #
                    if(runits != None and runits != W.varunits): break
                    
                    for rlev in rlevs:
                        if(W.levc == rlev):
                            for rtau in rtaus:
                                if(rtau == tau):
                                    if(verb): print 'MMMMMMMMMMMMM ',	var,rlev,tau,nrec,W.sizrecp1,W.timedesc
                                    ocard="%s:%d"%(W.recnum,W.sizrecp1)
                                    ocard=ocard+'\n'
                                    orecs.append(ocard)



        return(orecs)


    def Wgrib2VarAnal(self,records,tau):

        nr=len(records)

        vars=[]
        taus=[]
        levs=[]
        levds={}

        vardescs={}
        varlevs={}
        varcodes={}

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

            try:
                varcodes[var].append(var)
            except:
                varcodes[var]=[var]

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
                vc=varcodes[var]
                print "%-6s %6s  %s"%(var,vc[0],vv[0][:-1])


            print
            print "Lev desc:"
            print
            for lev in levs:
                print "%-15s  %s"%(lev,levds[lev])


    def Wgrib2Filter(self,orecs,inpath,outpath):

        wcmd="wgrib2 -i %s -grib %s"%(inpath,outpath)
        print wcmd

        w=os.popen(wcmd,'w')
        w.writelines(orecs)
        w.close()


