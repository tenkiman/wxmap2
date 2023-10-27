#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from TCtmtrkN import TmTrkN

class TmTrkN0p125(MFbase):
    
    def __init__(self,
                 dtg,
                 modOpt='fim9',
                 rev='r4975',
                 verb=0,
                 override=0,
                 ):
                 
        self.dtg=dtg
        self.override=override
        
        self.gtime=mf.dtg2gtime(dtg)
        self.etau=168
        self.dtau=6
        self.nt=self.etau/self.dtau + 1
        self.jDay=mf.Dtg2JulianDay(self.dtg)
        self.dtgJ="%s%s%s00"%(dtg[2:4],self.jDay,dtg[8:10])
        self.rev=rev
        
        
        if(w2.onWjet and modOpt == 'fim9'):

            self.fimRun='FIM9'
            self.fimRunW2flds='FIM9.%s.w2flds'%(self.rev)
            self.fimNameW2flds='fim9h'
            self.modelW2='fim9h'
            
            self.sdirBase='/home/rtfim'
            self.sdir="%s/%s/FIMrun/%s"%(self.sdirBase,self.fimRun,self.dtg)
            self.sdirW2flds="%s/post_C/174/NAT/grib2"%(self.sdir)
            self.dset="""%s/%s.%s0%%f3.grb2"""%(self.sdirW2flds,self.fimRunW2flds,self.dtgJ)
            self.index="""%s.%s.gmp2"""%(self.fimNameW2flds,self.dtg)
            
            self.models=['fim9','fim9h']
            self.model2AtcfName={
                'fim9h':'F9HJ',
                'fim9':'FM9J'
            }
            self.modelRes={
                'fim9h':0.125,
                'fim9':0.5
                }
            
            self.modelDotrkonly={
                'fim9h':1,
                'fim9':0,
                }

            self.modelOverride={
                'fim9h':1,
                'fim9':0,
                }
            

        elif(w2.onWjet and modOpt == 'fim8'):
            
            self.fimRun='FIM'
            self.fimRunW2flds='FIM.%s.w2flds'%(self.rev)
            self.fimNameW2flds='fim8h'
            self.modelW2='fim8h'
            
            self.sdirBase='/home/rtfim'
            self.sdir="%s/%s/FIMrun/%s"%(self.sdirBase,self.fimRun,self.dtg)
            self.sdirW2flds="%s/post_C/174/NAT/grib2"%(self.sdir)
            self.dset="""%s/%s.%s0%%f3.grb2"""%(self.sdirW2flds,self.fimRunW2flds,self.dtgJ)
            self.index="""%s.%s.gmp2"""%(self.fimNameW2flds,self.dtg)
            
            self.models=['fim8','fim8h']
            self.model2AtcfName={
                'fim8h':'F8HJ',
                'fim8':'FM8J'
            }
            self.modelRes={
                'fim8h':0.125,
                'fim8':0.5
                }
            
            self.modelDotrkonly={
                'fim8h':1,
                'fim8':0,
                }

            self.modelOverride={
                'fim8h':1,
                'fim8':0,
                }
            

            
        elif(w2.onZeus and modOpt == 'fim9'):
            
            self.fimRun='FIM9ZEUS'
            self.fimRunW2flds='FIM9.r4975.w2flds'
            self.fimNameW2flds='fim9h'
            self.modelW2='fim9h'
            
            self.sdirBase='/home/rtfim'
            self.sdir="%s/%s/FIMrun/%s"%(self.sdirBase,self.fimRun,self.dtg)
            self.sdirW2flds="%s/post_C/174/NAT/grib2"%(self.sdir)
            self.dset="""%s/%s.%s0%%f3.grb2"""%(self.sdirW2flds,self.fimRunW2flds,self.dtgJ)
            self.index="""%s.%s.gmp2"""%(self.fimNameW2flds,self.dtg)
            
            self.models=['fim9','fim9h']
            self.model2AtcfName={
                'fim9h':'F9HZ',
                'fim9':'FM9Z'
            }
            self.modelRes={
                'fim9h':0.125,
                'fim9':0.5
                }
            
            self.modelDotrkonly={
                'fim9h':1,
                'fim9':0,
                }

            self.modelOverride={
                'fim9h':1,
                'fim9':0,
                }
            
        elif(w2.onZeus and modOpt == 'fim8'):
            
            self.fimRun='FIMZEUS'
            self.fimRunW2flds='FIM8.r4975.w2flds'
            self.fimNameW2flds='fim8h'
            self.modelW2='fim8h'
            
            self.sdirBase='/home/rtfim'
            self.sdir="%s/%s/FIMrun/%s"%(self.sdirBase,self.fimRun,self.dtg)
            self.sdirW2flds="%s/post_C/174/NAT/grib2"%(self.sdir)
            self.dset="""%s/%s.%s0%%f3.grb2"""%(self.sdirW2flds,self.fimRunW2flds,self.dtgJ)
            self.index="""%s.%s.gmp2"""%(self.fimNameW2flds,self.dtg)
            
            self.models=['fim8','fim8h']
            self.model2AtcfName={
                'fim8h':'F8HZ',
                'fim8':'FM8Z'
            }
            self.modelRes={
                'fim8h':0.125,
                'fim8':0.5
                }
            
            self.modelDotrkonly={
                'fim8h':1,
                'fim8':0,
                }

            self.modelOverride={
                'fim8h':1,
                'fim8':0,
                }
            
            
        self.tdirDat="%s/nwp2/w2flds/dat/%s/%s"%(w2.DatBdirW2,self.modelW2,dtg)
        MF.ChkDir(self.tdirDat,'mk')
        self.ctlpath="%s/%s.w2flds.%s.ctl"%(self.tdirDat,self.modelW2,self.dtg)
        self.gmppath="%s/%s"%(self.tdirDat,self.index)
        
        # -- check if there are grib2s
        #
        grb2mask=self.dset.replace("%f3","???")
        grb2files=glob.glob(grb2mask)

        if(len(grb2files) == 0):
            self.datathere=0
        else:
            self.datathere=1

            
        
            
        
    def makeCtl(self):
        
        self.ctl='''dset %s
index ^%s
undef 9.999E+20
title /home/rtfim/FIM9ZEUS/FIMrun/2015050412/post_C/174/NAT/grib2/FIM9.r4975.w2flds.1512412000006.grb2
*  produced by g2ctl v0.0.4m
* griddef=1:0:(2880 x 1440):grid_template=0:winds(N/S): lat-lon grid:(2880 x 1440) units 1e-06 input WE:NS output WE:SN res 48 lat 89.938000 to -89.938000 by 0.125000 lon 0.062000 to 359.938000 by 0.125000 #points=4147200:winds(N/S)
dtype grib2
ydef 1440 linear  -89.938 0.125
xdef 2880 linear -359.938 0.125
tdef   %d linear %s %dhr
* PROFILE hPa
zdef 11 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000
options pascals template
vars 14
prc    0,1,0     0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr     0,1,0     0,1,8,1  ** surface Total Precipitation [kg/m^2]
zg    11,100     0,3,5    ** (1000 925 850 700 500.. 300 250 200 150 100) Geopotential Height [gpm]
prw    0,1,0     0,1,3    ** surface Precipitable Water [kg/m^2]
hur   11,100     0,1,1    ** (1000 925 850 700 500.. 300 250 200 150 100) Relative Humidity [%%]
hurs   0,105,1   0,1,1    ** 1 hybrid level Relative Humidity [%%s]
ts     0,1,0     0,0,0    ** surface Temperature [K]
ta    11,100     0,0,0    ** (1000 925 850 700 500.. 300 250 200 150 100) Temperature [K]
tas    0,105,1   0,0,0    ** 1 hybrid level Temperature [K]
ua    11,100     0,2,2    ** (1000 925 850 700 500.. 300 250 200 150 100) U-Component of Wind [m/s]
uas    0,103,10  0,2,2    ** 10 m above ground U-Component of Wind [m/s]
va    11,100     0,2,3    ** (1000 925 850 700 500.. 300 250 200 150 100) V-Component of Wind [m/s]
vas    0,103,10  0,2,3    ** 10 m above ground V-Component of Wind [m/s]
psl    0,101,0   0,3,198  ** mean sea level desc [unit]
ENDVARS'''%(self.dset,
            self.index,
            self.nt,self.gtime,self.dtau,
            
            )
        
        MF.WriteString2Path(self.ctl,self.ctlpath)
        
        
        if(self.override or MF.getPathSiz(self.gmppath) <= 0):
            
            MF.ChangeDir(self.tdirDat,verb=1)
            cmd="gribmap -v -i %s"%(self.ctlpath)
            mf.runcmd(cmd,'')
            
            MF.ChangeDir(CL.curdir,verb=1)
        
    
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgs'],
            #2:['modelopt',  """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
        }

        self.defaults={
            'doupdate':0,
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'modOpt':           ['m:','fim9','a','fim8|[fim9]'],
            'rev':              ['r:','r5137','a','r4794 | [r5137]'],
            'dols':             ['l',0,1,'ls basics'],
            'doCpOnly':         ['C',0,1,'1 - do the cp/rename only'],
            'doClean':          ['K',0,1,'1 - os.unlink fort.?? and i/o files'],
            'doCleanTrk':       ['x',0,1,'clean trk files in TT.doTrk method'],
            'doCleanAll':       ['k',0,1,'kill off tmtrk*'],
            'dotrkonly':        ['t',0,1,'1 - run only in tracker mode'],
            'dogenonly':        ['g',0,1,'1 - do genesis tracker only'],
            'doMFtrkN':         ['M',0,1,'1 - run MF tracker after...'],            

        }

        self.purpose="""
run new version of Tim Marchok's genesis tracker"""

        self.examples='''
%s cur12 gfs2'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

# -----------------------------------  default setting of max taus
#
maxtau=168
mintauTC=132

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)
dtg=dtgs[0]

# -- hardwired vars
#
taus=range(0,maxtau+1,6)
nfields={mintauTC:68}
dolsonly=0
dolsLong=0
if(dols): 
    dolsonly=1
    dolsLong=1
if(doCpOnly):
    dolsonly=1
    
dowindow=0
GRIBoverride=0
GENoverride=0

MF.sTimer('tmtrkN-ALL')

for dtg in dtgs:
    
    MF.sTimer('tmtrkN-%s'%(dtg))
    
    tmT=TmTrkN0p125(dtg,modOpt,rev,override=override)
    if(tmT.datathere == 0): 
        print "III(%s) - no grb2 for dtg: %s"%(CL.pyfile,dtg)
        continue
    
    tmT.makeCtl()
    models=tmT.models
    
    for model in models:
        
        modOverride=tmT.modelOverride[model]
        if(override): modOverride=1
        
        MF.sTimer('tmtrkN-base-%s'%(model))
        TT=TmTrkN(dtg,model,tmT.ctlpath,taus,maxtau,
                  atcfname=tmT.model2AtcfName[model],
                  nfields=nfields,
                  mintauTC=mintauTC,
                  dols=dolsonly,
                  regridTracker=tmT.modelRes[model],
                  override=modOverride)
        MF.dTimer('tmtrkN-base-%s'%(model))
        
        if(doCpOnly):
            TT.cpTrackers2AdeckDir()
            TT.relabelAdeckDirTrackers(verb=1)    
            continue
            
        # -- ls
        #
        if(dols or dolsLong):
            if(dolsLong): TT.lstrk(lsopt='l')
            else:         TT.lstrk(lsopt='s')
            continue
        
        # -- ttttttttttttttttttttttttttttttttttttttt actual tracking ttttttttttttttttttttttttttttttttttttttttttttttttttttt
        #
        
        # -- do data and tracking
        #
    
        MF.sTimer('tmtrkN-doTrk-%s'%(model))
        
        TT=TT.doTrk(
            dotrkonly=tmT.modelDotrkonly[model],
            dogenonly=dogenonly,
            doClean=doCleanTrk,
            override=override,
            dowindow=dowindow,
            dolsonly=dolsonly,
            TToverride=modOverride,
            GRIBoverride=modOverride,
            GENoverride=override,
        )
        
        MF.dTimer('tmtrkN-doTrk-%s'%(model))
        rcTrkAfter=TT.allreadydone
        
        # -- cp trackers to adeckdir and relabel to tctrk*.NNB.YYYY if override or tracking done
        #
        if(rcTrkAfter >= 0 or modOverride):  
            TT.cpTrackers2AdeckDir()
            TT.relabelAdeckDirTrackers(verb=1)    
    
    MF.dTimer('tmtrkN-%s'%(dtg))

MF.dTimer('tmtrkN-ALL')
