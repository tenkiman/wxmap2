#!/usr/bin/env python

"""%s

purpose:

  output TC positions to standard output for a given dtg or range of dtgs

usages:

  %s dtg -O -o opath
  %s dtgb.dtge -n ngpath      # range of dtgs

  %s cur -s 01L.2005          # run TC.findtc for mdecks by storm

-O - ops
-C - write to w2/dat/tc/carq dtg-by-dtg

-h - help
-n - ngpath      :: PATH to write the nogaps tracker input 'ngtrp' cards
-o - opath       :: PATH to write cards printed to screen
-b - tcbogpath   :: PATH with tcobg cards
-v - vitalspath  :: PATH with tcvitals

-T - only output tcs -- exclude SD SS
-S - srcopt [btops (btops card = mdcards) | 'mdeck'
-l - ls options: 'l' long 
-B - only NN storms

examples:

%s cur -n /tmp/ngtrp.cur.txt
%s                  -- sets dtgopt = 'cur-24.cur'
"""

from tcbase import *
bddir=None

#
#  defaults
#

dtgopt='cur-24.cur'
stmopt=None
prcopt='null'
carqopt=opsopt=map9xopt=None
dofilt9x=0
verb=0
ngpath=tcbogpath=mopath=opath=tcvitalspath='null'
dohelp=0
srcopt='btops'

tconly=0
lsopt=None

dodtgs=0
doradiionly=0

tcpyppath="/tmp/tc.pyp"

curdtg=mf.dtg()
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1

#
# options using getopt
#

if(narg >= 0):

    istart=2
    ### huh?  if(mf.find(dtgopt,'-')): istart=1

    if(narg >= 1):
        dtgopt=sys.argv[1]

        if(dtgopt == '-h'):
            dohelp=1

        ldd=len(dtgopt.split('.'))
        if(ldd > 1):
            bdtg=mf.dtg_command_prc(dtgopt.split('.')[0],quiet=0)
            if(bdtg == -1 or bdtg < 4):
                stmopt=dtgopt
                dtgopt=None
            else:
                dodtgs=1
                dtgoptin=dtgopt

        else:

            bdtg=mf.dtg_command_prc(dtgopt,quiet=0)
            if(bdtg == -1):
                dodtgs=0
                dtgoptin=dtgopt

                stmopt=dtgopt
                dtgopt=None

            elif(bdtg > 1):
                dodtgs=1

    if(dtgopt != None):
        ldd=len(dtgopt.split('.'))
        dodtgs=1
        dtgoptin=dtgopt
    else:
        ldd=0

    if(dtgopt == '-s'):
        istart=1
    else:
        if(ldd == 1):
            (dtgm0,phr)=mf.dtg_phr_command_prc(dtgopt)

    try:
        (opts, args) = getopt.getopt(sys.argv[istart:], "p:s:v:n:S:o:b:OCTVMl:9RZ")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-p",""): prcopt=a
        if o in ("-s",""): stmopt=a
        if o in ("-n",""): ngpath=a
        if o in ("-b",""): tcbogpath=a
        if o in ("-v",""): tcvitalspath=a
        if o in ("-S",""): srcopt=a
        if o in ("-o",""): opath=a
        if o in ("-O",""): opsopt=1
        if o in ("-C",""): carqopt=1
        if o in ("-T",""): tconly=1
        if o in ("-V",""): verb=1
        if o in ("-M",""): map9xopt=1
        if o in ("-l",""): lsopt=a
        if o in ("-9",""): dofilt9x=1
        if o in ("-R",""): doradiionly=1


else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

if(dohelp):
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

from WxMAP2 import W2
w2=W2()


if(narg == 0):
    print "NB: %s -h for help -----------------------------------------------------------"%(pyfile)
    dtgopt='cur-24.cur'

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

if(lsopt == None):
    lsopt='s' 
    ncharmax=117
elif(lsopt == 'l'):
    ncharmax=310


if(stmopt != None):
    stmids=MakeStmList(stmopt)
    stmopt=stmids[0]

if(not(dtgopt) and stmopt == None):
    print 'EEE must define dtgopt using 1st command line arg'
    sys.exit()

if(dodtgs):
    dtgs=mf.dtg_dtgopt_prc(dtgoptin)

#
# turn on ops if doing carq
#
if(carqopt or map9xopt):
    opsopt=1

source=srcopt
if(opsopt):
    source='mdeck'
    dofilt9x=0

if(srcopt == 'bt'):
    enddesc=' #TS'
else:
    enddesc=" u mot  v mot"
    
desc="YYYYMMDDHH   stm   vmax pmin   lat   lon  r30  r50  head   spd %s"%(enddesc)

ncards=0

ngtrpcards=[]
tcbogcards=[]
tcvitalscards=[]
printcards=[]
xtermcards=[]

#
# by stm ------------- old/new method -- use mdecks
#

class Radii:
    r34=[]
    r50=[]
    rmax=[]


if(stmopt != None and dodtgs == 0):

    if(doradiionly):

        Rs=Radii()

        for stmid in stmids:
            bts=GetBtRadii(stmid,Rs)

        PS=open(tcpyppath,'w')
        tcpyp=(stmids,Rs.r34,Rs.r50,Rs.rmax)
        pickle.dump(tcpyp,PS)
        PS.close()

        print len(Rs.rmax)



    else:

        #mcards=TC.findtc(stmopt,dofilt9x=1,srcopt=source,verb=verb)
        mcards=findMdeckTC(stmopt)

        dtgs=mcards.keys()
        dtgs.sort()

        for dtg in dtgs:
            mcard=copy.copy(mcards[dtg])
            tt=mcard.split()
            lon=tt[5].strip()
            wlon=FormatLon(float(lon))
            mcard=mcard.replace(lon,wlon,1)
            mcard=mcard.replace('-999.9','------')
            mcard=mcard.replace('-999','----')
            #
            #logic that insures the lon is always the same length on output
            # 
            nlon=len(lon)
            nwlon=len(wlon)
            if(nlon < nwlon-1):
                plon=mcard.find(lon)
                mcard=mcard[0:plon-1]+mcard[plon:]
            print "%s "%(mcard[0:ncharmax])

    sys.exit()


#
# dtg-by-dtg
#
else:

    cnt=0
    for dtg in dtgs:

        tcs=[]
        otcs=[]

        curdtg=mf.dtg6()
        otcs=findtcs(dtg,dofilt9x,source,verb=verb)

        cnt=cnt+1
        if(cnt%60 == 0):
            print 'w2-tc-posit-mdeck: ',dtg,dofilt9x,source,len(otcs)

        for otc in otcs:
            tt=otc.split()
            if(tconly and IsTcList(tt) == 0):
                continue
            else:
                tcs.append(otc)

        ntcs=len(tcs)

        if(ntcs == 0):
            continue

        ngtrpcard="%d  %s     at %s  902841"%(int(ntcs),dtg[2:10],curdtg[0:8])
        ngtrpcards.append(ngtrpcard)


        if(carqopt != None or map9xopt != None):
            printcards=[]


        printcards.append(' ')
        xtermcards.append(' ')

        for tc in tcs:

#nnn 0 2007103100
#nnn 1 16L.2007
#nnn 2 035
#nnn 3 1002
#nnn 4 21.2
#nnn 5 282.1
#nnn 6 37
#nnn 7 -999
#nnn 8 283.4
#nnn 9 4.3
#nnn 10 11
#nnn 11 FL:
#nnn 12 TC
#nnn 13 TS
#nnn 14 CQ
#nnn 15 WN
#nnn 16 LF:
#nnn 17 0.71
#nnn 18 TDO:
#nnn 19 RJP
#nnn 20 C:
#nnn 21 21.2
#nnn 22 282.1
#nnn 23 35
#nnn 24 305.0
#nnn 25 4.0
#nnn 26 1002
#nnn 27 NOEL
#nnn 28 W:
#nnn 29 -99.9
#nnn 30 -999.9
#nnn 31 -999
#nnn 32 999.9
#nnn 33 99.9
#nnn 34 RadSrc:
#nnn 35 carq
#nnn 36 r34:
#nnn 37 150
#nnn 38 0
#nnn 39 0
#nnn 40 0
#nnn 41 r50:
#nnn 42 -999
#nnn 43 -999
#nnn 44 -999
#nnn 45 -999
#nnn 46 CP/Roci:
#nnn 47 1008.0
#nnn 48 180.0
#nnn 49 CRm:
#nnn 50 90.0
#nnn 51 CDi:
#nnn 52 0.0
#nnn 53 Cdpth:
#nnn 54 M
            tt=tc.split()

            #for n in range(0,len(tt)):
            #    print 'nnnnnnnn ',n,tt[n]

            if(len(tt) == 0): continue
            dtg=tt[0]
            stmid=tt[1]
            vmax=tt[2]
            lat=tt[4]
            lon=tt[5]
            dir=tt[8]
            spd=tt[9]
            carqdir=float(tt[24])
            carqspd=float(tt[25])
            carqpmin=float(tt[26])
            carqname=tt[27]
            rdir=float(dir)
            rspd=float(spd)
            pmin=tt[3]
            r30=float(tt[6])
            r50=float(tt[7])

            carqpoci=float(tt[47])
            carqroci=float(tt[48])*nm2km

            carqvmax=float(vmax)*knots2ms
            carqrmax=float(tt[50])*nm2km

            carqr34ne=float(tt[37])*nm2km
            carqr34se=float(tt[38])*nm2km
            carqr34sw=float(tt[39])*nm2km
            carqr34nw=float(tt[40])*nm2km

            carqdepth=tt[54]
            if(not(carqdepth == 'S' or carqdepth == 'M' or carqdepth == 'S')):
                carqdepth='X'

            xtermtc=copy.copy(tc)
            wlon=FormatLon(float(lon)).strip()
            wlon=FormatLon(float(lon))
            xtermtc=xtermtc.replace(lon,wlon,1)
            xtermtc=xtermtc.replace('-999.9','------')
            xtermtc=xtermtc.replace('-999','----')
            nlon=len(lon)
            nwlon=len(wlon)
            if(nlon < nwlon-1):
                plon=xtermtc.find(lon)
                xtermtc=xtermtc[0:plon-1]+xtermtc[plon:]


            rlat0=float(lat)
            ihemns='N'
            if(rlat0<0.0):
                ihemns='S'
                rlat=rlat0*(-1.0)
            else:
                rlat=rlat0
            rlat=rlat*10
            clat="%03.0f%s"%(rlat,ihemns)

            rlon0=float(lon)

            ihemew='E'
            if(rlon0>180.0):
                ihemew='W'
                rlon=360.0-rlon0
            elif(rlon0<=0.0):
                ihemew='E'
                rlon=360.0+rlon0
            else:
                rlon=rlon0

            if(rlon < 0.0):
                ihemew='E'
                rlon=abs(rlon)

            rlon=rlon*10

            clon="%04.0f%s"%(rlon,ihemew)

            cdir="%04.0f"%(rdir*10)
            cspd="%03.0f"%(rspd*10)
            umean=0.0
            vmean=0.0


            #
            # use rhumb line to find u/v motion for tcgob
            #
            dt=-12
            (rlat1,rlon1)=rumltlg(rdir,rspd,dt,rlat0,rlon0)
            dt=12
            (rcourse,rspeed,umotion,vmotion)=rumhdsp(rlat1,rlon1,rlat0,rlon0,dt)


            ngtrpcard="%s %s %s %2s %1s -999 -999 %s %s"%\
                (clat,clon,vmax,stmid[0:2],stmid[2:3],cdir,cspd)

            tcbogcard="%s %s %3i %4i%6.1f%6.1f%5i%5i %5.1f %5.2f%7.2f%7.2f"%\
                (dtg,stmid.split('.')[0],
                 int(vmax),int(pmin),
                 float(lat),float(lon),
                 int(r50),int(r30),
                 rdir,rspd,
                 umotion,vmotion)




            #
            # go for carq dir/spd first
            #
            if(carqdir <= 360.0):
                vitdir="%03.0f"%(carqdir)
                vitspd="%03.0f"%(carqspd*10.0*knots2ms)
            else:
                vitdir="%03.0f"%(rdir)
                vitspd="%03.0f"%(rspd*knots2ms)

            if(carqpmin > 0.0):
                vitpmin="%04d"%int(carqpmin)
            elif(pmin > 0.0):
                vitpmin="%04d"%int(pmin)
            else:
                pmin=-999
                vitpmin="%04d"%int(pmin)

            if(int(vitpmin) == 9999 or int(vitpmin) < 0):
                pmin=-999
                vitpmin="%04d"%int(pmin)

            if(carqpoci > 0.0 and carqpoci < 9000.0):
                vitpoci="%04d"%(mf.nint(carqpoci))
            else:
                poci=-999
                vitpoci="%04d"%(poci)

            if(carqroci > 0.0 and carqroci < 900.0):
                vitroci="%04d"%(mf.nint(carqroci))
            else:
                roci=-999
                vitroci="%04d"%(roci)


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


            vitdepth=carqdepth


            #tcard='NHC  16L NOEL      20071031 0000 212N 0779W 305 021 1002 1008 0334 18 167 0278 -999 -999 -999 M'

            centerid='MFTC'
            stm3id=stmid.split('.')[0]
            stmyear=stmid.split('.')[1]
            tcnames=GetTCnamesHash(stmyear)
            try:
                stmname=tcnames[stmyear,stm3id][0:9]
            except:
                stmname='unknown  '.upper()

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


            #        read(26,602,end=100)
            #     $       cdtg,istmno(i),ibsn(i),
            #     $       imaxv,ipmin,slat(i),slon(i),ir50,ir30,
            #     $       rdir,rspd,umean(i),vmean(i)
            # 602    format(a,1x,i2,a1,1x,
            #     $       i3,1x,i4,2(f6.1),2i5,1x,
            #     $       f5.1,1x,f5.2,2f7.2)
            #print "1987090700 04L 030 1009  21.3 322.2  -99  -99 032.0 08.87 004.79 007.46"

            printcard=tc[0:]
            xtermcard="%9s %s"%(carqname,xtermtc[0:])
            xtermcard=xtermcard.replace('-999.9','------')
            xtermcard=xtermcard.replace('-999','----')
            ngtrpcards.append(ngtrpcard)
            tcbogcards.append(tcbogcard)
            tcvitalscards.append(tcvitalscard)
            printcards.append(printcard)
            xtermcards.append(xtermcard)


        if(carqopt != None):

            yyyy=dtg[0:4]
            tdir="%s/%s"%(w2.TcCarqDatDir,yyyy)
            mf.ChkDir(tdir,'mk')

            btopspath="%s/btops.%s.txt"%(tdir,dtg)
            print 'CARQ btops for: ',btopspath

            try:
                o=open(btopspath,'w')
            except:
                print "EEE unable to create: %s"%(btopspath)
                sys.exit()

            for card in printcards:
                if(len(card) > 2):
                    if(verb): print card
                    card=card+"\n"
                    o.writelines(card)

        if(map9xopt != None):

            yyyy=dtg[0:4]
            tdir="%s/%s"%(w2.TcCarqDatDir,yyyy)
            mf.ChkDir(tdir,'mk')

            #map9x=GetMap9x(dtg)
            map9x=GetMap9xDtg(dtg)
            if(len(map9x) == 0):
                print 'NO map9x for: ',dtg
                continue

            map9xpath="%s/map9xs.%s.txt"%(tdir,dtg)
            print 'CARQ map9x for: ',map9xpath

            map9xcards=[]
            kk=map9x.keys()
            kk.sort()
            for k in kk:
                map9xcards.append("%s %s"%(k,map9x[k]))
                if(verb): print 'map 9X -> [0-4]? ',k,map9x[k]

            try:
                o=open(map9xpath,'w')
            except:
                print "EEE unable to create: %s"%(map9xpath)
                sys.exit()

            for card in map9xcards:
                if(len(card) > 2):
                    if(verb): print card
                    card=card+"\n"
                    o.writelines(card)

            o.close()

    if((carqopt == None and map9xopt == None) and ngpath == 'null' and tcvitalspath == 'null'):
        for card in xtermcards:
            print card[0:ncharmax]

    #
    # ngtrp file output
    #

    if(mopath != 'null'):

        try:
            n=open(mopath,'w')
        except:
            print "EEE unable to create: %s"%(mopath)
            sys.exit()

        for card in printcards:
            if(verb): print card
            card=card+"\n"
            n.writelines(card)

        n.close()

    elif(opath != 'null'):

        try:
            o=open(opath,'w')
        except:
            print "EEE unable to create: %s"%(opath)
            sys.exit()

        for card in printcards:
            if(verb): print card
            card=card+"\n"
            o.writelines(card)

        o.close()

    elif(ngpath != 'null'):

        ncards=len(ngtrpcards)
        if(ncards == 0):
            sys.exit()

        try:
            n=open(ngpath,'w')
        except:
            print "EEE unable to create: %s"%(ngpath)
            sys.exit()


        for card in ngtrpcards:
            if(verb): print card
            card=card+"\n"
            n.writelines(card)

        n.close()

    elif(tcbogpath != 'null'):

        ncards=len(tcbogcards)
        if(ncards == 0):
            sys.exit()

        try:
            n=open(tcbogpath,'w')
        except:
            print "EEE unable to create: %s"%(tcbogpath)
            sys.exit()


        for card in tcbogcards:
            if(verb): print 'tcbog: ',card
            card=card+"\n"
            n.writelines(card)

        n.close()

    elif(tcvitalspath != 'null'):

        ncards=len(tcvitalscards)
        if(ncards == 0):
            sys.exit()

        try:
            n=open(tcvitalspath,'w')
        except:
            print "EEE unable to create: %s"%(tcvitalspath)
            sys.exit()


        for card in tcvitalscards:
            if(verb): print 'tcvitals: ',card
            card=card+"\n"
            n.writelines(card)

        n.close()

    elif(carqopt == 'null'):

        #
        # stdout (only when not writing a ngtrp)
        #

        for cards in printcards:
            print cards[0:ncharmax]





sys.exit()
