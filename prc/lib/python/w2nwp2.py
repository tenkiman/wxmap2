from M import *
MF=MFutils()

from w2localvars import W2rawECHiRes,EcNogapsCssFeed,onWjet,pan2Jet,onTenki
from w2switches import doPrCtl,doHlCtl,doMandCtl

if(pan2Jet):
    sbdir='/pan2/projects/fim-njet/fiorino/w21/dat/nwp2'    
else:
####    sbdir='/lfs2/projects/fim/fiorino/w21/dat/nwp2'
    sbdir='/lfs1/projects/fim/fiorino/w21/dat/nwp2'

class W2Nwp2(MFbase):

    if(pan2Jet):
        sbdir='/pan2/projects/fim-njet/fiorino/w21/dat/nwp2'    
    else:
####        sbdir='/lfs2/projects/fim/fiorino/w21/dat/nwp2'
        sbdir='/lfs1/projects/fim/fiorino/w21/dat/nwp2'

    # -- have to hardwire here because we can't do a from WxMAP2 import * ; w2=W2()
    #
    rserver='Michael.Fiorino@jetscp.rdhpcs.noaa.gov'
    rserver='Michael.Fiorino@dtn-jet.rdhpcs.noaa.gov'

    rserverTheia='Michael.Fiorino@dtn-theia.rdhpcs.noaa.gov'
    sbdirTheia='/scratch3/BMC/fim/fiorino/w21/dat/nwp2'

    rserverHera='Michael.Fiorino@dtn-hera.rdhpcs.noaa.gov'
    sbdirHera='/scratch2/BMC/gsd-fv3-dev/fiorino/w21/dat/nwp2'

    def GetPlotStatus(self,dtg,model,areaopt='all',plotopt='all'):

        tcmodel=self.Model2Model2TcModel(model)
        pmodel=self.Model2Model2PlotModel(model)
        taus=self.ModelPlotTaus(model,dtg)

        gcdir=self.getW2_MODELS_CURRENT_GRFDIR(model)
        gdir=gcdir+'/%s'%(dtg)

        plots2do=[]
        areas=[]

        if(areaopt == 'all'):
            if(plotopt == 'clm'):
                areas=self.W2_AREAS_CLIMO
            elif(plotopt == 'basemap'):
                areas=self.W2_AREAS_ALL
            else:
                areas=self.W2_AREAS
        else:
            areas=[areaopt]

        for tau in taus:

            for area in areas:

                if(plotopt == 'all'):
                    try:
                        plots=self.plot_control[pmodel,area,'plots']
                    except:
                        plots=''
                    plots=plots.split()
                else:
                    plots=[plotopt]

                if(len(plots) > 0):

                    for plot in plots:

                        gmodname=self.ModeltoGrfModel(model)

                        if(plot != 'basemap'):
                            gname="%s/%s.%s.%03d.%s.png"%(gdir,gmodname,plot,tau,area)
                        try:
                            mopt1=self.plot_control[area,plot,'units']
                        except:
                            mopt1=''

                        taschk=1
                        if((plot == 'tmx' or plot == 'tmn') and (tau < 24 or tau > 144) ): taschk=0
                        if(
                            (not(os.path.exists(gname) and os.path.getsize(gname)) > 0) and
                            taschk
                            ):
                            plots2do.append([tau,plot])

        #
        # extras ----- precip
        #

        etaus=[0]

        for etau in etaus:

            for area in areas:

                plots=['op06']

                for plot in plots:

                    gmodname=self.ModeltoGrfModel(model)

                    if(plot != 'basemap'):
                        gname="%s/%s.%s.%03d.%s.png"%(gdir,gmodname,plot,etau,area)
                    try:
                        mopt1=self.plot_control[area,plot,'units']
                    except:
                        mopt1=''

                    if(not(os.path.exists(gname) and os.path.getsize(gname) > 0)):
                        plots2do.append([etau,plot])


        nplots2do=len(plots2do)

        return(nplots2do)


    def ChkIfRunningNWP(self,dtg,pyfile,model=None,killjob=0,verb=0,incron=1):

        pids=mf.LsPids()

        rc=0
        for pid in pids:
            cpid=pid[0]
            prc=pid[2]
            
            if(mf.find(prc,pyfile)):
                incrontest=(mf.find(prc,'tcsh') or mf.find(prc,'/bin/sh -c') or not(mf.find(prc,'ython')))
                if(verb):
                    print 'w2.ChkIfRunningNWP() found pyfile: ',pyfile,'in prc: ',prc,' incrontest: ',incrontest
                    
                if(model == None):
                    if(incron and incrontest):
                        continue
                    else:
                        rc=rc+1
                        
                elif(mf.find(prc,model)):
                    if(incron and (mf.find(prc,'tcsh') or mf.find(prc,'/bin/sh -c'))): continue
                    tt=prc.split()
                    try:
                        opt1=tt[2]
                    except:
                        opt1=None

                    try:
                        opt2=tt[3]
                    except:
                        opt2=None

                    if(not((opt1 != None and opt1 == dtg) and (opt2 != None and opt2 == model))): continue

                    rc=rc+1

                    if(killjob):
                        cmd="kill %s"%(cpid)
                        mf.runcmd(cmd,'')

                    if(not(mf.find(prc,'-N'))):
                        print 'PPP current run: ',cpid,prc


        return(rc)


    def RsyncWeb(self,dtg,ropt,chkrun=1):

        sdir=self.W2BaseDirWeb
        tdir=self.EsrlHttpIntranetDocRoot
        pdir=self.PrcDirWxmap2W2
        rsyncopt="--delete -alv --exclude-from=%s/ex.rsync.brain.txt"%(pdir)
        cmd="rsync %s %s/. %s/."%(rsyncopt,sdir,tdir)

        AllReadyRunning=0
        pids=mf.LsPids()
        for pid in pids:
            cpid=pid[0]
            ppid=pid[1]
            prc=pid[2]
            rpid=mf.find(prc,cmd)
            if(rpid):
                AllReadyRunning=1
                break

        if(AllReadyRunning and chkrun):
            print 'WWW: RSYNC already running, keep going.... ',curdtg,curtime
            print 'WWW: rsync cmd: ',cmd
            return

        mf.runcmd(cmd,ropt)

    def RsyncWjetDcomNcep2Local(self,dtg,model,ropt=''):

        (omodel,grbtype,tautype,doLn)=self.Model2ModelProp(model)

        pdir=self.PrcDirWxmap2W2
        sdir="%s/%s/%s"%(self.sbdir,self.Model2CenterModel(model),dtg)
        tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
        tdir="%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model))
        rsyncopt='--delete --size-only -alv'

        if(doLn):
            rsyncopt=" -av --size-only --exclude-from=%s/ex.rsync.wjet.txt --timeout=90 --protocol=29 "%(pdir)
        else:
            rsyncopt=" -av --size-only --no-links --exclude-from=%s/ex.rsync.wjet.txt --timeout=90 --protocol=29 "%(pdir)

        #
        # blow away the .gmp files to force bring over the freshest
        #
        mask="%s/%s/*.gmp"%(tdir,dtg)
        gmppaths=glob.glob(mask)

        for gmppath in gmppaths:
            os.unlink(gmppath)

        cmd="rsync %s %s:%s %s"%(rsyncopt,self.rserver,sdir,tdir)
        mf.runcmd(cmd,ropt)

    def ScpWjetDcomNcep2Local(self,dtg,model,ropt=''):

        pdir=self.PrcDirWxmap2W2
        sdir="%s/%s/%s"%(self.sbdir,self.Model2CenterModel(model),dtg)
        tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
        MF.ChkDir(tdir,'mk')

        cmd="scp -p %s:%s/* %s/."%(self.rserver,sdir,tdir)
        mf.runcmd(cmd,ropt)


    def RsyncWjetW2flds2Local(self,dtg,model,ropt='',doKishou=0,doTheia=0,doHfip=0):

        (omodel,grbtype,tautype,doLn)=self.Model2ModelProp(model)

        if(doKishou):
            rserver='fiorino@kishou.fsl.noaa.gov'
            sbdir='/w21/dat/nwp2/w2flds/dat'
        elif(doTheia):
            rserver=self.rserverTheia
            sbdir=self.sbdirTheia
            # -- 20191002 -- now do hera vice theia
            rserver=self.rserverHera
            sbdir=self.sbdirHera
        else:
            rserver=self.rserver
            sbdir=self.sbdir

        sdir="%s/w2flds/dat/%s/%s/"%(sbdir,model,dtg)
        tdir="%s/w2flds/dat/%s/%s/"%(self.Nwp2DataBdir,model,dtg)
        mf.ChkDir(tdir,'mk')
        rsyncopt='--delete --size-only -alv'
        if(doLn):
            rsyncopt=' --protocol=29 --size-only -alv --timeout=60'
        else:
            rsyncopt=' --protocol=29 --size-only -av --no-links --timeout=60'
        #rsyncopt=''' --protocol=29 --size-only -alv -e "ssh -o HostKeyAlgorithms=ssh-dss"'''

        cmd="rsync %s %s:%s %s"%(rsyncopt,rserver,sdir,tdir)
        mf.runcmd(cmd,ropt)


        if(doHfip):

            sdir="%s/w2flds/dat/%s/%s/"%(self.Nwp2DataBdir,model,dtg)
            tbdir='%s/../../w21/dat/nwp2'%(os.getenv('W2_HFIP'))
            # -- make publically available
            #
            tbdir= '%s/w21/dat/nwp2'%(os.getenv('W2_HFIP'))
            tdir="%s/w2flds/dat/%s/%s/"%(tbdir,model,dtg)
            MF.ChkDir(tdir,'mk')
            rsyncopt='--delete --size-only -alv'
            if(doLn):
                rsyncopt=' --protocol=29 --size-only -alv --timeout=60'
            else:
                rsyncopt=' --protocol=29 --size-only -av --no-links --timeout=60'

            cmd="rsync %s %s %s"%(rsyncopt,sdir,tdir)
            mf.runcmd(cmd,ropt)


        if(grbtype == 'grb1'): wpext='wgrib1.txt'
        if(grbtype == 'grb2'): wpext='wgrib2.txt'
        localfilemask="%s/%s.%s.*.%s"%(tdir,omodel,dtg,grbtype)
        localmodelfiles=glob.glob(localfilemask)

        return(tdir,localmodelfiles)


    def RsyncWjetEsrlAdecks2Local(self,dtg,ropt=''):

        sdir='%s/tc/adeck/esrl/%s/'%(sbdir,dtg[0:4])
        tdir="%s/%s/"%(self.TcAdecksEsrlDir,dtg[0:4])
        rsyncopt=' --protocol=29 --update --size-only -alv'
        cmd="rsync %s %s:%s %s"%(rsyncopt,self.rserver,sdir,tdir)
        mf.runcmd(cmd,ropt)


    def RsyncWjetLocal2Cira(self,dtg,ropt=''):

        rsyncopt=' --protocol=29 --update --size-only -alv'

####        tdir='/lfs2/projects/fim/fiorino/w21/dat/tc/cira/mtcswa/%s/'%(dtg[0:4])
        tdir='/lfs1/projects/fim/fiorino/w21/dat/tc/cira/mtcswa/%s/'%(dtg[0:4])
        sdir="/w21/dat/tc/cira/mtcswa/%s/"%(dtg[0:4])
        cmd="rsync %s %s %s:%s"%(rsyncopt,sdir,self.rserver,tdir)
        mf.runcmd(cmd,ropt)

####        tdir='/lfs2/projects/fim/fiorino/w21/dat/tc/cira/mtcswa_Late/%s/'%(dtg[0:4])
        tdir='/lfs1/projects/fim/fiorino/w21/dat/tc/cira/mtcswa_Late/%s/'%(dtg[0:4])
        sdir="/w21/dat/tc/cira/mtcswa_Late/%s/"%(dtg[0:4])
        cmd="rsync %s %s %s:%s"%(rsyncopt,sdir,self.rserver,tdir)
        mf.runcmd(cmd,ropt)


    def FilterNwp2SmaskTaus(self,modelfiles,model,taus=range(0,168+1,6)):

        omodelfiles=[]

        modelfiles.sort()

        # -- alsways on the m2 object
        btau=self.m2.btau
        etau=self.m2.etau
        dtau=self.m2.dtau

        taus=range(btau,etau+1,dtau)


        for mfile in modelfiles:
            (dir,file)=os.path.split(mfile)
            if(model == 'gfs2' or model == 'fim8'):
                mtau=int(file[-4:])
                if(mtau in taus):
                    omodelfiles.append(mfile)
            else:
                omodelfiles.append(mfile)

        return(omodelfiles)


    def cleanMssGet(self,sdir,ropt=''):

        cmd="rm %s/*"%(sdir)
        mf.runcmd(cmd,ropt)


    def getRcHpssGet(self,lines,verb=0):
        rc=0
        for line in lines:
            if(verb): print line[:-1]
            if(mf.find(line,'no such HPSS file')): rc=-1

        return(rc)

    def DComNcepDirNRsync(self,dtg,model,doRsyncWjetOnly=0,override=0,ropt='',
                          doNomads=0,doNcepNomads=0,
                          dormdata=0,mssGetDir=None,verb=0):


        yymm=dtg[0:6]
        yymmdd=dtg[0:8]
        yy=dtg[2:4]
        mmddhh=dtg[4:10]
        hh=dtg[8:10]

        julday=int(mf.Dtg2JulianDay(dtg))

        deltaSiz=-999

        idtg=dtg
        odtg=dtg

        smask2=None

        from M2 import setModel2

        m2=setModel2(model)
        self.m2=m2

        if(mf.find(model,'gfs2')):

            tdirbase="%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model))
            tdir="%s/%s"%(tdirbase,dtg)

            if(onWjet and mssGetDir != None and ropt != 'norun'):

                sdir="%s/%s"%(tdirbase,mssGetDir)
                MF.ChkDir(sdir,'mk')

                if(dormdata):
                    cmd="rm %s/*"%(sdir)
                    mf.runcmd(cmd,ropt)
                    return(None,None,None,None,None,None,None)

                # -- old mss code
                #starball="%s/fc.%s00.tar.gz"%(sdir,dtg)
                #starballGsi="%s/an.%s00.tar.gz"%(sdir,dtg)
                #if(not(os.path.exists(starball))):

                # -- get the tarballs from hpss vice mss
                #

                yyyy=dtg[0:4]
                mm=dtg[4:6]
                dd=dtg[6:8]

                #/mss/fdr/2008/08/12/grib/ftp/7/0/96/0_259920_0/
                #msspath="/BMC/fdr/%s/%s/%s/grib/ftp/7/0/96/0_259920_0/%s00.tar.gz"%(yyyy,mm,dd,dtg)
                #cmd="mssGet %s %s"%(msspath,starball)
                #mf.runcmd(cmd,ropt)
                #msspathGsi="/mss/fdr/%s/%s/%s/grib/ftp/7/0/81/0_259920_0/%s00.tar.gz"%(yyyy,mm,dd,dtg)
                #cmd="mssGet %s %s"%(msspathGsi,starballGsi)
                #mf.runcmd(cmd,ropt)

                tarball="%s00.tar.gz"%(dtg)

                # -- forecast
                #
                msspath="/BMC/fdr/%s/%s/%s/grib/ftp/7/0/96/0_259920_0/%s"%(yyyy,mm,dd,tarball)
                MF.ChangeDir(sdir)

                cmd="/apps/hpss/hsi get %s ."%(msspath)
                mf.runcmd(cmd,ropt)

                cmd="tar -zxvf %s"%(tarball)
                mf.runcmd(cmd,ropt)

                cmd="rm %s"%(tarball)
                mf.runcmd(cmd,ropt)

                #  -- analysis -- overwrite the tau0 from the fc with analyses
                #
                msspathGsi="/BMC/fdr/%s/%s/%s/grib/ftp/7/0/81/0_259920_0/%s"%(yyyy,mm,dd,tarball)
                cmd="/apps/hpss/hsi get %s ."%(msspathGsi)
                mf.runcmd(cmd,ropt)

                cmd="tar -zxvf %s"%(tarball)
                mf.runcmd(cmd,ropt)

                cmd="rm %s"%(tarball)
                mf.runcmd(cmd,ropt)

            else:
                sdir="/public/data/grids/gfs/0p5deg/grib2"
                sdir="/public/data/grids/gfs/0p25deg/grib2"

            mf.ChkDir(tdir,'mk')

            smask="%2s%03d%2s*"%(yy,julday,hh)
            source='public'

            # -- pull from nomads.ncdc.noaa.gov
            #

            if(not(onWjet) and (doNomads or doNcepNomads) ):

                #taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168,180]
                # -- 20140611 - bug -- missing 168 <= this ctg
                taus=range(0,168+1,6)
                if(self.m2.etau > 168):
                    taus=taus+range(168+12,self.m2.etau+1,12)

                minGfsNomads=5000000
                sdir=tdir

                MF.sTimer('Nomads: %s %s'%(model,dtg))
                if(doNcepNomads):
                    for tau in taus:
                        tname="%2s%03d%2s00%04d"%(yy,julday,hh,tau)
                        tpath="%s/%s"%(tdir,tname)
                        siztpath=MF.GetPathSiz(tpath)
                        # -- mf 20150309 -- mod to filenaming > 20150114 gfs2--> T1534
                        #
                        turl="http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.%s/gfs.t%02dz.pgrb2.0p50.f%03d"%(dtg,int(hh),int(tau))
                        turl="%s --timeout=30 "%(turl)

                        if(not(os.path.exists(tpath)) or override == 1 or siztpath <= minGfsNomads):
                            cmd="wget %s -O %s"%(turl,tpath)
                            mf.runcmd(cmd,ropt)
                else:

                    for tau in taus:
                        tname="%2s%03d%2s00%04d"%(yy,julday,hh,tau)
                        tpath="%s/%s"%(tdir,tname)
                        siztpath=MF.GetPathSiz(tpath)

                        if(not(os.path.exists(tpath)) or override == 1 or siztpath <= 0):
                            cmd="wget http://nomads.ncdc.noaa.gov/data/gfs4/%s/%s/gfs_4_%s_%s00_%03d.grb2 -O %s"%(yymm,yymmdd,yymmdd,hh,tau,tpath)
                            mf.runcmd(cmd,ropt)


                MF.dTimer('Nomads: %s %s'%(model,dtg))

                source='nomads'


            omodel='gfs2'
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)

        elif(model == 'fv3e' or model == 'fv3g'):

            tdirbase="%s/%s"%(self.Nwp2DataBdir,m2.centermodel)
            tdir="%s/%s"%(tdirbase,dtg)
            omodel=model
            smask="%2s%03d%2s*"%(yy,julday,hh)

            nfiles=len(glob.glob("%s/%s.*.grb*"%(tdir,omodel)))

            sdir='/public/data/grids/fv3gfs_gsd/0p5deg/grib2'

            mf.ChkDir(tdir,'mk')
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='public'


        elif(model == 'fim8'):

            tdirbase="%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model))
            tdir="%s/%s"%(tdirbase,dtg)
            omodel='fim8'
            smask="%2s%03d%2s*"%(yy,julday,hh)

            nfiles=len(glob.glob("%s/%s.*.grb*"%(tdir,omodel)))

            if(onWjet and mssGetDir != None and ropt != 'norun'):

                sdir="%s/%s"%(tdirbase,mssGetDir)
                MF.ChkDir(sdir,'mk')
                MF.ChangeDir(sdir)

                if(dormdata):
                    cmd="rm %s/*"%(sdir)
                    mf.runcmd(cmd,ropt)
                    return(None,None,None,None,None,None,None)

                yyyy=dtg[0:4]
                mm=dtg[4:6]
                dd=dtg[6:8]

                tarball="%s00.tar.gz"%(dtg)
                siz=MF.GetPathSiz(tarball)

                if(siz < 0 or override):
                    msspath="/BMC/fdr/%s/%s/%s/data/fsl/fim/nat/grib1/%s"%(yyyy,mm,dd,tarball)
                    MF.sTimer("hsi get: %s"%(msspath))

                    cmd="/apps/hpss/hsi get %s ."%(msspath)
                    lines=MF.runcmdLog(cmd)
                    rc=self.getRcHpssGet(lines,verb=verb)
                    if(rc < 0): 
                        print 'WWW no hpss data for: ',model,' dtg: ',dtg,' continue...'
                        return(None,None,None,None,None,None,None)
                    MF.dTimer("hsi get: %s"%(msspath))

                cmd="tar -zxvf %s"%(tarball)
                mf.runcmd(cmd,ropt)

                cmd="rm %s"%(tarball)
                mf.runcmd(cmd,ropt)

                ##  -- analysis -- overwrite the tau0 from the fc with analyses
                ##
                #msspathGsi="/BMC/fdr/%s/%s/%s/grib/ftp/7/0/81/0_259920_0/%s"%(yyyy,mm,dd,tarball)
                #cmd="/apps/hpss/hsi get %s ."%(msspathGsi)
                #mf.runcmd(cmd,ropt)

                #cmd="tar -zxvf %s"%(tarball)
                #mf.runcmd(cmd,ropt)

                #cmd="rm %s"%(tarball)
                #mf.runcmd(cmd,ropt)



            else:

                sdir='/public/data/fsl/fim/nat/grib1'


            mf.ChkDir(tdir,'mk')
            omodel='fim8'
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='public'
            if(onWjet and dormdata):
                cmd="rm %s/*"%(sdir)
                mf.runcmd(cmd,ropt)
                return(None,tdir,smask,ctlpath,source,None,None)



        elif(model == 'ecmn'):

            sdir=W2rawECHiRes
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            mf.ChkDir(tdir,'mk')
            smask="*%s_%s*"%(dtg[0:8],dtg[8:10])
            omodel='ecmn'
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='ldm'

        elif(model == 'ecm2'):

            sdir=EcNogapsCssFeed
            # self.gmask="ecens_DCD%s*"%(mmddhh) changed with ecmwf hres
            #            upgrade on 2016030812 at NCO smask="ecens_DCD%s*"%(mmddhh)
            smask="DCD%s*"%(mmddhh)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel='ecmo'
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            doRsyncWjetOnly=0
            source='wjet'

            if(onWjet and dormdata):
                cmd="rm -r %s"%(tdir)
                mf.runcmd(cmd,ropt)
                return(None,tdir,smask,ctlpath,source,None,None)

        elif(model == 'ecm4'):

            sdir=EcNogapsCssFeed
            smask="U1D%s*"%(mmddhh)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel='ecm4'
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            doRsyncWjetOnly=0
            source='wjet'

            if( (onWjet or onTenki) and dormdata):
                cmd="rm -r %s"%(tdir)
                mf.runcmd(cmd,ropt)
                return(None,tdir,smask,ctlpath,source,None,None)

        elif(model == 'gfsk'):

            sdir='/lfs2/projects/fim/whitaker/gfsenkf_t574/%s/control'%(dtg)
            smask="pgb_gfscntl_%s_fhr*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)

            ctlpath="%s/%s.%s.ctl"%(tdir,model,dtg)
            doRsyncWjetOnly=0
            source='gfsenkf'

            if(onWjet and dormdata):
                cmd="rm -r %s"%(tdir)
                mf.runcmd(cmd,ropt)
                return(None,tdir,smask,ctlpath,source,None,None)

        elif(model == 'ngp2'):
            sdir=EcNogapsCssFeed
            smask="nogaps_%s*.grib2"%(dtg) # changed to navgem on 20130905
            smask="navgem_%s*.grib2"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            doRsyncWjetOnly=0
            source='wjet'
            if(onWjet and dormdata):
                cmd="rm -r %s"%(tdir)
                mf.runcmd(cmd,ropt)
                return(None,tdir,smask,ctlpath,source,None,None)

        elif(model == 'ngpc'):
            sdir=self.CagipsSdirNgpc
            smask="US058GMET*GR1*.0058*%s*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'navg'):
            sdir=self.CagipsSdirNgpc
            smask="US058GMET*GR1*.0018*%s*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'ngpj'):
            sdir=self.CagipsSdirNgpj
            # -- nogaps
            smask="US058GMET*GR1*.0058*%s*"%(dtg)
            # -- 20130221 -- get both nogaps and navgem until 13 mar
            smask="US058GMET*GR1*%s*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'gfsc'):
            sdir=self.CagipsSdirGfsc
            smask="US058*GR1*%s*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'ukmc'):
            sdir=self.CagipsSdiruKmc
            smask="US058*GR1*%s*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'jmac'):
            sdir=self.CagipsSdirJmac
            smask="US058*GR1*%s*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'ohc'):

            sdir=self.CagipsSdirOhc
            smask="US058GOCN*GR1*%s*"%(dtg)

            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)

        elif(model == 'ocn'):

            sdir=self.CagipsSdirOcn

            smask="US058GOCN*GR1*%s*sea*"%(dtg)
            smask2="US058GOCN*GR1*%s*ice*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)


        elif(model == 'ww3'):

            sdir=self.CagipsSdirWw3
            smask="US058GOCN*GR1*%s*sig*"%(dtg)
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            source='cagips'
            smaskfinal="*%s*"%(dtg)


        elif(model == 'ukm2'):

            if(dormdata):
                tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),odtg)
                cmd="rm -i %s/*"%(tdir)
                mf.runcmd(cmd,ropt)
                print 'EEEEEEEEEEEE ending since we are killing the files...'
                sys.exit()

            # *************************** mf 20101129
            # mislabelled dtg from ukmw2 in /public/data/grids/ukmet
            # dtg <- odtg on return to keep this relabelling internal to DComNcepDirNRsync()
            # ***************************

            didthat=1 # turn off by setting to True

            if(idtg == '2010112700' or  # done
               idtg == '2010112706' or  # done
               idtg == '2010112712' or  # done
               idtg == '2010112718' or  # 2906 data ok...
               idtg == '2010112800' and # 2912 data ok...
               not(didthat)
               ):
                odtg=mf.dtginc(idtg,36)

            if(idtg != odtg):
                spath="/public/data/grids/ukmet/%s_meto.grib"%(idtg)
                # -- 2011040506 xxxxxxxxxxxxxxxxxxxxxxxx versions
                #
                spath="/public/data/grids/ukmet/%s_metox.grib"%(idtg)
                tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),odtg)
                tpath="%s/%s_meto.grib"%(tdir,odtg)

            sdir='/public/data/grids/ukmet'
            if(idtg == '2011091812'): idtg='2011091812'
            ###if(idtg == '2013082112'): idtg='2013082100'

            smask="%s*"%(idtg)

            if(idtg == '2011091200' or
               idtg == '2012082212' or
               idtg == '2012082306'
               ):
                smask="%sx_*"%(idtg)

            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),odtg)
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,odtg)
            doRsyncWjetOnly=0
            source='public.ukmo'



        elif(model == 'cmc2'):

            sdir=EcNogapsCssFeed
            sdir="%s/%s"%(sdir,dtg[0:8])
            smask="glb_%s_???"%(dtg[8:])
            tdir="%s/%s/%s"%(self.Nwp2DataBdir,self.Model2CenterModel(model),dtg)
            MF.ChkDir(tdir,'mk')
            omodel=model
            ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
            doRsyncWjetOnly=0
            source='wjet'
            if(onWjet and dormdata):
                cmd="rm -r %s"%(tdir)
                mf.runcmd(cmd,ropt)
                return(None,tdir,smask,ctlpath,source)

        elif(model == 'fimx'):

            sdir='/w21/dat/nwp2/rtfim/dat/FIMX'
            tdir='%s/%s'%(sdir,dtg)
            smask="*fim8.FIMX.f???.grb2"
            ctlfile="fim8.FIMX.grb2.ctl"
            ctlpath="%s/%s"%(tdir,ctlfile)
            source='rtfim'


        elif(model == 'fimxchem'):

            sdir='/w21/dat/nwp2/rtfim/dat/FIMXchem'
            tdir='%s/%s'%(sdir,dtg)
            smask="*fim8.FIMXchem.f???.grb2"
            ctlfile="fim8.FIMXchem.grb2.ctl"
            ctlpath="%s/%s"%(tdir,ctlfile)
            source='rtfimchem'


        else:
            print 'EEEEEEEE invalid model: ',model
            sys.exit()

        if(doRsyncWjetOnly == 0 and source != 'rtfim'):
            mf.ChkDir(tdir,'mk')

        # -- uuuuuuuuuuuuuuuuuuuuuuuuuuuuuu - ukm2 rsync
        #
        if(source == 'public.ukmo'):

            ukmfiles=glob.glob("%s/*%s*.grib"%(tdir,idtg))

            if(len(ukmfiles) > 0): ukmfile=ukmfiles[0]
            else:                  ukmfile='/dev/null'

            sizBefore=MF.GetPathSiz(ukmfile)
            if(verb): print 'ukmfile: BBBB ',ukmfile,sizBefore

            if(idtg != odtg):
                # 20110921 -- special case for bad file name in /public during a recovery
                if(idtg == '20110918012'):
                    spath="%s/%s_meto.grib"%(sdir,idtg)
                    tpath="%s/%s_meto.grib"%(tdir,odtg)
                    MF.ChkDir(tdir,'mk')
                cmd="cp %s %s"%(spath,tpath)

            elif(idtg == '2011091200'):
                spath="%s/%sx_meto.grib"%(sdir,idtg)
                tpath="%s/%s_meto.grib"%(tdir,odtg)
                MF.ChkDir(tdir,'mk')
                cmd="cp %s %s"%(spath,tpath)


            else:
                cmd="rsync -av %s/%s %s"%(sdir,smask,tdir)

            mf.runcmd(cmd,ropt)
            ukmfiles=glob.glob("%s/*%s*.grib"%(tdir,odtg))

            ukmfile='/dev/null'
            if(len(ukmfiles) > 0):   ukmfile=ukmfiles[0]

            sizAfter=MF.GetPathSiz(ukmfile)
            if(verb): print 'ukmfile: AAAA ',ukmfile,sizAfter

            deltaSiz=sizAfter-sizBefore
            if(verb): print 'dddd deltaSiz: ',deltaSiz

            # mf 20101129 - relab target dtg with out dtg (odtg)
            #
            dtg=odtg

        if(source == 'wjet'):
            if (onWjet):

                cmd="rsync --size-only -av %s/%s %s"%(sdir,smask,tdir)
                #
                # since we're rsync'ng from jeff's dir to w21 dir, set the sdir to tdir (local)
                # for setting the modelfiles
                #
                sdir=tdir
                mf.runcmd(cmd,ropt)
            else:
                sdir=tdir

        # -------------------------- cccccccccccccccccc cagips handling
        #
        if(source == 'cagips'):

            (omodel,grbtype,tautype,doLn)=self.Model2ModelProp(model)

            spaths=glob.glob("%s/%s"%(sdir,smask))
            if(smask2 != None):
                spaths=spaths+glob.glob("%s/%s"%(sdir,smask2))

            for spath in spaths:
                (dir,file)=os.path.split(spath)
                tt=file.split('_')
                tau=int(tt[2][0:3])
                taufile="%s.%s.f%03d.%s"%(model,dtg,tau,grbtype)
                tpath="%s/%s"%(tdir,taufile)

                if(MF.ChkPath(spath) and MF.GetPathSiz(spath) > 0):

                    pauseTime=0.2
                    time.sleep(pauseTime)
                    cmd1="cat %s >> %s"%(spath,tpath)
                    mf.runcmd(cmd1,ropt)

                    cmd2="rm -f %s"%(spath)
                    mf.runcmd(cmd2,ropt)


            smask="*.%s*%s"%(dtg,grbtype)


        # return dtg with correct dtg
        #
        return(sdir,tdir,smask,ctlpath,source,deltaSiz,dtg)


    def Model2ModelProp(self,model):

        omodel=model
        tautype=None
        doLn=1
        if(model == 'gfs2' or model == 'goes'): grbtype='grb2' 
        if(model == 'fim8'): grbtype='grb1'
        if(model == 'fimx'): grbtype='grb2'
        if(model == 'ecmn'): grbtype='grb2' ; tautype='wgrib'
        if(model == 'ecm2'): grbtype='grb1' ; tautype='wgrib' ; omodel='ecmo' ; doLn=1
        if(model == 'ecm4'): grbtype='grb1' ; tautype='wgrib' ; doLn=1
        if(model == 'gfsk'): grbtype='grb1' ; tautype='wgrib'
        if(model == 'ngp2'): grbtype='grb2' ; tautype='wgrib' 
        if(model == 'ngpc'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'navg'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'ngpj'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'gfsc'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'ukmc'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'jmac'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'ohc'):  grbtype='grb1' ; tautype='wgrib' 
        if(model == 'ocn'):  grbtype='grb1' ; tautype='wgrib' 
        if(model == 'ww3'):  grbtype='grb1' ; tautype='wgrib' 
        if(model == 'cmc2'): grbtype='grb1' ; tautype='wgrib' 
        if(model == 'ukm2'): grbtype='grb1' ; tautype='alltau'

        if(model == 'fv7e'): grbtype='grb2' ; tautype='wgrib'
        if(model == 'fv7g'): grbtype='grb2' ; tautype='wgrib'
        if(model == 'fv3e'): grbtype='grb2' ; tautype='wgrib'
        if(model == 'fv3g'): grbtype='grb2' ; tautype='wgrib'

        return(omodel,grbtype,tautype,doLn)


    def makeLocalfileLdm(self,modelfile,grbtype):

        if(grbtype == 'grb1'):
            cmd="wgrib %s"%(modelfile)
        elif(grbtype == 'grb2'):
            cmd="wgrib2 %s"%(modelfile)

        cards=os.popen(cmd).readlines()
        # -- if bad read return 99999
        #
        if(len(cards) == 0):
            ctau=99999
            return(ctau)

        ctau=None
        if(len(cards) > 0):
            card=cards[-1]
            tt=card.split(':')
            var=tt[3]
            lev=tt[4]
            if(len(lev.split()) == 2):
                lev=lev.split()[0]

            dtg=tt[2].split('=')[-1]
            tau=tt[5]
            ###VVV print 'ccc ',card,' tt ',tau,card
            if(tau == 'anl'):
                itau=0
            else:
                tt=tau.split()
                if(tt[1] == 'hour'):
                    tau=tt[0]
                    if(mf.find(tau,'-')):
                        #print 'rrrrrrrrrrrr range ',tau
                        tau=tau.split('-')[1]
                    itau=int(tau)
                else:
                    print 'WWW wgrib invalid time unit in modfile: ',modelfile,' tt: ',tt
                    sys.exit()
            ctau="%03d"%(itau)

        return(ctau)



    def Model2SymbolicLinks(self,modelfiles,dtg,model,tdir,source,ropt,override):

        (omodel,grbtype,tautype,doLn)=self.Model2ModelProp(model)

        localmodelfiles=[]

        if(grbtype == 'grb1'): wpext='wgrib1.txt'
        if(grbtype == 'grb2'): wpext='wgrib2.txt'

        if(override):
            localfilemask="%s/%s.%s.*.%s"%(tdir,omodel,dtg,grbtype)
            lf=glob.glob(localfilemask)
            for l in lf:
                os.unlink(l)

            localgmpmask="%s/%s.%s.*.%s"%(tdir,omodel,dtg,wpext)
            lf=glob.glob(localgmpmask)
            for l in lf:
                os.unlink(l)

        for modelfile in modelfiles:

            lm=len(modelfile)

            if(tautype == None):
                if(model == 'fimx'):
                    ctau=modelfile[lm-8:lm-5]
                else:
                    ctau=modelfile[lm-3:lm]
                (mdir,mfile)=os.path.split(modelfile)
                lmfile="%s.%s.f%s.%s"%(omodel,dtg,ctau,grbtype)
                localmodelfile="%s/%s"%(tdir,lmfile)

                if(not(os.path.exists(localmodelfile)) or override):
                    if(tdir == mdir):
                        cmd="(cd %s ; ln -s -f %s %s)"%(mdir,mfile,lmfile)
                    else:
                        cmd="ln -s -f %s %s"%(modelfile,localmodelfile)

                    mf.runcmd(cmd,ropt)
                localmodelfiles.append(localmodelfile)


            elif(tautype == 'alltau'):

                localmodelfile="%s/%s.%s.%s"%(tdir,omodel,dtg,grbtype)
                if(not(os.path.exists(localmodelfile)) or override):
                    cmd="ln -f -s %s %s"%(modelfile,localmodelfile)
                    print 'cmd: ',cmd
                    mf.runcmd(cmd,ropt)
                localmodelfiles.append(localmodelfile)


            elif(tautype == 'wgrib'):

                # -- wgrib ggggggggggggggggfsenkf
                #
                if(source == 'gfsenkf'):

                    (dir,file)=os.path.split(modelfile)
                    localmodelfile="%s/%s"%(tdir,file)

                    if(not(os.path.exists(localmodelfile)) or override):
                        cmd="ln -s -f %s %s"%(modelfile,localmodelfile)
                        mf.runcmd(cmd,ropt)

                        if(grbtype == 'grb1'):
                            cmd="wgrib %s"%(modelfile)
                        elif(grbtype == 'grb2'):
                            cmd="wgrib2 %s"%(modelfile)

                        cards=os.popen(cmd).readlines()
                        ctau=None
                        if(len(cards) > 0):
                            card=cards[-1]
                            tt=card.split(':')
                            var=tt[3]
                            lev=tt[4]
                            if(len(lev.split()) == 2):
                                lev=lev.split()[0]

                            tau=tt[-2]
                            if(tt[-2] == ''): tau=tt[-4]

                            if(tau == 'anl'):
                                itau=0
                            else:
                                tt=tau.split()
                                if(mf.find(tt[0],'hr')):
                                    tau=tt[0]
                                    tau=tau.replace('hr','')

                                    if(mf.find(tau,'-')):
                                        #print 'rrrrrrrrrrrr range ',tau
                                        tau=tau.split('-')[1]
                                    itau=int(tau)
                                else:
                                    print 'WWW wgrib invalid time unit in modfile: ',modelfile,' tt: ',tt
                                    sys.exit()
                            ctau="%03d"%(itau)
                            #print 'ddd ',dtg,itau,ctau


                        # -- local tau file
                        #

                        if(ctau != None):
                            localfile="%s/%s.%s.f%s.%s"%(tdir,model,dtg,ctau,grbtype)
                            if(doLn):
                                cmd="ln -s -f %s %s"%(modelfile,localfile)
                            else:
                                cmd="mv %s %s"%(modelfile,localfile)

                            mf.runcmd(cmd,ropt)

                # -- wgrib wwwwwwwwwwwwwwwwjet
                #
                elif(source == 'wjet'):

                    if(grbtype == 'grb1'):
                        cmd="wgrib -4yr -d 1 -o /dev/null %s"%(modelfile)
                    elif(grbtype == 'grb2'):
                        cmd="wgrib2 -d 1 %s"%(modelfile)

                    cards=os.popen(cmd).readlines()

                    if(len(cards) > 0):
                        card=cards[-1]
                        tt=card.split(':')
                        ntt=len(tt)
                        var=tt[3]
                        lev=tt[4]
                        if(len(lev.split()) == 2):
                            lev=lev.split()[0]

                        idtg=tt[2].split('=')[-1]
                        tau=tt[-2]
                        # -- 2019031912 -- ecmwf now has 'type=' fields...detect...
                        #
                        if(mf.find(tau,'type')): tau=tt[-3]

                        # -- for ensemble grib1
                        #
                        if(tau == ''): tau=tt[-4]

                        if(tau == 'anl'):
                            itau=0
                        else:
                            tt=tau.split()
                            if(tt[1] == 'hour' or tt[1] == 'fcst'):
                                tau=tt[0]
                                if(mf.find(tau,'-')):
                                    tau=tau.split('-')[1]
                                elif(mf.find(tau,'hr')):
                                    tau=tau[0:len(tau)-2]
                                itau=int(tau)
                            elif(tt[0] == 'valid'):
                                tau=tt[1]
                                if(mf.find(tau,'-')):
                                    tau=tau.split('-')[1]
                                if(mf.find(tau,'hr')):
                                    tau=tau[0:-2]
                                itau=int(tau)

                            else:
                                print 'WWW wgrib invalid time unit in modfile: ',modelfile,' tt: ',tt
                                sys.exit()
                        ctau="%03d"%(itau)

                        # -- check if dtg in gribfile = target dtg
                        #
                        if(idtg != dtg):
                            print
                            print '!!!!!'
                            print 'EEE(w2nwp2.Model2SymbolicLinks) - dtg in grib file: ',idtg,' NOT EQuAL to target dtg:',dtg
                            print '!!!!!'
                            print
                            sys.exit()
                        #
                        # local tau file
                        #


                        localfile="%s/%s.%s.f%s.%s"%(tdir,omodel,idtg,ctau,grbtype)

                        if(not(os.path.exists(localfile))):
                            (dir,mfile)=os.path.split(modelfile)
                            mf.ChangeDir(dir)
                            (ldir,lfile)=os.path.split(localfile)
                            if(doLn):
                                cmd="ln -s -f %s %s"%(mfile,lfile)
                            else:
                                cmd="mv %s %s"%(mfile,lfile)
                            mf.runcmd(cmd,ropt)


                # -- wgrib lllllllllllllllllllldm
                #
                elif(source == 'ldm'):

                    (dir,file)=os.path.split(modelfile)

                    if(os.path.exists(modelfile) or override):

                        # local tau file
                        #
                        ctau=self.makeLocalfileLdm(modelfile,grbtype)

                        if(ctau != None and ctau != 99999):
                            # -- cat 
                            localfile="%s/%s.%s.f%s.%s"%(tdir,model,dtg,ctau,grbtype)
                            cmd="cat %s >> %s"%(modelfile,localfile)
                            mf.runcmd(cmd,ropt)

                        if(ctau == 99999 or ctau != None):
                            cmd2="rm -v -f %s"%(modelfile)
                            mf.runcmd(cmd2,ropt)



                # -- non wjet, gfsenkf, ldm
                #
                elif(source != 'wjet'):

                    (dir,file)=os.path.split(modelfile)
                    localmodelfile="%s/%s"%(tdir,file)

                    if(not(os.path.exists(localmodelfile)) or override):
                        cmd="ln -s -f %s %s"%(modelfile,localmodelfile)
                        mf.runcmd(cmd,ropt)

                        if(grbtype == 'grb1'):
                            cmd="wgrib %s"%(modelfile)
                        elif(grbtype == 'grb2'):
                            cmd="wgrib2 %s"%(modelfile)

                        cards=os.popen(cmd).readlines()
                        ctau=None
                        if(len(cards) > 0):
                            card=cards[-1]
                            tt=card.split(':')
                            var=tt[3]
                            lev=tt[4]
                            if(len(lev.split()) == 2):
                                lev=lev.split()[0]

                            dtg=tt[2].split('=')[-1]
                            tau=tt[5]

                            if(tau == 'anl'):
                                itau=0
                            else:
                                tt=tau.split()
                                if(tt[1] == 'hour'):
                                    tau=tt[0]
                                    if(mf.find(tau,'-')):
                                        tau=tau.split('-')[1]
                                    itau=int(tau)
                                else:
                                    print 'WWW wgrib invalid time unit in modfile: ',modelfile,' tt: ',tt
                                    sys.exit()
                            ctau="%03d"%(itau)
                            #print 'ddd ',dtg,itau,ctau

                        # local tau file
                        #

                        if(ctau != None):
                            localfile="%s/%s.%s.f%s.%s"%(tdir,model,dtg,ctau,grbtype)
                            cmd="cat %s >> %s"%(modelfile,localfile)
                            mf.runcmd(cmd,ropt)


                mmask="%s/%s.%s.f*.%s"%(tdir,omodel,dtg,grbtype)
                localmodelfiles=glob.glob(mmask)


        return(localmodelfiles)




    def MakeEsrlDataInventory(self,localpaths,dtg,model,pyfile,incrontab,override=0):

        status={}

        if(incrontab):
            eventtype='nwp2.data.inv'
            areaopt='ALL'
            eventtag="START--- nwp2.data.inv  model: %s dtg: %s"%(model,dtg)
            self.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

        for dpath in localpaths:

            (dir,file)=os.path.split(dpath)
            (base,ext)=os.path.splitext(dpath)

            tt=file.split('.')
            tau=int(tt[len(tt)-2][1:])
            grbtype=tt[-1]

            try:
                age=MF.PathCreateTimeDtgdiff(dtg,dpath)
            except:
                age=None

            if(grbtype == 'grb1' or grbtype == 'grb'):
                xwgrib='wgrib'
                wpext='wgrib1.txt'
            elif(grbtype == 'grb2'):
                xwgrib='wgrib2'
                wpext='wgrib2.txt'
            else:
                xwgrib=None


            # special handling for ukmo data -- single file and always do wgribinv since it now comes in a stages...
            #
            invOverride=0
            if(model == 'ukm2'):
                hh=dtg[8:10]
                wgribpath="%s.%s"%(base,wpext)
                if(hh == '00' or hh == '12'):
                    tau=144
                else:
                    tau=60
                invOverride=1
            else:
                wgribpath="%s.%s"%(base,wpext)

            if((not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0) or override or invOverride) and (os.path.exists(dpath)) ):
                cmd="%s %s > %s"%(xwgrib,dpath,wgribpath)
                mf.runcmd(cmd)

            if(not(os.path.exists(dpath))):
                nf=0
            else:
                nf=len(open(wgribpath).readlines())

            status[tau]=(age,nf)

        if(incrontab):
            eventtag="EEEND--- nwp2.data.inv  model: %s dtg: %s"%(model,dtg)
            self.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

        return(status)


    def GetDataStatus(self,status,dtg,model,tdir):

        lastTau=-999
        latestTau=-999
        latestCompleteTau=-999
        earlyTau=-999
        gmplastdogribmap=-999
        gmplatestTau=-999
        gmplastTau=-999

        mask="%s/gribmap.status.*.txt"%(tdir)

        gmps=glob.glob(mask)
        gmps.sort()


        gmpAge=0.0
        if(len(gmps) >= 1):
            for gmpspath in gmps:
                age=MF.PathCreateTimeDtgdiff(dtg,gmpspath)
                if(age > gmpAge):
                    gmpAge=age
                    latestgmpPath=gmpspath

            (dir,file)=os.path.split(latestgmpPath)
            tt=file.split('.')

            gmplastdogribmap=int(tt[3])
            gmplatestTau=int(tt[4])
            gmplastTau=int(tt[5])

        itaus=status.keys()
        itaus.sort()

        ages={}
        for itau in itaus:
            ages[itau]=status[itau][0]


        oldest=-1e20
        youngest=+1e20

        for itau in itaus:
            if(ages[itau] < youngest):
                youngest=ages[itau]
                earlyTau=itau

            if(ages[itau] > oldest):
                oldest=ages[itau]
                latestTau=itau


        if(len(status) >= 1):
            lastTau=itaus[-1]
            latestCompleteTau=lastTau

        datataus=self.Model2DataTaus(model,dtg)

        ndt=len(datataus)
        for n in range(0,ndt):
            datatau=datataus[n]

            goit=0
            for itau in itaus:
                if(datatau == itau):
                    goit=1
                    latestCompleteTau=datatau

            if(goit == 0):  break


        rc=[lastTau,gmpAge,oldest,latestTau,youngest,earlyTau,gmplastdogribmap,gmplatestTau,gmplastTau,latestCompleteTau]

        return(rc)


    def GetTCstructStatus(self,dtg,model,realtime=0):

        # -- for now...
        rc=0
        return(rc)

        if(model == 'fimx'):
            return(1)

        yyyy=dtg[0:4]

        bdir=self.TcTcanalDatDir
        if(realtime):
            bdir=self.TcTcanalDatDirRT

        odir="%s/%s/%s"%(bdir,yyyy,dtg)

        trks=glob.glob("%s/trk/ngtrk.track.%s.%s.*.txt*"%(odir,model,dtg))
        ntrks=len(trks)
        rc=0
        if(ntrks > 0): rc=1
        if(model == 'ecm1'): rc=1

        # -- for now...
        rc=0

        return(rc)


    def GetTCtrkStatus(self,dtg,model,verb=0,override=0):

        # -- for now...
        rc=0
        return(rc)

        if(model == 'fimx'): return(1)
        try:
            rc=FR.TT.chkTrkStatus()
        except:
            rc=0

        # -- for now...
        rc=0
        return(rc)


    def GetTCfiltStatus(self,dtg,model,realtime=0):

        # -- for now...
        rc=0
        return(rc)

        dbdir=self.TcTcfiltWebDir
        invpath="%s/inv.tcfilt.txt"%(dbdir)
        try:
            cards=open(invpath).readlines()
        except:
            cards=[]

        if(len(cards) == 0):
            rc=0
            return(rc)

        rc=0
        nhash=0
        i=0
        nc=len(cards)
        for i in range(0,nc):

            card=cards[i]

            if(card[0:4] == 'hash'):
                nhash=nhash+1

                if(nhash == 3):
                    nmodels=int(card.split(' ')[2])
                    for j in range(0,nmodels):
                        mcard=cards[j+i+1]
                        tt=mcard.split()
                        hmodel=tt[0]
                        hmodeldtgs=tt[2:]
                        if(hmodel == model):
                            for hdtg in hmodeldtgs:
                                if(hdtg == dtg):
                                    rc=1
                                    return(rc)

        return(rc)





    def MakeEsrlDataCtl(self,dtg,ctlpath,model,pyfile,lastTau,latestTau,dogribmap,forceGribmap,override,incrontab,verb=0,ropt=''):

        if(incrontab):
            eventtype='nwp2.data.gribmap'
            areaopt='ALL'
            eventtag="START--- nwp2.data.gribmap  model: %s dtg: %s"%(model,dtg)
            self.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

        ntlast=int(lastTau)

        mdhh=dtg[4:10]+'00'

        gtime=mf.dtg2gtime(dtg)
        ctlpr=ctlmand=ctlhl=None

        (dir,file)=os.path.split(ctlpath)
        (base,ext)=os.path.splitext(file)

        if(model == 'gfs2'):
            ctlprfile="%s.pr%s"%(base,ext)
            ctlprpath="%s/%s"%(dir,ctlprfile)

        if(model == 'fim8'):
            ctlhlfile="%s.hl%s"%(base,ext)
            ctlhlpath="%s/%s"%(dir,ctlhlfile)

        if(model == 'gfs2' or model == 'fim8'):
            ctlmandfile="%s.mand%s"%(base,ext)
            ctlmandpath="%s/%s"%(dir,ctlmandfile)

    #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    #
    # ecmn -- nwp ecmwf
    #

        if(model == 'ecmn'):

            ctl="""dset ^ecmn.%s.f%%f3.grb2
index ^ecmn.%s.gmp
undef 9.999E+20
options template
title t.grb2
*  produced by g2ctl v0.0.4m
* griddef=1:45:(360 x 91):grid_template=0: lat-lon grid:(360 x 91) units 1e-06 input WE:SN output WE:SN res 48 lat 0.000000 to 90.000000 by 1.000000 lon 0.000000 to 359.000000 by 1.000000 #points=32760:winds(N/S)
dtype grib2
ydef  91 linear 0.0 1.0
xdef 360 linear 0.0 1.0
tdef  41 linear %s 6hr
* PROFILE hPa
zdef 8 levels 100000 92500 85000 70000 50000 40000 30000 25000
options pascals
vars 13
pr     0,  1,0   0,1,8 ** surface Total Precipitation [kg/m^2]
tds    0,  1,0   0,0,6 ** surface Dew Point Temperature [K]
zg     8,100     0,3,5 ** (1000 925 850 700 500 400 300 250) Geopotential Height [gpm]
psl    0,  1,0   0,3,1 ** surface Pressure Reduced to MSL [Pa]
hur    8,100     0,1,1 ** (1000 925 850 700 500 400 300 250) Relative Humidity [%%]
tasmax 0,  1,0   0,0,4 ** surface Maximum Temperature [K]
tasman 0,  1,0   0,0,5 ** surface Minimum Temperature [K]
tas    0,  1,0   0,0,0 ** surface Temperature [K]
ta     8,100     0,0,0 ** (1000 925 850 700 500 400 300 250) Temperature [K]
uas    0,  1,0   0,2,2 ** surface U-Component of Wind [m/s]
ua     8,100     0,2,2 ** (1000 925 850 700 500 400 300 250) U-Component of Wind [m/s]
vas    0,  1,0   0,2,3 ** surface V-Component of Wind [m/s]
va     8,100     0,2,3 ** (1000 925 850 700 500 400 300 250) V-Component of Wind [m/s]
ENDVARS"""%(dtg,dtg,gtime)
            xgribmap='gribmap'

    #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    #
    # ecm2 -> ecmo
    #
        elif(model == 'ecm2'):

            ctl="""dset ^ecmo.%s.f%%f3.grb1
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
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
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
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars"""%(dtg,dtg,gtime)

            xgribmap='gribmap'

        elif(model == 'ecm4'):

            ctl="""dset ^ecm4.%s.f%%f3.grb1
index ^ecm4.%s.gmp
undef 9.999E+20
title ecm4 0.25deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25
tdef   41 linear %s 6hr
zdef   10 levels 1000 925 850 700 600 500 400 300 250 200
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       10 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      10 157,100,0 ** Relative humidity %%
ta       10 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       10 131,100,0 ** U-velocity m s**-1
va       10 132,100,0 ** V-velocity m s**-1
endvars"""%(dtg,dtg,gtime)

            xgribmap='gribmap'


        elif(model == 'gfsk'):


            ctl="""dset ^gfsk.%s.f%%f3.grb1
index ^gfsk.%s.gmp1
undef 9.999E+20
title /lfs2/projects/fim/whitaker/gfsenkf_t574/2011053000/control/pgb_gfscntl_2011053000_fhr06
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
tdef  29 linear %s 6hr
zdef 42 levels
1000 975 950 925 900 875 850 825 800 775 750 725 700 675 650 625 600 575 550 525 500 475 450 425 400 375 350 325 300 275 250 225 200 175 150 125 100 70 50 30 20 10 
vars 31
vrta      42  41,100,0   ** Absolute vorticity [/s]
prc        0  63,  1,0   ** Convective precipitation [kg/m^2]
pr         0  61,  1,0   ** Total precipitation [kg/m^2]
cape       0 157,  1,0   ** Convective Avail. Pot. Energy [J/kg]
cins       0 156,  1,0   ** Convective inhibition [J/kg]
clw       42 153,100,0   ** Cloud water [kg/kg]
clwt       0  76,200,0   ** Cloud water [kg/m^2]
zgs        0   7,  1,0   ** Geopotential height [gpm]
zg        42   7,100,0   ** Geopotential height [gpm]
sic        0  91,  1,0   ** Ice concentration (ice=1;no ice=0) [fraction]
lsmask     0  81,  1,0   ** Land cover (land=1;sea=0) [fraction]
o3        42 154,100,0   ** Ozone mixing ratio [kg/kg]
ps         0   1,  1,0   ** Pressure [Pa]
psl        0   2,102,0   ** Pressure reduced to MSL [Pa]
prw        0  54,200,0   ** Precipitable water [kg/m^2]
hur       34  52,100,0   ** Relative humidity [%%]
hurs       0  52,105,2   ** Relative humidity [%%]
mrsot      0 144,112,10  ** Volumetric soil moisture [fraction]
mrs        3 144,112,0   ** Volumetric soil moisture [fraction]
tas        0  11,  1,0   ** Temp. [K]
ta        42  11,100,0   ** Temp. [K]
tas        0  11,105,2   ** Temp. [K]
tsoils     0  11,112,10  ** Temp. [K]
tsoil      3  11,112,0   ** Temp. [K]
o3t        0  10,200,0   ** Total ozone [Dobson]
ua        42  33,100,0   ** u wind [m/s]
uas        0  33,105,10  ** u wind [m/s]
va        42  34,100,0   ** v wind [m/s]
vas        0  34,105,10  ** v wind [m/s]
wap       42  39,100,0   ** Pressure vertical velocity [Pa/s]
snow       0  65,  1,0    ** Accum. snow [kg/m^2]
endvars"""%(dtg,dtg,gtime)


            xgribmap='gribmap'



    #uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
    #
    # ukm2 
    #

        elif(model == 'ukm2'):

            grid="""xdef 640 linear   0.0 0.5625
ydef 481 linear -90.0 0.375"""

            # grid res change...2010030912...
            #
            if(mf.dtgdiff('2010030912',dtg) >= 0):
                grid="""xdef 1024 linear   0.0  0.3515625
 ydef 769 linear -90.0 0.234375"""

            if(mf.dtgdiff('2014072200',dtg) >= 0):
                grid="""xdef 1536 linear 0.0 00.23422251
ydef 1153 linear -90.0 0.156114"""

            ctl="""dset ^%s.%s.grb1
index ^%s.%s.gmp1
undef 9.999E+20
title 2009051200_meto.grib
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
%s
zdef   7 levels 1000 925 850 700 500 300 200 
tdef  25 linear %s 6hr
vars 11
tas    0  11,  1,0  ** sfc Temp. [K]
pr     0  61,  1,0  ** Total precipitation [kg/m^2]
prc    0 140,  1,0  ** Categorical rain [yes=1;no=0]
zg     7   7,100,0  ** Geopotential height [gpm]
psl    0   2,102,0  ** Pressure reduced to MSL [Pa]
hur    7  52,100,0  ** Relative humidity [%%]
ta     7  11,100,0  ** Temp. [K]
uas    0  33,  1,0  ** u wind [m/s]
ua     7  33,100,0  ** u wind [m/s]
vas    0  34,  1,0  ** v wind [m/s]
va     7  34,100,0  ** v wind [m/s]
endvars"""%(model,dtg,model,dtg,grid,gtime)

            xgribmap='gribmap'

    #gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
    #
    # gfs
    #
        elif(model == 'gfs2'):


            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^gfs2.%s.f%%f3.grb2
index ^gfs2.%s.gmp2
undef 1e+20
title gfs2.2007100112.f006.grb2
options template pascals
dtype grib2
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 26 levels 100000 97500 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000
tdef %d linear %s %dhr
vars 24
ts         0,  1  ,0   0,  0,  0     ** surface Temperature [K]
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3     ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
zg        26,100       0,  3,  5     ** (1000 975 950 925 900.. 70 50 30 20 10) Geopotential Height [gpm]
psl        0,101,  0   0,  3,  1     ** mean sea level Pressure Reduced to MSL [Pa]
hur       21,100       0,  1,  1     ** (1000 975 950 925 900.. 300 250 200 150 100) Relative Humidity [%%]
clt        0,200,  0   0,  6,  1,  0 ** entire atmosphere (considered as a single layer) Total Cloud Cover [%%]
cll        0,214,  0   0,  6,  1,  0 ** low cloud layer Total Cloud Cover [%%]
clm        0,224,  0   0,  6,  1,  0 ** middle cloud layer Total Cloud Cover [%%]
clh        0,234,  0   0,  6,  1,  0 ** high cloud layer Total Cloud Cover [%%]
cltc       0,244,  0   0,  6,  1     ** convective cloud layer Total Cloud Cover [%%]
tasmx      0,103,  2   0,  0,  4     ** 2 m above ground Maximum Temperature [K]
tasmn      0,103,  2   0,  0,  5     ** 2 m above ground Minimum Temperature [K]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
ua        26,100       0,  2,  2     ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10   0,  2,  2     ** 10 m above ground U-Component of Wind [m/s]
rlut       0,  8,  0   0,  5,193,  0 ** top of atmosphere Upward Long-Wave Rad. Flux [W/m^2]
va        26,100       0,  2,  3     ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
ta        26,100       0,  0,  0     ** (1000 975 950 925 900.. 70 50 30 20 10) Temperature [K]
vas        0,103,10    0,  2,  3     ** 10 m above ground V-Component of Wind [m/s]
wap       21,100       0,  2,  8     ** (1000 975 950 925 900.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
endvars"""%(dtg,dtg,nt,gtime,dtctl)


            dtctlpr=3
            ntpr=ntlast/dtctlpr + 1
            ctlpr="""dset ^gfs2.%s.f%%f3.grb2
index ^gfs2.%s.pr.gmp2
undef 1e+20
title gfs2.2007100112.f006.pr.grb2
options template
dtype grib2
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5  
zdef 10 levels
1000 925 850 700 500 300 250 200 150 100 
tdef %d linear %s %dhr
vars 4
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
endvars"""%(dtg,dtg,ntpr,gtime,dtctlpr)


            dtctlmand=6
            ntmand=ntlast/dtctlmand + 1
            ctlmand="""dset ^gfs2.%s.f%%f3.grb2
index ^gfs2.%s.mand.gmp2
undef 1e+20
title gfs2.2007100112.f006.grb2
options template pascals
dtype grib2
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 16 levels 100000 92500 85000 70000  50000 40000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000
tdef %d linear %s %dhr
vars 25
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3     ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
zg        16,100       0,  3,  5     ** (1000 975 950 925 900.. 70 50 30 20 10) Geopotential Height [gpm]
psl        0,101,  0   0,  3,  1     ** mean sea level Pressure Reduced to MSL [Pa]
hur       16,100       0,  1,  1     ** (1000 975 950 925 900.. 300 250 200 150 100) Relative Humidity [%%]
clt        0,200,  0   0,  6,  1,  0 ** entire atmosphere (considered as a single layer) Total Cloud Cover [%%]
cll        0,214,  0   0,  6,  1,  0 ** low cloud layer Total Cloud Cover [%%]
clm        0,224,  0   0,  6,  1,  0 ** middle cloud layer Total Cloud Cover [%%]
clh        0,234,  0   0,  6,  1,  0 ** high cloud layer Total Cloud Cover [%%]
cltc       0,244,  0   0,  6,  1     ** convective cloud layer Total Cloud Cover [%%]
tasmx      0,103,  2   0,  0,  4     ** 2 m above ground Maximum Temperature [K]
tasmn      0,103,  2   0,  0,  5     ** 2 m above ground Minimum Temperature [K]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
ua        16,100       0,  2,  2     ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10   0,  2,  2     ** 10 m above ground U-Component of Wind [m/s]
rlut       0,  8,  0   0,  5,193,  0 ** top of atmosphere Upward Long-Wave Rad. Flux [W/m^2]
va        16,100       0,  2,  3     ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
ta        16,100       0,  0,  0     ** (1000 975 950 925 900.. 70 50 30 20 10) Temperature [K]
vas        0,103,10    0,  2,  3     ** 10 m above ground V-Component of Wind [m/s]
wap       16,100       0,  2,  8     ** (1000 975 950 925 900.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
ts         0,1  ,0     0,  0,  0     ** surface Temperature [K]
sic        0,1  ,0    10,  2,  0     ** surface Ice Cover [Proportion]
endvars"""%(dtg,dtg,ntmand,gtime,dtctlmand)


            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN gfs2: ',ntlast,nt,ntpr,ntmand

    #nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    #
    # nogaps
    #
        elif(model == 'ngp2'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^ngp2.%s.f%%f3.grb2
index ^ngp2.%s.gmp2
undef 1e+20
title ngp2.2007100112.f006.grb2
options template pascals
dtype grib2
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
*RH goes 1000, 950, 900... 300
*zg,ua,va,ta goes to 1000,925,850,700...100,70,50,10 on tau0 only
zdef 23 levels 100000 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000 5000 1000
tdef %d linear %s %dhr
* PROFILE hPa
vars 23
avrt5   0,100,50000   0,2,10    ** 500 mb none Absolute Vorticity [1/s]
v25519m 0,103,19    255,255,255 ** 19 m above ground desc [unit]
prc     0,  1,0       0,1,10,1  ** surface acc Convective Precipitation [kg/m^2]
pr      0,  1,0       0,1,8,1   ** surface acc Total Precipitation [kg/m^2]
ps      0,  1,0       0,3,0     ** surface Pressure [Pa]
pmwl    0,  6,0       0,3,0     ** max wind Pressure [Pa]
ptrop   0,  7,0       0,3,0     ** tropopause Pressure [Pa]
ttrop   0,  7,0       0,0,0     ** tropopause Temperature [K]
umwl    0,  6,0       0,2,2     ** max wind U-Component of Wind [m/s]
vmwl    0,  6,0       0,2,3     ** max wind V-Component of Wind [m/s]
tmwl    0,  6,0       0,0,0     ** max wind Temperature [K]
zgmwl   0,  6,0       0,3,5     ** max wind Geopotential Height [gpm]
tas     0,103,2       0,0,0     ** 2 m above ground none Temperature [K]
psl     0,101,0       0,3,1     ** mean sea level none Pressure Reduced to MSL [Pa]
uas     0,103,10      0,2,2     ** 10 m above ground none U-Component of Wind [m/s]
vas     0,103,10      0,2,3     ** 10 m above ground none V-Component of Wind [m/s]
zg     23,100         0,3,5     ** (1000 925 850 700 500.. 300 250 200 150 100) none Geopotential Height [gpm]
hur    23,100         0,1,1     ** (1000 950 900 850 800.. 500 450 400 350 300) none Relative Humidity [%%]
ta     23,100         0,0,0     ** (1000 850 700 500 400.. 300 250 200 150 100) none Temperature [K]
ua     23,100         0,2,2     ** (1000 925 850 700 500.. 300 250 200 150 100) none U-Component of Wind [m/s]
va     23,100         0,2,3     ** (1000 925 850 700 500.. 300 250 200 150 100) none V-Component of Wind [m/s]
wap    23,100         0,2,8     ** (1000 850 700 500 400.. 300 250 200 150 100) none Vertical Velocity (Pressure) [Pa/s]
v255   23,100       255,255,255 ** (1000 925 850 700 500.. 300 250 200 150 100) desc [unit]
endvars
###--- pr is mm/6h *4 = mm/d
"""%(dtg,dtg,nt,gtime,dtctl)



            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN ngp2: ',ntlast,nt,ntpr,ntmand

        elif(model == 'ngpc'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^ngpc.%s.f%%f3.grb1
index ^ngpc.%s.gmp1
undef 1e+20
title ngpc.2007100112.f006.grb2
options template
dtype grib 255
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
zdef 12 levels
1000 925 850 700 500 400 300 250 200 150 100 50 
tdef %d linear %s %dhr
* PROFILE hPa
vars 13
prc       0  63,  1,  0 ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0 ** Total precipitation [kg/m^2]
zg       12   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0 ** Pressure reduced to MSL [Pa]
hur      12  52,100,  0 ** Relative humidity [%%]
tasmx     0  15,105,  2 ** Max. temp. [K]
tasmn     0  16,105,  2 ** Min. temp. [K]
ta       12  11,100,  0 ** Temp. [K]
tas       0  11,105,  2 ** Temp. [K]
ua       12  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       12  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
endvars
###--- pr is mm/6h *4 = mm/d
"""%(dtg,dtg,nt,gtime,dtctl)

            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN ngpc: ',ntlast,nt,ntpr,ntmand

        elif(model == 'navg'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^navg.%s.f%%f3.grb1
index ^navg.%s.gmp1
undef 1e+20
title navg.2007100112.f006.grb2
options template
dtype grib 255
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
zdef 12 levels
1000 925 850 700 500 400 300 250 200 150 100 50 
tdef %d linear %s %dhr
* PROFILE hPa
vars 13
prc       0  63,  1,  0 ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0 ** Total precipitation [kg/m^2]
zg       12   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0 ** Pressure reduced to MSL [Pa]
hur      12  52,100,  0 ** Relative humidity [%%]
tasmx     0  15,105,  2 ** Max. temp. [K]
tasmn     0  16,105,  2 ** Min. temp. [K]
ta       12  11,100,  0 ** Temp. [K]
tas       0  11,105,  2 ** Temp. [K]
ua       12  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       12  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
endvars
###--- pr is mm/6h *4 = mm/d
"""%(dtg,dtg,nt,gtime,dtctl)

            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN navg: ',ntlast,nt,ntpr,ntmand

        elif(model == 'ngpj'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^ngpj.%s.f%%f3.grb1
index ^ngpj.%s.gmp1
undef 1e+20
title ngpj.2007100112.f006.grb2
options template
dtype grib 255
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
zdef 12 levels
1000 925 850 700 500 400 300 250 200 150 100 50 
tdef %d linear %s %dhr
* PROFILE hPa
vars 13
prc       0  63,  1,  0 ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0 ** Total precipitation [kg/m^2]
zg       12   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0 ** Pressure reduced to MSL [Pa]
hur      12  52,100,  0 ** Relative humidity [%%]
tasmx     0  15,105,  2 ** Max. temp. [K]
tasmn     0  16,105,  2 ** Min. temp. [K]
ta       12  11,100,  0 ** Temp. [K]
tas       0  11,105,  2 ** Temp. [K]
ua       12  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       12  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
endvars
###--- pr is mm/6h *4 = mm/d
"""%(dtg,dtg,nt,gtime,dtctl)

            xgribmap='gribmap'
            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN ngpj: ',ntlast,nt,ntpr,ntmand


        elif(model == 'gfsc'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^gfsc.%s.f%%f3.grb1
index ^gfsc.%s.gmp1
undef 1e+20
title gfsc.2007100112.f006.grb1
options template 
dtype grib 255
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef 11 levels 1000 925 850 750 500 400 300 250 200 150 100 
tdef 1 linear 12Z05oct2010 1mo
tdef %d linear %s %dhr
vars 13
sst      0  80,  1,0   ** Water temp. [K]
psl      0   2,102,0   ** Pressure reduced to MSL [Pa]
prc      0  63,  1,0   ** Convective precipitation [kg/m^2]
pr       0  61,  1,0   ** Total precipitation [kg/m^2]
prw      0  54,200,0   ** Precipitable water [kg/m^2]
clt      0  71,200,0   ** Total cloud cover [%%]
uas      0  33,105,10  ** u sfc wind [m/s]
vas      0  34,105,10  ** v sfc wind [m/s]
zg      11   7,100,0   ** Geopotential height [gpm]
hur     11  52,100,0   ** Relative humidity [%%]
ta      11  11,100,0   ** Temp. [K]
ua      11  33,100,0   ** u wind [m/s]
va      11  34,100,0   ** v wind [m/s]
endvars"""%(dtg,dtg,nt,gtime,dtctl)


            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN gfsc: ',ntlast,nt,ntpr,ntmand


        #uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
        # ukmc
        #
        elif(model == 'ukmc'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^ukmc.%s.f%%f3.grb1
index ^ukmc.%s.gmp1
undef 1e+20
title gfsc.2007100112.f006.grb1
options template 
dtype grib 255
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100 
tdef %d linear %s %dhr
vars 9
psl      0   2,102,0   ** Pressure reduced to MSL [Pa]
pr       0  61,  1,0   ** Total precipitation [kg/m^2]
uas      0  33,  1,0   ** u sfc wind [m/s]
vas      0  34,  1,0   ** v sfc wind [m/s]
zg      11   7,100,0   ** Geopotential height [gpm]
hur     11  52,100,0   ** Relative humidity [%%]
ta      11  11,100,0   ** Temp. [K]
ua      11  33,100,0   ** u wind [m/s]
va      11  34,100,0   ** v wind [m/s]
endvars"""%(dtg,dtg,nt,gtime,dtctl)


            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN gfsc: ',ntlast,nt,ntpr,ntmand

        #JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ
        # jmac
        #
        elif(model == 'jmac'):

            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^jmac.%s.f%%f3.grb1
index ^jmac.%s.gmp1
undef 1e+20
title gfsc.2007100112.f006.grb1
options template 
dtype grib 255
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef 11 levels 1000 925 850 750 500 400 300 250 200 150 100 
tdef %d linear %s %dhr
vars 9
psl      0   2,102,0   ** Pressure reduced to MSL [Pa]
pr       0  61,  1,0   ** Total precipitation [kg/m^2]
uas      0  33,105,10  ** u sfc wind [m/s]
vas      0  34,105,10  ** v sfc wind [m/s]
zg      11   7,100,0   ** Geopotential height [gpm]
hur     11  52,100,0   ** Relative humidity [%%]
ta      11  11,100,0   ** Temp. [K]
ua      11  33,100,0   ** u wind [m/s]
va      11  34,100,0   ** v wind [m/s]
endvars"""%(dtg,dtg,nt,gtime,dtctl)


            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN gfsc: ',ntlast,nt,ntpr,ntmand


        elif(model == 'ohc'):

            dtctl=6
            nt=1
            ctl="""dset ^ohc.%s.f%%f3.grb1
index ^ohc.%s.gmp1
undef 1e+20
title ohc.2007100112.f006.grb2
options template
dtype grib 255
ydef  350 linear -30.000000 0.2
xdef 1576 linear 35.000000 0.200000
zdef    1 levels 0
tdef   %d linear %s %dhr
vars 3
ohc       0 167,  1,  0  ** OHC [kJ/cm^2]
d26c      0 242,  4, 26  ** depth of 26C ocean isotherm [m]
sst       0  80,  1,  0  ** SST [K]
endvars
"""%(dtg,dtg,nt,gtime,dtctl)

            xgribmap='gribmap'

            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN ohc: '

        elif(model == 'ocn'):

            dtctl=6
            nt=1
            ctl="""dset ^ocn.%s.f%%f3.grb1
index ^ocn.%s.gmp1
undef 1e+20
title ocn.2007100112.f006.grb2
options template
dtype grib 255
ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25
zdef    1 levels 0
tdef   %d linear %s %dhr
vars 2
sst       0 80,  1  ,0  ** SST [K]
sic       0 91,  1  ,0  ** SIC [fraction]
endvars
"""%(dtg,dtg,nt,gtime,dtctl)

            xgribmap='gribmap'

            if(verb): print 'OOOOOOOOOOOOOOOOOOOOOOOOOOOO ocn: '


        elif(model == 'ww3'):

            dtctl=6
            nt=31

            ctl="""dset ^ww3.%s.f%%f3.grb1
index ^ww3.%s.gmp1
undef 1e+20
title ww3.2007100112.f006.grb2
options template
dtype grib 255
xdef 1440 linear   0.0 0.25
ydef  721 linear -90.0 0.25
zdef    1 levels 0
tdef   %d linear %s %dhr
vars 1
wvzs      0 100,  1  ,0  ** Sig height of wind waves and swell [m]
endvars
"""%(dtg,dtg,nt,gtime,dtctl)

            xgribmap='gribmap'

            if(verb): print 'OOOOOOOOOOOOOOOOOOOOOOOOOOOO ocn: '




    #cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    #
    # cmc
    #
        elif(model == 'cmc2'):

            # 2012020812 -- changed coding of sfc fields
            dtctl=6
            nt=ntlast/dtctl + 1
            ctl="""dset ^glb_%s_%%f3.grb1
index ^cmc2.%s.gmp
undef 9.999E+20
title cmc2 1deg deterministic run
options template
dtype grib 255
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
tdef %d linear %s %dhr
zdef 7 levels 1000 925 850 700 500 250 200 
vars 11
avt    6  41,100,0      ** Absolute vorticity [/s]
pr     0  61,  1,0      ** Total precipitation [kg/m^2]
zg     6   7,100,0      ** Geopotential height [gpm]
psl    0   2,102,0      ** Pressure reduced to MSL [Pa]
hur    6  52,100,0      ** Relative humidity [%%]
ta     6  11,100,0      ** Temp. [K]
tas    0  11,105,2     ** Temp. [K]
ua     7  33,100,0      ** u wind [m/s]
uas    0  33,105,10     ** u wind [m/s]
va     7  34,100,0      ** v wind [m/s]
vas    0  34,105,10     ** v wind [m/s]
endvars"""%(dtg[8:],dtg,nt,gtime,dtctl)
            xgribmap='gribmap'


    #ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    # 
    # fim8 -> rtfim
    #

        elif(model == 'fim8'):

            dtctl=6
            nt=ntlast/dtctl + 1

            ctl="""dset ^fim8.%s.f%%f3.grb1
index ^fim8.%s.gmp1
undef 1e+20
title fim8.2007100112.f006.grb1
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 40 levels
1000 975 950 925 900 875 850 825 800 775 750 725 700 675 650 625 600 575 550 525 500 475 450 425 400 375 350 325 300 275 250 225 200 175 150 125 100 75 50 25
tdef %d linear %s %dhr
vars 21
prc      0  63,  1,1  ** Convective precipitation [kg/m^2]
pr       0  61,  1,1  ** Total precipitation [kg/m^2]
ustar    0 253,  1,1  ** Friction velocity [m/s]
zg      40   7,100,0  ** Geopotential height [gpm]
zg1      0   7,  2,1  ** Geopotential height [gpm]
zg2      0   7,  3,1  ** Geopotential height [gpm]
hfls     0 121,  1,1  ** Latent heat flux [W/m^2]
psl      0 129,102,1  ** Mean sea level pressure (MAPS) [Pa]
prl      0  62,  1,1  ** Large scale precipitation [kg/m^2]
rlns     0 112,  1,1  ** Net long wave (surface) [W/m^2]
rsns     0 111,  1,1  ** Net short wave (surface) [W/m^2]
prw      0  54,  1,1  ** Precipitable water [kg/m^2]
hur     40  52,100,0  ** Relative humidity [%%]
hfss     0 122,  1,1  ** Sensible heat flux [W/m^2]
ta1      0  11,  1,1  ** Temp. [K]
ta      40  11,100,0  ** Temp. [K]
ua      40  33,100,0  ** u wind [m/s]
va      40  34,100,0  ** v wind [m/s]
uas      0  33,109,1  ** u wind [m/s]
vas      0  34,109,1  ** v wind [m/s]
sno      0  65,  1,1  ** Accum. snow [kg/m^2]
endvars"""%(dtg,dtg,nt,gtime,dtctl)


            dtctlhl=6
            nthl=ntlast/dtctlhl + 1

            ctlhl="""dset ^fim8.%s.f%%f3.grb1
index ^fim8.%s.hl.gmp1
undef 1e+20
title fim8.2007100112.f006.grb1
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef  65 linear  1 1
tdef %d linear %s %dhr
vars 22
prc      0  63   1,1  ** Convective precipitation [kg/m^2]
pr       0  61,  1,1  ** Total precipitation [kg/m^2]
tdd     64  17,109,0  ** Dew point temp. [K]
ustar    0 253,  1,1  ** Friction velocity [m/s]
zg      65   7,109,0  ** Geopotential height [gpm]
zg1      0   7,  2,1  ** Geopotential height [gpm]
zg2      0   7,  3,1  ** Geopotential height [gpm]
hfls     0 121,  1,1  ** Latent heat flux [W/m^2]
psl      0 129,102,1  ** Mean sea level pressure (MAPS) [Pa]
prl      0  62,  1,1  ** Large scale precipitation [kg/m^2]
rlns     0 112,  1,1  ** Net long wave (surface) [W/m^2]
rsns     0 111,  1,1  ** Net short wave (surface) [W/m^2]
pl      65   1,109,0  ** Pressure [Pa]
prw      0  54,  1,1  ** Precipitable water [kg/m^2]
hur     64  52,109,0  ** Relative humidity [%%]
hfss     0 122,  1,1  ** Sensible heat flux [W/m^2]
ta1      0  11,  1,1  ** Temp. [K]
ta      64  11,109,0  ** Temp. [K]
ua      64  33,109,0  ** u wind [m/s]
va      64  34,109,0  ** v wind [m/s]
wap     64  39,109,0  ** Pressure vertical velocity [Pa/s]
psno     0  65,  1,1  ** Accum. snow [kg/m^2]
endvars"""%(dtg,dtg,nthl,gtime,dtctlhl)


            dtctlmand=6
            ntmand=ntlast/dtctlmand + 1
            ctlmand="""dset ^fim8.%s.f%%f3.grb1
index ^fim8.%s.mand.gmp1
undef 1e+20
title fim8.2007100112.f006.grb1
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef 16 levels 1000 925 850 700  500 400 300 250 200 150 100 70 50 30 20 10
tdef %d linear %s %dhr
vars 21
prc      0  63,  1,1  ** Convective precipitation [kg/m^2]
pr       0  61,  1,1  ** Total precipitation [kg/m^2]
ustar    0 253,  1,1  ** Friction velocity [m/s]
zg      16  7,100,0  ** Geopotential height [gpm]
zg1      0   7,  2,1  ** Geopotential height [gpm]
zg2      0   7,  3,1  ** Geopotential height [gpm]
hfls     0 121,  1,1  ** Latent heat flux [W/m^2]
psl      0 129,102,1  ** Mean sea level pressure (MAPS) [Pa]
prl      0  62,  1,1  ** Large scale precipitation [kg/m^2]
rlns     0 112,  1,1  ** Net long wave (surface) [W/m^2]
rsns     0 111,  1,1  ** Net short wave (surface) [W/m^2]
prw      0  54,  1,1  ** Precipitable water [kg/m^2]
hur     16 52,100,0  ** Relative humidity [%%]
hfss     0 122,  1,1  ** Sensible heat flux [W/m^2]
ta1      0  11,  1,1  ** Temp. [K]
ta      16  11,100,0  ** Temp. [K]
ua      16  33,100,0  ** u wind [m/s]
va      16  34,100,0  ** v wind [m/s]
uas      0  33,109,1  ** u wind [m/s]
vas      0  34,109,1  ** v wind [m/s]
sno      0  65,  1,1  ** Accum. snow [kg/m^2]
endvars"""%(dtg,dtg,ntmand,gtime,dtctlmand)


            xgribmap='gribmap'
            if(verb): print 'NNNNNNNNNNNNNNNNNNNNNN fim8: ',ntlast,nt,nthl,ntmand

        elif(model == 'fimx'):

            localdir='/w21/dat/nwp2/rtfim/dat/FIMX/%s'%(dtg)
            dmask="*fim8.FIMX.f???.grb2"
            ctlfile="fim8.FIMX.grb2.ctl"
            ctlpath="%s/%s"%(localdir,ctlfile)

            try:
                ctl=os.open(ctlpath).readlines()
            except:
                ctl=None

            xgribmap='gribmap'



        else:
            print 'EEE invalid model:',model
            sys.exit()


        if(model != 'fimx'):
            mf.WriteCtl(ctl,ctlpath)

        if(ctlpr != None and doPrCtl):
            mf.WriteCtl(ctlpr,ctlprpath)

        if(ctlhl != None and doHlCtl):
            mf.WriteCtl(ctlhl,ctlhlpath)

        if(ctlmand != None and doMandCtl):
            mf.WriteCtl(ctlmand,ctlmandpath)


        curdtgms=mf.dtg('dtg_ms')
        gribmapStatusFile="%s/gribmap.status.%s.%d.%03d.%03d.txt"%(dir,curdtgms,dogribmap,latestTau,lastTau)

        gribmapStatusFileMaskAll="%s/gribmap.status.*.*.txt"%(dir)
        gribmapStatusFileMaskLast="%s/gribmap.status.*.%03d.*.txt"%(dir,lastTau)

        nfall=len(glob.glob(gribmapStatusFileMaskAll))
        nflast=len(glob.glob(gribmapStatusFileMaskLast))


        if(nflast and not(forceGribmap)): dogribmap=0

        if(override): dogribmap=2


        if(dogribmap >=1):
            gmapopt='-u'
            if(nfall == 0):
                gmapopt='-q'
                gmapopt=''
            else:
                gmapopt='-q'
                gmapopt='-u'
                gmapopt=''

            if(forceGribmap or dogribmap == 2):  gmapopt=''
            if(model == 'ecm2'): gmapopt="%s -s100000 -E"%(gmapopt)

            cmd="%s %s -i %s"%(xgribmap,gmapopt,ctlpath)
            mf.runcmd(cmd,ropt)

            if(ctlpr != None and doPrCtl):
                cmd="%s %s -i %s"%(xgribmap,gmapopt,ctlprpath)
                mf.runcmd(cmd,ropt)

            if(ctlhl != None and doHlCtl):
                cmd="%s %s -i %s"%(xgribmap,gmapopt,ctlhlpath)
                mf.runcmd(cmd,ropt)

            if(ctlmand != None and doMandCtl):
                cmd="%s %s -i %s"%(xgribmap,gmapopt,ctlmandpath)
                mf.runcmd(cmd,ropt)

            print 'GGGGGstatus: ',gribmapStatusFile
            cmd="touch %s"%(gribmapStatusFile)
            mf.runcmd(cmd,'')

        if(incrontab):
            eventtag="EEEND--- nwp2.data.gribmap  model: %s dtg: %s"%(model,dtg)
            self.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)



    def getOpsDtg(self,dtgopt,model=None,fphr12=4.0,fphr06=2.5):

        dd=dtgopt.split('.')
        ddc=dtgopt.split(',')

        if(len(dd) == 1 and len(ddc) > 1):
            dtgs=ddc

        elif(len(dd) == 1):

            # -- very specific handling of ops12|6 for ew2
            #
            if(dtgopt == 'ops12'):
                dtg=mf.dtg12()
                fphr=float(mf.dtg12('fphr'))
                if(fphr <= fphr12):
                    dtg=mf.dtginc(dtg,-12)

                dtgs=[dtg]

            elif(dtgopt == 'ops6'):
                (dtg,phr)=mf.dtg_phr_command_prc('cur')
                fphr=float(phr)
                if(fphr <= fphr06):
                    dtg=mf.dtginc(dtg,-6)

                dtgs=[dtg]

            else:
                # -- look for YYYYMM dtgopt
                #
                dtgopt1=dd[0]
                dtgs=mf.dtg_dtgopt_prc(dtgopt1)
                if(model != None and len(dtgs) > 1):
                    dtmodel=self.Model2DdtgData(model)
                    dtgopt1="%s.%d"%(dtgopt1,dtmodel)
                dtgs=mf.dtg_dtgopt_prc(dtgopt1)


        elif(len(dd) >= 2 and len(dd) <= 3):
            if(model != None):
                dtmodel=self.Model2DdtgData(model)
                if(len(dd) == 2 and dtmodel == 12):
                    dtgopt="%s.%d"%(dtgopt,dtmodel)
            dtgs=mf.dtg_dtgopt_prc(dtgopt)


        return(dtgs)




