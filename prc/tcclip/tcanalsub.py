from tcbase import *

units='english'

#
# bound on 2-d plot
#

latinc=loninc=5.0
latinc=loninc=1.0

latbuff=5.0
lonbuff=10.0

latoffset=5.0
lonoffset=10.0

latoffsetmax=5
lonoffsetmax=10

latoffset=0.0
lonoffset=0.0

latmaxplot=40.0
lonmaxplot=60.0

lonmaxplot=40.0
latmaxplot=lonmaxplot*(3.0/4.0)

NewLatlonBoundsScheme=1

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


def CpOfcAdecks(dtg,tdir,ropt=''):

    yyyy=dtg[0:4]
    sdir="%s/%s/wxmap"%(w2.TcAdecksJtwcDir,yyyy)
    cmd="cp %s/*.ofc?.%s.??? %s/."%(sdir,dtg,tdir)
    mf.runcmd(cmd,ropt)

    sdir="%s/%s/wxmap"%(w2.TcAdecksNhcDir,yyyy)
    cmd="cp %s/*.ofc?.%s.??? %s/."%(sdir,dtg,tdir)
    mf.runcmd(cmd,ropt)
    



def TcstructDataCards(dtg,stmdata,stm3tofull,otdir,ogdir,osdir,odir,verb=0):

    if(verb): print 'sss ',otdir,osdir,dtg

    cmask="%s/carq.*"%(otdir)
    cf=glob.glob(cmask)

    if(verb): print 'sss ',cmask,cf
    
    #STM VMAX RMAX R3NE R3SE R3SW R3NW R5NE R5SE R5SW R5NW PRCI ROCI

    stmids=[]
    stm3ids=[]
    stmparms={}

    for c in cf:
        if(verb): print 'ccc ',c
        o=open(c)
        tt=o.readlines()
        o.close()
        carqcard=tt[1]
        if(verb): print 'CCC ',carqcard
        tt=carqcard.split()
        stm3=tt[0]
        stmthere=1
        try:
            stm=stm3tofull[stm3]
        except:
            stmthere=0

        if(stmthere):
            vmax=int(tt[1])
            rmax=int(tt[2])
            r34=0
            for i in range(3,7,1):
                r34=r34+int(tt[i])
            
            r34=int(float(r34)*0.25)
            stmids.append(stm)
            stm3ids.append(stm3)
            stmparms[stm]=(vmax,rmax,r34)

    #
    # set up db file
    #

    dbpath="%s/tc.db.%s.txt"%(odir,dtg)
    print 'dddddddddddddddd ',dbpath
    db=open(dbpath,'w')

    otaus=['000','012','024','036','048','060','072','084','096','108','120']
    
    for stm in stmids:

        (stmdtg,stmrlat,stmrlon,stmvmax,stmpmin)=stmdata[stm,'posit']
        (clat,clon)=Rlatlon2Clatlon(stmrlat,stmrlon)

        dbcard="%s %5.1f %6.1f "%(stm,stmrlat,stmrlon)
        for stmparm in stmparms[stm]:
            dbcard="%s %3s "%(dbcard,stmparm)
        
        gpmask="%s/plt.*.%s.*.png"%(ogdir,stm)
        if(verb): print 'tcstrucdb gpmask: ',gpmask
        gf=glob.glob(gpmask)
        gf.sort()
        for g in gf:
            (gdir,gfile)=os.path.split(g)
            tt=gfile.split('.')
            gmodel=tt[1]
            gtau=tt[4]
            for otau in otaus:
                if(gtau == otau):
                    dbcard=dbcard+"%s.%s "%(gmodel,gtau)

        print dbcard[0:132]+' ...'
        db.writelines(dbcard+'\n')

    db.close()
            
    return

    
def JtwcLatLonBounds(cdirjtwc,cdirnhc,fstm,stmdata,stmmotion,dtg):


    if(NewLatlonBoundsScheme==1):


        
        (stmdtg,stmrlat,stmrlon,stmvmax,stmpmin)=stmdata[fstm,'posit']
        (stmdir,stmspd)=stmmotion[fstm,'motion']

        dt=24.0
        dt=48.0
        (rlatoffset,rlonoffset)=rumltlg(stmdir,stmspd,dt,stmrlat,stmrlon)

        latoffset=int(rlatoffset-stmrlat)
        lonoffset=int(rlonoffset-stmrlon)

        #
        # limit check
        #

        if(latoffset < -latoffsetmax): latoffset = -latoffsetmax
        if(latoffset > +latoffsetmax): latoffset = +latoffsetmax
        
        if(lonoffset < -lonoffsetmax): lonoffset = -lonoffsetmax
        if(lonoffset > +lonoffsetmax): lonoffset = +lonoffsetmax


        #lonoffset=0
        jtlatbar=stmrlat
        jtlonbar=stmrlon

        #
        # new scheme to define fix lat/lon width plot areas
        #

        latplotmin=int( (jtlatbar - latmaxplot*0.5 )/latinc + 0.5)*latinc
        if(stmrlat > 0.0):
            latplotmin=latplotmin + latoffset

        latplotmax=latplotmin + latmaxplot

        lonplotmin=int( (jtlonbar - lonmaxplot*0.5 )/loninc + 0.5)*loninc
        if(stmrlat > 0.0):
            lonplotmin=lonplotmin + lonoffset
            
        lonplotmax=lonplotmin + lonmaxplot

        print 'ssssssssss ',fstm,dtg,stmdir,stmspd
        print 'ssssssssss ',stmrlat,stmrlon,rlatoffset,rlonoffset
        print 'ssssssssss ',latoffset,lonoffset
        print 'ssssssssss ',latplotmin,latplotmax,lonplotmin,lonplotmax

        return(latplotmin,latplotmax,lonplotmin,lonplotmax)



    stm=fstm.split('.')[0]
    yyyy=fstm.split('.')[1]

    basinid=Basin1toBasin2[stm[2:]]
    basinid=basinid.lower()
    
    print 'BBB ',basinid
    dtgcheck=dtg
    hh=dtg[8:10]

    #
    # 20021227 -- if sh and off time look for previous dtg forecast
    #

    if(hh == '18' and basinid == 'sh'):
        dtgcheck=dtg[0:8]+'12'
        
    if(hh == '06' and basinid == 'sh'):
        dtgcheck=dtg[0:8]+'06'

    
    adeckpath="%s/%s/a%s%s%s.dat"%(cdirjtwc,yyyy,basinid,stm[0:2],yyyy)
    if(basinid == 'al' or basinid == 'ep' or basinid == 'cp'):
        adeckpath="%s/%s/a%s%s%s.dat"%(cdirnhc,yyyy,basinid,stm[0:2],yyyy)
    
    pass1id='JTWC'
    if(basinid == 'al' or basinid == 'ep' or basinid == 'cp'): pass1id='OFCL'
    cmd="grep -h '%s,' %s | grep -h %s "%(pass1id,adeckpath,dtgcheck)
    print 'CCC: ',cmd
    jtwc=os.popen(cmd).readlines()

    #
    # check if there are any cards; if not then use C120
    #
    print 'LLLLLLLL jtwc (1st pass): ',len(jtwc)

    #
    # pass 2 C120
    #
    pass2id='C120'
    if(basinid == 'al' or basinid == 'ep' or basinid == 'cp'): pass2id='OFCI'
    if(len(jtwc) <= 0):
        print 'BBB ',basinid
        cmd="grep -h '%s,' %s | grep -h %s "%(pass2id,adeckpath,dtgcheck)
        print 'CCC: ',cmd
        jtwc=os.popen(cmd).readlines()
        print 'LLLLLLLL jtwc (2nd pass): ',len(jtwc)

    #
    # pass 3 CLP5
    #
    pass3id='CLP5'
    if(basinid == 'al' or basinid == 'ep' or basinid == 'cp'): pass3id='CLP5'
    if(len(jtwc) <= 0):
        cmd="grep -h '%s,' %s | grep -h %s "%(pass3id,adeckpath,dtgcheck)
        print 'CCC: ',cmd
        jtwc=os.popen(cmd).readlines()
        print 'LLLLLLLL jtwc (3nd pass): ',len(jtwc)

    #
    # pass 4 XTRP
    #
    pass4id='XTRP'
    if(basinid == 'al' or basinid == 'ep' or basinid == 'cp'): pass4id='CONU'
    if(len(jtwc) <= 0):
        cmd="grep -h '%s,' %s | grep -h %s "%(pass4id,adeckpath,dtgcheck)
        print 'CCC: ',cmd
        jtwc=os.popen(cmd).readlines()
        print 'LLLLLLLL jtwc (4th pass): ',len(jtwc)

    #
    # pass 5 CLIM (72 for SHEM)
    #
    if(len(jtwc) <= 0):
        cmd="grep -h '%s,' %s | grep -h %s "%('CLIM',adeckpath,dtgcheck)
        print 'CCC: ',cmd
        jtwc=os.popen(cmd).readlines()
        print 'LLLLLLLL jtwc (5th pass): ',len(jtwc)

    #
    # pass 6 CLIP (72 for SHEM)
    #
    if(len(jtwc) <= 0):
        cmd="grep -h '%s,' %s | grep -h %s "%('CLIP',adeckpath,dtgcheck)
        print 'CCC: ',cmd
        jtwc=os.popen(cmd).readlines()
        print 'LLLLLLLL jtwc (6th pass): ',len(jtwc)

    gotjtwc=1
    
    if(len(jtwc) <= 0):
        gotjtwc=0
        (stmdtg,stmrlat,stmrlon,stmvmax,stmpmin)=stmdata[fstm,'posit']
        (clat,clon)=Rlatlon2Clatlon(stmrlat,stmrlon)

        print 'WWWWW: no forecast basis for doing field plots'
        print 'WWWWW: Using the initial position: ',stmrlat,stmrlon
    

    if(gotjtwc == 1):
        
        jttaus=[]
        jtlats={}
        jtlons={}

        for j in jtwc:
            tt=string.split(j,',')
            tau=int(tt[5].strip())
            lat=tt[6].strip()
            lon=tt[7].strip()
            jttaus.append(tau)
            hemns=lat[len(lat)-1:]
            hemew=lon[len(lon)-1:]
            jtlats[tau]=int(lat[0:(len(lat)-1)])*0.1
            jtlons[tau]=int(lon[0:(len(lon)-1)])*0.1

            if(hemns == 'S'):
                jtlats[tau]=-jtlats[tau]

            if(hemew == 'W'):
                jtlons[tau]=360.0-jtlons[tau]


        taus=mf.uniq(jttaus)

        jtmaxlat=jtmaxlon=-999.9
        jtminlat=jtminlon=999.9

        for tau in taus:
            if(jtlats[tau] < jtminlat): jtminlat=jtlats[tau]
            if(jtlons[tau] < jtminlon): jtminlon=jtlons[tau]
            if(jtlats[tau] > jtmaxlat): jtmaxlat=jtlats[tau]
            if(jtlons[tau] > jtmaxlon): jtmaxlon=jtlons[tau]

        jtlatbar=(jtminlat+jtmaxlat)*0.5
        jtlonbar=(jtminlon+jtmaxlon)*0.5

        nj1=int( jtminlat/latinc+0.5 )
        nj2=int( jtmaxlat/latinc+0.5 )
        nj3=int( jtminlon/loninc+0.5 )
        nj4=int( jtmaxlon/loninc+0.5 )


        j1=nj1*latinc
        j2=nj2*latinc
        j3=nj3*loninc
        j4=nj4*loninc

    else:

        j1=j2=stmrlat
        j3=j4=stmrlon
        jtlatbar=stmrlat
        jtlonbar=stmrlon
    
    latplotmin=j1-latbuff
    latplotmax=j2+latbuff
    lonplotmin=j3-lonbuff
    lonplotmax=j4+lonbuff

    
    if(NewLatlonBoundsScheme==1):
        
        (stmdtg,stmrlat,stmrlon,stmvmax,stmpmin)=stmdata[fstm,'posit']
        
        latplotmin=stmrlat - latbuff
        latplotmax=stmrlat + latbuff
        lonplotmin=stmrlon - lonbuff
        lonplotmax=stmrlon + lonbuff

        #
        # new scheme to define fix lat/lon width plot areas
        #

        latplotmin=int( (jtlatbar - latmaxplot*0.5 )/latinc + 0.5)*latinc
        latplotmax=latplotmin + latmaxplot

        lonplotmin=int( (jtlonbar - latmaxplot*0.5 )/loninc + 0.5)*loninc
        lonplotmax=lonplotmin + lonmaxplot

        #print "QQQQ ",latplotmin,latplotmax,jtlatbar
        #print "QQQQ ",lonplotmin,lonplotmax,jtlonbar
    

    return(latplotmin,latplotmax,lonplotmin,lonplotmax)

#----------------------------------------------------------------------
#
#  basemapplot
#
#----------------------------------------------------------------------

def BaseMapPlot(ogdir,opdir,stm,model,dtg,
                gradsopt,orogpath,
                latplotmin,latplotmax,
                lonplotmin,lonplotmax,
                xsize,ysize,dobmapplt):


    gradspolydir=w2.GradsGslibDir+'/'
    gradsgsdir=w2.GradsGslibDir
    bmappath="%s/basemap.%s.%s.png"%(ogdir,stm,dtg)
    bmappath=bmappath
    print 'QQQQ ',bmappath
        
    basemapgs="""
    
function main(args)

rc=gsfallow('on')
rc=const()

'open %s'
'set grads off'
'set parea 0.75 10.25 0.75 7.75'
'set lat %s %s'
'set lon %s %s'
'set ylint 5'
'set xlint 10'
'set mpdset mres'


lcol=90
ocol=91
'set rgb 90 100 50 25'
'set rgb 91 10 20 85'
'set cmin 100000'
#
# use lat, incase no land!!! open ocen
#
'd lat'

'%s/basemap.2 L 'lcol' 1 %s'
'%s/basemap.2 O 'ocol' 1 %s'

'set map 0 0 10'
'draw map'

'set grid on 3 0 5'
'set cmin 100000'
'd lat'

'set map 1 0 3'
'draw map'


#'printim -- white -- --'
'printim %s x%s y%s'
'quit'
"""%(orogpath,
     latplotmin,latplotmax,
     lonplotmin,lonplotmax,
     gradsgsdir,gradsgsdir,gradsgsdir,gradsgsdir,
     bmappath,xsize,ysize
     )

    if(dobmapplt):
        basemapgspath="%s/basemap.%s.%s.%s.gs"%(opdir,model,stm,dtg)
        o=open(basemapgspath,'w')
        o.writelines(basemapgs)
        o.close()
        
        gradscmd="grads %s \"run %s\" -g %sx%s"%(gradsopt,basemapgspath,xsize,ysize)
        print "gradscmd: ",gradscmd
        os.system(gradscmd)

    return(bmappath)

#----------------------------------------------------------------------
#
#  ntimemodel - number 
#
#----------------------------------------------------------------------


def NtimeModel(model):
    nt=11
    if(model == 'ukm'): nt=7
    if(model == 'gsm'): nt=7
    return(nt)


#----------------------------------------------------------------------
#
# obs .ctl setup
#
#----------------------------------------------------------------------

def ObsCtlSetup(oddir,omodel,model,fstm,dtg,ntcf):

    ntmod=NtimeModel(omodel)

    gtime=mf.dtg2gtime(dtg)

    msd="%s.%s.%s"%(model,fstm,dtg)
    
    tsctl="""dset ^tcstruct.%s.obs
title radial profile station data from tcsanal.x
dtype station
options sequential
stnmap ^tcstruct.%s.smp
undef 1e20
tdef %s linear %s 12hr
vars 5
r  0 0  r radius [nm]
u  0 0  u radial wind [kt]
v  0 0  v tangential wind [kt]
uc 0 0  uc E-W u comp [kt]
vc 0 0  vc N-S v comp [kt]
endvars"""%(msd,msd,ntcf,gtime)

    print tsctl

    ctlfile="%s/tcstruct.%s.ctl"%(oddir,msd)
    o=open(ctlfile,'w')
    o.writelines(tsctl)
    o.close()
    
    #
    # run stnmap
    #

    cmd="stnmap -i %s"%(ctlfile)
    print 'CCC: ',cmd
    os.system(cmd)

def NgtrkFldCtl(ngtrkfldpath,ngtrkctlpath,nt=11,dt='12hr'):

    (dir,file)=os.path.split(ngtrkfldpath)
    model=file.split('.')[2]
    dtg=file.split('.')[3]

    gtime=mf.dtg2gtime(dtg)
    ctl="""dset ^%s
title fields for tcstruct analysis
undef 1e20
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 1013
tdef  %s linear %s %s
vars 3
uas  0 0 uas
vas  0 0 vas
vt8  0 0 850 rel vort
endvars"""%(file,nt,gtime,dt)

    c=open(ngtrkctlpath,'w')

    c.writelines(ctl)
    c.close()

    
                                             

#----------------------------------------------------------------------
#
# .ctl setup
#
#----------------------------------------------------------------------

def CtlSetup(oddir,omodel,model,stm,dtg,ntcf):

    ntmod=NtimeModel(omodel)

    gtime=mf.dtg2gtime(dtg)

    msd="%s.%s.%s"%(model,stm,dtg)
    
    prfctl="""dset ^profiles.tcstruct.%s.dat
title radial average profiles by storm model all, and 90 deg quads 
undef 1e20
options sequential
xdef 101 linear   0.0 10.0
ydef   5 levels   0.0 45 135 225 315
zdef   1 levels 1013
tdef  %s linear %s 12hr
vars 4
vc    0 0 tangential wind [kt]
uc    0 0 radial wind [kt]
sc    0 0 wind speed [kt]
vcngp 0 0 ngp tcbog tangential profile [kt]
endvars"""%(msd,ntmod,gtime)

    print prfctl

    ctlfile="%s/profiles.tcstruct.%s.ctl"%(oddir,msd)
    o=open(ctlfile,'w')
    o.writelines(prfctl)
    o.close()

    profilectlpath=ctlfile

    return(profilectlpath)

#----------------------------------------------------------------------
#
# namelist of tcsanal.x
#
#----------------------------------------------------------------------

def NlSetup(otdir,oddir,osdir,opdir,omodel,model,stm,stm3,dtg):

    # mds3 - wxmap.
    # sd   - carq.
    # md   - fld
    # msd  - obs
    
    mds3="%s.%s.%s"%(omodel,dtg,stm3)
    sd="%s.%s"%(stm,dtg)
    md="%s.%s"%(model,dtg)
    msd="%s.%s.%s"%(model,stm,dtg)

    #
    # spdcrit = threshold wind calc sig output wind
    # vcrit = tangential wind threshold to find point
    #        of transition between TC and the environment
    # levwind = vertical coor to do calcs 1=sfc ; 2=850
    # verb = turn diagnostics
    #
    
    tcsappnl="""$parameters
  spdcrit=15.0,
  vcrit=7.5,
  verb=.false.,
  levwind=1
$end
$paths
  tcapath='%s/wxmap.%s.txt',
  tcspath='%s/carq.%s.txt',
  tcfpath='%s/fld.tcstruct.%s.dat',
  tcopath='%s/tcstruct.%s.obs',
  tcdpath='%s/parms.tcstruct.%s.txt',
  tcppath='%s/profiles.tcstruct.%s.dat',
$end"""%(otdir,mds3,
         otdir,sd,
         oddir,md,
         oddir,msd,
         osdir,msd,
         oddir,msd
         )

    print tcsappnl

    nlpath="%s/tcsanal.namelist.%s.txt"%(opdir,msd)

    o=open(nlpath,'w')
    o.writelines(tcsappnl)
    o.close()
    

    return(nlpath)


def CarqCardStmParms(fstm,carqcards):

    stm=fstm.split('.')[0]
    
    carqcard=carqcards[fstm]

    print 'CCCCCC ',carqcard
    tt=carqcard.split()
###    CCCCCC  21w 0090 0020 0180 0110 0110 0150 0070 0060 0060 0070 0995 0150 9999

    
    stmid=tt[0]
    stmvmax=float(tt[1])
    stmrmax=float(tt[2])
    stmdeye=float(tt[13])

    if(stmrmax > 200.0 and stmdeye < 500.0):
        stmrmax=(stmeyedia*1.2)/2.0

    stmr34mean=0.0
    for i in range(3,7):
        stmr34mean=stmr34mean+float(tt[i])
    stmr34mean=stmr34mean/4.0

    stmr50mean=0.0
    for i in range(7,11):
        stmr50mean=stmr50mean+float(tt[i])
    stmr50mean=stmr50mean/4.0

    return(stmid,stmvmax,stmrmax,stmr34mean,stmr50mean)

#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# field plot
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp

def FldPlot(ogdir,otdir,oddir,opdir,
            curdir,stm,stm3,carqcards,
            gradsopt,omodel,model,dtg,
            cfldpath,bmappath,ntcf,
            latplotmin,latplotmax,
            lonplotmin,lonplotmax,
            xsize,ysize,dofldplt):

    verb=0

    bmappathtmp="basemap.png"
    
    adeckpath="%s/wxmap.%s.%s.%s.txt"%(otdir,omodel,dtg,stm3)
    cobspath="%s/tcstruct.%s.%s.%s.ctl"%(oddir,model,stm,dtg)

    aomodel=omodel
    aname=atcf.ModelNametoAdeckName[aomodel]

    if(verb):
        print 'adeckpath = ',adeckpath
        print ' cobspath = ',cobspath
        print ' cfldpath = ',cfldpath

    modelup=omodel.upper()
    stmup=stm.upper()
    
    (stmid,stmvmax,stmrmax,stmr34mean,stmr50mean)=CarqCardStmParms(stm,carqcards)

    tt2="\'CARQ:   V`bmax`n=%d kt  R`bmax`n=%d nm  R34=%s nm  R50=%s nm\'"%\
         (int(stmvmax),int(stmrmax),int(stmr34mean),int(stmr50mean))
    
    gs="""
function main(args)

rc=gsfallow('on')
rc=const()

aid='%4s'
adeck='%s'

rc=tcadeck(adeck)

'open %s'
'open %s'
'set lat %s %s'
'set lon %s %s'

'set rgb 91 254 254 254'
'set rgb 92 1 1 1'

'set t 1'
bdtg=%s
model=%s
stm=%s
modelup=%s
stmup=%s
t=1
tmax=%s

#
# tc posits
#
_btautc=0
_dtautc=12
rc=tcbtft()
rc=tcftof()
if(_ntcbt > 0 | _ntcbtof > 0); _btthere=1; endif


while(t<=tmax)
  'c'
  'set dfile 1'
  'set grads off'
  'set timelab on'
  _tau=(t-1)*12
  tout=_tau
  if(_tau<=9)  ; tout='00'_tau ; endif
  if(_tau<=99) ; tout='0'_tau ; endif
  if(_tau=0)   ; tout='000' ; endif
  'set t 't
  'set mpdset mres'
  'set ylint 5'
  'set xlint 10'
  'set parea 0.75 10.25 0.75 7.75'

  'set map 1 0 5'
  'set gxout stnmark'
  'set cmark 5'
  'set digsiz 0.035'
  'set rbrange 0 35'
  'set cint 5'
  'd mag(u,v)'
  'cbarn 0.75'

  'set gxout stream'
  'set strmden 5'
  'set ccolor 0'
  'set cthick 10'
  'd uas.2(t='t');vas.2(t='t')'
  'set rbrange 0 35'
  'set ccolor rainbow'
  'set cthick 5'
  'set cint 5'
  'd uas.2(t='t');vas.2(t='t');mag(uas.2(t='t'),vas.2(t='t'))'

  'set gxout contour'
  'set ccolor 0'
  'set cthick 10'
  'set clevs 15 35'
  'd mag(uas.2(t='t'),vas.2(t='t'))'
 
  'set grid on 3 7 3'
  'set ccolor 91'
  'set clevs 15 35'
  'set cthick 6'
  'd mag(uas.2(t='t'),vas.2(t='t'))'

  'draw map'
 
#
# do titles before setting clip for 
#

  tt1=modelup' V`bsfc`n for: 'stmup' at: 'bdtg' tau = 'tout
  tt2=%s
#  rc=toptitle(tt1,tt2,1,92,92)
  rc=toptitle(tt1,tt2,1,91,91)

  'set strsiz 0.14'
  'set string 4 l 6'
  vdate=mydate()
 'draw string 0.2 0.35 Verify: 'vdate

#
#  plot the radii and TC center
#
  'set dfile 2'
  rc=plotdims()
  'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

  tclat=subwrd(_tca.aid._tau,1)
  tclon=subwrd(_tca.aid._tau,2)
  drs='60 120 180 240'
  rc=pltradii(tclon,tclat,drs)

#
# get ft posits and draw
#
  rc=ftposits(_tau,_btautc,_dtautc)
  rc=drawtcft()

#
# draw bt
#
  rc=drawtcbt()

#
# get of posits and draw
#
  rc=ofposits(_tau,_btautc,_dtautc)
  rc=drawtcof()

##  'printim --/plt.'model'.'stm'.'tout'.png  white -b -- -t 0 x-- y-- png'
  'printim %s/plt.'model'.'stm'.'tout'.png  -b %s -t 0 x%s y%s png'
 
  t=t+1
  
endwhile
'quit'
return

"""%(aname,adeckpath,cobspath,cfldpath,
     latplotmin,latplotmax,
     lonplotmin,lonplotmax,
     dtg,omodel,stm,modelup,stmup,
     ntcf,
     tt2,ogdir,
     bmappathtmp,
     xsize,ysize
     )

    #
    # add tc and ofcl posits gsf, as in w2.plot.py
    #
    yyyy=dtg[0:4]
    tcmodel=model
    if(model == 'ocn'): tcmodel='ngp'
    tcgsfpath="%s/ngtrk.tcbtft.%s.%s.gsf"%(otdir,tcmodel,dtg)
    ofgsfpath="%s/ngtrk.tcbtof.%s.%s.gsf"%(otdir,tcmodel,dtg)

    gstc="tcposit.noload.gsf"
    if(os.path.exists(tcgsfpath)):
        siz=os.path.getsize(tcgsfpath)
        if(siz > 0):
            print 'ttttttttttttt ',tcgsfpath
            print 'TCTCTCTCTC got tcstruct .gsf siz: ',siz
            gstc=tcgsfpath

    gstcs=open(gstc).readlines()

    gstcposits=""
    for gscard in gstcs:
        gstcposits=gstcposits+gscard

    gsof="ofposit.noload.gsf"
    if(os.path.exists(ofgsfpath)):
        siz=os.path.getsize(ofgsfpath)
        if(siz > 0):
            print 'ooooooooooo ',ofgsfpath
            print 'TCTCTCTCTC got ofc      .gsf siz: ',siz
            gsof=ofgsfpath

    print 'cccccccccccc ',os.getcwd()

    gsofs=open(gsof).readlines()
    gsofposits=""
    for gscard in gsofs:
        gsofposits=gsofposits+gscard
    



    if(dofldplt):

        gsfile="plot.%s.%s.%s.gs"%(stm,model,dtg)
        gspath="%s/%s"%(opdir,gsfile)
        o=open(gspath,'w')
        o.writelines(gs)
        o.writelines(gstcposits)
        o.writelines(gsofposits)
        o.close()

        cmd="cat draw*.gsf >> %s"%(gspath)
        mf.runcmd(cmd,'')
            
        cmd="cat ??posits*.gsf >> %s"%(gspath)
        mf.runcmd(cmd,'')
            
        os.chdir(opdir)

        cmd="cp %s basemap.png"%(bmappath)
        mf.runcmd(cmd)
            
        gradscmd="grads %s \"run %s\" -g %sx%s"%(gradsopt,gsfile,xsize,ysize)
        print "gradscmd: ",gradscmd
        os.system(gradscmd)

        os.chdir(curdir)

#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# profile plot
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp

def ProfilePlot(ogdir,opdir,curdir,stm,model,dtg,carqcards,ntcf,
                gradsopt,profilectlpath,
                xsize,ysize,doprofileplt):


    verb=0
    (stmid,stmvmax,stmrmax,stmr34mean,stmr50mean)=CarqCardStmParms(stm,carqcards)
    if(verb): print 'CCCCCC ',carqcard
    
    tt1="\'%s  MEAN  v`btang`n for: %s at %s\'"%\
         (model.upper(),stm.upper(),dtg)
    tt2="\'CARQ:   V`bmax`n=%d kt  R`bmax`n=%d nm  R34=%s nm  R50=%s nm\'"%\
         (int(stmvmax),int(stmrmax),int(stmr34mean),int(stmr50mean))
    tt3="\'NOGAPS bogus black; dash tau=0 ; red 24 ; green 48 ; blue 72\'"
    
#'draw title 'model' for: 'stm' at: 'bdtg'\

    gs="""function main(args)

rc=gsfallow('on')
rc=const()

'set grads off'
'set timelab on'

'open %s'

bdtg=%s
model=%s
stm=%s
xsize=%s
ysize=%s
tt1=%s
tt2=%s
tt3=%s
ntcf=%s
pltdir='%s'

'set y 1'

'set xaxis 0 1000 60'
'set parea 1 10 0.75 7.75'
#
# set vrange to fix
#
'set vrange -10 100'
'set ylint 10'
if(ntcf >=1)
'set t 1'

'set cmark 0'
'set ccolor 1'
'set cthick 7'
'd vcngp'

'set cmark 0'
'set ccolor 1'
'set cstyle 3'
'set cthick 6'
'd vc'
endif

if(ntcf >=3)
'set t 3'

'set cmark 0'
'set ccolor 2'
'set cstyle 1'
'set cthick 4'
'd vc'
endif

if(ntcf >=5)
'set t 5'

'set cmark 0'
'set ccolor 3'
'set cthick 4'
'd vc'
endif

if(ntcf >=7)
'set t 7'

'set cmark 0'
'set ccolor 4'
'set cthick 4'
'd vc'
endif



vcrit=0
'q w2xy 0 'vcrit
x0l=subwrd(result,3)
y0l=subwrd(result,6)

'q w2xy 1000 'vcrit
x0r=subwrd(result,3)
y0r=subwrd(result,6)

print '0 line 'x0l' 'y0l' 'x0r' 'y0r
'draw line 'x0l' 'y0l' 'x0r' 'y0r

vcrit=15
'q w2xy 0 'vcrit
x15l=subwrd(result,3)
y15l=subwrd(result,6)

'q w2xy 1000 'vcrit
x15r=subwrd(result,3)
y15r=subwrd(result,6)

print '15 line 'x15l' 'y15l' 'x15r' 'y15r

'draw line 'x15l' 'y15l' 'x15r' 'y15r

'draw ylab v`btc`n [kt]'
'draw xlab r [nm]'

rc=toptle3(tt1,tt2,tt3,1.0,1,2,3)

##'q pos'

'printim 'pltdir'/profile.'model'.'stm'.'bdtg'.png white x'xsize' y'ysize' png'

'c'
'quit'
return
"""%(profilectlpath,dtg,model,stm,
     xsize,ysize,tt1,tt2,tt3,ntcf,ogdir)
    
    if(doprofileplt):

        gsfile="profile.plot.%s.%s.%s.gs"%(stm,model,dtg)
        gspath="%s/%s"%(opdir,gsfile)
        o=open(gspath,'w')
        o.writelines(gs)
        o.close()
            
        os.chdir(opdir)

        gradscmd="grads %s \"run %s\" -g %sx%s"%(gradsopt,gsfile,xsize,ysize)
        print "gradscmd: ",gradscmd
        os.system(gradscmd)

        os.chdir(curdir)
            
        

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# parse adecks for carqs to get storms and params 
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


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
        

def LoadStmDataBtops(n,stmids,stmdata,stmmotion,stmids1,stmdata1,stmmotion1):

    from math import cos
    from math import sin
    
    stm=stmids1[n]
    stmids.append(stm)
    #
    # convert tuple to mutable list
    #
    posit=list(stmdata1[stm,'posit'])
    rlat=posit[1]
    rlon=posit[2]
    #
    # convert from float -> char lat/lon
    #
    (clat,clon)=Rlatlon2Clatlon(rlat,rlon)
    posit[1]=" %s"%(clat)
    posit[2]=" %s"%(clon)
    stmdata[stm,'posit']=tuple(posit)
    stmdata[stm,'r34']=stmdata1[stm,'r34']
    stmdata[stm,'r50']=stmdata1[stm,'r50']
    stmdata[stm,'roci']=stmdata1[stm,'roci']
    stmdata[stm,'rmax']=stmdata1[stm,'rmax']
    #
    # add u/v comps of motion
    #
    motion=list(stmmotion1[stm,'motion'])
    spdmtn=motion[1]
    course=motion[0]
    angle=(90.0-course)*deg2rad
    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    motion.append(umotion)
    motion.append(vmotion)
    stmmotion[stm,'motion']=tuple(motion)


    return
        

def UniqStorms(stmidscq,stmdatacq,stmmotioncq,
               stmidsbt,stmdatabt,stmmotionbt,
               stmidsbo,stmdatabo,stmmotionbo):

    verb=0
    
    stmids=[]
    stmdata={}
    stmmotion={}

    stmidscq=mf.uniq(stmidscq)
    stmidsbt=mf.uniq(stmidsbt)
    stmidsbo=mf.uniq(stmidsbo)

    if(stmidscq[0] == 'nocarq' and stmidsbt[0] == 'nobest'):
        stmids.append('notcs')
        return(stmids,stmdata,stmmotion)

    ncq=0
    nbt=0
    nbo=0
    
    if(stmidscq[0] != 'nocarq'):
        ncq=len(stmidscq)
    if(stmidsbt[0] != 'nobest'):
        nbt=len(stmidsbt)

    nbo=len(stmidsbo)
    
    if(verb):
        print 'UUUU SSSS ncq, nbt, nbo: ',ncq,nbt,nbo
        print 'uuuu SSSS stmidscq:      ',stmidscq
        print 'uuuu SSSS stmidsbt:      ',stmidsbt
        print 'uuuu SSSS stmidsbo:      ',stmidsbo
    
    #
    # first go through bo cards; load from carq
    #

    if(nbo > 0):
        for nb in range(0,nbo):
            stmbt=stmidsbo[nb].split('.')[0]
            #
            # cycle through cq and see if there's a match
            #
            if(verb):
                print
                print 'uuuu SSSS BO<-CQ: ',stmbt,'.............'
            foundcq=0
            if(ncq > 0):
                for nc in range(0,ncq):
                    stmcq=stmidscq[nc]
                    if(verb):
                        print 'UUUU SSSS BO<-CQ: ',stmcq,stmbt,nb,nc
                    if(stmcq == stmbt):
                        foundcq=1
                        if(verb):
                            print 'UUUU SSSS BO<-CQ --   FOuND...load...CARQ: ',stmidscq[nc]
                        LoadStmData(nc,stmids,stmdata,stmmotion,stmidscq,stmdatacq,stmmotioncq)
                        break
                        
                        
            if(foundcq == 0):
                if(verb):
                    print 'UUUU SSSS BO<-CQ -- nofound...load...BO:   ',stmidsbo[nb]
                LoadStmDataBtops(nb,stmids,stmdata,stmmotion,stmidsbo,stmdatabo,stmmotionbo)

    ntc=len(stmids)

    nstmidshash={}
    nstmids=[]

    if(ntc > 0):
        for nt in range(0,ntc):
            stmtc=stmids[nt].upper()
            lstmtc=stmids[nt]
            nstmtc=stmtc[0:2]
            istmtc=stmtc[2:3]
            nstm=nstmtc
            istm=istmtc
            if(nbo > 0):
                for nb in range(0,nbo):
                    stmbo=stmidsbo[nb]
                    nstmbo=stmbo[0:2]
                    istmbo=stmbo[2:3]
                    if(nstmtc == nstmbo):
                        nstmyearbo=stmbo.split('.')[1]
                        if(istmtc == 'I' or istmtc == 'S'):
                            istm=istmbo
                            
                    #print 'qqqqq ',nt,nb,stmtc,stmbo,nstmtc,istmtc,nstmbo,istmbo,nstmyearbo

            nstmid="%s%s.%s"%(nstm,istm,nstmyearbo)
            nstmids.append(nstmid)
            nstmidshash[lstmtc]=nstmid



    kk=nstmidshash.keys()
    kk.sort()

    if(verb):
        for k in kk:
            print 'ffff ',k,nstmidshash[k]

    kk=stmdata.keys()
    kk.sort()
    nstmdata={}
    for k in kk:
        knew=(nstmidshash[k[0]],k[1])
        nstmdata[knew]=stmdata[k]
        if(verb):
            print 'oooodddd ',k,knew,stmdata[k]
        

    kk=stmmotion.keys()
    kk.sort()
    nstmmotion={}
    for k in kk:
        knew=(nstmidshash[k[0]],k[1])
        nstmmotion[knew]=stmmotion[k]
        if(verb):
            print 'oooommmm ',k,knew,stmmotion[k]
        

    if(verb):
        kk=nstmdata.keys()
        kk.sort()
        for k in kk:
            print 'nnnndddd ',k,nstmdata[k]


        kk=nstmmotion.keys()
        kk.sort()
        for k in kk:
            print 'nnnnmmmm ',k,nstmmotion[k]

        for stmid in stmids:
            print 'IIIISSSS ',stmid

        for nstmid in nstmids:
            print 'NNNNSSSS ',nstmid


    return(nstmids,nstmdata,nstmmotion)
    

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
        stmids=['nobest']
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
            print 'had to regen... ',bddtgpath
        else:
            print 'EEE failure in redo carq grep for ',bddtgpath
            sys.exit()

    bdeck=open(bddtgpath,'r').readlines()

    nbdeck=len(bdeck)

    if(nbdeck == 0):
        print 'No bdeck TCs for : ',dtg
        stmids=['nobest']
        stmdata={}
        stmmotion={}
        return(stmids,stmdata,stmmotion)

    stmdata={}
    stmids=[]
    stmmotion={}

    gotstmid=BtOps2Stm(stmids,stmdata,stmmotion,stmidset,bdeck)

    if(gotstmid == 0): sys.exit()

    return(stmids,stmdata,stmmotion)


def Carq2Ngtrp(dtg,stmids,stmdata,stmmotion,ngtrppath):

    verb=0
    
    curdtg=mf.dtg6()

    ntc=0
    for stmid in stmids:
        ntc=ntc+1

    if(verb): print 'NNN000 ntc: ',ntc

    yymmddhh=dtg[2:]
    curyyyymmdd=curdtg[0:8]

    ngpcards=[]
    
    ncard1="%1d  %8s     at %s  902841"%(int(ntc),yymmddhh,curyyyymmdd)
    
    if(verb): print 'NNN111 ',ncard1

    ncard1=ncard1+'\n'

    ngpcards.append(ncard1)

    ntc=1
    for stmid in stmids:

        (stmdtg,rlat,rlon,stmvmax,stmpmin)=stmdata[stmid,'posit']
        (quada,r1a,r2a,r3a,r4a)=stmdata[stmid,'r34']
        (quadb,r1b,r2b,r3b,r4b)=stmdata[stmid,'r50']

        r34bar=(r1a+r2a+r3a+r4a)/4.0
        r50bar=(r1b+r2b+r3b+r3b)/4.0
        
        (r1c,r2c)=stmdata[stmid,'roci']
        if(r1c == 'NA'): r1c=999

        (r1d)=stmdata[stmid,'rmax']
        if(r1d == 'NA'): r1d=999
        
        #ncardtest="034N 0900E 025 32 W -999 -999 2310 064"
        (course,speed)=stmmotion[stmid,'motion']
        icourse=int(course)
        ispeed=int(speed)

        #print 'QQQQQ ',r34bar,r50bar

        r34bar=int(r34bar)
        r50bar=int(r50bar)
        
        if(r34bar >= 900): r34bar=-999
        if(r50bar >= 900): r50bar=-999
        
        stmnum=stmid[0:2]
        stmbasin=stmid[2:3]
        stmbasin=stmbasin.upper()
        (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(rlat,rlon)
        ngpstmdata=(int(ilat),hemns,int(ilon),hemew,int(stmvmax),
                    stmnum,stmbasin,r50bar,r34bar,int(icourse)*10,int(ispeed)*10)
        ncard="%03d%1s %04d%1s %03d %2s %1s %4d %4d %04d %03d"%ngpstmdata
        if(verb): print 'NNN222 ',ncard
        
        ncard=ncard+'\n'
        ngpcards.append(ncard)
            
        ntc=ntc+1

    o=open(ngtrppath,'w')
    o.writelines(ngpcards)
    o.close()

    return(ngpcards)


def Bdeck2Stm(stmids,stmdata,stmidset,carq):

    verb=0
    b21=Basin2toBasin1

    gotstmid=0

    for c in carq:
        if(verb): print 'BEST CARD: ',c
        tt=string.split(c,',')
        b2=tt[0]
        stid=tt[1]

        #
        # filter out 8X storms
        #
        bid=b21[b2]
        stmnum=int(stid)
        
        if( stmnum >= 80 and stmnum <= 89 ):
            continue

        stmid=stid+bid
        stmid=stmid.strip()
        
        stmdtg=tt[2]
        stmclat=tt[6]
        stmclon=tt[7]
        stmvmax=tt[8]
        
        #
        # 20021227 - pull stmid from the carq card for shem
        #

        if(b2 == 'SH'):

            stid=stid.strip()
            
            try:
                there22=1
                stmbid=tt[22]
                stmbid=stmbid.strip()
                
            except:
                there22=0

            if(there22 == 0 or stmbid == ''):
               
                lon=float(stmclon[0:len(stmclon)-1])*0.1
                bid=stmclon[(len(stmclon)-1):len(stmclon)]
                #
                # pacom 3140.1X S -> lon <=135E
                #
                if(bid == 'E' and lon >= 135.0):
                    stmbid='P'
                elif(bid == 'W'):
                    stmbid='P'
                else:
                    stmbid='S'

            
            stmid=stid+stmbid
            if(verb): print "WWWWWWWWWWWWWW shem stid calc",stmclon,bid,stid,stmid
        
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
        
        stmdtg=tt[2]
        stmclat=tt[6]
        stmclon=tt[7]
        stmvmax=tt[8]

        stmpmin=-999
    
        stmdata[stmid,'posit']=(stmdtg,stmclat,stmclon,stmvmax,stmpmin)
        try:
            stmdata[stmid,'r34']
            if(verb): print 'CCC R34',stmdata[stmid,'r34']
        except:
            stmdata[stmid,'r34']=('NA',999,999,999,999)

        try:
            stmdata[stmid,'r50']
            if(verb): print 'CCC R50',stmdata[stmid,'r50']
        except:
            stmdata[stmid,'r50']=('NA',999,999,999,999)

        try:
            stmdata[stmid,'roci']
            if(verb): print 'CCC ROCI',stmdata[stmid,'roci']
        except:
            stmdata[stmid,'roci']=('NA',999)

        try:
            stmdata[stmid,'rmax']
            if(verb): print 'CCC RMAX',stmdata[stmid,'rmax']
        except:
            stmdata[stmid,'rmax']=('NA')

        if(len(tt) >= 18):
            pmin=tt[9]
            vrad=int(tt[11])
            quad=tt[12].strip()
            stmdata[stmid,'posit']=(stmdtg,stmclat,stmclon,stmvmax,stmpmin)

            if(vrad == 34 or vrad == 35):
                try:
                    stmdata[stmid,'r34']=(quad,int(tt[13]),int(tt[14]),int(tt[15]),int(tt[16]))
                except:
                    stmdata[stmid,'r34']=('NA',999,999,999,999)

            if(vrad == 50):
                try:
                    stmdata[stmid,'r50']=(quad,int(tt[13]),int(tt[14]),int(tt[15]),int(tt[16]))
                except:
                    stmdata[stmid,'r50']=('NA',999,999,999,999)

            try:
                stmdata[stmid,'roci']=(int(tt[17]),int(tt[18]))
            except:
                stmdata[stmid,'roci']=('NA',999)

            try:
                stmdata[stmid,'rmax']=(int(tt[19]))
            except:
                stmdata[stmid,'rmax']=('NA')


    return(gotstmid)





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



def Carq2Stm(stmids,stmdata,stmidset,carq):

    verb=0
    b21=Basin2toBasin1

    gotstmid=0

    for c in carq:
        if(verb): print 'CARQ CARD: ',c
        tt=string.split(c,',')
        b2=tt[0]
        stid=tt[1]
        bid=b21[b2]
        
        #
        # filter out 8X storms
        #
        bid=b21[b2]
        stmnum=int(stid)
        
        if( stmnum >= 80 and stmnum <= 89 ):
            continue

        stmid=stid+bid
        stmid=stmid.strip()
        
        stmdtg=tt[2]
        stmclat=tt[6]
        stmclon=tt[7]
        stmvmax=tt[8]
        
        #
        # 20021227 - pull stmid from the carq card for shem
        #

        if(b2 == 'SH'):

            stid=stid.strip()
            
            try:
                stmbid=tt[22]
                stmbid=stmbid.strip()
                
            except:

                lon=float(stmclon[0:len(stmclon)-1])*0.1
                bid=stmclon[(len(stmclon)-1):len(stmclon)]
                #
                # pacom inst 3140.1X S -> <= 135E
                #
                if(bid == 'E' and lon >= 135.0):
                    stmbid='P'
                elif(bid == 'W'):
                    stmbid='P'
                else:
                    stmbid='S'

            
            stmid=stid+stmbid
            if(verb): print "WWWWWWWWWWWWWW shem stid calc",stmclon,bid,stid,stmid
        
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
        
        stmdtg=tt[2]
        stmclat=tt[6]
        stmclon=tt[7]
        stmvmax=tt[8]
        

        stmpmin=-999
    
        stmdata[stmid,'posit']=(stmdtg,stmclat,stmclon,stmvmax,stmpmin)
        try:
            stmdata[stmid,'r34']
            if(verb): print 'CCC R34',stmdata[stmid,'r34']
        except:
            stmdata[stmid,'r34']=('NA',999,999,999,999)

        try:
            stmdata[stmid,'r50']
            if(verb): print 'CCC R50',stmdata[stmid,'r50']
        except:
            stmdata[stmid,'r50']=('NA',999,999,999,999)

        try:
            stmdata[stmid,'roci']
            if(verb): print 'CCC ROCI',stmdata[stmid,'roci']
        except:
            stmdata[stmid,'roci']=('NA',999)

        try:
            stmdata[stmid,'rmax']
            if(verb): print 'CCC RMAX',stmdata[stmid,'rmax']
        except:
            stmdata[stmid,'rmax']=('NA')

        if(len(tt) >= 18):
            pmin=tt[9]
            vrad=int(tt[11])
            quad=tt[12].strip()
            stmdata[stmid,'posit']=(stmdtg,stmclat,stmclon,stmvmax,stmpmin)

            if(vrad == 34 or vrad == 35):
                try:
                    stmdata[stmid,'r34']=(quad,int(tt[13]),int(tt[14]),int(tt[15]),int(tt[16]))
                except:
                    stmdata[stmid,'r34']=('NA',999,999,999,999)

            if(vrad == 50):
                try:
                    stmdata[stmid,'r50']=(quad,int(tt[13]),int(tt[14]),int(tt[15]),int(tt[16]))
                except:
                    stmdata[stmid,'r50']=('NA',999,999,999,999)

            try:
                stmdata[stmid,'roci']=(int(tt[17]),int(tt[18]))
            except:
                stmdata[stmid,'roci']=('NA',999)

            try:
                stmdata[stmid,'rmax']=(int(tt[19]))
            except:
                stmdata[stmid,'rmax']=('NA')


    return(gotstmid)


def StmIdsStmDataFromCarqNgtrp(otdir,dtg):

    verb=0

    cmask="%s/carq.*"%(otdir)
    cf=glob.glob(cmask)

    stmids=[]
    stmparms={}

    for c in cf:
        o=open(c)
        tt=o.readlines()
        o.close()
        carqcard=tt[1]
        tt=carqcard.split()
        stm=tt[0]
        vmax=int(tt[1])
        rmax=int(tt[2])
        r34=0
        for i in range(3,7,1):
            r34=r34+int(tt[i])
            
        r34=int(float(r34)*0.25)
        stmids.append(stm)
        stmparms[stm]=(vmax,rmax,r34)

    if(verb):
        for stmid in stmids:
            print 'QQQQQ ',stmid


    stmdata={}

    nmask="%s/ngtrk.ngtrp.???.*"%(otdir)
    nf=glob.glob(nmask)

    for n in nf:

        o=open(n)
        ncards=o.readlines()
        o.close()

        i=1
        for ncard in ncards:
            if(i==1):
                ntc=ncard.split()[0]
            elif(i>1):
                tt=ncard.split()
                clat=tt[0]
                clon=tt[1]
                vmax=tt[2]
                stmnum=tt[3]
                stmbasin=tt[4]
                stmid="%02d%s"%(int(stmnum),stmbasin)
                if(verb): print 'SSSSS ',ncard,ntc,clat,clon,stmid
                stmdata[stmid,'posit']=(dtg,clat,clon,vmax,'9999')

            i=i+1

    if(verb):
        for stmid in stmids:
            print 'FFFF ',stmdata[stmid,'posit']

    return(stmids,stmdata)



def MakeCarqStormFile(model,otdir,curdir,pdir,wpddir,
                      dtg,stmids,stmdata):

    carqcards={}
    
    for stm in stmids:

        stmup=stm.upper()
        
        cfile="%s/carq.%s.%s.txt"%(otdir,stm,dtg)
        carq=open(cfile,'w')

        print 'stm ',stm,stmdata[stm,'posit']

        print 'rmax',stmdata[stm,'rmax']
        print 'deye',stmdata[stm,'deye']
        print ' r34',stmdata[stm,'r34']
        print ' r50',stmdata[stm,'r50']
        print 'roci',stmdata[stm,'roci']

        (stmdtg,stmclat,stmclon,stmvmax,stmpmin)=stmdata[stm,'posit']

        #
        # header card
        #
        carqhead='STM VMAX RMAX R3NE R3SE R3SW R3NW R5NE R5SE R5SW R5NW PRCI ROCI DEYE\n'

        #
        # stmid, vmax, rmax, deye
        #
        if(stmdata[stm,'rmax'] == 'NA'):
            r1=0
        else:
            r1=int(stmdata[stm,'rmax'])

        stm3=stm.split('.')[0]
        carqcard="%3s %04d %04d"%(stm3,int(stmvmax),r1)
        
        #
        # r34
        #
        print 'R34: ',stmdata[stm,'r34']
        if(stmdata[stm,'r34'][0] != 'NA'):
            (quad,r1,r2,r3,r4)=stmdata[stm,'r34']
        else:
            r1=r2=r3=r4=0.0
        carqcard="%s %04d %04d %04d %04d"%(carqcard,r1,r2,r3,r4)

        #
        # r50
        #
        if(stmdata[stm,'r50'][0] != 'NA'):
            (quad,r1,r2,r3,r4)=stmdata[stm,'r50']
        else:
            r1=r2=r3=r4=0
        carqcard="%s %04d %04d %04d %04d"%(carqcard,r1,r2,r3,r4)

        #
        # roci
        #

        if(stmdata[stm,'roci'][0] != 'NA'):
            (proci,roci)=stmdata[stm,'roci']
        else:
            (proci,roci)=(9999,9999)

        #
        # deye
        #

        if(stmdata[stm,'deye'] == 'NA'):
            deye=0
        else:
            deye=int(stmdata[stm,'deye'])


        carqcard="%s %04d %04d %04d"%(carqcard,proci,roci,deye)

        print 'CARQ card: ',carqcard
        carq.writelines(carqhead)
        carq.writelines(carqcard)
        carqcards[stm]=carqcard
        carq.close()


    return(carqcards)

#----------------------------------------------------------------------
#
#  animate gif plot
#
#----------------------------------------------------------------------

def AnimateGifPlot(ogdir,stm,model,dtg):

    convertexe=w2.BinBdirW2+'/convert'

    btau=0
    etau=120
    
    dtau=12

    delayfactorbeg=150
    delayfactorloop=100

    gifpath='%s/animate.%s.%s.%s.gif'%(ogdir,model,stm,dtg)

    nplt=0

    taus=xrange(btau,etau+1,dtau)

    for tau in taus:

        nplt=nplt+1

        pfile="plt.%s.%s.%03d.png"%(model,stm,int(tau))
        pfile="%s/%s"%(ogdir,pfile )

        if(nplt == 1):
            ccmd="-loop 0 -delay %s %s -delay %s"%(delayfactorbeg,pfile,delayfactorloop)
        else:
            ccmd="%s %s"%(ccmd,pfile)

    ccmd="%s %s %s"%(convertexe,ccmd,gifpath)

    print ccmd
    os.system(ccmd)

    return


def FieldsThere(model,dtg,specopt=None):

    if(w2.IsModel2(model)):
        fpath=w2.Model2CtlPath(model,dtg)
        (localpaths,localarchpaths)=w2.Model2LocalArchivePaths(model,dtg)
        for path in localarchpaths:
            if(os.path.exists(path)): fpath=path


    else:
        fdir=w2.NwpDataBdir(model)
        res=w2.ModelRes(model)
        if(specopt == 'npmoc.ldm'):
            fpath="%s/%s.LDM.%s.%s.ctl"%(fdir,model,res,dtg)
        if(specopt == 'cagips'):
            fpath="%s/%s.%s.cagips.%s.ctl"%(fdir,model,res,dtg)
        else:
            fpath="%s/%s.%s.%s.ctl"%(fdir,model,res,dtg)
            
    status=1
    try:
        if(not(os.path.exists(fpath))):
            print "Fields for model: %s on dtg: %s NOT THERE..."%(model,dtg)
            print "fpath: %s"%(fpath)
            status=0
    except:
        status=0
        fpath=None

    return(status,fpath)


def FieldsRestore(model,dtg):

    pdir=w2.PrcDirFlddatW2
    rscript="w2.archive.fld.py -d %s -m %s -p get"%(dtg,model)

    cmd="%s/%s"%(pdir,rscript)
    print "CCC: %s\n"%(cmd)
    os.system(cmd)

    return(1)
    
def FieldsRemove(model,dtg):
    
    fdir=w2.NwpDataBdir(model)
    res=ModelRes(model)
    fpath="%s/%s.%s.%s.*"%(fdir,model,res,dtg)
    cmd="rm -i %s"%(fpath)
    print "CCC remove: ",cmd
    os.system(cmd)

    return(1)

def ParseHeadMFdiag(n,cards):

    verb=0
    tt=cards[n].split()
    type=tt[0]
    rtau=float(tt[2])
    stm=tt[4]
    rlon0=float(tt[5])
    rlat0=float(tt[6])
    if(verb): print 'mm1 ',cards[n],len(cards),type,rtau,stm,rlat0,rlon0

    n=n+1
    tt=cards[n].split()
    
    npts=int(tt[0])+int(tt[1])
    
    if(verb): print 'mm2 ',npts

    return(n,stm,rtau,rlat0,rlon0,type,npts)

def ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts):

    #
    # mf 20090401 -- changed format of the mf diag output from ngtrk.x
    #
    verb=0
    
    maxtau=-999.0
    disttau=-999.0

    for nn in range(0,npts):
        n=n+1
        try:
            tt=cards[n].split()
            doparse=1
        except:
            doparse=0

        if(doparse):
            dist=float(tt[1])
            rlon=float(tt[2])
            rlat=float(tt[3])
            rmax=float(tt[4])
            
            if(rmax>maxtau):
                maxtau=rmax
                disttau=dist
        
        if(verb):
            print "%s :: %6.2f %6.2f %6.2f %6.2f"%('mm3 ',rlat,rlon,rmax,dist)

    n=n+1

    return(n,maxtau,disttau)


def ParseNgtrkTrackCards(ngtrkpath,verb=0):
    
    o=open(ngtrkpath)
    cards=o.readlines()
    o.close()
    
    ncards=len(cards)
    
    n=0
    tt=cards[n].split()
    nstm=int(tt[0])

    stmids=[]
    stmdata={}
    stmtaus={}
    
    n=n+1
    
    for i in range(0,nstm):
        tt=cards[n].split()
        stmids.append(tt[0])
        n=n+1
        
    # next card is blank
        
    n=n+1

    while(n < ncards):
    
        tt=cards[n].split()
        tau=tt[0]
            
        if(tau == '***'):
            stm=tt[1]
            rlatcarq=float(tt[2])
            rloncarq=float(tt[3])
            itau=0

            stmdata[stm,itau,'carq']=(rlatcarq,rloncarq)

        elif(tau.find('FIN') >= 0 or tau.find('LOS') >= 0):
            print 'done/lost'

        else:
            stm=tt[1]
            rlat=tt[2]
            rlon=tt[3]
            rdir=tt[4]
            rspd=tt[5]
            rcnf="%s %s %s"%(tt[6],tt[7],tt[8])
            itau=int(tau)
            rlatfc=float(rlat)
            rlonfc=float(rlon)

            if(verb): print 'nnn ',itau,stm,rlat,rlon,rdir,rspd,rcnf
            if(rlatfc > 90.0):
                n=n+1
                continue            

            rdirfc=float(rdir)
            rspdfc=float(rspd)

            stmdata[stm,itau,'fcst']=(rlatfc,rlonfc,rdirfc,rspdfc,rcnf)
            
            try:
                stmtaus[stm].append(itau)
            except:
                stmtaus[stm]=[]
                stmtaus[stm].append(itau)

        n=n+1

    return(stmids,stmdata,stmtaus)



def ParseNgtrkNgtrpDiagCards(ngtrkngtrppath,ngtrkdiagmfpath,verb=0):
    

    #----------------------------------------------------------------------
    # parse the ngtrp file
    #----------------------------------------------------------------------

    stmdatang={}
    stmidsng=[]
    stmvmaxmf={}
    stmidsmf=[]

    o=open(ngtrkngtrppath)
    cards=o.readlines()
    o.close()

    ncards=len(cards)

    n=1
    while(n < ncards):
        
        tt=cards[n].split()

        (tcrlat,tcrlon)=Clatlon2Rlatlon(tt[0],tt[1])

        stmid=tt[3]+tt[4]
        tcvmax=int(tt[2])
        tcdir=float(tt[7])*0.1
        tcspd=float(tt[8])*0.1
        tcr34=float(tt[5])
        tcr50=float(tt[6])

        stmidsng.append(stmid)
        
        stmdatang[stmid,'tcvmax']=tcvmax
        stmdatang[stmid,'tcdir']=tcdir
        stmdatang[stmid,'tcspd']=tcspd
        stmdatang[stmid,'tcr34']=tcr34
        stmdatang[stmid,'tcr50']=tcr50
        stmdatang[stmid,'tcrlat']=tcrlat
        stmdatang[stmid,'tcrlon']=tcrlon

        n=n+1

    #----------------------------------------------------------------------
    # parse the mf diag file from ngtrk.x
    #----------------------------------------------------------------------

    o=open(ngtrkdiagmfpath)
    cards=o.readlines()
    o.close()

    ncards=len(cards)
    if(verb): print 'NNN ncards ',ncards,ngtrkdiagmfpath
    
    n=0
    while(n < ncards):
        
        (n,stm,rtau,rlat0,rlon0,type,npts)=ParseHeadMFdiag(n,cards)
        stmidsmf.append(stm)
        
        (n,maxtau,disttau)=ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts)
        if(verb): print 'EXTRMA n: ',n,maxtau,disttau,type,stm,rlat0,rlon0

        if(type == 'SPD'):
            tau=int(rtau)
            stmvmaxmf[stm,tau,'vmax']=maxtau
            stmvmaxmf[stm,tau,'dist']=disttau


    if(len(stmidsmf) == 0):
        rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)

    stmidsmf=mf.uniq(stmidsmf)

    dtau=12
    etau=120
    btau=0

    for stm in stmidsmf:

        for tau in range(btau,etau+1,dtau):
            
            try:
                vmax=stmvmaxmf[stm,tau,'vmax']
                dist=stmvmaxmf[stm,tau,'dist']
                if(tau >= dtau):
                    taumdtau=tau-dtau
                    dvmax=stmvmaxmf[stm,tau,'vmax']-stmvmaxmf[stm,0,'vmax']
                    dvmax=dvmax/stmvmaxmf[stm,0,'vmax']
                elif(tau == 0):
                    dvmax=0.0
                stmvmaxmf[stm,tau,'dvmax']=dvmax

                if(verb): print 'TTTT %s :: %03d  %6.1f  %7.1f  %7.3f'%(stm,tau,vmax,dist,dvmax)
                
            except:
                
                stmvmaxmf[stm,tau,'vmax']=-999
                stmvmaxmf[stm,tau,'dist']=-999
                stmvmaxmf[stm,tau,'dvmax']=-999
                if(verb): print 'TTTT(except) %s :: %03d  %6.1f  %7.1f  %7.3f'%(stm,tau,vmax,dist,dvmax)
                
                test=1

    rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)
    return(rc)



def Ngtrk2Adeck(dtg,model,trk1,trk2,
                otdir,oadir,biascorrvmax=0):

    verb=0

    ntcfs={}
    
    (ngtrktrackpath1,ngtrkdiagmfpath1,ngtrkngtrppath1)=trk1
    (ngtrktrackpath2,ngtrkdiagmfpath2,ngtrkngtrppath2)=trk2
    
    #----------------------------------------------------------------------
    # read in ngtrk ngtrp and diag 
    #----------------------------------------------------------------------

    (stmdatang1,stmidsng1,stmvmaxmf1,stmidsmf1)=ParseNgtrkNgtrpDiagCards(ngtrkngtrppath1,ngtrkdiagmfpath1)
    (stmdatang2,stmidsng2,stmvmaxmf2,stmidsmf2)=ParseNgtrkNgtrpDiagCards(ngtrkngtrppath2,ngtrkdiagmfpath2)

    #----------------------------------------------------------------------
    # read in ngtrk track
    #----------------------------------------------------------------------

    (stmids1,stmdata1,stmtaus1)=ParseNgtrkTrackCards(ngtrktrackpath1)
    (stmids2,stmdata2,stmtaus2)=ParseNgtrkTrackCards(ngtrktrackpath2)

    (stmids,stmdata,stmtaus,stmdatang,stmidsng,stmvmaxmf,stmidsmf)=SetBestNgtrkTrack(
        dtg,model,
        stmids1,stmdata1,stmtaus1,stmdatang1,stmidsng1,stmvmaxmf1,stmidsmf1,
        stmids2,stmdata2,stmtaus2,stmdatang2,stmidsng2,stmvmaxmf2,stmidsmf2
        )

    amodel=model
    #if(w2.IsModel2(model)): amodel=model[0:3]
        
    adeckname=atcf.ModelNametoAdeckName[amodel]
    adecknum=atcf.ModelNametoAdeckNum[amodel]
        
    pmin=0
    r34ne=0
    r34se=0
    r34sw=0
    r34nw=0
    
    for stmid in stmids:

        #
        # open adeck file
        #
        stmlow=stmid
        adeckpath="%s/wxmap.%s.%s.%s.txt"%(otdir,amodel,dtg,stmlow)
        adeckatcfpath="%s/wxmap.%s.%s.%s"%(oadir,amodel,dtg,stmid)
        #
        # --- create symbolic link between local ngp2 and ngp wxmap adeck ... nhc feed missing tau0
        #
        if(amodel == 'ngp2'):
            adeckatcfpathalias="%s/wxmap.%s.%s.%s"%(oadir,amodel[0:3],dtg,stmid)
        else:
            adeckatcfpathalias=''

        if(adeckatcfpathalias != ''):
            cmd="ln -s %s %s"%(adeckatcfpath,adeckatcfpathalias)
            mf.runcmd(cmd,'')
            
        if(verb >= 0):
            print 'AAAA:     adeckpath: ',adeckpath
            print 'AAAA: adeckatcfpath: ',adeckatcfpath

        a=open(adeckpath,'w')
        aatcf=open(adeckatcfpath,'w')
        
        stmnum=stmid[0:2]
        basin1=stmid[2:]
        basin2=Basin1toBasin2[basin1]

        if(verb): print 'SSS ',stmid,basin1,basin2,adeckname,adecknum

        vmaxbias=int(stmdatang[stmid,'tcvmax']) - int(stmvmaxmf[stmid,0,'vmax'])
        
        vmax0=stmvmaxmf[stmid,0,'vmax']

        ntcfcst=0

        print
        for itau in stmtaus[stmid]:

            try:
                (rlatfc,rlonfc,rdirfc,rspdfc,rcnf)=stmdata[stmid,itau,'fcst']
                (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(rlatfc,rlonfc)
                vmax=stmvmaxmf[stmid,itau,'vmax']
                dvmax=stmvmaxmf[stmid,itau,'dvmax']
                ntcfcst=ntcfcst+1

            except:
                continue
                

            if(biascorrvmax):
                #
                # bias correct vmax forecast
                #
                
                vmaxadd=vmax
                if(dvmax != -999):
                    vmaxadd=vmax0 + vmax0*dvmax
                    
                    vmaxcorr=vmaxadd+vmaxbias
                    
                #
                # round to nearest 5 kt
                #

                vmaxcorr=int(float(vmaxcorr)/5.0 + 0.5)*5

            else:
                vmaxcorr=vmax
          
            if(verb):
                print "VVV %6.1f %7.3f %6.1f %3d"%(vmax0,dvmax,vmaxadd,vmaxcorr)
                print 'FFF %03d  %6.1f  %7.1f :: %6.1f %6.1f'%(itau,rlatfc,rlonfc,rdirfc,rspdfc)
                print "FFF %03d %03d%1s %04d%1s"%(itau,ilat,hemns,ilon,hemew)
                
            acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,dtg,adecknum,adeckname,itau)
            # 20030428 -- make more atcf friendly
            adum=0 
            acard1=" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                    (ilat,hemns,ilon,hemew,vmaxcorr,pmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

            acard=acard0+acard1
            print 'AAA %s'%(acard)
            acard=acard+'\n'

            a.writelines(acard)
            aatcf.writelines(acard)

        a.close()
        aatcf.close()
        
        ntcfs[stmid]=ntcfcst

    #
    # add lower case stmid to ntcfs
    #
    
    for stmid in stmids:
        stmlow=stmid
        ntcfs[stmlow]=ntcfs[stmid]
        print 'NNNNNNNNNNNNNN ntcfs: ',stmlow,' ',ntcfs[stmid]

    return(ntcfs,stmids,stmdata,stmidsng,stmdatang)



def TcStruct2BtFtGs(dtg,model,stmids,stmdata,stmidsng,stmdatang,
                    ngtrktcbtftgsfpath):


    amodel=model
    #if(w2.IsModel2(model)): amodel=model[0:3]

    verb=0

    cards=[]

    cards.append('function tcbtft()\n')

    etau6=48
    btau12=60
    etauall=120
    
    taus6=range(0,etau6+1,6)
    taus=range(btau12,etauall+1,12)

    tausall=taus6+taus
    
    for tau in tausall:

        nt=1
        itau=int(tau)

        if( itau%12 == 6 and itau < 48 and itau > 0):
            
            itau0=int(tau-6)
            itau12=int(tau+6)
        
            for stmid in stmids:
                try:
                    (rlat0,rlon0,rdir0,rspd0,rcnf0)=stmdata[stmid,itau0,'fcst']
                    (rlat1,rlon1,rdir1,rspd1,rcnf1)=stmdata[stmid,itau12,'fcst']
                    rlat=(rlat1+rlat0)*0.5
                    rlon=(rlon1+rlon0)*0.5

                    gsfcard="_tcft.%d.%d='%5.2f %6.2f %s'"%(itau,nt,rlat,rlon,rcnf0.split()[0])
                    cards.append(gsfcard)
                    nt=nt+1
                except:
                    print 'no data for ',stmid,itau
                    continue

        else:

            for stmid in stmids:
                try:
                    (rlat,rlon,rdir,rspd,rcnf)=stmdata[stmid,itau,'fcst']
                    gsfcard="_tcft.%d.%d='%5.2f %6.2f %s'"%(itau,nt,rlat,rlon,rcnf.split()[0])
                    cards.append(gsfcard)
                    nt=nt+1
                except:
                    print 'no data for ',stmid,itau
                    continue

                
        if(nt == 1):
            gsfcard="_ntcft.%s=0"%(itau)
        else:
            nt=nt-1
            gsfcard="_ntcft.%s=%d"%(itau,nt)
        cards.append(gsfcard)
        cards.append(' ')


            
        if(nt == 1):
            gsfcard="_ntcft.%s=0"%(itau)
        else:
            nt=nt-1
            gsfcard="_ntcft.%s=%d"%(itau,nt)


    #
    # 20080507 -- case where only one storm and model completely failed to track -> no stmids which are calculated
    # from tracked storms... this causes the except: and added code to put a _tcbt.1 card so the drawtcbt.gsf doesn't fail
    #
    
    nbt=1
    for stmid in stmidsng:
        try:
            tcrlat=stmdatang[stmid,'tcrlat']
            tcrlon=stmdatang[stmid,'tcrlon']
            tcvmax=stmdatang[stmid,'tcvmax']
            gsfcard="_tcbt.%d='%5.2f %6.2f %d %s'"%(nbt,tcrlat,tcrlon,tcvmax,stmid)
            cards.append(gsfcard)
            nbt=nbt+1
        except:
            gsfcard="_tcbt.%d='%5.2f %6.2f %d %s'"%(nbt,-99.,-999.,-99,stmid)
            cards.append(gsfcard)
            gsfcard="_ntcbt=0"
            cards.append(gsfcard)
            continue

        #print 'no data for ',stmid,itau

    if(nbt == 1):
        gsfcard="_tcbt.%d='%5.2f %6.2f %d exception'"%(nbt,-99.,-999.,-99)
        cards.append(gsfcard)
        gsfcard="_ntcbt=0"
        cards.append(gsfcard)
    else:
        nbt=nbt-1
        gsfcard="_ntcbt=%d"%(nbt)
        cards.append(gsfcard)
        cards.append(' ')

    cards.append('return')

    print 'OOOOO - gfs tracker: ',model,' path: ',ngtrktcbtftgsfpath
    GS=open(ngtrktcbtftgsfpath,'w')
    for card in cards:
        GS.writelines(card+'\n')
        ###print card

    GS.close()
    
    return



def TcStruct2BtOfGs(dtg,model,otdir,
                    ngtrktcbtofgsfpath,verb=0,ropt=''):


    amodel=model
    #if(w2.IsModel2(model)): amodel=model[0:3]

    dtautracker=atcf.DtauModelTracker[amodel]

    #
    #  cp from nhc/jtwc adeck dirs, wxmap.ofc? forms of ofcl/ofci tracks for overlay on model track
    #

    year=dtg[0:4]
    ofcljtwcdir="%s/%s/wxmap"%(w2.TcAdecksJtwcDir,year)
    cmd="cp %s/wxmap.ofc?.%s.??? %s/."%(ofcljtwcdir,dtg,otdir)
    mf.runcmd(cmd,ropt)

    ofclnhcdir="%s/%s/wxmap"%(w2.TcAdecksNhcDir,year)
    cmd="cp %s/wxmap.ofc?.%s.??? %s/."%(ofclnhcdir,dtg,otdir)
    mf.runcmd(cmd,ropt)

    #
    # go for both ofc and ofi
    #
    amask="%s/wxmap.ofc?.%s.???"%(otdir,dtg)
    adecks=glob.glob(amask)

    #
    # pick ofc over ofi
    #

    stms=[]
    for adeck in adecks:
        (dir,file)=os.path.split(adeck)
        (ofile,stm)=os.path.splitext(file)
        stms.append(stm[1:])

    #
    # if no ofc? forecasts...
    #
    if(len(stms) == 0):
        return

    ustms=mf.uniq(stms)

    uadecks=[]

    for stm in ustms:
        ofcadeck="%s/wxmap.ofcl.%s.%s"%(otdir,dtg,stm)
        ofiadeck="%s/wxmap.ofci.%s.%s"%(otdir,dtg,stm)
        ofcthere=os.path.exists(ofcadeck)
        ofithere=os.path.exists(ofiadeck)

        if(ofcthere and ofithere):
            uadecks.append(ofcadeck)

        elif(not(ofcthere) and ofithere):
            uadecks.append(ofiadeck)

        elif(ofcthere and not(ofithere)):
            uadecks.append(ofcadeck)


    adecks=copy.deepcopy(uadecks)

    if(verb):
        print 'aaaa ',amask
        print adecks

    gscards=[]
    
    if(len(adecks) == 0):
        ftcs=None
        ftcstruct=None
        return(ftcs,ftcstruct)

    else:

        oflatlons={}
        for adeck in adecks:
            try:
                cards=open(adeck).readlines()
            except:
                cards=None
            
            if(cards != None):
                (ftcs,ftcs2,ftcstruct)=TCveri.ParseAdeckCards(dtg,cards,dtautracker)

                stms=ftcs.keys()
                for stm in stms:
                    ftc=ftcs[stm]

                    for i in range(0,len(ftc)):
                        tt=ftc[i]
                        if(i==0):
                            btlat=tt[0]
                            btlon=tt[1]
                            if(verb): print 'bttttttt ',btlat,btlon
                        else:
                            fttau=tt[0]
                            ftlat=tt[4]
                            ftlon=tt[5]
                            if(ftlat < 89.0):

                                if(fttau == 48):
                                    lat48=ftlat
                                    lon48=ftlon
                                elif(fttau == 72):
                                    lat72=ftlat
                                    lon72=ftlon
                                elif(fttau == 96):
                                    lat96=ftlat
                                    lon96=ftlon
                                elif(fttau == 120):
                                    lat120=ftlat
                                    lon120=ftlon
                                
                                if(verb): print 'fttttt ',fttau,ftlat,ftlon

                                try:
                                    oflatlons[fttau].append([ftlat,ftlon])
                                except:
                                    oflatlons[fttau]=[]
                                    oflatlons[fttau].append([ftlat,ftlon])

                                #
                                # interp for tau 60
                                #
                                if(fttau == 72):

                                    lat60=(ftlat+lat48)*0.5
                                    lon60=(ftlon+lon48)*0.5

                                    try:
                                        oflatlons[60].append([lat60,lon60])
                                    except:
                                        oflatlons[60]=[]
                                        oflatlons[60].append([lat60,lon60])
                                    


                                #
                                # interp for tau 84
                                #
                                if(fttau == 96):

                                    lat84=(ftlat+lat72)*0.5
                                    lon84=(ftlon+lon72)*0.5

                                    try:
                                        oflatlons[84].append([lat84,lon84])
                                    except:
                                        oflatlons[84]=[]
                                        oflatlons[84].append([lat84,lon84])
                                    

                                #
                                # interp for tau 108
                                #
                                if(fttau == 120):

                                    lat108=(ftlat+lat96)*0.5
                                    lon108=(ftlon+lon96)*0.5

                                    try:
                                        oflatlons[108].append([lat108,lon108])
                                    except:
                                        oflatlons[108]=[]
                                        oflatlons[108].append([lat108,lon108])
                                    



        taus=oflatlons.keys()
        taus.sort()

        card='function tcftof()'
        gscards.append(card)

        card=''
        gscards.append(card)

        for tau in taus:
            npts=len(oflatlons[tau])

            for i in range(0,npts):
                lat=0
                lon=0
                (lat,lon)=oflatlons[tau][i]
                card="_tcof.%d.%d='%5.1f %6.1f 1'"%(tau,i+1,lat,lon)
                gscards.append(card)

            card="_ntcof.%d=%s"%(tau,npts)
            gscards.append(card)

            card=''
            gscards.append(card)
                    

        card='return'
        gscards.append(card)


        if(verb):
            for gscard in gscards:
                print gscard

        print 'OOOOO - ofcl tracker .gsf: ',amodel,' path: ',ngtrktcbtofgsfpath
        GS=open(ngtrktcbtofgsfpath,'w')
        for gscard in gscards:
            GS.writelines(gscard+'\n')

        GS.close()
    

    return


#
# filter out stortm for limited-area model fields
#

def FiltStormIds(stmids,model):

    ostmids=[]
    for stmid in stmids:
        bid=stmid[2].upper()
        if(model == 'gsm'):
            if(bid == 'W'):
                ostmids.append(stmid)
        else:
            ostmids.append(stmid)

    #for ostmid in ostmids:
    #    print 'oooo ',ostmid

    return(ostmids)

def PrintCarqCards(dtg,model,stmids,stmdata):

    card="**** tc.ls: %s  for: %s"%( dtg,model)
    print
    print card
    print

    ntc=1
    for stmid in stmids:
    
        (quada,r1a,r2a,r3a,r4a)=stmdata[stmid,'r34']
        (quadb,r1b,r2b,r3b,r4b)=stmdata[stmid,'r50']
    
        (r1c,r2c)=stmdata[stmid,'roci']
        if(r1c == 'NA'): r1c=999

        (r1d)=stmdata[stmid,'rmax']
        if(r1d == 'NA'): r1d=999
    
        (r1e)=stmdata[stmid,'deye']
        if(r1e == 'NA'): r1e=999
    
        (stmdtg,stmclat,stmclon,stmvmax,stmpmin)=stmdata[stmid,'posit']

        card="TC #%d: %s | %03d | %s %6s"%(ntc,stmid,int(stmvmax),stmclat,stmclon)
        card=card+" | 34:%3s % 4d % 4d % 4d % 4d"%(quada,r1a,r2a,r3a,r4a)
        card=card+" | 50:%3s % 4d % 4d % 4d % 4d"%(quadb,r1b,r2b,r3b,r4b)
        card=card+" | CI:% 5d % 4d"%(r1c,r2c)
        card=card+" | RM:%4d"%(r1d)
        card=card+" | ED:%4d"%(r1e)
    
        print card
        ntc=ntc+1

    return
        

def SetModels(dtg,modelopt):

    hh=dtg[8:10]
    models=[]
    
    if(modelopt == 'all'):
        if(hh == '06' or hh == '18'):
            models=TcanalModelsoff
        else:
            models=TcanalModels
            
    elif(w2.IsModel2(modelopt)):
        models.append(modelopt)

    else:
        for tcmodel in TcanalModels:
            if(tcmodel == modelopt):
                models.append(modelopt)

    if(len(models) == 0):
        print 'EEE invalid model opt',modelopt
        sys.exit()
            
    return(models)

#
# cp over .gsf so plotter works
# needed because we don't want to rely on
# env
#
def SetPlotGsf(sdir,tdir):

    gsffiles=['mydate.gsf','ll2xy.gsf','tcadeck.gsf','pltradii.gsf']

    for gsffile in gsffiles:
        cmd="cp %s/%s %s"%(sdir,gsffile,tdir)
        mf.runcmd(cmd,'')

    return

        
def SetBestNgtrkTrack(
    dtg,model,
    stmids1,stmdata1,stmtaus1,stmdatang1,stmidsng1,stmvmaxmf1,stmidsmf1,
    stmids2,stmdata2,stmtaus2,stmdatang2,stmidsng2,stmvmaxmf2,stmidsmf2,
    ipemax=200.0,ipeclose=60.0,tdratiomin=70.0,sqrlmax=40.0,fnldistratiomax=30.0
    ):


    def bestrule(model):
        #
        # 0 -- use algorith
        # 1 -- always select sfc wind
        # 2 -- always select 850 vort
        
        rule=0
        if(model == 'fim8'):
            rule=2
            rule=0
        return(rule)

    
    def xequator(stmdata,stmid,taus):
        
        isshem=IsShemBasinStm(stmid)
        isxeq=0
        for tau in taus:
            flat=stmdata[stmid,tau,'fcst'][0]
            if(flat > -88.0 and flat < 88.0):
                if(isshem and flat > 0.0): isxeq=1
                if(not(isshem) and flat < 0.0): isxeq=1

        return(isxeq)



    stmids=[]
    stmdata={}
    stmtaus={}
    
    stmdatang={}
    stmidsng=[]
    stmvmaxmf={}
    stmidsmf=[]

    for stmid in stmids1:

        tcvmax=stmdatang1[stmid,'tcvmax']
        tcdir=stmdatang1[stmid,'tcdir']
        tcspd=stmdatang1[stmid,'tcspd']

        try:
            taus1=stmtaus1[stmid]
        except:
            taus1=[]
            
        try:
            taus2=stmtaus2[stmid]
        except:
            taus2=[]


        nt1=len(taus1)
        nt2=len(taus2)

        print
        print 'BBBB',dtg,' Best trker: ',stmid,' tcdir/tcspd: ',tcdir,tcspd

        ntest=0
        
        if( nt1 > 0 and nt2 == 0 ):
            best=1
            if(xequator(stmdata1,stmid,taus1)): best=0
            
        elif(nt1 == 0 and nt2 > 0):
            best=2
            if(xequator(stmdata2,stmid,taus2)): best=0

        elif( nt1 > 0 and nt2 > 0 ):

            if(nt2 > nt1):
                ataus=taus2
            else:
                ataus=taus1

            totdist1=0.0
            totdist2=0.0

            for k in range(0,len(ataus)):
                
                tau=ataus[k]
                taup=ataus[k-1]
            
                if(tau == 0):
                    
                    clat1=stmdata1[stmid,tau,'carq'][0]
                    clon1=stmdata1[stmid,tau,'carq'][1]
                
                    try:
                        flat10=stmdata1[stmid,tau,'fcst'][0]
                        flon10=stmdata1[stmid,tau,'fcst'][1]
                        ipe1=gc_dist(clat1,clon1,flat10,flon10)
                    except:
                        flon10=999.
                        flat10=99.
                        ipe1=999.

                    try:
                        flat20=stmdata2[stmid,tau,'fcst'][0]
                        flon20=stmdata2[stmid,tau,'fcst'][1]
                        ipe2=gc_dist(clat1,clon1,flat20,flon20)
                    except:
                        flat20=99.
                        flon20=999.
                        ipe2=999.

                    fdist12=gc_dist(flat10,flon10,flat20,flon20)
                    print 'BBBB',dtg,' ipe CARQ: ',clat1,clon1,' 1: %5.1f %6.1f ipe: %4.1f '%(flat10,flon10,ipe1),\
                          ' 2: %5.1f %6.1f ipe: %4.1f '%(flat20,flon20,ipe2),' fdist12: %4.1f'%(fdist12)

        
                try:
                    flat1f=stmdata1[stmid,tau,'fcst'][0]
                    flon1f=stmdata1[stmid,tau,'fcst'][1]

                    if(k > 0):
                        flat1fp=stmdata1[stmid,taup,'fcst'][0]
                        flon1fp=stmdata1[stmid,taup,'fcst'][1]
                        totdist1=totdist1+gc_dist(flat1f,flon1f,flat1fp,flon1fp)

                    spd1f=stmdata1[stmid,tau,'fcst'][3]

                except:
                    flat1f=-99.
                    flon1f=-999.
                    spd1f=-99.
                    
                try:
                    flat2f=stmdata2[stmid,tau,'fcst'][0]
                    flon2f=stmdata2[stmid,tau,'fcst'][1]
                    
                    if(k > 0):
                        flat2fp=stmdata2[stmid,taup,'fcst'][0]
                        flon2fp=stmdata2[stmid,taup,'fcst'][1]
                        totdist2=totdist2+gc_dist(flat2f,flon2f,flat2fp,flon2fp)
                    spd2f=stmdata2[stmid,tau,'fcst'][3]

                except:
                    flat2f=-99.
                    flon2f=-999.
                    spd2f=-99.

                    

                fdist12=-999.
                if(chklat(flat1f) and chklat(flat2f)):
                    fdist12=gc_dist(flat1f,flon1f,flat2f,flon2f)
                print 'ffff: %03d'%(tau),' 1: %5.1f %6.1f %4.1f '%(flat1f,flon1f,spd1f),' 2: %5.1f %6.1f %4.1f '%(flat2f,flon2f,spd2f),\
                      ' fdist12: %5.1f'%(fdist12)
            
            #
            # find distance from initial postion to final positions
            #

            flat1fnl=stmdata1[stmid,taus1[-1],'fcst'][0]
            flon1fnl=stmdata1[stmid,taus1[-1],'fcst'][1]
            i2fdist1=gc_dist(flat10,flon10,flat1fnl,flon1fnl)
            
            #
            # persistence forecast
            #
            (flat1pers,flon1pers)=rumltlg(tcdir,tcspd,taus1[-1],flat10,flon10)

            flat2fnl=stmdata2[stmid,taus2[-1],'fcst'][0]
            flon2fnl=stmdata2[stmid,taus2[-1],'fcst'][1]
            i2fdist2=gc_dist(flat20,flon20,flat2fnl,flon2fnl)
            (flat2pers,flon2pers)=rumltlg(tcdir,tcspd,taus2[-1],flat20,flon20)

            if(flat2pers == None or flat1pers == None):
                #
                # case where TC goes over the poles...
                #
                f2f2perdist=None
                f12f2dist=None
                f1f2perdist=None
            else:

                #
                # distance from final 1 and 2 points
                #
                f2f2perdist=gc_dist(flat2fnl,flon2fnl,flat2pers,flon2pers)
                f12f2dist=gc_dist(flat1fnl,flon1fnl,flat2fnl,flon2fnl)

                #
                # distance between final and persistence points
                #
                f1f2perdist=gc_dist(flat1fnl,flon1fnl,flat1pers,flon1pers)

            #
            # normalize all distacnce to per time step 12 h
            #
            #if(nt1 >= 2):
            #   totdist1=totdist1/(nt1-1)
            #   i2fdist1=i2fdist1/(nt1-1)
            #if(nt2 >= 2):
            #   totdist2=totdist2/(nt2-1)
            #   i2fdist2=i2fdist2/(nt2-1)

            #
            # squirely ratio =  distance from tau=0 to tau=final / total distance, if small the the storm did a lot of motion to go nowhere
            #
            sqrly1=sqrly2=-999.
            
            if(totdist1 > 0.0):
               sqrly1=(i2fdist1/totdist1)*100.0

            if(totdist2 > 0.0):
               sqrly2=(i2fdist2/totdist2)*100.0
            
            print 'BBBB',dtg,' select nt1/ipe1: %d %3.0f'%(nt1,ipe1),' nt2/ipe2: %d %3.0f'%(nt2,ipe2),' ipemax: ',ipemax,' ipeclose: ',ipeclose
            print 'BBBB',dtg,'    totdist1: %6.0f'%(totdist1),'  totdist2: %6.0f'%(totdist2)
            print 'BBBB',dtg,'    i2fdist1: %6.0f'%(i2fdist1),'  i2fdist2: %6.0f'%(i2fdist2)
            print 'BBBB',dtg,'    sqrly1/2: %3.0f  %3.0f'%(sqrly1,sqrly2)

            #print 'BBBB',dtg,' f1f2perdist: %6.0f'%(f1f2perdist),flat10,flon10,flat1pers,flon1pers
            #print 'BBBB',dtg,' f2f2perdist: %6.0f'%(f2f2perdist)

            #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
            #
            # selection rules:
            #
            # 1) take longest (tau) track if ipe <= ipemax
            #
            
            ipe1test=(ipe1 <= ipemax)
            ipe2test=(ipe2 <= ipemax)

            ipe1closetest=(ipe1 <= ipeclose)
            ipe2closetest=(ipe2 <= ipeclose)

            ipetest=0
            if(nt1 > nt2 and ipe1test):
                best=1
                ntest=1

            elif(nt2 > nt1 and ipe2test):
                best=2
                ntest=1

            #
            # if one track fails the ipemax test, just go with the one that passes
            #
            elif(ipe2test and not(ipe1test)):
                best=2
                ntest=22

            elif(not(ipe2test) and ipe1test):
                best=1
                ntest=11

            #
            # both failed...
            #
            elif(not(ipe2test) and not(ipe1test)):
                best=0
                ntest=99

            #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
            #
            # 2) if lengths =, go for lower ipe
            #
            elif(nt1 == nt2):
                
                if(ipe1 <= ipe2):
                    best=1
                else:
                    best=2

                ipetest=1
                
                #
                # go with the sfc if both are less than ipeclose (60 nm)
                #
                
                if(best == 2 and ipe1 < ipeclose):
                    ipetest=3
                    best=1

                ntest=2
                print 'BBBB',dtg,' nt1=nt2 ipetest: %d  best: %d'%(ipetest,best)

            #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
            #
            # 3) check length of track...if one track much shorter/longer than the other
            #    then use longer, unless ipe is very good
            #

            disttest=0
            tdratio=-999.0
            if(totdist1 <= totdist2 and totdist2 > 0.0):
                tdratio=(totdist1/totdist2)*100.0
                if(tdratio < tdratiomin and not(ipe1closetest)):
                    best=2
                    disttest=2
                    ntest=3
            elif(totdist1 > 0.0):
                tdratio=(totdist2/totdist1)*100.0
                if(tdratio < tdratiomin and not(ipe2closetest) ):
                    best=1
                    disttest=1
                    ntest=3
            else:
                distest=-1
                best=1
                ntest=3

            fnldisttest=0
            fnldstratio=-999.0


            #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
            #
            # 4) now check squirlyness -- tracks that are long but go near initial position -- go for the less squirly
            #

            sqrltest=0
            dsqrl=sqrly1-sqrly2

            print 'BBBB',dtg,'      dsqrl: %4.0f'%(dsqrl)

            if(abs(dsqrl) > sqrlmax):
                if(dsqrl > 0.0):
                    sqrltest=2
                    best=1
                    ntest=4
                elif(dsqrl < 0.0):
                    sqrltest=1
                    best=2
                    ntest=4

                print 'BBBBSSSQQQRRRLLLYYY setting best by squirelyness: disttest: ',disttest,' dsqrl: %4.0f'%(dsqrl),' best: ',best

            print 'BBBB',dtg,'       ntest: ',ntest,' ipetest: ',ipetest,' best= ',best
            print 'BBBB',dtg,'    disttest: ',disttest," tdratio: %3.0f"%(tdratio),' best= ',best


            #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
            #
            # 5) check a big difference between the trackers, go with sfc
            #

            totdist12=totdist1+totdist2
            if(totdist12 > 0.0 and f12f2dist != None):
                fnldistratio=(f12f2dist/totdist12*0.5)*100.0
            else:
                fnldistratio=0.0
                f12f2dist=-999.
                
            print 'BBBB',dtg,'   f12f2dist: %6.0f  fnldistratio: %3.0f fnldistratiomax: %3.0f'%(f12f2dist,fnldistratio,fnldistratiomax),\
                  ' disttest: ',disttest,' sqrltest: ',sqrltest
            if(totdist2 > 0.0 and totdist1 > 0.0 and disttest == 0 and sqrltest == 0 and fnldistratio > fnldistratiomax):
                best=1
                fnldisttest=0
                ntest=5
                print 'BBBBFFFNNNLLDDDRATIO   f12f2dist: %6.0f  fnldistratio: %3.0f  fnldisttest: %d'%(f12f2dist,fnldistratio,fnldisttest)

            #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
            #
            # 6) cross equator
            #
            
            if(best == 1 and xequator(stmdata1,stmid,taus1)):
                best=2
                ntest=6
                print 'BBBBB',dtg,' XXXXXXXXXEEEEEEEEEEEEEQQQQQQQQQQQQQQQ track 1, set best=2'
            if(best == 2 and xequator(stmdata2,stmid,taus2)):
                best=1
                ntest=6
                print 'BBBBB',dtg,' XXXXXXXXXEEEEEEEEEEEEEQQQQQQQQQQQQQQQ track 2, set best=1'

            
        else:
            
            #
            # no positions -- total failure of tracker
            #

            best=0
            ntest=0

        if(bestrule(model) > 0):
            best=bestrule(model)
            ntest="override by model: %s"%(model)
            
        print 'BBBB %s%s'%(dtg,'BBBBBBBBBBBBBBBBBBBB---> '),stmid,' best: ',best,' ntest: ',ntest

        if(best > 0):
            stmids.append(stmid)
            stmidsng.append(stmid)
            stmidsmf.append(stmid)

        if(best == 0):

                    
            stmidsng.append(stmid)
            stmdatang[stmid,'tcvmax']=stmdatang1[stmid,'tcvmax']
            stmdatang[stmid,'tcdir']=stmdatang1[stmid,'tcdir']
            stmdatang[stmid,'tcspd']=stmdatang1[stmid,'tcspd']
            stmdatang[stmid,'tcr34']=stmdatang1[stmid,'tcr34']
            stmdatang[stmid,'tcr50']=stmdatang1[stmid,'tcr50']
            stmdatang[stmid,'tcrlat']=stmdatang1[stmid,'tcrlat']
            stmdatang[stmid,'tcrlon']=stmdatang1[stmid,'tcrlon']
            
        elif(best == 1):

            stmdata[stmid,0,'carq']=stmdata1[stmid,0,'carq']

            for tau in taus1:
                stmdata[stmid,tau,'fcst']=stmdata1[stmid,tau,'fcst']
                stmvmaxmf[stmid,tau,'vmax']=stmvmaxmf1[stmid,tau,'vmax']
                stmvmaxmf[stmid,tau,'dist']=stmvmaxmf1[stmid,tau,'dist']
                stmvmaxmf[stmid,tau,'dvmax']=stmvmaxmf1[stmid,tau,'dvmax']

            stmtaus[stmid]=taus1
                    
            stmdatang[stmid,'tcvmax']=stmdatang1[stmid,'tcvmax']
            stmdatang[stmid,'tcdir']=stmdatang1[stmid,'tcdir']
            stmdatang[stmid,'tcspd']=stmdatang1[stmid,'tcspd']
            stmdatang[stmid,'tcr34']=stmdatang1[stmid,'tcr34']
            stmdatang[stmid,'tcr50']=stmdatang1[stmid,'tcr50']
            stmdatang[stmid,'tcrlat']=stmdatang1[stmid,'tcrlat']
            stmdatang[stmid,'tcrlon']=stmdatang1[stmid,'tcrlon']
            

        elif(best == 2):
        
            stmdata[stmid,0,'carq']=stmdata2[stmid,0,'carq']
            for tau in taus2:
                stmdata[stmid,tau,'fcst']=stmdata2[stmid,tau,'fcst']
                stmvmaxmf[stmid,tau,'vmax']=stmvmaxmf2[stmid,tau,'vmax']
                stmvmaxmf[stmid,tau,'dist']=stmvmaxmf2[stmid,tau,'dist']
                stmvmaxmf[stmid,tau,'dvmax']=stmvmaxmf2[stmid,tau,'dvmax']
                
            stmtaus[stmid]=taus2
            
            stmdatang[stmid,'tcvmax']=stmdatang2[stmid,'tcvmax']
            stmdatang[stmid,'tcdir']=stmdatang2[stmid,'tcdir']
            stmdatang[stmid,'tcspd']=stmdatang2[stmid,'tcspd']
            stmdatang[stmid,'tcr34']=stmdatang2[stmid,'tcr34']
            stmdatang[stmid,'tcr50']=stmdatang2[stmid,'tcr50']
            stmdatang[stmid,'tcrlat']=stmdatang2[stmid,'tcrlat']
            stmdatang[stmid,'tcrlon']=stmdatang2[stmid,'tcrlon']
            

    rc=(stmids,stmdata,stmtaus,stmdatang,stmidsng,stmvmaxmf,stmidsmf)

    return(rc)


def TcAnalPost(dtg,model,ropt=''):

    amodel=model
    #if(w2.IsModel2(model)): amodel=model[0:3]
    
    datprcdir=w2.PrcDirTcdatW2

    #
    # convert to wxmap adeck
    #
    imodel=atcf.ModelNametoAdeckName[amodel]
    cmd="%s/w2.tc.adeck.2.wxmap.adeck.py %s -i %s -o %s -s local"%(datprcdir,dtg,imodel,amodel)
    mf.runcmd(cmd,ropt)

    #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    # cycle by storm
    #

    stmids,stmopt=GetStmidsByDtg(dtg)
    for stmid in stmids:

        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # vecks + bias corr + 6/12 interp
        #

        jmodel=amodel+'j'
        kmodel=amodel+'k'
        p06model=amodel+'06'
        p12model=amodel+'12'
        
        cmd="%s/w2.tc.vdeck.py %s %s -B"%(datprcdir,stmid,amodel)
        mf.runcmd(cmd,ropt)

        #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
        # consensus to make j track = 06|12
        #
        cmd="%s/w2.tc.vdeck.con.adeck.py %s %s"%(datprcdir,stmid,jmodel)
        mf.runcmd(cmd,ropt)

        #kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
        # consensus to make k track = 06|12
        #
        cmd="%s/w2.tc.vdeck.con.adeck.py %s %s"%(datprcdir,stmid,kmodel)
        mf.runcmd(cmd,ropt)

        #dddddddddddddddddddddddddddddddddddddddd
        # delta qc - consistency anal
        #
        cmd="%s/w2.tc.vdeck.dqc.py %s %s"%(datprcdir,dtg,jmodel)
        mf.runcmd(cmd,ropt)
        cmd="%s/w2.tc.vdeck.dqc.py %s %s"%(datprcdir,dtg,kmodel)
        mf.runcmd(cmd,ropt)

        #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # make atcf adecks and put to moonfish
        #
        
        if(atcf.IsOpsAtcfAid(jmodel)):
            cmd="%s/w2.tc.vdeck.2.adeck.py %s %s"%(datprcdir,stmid,jmodel)
            mf.runcmd(cmd,ropt)

        if(atcf.IsOpsAtcfAid(p06model)):
            cmd="%s/w2.tc.vdeck.2.adeck.py %s %s"%(datprcdir,stmid,p06model)
            mf.runcmd(cmd,ropt)

        if(atcf.IsOpsAtcfAid(p12model)):
            cmd="%s/w2.tc.vdeck.2.adeck.py %s %s"%(datprcdir,stmid,p12model)
            mf.runcmd(cmd,ropt)

