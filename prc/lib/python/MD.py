
from TC import *


class Mdeck(MFutils,TCutils):

    def __init__(self,year,mdD,mdDg,mdDs,verb=1,dop1year=1):

        # -- make dataset
        #
        dsname="mdeck_%s"%(year)
        ds=DataSet(name=dsname,dtype='tcmdeck')
        yearp1=str(int(year)+1)

        dsDname='mdeck_dtg'
        dsDtg=DataSet(name=dsDname,dtype='tcmdeckdtg')
        if(mdD == None): mdD=dsDtg

        dsDname='mdeck_dtg_gen'
        dsDtgGen=DataSet(name=dsDname,dtype='tcmdeckdtg')
        if(mdDg == None): mdDg=dsDtgGen

        dsDname='mdeck_stmid'
        dsStmid=DataSet(name=dsDname,dtype='tcmdeckdtg')
        if(mdDs == None): mdDs=dsStmid

        # -- get mdecks from current year + future year for shem season
        #
        self.mds=glob.glob("%s/%s/MdOps*txt"%(MdeckBaseDir,year))
        if(dop1year): self.mds=self.mds+glob.glob("%s/%s/MdOps*txt"%(MdeckBaseDir,yearp1))

        for md in self.mds:
            if(verb): print 'MD: ',md
            (dir,file)=os.path.split(md)
            tt=file.split('.')
            stmb3id=tt[1]
            stmyear=tt[2]
            stmid=tt[3]
            stmbdtg=tt[4]
            stmedtg=tt[5]

            #print stmb3id,stmyear,stmid,stmbdtg,stmedtg

        self.bts={}
        self.btdtgs={}
        self.firstTCdtg={}

        self.gts={}
        self.stms=[]
        self.stm1ids={}
        self.stm2ids={}
        self.stmdtg={}

        try:
            self.stm1dtg=mdD.stm1dtg
            self.tcvitalsdtg=mdD.tcvitalsdtg
            self.gen1dtg=mdDg.gen1dtg
            self.gendtgs=mdDg.gendtgs
            self.sbts=mdDs.sbts
        except:
            self.stm1dtg={}
            self.gen1dtg={}
            self.gendtgs={}
            self.tcvitalsdtg={}
            self.sbts={}

        self.stm2dtg={}
        self.stmnames={}

        for md in self.mds:
            try:
                for mdcard in open(md).readlines():
                    self.ParseMdeckCard2Btcs(mdcard)
            except:
                print 'EEE(MD.Mdeck() unable to open: ',md,' continue...'
                continue


        self.stms=self.uniq(self.stms)

        tcnames=GetTCnamesHash(year)

        for stm in self.stms:
            sid=stm.split('.')[0]
            syy=stm.split('.')[1]
            try:
                name=tcnames[syy,sid]
            except:
                name='undef'
            self.stmnames[stm]=name
            stm2id=stm1idTostm2id(stm)
            stm1id=stm
            self.stm2ids[stm1id]=stm2id
            self.stm1ids[stm2id]=stm1id

            # -- get genesis dtgs, props => gendtgs and gen1dtg
            #
            self.getBtGen(stm)


        # -- dict version of stms by dtg
        #
        for dtg in self.stmdtg.keys():
            (stm2,stm1)=self.getStms4Dtg(dtg)
            self.stm2dtg[dtg]=stm2
            self.stm1dtg[dtg]=stm1

        kk=self.stm1dtg.keys()

        ds.bts=self.bts
        ds.btdtgs=self.btdtgs

        ds.gts=self.gts
        ds.gendtgs=self.gendtgs

        ds.stms=self.stms
        ds.stmdtg=self.stmdtg
        ds.stm2dtg=self.stm2dtg
        ds.stm1dtg=self.stm1dtg
        ds.stmnames=self.stmnames

        ds.md=self

        self.ds=ds

        mdD.stm1dtg=self.stm1dtg
        self.uniqDictDict(self.tcvitalsdtg)
        mdD.tcvitalsdtg=self.tcvitalsdtg
        self.mdD=mdD

        mdDg.gendtgs=self.gendtgs
        mdDg.gen1dtg=self.gen1dtg
        self.mdDg=mdDg

        mdDs.sbts=self.sbts
        self.mdDs=mdDs




    def getTC2idsFromDtg(self,dtg,dofilt9x=0):

        try:
            stms=self.stm2dtg[dtg]
        except:
            stms=None

        ostms={}

        if(stms != None):
            stm2ids=stms.keys()
            stm2ids.sort()

            for stm2id in stm2ids:

                tc=stms[stm2id]
                snum=int(stm2id[2:4])

                if(dofilt9x and (snum >= 90 and snum <= 99) ): continue

                lat=tc[0]
                lon=tc[1]
                vmax=tc[2]

                ostms[stm2id]=(lat,lon,vmax)

        return(ostms)


    def getStms4Dtg(self,dtg):

        try:
            stms=self.stmdtg[dtg]
        except:
            stms=None

        ostms2={}
        ostms1={}

        if(stms != None):
            for stm in stms:
                stm1id=stm[0]
                stm2id=stm1idTostm2id(stm1id)
                lat=stm[1]
                lon=stm[2]
                vmax=stm[3]
                pmin=stm[4]
                age=stm[5]
                ostms2[stm2id]=(lat,lon,vmax,pmin,age)
                ostms1[stm1id]=(lat,lon,vmax,pmin,age)

        return(ostms2,ostms1)




    def ParseMdeckCard2Btcs(self,mdcard):


        #new format for mdeck
        #
        #  0 2007090800
        #  1 09L.2007
        #  2 020
        #  3 1009
        #  4 23.5
        #  5 274.5
        #  6 -999
        #  7 -999
        #  8 360.0
        #  9 0.0
        #  10 0
        #  11 FL:
        #  12 NT
        #  13 DB
        #  14 NC
        #  15 NC
        #  16 NW
        #  17 LF:
        #  18 0.00
        #  19 TDO:
        #  20 ___
        #  21 C:
        #  22 -99.9
        #  23 -999.9
        #  24 -999
        #  25 999.9
        #  26 99.9
        #  27 ______
        #  28 W:
        #  29 -99.9
        #  30 -999.9
        #  31 -999
        #  32 999.9
        #  33 99.9
        #  34 RadSrc:
        #  35 none
        #  36 r34:
        #  37 -999
        #  38 -999
        #  39 -999
        #  40 -999
        #  41 r50:
        #  42 -999
        #  43 -999
        #  44 -999
        #  45 -999
        #  46 CP/Roci:
        #  47 9999.0
        #  48 999.0
        #  49 CRm:
        #  50 999.0
        #  51 CDi:
        #  52 999.0
        #  53 Cdpth:
        #  54 K



        tt=mdcard.split()
        ntt=len(tt)

        #for n in range(0,ntt):
        #    print 'mmmmmmm ',n,tt[n]

        i=0

        dtg=tt[i] ; i=i+1
        sid=tt[i] ; i=i+1
        bvmax=float(tt[i])  ; i=i+1
        bpmin=float(tt[i]) ; i=i+1
        blat=float(tt[i]) ; i=i+1
        blon=float(tt[i]) ; i=i+1
        r34=float(tt[i]) ; i=i+1
        r50=float(tt[i]) ; i=i+1
        bdir=float(tt[i]) ; i=i+1
        bspd=float(tt[i]) ; i=i+1
        tsnum=int(tt[i]) ; i=i+1
        dum=tt[i] ; i=i+1
        flgtc=tt[i] ; i=i+1
        flgind=tt[i] ; i=i+1
        flgcq=tt[i] ; i=i+1
        flgwn=tt[i] ; i=i+1
        dum=tt[i] ; i=i+1
        lf=float(tt[i]) ; i=i+1
        dum=tt[i] ; i=i+1
        tdo=tt[i] ; i=i+1

        if(flgtc == 'TC'):
            try:
                got1st=(len(self.firstTCdtg[sid]) == 0)
            except:
                self.firstTCdtg[sid]=dtg

        ic=21
        cqlat=float(tt[ic])  ; ic=ic+1
        cqlon=float(tt[ic])  ; ic=ic+1
        cqvmax=float(tt[ic]) ; ic=ic+1
        cqdir=float(tt[ic])  ; ic=ic+1
        cqspd=float(tt[ic])  ; ic=ic+1
        cqpmin=float(tt[ic]) ; ic=ic+1
        cqname=tt[ic]        ; ic=ic+1

        iw=29
        wlat=float(tt[iw])  ; iw=iw+1
        wlon=float(tt[iw])  ; iw=iw+1
        wvmax=float(tt[iw]) ; iw=iw+1

        if(ntt == 55):
            ir=37
            r34ne=int(tt[ir]) ; ir=ir+1
            r34se=int(tt[ir]) ; ir=ir+1
            r34sw=int(tt[ir]) ; ir=ir+1
            r34nw=int(tt[ir]) ; ir=ir+2

            r50ne=int(tt[ir]) ; ir=ir+1
            r50se=int(tt[ir]) ; ir=ir+1
            r50sw=int(tt[ir]) ; ir=ir+1
            r50nw=int(tt[ir]) ; ir=ir+2

            ir=47
            poci=float(tt[ir]) ; ir=ir+1
            roci=float(tt[ir]) ; ir=ir+2

            rmax=float(tt[ir]) ; ir=ir+2
            reye=float(tt[ir]) ; ir=ir+2
            tcdepth=tt[ir]

        else:
            r34ne=r34se=r34sw=r34nw=-999.0
            r50ne=r50se=r50sw=r50nw=-999.0

        r34quad=[r34ne,r34se,r34sw,r34nw]
        r50quad=[r50ne,r50se,r50sw,r50nw]

        if(cqdir > 720.0):
            cqdir=-999.9
            cqspd=-99.9

        # new version of btc for VD.py
        #

        btdic=[blat,blon,bvmax,bpmin,bdir,bspd]
        cqdic=[cqlat,cqlon,cqvmax,cqpmin,cqdir,cqspd]
        wndic=[wlat,wlon,wvmax]
        fldic=[flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]
        stdic=[bvmax,r34,r50,rmax,reye,poci,roci,tcdepth]

        btc=[btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]

        sbtc=[blat,blon,bvmax,bpmin]

        (stm3id,stmname)=self.getStmName3id(sid)


        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv vitals
        #


        if(cqlat > -85.0):   rlat=cqlat
        else:                rlat=blat

        if(cqlon > -360.0):  rlon=cqlon
        else:                rlon=blon

        (clat,clon)=self.rlatLon2clatLon(rlat,rlon)

        if(cqvmax > 0):   carqvmax=cqvmax*knots2ms
        else:             carqvmax=bvmax*knots2ms

        carqpoci=poci
        carqroci=roci*nm2km
        carqrmax=rmax*nm2km

        carqr34ne=r34quad[0]*nm2km
        carqr34se=r34quad[1]*nm2km
        carqr34sw=r34quad[2]*nm2km
        carqr34nw=r34quad[3]*nm2km

        if(not(tcdepth == 'S' or tcdepth == 'M' or tcdepth == 'S')): tcdepth='X'

        # go for carq dir/spd first
        #
        if(cqdir > 0 and cqdir <= 360.0):
            vitdir="%03.0f"%(cqdir)
            vitspd="%03.0f"%(cqspd*10.0*knots2ms)
        else:
            vitdir="%03.0f"%(bdir)
            vitspd="%03.0f"%(bspd*knots2ms)

        if(cqpmin > 0.0):
            vitpmin="%04d"%int(cqpmin)
        elif(bpmin > 0.0):
            vitpmin="%04d"%int(bpmin)
        else:
            pmin=-999
            vitpmin="%04d"%int(pmin)

        if(int(vitpmin) == 9999 or int(vitpmin) < 0):
            pmin=-999
            vitpmin="%04d"%int(pmin)

        if(carqpoci > 0.0 and carqpoci < 9000.0):
            vitpoci="%04d"%(mf.nint(carqpoci))
        else:
            carqpoci=-999
            vitpoci="%04d"%(carqpoci)

        if(carqroci > 0.0 and carqroci < 900.0):
            vitroci="%04d"%(mf.nint(carqroci))
        else:
            carqroci=-999
            vitroci="%04d"%(carqroci)

        if(carqvmax > 0.0):
            vitvmax="%02d"%(mf.nint(carqvmax))
        else:
            carqvmax=-9
            vitvmax="%02d"%(carqvmax)

        if(carqrmax > 0.0 and carqrmax < 900.0):
            vitrmax="%03d"%(mf.nint(carqrmax))
        else:
            carqrmax=-99
            vitrmax="%03d"%(carqrmax)

        if(carqr34ne > 0.0):
            vitr34ne="%04.0f"%(carqr34ne)
        else:
            r34ne=-999.
            vitr34ne="%04.0f"%(r34ne)

        if(carqr34se > 0.0):
            vitr34se="%04.0f"%(carqr34se)
        else:
            r34se=-999.
            vitr34se="%04.0f"%(r34se)

        if(carqr34sw > 0.0):
            vitr34sw="%04.0f"%(carqr34sw)
        else:
            r34sw=-999.
            vitr34sw="%04.0f"%(r34sw)

        if(carqr34nw > 0.0):
            vitr34nw="%04.0f"%(carqr34nw)
        else:
            r34nw=-999.
            vitr34nw="%04.0f"%(r34nw)


        vitdepth=tcdepth

        # MFTC 97S UNKNOWN   20100415 1200 083S 1017E 130 007 1010 -999 -999 08 -99 -999 -999 -999 -999 X       
        tcvitalscard="%4s %3s %-9s %8s %04d %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%\
            (centerid,stm3id,stmname,
             dtg[0:8],int(dtg[8:10])*100,
             clat,clon,
             vitdir,vitspd,
             vitpmin,
             vitpoci,vitroci,
             vitvmax,vitrmax,
             vitr34ne,vitr34se,vitr34sw,vitr34nw,
             vitdepth)



        self.append2KeyDictList(self.tcvitalsdtg,dtg,sid,tcvitalscard)

        self.stms.append(sid)

        try:
            age=mf.dtgdiff(self.firstTCdtg[sid],dtg)
        except:
            age=-999.0
        stuple=(sid,blat,blon,bvmax,bpmin,age)
        self.loadDictList(self.stmdtg,dtg,stuple)

        self.loadDictList(self.btdtgs,sid,dtg)

        try:
            self.bts[sid][dtg]=btc
        except:
            self.bts[sid]={}
            self.bts[sid][dtg]=btc

        try:
            self.sbts[sid][dtg]=sbtc
        except:
            self.sbts[sid]={}
            self.sbts[sid][dtg]=sbtc




    def scaledTCdays(self,vmax):

        tdmin=25.0
        tsmin=35.0
        tymin=65.0
        stymin=130.0

        stc=0.0
        if(vmax >= tdmin and vmax < tsmin):
            stc=0.25

        elif(vmax >= tsmin and vmax < tymin):
            dvmax=(vmax-tsmin)/(tymin-tsmin)
            stc=0.5+dvmax*0.5

        elif(vmax >= tymin and vmax < stymin):
            dvmax=(vmax-tymin)/(stymin-tymin)
            stc=1.0+dvmax*1.0

        elif(vmax >= stymin):
            stc=2.0

        return(stc)


    def getTCace(self,vmax):
        tsmin=35.0
        if(vmax >= tsmin):
            ace=vmax*vmax
        else:
            ace=0.0
        return(ace)



    def getBtGen(self,stmid,dtaubck=-24,dtaufor=12,vmaxtd=25.0,vmaxgen=30.0):

        snum=int(stmid[0:2])
        is9x=0
        if(snum >= 90 and snum <= 99): is9x=1

        bts=self.bts[stmid]

        dtgs=bts.keys()
        dtgs.sort()

        gendtgs=[]

        warndtg=None

        for dtg in dtgs:
            btc=bts[dtg]
            btdic=btc[0]
            btvmax=btdic[2]
            fldic=btc[4]
            warn=fldic[3]
            if((warn == 'WN') and (warndtg == None) and not(is9x) ):
                warndtg=dtg
                break
            elif(is9x and (btvmax >= vmaxgen)):
                warndtg=dtg
                break

        if(warndtg == None):
            self.gendtgs[stmid]=gendtgs
            return

        wndtgs=mf.dtgrange(mf.dtginc(warndtg,dtaubck+6),mf.dtginc(warndtg,dtaufor))

        gts={}

        for wndtg in wndtgs:

            try:
                btc=bts[wndtg]
            except:
                continue


            genlat=btc[0][0]
            genlon=btc[0][1]
            genvmax=btc[0][2]

            stdtgs=mf.dtgrange(mf.dtginc(wndtg,-18),wndtg)

            stdd=0.0
            nstdd=0

            for stdtg in stdtgs:

                try:
                    btc=bts[stdtg]
                    lat=btc[0][0]
                    lon=btc[0][1]
                    vmax=btc[0][2]
                except:
                    continue
                nstdd=nstdd+1
                stdd=stdd+(vmax/vmaxtd)*6.0
                #print 'sssssssssssssssssssss ',stdtg,vmax,stdd,nstdd


            if(nstdd>0):
                stdd=stdd/(nstdd*6.0)

            dt=mf.dtgdiff(warndtg,wndtg)
            genposit=(genlat,genlon,genvmax,dt,stdd)
            gentuple=(stmid,genlat,genlon,genvmax,dt,stdd)
            gendtgs.append(wndtg)
            self.appendDictList(self.gen1dtg,wndtg,gentuple)

            try:
                self.gts[stmid][wndtg]=genposit
            except:
                self.gts[stmid]={}
                self.gts[stmid][wndtg]=genposit

        self.uniqDictList(self.gen1dtg)
        self.gendtgs[stmid]=gendtgs



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#


class MdeckSimple(Mdeck):

    def __init__(self,year,mdSS,verb=0):

        # don't do year+1: yearp1=str(int(year)+1)

        # -- make/set dataset
        #
        dsDname='mdeck_stmstats'
        dsStmStat=DataSet(name=dsDname,dtype='tcmdeckdtg')
        if(mdSS == None): mdSS=dsStmStat

        try:
            self.FinalStmStats=mdSS.FinalStmStats
        except:
            self.FinalStmStats={}


        self.stms=[]
        self.bts={}

        # -- get mdecks from current year + future year for shem season
        #
        self.mds=glob.glob("%s/%s/MdOps*.txt"%(MdeckBaseDir,year))
        # don't do year+1: self.mds=self.mds+glob.glob("%s/%s/MdOps.*.txt"%(MdeckBaseDir,yearp1))

        for md in self.mds:
            (dir,file)=os.path.split(md)
            tt=file.split('.')
            stm3id=tt[1]
            stmyear=tt[2]
            stmid=tt[3]
            stmbdtg=tt[4]
            stmedtg=tt[5]
            if(verb): print 'MD: ',md,dir,file,stm3id,stmyear,stmid,stmbdtg,stmedtg

        for md in self.mds:

            try:
                for mdcard in open(md).readlines():
                    self.ParseMdeckCard2Btcs(mdcard)
            except:
                print 'EEE(MD.MdeckSimple() unable to open: ',md,' continue...'
                continue

        self.stms=self.uniq(self.stms)



    def ParseMdeckCard2Btcs(self,mdcard):

        tt=mdcard.split()
        ntt=len(tt)

        i=0

        dtg=tt[i] ; i=i+1
        sid=tt[i] ; i=i+1
        bvmax=float(tt[i])  ; i=i+1
        bpmin=float(tt[i]) ; i=i+1
        blat=float(tt[i]) ; i=i+1
        blon=float(tt[i]) ; i=i+1
        r34=float(tt[i]) ; i=i+1
        r50=float(tt[i]) ; i=i+1
        bdir=float(tt[i]) ; i=i+1
        bspd=float(tt[i]) ; i=i+1
        tsnum=int(tt[i]) ; i=i+1
        dum=tt[i] ; i=i+1
        flgtc=tt[i] ; i=i+1
        flgind=tt[i] ; i=i+1
        flgcq=tt[i] ; i=i+1
        flgwn=tt[i] ; i=i+1
        dum=tt[i] ; i=i+1
        lf=float(tt[i]) ; i=i+1
        dum=tt[i] ; i=i+1
        tdo=tt[i] ; i=i+1

        ic=21
        cqlat=float(tt[ic])  ; ic=ic+1
        cqlon=float(tt[ic])  ; ic=ic+1
        cqvmax=float(tt[ic]) ; ic=ic+1
        cqdir=float(tt[ic])  ; ic=ic+1
        cqspd=float(tt[ic])  ; ic=ic+1
        cqpmin=float(tt[ic]) ; ic=ic+1
        cqname=tt[ic]        ; ic=ic+1

        iw=29
        wlat=float(tt[iw])  ; iw=iw+1
        wlon=float(tt[iw])  ; iw=iw+1
        wvmax=float(tt[iw]) ; iw=iw+1

        if(ntt == 55):
            ir=37
            r34ne=int(tt[ir]) ; ir=ir+1
            r34se=int(tt[ir]) ; ir=ir+1
            r34sw=int(tt[ir]) ; ir=ir+1
            r34nw=int(tt[ir]) ; ir=ir+2

            r50ne=int(tt[ir]) ; ir=ir+1
            r50se=int(tt[ir]) ; ir=ir+1
            r50sw=int(tt[ir]) ; ir=ir+1
            r50nw=int(tt[ir]) ; ir=ir+2

            ir=47
            poci=float(tt[ir]) ; ir=ir+1
            roci=float(tt[ir]) ; ir=ir+2

            rmax=float(tt[ir]) ; ir=ir+2
            reye=float(tt[ir]) ; ir=ir+2
            tcdepth=tt[ir]

        else:
            r34ne=r34se=r34sw=r34nw=-999.0
            r50ne=r50se=r50sw=r50nw=-999.0

        r34quad=[r34ne,r34se,r34sw,r34nw]
        r50quad=[r50ne,r50se,r50sw,r50nw]

        if(cqdir > 720.0):
            cqdir=-999.9
            cqspd=-99.9

        # new version of btc for VD.py
        #

        btdic=[blat,blon,bvmax,bpmin,bdir,bspd]
        cqdic=[cqlat,cqlon,cqvmax,cqpmin,cqdir,cqspd]
        wndic=[wlat,wlon,wvmax]
        fldic=[flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]
        stdic=[bvmax,r34,r50,rmax,reye,poci,roci,tcdepth]

        btc=[btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]

        (stm3id,stmname)=self.getStmName3id(sid)

        self.stms.append(sid)


        try:
            self.bts[sid][dtg]=btc
        except:
            self.bts[sid]={}
            self.bts[sid][dtg]=btc


    def analyzeBt(self,mdDSs=None,
                  mdD=None,
                  mdDs=None,
                  mdDg=None,
                  verb=0):

        def sumList(list):
            sum=0
            for l in list:
                sum=sum+l
            return(sum)

        tD=TcData(mdDSs,mdD,mdDs,mdDg,verb=verb)

        stmids=self.stms
        for stmid in stmids:

            (stm3id,stmname)=tD.getStmName3id(stmid)

            btcs=self.bts[stmid]
            dtgs=btcs.keys()
            dtgs.sort()

            bdtg=dtgs[0]
            edtg=dtgs[-1]

            nd=len(dtgs)

            # stats

            Latmean=0.0
            Lonmean=0.0

            Latmin=999.
            Latmax=-999.
            Lonmin=999.0
            Lonmax=-999.0

            Vmax=-999.0

            Ace=0.0
            sTCd=0.0

            nRi=0
            nED=0
            nRd=0

            for dtg in dtgs:

                [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r5quad]=btcs[dtg]
                (blat,blon,bvmax,bpmin,bdir,bspd)=btdic
                (flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum)=fldic

                dtg24=mf.dtginc(dtg,24)

                try:
                    [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r5quad]=btcs[dtg24]
                    (blat24,blon24,bvmax24,bpmin24,bdir24,bspd24)=btdic
                    (flgtc24,flgind24,flgcq24,flgwn24,tdo24,lf24,tsnum24)=fldic
                except:
                    flgtc24=None

                if(flgtc24 != None):
                    dvmax24=None
                    if(flgtc == 'TC' and flgtc24 == 'TC'): dvmax24=bvmax24-bvmax
                    if(dvmax24 != None):
                        if(dvmax24 >= 30.0 and dvmax24 < 50.0):  nRi=nRi+1
                        if(dvmax24 >= 50.0):                     nED=nED+1
                        if(dvmax24 <= -30.0):                    nRd=nRd+1
                        #print 'DDDDDDDDDD dtg: ',dtg,' dtg24: ',dtg24,' dvmax24: ',dvmax24,bvmax,bvmax24,stmid



                if(blat < Latmin): Latmin=blat
                if(blat >= Latmax): Latmax=blat
                Latmean=Latmean+blat

                if(blon < Lonmin): Lonmin=blon
                if(blon >= Lonmax): Lonmax=blon
                Lonmean=Lonmean+blon

                if(bvmax > Vmax): Vmax=bvmax

                Ace=Ace+self.getTCace(bvmax)
                sTCd=sTCd+self.scaledTCdays(bvmax)

            Latmean=Latmean/nd
            Lonmean=Lonmean/nd

            sAceDays=Ace/(65.0*65.0)

            nhrWarn={}
            DtgwnChange={}
            NwnChange=0

            nhrTC={}
            DtgtcChange={}
            NtcChange=0

            TimePeriodsWarn=[]
            TimePeriodsTC=[]

            for n in range(1,nd):

                lastpoint=0
                dtg0=dtgs[n-1]
                [btdic0,cqdic0,wndic0,stdic0,fldic0,stdic0,r34quad0,r50quad0]=btcs[dtg0]
                if(n < nd-1):
                    dtg1=dtgs[n]
                    [btdic1,cqdic1,wndic1,stdic1,fldic1,stdic1,r34quad1,r50quad1]=btcs[dtg1]
                elif(n == nd-1 and nd > 1):
                    dtg0=dtgs[n-2]
                    dtg1=dtgs[n-1]
                    [btdic0,cqdic0,wndic0,stdic0,fldic0,stdic0,r34quad0,r50quad0]=btcs[dtg0]
                    [btdic1,cqdic1,wndic1,stdic1,fldic1,stdic1,r34quad1,r50quad1]=btcs[dtg1]
                    lastpoint=1

                (flgtc0,flgind0,flgcq0,flgwn0,tdo0,lf0,tsnum0)=fldic0
                (flgtc1,flgind1,flgcq1,flgwn1,tdo1,lf1,tsnum1)=fldic1

                if(flgwn0 == 'NW'):
                    dtgperiod=mf.dtgdiff(dtg0,dtg1)
                    MF.appendDictList(nhrWarn,NwnChange,dtgperiod)
                    dochangeWarn=0
                    if(flgwn1 != 'NW'):
                        if(not(lastpoint)): dochangeWarn=1

                if(flgwn0 == 'WN'):
                    dtgperiod=mf.dtgdiff(dtg0,dtg1)
                    MF.appendDictList(nhrWarn,NwnChange,dtgperiod)
                    dochangeWarn=0
                    if(flgwn1 != 'WN'):
                        if(not(lastpoint)): dochangeWarn=1

                if(flgtc0 == 'TC'):
                    dtgperiod=mf.dtgdiff(dtg0,dtg1)
                    MF.appendDictList(nhrTC,NtcChange,dtgperiod)
                    dochangeTC=0
                    if(flgtc1 != 'TC'):
                        if(not(lastpoint)): dochangeTC=1

                if(flgtc0 == 'NT'):
                    dtgperiod=mf.dtgdiff(dtg0,dtg1)
                    MF.appendDictList(nhrTC,NtcChange,dtgperiod)
                    dochangeTC=0
                    if(flgtc1 != 'NT'):
                        if(not(lastpoint)): dochangeTC=1

                #print 'dddddddd stmid: ',stmid,' 0: ',dtg0,flgtc0,flgwn0,' 1: ',dtg1,flgtc1,flgwn1,'9x: ',NwnChange,len(nhrWarn[NwnChange]),sumList(nhrWarn[NwnChange])
                #print 'dddddddd stmid: ',stmid,' 0: ',dtg0,flgtc0,flgwn0,' 1: ',dtg1,flgtc1,flgwn1,'9x: ',NwnChange,lastpoint
                #print 'dddddddd stmid: ',stmid,' 0: ',dtg0,flgtc0,flgwn0,' 1: ',dtg1,flgtc1,flgwn1,'9x: ',len(nhrWarn),sumList(nhrWarn[NwnChange])

                if(dochangeWarn):
                    DtgwnChange[NwnChange]=(dtg1,flgwn0,flgwn1)
                    NwnChange=NwnChange+1


                if(dochangeTC):
                    DtgtcChange[NtcChange]=(dtg1,flgtc0,flgtc1)
                    NtcChange=NtcChange+1


            ndtgwn=len(DtgwnChange)
            ndtgtc=len(DtgtcChange)

            lendtg=mf.dtgdiff(bdtg,edtg)
            lendtg=lendtg/24.0

            if(verb): 
                print '     stmid: ',stmid
                print '      bdtg: ',bdtg
                print '      edtg: ',edtg
                print '    lendtg: ',lendtg
                print '    ndtgwn: ',ndtgwn
                print '    ndtgtc: ',ndtgtc

            # -- analyze periods only if changes, could get warnings for provisionals from nhc...
            #

            if(ndtgwn > 0):

                if(verb): 
                    print
                    print ' NwnChange: ',NwnChange
                    for n in range(0,NwnChange):
                        print ' NwnChange: ',n,DtgwnChange[n]

                tothrWarn=0
                for n in range(0,NwnChange+1):
                    tothrWarn=tothrWarn+sumList(nhrWarn[n])
                    if(verb): print ' NwnChange: ',n,len(nhrWarn[n]),sumList(nhrWarn[n])

                if(verb): print 'WWWWWNNNNN: '
                totlen=0.0
                for n in range(0,NwnChange+1):
                    if(n == 0):
                        startdtg=bdtg
                        enddtg=DtgwnChange[0][0]
                        state=DtgwnChange[0][1]
                    elif(n == NwnChange):
                        startdtg=DtgwnChange[n-1][0]
                        enddtg=edtg
                        state=DtgwnChange[n-1][2]
                    else:
                        startdtg=DtgwnChange[n-1][0]
                        enddtg=DtgwnChange[n][0]
                        state=DtgwnChange[n-1][2]

                    length=sumList(nhrWarn[n])
                    length=length/24.0
                    totlen=totlen+length

                    TimePeriodsWarn.append([state,length,startdtg,enddtg])
                    if(verb): print 'WWWWWNNNNN: ',n,startdtg,enddtg,state,"%5.2f"%(length),stmid

                ndtgtc=len(DtgtcChange)
                if(verb):
                    print
                    print ' NtcChange: ',NwnChange,' Ndtgchange: ',ndtgtc

                if(verb): print 'WWWWWNNNNN: (tot) %5.2f %5.2f %s'%(lendtg,totlen,stmid),bdtg,edtg


            # -- only analyze if a TC -- exclude 90 storms...
            #

            if(ndtgtc > 0):

                totlen=0.0
                for n in range(0,NtcChange+1):
                    if(n == 0):
                        startdtg=bdtg
                        enddtg=DtgtcChange[0][0]
                        state=DtgtcChange[0][1]
                    elif(n == NtcChange):
                        startdtg=DtgtcChange[n-1][0]
                        enddtg=edtg
                        state=DtgtcChange[n-1][2]
                    else:
                        startdtg=DtgtcChange[n-1][0]
                        enddtg=DtgtcChange[n][0]
                        state=DtgtcChange[n-1][2]

                    length=sumList(nhrTC[n])
                    length=length/24.0
                    totlen=totlen+length

                    if(verb): print 'NNNNNWWWWW: ',n,startdtg,enddtg,state,"%5.2f"%(length),stmid
                    TimePeriodsTC.append([state,length,startdtg,enddtg])

                if(verb): print 'NNNNNWWWWW: (tot) %5.2f %5.2f %s'%(lendtg,totlen,stmid),bdtg,edtg

                tothrTC=0
                for n in range(0,NtcChange+1):
                    tothrTC=tothrTC+sumList(nhrTC[n])
                    if(verb): print ' NtcChange: ',n,len(nhrTC[n]),sumList(nhrTC[n])

            if(verb):
                print
                print '    lendtg: ',mf.dtgdiff(bdtg,edtg)
                print ' tothrWarn: ',tothrWarn
                print '   tothrTC: ',tothrTC



            if(verb):
                print "FFF Stmid: %s  Stmname: %s"%(stmid,stmname)
                print "FFF Latmin: %5.1f Latmax: %5.1f Latmean: %5.1f"%(Latmin,Latmax,Latmean)
                print "FFF Lonmin: %5.1f Lonmax: %5.1f Lonmean: %5.1f"%(Lonmin,Lonmax,Lonmean)
                print "FFF Vmax: %4.0f  Ace: %7.0f  sAceDays: %5.1f sTCd: %5.1f"%(Vmax,Ace,sAceDays,sTCd)
                print 'FFF nRi: ',nRi,' nED: ',nED,' nRd: ',nRd,stmid
                print "FFF TimePeriodsWarn: ",TimePeriodsWarn
                print "FFF TimePeriodsTC: ",TimePeriodsTC
                print "FFF "

            rc=(stmname,Latmin,Latmax,Latmean,Lonmin,Lonmax,Lonmean,Vmax,
                Ace,sAceDays,sTCd,
                nRi,nED,nRd,
                TimePeriodsWarn,
                TimePeriodsTC)

            self.FinalStmStats[stmid]=rc









#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded metods
#
def LsStormsDss(DSs,year=None,tstmids=None,dofilt9x=0,lsopt='s',lstype='r',verb=1):

    MF=MFutils()
    ostms=[]

    if(year == None):
        years=[]
        for tstmid in tstmids:
            years.append(tstmid.split('.')[1])

        years=MF.uniq(years)
    else:
        years=[year]


    for year in years:

        try:
            mD=DSs.db[year]
        except:
            print 'MD.LsStormsDss no data for year: ',year
            continue

        for stm in mD.stms:

            dostm=1
            stmnum=int(stm[0:2])
            if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

            if(tstmids != None):
                dostm=0
                if(type(tstmids) != ListType): tstmids=[tstmids]
                for tstmid in tstmids:
                    stmnum=int(stm[0:2])
                    if(mf.find(stm,tstmid.upper())): dostm=1
                    if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

            if(dostm): ostms.append(stm)


        for ostm in ostms:

            dtgs=mD.btdtgs[ostm]
            dtgs=mf.uniq(dtgs)
            dtgpre='    dtgs(%02d):'%(len(dtgs))

            if(lstype == 'g'):
                dtgpre=' gendtgs:'
                dtgs=mD.gendtgs[ostm]
                dtgs=mf.uniq(dtgs)

            if(lsopt == 's'):
                dtgstr='%s %s'%(dtgpre,MF.makeDtgsString(dtgs))
                card='stmid: %s'%(ostm)+dtgstr
                print card

            if(lsopt == 'l'):
                dtgstr='%s %s'%(dtgpre,MF.makeDtgsString(dtgs,osiz=256,ndtg=50))
                card='stmid: %s'%(ostm)+dtgstr
                print card


    return(ostms)


