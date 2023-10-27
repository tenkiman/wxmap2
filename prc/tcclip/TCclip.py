''' TC liper forecasts '''

from tcbase import *
import jclip
import nclip

verb=0

def BtOps2Stm(stmids,stmdata,stmmotion,stmidset,btops):

#new format for mdeck
#nnnn  0 2007103112
#nnnn  1 96W.2007
#nnnn  2 015
#nnnn  3 1010
#nnnn  4 17.2
#nnnn  5 138.6
#nnnn  6 -999
#nnnn  7 -999
#nnnn  8 254.7
#nnnn  9 11.4
#nnnn  10 0
#nnnn  11 FL:
#nnnn  12 NT
#nnnn  13 DB
#nnnn  14 NC
#nnnn  15 NW
#nnnn  16 LF:
#nnnn  17 0.00
#nnnn  18 TDO:
#nnnn  19 ___
#nnnn  20 C:
#nnnn  21 -99.9
#nnnn  22 -999.9
#nnnn  23 -999
#nnnn  24 999.9
#nnnn  25 99.9
#nnnn  26 -999
#nnnn  27 ______
#nnnn  28 W:
#nnnn  29 -99.9
#nnnn  30 -999.9
#nnnn  31 -999
#nnnn  32 999.9
#nnnn  33 99.9
#nnnn  34 RadSrc:
#nnnn  35 none
#nnnn  36 r34:
#nnnn  37 -999
#nnnn  38 -999
#nnnn  39 -999
#nnnn  40 -999
#nnnn  41 r50:
#nnnn  42 -999
#nnnn  43 -999
#nnnn  44 -999
#nnnn  45 -999
#nnnn  46 CP/Roci:
#nnnn  47 9999.0
#nnnn  48 999.0
#nnnn  49 CRm:
#nnnn  50 999.0
#nnnn  51 CDi:
#nnnn  52 999.0
#nnnn  53 Cdpth:
#nnnn  54 K

    verb=0

    gotstmid=0


    for mdcard in btops:
        
        btc=ParseMdeckCard2Btcs(mdcard)
        
        [blat,blon,bvmax,bpmin,
         bdir,bspd,
         btdic,cqdic,bwdic,r34quad,r50quad]=btc

        [cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]=cqdic
        
        tt=mdcard.split()
        b2=tt[0]
        stid=tt[1].split('.')[0]
        stmid=tt[1]
        stmdtg=tt[0]

        if(cqlat > -88. and cqlat < 88.):
            stmrlat=cqlat
            stmrlon=cqlon
        else:
            stmrlat=blat
            stmrlon=blon

        if(cqvmax > 0.):
            stmvmax=cqvmax
        else:
            stmvmax=bvmax

        if(cqpmin > 0.):
            stmpmin=cqpmin
        else:
            stmpmin=bpmin

        if(cqspd > 0.):
            course=cqdir
            speed=cqspd
        else:
            course=bdir
            speed=bspd

        #
        # detect of storms available when setting by command line input
        #
        
        if(stmidset == 'all'): gotstmid=1

        if(stmidset != 'all'):
            if(stmid == stmidset):
                gotstmid=1
            else:
                if(gotstmid == 1):
                    continue
                else:
                    gotstmid=0
                    continue
                
        
        stmids.append(stmid)
        
        stmmotion[stmid,'motion']=(course,speed)

        stmdata[stmid,'posit']=(stmdtg,stmrlat,stmrlon,stmvmax,stmpmin)


        ndx=37
        try:
            r34ne=int(tt[ndx]) ; ndx=ndx+1
            r34se=int(tt[ndx]) ; ndx=ndx+1
            r34sw=int(tt[ndx]) ; ndx=ndx+1
            r34nw=int(tt[ndx]) ; ndx=ndx+1

            ndx=ndx+1
            r50ne=int(tt[ndx]) ; ndx=ndx+1
            r50se=int(tt[ndx]) ; ndx=ndx+1
            r50sw=int(tt[ndx]) ; ndx=ndx+1
            r50nw=int(tt[ndx]) ; ndx=ndx+1
            
        except:
            
            r34quad=r50quad=None


        ndx=ndx+1
        
        try:
            stmdata[stmid,'r34']=('NEQ',r34ne,r34se,r34sw,r34nw)
        except:
            stmdata[stmid,'r34']=('NA',999,999,999,999)

        try:
            stmdata[stmid,'r50']=('NEQ',r50ne,r50se,r50sw,r50nw)
        except:
            stmdata[stmid,'r50']=('NA',999,999,999,999)

        try:
            stmdata[stmid,'roci']=(int(float(tt[ndx])),int(float(tt[ndx+1])))
        except:
            stmdata[stmid,'roci']=('NA',999)

        ndx=ndx+3

        try:
            stmdata[stmid,'rmax']=(int(float(tt[ndx])))
        except:
            stmdata[stmid,'rmax']=('NA')

        ndx=ndx+2
            
        try:
            stmdata[stmid,'deye']=int(float(tt[ndx]))
        except:
            stmdata[stmid,'deye']=('NA')


    return(gotstmid)



def ParseCarqStorms(dtg,stmidset='all'):

    verb=0
    ropt='quiet'
    
    pdir=w2.PrcDirTcdatW2
    carqsource='CARQ'
       

    #
    # this is very expensive
    # added wxmap.tc.grep*py to c.wg.d to create on a dtg-dtg basis
    #
    yyyy=dtg[0:4]
    cgdir="%s/%s"%(w2.TcCarqDatDir,yyyy)
    cqdtgpath="%s/carq.%s.txt"%(cgdir,dtg)
    if(os.path.exists(cqdtgpath)):
        cmd="grep -h '%s,   0,' %s "%(carqsource,cqdtgpath)
        cmdm12="grep -h '%s, -12,' %s "%(carqsource,cqdtgpath)
    else:
        #
        # run the grep .py
        #
        
        cmdgrep="%s/w2.tc.grep.carq.tcstruct.py %s"%(pdir,dtg)
        mf.runcmd(cmdgrep,ropt)
        
        if(os.path.exists(cqdtgpath)):
            print 'had to regen... ',cqdtgpath
            cmd="grep -h '%s,   0,' %s "%(carqsource,cqdtgpath)
            cmdm12="grep -h '%s, -12,' %s "%(carqsource,cqdtgpath)
        else:
            print 'EEE failure in redo carq grep for ',cqdtgpath
            sys.exit()

    if(verb): print 'CCC: ',cmd
    carq=os.popen(cmd).readlines()
    carqm12=os.popen(cmdm12).readlines()

    ncarq=len(carq)

    if(ncarq == 0):
        print 'No adeck TCs for : ',dtg
        stmids=['nocarq']
        stmdata={}
        stmmotion={}
        return(stmids,stmdata,stmmotion)

    stmdata={}
    stmids=[]

    gotstmid=Carq2Stm(stmids,stmdata,stmidset,carq)

    #
    # 20030326 -- only 8X storms
    #

    if(gotstmid == 0 and ncarq != 0):
        print 'No non 8X TCs for : ',dtg
        stmids=['nocarq']
        stmdata={}
        stmmotion={}
        return(stmids,stmdata,stmmotion)

    if(gotstmid == 0): sys.exit()

    stmids=mf.uniq(stmids)

    stmdatam12={}
    stmidsm12=[]

    stmmotion={}

    gotstmidm12=Carq2Stm(stmidsm12,stmdatam12,stmidset,carqm12)

    for stmid in stmids:
        
        (stmdtg,stmclat,stmclon,stmvmax,stmpmin)=stmdata[stmid,'posit']

        try:
            (stmdtgm12,stmclatm12,stmclonm12,stmvmaxm12,stmpminm12)=stmdatam12[stmid,'posit']
        except:
            (stmdtgm12,stmclatm12,stmclonm12,stmvmaxm12,stmpminm12)=('NA',999,999,999,999)


        if(stmdtgm12 != 'NA'):
            
            (rlat1,rlon1)=Clatlon2Rlatlon(stmclat,stmclon)
            (rlat0,rlon0)=Clatlon2Rlatlon(stmclatm12,stmclonm12)

            if(verb):
                print "SSS    ",stmdtg,stmclat,stmclon,stmvmax,stmpmin
                print "SSSm12 ",stmdtgm12,stmclatm12,stmclonm12,stmvmaxm12,stmpminm12
                print "SSS    ",rlat0,rlon0,rlat1,rlon1

            dtbase=12
            (icourse,ispeed,iumotion,ivmotion)=mf.rumhdsp(rlat0,rlon0,rlat1,rlon1,dtbase)
            
        else:

            (icourse,ispeed,iumotion,ivmotion)=(999,999,999,999)
            
        stmmotion[stmid,'motion']=(icourse,ispeed,iumotion,ivmotion)
            
        if(verb): print "SSS    ",icourse,ispeed,iumotion,ivmotion

    return(stmids,stmdata,stmmotion)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# parse abdecks data in btops from w2.tc.posit.py DTG -C -O
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc



def LoadStmData(n,stmids,stmdata,stmmotion,stmids1,stmdata1,stmmotion1):

    stm=stmids1[n]
    stmids.append(stm)
    stmdata[stm,'posit']=stmdata1[stm,'posit']
    stmdata[stm,'r34']=stmdata1[stm,'r34']
    stmdata[stm,'r50']=stmdata1[stm,'r50']
    stmdata[stm,'roci']=stmdata1[stm,'roci']
    stmdata[stm,'rmax']=stmdata1[stm,'rmax']
    stmmotion[stm,'motion']=stmmotion1[stm,'motion']

    return
        
def ParseBdeckStorms(dtg,stmidset='all'):

    verb=0
    
    if(verb):
        ropt=''
    else:
        ropt='quiet'

    pdir=w2.PrcDirTcdatW2

    bdecksource='BEST'

    dtgm12=mf.dtginc(dtg,-12)

    #
    # this is very expensive
    # added wxmap.tc.grep*py to c.wg.d to create on a dtg-dtg basis
    #
    yyyy=dtg[0:4]
    cgdir="%s/%s"%(w2.TcCarqDatDir,yyyy)

    bddtgpath="%s/bdeck.%s.txt"%(cgdir,dtg)
    
    if(os.path.exists(bddtgpath) == 1):
        cmd="grep -h '%s,' %s "%(dtg,bddtgpath)
        cmdm12="grep -h '%s,' %s "%(dtgm12,bddtgpath)

    else:

        #
        # run the grep .py
        #
        
        cmdgrep="%s/w2.tc.grep.bdeck.tcstruct.py %s"%(pdir,dtg)
        mf.runcmd(cmdgrep,ropt)
        
        if(os.path.exists(bddtgpath)):
            print 'had to regen... ',bddtgpath
            cmd="grep -h '%s,   0,' %s "%(bdecksource,bddtgpath)
            cmdm12="grep -h '%s, -12,' %s "%(bdecksource,bddtgpath)
        else:
            print 'EEE failure in redo carq grep for ',bddtgpath
            sys.exit()

    if(verb): print 'CCC: ',cmd
    bdeck=os.popen(cmd).readlines()
    bdeckm12=os.popen(cmdm12).readlines()

    nbdeck=len(bdeck)

    if(nbdeck == 0):
        print 'No bdeck TCs for : ',dtg
        stmids=[]
        stmdata={}
        stmmotion={}
        return(stmids,stmdata,stmmotion)

    stmdata={}
    stmids=[]

    gotstmid=Bdeck2Stm(stmids,stmdata,stmidset,bdeck)

    if(gotstmid == 0): sys.exit()

    stmids=mf.uniq(stmids)

    stmdatam12={}
    stmidsm12=[]

    stmmotion={}

    gotstmidm12=Bdeck2Stm(stmidsm12,stmdatam12,stmidset,bdeckm12)

    for stmid in stmids:
        
        (stmdtg,stmclat,stmclon,stmvmax,stmpmin)=stmdata[stmid,'posit']

        try:
            (stmdtgm12,stmclatm12,stmclonm12,stmvmaxm12,stmpminm12)=stmdatam12[stmid,'posit']
        except:
            (stmdtgm12,stmclatm12,stmclonm12,stmvmaxm12,stmpminm12)=('NA',999,999,999,999)


        if(stmdtgm12 != 'NA'):
            
            (rlat1,rlon1)=Clatlon2Rlatlon(stmclat,stmclon)
            (rlat0,rlon0)=Clatlon2Rlatlon(stmclatm12,stmclonm12)

            if(verb):
                print "SSS    ",stmdtg,stmclat,stmclon,stmvmax,stmpmin
                print "SSSm12 ",stmdtgm12,stmclatm12,stmclonm12,stmvmaxm12,stmpminm12
                print "SSS    ",rlat0,rlon0,rlat1,rlon1

            dt=12
            (icourse,ispeed,iumotion,ivmotion)=mf.rumhdsp(rlat0,rlon0,rlat1,rlon1,dt)
            
        else:

            IcourseDefault=270
            IspeedDefault=15
            
            (icourse,ispeed,iumotion,ivmotion)=(IcourseDefault,IspeedDefault,999,999)
            
        stmmotion[stmid,'motion']=(icourse,ispeed,iumotion,ivmotion)
            
        if(verb): print "SSS final    ",icourse,ispeed,iumotion,ivmotion

    return(stmids,stmdata,stmmotion)


def ParseBtOpsStorms(dtg,stmidset='all'):

    verb=1
    
    if(verb):
        ropt=''
    else:
        ropt='quiet'

    pdir=w2.PrcDirTcdatW2

    #
    # this is very expensive
    # added wxmap.tc.grep*py to c.wg.d to create on a dtg-dtg basis
    #
    yyyy=dtg[0:4]
    cgdir="%s/%s"%(w2.TcCarqDatDir,yyyy)

    bddtgpath="%s/btops.%s.txt"%(cgdir,dtg)

    if(os.path.exists(bddtgpath) == 0):
        
        #
        # run the btops using w2.tc.posit.py
        #

        cmd="%s/w2.tc.posit.py %s -C -O"%(pdir,dtg)
        mf.runcmd(cmd,ropt)
        
        if(os.path.exists(bddtgpath)):
            print 'Tried to to regen... ',bddtgpath
        else:
            print 'no TCs for dtg: ',dtg,'return blanks...'
            stmdata={}
            stmids=[]
            stmmotion={}
            return(stmids,stmdata,stmmotion)

    bdeck=open(bddtgpath,'r').readlines()

    nbdeck=len(bdeck)

    if(nbdeck == 0):
        print 'No bdeck TCs for : ',dtg
        stmids=[]
        stmdata={}
        stmmotion={}
        return(stmids,stmdata,stmmotion)

    stmdata={}
    stmids=[]
    stmmotion={}

    gotstmid=BtOps2Stm(stmids,stmdata,stmmotion,stmidset,bdeck)

    if(gotstmid == 0): sys.exit()

    return(stmids,stmdata,stmmotion)


def SetTcanalDirs(dtg,realtime=0):

    yyyy=dtg[0:4]

    cdir=w2.TcAdecksJtwcDir
    bdir=w2.TcTcanalDatDir
    if(realtime):
        bdir=w2.TcTcanalDatDirRT
    
    prcddir=w2.PrcDirTcdatW2

    odir="%s/%s/%s"%(bdir,yyyy,dtg)
    mf.ChkDir(odir,'mk')
    
    ogdir="%s/plt"%(odir)
    osdir="%s/stt"%(odir)
    otdir="%s/trk"%(odir)
    oddir="%s/dat"%(odir)
    opdir="%s/prc"%(odir)

    #
    # change target to adeck dir, this was how it was set up at jtwc
    #
    #oadir="%s/%s"%(w2.TcAtcfDatDir,yyyy)
    oadir="%s/%s"%(w2.TcAdecksLocalDir,yyyy)
    mf.ChkDir(oadir,'mk')

    pdir=w2.PrcDirTcanalW2
    wpddir=w2.PrcDirFlddatW2
    wgddir=w2.GeogDatDirW2

    #
    # check if output dir and output plt stat dir are there; if not mkdir
    #

    if not(os.path.isdir(odir)):
        print "odir: ",odir," is not there -- mkdir"
        os.mkdir(odir)

    if not(os.path.isdir(ogdir)):
        print "ogdir: ",ogdir," is not there -- mkdir"
        os.mkdir(ogdir)

    if not(os.path.isdir(osdir)):
        print "osdir: ",osdir," is not there -- mkdir"
        os.mkdir(osdir)

    if not(os.path.isdir(otdir)):
        print "otdir: ",otdir," is not there -- mkdir"
        os.mkdir(otdir)

    if not(os.path.isdir(oddir)):
        print "oddir: ",oddir," is not there -- mkdir"
        os.mkdir(oddir)

    if not(os.path.isdir(opdir)):
        print "opdir: ",opdir," is not there -- mkdir"
        os.mkdir(opdir)


    
    rc=(cdir,bdir,prcddir,
        odir,ogdir,osdir,otdir,oddir,opdir,
        oadir,pdir,
        wpddir,wgddir)


    return(rc)


def NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin,
              latm12=None,lonm12=None,
              latm24=None,lonm24=None,
              cq12dir=None,cq12spd=None,
              verb=0):

    if(latm12 == None):
        (latm12,lonm12)=rumltlg(dir,spd,-12.0,lat0,lon0)
    if(latm24 == None):
        (latm24,lonm24)=rumltlg(dir,spd,-24.0,lat0,lon0)

    # convert lon to deg W for input

    lon0w=360.0-lon0
    lonm12w=360.0-lonm12
    lonm24w=360.0-lonm24
    
    if(cq12dir == None):
        dirm12=dir
        spdm12=spd
    else:
        dirm12=cq12dir
        spdm12=cq12spd

    if(basin == 'EPC'):
        if(verb): print "EEEEEEEEEEEEEEE"
        nclip.epcl84(idtg,lat0,lon0w,latm12,lonm12w,latm24,lonm24w,dir,spd,vmax,sid)

    elif(basin == 'ATL'):
        if(verb): print "LLLLLLLLLLLLLLLLL",dir,spd,'m12: ',dirm12,spdm12
        nclip.atclip(idtg,lat0,lon0w,dir,spd,dirm12,spdm12,vmax,sid)

    
    flat=nclip.cliper.flat
    flon=nclip.cliper.flon
    for i in range(0,7): flon[i]=360.0-flon[i] # convert to deg E

    if(verb):
        for i in range(7):
            print"%5.2f  %5.2f"%(flat[i],flon[i])
    
    return(flat,flon)


def JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin,
               latm12=None,lonm12=None,
               latm24=None,lonm24=None,
               warn=0,verb=0):

    # ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    #
    #  speed check
    #
    # ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    
    if(spd > 45.0):
        print "EEEEEEEEEEEE SSSSSSS speed error for: ",sid,' at: ',lat0,lon0,' on: ',idtg
        print "EEEEEEEEEEEE SSSSSSS speed= ",spd
        return([-999.0],[-999.0])

    if(latm12 == None):
        (latm12,lonm12)=rumltlg(dir,spd,-12.0,lat0,lon0)
    if(latm24 == None):
        (latm24,lonm24)=rumltlg(dir,spd,-24.0,lat0,lon0)
    
    if(verb):
        print 'JJJclip: ',lat0,lon0,' m12: ',latm12,lonm12,' m24: ',latm24,lonm24

    #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
    #
    #  JTWC clipers
    #
    #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

    #
    #  calculate appropriate cliper model
    #

    clipermodel='NULL'
    nsind=-999

    #
    #  NHEM
    #

    if( lat0 >  3.0 ):
        if( lon0>=100.0 and lon0 <=180.0):
            if(lat0 < 45.0 ):
                clipermodel='wpclpr'
            else:
                clipermodel='oclip'
                nsind=2
        #
        #  NIO
        #
        elif(lon0>  0.0 and lon0 < 100.0):
            clipermodel='oclip'
            nsind=1

        #
        #  CPAC
        #
        elif(lon0>180.0 and lon0 <=220.0):
            clipermodel='oclip'
            nsind=4
            
    #
    #  SHEM
    #

    elif( lat0 < -3.0 ):

        #
        #  SWPAC
        #
        if( lon0>=140.0 and lon0 <=225.0):
            if( lat0 > -45.0 ):
                clipermodel='swpclp'
                nsind=-3
            else:
                clipermodel='oclip'
                nsind=-3
        #
        #  SEIO
        #
        elif( lon0>=100.0 and lon0 <140.0):
        
            if(lat0 > -45.0):
                clipermodel='seiclp'
                nsind=-2
            else:
                clipermodel='oclip'
                nsind=-2
        
        else:
            clipermodel='oclip'
            nsind = -1 # swio
    
    if(clipermodel == 'oclip'):
        if(warn): print "WWWW no new jtwc cliper for: ",lat0,lon0


    if(verb): print "CCCCC ",clipermodel,nsind

    if(clipermodel == 'NULL'):
        print "EEEEEEEEEEEE problem with finding a cliper model for: ",sid,' at: ',lat0,lon0,' on: ',idtg
        return([-999.0],[-999.0])

    if(clipermodel == 'wpclpr'):
        jclip.wpclpr (idtg,lat0,lon0,latm12,lonm12,latm24,lonm24,vmax)
        lalo=jclip.wpclpfcst.cfcst

    elif(clipermodel == 'swpclp'):
        jclip.swpclp (idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24,vmax)  # wants + lats
        lalo=jclip.swpclpfcst.cfcst
        for i in range(0,12,2): lalo[i]=-lalo[i] # convert to deg S

    elif(clipermodel == 'seiclp'):
        jclip.seiclp (idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24,vmax)  # wants + lats
        lalo=jclip.seiclpfcst.cfcst
        for i in range(0,12,2): lalo[i]=-lalo[i] # convert to deg S


    elif(clipermodel == 'oclip'):

        # nsind = -3 spac (lon >= 135.0)
        # nsind = -2 seio (lon >= 100 and lon < 135)
        # nsind = -1 swio (lon < 100)
        # nsind = 4 epac (lon > 220)
        # nsind = 3 cpac (lon > 180 and lon <= 220)
        # nsind = 2 wpac (lon > 100 and lon <= 180)
        # nsind = 1 nio (lon <=100)

        if(verb): print "QQQ ",nsind
        if(nsind < 0):
            jclip.oclip (nsind,idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24)
        else:
            jclip.oclip (nsind,idtg,lat0,lon0,latm12,lonm12,latm24,lonm24)

        lalo=jclip.oldclpfcst.cfcst

        #
        # tau 72 in tau 60 for SIO, interpolate
        #

        if(nsind == -1):
            lalo[8]=(lalo[6]+lalo[8])*0.5
            lalo[9]=(lalo[7]+lalo[9])*0.5


    if(clipermodel == 'wpclpr' or clipermodel == 'swpclp' or clipermodel == 'seiclp'
       or clipermodel == 'oclip' ):

        if(verb): print lalo

        flat=[]
        flon=[]

        flat.append(lat0)
        flon.append(lon0)
        
        if(verb): print "lat lon %5.1f %6.1f"%(lat0,lon0)
        
        for i in range(6):
            lat=lalo[2*i]
            lon=lalo[2*i+1]
            flat.append(lat)
            flon.append(lon)
            if(verb): print "lat lon %5.1f %6.1f"%(lat,lon)

    return(flat,flon)

#333333333333333333333333333333333333333333333 even more new version
#
# make cliper forecasts and output adeck
# using input from btops vice carq/bdeck
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


def MakeCliperForecast(tD,dtg,model,
                       tstmid=None,
                       doMotion=0,
                       verb=0):
    

    def b1id2basin(b1id,lat0,lon0):
        basin=None
        if(b1id == 'L'): basin='ATL'
        if(b1id == 'C' or b1id == 'E'): 
            basin='EPC'
            # -- cross date line from E->W
            if(lon0 < 180.0): basin='WPC'
        if(b1id == 'W'): basin='WPC'
        if(b1id == 'I'):
            basin=tcbasin(lat0, lon0)
        if(b1id == 'A'): basin='NIA'
        if(b1id == 'B'): basin='NIB'
        if(b1id == 'S'): basin='SIO'
        if(b1id == 'P'): basin='SEP'
        if(b1id == 'H'): 
            basin=tcbasin(lat0,lon0)
            
        return(basin)
    
    def getCQm12m24(mD,dtg,tstmid,dobt=0):
        
        cq00lat=cq00lon=cq00vmax=None
        cq12lat=cq12lon=cq12vmax=None
        cq24lat=cq24lon=cq24vmax=None
        cq12dir=cq12spd=None
        cq12dir12=-99.9
        cq12spd12=-9.9
        
        if(dobt):
            dtgm06=mf.dtginc(dtg,-6)
            dtgm12=mf.dtginc(dtg,-12)
            dtgm18=mf.dtginc(dtg,-18)
            dtgm24=mf.dtginc(dtg,-24)
            
            try:    bt00=mD.trk[dtg]
            except: bt00=None
                
            try:    bt06=mD.trk[dtgm06]
            except: bt06=None
                
            try:    bt12=mD.trk[dtgm12]
            except: bt12=None
                
            try:    bt18=mD.trk[dtgm18]
            except: bt18=None
                
            try:    bt24=mD.trk[dtgm24]
            except: bt24=None

            if(bt00 == None and bt06 == None and bt12 == None and bt18 == None and bt24 == None):
                print
                print 'WWWW -- no BT for dtg: ',dtg,' tstmid: ',tstmid,'press...use the CARQ initial motion -- happens for working best tracks....' 
                print
                return(cq12lat,cq12lon,cq24lat,cq24lon,cq12dir,cq12spd)
                

                
            if(bt00 != None):
                cq00lat=bt00.rlat
                cq00lon=bt00.rlon
                cq00vmax=bt00.vmax
                
            if(bt12 != None):
                cq12lat=bt12.rlat
                cq12lon=bt12.rlon
                cq12vmax=bt12.vmax
                cq12dir12=bt12.trkdir
                cq12spd12=bt12.trkspd 
            
            if(bt24 != None):
                cq24lat=bt24.rlat
                cq24lon=bt24.rlon
                cq24vmax=bt24.vmax
                
            # -- calc bt m12 spd dir
            #
            lat0=None
            
            if(bt06 != None and bt18 != None):
                lat0=bt06.rlat
                lon0=bt06.rlon
                lat1=bt18.rlat
                lon1=bt18.rlon
                dtbt=12
                bttype='bt06-18'
                
                
            if(lat0 == None and bt00 != None and bt12 != None):
                lat0=bt00.rlat
                lon0=bt00.rlon
                lat1=bt12.rlat
                lon1=bt12.rlon
                dtbt=12
                bttype='bt00-12'
                
                
            if(lat0 == None and bt00 != None and bt06 != None):
                lat0=bt00.rlat
                lon0=bt00.rlon
                lat1=bt06.rlat
                lon1=bt06.rlon
                dtbt=6
                bttype='bt00-06'
                
                
            if(lat0 == None and bt00 != None):
                print """CCCC-----------getCQm12m12 - can't calc bt12 dir/spd using initial motion""",bt00,bt06,bt12,bt18,bt24
                try:
                    cq12dir=bt00.dir
                except:
                    cq12dir=bt00.trkdir
                
                try:
                    cq12spd=bt00.spd
                except:
                    cq12dir=bt00.trkspd
                    
                bttype='btDR-SD'
                
            else:
                (cq12dir,cq12spd,umotion,vmotion)=rumhdsp(lat1, lon1, lat0, lon0, dtbt)
                
                
            bt12cqdir=-99.9
            bt12cqspd=-9.9
            try:
                bt12cqdir=bt12.dir
            except:
                None
            try:
                bt12cqspd=bt12.spd
            except:
                None
                
            print 'CCCCCCCCCCCCCCCC--------------',dtg,tstmid,'bt12: %5.1f %4.1f'%(cq12dir12,cq12spd12),\
                  'direct: %s %5.1f %4.1f'%(bttype,cq12dir,cq12spd),' CARQ: %5.1f %4.1f'%(bt12cqdir,bt12cqspd)
                
            
            
        else:
            try: cq00=mD.cq00[dtg]
            except: cq00=None
            
            try: cq12=mD.cq12[dtg]
            except: cq12=None
            
            try: cq24=mD.cq24[dtg]
            except: cq24=None
            
            if(cq00 != None): 
                cq00lat=cq00.rlat
                cq00lon=cq00.rlon
                cq00vmax=cq00.vmax
                
            if(cq12 != None):
                cq12lat=cq12.rlat
                cq12lon=cq12.rlon
                cq12vmax=cq12.vmax
                try:
                    cq12dir=cq12.dir
                    cq12spd=cq12.spd
                except:
                    None
                
            if(cq24 != None):
                cq24lat=cq24.rlat
                cq24lon=cq24.rlon
                cq24vmax=cq24.vmax
            
        return(cq12lat,cq12lon,cq24lat,cq24lon,cq12dir,cq12spd)

    def getOstmid(rawstmids,stmid):

        # -- always use the rawstmid for output
        #
        ostmid=None
        try:
            ostmid=rawstmids[stmid]
            return(ostmid)
        except:
            
            rc=getStmParams(stmid)
            stm2id=rc[-2]
            rc=getStmParams(stm2id)
            stmid=rc[-1]
            
            for stmid1 in rawstmids.keys():
                rc=getStmParams(stmid1,convert9x=1)
                tstmid1=rc[-1]
                if(stmid == tstmid1):
                    ostmid=rawstmids[stmid1]
                    return(ostmid)

        return(ostmid)

        
         
    # -- convert to 8 char dtg for cliper legacy application
    #
    idtg=dtg[2:]

    # -- Y2K
    #
    yy=int(dtg[2:4])
    if(yy<10):
        yy=yy+10
        idtg=str(yy)+idtg[2:]
    if(verb): print "YYYY",yy,idtg

    idtg=int(idtg)

    # -- to best match operations...where they mv a??9X to a??NN, force select of the NN vice 9X
    #
    dobt=0
    if(model == 'clpb'): dobt=1
    if(dobt == 0):
        tcV=tD.getTCvDtg(dtg,dupchk=0,selectNN=1,dobt=dobt)
    else:
        tcV=tD.getTCvDtg(dtg,dupchk=0,selectNN=1,dobt=dobt)
        
    trks=tcV.trk

    if(tstmid == None):
        stmids=trks.keys()  
    else:
        print 'qqqqqqqq',dtg,trks.keys()
        stmids=[tstmid]

    ntcs=len(stmids)

    if(verb): print "DDDDDDDDD ",dtg,idtg,tstmid,stmids
    if(verb): print "NNN: ",ntcs

    if(dobt):
        rawstmids=tD.getRawStm1idDtg(dtg,dobt=1,verb=verb)
    else:
        rawstmids=tD.getRawStm1idDtg(dtg,dupchk=0,selectNN=1,verb=0)
    
    allAcards={}
    tstmids=stmids
    if(doMotion == 0): tstmids=rawstmids.keys() 
    
    for stmid in tstmids:

        ostmid=getOstmid(rawstmids,stmid)
        latm12=lonm12=latm24=lonm24=cq12dir=cq12spd=None
        
        if(doMotion == 0):
            
            (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stmid,convert9x=1)
            
            # -- make sure we get the .bt obj if dobt=1
            #
            mD=tD.getDSsStm(stmid,dobt=dobt,verb=verb)
            (cq12lat,cq12lon,cq24lat,cq24lon,cq12dir,cq12spd)=getCQm12m24(mD,dtg,stmid,dobt=dobt)
            print 'CQ12-24-----------'
            
            icq12lat=cq12lat
            icq12lon=cq12lon
            icq24lat=cq24lat
            icq24lon=cq24lon
            icq12dir=cq12dir
            icq12spd=cq12spd
            
            if(cq12dir == None):
                icq12dir=icq12spd=999.
            if(cq12lat == None):
                icq12lat=icq12lon=999.9
            if(cq24lat == None):
                icq24lat=icq24lon=999.9
                
                
            print 'CQ12-24 dtg: ',dtg,'stmid: ',stmid,'OOOOstmid: ',ostmid,' cq12: %5.1f %5.1f'%(icq12lat,icq12lon),\
                  ' cq24: %5.1f %5.1f'%(icq24lat,icq24lon),' cq12dir/spd: %03.0f/%04.1f'%(icq12dir,icq12spd)
            print 'CQ12-24-----------'
            
            if(cq12lat != None):
                latm12=cq12lat
                lonm12=cq12lon
            if(cq24lat != None):
                latm24=cq24lat
                lonm24=cq24lon
            
            stm1id=tD.getSubbasinStmid(stm1id)
            stmid=stm1id

        sid=stmid
        
        vmax=trks[stmid].vmax
        rlat=trks[stmid].rlat
        rlon=trks[stmid].rlon
        dir=trks[stmid].dir
        spd=trks[stmid].spd
        
        lat0=rlat
        lon0=rlon
        
        (clat,clon)=Rlatlon2Clatlon(rlat,rlon)
        
        rc=getStmParams(stmid)
        b1id=rc[1].upper()
        basin=b1id2basin(b1id, lat0, lon0)
        fstmid=tD.getFinalStm1idFromRlonTcnames(stmid,rlon,b1id)
        if(verb):
            print 'BBBBBBB---------: ',dtg,stmid,b1id,basin,clat,clon,vmax,dir,spd
            print 'LLLLLL----m12m24: ',latm12,lonm12,latm24,lonm24
            
        # -- handle case of E->W run cliper based on basin id vice b1id
        #
        if(basin == 'EPC' or basin == 'ATL'):
            (flat,flon)=NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin,
                                  latm12=latm12,lonm12=lonm12,
                                  latm24=latm24,lonm24=lonm24,
                                  cq12dir=cq12dir,cq12spd=cq12spd,
                                  verb=verb)
            # -- check for cross the date-line
            #
            oflon=[]
            for lon in flon:
                if(lon > 360.0): lon=lon-360.0
                oflon.append(lon)
                
            flon=oflon

        else:
            (flat,flon)=JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin,
                                   latm12=latm12,lonm12=lonm12,
                                   latm24=latm24,lonm24=lonm24,
                                   verb=verb)

        if(verb): print "FFFFFFFFFFFFFFF00000",flat[0],flon[0],flat[-1],flon[-1]

        trk={}
        if(flat[0] != -999.0):
            n=0
            for tau in range(0,84,12):
                lat=flat[n]
                lon=flon[n]
                if(abs(lat) > 90 ):
                    print 'BBBBBBBBBBBBBBBBBBB----------cliper blew up for stmid: ',stmid,\
                          'dtg: ',dtg,' basin: ',basin,' lat/lon0: ',lat0,lon0
                    break
                
                trk[tau]=(lat,lon)
                n=n+1
        else:
            allAcards[stmid]=[]
            
        if(verb): print 'OOOSSSTTTMMMIIIDDD: ',ostmid
        acards=MakeAdeckCards(model, dtg, trk, ostmid,verb=verb)
        allAcards[ostmid]=acards
        

    return(allAcards)
	