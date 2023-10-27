#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

class curlGetGfs0p25(MFbase):
    
    varTaus={
        'anl':['ua','msl','atm'],
        0:['2m','10m','sfc'],
    }
    
    levVarLabels={
        'atm':"lev_entire_atmosphere_%5C%28considered_as_a_single_layer%5C%29&var_PWAT=on",
        '2m':"lev_2_m_above_ground&var_TMP=on&var_TMAX=on&var_TMIN=on",
        '10m':"lev_10_m_above_ground&var_UGRD=on&var_VGRD=on",
        'sfc':"lev_surface&var_TMP=on&var_PRATE=on&var_CPRAT=on&var_APCP=on&var_ACPCP=on",
        ###'msl':"lev_mean_sea_level&var_PRMSL=on",
        'msl':"lev_mean_sea_level&var_MSLET=on", # -- 'correct' slp using eta method
        'ua':"lev_1000_mb=on&lev_100_mb=on&lev_150_mb=on&lev_200_mb=on&lev_250_mb=on&lev_300_mb=on&lev_400_mb=on&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_925_mb=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on",
    }

    areaGrid="leftlon=0&rightlon=360&toplat=90&bottomlat=-90"
    cgiCmd="http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
    cgiCmd="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
    
    def __init__(self,dtg,
                 reqtype='w2flds',
                 model='gfs2',
                 ropt='norun'):

        from M2 import setModel2
        
        yyyymmdd=dtg[0:8]
        self.dtg=dtg
        hh=dtg[8:10]
        self.hh=hh
        self.ropt=ropt
        self.reqtype=reqtype
        self.model=model
        self.modelFileName='gfs-0p25'
        self.modelFileName='gfs2.%s'%(reqtype)
        self.dirGfs="dir=%%2Fgfs.%s%%2F%02d%%2Fatmos"%(yyyymmdd,int(hh))
        m2=setModel2(model)
        self.m2=m2
        self.tdir="%s/%s"%(m2.w2fldsSrcDir,dtg)
        MF.ChkDir(self.tdir,'mk')
        self.fm=m2.DataPath(dtg,dtype='w2flds',dowgribinv=1,verb=1)
        self.fstatuss=self.fm.statuss[dtg]
        
        # -- tdir on kishou
        #
        tdirKishou="%s/%s/dat/%s"%(w2.Nwp2DataBdir,reqtype,model)
        self.tdirKishou=tdirKishou.replace(w2.Nwp2DataBdir,'fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2')

        self.ctlpath="%s/%s.%s.%s.ctl"%(self.tdir,self.model,self.reqtype,self.dtg)
        self.gmppath="%s/%s.%s.%s.grib2.gmp"%(self.tdir,self.model,self.reqtype,self.dtg)

        # -- counter for tau processed
        #
        self.ntauPrc=0
        

    def getTauVars(self,tau):
        
        if(tau == 'anl'):
            ovars=self.varTaus['anl']
            otau=0
        elif(tau == 0):
            ovars=self.varTaus[0]
            otau=tau
        elif(tau > 0):
            ovars=self.levVarLabels.keys()
            ovars.sort()
            otau=tau
        return(ovars,otau)
            
            
        
    def curlTau(self,tau):
        
        if(tau == 'anl'): 
            ctau=tau
        elif(tau >= 0):
            ctau="f%03d"%(tau)
            
        fileGfs="file=gfs.t%2sz.pgrb2.0p25.%s"%(self.hh,ctau)
        return(fileGfs)
    
        
    def curlGet(self,tau,override=0,
                nfilesanl=57,
                
                #nfiles00=61,
                #nfiles00=57,       # -- 20190224 because???
                nfiles00=62,        # -- 20190612 new gfs 
                	
                #nfilesTau=67,
                nfilesTau=71,       # -- 20190612 new gfs
                
                sizmintmp=100000,

                #sizmin00=34500000,
                #sizmin00=31000000, # -- 20190223
                sizmin00=40000000, # -- 20190223

                #sizmin= 35500000,
                #sizmin=  32500000, # -- 20190223 0325
                #sizmin=  42500000, # -- 20190612 new gfs
                sizmin=  42000000, # -- 20200904 make smallernew gfs

                agemin=1.0):
        
        """ run twice in w2.nwp2.py first to get the fields and the 2nd to make sure we got enough
"""
        
        if(tau == 'anl'):
            itau=01
        else:
            itau=int(tau)
            
        MF.sTimer('curl-get-tau-%03d'%(itau))
        (ovars,otau)=self.getTauVars(tau)
        
        opath="%s/%s.%s.f%03d.grb2"%(self.tdir,self.modelFileName,self.dtg,otau)
        tpath="/tmp/tt.%s.f%03d.grb2"%(self.dtg,otau)

        if(len(self.fstatuss.keys()) > 0):
            try:
                nftau=self.fstatuss[otau][1]
            except:
                nftau=-1
        else:
            nftau=-1
        

        sizopath=MF.getPathSiz(opath)
        print 'TTTTTTTTTTTTTTTTTTTTTTTTTTT tau: ',tau,' otau:',otau,' override: ',override,' sizopath: ',sizopath
        if(override and sizopath > 0):
            if(tau == 0):
                print 'OOOOBBBBB -- bypass tau 0 becaue anl has already gotten most of the fields'
            else:
                print 'OOOO - override so blow off opath: ',opath,' tau: ',tau,' otau: ',otau
                cmd="rm %s"%(opath)
                mf.runcmd(cmd,self.ropt)
                sizopath=-999
                nftau=-1
            
        
        #  -- use siz to detect anl,0
        #
        osizmin=sizmin
        if(tau == 'anl' or tau == 0): osizmin=sizmin
        print 'SSSSSSSSSSSS----BBBBBBBBBBB tau: ',tau,sizopath,osizmin
        print 'NNNNNNNNNNNNNNNNNNNNNNNNNNN tau: ',tau,nftau
        
        # -- check if there are enough fields
        #
        if(not(tau == 'anl' or tau == 0) and sizopath > sizmin and nftau > 0):

            if(nftau < nfilesTau):
                print '***************************** III-NNN killing tau: ',tau,' because has too few fields...'
                cmd="rm %s"%(opath)
                mf.runcmd(cmd,self.ropt)
            else:
                print 'WWWWWWW-already curled...tau: ',tau,' opath: ',opath,' sizopath: ',sizopath
                return
                
        # -- check tau 0 = anl+0 should have 61 fields
        #
        ###########elif((tau == 'anl' or tau == 0) and sizopath > sizmin00):
        elif((tau == 0) and sizopath > sizmin00 and nftau >= nfilesanl):  # only check AFTER 'anl' done...
            
            if(nftau < nfiles00):
                print '***************************** III-000 killing tau:  0 because has too few fields... nftau: ',nftau,' nfiles00: ',nfiles00,' sizopath: ',sizopath,' sizmin00: ',sizmin00
                cmd="rm %s"%(opath)
                mf.runcmd(cmd,self.ropt)
            else:
                print 'WWW-000 return because tau: ',tau,' and sizopath: ',sizopath,' > sizmin00: ',sizmin00
                return
            
        # -- check anl which should have most of the bits and 57 fields
        #
        elif((tau == 'anl') and sizopath > sizmin00 and nftau > 0):  # only check AFTER 'anl' done...
            
            if(nftau < nfilesanl):
                print '***************************** III-AAA killing tau:  ANL because has too few fields... nftau: ',nftau,' nfiles00: ',nfiles00,' sizopath: ',sizopath,' sizmin00: ',sizmin00
                cmd="rm %s"%(opath)
                mf.runcmd(cmd,self.ropt)
            else:
                print 'WWW-AAA return because tau: ',tau,' and sizopath: ',sizopath,' > sizmin00: ',sizmin00
                return
                
                
        # -- noload...only if there...
        #
        else:

            if(sizopath != -999 and tau != 0):
                print 'III-incomplete download siz too small opath: ',opath,' siz: ',sizopath,' rm...'
                cmd="rm %s"%(opath)
                mf.runcmd(cmd,self.ropt)

        if(tau != 'anl'):
            self.ntauPrc=self.ntauPrc+1
            
        # -- do the curl here
        #
        doDelay=1
        delaySec=2
        maxCurlTime=30
        maxCurlTime=45
        maxCurtTime=60
        
        #curlOpt='--progress-bar'
        #curlOpt='-sS --max-time %d'%(maxCurlTime)
        # -- 20220825 -- ncep change in cert authority
        curlOpt='-k -sS --max-time %d'%(maxCurlTime)
        
        for ovar in ovars:
            levvar=self.levVarLabels[ovar]
            url="%s?%s&%s&%s&%s"%(self.cgiCmd,self.curlTau(tau),levvar,self.areaGrid,self.dirGfs)
            cmd='''curl %s "%s" -o %s'''%(curlOpt,url,tpath)
            mf.runcmd(cmd,self.ropt)
            
            # -- 2021042000 throttle at NCO
            #
            if(doDelay):
                sleep(delaySec)
            
            siztpath=MF.getPathSiz(tpath)
            if(siztpath > sizmintmp):
                cmd="cat %s >> %s"%(tpath,opath)        
                mf.runcmd(cmd,self.ropt)
            
            cmd="rm %s"%(tpath)
            mf.runcmd(cmd,self.ropt)
            
        sizopath=MF.getPathSiz(opath)
        osizmin=sizmin
        if(tau == 'anl' or tau == 0): osizmin=sizmin00
        print 'SSSSSSSSSSSS----AAAAAAAAAAA tau: ',tau,sizopath,osizmin,' ntauPrc: ',self.ntauPrc
        MF.dTimer('curl-get-tau-%03d'%(itau))
            
    def doGribmap(self,ropt=''):

        wgribFilterOpt='-C'
        if(w2.onKaze): wgribFilterOpt='-C -R'
        if(self.ntauPrc > 0):
            cmd="w2-fld-wgrib-filter.py %s %s %s"%(self.dtg,self.model,wgribFilterOpt)
            mf.runcmd(cmd,ropt)
        else:
            print '---'
            print 'III-TTT skip doing w2-fld-wgrib-filter.py because no taus actually processed for dtg: ',self.dtg
            print '---'
            return
        
#"http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl
#?
#file=gfs.t12z.pgrb2.0p25.anl&lev_1000_mb=on&lev_100_mb=on&lev_150_mb=on&lev_200_mb=on&lev_250_mb=on&lev_300_mb=on&lev_400_mb=on&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_925_mb=on&var_HGT=on&var_RH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&
#leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.2017021512
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class CurlCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            'model':'gfs2',
            }

        self.options={
            'override':      ['O',0,1,'override'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'tauopt':        ['t:',None,'a',"""tauopt: 'anl0' or btau.etau.dtau"""],
            }

        self.purpose='''
purpose -- pull hi-res gfs2 w2flds local and mss
%s cur'''
        self.examples='''
%s cur'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

MF.sTimer(tag='curl-all')
CL=CurlCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

btau=0 ; etau=192 ; dtau=6
taus=['anl']+range(btau,etau+1,dtau)

if(tauopt != None): 
    if(tauopt == 'anl0'): 
        taus=['anl',0]
    else:
        taus=w2.getTausFromTauopt(tauopt)

dtgs=mf.dtg_dtgopt_prc(dtgopt)
for dtg in dtgs:
    MF.sTimer('curl-gfs-%s'%(dtg))
    cG=curlGetGfs0p25(dtg,ropt=ropt)
    cG.alltaus=taus
    for tau in taus:
        cG.curlGet(tau,override=override)
        
    cG.doGribmap(ropt=ropt)
    MF.dTimer('curl-gfs-%s'%(dtg))

MF.dTimer(tag='curl-all')

