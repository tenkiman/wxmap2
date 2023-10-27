diag=1
from M import MFutils
MFt=MFutils()
if(diag): MFt.sTimer('load')
from WxMAP2 import *
w2=W2()

w2center=w2.W2Center.lower()
if(diag): MFt.dTimer('load')

hpssHead='5year/BMC'
hpssHeadOld='BMC'

class Nwp2Models(MFbase):

    models=w2.Nwp2ModelsNwp

    dmodels={
        'ecmo':'ecm2',
        'ecmo_nws':'ecmn',
        'ngp05cagips':'ngpc',
        'nav05cagips':'navg',
        'ngp05jtwc':'ngpj',
        'nogaps':'ngp2',
        'cmc':'cmc2',
        'sst':'ocn',
        'ww3':'ww3',
        'ohc':'ohc',
    }

    dcenters=['cmc','ecmwf','fnmoc','jma','ncep','ukmo','esrl']


    def __init__(self,sdir='/dat2/w21/dat/nwp2',verb=0):

        models=[]
        modcen={}
        idirs=glob.glob("%s/*/*/"%(sdir))
        dirs=[]
        # -- dirs to exclude from nwp2 models
        #
        for idir in idirs:
            if(not(mf.find(idir,'ocean')) and not(mf.find(idir,'rtfim')) and not(mf.find(idir,'DSs')) and
               not(mf.find(idir,'access-t')) and
               not(mf.find(idir,'gfsenkf_t254')) and
               not(mf.find(idir,'fimens_g7')) and
               not(mf.find(idir,'yotc')) and
               not(mf.find(idir,'gfsgf')) and
               not(mf.find(idir,'tigge')) and
               not(mf.find(idir,'ensFC')) and
               not(mf.find(idir,'panasonic')) and
               not(mf.find(idir,'veriWMO')) and
               not(mf.find(idir,'w2flds'))): dirs.append(idir)
            n1dirs=len(idir.split('/'))

        dirs=dirs+glob.glob("%s/*/ocean/*/"%(sdir))

        for dir in dirs:
            (base,file)=os.path.split(dir)

            n1=len(dir.split('/'))
            tt=base.split('/')
            if(n1 == n1dirs):
                center=tt[-2]
            else:
                center="%s/%s"%(tt[-3],tt[-2])
            dmodel=tt[-1]
            try:
                model=self.dmodels[dmodel]
            except:
                model=dmodel
            models.append([dmodel,model])
            MF.loadDictList(modcen,center,[dmodel,model])
            if(verb): print n1,center,dmodel,model


        centers=modcen.keys()

        if(verb):
            for center in centers:
                print 'ccc ',center,modcen[center]

            for model in models:
                print 'mmm ',model

        self.modcen=modcen
        self.models=models
        self.dcenters=centers
        



class Nwp2Data(MFbase):


    sdir0='/data/amb/users/fiorino/w21/dat/nwp2'
    sdir2='/dat2/w21/dat/nwp2'
    sdir3='/dat3/nwp2'
    sdir4='/dat4/nwp2'
    sdir5='/dat5/nwp2'
    sdir6='/dat6/nwp2'
    sdirE2='/FWV2/dat2/nwp2'
####    sdirJ2='/mnt/lfs2/projects/fim/fiorino/w21/dat/nwp2'
# -- new qumulo fs 201805-06
    sdirg='/data/global/dat/nwp2'
    sdirr='/data/rt/dat/nwp2'

    sdirJ2='/mnt/lfs1/projects/fim/fiorino/w21/dat/nwp2'
    if(w2.onZeus): sdirJ2='/scratch1/portfolios/BMC/fim/fiorino/w21/dat/nwp2'
    if(w2.onTheia): sdirJ2='/scratch3/BMC/fim/fiorino/w21/dat/nwp2'

    sdirs=[sdir2,sdir3,sdir4,sdirE2]

    mssbdir='/mss/jet/projects/fim/fiorino/nwp2'
    hpssbdir='/%s/fim/fiorino/nwp2'%(hpssHead)
    if(w2.curuSer == 'rtfim'):
        mssbdir='/mss/jet/projects/fim/rtfim/nwp2'
        hpssbdir="/5year/BMC/fim/rtfim/nwp2"

###    jetbdir='/lfs2/projects/fim/fiorino/w21/dat/nwp2'
    jetbdir='/lfs1/projects/fim/fiorino/w21/dat/nwp2'
    dat5bdir='/dat5/dat/nwp2'
    dat6bdir='/dat6/dat/nwp2'

    suffixLLLNNN='''>>>-----lll-nnn------>>>'''
    suffixMMMNNN='''<<<-----MMM-nnn------<<<'''

    mssBase='/apps/msstools/default/bin'
    mssGetCmd='%s/mssGet'%(mssBase)
    mssTarCmd='%s/mssTar'%(mssBase)
    mssLsCmd='%s/mssLs'%(mssBase)

    mssJetSunLsCmd='ssh jet-sun /usr/adic/local/mssTools/bin/simpleLs'

    hpssLsCmd='ssh -l Michael.Fiorino hpssvfs4.fairmont.rdhpcs.noaa.gov ls'
    hpssLsCmd='/apps/hpss/hsi -q ls'
    hpssRmCmd='ssh -l Michael.Fiorino hpssvfs4.fairmont.rdhpcs.noaa.gov rm'
    hpssRmCmd='/apps/hpss/hsi -q rm'
    hpssMkdirCmd='ssh -l Michael.Fiorino hpssvfs4.fairmont.rdhpcs.noaa.gov mkdir'
    hpssMkdirCmd='/apps/hpss/hsi -q mkdir'
    hpssGetCmd='/apps/hpss/hsi get'
    hpssTarCmd='/apps/hpss/htar'

    zeusPreStageuRl='%s@%s'%(w2.ZeusScpServerLogin,w2.ZeusScpServer)
    zeusPreStageDir='/scratch1/portfolios/BMC/fim/fiorino/w21/tmp'
    zeusInvDir='/scratch1/portfolios/BMC/fim/fiorino/w21/dat/nwp2/DSs'

    theiaPreStageuRl='%s@%s'%(w2.TheiaScpServerLogin,w2.TheiaScpServer)
    theiaPreStageDir='/scratch1/portfolios/BMC/fim/fiorino/w21/tmp'
    theiaInvDir='/scratch1/portfolios/BMC/fim/fiorino/w21/dat/nwp2/DSs'

    jetPreStageuRl='%s@%s'%(w2.WjetScpServerLogin,w2.WjetScpServer)
###    jetPreStageDir='/lfs2/projects/fim/fiorino/w21/tmp'
###    jetInvDir='/lfs2/projects/fim/fiorino/w21/dat/nwp2/DSs'
    jetPreStageDir='/lfs1/projects/fim/fiorino/w21/tmp'
    jetInvDir='/lfs1/projects/fim/fiorino/w21/dat/nwp2/DSs'

    jetScpuRl=jetPreStageuRl

    MF.ChkDir(w2.Nwp2DataDSsBdir,'mk')

    dsbdir="%s"%(w2.Nwp2DataDSsBdir)
    dbkeyLocal='local'
    dbkeyMss='mss'

    def __init__(self,sdirs=None,sdiropt=None,mssbdir=None,
                 overrideL=0,
                 overrideM=0,
                 verb=0,
                 doremoteRsync=1,
                 dbname='invNwp2',
                 dojet=0):

        self.dtgDirs=[]
        self.center_model_dtgs={}
        self.verb=verb
        self.sdiropt=sdiropt

        self.dbname="%s-%s"%(dbname,sdiropt)
        if(w2.curuSer == 'rtfim'): self.dbname="%s-RTFIM-%s"%(dbname,sdiropt)
        self.dbfile="%s.pypdb"%(self.dbname)

        self.dbfileLocal="%s-local.pypdb"%(self.dbname)
        self.dbfileMss="%s-mss.pypdb"%(self.dbname)
        self.dbfileLocalJet="%s-datj2-local.pypdb"%(dbname)
        self.dbfileMssJet="%s-datj2-mss.pypdb"%(dbname)


        if(sdirs == None):
            self.sdirs=sdirs

        if(mssbdir == None): self.mssbdir=self.mssbdir

        if(sdiropt == 'dat4'):
            self.sdirs=self.sdir4
            self.sbdirs=self.sdir4
        elif(sdiropt == 'dat3'):
            self.sdirs=self.sdir3
            self.sbdirs=self.sdir3
        elif(sdiropt == 'dat5'):
            self.sdirs=self.sdir5
            self.sbdirs=self.sdir5
        elif(sdiropt == 'dat6'):
            self.sdirs=self.sdir6
            self.sbdirs=self.sdir6
        elif(sdiropt == 'dat0'):
            self.sdirs=self.sdir0
            self.sbdirs=self.sdir0
        elif(sdiropt == 'dat2'):
            self.sdirs=self.sdir2
            self.sbdirs=self.sdir2
        elif(sdiropt == 'datg'):
            self.sdirs=self.sdirg
            self.sbdirs=self.sdirg
        elif(sdiropt == 'datr'):
            self.sdirs=self.sdirr
            self.sbdirs=self.sdirr
        elif(sdiropt == 'datE2'):
            self.sdirs=self.sdirE2
            self.sbdirs=self.sdirE2
        elif(sdiropt == 'datj2'):
            self.sdirs=self.sdirJ2
        else:
            print 'EEE invalid sdiropt for nwp2data: ',sdiropt
            sys.exit()


        n2m=Nwp2Models(self.sdirs)
        self.allmodels=n2m.models
        self.dmodels=n2m.dmodels
        self.dcenters=n2m.dcenters
        self.dmodcen=n2m.modcen

        self.setDSs(overrideL,overrideM,verb=verb,doremoteRsync=doremoteRsync,dojet=dojet)

        if(overrideL or hasattr(self,'overrideL')): self.invLocal()
        if(overrideM or hasattr(self,'overrideM')):
            if(w2.onWjet or w2.onTheia):
                self.invMssJet(verb=verb)
            else:
                print """WWW (nwp2.Nwp2Data.__init__): can't run invMssJet on local machine..."""
                

        try:
            self.n2models=self.dsM.data
        except:
            self.n2models=self.allmodels

        self.center_model_dtgs=self.dsL.data


        AllMssModDtgs={}
        if(self.dsM != None):
            n2hash=self.dsM.data
        else:
            n2hash={}
            
        moddtgs=n2hash.keys()

        for moddtg in moddtgs:
            (mmod,dtg)=moddtg
            MF.appendDictList(AllMssModDtgs,mmod,dtg)

        self.AllMssModDtgs=AllMssModDtgs



    def setDSs(self,overrideL=0,overrideM=0,verb=0,doremoteRsync=1,dojet=0):
        """ setup the python shelf db with inventories local and on mss"""

        # -- bring over inv*pypdb from jet
        #
        if(w2.onKishou or w2.onKaze and doremoteRsync):
            ropt='quiet'
            if(verb): ropt=''
            MF.sTimer('rsync2kazekishou4jet')
            # -- mss jet
            cmd="rsync --protocol=29 -alv %s:%s/%s %s/%s"%(self.jetPreStageuRl,self.jetInvDir,self.dbfileMssJet,self.dsbdir,self.dbfileMssJet)
            MF.runcmd(cmd,ropt)
            # -- local jet
            cmd="rsync --protocol=29 -alv %s:%s/%s %s/%s"%(self.jetPreStageuRl,self.jetInvDir,self.dbfileLocalJet,self.dsbdir,self.dbfileLocalJet)
            MF.runcmd(cmd,ropt)
            MF.dTimer('rsync2kazekishou4jet')

        dounlink=(overrideL and overrideM)
        self.dounlink=dounlink
        DSsJL=None
        DSsJM=None

        onLocal=(w2.onKishou or w2.onKaze)

        if(diag): verb=1
        if(diag): MF.sTimer('setDSs')
        self.DSsL=DataSets(bdir=self.dsbdir,name=self.dbfileLocal,dtype=self.dbname,unlink=dounlink,verb=verb,doDSsWrite=1,dowriteback=0)
        self.DSsM=DataSets(bdir=self.dsbdir,name=self.dbfileMss,dtype=self.dbname,unlink=dounlink,verb=verb,doDSsWrite=1,dowriteback=0)
        if(onLocal):
            DSsJM=DataSets(bdir=self.dsbdir,name=self.dbfileMssJet,dtype=self.dbname,unlink=dounlink,verb=verb,doDSsWrite=0)
            DSsJL=DataSets(bdir=self.dsbdir,name=self.dbfileLocalJet,dtype=self.dbname,unlink=dounlink,verb=verb,doDSsWrite=0)
        if(diag): MF.dTimer('setDSs')


        # -- go for jet pypdb for mss
        #
        if(DSsJM == None):
            self.dsM=self.DSsM.getDataSet(key=self.dbkeyMss,verb=verb)
        else:
            self.dsM=DSsJM.getDataSet(key=self.dbkeyMss,verb=verb)
            overrideM=1

        if(dojet):
            if(DSsJL == None):
                print 'EEE(nwp.Nwp2Data.setDSs): looking for local jet pypdb, but not there and/or onJet...sayoonara'
            else:
                if(diag): print 'III(nwp.Nwp2Data.setDSs): using local jet pypdb........................'
                self.dsL=DSsJL.getDataSet(key=self.dbkeyLocal,verb=verb)
        else:

            self.dsL=self.DSsL.getDataSet(key=self.dbkeyLocal,verb=verb)

            if( self.dsL == None or overrideL):
                if(diag): print 'III:setDSs() new self.dsL...set self.ovrrideL to force local inventory'
                self.dsL=DataSet(name=self.dbkeyLocal,dtype='hash')
                self.overrideL=1

            if( self.dsM == None or ( overrideM and not((onLocal))) ):
                if(diag): print 'III:setDSs() new self.dsM...'
                self.dsM=DataSet(name=self.dbkeyMss,dtype='hash')
                self.overrideM=1


    def setMssInvMask(self):
        smasks=[]
        for dcenter in self.dcenters:
            smasks.append("%s/%s/%s/%s/"%(self.mssbdir,dcenter,'*','??????'))
        return(smasks)


    def parseMssOutput(self,output,itddir=None,verb=0):

        ddir=None
        ddiro=None

        if(len(output) <= 3):
            print 'WWW(invMssJet) no files in output: ',output
            return

        for o in output:

            tt=o.split()
            ltt=len(tt)

            if(mf.find(o,'[connecting to') or ltt == 0): continue

            # 20131101 -- new error
            if(mf.find(o,' error -13 ')): 
                print 'EEE - authentication/initialization failed, sayoonara'
                sys.exit()

            if(mf.find(o,'No such')):
                break

            elif(mf.find(o,'No such') or mf.find(o,'total') or
                 mf.find(o,'drwxr-xr-x')
                 ): continue

            elif(mf.find(o,'hostname') and ltt == 5
                 ): continue

            elif(mf.find(o,'Connection timed out')
                 ):
                print 'EEE(fatal;nwp.invMssJet): hpss down...sayoonara'
                sys.exit()

            elif(mf.find(o,'not responding')
                 ):
                print 'EEE(fatal;nwp.invMssJet): hpss not responding=down...sayoonara'
                sys.exit()


            if(ltt == 1):
                tddir=tt[0][0:-1]

            elif(itddir != None):
                tddir=itddir

            if(ddir == None or tddir != ddiro and tddir != None):
                ddir=tddir
                ddiro=ddir


            if(len(tt) == 9):

                if(mf.find(o,'.idx')): continue

                siz=tt[len(tt)-5]
                path="%s/%s"%(ddir,tt[-1])

                n2model=tt[-1].split('.')[0]
                dtg=tt[-1].split('.')[1]
                if(verb): print 'sss ',siz,path,n2model,dtg

                self.n2fimruns.append(n2model)
                MF.appendDictList(self.n2models,(n2model,dtg),(path,siz))



    def parseMssOutputDirs(self,output,itddir=None,verb=0):

        tddirs=[]

        if(len(output) <= 3):
            print 'WWW(invMss) no files in output: ',output
            return

        for o in output:

            if(mf.find(o,'No such')):
                break
            elif(mf.find(o,'No such') or mf.find(o,'total') or
                 mf.find(o,'drwxr-xr-x')
                 ): continue
            elif(mf.find(o,'Connection timed out')
                 ):
                print 'EEE(fatal;nwp.invMss): hpss down...sayoonara'
                sys.exit()
            elif(mf.find(o,'not responding')
                 ):
                print 'EEE(fatal;nwp.invMss): hpss not responding=down...sayoonara'
                sys.exit()

            tt=o.split()

            if(len(tt) > 1): continue

            if(mf.find(o,'fim/fiorino')):
                tddir=tt[0]

            tddir=tddir[0:-1]
            tddirs.append(tddir)

        tddirs=mf.uniq(tddirs)


        for tddir in tddirs:
            cmd='''%s -l "%s"'''%(self.mssLsCmd,tddir)
            output=MF.runcmdLog(cmd)

            for o in output:

                tt=o.split()

                if(len(tt) == 9):

                    if(mf.find(tt[0],'drwxr')):   continue

                    siz=tt[len(tt)-5]
                    path="%s/%s"%(tddir,tt[-1])

                    n2model=tt[-1].split('.')[0]
                    dtg=tt[-1].split('.')[1]
                    if(verb): print 'sss ',siz,path,n2model,dtg

                    if(mf.find(path,'.idx')): continue

                    #print 'nnnnnnnnnnnnnnnnnn ',n2model,dtg,path,siz
                    self.n2fimruns.append(n2model)
                    self.n2models[n2model,dtg]=(path,siz)


        return(1)


    def invMssJet(self,verb=0,dojetmss=0):

        smasks=self.setMssInvMask()
        
        self.n2models={}
        self.n2fimruns=[]

        for smask in smasks:
            
            if(dojetmss):
                # -- jet mss
                #
                MF.sTimer("jet-mss")
                smask1=smask.replace('mss','mss2')
                cmd='''%s -d "%s"'''%(self.mssJetSunLsCmd,smask1)
                output1=MF.runcmdLog(cmd)
                rc=self.parseMssOutputDirs(output1)
                MF.dTimer("jet-mss")


            # -- zeus hpss
            #
            MF.sTimer("zeus-hpss")
            smask2=smask.replace('mss/jet/projects',hpssHeadOld)
            smask2N=smask.replace('mss/jet/projects',hpssHead)

            smask2s=[smask2,smask2N]

            for smask2 in smask2s:
                
                MF.sTimer("zeus-hpss-%s"%(smask2))

                # -- get listing of dirs
                #
                cmd='''%s -ld "%s"'''%(self.hpssLsCmd,smask2)
                output3=MF.runcmdLog(cmd)
                itddir=None
                if(len(output3) == 4 and not(mf.find(output3[1],'No such'))):
                    itddir=output3[1].replace(':','/')+output3[2].split()[3]
                    print 'WWWWWWWWWWWWWWWWWWWW invMss -- single data dir: ',itddir
    
                cmd='''%s -l "%s"'''%(self.hpssLsCmd,smask2)
                output2=MF.runcmdLog(cmd)
                rc=self.parseMssOutput(output2,itddir,verb=verb)
                MF.dTimer("zeus-hpss-%s"%(smask2))


        self.n2fimruns=mf.uniq(self.n2fimruns)

        if(hasattr(self,'dsM')):
            self.dsM.data=self.n2models
            self.DSsM.putDataSet(self.dsM,key=self.dbkeyMss)
            self.DSsM.closeDataSet()

        if(w2.onTheia):
            ropt='quiet'
            ropt=''
            MF.sTimer('rsync2jet4theia')
            cmd="rsync --protocol=29 -alv %s/%s %s:%s/%s "%(self.dsbdir,self.dbfileMss,self.jetPreStageuRl,self.jetInvDir,self.dbfileMss)
            MF.runcmd(cmd,ropt)
            MF.dTimer('rsync2jet4theia')

    def invHpssJet(self,verb=0):

        smasks=self.setHpssInvMask()
        
        self.n2models={}
        self.n2fimruns=[]

        for smask in smasks:
            
            MF.sTimer("zeus-hpss-%s"%(smask))

            # -- get listing of dirs
            #
            cmd='''%s -ld "%s"'''%(self.hpssLsCmd,smask)
            output3=MF.runcmdLog(cmd)
            itddir=None
            if(len(output3) == 4 and not(mf.find(output3[1],'No such'))):
                itddir=output3[1].replace(':','/')+output3[2].split()[3]
                print 'WWWWWWWWWWWWWWWWWWWW invMss -- single data dir: ',itddir

            cmd='''%s -l "%s"'''%(self.hpssLsCmd,smask)
            #mf.runcmd(cmd)
            output2=MF.runcmdLog(cmd)
            rc=self.parseMssOutput(output2,itddir,verb=verb)
            MF.dTimer("zeus-hpss-%s"%(smask))


        self.n2fimruns=mf.uniq(self.n2fimruns)

        if(hasattr(self,'dsM')):
            #kk=self.n2models.keys()
            self.dsM.data=self.n2models
            self.DSsM.putDataSet(self.dsM,key=self.dbkeyMss)
            self.DSsM.closeDataSet()

        if(w2.onTheia):
            ropt='quiet'
            ropt=''
            MF.sTimer('rsync2jet4theia')
            cmd="rsync --protocol=29 -alv %s/%s %s:%s/%s "%(self.dsbdir,self.dbfileMss,self.jetPreStageuRl,self.jetInvDir,self.dbfileMss)
            MF.runcmd(cmd,ropt)
            MF.dTimer('rsync2jet4theia')



    def gettaus(self,files,warn=1,verb=0):
        taus=[]
        for ffile in files:
            if(verb): print 'ffff ',ffile
            # -- special case for gfs goes imagery
            #
            if(mf.find(ffile,'goes')):
                ttau=ffile.split('.')[-3]
            # -- navgem from ncep vice cagips
            #
            elif(mf.find(ffile,'navgem')):
                (ndir,nfile)=os.path.split(ffile)
                ttau=nfile.split('.')[-2][-4:]
            else:
                ttau=ffile.split('.')[-2]
            
            if(ttau[0] != 'f' or len(ttau) != 4):
                if(warn): print 'WWW(nwp.Nwp2Data.gettaus): --- bad file name for getting tau: ',ffile
                taus.append(0)
                return(taus)
            tau=int(ttau[1:])
            taus.append(tau)
            
        return(taus)



    def invLocal(self,overrideKey1=None,verb=1,singleModel=None,tauverb=0):


        def isSingleInSmodels(singleModel,smodels):
            rc=0
            for smodel in smodels:
                for sm in smodel:
                    if(singleModel==sm):
                        smodels=[smodel]
                        rc=1
                        break
            return(rc,smodels)


        if(singleModel != None): self.center_model_dtgs={}

        if(len(self.dcenters) == 0):
            print 'EEE no dcenters for self.sdirs: ',self.sdirs
            sys.exit()

        for dcenter in self.dcenters:

            smodels=self.dmodcen[dcenter]
            (rc,smodels)=isSingleInSmodels(singleModel,smodels)

            if(singleModel != None and not(rc) ):
                continue

            for smodel in smodels:
                if(overrideKey1 == 'w2flds'):
                    sdir="%s/%s"%(self.sdirs,smodel[0])
                else:
                    sdir="%s/%s/%s"%(self.sdirs,dcenter,smodel[0])


                sdtgs=glob.glob("%s/??????????"%(sdir))
                dtgs=[]
                for sdtg in sdtgs:
                    (base,dtg)=os.path.split(sdtg)
                    dtgs.append(dtg)

                MF.sTimer("%-10s"%(smodel[1]))

                taus={}

                for dtg in dtgs:

                    mask="%s/%s/*.gr*b?"%(sdir,dtg)
                    if(w2.curuSer == 'rtfim'): mask="%s/%s/*.ctl"%(sdir,dtg)

                    try:
                        files=glob.glob(mask)
                        dtaus=self.gettaus(files)
                    except:
                        files=None
                        dtaus=[]

                    if(w2.curuSer == 'rtfim'):
                        dtaus=range(0,168+1,6)
                        dtaus.append(999)

                    dtaus.sort()
                    if(tauverb): print 'dtg,taus: ',smodel,mask,dtg,dtaus
                    taus[dtg]=dtaus

                if(overrideKey1 != None):
                    key1=overrideKey1
                else:
                    key1=dcenter

                key1=dcenter
                omodel=smodel[1]
                self.center_model_dtgs[key1,omodel,sdir]=(dtgs,taus)
                if(verb): print "IIIIIIIIIIIIIIIIIIIIII ndtgs: %4i dcenter: %-15s omodel: %-10s  sdir: %-70s"%(len(dtgs),dcenter,omodel,sdir)

                MF.dTimer("%-10s"%(smodel[1]))

            if(singleModel != None):
                return

        if(hasattr(self,'dsL')):
            self.dsL.data=self.center_model_dtgs
            self.DSsL.putDataSet(self.dsL,key=self.dbkeyLocal,verb=1)
            self.DSsL.closeDataSet()


    def invLocalSingle(self,singleModel=None,overrideKey1=None,verb=0):
        self.invLocal(overrideKey1=overrideKey1,verb=verb,singleModel=singleModel)



    def invLocalOld(self,overrideKey1=None,verb=1):

        s1dirs=self.getsubdirs(self.sdirs)


        for s1 in s1dirs.keys():
            s2dirs=self.getsubdirs(s1dirs[s1])

            for s2dir in s2dirs.keys():
                MF.sTimer(s2dir)
                taus={}

                s3dirs=self.getsubdirs(s2dirs[s2dir])
                sdir=s2dirs[s2dir]
                dtgs=s3dirs.keys()

                try:      omodel=self.dmodels[s2dir]
                except:   omodel=s2dir

                if(verb): print len(dtgs),sdir,s1,s2dir,omodel

                for dtg in dtgs:

                    mask="%s/%s/%s/*.grb?"%(s1dirs[s1],s2dir,dtg)
                    tauverb=0
                    try:
                        files=glob.glob(mask)
                        dtaus=self.gettaus(files)
                    except:
                        files=None
                        dtaus=[]

                    #print 'dtg,taus: ',omodel,mask,dtg,dtaus
                    taus[dtg]=dtaus

                if(overrideKey1 != None):
                    key1=overrideKey1
                else:
                    key1=s1

                sdir="%s/%s"%(s1dirs[s1],s2dir)

                self.center_model_dtgs[key1,omodel,sdir]=(dtgs,taus)
                MF.dTimer(s2dir)




    def getsubdirs(self,sdirs,exclude=['w2flds','rtfim']):

        if(type(sdirs) != ListType): sdirs=[sdirs]
        subdirs={}
        for sdir in sdirs:
            ssdirs=os.listdir(sdir)
            for ss in ssdirs:
                if(mf.find(ss,'.DS_') or
                   ss in exclude
                   ): continue
                spath="%s/%s"%(sdir,ss)
                if(os.path.islink(spath) or not(os.path.isdir(spath)) ): continue
                subdirs[ss]=spath

        return(subdirs)



    def getDtgDirs(self,model):

        self.modelLocalDirs={}
        self.dtgLocalDirs={}
        self.tausLocalDirs={}

        kk=self.center_model_dtgs.keys()
        for k in kk:
            if (model == k[1]):
                self.modelLocalDirs[model]=k[2]
                self.model=model
                rc=self.center_model_dtgs[k]
                if(type(rc) is TupleType):
                    (mdtgs,mtaus)=rc
                else:
                    mdtgs=rc
                    mtaus={}

                mdtgs.sort()
                
                for dtg in mdtgs:
                    self.dtgLocalDirs[dtg]="%s/%s"%(k[2],dtg)

                    try:
                        self.tausLocalDirs[dtg]=mtaus[dtg]
                    except:
                        self.tausLocalDirs[dtg]=[]


    def lsLocalDtgDirs(self,model,lsdtgs,rmodel=None,doprint=1,fulltaus=0,showall=0):

        self.localthere={}

        self.getDtgDirs(model)

        if(not(type(lsdtgs) is ListType)): lsdtgs=[lsdtgs]

        alltaus=[]
        for dtg in lsdtgs:
            try:
                taus=self.tausLocalDirs[dtg]
            except:
                taus=[]
            alltaus=alltaus + taus

        if(doprint and len(alltaus) >= 0 or showall):
            if(rmodel != None):
                print 'LLL------------------------------local for model: ',model,' rmodel: ',rmodel
            else:
                print 'LLL------------------------------local for model: ',model

        else:
            doprint=0

        thereDtgs=[]

        for dtg in lsdtgs:

            try:
                taus=self.tausLocalDirs[dtg]
            except:
                taus=[]


            if(len(taus) > 0): thereDtgs.append(dtg)

            taus=mf.uniq(taus)

            self.localthere[dtg]=len(taus)

            if(doprint):
                if(fulltaus):
                    taucard="Ntaus: %3d taus:"%(len(taus))
                    for tau in taus:
                        taucard="%s %03d"%(taucard,tau)

                omodel="%-30s %10s"%(model,dtg)
                if(rmodel != None): omodel="%-30s %10s"%(rmodel,dtg)

                if(len(taus) > 3):
                    if(not(fulltaus)): taucard="taus: %03d %03d ... %03d"%(taus[0],taus[1],taus[-1])
                    print 'LLL_YYY: %s'%(omodel),"%-80s  %s"%(self.dtgLocalDirs[dtg],taucard)
                elif(len(taus) == 1):
                    if(not(fulltaus)): taucard="taus: %03d"%(taus[0])
                    print 'LLL_YYY: %s'%(omodel),"%-80s %s"%(self.dtgLocalDirs[dtg],taucard)
                else:
                    print 'LLL_NNN: %s %s'%(omodel,self.suffixLLLNNN)

        if(doprint): print

        return(thereDtgs)


    def rmLocalDtgDirs(self,model,lsdtgs,rmodel=None,ropt='norun'):

        self.localthere={}
        self.getDtgDirs(model)

        if(not(type(lsdtgs) is ListType)): lsdtgs=[lsdtgs]

        for dtg in lsdtgs:

            try:
                taus=self.tausLocalDirs[dtg]
            except:
                taus=[]

            taus=mf.uniq(taus)

            self.localthere[dtg]=len(taus)

            taucard="Ntaus: %3d taus:"%(len(taus))
            for tau in taus:
                taucard="%s %03d"%(taucard,tau)

            omodel="%-30s %10s"%(model,dtg)
            if(rmodel != None): omodel="%-30s %10s"%(rmodel,dtg)

            dorm=0
            if(len(taus) > 3):
                #taucard="taus: %03d %03d ... %03d"%(taus[0],taus[1],taus[-1])
                #print 'RM_----: %s'%(omodel),"%-80s  %s"%(self.dtgLocalDirs[dtg],taucard)
                dorm=1
            elif(len(taus) == 1):
                #taucard="taus: %03d"%(taus[0])
                #print 'RM_iiiii: %s'%(omodel),"%-80s %s"%(self.dtgLocalDirs[dtg],taucard)
                dorm=1

            if(dorm):
                cmd="rm -f -r %s"%(self.dtgLocalDirs[dtg])
                mf.runcmd(cmd,ropt)



    def setMssDir(self,ldir,model,dtg):
        center=ldir.split('/')[-3]
        mssdir="%s/%s/%s/%s"%(self.mssbdir,center,model,dtg[0:6])
        print 'PPP(put2mss)       ldir: ',ldir
        print 'PPP(put2mss)     mssdir: ',mssdir
        rc=self.chkMssDir(mssdir,verb=0)
        
        mssfile="%s.%s.%s.tar"%(model,dtg,w2center)
        return(mssdir,mssfile)

    def setHpssDir(self,ldir,model,dtg,verb=1):
        
        center=ldir.split('/')[-3]
        hpssdir="%s/%s/%s/%s"%(self.hpssbdir,center,model,dtg[0:6])
        rc=self.chkHpssDir(hpssdir,verb=verb)

        # -- cycling if fails
        #
        if(rc == 0):
            ntry=1
            ntryMax=3
            trySleep=15
            while(ntry <= ntryMax):
                print
                print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII--------------------------retry chkHpssDir...ntry: ",ntry,"rc: ",rc,"model: ",model,"dtg: ",dtg
                print
                time.sleep(trySleep)  
                rc=self.chkHpssDir(hpssdir,verb=verb)
                if(rc > 0):
                    ntry=999
                else:
                    ntry=ntry+1
        
        hpssfile="%s.%s.tar"%(model,dtg)
        return(rc,hpssdir,hpssfile)


    def setJetDir(self,ldir,model,dtg):
        center=ldir.split('/')[-3]
        jetdir=ldir.replace(self.sbdirs,self.jetbdir)

        print 'PPP(put2jet.nwp2)       ldir: ',ldir
        print 'PPP(put2jet.nwp2)     jetdir: ',jetdir
        return(jetdir)


    def setDat5Dir(self,ldir,model,dtg):
        center=ldir.split('/')[-3]
        dat5dir=ldir.replace(self.sbdirs,self.dat5bdir)

        print 'PPP(put2Dat5.nwp2)       ldir: ',ldir
        print 'PPP(put2Dat5.nwp2)    dat5dir: ',dat5dir
        return(dat5dir)

    def setDat6Dir(self,ldir,model,dtg):
        center=ldir.split('/')[-3]
        dat6dir=ldir.replace(self.sbdirs,self.dat6bdir)

        print 'PPP(put2Dat6.nwp2)       ldir: ',ldir
        print 'PPP(put2Dat6.nwp2)    dat6dir: ',dat6dir
        return(dat6dir)


    def setKlean(self,sddir,ropt):
        print 'WWW(setKlean): doKlean of sddir: ',sddir
        if(MF.ChkDir(sddir)):
            print 'WWW(putLocal2MssModelDtgs): doKlean of sddir: ',sddir
            cmd="rm -f -r %s"%(sddir)
            mf.runcmd(cmd,ropt)


    def setLocalGrbMask(self,dtg):
        grbmask=None
        try:
            gmask="%s/*.grb?"%(self.dtgLocalDirs[dtg])
            if(w2.curuSer == 'rtfim'): gmask="%s/*.ctl"%(self.dtgLocalDirs[dtg])
            grbmask=gmask
        except:
            None
        return(grbmask)


    def putLocal2MssModelDtgs(self,model,dtgs,ropt='',override=0,doKlean=0,verb=1):

        if(dtgs == None):
            if(hasattr(self,'localModelDtgs')):
                dtgs=self.localModelDtgs[model]
            else:
                print 'EEE(putLocal2MssModelDtgs): dtgs=None and getAllDtgs() not run'
                sys.exit()

        elif(not(type(dtgs) is ListType)):
            dtgs=[dtgs]

        # -- get dtglocaldirs for this model
        #
        self.getDtgDirs(model)

        for dtg in dtgs:

            grbmask=self.setLocalGrbMask(dtg)

            try:
                files=glob.glob(grbmask)
                ldir=self.dtgLocalDirs[dtg]
                ldirthere=1
                if(len(files) == 0): ldirthere=0
            except:
                ldir=None
                ldirthere=0

            if(ldirthere):

                (mssdir,mssfile)=self.setMssDir(ldir,model,dtg)

                mssTOCfile="%s.toc"%(mssfile)

                (sbdir,file)=os.path.split(ldir)
                sddir=ldir
                msspath="%s/%s"%(mssdir,mssfile)
                mssTOCpath="%s/%s"%(sbdir,mssTOCfile)

                print 'PPP(put2mss)     msspath: ',msspath
                print 'PPP(put2mss)  mssTOCpath: ',mssTOCpath
                print 'PPP(put2mss)       sddir: ',sddir

                MF.ChangeDir(sddir,verb=verb)

                # -- check if tarball there
                #
                rcmssmss=self.chkMssPath(msspath,verb=verb)
                rcmsshpss=self.chkHpssPath(hpsspath,verb=verb)

                # -- if -999 something happend with Popen; bail
                # 
                if(rcmsshpss == -99999 or rcmssmss == -999):
                    print 'EEE Popen failed in chMssPath for dtg: ',dtg,' die'
                    sys.exit()

                # -- if not tarball
                #
                rctar=1
                if(rcmss < 0 or override):

                    # -- blow away mss tarball if > 0 and override
                    #
                    if( override or self.chkMssSize(msspath,verb=verb) > 0 ):

                        cmd="rm -f %s"%(mssTOCpath)
                        mf.runcmd(cmd,ropt)

                        cmd='''mssRm --verbose "%s"'''%(msspath)
                        mf.runcmd(cmd,ropt)

                    cmd="%s --verbose -v --toc-file %s -cf %s ."%(self.mssTarCmd,mssTOCpath,msspath)
                    cmd="%s -cvf %s ."%(self.hpssTarCmd,hpsspath)
                    lines=MF.runcmdLog(cmd)
                    for line in lines:

                        if(mf.find(line,'failed') and mf.find(line,'mssPut') and (w2.onWjet or w2.onTheia) ):
                            print 'WWW(mssPut failed) but works on wjet?'
                            rctar=1
                            break

                        elif(mf.find(line,'failed') ):
                            rctar=0
                            break


                else:
                    print 'WWW(putLocal2MssModelDtgs): msspath: ',msspath,' on mss; set override=1 to overwrite'

                print 'rctar------------------------------------: ',rctar,sddir
                if(doKlean and os.path.isdir(sddir) and rctar):
                    self.setKlean(sddir,ropt)

            else:
                # -- skip if not there...
                #
                if(ldir == None): 
                    print 'WWW ldir-local2Mss: ',ldir,' empty -- press...'
                    continue

                if(doKlean):
                    print 'III doKlean=1 kill off empty dir'
                    if(MF.ChkDir(ldir)):
                        cmd='rm -r -f %s'%(ldir)
                        mf.runcmd(cmd,'')

                #if(ropt == 'norun'): continue


    def putLocal2HpssModelDtgs(self,model,dtgs,ropt='',override=0,doKlean=0,verb=1,minSiz=0.02):

        def doHtar(model,dtg):
        
            rctar=-999
            
            MF.sTimer('htar: %s %s'%(model,dtg))
            cmd="%s -cvf %s ."%(self.hpssTarCmd,hpsspath)
            lines=MF.runcmdLog(cmd)
            MF.dTimer('htar: %s %s'%(model,dtg))

            for line in lines:
                rctar=0
                if(mf.find(line,'failed') ):
                    rctar=0
                    break

                elif(mf.find(line,'HTAR SUCCESSFUL')):
                    rctar=1
                    break
                
            return(rctar,cmd,lines)
        
        
        if(dtgs == None):
            if(hasattr(self,'localModelDtgs')):
                dtgs=self.localModelDtgs[model]
            else:
                print 'EEE(putLocal2HpssModelDtgs): dtgs=None and getAllDtgs() not run'
                sys.exit()

        elif(not(type(dtgs) is ListType)):
            dtgs=[dtgs]

        # -- get dtglocaldirs for this model
        #
        self.getDtgDirs(model)

        for dtg in dtgs:

            MF.sTimer("putLocal2HpssModelDtgs: model: %s dtg: %s"%(model,dtg))
            grbmask=self.setLocalGrbMask(dtg)

            try:
                files=glob.glob(grbmask)
                ldir=self.dtgLocalDirs[dtg]
                ldirthere=1
                if(len(files) == 0): ldirthere=0
            except:
                ldir=None
                ldirthere=0

            if(ldirthere):

                (rc,hpssdir,hpssfile)=self.setHpssDir(ldir,model,dtg)
                
                # -- what to do if setHpssDir fails...
                if(rc == 0):
                    print
                    print "IIIIIIIIIIIIIII----------------- setHpssDir failed..."
                    print "IIIIIIIIIIIIIII----------------- model: ",model,"dtg: ",dtg,"ldir: ",ldir
                    print "IIIIIIIIIIIIIII----------------- continue to next dtg..."
                    print
                    continue
                    
                hpssTOCfile="%s.idx"%(hpssfile)

                (sbdir,file)=os.path.split(ldir)
                sddir=ldir

                hpsspath="%s/%s"%(hpssdir,hpssfile)
                hpssTOCpath="%s/%s"%(hpssdir,hpssTOCfile)
                localhpssTOCpath="%s/%s"%(sbdir,hpssTOCfile)

                print 'PPP(put2hpss)         hpsspath: ',hpsspath
                print 'PPP(put2hpss)      hpssTOCpath: ',hpssTOCpath
                print 'PPP(put2hpss) localhpssTOCpath: ',localhpssTOCpath
                print 'PPP(put2hpss)            sbdir: ',sbdir
                print 'PPP(put2hpss)            sddir: ',sddir

                MF.ChangeDir(sddir,verb=verb)

                # -- check if tarball there
                #
                rchpss=self.chkHpssPath(hpsspath,verb=verb)

                # -- if -99999 something happend with Popen; bail
                # 
                if(rchpss == -99999):
                    print 'EEE Popen failed in chHpssPath for dtg: ',dtg,' die'
                    sys.exit()
                    
                # -- get size of hpsspath
                #
                hpsspathSiz=self.chkHpssSize(hpsspath,verb=0)
                
                # -- assume rctar is 1, i.e., that will not go into doing the rctar below
                #
                rctar=1
                
                if(hpsspathSiz < 0 or override or (hpsspathSiz <= minSiz) ):

                    # -- blow away hpss tarball if > 0 and override
                    #
                    rctar=0
                    if( override or (hpsspathSiz > 0 and hpsspathSiz <= minSiz) ):

                        cmd="rm -f %s"%(localhpssTOCpath)
                        mf.runcmd(cmd,ropt)

                        cmd="%s %s"%(self.hpssRmCmd,hpsspath)
                        mf.runcmd(cmd,ropt)
                        
                    if(rchpss == -1):
                        
                        # -- hpss down, cycle...
                        #
                        ntry=1
                        ntryMax=3
                        trySleep=15
                        while(ntry <= ntryMax):
                            print
                            print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII--------------------------retry htar..."
                            print
                            time.sleep(trySleep)  
                            # -- check if tarball there
                            #
                            rchpss=self.chkHpssPath(hpsspath,verb=verb)                            
                            if(rchpss != -99999 and (rchpss < 0 and rchpss != -1)):
                                
                                (rctar,cmd,lines)=doHtar(model,dtg)
                                if(rctar == 0):
                                    print 'EEEE cmd: ',cmd
                                    for line in  lines:
                                        print line
       
                                if(rctar):
                                    # -- copy over the .idx file to local
                                    #
                                    cmd="%s %s : %s"%(self.hpssGetCmd,localhpssTOCpath,hpssTOCpath)
                                    lines=MF.runcmdLog(cmd)
                                ntry=999
                                    
                            else:
                                ntry=ntry+1
                                
                                    
                            
                    else:
                        # --- hpss up...
                        #
                        (rctar,cmd,lines)=doHtar(model,dtg)
                    
                        if(rctar == 0):
                            print 'EEEE cmd: ',cmd
                            for line in  lines:
                                print line

                        if(rctar):
                            # -- copy over the .idx file to local
                            #
                            cmd="%s %s : %s"%(self.hpssGetCmd,localhpssTOCpath,hpssTOCpath)
                            lines=MF.runcmdLog(cmd)

                else:
                    print 'WWW(putLocal2HpssModelDtgs): hpsspath: ',hpsspath,' on hpss; set override=1 to overwrite'

                print 'rctar------------------------------------: ',rctar,sddir
                if(doKlean and os.path.isdir(sddir) and rctar):
                    self.setKlean(sddir,ropt)

            else:
                # -- skip if not there...
                #
                if(ldir == None): 
                    print 'WWW ldir-local2Hpss: ',ldir,' empty -- press...'
                    continue

                if(doKlean):
                    print 'III doKlean=1 kill off empty dir',ldir
                    if(MF.ChkDir(ldir)):
                        cmd='rm -r -f %s'%(ldir)
                        mf.runcmd(cmd,'')

                #if(ropt == 'norun'): continue

            MF.dTimer("putLocal2HpssModelDtgs: model: %s dtg: %s"%(model,dtg))
            print


    def chkJetRc(self,rc,verb=0):

        rcdone=0
        rcsize=0
        finalRC=0

        siz=None
        for r in rc:
            if(verb): print 'r: ',r
            if(mf.find(r,'... done')): rcdone=1
            if(mf.find(r,'total size')):
                siz=r.split()[3]
                rcsize=1
            if(mf.find(r,'connection unexpectedly closed')):
                finalRC=-1

        if(rcdone and rcsize and siz > 0):
            finalRC=1

        print 'FFF chkRc: finalRC: ',finalRC,' siz: ',siz
        return(finalRC)

    def chkDat5Rc(self,rc,verb=0):

        rcdone=0
        rcsize=0
        finalRC=0

        siz=None
        for r in rc:
            if(verb): print 'r: ',r
            if(mf.find(r,'... done')): rcdone=1
            if(mf.find(r,'total size')):
                siz=r.split()[3]
                rcsize=1

        if(rcdone and rcsize and siz > 0):
            finalRC=1

        print 'FFF chkRc: finalRC: ',finalRC,' siz: ',siz
        return(finalRC)


    def chkDat6Rc(self,rc,verb=0):

        rcdone=0
        rcsize=0
        finalRC=0

        siz=None
        for r in rc:
            if(verb): print 'r: ',r
            if(mf.find(r,'... done')): rcdone=1
            if(mf.find(r,'total size')):
                siz=r.split()[3]
                rcsize=1

        if(rcdone and rcsize and siz > 0):
            finalRC=1

        print 'FFF chkRc: finalRC: ',finalRC,' siz: ',siz
        return(finalRC)




    def putLocal2JetModelDtgs(self,model,dtgs,ropt='',override=0,doKlean=0,verb=1):


        if(dtgs == None):
            if(hasattr(self,'localModelDtgs')):
                dtgs=self.localModelDtgs[model]
            else:
                print 'EEE(putLocal2MssModelDtgs): dtgs=None and getAllDtgs() not run'
                sys.exit()

        elif(not(type(dtgs) is ListType)):
            dtgs=[dtgs]

        # -- get dtglocaldirs for this model
        #
        self.getDtgDirs(model)

        for dtg in dtgs:

            MF.sTimer("putLocal2JetModelDtgs: model: %s dtg: %s"%(model,dtg))

            try:
                files=glob.glob("%s/*.grb?"%(self.dtgLocalDirs[dtg]))
                ldir=self.dtgLocalDirs[dtg]
                ldirthere=1
                if(len(files) == 0): ldirthere=0
            except:
                ldir=None
                ldirthere=0


            if(ldirthere):

                # -- check the jet inventory before rsync to jet
                #
                (mssthere,msssiz)=self.chkMssPathInv(model,dtg)

                domss=1
                if(mssthere and msssiz > 0 and not(override)):
                    print 'WWW(putLocal2JetModelDtgs): already on mss siz: ',msssiz,' will clean off if doKlean'
                    domss=0
                    finalRC=1

                if(domss):

                    jetdir=self.setJetDir(ldir,model,dtg)
                    (sbdir,file)=os.path.split(ldir)
                    sddir=ldir

                    # first mkdir on jet
                    #
                    cmd="ssh %s mkdir -p %s/"%(self.jetScpuRl,jetdir)
                    rc=MF.runcmdLog(cmd,ropt)

                    # -- rsync over the data
                    #
                    cmd="rsync --protocol=29 -alv %s/ %s:%s/"%(sddir,self.jetScpuRl,jetdir)
                    rc=MF.runcmdLog(cmd,ropt)
                    finalRC=self.chkJetRc(rc,verb=0)
                    
                    # -- set finalRC for testing
                    if(ropt == 'norun' ): finalRC=1

                    # -- if rsync fails try ntryMax times
                    #
                    if(finalRC <= 0):
                        
                        print 'WWW(putLocal2JetModelDtgs): starting to loop...',model,dtg
                        ntry=1
                        ntryMax=3
                        trySleep=15
                        while(ntry <= ntryMax):
                            print
                            print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII--------------------------retry rsync..."
                            print
                            time.sleep(trySleep)
                            MF.sTimer("III(putLocal2JetModelDtgs): redoing rsync...ntry: %d model: %s dtg: %s"%(ntry,model,dtg))
                            cmd="rsync --protocol=29 -alv %s/ %s:%s/"%(sddir,self.jetScpuRl,jetdir)
                            rc=MF.runcmdLog(cmd,ropt)
                            finalRC=self.chkJetRc(rc,verb=1)
                            MF.dTimer("III(putLocal2JetModelDtgs): redoing rsync...ntry: %d model: %s dtg: %s"%(ntry,model,dtg))

                            if(finalRC <= 0):
                                ntry=ntry+1
                            else:
                                print "III(putLocal2JetModelDtgs): rsync redo WORKED!!  ntry: %d model: %s dtg: %s"%(ntry,model,dtg)
                                break


                # -- check if there and clean off
                #
                if(doKlean and os.path.isdir(ldir) and (finalRC == 1)):
                    self.setKlean(ldir,ropt)
                    
                if(finalRC == -1):
                    print
                    print "WWW(putLocal2JetModelDtgs): jet is down/inaccessible for model: %s dtg: %s  ...  press"%(model,dtg)
                    print
                
            
            
            else:
                # -- skip if not there...
                #
                if(ldir == None): 
                    print 'WWW ldir-local2jet: ',ldir,' empty -- press...'
                    continue

                if(doKlean):

                    if(MF.ChkDir(ldir)):
                        print 'III doKlean=1 kill off empty dir'
                        cmd='rm -r -f %s'%(ldir)
                        mf.runcmd(cmd,'')

            MF.dTimer("putLocal2JetModelDtgs: model: %s dtg: %s"%(model,dtg))
            print

    def putLocal2Dat5ModelDtgs(self,model,dtgs,ropt='',override=0,doKlean=0,verb=1):

        if(dtgs == None):
            if(hasattr(self,'localModelDtgs')):
                dtgs=self.localModelDtgs[model]
            else:
                print 'EEE(putLocal2Dat5Dtgs): dtgs=None and getAllDtgs() not run'
                sys.exit()

        elif(not(type(dtgs) is ListType)):
            dtgs=[dtgs]

        # -- get dtglocaldirs for this model
        #
        self.getDtgDirs(model)

        for dtg in dtgs:

            MF.sTimer("putLocal2Dat5ModelDtgs: model: %s dtg: %s"%(model,dtg))

            try:
                files=glob.glob("%s/*.grb?"%(self.dtgLocalDirs[dtg]))
                ldir=self.dtgLocalDirs[dtg]
                ldirthere=1
                if(len(files) == 0): ldirthere=0
            except:
                ldir=None
                ldirthere=0


            if(ldirthere):

                dat5dir=self.setDat5Dir(ldir,model,dtg)
                (sbdir,file)=os.path.split(ldir)
                sddir=ldir

                MF.ChkDir(dat5dir,'mk')

                # -- rsync over the data
                #
                cmd="rsync --protocol=29 -alv %s/ %s/"%(sddir,dat5dir)
                rc=MF.runcmdLog(cmd,ropt)
                finalRC=self.chkDat5Rc(rc,verb=verb)

                # -- check if there and clean off
                #
                if(doKlean and os.path.isdir(ldir) and finalRC):
                    self.setKlean(ldir,ropt)

            else:
                # -- skip if not there...
                #
                if(ldir == None): 
                    print 'WWW ldir-local2dat5: ',ldir,' empty -- press...'
                    continue

                if(doKlean):
                    if(MF.ChkDir(ldir)):
                        print 'III doKlean=1 kill off empty dir'
                        cmd='rm -r -f %s'%(ldir)
                        mf.runcmd(cmd,'')

            MF.dTimer("putLocal2Dat5ModelDtgs: model: %s dtg: %s"%(model,dtg))
            print

    def putLocal2Dat6ModelDtgs(self,model,dtgs,ropt='',override=0,doKlean=0,verb=1):

        if(dtgs == None):
            if(hasattr(self,'localModelDtgs')):
                dtgs=self.localModelDtgs[model]
            else:
                print 'EEE(putLocal2Dat5Dtgs): dtgs=None and getAllDtgs() not run'
                sys.exit()

        elif(not(type(dtgs) is ListType)):
            dtgs=[dtgs]

        # -- get dtglocaldirs for this model
        #
        self.getDtgDirs(model)

        for dtg in dtgs:

            MF.sTimer("putLocal2Dat6ModelDtgs: model: %s dtg: %s"%(model,dtg))

            try:
                files=glob.glob("%s/*.grb?"%(self.dtgLocalDirs[dtg]))
                ldir=self.dtgLocalDirs[dtg]
                ldirthere=1
                if(len(files) == 0): ldirthere=0
            except:
                ldir=None
                ldirthere=0


            if(ldirthere):

                dat6dir=self.setDat6Dir(ldir,model,dtg)
                (sbdir,file)=os.path.split(ldir)
                sddir=ldir

                MF.ChkDir(dat6dir,'mk')

                # -- rsync over the data
                #
                cmd="rsync --protocol=29 -alv %s/ %s/"%(sddir,dat6dir)
                rc=MF.runcmdLog(cmd,ropt)
                finalRC=self.chkDat6Rc(rc,verb=verb)

                # -- check if there and clean off
                #
                if(doKlean and os.path.isdir(ldir) and finalRC):
                    self.setKlean(ldir,ropt)

            else:
                # -- skip if not there...
                #
                if(ldir == None): 
                    print 'WWW ldir-local2dat6: ',ldir,' empty -- press...'
                    continue

                if(doKlean):
                    if(MF.ChkDir(ldir)):
                        print 'III doKlean=1 kill off empty dir'
                        cmd='rm -r -f %s'%(ldir)
                        mf.runcmd(cmd,'')

            MF.dTimer("putLocal2Dat6ModelDtgs: model: %s dtg: %s"%(model,dtg))
            print


    def setLocalMssPaths(self,n2hash,tbdir,model,dtg):

        msspath=n2hash[(model,dtg)][0]
        ssiz=n2hash[(model,dtg)][1]
        (dir,file)=os.path.split(msspath)
        mssTOCfile="%s.toc"%(file)

        center=dir.split('/')[-3]

        omodel=model

        for dmodel in self.dmodels.keys():
            vmodel=self.dmodels[dmodel]
            if(model == vmodel): omodel=dmodel

        tdir="%s/%s/%s/%s"%(tbdir,center,omodel,dtg)
        mssTOCpath="%s/%s/%s/%s"%(tbdir,center,model,mssTOCfile)
        return(tdir,mssTOCpath,msspath)



    def setLocalHpssPaths(self,n2hash,tbdir,model,dtg):
        """ for nwp2 fields"""

        try:
            hpsspath=n2hash[(model,dtg)][0][0]
        except:
            return(None,None,None)

        ssiz=n2hash[(model,dtg)][0][1]
        hpssTOCfile="%s.idx"%(hpsspath)


        # -- get the center for the hpsspath dir
        #
        (dir,file)=os.path.split(hpsspath)
        dir=dir[0:len(dir)-7]
        tt=dir.split('/')
        center=tt[-2]
        model=tt[-1]


        try:
            dmodel=self.dmodels.keys()[self.dmodels.values().index(model)]
        except:
            print 'WWW in nwp.setLocalHpssPaths unable to find dmodel for model: ',model,' setting dmodel=model'
            dmodel=model

        tdir="%s/%s/%s/%s"%(tbdir,center,dmodel,dtg)
        hpssTOCpath="%s/%s/%s/%s"%(tbdir,center,model,hpssTOCfile)

        return(tdir,hpssTOCpath,hpsspath)


    def getMss2LocalModelDtgs(self,model,dtgs,tbdir=None,ropt='',override=0,verb=1,prestage=1):

        if(not(type(dtgs) is ListType)): dtgs=[dtgs]

        if(tbdir == None):
            if(type(self.sdirs) is ListType):
                tbdir=self.sdirs[0]
            else:
                tbdir=self.sdirs

        if(prestage and hasattr(self,'dsM')):
            self.n2models=self.dsM.data
        else:
            self.getMssModelDtgDirs(model,dtgs)

        n2hash=self.n2models
        moddtgs=n2hash.keys()
        moddtgs=mf.uniq(moddtgs)

        for dtg in dtgs:
            if (model,dtg) in moddtgs:
                if(override or self.localthere[dtg] == 0):
                    (tdir,mssTOCpath,msspath)=self.setLocalMssPaths(n2hash,tbdir,model,dtg)
                    if(tdir == None): continue
                    if(MF.ChkDir(tdir,'mk') == -1): sys.exit()
                    MF.ChangeDir(tdir)

                    print 'GGG(get2mss)    msspath: ',msspath
                    if(MF.ChkPath(mssTOCpath)):
                        print 'GGG(get2mss) mssTOCpath: ',mssTOCpath

                    if(prestage):
                        cmd="scp %s:%s/%s ."%(self.jetPreStageuRl,self.jetPreStageDir,file)
                        mf.runcmd(cmd,ropt)

                    else:
                        cmd="%s %s ."%(self.mssGetCmd,msspath)
                        mf.runcmd(cmd,ropt)

                    (dir,file)=os.path.split(msspath)
                    cmd="tar -xvf %s"%(file)
                    mf.runcmd(cmd,ropt)

                    cmd="rm -f %s"%(file)
                    mf.runcmd(cmd,ropt)


    def getJet2LocalModelDtgs(self,model,dtgs,tbdir=None,ropt='',override=0,verb=1):

        if(not(type(dtgs) is ListType)): dtgs=[dtgs]

        if(tbdir == None):
            if(type(self.sdirs) is ListType):
                tbdir=self.sdirs[0]
            else:
                tbdir=self.sdirs

        for dtg in dtgs:

            try:
                files=glob.glob("%s/*.grb?"%(self.dtgLocalDirs[dtg]))
                ldir=self.dtgLocalDirs[dtg]
                ldirthere=1
                if(len(files) == 0): ldirthere=0
            except:
                ldir=None
                ldirthere=0

            if(ldir == None):
                try:
                    ldir="%s/%s"%(self.modelLocalDirs[model],dtg)
                except:
                    print 'EEE(getJet2LocalModelDtgs) getting ldir from self.modelLocalDirs for model: ',model,' you might have to create the target dir: ',model
                    sys.exit()
                if(MF.ChkDir(ldir,'mk')): ldirthere=1


            jetdir=self.setJetDir(ldir,model,dtg)
            (sbdir,file)=os.path.split(ldir)
            sddir=ldir
            
            # -- make sure local dir there -- 20161227 -- /dat5 raid5 died :( so ldir might not be there
            #
            MF.ChkDir(sddir,'mk')

            # -- rsync over the data
            #
            MF.sTimer('getjet2local-%s-%s'%(model,dtg))
            cmd="rsync --protocol=29 -alv %s:%s/ %s/"%(self.jetScpuRl,jetdir,sddir)
            rc=MF.runcmdLog(cmd,ropt)
            finalRC=self.chkJetRc(rc)

            MF.ChangeDir(sddir)

            # -- check if there's a fim_* dir for Nwp2DataRtfim class
            #
            subdirs=os.listdir('.')
            if(len(subdirs) == 1 and mf.find(self.dbkeyLocal,'fim')):
                subdir=subdirs[0]
                MF.ChkDir(subdir,'mk')
                MF.ChangeDir(subdir)
                cmd="mv * ../."
                mf.runcmd(cmd,ropt)
                MF.ChangeDir('..')
                print os.getcwd()
                cmd="rmdir %s"%(subdir)
                mf.runcmd(cmd,ropt)


            print 'getJet2Local finalRC: ',finalRC,' for dtg: ',dtg,' model: ',model
            MF.dTimer('getjet2local-%s-%s'%(model,dtg))


    def getHpss2LocalModelDtgs(self,model,dtgs,tbdir=None,ropt='',override=0,verb=1,prestage=0):

        if(not(type(dtgs) is ListType)): dtgs=[dtgs]

        if(tbdir == None):
            if(type(self.sdirs) is ListType):
                tbdir=self.sdirs[0]
            else:
                tbdir=self.sdirs

        if(hasattr(self,'dsM')):
            self.n2models=self.dsM.data
        else:
            self.getHpssModelDtgDirs(model,dtgs)

        n2hash=self.n2models
        moddtgs=n2hash.keys()
        moddtgs=mf.uniq(moddtgs)

        for dtg in dtgs:

            if (model,dtg) in moddtgs:

                # -- if in inventory; may not be there after doput
                # -- check the local
                MF.sTimer("getHpss: %s %s"%(model,dtg))

                grbmask=self.setLocalGrbMask(dtg)
                if(grbmask != None):
                    files=glob.glob(grbmask)
                    nlocalfiles=len(files)
                else:
                    nlocalfiles=0
                    self.localthere[dtg]=0

                if(override or self.localthere[dtg] == 0 or nlocalfiles == 0):
                    (tdir,hpssTOCpath,hpsspath)=self.setLocalHpssPaths(n2hash,tbdir,model,dtg)
                    print 'GGG(get2hpss)       tdir: ',tdir

                    if(tdir == None): continue
                    if(MF.ChkDir(tdir,'mk') == -1): sys.exit()
                    MF.ChangeDir(tdir)

                    print 'GGG(get2hpss)    hpsspath: ',hpsspath
                    if(MF.ChkPath(hpssTOCpath)):
                        print 'GGG(get2hpss) hpssTOCpath: ',hpssTOCpath

                    if(prestage):
                        cmd="scp %s:%s/%s ."%(self.jetPreStageuRl,self.jetPreStageDir,file)
                        mf.runcmd(cmd,ropt)

                    else:
                        cmd="%s %s ."%(self.hpssGetCmd,hpsspath)
                        mf.runcmd(cmd,ropt)

                    (dir,file)=os.path.split(hpsspath)
                    cmd="tar -xvf %s"%(file)
                    mf.runcmd(cmd,ropt)

                    cmd="rm -f %s"%(file)
                    mf.runcmd(cmd,ropt)
                else:
                    print 'WWW(getHpss2LocalModelDtgs) will NOT get model: ',model,' dtg: ',dtg,' because localthere > 0 and override != 1'

                MF.dTimer("getHpss: %s %s"%(model,dtg))


    def setMssMask(self,model,dtg):
        smask="%s/*/%s/%s/%s*%s*tar"%(self.mssbdir,model,dtg[0:6],model,dtg)
        return(smask)

    def setHpssMask(self,model,dtg):
        smask="%s/%s/%s/%s*%s*tar"%(self.hpssbdir,model,dtg[0:6],model,dtg)
        return(smask)

    def setHpssInvMask(self):
        
        # -- get listing of dirs
        #
        
        smasks=[]
        cmd='''%s -ld "%s/*"'''%(self.hpssLsCmd,self.hpssbdir)
        output3=MF.runcmdLog(cmd)
        for o in output3:
            tt=o.split()
            if(len(tt) == 9 and tt[0][0] == 'd'):
                model=tt[-1]
                smask="%s/%s/??????"%(self.hpssbdir,model)
                smasks.append(smask)
        
        cmd='''%s -ld "%s/*"'''%(self.hpssLsCmd,self.hpssbdirOld)
        output3=MF.runcmdLog(cmd)
        for o in output3:
            tt=o.split()
            if(len(tt) == 9 and tt[0][0] == 'd'):
                model=tt[-1]
                smask="%s/%s/??????"%(self.hpssbdirOld,model)
                smasks.append(smask)
                
        return(smasks)

    def getHpssModelDtgDirs(self,model,lsdtgs,verb=0,override=0):

        n2models={}

        for dtg in lsdtgs:

            smask=self.setHpssMask(model,dtg)
            print 'SSSSS(getHpssModelDtgDirs) smask: ',smask
            cmd='''%s -lh "%s"'''%(self.hpssLsCmd,smask)
            lines=MF.runcmdLog(cmd)

            for line in lines:
                if(mf.find(line,'No such')): continue
                tt=line.split()
                if(len(tt) > 0):
                    siz=tt[len(tt)-5]
                    path=tt[len(tt)-1]
                    tt2=path.split('/')[-1]
                    n2model=tt2.split('.')[0]
                    n2models[n2model,dtg]=(path,siz)


        self.n2models=n2models


    def getMssModelDtgDirs(self,model,lsdtgs,verb=0,override=0):

        n2models={}

        for dtg in lsdtgs:

            smask=self.setMssMask(model,dtg)
            print 'SSSSSSSSSSSSSSSSS(getMssModelDtgDirs) mss',smask
            cmd="%s -lh %s"%(self.mssLsCmd,smask)
            lines=MF.runcmdLog(cmd)

            for line in lines:
                if(mf.find(line,'No such')): continue
                tt=line.split()
                if(len(tt) > 0):
                    siz=tt[len(tt)-5]
                    path=tt[len(tt)-1]
                    tt2=path.split('/')[-1]
                    n2model=tt2.split('.')[0]
                    n2models[n2model,dtg]=(path,siz)


        self.n2models=n2models


    def chkMssPathInv(self,model,dtg,verb=1,domss=0):

        if(self.dsM == None):
            gotit=0
            siz=0
            return(gotit,siz)
        
        if(hasattr(self,'dsM') and self.dsM != None):
            self.n2models=self.dsM.data
        elif(domss):
            self.getMssModelDtgDirs(model,dtg)
        else:
            self.n2models=[]

        if( len(self.n2models) > 0):

            n2hash=self.n2models
            moddtgs=n2hash.keys()
            moddtgs.sort()

            gotit=0
            siz=0
            for moddtg in moddtgs:
                (mmod,mdtg)=moddtg
                if(model == mmod and (dtg == mdtg or dtg == '1776070400') ):
                    gotit=1
                    for n2 in n2hash[moddtg]:
                        path=n2[0]
                        siz=n2[1]
                        print 'MSS_YYY: %10s %10s'%(model,mdtg),"%-80s   siz: %s"%(path,siz)

            if(not(gotit) and verb):
                print 'MSS_NNN: %10s %10s %s'%(model,dtg,self.suffixMMMNNN)

        else:

            gotit=0
            siz=0

            if(verb): print 'MSS_NNN: %10s %10s %s'%(model,dtg,self.suffixMMMNNN)
            if(w2.onWjet or w2.onTheia):
                print 'EEE (chkMssPathInv): no mss data in self.dsM.data -- problem in mss/nwp'
                sys.exit()


        return(gotit,siz)



    def lsMssDtgDirs(self,model,dtgs):

        if(dtgs == 'all'): dtgs=['1776070400']
        if(hasattr(self,'dsM')):
            self.n2models=self.dsM.data
        else:
            self.getMssModelDtgDirs(model,dtgs)

        if( len(self.n2models) > 0):

            n2hash=self.n2models
            moddtgs=n2hash.keys()
            moddtgs.sort()

            # -- if no dtgs use moddtgs to get all available for the model
            #
            if(dtgs == None or len(dtgs) == 0):
                dtgs=[]
                for moddtg in moddtgs:
                    (mmod,dtg)=moddtg
                    if(mmod == model):
                        dtgs.append(dtg)
                dtgs=mf.uniq(dtgs)

            for dtg in dtgs:
                goit=0
                for moddtg in moddtgs:
                    (mmod,mdtg)=moddtg
                    if(model == mmod and (dtg == mdtg or dtg == '1776070400') ):
                        goit=1
                        n2moddtgs=n2hash[moddtg]
                        for n2moddtg in n2moddtgs:
                            path=n2moddtg[0]
                            siz=n2moddtg[1]
                            print 'MSS_YYY: %10s %10s'%(model,mdtg),"%-80s   siz: %s"%(path,siz)

                if(not(goit)):
                    print 'MSS_NNN: %10s %10s %s'%(model,dtg,self.suffixMMMNNN)


        else:

            for dtg in dtgs:
                print 'MSS_NNN: %10s %10s %s'%(model,dtg,self.suffixMMMNNN)

        print




    def lsAllMssDtgs(self,model,rmodel=None):


        if(hasattr(self,'AllMssModDtgs')):

            models=self.AllMssModDtgs.keys()

            if(rmodel == None):  rmodel=model

            if(model in models):
                try:
                    dtgs=self.AllMssModDtgs[model]
                except:
                    dtgs=[]

                dtgs.sort()
                dtgout=MF.makeDtgsString(dtgs)

                omodel="%10s : %-10s"%(rmodel,model)
                if(diag):
                    print "AAA_MMM: %s %s"%(omodel,dtgout)
                    print



    def chkMssDir(self,dir,diropt='mk',verb=0):

        cmd="%s -ld %s"%(self.mssLsCmd,dir)
        output=MF.runcmdLogOutput(cmd)

        if(verb):
            print 'OOOBBB'
            print 'output: ',output
            print 'OOOAAA'

        if(mf.find(output,'error retrieving current directory')):
            print 'WWW(nwp.chkMssDir:error retrieving) dir: ',dir
            return(0)


        if( mf.find(output,'No such') and not(mf.find(output,dir[4:])) ):
            if(verb): print "dir  (not there): ",dir
            if(diropt == 'mk' or diropt == 'mkdir'):
                try:
                    os.system('mssMkdir -p %s'%(dir))
                except:
                    print 'EEE unable to mkdir: ',dir,' in mf.ChkDir, return -1 ...'
                    return(-1)
                print 'dir     (MADE): ',dir
                return(2)
            else:
                return(0)
        else:
            
            if(verb):  print "dir      (there): ",dir
            return(1)


    def chkHpssDir(self,dir,diropt='mk',verb=0):

        cmd="%s -ld %s"%(self.hpssLsCmd,dir)
        output=MF.runcmdLogOutput(cmd)
        #-- strip out shell-init: error 
        outputLines=''
        for oline in output.splitlines(True):
            if(mf.find(oline,'shell-init: error')):
                continue
            else:
                outputLines=outputLines+oline
                
        if(verb):
            print 'OOOBBB'
            print 'outputLines: '
            for oline in outputLines.splitlines():
                print oline
            print 'OOOAAA'

        if(mf.find(outputLines,'error retrieving current directory')):
            print 'WWW(nwp.chkHpssDir:error retrieving) dir: ',dir
            return(0)
            

        if( mf.find(outputLines,'No such') ):
            if(verb): print "dir  (not there): ",dir
            if(diropt == 'mk' or diropt == 'mkdir'):
                try:
                    os.system('%s -p %s'%(self.hpssMkdirCmd,dir))
                except:
                    print 'EEE unable to mkdir: ',dir,' in mf.ChkDir, return -1 ...'
                    return(-1)
                print 'dir     (MADE): ',dir
                return(2)
            else:
                return(0)
        else:
            if(verb):
                print "dir      (there): ",dir
            return(1)



    def chkMssPath(self,msspath,verb=0):

        cmd='%s -l %s'%(self.mssLsCmd,msspath)
        try:
            output = MF.runcmdLogOutput(cmd)
            if(verb==2): print 'output: ',output

            if(mf.find(output,'No such')):
                rc=-1
            else:
                rc=int(output.split()[4])
        except:
            return(-999)

        siz=float(rc)/(1024*1024*1024)
        if(verb): print 'msspath: ',msspath,' siz: %6.2f GB'%(siz)
        return(siz)


    def chkHpssPath(self,hpsspath,verb=0):

        cmd="%s -la %s"%(self.hpssLsCmd,hpsspath)
        # -- 20130729 -- output of hsi -q changed -- not quiet anymore?
        # code to check
        try:
            output = MF.runcmdLogOutput(cmd)
            if(verb==2): print 'output: ',output

            if(mf.find(output,'No such')):
                rc=-999*1024*1024*1024
                
            elif(mf.find(output,'Connection refused')):
                print 'WWW connection to hpss broke...retrying output ',output
                return(-1)
            
            else:
                tt=output.split()
                if(len(tt) > 10): siz=tt[-5]
                else:             siz=tt[4]
                if(not(siz.isdigit())):
                    print 'EEE error getting size in chkHpssPath tt: ',tt
                    sys.exit()
                rc=int(siz)
        except:
            return(-99999)

        siz=float(rc)/(1024*1024*1024)
        if(verb): print 'hpsspath: ',hpsspath,' siz: %6.2f GB'%(siz)
        return(siz)



    def chkMssSize(self,msspath,verb=0):

        siz=self.chkMssPath(msspath,verb=verb)
        return(siz)



    def chkHpssSize(self,hpsspath,verb=0):

        siz=self.chkHpssPath(hpsspath,verb=verb)
        return(siz)



    def getDtgs4localModelDtgs(self,model,tdtgs,listNNN=1):

        dtgs=[]
        try:
            moddtgs=self.localModelDtgs[model]
        except:
            return(dtgs)
        
        # -- clean up moddtgs? of ecmt -W on kishou got -rw-r--r--
        fmoddtgs=[]
        for moddtg in moddtgs:
            if(len(moddtg) == 10 and not(mf.find(moddtg,'-'))):
                fmoddtgs.append(moddtg)
        moddtgs=fmoddtgs

        if(type(tdtgs) != ListType and mf.find(tdtgs,'all') ):
            aa=tdtgs.split('.')
            if(len(aa) == 2):
                bdtgs=mf.dtg_dtgopt_prc(aa[1])
                if(len(bdtgs) > 1):
                    print 'EEE in getDtgs4localModelDtgs, tdtgs: ',tdtgs,' must be in form all.SSS where SSS= single dtg'
                    sys.exit()
                else:
                    bdtg=bdtgs[0]
                    for mdtg in moddtgs:
                        dfdtg=mf.dtgdiff(mdtg,bdtg)
                        if(dfdtg >= 0): dtgs.append(mdtg)
            else:
                if(listNNN):
                    if(len(moddtgs) >= 2):
                        # -- logic to find the dtginc
                        #
                        dtginc=mf.dtgdiff(moddtgs[-2],moddtgs[-1])
                        if(dtginc%24== 0):    dtginc=24
                        elif(dtginc%12 == 0): dtginc=12
                        elif(dtginc%6 == 0):  dtginc=6
                        dtgs=mf.dtg_dtgopt_prc("%s.%s.%d"%(moddtgs[0],moddtgs[-1],dtginc))
                    else:
                        dtgs=moddtgs
                else:
                    dtgs=moddtgs

        else:

            for tdtg in tdtgs:
                if(tdtg in moddtgs):
                    dtgs.append(tdtg)

        return(dtgs)


    def getAllLocalDtgs(self,modelopt,verb=0):

        self.localModelDtgs={}
        kk=self.center_model_dtgs.keys()

        if(modelopt == 'all'):
            models=self.allmodels
        else:
            models=modelopt.split(',')


        for model in models:

            for k in kk:

                if(k[1] == model):

                    rc=self.center_model_dtgs[k]
                    if(type(rc) is TupleType):
                        (dtgs,itaus)=rc
                    else:
                        dtgs=rc
                        itaus={}
                    dtgs.sort()
                    dtgout=MF.makeDtgsString(dtgs)
                    if(verb): print '111111111111 ',model,dtgout
                    
                    self.localModelDtgs[model]=dtgs


    def lsAllLocalDtgs(self,modelopt,rmodel=None,verb=0):

        self.getAllLocalDtgs(modelopt,verb=verb)

        #models=self.localModelDtgs.keys()

        #for model in models: 
            #dtgs=self.localModelDtgs[model]
            #if(verb): print model,dtgs



#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# -- w2flds class
#
class W2Models(MFbase):

    def __init__(self,sdir='/dat2/w21/dat/nwp2',verb=0):

        models=[]
        allmodels=[]
        modcen={}
        idirs=glob.glob("%s/*/"%(sdir))

        for idir in idirs:

            (base,ifile)=os.path.split(idir)
            tt=base.split('/')
            center=tt[-1]
            dmodel=tt[-1]
            model=dmodel
            # -- filter out SCM versions of GFS runs
            #
            if(not(mf.find(idir,'gfsgf')) and
               not(mf.find(idir,'gfss')) and
               not(mf.find(idir,'gfssa'))
               ):
                models.append([dmodel,model])   
                allmodels.append(model)
            MF.loadDictList(modcen,center,[dmodel,model])
            if(verb): print center,dmodel,model

        centers=modcen.keys()

        if(w2.curuSer == 'rtfim'): 
            allmodels=['fim7h','fim7xh','fim9h','fimens','fimxh']
            allmodels=['fim7h','fim7xh']
            modcen={}
            models=[]
            for dmodel in allmodels:
                center=dmodel
                models.append([dmodel,dmodel])
                MF.loadDictList(modcen,center,[dmodel,dmodel])
            centers=modcen.keys()

        if(verb):
            for center in centers:
                print 'ccc ',center,modcen[center]
                
            for model in models:
                print 'mmm ',model
            
        self.modcen=modcen
        self.models=models
        self.allmodels=allmodels
        self.dcenters=centers



class Nwp2DataW2flds(Nwp2Data):

    sbdir4='/dat4/nwp2'
    sdir4='%s/w2flds/dat'%(sbdir4)

    sbdir5='/dat5/dat/nwp2'
    sdir5='%s/w2flds/dat'%(sbdir5)

    sbdir6='/dat6/dat/nwp2'
    sdir6='%s/w2flds/dat'%(sbdir6)

    sbdir0='/data/amb/users/fiorino/w21/dat/nwp2'
    sdir0='%s/w2flds/dat'%(sbdir0)

    sbdir2='/dat2/w21/dat/nwp2/w2flds/dat'
    sdir2='%s/w2flds/dat'%(sbdir2)

    sbdirE2='/FWV2/dat2/nwp2'
    sdirE2='%s/w2flds/dat'%(sbdirE2)

    mssbdir='/mss/jet/projects/fim/fiorino/nwp2/w2flds/dat'
    hpssbdir='/%s/fim/fiorino/nwp2/w2flds/dat'%(hpssHead)
    hpssbdirOld='/%s/fim/fiorino/nwp2/w2flds/dat'%(hpssHeadOld)
    
    if(w2.curuSer == 'rtfim'):
        mssbdir='/mss/jet/projects/fim/rtfim/nwp2/w2flds/dat'
        hpssbdir="/5year/BMC/fim/rtfim/nwp2/w2flds/dat"

    sdirs=[sdir2,sdirE2,sdir4]

####    sdirJ2='/mnt/lfs2/projects/fim/fiorino/w21/dat/nwp2/w2flds/dat'
    sdirJ2='/mnt/lfs1/projects/fim/fiorino/w21/dat/nwp2/w2flds/dat'
    if(w2.onZeus):
        sdirJ2='/scratch1/portfolios/BMC/fim/fiorino/w21/dat/nwp2/w2flds/dat'

    dmodels=Nwp2Models().dmodels

    suffixLLLNNN='''>>>-----WW22lll-nnn------>>>'''
    suffixMMMNNN='''<<<-----WW22MMM-nnn------<<<'''

    dbkeyLocal='local'
    dbkeyMss='mss'

    def __init__(self,sdirs=None,sdiropt=None,mssbdir=None,verb=0,
                 overrideL=0,
                 overrideM=0,
                 updateOnly=0,
                 doremoteRsync=1,
                 dbname='invW2flds',
                 dojet=0):

        self.dtgDirs=[]
        self.center_model_dtgs={}
        self.verb=verb
        self.updateOnly=updateOnly

        self.sdiropt=sdiropt
        self.dbname="%s-%s"%(dbname,sdiropt)
        if(w2.curuSer == 'rtfim'): self.dbname="%s-RTFIM-%s"%(dbname,sdiropt)

        self.dbfile="%s.pypdb"%(self.dbname)
        self.dbfileJet="%s-datj2.pypdb"%(dbname)

        self.dbfileLocal="%s-local.pypdb"%(self.dbname)
        self.dbfileMss="%s-mss.pypdb"%(self.dbname)
        self.dbfileLocalJet="%s-datj2-local.pypdb"%(dbname)
        self.dbfileMssJet="%s-datj2-mss.pypdb"%(dbname)


        if(mssbdir != None): self.mssbdir=mssbdir

        if(sdiropt == 'datE2'):
            self.sdirs=self.sdirE2
            self.sbdirs=self.sbdirE2
        elif(sdiropt == 'dat4'):
            self.sdirs=self.sdir4
            self.sbdirs=self.sbdir4
        elif(sdiropt == 'dat5'):
            self.sdirs=self.sdir5
            self.sbdirs=self.sbdir5
        elif(sdiropt == 'dat6'):
            self.sdirs=self.sdir6
            self.sbdirs=self.sbdir6
        elif(sdiropt == 'dat0'):
            self.sdirs=self.sdir0
            self.sbdirs=self.sbdir0
        elif(sdiropt == 'dat2'):
            self.sdirs=self.sdir2
            self.sbdirs=self.sbdir2
        elif(sdiropt == 'datj2'):
            self.sdirs=self.sdirJ2
        else:
            print 'EEE invalid sdiropt for nwp2dataw2flds: ',sdiropt
            sys.exit()

        n2m=W2Models(self.sdirs)
        self.allmodels=n2m.allmodels
        self.dcenters=n2m.dcenters
        self.dmodcen=n2m.modcen

        self.setDSs(overrideL,overrideM,doremoteRsync=doremoteRsync,verb=verb,dojet=dojet)

        if(overrideL or hasattr(self,'overrideL')): self.invLocal(verb=verb,overrideKey1='w2flds')
        if(overrideM):
            if(w2.onWjet or w2.onTheia):
                self.invHpssJet(verb=verb)

        try:
            self.n2models=self.dsM.data
        except:
            self.n2models=self.allmodels

        try:
            self.center_model_dtgs=self.dsL.data
        except:
            print 'EEE(nwp.Nwp2DataW2flds.__init__): cannot set self.center_model_dtgs...sayonoara'
            sys.exit()


        AllMssModDtgs={}
        n2hash=self.dsM.data
        moddtgs=n2hash.keys()

        for moddtg in moddtgs:
            (mmod,dtg)=moddtg
            MF.appendDictList(AllMssModDtgs,mmod,dtg)

        self.AllMssModDtgs=AllMssModDtgs


    def invLocalSingle(self,singleModel=None,overrideKey1='w2flds',verb=1):
        self.invLocal(overrideKey1=overrideKey1,verb=verb,singleModel=singleModel)


    def getsubdirs(self,sdirs,exclude=['ensFC']):

        if(type(sdirs) != ListType): sdirs=[sdirs]
        subdirs={}
        for sdir in sdirs:
            ssdirs=os.listdir(sdir)
            for ss in ssdirs:
                if(
                    (mf.find(ss[0],'f') and ss != 'fim8') or
                    mf.find(ss,'-1') or
                    mf.find(ss,'.DS_') or
                    mf.find(ss,'.toc') or
                    ss in exclude
                    ): continue
                spath="%s/%s"%(sdir,ss)
                if(
                    os.path.islink(spath) or
                    not(os.path.isdir(spath))
                    ): continue

                MF.appendDictList(subdirs,ss,spath)

        return(subdirs)



    def setMssDir(self,ldir,model,dtg):
        mssdir="%s/%s/%s"%(self.mssbdir,model,dtg[0:6])
        print 'PPP(put2mss)       ldir: ',ldir
        print 'PPP(put2mss)     mssdir: ',mssdir
        rc=self.chkMssDir(mssdir,verb=0)
        mssfile="%s.%s.%s.w2flds.tar"%(model,dtg,w2center)
        return(mssdir,mssfile)

    def setHpssDir(self,ldir,model,dtg,verb=1):
        hpssdir="%s/%s/%s"%(self.hpssbdir,model,dtg[0:6])
        rc=self.chkHpssDir(hpssdir,verb=verb)
        # -- cycling if fails
        #
        if(rc == 0):
            ntry=1
            ntryMax=3
            trySleep=15
            while(ntry <= ntryMax):
                print
                print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII--------------------------retry chkMssDir..."
                print
                time.sleep(trySleep)  
                rc=self.chkHpssDir(hpssdir,verb=verb)
                if(rc > 0):
                    ntry=999
                else:
                    ntry=ntry+1
         
        hpssfile="%s.%s.%s.w2flds.tar"%(model,dtg,w2center)
        return(rc,hpssdir,hpssfile)
        

    def setMssMask(self,model,dtg):
        smask="%s/%s/%s/%s*%s*tar"%(self.mssbdir,model,dtg[0:6],model,dtg)
        return(smask)

    def setMssInvMask(self):
        
        smasks=[]
        for model in self.allmodels:
            smasks.append("%s/%s/%s/"%(self.mssbdir,model,'??????'))
        return(smasks)




    def setLocalHpssPaths(self,n2hash,tbdir,model,dtg):
        """ for w2flds """

        try:
            hpsspath=n2hash[(model,dtg)][0][0]
        except:
            return(None,None,None)

        ssiz=n2hash[(model,dtg)][0][1]
        hpssTOCfile="%s.idx"%(hpsspath)

        tdir="%s/%s/%s"%(tbdir,model,dtg)
        hpssTOCpath="%s/%s/%s"%(tbdir,model,hpssTOCfile)
        return(tdir,hpssTOCpath,hpsspath)



    def setLocalMssPaths(self,n2hash,tbdir,model,dtg):

        try:
            msspath=n2hash[(model,dtg)][0]
        except:
            return(None,None,None)
        ssiz=n2hash[(model,dtg)][1]
        (dir,file)=os.path.split(msspath)
        mssTOCfile="%s.toc"%(file)

        tdir="%s/%s/%s"%(tbdir,model,dtg)
        mssTOCpath="%s/%s/%s"%(tbdir,model,mssTOCfile)
        return(tdir,mssTOCpath,msspath)

    def setKlean(self,sddir,ropt):
        """ don't kill off entire dir; keep tctrk/ with tracker .pyp*"""
        print 'WWW(putLocal2MssModelDtgs:w2flds): doKlean of sddir: ',sddir
        cmd="rm -f -r %s"%(sddir)
        mf.runcmd(cmd,ropt)



#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# -- rtfim class
#

class Nwp2DataRtfim(Nwp2DataW2flds):

    from FM import rtfimRuns
    fR=rtfimRuns()

    sdir0='/data/amb/users/fiorino/w21/dat/nwp2/rtfim/dat'
    sdirE2='/FWV2/dat2/nwp2/rtfim/dat'
    sdir4='/dat4/nwp2/rtfim/dat'
    sdir2='/dat2/w21/dat/nwp2/rtfim/dat'
    sdirg='/data/global/dat/nwp2/rtfim/dat'

    sbdir5='/dat5/dat/nwp2'
    sdir5='%s/rtfim/dat'%(sbdir5)

    sbdir6='/dat6/dat/nwp2'
    sdir6='%s/rtfim/dat'%(sbdir6)

    sdirs=[sdir2,sdirE2,sdir4]
    mssbdir='/mss/jet/projects/fim/fiorino/rtfim'
    hpssbdir='/%s/fim/fiorino/rtfim'%(hpssHead)
    hpssbdirOld='/%s/fim/fiorino/rtfim'%(hpssHeadOld)
    if(w2.curuSer == 'rtfim'):
        mssbdir='/mss/jet/projects/fim/rtfim/rtfim'
        hpssbdir="/5year/BMC/fim/rtfim/rtfim"


####    sdirJR='/mnt/lfs2/projects/fim/fiorino/rtfim/dat'
    sdirJR='/mnt/lfs1/projects/fim/fiorino/rtfim/dat'
    if(w2.onZeus):
        sdirJR='/scratch1/portfolios/BMC/fim/fiorino/w21/dat/nwp2/rtfim/dat'

####    jetbdir='/lfs2/projects/fim/fiorino/rtfim/dat'
    jetbdir='/lfs1/projects/fim/fiorino/rtfim/dat'

    dmodels=Nwp2Models().dmodels

    suffixLLLNNN='''>>>-----FIMlll-nnn------>>>'''
    suffixMMMNNN='''<<<-----FIMMMM-nnn------<<<'''

    dbkeyLocal='local-rtfim'
    dbkeyMss='mss-rtfim'


    def __init__(self,sdirs=None,sdiropt=None,mssbdir=None,verb=0,
                 overrideL=0,
                 overrideM=0,
                 updateOnly=0,
                 doremoteRsync=1,
                 dbname='invRtfim',
                 dojet=0):

        self.dtgDirs=[]
        self.center_model_dtgs={}
        self.verb=verb
        self.updateOnly=updateOnly

        self.sdiropt=sdiropt
        self.dbname="%s-%s"%(dbname,sdiropt)
        if(w2.curuSer == 'rtfim'): self.dbname="%s-RTFIM-%s"%(dbname,sdiropt)

        self.dbfile="%s.pypdb"%(self.dbname)
        self.dbfileJet="%s-datjr.pypdb"%(dbname)

        self.dbfileLocal="%s-local.pypdb"%(self.dbname)
        self.dbfileMss="%s-mss.pypdb"%(self.dbname)
        self.dbfileLocalJet="%s-datjr-local.pypdb"%(dbname)
        self.dbfileMssJet="%s-datjr-mss.pypdb"%(dbname)

        if(mssbdir != None): self.mssbdir=mssbdir

        if(sdiropt == 'datE2'):
            self.sdirs=self.sdirE2
            self.sbdirs=self.sdirE2
        elif(sdiropt == 'dat4'):
            self.sdirs=self.sdir4
            self.sbdirs=self.sdir4
        elif(sdiropt == 'dat0'):
            self.sdirs=self.sdir0
            self.sbdirs=self.sdir0
        elif(sdiropt == 'dat2'):
            self.sdirs=self.sdir2
            self.sbdirs=self.sdir2
        elif(sdiropt == 'dat5'):
            self.sdirs=self.sdir5
            self.sbdirs=self.sdir5
        elif(sdiropt == 'dat6'):
            self.sdirs=self.sdir6
            self.sbdirs=self.sdir6
        elif(sdiropt == 'datg'):
            self.sdirs=self.sdirg
            self.sbdirs=self.sdirg
        elif(sdiropt == 'datjr'):
            self.sdirs=self.sdirJR
            self.sbdirs=self.sdirJR
        else:
            print 'EEE invalid sdiropt for nwp2datartfim: ',sdiropt
            sys.exit()

        self.setDSs(overrideL,overrideM,doremoteRsync=doremoteRsync,verb=verb,dojet=dojet)

        try:
            self.center_model_dtgs=self.dsL.data
            if(len(self.center_model_dtgs) == 0): overrideL=1
        except:
            overrideL=1
            if((w2.onWjet or w2.onTheia) and overrideM):
                overrideM=1
            else:
                overrideM=0

        if(overrideL):
            s1dirs=self.getsubdirs(self.sdirs)
            self.allmodels=[]
            for s1 in s1dirs.keys():
                self.allmodels.append(s1)

            self.invLocal(key1='rtfim',verb=1)
            self.n2models=self.allmodels

        if(overrideM and (w2.onWjet or w2.onTheia)): self.invHpssJet(verb=verb)


        # -- for rtfim and all(?) -  n2models based on local
        #
        
        self.center_model_dtgs=self.dsL.data
        kk=self.center_model_dtgs.keys()

        n2models={}
        allmodels=[]

        for k in kk:
            fmodel=k[1].strip()
            rmodel=self.fR.getMyRun(fmodel)
            allmodels.append(rmodel)
            n2models[rmodel]=fmodel

        self.allmodelsLocal=mf.uniq(allmodels)


        # -- use mss...
        #
        n2hash=self.dsM.data
        n2models={}
        allmodels=[]

        for k in n2hash:
            fmodel=k[0].strip()
            rmodel=self.fR.getMyRun(fmodel)
            allmodels.append(rmodel)
            n2models[rmodel]=fmodel

        allmodels=mf.uniq(allmodels)

        self.n2models=n2models
        self.allmodels=allmodels

        AllMssModDtgs={}

        moddtgs=n2hash.keys()

        for moddtg in moddtgs:
            (mmod,dtg)=moddtg
            MF.appendDictList(AllMssModDtgs,mmod,dtg)

        self.AllMssModDtgs=AllMssModDtgs



    def invLocalSingle(self,singleModel=None,verb=0):
        self.invLocal(key1=singleModel,verb=verb)


    def setinvLocalMask(self,s2dir,dtg):
        # -- reorg the target dir to be consistent with kaze/kishou
        #
        if(w2.onWjet or w2.onTheia):
            invmask1="%s/%s/*/*.grb?"%(s2dir,dtg)
            invmask="%s/%s/*.grb?"%(s2dir,dtg)
        else:
            invmask="%s/%s/*.grb?"%(s2dir,dtg)

        if(w2.curuSer == 'rtfim'):
            invmask1="%s/%s/*/*.ctl"%(s2dir,dtg)
            invmask="%s/%s/*.ctl"%(s2dir,dtg)

        # handle case where data come from kishou/kaze, e.g., from zeus
        #
        files=glob.glob(invmask)
        if(len(files) == 0 and (w2.onWjet or w2.onTheia)):
            invmask=invmask1
        return(invmask)


    def invLocal(self,key1='rtfim',dotaus=1,verb=1):

        s1dirs=self.getsubdirs(self.sdirs)

        for s1 in s1dirs.keys():
            omodel=s1
            if(not(omodel in self.allmodels)):
                continue
            else:
                print'III(nwp.rtfim.invLocal) doing model: ',omodel

            if(not(self.updateOnly)): taus={}

            s2dirs=s1dirs[omodel]
            s2dirs.sort()

            for s2dir in s2dirs:

                taus={}
                try:
                    (idtgs,itaus)=self.center_model_dtgs[key1,omodel,s2dir]
                except:
                    itaus=None
                    None

                MF.sTimer('%s:%s'%(key1,s2dir))
                s3dirs=self.getsubdirs(s2dir)
                dtgs=s3dirs.keys()
                dtgs.sort()

                nglob=0
                if(dotaus):
                    for dtg in dtgs:

                        invmask=self.setinvLocalMask(s2dir,dtg)
                        ###print 'iiiiiii ',omodel,dtg,invmask,itaus

                        dtaus=[]
                        doglob=0
                        if(itaus == None or len(itaus) == 0):
                            doglob=1
                        else:
                            try:
                                dtaus=itaus[dtg]
                            except:
                                doglob=1

                        if(not(self.updateOnly)): doglob=1

                        if(doglob):

                            try:
                                files=glob.glob(invmask)
                                dtaus=self.gettaus(files)
                                nglob=nglob+1
                            except:
                                files=None
                                dtaus=[]


                        dtaus=mf.uniq(dtaus)
                        taus[dtg]=dtaus


                if(verb): print len(dtgs),s1,s2dir,omodel,nglob
                MF.dTimer('%s:%s'%(key1,s2dir))

            self.center_model_dtgs[key1,omodel,s2dir]=(dtgs,taus)

        print 'rtfim len: ',len(self.center_model_dtgs)
        self.dsL.data=self.center_model_dtgs
        self.DSsL.putDataSet(self.dsL,key=self.dbkeyLocal,verb=1)
        self.DSsL.closeDataSet()


    def setJetDir(self,ldir,model,dtg):
        center=ldir.split('/')[-3]
        jetdir=ldir.replace(self.sbdirs,self.jetbdir)

        print 'PPP(setJetDir.rtfim)       ldir: ',ldir
        print 'PPP(setJetDir.rtfim)     jetdir: ',jetdir
        return(jetdir)


    def setMssInvMask(self):
        smasks=[]
        smasks.append("%s/%s/"%(self.mssbdir,'*'))
        return(smasks)

    def setHpssDir(self,ldir,model,dtg,verb=1):
        hpssdir="%s/%s"%(self.hpssbdir,model)
        rc=self.chkHpssDir(hpssdir,verb=verb)
        # -- cycling if fails
        #
        if(rc == 0):
            ntry=1
            ntryMax=3
            trySleep=15
            while(ntry <= ntryMax):
                print
                print "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII--------------------------retry chkMssDir..."
                print
                time.sleep(trySleep)  
                rc=self.chkHpssDir(hpssdir,verb=verb)
                if(rc > 0):
                    ntry=999
                else:
                    ntry=ntry+1
                    
        hpssfile="%s.%s.tar"%(model,dtg)
        return(rc,hpssdir,hpssfile)
        

    def getAllLocalDtgs(self,verb=0):

        self.localModelDtgs={}
        kk=self.center_model_dtgs.keys()

        self.allmodelsLocal=[]

        for k in kk:
            model=k[1]
            self.allmodelsLocal.append(model)
            rc=self.center_model_dtgs[k]

            if(type(rc) is TupleType):
                (dtgs,taus)=rc
            else:
                dtgs=rc
                taus={}

            dtgs.sort()
            self.localModelDtgs[model]=dtgs
            dtgout=MF.makeDtgsString(dtgs)
            if(verb): print model,dtgout


    def lsAllLocalDtgs(self,fimrun,rmodel=None,verb=0):

        self.getAllLocalDtgs(verb=verb)

        fimruns=self.localModelDtgs.keys()
        fimruns=MF.uniq(fimruns)

        if(fimrun == 'all'):
            for frun in fimruns:
                dtgs=self.localModelDtgs[frun]
                dtgout=MF.makeDtgsString(dtgs)
                try:
                    model=self.fR.getMyRun(frun)
                except:
                    model='uunnkkoowwnn'
                print "%-30s %-30s %s"%(frun,model,dtgout)

            return


        if(fimrun in fimruns):
            dtgs=self.localModelDtgs[fimrun]
            dtgout=MF.makeDtgsString(dtgs)

            if(rmodel == None):  rmodel=fr.getRmodel(fimrun)
            ofimrun="%25s : %-40s"%(rmodel,fimrun)
            if(diag): print "AAA_LLL: %s %s"%(ofimrun,dtgout)


    def lsAllMssDtgs(self,fimrun,rmodel=None):

        fimruns=self.allmodels

        if(hasattr(self,'AllMssModDtgs')):

            if(rmodel == None):  rmodel=fr.getRmodel(fimrun)

            if(rmodel in fimruns):
                try:
                    dtgs=self.AllMssModDtgs[fimrun]
                except:
                    dtgs=[]

                dtgs.sort()
                dtgout=MF.makeDtgsString(dtgs)

                ofimrun="%25s : %-40s"%(rmodel,fimrun)
                if(diag):
                    print "AAA_MMM: %s %s"%(ofimrun,dtgout)
                    print


    def getlocalModels(self,tdtgs):

        self.getAllLocalDtgs()

        fimruns=[]
        models=[]
        frs=self.localModelDtgs.keys()
        frs=MF.uniq(frs)

        for fr in frs:
            moddtgs=self.localModelDtgs[fr]

            if(tdtgs == None):
                models.append(fr)
                fimruns.append(self.fR.getMyRun(fr))

            else:
                for tdtg in tdtgs:
                    if(tdtg in moddtgs):
                        models.append(fr)
                        fimruns.append(self.fR.getMyRun(fr))

        models=MF.uniq(models)
        fimruns=MF.uniq(fimruns)

        return(models,fimruns)


    def getlocalDtgs(self,fimrun):

        self.getAllLocalDtgs()
        dtgs=self.localModelDtgs[fimrun]

        return(dtgs)


    def setMssMask(self,model,dtg):
        smask="%s/%s/%s*%s*tar"%(self.mssbdir,model,model,dtg)
        return(smask)

    def setHpssMask(self,model,dtg):
        smask="%s/%s/%s*%s*tar"%(self.hpssbdir,model,model,dtg)
        return(smask)
    def setHpssInvMask(self):
        
        # -- get listing of dirs
        #
        
        smasks=[]
        cmd='''%s -ld "%s/*"'''%(self.hpssLsCmd,self.hpssbdir)
        output3=MF.runcmdLog(cmd)
        for o in output3:
            tt=o.split()
            if(len(tt) == 9 and tt[0][0] == 'd'):
                model=tt[-1]
                smask="%s/%s/*.tar"%(self.hpssbdir,model)
                smasks.append(smask)
        
        cmd='''%s -ld "%s/*"'''%(self.hpssLsCmd,self.hpssbdirOld)
        output3=MF.runcmdLog(cmd)
        for o in output3:
            tt=o.split()
            if(len(tt) == 9 and tt[0][0] == 'd'):
                model=tt[-1]
                smask="%s/%s/*.tar"%(self.hpssbdirOld,model)
                smasks.append(smask)
                
        return(smasks)


    def setMssDir(self,ldir,model,dtg):
        mssdir="%s/%s"%(self.mssbdir,model)
        print 'PPP(put2mss_rtfim)       ldir: ',ldir
        print 'PPP(put2mss_rtfim)     mssdir: ',mssdir
        self.chkMssDir(mssdir,verb=0)
        mssfile="%s.%s.tar"%(model,dtg)
        return(mssdir,mssfile)


    def setLocalMssPaths(self,n2hash,tbdir,model,dtg):

        try:
            msspath=n2hash[(model,dtg)][0]
        except:
            return(None,None,None)
        ssiz=n2hash[(model,dtg)][1]
        (dir,file)=os.path.split(msspath)
        mssTOCfile="%s.toc"%(file)

        tdir="%s/%s/%s"%(tbdir,model,dtg)
        mssTOCpath="%s/%s/%s"%(tbdir,model,mssTOCfile)
        return(tdir,mssTOCpath,msspath)


    def setLocalHpssPaths(self,n2hash,tbdir,model,dtg):
        """ for rtfim """

        try:
            hpsspath=n2hash[(model,dtg)][0]
        except:
            return(None,None,None)

        ssiz=n2hash[(model,dtg)][1]
        hpssTOCfile="%s.idx"%(hpsspath)

        tdir="%s/%s/%s"%(tbdir,model,dtg)
        hpssTOCpath="%s/%s/%s"%(tbdir,model,hpssTOCfile)
        return(tdir,hpssTOCpath,hpsspath)


    def setKlean(self,sddir,ropt):
        """ kill entire..."""
        print 'WWW(setKlean): doKlean of sddir: ',sddir
        cmd="rm -f -r %s"%(sddir)
        mf.runcmd(cmd,ropt)

    def setLocalGrbMask(self,dtg):
        grbmask=None
        try:
            grbmask="%s/*/*.grb?"%(self.dtgLocalDirs[dtg])
        except:
            None

        # handle case where data come from kishou/kaze, e.g., from zeus
        #
        if(grbmask != None and len(glob.glob(grbmask)) == 0):
            try:
                grbmask="%s/*.grb?"%(self.dtgLocalDirs[dtg])
            except:
                None

        return(grbmask)




#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# -- gfdl/hwrf class
#

class Nwp2DataGfdlHwrf(Nwp2DataW2flds):

    sdir='/dat3/nwp2/ncep'
    mssbdir='/mss/jet/projects/fim/fiorino/nwp2/ncep'

    dmodels=['gfdl','hwrf']

    suffixLLLNNN='''>>>-----lll-nnn------>>>'''
    suffixMMMNNN='''<<<-----MMM-nnn------<<<'''

    def __init__(self,dir=None,doinv=1,verb=0,dbname='invGfdlHwrf',sdiropt='dat3'):


        self.dtgDirs=[]
        self.center_model_dtgs={}
        self.verb=verb

        self.dbname="%s-%s"%(dbname,sdiropt)
        self.sdirs=self.sdir

        self.doinv=doinv
        if(doinv == 1): self.invLocal()

    def invLocal(self):

        self.verb=1
        s1dirs=self.getsubdirs(self.sdirs)

        for s1 in s1dirs.keys():
            s2dirs=self.getsubdirs(s1dirs[s1])
            idtgs=s2dirs.keys()
            idtgs.sort()
            omodel=s1
            sdir=s1dirs[omodel]
            odtgs=[]
            for idtg in idtgs:
                idir="%s/%s"%(sdir,idtg)
                if(MF.GetNfilesDir(idir,'*.tar') > 0):
                    odtgs.append(idtg)
            if(self.verb): print 'IIII: ',len(odtgs),omodel,sdir
            self.center_model_dtgs['w2flds',omodel,sdir]=odtgs


    def getsubdirs(self,sdirs,exclude=['ensFC']):

        if(type(sdirs) != ListType): sdirs=[sdirs]
        subdirs={}
        for sdir in sdirs:
            ssdirs=os.listdir(sdir)
            for ss in ssdirs:
                if(
                    mf.find(ss,'gfs2') or
                    mf.find(ss,'-1') or
                    mf.find(ss,'.DS_') or
                    ss in exclude
                    ): continue
                spath="%s/%s"%(sdir,ss)
                if(os.path.islink(spath) or
                   not(os.path.isdir(spath))
                   ): continue
                subdirs[ss]=spath

        return(subdirs)



    def lsLocalDtgDirs(self,model,lsdtgs,doprint=1,fulltaus=0):


        self.localthere={}

        if(self.doinv == 0):
            self.invLocal()
            self.doinv=1

        self.getDtgDirs(model)

        if(not(type(lsdtgs) is ListType)): lsdtgs=[lsdtgs]

        for dtg in lsdtgs:
            try:
                files=glob.glob("%s/*.tar"%(self.dtgLocalDirs[dtg]))
                taus=range(0,120+1,6)
            except:
                files=None
                taus=[]

            taus=mf.uniq(taus)

            self.localthere[dtg]=len(taus)

            if(doprint):
                if(fulltaus):
                    taucard="taus: "
                    for tau in taus:
                        taucard="%s %03d"%(taucard,tau)
                if(len(taus) > 3):
                    if(not(fulltaus)): taucard="taus: %03d %03d ... %03d"%(taus[0],taus[1],taus[-1])
                    print 'LLL_YYY: %10s %10s'%(model,dtg),"%-80s  %s"%(self.dtgLocalDirs[dtg],taucard)
                elif(len(taus) == 1):
                    if(not(fulltaus)): taucard="taus: %03d"%(taus[0])
                    print 'LLL_YYY: %10s %10s'%(model,dtg),"%-80s %s"%(self.dtgLocalDirs[dtg],taucard)
                else:
                    print 'LLL_NNN: %10s %10s %s'%(model,dtg,self.suffixLLLNNN)

        if(doprint): print





if (__name__ == "__main__"):


    n2=Nwp2Models()

    sys.exit()

    dtgopt='2009100100.2010030100.12'
    dtgopt='2011030100.2011030112.6'
    dtgopt='2011020100.2011070100.6'
    modelopt='fim8,gfs2,ecm2,ukm2,cmc2,ngpc,ngp2'

    # -- to test checking for failed before doing rm -r
    dtgopt='2011020100.2011070100.6'
    modelopt='ngp2'

    # -- just ngpc
    dtgopt='2011020100.2011070100.6'
    modelopt='ngpc,ngp2'

    ropt=''
    doKlean=1

    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    if(modelopt == 'all'):
        models=n2.allmodels
    else:
        models=modelopt.split(',')

    n2=Nwp2Data(sdiropt='dat2',doinv=1)

    for model in models:
        n2.lsLocalDtgDirs(model,dtgs)
        n2.lsMssDtgDirs(model,dtgs)
        n2.putLocal2MssModelDtgs(model,dtgs,ropt=ropt,doKlean=doKlean)
        #n2.getMss2LocalModelDtgs(model,dtgs,ropt=ropt)


    sys.exit()

    modelopt='all'
    modelopt='gfs2,ngpc,ukm2'
    dtgopt='2010121500.2011010100.6'
    dtgopt='2011010106.2011030100.6'
    dtgopt='2011030306.cur-6.12'
    dtgopt='2011050106.cur-6.12'
    ropt=''
    doKlean=1
    override=0
    n2=Nwp2DataW2flds(sdiropt='dat4',override=override)
    n2.lsAllLocalDtgs('all')

    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    if(modelopt == 'all'):
        models=n2.allmodels
    else:
        models=modelopt.split(',')

    for model in models:
        n2.lsLocalDtgDirs(model,dtgs)
        n2.lsMssDtgDirs(model,dtgs)
        n2.putLocal2MssModelDtgs(model,dtgs,ropt=ropt,doKlean=doKlean)
        #n2.getMss2LocalModelDtgs(model,dtgs,ropt=ropt)

    sys.exit()


    # -- 20110627 -- clean up dat3

    doKlean=1
    ropt=''

    n2=Nwp2Data(sdiropt='dat3')

    modelopt='ukm2,fim8,ecm2,gfs2,cmc2'
    models=modelopt.split(',')
    #models=n2.allmodels

    for model in models:
        n2.lsAllLocalDtgs(model)
        n2.putLocal2MssModelDtgs(model,dtgs=None,ropt=ropt,doKlean=doKlean)

    sys.exit()

    #modelopt='ngpc'
    #dtgopt='2010090106.2011051006.12'
    #ropt=''
    #doKlean=1
    #n2=Nwp2DataW2flds(sdiropt='dat4')
    #n2.lsAllLocalDtgs('all')



    dtgopt='2008090112.2008100100.12'
    dtgopt='2008051500.2008090100.12'
    dtgopt='2008100112.2008111500.12'


    dtgopt='2010050100.2010050300.12'
    override=0
    dtgs=mf.dtg_dtgopt_prc(dtgopt)

    models=['ecm2','gfs2','ngp2','ngpc','ukm2']
    n2=Nwp2DataW2flds(override=override)

    for model in models:
        n2.lsLocalDtgDirs(model,dtgs)
        n2.lsMssDtgDirs(model,dtgs)

    sys.exit()




    models=['gfdl','hwrf']
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    n2=Nwp2DataGfdlHwrf(doinv=1)

    for model in models:
        n2.lsLocalDtgDirs(model,dtgs)
        n2.lsMssDtgDirs(model,dtgs)
        n2.getMss2LocalModelDtgs(model,dtgs)

    #n2.lsAllLocalDtgs('all')
    sys.exit()

    donwp2=0
    dow2flds=1

    # -- nwp2 fields
    #
    if(donwp2):
        dtgopt='2009070100.2009090100'
        dtgopt='2009090100.2009090200'
        modelopt='fim8,gfs2,ecm2,ukm2,cmc2,ngpc,ngp2'

        dtgopt='2009090512.2009100100.12'
        dtgopt='2009090512.2009090600.12'

        dtgopt='2009080106.2009083118.12'
        modelopt='gfs2,ukm2,ngpc'

        dtgopt='2009100100.2010030100.12'
        modelopt='fim8,gfs2,ecm2,ukm2,cmc2,ngpc,ngp2'
        ####n2=Nwp2Data(sdiropt='dat3',doinv=1)

    # -- w2flds
    #
    if(dow2flds):
        modelopt='gfs2,ukm2,ngpc'
        dtgopt='2010090106.2011020118.12'
        ropt=''
        doKlean=1

        modelopt='gfs2,ukm2,ngpc'
        modelopt='fim8,gfs2,ecm2,ukm2,cmc2,ngpc,ngp2'
        dtgopt='2010111000.2011020112.12'
        dtgopt='2010111000.2010111100.12'
        dtgopt='2010111000.2010111100.12'
        ropt=''
        doKlean=1

        n2=Nwp2DataW2flds(sdiropt='dat4',doinv=1)
        n2.lsAllLocalDtgs('all')
        #sys.exit()
        # -- based on the listing above, set dtg
        dtgopt='201051100.20101090112.12'
        dtgopt='2010090112.2010090200.6'
        dtgopt='2010090206.2010100100.6'
        modelopt='all'

    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    if(modelopt == 'all'):
        models=n2.allmodels
    else:
        models=modelopt.split(',')


    for model in models:
        n2.lsLocalDtgDirs(model,dtgs)
        n2.lsMssDtgDirs(model,dtgs)
        n2.putLocal2MssModelDtgs(model,dtgs,ropt=ropt,doKlean=doKlean)
        #n2.getMss2LocalModelDtgs(model,dtgs,ropt=ropt)

    sys.exit()

    mssdtgopt='2009070100.2009070200.6'
    mssdtgs=mf.dtg_dtgopt_prc(mssdtgopt)

    for model in models:
        n2.lsMssDtgDirs(model,mssdtgs)
        n2.lsLocalDtgDirs(model,mssdtgs)

    sys.exit()

