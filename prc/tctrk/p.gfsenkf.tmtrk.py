#!/usr/bin/env python

import GA
import WxMAP2 as W2

from FM import FimRunModel2
from M import *
from tcbase import AdeckBaseDir
from TCtrk import TmTrk
import FM
from GRIB import Grib1

MF=MFutils()

class Qsub(MFbase):

    def __init__(self,
                 argv=None,
                 project='fim',
                 vmem='2.0G',
                 queue='nserial',
                 qname='tctrk',
                 runcmd='/lfs1/projects/fim/fiorino/w21/run.cron.tcsh',
                 pydir='/lfs1/projects/fim/fiorino/w21/prc/tctrk',
                 doqsub=0,
                 ropt='',
                 min4dtg=50,
                 verb=0,
                 ):


        self.min4dtg=min4dtg
        
        (dir,pycmd)=os.path.split(argv[0])

        dtgopt=argv[1]
        dtgs=mf.dtg_dtgopt_prc(dtgopt)

        ndtgs=len(dtgs)

        totmin=self.min4dtg*ndtgs
        nmin=totmin%60
        nhour=totmin/60
        rttime="%02d:%02d:00"%(nhour,nmin)

        if(ndtgs == 1):
            dtg=dtgs[0]
            pyopt=dtg
            nargstart=2
        else:
            pyopt=dtgopt
            nargstart=2
            
        for arg in argv[nargstart:]:
            if(arg != '-Q' and arg != '-V' and arg != '-N'):
                arg=arg.strip()
                pyopt="%s %s"%(pyopt,arg)
            elif(arg == '-N'):
                ropt='norun'


        qsubsh='''
#!/bin/sh
#$ -S /bin/sh
#$ -N %s_%s
#$ -A %s 
#$ -l h_rt=%s,h_vmem=2.0G
#$ -o %s/wjet_%s_%s.log
#$ -cwd
#$ -pe %s 1
#$ -j y

# Set up paths to unix commands

RM=/bin/rm
CP=/bin/cp
MV=/bin/mv
LN=/bin/ln
MKDIR=/bin/mkdir
CAT=/bin/cat
ECHO=/bin/echo
CUT=/bin/cut
WC=/usr/bin/wc
DATE=/bin/date
AWK="/bin/awk --posix"
SED=/bin/sed
TAIL=/usr/bin/tail

# Executable script and path
RUNCMD="%s"
PYDIR="%s"
PYCMD="%s"

# Set CWD to script location and execute redirecting stdout/stderr
cd $PYDIR
$RM -f %s_%s_out.txt
$RUNCMD "$PYDIR/$PYCMD %s" > %s_%s_out.txt 2>&1

# Check for exit status of script
#error=$?
#if [ ${error} -ne 0 ]; then
#  ${ECHO} "ERROR: ${PYCMD} crashed  Exit status=${error}"
#  exit ${error}
#fi

# Sucessful exit
exit 0
'''%(qname,pyopt[0:1],project,rttime,pydir,qname,pyopt[0:1],
     queue,
     runcmd,pydir,pycmd,qname,pyopt[0:1],pyopt,qname,pyopt[0:1])

        pytag='test'

        if(doqsub and ropt != 'norun'):
            qpath="%s/p.qsub.%s.sh"%(pydir,pytag)
            rc=MF.WriteString2File(qsubsh,qpath)

            if(verb):
                print '  qpath: ',qpath
                print ' qsubsh: ',qsubsh

            cmd="qsub %s"%(qpath)
            MF.runcmd(cmd,ropt)
            

        else:

            print qsubsh




            
        
class GfsEnkf(MFbase,Grib1):

    def __init__(self,
                 override=0,
                 ropt=''):

        self.override=override
        self.ropt=ropt

        self.initBaseVars()
        self.initVars()

        
    def initBaseVars(self):
        

        self.bddir="/lfs1/projects/fim/whitaker/gfsenkf_t254"
        self.model='gfsenkf'
        self.dmodel='gfsenkf_t254'
        self.omodel='gfsenkf'
        self.dmaskformat="pgrbfg_%s_fhr*_mem%03d"
        self.dsetmaskformat="pgrbfg_%s_fhr%%f2_mem%03d"
        self.atcf2id='GK'
        self.qname='tctrk'

        self.dtau=6
        self.maxtau=168

        self.nb=1
        self.ne=21
        self.ni=1
        


    def setDmask(self,dtg,member):
        self.dmaskbase=self.dmaskformat%(dtg,member)
        self.dsetmaskbase=self.dsetmaskformat%(dtg,member)


    def setQname(self,dtgopt=None):

        name=self.qname
        if(dtgopt != None):
            qname="%s_%s"%(name,dtgopt)
        else:
            qname="%s_%s"%(name,dtgopt)
            
        return(qname)

    def setDdir(self):
        self.ddir="%s/%s/ens20"%(self.bddir,dtg)

        

    def setDtgMember(self,dtg,member):
        
        self.dtg=dtg
        self.member=member
        self.gtime=mf.dtg2gtime(dtg)

        self.setDdir()
        
        self.cdir="%s/%s"%(self.bcdir,dtg)
        MF.ChkDir(self.cdir,'mk')
        self.cdirtctrk="%s/%s/tctrk"%(self.bcdir,dtg)
        MF.ChkDir(self.cdirtctrk,'mk')

        self.setDmask(dtg,member)
            
        self.dmask="%s/%s"%(self.ddir,self.dmaskbase)
        self.dset="dset %s/%s"%(self.ddir,self.dsetmaskbase)

        self.dmask1="%s/%s.grib1"%(self.cdirtctrk,self.dmaskbase)
        self.dset1="dset %s/%s.grib1"%(self.cdirtctrk,self.dsetmaskbase)
        
        self.dmask2="%s/%s.grib2"%(self.ddir,self.dmaskbase)
        self.dset2="dset %s/%s.grib2"%(self.cdirtctrk,self.dsetmaskbase)
        
        self.cfile=self.cmaskformat%(dtg,member)
        self.gfile=self.gmaskformat%(dtg,member)

        self.cfile1=self.cmaskformat1%(dtg,member)
        self.gfile1=self.gmaskformat1%(dtg,member)

        self.cfile2=self.cmaskformat2%(dtg,member)
        self.gfile2=self.gmaskformat2%(dtg,member)

        self.mask1="*.grib1"
        self.mask2="*.grib2"

        self.tdir=GE.cdirtctrk
        self.tdirAdeck="%s/adeck/esrl/%s/%s/%s"%(W2.TcDataBdir,dtg[0:4],GE.omodel,self.dtg)
        MF.ChkDir(self.tdirAdeck,'mk')

        self.tDir="/lfs1/projects/fim/fiorino/w21/dat/nwp2/w2flds/dat/%s/%s"%(self.dmodel,self.dtg)
        MF.ChkDir(self.tDir,'mk')

    def initVars(self):

        self.bcdir="%s/ncep/%s"%(W2.Nwp2DataBdir,self.dmodel)

        self.cmaskformat="%s.%%s.mem%%03d.ctl"%(self.model)
        self.gmaskformat="%s.%%s.mem%%03d.gmp1"%(self.model)
        
        self.cmaskformat1="%s.%%s.mem%%03d.grib1.ctl"%(self.model)
        self.gmaskformat1="%s.%%s.mem%%03d.grib1.gmp1"%(self.model)
        
        self.cmaskformat2="%s.%%s.mem%%03d.grib2.ctl"%(self.model)
        self.gmaskformat2="%s.%%s.mem%%03d.grib2.gmp2"%(self.model)
        
        self.ntau=self.maxtau/self.dtau+1
        self.taus=range(0,self.maxtau+1,self.dtau)
        self.dtau='%dhr'%(self.dtau)

        

    def cleanData(self):

        cmd="rm %s/*"%(self.cdir)
        mf.runcmd(cmd,ropt)

        cmd="rm %s/*"%(self.cdirtctrk)
        mf.runcmd(cmd,ropt)



    def defineCtl(self):

        self.ctl="""%s
index ^%s
undef 9.999E+20
title pgrbfg_2010061700_fhr72_mem001
*  produced by grib2ctl v0.9.12.5p16
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 8   levels 1000 850 700 500 400 300 250 200
tdef %2d  linear %s %s
vars 11
prc     0 63,   1,0     ** Convective precipitation [kg/m^2]
pr      0 61,   1,0     ** Total precipitation [kg/m^2]
psl     0  2, 102,0     ** Pressure reduced to MSL [Pa]
prw     0 54, 200,0     ** Precipitable water [kg/m^2]
tas     0 11, 105,2     ** Temp. [K]
uas     0 33, 105,10    ** u wind [m/s]
vas     0 34, 105,10    ** v wind [m/s]
zg      8  7, 100,0     ** Geopotential height [gpm]
ta      8 11, 100,0     ** Temp. [K]
ua      8 33, 100,0     ** u wind [m/s]
va      8 34, 100,0     ** v wind [m/s]
endvars"""%(self.dset,self.gfile,self.ntau,self.gtime,self.dtau)

        self.ctl1="""%s
index ^%s
undef 9.999E+20
title pgrbfg_2010061700_fhr72_mem001
*  produced by grib2ctl v0.9.12.5p16
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 8   levels 1000 850 700 500 400 300 250 200
tdef %s  linear %s %s
vars 11
prc     0 63,   1,0     ** Convective precipitation [kg/m^2]
pr      0 61,   1,0     ** Total precipitation [kg/m^2]
uas     0 33, 105,10    ** u wind [m/s]
vas     0 34, 105,10    ** v wind [m/s]
tas     0 11, 105,2     ** Temp. [K]
psl     0  2, 102,0     ** Pressure reduced to MSL [Pa]
prw     0 54, 200,0     ** Precipitable water [kg/m^2]
zg      8  7, 100,0     ** Geopotential height [gpm]
ta      8 11, 100,0     ** Temp. [K]
ua      8 33, 100,0     ** u wind [m/s]
va      8 34, 100,0     ** v wind [m/s]
endvars"""%(self.dset1,self.gfile1,self.ntau,self.gtime,self.dtau)


        self.ctl2="""%s
index ^%s
undef 9.999E+20
title pgrbfg_2010061700_fhr72_mem001
dtype grib2
options pascals template
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
* PROFILE Pa
zdef 7 levels 100000 85000 70000 50000 40000 30000 20000
tdef %s  linear %s %s
vars 11
prc    0,1,0   0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr     0,1,0    0,1,8,1 ** surface Total Precipitation [kg/m^2]
zg     7,100      0,3,5 ** (1000 850 700 500 200) Geopotential Height [gpm]
psl    0,101,0    0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
prw    0,200,0    0,1,3 ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
ta     7,100      0,0,0 ** 850 mb Temperature [K]
tas    0,103,2    0,0,0 ** 2 m above ground Temperature [K]
ua     7,100      0,2,2 ** (850 700 500 250 200) U-Component of Wind [m/s]
uas    0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
va     7,100      0,2,3 ** (850 700 500 250 200) V-Component of Wind [m/s]
vas    0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
endvars
edef 1
e1 %s  %s 3,%d
endedef"""%(self.dset2,self.gfile2,self.ntau,self.gtime,self.dtau,
            self.ntau,self.gtime,self.member)


        
    def setCtl(self):


        cpath="%s/%s"%(self.cdir,self.cfile)
        gpath="%s/%s"%(self.cdir,self.gfile)

        cpath1="%s/%s"%(self.cdir,self.cfile1)
        gpath1="%s/%s"%(self.cdir,self.gfile1)

        cpath2="%s/%s"%(self.cdir,self.cfile2)
        gpath2="%s/%s"%(self.cdir,self.gfile2)


        self.cpath=cpath
        self.gpath=gpath

        self.cpath1=cpath1
        self.gpath1=gpath1
        
        self.cpath2=cpath2
        self.gpath2=gpath2


        # -- check if already processed...if the .gmp there
        #

        if(self.override == 0):
        
            if(MF.GetPathSiz(gpath1,verb=0) > 0):
                print 'WWW gpath1: ',gpath1,' there; already processed...set override=1 to reprocess...'
                return(0)

            if(MF.GetPathSiz(gpath,verb=0) > 0):
                print 'WWW  gpath: ',gpath,' there; already processed...set override=1 to reprocess...'
                return(0)



        # -- get file sizes
        #
        dfiles=glob.glob(self.dmask)
        dfiles2=glob.glob(self.dmask2)


        # ---------------- real work
        #
        if(len(dfiles2) > 0):

            cmd="cp %s %s/."%(self.dmask2,self.cdirtctrk)
            mf.runcmd(cmd,ropt)

            dfiles2=glob.glob("%s/%s"%(self.cdirtctrk,self.mask2))
            dfiles1=glob.glob("%s/%s"%(self.cdirtctrk,self.mask1))

            dogrib2to1=0
            
            if( (len(dfiles1) == 0 or self.override) and dogrib2to1 ):

                for dfile2 in dfiles2:
                    if(self.member == 0):
                        opath1=dfile2.replace('pgb2','pgb')
                    else:
                        (dir,file)=os.path.split(dfile2)
                        (base,ext)=os.path.splitext(file)
                        opath1="%s/%s.grib1"%(dir,base)

                    cmd="cnvgrib -g21 %s %s"%(dfile2,opath1)
                    mf.runcmd(cmd,ropt)


        dfiles1=glob.glob(self.dmask1)
        dfiles2=glob.glob(self.dmask2)

        self.defineCtl()
        
        # -- bail point -- setup the ctl
        #
        #if(len(dfiles) == 0 and len(dfiles2) == 0 ):   return

        print 'DDDDDDDDDDDDDDDDDDDDDDDD ',len(dfiles),cpath,MF.GetPathSiz(gpath),gpath
    
        if(len(dfiles) > 0 and (MF.GetPathSiz(gpath) == None or MF.GetPathSiz(gpath) == 0) ):
            
            MF.WriteString2File(self.ctl,cpath)
            # -- bad grib for gfsenkf 2008 (-8) options
            cmd="gribmap -s1000000 -v -i %s"%(cpath)
            cmd="gribmap -s1000000 -i %s"%(cpath)
            #rc=os.popen(cmd).readlines()
            #rc=mf.runcmd(cmd,logpath='quiet')
            rc=mf.runcmd(cmd)
            # -- check if problem in gribmap
            #
            if(mf.find(str(rc),'GRIB file format error')):
                print 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
                print 'gribmap error for dtg: ',self.dtg,' member: ',self.member
                return(-1)
            else:
                None
                #for r in rc:
                #    print r[:-1]


        if(len(dfiles1) > 0 and self.ctl1 != None):
            MF.WriteString2File(self.ctl1,cpath1)
            cmd="gribmap -v -i %s"%(cpath1)
            mf.runcmd(cmd,ropt)
            gribver=1

        if(len(dfiles2) > 0 and self.ctl2 != None):
            MF.WriteString2File(self.ctl2,cpath2)
            cmd="gribmap -v -i %s"%(cpath2)
            mf.runcmd(cmd,ropt)
            self.cpath=cpath2
            gribver=2
        
        if(MF.GetPathSiz(gpath1,verb=0) > 0 and len(dfiles1) > 0):
            self.cpath=cpath1
            gribver=-1

        #if(gribver == 2):
        #    print 'EEE suppose to do grib2 -> grib1, but this failed...'
        #    sys.exit()


    def lsData(self,verb=0):

        dfiles=glob.glob(self.dmask)

        if(verb):
            print 'ddddd ',self.ddir
            print '00000 ',self.dmask
            
        l0=len(dfiles)
        
        if(l0 > 0):
            taus=self.getTaus0(dfiles)
            print 'YYYYYYDDDD---- last tau: ',taus[-1],dfiles[-1]

        if(l0 == 0):
            print 'NNNNNNDDDD----',self.dtg,self.dmask


        dfiles=glob.glob("%s/tcgen.atcf.lant.*.txt"%(self.tdirAdeck))
        dfiles.sort()

        l0=len(dfiles)
        
        if(l0 > 0):
            print 'YYYYYYAAAA----: ',dfiles[-1]

        if(l0 == 0):
            print 'NNNNNNAAAA----',self.dtg


        mask="%s/*.grb1"%(self.tDir)
        dfiles=glob.glob(mask)
        dfiles.sort()

        l0=len(dfiles)
        
        if(l0 > 0):
            print 'YYYYYY2222----: ',dfiles[-1]

        if(l0 == 0):
            print 'NNNNNN2222----',self.dtg,mask

        print



    def getTaus0(self,files):

        taus=[]
        for file in files:
            (dir,file)=os.path.split(file)
            tau=self.getTau0(file)
            taus.append(tau)

        taus.sort()
        return(taus)

    def getTaus2(self,files):

        taus=[]
        for file in files:
            (dir,file)=os.path.split(file)
            tau=self.getTau2(file)
            taus.append(tau)

        taus.sort()
        return(taus)
    

    def getTau0(self,file):
        tt=file.split('_')
        ctau=tt[2]
        tau=int(ctau[3:])
        return(tau)

        
    def getTau2(self,file):
        tt=file.split('_')
        ctau=tt[2]
        tau=int(ctau[3:])
        return(tau)


    # -- grib1 filter methods
    #
    def setFieldRequest1(self,ftype='std',etau=168):
        
        uvplevs=[925,850,200]
        zplevs=[850,500]
        tplevs=[]
        rhplevs=[]
        

        sfcvars={}
        uavars={}

        uarequest={}

        uarequest['ugrd']=[]
        uarequest['vgrd']=[]
        uarequest['hgt']=[]
        uarequest['tmp']=[]
        uarequest['rh']=[]
        
        
        for plev in uvplevs:
            uarequest['ugrd']=uarequest['ugrd']+ ['100.%d'%(plev)]
            uarequest['vgrd']=uarequest['vgrd']+ ['100.%d'%(plev)]
        
        for plev in zplevs:
            uarequest['hgt']=uarequest['hgt']+ ['100.%d'%(plev)]

        for plev in tplevs:
            uarequest['tmp']=uarequest['tmp']+ ['100.%d'%(plev)]

        if(len(rhplevs) > 0):
            for plev in rhplevs:
                uarequest['rh']=uarequest['rh']+ ['100.%d'%(plev)]


        sfcvars['uas']=['ugrd','105.10']
        sfcvars['vas']=['vgrd','105.10']
        sfcvars['psl']=['prmsl','102.0'] 
        sfcvars['pr'] =['apcp','1.0']
        sfcvars['prc']=['acpcp','1.0']
        sfcvars['prw']=['pwat','200.0']

        uavars['ua']  = ['ugrd', uarequest['ugrd'] ]
        uavars['va']  = ['vgrd', uarequest['vgrd'] ]
        uavars['zg']  = ['hgt',  uarequest['hgt']  ]
        uavars['hur'] = ['rh',   uarequest['rh']   ]
        uavars['ta']  = ['tmp',  uarequest['tmp']  ]

        btau=0
        dtau=6
        ttaus=range(btau,etau+1,dtau)

        self.sfcvars=sfcvars
        self.uavars=uavars
        self.ttaus=ttaus
        self.ftype=ftype


    def GetTauGrib1File(self,file):
        tt=file.split('_')
        tau=tt[2][-3:]
        tau=int(tau)
        return(tau)


    def I2Osfcvar(self,ivar,ilevcode,unitscode=None):
        ovar=ivar
        for s in self.sfcvars.keys():

            ilevchk=ilevcode.replace(',','.')
            vcomp=(ivar == self.sfcvars[s][0])
            lcomp=(ilevchk == self.sfcvars[s][1])
            ucomp=1
            if(vcomp and lcomp and ucomp):
                return(s)
        return(ovar)


    def I2Ouavar(self,ivar):
        ovar=ivar
        for u in self.uavars.keys():
            if(ivar == self.uavars[u][0]):
                return(u)
        return(ovar)


    def SetFieldRequest(self,sfcvars,uavars,tau):

        request={}
        sfckeys=sfcvars.keys()
        for sfckey in sfckeys:
            tt=sfcvars[sfckey]
            rvar=tt[0]
            rlev=tt[1]
            try:
                runits=tt[2]
            except:
                runits=None

            try:
                request[rvar].append(rlev)
            except:
                request[rvar]=[]
                request[rvar].append(rlev)

            request[rvar,'units']=runits


        uakeys=uavars.keys()

        for uakey in uakeys:
            tt=uavars[uakey]
            rvar=tt[0]
            rlevs=tt[1]

            try:
                runits=tt[2]
            except:
                runits=None
            request[rvar,'units']=runits
            
            for rlev in rlevs:
                try:
                    request[rvar].append(rlev)
                except:
                    request[rvar]=[]
                    request[rvar].append(rlev)


        request['taus']=[tau]

        return(request)

    def setPathsGrib1(self):

        self.gribtype='grb1'
        self.gmask="%s/%s/ens20/%s"%(self.bddir,self.dtg,self.dmaskbase)

        self.tbase="gfsenkf_m%03d"%(self.member)
        self.tdatbase="%s/%s"%(self.tDir,self.tbase)
        
        self.xwgrib='wgrib'
        self.xgribmap='gribmap'

        self.ctlpath="%s.%s.ctl"%(self.tdatbase,self.gribtype)
        self.gmppath="%s.%s.gmp"%(self.tdatbase,self.gribtype)
        self.gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)
        
        
        self.tpathmask="%s.f???.%s"%(self.tdatbase,self.gribtype)


    def filtGrib1(self,override=0,verb=0,
                  fdb1override=0,
                  alwaysDoCtl=0):
        """
        """

        self.setPathsGrib1()
        self.setFieldRequest1()
        
        
        if(override): fdb1override=1
        self.MakeFdb1(override=fdb1override)
        self.reqtaus=self.taus

        gribs=glob.glob(self.tpathmask)
        gribs.sort()


        self.fldrequest={}
        self.ioktaus={}
        self.iokreqtaus={}
        for tau in self.reqtaus:
            self.iokreqtaus[tau]=0

        self.tdatstatus={}

        shortDone=0
        for ttau in self.ttaus:

            try:
                ipath=self.sdatpaths[ttau]
                opath=self.tdatpaths[ttau]
                self.ioktaus[ttau]=1
                filethere=1
            except:
                filethere=0
                opath="%s.f%%f3.%s"%(self.tbase,self.gribtype)
                self.tdatpaths[ttau]=opath
                self.ioktaus[ttau]=0

            request=self.SetFieldRequest(self.sfcvars,self.uavars,ttau)

            self.fldrequest[ttau]=request

            try:
                nf=self.tdatstatus[ttau][1]
            except:
                nf=0

            didwgribfilt=0
            if( (filethere and not(os.path.exists(opath))) or override >= 1):

                if(self.gribtype == 'grb1'):
                    (records,recsiz,nrectot)=self.ParseFdb1(ttau=ttau)
                    orecs=self.Wgrib1VarFilter(records,request,verb=verb)

                if(len(orecs) > 0):
                    if(self.gribtype == 'grb1'): self.Wgrib1Filter(orecs,ipath,opath)
                    self.ioktaus[ttau]=1
                else:
                    self.ioktaus[ttau]=0
                
                didwgribfilt=1


        #self.MakeCtl(verb=verb,override=override)

        # check if the .ctl and .gmp are there...and all the requested taus...or fixed short taus...
        #

        if(didwgribfilt or override >= 1) :
            self.MakeCtl(verb=verb,override=override)

        else:
            for ttau in self.ttaus:
                if(self.ioktaus[ttau] == 0):
                    print "III need tau: %d for %s"%(ttau,self.dtg)



            
# -- 2010 irwd xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#

class GfsEnkfIrwd(GfsEnkf):

    def initBaseVars(self):
        
        self.model='gfsenkf'
        self.dmodel='gfsenkf_irwd'
        self.omodel='gfsenkf_irwd'
        self.bddir="/lfs1/projects/fim/ppegion/gfsenkf/t254/cira_winds/fcst"
        self.dmaskformat="pgrbf_%s_f*_mem%03d.grb"
        self.dsetmaskformat="pgrbf_%s_f%%f2_mem%03d.grb"
        self.atcf2id='GI'
        self.qname='tctrk'

        self.dtau=6
        self.maxtau=168

    def setDmask(self,dtg,member):
        self.dmaskbase=self.dmaskformat%(dtg,member)
        self.dsetmaskbase=self.dsetmaskformat%(dtg,member)


    def setDdir(self):
        self.ddir="%s/%s"%(self.bddir,dtg)


    def getTau0(self,file):
        tt=file.split('_')
        ctau=tt[2]
        tau=int(ctau[1:])
        return(tau)
    
    def getTau2(self,file):
        tt=file.split('_')
        ctau=tt[2]
        tau=int(ctau[1:])
        return(tau)
        



# -- 2008 reruns xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#

class GfsEnkf2008(GfsEnkf):

    def initBaseVars(self):
        
        self.model='gfsenkf'
        self.dmodel='gfsenkf_t254'
        self.omodel='gfsenkf'
        self.bddir="/lfs1/projects/fim/whitaker/tracks/gfsenkf_200907"
        
        #pgrb_2008071500_fhr120_mem021

        self.dmaskformat="pgrb_%s_fhr*_mem%03d"
        self.dsetmaskformat="pgrb_%s_fhr%%f3_mem%03d"
        self.atcf2id='GK'
        self.qname='tctrk'

        self.dtau=6
        self.maxtau=168

    def setDmask(self,dtg,member):
        self.dmaskbase=self.dmaskformat%(dtg,member)
        self.dsetmaskbase=self.dsetmaskformat%(dtg,member)



# -- 2010 irwd  control xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#

class GfsEnkfIrwdX(GfsEnkf):

    bddir="/lfs1/projects/fim/whitaker/gfsenkf_t254x"
    bddir="/lfs1/projects/fim/fiorino/gfsenkf_t254x"
    
    def initBaseVars(self):
        
        self.model='gfsenkf_irwdx'
        self.dmodel='gfsenkf_t254x'
        self.omodel='gfsenkf_irwdx'
        self.dmaskformat="pgrbfg_%s_fhr*_mem%03d"
        self.dsetmaskformat="pgrbfg_%s_fhr%%f2_mem%03d"
        self.atcf2id='GX'
        self.qname='tctrk'

        self.dtau=12
        self.maxtau=120

    def setDmask(self,dtg,member):
        self.dmaskbase=self.dmaskformat%(dtg,member)
        self.dsetmaskbase=self.dsetmaskformat%(dtg,member)



# -- 2011 hfip demo irwd  control xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#

class GfsEnkf2011(GfsEnkf):

    bddir="/lfs1/projects/gfsenkf/gfsenkf_t574"
    
    def initBaseVars(self):
        
        self.model='gfsenkf'
        self.dmodel='gfsenkf_t254'
        self.omodel='gfsenkf'
        self.dmaskformat="pgrbfg_%s_fhr*_mem%03d"
        self.dsetmaskformat="pgrbfg_%s_fhr%%f3_mem%03d"
        self.atcf2id='GE'
        self.qname='tctrk'
        self.min4dtg=90
        self.nb=1
        self.ne=21
        self.ni=1

        self.dtau=6
        self.maxtau=168

    def setDmask(self,dtg,member):
        self.dmaskbase=self.dmaskformat%(dtg,member)
        self.dsetmaskbase=self.dsetmaskformat%(dtg,member)
        self.ddir="%s/%s/ens20/"%(self.bddir,dtg)


    def defineCtl(self):

        self.ctl="""%s
index ^%s
undef 9.999E+20
title pgrbfg_2010061700_fhr72_mem001
*  produced by grib2ctl v0.9.12.5p16
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 8   levels 1000 850 700 500 400 300 250 200
tdef %2d  linear %s %s
zdef 26 levels
1000 975 950 925 900 850 800 750 700 650 600 550 500 450 400 350 300 250 200 150 100 70 50 30 20 10 
vars 28
vrta      2  41,100,  0 ** Absolute vorticity [/s]
prc       0  63,  1,  0 ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0 ** Total precipitation [kg/m^2]
capes     0 157,  1,  0 ** Convective Avail. Pot. Energy [J/kg]
cins      0 156,  1,  0 ** Convective inhibition [J/kg]
clt       0  76,200,  0 ** Cloud water [kg/m^2]
zgs       0   7,  1,  0 ** Geopotential height [gpm]
zg       26   7,100,  0 ** Geopotential height [gpm]
sic       0  91,  1,  0 ** Ice concentration (ice=1;no ice=0) [fraction]
lf        0  81,  1,  0 ** Land cover (land=1;sea=0) [fraction]
ps        0   1,  1,  0 ** Pressure [Pa]
psl       0   2,102,  0 ** Pressure reduced to MSL [Pa]
prw       0  54,200,  0 ** Precipitable water [kg/m^2]
hur      26  52,100,  0 ** Relative humidity [%%]
hurs      0  52,105,  2 ** Relative humidity [%%]
soilf     0 144,112, 10 ** Volumetric soil moisture [fraction]
soilw     3 144,112,  0 ** Volumetric soil moisture [fraction]
ts        0  11,  1,  0 ** Temp. [K]
ta       26  11,100,  0 ** Temp. [K]
tas       0  11,105,  2 ** Temp. [K]
tsoil10   0  11,112, 10 ** Temp. [K]
tsoil     3  11,112,  0 ** Temp. [K]
o3t       0  10,200,  0 ** Total ozone [Dobson]
ua       26  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       26  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
sno       0 65,1,0  ** Accum. snow [kg/m^2]
endvars"""%(self.dset,self.gfile,self.ntau,self.gtime,self.dtau)

        self.ctl1=None
        self.ctl2=None
        


class FimEnkfEns2011(GfsEnkf):

    bddir="/lfs1/projects/gfsenkf/gfsenkf_t574"
    
    def initBaseVars(self):

        self.model='fimens'
        self.dmodel='fimens_g7'
        self.omodel='fimens'
        self.atcf2id='FE'
        self.qname='tctrk'

        self.dtau=6
        self.maxtau=168
        self.min4dtg=45
        
        self.nb=1
        self.ne=10
        self.ni=1
        

    def setDdir(self):
        self.ddir="%s/%s/fimens/mem%03d/fim_C"%(self.bddir,self.dtg,self.member)

        
    def setDmask(self,dtg,member):

        self.yy=dtg[2:4]
        self.hh=dtg[8:10]
        self.jday=mf.Dtg2JulianDay(dtg)

        self.dmaskbase="%s%s????????"%(self.yy,self.jday)
        self.dsetmaskbase='''%s%s%s000%%f3'''%(self.yy,self.jday,self.hh)


    def setPathsGrib1(self):

        self.gribtype='grb1'
        self.gmask="%s/%s"%(self.ddir,self.dmaskbase)

        self.tbase="%s_m%03d"%(self.model,self.member)
        self.tdatbase="%s/%s"%(self.tDir,self.tbase)
        
        self.xwgrib='wgrib'
        self.xgribmap='gribmap'

        self.ctlpath="%s.%s.ctl"%(self.tdatbase,self.gribtype)
        self.gmppath="%s.%s.gmp"%(self.tdatbase,self.gribtype)
        self.gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)
        
        self.tpathmask="%s.f???.%s"%(self.tdatbase,self.gribtype)


    def GetTauGrib1File(self,file):
        tau=file[-3:]
        tau=int(tau)
        return(tau)


    # -- grib1 filter methods
    #
    def setFieldRequest1(self,ftype='std',etau=168):
        
        uvplevs=[925,850,200]
        zplevs=[850,500]
        tplevs=[]
        hurplevs=[]
        

        sfcvars={}
        uavars={}

        uarequest={}

        uarequest['ua']=[]
        uarequest['va']=[]
        uarequest['zg']=[]
        uarequest['ta']=[]
        uarequest['hur']=[]
        
        
        for plev in uvplevs:
            uarequest['ua']=uarequest['ua']+ ['100.%d'%(plev)]
            uarequest['va']=uarequest['va']+ ['100.%d'%(plev)]
        
        for plev in zplevs:
            uarequest['zg']=uarequest['zg']+ ['100.%d'%(plev)]

        for plev in tplevs:
            uarequest['ta']=uarequest['ta']+ ['100.%d'%(plev)]

        if(len(hurplevs) > 0):
            for plev in hurplevs:
                uarequest['hur']=uarequest['hur']+ ['100.%d'%(plev)]


        sfcvars['uas']=['ua','109.1']
        sfcvars['vas']=['va','109.1']
        sfcvars['psl']=['psl','102.1'] 
        sfcvars['pr'] =['pr','1.1']
        sfcvars['prc']=['prc','1.1']
        sfcvars['prw']=['prw','1.1']

        uavars['ua']  = ['ua', uarequest['ua'] ]
        uavars['va']  = ['va', uarequest['va'] ]
        uavars['zg']  = ['zg',  uarequest['zg']  ]
        uavars['hur'] = ['hur',   uarequest['hur']   ]
        uavars['ta']  = ['ta',  uarequest['ta']  ]

        btau=0
        dtau=6
        ttaus=range(btau,etau+1,dtau)

        self.sfcvars=sfcvars
        self.uavars=uavars
        self.ttaus=ttaus
        self.ftype=ftype

    def defineCtl(self):

        # -- use FM to make ctlfile
        #
        
        from FM import PrsCtl

        pC=PrsCtl(self.dtg,tdir=self.tDir,dset="%s/%s"%(self.ddir,self.dsetmaskbase))
        pC.taus=self.taus
        pC.setCtl()
        
        self.ctl=pC.ctl
        
        self.ctl1=None
        self.ctl2=None
        


    def getTaus0(self,files):

        taus=[]
        for file in files:
            (dir,file)=os.path.split(file)
            tau=self.getTau0(file)
            taus.append(tau)

        taus.sort()
        return(taus)

    def getTau0(self,file):
        tau=int(file[-3:])
        return(tau)



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setupdset ^pgrbfg_2010061700_fhr%f2_mem001
#

class MFCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'override':['O',0,1,'override'],
            'dtGcycle':['G',0,1,'cycle by dtgs'],
            'lsopt':['L:',None,'a',"""lsopt """],
            'doKlean':['K',1,0,'1 - os.unlink fort.?? and i/o files'],
            'doqsub':['Q',0,1,"""make qsub.sh and qsub"""],
            'members':['M:',None,'a',"""do member opt Nb.Ne.Ni """],
            'min4dtg':['m:',50,'i',"""wall time in minutes for each dtg default is 35"""],
            'dodet':['D',0,1,"dodet = 1 ; run tracker on deterministic"],
            'doClean':['C',0,1,'1 - clean out entire target directory'],
            'expType':['T:',None,'a',"""exp Type -- 2008 for '2008' runs; 'irwd' for runs with irwd superobs"""],
            'lsdata':['l',0,1,"""ls source data"""],
            }

        self.purpose="""
purpose -- create .ctl for gfsenkf
"""
        self.examples='''
%s cur-12
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


argv=sys.argv
CL=MFCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#### if(expType ==  None):   GE=GfsEnkf()
if(expType == 'irwd'):  GE=GfsEnkfIrwd()
if(expType == '2008'):  GE=GfsEnkf2008()
if(expType == 'irwdx'): GE=GfsEnkfIrwdX()
if(expType ==  None or expType == '2011'):   GE=GfsEnkf2011()

print expType

if(expType == 'fimens'): GE=FimEnkfEns2011()

GE.override=override


if(members != None):
    tt=members.split('.')
    if(len(tt) >= 1): GE.nb=int(tt[0])
    if(len(tt) >= 2): GE.ne=int(tt[1])
    else: GE.ne=GE.nb
    if(len(tt) >= 3): GE.ni=int(tt[2])

members=range(GE.nb,GE.ne+1,GE.ni)    

if(dodet):
    members=[0]
    
dtgs=mf.dtg_dtgopt_prc(dtgopt)

if(len(dtgs) > 1 and dtGcycle):

    for dtg in dtgs:
        cmd="%s %s"%(pypath,dtg)
        for a in argv[len(CL.argopts)+1:]:
            if(a != '-G' and a != '-N'):
                cmd="%s %s"%(cmd,a)
        mf.runcmd(cmd,ropt)
    sys.exit()


qname=GE.setQname(dtgopt)
if(doqsub):
    # for 2011 min4dtg=90
    qs=Qsub(argv,doqsub=doqsub,min4dtg=GE.min4dtg,ropt=ropt,qname=qname)
    sys.exit()


for dtg in dtgs:

    for member in members:

        if(doClean): GE.cleanData()

        GE.setDtgMember(dtg,member)
        
        if(lsdata):
            GE.lsData(verb=verb)
            break

        
        if(lsopt == None):
            if(GE.setCtl() == -1): continue

        # -- filter the grib to make small data set to run the mftrk and plot tcgen
        #
        GE.filtGrib1(override=override)

        if(lsopt == None):   print 'III working dtg: ',dtg,' member: %02d'%(member),' GE.ddir ',GE.cdir,GE.cdirtctrk
        if(ropt == 'norun'): continue


        atcfname="%s%02d"%(GE.atcf2id,member)
        modeltrk="%s.mem%02d"%(GE.model,member)
        taus=GE.taus
        maxtau=GE.maxtau
        if(hasattr(GE,'cpath')):
            ctlpath=GE.cpath
        else:
            if(lsopt != None):
                ctlpath='/dev/null'
            else:
                print 'WWW no data for dtg: ',dtg,' member: ',member,lsopt
                continue


        TT=TmTrk(dtg,modeltrk,atcfname,GE.tdir,GE.tdirAdeck,taus,maxtau,ctlpath,domodelpyp=1,verb=1)

        if(lsopt == None):
            TT.doTrk(override=override,doKlean=doKlean,TToverride=override)
            
        if(TT.lstrk(lsopt=lsopt) == 0): print '----- %s : %s '%(dtg,modeltrk)

