import mf
import w2
import sys

def setsfcvars(fpath,grbpath,model,tau):

    sfcvars=[]
    #
    # sssssssssssssffffffffffffffffffcccccccccccc
    #
    if(model == 'ecm'):
        sfcvars=[
            ('pmsl','none',0,2,'b',-2),
            ('pxxm','none',0,61,'d',3),
            ('uwnd','none',0,33,'b',-4),
            ('vwnd','none',0,34,'b',-4)
            ]

    elif(model == 'cmc'):
        if(tau == 0):
            ctau='pxxm'
        else:
            ctau="p%dm"%(tau)
            
        sfcvars=[
            ('pmsl','none',0,2,'b',-2),
            ('%s'%(ctau),'none',0,61,'d',3),
            ('urel','pres',1000,33,'b',-4),
            ('vrel','pres',1000,34,'b',-4)
            ]

    elif(model == 'ukm'):
        if(tau == 0):
            ctau='pxxm'
        elif(tau < 60):
            ctau="p06m"
        elif(tau >= 60):
            ctau="p12m"

        sfcvars=[
            ('pmsl','none',0,2,'b',-2),
            ("%s"%(ctau),'none',0,62,'d',3),
            ('prxx','none',0,61,'d',3),
            ('urel','none',0,33,'b',-4),
            ('vrel','none',0,34,'b',-4)
            ]

    elif(model == 'ngp'):
        sfcvars=[
            ('pmsl','none',0,2,'b',-2),
            ('pxxm','none',0,61,'d',3),
            ('urel','hght',10,33,'b',-4),
            ('vrel','hght',10,34,'b',-4)
            ]

    elif(model == 'gfs'):
        sfcvars=[
            ('pmsl','none',0,2,'b',-2),
            ('pr06','none',0,61,'d',3),
            ('c06m','none',0,62,'d',3),
            ('urel','hght',10,33,'b',-4),
            ('vrel','hght',10,34,'b',-4)
            ]

    ngss=[]
    for sfcvar in sfcvars:
        print 'ngsget:ssss ',sfcvar
        ngs="""
gdfile=		%s
gdattim=	f%d
gbfile=		%s

gfunc=	        %s
gvcord=		%s
glevel=		%d
pdsval=		%d

precsn=		%s/%d
wmohdr=
cpyfil=         #3
proj= 
grdarea=
kxky=
run
"""%(fpath,tau,
     grbpath,
     sfcvar[0],sfcvar[1],sfcvar[2],sfcvar[3],
     sfcvar[4],sfcvar[5]
     )
        ngss.append(ngs)
        
    return(ngss)

ualevs=[1000,850,700,500,300,200]

#
# uuuuuuuuuuuuuuuuu aaaaaaaaaaaaaaaaaaaaa
#

def setuavar(fpath,grbpath,model,lev,tau):

    uavars=[]

    if(lev == 1000):

        uavars=[
            ('hght','pres',lev,7,'b',-1)
            ]

    elif(lev == 500):
        if(model == 'cmc'):
            uavars=[
                ('urel','pres',lev,33,'b',-4),
                ('vrel','pres',lev,34,'b',-4),
                ('hght','pres',lev,7,'b',-1),
                ('tmpk','pres',lev,11,'b',-3),
                ('relh','pres',lev,52,'b',-1),
                ]

        elif(model == 'ngp'):
            uavars=[
                ('urel','pres',lev,33,'b',-4),
                ('vrel','pres',lev,34,'b',-4),
                ('hght','pres',lev,7,'b',-1),
                ]

        else:
            uavars=[
                ('uwnd','pres',lev,33,'b',-4),
                ('vwnd','pres',lev,34,'b',-4),
                ('hght','pres',lev,7,'b',-1),
                ('tmpk','pres',lev,11,'b',-3),
                ('relh','pres',lev,52,'b',-1),
                ]

    elif(lev == 850 or lev == 700 or lev == 300 or lev == 200):
        if(model == 'cmc'):
            uavars=[
                ('urel','pres',lev,33,'b',-4),
                ('vrel','pres',lev,34,'b',-4),
                ('tmpk','pres',lev,11,'b',-3),
                ('relh','pres',lev,52,'b',-1),
                ]
        elif(model == 'ngp'):
            uavars=[
                ('urel','pres',lev,33,'b',-4),
                ('vrel','pres',lev,34,'b',-4),
                ]
        else:
            uavars=[
                ('uwnd','pres',lev,33,'b',-4),
                ('vwnd','pres',lev,34,'b',-4),
                ('tmpk','pres',lev,11,'b',-3),
                ('relh','pres',lev,52,'b',-1),
                ]

        if(model != 'ngp'):
            if(lev == 850 or lev == 200):
                uavars.append(('tmpk','pres',lev,11,'b',-3))

        if(lev == 200):
            uavars.append(('hght','pres',lev,7,'b',-1))


    ngss=[]
    for u in uavars:
        
        print 'ngsget:uuuu ',u
        ngs="""
gdfile=		%s
gdattim=	f%d
gbfile=		%s

gfunc=	        %s
gvcord=		%s
glevel=		%d
pdsval=		%d

precsn=         %s/%d
wmohdr=
cpyfil=         #3
proj= 
grdarea=
kxky=
run
"""%(fpath,tau,
     grbpath,
     u[0],u[1],u[2],u[3],
     u[4],u[5]
     )
        ngss.append(ngs)


    return(ngss)
    
def NawipsModelDir(model,dtg,center=w2.W2Center.lower()):

    verb=0
    icodes=[]

    yyyy=dtg[0:4]
    hh=dtg[8:10]
    cdirat=None
    
    if(center == 'nhc'):
        
        if(model == 'ecm'):
            cdir="%s/ecmwf_hr"%(w2.NhcNawipsGridLocalDir)
            cdira="%s/%s/daily/model/ecmwf_hr"%(w2.NhcNawipsGridArchDir,yyyy)
            cdirat="%s/%s/july/model/ecmwf_hr"%(w2.NhcNawipsGridArchTmpDir,yyyy)
            fmask='ecmwf_hr_'
            
        elif(model == 'ukm'):
            if(hh == '06' or hh == '18'):
                cdir="%s/ukmet_hri"%(w2.NhcNawipsGridLocalDir)
                cdira="%s/%s/daily/model/ukmet_hri"%(w2.NhcNawipsGridArchDir,yyyy)
            else:
                cdir="%s/ukmet_hr"%(w2.NhcNawipsGridLocalDir)
                cdira="%s/%s/daily/model/ukmet_hr"%(w2.NhcNawipsGridArchDir,yyyy)
                cdirat="%s/%s/july/model/ukmet_hr"%(w2.NhcNawipsGridArchTmpDir,yyyy)
            fmask='ukmet_'
            
        elif(model == 'gfs'):
            cdir="%s/gfs"%(w2.NhcNawipsGridLocalDir)
            cdira="%s/%s/daily/model/gfs"%(w2.NhcNawipsGridArchDir,yyyy)
            cdirat="%s/%s/july/model/gfs"%(w2.NhcNawipsGridArchTmpDir,yyyy)
            fmask='gfs_'
            
        elif(model == 'cmc'):
            cdir="%s/cmc"%(w2.NhcNawipsGridLocalDir)
            cdira="%s/%s/daily/model/cmc"%(w2.NhcNawipsGridArchDir,yyyy)
            cdirat="%s/%s/july/model/cmc"%(w2.NhcNawipsGridArchTmpDir,yyyy)
            fmask='cmc_'
            
        elif(model == 'ngp'):
            cdir="%s/nogaps"%(w2.NhcNawipsGridLocalDir)
            cdira="%s/%s/daily/model/nogaps"%(w2.NhcNawipsGridArchDir,yyyy)
            cdirat="%s/%s/july/model/nogaps"%(w2.NhcNawipsGridArchTmpDir,yyyy)
            fmask='nogaps_'
            
        else:
            if(verb): print 'EEEE invalid model: ',model,' for center: ',center,' sayoonara, o genki de!'
            return(None,None,None,None)


    else:
        print 'EEEE invalid center: ',center,' sayoonara, o genki de!'
        sys.exit()

    return(cdir,cdira,cdirat,fmask)

def NawipsNwpCtlFile(model,dtg,ctlfile,grbfile,gmpfile,dogribmap=1):

    bdir=w2.NwpDataBdir(model)
    gtime=mf.dtg2gtime(dtg)
    
    if(model == 'gfs' or model == 'ngp'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title nawips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 3
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef  6 levels
1000 850 700 500 300 200
tdef  13 linear %s 12hr
vars  10
prm     0 62,1,0     ** misc precipitation [kg/m^2]
pr      0 61,1,0     ** Total precipitation [kg/m^2]
psl     0  2,1,0     ** Pressure reduced to MSL [Pa]
uas     0 33,103,10  ** u wind [m/s]
vas     0 34,103,10  ** v wind [m/s]
zg      6  7,100,0   ** Geopotential height [gpm]
hur     6 52,100,0   ** Relative humidity [%%]
ta      6 11,100,0   ** Temp. [K]
ua      6 33,100,0   ** u wind [m/s]
va      6 34,100,0   ** v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'cmc'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title nawips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 3
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef  6 levels
1000 850 700 500 300 200
tdef  13 linear %s 12hr
vars  9
pr      0 61,1,0     ** Total precipitation [kg/m^2]
psl     0  2,1,0     ** Pressure reduced to MSL [Pa]
uas     0 33,100,1000  ** u wind [m/s]
vas     0 34,100,1000  ** v wind [m/s]
zg      6  7,100,0   ** Geopotential height [gpm]
hur     6 52,100,0   ** Relative humidity [%%]
ta      6 11,100,0   ** Temp. [K]
ua      6 33,100,0   ** u wind [m/s]
va      6 34,100,0   ** v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'ecm' or model == 'ukm'):

        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title nawips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 3
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef  6 levels
1000 850 700 500 300 200
tdef  13 linear %s 12hr
vars  10
prm     0 62,1,0     ** misc precipitation [kg/m^2]
pr      0 61,1,0     ** Total precipitation [kg/m^2]
psl     0  2,1,0     ** Pressure reduced to MSL [Pa]
uas     0 33,1,0     ** u wind [m/s]
vas     0 34,1,0     ** v wind [m/s]
zg      6  7,100,0   ** Geopotential height [gpm]
hur     6 52,100,0   ** Relative humidity [%%]
ta      6 11,100,0   ** Temp. [K]
ua      6 33,100,0   ** u wind [m/s]
va      6 34,100,0   ** v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)


    elif(model == 'ngp'):

        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
ydef 181 linear -90.0 1.0
xdef 360 linear   0.0 1.0
zdef  6 levels
1000 850 700 500 300 200
tdef  13 linear %s 12hr
vars  10
psl    0   1,102,0   Pressure [Pa]
pr     0  61,1  ,0   Total precipitation [kg/m^2]
tas    0  11,105,2   Temp. [K]
uas    0  33,105,10  u wind [m/s]
vas    0  34,105,10  v wind [m/s]
zg     6   7,100,0   Geopotential height [gpm]
hur    6  52,100,0   Relative humidity [%%]
ta     6  11,100,0   Temp. [K]
ua     6  33,100,0   u wind [m/s]
va     6  34,100,0   v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    print ctl
    ctlpath="%s/%s"%(bdir,ctlfile)
    mf.WriteCtl(ctl,ctlpath)

    ropt=''
    if(dogribmap):
        cmd="gribmap -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)
    
    return(ctlpath)


def NawipsModelTaus(model,dtg,center=w2.W2Center.lower()):

    
    chktaus48_06=[0,12,24,48]
    dattaus48_06=[0,6,12,18,24,48]

    chktaus120_06=[0,12,24,48,60,72,84,96,108,120]
    dattaus120_06=[0,6,12,18,24,36,48,60,72,84,96,108,120]
    
    chktaus144_12=[0,12,24,36,48,60,72,84,96,108,120,132,144]
    dattaus144_12=[0,12,24,36,48,60,72,84,96,108,120,132,144]
    
    chktaus144_06=[0,6,12,18,24,36,48,60,72,84,96,108,120,132,144]
    dattaus144_06=[0,6,12,18,24,36,48,60,72,84,96,108,120,132,144]
    

    if(model == 'gfs'):
        chktaus=chktaus144_06
        dattaus=dattaus144_06

    elif(model == 'ngp'):
        chktaus=chktaus144_06
        dattaus=dattaus144_06

    elif(model == 'ecm'):
        chktaus=chktaus144_12
        dattaus=dattaus144_12

    elif(model == 'ukm'):
        
        if(dtg[8:10] == '06' or dtg[8:10] == '18'):
            chktaus=chktaus48_06
            dattaus=dattaus48_06

        else:
            chktaus=chktaus144_06
            dattaus=dattaus144_06
            

    elif(model == 'cmc'):
        chktaus=chktaus120_06
        dattaus=dattaus120_06

        
    return(dattaus,chktaus)

#
# pull grid, var, etc.  info from na file info
#

def ParseNls(lfile,verb=0):

    nls=open(lfile).readlines()

    dfile=proj=pangles=ni=nj=rlatmin=rlonmin=rlatmax=rlonmax=None
    nfields=None
    
    dtgs=[]
    taus=[]
    vars=[]
    levels=[]
    levtypes=[]

    AllVars={}
        
    
    n=0
    for nl in nls:
        card=nls[n]
        if(n<50):
            print 'cccc ',n,card[:-1]
            
        if(n == 1):
            dfile=card.split()[2]

        if(n == 4):
            proj==card.split()[1]

        if(n == 5):
            tt=card.split()
            pangles=[float(tt[1]),float(tt[2]),float(tt[3])]

        if(n == 6):
            tt=card.split()
            ni=tt[2]
            nj=tt[3]

        if(n == 7):
            tt=card.split()
            rlatmin=float(tt[2])
            rlonmin=float(tt[3])

        if(n == 8):
            tt=card.split()
            rlatmax=float(tt[2])
            rlonmax=float(tt[3])

        if(n == 19):
            tt=card.split()
            nfields=tt[5]


        if(n >= 24):
            tt=card.split()
            nf=int(card[1:5])
            yymmdd=card[10:16]
            hh=card[17:19]
            mm=card[19:21]

            dtg=yymmdd+hh
            tau=card[22:25].strip()
            itau=int(tau)
            levl1=card[46:52].strip()
            levl2=card[53:58].strip()
            vcord=card[58:65].strip()
            var=card[66:74].strip()
            if(verb):
                print "CC:%s:CC"%(card[:-1])
                print 'nf         ',nf
                print 'yymmdd     ',yymmdd
                print 'hh,mm      ',hh,mm
                print 'tau        ',tau
                print 'levl1      ',levl1
                print 'levl2      ',levl2
                print 'vcord      ',vcord
                print 'var        ',var

            vars.append(var)
            dtgs.append(dtg)
            taus.append(itau)
            levels.append(levl1)
            levtypes.append(vcord)
                

#    1     060826/0000F000                         10         HGHT UREL        :CC
#    1     060826/0000F000                         10         HGHT UREL
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#          10        20        30        40        50        60        70


            


            

        n=n+1

        AllVars[var,itau,level]=[var,dtg,itau,levl1,levl2,vcord]

    taus=mf.uniq(taus)
    dtgs=mf.uniq(dtgs)
    vars=mf.uniq(vars)
    levels=mf.uniq(levels)
    levtypes=mf.uniq(levtypes)

    for tau in taus:
        print 'tau      ',tau

    for level in levels:
        print 'level    ',level

    for levtype in levtypes:
        print 'levtype  ',levtype

    for var in vars:
        print 'var      ',var

    rc=(dfile,proj,pangles,
        ni,nj,
        rlatmin,rlonmin,
        rlatmax,rlonmax,
        nfields)

    return(rc)
            


