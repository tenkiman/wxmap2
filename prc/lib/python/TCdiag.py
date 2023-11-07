from tcbase import *

import M2
import FM
from M2 import setModel2

from w2base import InvHash

#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# package variables
#

tcdiagModels=['gfs2','ecm2','ngpc','ukm2','cmc2','fim8','rtfimy','ngp2']
# -- remove ngp2 -- causing pygrads to glitch
tcdiagModels=['gfs2','ecm2','ngpc','ukm2','cmc2','fim8','rtfimy','gfsr','gfr1']
tcdiagModels=['gfs2','ecmn','ngpc','ukm2','cmc2','fim8','rtfimy','gfsr','gfr1']
tcdiagModels=['gfs2','ecm2','ngpc','ukm2','cmc2','fim8','rtfim9','navg']
tcdiagModels=['gfs2','ecm2','ukm2','cmc2','fim8','rtfim9','navg']
tcdiagModels=['gfs2','ecm4','ecm2','ukm2','cmc2','fim8','rtfim9','navg']
tcdiagModels=['gfs2','ecm4','ukm2','cmc2','fim8','rtfim9','navg'] # 20170222 -- hi-res ecm4 only
tcdiagModels=['gfs2','fv3e','fv3g','ecm4','ukm2','cmc2','navg']   # 20180112 -- deprecate *fim*; add fv3?
tcdiagModels=['gfs2','ecm4','ukm2','cmc2','navg']                 # 20190131 -- deprecate fv3 until the local run is sorted
tcdiagModels0618Old=['gfs2','ngpc','ukm2']
tcdiagModels0618=['gfs2','ukm2','navg']

if(w2.onTenki):
    tcdiagModels=['gfs2','ecm5','cgd2','navg','jgsm']                 # 20190131 -- deprecate fv3 until the local run is sorted
    tcdiagModels0618=['gfs2','navg','jgsm']

tcdiagModelOrderVar=['gfs2','ecm4','ecm2','fim8','rtfim9','ecmt','ukm2','cmc2','navg']
tcdiagModelOrderVar=['gfs2','ecm4','ukm2','fim8','rtfim9','ecmt','cmc2','navg'] # 20170222 -- hi-res ecm4 only
tcdiagModelOrderVar=['gfs2','fv3e','fv3g','ecm4','ukm2','cmc2','navg'] # 20180112 -- deprecate *fim*; add fv3?
tcdiagGenModels=['gfs2','fv3e','fv3g','ecm4','ukm2','cmc2','navg']
tcdiagBasins=['E','L','C','W','S','I','P','A','B']

# -- jtdiag models
#
# 20181218 -- jtdiag models 
# 20200724 -- added jgsm
jtdiagModels=['gfs2','ecm5','cgd2','navg','jgsm']   
jtdiagModels0618=['gfs2','navg','jgsm']



modelOname={
    'gfs2':'GFS (NCEP GFS T574)',
    'gfsr':'CFSR (NCEP GFS T274)',
    'fim8':'FIM (ESRL 30km)',
    'cmc2':'CMC (CMC GEM)',
    'ngpc':'NGP (FNMOC NOGAPS T319L42)',
    'navg':'NVG (FNMOC NAVGEM T359L42)',
    'ngp2':'NGP (FNMOC NOGAPS T319L42)',
    'ukm2':'UKM (UKMO UM 30km)',
    'rtfimz':'FIMZ (ESRL 30km)',
    'rtfimy':'FIMY (ESRL 30km, EnKF IC)',
    'rtfim9':'FIM9 (ESRL 15km, Hybrid IC)',
    'ecm2':'ECM (ECMWF IFS T1299)',
    'ecm4':'ECM (ECMWF HRES T1299)',
    'ecm5':'ECM (ECMWF HRES T1299)',
    'era5':'ERA5 T600L143',
    'jgsm':'JMA (GSM)',
    #'cgd2':'CMC (CMC GDPS dx 0.24deg)',
    # -- 2021092812 -- new higher res
    'cgd2':'CMC (CMC GDPS dx 0.15deg)',
    'ecmn':'ECM (ECMWF IFSCy38r1 T1299)',
    'ecmt':'ECM (ECMWF IFSCy38r1 T1299)',
    'fv3e':'FV3E (ESRL 27 km ; NCEP)',
    'fv3g':'FV3G (ESRL 27 km ; GF-phys)',
}

modelTagOname={
    'gfs2':'GFS',
    'gfsr':'GFSR',
    'fim8':'FIM8',
    'cmc2':'CMC',
    'ngpc':'NGP',
    'navg':'NAVG',
    'ngp2':'NGP',
    'ukm2':'UKM',
    'rtfimz':'FIMZ',
    'rtfimy':'FIMY',
    'rtfim9':'FIM9',
    'ecm2':'ECM',
    'ecm4':'ECM4',
    'ecm5':'ECM5',
    'era5':'ERA5',
    'jgsm':'JGSM',
    'cgd2':'CMC',
    'ecmn':'ECM',
    'ecmt':'ECMT',
    'fv3e':'FV3E',
    'fv3g':'FV3G',
}


modelTrkPlotProps={
    'gfs2':[3],
    'gfsr':[3],
    'fim8':[7],
    'cmc2':[10],
    'ngpc':[4],
    'navg':[4],
    'ngp2':[4],
    'ukm2':[9],
    'rtfim9':[8],
    'rtfimy':[11],
    'ecm2':[14],
    'ecm4':[14],
    'ecm5':[14],
    'era5':[14],
    'jgsm':[14],
    'cgd2':[14],
    'ecmn':[14],
    'ecmt':[14],
    'fv3e':[8],
    'fv3g':[11],
}


modelMinTau0012={
    'gfs2':168,
    'gfsr':168,
    'fim8':168,
    'cmc2':144,
    'ngpc':168,
    'navg':168,
    'ngp2':168,
    'ukm2':144,
    'ukmc':120,
    'rtfim9':168,
    'rtfimy':168,
    'ecm2':168,
    'ecm4':168,
    'ecm5':168,
    'era5':168,
    'jgsm':132,
    'cgd2':168,
    'ecmn':168,
    'ecmt':168,
    'fv3e':168,
    'fv3g':168,
}


modelMinTau0618={
    'gfs2':168,
    'gfsr':168,
    'fim8':168,
    'cmc2':144,
    'ngpc':144,
#    'navg':144,
'navg':168,  # from ncep
'ngp2':144,
'ukm2':60,
'rtfim9':168,
'rtfimy':168,
'ecm2':-999,
'ecm4':-999,
'ecm5':-999,
'era5':-999,
'jgsm':132,
'cgd2':-999,
'ecmn':-999,
'ecmt':-999,
'fv3e':-999,
'fv3g':-999,
}

phrP06={
    6:0,
    12:6,
    18:12,
    24:18,
    30:24,
    36:30,
    42:36,
    48:42,
    60:48,
    72:60,
    84:72,
    96:84,
    108:96,
    120:108,
    132:120,
}

phrP12={
    12:0,
    18:6,
    24:12,
    30:18,
    36:24,
    42:30,
    48:36,
    60:42,
    61:48,
    72:60,
    84:72,
    96:84,
    108:96,
    120:108,
    132:120,
}

allJTdiagTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120]

class LsdiagAreaNhem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-10.0,
                 latN=80.0,
                 dx=None,
                 dy=None,
                 ):

        if(dx == None): dx=0.5
        if(dy == None): dy=0.5
        
        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class LsdiagAreaShem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=10.0,
                 dx=None,
                 dy=None,
                 ):

        if(dx == None): dx=0.5
        if(dy == None): dy=0.5

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class LsdiagAreaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=60.0,
                 dx=None,
                 dy=None,
                 ):

        if(dx == None): dx=0.5
        if(dy == None): dy=0.5

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)




#class InvHash(InvHash):

    #def lsInv(self,
              #models,
              #dtgs,
              #):


        #kk=self.hash.keys()
        #for k in kk:
            #imodel=k[0]
            #idtg=k[1]
            #if((idtg in dtgs) and
               #(imodel in models)
               #):
                #print k,imodel,idtg,self.hash[k]


class InvHashTD(InvHash):

    def lsInv(self,
              models,
              dtgs,
              ):


        kk=self.hash.keys()
        for k in kk:
            kmodel=k[0]
            kdtg=k[1]
            print 'iV model: ',kmodel,' dtg: ',kdtg
            vals=self.hash[k]
            print vals
            #for val in self.hash[k]:
            #    print val
        



class phpInv(MFbase):

    def PrintHash(self,hash,name='hash',verb=0):

        cards=[]
        kk=hash.keys()
        kk.sort()
        nh=len(hash)

        if(verb):
            print kk
            print nh

        if(isinstance(kk[0],tuple)):   nk=len(kk[0])
        else:                          nk=1


        card="%s %d %d"%(name,nk,nh)
        cards.append(card)

        for k in kk:
            card=''
            if(isinstance(k,tuple)):
                for n in k:
                    card=card+' '+n
            else:
                card=card+' '+k

            card=card+' : '
            for n in hash[k]:
                card=card+' '+n
            cards.append(card)

        return(cards)


    def uNiqHash(self,hash):
        tt={}
        for kk in hash.keys():
            dd=hash[kk]
            dd=mf.uniq(dd)
            tt[kk]=dd
        return(tt)


class TcdiagInv(phpInv):


    def __init__(self,tG,
                 dtgopt=None,
                 ndayback=25,
                 do0618=1,
                 invtag=None,
                 tstmid=None,
                 keepmodels=None,
                 verb=0):


        self.ndayback=ndayback
        self.verb=verb

        MF.sTimer('inv.tcdiag')

        if(dtgopt == None):

            if(do0618):
                bdtg="cur-d%d"%(ndayback)
                tdtgopt="%s.cur.6"%(bdtg)
                tdtgs=mf.dtg_dtgopt_prc(tdtgopt)
            else:
                bdtg="cur12-d%d"%(ndayback)
                tdtgopt="%s.cur12"%(bdtg)
                tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

        elif(len(dtgopt.split('.')) > 1):
            tdtgs=mf.dtg_dtgopt_prc(dtgopt)

        elif(not(mf.find(dtgopt,'cur')) and ndayback > 0):
            edtg=mf.dtg_command_prc(dtgopt)
            bdtg=mf.dtginc(edtg,-24*ndayback)
            tdtgopt="%s.%s"%(bdtg,edtg)
            tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

        else:
            print 'EEE invalid dtgopt: ',dtgopt,' in TcdiagInv'

        webdir=tG.webdir

        if(not(hasattr(tG,'tD'))):
            tD=TcData(dtgopt=tdtgs[-1],verb=self.verb)
        else:
            tD=tG.tD

        webdir="%s/%s"%(webdir,tG.basename.lower())
        MF.ChangeDir(webdir)

        stmsDtg={}
        allstmsDtg={}
        dtgsStm={}
        dtgsModel={}
        modelsDtgStm={}

        for dtg in tdtgs:

            year=dtg[0:4]

            hmask="%s/%s/*/*.htm"%(year,dtg)

            htmls=glob.glob(hmask)

            if(len(htmls) == 0):
                print 'WWW no htmls in webdir: ',webdir,' for dtg: ',dtg

            print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII ',dtg,hmask
            for html in htmls:
                (dir,file)=os.path.split(html)
                (base,ext)=os.path.splitext(file)
                tt=file.split('.')
                model=tt[0]
                dtg=tt[1]
                stm3id=tt[2]
                stmyear=tt[3]
                stm="%s.%s"%(stm3id,stmyear)
                if(tstmid != None and stm != tstmid): continue
                if(keepmodels != None and not(model in keepmodels)): continue
                stm=stm.upper()
                if(verb): print 'FFF model: ',model,dtg,stm
                # -- dtg <- model
                MF.appendDictList(dtgsModel,model,dtg)
                # -- stm <- dtg
                MF.appendDictList(stmsDtg,dtg,stm)
                # -- dtg <- stm
                MF.appendDictList(dtgsStm,stm,dtg)
                # -- models <- dtg,basin
                MF.append2TupleKeyDictList(modelsDtgStm,dtg,stm,model)


            if(len(htmls) > 0):
                if(tstmid != None):
                    allstmsDtg[dtg]=stmsDtg[dtg]
                else:
                    allstmsDtg[dtg]=tD.getStmidDtg(dtg)
                if(verb): print 'FFF allstms: ',dtg,allstmsDtg[dtg]

        stmsDtg=self.uNiqHash(stmsDtg)
        dtgsStm=self.uNiqHash(dtgsStm)
        dtgsModel=self.uNiqHash(dtgsModel)
        modelsDtgStm=self.uNiqHash(modelsDtgStm)

        cards=[]
        cards=cards+self.PrintHash(stmsDtg)
        cards=cards+self.PrintHash(allstmsDtg)
        cards=cards+self.PrintHash(dtgsStm)
        cards=cards+self.PrintHash(dtgsModel)
        cards=cards+self.PrintHash(modelsDtgStm)

        invpath="%s/inv.hfip.tcdiag.txt"%(webdir)
        if(invtag != None):
            invpath="%s/inv.hfip.tcdiag.%s.txt"%(webdir,invtag)

        rc=MF.WriteList2File(cards,invpath,verb=verb)

        MF.dTimer('inv.tcdiag')





class TcDiag(MFbase):


    aidAliases={
        'ngf2':'gfs2',
        'nuk2':'ukm2',
        'nec2':'ecm2',
        'nec4':'ecm4',
        'necn':'ecmn',
        'nng2':'ngp2',
        'ncm2':'cmc2',
        'nngc':'ngpc',
    }

    aspectRatio=4.0/3.0

    dlatDefault=12.0
    dlonDefault=dlatDefault*aspectRatio

    taulastMax=168

    dr=5
    dtheta=45
    rmax=200

    undef=9999.

    # units are km for dr and rmax
    drnm=dr*km2nm
    rmaxnm=rmax*km2nm

    radinfIn=200
    radinfOut=800
    radinfInnm=radinfIn*km2nm
    radinfOutnm=radinfOut*km2nm

    radinfInWind=0
    radinfOutWind=500

    radinfInWindnm=radinfInWind*km2nm
    radinfOutWindnm=radinfOutWind*km2nm

    radinfSst=100
    # -- reduce for improper handling of undef in tcprop
    #
    radinfSst=50
    radinfSstnm=radinfSst*km2nm

    areaIn=radinfIn*radinfIn
    areaOut=radinfOut*radinfOut
    areaAnnulus=areaOut-areaIn
    basename='TCdiag'

    xsize=912
    xsize=1200
    ysize=(xsize*3)/4

    sfcLevel='surf'

    printMethod='printim'
    #printMethod='gxyat'
    printOpt="x%d y%d"%(xsize,ysize)
    if(printMethod == 'gxyat'):  printOpt="-r -x %s -y %s"%(xsize,ysize)


    # -- limit distance from center to look for H/L in mfhilo gr
    #
    reRes='0.25'
    mfhiloRad=300


    # -- increase dlat/dlon for storms way poleward
    #
    latitudeET=50.0
    dlatETFact=1.25

    maxLatitude=68.0
    barbskip=6

    stmVarNameByIndex={

        1:'latitude',
        2:'longitude',
        3:'max_wind',
        4:'rms',
        5:'min_slp',
        6:'shr_mag',
        7:'shr_dir',
        8:'stm_spd',
        9:'stm_hdg',
        10:'sst',
        11:'ohc',
        12:'tpw',
        13:'land',
        14:'850tang',
        15:'850vort',
        16:'200dvrg',
    }


    customVarNameByIndex={
        1:'ADECK  VMAX (KT)',
        2:'DIAG   VMAX (KT)',
        #3:'ADECK  PMIN (MB)',
        3:'precip',             # -- use psl into jtdiag table
        4:'DIAG   PMIN (MB)',
        5:'sstanom',
        6:'precip-actual',
        7:'PR  ASYM/TOT (%)',
        8:'TOTSHR MAG  (KT)',
        9:'SHR/TOTSHR   (%)',
        10:'SHR ASYM/TOT (%)',
        11:'CPS  B(AROCLINC)',
        12:'CPS   VTHERM(LO)',
        13:'CPS   VTHERM(HI)',
        14:'POCI        (MB)',
        15:'ROCI        (KM)',
        16:'R34mean     (KM)',
        17:'R50mean     (KM)',
        18:'R64mean     (KM)',
    }


    def __init__(self,dtg,model,
                 ttaus=None,
                 ctlpath=None,
                 domandonly=0,
                 doStndOnly=1,
                 doDiagOnly=0,
                 doDiagPlotsOnly=1,
                 doga=1,
                 gaopt='gacore',
                 verb=0,
                 dols=0,
                 dowebserver=0,
                 override=0,
                 doshort=0,
                 trkSource='tmtrk',
                 selectNN=1,
                 dobt=0,
                 dobail=1,
                 useLsdiagDat=0,
                 adeckSdir=None,
                 tbdir=None,
                 ctlquiet=1,
                 tD=None,
                 dlat=None,dlon=None,
                 justInit=0,
                 xgrads='grads',
                 doSfc=0,
                 doRoci=1,
                 useFldOutput=0,
                 dr=dr,dtheta=dtheta,rmax=rmax):


        if(adeckSdir == None):
            sdir='/dat3/tc/tmtrkN'
            sdir='/w21/dat/tc/tmtrkN'
            sdir="%s/tmtrkN"%(w2.TcDatDir)
            self.sdir=sdir
        else:
            self.adeckSdir=adeckSdir


        if(tbdir == None):
            tbdir=w2.TcTcanalDatDir

            
        self.year=dtg[0:4]

        self.tbdir=tbdir
        self.tdir="%s/%s/%s/%s"%(self.tbdir,self.year,dtg,model)

        rc=MF.ChkDir(self.tdir,'mk')

        # -- never write full diag file to webserver
        #
        if(doDiagOnly): dowebserver=0

        self.dtg=dtg
        self.model=model
        self.umodel=model.upper()
        self.domandonly=domandonly
        self.doStndOnly=doStndOnly
        self.doDiagOnly=doDiagOnly
        self.doDiagPlotsOnly=doDiagPlotsOnly
        self.verb=verb
        self.doga=doga
        self.gaopt=gaopt
        self.dols=dols
        self.dowebserver=dowebserver
        self.trkSource=trkSource
        self.selectNN=selectNN
        self.dobt=dobt
        self.override=override

        self.ctlquiet=ctlquiet

        self.xgrads=xgrads

        self.tD=tD
        self.doSfc=doSfc

        if(dlat == None):
            self.dlat=self.dlatDefault
            self.dlon=self.dlonDefault
        else:
            self.dlat=dlat
            self.dlon=self.dlat*self.aspectRatio

        if(dlon != None): self.dlon=dlon

        self.year=dtg[0:4]
        ddir="%s/nwp2/w2flds/dat"%(w2.W2BaseDirDat)

        webdir=w2.HfipWebBdir

        wdir="%s/tcdiagDAT"%(webdir)
        # use symbolic link
        wdir="%s/tcdiag"%(webdir)
        bdir=TcDiagDatDir

        wdirl=wdir

        dtgdir="%s/%s"%(self.year,dtg)
        urldir="%s/%s"%(dtgdir,model)
        pltdir="%s/%s"%(wdir,urldir)
        datdir="%s/%s"%(bdir,urldir)
        adkdir="%s/%s/ADECKS"%(wdir,dtgdir)
        dgndir="%s/%s/DIAGFILES"%(wdir,dtgdir)

        adkdirl="%s/%s/ADECKS"%(wdirl,dtgdir)
        dgndirl="%s/%s/DIAGFILES"%(wdirl,dtgdir)

        if(dowebserver == 0):
            pltdir=datdir
            webdir=TcDataBdir
        else:
            MF.ChkDir(adkdir,'mk')
            MF.ChkDir(dgndir,'mk')
            MF.ChkDir(adkdirl,'mk')
            MF.ChkDir(dgndirl,'mk')

        webdiagdir=pltdir

        # -- 20221110 -- do rocis in w2-tc-lsdiag.py
        #
        self.ddir=ddir
        self.wdir=wdir
        self.webdir=webdir
        self.pltdir=pltdir
        self.urldir=urldir
        self.datdir=datdir
        self.webdiagdir=webdiagdir
        self.adeckOutdir=adkdir
        self.diagfileOutdir=dgndir

        self.adeckOutdirLocal=adkdirl
        self.diagfileOutdirLocal=dgndirl
        self.useFldOutput=useFldOutput

        self.xgrads=xgrads
        # -- make dict to store rocis
        #
        self.AllRocis={}
        
        self.initOutput()
        self.initTC(dtg)

        if(justInit): return


        # -- initialize the m2 object first
        #
        self.rcM2=self.initM2(dtg,model)


        # -- initialize the adeck object
        #
        self.initAD(dtg,model)

        # -- if doing ls set targetaus for chk and ualevsPlot for plotting
        #
        if(dols):
            self.targetTaus=range(0,120+1,6)+range(132,168+1,12)
            self.initPlotControl()
            self.ctlStatus=-1
            return

        lsdiagCtlpath=None
        if(ctlpath == None):
            rc=w2.getW2fldsRtfimCtlpath(model,dtg)
            
            self.ctlStatus=1
            if(rc == None):
                print 'WWW-TcDiag.__init__: no model ctl for: ',model,' at dtg:',dtg,'...return...'
                self.ctlStatus=0
                return

            (w2rc,w2ctlpath,w2taus,w2gribtype,w2gribver,datpaths,w2nfields,w2tauOffset)=rc
            # -- model dtg whe tauOffset=6
            #
            mdtg=mf.dtginc(dtg,-w2tauOffset)
            self.mdtg=mdtg
            self.tauOffset=w2tauOffset

            if(w2rc == 0 and lsdiagCtlpath == None):
                if(not(self.ctlquiet)): print 'III TCdiag.__init__ ctlpath= None'
                ctlpath=None
                maxtauModel=None
            elif(w2rc):
                if(not(self.ctlquiet)): print 'III TCdiag.__init__ ctlpath=w2ctlpath'
                ctlpath=w2ctlpath
                (tdir,file)=os.path.split(ctlpath)
                
            # -- get sfc ctlpath
            #
            self.ctlStatus2=0
            self.ctlpath2=None
            
            if(model == 'era5' and doSfc):

                rc=w2.getW2fldsRtfimCtlpath(model,dtg,doSfc=1)
                self.ctlStatus2=1
                if(rc == None):
                    print 'WWW-TcDiag.__init__: no model ctl for: ',model,' at dtg:',dtg,'22222222 ...return...'
                    self.ctlStatus2=0
                    return
    
                (w2rc2,w2ctlpath2,w2taus2,w2gribtype2,w2gribver2,datpaths2,w2nfields2,w2tauOffset2)=rc
            
                if(w2rc):
                    ctlpath2=w2ctlpath2
                    self.ctlpath2=ctlpath2

                    if(not(self.ctlquiet)): 
                        print 'III TCdiag.__init__ ctlpath=w2ctlpath 2222222'
                        print 'III -- ERA5 -- get sfc self.ctlpath2: ',self.ctlpath2


        # -- add look for output path in case of redo without w2flds there...
        #
        ctls=glob.glob("%s/%s.%s.*.ctl"%(self.tdir,model,dtg))
        if(len(ctls) == 1): lsdiagCtlpath=ctls[0]

        if(lsdiagCtlpath != None):
            self.lsdiagCtlpath=lsdiagCtlpath

        if(useLsdiagDat):

            if(lsdiagCtlpath != None):
                print 'III TCdiag.__init__ ctlpath=lsdiagCtlpath'
                ctlpath=lsdiagCtlpath

                dmask=lsdiagCtlpath.replace('.ctl','.f???.dat')
                dats=glob.glob(dmask)
                w2taus=[]
                for dat in dats:
                    tau=dat.split('.')[-2][1:]
                    w2taus.append(int(tau))




        # -- override variables from m2

        # -- define reduced # of taus
        #
        if(ttaus == None):
            self.targetTaus=range(0,120+1,6)+range(132,168+1,12)
        else:
            self.targetTaus=ttaus

        # -- avoid tau data check if setting the ctlpath
        #
        if(ctlpath == None):

            # -- 20111031 -- make sure there is data -- for situations with limited taus, e.g., ecm2 2011061012, 061100
            #
            dtaus=[]
            ttaus=self.targetTaus
            lttaus=len(ttaus)
            for n in range(0,len(ttaus)):
                tau0=ttaus[n]
                taum1=tau0
                taup1=tau0

                if(n > 0):         taum1=ttaus[n-1]
                if(n < lttaus-1):  taup1=ttaus[n+1]

                if(w2taus == None): continue
                if(tau0 in w2taus or (taum1 in w2taus and taup1 in w2taus) ): dtaus.append(tau0)

            self.targetTaus=dtaus


        self.ctlpath=ctlpath

        if(ctlpath == None):
            print 'WWW(TcDiag) ctlpath == None)...returning'
            self.rcM2=None
            return

        if(self.doga): self.initGA(self.gaopt)


        # -- 20101031 -- bypass m2 data check since we're using
        # the more generic getW2fldsRtfimCtlpath method in w2base.py
        #if(self.rcM2):  self.rcM2=None ; return

        if(MF.GetPathSiz(self.ctlpath) == None):
            if(not(self.dols)): print "EEE.TCdiag(%s) does not exist...bailing with sys.exit() if dobail=1 currently: %d"%(self.ctlpath,dobail)
            if(dobail): sys.exit()


        if(not(self.dols)):
            MF.ChkDir(datdir,'mk')
            MF.ChkDir(pltdir,'mk')


        if(self.doDiagOnly and not(hasattr(self,'targetTaus'))):
            btau=0
            etau=126
            dtau=6
            self.targetTaus=range(btau,etau+1,dtau)+[132,144,156,168]


        self.initPlotControl()

    def getGAfromGaProc(self,
                        ):

        if(not(hasattr(self,'ga'))):

            # -- doreinit reinits the grads obj
            #
            self.gaP.initGA(ctlpath=self.ctlpath,doreinit=1)
            ga=self.gaP.ga

            self.ga=ga
            self.ge=ge
            self.gp=gp

        else:
            self.ga('q files')
            self.ga('close 1')

            ga=self.ga
            ge=self.ge
            gp=self.gp

        return(ga,ge,gp)


    def initPlotControl(self):

        self.ualevsPlot={}


        self.ualevsPlot[1000]={}
        self.ualevsPlot[1000]['r']=1

        self.ualevsPlot[850]={}
        self.ualevsPlot[850]['z']=1
        self.ualevsPlot[850]['t']=1
        self.ualevsPlot[850]['r']=1
        self.ualevsPlot[850]['u']=1
        self.ualevsPlot[850]['v']=1


        self.ualevsPlot[850]={}
        self.ualevsPlot[850]['z']=1
        self.ualevsPlot[850]['t']=1
        self.ualevsPlot[850]['r']=1
        self.ualevsPlot[850]['u']=1
        self.ualevsPlot[850]['v']=1

        self.ualevsPlot[700]={}
        self.ualevsPlot[700]['u']=1
        self.ualevsPlot[700]['v']=1

        self.ualevsPlot[500]={}
        self.ualevsPlot[500]['z']=1
        self.ualevsPlot[500]['t']=1
        self.ualevsPlot[500]['r']=1
        self.ualevsPlot[500]['u']=1
        self.ualevsPlot[500]['v']=1


        self.ualevsPlot[200]={}
        self.ualevsPlot[200]['z']=1
        self.ualevsPlot[200]['u']=1
        self.ualevsPlot[200]['v']=1

        self.ualevsPlot[100]={}
        self.ualevsPlot[100]['z']=1


    def setDataGrid(self,ropt='',override=0):

        self.hemigrid=getHemis(self.istmids)
        if(self.hemigrid == 'nhem'):  aa=LsdiagAreaNhem()
        if(self.hemigrid == 'shem'):  aa=LsdiagAreaShem()
        if(self.hemigrid == 'global'):  aa=LsdiagAreaGlobal()

        self.area=aa

        # override to test with more general code
        #
        #self.area=W2areaGlobal()

        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None


    def initOutput(self):

        # -- output
        #
        self.stmData={}
        self.customData={}
        self.sndData={}
        self.sndDataVar={}
        self.sndPlevs=[]
        self.urlData={}
        self.sndKeys=[]

        self.diagVals={}
        self.diagTypes={}
        self.diaguRls={}
        self.diagKeys=[]
        self.diagFilenames={}



    def setDiagPath(self,stmid,tdir=None,tbdir=None,diag=0,dobail=0):

        if(tbdir != None):
            rc=MF.ChkDir(self.tdir,'quiet')
            if(not(rc == 1)):
                print """EEE TCdiag.setDiagPath: trying to find self.tdir from tbdir failed -- haven't run correctly or yet...""",tdir
                if(dobail):  sys.exit()
                else:        return(-1)

        elif(tdir != None):
            self.tdir=tdir

        elif(hasattr(self,'tdir')):
            None

        else:
            print 'EEE TCdiag.setDiagPath: either tdir or tbdir needs to be set here'
            rc=(-1,None,None)
            return(rc)

        osource='NADA'
        if(hasattr(self,'aidsource')):
            osource="%s-%s"%(self.aid,self.aidsource)

        elif(hasattr(self,'trkSource')):
            osource=self.trkSource

        self.finalDiagPath="%s/tcdiag.%s.%s.%s.%s.txt"%(self.tdir,self.model,self.dtg,stmid.lower(),osource)

        (dtimei,ldtg,gdtg)=MF.PathModifyTime(self.finalDiagPath)
        siz=MF.GetPathSiz(self.finalDiagPath)
        rc=(1,None,None)
        if(siz == None):
            dtimei='----------:----'
            siz=-999
            rc=(0,None,None)

        rc=(siz,dtimei,self.finalDiagPath)
        if(diag):
            print 'III(self.finalDiagPath): ',"%10s  %6d  %s  %s"%(stmid,siz,dtimei,self.finalDiagPath)

        dpath=self.finalDiagPath
        self.shipstxt=dpath.replace('tcdiag','ships.txt')
        self.shipsadk=dpath.replace('tcdiag','ships.adk')
        self.shipslog=dpath.replace('tcdiag','ships.log')
        self.shipscrq=dpath.replace('tcdiag','ships.crq')


        return(rc)


    def getLsdiagPathsStmids(self,model,verb=0):

        stmids=[]
        mask="%s/*.%s.*"%(self.diagfileOutdir,model)
        lsdiagPaths=glob.glob(mask)
        olsdiagPaths={}

        for lsdiagPath in lsdiagPaths:
            (fdir,ffile)=os.path.split(lsdiagPath)
            tt=ffile.split('.')
            stmid="%s.%s"%(tt[-4],tt[-3])
            stmid=stmid.upper()
            if(verb): print 'lll',lsdiagPath,'ssss',stmid
            stmids.append(stmid)
            olsdiagPaths[stmid]=lsdiagPath


        stmids=mf.uniq(stmids)

        return(stmids,olsdiagPaths)



    def lsDiag(self,stmid,lsdiagpath=None,dobail=1,nhead=44):


        if(not(hasattr(self,'finalDiagPath')) and lsdiagpath == None):
            print "EEE self.finalDiagPath not there...self.setDiagPath(stmid,self.tdir)",stmid,self.dtg,self.model
            if(dobail):
                sys.exit()
            else:
                return
        elif(lsdiagpath != None):
            None
        else:
            lsdiagpath=self.finalDiagPath

        (dtimei,ldtg,gdtg)=MF.PathModifyTime(lsdiagpath)
        siz=MF.GetPathSiz(lsdiagpath)
        if(siz == None):
            siz=-999
            dtimei='----------:----'

        print
        print "LLLLL: %-10s  %6d  %s  %s"%(stmid,siz,dtimei,lsdiagpath)
        if(lsdiagpath and siz > 0):
            cards=open(lsdiagpath).readlines()
            for n in range(0,nhead+1):
                card=cards[n]
                print card[0:-1]


    def putAdeckCards(self,stmid,verb=1,dobail=1):

        if(not(hasattr(self,'aidcards'))):
            print "EEE TcDiag.putAdeckCards no cards there...",stmid,self.dtg,self.model
            if(dobail):
                sys.exit()
            else:
                return

        adeckpath="%s/adeck.%s.%s.%s.txt"%(self.adeckOutdir,self.aid,stmid,self.dtg)
        print 'AAA -- putting: ',adeckpath
        MF.WriteList2Path(self.aidcards,adeckpath,verb=verb)

        if(hasattr(self,'adeckOutdirLocal')):
            adeckpathl="%s/adeck.%s.%s.%s.txt"%(self.adeckOutdirLocal,self.aid,stmid,self.dtg)
            print 'AAA -- putting -- local: ',adeckpathl
            MF.WriteList2Path(self.aidcards,adeckpathl,verb=verb)

        # -- cp the diagfiles over too...
        #
        if(hasattr(self,'finalDiagPath')):
            cmd="cp %s %s/."%(self.finalDiagPath,self.diagfileOutdir)
            mf.runcmd(cmd)

            if(hasattr(self,'diagfileOutdirLocal')):
                cmd="cp %s %s/."%(self.finalDiagPath,self.diagfileOutdirLocal)
                mf.runcmd(cmd)  


    def parseDiag(self,stmid,lsdiagpath=None,dobail=1,verb=0):
        """ parse output from lsdiag.x
        """


        def makekey(label):
            tt=label.lower().split()
            nlabel=tt[0]
            ne=-1
            if(nlabel == 'cps'): ne=0
            for n in range(1,len(tt)+ne):
                nlabel="%s_%s"%(nlabel,tt[n])

            nlabel=nlabel.replace(')','')
            nlabel=nlabel.replace('(','')

            return(nlabel)

        if(not(hasattr(self,'finalDiagPath')) and lsdiagpath == None):
            print "EEE self.finalDiagPath not there...self.setDiagPath(stmid,self.tdir)",stmid,self.dtg,self.model
            if(dobail):
                sys.exit()
            else:
                return
        elif(lsdiagpath != None):
            None
        else:
            lsdiagpath=self.finalDiagPath

        # -- check if SHEM storm
        stmIsShem=0
        if(isShemBasinStm(stmid)): stmIsShem=1
        
        rc=1
        self.stmData={}
        self.stmDataVars={}
        self.cstmData={}
        self.stmLabels={}

        self.customData={}
        self.ccustomData={}
        self.customLabels={}

        self.sndData={}
        self.csndData={}
        self.sndLabels={}

        self.urlData={}
        self.sndKeys=[]

        self.diagVals={}
        self.diagTypes={}
        self.diaguRls={}
        self.diagKeys=[]
        self.diagFilenames={}

        self.diagTaus=[]

        self.nstmvars=16
        self.nsndvars=5

        self.curstmid=stmid


        gotstm=0
        gotusr=0
        gotsnd=0
        try:
            cards=open(lsdiagpath).readlines()
        except:
            print """WWW TCDiag.parseDiag couldn't read file: %s"""%(lsdiagpath)
            return(0)
            if(dobail): sys.exit()

        if(len(cards) == 0):
            print """WWW TCDiag.parseDiag file: %s is 0 length"""%(lsdiagpath)
            return(0)

        for n in range(0,len(cards)):
            if(gotstm and gotusr and gotsnd): break
            card=cards[n]
            aid=None
            if(n == 0 and mf.find(card,'*')):
                tt=card.split()
                aid=tt[1]
                dtg=tt[2]
            
            # -- check for bad deck
            #
            if(n == 0 and aid == None):
                print """WWW TCDiag.parseDiag file: %s is full of NOLOADS..."""%(lsdiagpath)
                return(0)

            if(n == 1 and mf.find(card,'*')):
                tt=card.split()
                stm2id=tt[1]
                stmname=tt[2]

            if(mf.find(card,'STORM') and gotstm == 0):
                gotstm=1
                n=n+1
                card=cards[n]
                if(mf.find(card,'NTIME')):
                    tt=card.split()
                    ntau=int(tt[1])
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for i in range(0,ntau):
                        self.diagTaus.append(int(tt[i]))

                    if(self.verb): print 'self.diagTaus: ',self.diagTaus


                for i in range(0,self.nstmvars):
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        if(mf.find(card,'LAT') or mf.find(card,'LON')):
                            val=float(tt[j])
                        else:
                            # -- convert rel vort to cyclonic vort
                            #
                            ival=int(tt[j])
                            if(mf.find(label,'850VORT') and stmIsShem): ival=-1*ival
                            val=ival
                        self.stmData[tau,i+1]=val
                        self.cstmData[tau,i+1]=tt[j]
                        self.stmLabels[i+1]=label

            n=n+1
            card=cards[n]
            if(mf.find(card,'CUSTOM') and gotusr == 0):
                gotusr=1
                n=n+1
                card=cards[n]
                self.ncustomvars=int(card.split()[1])
                n=n+1
                for i in range(0,self.ncustomvars):
                    n=n+1
                    card=cards[n]
                    label=card[0:16]
                    label=label.replace('/','_')
                    tt=card[16:].split()
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        val=int(tt[j])
                        self.customData[tau,i+1]=val
                        self.ccustomData[tau,i+1]=tt[j]
                        self.customLabels[i+1]=label

            n=n+1
            card=cards[n]
            if(mf.find(card,'SOUNDING') and gotsnd == 0):
                gotsnd=1
                n=n+1
                card=cards[n]
                self.nlevs=int(card.split()[1])
                n=n+1
                for i in range(0,self.nlevs):
                    for ii in range(0,self.nsndvars):
                        n=n+1
                        card=cards[n]
                        label=card[0:16]
                        label=label.replace('/','_')
                        tt=card[16:].split()

                        var=label.split()[0].split('_')[0]
                        var=var.lower()

                        plev=label.split()[0].split('_')[-1]
                        plev=plev.lower()
                        if(plev == self.sfcLevel):
                            ilev=plev
                        else:
                            ilev=int(plev)

                        self.sndPlevs.append(plev)
                        for j in range(0,ntau):
                            tau=self.diagTaus[j]
                            val=int(tt[j])
                            self.sndDataVar[tau,var,ilev]=val
                            self.sndData[tau,ii+1,i+1]=val
                            self.csndData[tau,ii+1,i+1]=tt[j]
                            self.sndLabels[ii+1,i+1]=label

                self.sndPlevs=mf.uniq(self.sndPlevs)

        if(self.verb > 1):

            for i in range(0,self.nlevs):
                for ii in range(0,self.nsndvars):
                    for j in range(0,ntau):
                        tau=self.diagTaus[j]
                        print 'ssss(parseDiag) ',tau,self.csndData[tau,ii+1,i+1],self.sndData[tau,ii+1,i+1]





        #ppp -- glob for fields plots to set urlData
        #

        pltpaths=[]
        tpltpaths=glob.glob("%s/*.png"%(self.pltdir))

        for tp in tpltpaths:
            if(not(mf.find(tp,'trkplt')) and not(mf.find(tp,'bm.'))): pltpaths.append(tp)

        for p in pltpaths:
            (dir,file)=os.path.split(p)
            tt=file.split('.')
            pltkey=tt[0]
            pltstm="%s.%s"%(tt[1],tt[2])
            plttau=int(tt[-2])

            # -- match the stmid to plot
            #
            if(pltstm == stmid):
                urlpath="%s/%s/%s/%s"%(self.year,self.dtg,self.model,file)
                MF.set2KeyDictList(self.urlData,plttau,pltkey,urlpath)


        #lll -- load diagVals,diagKeys,diagFilenames
        # storm

        if(self.verb): print
        for i in range(1,self.nstmvars+1):
            for j in range(0,ntau):
                tau=self.diagTaus[j]
                val=self.stmData[tau,i]
                cval=self.cstmData[tau,i]
                label=self.stmLabels[i]

                if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                    cstmkey=makekey(label)
                    if(not(cstmkey in self.diagKeys)):
                        self.diagKeys.append(cstmkey)
                    self.diagFilenames[cstmkey]="%s.%s"%(cstmkey,stmid)

                if(j == 0 and self.verb > 1):
                    print 'ssstttmmmmm %2d     %-15s %6.0f'%(i,cstmkey,val)

                MF.set2KeyDictList(self.diagVals,tau,cstmkey,cval)
                MF.set2KeyDictList(self.diagTypes,tau,cstmkey,'storm')

                try:
                    MF.set2KeyDictList(self.diaguRls,tau,cstmkey,self.urlData[tau][cstmkey])
                    if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, cstmkeky: ',tau,cstmkey,self.urlData[tau][cstmkey]
                except:
                    MF.set2KeyDictList(self.diaguRls,tau,cstmkey,'None')


        #llllllllllllllllllllllllllllllllllllllllllllllllll -- load diagVals,diagKeys,diagFilenames
        # custom

        if(self.verb): print
        for i in range(1,self.ncustomvars+1):
            for j in range(0,ntau):
                tau=self.diagTaus[j]
                val=self.customData[tau,i]
                cval=self.ccustomData[tau,i]
                label=self.customLabels[i]

                if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                    ccustomkey=makekey(label)
                    if(not(ccustomkey in self.diagKeys)):
                        self.diagKeys.append(ccustomkey)
                    self.diagFilenames[ccustomkey]="%s.%s"%(ccustomkey,stmid)

                if(j == 0 and self.verb > 1):
                    print 'ccccccccccc %2d     %-15s %6.0f'%(i,ccustomkey,val)

                MF.set2KeyDictList(self.diagVals,tau,ccustomkey,cval)
                MF.set2KeyDictList(self.diagTypes,tau,ccustomkey,'custom')

                try:
                    MF.set2KeyDictList(self.diaguRls,tau,ccustomkey,self.urlData[tau][ccustomkey])
                    if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, ccustomkey: ',tau,ccustomkey,self.urlData[tau][ccustomkey]
                except:
                    MF.set2KeyDictList(self.diaguRls,tau,ccustomkey,'None')

        #llllllllllllllllllllllllllllllllllllllllllllllllll -- load diagVals,diagKeys,diagFilenames
        # sounding

        if(self.verb): print
        for i in range(1,self.nlevs+1):
            for ii in range(1,self.nsndvars+1):
                for j in range(0,ntau):
                    tau=self.diagTaus[j]
                    val=self.sndData[tau,ii,i]
                    cval=self.csndData[tau,ii,i]
                    label=self.sndLabels[ii,i]
                    if(tau == self.diagTaus[0] or len(self.diagTaus) == 1):
                        csndkey=makekey(label)
                        if(not(csndkey in self.diagKeys)):
                            self.diagKeys.append(csndkey)
                        self.diagFilenames[csndkey]="%s.%s"%(csndkey,stmid)

                    MF.set2KeyDictList(self.diagVals,tau,csndkey,cval)
                    MF.set2KeyDictList(self.diagTypes,tau,csndkey,'sounding')

                    if(j == 0 and self.verb > 1):
                        print 'sssdddnnngg %2d %2d  %-15s %6.0f'%(ii,i,csndkey,val)

                    try:
                        MF.set2KeyDictList(self.diaguRls,tau,csndkey,self.urlData[tau][csndkey])
                        if(self.verb): print 'sssssssssssssssssssss setting diaguRLs tau, csndkey: ',tau,csndkey,self.urlData[tau][csndkey]
                    except:
                        MF.set2KeyDictList(self.diaguRls,tau,csndkey,'None')

        if(self.verb): print
        for kk in self.diagKeys:
            card=kk
            for tau in self.diagTaus:
                card="%15s %5s"%(card,self.diagVals[tau][kk])
            if(self.verb): print 'parseDiag:',card

        # -- set the taus
        #
        self.taus=self.diagTaus

        return(rc)


    def makeJsInv(self,getStmVars,getCusVars=[],phr=None,stmid=None):

        allprods=[]
        js={}

        oVarDictTaus={}
        oVarDictVals={}

        if(phr != None):
            if(phr == 'p06'):
                phrP=phrP06
            elif(phr == 'p12'):
                phrP=phrP12

            phrs=phrP.keys()
            phrv=phrP.values()
            phrs.sort()
            phrv.sort()

        # -- ssssssssssssssssssssssssssss storm vars
        #

        for kk in self.stmData.keys():

            (itau,ndxvar)=kk

            if(phr != None):

                #print 'kk: ',self.model,kk,itau,(itau in phrs or (61 in phrs)),phrs

                if((61 in phrs)):
                    otau=999
                    if(itau in phrs):
                        otau=phrP[itau]
                        # -- special case where no 48 hour in keys because we signal 61 was a dup for 42 & 48 h
                        if(otau == 42):
                            otau48=48
                            for gvar in getStmVars:
                                ovar=self.stmVarNameByIndex[ndxvar]
                                if(ovar == gvar):
                                    
                                    allprods.append(ovar)
                                    val=self.stmData[kk]
                                    
                                    # -- get adeck Vmax
                                    if(ovar == 'max_wind'): 
                                        ukk=(kk[0],1)
                                        uval=self.customData[ukk]
                                        val=uval
                                        
                                    #print '============mmmm',self.model,stmid,gvar,otau48,val
                                    #print 'qqq',self.model,self.curstmid,self.dtg,ovar,itau,otau,val
                                    MF.appendDictList(oVarDictTaus, gvar, otau48)
                                    oVarDictVals[gvar,otau48]=val

                if(itau in phrs):
                    otau=phrP[itau]
                else:
                    continue

            else:
                otau=itau

            if(not(otau in allJTdiagTaus)): continue

            for gvar in getStmVars:
                ovar=self.stmVarNameByIndex[ndxvar]
                if(ovar == gvar):
                    val=self.stmData[kk]
                    # -- get adeck Vmax
                    if(ovar == 'max_wind'): 
                        ukk=(kk[0],1)
                        uval=self.customData[ukk]
                        val=uval
                        #print 'got it',kk,'val: ',val,'model: ',self.model,self.stmids,'uval: ',uval
                    #print 'qqq',self.model,self.curstmid,self.dtg,ovar,itau,otau,val
                    MF.appendDictList(oVarDictTaus, gvar, otau)
                    oVarDictVals[gvar,otau]=val

        # -- custom vars
        #
        for kk in self.customData.keys():
            (itau,ndxvar)=kk
            if(phr != None):

                if((61 in phrs)):
                    otau=999
                    if(itau in phrs):
                        otau=phrP[itau]
                        # -- special case where no 48 hour in keys because we signal 61 was a dup for 42 & 48 h
                        if(otau == 42):
                            otau48=48
                            for gvar in getCusVars:
                                ovar=self.customVarNameByIndex[ndxvar]
                                if(ovar == gvar):
                                    allprods.append(ovar)
                                    # -- display in table pmin vice predcip
                                    #
                                    ckk=kk
                                    if(gvar == 'precip'): ckk=(itau,3)
                                    val=self.customData[ckk]
                                    MF.appendDictList(oVarDictTaus, gvar, otau48)
                                    oVarDictVals[gvar,otau48]=val

                if(itau in phrs):
                    otau=phrP[itau]
                else:
                    continue

            else:
                otau=itau

            if(not(otau in allJTdiagTaus)): continue

            for gvar in getCusVars:
                ovar=self.customVarNameByIndex[ndxvar]
                if(ovar == gvar):
                    # -- display in table pmin vice predcip
                    #
                    ckk=kk
                    if(gvar == 'precip'): ckk=(itau,3)
                    val=self.customData[ckk]
                    MF.appendDictList(oVarDictTaus, gvar, otau)
                    oVarDictVals[gvar,otau]=val

        for ovar in oVarDictTaus.keys():

            otaus=oVarDictTaus[ovar]
            otaus.sort()

            jskey='%s-%s-%s-%s'%(self.model,self.curstmid,self.dtg,ovar)
            card0="""dtgStmDict['%s'] =
[
"""%(jskey)
            card1='   [ '
            card2='   [ '
            for otau in otaus:
                val=oVarDictVals[ovar,otau]
                #print 'ooo',self.model,self.curstmid,self.dtg,ovar,otau,val
                cotau="""'%d'"""%(otau)
                coval="""'%d'"""%(val)
                card1=card1+"%6s,"%(cotau)
                card2=card2+"%6s,"%(coval)

            card1=card1+""" ],
"""
            card2=card2+""" ],
]
"""

            js[jskey]=card0+card1+card2

            #print 'iiii',js[jskey]

            allprods=mf.uniq(allprods)

        return(allprods,js)



    def initGA(self,gaopt=None,Quiet=1):

        if( not(hasattr(self,'ga')) and not(hasattr(self,'ge')) ):

            from ga2 import setGA
            ga=setGA(Quiet=Quiet,Bin=self.xgrads)
            ga.fh=ga.open(self.ctlpath)
            # -- don't open here
            #if(self.ctlpath2 != None): ga.fh=ga.open(self.ctlpath2)
            ge=ga.ge
            ge.fh=ga.fh
            ge.getFileMeta()

            # -- tell the oisst class the file is not opened
            #
            ga.oisstOpened=0

            self.ga=ga
            self.ge=ge
            self.ge.getLevs()
            # -- set jaecolw2 colors
            self.ge.setColorTable()

    def getTCdiagStorms(self,istmids):

        ostmids=[]

        for istmid in istmids:
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(istmid)
            if(b1id in tcdiagBasins):
                ostmids.append(stm1id)

        return(ostmids)



    def getFRlocal(self,model,dtg,verb=0):

        FE=FM.setFE(dtg,model)
        FElocal=FM.setFE(dtg,model,fmodel=FE.fmodel,expopt=FE.expopt,sroot=FM.trootWjet,troot=FM.lrootLocal,npes=FE.npes,glvl=FE.glvl)
        FRlocal=FM.FimRun(FElocal,gribver=2)

        FRlocal.m2=setModel2('rtfim')

        return(FRlocal)


    def initM2(self,dtg,model,verb=0,override=0,bypassModel2=1):


        if( not( (model in (FM.wjetmodels + FM.taccmodels) ) or ( model in w2.Nwp2ModelsAll) )
            and not(bypassModel2)
            ):
            print 'EEE(initM2) invalid model: ',model
            sys.exit()

        if(model in (FM.wjetmodels + FM.taccmodels) ):
            FR=self.getFRlocal(model,dtg)

            if(FR == None):
                print 'EEE FM not available for model: ',model,' dtg: ',dtg
                sys.exit()
            else:
                m2=FR.m2

            # -- need to run this to get tdattaus on FR

            FR.LsGrib()

            self.ctlpath=FR.ctlpath

            self.dtaus=FR.tdattausData

            self.m2=m2

            self.adecksource=model
            if(model == 'rtfimy'):  self.adeckaid='f8cy'
            if(model == 'rtfim9'):  self.adeckaid='fim9'
            if(model == 'rtfim'):  self.adeckaid='fim8'

            self.setprvar=m2.setprvar
            self.modelprvar=m2.modelprvar

            self.modeltype='rtfim'


        else:

            m2=M2.setModel2(model)
            dom2=1
            dmodelType='w2flds'


##             self.bddir="%s/%s/dat/%s"%(w2.Nwp2DataBdir,dmodelType,model)
##             m2.bddir=self.bddir

##             m2.dmodel="%s.%s"%(model,dmodelType)
##             m2.lmodel=m2.dmodel
##             m2.dmodelType=dmodelType


##             def name2tau(file,dtg):
##                 try:
##                     tau=file.split('.')[3][1:]
##                     tau=int(tau)
##                 except:
##                     tau=None
##                 return(tau)

##             m2.name2tau=name2tau

            fm=m2.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,diag=1)
            fd=fm.GetDataStatus(dtg)

            self.m2=m2
            self.ctlpath=m2.dpath
            self.dtaus=m2.dsitaus
            self.adeckaid=m2.adeckaid
            self.adecksource=m2.adecksource
            self.setprvar=m2.setprvar
            self.modelprvar=m2.modelprvar

            # -- code to handle rtfim
            #
            if(hasattr(m2,'modeltype') and m2.modeltype == 'rtfim'):
                self.modeltype=m2.modeltype
                if(model == 'rtfimy'):  self.adeckaid='f8cy'
                if(model == 'rtfim9'):  self.adeckaid='fim9'
                if(model == 'rtfim'):   self.adeckaid='fim8'
            else:
                self.modeltype='w2flds'

            if(len(self.dtaus) == 0):
                return(1)



        return(0)


    def initAD(self,dtg,model,mfversion='v011',doZip=1,verb=0):

        def getADTM(apathT,apathM,verb=0):

            aDT=Adeck(apathT,verb=verb,aliases=self.aidAliases)
            aDM=Adeck(apathM,verb=verb,aliases=self.aidAliases)
            aD=copy.deepcopy(aDT)

            if(verb):
                print 'TcDiag.initAD(longest) aaaaaT ',apathT
                print 'TcDiag.initAD(longest) aaaaaM ',apathM

            return(aDT,aDM,aD)


        def getAdeckApathMFtrkN(apath):

            (adir,afile)=os.path.split(apath)

            aa=adir.split('/')
            dtg=aa[-1]
            source=aa[-3]
            yyyy=dtg[0:4]
            yyyymm=dtg[0:6]

            afileMask=afile.replace('*','')

            if(source == 'tmtrkN'):
                zipDir=TcAdecksTmtrkNDir
            elif(source == 'mftrkN'):
                zipDir=TcAdecksMftrkNDir

            zipPath="%s/%s/%s-%s.zip"%(zipDir,yyyy,source,yyyymm)
            rc=MF.ChkPath(zipPath)
            if(rc == 0):
                print 'EEE-AdeckGen2.initAdeckPathsZip zipPath: ',zipPath,' not there sayounara'
                sys.exit()

            AZ=zipfile.ZipFile(zipPath)
            zls=AZ.namelist()   
            adpaths=[]
            for zl in zls:
                if(mf.find(zl,afileMask)):
                    adpaths.append(zl)

            adeckCards=[]
            for adpath in adpaths:
                adcards=AZ.open(adpath).readlines()
                adeckCards=adeckCards+adcards

            aD=Adeck(apath,adeckCards=adeckCards,verb=verb,aliases=self.aidAliases)

            return(aD)

        def getAdeckApath(apath):

            (adir,afile)=os.path.split(apath)

            aa=adir.split('/')
            dtg=aa[-1]
            source=aa[-3]
            yyyy=dtg[0:4]
            yyyymm=dtg[0:6]

            if(source == 'tmtrkN'):
                zipDir=TcAdecksTmtrkNDir
            elif(source == 'mftrkN'):
                zipDir=TcAdecksMftrkNDir

            zipPath="%s/%s/%s-%s.zip"%(zipDir,yyyy,source,yyyymm)
            rc=MF.ChkPath(zipPath)
            if(rc == 0):
                print 'EEE-AdeckGen2.initAdeckPathsZip zipPath: ',zipPath,' not there sayounara'
                sys.exit()

            AZ=zipfile.ZipFile(zipPath)
            zls=AZ.namelist()            
            adpath="%s/%s"%(dtg,afile)

            adeckCards=[]
            if(adpath in zls):
                adeckCards=AZ.open(adpath).readlines()
            else:
                print 'EEE could not find: ',adpath,' in zipPath: ',zipPath

            aD=Adeck(apath,adeckCards=adeckCards,verb=verb,aliases=self.aidAliases)

            return(aD)

        def getADTMZip(apathT,apathM,verb=0):

            aDT=getAdeckApath(apathT)

            aDM=getAdeckApathMFtrkN(apathM)
            aD=copy.deepcopy(aDT)

            if(verb):
                print 'TcDiag.initAD(longest) aaaaaT ',apathT
                print 'TcDiag.initAD(longest) aaaaaM ',apathM

            return(aDT,aDM,aD)


        dosdir=0
        if(hasattr(self,'adeckSdir')):
            sdir=self.adeckSdir
        elif(hasattr(self,'sdir')):
            sdir=self.sdir
            dosdir=1

        # -- long for tracker with greatest taus in mftrkN or tmtrkN
        #
        didADlongest=0
        if(self.trkSource == 'longest' or self.trkSource == 'tmtrkN'):
            
            # -- don't use sink
            #
            spath=None

            if(dosdir):
                apathT="%s/%s/%s/tctrk.atcf.%s.%s.txt"%(sdir,dtg,model,dtg,model)
                spathT="%s/%s/%s/tctrk.sink.%s.%s.txt"%(sdir,dtg,model,dtg,model)
                apathM="%s/%s/%s/wxmap2.%s.%s.%s.*"%(sdir,dtg,model,mfversion,model,dtg)
                spathM=None
            else:
                if(mf.find(sdir,'adeck')):
                    sdirTM=TcAdecksTmtrkNDir
                    sdirMF=TcAdecksMftrkNDir
                    yyyy=dtg[0:4]
                    apathT="%s/%s/%s/tctrk.atcf.%s.%s.txt"%(sdirTM,yyyy,dtg,dtg,model)
                    spathT="%s/%s/%s/tctrk.sink.%s.%s.txt"%(sdirTM,yyyy,dtg,dtg,model)
                    apathM="%s/%s/%s/wxmap2.%s.%s.%s.*"%(sdirMF,yyyy,dtg,mfversion,model,dtg)
                    spathM=None
                else:
                    apathT="%s/tctrk.atcf.%s.%s.txt"%(sdir,dtg,model)
                    spathT="%s/tctrk.sink.%s.%s.txt"%(sdir,dtg,model)
                    apathM="%s/wxmap2.%s.%s.%s.*"%(sdir,mfversion,model,dtg)
                    spathM=None


            # -- make the V1 Adecks from the paths
            #
            if(doZip):
                (aDT,aDM,aD)=getADTMZip(apathT, apathM, verb)
            else:
                (aDT,aDM,aD)=getADTM(apathT, apathM, verb)

            Tstm2ids=aDT.stm2ids
            Mstm2ids=aDM.stm2ids
            Tstm1ids=aDT.stm1ids
            Mstm1ids=aDM.stm1ids

            # -- get the aid names from the aD obj
            #
            try:
                Taid=aDT.aids[0]
            except:
                Taid=model
            try:
                Maid=aDM.aids[0]
            except:
                Maid=model


            Astm2ids=Tstm2ids+Mstm2ids
            Astm2ids=mf.uniq(Astm2ids)

            FtrkSource={}
            Fstm2ids=[]
            Fstm1ids=[]
            Faidstms=[]

            Faidcards={}
            Faidtaus={}
            Faidtrks={}

            nM=0
            nT=0


            for stm2id in Astm2ids:

                Ttaus=[]
                Mtaus=[]
                Tlasttau=-999
                Mlasttau=-999


                try:
                    Ttrks=aDT.aidtrks[Taid,stm2id][self.dtg]
                    Tcards=aDT.aidcards[Taid,stm2id][self.dtg]
                    Tstm1id=aDT.stm1ids[Tstm2ids.index(stm2id)]
                    Ttaus=Ttrks.keys()
                except:
                    Tstm1id=None


                try:
                    Mtrks=aDM.aidtrks[Maid,stm2id][self.dtg]
                    Mcards=aDM.aidcards[Maid,stm2id][self.dtg]
                    Mstm1id=aDM.stm1ids[Mstm2ids.index(stm2id)]
                    Mtaus=Mtrks.keys()
                except:
                    Mstm1id=None

                Ttaus.sort()
                Mtaus.sort()
                nTtaus=len(Ttaus)
                nMtaus=len(Mtaus)

                if(nTtaus > 0): Tlasttau=Ttaus[-1]
                if(nMtaus > 0): Mlasttau=Mtaus[-1]

                Tmintau=72

                if(verb): print 'TcDiag.initAD(longest) SSS ',stm2id,'nTM taus: ',nTtaus,'nM Ftaus: ',nMtaus,' Tlasttau: ',Tlasttau,' Mlasttau: ',Mlasttau

                # -- conditions to use tmtrkN
                #

                useTM=(nTtaus > 0 and (Tlasttau >= Mlasttau or Tlasttau > Tmintau) and Tstm1id != None)
                useMF=(nMtaus > 0 and Mstm1id != None)

                # --------------------------------- only use tmtrk for ukm2 -- problem with models with gaps in the taus/fields/levels
                # -- 20140318 -- OBE?
                #
                #if( (model == 'ukm2' or model == 'fim8') ):
                    #if(useTM):
                        #useTM=1
                    #else:
                        #useTM=0
                        #useMF=0

                if(self.trkSource == 'tmtrkN'): 
                    
                    useTM=1
                    if(nTtaus == 0):useTM=0
                    useMF=0
                    
                if(useTM):

                    Tstm1id=getFinalStm1idFromStmids(Tstm1id,self.stmids)
                    if(verb): print 'TcDiag.initAD(longest) uuuTTT ',Tstm1id,stm2id,'Tlasttau: ',Tlasttau

                    FtrkSource[Tstm1id]='tmtrkN'

                    Fstm2ids.append(stm2id)
                    Fstm1ids.append(Tstm1id)

                    MF.set2KeyDictList(Faidtrks, (Taid,stm2id),self.dtg,Ttrks)
                    MF.set2KeyDictList(Faidtaus, (Taid,stm2id),self.dtg,Ttrks.keys())
                    MF.set2KeyDictList(Faidcards,(Taid,stm2id),self.dtg,Tcards)
                    nT=nT+nTtaus

                elif(useMF):

                    Mstm1id=getFinalStm1idFromStmids(Mstm1id,self.stmids)
                    if(verb): print 'TcDiag.initAD(longest) uuuMMM ',Mstm1id,stm2id,' Mlasttau: ',Mlasttau

                    FtrkSource[Mstm1id]='mftrkN'

                    Fstm2ids.append(stm2id)
                    Fstm1ids.append(Mstm1id)
                    MF.set2KeyDictList(Faidtrks, (Maid,stm2id),self.dtg,Mtrks)
                    MF.set2KeyDictList(Faidtaus, (Maid,stm2id),self.dtg,Mtrks.keys())
                    MF.set2KeyDictList(Faidcards,(Maid,stm2id),self.dtg,Mcards)
                    nM=nM+nMtaus

                else:
                    FtrkSource[Mstm1id]=None
                    if(verb): print """TcDiag.initAD(longest) NOLOAD--------------- can't find good tracker for  OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOops""",Mstm1id



            #aDT.ls()
            #aDM.ls()
                    
            aD.stm1ids=Fstm1ids
            aD.stm2ids=Fstm2ids
            aD.aidtrks=Faidtrks
            aD.aidtaus=Faidtaus
            aD.aidcards=Faidcards
            self.FtrkSource=FtrkSource

            #print aDM.aidtrks['ecmt','wp09.2012'][self.dtg].keys()
            #print Faidtrks['ecmt','wp09.2012'][self.dtg].keys()
            #aDT.ls()
            #aD.ls()

            if(self.trkSource == 'longest'):
                self.trkSource='mftrkN'
                self.apath=apathM
                self.spath=spathM
                if(nT >= nM):
                    self.trkSource='tmtrkN'
                    self.apath=apathT
                    self.spath=spathT
                    
                didADlongest=1
                    
            elif(self.trkSource == 'tmtrkN'):
                
                self.trkSource='tmtrkN'
                self.apath=apathT
                self.spath=spathT
                didADlongest=0

            self.aD=aD

           
        else:
            print 'EEE invalid trkSource: ',trkSource
            sys.exit()


        self.aid=self.adeckaid
        if(not(mf.find(model,'rtfim'))): self.aid=model

        # -- if not doing longest...
        #
        if(not(didADlongest) and self.trkSource == 'longest'):

            useyear=0
            if(useyear):
                adps=AtcfAdeckPaths(adecks=[apath])
                year=dtg[0:4]
                aDs=MakeAdecksByYear(adps,year,verb=verb,aliases=self.aidAliases)
                print 'AAAAAAAAAAAAAAAA ',aDs.keys()
            else:
                self.aD=Adeck(self.apath,verb=verb,aliases=self.aidAliases)


        # -- since we're only doing one aid, pull first aid in aids
        #
        if(len(self.aD.aids) > 0): self.aidname=self.aD.aids[0]

        if(self.spath != None and not(didADlongest)):
            self.aDS=AdeckSink(self.spath,verb=self.verb)
        else:
            self.aDS=None

        if((self.verb or verb) and not(didADlongest) ):
            print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA apath: ',self.apath,' self.aid: ',self.aid,' self.adeckaid ',self.adeckaid,' model: ',model
            if(self.spath != None): print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS spath: ',self.spath

        self.adstm2ids=self.aD.stm2ids
        self.didADlongest=didADlongest



    def initTC(self,dtg,useDSs=0):

        if(not(hasattr(self,'tD')) or self.tD == None):
            print 'III(initTC): making tD object'
            self.tD=TcData(dtgopt=dtg)

        (self.stmids,self.btcs)=self.tD.getDtg(self.dtg,selectNN=self.selectNN,dobt=self.dobt,dupchk=0)
        self.stmids.sort()

        if(useDSs):
            ostmids=self.tD.getDSsDtg(self.dtg)
            self.stmids=ostmids



    def getTCinfo(self,stmid):

        self.bts=self.tD.getBtLatLonVmax(stmid,stmdtg=self.dtg)
        try:    self.tcvmax=self.bts[self.dtg][2]
        except: self.tcvmax=-999

        (self.stm3id,self.stmname)=self.tD.getStmName3id(self.stmid)

        rc=(self.bts,self.tcvmax,self.stm3id,self.stmname)
        return(rc)


    def lsTC(self):

        print "Dtg: %s"%(self.dtg)
        for stmid in self.stmids:
            btc=self.tD.getBtc4StmidDtg(stmid,self.dtg,selectNN=self.selectNN)
            if(len(btc) == 0):
                print 'WWWWWW no BT for ',stmid,' at dtg: ',self.dtg
            else:
                (rlat,rlon,rvmax,rpmin)=btc[0:4]
                (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
                #print "%s %s %s %03d %4.0f"%(stmid,clat,clon,int(rvmax),float(rpmin))

    def makeTCmeta(self,taus=None,tdir='/tmp',verb=0):

        stmid=self.stmid.lower()

        (stm3id,stmname)=self.tD.getStmName3id(stmid)
        stm2id=stm1idTostm2id(stmid)

        filename="tcmeta.%s.%s.%s.txt"%(stmid,self.model,self.dtg)
        self.mpath="%s/%s"%(tdir,filename)

        acards=[]
        metas={}
        otaus=[]
        trk={}


        if(taus == None):
            ttaus=self.aidtaus
        else:
            ttaus=taus

        for tau in self.aidtaus:
            print 'qqq',tau,self.aidtrk[tau]
            if(not(tau in ttaus) or len(self.aidtrk[tau]) == 0): 
                if(len(self.aidtrk[tau] == 0)):
                    print 'WWW-TcDiag.metaTCmeta no posits for tau: ',tau,' press...'
                    rc=-1
                continue
            
            otaus.append(tau)
            lat=self.aidtrk[tau][0]
            lon=self.aidtrk[tau][1]
            vmax=self.aidtrk[tau][2]
            pmin=self.aidtrk[tau][3]

            # -- check for undef - messes up read in lsdiag.x
            #
            if(vmax < 0.0): vmax=-99
            if(pmin < 0.0): pmin=-999

            dir=self.aidMotion[tau][0]
            spd=self.aidMotion[tau][1]
            ometa="""%3d %5.1f %6.1f %3d %4.0f %3.0f %4.1f"""%(tau,lat,lon,vmax,pmin,dir,spd)
            metas[tau]=ometa
            trk[tau]=[lat,lon,vmax,pmin,[],[]]

        diagfileAid=self.model
        if(hasattr(self,'aidname')): diagfileAid=self.aidname
        meta="""%-6s %10s %s %s %-9s
nt: %3d (taus)"""%(diagfileAid.upper(),self.dtg,stmid.upper(),stm2id.upper(),stmname[0:9].upper(),
                   len(otaus)
                   )

        # -- set return code to signal if no trackers
        #
        if(len(otaus) > 0): rc=1
        else:               rc=-1
        
        for otau in otaus:
            meta="""%s
%s"""%(meta,metas[otau])

        MF.WriteString2File(meta,self.mpath,verb=verb)
        if(verb): MF.listTxtPath(self.mpath)


        if(len(trk) > 0):
            acards=MakeAdeckCards(self.aid,self.dtg,trk,self.stmid)
            if(verb): 
                for acard in acards:
                    print 'acard: ',acard[:-1]

        self.oadeck=acards
        self.aidcards=acards
        return(rc)


    def setTCtracker(self,stmid,aidSource=None,aidnameOverride=None,maxtau=168,quiet=0,verb=0):


        # -- find BT tracks to subsitute if model tracker fails
        #
        def makeBTaidtrk(stmid,dtg,etau=24,dtau=6,verb=0):

            def btcs2aidtrk(btcs,btdtg):
                
                btl=[]
                try:
                    tt=btcs[btdtg]
                except:
                    if(verb): print 'problem with btcs for: ',stmid,btdtg
                    return(btl)

                r34=tt[-3]
                r50=tt[-2]
                
                br34=None
                br50=None
                if(r34 != None): br34=tuple(r34)
                if(r50 != None): br50=tuple(r50)
                btl=[tt[0],tt[1],tt[2],tt[3],br34,br50,None]
                
                return(btl)
            
            bttrk={}
            bttaus=[]
    
            btcs=self.tD.getBtcs4Stmid(stmid,dtg,dupchk=0,selectNN=0)
            btdtgs=mf.dtgrange(self.dtg,mf.dtginc(self.dtg,24))
            for btdtg in btdtgs:
                tau=mf.dtgdiff(self.dtg,btdtg)
                itau=int(tau)
                bttaus.append(itau)
                btl=btcs2aidtrk(btcs,btdtg)
                bttrk[itau]=btl
    
            if(verb):
                for tau in range(0,etau+1,dtau):
                    print 'bbb---',tau,bttrk[tau]
    
            return(bttrk,bttaus)    



        usingBTs=0

        # -- make BT equiv of aidtrk
        #
        (bttrk,bttaus)=makeBTaidtrk(stmid,self.dtg)

        if(verb):
            print 'BBBBBBBBBBBBBBBBBB',stmid
            for bttau in bttaus:
                print 'bbb',bttau,bttrk[bttau]

        
        if(aidSource != None):
            tt=aidSource.split('.')
            if(len(tt) != 2):
                print 'EEE TCdiag.setTCtracker.aidSource not well formed, should be AAAA.SSSSS but is: ',aidSource
                return(0)

            aid=tt[0]
            source=tt[1]

            self.getAidtrkFromAdss(self.dtg,stmid,sources=source,adeckaid=aid)


            if(self.ADaidtaus != None):
                self.aid=aid
                self.aidtrk=self.ADaidtrk
                self.aidtaus=self.ADaidtaus
                self.aidsource=source
                self.aidname=aid
                self.stmid=stmid

            else:
                print 'WWW TCdiag.setTCtracker no aD for source: ',source,' aid: ',aid,' stmid: ',stmid
                return(0)


            do6hinterp=1
            if(do6hinterp):
                aDu=ADutils()
                (iatrk,itaus)=aDu.FcTrackInterpFill(self.aidtrk,dtx=6)
                itaus=iatrk.keys()
                itaus.sort()
                self.aidtrk=iatrk
                self.aidtaus=itaus


        else:

            # -- case where we make aD from tmtrkN or mftrkN cards in initAD()
            #

            if(self.aD != None):

                self.stmid=stmid
                self.getAidtrk(self.dtg,self.stmid)
                rcg=self.getAidcards(self.dtg,self.stmid)
                ntaus1=0
                lasttau1=0

                if(self.aidtaus != None):
                    aidtrks1=self.aidtrk
                    aidtaus1=self.aidtaus
                    ntaus1=len(self.aidtaus)
                    lasttau1=aidtaus1[-1]
                else:
                    # -- bail point 0 -- no tracker taus for aid
                    #
                    if(len(bttaus) > 0):
                        if(verb): print 'III we do...substitute BT for: ',self.stmid,' even though there is a tracker... '
                        aidtrks1=bttrk
                        aidtaus1=bttaus
                        self.aidsource='best'
                        self.aidname='best'
                        #self.stmid=stmid
                        usingBTs=1
                        self.FtrkSource[self.stmid]='best'
                        
                    else:
                        if(not(quiet) and rcg == 1): 
                            print '1111111 WWW bail point 0 noadeck cards                                  aid:  %s  stmid:  %s 0000000'%(self.model,stmid)
                        return(0)

            else:

                # -- bail point 1 -- no tracker taus for aid
                #
                print "WWW(TcDiag.setTCtracker) no trackers for %s"%(self.trkSource)
                print "III checking if best track is available..."
                if(len(bttaus) > 0):
                    if(verb): print 'III we do...substitute BT for: ',self.stmid,' ... '
                    aidtrks1=bttrk
                    aidtaus1=bttaus
                    usingBTs=1
                    self.aidsource='best'
                    self.aidname='best'
                    self.stmid=stmid
                    self.FtrkSource[self.stmid]='best'
                else:
                    print "2222222 no joy with BT -- sayounara..."
                    return(0)

            self.aidtrk=aidtrks1
            self.aidtaus=aidtaus1
            
            # -- decorate with bt lat/lon/vmax
            #
            if(len(bttrk[0]) > 0):
                if(verb): print '000',bttrk[0]
                self.blat0=bttrk[0][0]
                self.blon0=bttrk[0][1]
                self.bvmx0=bttrk[0][2]
            elif(len(bttrk[6]) > 0):
                if(verb): print '666',bttrk[6]
                self.blat0=bttrk[6][0]
                self.blon0=bttrk[6][1]
                self.bvmx0=bttrk[6][2]
            elif(len(bttrk[12]) > 0):
                if(verb): print '121',bttrk[12]
                self.blat0=bttrk[12][0]
                self.blon0=bttrk[12][1]
                self.bvmx0=bttrk[12][2]
            else:
                if(verb): print '999',bttrk[0]
                self.blat0=-99.
                self.blon0=-999.
                self.bvmx0=-99
                

            
            # -- when setting trkSource='longest' -- lllllllllllllllllllllllllllllllllllllllooooonnnnngggggeeeeesssstttt
            #
            if(hasattr(self,'FtrkSource')):
                try:
                    self.aidsource=self.FtrkSource[stmid]
                except:
                    # --- set if not there...set to None
                    self.aidsource=None
            else:
                self.aidsource=self.trkSource

            # -- bail point 2 -- no tracker taus for aid
            #
            if(len(self.aidtaus) == 0):
                print 'WWW(%s)'%(self.basename),'no final  tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
                return(0)

            # -- bail point 3 -- singleton -- rlat 0/0...do it if ok
            #
            if(len(self.aidtaus) == 1):

                trk0=self.aidtrk[self.aidtaus[0]]
                if( len(trk0) >= 1 and trk0[0] == 0.0 or trk0[1] == 0.0):
                    print 'WWW(%s)'%(self.basename),'singleton trk = 0,0 taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
                    return(0)


            self.diagpath="%s/diag.%s.%s.txt"%(self.pltdir,self.stmid,self.model)

            self.pyppathDiag="%s/diag.%s.pyp"%(self.pltdir,self.stmid)
            self.pyppathHtml="%s/html.%s.pyp"%(self.pltdir,self.stmid)
            self.pyppathData="%s/data.%s.pyp"%(self.pltdir,self.stmid)
            self.diagpathALL="%s/diag.all.%s.%s.txt"%(self.pltdir,self.stmid,self.model)
            self.diagpathWebALL="%s/diag.all.%s.%s.txt"%(self.webdiagdir,self.stmid,self.model)

            self.pyppathDataALL="%s/data.all.%s.pyp"%(self.pltdir,self.stmid)
            
            if(self.doDiagOnly):
                self.diagpath=self.diagpathALL
                self.pyppathData=self.pyppathDataALL


        # -- limit taus
        ataus=[]
        if(maxtau != None):
            for atau in self.aidtaus:
                if(atau in self.targetTaus):
                    ataus.append(atau)
            self.aidtaus=ataus


        # -- look for case where there are no tracker taus in data taus from above
        #
        if(len(self.aidtaus) == 0): return(0)

        if(self.aidtrk != None and quiet != 1):
            print 'TCTCTCTC got tracker from aidsource: %-10s'%(self.aidsource),' model: %-6s'%(self.model),\
                  ' aid: ',self.aid,' dtg: ',self.dtg,\
                  ' stmid: ',self.stmid,\
                  " BT: %3d %5.1f %6.1f"%(self.bvmx0,self.blat0,self.blon0),\
                  ' ntaus: %3d'%(len(self.aidtaus)),' lasttau: %3d'%(self.aidtaus[-1])

        self.aidMotion={}

        # -- get the motion based on the next tau
        #
        ntaus=len(self.aidtaus)

        for tau in self.aidtaus:

            # -- get track for spd/dir calc
            taup0=tau
            rc=self.aidtrk[taup0]
            if(len(rc) == 0):
                dt=0
            else:
                (latcp0,loncp0,vmaxcp0,pmincp0)=rc[0:4]

            np=self.aidtaus.index(tau)

            # -- check if at end of tau...
            #
            if(np == ntaus-1):
                np=np-1
                taup0=self.aidtaus[np]
                rc=self.aidtrk[taup0]
                if(len(rc) == 0):
                    dt=0
                else:
                    (latcp0,loncp0,vmaxcp0,pmincp0)=rc[0:4]

            # -- get track at next tau
            #
            np1=np+1
            taup1=self.aidtaus[np1]
            rc=self.aidtrk[taup1]
            tauP1point=1
            if(len(rc) == 0):
                tauP1point=0
                dt=0
            else:
                (latcp1,loncp1,vmaxcp1,pmincp1)=rc[0:4]
                dt=taup1-taup0

            if(dt == 0):
                dir=9999.
                spd=9999.
            else:
                (dir,spd,umot,vmot)=rumhdsp(latcp0,loncp0,latcp1,loncp1,taup1-taup0)
                if(dir == 360.0): dir=0.0

            # -- bug in setting the endpoint, bandaid for now...
            #
            if(spd < 0.0):
                spd=9999.
                dir=9999.

            self.aidMotion[tau]=(dir,spd)

        # -- set name for iships.x which is the point of the classs -- run lgem
        #
        if(mf.find(self.aidsource,'tmtrk')):
            self.aidname='t'+self.model[0:3]
        elif(mf.find(self.aidsource,'best')):
            self.aidname='b'+self.model[0:3]
        elif(mf.find(self.aid,'ofci')):
            self.aidname='o'+self.model[0:3]
            # - for setting only initial sst and then undef
            self.aidname='s'+self.model[0:3]
            self.aidname='a'+self.model[0:3]
        else:
            self.aidname='x'+self.model[0:3]


        if(aidnameOverride != None):
            self.aidname=aidnameOverride

        return(1)


    def chKOutput(self,dtg,tbdir,dstmids=None,aidSource=None,rc=None,quiet=0):


        # -- 20230816 -- do inventory here so the file doesn't hang open
        #
        year=dtg[0:4]
        tbdirInv="%s/%s"%(tbdir,year)
        dbname='invTcdiag.%s'%(dtg)
        
        print '--------------TcTcDiag.Output'
        print 'TcDiag.chKOutput -- CCCKKKOOO -- Output dtg: ',dtg

        inv={}

        if(dstmids == None):
            iV=InvHashTD(dbname=dbname,tbdir=tbdirInv)
            inv='dstmids=None'
            if(rc != None): inv=inv+rc
            iV.hash[self.model,self.dtg]=inv
            iV.put()
            iV.close()
            print '--------------TcTcDiag.Output -- NO STORMS done yet....'
            print 
            return(-2)

        if(aidSource != None and len(aidSource.split('.')) == 2):
            self.aidsource=aidSource.split('.')[1]
            self.aid=aidSource.split('.')[0]

        todoStmids=[]
        sizStmid=[]

        for stmid in dstmids:
            rctrk=self.setTCtracker(stmid,aidSource,quiet=quiet)
            if(rctrk == 0): continue
            (rcdiag,dtime,dpath)=self.setDiagPath(stmid,tbdir=self.tbdir)
            sizStmid.append(rcdiag)
            if(rcdiag == -999):
                todoStmids.append(stmid)
                rcdiag=('notrun yet')
            inv[stmid]=rcdiag

        if(len(dstmids) == 0):
            inv=('no tcs or no tcs in TCdiag.tcdiagBasins')
            print 'WWW(chKoutput): ',inv
            status=-2

        status=0
        if(len(sizStmid) == 0): status=-1
        elif(max(sizStmid) <= 0): status=-1
        elif(len(todoStmids) > 0): status=-2

        if(status == -1):
            print """WWW TCdiagN.setDiagPath: hasn't been run yet..."""
        elif(status == -2):
            print """WWW TCdiagN.setDiagPath: hasn't been run yet...for these storms: """,todoStmids
        else:
            if(not(quiet)):
                print
                print '''IIIIIIIIIIII -- already run; use -O(override=1)  or -o (TDoverride= test-trkplot | test-htmlonly | test-plot-html) to override'''
                print

        print '-------------- TcTcDiag.Output -- DDDDOOO SSSTTTOOORRRMMMSSS...'
        print 
        
        iV=InvHashTD(dbname=dbname,tbdir=tbdirInv)
        iV.hash[self.model,self.dtg]=inv
        iV.put()
        iV.close()

        return(status,todoStmids)



    def thinOutputByTaus(self,doall=0,ropt=''):

        tdir="%s/%s/%s"%(self.tbdir,self.dtg,self.model)

        datpaths=glob.glob("%s/*dat"%(tdir))

        taus=[]
        dpaths={}
        for dat in datpaths:
            tau=dat.split('.')[-2][1:]
            tau=int(tau)
            taus.append(tau)
            dpaths[tau]=dat


        thinTaus=range(6,126+1,12)+range(126,168+1,6)

        if(doall): thinTaus=taus

        nkill=0
        for thintau in thinTaus:
            if(thintau in taus):
                dpath=dpaths[thintau]
                cmd="rm %s"%(dpath)
                mf.runcmd(cmd,ropt)
                nkill=nkill+1


        print 'III(TcDiag.thinOutputByTaus) nkill: ',nkill
        return(nkill)



    def replaceAidcards(self,param,aidname=None):


        print 'current: ',self.aid

        def replace2card(list,val,ikey):
            card=''

            for n in range(0,len(list)):
                ll=list[n]
                if(n == ikey): ll=val
                card=card+ll+','

            return(card)

        for ocard in self.aidcards:
            print 'ooo ',ocard[:-1]
            tt=ocard.split(',')
            if(aidname != None):
                ikey=4
                val=aidname.upper()
                val=val.strip()
                val=' '+val

            ncard=replace2card(tt,val,ikey)
            print 'nnn ',ncard[:-1]

    def getTcdiagStatus(self):
        
        ddir=self.diagfileOutdirLocal
        nstmids=len(self.stmids)
        diagfiles=glob.glob("%s/*%s*"%(ddir,self.model))
        ndiagfiles=len(diagfiles)
        statTcdiag=0
        if(ndiagfiles == nstmids):
            statTcdiag=1
            
        return(statTcdiag)

    def getDiagStatus(self,override=0):

        tGprev=self.gettGpyp()

        dotaus=self.taus
        self.tausDone=[]
        self.taus2Do=[]
        self.tausFinal=dotaus

        if(tGprev != None):

            tausDone=tGprev.taus
            taus2Do=self.taus
            dotaus=[]
            for taud in tausDone:
                gottau=0
                for tau2 in taus2Do:
                    if(tau2 == taud): gottau=1
                if(not(gottau)):  dotaus.append(tau2)

            if(override): dotaus=taus2Do

            self.tausDone=tausDone
            self.taus2Do=taus2Do
            self.tausFinal=dotaus

        # -- decorate so we could use...
        #
        if(tGprev != None):
            tGprev.ga=self.ga
            tGprev.ge=self.ge
            tGprev.tD=self.tD
            tGprev.aD=self.aD
            tGprev.m2=self.m2
            if(hasattr(self,'pT')): tGprev.pT=self.pT

        self.tGprev=tGprev


    def getDataStatus(self,override=0):

        tGdprev=self.gettGdpyp()


        dotaus=self.taus
        self.tausDone=[]
        self.taus2Do=[]
        self.tausFinal=dotaus

        if(tGdprev != None):

            tausDone=tGdprev.taus
            taus2Do=self.taus
            dotaus=[]
            for taud in tausDone:
                gottau=0
                for tau2 in taus2Do:
                    if(tau2 == taud): gottau=1
                if(not(gottau)):  dotaus.append(tau2)

            if(override): dotaus=taus2Do

            self.tausDone=tausDone
            self.taus2Do=taus2Do
            self.tausFinal=dotaus


        self.tGdprev=tGdprev



    def getAidtrk(self,dtg,stmid):

        aT=self.aD.GetAidTrks(self.aid,stm1id=stmid)
        if(self.aDS != None):
            aS=self.aDS.GetAidStruct(self.aid,stm1id=stmid)
        else:
            aS=None

        try:
            self.aidtrk=aT.atrks[dtg]
            self.aidtaus=self.aidtrk.keys()
            self.aidtaus.sort()

        except:
            if(self.verb): print 'WWW(%s) no adeck trackers for aid: %s stmid: %s'%(self.basename,self.model,stmid)

            self.aidtrk=None
            self.aidtaus=None


        try:
            self.aidstruct=aS.atrks[dtg]
            self.aidstructtaus=self.aidstruct.keys()
            self.aidstructtaus.sort()

        except:
            if(self.verb): print 'WWW(%s) no adeck struct for aid: %s stmid: %s'%(self.basename,self.model,stmid)

            self.aidstruct=None
            self.aidstructtaus=None


        if(self.verb and self.aidtrk != None):

            print 'TMaidtrk:  '
            for tau in self.aidtaus:
                tt=list(self.aidtrk[tau])
                print "%03d  %5.1f  %6.1f  %4.1f  %6.1f"%(int(tau),tt[0],tt[1],tt[2],tt[3])


        if(self.verb and self.aidstruct != None):

            print 'TMaidstruct:  '
            for tau in self.aidstructtaus:
                tt=list(self.aidstruct[tau])
                (alat,alon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTl,cpsVTu,z8mean,z8max,z7mean,z7max)=tt
                print "%03d  %5.1f  %6.1f  %4.1f  %6.1f cpsB: %6.1f cpsVTl: %6.1f cpsVTu: %6.1f"%(int(tau),alat,alon,vmax,pmin,cpsB,cpsVTl,cpsVTu)



    def getAidtrkFromAdss(self,dtg,stmid,
                          sources=None,adeckaid=None,
                          set2AD=1,forceAD=0):
        """
        get aid track for adeck DSs; handles multiply sources
        """

        if(sources == None):
            sources=self.adecksource.split(',')
        if(adeckaid == None):
            self.ADaid=self.adeckaid
        else:
            self.ADaid=adeckaid

        self.adecksources=sources

        aDSs=getAdssFromDss(sources,stmid,self.ADaid,verb=self.verb)
        kk=aDSs.keys()

        aTs={}
        for k in kk:
            aD=aDSs[k]

            try:
                aTs[k]=aD.ats[dtg]
            except:
                aTs[k]={}


        # -- get track with most taus from multiply sources
        #
        longest=-999
        longestK=None

        for k in kk:
            sizK=len(aTs[k])
            if( sizK > longest):
                longest=sizK
                longestK=k

        if(longest > 0):
            self.ADaidtrk=aTs[longestK]
            self.ADaidtaus=self.ADaidtrk.keys()
            self.ADaidtaus.sort()
        else:
            self.ADaidtrk=None
            self.ADaidtaus=None


        if(self.verb and self.ADaidtaus != None):
            if(len(self.ADaidtaus) > 0):
                print 'ADaidtrk:  '
                for tau in self.ADaidtaus:
                    tt=list(self.ADaidtrk[tau])
                    print "%03d  %5.1f  %6.1f  %4.1f  %6.1f"%(int(tau),tt[0],tt[1],tt[2],tt[3])



    def getAidcards(self,dtg,stmid,verb=0):

        acds=self.aD.GetAidCards(self.aid,stmid)

        rc=1
        try:
            self.aidcards=acds[dtg]
        except:
            rc=0
            self.aidcards=[]
            if(verb): print 'WWW(%s.getAidcards) no adeck cards                          aid:  %s  stmid:  %s  NNNNNNN'%(self.basename,self.model,stmid)
            return(rc)
        
        return(rc)



    def setLatLonTimeByTau(self,dtg,model,stmid,tau,dfile=1):

        try:
            rc=self.aidtrk[tau]
            (latc,lonc,vmaxc,pminc)=rc[0:4]
        except:
            return(0)

        if(abs(latc) >= self.maxLatitude):
            print 'ETETET -- too far poleward, bail...stop doing diag'
            return(-1)


        ga=self.ga
        ge=self.ge

        dir=self.aidMotion[tau][0]
        spd=self.aidMotion[tau][1]

        # -- bug in setting the endpoint, bandaid for now...
        #
        if(spd < 0.0):
            spd=9999.
            dir=9999.

        #-- add adeck vmax and pmin to custom data
        #

        if(vmaxc < 0.0 or abs(vmaxc) > 1000.0): vmaxc=9999.
        if(pminc < 0.0 or abs(pminc) > 1050.0): pminc=9999.

        print 'TTTT model: ',model,' dtg: ',dtg,' stmid: ',stmid,' tau: ',tau,\
              ' latc: ',latc,' lonc: ',lonc,' vmaxc: ',vmaxc,' pminc: ',pminc,\
              ' dir: ',dir,' spd: ',spd

        # -- set the tc lat/lon/... for this tau
        #
        self.latc=latc
        self.lonc=lonc
        self.vmaxc=vmaxc
        self.pminc=pminc

        self.stmid=stmid
        self.tau=tau

        self.vdtg=mf.dtginc(dtg,tau)
        self.vgtime=mf.dtg2gtime(self.vdtg)

        ga('set dfile %d'%(dfile))

        dlat=self.dlat
        dlon=self.dlon

        if(abs(latc) >= self.latitudeET):
            dlat=self.dlat*self.dlatETFact
            dlon=dlat*self.aspectRatio

        ge.lat1=latc-dlat
        ge.lat2=latc+dlat
        ge.lon1=lonc-dlon
        ge.lon2=lonc+dlon

        # -- set the lat/lon/lev/time dims
        ge.lev1=ge.Levs[0]
        ge.setLevs()
        ge.setLatLon()
        ge.setTimebyDtgTau(dtg,tau,verb=1)

        self.pT=ga.gp.title
        self.pT.set(scale=0.70)

        return(1)


    def setLatLonTimeByTauORIG(self,dtg,model,stmid,tau,dfile=1):


        try:
            (latc,lonc,vmaxc,pminc)=self.aidtrk[tau]
        except:
            return(0)

        print 'TTTT model: ',model,' dtg: ',dtg,' stmid: ',stmid,' tau: ',tau,' latc: ',latc,' lonc: ',lonc,' vmaxc: ',vmaxc,' pminc: ',pminc

        if(abs(latc) >= self.maxLatitude):
            print 'ETETET -- too far poleward, bail...stop doing diag'
            return(-1)


        self.stmTaus.append(tau)
        ga=self.ga
        ge=self.ge

        self.stmData[tau]={}
        self.urlData[tau]={}
        self.customData[tau]={}

        self.diagVals[tau]={}
        self.diagTypes[tau]={}
        self.diaguRls[tau]={}

        self.stmData[tau]['10 sst       (10c)']="%5.0f"%(9999)
        self.stmData[tau]['11 ohc    (kj/cm2)']="%5.0f"%(9999)
        self.stmData[tau]['13 land       (km)']="%5.0f"%(9999)

        self.sndData[tau]={}


        # -- get track for spd/dir calc
        taup0=tau
        (latcp0,loncp0,vmaxcp0,pmincp0)=self.aidtrk[taup0]

        # -- get the motion based on the next tau
        #
        ntaus=len(self.aidtaus)
        np=self.aidtaus.index(tau)

        # -- check if at end of tau...
        #
        if(np == ntaus-1):
            np=np-1
            taup0=self.aidtaus[np]
            (latcp0,loncp0,vmaxcp0,pmincp0)=self.aidtrk[taup0]

        # -- get track at next tau
        #
        np1=np+1
        taup1=self.aidtaus[np1]
        (latcp1,loncp1,vmaxcp1,pmincp1)=self.aidtrk[taup1]

        dt=taup1-taup0
        if(dt == 0):
            dir=9999.
            spd=9999.
        else:
            (dir,spd,umot,vmot)=rumhdsp(latcp0,loncp0,latcp1,loncp1,taup1-taup0)
            if(dir == 360.0): dir=0.0

        # -- bug in setting the endpoint, bandaid for now...
        #
        if(spd < 0.0):
            spd=9999.
            dir=9999.

        self.stmData[tau]['00 time       (hr)']="%5d"%(tau)
        self.stmData[tau]['01 latitude  (deg)']="%5.1f"%(latc)
        self.stmData[tau]['02 longitude (deg)']="%5.1f"%(lonc)
        self.stmData[tau]['08 stm spd    (kt)']="%5.0f"%(spd)
        self.stmData[tau]['09 stm hdg   (deg)']="%5.0f"%(dir)

        #-- add adeck vmax and pmin to custom data
        #

        if(vmaxc < 0.0 or abs(vmaxc) > 1000.0): vmaxc=9999.
        if(pminc < 0.0 or abs(pminc) > 1050.0): pminc=9999.

        ckeyv='''06 adeck vmax (kt)'''
        self.customData[tau][ckeyv]="%5.0f"%(vmaxc)

        ckeyp='''08 adeck pmin (mb)'''
        self.customData[tau][ckeyp]="%5.0f"%(pminc)

        # -- set the tc lat/lon/... for this tau
        #
        self.latc=latc
        self.lonc=lonc
        self.vmaxc=vmaxc
        self.pminc=pminc

        self.stmid=stmid
        self.tau=tau

        self.vdtg=mf.dtginc(dtg,tau)
        self.vgtime=mf.dtg2gtime(self.vdtg)

        ga('set dfile %d'%(dfile))

        dlat=self.dlat
        dlon=self.dlon

        if(abs(latc) >= self.latitudeET):
            dlat=self.dlat*self.dlatETFact
            dlon=dlat*self.aspectRatio

        ge.lat1=latc-dlat
        ge.lat2=latc+dlat
        ge.lon1=lonc-dlon
        ge.lon2=lonc+dlon

        # -- set the lat/lon/lev/time dims
        ge.lev1=ge.Levs[0]
        ge.setLevs()
        ge.setLatLon()
        ge.setTimebyDtgTau(dtg,tau,verb=1)

        self.pT=ga.gp.title
        self.pT.set(scale=0.80)




    def setInitialGA(self,xlint=10,ylint=5,dobasemap=1,bmoverride=0):

        if(not(hasattr(self,'ga'))): self.initGA(self.gaopt)

        self.ga('c')
        self.ga('set grads off')
        self.ga('set timelab on')
        self.ga('set mpdset mres')
        self.ga('set map 1 0 8')
        self.ga('set xlint %d'%(xlint))
        self.ga('set ylint %d'%(ylint))

        # -- set parea for diag plots
        #
        self.ge.pareaxl= 0.50
        self.ge.pareaxr=10.00
        self.ge.pareayb= 0.75
        self.ge.pareayt= 8.00

        self.ge.setLatLon()
        self.ge.setParea()
        self.ge.setPlotScale()
        self.ge.pngmethod=self.printMethod

        if(dobasemap):

            bmname="%s.%s.%s.f%03d"%(self.model,self.stmid,self.dtg,self.tau)

            bm=self.ga.gp.basemap2
            bm.set(landcol='sienna',oceancol='navy',
                   bmdir=self.pltdir,
                   xsize=self.xsize,
                   ysize=self.ysize,
                   bmname=bmname)

            if(not(MF.ChkPath(bm.pngpath,verb=1)) or bmoverride):
                bm.draw()
                bm.putPng()

            self.bm=bm

        # -- arrow length
        #
        # -- scale shear arrow by 10 kt
        #
        try:
            self.stmvmax=self.stmData[self.tau,3]
            self.stmspd=self.stmData[self.tau,8]
            self.stmdir=self.stmData[self.tau,9]
        except:
            print 'EEE(TcDiag.setInitialGA): bad self.stmData at tau: ',self.tau,' set to 180 at 0 kt'
            self.stmdir=180
            self.stmspd=0
            self.stmvmax=999

        if(self.stmdir == 999):
            print 'WWW undefined stm motion TcDidag.setInitialGA() at tau:',self.tau,' stmid: ',self.stmid,' maybe because only tau0...'
            self.stmdir=180
            self.stmspd=0
            self.stmvmax=999

        self.arrlen=0.5*(self.stmspd/10.0)
        self.arrdir=self.stmdir

        if(self.stmid in self.btcs.keys()):
            self.tau0stmvmax=self.btcs[self.stmid][2]
            self.tau0stmdir=self.btcs[self.stmid][4]
            self.tau0stmspd=self.btcs[self.stmid][5]
            self.tau0stmspdArr=0.5*(self.btcs[self.stmid][5]/10.0)
        else:
            if(self.verb): print 'WWW TCDiag.setInitialGA() no stmid: ',self.stmid,' in self.btcs.keys()'
            self.tau0stmvmax=999
            self.tau0stmdir=270.0
            self.tau0stmspd=10.0
            self.tau0stmspdArr=0.5*(self.tau0stmspd/10.0)


        self.t2b=" latc: %4.1f lonc: %4.1f"%(self.latc,self.lonc)

        obsrc='CRQ'
        if(self.dobt > 0): obsrc='BT'
        if(self.tau == 0):
            self.t2c=" %s(G)/modVmax(W): %3.0f/%-3.0fkt %s/modSpd: %2.0f/%-2.0fkt %s/modDir: %3.0f`3.`0/%-3.0f`3.`0 (W)"%(obsrc,self.tau0stmvmax,self.stmvmax,
                                                                                                                      obsrc,self.tau0stmspd,self.stmspd,
                                                                                                                      obsrc,self.tau0stmdir,self.stmdir)
        else:
            self.t2c=" modVmax: %3.0fkt  modSpd: %2.0fkt  modDir: %3.0f`3.`0 (W)"%(self.stmvmax,
                                                                               self.stmspd,
                                                                               self.stmdir)
        # -- plot the tracker source
        #
        otrksource=self.trkSource
        if(hasattr(self,'FtrkSource')):    otrksource=self.FtrkSource[self.stmid]
        self.t2c="%s trk: %s"%(self.t2c,otrksource)

        self.obsmotionLCOL=3
        self.obsmotionBO=1
        self.obsmotionTHK=10

    def getW2xy(self,lat,lon):

        self.ga("q w2xy %f %f"%(lon,lat))

        xp=self.ga.rword(1,3)
        yp=self.ga.rword(1,6)

        return(xp,yp)


    def printPlot(self,pltpath,verb=0):

        if(verb): print 'PPPP pltpath: ',pltpath
        self.ge.pngmthod=self.printMethod

        if(self.printMethod == 'printim'):
            #self.ge.makePng(pltpath,bmpath=None)
            if(MF.ChkPath(self.bm.pngpath)):
                self.ge.makePng(pltpath,bmpath=self.bm.pngpath,xsize=self.xsize,ysize=self.ysize)
        else:
            cmd="%s %s %s"%(self.printMethod,self.printOpt,pltpath)
            self.ga(cmd)


    def doMfhilo(self,fld,hltype,pltpath,dohlplot=1,dohl=1):


        if(dohl == 0):
            lathl=999.
            lonhl=999.
            maxhl=9999.
            return(lathl,lonhl,maxhl)

        doundef=0
        wpgothl=0

        try:
            self.ga._cmd("mfhilo %s gr %s d 100 %f %f %f"%(fld,hltype,self.latc,self.lonc,self.mfhiloRad))
            gothl=1

        except:
            print 'WWWW:        ',self.ga.Lines
            print "EEEE(mfhilo): problem with plotting H/L for: %s hltype: %s pltpath: %s"%(fld,hltype,pltpath)
            doundef=1
            gothl=0

        # -- check return code; if not 0
        #
        if(int(self.ga.rc) > 0): gothl=0; doundef=1

        if(gothl):
            npoints=int(self.ga.rword(1,5))
            if(npoints > 0):
                lathl=float(self.ga.rword(2,2))
                lonhl=float(self.ga.rword(2,3))
                maxhl=float(self.ga.rword(2,5))
                if(self.verb): print 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn ',npoints,maxhl
                if(dohlplot): self.drawMark(lathl,lonhl,"%02.0f"%(maxhl))
            else:
                doundef=1


        if(doundef):
            lathl=999.
            lonhl=999.
            maxhl=9999.

        return(lathl,lonhl,maxhl)



    def getVmaxRmax4Tcxy2rt(self,RmaxDrMinfact=1.5,verb=0,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        latc=self.latc
        lonc=self.lonc

        fld='w'
        pinc=5

        ga("%s=mag(uas,vas)*%f"%(fld,ms2knots))

        if(not(self.doDiagPlotsOnly)):
            # -- check if we have any data ... if not then set to undef and bail
            #
            exprstats=ga.getExprStats(fld)
            nvalid=exprstats.nvalid
            if(nvalid == 0):
                print 'WWWWWWWWWWW nvalid = 0 in getVmaxRmax4Tcxy2rt'
                finalVmax=9999.
                finalRmax=9999.
                ckey1='03 max wind   (kt)'
                ckey2='04 rmw        (km)'
                self.stmData[self.tau][ckey1]="%5.0f"%(finalVmax)
                self.stmData[self.tau][ckey2]="%5.0f"%(finalRmax)
                ckeyv='''07 diag vmax  (kt)'''
                self.customData[self.tau][ckeyv]="%5.0f"%(finalVmax)
                return

            self.setInitialGA()
            self.plotFldContour(fld,pinc)
            # -- convert from x,y -> r,theta and parse result
            #
            ga("tcxy2rt %s %f %f %f %f %f"%(fld,latc,lonc,self.drnm,self.dtheta,self.rmaxnm))

            nlines=ga.nLines

            R=[]
            T=[]
            V={}
            Lat={}
            Lon={}
            Vmax={}
            Rmax={}
            Latmax={}
            Lonmax={}

            nr=ga.rword(2,2)
            nt=ga.rword(2,4)

            for n in range(4,nlines+1):
                #17    0   255    0    31.19  287.80       100974.12

                i=ga.rword(n,1)
                j=ga.rword(n,2)
                r=float(ga.rword(n,3))
                t=float(ga.rword(n,4))
                lat=float(ga.rword(n,5))
                lon=float(ga.rword(n,6))
                val=float(ga.rword(n,7))

                V[r,t]=val
                Lat[r,t]=lat
                Lon[r,t]=lon

                R.append(r)
                T.append(t)


            R=MF.uniq(R)
            T=MF.uniq(T)

            finalVmax=-999
            finalRmax=0.0
            nRmax=0

            nR=len(R)
            for t in T:

                Vm=-1e20

                for j in range(0,nR):

                    r0=R[j]
                    v0=V[r0,t]

                    if(j==nR-1):
                        rp1=r0
                        vp1=V[r0,t]
                    else:
                        rp1=R[j+1]
                        vp1=V[rp1,t]

                    if(v0>Vm):
                        Vm=v0
                        Vmax[t]=v0
                        Rmax[t]=r0
                        Latmax[t]=Lat[r0,t]
                        Lonmax[t]=Lon[r0,t]

                    #print 't ',t,r0,v0

                if(Vmax[t] > finalVmax):  finalVmax=Vmax[t]

                # -- require rmax > Rmax min for cases
                if(Rmax[t] > self.drnm*RmaxDrMinfact):
                    finalRmax=finalRmax+Rmax[t]
                    nRmax=nRmax+1

                if(verb): print 'FFFF ',t,Vmax[t],Rmax[t],Latmax[t],Lonmax[t],v0,r0,Lat[r0,t],Lon[r0,t]


            if(nRmax > 0):
                if(verb): print 'FFFF ',nRmax,finalRmax/nRmax
                finalRmax=(finalRmax/nRmax)*nm2km


            if(verb): print 'Final Vmax: ',finalVmax,' finalRmax: ',finalRmax

        else:

            finalVmax=9999.
            finalRmax=9999.

        ckey1='03 max wind   (kt)'
        ckey2='04 rmw        (km)'
        self.stmData[self.tau][ckey1]="%5.0f"%(finalVmax)
        self.stmData[self.tau][ckey2]="%5.0f"%(finalRmax)

        ckeyv='''07 diag vmax  (kt)'''
        self.customData[self.tau][ckeyv]="%5.0f"%(finalVmax)


        pvar='vmax'
        pltpath=self.setPlotuRl(pvar,ckey1)
        pltpath=self.setPlotuRl(pvar,ckey2)

        if(self.doplot):

            self.plotFldContour(fld,pinc)
            # -- draw the search radius (nm)
            #
            self.drawRadinf(self.rmaxnm)

            if(not(self.doDiagPlotsOnly)):

                # -- draw the max points
                #
                for t in T:
                    (xp,yp)=self.getW2xy(Latmax[t],Lonmax[t])
                    ga('set line 2')
                    ga("draw mark 3 %s %s 0.20"%(xp,yp))
                    ga('set strsiz 0.09')
                    ga('set string 0 c 5')
                    ga("draw string  %s %s %2.0f"%(xp,yp,Vmax[t]))


                self.doMfhilo(fld,'l',pltpath,dohl=dohl)

            self.drawHurr()

            t1="TCdiag(%s) MAX WIND: %3.0f RMAX: %4.0f  for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,finalVmax,finalRmax,self.stmid,self.dtg,self.tau,self.rmax)
            t2="sfc wind speed [kt]  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)


    def getPrw(self,domodelprw=0,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        fld='tpw'
        fldG="grd%s"%(fld)

        pvar='prw'
        ckey='12 tpw        (mm)'

        # ----------------------------------------------------------
        # for models without prw output -- use grads vint function
        # not sure if ta is tv (probably not) need to calc q separately?
        # error of ~ 1-3 mm over ocean, bad over big terrain
        #
        #prwexpr1="vint(psl*0.01,tvrh2q(ta,hur),100)"
        # -- more correct based on the classic formula
        #
        rhfact='0.01'
        if(self.model == 'ngp2'): rhfact='1.0'
        vaporP='(esmrf(ta)*hur*%s)'%(rhfact)

        # -- ngp2 blow up for /w21/dat/nwp2/w2flds/dat/ngp2/2010060112/ngp2.w2flds.2010060112.ctl because
        #  ta undef

        vaporP='(esmrf(const(ta,273.16,-u))*hur*%s)'%(rhfact)
        mixingR="0.622*(%s/(lev-%s))"%(vaporP,vaporP)
        prwexpr="vint(psl*0.01,%s,100)"%(mixingR)

        if(self.model == 'gfs2' and domodelprw): prwexpr='prw'

        if(not(self.doDiagPlotsOnly)):

            ga("%s=%s"%(fldG,prwexpr))
            ga("%s=re(%s,%s)"%(fld,fldG,self.reRes))
            ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,self.rmaxnm))
            meantpw=float(ga.rword(5,2))

        else:
            ga("%s=%s"%(fld,prwexpr))
            dohl=0
            meantpw=9999.

        self.stmData[self.tau][ckey]="%5.0f"%(meantpw)

        pltpath= self.setPlotuRl(pvar,ckey)

        if(self.doplot):
            ga('d %s'%(fld))

            if(dohl): self.doMfhilo(fldG,'h',pltpath,dohl=dohl)
            self.drawHurr()
            self.drawRadinf(self.rmaxnm)

            t1="TCdiag(%s) TPW: %2.0f for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,meantpw,self.stmid,self.dtg,self.tau,self.rmax)
            t2="prw [mm H20]  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)



    def getSst(self,minsstC=0.0,maxsstC=35.0,useall=0,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        fld='sst2'
        fldG="grd%s"%(fld)

        if(not(self.doDiagPlotsOnly)):

            # -- option to use sst anl with values everywhere (from weaving)
            if(useall):
                ga("%s=sstall"%(fldG))
                ga("%s=re(sstall,%s)"%(fld,self.reRes))

            else:
                ga("%s=sst"%(fldG))
                ga("%s=re(sst,%s)"%(fld,self.reRes))

            ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,self.radinfSstnm))
            meansst=float(ga.rword(5,2))
            maxradsst=float(ga.rword(7,2))
            minradsst=float(ga.rword(8,2))

        else:
            dohl=0
            if(useall):
                ga("%s=sstall"%(fld))
            else:
                ga("%s=sst"%(fld))

            meansst=maxradsst=minradsst=9999.


        flda='sst2a'
        fldaG="grd%s"%(flda)
        if(not(self.doDiagPlotsOnly)):

            ga("%s=ssta"%(fldaG))
            ga("%s=re(ssta,%s)"%(flda,self.reRes))
            ga("tcprop %s %f %f %f"%(flda,self.latc,self.lonc,self.radinfSstnm))
            meanssta=float(ga.rword(5,2))

        else:
            ga("%s=ssta"%(flda))
            meanssta=9999.


        if(self.verb):
            print 'mmmmmmmmmmmmmmm   meansst: ',meansst
            print 'mmmmmmmmmmmmmmm maxradsst: ',maxradsst
            print 'mmmmmmmmmmmmmmm minradsst: ',minradsst
            print 'mmmmmmmmmmmmmmm  meanssta: ',meanssta

        ckey='10 sst       (10c)'
        ckeya='00 sstanom   (10c)'
        # -- check for bad sst -- from ~ coasts and improper
        #
        if(minradsst < minsstC or maxradsst > maxsstC):
            meansst=9999.
            self.stmData[self.tau][ckey]="%5.0f"%(meansst)
        else:
            self.stmData[self.tau][ckey]="%5.0f"%(meansst*10.0)

        if(meanssta < minsstC or meanssta > maxsstC):
            meanssta=9999.
            self.customData[self.tau][ckeya]="%5.0f"%(meanssta)
        else:
            self.customData[self.tau][ckeya]="%5.0f"%(meanssta*10.0)

        pvar='sst'
        pltpath=self.setPlotuRl(pvar,ckey)
        pvara='ssta'
        pltpatha=self.setPlotuRl(pvara,ckeya)

        if(self.doplot):

            self.plotFldGrfill(fld,cint=1)

            if(dohl): self.doMfhilo(fldG,'h',pltpath,dohl=dohl)
            self.drawHurr()
            self.drawRadinf(self.radinfSstnm)

            t1="TCdiag(%s) SST: %3.1f for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,meansst,self.stmid,self.dtg,self.tau,self.rmax)
            t2="sst [C]  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)


            # -- plot the sst anom
            #
            self.setInitialGA()
            self.plotFldShaded(flda,cint=0.5,black1=-0.5,black2=0.5,drawcontour=1)

            if(dohl): self.doMfhilo(fldaG,'h',pltpath)
            self.drawHurr()
            self.drawRadinf(self.radinfSstnm)

            t1="TCdiag(%s) SSTA: %2.0f for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,meanssta,self.stmid,self.dtg,self.tau,self.rmax)
            t2="slp [mb]  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpatha)



    def getPmin(self):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        fld='slp'
        fldG="grd%s"%(fld)

        ga("%s=psl*0.01"%(fld))

        pvar='pmin'
        ckey='05 min slp    (mb)'

        pltpath=self.setPlotuRl(pvar,ckey)

        dopmin=1
        if(not(self.doDiagPlotsOnly)):
            (latpmin,lonpmin,pmin)=self.doMfhilo(fld,'l',pltpath,dohlplot=0)
        else:
            dopmin=0
            pmin=9999.

        self.stmData[self.tau][ckey]="%5.0f"%(pmin)

        ckeyp='''09 diag pmin  (mb)'''
        self.customData[self.tau][ckeyp]="%5.0f"%(pmin)

        if(self.doplot):

            pinc=2
            if(pmin < 980): pinc=4
            self.plotFldContour(fld,pinc)

            if(dopmin): self.drawMark(latpmin,lonpmin,"%02.0f"%(pmin-1000.0))

            self.drawHurr()
            self.drawRadinf(self.mfhiloRad)

            t1="TCdiag(%s) MINSLP: %4.0f for: %s  dtg: %s  tau: %d"%(self.umodel,pmin,self.stmid,self.dtg,self.tau)
            t2="slp [mb]  latc: %4.1f  lonc: %4.1f search radius: %5.0f [km]"%(self.latc,self.lonc,self.mfhiloRad*nm2km)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)



    def getShear(self,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=500
        radinfnm=radinf*km2nm

        fld='magshr'
        fldG="grd%s"%(fld)
        pvar='magshr'
        ufld='ushr'
        ufldG="grd%s"%(ufld)
        vfld='vshr'
        vfldG="grd%s"%(vfld)

        ckeyc='01 tot shrmag (kt)'
        ckey1='06 shr mag    (kt)'
        ckey2='07 shr dir   (deg)'
        ckeyr='02 mag2tot  shr(%)'

        if(not(self.doDiagPlotsOnly)):

            ga("%s=mag((ua(lev=200)-ua(lev=850)),(va(lev=200)-va(lev=850)))*%f"%(fldG,ms2knots))
            ga("%s=re(%s,%s)"%(fld,fldG,self.reRes))
            ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,radinfnm))
            meantotshear=float(ga.rword(5,2))
            self.customData[self.tau][ckeyc]="%5.0f"%(meantotshear)

            ufld='ushr'
            ufldG="grd%s"%(ufld)
            ga("%s=(ua(lev=200)-ua(lev=850))*%f"%(ufldG,ms2knots))
            ga("%s=re(%s,%s)"%(ufld,ufldG,self.reRes))
            ga("tcprop %s %f %f %f"%(ufld,self.latc,self.lonc,radinfnm))
            meanu=float(ga.rword(5,2))

            vfld='vshr'
            vfldG="grd%s"%(vfld)
            ga("%s=(va(lev=200)-va(lev=850))*%f"%(vfldG,ms2knots))
            ga("%s=re(%s,%s)"%(vfld,vfldG,self.reRes))
            ga("tcprop %s %f %f %f"%(vfld,self.latc,self.lonc,radinfnm))
            meanv=float(ga.rword(5,2))

            shrmag=sqrt( meanu*meanu + meanv*meanv )
            shrdir=270.0-atan2(meanv,meanu)*rad2deg 

            if(shrdir < 0.0): shrdir=shrdir+360.0
            if(shrdir > 360.0): shrdir=shrdir-360.0

            mag2tot=(shrmag/meantotshear)*100.0

            # -- set stmdata, etc if grads calcs the diags
            #
            self.stmData[self.tau][ckey1]="%5.0f"%(shrmag)
            self.stmData[self.tau][ckey2]="%5.0f"%(shrdir)

            self.customData[self.tau][ckeyr]="%5.0f"%(mag2tot)

        else:

            ga("%s=mag((ua(lev=200)-ua(lev=850)),(va(lev=200)-va(lev=850)))*%f"%(fld,ms2knots))
            ga("%s=(ua(lev=200)-ua(lev=850))*%f"%(ufld,ms2knots))
            ga("%s=(va(lev=200)-va(lev=850))*%f"%(vfld,ms2knots))

            dohl=0
            dlat=0; dlon=0
            if(hasattr(self.ge,'dlat')): dlat=self.ge.dlat
            if(hasattr(self.ge,'dlon')): dlat=self.ge.dlon


            if(dlat > 0.): self.barbskip=dlat/2

            shrmag=999.
            shrdir=999.
            meantoshear=999.
            meanu=999.
            meanv=999.
            mag2tot=999.


        pltpath=self.setPlotuRl(pvar,ckey1)
        pltpath=self.setPlotuRl(pvar,ckey2)
        pltpath=self.setPlotuRl(pvar,ckeyc)
        pltpath=self.setPlotuRl(pvar,ckeyr)


        if(self.doplot):

            shrmag=self.stmData[self.tau,6]
            shrdir=self.stmData[self.tau,7]

            #for i in range(0,self.nstmvars):
            #    print 'vvv ',i+1,
            #    print 'ccc ',i+1,self.cstmData[self.tau,i+1]
            #    print 'lll ',i+1,self.stmLabels[i+1]


            self.plotFldContour(fld)
            self.plotWindBarbs(ufld,vfld)

            if(dohl): self.doMfhilo(fldG,'l',pltpath,dohl=dohl)
            self.drawHurr()
            self.drawRadinf(radinfnm)
            self.drawArrow(self.latc,self.lonc,dir=shrdir,lcol=1,lthk=20)

            t1="TCdiag(%s) SHRMAG: %3.0f SHRDIR: %3.0f for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,shrmag,shrdir,self.stmid,self.dtg,self.tau,radinf)
            t2="shear [kt] latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)





    def getPrecip(self,dohl=0):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=500
        radinfnm=radinf*km2nm

        fld='totpr'
        fldG="grd%s"%(fld)

        fldc='cnvpr'
        fldcG="grd%s"%(fldc)

        prvar=self.setprvar(self.dtg,self.tau)
        prvar=prvar.split('=')[1]
        prvar=prvar.replace("\'",'')
        prvarc=prvar.replace('pr','prc')

        ckey='03 tot pr (10mm/d)'
        ckeyc='04 cnv pr (10mm/d)'

        if(not(self.doDiagPlotsOnly)):
            try:
                ga("%s=%s"%(fldG,prvar))
                ga("%s=re(%s,%s)"%(fld,fldG,self.reRes))
                ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,radinfnm))
                meanpr=float(ga.rword(5,2))
            except:
                meanprc=9999.

            try:
                ga("%s=%s"%(fldcG,prvarc))
                ga("%s=re(%s,%s)"%(fldc,fldcG,self.reRes))
                ga("tcprop %s %f %f %f"%(fldc,self.latc,self.lonc,radinfnm))
                meanprc=float(ga.rword(5,2))
            except:
                meanprc=9999.


            if(abs(meanpr) > 9999.): meanpr=999.
            if(abs(meanprc) > 9999.): meanprc=999.

            self.customData[self.tau][ckey]="%5.0f"%(meanpr*10.0)
            self.customData[self.tau][ckeyc]="%5.0f"%(meanprc*10.0)


        else:

            ga("%s=%s"%(fld,prvar))
            ga("%s=%s"%(fldc,prvarc))
            meanpr=999.
            meanprc=999.


        if(self.doplot and meanpr != 9999.):

            pvar='totpr'
            pltpath=self.setPlotuRl(pvar,ckey)
            self.plotFldContour(fld)

            self.doMfhilo(fldG,'h',pltpath,dohl=dohl)
            self.drawHurr()
            self.drawRadinf(radinfnm)

            t1="TCdiag(%s) TOT PR: %3.0f for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,meanpr,self.stmid,self.dtg,self.tau,radinf)
            t2="total precip 10 [mm/d] latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)
            self.printPlot(pltpath)

        if(self.doplot and meanprc != 9999.):

            self.setInitialGA()

            pvar='cnvpr'
            pltpath=self.setPlotuRl(pvar,ckeyc)
            self.plotFldContour(fldc)

            self.doMfhilo(fldG,'h',pltpath)
            self.drawHurr()
            self.drawRadinf(radinfnm)

            t1="TCdiag(%s) CNV PR: %3.0f for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,meanpr,self.stmid,self.dtg,self.tau,radinf)
            t2="convective precip 10 [mm/d] latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)
            self.printPlot(pltpath)

        if(meanprc != 9999. and meanpr != 9999.0):
            ratio=meanprc/meanpr
            ratio=ratio*100.0
        else:
            ratio=9999.

        ckeyc='''05 cnv2tot pr  (%)'''
        self.customData[self.tau][ckeyc]="%5.0f"%(ratio)



    def getVort850(self,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=1000
        radinfnm=radinf*km2nm

        fld='vt8'
        fldG="grd%s"%(fld)
        ckey='15 850vort    (/s)'
        pvar='vt850'

        if(not(self.doDiagPlotsOnly)):

            ga("%s=hcurl(ua(lev=850),va(lev=850))*1e7"%(fldG))
            ga("%s=re(%s,%s)"%(fld,fldG,self.reRes))
            ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,radinfnm))
            meanvt850=float(ga.rword(5,2))

        else:
            ga("%s=hcurl(ua(lev=850),va(lev=850))*1e7"%(fld))
            dohl=0
            meanvt850=999.

        pltpath=self.setPlotuRl(pvar,ckey)
        self.stmData[self.tau][ckey]="%5.0f"%(meanvt850)


        if(self.doplot):

            self.plotFldContour(fld)

            try:
                self.doMfhilo(fld,'h',pltpath,dohl=dohl)
            except:
                print 'WWWW:        ',self.ga.Lines
                print "EEEE(mfhilo): problem with plotting H/L for: %s hltype: %s pltpath: %s"%(fld,hltype,pltpath)

            self.drawHurr()
            self.drawRadinf(radinfnm)

            t1="TCdiag(%s) 850VORT: %4.0f for: %s  dtg: %s  tau: %d  R=0-%2.0f km"%(self.umodel,meanvt850,self.stmid,self.dtg,self.tau,radinf)
            t2="10e-7 s`a-1`n  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)



    def getDiv200(self,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=1000
        radinfnm=radinf*km2nm

        fld='div200'
        fldG="grd%s"%(fld)
        ckey='16 200dvrg    (/s)'
        pvar='div200'

        if(not(self.doDiagPlotsOnly)):
            ga("%s=hdivg(ua(lev=200),va(lev=200))*1e7"%(fldG))
            ga("%s=re(%s,%s)"%(fld,fldG,self.reRes))
            ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,radinfnm))
            meandiv200=float(ga.rword(5,2))
        else:
            ga("%s=hdivg(ua(lev=200),va(lev=200))*1e7"%(fld))
            meandiv200=999.

        self.stmData[self.tau][ckey]="%5.0f"%(meandiv200)
        pltpath=self.setPlotuRl(pvar,ckey)

        if(self.doplot):

            self.plotFldContour(fld)

            self.doMfhilo(fldG,'h',pltpath,dohl=dohl)
            self.drawHurr()
            self.drawRadinf(radinfnm)

            t1="TCdiag(%s) 200DVRG: %4.0f for: %s  dtg: %s  tau: %d  R=0-%2.0f km"%(self.umodel,meandiv200,self.stmid,self.dtg,self.tau,radinf)
            t2="10e-7 s`a-1`n  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)

            self.pT.top(t1,t2)

            self.printPlot(pltpath)



    def getTang850(self,dore=1,dohl=1):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=600
        radinfnm=radinf*km2nm

        fld='tv8'
        fldG="grd%s"%(fld)

        pvar='tv850'
        ckey='14 850tang (10m/s)'

        if(not(self.doDiagPlotsOnly)):

            ga("%s=uv2trw(ua(lev=850),va(lev=850),%f,%f,1)*10"%(fldG,self.latc,self.lonc))
            # -- big problem with either re/mfhilo for this field, seems to be in re/re2 bringing down mfhilo...
            if(dore):   ga("%s=re(%s,%s)"%(fld,fldG,self.reRes))
            ga("tcprop %s %f %f %f"%(fld,self.latc,self.lonc,radinfnm))
            meantv850=float(ga.rword(5,2))
        else:
            ga("%s=uv2trw(ua(lev=850),va(lev=850),%f,%f,1)*10"%(fld,self.latc,self.lonc))
            dohl=0
            meantv850=999.


        self.stmData[self.tau][ckey]="%5.0f"%(meantv850)

        pltpath=self.setPlotuRl(pvar,ckey)

        if(self.doplot):

            self.plotFldGrfill(fld)

            if(dohl): self.doMfhilo(fldG,'l',pltpath,dohl=dohl)
            self.drawHurr()
            self.drawRadinf(radinfnm)

            t1="TCdiag(%s) 850TANG: %2.0f for: %s  dtg: %s  tau: %d  R=0-%2.0f km"%(self.umodel,meantv850,self.stmid,self.dtg,self.tau,radinf)
            t2="10e1 kt  latc: %4.1f  lonc: %4.1f"%(self.latc,self.lonc)
            self.pT.top(t1,t2)

            self.printPlot(pltpath)


    def setCustomData(self,tau,num,title,value):

        ckey='''%02d %s'''%(num,title[0:15])
        self.customData[tau][ckey]="%5.0f"%(value)


    def getHartCps(self):

        try:
            tt=list(self.aidstruct[self.tau])
            (alat,alon,vmax,pmin,
             alf,
             poci,roci,
             rmax,
             dir,spd,
             cpsB,cpsVTl,cpsVTu,
             z8mean,z8max,z7mean,z7max)=tt

        except:
            cpsB=cpsVTl=cpsVTu=self.undef


        if(cpsB == -99.): cpsB=self.undef
        if(cpsVTl == -9999.): cpsVTl=self.undef
        if(cpsVTu == -9999.): cpsVTu=self.undef

        self.setCustomData(self.tau,10,'CPS B(aroclinic)',cpsB)
        self.setCustomData(self.tau,11,'CPS Vtherm Lo   ',cpsVTl)
        self.setCustomData(self.tau,12,'CPS Vtherm Hi   ',cpsVTu)


    def getHemiVals(self,fld,latc,lonc,radinfnm,hemidir):
        """use mf udc tcprop to get means in hemispheres set by hemidir
        """
        hemiR=hemiL=-999.
        self.ga("tcprop %s %f %f %f %f"%(fld,latc,lonc,radinfnm,hemidir))
        for n in range(0,self.ga.nLines):
            ww=self.ga.rline(n)
            if(mf.find(ww,'MeanHemi')):
                hemiR=float(self.ga.rword(n,2))
                hemiL=float(self.ga.rword(n,4))

        return(hemiR,hemiL)


    def getCircleMean(self,fld,latc,lonc,radinfnm,undef=-999):
        """use mf udc tcprop to get means in hemispheres set by hemidir
        """
        mean=undef
        self.ga("tcprop %s %f %f %f"%(fld,latc,lonc,radinfnm))
        for n in range(0,self.ga.nLines):
            ww=self.ga.rline(n)
            if(mf.find(ww,'MeanRadinf')):
                mean=float(self.ga.rword(n,2))

                if(abs(mean) > 1e10): mean=undef

        return(mean)

    #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp -- TCdiag plotting methods
    #


    def pltBasemap(self,bmoverride=0):

        self.setInitialGA(bmoverride=bmoverride)


    def pltAllSoundings(self):

        ualevs=self.ge.Levs
        if(self.domandonly): ualevs=[850,500,200]
        levels=[self.sfcLevel]+ualevs

        if(self.doStndOnly):
            ualevs=[1000,850,700,500,400,300,250,200,150,100]
            levels=ualevs

        gotfromdiagfile=0
        if(hasattr(self,'sndPlevs')):
            gotfromdiagfile=1
            levels=self.sndPlevs


        fldssfc=['t','r','p','u','v']
        fldua=['t','r','z','u','v']

        fldlevels={
            'surf':['p','u'],
            850:['t','r','z','u'],
            700:['t','r','z','u'],
            500:['t','r','z','u'],
            200:['t','r','u'],
        }

        # -- testing
        #

        levels=fldlevels.keys()

        for level in levels:

            flds=fldlevels[level]

            for fld in flds:
                rc=self.pltSounding(fld,level)


    def pltSounding(self,ifld,level,verb=0):

        def printmean(ifld,level,meanfld):
            cmeanfld="%s"%(format)%(meanfld)
            print 'fld: %3s level: %4s  mean: %s'%(ifld,level,cmeanfld)


        def getkey(ifld,level,units,format,meanfld):

            if(level == self.sfcLevel):
                sndkey="%s_%s   %s"%(ifld,units,self.sfcLevel)
            else:
                sndkey="%s_%04d   %s"%(ifld,int(level),units)

            return(sndkey)

        def getcmean(dfld):
            # -- calc mean in annulus
            #
            meanin=self.getCircleMean(dfld,self.latc,self.lonc,self.radinfInnm)
            meanin=meanin*self.areaIn
            meanout=self.getCircleMean(dfld,self.latc,self.lonc,self.radinfOutnm)
            meanout=meanout*self.areaOut
            cmean=(meanout-meanin)/self.areaAnnulus
            return(cmean)

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        (var,fact,afact,format,cfact,units)=self.fld2var(ifld,level)

        dfld=ifld+'grd'

        if(level != self.sfcLevel):
            ga("set lev %s"%(level))
            ilevel=int(level)
        else:
            ilevel=1013

        # -- plot unscaled
        #
        ga("%s=%s*%s + %s*%s"%(ifld,var,fact,afact,fact))
        meanfld=999.

        mfact=1.0
        if(cfact != '' ): mfact=1.0/int(cfact)

        try:
            meanfld=int(self.sndDataVar[self.tau,ifld,level])*mfact
        except:
            meanfld=-999.0

        if(ifld == 'u' or ifld == 'v'):

            if(self.dlat > 0.): barbskip=self.dlat/2

            ga("%s=%s*%f*%f"%(dfld,var,fact,mfact))
            cmean=getcmean(dfld)

            dufld='u2'
            dvfld='v2'

            uvar='ua' ; vvar='va'
            if(level == self.sfcLevel): uvar='uas' ; vvar='vas'

            uexpr="%s=%s*%f*%f"%(dufld,uvar,fact,mfact)
            vexpr="%s=%s*%f*%f"%(dvfld,vvar,fact,mfact)
            ga(uexpr)
            ga(vexpr)

            if(level != self.sfcLevel and int(level) <= 850): doscale=1

            self.plotWindBarbs(  dufld,dvfld,doscale=1,barbskip=barbskip)
            self.plotWindStreams(dufld,dvfld,doscale=0,starrspc=2.0,strmden=3,ccolor=7,cthick=4)

            self.plotFldContour(dfld,cint=10,ccolor=1,clthick=6,clsize=0.07)

            t1="TCdiag(%s) Var: %s Level: %s  Mean: %-2.1f for: %s  dtg: %s  tau: %d  R=%2.0f-%2.0f km"%\
                (self.umodel,ifld.upper(),level,meanfld,self.stmid,self.dtg,self.tau,self.radinfIn,self.radinfOut)
            t2a="Wind barbs [kt] mean: %3.0f"%(cmean)
            t2=t2a+self.t2b+self.t2c

        else:

            if(ifld == 'z' or ifld == 'p'):
                ga("%s=%s*%s + %s"%(dfld,var,fact,afact))
            else:
                ga("%s=%s*%s + %s"%(dfld,var,1.0,afact))

            # -- set cint
            #
            cint=None
            if(ifld == 'p'): cint=4

            # -- get mean
            #
            cmean=getcmean(dfld)

            if(ifld == 'r'):

                gac='''set gxout shaded
set csmooth on
set rgb 71  250 250 250 0   
set rgb 72  220 220 220 0   
set rgb 75  195 195 195 0   
set rgb 74  182 182 182 0   
set rgb 76  180 180 180 0   
set rgb 77  128 128 128 0   
set rgb 78  112 112 112 0
set rgb 79  64 64 64    0'''

                ga(gac)

                illo=700
                ilhi=300
                if(ilevel >= illo):
                    gacCL='''               
set clevs   80  85  90  95  98'''

                elif(ilevel > ilhi and ilevel < illo):
                    gacCL='''               
set clevs   70  80  90  95  98'''

                elif(ilevel <= ilhi):
                    gacCL='''               
set clevs   40  50  60 65  70'''


                ga(gacCL)

                gac='''
set ccols 0  79  78  76  72 71
d r
cbarn'''
                ga(gac)

                gac='''
set gxout contour
set clopts 1 5 0.07
set clskip 2
set ccolor 1'''
                ga(gac)
                ga(gacCL)

                gac='''
d r
'''
                ga(gac)


            else:

                self.plotFldContour(dfld,cint=cint,clsize=0.07)

            t1="TCdiag(%s) Var: %s Level: %s  Mean: %-3.1f for: %s  dtg: %s  tau: %d  R=%2.0f-%2.0f km"%\
                (self.umodel,ifld.upper(),level,meanfld,self.stmid,self.dtg,self.tau,self.radinfIn,self.radinfOut)

            t2a="units: %s mean: %-3.1f"%(units,cmean)
            t2=t2a+self.t2b+self.t2c


        self.drawHurr()
        self.drawRadinf(self.radinfInnm)
        self.drawRadinf(self.radinfOutnm)

        self.drawArrow(self.latc,self.lonc,lcol=2)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)


        ckey=getkey(ifld,level,units,format,meanfld)

        if(level == self.sfcLevel):   clevel=level
        else:                         clevel="%04d"%(int(level))

        pvar="%s_%s"%(ifld,clevel)
        pltpath=self.setPlotuRl(pvar,ckey)

        if(verb): printmean(ifld,level,meanfld)

        self.pT.top(t1,t2)
        self.printPlot(pltpath)



    def pltVort850(self,dotest=0,override=0):

        self.setInitialGA()

        ckey='15 850vort    (/s)'
        pvar='850vort'

        pltpath=self.setPlotuRl(pvar,ckey)

        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return        

        ga=self.ga
        ge=self.ge

        radinf=1000
        radinfnm=radinf*km2nm

        fld='vt8'

        ufld='ua(lev=850)'
        vfld='va(lev=850)'
        ga("%s=hcurl(%s,%s)*1e6"%(fld,ufld,vfld))

        # -- convert SHEM neg rel vort to positive...
        #
        stmIsShem=isShemBasinStm(self.stmid)
        if(stmIsShem):
            ga("%s=-%s"%(fld,fld))

        # --get storm params
        #
        try:
            meanvt850=self.stmData[self.tau,15]
            if(stmIsShem):
                meanvt850=-meanvt850
        except:
            print 'WWW(TcDiag.pltVort850) -- no meanvt850 from diag file for tau: ',self.tau,' set undef'
            meanvt850=-999.
            

        cmean=self.getCircleMean(fld,self.latc,self.lonc,radinfnm)
        cmean=cmean*10.0


        pint=40
        #self.plotFldShaded(fld,pint,black1=-40,black2=40,rbrange='-120 480',drawcontour=0,clsize=0.06)
        self.plotFldShaded(fld,ptype='850vort',drawcontour=1,clsize=0.06)

        #self.plotFldShaded(fld,pint,black1=-20,black2=20,drawcontour=0,clsize=0.06)
        #self.plotFldContour(fld,clevs='20 60 120 180 240',doblackout=1,ccolor=3,cthick=5,clsize=0.06)
        self.plotWindStreams(ufld,vfld,starrspc=2.0,strmden=4)

        self.drawHurr()
        self.drawRadinf(radinfnm)
        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir,lcol=2,doblackout=0,lthk=20)

        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)


        t1="TCdiag(%s) 850VRT(mean): %3.0f for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,meanvt850,self.stmid,self.dtg,self.tau,radinf)
        t2a="Rel Vort (10`a-6`n s`a-1`n) mean: %3.0f "%(cmean)
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)
        self.printPlot(pltpath)
        if(dotest):
            cmd="xv %s"%(pltpath)
            mf.runcmd(cmd)




    def pltDiv200(self,regrid=0.5,
                  regriddiv=0.25,
                  dotest=0,
                  override=0):

        self.setInitialGA()

        ckey='16 200dvrg    (/s)'
        pvar='200dvrg'
        pltpath=self.setPlotuRl(pvar,ckey)

        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return

        ga=self.ga
        ge=self.ge

        radinf=1000
        radinfnm=radinf*km2nm

        fld='div200'

        u2='u2'
        v2='v2'
        ufld='(ua(lev=200))'
        vfld='(va(lev=200))'

        if(regrid != None):
            ga("%s=re(%s,%f)"%(u2,ufld,regrid))
            ga("%s=re(%s,%f)"%(v2,vfld,regrid))
        else:
            ga("%s=%s"%(u2,ufld))
            ga("%s=%s"%(v2,vfld))

        ga("%s=hdivg(%s,%s)*1e6"%(fld,ufld,vfld))
        if(regriddiv != None):
            ga("%s=re(%s,%f)"%(fld,fld,regriddiv))

        ga("%s=smth9(%s))"%(fld,fld))

        ga("%s=%s*%f"%(u2,u2,ms2knots))
        ga("%s=%s*%f"%(v2,v2,ms2knots))

        # --get storm params
        #
        try:
            meandiv200=self.stmData[self.tau,16]
        except:
            meandiv200=999.

        cmean=self.getCircleMean(fld,self.latc,self.lonc,radinfnm)
        cmean=cmean*10.0

        pint=20
        self.plotFldShaded(fld,cint=pint,black1=-40,black2=40,rbrange='-150 150',drawcontour=0,clsize=0.06)
        #self.plotFldShaded(fld,pint,black1=-20,black2=20,drawcontour=0,clsize=0.06)
        #self.plotFldContour(fld,clevs='20 60 120 180 240',doblackout=1,ccolor=3,cthick=5,clsize=0.06)
        self.plotWindStreams(u2,v2,ptype='w200',
                             starrspc=2.0,strmden=4,doscale=1,cthick=6)
        #self.plotWindBarbs(u2, v2, doscale=1, doclear=0, barbskip=None, 
        #                   barbsize=0.05)

        self.drawHurr()
        self.drawRadinf(radinfnm)

        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir,lcol=1,doblackout=0,lthk=20)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)

        t1="TCdiag(%s) 200DVRG(mean): %3.0f for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,meandiv200,self.stmid,self.dtg,self.tau,radinf)
        t2a="Div (10`a-6`n s`a-1`n) mean: %3.0f"%(cmean)
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)
        self.printPlot(pltpath)
        if(dotest):
            cmd="xv %s"%(pltpath)
            mf.runcmd(cmd)


    def pltSst(self,ptype='sst',dotest=0,
               minsstC=0.0,maxsstC=35.0,useall=0,dohl=0,
               override=0):

        self.setInitialGA()

        ckey='10 sst       (10c)'
        pvar='sst'
        pltpath=self.setPlotuRl(pvar,ckey)

        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return

        ga=self.ga
        ge=self.ge

        if(ga.oisstOpened == 0 and hasattr(self,'oisstCtlpath')):
            ga.fh2=ga.open(self.oisstCtlpath)
            ga.oisstOpened=1



        fld='sst2'

        if(useall):
            ga("%s=sstall.2(t=1)"%(fld))
        else:
            ga("%s=maskout(sst.2(t=1),abs(sst.2(t=1))*1-0.01)"%(fld))

        flda='sst2a'
        ga("%s=ssta.2(t=1)"%(flda))


        try:
            #vmaxF=self.stmData[self.tau,3]
            # -- use adeck Vmax vice tcdiag Vmax
            vmaxF=self.customData[self.tau,1]
            rmaxF=self.stmData[self.tau,4]  
        except:
            vmaxF=-999.
            rmaxF=-999.


        try:
            meansst=int(self.stmData[self.tau,10])
            meanssta=int(self.customData[self.tau,5])
        except:
            meansst=9999
            meanssta=9999


        pvara='sstanom'
        ckeya='00 sstanom   (10c)'
        pltpatha=self.setPlotuRl(pvara,ckeya)

        self.plotFldShaded(fld,ptype,drawcontour=1)
        self.plotFldContour(fld,clevs='26.5',doblackout=1,ccolor=1,cthick=5)

        self.drawHurr()
        self.drawRadinf(self.radinfSstnm,lcol=3,hemiDir='quad',lthk=5)
        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)


        cmeansst='---'
        if(meansst != 9999): cmeansst="%3.1f"%(meansst*0.1)

        t1="TCdiag(%s) SST(mean): %s C for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,cmeansst,self.stmid,self.dtg,self.tau,self.radinfSst)
        t2a="sst [C]"
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)

        self.printPlot(pltpath)
        if(dotest):
            cmd="xv %s"%(pltpath)
            mf.runcmd(cmd)
            return

        # -- plot the sst anom
        #
        self.setInitialGA()

        flda='sst2a'
        ga("%s=ssta.2(t=1)*const(%s,1.0)"%(flda,fld))

        self.plotFldShaded(flda,cint=0.5,black1=-0.5,black2=0.5,rbrange='-3 3',drawcontour=0)

        self.drawHurr()
        self.drawRadinf(self.radinfSstnm)
        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)

        cmeanssta='---'
        if(meanssta != 9999): cmeanssta="%3.1f"%(meanssta*0.1)

        t1="TCdiag(%s) SSTA(mean): %s C for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,cmeanssta,self.stmid,self.dtg,self.tau,self.rmax)
        t2a="sst anom [C]"
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)

        self.printPlot(pltpatha)
        if(dotest):
            cmd="xv %s"%(pltpatha)
            mf.runcmd(cmd)

    def makeRociPociGs(self,var,cint,cmax,cmin,
                       dcenterTol=200.0,undef99=999.,
                       verb=0,doplot=0):

        from osgeo import ogr

        def getMeanLatLon(geom):

            np=geom.GetPointCount()
            latm=0.0
            lonm=0.0
            mroci=0.0
            for i in range(0,np):

                (lon,lat)=geom.GetPoint(i)[0:2]
                if(lon < 0.0): lon=lon+360.0

                latm=latm+lat
                lonm=lonm+lon
                droci=gc_dist(latc,lonc,lat,lon)
                mroci=mroci+droci

            latm=latm/np
            lonm=lonm/np
            dcenter=gc_dist(latc,lonc,latm,lonm)
            mroci=mroci/np
            #print 'CCC',latc,lonc
            #print 'LatLonMean: %5.1f %6.1f dCen: %5.0f'%(latm,lonm,dcenter)
            if(dcenter > dcenterTol):
                rc=None
            else:
                rc=(latm,lonm,dcenter,mroci)

            return(rc)


        gradscmd=self.grads21Cmd

        gspath='/tmp/roci.%s.%s.gs'%(self.dtg,self.model)
        okmlpath='/tmp/roci.%s.%s'%(self.dtg,self.model)
        kmlpath='/tmp/roci.%s.%s.kml'%(self.dtg,self.model)
        pngpath='/tmp/roci.%s%s.png'%(self.dtg,self.model)

        latc=self.latc
        lonc=self.lonc

        ge=self.ge
        gtime=ge.gtime
        lat1=ge.lat1
        lat2=ge.lat2
        lon1=ge.lon1
        lon2=ge.lon2
        ctlpath=self.ctlpath

        gs="""function main(args)
rc=gsfallow('on')
rc=const()
'open %s'
'set lat %f %f'
'set lon %f %f'
'set time %s'
'set gxout kml'
'set kml -ln %s'
'set cmax %f'
'set cmin %f'
'set cint %f'
'd smth9(smth9(%s))'
'c'
'quit'
return
"""%(ctlpath,
     lat1,lat2,
     lon1,lon2,
     gtime,
     okmlpath,
     cmax,cmin,cint,
     var)

        rc=MF.WriteString2Path(gs,gspath)
        cmd='''%s -lbc "run %s"'''%(gradscmd,gspath)
        mf.runcmd(cmd)

        rocis=[]
        ds = ogr.Open(kmlpath)
        nl=0

        if(ds == None): return (rocis)
        for lyr in ds:
            nl=nl+1
            if(verb): print 'LLLLLLLLLLLLLLL ',nl
            for feat in lyr:
                clev=feat.name
                geom = feat.GetGeometryRef()
                if geom != None:
                    np=geom.GetPointCount()
                    pb=geom.GetPoint(0)[0:2]
                    pe=geom.GetPoint(np-1)[0:2]

                    if(pb[0] == pe[0] and pb[1] == pe[1]):
                        rc=getMeanLatLon(geom)
                        # -- bypass closed isobars far from storm center
                        #
                        if(rc == None): continue
                        dcent=rc[-2]
                        mroci=rc[-1]
                        if(verb): print 'CCC: %s dcenter: %5.0f  ROCI: %5.0f'%(clev,dcent,mroci)
                        rocis.append([clev,mroci])


        if(len(rocis) == 0):
            pocil=undef99
            rocil=undef99
        else:
            (pocil,rocil)=rocis[-1]

        if(len(rocis) >= 2): 
            (pocilm1,rocilm1)=rocis[-2]
        else:
            pocilm1=undef99
            rocilm1=undef99


        gsplt="""function main(args)
rc=gsfallow('on')
rc=const()
'open %s'
'set lat %f %f'
'set lon %f %f'
'set time %s'
'set gxout contour'
'set cint %f'
'd smth9(smth9(%s))'
t1='Rlast %s/%3.0f RlastM1: %s/%3.0f'
t2='%s %s tau: %d'
rc=toptitle(t1,t2)
'printim %s'
'quit'
return
"""%(ctlpath,
     lat1,lat2,
     lon1,lon2,
     gtime,
     cint,var,
     pocil,rocil,
     pocilm1,rocilm1,
     self.model,self.dtg,self.tau,
     pngpath)

        if(doplot):
            rc=MF.WriteString2Path(gsplt,gspath)
            cmd='''%s -lbc "run %s"'''%(gradscmd,gspath)
            mf.runcmd(cmd)
            cmd="xv %s"%(pngpath)
            mf.runcmd(cmd)
            
        # -- save on main object
        #
        self.AllRocis[self.stmid,self.tau]=rocis
        return(rocis)



    def pltPrecip(self,dohemiPR=1,dohl=0,dotest=0,
                  override=0):

        from numpy import arange

        pvar='precip'
        ckey='03 tot pr (10mm/d)'
        pltpath=self.setPlotuRl(pvar,ckey)

        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=500
        radinfnm=radinf*km2nm

        pslmin=920.0
        pslhilo=1004.0
        pslmax=1034.0

        pintpsllo=4.0
        pintpslhi=2.0

        pslclevs=''

        for p in arange(pslmin,pslhilo+0.1,pintpsllo):
            pslclevs=pslclevs+'%6.1f '%(p)

        for p in arange(pslhilo,pslmax+0.01,pintpslhi):
            pslclevs=pslclevs+'%6.1f '%(p)

        if(hasattr(self,'useFldOutput')  and self.useFldOutput == 1):
            prexpr='pr'
            fldpr='pr'

        elif(hasattr(self.m2,'setprvar')):
            prexpr=self.m2.setprvar(self.dtg,self.tau)
            fldpr='prplt'
            prexpr=prexpr.replace('_prvar',fldpr)
            prexpr=prexpr.replace("'",'')
        else:
            print 'EEEE TcDiag.pltPrecip -- ',self.model,' must have setprvar method'
            sys.exit()

        ga(prexpr)

        if(hasattr(self,'useFldOutput') and self.useFldOutput == 1):
            fldpsl='psl'
            fldpsllo='(maskout(psl,%f+0.1-psl))'%(pslhilo)
            fldpslhi='(maskout(psl,psl-%f-0.1))'%(pslhilo)
        else:
            fldpsl=self.m2.modelpslvar
            fldpsllo='(maskout(psl*0.01,%f+0.1-psl*0.01))'%(pslhilo)
            fldpslhi='(maskout(psl*0.01,psl*0.01-%f-0.1))'%(pslhilo)

        # -- get roci/poci
        #
        pminc=self.pminc
        if(pminc < 0): pminc=9999.

        pmax2mb=1018.0
        pmin2mb=990.0
        pint2mb=2.0
        rocis=self.makeRociPociGs(fldpsl,pint2mb,pmax2mb,pmin2mb)

        # -- output ROCI/POCI & labels
        #
        gotrocil=0
        gotrocilm1=0

        if(len(rocis) == 0):
            t2a="PMIN: %4.0f mb  NNN-no POCI/ROCI"%(pminc)

        elif(len(rocis) == 1):
            (pocil,rocil)=rocis[-1]
            t2a="PMIN: %4.0f mb   P/Roci L: %s / %3.0f nm"%\
                (pminc,pocil,rocil)
            gotrocil=1
            gotrocilm1=0

        elif(len(rocis) >= 2):
            (pocil,rocil)=rocis[-1]
            (pocilm1,rocilm1)=rocis[-2]
            t2a="PMIN: %4.0f mb   P/Roci L: %s / %3.0f nm   P/Roci L-1: %s / %3.0f nm"%\
                (pminc,pocil,rocil,pocilm1,rocilm1)

            gotrocil=1
            gotrocilm1=1

        # --get storm params
        #
        try:
            #vmaxF=self.stmData[self.tau,3]
            # -- use adeck Vmax vice tcdiag Vmax
            vmaxF=self.customData[self.tau,1]
            rmaxF=self.stmData[self.tau,4]
        except:
            vmaxF=999
            rmaxF=999


        try:
            meanpr=self.customData[self.tau,6]
        except:
            meanpr=999

        prhemiR=prhemiL=-999.
        if(dohemiPR):
            (prhemiR,prhemiL)=self.getHemiVals(fldpr,self.latc,self.lonc,radinfnm,self.stmdir)


        pint=10
        #self.plotFldShaded(fld,cint=pint,black1=-100,black2=20,drawcontour=0,rbrange='0 200',clsize=0.06)
        self.plotFldShaded(fldpr,ptype='pr',drawcontour=0,clsize=0.06)

        self.plotFldContour(fldpsl,pintpslhi,ccolor=1,cthick=5,clskip=4,clsize=0.06,clevs=pslclevs)
        if(gotrocil): self.plotFldContour(fldpsl,clevs='%s'%(pocil),doblackout=1,ccolor=2,cthick=10,clsize=0.07)
        if(gotrocilm1): self.plotFldContour(fldpsl,clevs='%s'%(pocilm1),doblackout=1,ccolor=2,cthick=10,clsize=0.07)

        self.drawHurr()
        self.drawRadinf(radinfnm,hemiDir=self.stmdir,lcol=65,lthk=5)

        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)


        t1="TCdiag(%s) TOT PR: %3.0f mm/d for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,meanpr,self.stmid,self.dtg,self.tau,radinf)
        #t2a="HemiR: %4.0f HemiL: %4.0f"%(prhemiR,prhemiL)
        #t2=t2a+self.t2b+self.t2c
        t2=t2a+self.t2b

        self.pT.top(t1,t2)
        self.printPlot(pltpath)
        if(dotest):
            cmd="xv %s"%(pltpath)
            mf.runcmd(cmd)
        
        return(rocis)




    def pltPrw(self,regrid=0.5,domodelprw=1,dotest=0,
               override=0):

        self.setInitialGA(bmoverride=0)

        pvar='tpw'
        ckey='12 tpw        (mm)'

        pltpath= self.setPlotuRl(pvar,ckey)
        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return

        ga=self.ga
        ge=self.ge

        fld='tpw'
        fldG="grd%s"%(fld)


        # --get storm params
        #
        try:
            #vmaxF=self.stmData[self.tau,3]
            # -- use adeck vice tcdiag Vmax
            vmaxF=self.customData[self.tau,1]
            rmaxF=self.stmData[self.tau,4]
            stmspd=self.stmData[self.tau,8]
        except:
            vmaxF=-999.
            rmaxF=-999.
            stmdpsd=-999.

        try:
            meanprw=self.stmData[self.tau,12]
        except:
            meanprw=-999.

        # ----------------------------------------------------------
        # for models without prw output -- use grads vint function
        # not sure if ta is tv (probably not) need to calc q separately?
        # error of ~ 1-3 mm over ocean, bad over big terrain
        #
        #prwexpr1="vint(psl*0.01,tvrh2q(ta,hur),100)"
        # -- more correct based on the classic formula
        #
        rhfact='0.01'
        if(self.model == 'ngp2'): rhfact='1.0'
        vaporP='(esmrf(ta)*hur*%s)'%(rhfact)

        # -- ngp2 blow up for /w21/dat/nwp2/w2flds/dat/ngp2/2010060112/ngp2.w2flds.2010060112.ctl because
        #  ta undef

        vaporP='(esmrf(const(ta,273.16,-u))*hur*%s)'%(rhfact)
        mixingR="0.622*(%s/(lev-%s))"%(vaporP,vaporP)

        # -- cmc has hus for moisture var
        #
        if(self.model == 'cgd2'):  mixingR='hus'
        prwexpr="vint(psl*0.01,%s,100)"%(mixingR)

        if((self.model == 'gfs2' or self.model == 'ecmt') and
           domodelprw): prwexpr='prw'

        if(hasattr(self,'useFldOutput')):
            prwexpr='prw'

        ga("%s=%s"%(fld,prwexpr))

        self.plotFldShaded(fld,ptype='prw',
                           cint=5,black1=-100,black2=60,
                           drawcontour=0,rbrange='20 80')

        usplt='uas*%f'%(ms2knots)
        vsplt='vas*%f'%(ms2knots)

        ga("us=%s"%(usplt))
        ga("vs=%s"%(vsplt))
        ush='us'
        vsh='vs'

        if(regrid != None):
            ga("%s=re(%s,%f)"%(ush,ush,regrid))
            ga("%s=re(%s,%f)"%(vsh,vsh,regrid))

        self.plotWindBarbs(ush,vsh,doscale=0, doclear=0, barbskip=2, 
                           doblack=1,ccolor=1,cint=5,barbsize=0.030)

        #self.plotFldContour(fld,cint=5)
        self.drawHurr()
        self.drawRadinf(self.rmaxnm)

        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)

        # -- title
        #
        t1="TCdiag(%s) TPW(mean): %2.0f mm for: %s  dtg: %s  tau: %d R=0-%2.0f km"%(self.umodel,meanprw,self.stmid,self.dtg,self.tau,self.rmax)
        t2a="prw [mm H20]"
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)
        self.printPlot(pltpath)
        if(dotest):
            cmd='xv %s'%(pltpath)
            mf.runcmd(cmd)



    def pltHartCpsB(self,dohemiZ=1,verb=0):

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        radinf=500
        radinfnm=radinf*km2nm

        latc=self.latc
        lonc=self.lonc

        cpsB=self.customData[self.tau,11]

        fld='cpsb'
        pinc=10
        ga("%s=zthklo"%(fld))

        pvar='cps_baroclinc'
        ckey2='04 rmw        (km)'

        pltpath=self.setPlotuRl(pvar,ckey2)

        # -- get mean in R/L hemispheres
        #
        zhemiR=zhemiL=-999.
        if(dohemiZ):
            (zhemiR,zhemiL)=self.getHemiVals(fld,self.latc,self.lonc,radinfnm,self.stmdir)


        self.plotFldContour(fld,pinc)

        self.drawRadinf(radinfnm,hemiDir=self.stmdir)
        self.drawHurr()

        # -- scale shear arrow by 10 kt
        #
        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)

        t1="TCdiag(%s) Hart CPS B (900-600 Z`bthk`n): %3d for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,cpsB,self.stmid,self.dtg,self.tau,radinf)
        t2a="HemiR: %4.0f HemiL: %4.0f"%(zhemiR,zhemiL)
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)

        self.printPlot(pltpath)




    def pltVmax(self,dotest=0,verb=0,
                override=0):

        self.setInitialGA()

        pvar='max_wind'
        ckey2='04 rmw        (km)'

        pltpath=self.setPlotuRl(pvar,ckey2)
        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return


        ga=self.ga
        ge=self.ge

        latc=self.latc
        lonc=self.lonc

        fld='w'
        pinc=5

        ga("%s=mag(uas,vas)*%f"%(fld,ms2knots))


        self.plotFldShaded(fld,ptype='vmax',cint=pinc,
                           black1=-100,black2=25,drawcontour=1)
        #self.plotFldContour(fld,pinc)

        # -- draw the radius of max wind (nm)
        #
        try:
            #vmaxF=self.stmData[self.tau,3]
            # -- use adeck vice tcdiag Vmax
            vmaxF=self.customData[self.tau,1]
            rmaxF=self.stmData[self.tau,4]
        except:
            vmaxF=-999.
            rmaxF=-999.

        if(rmaxF > 0.0): self.drawRadinf(rmaxF*km2nm)
        self.drawHurr()
        self.drawRadinf(90.,lcol=3,hemiDir='quad',lthk=5)
        self.drawRadinf(180.,lcol=3,hemiDir='quad',lthk=5)


        # -- scale shear arrow by 10 kt
        #
        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)

        t1="TCdiag(%s) V`bMAX`n: %3.0f kt  R`bMAX`n: %4.0f nm  for: %s  dtg: %s  tau: %d "%(self.umodel,vmaxF,rmaxF*km2nm,self.stmid,self.dtg,self.tau)

        t2a="sfc wind speed [kt]"
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)
        self.printPlot(pltpath)
        if(dotest):
            cmd="xv %s"%(pltpath)
            mf.runcmd(cmd)





    def pltShear(self,barbskip=4,regrid=0.5,
                 dohemiShr=1,dohl=1,dotest=0,
                 override=0):

        """ plot the 850-200 mb shear fields and the mean in the 500 km radius circle
        """

        self.setInitialGA()

        pvar='shr_mag'
        ckeyc='01 tot shrmag (kt)'

        pltpath=self.setPlotuRl(pvar,ckeyc)
        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return


        ga=self.ga
        ge=self.ge

        pvar='shr_mag'
        ckeyc='01 tot shrmag (kt)'

        pltpath=self.setPlotuRl(pvar,ckeyc)
        doplot=0
        if(not(MF.ChkPath(pltpath)) or override): doplot=1
        if(not(doplot)): 
            print 'WWW -- %s -- already done or not override -- press...'%(pltpath)
            return

        radinf=500
        radinfnm=radinf*km2nm

        fld='magshr'
        fldG="grd%s"%(fld)
        ufld='ushr'
        vfld='vshr'
        ufld2='u2'
        vfld2='v2'
        ufld8='u8'
        vfld8='v8'

        # -- name of file => cstmkey in parseDiagFile
        #

        ga("%s=mag((ua(lev=200)-ua(lev=850)),(va(lev=200)-va(lev=850)))*%f"%(fld,ms2knots))
        ga("%s=(ua(lev=200)-ua(lev=850))*%f"%(ufld,ms2knots))
        ga("%s=(va(lev=200)-va(lev=850))*%f"%(vfld,ms2knots))

        ga("%s=(ua(lev=200))*%f"%(ufld2,ms2knots))
        ga("%s=(va(lev=200))*%f"%(vfld2,ms2knots))

        ga("%s=(ua(lev=850))*%f"%(ufld8,ms2knots))
        ga("%s=(va(lev=850))*%f"%(vfld8,ms2knots))


        if(regrid != None):
            ga("%s=re(%s,%f)"%(ufld,ufld,regrid))
            ga("%s=re(%s,%f)"%(vfld,vfld,regrid))

        if(self.dlat > 0.):
            self.barbskip=self.dlat/3


        try:
            shrmag=self.stmData[self.tau,6]
            shrdir=self.stmData[self.tau,7]
        except:
            shrmag=999.
            shrdir=999.

        # -- get mean in R/L hemispheres
        #
        whemiR=whemiL=vhemiR=uhemiR=uhemiL=vhemiR=vhemiL=dhemiR=dhemiL=-999.

        goodshr=1
        hemidir=self.stmdir
        hemidir=shrdir
        if(hemidir == 9999): goodshr=0

        try:
            shrmag=self.stmData[self.tau,6]
            shrdir=self.stmData[self.tau,7]
        except:
            shrmag=999.
            shrdir=999.
            goodshr=0

        if(dohemiShr and goodshr):

            # -- mean wind in each hemi at 200 and 850
            #

            (uhemiR2,uhemiL2)=self.getHemiVals(ufld2,self.latc,self.lonc,radinfnm,hemidir)
            (uhemiR8,uhemiL8)=self.getHemiVals(ufld8,self.latc,self.lonc,radinfnm,hemidir)

            (vhemiR2,vhemiL2)=self.getHemiVals(vfld2,self.latc,self.lonc,radinfnm,hemidir)
            (vhemiR8,vhemiL8)=self.getHemiVals(vfld8,self.latc,self.lonc,radinfnm,hemidir)


            # -- mean shear in each hemi
            #
            (uhemiR,uhemiL)=self.getHemiVals(ufld,self.latc,self.lonc,radinfnm,hemidir)
            (vhemiR,vhemiL)=self.getHemiVals(vfld,self.latc,self.lonc,radinfnm,hemidir)


            ushemiR=uhemiR2-uhemiR8
            vshemiR=vhemiR2-vhemiR8

            ushemiL=uhemiL2-uhemiL8
            vshemiL=vhemiL2-vhemiL8

            whemiR=sqrt(ushemiR*ushemiR + vshemiR*vshemiR)
            whemiL=sqrt(ushemiL*ushemiL + vshemiL*vshemiL)

            dhemiR=atan2(ushemiR,vshemiR)*rad2deg
            dhemiL=atan2(ushemiL,vshemiL)*rad2deg

            if(dhemiR < 0.0): dhemiR=360.0+dhemiR
            if(dhemiL < 0.0): dhemiL=360.0+dhemiL


        self.plotWindBarbs(ufld,vfld,barbskip=barbskip,barbsize=0.035,doscale=1,docbarn=1)
        self.plotWindStreams(ufld,vfld,strmden=4,doscale=1,starrspc=2)

        ga("%s=re(%s,1.0)"%(fld,fld))
        ga("%s=smth9(smth9(%s))"%(fld,fld))

        self.plotFldContour(fld,clevs='5 10 15 20 25 30 35 40 ',clsize=0.07,
                            ccols='3 3 3 7 7 2 2 2',cthick=7,doblackout=1)


        if(dohl): self.doMfhilo(fldG,'l',pltpath,dohl=dohl)

        self.drawHurr()
        self.drawRadinf(radinfnm,lcol=43)

        # -- scale shear arrow by 10 kt
        #
        if(goodshr):
            len=0.5*(shrmag/10.0)
            self.drawArrow(self.latc,self.lonc,len=len,dir=shrdir,lcol=43)

            #len=0.5*(whemiR/10.0)
            #self.drawArrow(self.latc,self.lonc,len=len,dir=dhemiR,lcol=3)

            #len=0.5*(whemiL/10.0)
            #self.drawArrow(self.latc,self.lonc,len=len,dir=dhemiL,lcol=4)

        self.drawArrow(self.latc,self.lonc,len=self.arrlen,dir=self.arrdir,lcol=1)
        if(self.tau == 0):
            self.drawArrow(self.latc,self.lonc,len=self.tau0stmspdArr,dir=self.tau0stmdir,lcol=self.obsmotionLCOL,doblackout=self.obsmotionBO,lthk=self.obsmotionTHK)

        t1="TCdiag(%s) SHR`bMAG`n %3.0f kt SHR`bDIR`n: %3.0f`3.`0 (B) for: %s dtg: %s tau: %d R=0-%2.0f km"%(self.umodel,shrmag,shrdir,self.stmid,self.dtg,self.tau,radinf)

        t2a="HemiR:%2.0f/%3.0f`3.`0 HemiL:%2.0f/%3.0f`3.`0"%(whemiR,dhemiR,whemiL,dhemiL)
        t2=t2a+self.t2b+self.t2c

        self.pT.top(t1,t2)
        self.printPlot(pltpath)
        if(dotest):
            cmd="xv %s"%(pltpath)
            mf.runcmd(cmd)


    def fld2var(self,fld,level):

        fact=1.0
        afact=0.0
        cfact=str(fact)

        format='%5.0f'
        if(fld == 'u' and level == self.sfcLevel):
            var='uas'
            fact=ms2knots*10.0
            units='(10kt)'
            cfact='10'
        elif(fld == 'u' and level != self.sfcLevel):
            var='ua'
            fact=ms2knots*10.0
            units='(10kt)'
            cfact='10'
        elif(fld == 'v' and level == self.sfcLevel):
            var='vas'
            fact=ms2knots*10.0
            units='(10kt)'
            cfact='10'
        elif(fld == 'v' and level != self.sfcLevel):
            var='va'
            fact=ms2knots*10.0
            units='(10kt)'
            cfact='10'
        elif(fld == 'r' and level == self.sfcLevel):
            var='hurs'
            format='%5.0f'
            units='   (%)'
            cfact=''
        elif(fld == 'r' and level != self.sfcLevel):
            var='hur'
            format='%5.0f'
            units='   (%)'
            cfact=''
        elif(fld == 't' and level == self.sfcLevel):
            var='tas'
            afact=-273.16
            units=' (10c)'
            cfact='10'
        elif(fld == 't' and level != self.sfcLevel):
            var='ta'
            afact=-273.16
            fact=10.
            units=' (10c)'
            cfact='10'
        elif(fld == 'p' and level == self.sfcLevel):
            var='psl'
            fact='0.01'
            format='%5.0f'
            units='  (mb)'
            cfact=''
        elif(fld == 'z' and level != self.sfcLevel):
            var='zg'
            fact=0.1
            format='%5.0f'
            units='  (dm)'
            cfact=''

        return(var,fact,afact,format,cfact,units)



    def getSoundingData(self):


        ualevs=self.ge.Levs
        if(self.domandonly): ualevs=[850,500,200]
        levels=['sfc']+ualevs
        if(self.doStndOnly):
            ualevs=[1000,850,700,500,400,300,250,200,150,100]
            levels=ualevs

        fldssfc=['t','r','p','u','v']
        fldua=['t','r','z','u','v']

        clevels='NLEVS %03d '%(len(levels))

        for level in levels:

            if(level == 'sfc'):
                flds=fldssfc
                clevels=clevels+self.sfcLevel.upper()
            else:
                flds=fldua
                level="%2.0f"%(level)
                clevels=clevels+' %04d'%(int(level))

            for fld in flds:
                rc=self.getSounding(fld,level)

        self.clevels=clevels




    def getSounding(self,ifld,level,verb=0):

        def printmean(ifld,level,meanfld):
            cmeanfld="%s"%(format)%(meanfld)
            print 'fld: %3s level: %4s  mean: %s'%(ifld,level,cmeanfld)


        def loadhash(ifld,level,units,format,meanfld):

            if(level == 'sfc'):
                self.sndkey="%s_surf   %s"%(ifld,units)
            else:
                self.sndkey="%s_%04d   %s"%(ifld,int(level),units)

            cmeanfld="%s"%(format)%(meanfld)
            if(self.tau == self.taus[0]): self.sndKeys.append(self.sndkey)
            self.sndData[self.tau][self.sndkey]=cmeanfld


        try:
            if(self.ualevsPlot[int(level)][ifld] == 1): chkplot=1
        except:
            chkplot=0

        doplot=0
        if(chkplot and self.doplot): doplot=1

        self.setInitialGA()

        ga=self.ga
        ge=self.ge

        (fld,fact,afact,format,cfact,units)=self.fld2var(ifld,level)

        dfld=ifld+'grd'

        if(not(self.doDiagPlotsOnly)):
            try:
                if(level != 'sfc'):
                    ga("set lev %s"%(level))
                ga("%s=re(%s,%s)*%s + %s*%s"%(ifld,fld,self.reRes,fact,afact,fact))
                ga("%s=re(%s,%s)*%s + %s"%(dfld,fld,self.reRes,1.0,afact))
            except:
                meanfld=9999.
                format='%5.0f'
                loadhash(ifld,level,units,format,meanfld)
                return
        else:
            if(level != 'sfc'):
                ga("set lev %s"%(level))
            ga("%s=%s*%s + %s*%s"%(ifld,fld,fact,afact,fact))
            ga("%s=%s*%s + %s"%(dfld,fld,1.0,afact))
            meanfld=999.


        if(ifld == 'u' or ifld == 'v'):
            if(not(self.doDiagPlotsOnly)):
                ga("tcprop %s %f %f %f"%(ifld,self.latc,self.lonc,self.radinfOutWindnm))
                meanfld=float(ga.rword(5,2))
                if(abs(meanfld) >= 9999.):
                    meanfld=9999.0
                    format='%5.0f'
            else:
                meanfld=999.0

            loadhash(ifld,level,units,format,meanfld)

            if(doplot and meanfld != 9999.):
                self.plotFldContour(ifld)
                self.drawHurr()
                self.drawRadinf(self.radinfInnm)
                self.drawRadinf(self.radinfOutnm)
                t1="TCdiag(%s) Var: %s Level: %s  Mean: %-2.1f for: %s  dtg: %s  tau: %d  R=%2.0f-%2.0f km"%\
                    (self.umodel,ifld.upper(),level,meanfld,self.stmid,self.dtg,self.tau,self.radinfIn,self.radinfOut)
                t2="Wind barbs [kt] mfact: %s latc: %4.1f  lonc: %4.1f"%(cfact,self.latc,self.lonc)

        else:

            if(not(self.doDiagPlotsOnly)):
                ga("tcprop %s %f %f %f"%(ifld,self.latc,self.lonc,self.radinfInnm))
                meanin=float(ga.rword(5,2))*self.areaIn
                ga("tcprop %s %f %f %f"%(ifld,self.latc,self.lonc,self.radinfOutnm))
                meanout=float(ga.rword(5,2))*self.areaOut
                meanfld=(meanout-meanin)/self.areaAnnulus
                if(abs(meanfld) >= 9999.):
                    meanfld=9999.0
            else:
                meanfld=999.

            format='%5.0f'
            loadhash(ifld,level,units,format,meanfld)

            if(doplot and meanfld != 9999.):
                self.plotFldContour(ifld)
                self.drawHurr()
                self.drawRadinf(self.radinfInnm)
                self.drawRadinf(self.radinfOutnm)
                t1="TCdiag(%s) Var: %s Level: %s  Mean: %-2.1f for: %s  dtg: %s  tau: %d  R=%2.0f-%2.0f km"%\
                    (self.umodel,ifld.upper(),level,meanfld,self.stmid,self.dtg,self.tau,self.radinfIn,self.radinfOut)
                t2="mfact: %s  latc: %4.1f  lonc: %4.1f"%(cfact,self.latc,self.lonc)


        if(doplot and not(ifld == 'u' or ifld == 'v') and meanfld != 9999.):
            ckey=self.sndkey
            pvar="%s_%s"%(ifld,level)
            pltpath=self.setPlotuRl(pvar,ckey)
            self.pT.top(t1,t2)
            self.printPlot(pltpath)

        if(verb): printmean(ifld,level,meanfld)

        if( (ifld == 'u' or ifld == 'v') and doplot and meanfld != 9999.):
            ckey=self.sndkey
            pvar="%s_%s"%(ifld,level)
            pltpath=self.setPlotuRl(pvar,ckey)
            meanu=meanfld
            ufld='u'
            vfld='v'
            ufld2='u2'
            vfld2='v2'

            dufld=ufld2+'grd'
            dvfld=vfld2+'grd'

            (uvar,fact,afact,format,cfact,units)=self.fld2var(ufld,level)

            if(not(self.doDiagPlotsOnly)):

                expr="%s=re(%s,%s)*%s + %s*%s"%(ufld2,uvar,self.reRes,fact,afact,fact)
                ga(expr)
                expr="%s=re(%s,%s)*%s + %s"%(dufld,uvar,self.reRes,fact*0.1,afact)
                ga(expr)

                (vvar,fact,afact,format,cfact,units)=self.fld2var(vfld,level)
                ga("%s=re(%s,%s)*%s + %s*%s"%(vfld2,vvar,self.reRes,fact,afact,fact))
                ga("%s=re(%s,%s)*%s + %s"%(dvfld,vvar,self.reRes,fact*0.1,afact))

                ga("tcprop %s %f %f %f"%(ufld2,self.latc,self.lonc,self.radinfOutWindnm))
                meanu=float(ga.rword(5,2))
                ga("tcprop %s %f %f %f"%(vfld2,self.latc,self.lonc,self.radinfOutWindnm))
                meanv=float(ga.rword(5,2))

            else:

                (vvar,fact,afact,format,cfact,units)=self.fld2var(vfld,level)
                ga("%s=%s*%s + %s"%(dufld,uvar,fact*0.1,afact))
                ga("%s=%s*%s + %s"%(dvfld,vvar,fact*0.1,afact))


            doscale=0
            if(level != 'sfc' and int(level) <= 850): doscale=1
            self.plotWindBarbs(dufld,dvfld,doscale=doscale,doclear=0)
            self.drawHurr()


            self.pT.top(t1,t2)
            self.printPlot(pltpath)


    #dddddddddddddddddddddddddddddddddddddddddddddddddd -- general drawing methods
    #

    def drawHurr(self):

        (xp,yp)=self.getW2xy(self.latc,self.lonc)
        self.ga("draw wxsym 41 %s %s 0.25 1"%(xp,yp))
        self.ga("draw map")


    def drawRadinf(self,radinf,hemiDir=None,lcol=2,lsty=1,lthk=6,doblackout=1):

        pC=self.ga.gp.polyCircle
        if(hemiDir != 'quad'):
            pC.set(self.latc,self.lonc,radinf,hemiDir=hemiDir)
        else:
            pC.set(self.latc,self.lonc,radinf,hemiDir=None)

        if(doblackout):
            pC.border(lcol=0,lsty=lsty,lthk=20)
        pC.border(lcol=lcol,lsty=lsty,lthk=lthk)

        if(hemiDir != None):

            if(hemiDir == 'quad'):
                pC.set(self.latc,self.lonc,radinf,hemiDir=0)
                if(doblackout):
                    pC.hemiline(0,lcol=0,lsty=lsty,lthk=20)
                pC.hemiline(0,lcol=lcol,lsty=lsty,lthk=lthk)

                pC.set(self.latc,self.lonc,radinf,hemiDir=90)
                if(doblackout):
                    pC.hemiline(90,lcol=0,lsty=lsty,lthk=20)
                pC.hemiline(90,lcol=lcol,lsty=lsty,lthk=lthk)

            else:
                if(doblackout):
                    pC.hemiline(hemiDir,lcol=0,lsty=lsty,lthk=20)
                pC.hemiline(hemiDir,lcol=lcol,lsty=lsty,lthk=lthk)


    def drawArrow(self,x,y,len=None,dir=None,lab=None,labopt=None,
                  lcol=1,lsty=1,lthk=10,
                  doblackout=1,
                  ):


        if(dir == None):
            if(hasattr(self,'arrdir')):
                dir=self.arrdir
            else:
                dir=180.0

        if(len == None):
            if(hasattr(self,'arrlen')):
                len=self.arrlen
            else:
                len=0.5


        pA=self.ga.gp.arrow
        pA.set(self.latc,self.lonc,len,dir)
        if(doblackout):
            pA.draw(lcol=0,lsty=lsty,lthk=20)
        pA.draw(lcol=lcol,lsty=lsty,lthk=lthk)


    def drawMark(self,lat,lon,cmarkval,markcol=3):

        (xp,yp)=self.getW2xy(lat,lon)
        self.ga('set line %d'%(markcol))
        self.ga("draw mark 3 %s %s 0.20"%(xp,yp))
        self.ga('set strsiz 0.07')
        self.ga('set string 0 c 5')
        self.ga("draw string  %s %s %s"%(xp,yp,cmarkval))



    #pppppppppppppppppppppppppppppppppppppppppppppppppp -- general field plotting methods
    #

    def plotFldGrfill(self,fld,cint=None):

        ga=self.ga
        ga('set gxout grfill')
        if(cint != None):
            ga('set cint %f'%(cint))
        ga('d %s'%(fld))
        ga('cbarn')
        ga('set map 0 0 8')
        ga('draw map')
        ga('set map 1 0 4')
        ga('draw map')


    def plotFldShaded(self,fld,ptype=None,
                      cint=None,black1=None,black2=None,rbrange=None,
                      clcolor=-1,clthick=-1,clsize=0.09,cbarnsiz=0.8,
                      drawcontour=None):

        ga=self.ga
        ga('set gxout shaded')
        ga('set csmooth on')

        if(ptype == None):
            if(cint != None):
                ga('set cint %f'%(cint))

            if(rbrange != None):
                ga("set rbrange %s"%(rbrange))

            if(black1 != None and black2 != None):
                ga("set black %f %f"%(black1,black2))

            ga("set clopts %d %d %f"%(clcolor,clthick,clsize))

        elif(ptype == 'shear' or ptype == 'prw' or ptype == 'vmax' or
             ptype == 'w200' or ptype == 'sst' or ptype == '850vort' or
             ptype == 'pr'):
            self.colScale(ptype)


        ga('d %s'%(fld))


        if(drawcontour):
            ga('set gxout contour')
            ga('set clab off')

            if(cint != None):  ga('set cint %f'%(cint))
            ga('set ccolor 0')
            ga('set cthick 10')
            self.colScale(ptype,clevsOnly=1)
            ga('d %s'%(fld))

            if(cint != None):  ga('set cint %f'%(cint))
            ga('set ccolor 1')
            ga('set cthick 4')
            self.colScale(ptype,clevsOnly=1)
            ga('d %s'%(fld))

        ga('cbarn %f'%(cbarnsiz))
        ga('set map 0 0 8')
        ga('draw map')
        ga('set map 1 0 4')
        ga('draw map')


    def plotWindBarbs(self,u,v,ptype='shear',
                      doblack=0,ccolor=1,cint=5.0,cthick=5,docbarn=1,
                      doscale=1,doclear=0,barbskip=None,barbsize=0.05):

        ga=self.ga
        if(doclear): ga('c')
        ga('set gxout barb')

        bskip=barbskip
        if(barbskip == None): bskip=self.barbskip

        ga('set digsiz %f'%(barbsize))
        ga('set cthick 4')
        if(doscale):
            self.colScale(ptype='shear')
            expr='d %s;skip(%s,%d);mag(%s,%s)'%(u,v,int(bskip),u,v)
            ga(expr)

        else:

            expr='d %s;skip(%s,%d)'%(u,v,int(bskip))
            if(doblack):
                ga('set ccolor 0')
                ga('set cthick 20')
                ga('set cint %f'%(cint))
                ga(expr)

            ga('set ccolor %d'%(ccolor))
            ga('set cthick %d'%(cthick))
            ga('set cint %f'%(cint))
            ga(expr)

        if(doscale and docbarn):
            ga('cbarn') 
        ga('set map 0 0 8')
        ga('draw map')
        ga('set map 1 0 4')
        ga('draw map')


    def colScale(self,ptype='shear',clevsOnly=0):

        self.ga('run jaecolw2.gsf')
        if(ptype == 'shear'):
            #self.ga('set clevs  10  15  20   25  35  50  65 120')
            #if(not(clevsOnly)): self.ga('set ccols 39  37  35  21  22  24  25  27  29')            

            self.ga('set clevs  5  10  15  20   25  30  35  40')
            if(not(clevsOnly)): self.ga('set ccols 3 3    3   7    7   2  2   2   2')            

        elif(ptype == 'w200'):
            self.ga('set clevs   20  35  50   65   100  120 ')
            if(not(clevsOnly)): self.ga('set ccols 39  35  23   25   27   29    45' )

        elif(ptype == 'prw'):
            self.ga('run jaecol2a.gsf')
            self.ga('set clevs  15  20  25  30  35  40  45  50  55  60  65')
            if(not(clevsOnly)): self.ga('set ccols 59 58  49  48  45  43  35  23  24  25  28  29')

        elif(ptype == 'vmax'):

            self.ga('set rgb 47  10 80 160')
            self.ga('set rgb 49  00 50 100')
            self.ga('set clevs  10  15   20   35   50  65')
            if(not(clevsOnly)): self.ga('set ccols 0  49  47    43  21   25   29')

        elif(ptype == 'sst'):

            #self.ga('set clevs   22  24  26.5   28   29  30  31  32  35')
            self.ga('set clevs   22   24  25  26  27  28   29  30  31  32  35')
            if(not(clevsOnly)): self.ga('set ccols 0   49   47  43  21   23  25  27  29  61   63  65')

        elif(ptype == '850vort'):

            self.ga('set clevs   20   50  100  150  200  250   300  400  500  ')
            if(not(clevsOnly)): self.ga('set ccols 0   49  41 21   23  25  27  29  61 ')

        elif(ptype == 'pr'):

            self.ga('set rgb 98 185 255 00')
            self.ga('                    set ccols 0 39  37 36 98  22  24  26   29   63')
            if(not(clevsOnly)): self.ga('set clevs   1  2  4  8  16  32  64  128 256')
        else:
            print 'EEE invalid ptype in TcDiag.colScale()'
            sys.exit()



    def plotWindStreams(self,u,v,ptype='shear',wscale=1.0,
                        ccolor=1,cthick=5,doscale=0,doclear=0,
                        redrawmap=0,strmden=5,starrspc=None,
                        starrsiz=0.05,starrtyp=1):

        ga=self.ga
        if(doclear): ga('c')

        ga('set gxout stream')
        ga('set rgbrange off')
        ga('set ccolor %s'%(ccolor))
        ga('set cthick %s'%(cthick))

        if(starrspc != None):
            ga('set strmopts %d %f %f %d'%(strmden,starrspc,starrsiz,starrtyp))
        else:
            ga('set strmopts %d'%(strmden))

        if(doscale):

            ga('set ccolor 0')
            ga('set cthick 20')
            ga('d %s;%s'%(u,v))

            ga('set cthick %s'%(cthick))            

            self.colScale(ptype)

            ga('d %s;%s;mag(%s,%s)*%f'%(u,v,u,v,wscale))
            ga('cbarn 0.75 0')
        else:
            ga('set ccolor %s'%(ccolor))
            ga('d %s;%s)'%(u,v))

        if(redrawmap):
            ga('set map 0 0 8')
            ga('draw map')
            ga('set map 1 0 4')
            ga('draw map')

    def plotFldContour(self,fld,cint=None,clevs=None,ccols=None,ccolor=None,cthick=None,clskip=None,
                       clcolor=-1,clthick=-1,clsize=0.09,
                       doblackout=0):

        ga=self.ga

        ga('set gxout contour')

        if(cint != None):
            ga('set cint %f'%(cint))

        if(clevs != None):
            ga('set clevs %s'%(clevs))

        if(ccolor != None):
            ga('set ccolor %s'%(ccolor))

        if(clskip != None):
            ga('set clskip %d'%(clskip))

        if(ccols != None):
            ga('set ccols %s'%(ccols))

        if(cthick != None):
            ga('set cthick %d'%(cthick))

        ga("set clopts %d %d %f"%(clcolor,clthick,clsize))

        # -- black out contours
        #
        if(doblackout):

            if(ccols != None):
                ga('set ccols %s'%('0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  0 0'))
            else:
                ga('set ccolor 0')

            ga('set cthick 20')
            ga('d %s'%(fld))

            if(cint != None):
                ga('set cint %f'%(cint))

            if(clevs != None):
                ga('set clevs %s'%(clevs))

            if(ccolor != None):
                ga('set ccolor %s'%(ccolor))

            if(ccols != None):
                ga('set ccols %s'%(ccols))

            if(cthick != None):
                ga('set cthick %d'%(cthick))

            if(clskip != None):
                ga('set clskip %s'%(clskip))


        ga('d %s'%(fld))



    def finalizePyp(self,unlinkException=1):

        del self.ga
        del self.ge
        del self.tD
        del self.aD
        del self.m2
        if(hasattr(self,'pT')): del self.pT

        self.putPyp()


    def setPlotuRl(self,pvar,ckey):

        pltpath="%s/%s.%s.%03d.png"%(self.pltdir,pvar,self.stmid,self.tau)
        urlpath="%s/%s.%s.%03d.png"%(self.urldir,pvar,self.stmid,self.tau)
        MF.set2KeyDictList(self.urlData,self.tau,ckey,urlpath)
        return(pltpath)


    def tarball2Wxmap2(self,dtg,tag='diagflds',dmodelType='w2fld',ropt='',doW2scp=0):

        adeckSdir="%s/%s"%(self.bddir,dtg)
        MF.ChangeDir(adeckSdir)

        tdir='/tmp'

        tarball="%s/%s.%s.%s.tar"%(tdir,tag,self.model,dtg)
        cmd="tar -cvf %s *"%(tarball)
        mf.runcmd(cmd,ropt)

        (ddir,dfile)=os.path.split(self.diagpathALL)
        MF.ChangeDir(ddir)
        cmd="tar -uvf %s %s"%(tarball,dfile)
        mf.runcmd(cmd,ropt)

        if(doW2scp):
            cmd="scp %s mike_fiorino,wxmap2@frs.sourceforge.net:/home/frs/project/w/wx/wxmap2/dat/."%(tarball)
            mf.runcmd(cmd,ropt)


    def gettGdpyp(self,verb=0,abort=0):

        tG=None
        if(hasattr(self,'pyppathData')):
            tG=self.getPyp(pyppath=self.pyppathData,verb=self.verb)

        if(tG == None and abort):
            print 'EEE failed to open ',self.pyppathData
            sys.exit()

        return(tG)

    def gettGdAllpyp(self,verb=1):

        tG=None
        if(hasattr(self,'pyppathDataALL')):
            if(verb): print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ',self.pyppathDataALL
            tG=self.getPyp(pyppath=self.pyppathDataALL,verb=1)

        return(tG)


    def gettGhpyp(self):

        tGh=None
        if(hasattr(self,'pyppathHtml')):
            if(self.verb): print 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHH ',self.pyppathHtml
            tGh=self.getPyp(pyppath=self.pyppathHtml,verb=self.verb)

        return(tGh)


    def cleanDiagFiles(self,keepdtg,ropt=''):


        MF.ChangeDir(self.wdir)
        curdtgs=glob.glob("????/%s??????"%(keepdtg[0:4]))
        curdtgs.sort()

        for curdtg in curdtgs:
            cdtg=curdtg.split('/')[1]
            dtime=mf.dtgdiff(keepdtg,cdtg)
            if(dtime < 0.0):
                cmd="rm -r %s/%s"%(self.wdir,curdtg)
                mf.runcmd(cmd,ropt)






class TcDiagTau0(TcDiag):

    aidAliases={
        'ngf2':'gfs2',
        'nuk2':'ukm2',
        'nec2':'ecm2',
        'nec4':'ecm4',
        'necn':'ecmn',
        'nng2':'ngp2',
        'ncm2':'cmc2',
        'nngc':'ngpc',
    }

    aspectRatio=4.0/3.0

    dlatDefault=12.0
    dlonDefault=dlatDefault*aspectRatio

    dr=5
    dtheta=45
    rmax=200

    undef=9999.

    # units are km for dr and rmax
    #
    drnm=dr*km2nm
    rmaxnm=rmax*km2nm

    radinfIn=200
    radinfOut=800
    radinfInnm=radinfIn*km2nm
    radinfOutnm=radinfOut*km2nm

    radinfInWind=0
    radinfOutWind=500

    radinfInWindnm=radinfInWind*km2nm
    radinfOutWindnm=radinfOutWind*km2nm

    radinfSst=100

    # -- reduce for improper handling of undef in tcprop
    #
    radinfSst=50
    radinfSstnm=radinfSst*km2nm

    areaIn=radinfIn*radinfIn
    areaOut=radinfOut*radinfOut
    areaAnnulus=areaOut-areaIn
    basename='TCdiag'

    xsize=912
    xsize=1200
    ysize=(xsize*3)/4

    sfcLevel='surf'

    printMethod='printim'
    #printMethod='gxyat'
    printOpt="x%d y%d"%(xsize,ysize)
    if(printMethod == 'gxyat'):  printOpt="-r -x %s -y %s"%(xsize,ysize)


    # -- limit distance from center to look for H/L in mfhilo gr
    #
    reRes='0.25'
    mfhiloRad=300


    # -- increase dlat/dlon for storms way poleward
    #
    latitudeET=50.0
    dlatETFact=1.25

    maxLatitude=68.0
    barbskip=6

    stmVarNameByIndex={

        1:'latitude',
        2:'longitude',
        3:'max_wind',
        4:'rms',
        5:'min_slp',
        6:'shr_mag',
        7:'shr_dir',
        8:'stm_spd',
        9:'stm_hdg',
        10:'sst',
        11:'ohc',
        12:'tpw',
        13:'land',
        14:'850tang',
        15:'850vort',
        16:'200dvrg',
    }


    customVarNameByIndex={
        1:'ADECK  VMAX (KT)',
        2:'DIAG   VMAX (KT)',
        #3:'ADECK  PMIN (MB)',
        3:'precip',             # -- use psl into jtdiag table
        4:'DIAG   PMIN (MB)',
        5:'sstanom',
        6:'precip-actual',
        7:'PR  ASYM/TOT (%)',
        8:'TOTSHR MAG  (KT)',
        9:'SHR/TOTSHR   (%)',
        10:'SHR ASYM/TOT (%)',
        11:'CPS  B(AROCLINC)',
        12:'CPS   VTHERM(LO)',
        13:'CPS   VTHERM(HI)',
        14:'POCI        (MB)',
        15:'ROCI        (KM)',
        16:'R34mean     (KM)',
        17:'R50mean     (KM)',
        18:'R64mean     (KM)',
    }


    def __init__(self,dtg,model,tD,
                 ttaus=[0],
                 ctlpath=None,
                 domandonly=0,
                 doStndOnly=1,
                 doDiagOnly=0,
                 doDiagPlotsOnly=1,
                 doga=1,
                 gaopt='gacore',
                 verb=0,
                 dols=0,
                 dowebserver=0,
                 override=0,
                 doshort=0,
                 trkSource='tmtrk',
                 selectNN=1,
                 dobt=0,
                 dobail=1,
                 useLsdiagDat=0,
                 adeckSdir=None,
                 tbdir=None,
                 ctlquiet=0,
                 dlat=None,dlon=None,
                 justInit=0,
                 xgrads='grads',
                 dr=dr,dtheta=dtheta,rmax=rmax):

        if(adeckSdir == None):
            sdir='/dat3/tc/tmtrkN'
            sdir='/w21/dat/tc/tmtrkN'
            sdir="%s/tmtrkN"%(w2.TcDatDir)
            self.sdir=sdir
        else:
            self.adeckSdir=adeckSdir

        if(tbdir == None):
            tbdir=w2.TcTcanalDatDir0

        self.tbdir=tbdir
        self.tdir="%s/%s/%s"%(self.tbdir,dtg,model)

        rc=MF.ChkDir(self.tdir,'mk')

        self.dtg=dtg
        self.model=model
        self.umodel=model.upper()
        self.domandonly=domandonly
        self.doStndOnly=doStndOnly
        self.doDiagOnly=doDiagOnly
        self.doDiagPlotsOnly=doDiagPlotsOnly
        self.verb=verb
        self.doga=doga
        self.gaopt=gaopt
        self.dols=dols
        self.dowebserver=dowebserver
        self.trkSource=trkSource
        self.selectNN=selectNN
        self.dobt=dobt

        self.ctlquiet=ctlquiet

        self.tD=tD

        if(dlat == None):
            self.dlat=self.dlatDefault
            self.dlon=self.dlonDefault
        else:
            self.dlat=dlat
            self.dlon=self.dlat*self.aspectRatio

        if(dlon != None): self.dlon=dlon


        self.year=dtg[0:4]
        ddir="%s/nwp2/w2flds/dat"%(w2.W2BaseDirDat)

        webdir=w2.HfipWebBdir

        wdir="%s/tcdiagDAT0"%(w2.HfipWebBdir)
        bdir=TcDiagDatDir0
        
        wdirl=wdir

        dtgdir="%s/%s"%(self.year,dtg)
        urldir="%s/%s"%(dtgdir,model)
        pltdir="%s/%s"%(wdir,urldir)
        datdir="%s/%s"%(bdir,urldir)
        adkdir="%s/%s/ADECKS"%(wdir,dtgdir)
        dgndir="%s/%s/DIAGFILES"%(wdir,dtgdir)

        adkdirl="%s/%s/ADECKS"%(wdirl,dtgdir)
        dgndirl="%s/%s/DIAGFILES"%(wdirl,dtgdir)

        if(dowebserver == 0):
            pltdir=datdir
            webdir=TcDataBdir
        else:
            MF.ChkDir(adkdir,'mk')
            MF.ChkDir(dgndir,'mk')
            MF.ChkDir(adkdirl,'mk')
            MF.ChkDir(dgndirl,'mk')

        webdiagdir=pltdir

        self.ddir=ddir
        self.wdir=wdir
        self.webdir=webdir
        self.pltdir=pltdir
        self.urldir=urldir
        self.datdir=datdir
        self.webdiagdir=webdiagdir
        self.adeckOutdir=adkdir
        self.diagfileOutdir=dgndir

        self.adeckOutdirLocal=adkdirl
        self.diagfileOutdirLocal=dgndirl

        self.xgrads=xgrads

        self.initOutput()
        self.initTC(dtg)
        
        if(justInit): return


        # -- initialize the m2 object first
        #
        self.rcM2=self.initM2(dtg,model)

        FRtdatathere=0
        self.tauOffset=0

        lsdiagCtlpath=None
        if(ctlpath == None):
            rc=w2.getW2fldsRtfimCtlpath(model,dtg)
            (w2rc,w2ctlpath,w2taus,w2gribtype,w2gribver,datpaths,w2nfields,w2tauOffset)=rc
            self.tauOffset=w2tauOffset

            if(FRtdatathere == 0 and w2rc == 0 and lsdiagCtlpath == None):
                if(not(self.ctlquiet)): print 'III TCdiag.__init__ ctlpath= None'
                ctlpath=None
                maxtauModel=None
            elif(w2rc):
                if(not(self.ctlquiet)): print 'III TCdiag.__init__ ctlpath=w2ctlpath'
                ctlpath=w2ctlpath
                (tdir,file)=os.path.split(ctlpath)
            elif(FRtdatathere):
                if(not(self.ctlquiet)): print 'III TCdiag.__init__ ctlpath=FR.ctlpathM2'
                ctlpath=FR.ctlpathM2



        # -- add look for output path in case of redo without w2flds there...
        #
        ctls=glob.glob("%s/%s.%s.*.ctl"%(self.tdir,model,dtg))
        if(len(ctls) == 1): lsdiagCtlpath=ctls[0]

        if(lsdiagCtlpath != None):
            self.lsdiagCtlpath=lsdiagCtlpath

        if(useLsdiagDat):

            if(lsdiagCtlpath != None):
                print 'III TCdiag.__init__ ctlpath=lsdiagCtlpath'
                ctlpath=lsdiagCtlpath

                dmask=lsdiagCtlpath.replace('.ctl','.f???.dat')
                dats=glob.glob(dmask)
                w2taus=[]
                for dat in dats:
                    tau=dat.split('.')[-2][1:]
                    w2taus.append(int(tau))


        # -- override variables from m2

        # -- define reduced # of taus
        #
        if(ttaus == None):
            self.targetTaus=range(0,120+1,6)+range(132,168+1,12)
        else:
            self.targetTaus=ttaus

        # -- avoid tau data check if setting the ctlpath
        #
        if(ctlpath == None):

            # -- 20111031 -- make sure there is data -- for situations with limited taus, e.g., ecm2 2011061012, 061100
            #
            dtaus=[]
            ttaus=self.targetTaus
            lttaus=len(ttaus)
            for n in range(0,len(ttaus)):
                tau0=ttaus[n]
                taum1=tau0
                taup1=tau0

                if(n > 0):         taum1=ttaus[n-1]
                if(n < lttaus-1):  taup1=ttaus[n+1]

                if(w2taus == None): continue
                if(tau0 in w2taus or (taum1 in w2taus and taup1 in w2taus) ): dtaus.append(tau0)

            self.targetTaus=dtaus


        self.ctlpath=ctlpath

        if(ctlpath == None):
            print 'WWW(TcDiag) ctlpath == None)...returning'
            self.rcM2=None
            return

        if(self.doga): self.initGA(self.gaopt)


        # -- 20101031 -- bypass m2 data check since we're using
        # the more generic getW2fldsRtfimCtlpath method in w2base.py
        #if(self.rcM2):  self.rcM2=None ; return

        if(MF.GetPathSiz(self.ctlpath) == None):
            if(not(self.dols)): print "EEE.TCdiag(%s) does not exist...bailing with sys.exit() if dobail=1 currently: %d"%(self.ctlpath,dobail)
            if(dobail): sys.exit()


        if(not(self.dols)):
            MF.ChkDir(datdir,'mk')
            MF.ChkDir(pltdir,'mk')


        if(self.doDiagOnly and not(hasattr(self,'targetTaus'))):
            btau=0
            etau=126
            dtau=6
            self.targetTaus=range(btau,etau+1,dtau)+[132,144,156,168]


    def setTCtracker(self,stmid):

        # -- force the track to come from the best track

        btrk=self.btcs[stmid]
        self.aid=self.model
        
        btrk=list(btrk)
        if(btrk[3] == None): btrk[3]=-9999

        aidTau=0
        if(self.tauOffset):
            aidTau=self.tauOffset
            
        self.aidtrk={
            aidTau:btrk,        
        }
        
        self.aidtaus=self.targetTaus
        self.aidsource='mdeck2'
        self.aidname=self.model
        self.stmid=stmid

        self.aidMotion={
            aidTau:(btrk[4],btrk[5]),
        }

        # -- get the motion based on the next tau
        #
        ntaus=len(self.aidtaus)


        return(1)







class TcDiagAnl(TcDiag):


    def __init__(self,dtg,model,stmids=None,
                 tbdir=None,
                 wdir=None,
                 verb=0,
                 dols=0,
                 dobt=0,
                 dobail=1,
                 tD=None):


        if(tbdir == None):
            tbdir=w2.TcTcanalDatDir

        self.tbdir=tbdir
        self.tdir="%s/%s/%s"%(self.tbdir,dtg,model)


        self.dtg=dtg
        self.model=model
        self.umodel=model.upper()
        self.verb=verb
        self.dols=dols
        self.selectNN=1
        self.dobt=dobt
        self.tD=tD

        self.year=dtg[0:4]
        ddir="%s/nwp2/w2flds/dat"%(w2.W2BaseDirDat)
        webdir=w2.HfipWebBdir
        if(wdir == None):
            wdir="%s/tcdiagDAT"%(w2.HfipWebBdir)
            # use symbolic link
            wdir="%s/tcdiag"%(w2.HfipWebBdir)

        bdir=TcDiagDatDir

        dtgdir="%s/%s"%(self.year,dtg)
        pngdir="%s/%s"%(wdir,dtgdir)
        urldir="%s/%s"%(dtgdir,model)
        pltdir="%s/%s"%(wdir,urldir)
        datdir="%s/%s"%(bdir,urldir)
        adkdir="%s/%s/ADECKS"%(wdir,dtgdir)
        dgndir="%s/%s/DIAGFILES"%(wdir,dtgdir)

        webdiagdir=pltdir

        self.ddir=ddir
        self.wdir=wdir
        self.webdir=webdir
        self.pngdir=pngdir
        self.pltdir=pltdir
        self.urldir=urldir
        self.datdir=datdir
        self.webdiagdir=webdiagdir
        self.adeckOutdir=adkdir
        self.diagfileOutdir=dgndir

        if(stmids == None): self.initTC(dtg)
        else: self.stmids=stmids


        # -- initialize the m2 object first
        #
        self.rcM2=self.initM2(dtg,model)

        self.initOutput()



class TcFldsDiag(f77GridOutput,W2areas):

    def __init__(self,
                 dtg,
                 model,
                 ctlpath,
                 dstmids,
                 area=None,
                 ctlpath2=None,
                 dlon=None,dlat=None,
                 taus=None,
                 tauoffset=None,
                 tunits='hr',
                 vars=None,
                 doregrid=1,
                 tbdir=None,
                 doLogger=0,
                 Quiet=0,
                 verb=0,
                 doByTau=1,
                 setDxDyPrec=1,
                 dols=0,
                 diag=0,  
                 sstOnly=0,
                 tauData=None,
                 doSfc=1,
                 ):



        self.doSfc=doSfc
        self.m2=setModel2(model)
        if(model == 'era5'):
            if(doSfc):
                self.m2=setModel2(model)
            else:
                self.m2=setModel2('era5x')

        self.dstmids=dstmids
        self.doregrid=doregrid

        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.verb=verb
        self.doByTau=doByTau
        self.setDxDyPrec=setDxDyPrec

        self.diag=diag
        cP=ctlProps(ctlpath)

        if(dlon == None):
            dx=cP.dlon
        else:
            dx=dlon

        if(dlat == None):
            dy=cP.dlat
        else:
            dy=dlat

        self.tcB=TcBasin()

        if(area == None):
            self.setFldGridArea(dx=dx,dy=dy)
        else:
            self.area=area

        if(self.area == None): print "EEE error in getW2Area for area: ",area ; sys.exit()

        if(hasattr(area,'areaname')): self.areaname=area.areaname

        lonW=self.area.lonW
        lonE=self.area.lonE
        latS=self.area.latS
        latN=self.area.latN

        if(taus == None):
            self.btau=0
            self.etau=120
            self.dtau=6
            self.extaus=[132,144,156,168]
            taus=range(self.btau,self.etau+1,self.dtau)+self.extaus
            #taus=[0,6]

        else:
            self.btau=taus[0]
            self.etau=taus[-1]
            if(len(taus) > 1):
                self.dtau=taus[1]-taus[0]
            else:
                self.dtau=6

        if(tauoffset == None):
            tauoffset=0
            
        # -- adjust data taus by w2tauOffcset
        #
        otaus=[]
        for tau in taus:
            otau=tau+tauoffset
            otaus.append(otau)
            
        taus=otaus
        self.tunits=tunits
        self.taus=taus

        mdtg=mf.dtginc(dtg,-tauoffset)
        print 'DDDDDDDDDDDDDDDDDDDDDDddd',tauoffset,dtg,'model dtg',mdtg

        self.dtg=dtg
        self.mdtg=mdtg
        self.tauoffset=tauoffset
        
        self.model=model
        self.ctlpath=ctlpath
        self.ctlpath2=ctlpath2
        
        if(tbdir == None):
            print 'EEE in TCdiag.TcFldsDiag tbdir must be set with instantiation...'
            sys.exit()

        self.tbdir=tbdir
        
        self.year=self.dtg[0:4]
        self.tdirBase="%s/%s/%s"%(self.tbdir,self.year,self.dtg)
        self.tdir="%s/%s"%(self.tdirBase,self.model)

        if(not(sstOnly)):
            self.setCtl(ctlpath=ctlpath,tbdir=self.tbdir,dols=dols)
        else:
            self.status=1

        self.tdirsst="%s/oisst"%(self.tdirBase)
        MF.ChkDir(self.tdirsst,'mk')

        sstfile='oisst.%s.%s.dat'%(self.dtg,self.areaname)
        sstctlfile='oisst.%s.%s.ctl'%(self.dtg,self.areaname)
        self.sstdpath="%s/%s"%(self.tdirsst,sstfile)
        self.sstcpath="%s/%s"%(self.tdirsst,sstctlfile)

        if(sstOnly):  return  

        self.initVars()

        filename="%s.%s.%s"%(self.model,self.dtg,self.areaname)

        self.setOutput(filename=filename)

        self.ctlpathFldOutput=self.cpath

        sstfile='oisst.%s.%s.dat'%(self.dtg,self.areaname)
        self.sstdpath="%s/%s"%(self.tdirsst,sstfile)

        self.getDpaths(verb=verb)


    def initVars(self,
                 varSsfc=None,
                 varSua=None,
                 undef=-1e20):

        if(self.area == None): self.area=W2areaGlobal()

        if(varSsfc == None):

            # -- new field in var string parsed by WxMAP2.varProps, testvar-vartobemadeundef
            #    added hurs but not many models have this...ditto for tas
            self.varSsfc=['uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                          'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                          'tas:tas:(tas(t-TM1)*TFM1 + tas(t+TP1)*TFP1):0:-999:-999:tas [K]:None:tas', # add testvar and avail var to using in setting undef
                          '''hurs:hurs:(hurs(t-TM1)*TFM1 + hurs(t+TP1)*TFP1):0:-999:-999:hurs [%]:None:hurs''',

#                          'ts:ts:(ts(t-TM1)*TFM1 + ts(t+TP1)*TFP1):0:-999:-999:ts [K]:None:ts-uas',

'psl:(psl*1.00):(psl(t-TM1)*TFM1 + psl(t+TP1)*TFP1):0:-999:-999:psl [mb]',
'prw:(prw*1.00):(prw(t-TM1)*TFM1 + prw(t+TP1)*TFP1):0:-999:-999:prw [mm]',
'pr:getprvar:0:-999:-999:pr 6-h rate [mm/day]',
'vrt925:(hcurl(ua,va)*1e5):925:-999:-999:rel vort 925 [*1e5 /s]',
'vrt850:(hcurl(ua,va)*1e5):850:-999:-999:rel vort 850 [*1e5 /s]',
'vrt700:(hcurl(ua,va)*1e5):700:-999:-999:rel vort 700 [*1e5 /s]',
'zthklo:getexpr:0:-999:-999:600-900 thick [m]',
'zthkup:getexpr:0:-999:-999:300-600 thick [m]',
'z900:getexpr:0:-999:-999:900 [m]',
'z850:getexpr:0:-999:-999:850 [m]',
'z800:getexpr:0:-999:-999:800 [m]',
'z750:getexpr:0:-999:-999:750 [m]',
'z700:getexpr:0:-999:-999:700 [m]',
'z650:getexpr:0:-999:-999:650 [m]',
'z600:getexpr:0:-999:-999:600 [m]',
'z550:getexpr:0:-999:-999:550 [m]',
'z500:getexpr:0:-999:-999:500 [m]',
'z450:getexpr:0:-999:-999:450 [m]',
'z400:getexpr:0:-999:-999:400 [m]',
'z350:getexpr:0:-999:-999:350 [m]',
'z300:getexpr:0:-999:-999:300 [m]',
]

        if(varSua == None):

            self.varSua=[]

            self.varSuavar=['ua','va']
            self.varSl=[850,200]

            self.varSuavar=['ua','va','hur','ta','zg']
            self.varSl=[1000,850,700,500,400,300,250,200,150,100]
            self.varSzinterp={1000:0,850:0,700:0,500:0,400:0,300:0,250:0,200:0,150:0,100:0}
            # -- add 925
            self.varSl=[1000,925,850,700,500,400,300,250,200,150,100]
            self.varSzinterp={1000:0,925:1,850:0,700:0,500:0,400:0,300:0,250:0,200:0,150:0,100:0}

            self.varSu={
                'ua':('ua','ua [m/s]'),
                'va':('va','va [m/s]'),
                'hur':('hur','''hur [%]'''),
                'ta':('ta','ta [K]'),
                'zg':('zg','zg [m]'),
            }

            # -- special case for ecmt from tigge -- only have hus and different levels
            if(self.model == 'ecmt'):
                self.varSl=[1000,850,700,500,400,300,250,200]
                self.varSzinterp={1000:0,850:0,700:0,500:0,400:1,300:0,250:0,200:0}
                self.varSu['hur']=('((lev*hus/((0.622+hus)*esmrf(ta)))*100)','''hur [%]''')

            elif(self.model == 'cgd2'):
                self.varSuavar=['ua','va','hur','ta','zg']
                self.varSl=[1000,925,850,700,500,400,300,250,200]
                self.varSzinterp={1000:0,925:0,850:0,700:0,500:0,400:0,300:0,250:0,200:0}
                self.varSu['hur']=('((lev*hus/((0.622+hus)*esmrf(ta)))*100)','''hur [%]''')


                self.varSsfc=['uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                              'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                              'tas:tas:(tas(t-TM1)*TFM1 + tas(t+TP1)*TFP1):0:-999:-999:tas [K]:None:tas', # add testvar and avail var to using in setting undef
                              '''hurs:hurs:(hurs(t-TM1)*TFM1 + hurs(t+TP1)*TFP1):0:-999:-999:hurs [%]:None:hurs''',
                              'psl:(psl*0.01):(psl(t-TM1)*TFM1 + psl(t+TP1)*TFP1):0:-999:-999:psl [mb]',
                              'prw:(prw*1.0):(prw(t-TM1)*TFM1 + prw(t+TP1)*TFP1):0:-999:-999:prw [mm]',
                              'pr:getprvar:0:-999:-999:pr 6-h rate [mm/day]',
                              'vrt925:(hcurl(ua,va)*1e5):925:-999:-999:rel vort 925 [*1e5 /s]',
                              'vrt850:(hcurl(ua,va)*1e5):850:-999:-999:rel vort 850 [*1e5 /s]',
                              'vrt700:(hcurl(ua,va)*1e5):700:-999:-999:rel vort 700 [*1e5 /s]',
                              'zthklo:getexpr:0:-999:0.101972:600-900 thick [m]',
                              'zthkup:getexpr:0:-999:0.101972:300-600 thick [m]',
                              'z900:getexpr:0:-999:0.101972:900 [m]',
                              'z850:getexpr:0:-999:0.101972:850 [m]',
                              'z800:getexpr:0:-999:0.101972:800 [m]',
                              'z750:getexpr:0:-999:0.101972:750 [m]',
                              'z700:getexpr:0:-999:0.101972:700 [m]',
                              'z650:getexpr:0:-999:0.101972:650 [m]',
                              'z600:getexpr:0:-999:0.101972:600 [m]',
                              'z550:getexpr:0:-999:0.101972:550 [m]',
                              'z500:getexpr:0:-999:0.101972:500 [m]',
                              'z450:getexpr:0:-999:0.101972:450 [m]',
                              'z400:getexpr:0:-999:0.101972:400 [m]',
                              'z350:getexpr:0:-999:0.101972:350 [m]',
                              'z300:getexpr:0:-999:0.101972:300 [m]',
                              ]


            elif(self.model == 'ecm5' or self.model == 'era5'):
 
                self.varSuavar=['ua','va','hur','ta','zg']
                self.varSl=[1000,925,850,700,500,400,300,250,200]
                self.varSzinterp={1000:0,925:0,850:0,700:0,500:0,400:0,300:0,250:0,200:0}
                # -- named hur hura -- hmmm -- don't need because doing replace.pl to reset hura -> hur
                if(self.model == 'era5'):
                    self.varSu['hur']=('hura','''hur [%]''')

                # -- get mfact to convert from geopotential to geopotential meters
                zgfact=1.0/gravity
                czgfact="%7.6f"%(zgfact)
                czgfact='0.101972'

                self.varSu['zg']=('zg','zg [m]','-999',czgfact,'zg [m]')

                # -- special case for geopotential
                #
                if(self.model == 'era5'):
                    if(self.doSfc):
                        varSUVP=[
                            'uas:uas:(uas.2(t-TM1)*TFM1 + uas.2(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                            'vas:vas:(vas.2(t-TM1)*TFM1 + vas.2(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                            'psl:(psl*0.01):(psl.2(t-TM1)*TFM1 + psl.2(t+TP1)*TFP1):0:-999:-999:psl [mb]',
                            'pr:getprvar:0:-999:-999:pr 6-h rate [mm/day]',
                        ]
                    else:
                        varSUVP=[
                            'uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                            'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                            'psl:(psl*0.01):(psl(t-TM1)*TFM1 + psl(t+TP1)*TFP1):0:-999:-999:psl [mb]',
                            'pr:getprvar:0:-999:-999:pr 6-h rate [mm/day]',
                        ]
                        
                        
                    
                else:
                    varSUVP=[
                        'uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                        'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                        'tas:tas:(tas(t-TM1)*TFM1 + tas(t+TP1)*TFP1):0:-999:-999:tas [K]:None:tas', # add testvar and avail var to using in setting undef
                        '''hurs:hurs:(hurs(t-TM1)*TFM1 + hurs(t+TP1)*TFP1):0:-999:-999:hurs [%]:None:hurs''',
                        'psl:(psl*0.01):(psl(t-TM1)*TFM1 + psl(t+TP1)*TFP1):0:-999:-999:psl [mb]',
                        'pr:getprvar:0:-999:-999:pr 6-h rate [mm/day]',
                    ]
                    
                
                self.varSsfc=varSUVP + \
                [
                    'prw:(prw*1.0):(prw(t-TM1)*TFM1 + prw(t+TP1)*TFP1):0:-999:-999:prw [mm]',
                    'vrt925:(hcurl(ua,va)*1e5):925:-999:-999:rel vort 925 [*1e5 /s]',
                    'vrt850:(hcurl(ua,va)*1e5):850:-999:-999:rel vort 850 [*1e5 /s]',
                    'vrt700:(hcurl(ua,va)*1e5):700:-999:-999:rel vort 700 [*1e5 /s]',
                    'zthklo:getexpr:0:-999:0.101972:600-900 thick [m]',
                    'zthkup:getexpr:0:-999:0.101972:300-600 thick [m]',
                    'z900:getexpr:0:-999:0.101972:900 [m]',
                    'z850:getexpr:0:-999:0.101972:850 [m]',
                    'z800:getexpr:0:-999:0.101972:800 [m]',
                    'z750:getexpr:0:-999:0.101972:750 [m]',
                    'z700:getexpr:0:-999:0.101972:700 [m]',
                    'z650:getexpr:0:-999:0.101972:650 [m]',
                    'z600:getexpr:0:-999:0.101972:600 [m]',
                    'z550:getexpr:0:-999:0.101972:550 [m]',
                    'z500:getexpr:0:-999:0.101972:500 [m]',
                    'z450:getexpr:0:-999:0.101972:450 [m]',
                    'z400:getexpr:0:-999:0.101972:400 [m]',
                    'z350:getexpr:0:-999:0.101972:350 [m]',
                    'z300:getexpr:0:-999:0.101972:300 [m]',
                ]
                


            for var in self.varSuavar:
                ovar=var
                for lev in self.varSl:
                    vafact='-999'
                    vmfact='-999'
                    if(len(self.varSu[var]) >= 4):
                        vafact=self.varSu[var][2]
                        vmfact=self.varSu[var][3]
                    expr=self.varSu[var][0]
                    desc=self.varSu[var][1]

                    if(expr == 'hura' and var == 'hur'): ovar=expr
                    vlev=lev
                    vlev=str(lev)
                    if(self.varSzinterp[lev] == 1):
                        vlev='Z'+str(vlev)

                    # -- special case for ecmn -- no 200 mb, so set to 250
                    #
                    if(self.model == 'ecmn' and lev == 200): vlev=250
                    vtexpr="(%s(t-TM1)*TFM1 + %s(t+TP1)*TFP1)"%(ovar,ovar)
                    vvvv='%s:%s:%s:%s:%s:%s:%s'%(var,expr,vtexpr,vlev,vafact,vmfact,desc)
                    self.varSua.append('%s:%s:%s:%s:%s:%s:%s'%(var,expr,vtexpr,vlev,vafact,vmfact,desc))

        self.dpaths={}
        self.vars=[]

        for var in self.varSsfc:
            self.vars.append(var)

        for var in self.varSua:
            self.vars.append(var)


        self.undef=undef

        if(self.taus == None):
            self.btau=0
            self.etau=120
            self.dtau=6
            self.tunits='hr'
            self.taus=range(self.btau,self.etau+1,self.dtau)

        aa=self.area

        cdx="%f"%(aa.dx)
        cdy="%f"%(aa.dy)
        if(self.setDxDyPrec):
            cdx="%7.3f"%(aa.dx)
            cdy="%7.3f"%(aa.dy)


        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%s,%d,%s,%f,%s"%(aa.ni,self.rexopt,aa.lonW,cdx,aa.nj,self.reyopt,aa.latS,cdy)
        else:
            self.reargs="%d,%s,%f,%s,%d,%s,%f,%s,%s"%(aa.ni,self.rexopt,aa.lonW,cdx,aa.nj,self.reyopt,aa.latS,cdy,self.remethod)

        if(not(self.doregrid)): self.reargs=None

    def makeOisst(self,override=0):

        if(not(hasattr(self,'ga')) or not(hasattr(self,'ge')) or not(hasattr(self,'dtg')) ):
            print 'EEE makeOisst, need to run makeFldInput first...'
            sys.exit()

        self.ga.oisstOpened=0

        # -- instantiate the ssT object for follow on apps
        #

        MF.sTimer(tag='sst')
        ssT=Oisst(self.ga,self.ge,self.dtg,verb=self.verb,area=self.area,dpath=self.sstdpath,reargs=self.reargs,override=override)
        MF.dTimer(tag='sst')

        self.ssT=ssT

        # -- the first file open is the met fields, make it the default
        #
        self.ga('set dfile 1')
        self.ga('set z 1')

        if(MF.ChkPath(self.sstdpath,verb=1) and not(override)): return

    def makeEra5sst(self,override=0):

        if(not(hasattr(self,'ga')) or not(hasattr(self,'ge')) or not(hasattr(self,'dtg')) ):
            print 'EEE makeOisst, need to run makeFldInput first...'
            sys.exit()

        self.ga.oisstOpened=0

        # -- instantiate the ssT object for follow on apps
        #

        MF.sTimer(tag='era5-sst')
        ssT=Era5sst(self.ga,self.ge,self.dtg,ctlpath2=self.ctlpath2,
                    verb=self.verb,area=self.area,dpath=self.sstdpath,reargs=self.reargs,override=override)
        MF.dTimer(tag='era5-sst')

        self.ssT=ssT

        # -- the first file open is the met fields, make it the default
        #
        self.ga('set dfile 1')
        self.ga('set z 1')

        if(MF.ChkPath(self.sstdpath,verb=1) and not(override)): return

    def makeEcm5sst(self,override=0):

        if(not(hasattr(self,'ga')) or not(hasattr(self,'ge')) or not(hasattr(self,'dtg')) ):
            print 'EEE makeEcm5sst, need to run makeFldInput first...'
            sys.exit()

        self.ga.oisstOpened=0

        # -- instantiate the ssT object for follow on apps
        #

        MF.sTimer(tag='ecm5-sst')
        ssT=Ecm5sst(self.ga,self.ge,self.dtg,ctlpath2=None,
                    verb=self.verb,area=self.area,dpath=self.sstdpath,reargs=self.reargs,override=override)
        MF.dTimer(tag='ecm5-sst')

        self.ssT=ssT

        # -- the first file open is the met fields, make it the default
        #
        self.ga('set dfile 1')
        self.ga('set z 1')

        if(MF.ChkPath(self.sstdpath,verb=1) and not(override)): return


    def setFldGridArea(self,ropt='',dx=None,dy=None,override=0):

        self.hemigrid=getHemis(self.dstmids)

        if(self.hemigrid == None):
            print '''EEE TcFldsDiag.setFldGridArea no storms! sayoonara'''
            sys.exit()

        if(self.hemigrid == 'nhem'):  aa=LsdiagAreaNhem(dx=dx,dy=dy)
        if(self.hemigrid == 'shem'):  aa=LsdiagAreaShem(dx=dx,dy=dy)
        if(self.hemigrid == 'global'):  aa=LsdiagAreaGlobal(dx=dx,dy=dy)

        self.areaname=self.hemigrid

        self.area=aa

        # override to test with more general code
        #
        #self.area=W2areaGlobal()

        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None


    def makeFldInputGA(self,gaP):

        # -- decorate the GaProc (gaP) object
        #

        if(gaP.ga == None):
            print 'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM -- making gaP.ga -- makeFldInputGA'
            gaP.initGA()


        self.ga                      =gaP.ga
        self.ga2                     =gaP.ga

        # -- do file open via ge so getFileMeta works...
        print 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO -- open: ',self.ctlpath
        self.ga.ge.fh                =self.ga.open(self.ctlpath)
        #print 'gggg111111',self.ga.ge.fh
        
        self.ga.ge.getFileMeta()
        self.ge                      =self.ga.ge
        gaP.ge                       =self.ga.ge

        if(self.ctlpath2 != None): 
            print 'OOOOOOOOOOOOOOOOOOOOOO22222222222222 -- open: ',self.ctlpath2
            self.ga.ge.fh=self.ga.open(self.ctlpath2)
            #print 'gggg222222',self.ga.ge.fh

        return(gaP)


    def reinitGA(self,gaP):
        gaP.ge.reinit()


    def destructGA(self):
        if(hasattr(self,'ga')):
            print 'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ ga'
            self.ga('quit')

        if(hasattr(self,'ga2')):
            print 'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ ga2'
            self.ga2('quit')


    def thinDpathsByTaus(self,verb=0,ropt=''):

        thinTaus=range(6,126+1,12)

        for thintau in thinTaus:
            if(thintau in self.taus):
                (rc,path)=self.dpaths[thintau]
                cmd="rm %s"%(path)
                mf.runcmd(cmd,ropt)


    def cleanDpaths(self,verb=0,ropt=''):

        # -- oisst
        #
        MF.sTimer('clean-oisst')
        sstpath=self.sstdpath
        if(MF.ChkPath(sstpath)):
            cmd="rm %s"%(sstpath)
            mf.runcmd(cmd,ropt)
            
        MF.dTimer('clean-oisst')

        # -- meteo fields
        #
        for tau in self.taus:
            try:
                (rc,path)=self.dpaths[tau]
            except:
                print 'WWW -- TcFldsDiag.cleanDpaths() -- no dpaths...press...'
                return
            if(MF.ChkPath(path)):
                cmd="rm %s"%(path)
                mf.runcmd(cmd,ropt)



class Oisst(DataSet,f77GridOutput):

    ddir="%s/ocean/oisst"%(w2.W2BaseDirDat)

    sstctl="%s/oiv2.ctl"%(ddir)
    sstcctl="%s/aoiclim.71_00.daily.ctl"%(ddir)


    def __init__(self,ga,ge,dtg,
                 area=None,
                 reargs=None,
                 dpath=None,
                 undef=1e20,
                 override=0,
                 verb=0):

        self.dtg=dtg
        self.ga=ga
        self.ge=ge
        self.verb=verb
        self.undef=undef
        self.taus=[0]
        self.dtau=6
        self.tunits='hr'

        self.area=area
        self.reargs=reargs
        self.dpath=dpath

        if(MF.ChkPath(self.dpath) and override == 0):
            print 'III Oisst.dpath exists, NOT making dpath: ',self.dpath
            return

        if(ga.oisstOpened == 0):
            ga.fh=ga.open(self.sstctl)
            ga.fh=ga.open(self.sstcctl)
            ga.oisstOpened=1


        if(area != None):

            cmd="""set lat %f %s
            set lon %f %f"""%(area.latS,area.latN,area.lonW,area.lonE)
            ga(cmd)


        ga('set dfile 2')
        ga('set z 1')

        ge.setTimebyDtgTau(dtg,tau=0,verb=1)

        var='sst'
        varall='sstall'
        (t0,fact0,t1,fact1)=self.getTrangeInterpfacts(var,dtg)

        sstexpr="(%s.2(t=%d)*%f + %s.2(t=%d)*%f)"%(var,t0,fact0,var,t1,fact1)
        sstexprall="(%s.2(t=%d)*%f + %s.2(t=%d)*%f)"%(var,t0,fact0,var,t1,fact1)
        sstdefine="%s=(%s-273.15)*const(%sc.3,1)"%(var,sstexpr,var)
        sstdefineall="%s=(%s-273.15)"%(varall,sstexprall)
        sstanom="%sa=%s-%sc.3"%(var,var,var)

        if(verb):

            print '       t0: ',t0
            print '    fact0: ',fact0
            print '       t1: ',t1
            print '    fact1: ',fact1

            print '   sstctl: ',self.sstctl
            print '  sstcctl: ',self.sstcctl
            print 'sstdefine: ',sstdefine
            print 'sstdefine: ',sstdefineall
            print '  sstanom: ',sstanom

        # -- define before sst because uses sst in the the sstexpr
        ga('%s'%(sstdefine))
        ga('%s'%(sstanom))
        ga('%s'%(sstdefineall))

        self.vars=[
            ('sst','sst with mask [K]'),
            ('sstall','sst filled in mask [K]'),
            ('ssta','sst anom [C]'),
        ]

        if(self.dpath != None):
            ga.ge.setFwrite(name=self.dpath)
            ga('set gxout fwrite')
            ga.dvar.dregrid0('sst','sst',self.reargs)
            ga.dvar.dregrid0('sstall','sstall',self.reargs)
            ga.dvar.dregrid0('ssta','ssta',self.reargs)
            ga('disable fwrite')

            self.makeCtlfile()


    def makeCtlfile(self):

        aa=self.area
        gtime=mf.dtg2gtime(self.dtg)

        (ddir,dfile)=os.path.split(self.dpath)
        cfile=dfile.replace('.dat','.ctl')
        self.ctlpathSstOutput="%s/%s"%(ddir,cfile)

        self.ctl="""dset ^%s
title test
undef %g
* template not needed
options sequential 
xdef %3d linear %7.2f %7.2f
ydef %3d linear %7.2f %7.2f"""%(dfile,self.undef,
                                aa.ni,aa.lonW,aa.dx,
                                aa.nj,aa.latS,aa.dy)


        self.makeCtlZdef()

        self.ctl=self.ctl+"""
%s
tdef %d linear %s %d%s"""%(
                             self.zdef,len(self.taus),gtime,self.dtau,self.tunits,
                         )

        self.makeCtlVars()

        MF.WriteString2File(self.ctl,self.ctlpathSstOutput,verb=1)

    def makeCtlVars(self):

        self.ctl=self.ctl+"""
vars %d"""%(
              len(self.vars),
          )

        for (var,vdesc) in self.vars:
            card="%-10s 0 0 %s"%(var,vdesc)
            self.ctl="""%s
%s"""%(self.ctl,card)


        self.ctl="""%s
endvars"""%(self.ctl)

    # -- 20221217 -- increase to 120 h...not updating in
    #https://ftp.cpc.ncep.noaa.gov/precip/PORT/sst/oisst_v2/GRIB/
    #
    def getTrangeInterpfacts(self,expr,dtg,gdt1Max=240.0):


        def getgdtstats(t):

            self.ga("set t %d"%(t))
            self.ga('q time')
            gtime=self.ga.rword(1,3)
            gdtg=mf.gtime2dtg(gtime)
            gdt=mf.dtgdiff(gdtg,dtg)

            stats=self.ga.getExprStats(expr)

            return(gdtg,gdt,stats)


        qh=self.ga.coords()
        t1=qh.denv.t[0]

        (gdtg1,gdt1,stats1)=getgdtstats(t1)
        nvalid1=stats1.nvalid

        # -- 20190306 -- gdt1Max is how far forward in time to go (h) when dtg not in dtgrange of one week
        #
        print 'dddd',gdt1,gdt1Max
        if(gdt1 >= gdt1Max):
            t1=t1+1
            (gdtg1,gdt1,stats1)=getgdtstats(t1)
            nvalid1=stats1.nvalid

        t0=t1-1
        (gdtg0,gdt0,stats0)=getgdtstats(t0)
        nvalid0=stats0.nvalid

        datadt=gdt0-gdt1

        fact0=abs(gdt0)/datadt
        fact1=abs(gdt1)/datadt

        # -- case when no data at forward time point but data on back point, extrap by holding constant
        #
        if(nvalid1 == 0 and nvalid0 > 0):
            t1=t0
            fact0=1.0
            fact1=0.0
            print 'WWW--Oisst.getTrangeInterpfacts--going beyond 7 d...use last and latest...'

        elif(nvalid1 == 0 and nvalid0 == 0):
            if(self.verb): print 'WWW -- no data in t range: ',t0,' to ',t1,' hold latest value (t0-1) for one week at most'
            t0=t0-1
            t1=t0
            fact0=fact1=0.5
            (gdtg1,gdt1,stats1)=getgdtstats(t1)
            if(self.verb): print 'CCC -- nvalid1: ',stats1.nvalid
            if(stats1.nvalid == 0):
                print 'EEE sayoonara, we have a problem houston...in TCdiag.Oisst the input dtg is too far forward in time to hold latest...'
                sys.exit()

        return(t0,fact0,t1,fact1)


class Era5sst(DataSet,f77GridOutput):

    ddir="%s/ocean/era5"%(w2.W2BaseDirDat)
    ddirO="%s/ocean/oisst"%(w2.W2BaseDirDat)

    sstctl="%s/sst.ctl"%(ddir)
    sstcctl="%s/aoiclim.71_00.daily.ctl"%(ddirO)


    def __init__(self,ga,ge,dtg,
                 ctlpath2=None,
                 area=None,
                 reargs=None,
                 dpath=None,
                 undef=1e20,
                 override=0,
                 verb=0):

        self.dtg=dtg
        self.ctlpath2=ctlpath2
        self.ga=ga
        self.ge=ge
        self.verb=verb
        self.undef=undef
        self.taus=[0]
        self.dtau=6
        self.tunits='hr'

        self.area=area
        self.reargs=reargs
        self.dpath=dpath

        if(MF.ChkPath(self.dpath) and override == 0):
            print 'III Oisst.dpath exists, NOT making dpath: ',self.dpath
            return

        if(ga.oisstOpened == 0):
            ga.fh=ga.open(self.sstctl)
            ga.fh=ga.open(self.sstcctl)
            ga.oisstOpened=1


        if(area != None):

            cmd="""set lat %f %s
            set lon %f %f"""%(area.latS,area.latN,area.lonW,area.lonE)
            ga(cmd)


        if(self.ctlpath2 != None):
            nSST=3
            nSSTclim=4
        else:
            nSST=2
            nSSTclim=3
        ga('set dfile %d'%(nSST))
        ga('set z 1')

        ge.setTimebyDtgTau(dtg,tau=0,verb=1)

        var='sst'
        varall='sstall'

        #ydef 180 linear -89.500000 1
        #xdef 360 linear 0.500000 1.000000

        nxre=360
        nyre=180
        dlat=1.0
        dlon=1.0
        
        sstexpr="(re(%s,%d,linear,0.5,%f,%d,linear,-89.5,%f))"%(var,nxre,dlon,nyre,dlat)
        sstdefine="%s=(%s-273.15)*const(%sc.%d,1)"%(var,sstexpr,var,nSST)
        sstdefine="%s=(%s-273.15)"%(var,sstexpr)
        sstdefineA="%sall=const(%s,0,-u)"%(var,var)
        sstanom="%sa=%s-%sc.%d"%(var,var,var,nSSTclim)

        if(verb):

            print '   sstctl: ',self.sstctl
            print '  sstcctl: ',self.sstcctl
            print 'sstdefine: ',sstdefine
            print '  sstanom: ',sstanom

        # -- define before sst because uses sst in the the sstexpr
        #
        ga('%s'%(sstdefine))
        ga('%s'%(sstdefineA))
        ga('set dfile %d'%(nSSTclim))
        ga('%s'%(sstanom))
        ga('set dfile %d'%(nSST))

        self.vars=[
            ('sst','sst with mask [K]'),
            ('sstall','sst with const 0 land points [K]'),
            ('ssta','sst anom [C]'),
        ]

        if(self.dpath != None):
            ga.ge.setFwrite(name=self.dpath)
            ga('set gxout fwrite')
            ga.dvar.dregrid0('sst','sst',self.reargs)
            ga.dvar.dregrid0('sstall','sstall',self.reargs)
            ga.dvar.dregrid0('ssta','ssta',self.reargs)
            ga('disable fwrite')

            self.makeCtlfile()


    def makeCtlfile(self):

        aa=self.area
        gtime=mf.dtg2gtime(self.dtg)

        (ddir,dfile)=os.path.split(self.dpath)
        cfile=dfile.replace('.dat','.ctl')
        self.ctlpathSstOutput="%s/%s"%(ddir,cfile)

        self.ctl="""dset ^%s
title test
undef %g
* template not needed
options sequential 
xdef %3d linear %7.2f %7.2f
ydef %3d linear %7.2f %7.2f"""%(dfile,self.undef,
                                aa.ni,aa.lonW,aa.dx,
                                aa.nj,aa.latS,aa.dy)


        self.makeCtlZdef()

        self.ctl=self.ctl+"""
%s
tdef %d linear %s %d%s"""%(
                             self.zdef,len(self.taus),gtime,self.dtau,self.tunits,
                         )

        self.makeCtlVars()

        MF.WriteString2File(self.ctl,self.ctlpathSstOutput,verb=1)

    def makeCtlVars(self):

        self.ctl=self.ctl+"""
vars %d"""%(
              len(self.vars),
          )

        for (var,vdesc) in self.vars:
            card="%-10s 0 0 %s"%(var,vdesc)
            self.ctl="""%s
%s"""%(self.ctl,card)


        self.ctl="""%s
endvars"""%(self.ctl)


class Ecm5sst(DataSet,f77GridOutput):

    ddirO="%s/ocean/oisst"%(w2.W2BaseDirDat)
    sstcctl="%s/aoiclim.71_00.daily.ctl"%(ddirO)


    def __init__(self,ga,ge,dtg,
                 ctlpath2=None,
                 area=None,
                 reargs=None,
                 dpath=None,
                 undef=1e20,
                 override=0,
                 model='ecm5',
                 pcntLand=0.1,
                 verb=0):
        
        m2=M2.setModel2(model)
        dmodelType='w2flds'
        # -- for models before ecm5 have to use previous run
        dtgE=dtg
        if(w2.is0618Z(dtgE)): 
            dtgE=mf.dtginc(dtg,-18)
        else:
            dtgE=mf.dtginc(dtg,-12)
            
        dtgE12=mf.dtginc(dtgE,-12)
        dtgE24=mf.dtginc(dtgE,-24)
            
        fm=m2.DataPath(dtgE,dtype=dmodelType,dowgribinv=1,override=override,diag=1)
        fd=fm.GetDataStatus(dtgE)
        
        # -- cur12-12 file late or not there...got back 12 h
        #
        if(len(fd.statuss[dtgE]) == 0):
            
            # -- tau-12
            #
            fm=m2.DataPath(dtgE12,dtype=dmodelType,dowgribinv=1,override=override,diag=1)
            fd=fm.GetDataStatus(dtgE12)

            if(len(fd.statuss[dtgE12]) == 0):
                
                # -- tau-24
                #
                fm=m2.DataPath(dtgE24,dtype=dmodelType,dowgribinv=1,override=override,diag=1)
                fd=fm.GetDataStatus(dtgE24)

                if(len(fd.statuss[dtgE24]) == 0):
                    print 'EEEEEEE in Ecm5sst -- no data for dtgE: ',dtgE,' or ',dtgE12,' or ',dtgE24,' sayounara...'
                    sys.exit()
                else:
                    print 'III--Ecm5sst: got data for dtgE24: ',dtgE24
            else:
                print 'III--Ecm5sst: got data for dtgE12: ',dtgE12

        else:
            print 'III--Ecm5sst: got data for dtgE: ',dtgE
        
        self.sstctl=m2.dpath
        self.dtg=dtg
        self.ctlpath2=ctlpath2
        self.ga=ga
        self.ge=ge
        self.verb=verb
        self.undef=undef
        self.taus=[0]
        self.dtau=6
        self.tunits='hr'

        self.area=area
        self.reargs=reargs
        self.dpath=dpath

        if(MF.ChkPath(self.dpath) and override == 0):
            print 'III Oisst.dpath exists, NOT making dpath: ',self.dpath
            return

        if(ga.oisstOpened == 0):
            ga.fh=ga.open(self.sstctl)
            ga.fh=ga.open(self.sstcctl)
            ga.oisstOpened=1


        if(area != None):

            cmd="""set lat %f %s
            set lon %f %f"""%(area.latS,area.latN,area.lonW,area.lonE)
            ga(cmd)


        if(self.ctlpath2 != None):
            nSST=3
            nSSTclim=4
        else:
            nSST=2
            nSSTclim=3
        
        ga('set dfile %d'%(nSST))
        ga('set z 1')

        ge.setTimebyDtgTau(dtg,tau=0,verb=1)

        var='sst'
        varE='maskout(ave(sst.%d,t=1,t=12),%f-ls.%d(t=1))'%(nSST,pcntLand,nSST)
        varall='sstall'

        #ydef 180 linear -89.500000 1
        #xdef 360 linear 0.500000 1.000000

        nxre=360
        nyre=180
        dlat=1.0
        dlon=1.0
        
        sstexpr="(re(%s,%d,linear,0.5,%f,%d,linear,-89.5,%f))"%(varE,nxre,dlon,nyre,dlat)
        sstdefine="%s=(%s-273.15)*const(%sc.%d,1)"%(var,sstexpr,var,nSST)
        sstdefine="%s=(%s-273.15)"%(var,sstexpr)
        sstdefineA="%sall=const(%s,0,-u)"%(var,var)
        sstanom="%sa=%s-%sc.%d"%(var,var,var,nSSTclim)

        if(verb):

            print '   sstctl: ',self.sstctl
            print '  sstcctl: ',self.sstcctl
            print 'sstdefine: ',sstdefine
            print '  sstanom: ',sstanom

        # -- define before sst because uses sst in the the sstexpr
        #
        ga('%s'%(sstdefine))
        ga('%s'%(sstdefineA))
        ga('set dfile %d'%(nSSTclim))
        ga('%s'%(sstanom))
        ga('set dfile %d'%(nSST))

        self.vars=[
            ('sst','sst with mask [K]'),
            ('sstall','sst with const 0 land points [K]'),
            ('ssta','sst anom [C]'),
        ]

        if(self.dpath != None):
            ga.ge.setFwrite(name=self.dpath)
            ga('set gxout fwrite')
            ga.dvar.dregrid0('sst','sst',self.reargs)
            ga.dvar.dregrid0('sstall','sstall',self.reargs)
            ga.dvar.dregrid0('ssta','ssta',self.reargs)
            ga('disable fwrite')

            self.makeCtlfile()


    def makeCtlfile(self):

        aa=self.area
        gtime=mf.dtg2gtime(self.dtg)

        (ddir,dfile)=os.path.split(self.dpath)
        cfile=dfile.replace('.dat','.ctl')
        self.ctlpathSstOutput="%s/%s"%(ddir,cfile)

        self.ctl="""dset ^%s
title test
undef %g
* template not needed
options sequential 
xdef %3d linear %7.2f %7.2f
ydef %3d linear %7.2f %7.2f"""%(dfile,self.undef,
                                aa.ni,aa.lonW,aa.dx,
                                aa.nj,aa.latS,aa.dy)


        self.makeCtlZdef()

        self.ctl=self.ctl+"""
%s
tdef %d linear %s %d%s"""%(
                             self.zdef,len(self.taus),gtime,self.dtau,self.tunits,
                         )

        self.makeCtlVars()

        MF.WriteString2File(self.ctl,self.ctlpathSstOutput,verb=1)

    def makeCtlVars(self):

        self.ctl=self.ctl+"""
vars %d"""%(
              len(self.vars),
          )

        for (var,vdesc) in self.vars:
            card="%-10s 0 0 %s"%(var,vdesc)
            self.ctl="""%s
%s"""%(self.ctl,card)


        self.ctl="""%s
endvars"""%(self.ctl)




class TcdiagGA(TcDiag):

    def __init__(self,
                 gaQuiet=1,
                 gaWindow=0,
                 gadoLogger=0,
                 gaOpts='',
                 xsize=1200,
                 ):


        # --set put gaP objects...
        """

"""
        self.xsize=xsize
        aspect=w2.W2plotAspect
        self.ysize=int(self.xsize*aspect) 

        self.gaopt='-g 20+20+%dx%d'%(self.xsize,self.ysize)
        self.gaopt=''
        self.gaQuiet=gaQuiet
        self.gaWindow=gaWindow
        self.gadoLogger=gadoLogger
        self.gaOpts=gaOpts


        self.gaP=GaProc(
            Quiet=self.gaQuiet,
            Window=self.gaWindow,
            Opts=self.gaOpts,
            doLogger=self.gadoLogger,
        )




class TcDiagData(MFbase):


    def __init__(self,tG=None,verb=0):


        self.verb=verb

        self.rctG=1
        if(not(hasattr(tG,'year'))):
            self.rctG=0
            return

        self.year=tG.year
        self.dtg=tG.dtg
        self.model=tG.model.lower()
        self.umodel=tG.model.upper()

        self.taus=tG.taus
        # -- check if taus reduced because of going to far poleward
        #
        if(hasattr(tG,'stmTaus') and (len(self.taus) > len(tG.stmTaus)) ):
            self.taus=tG.stmTaus

        self.stmid=tG.stmid.lower()
        self.basename=tG.basename
        self.diagpath=tG.diagpath
        if(hasattr(tG,'aidtrk')): self.aidtrk=tG.aidtrk
        if(hasattr(tG,'aidtaus')): self.aidtaus=tG.aidtaus
        if(hasattr(tG,'aidstruct')): self.aidstruct=tG.aidstruct
        if(hasattr(tG,'diagpathWebALL')): self.diagpathWebALL=tG.diagpathWebALL


        self.pyppathData=tG.pyppathData
        self.pyppathHtml=tG.pyppathHtml
        self.pyppath=self.pyppathData

        self.targetTaus=tG.targetTaus

        self.customData=tG.customData
        self.clevels=tG.clevels

        self.stmData=tG.stmData
        self.sndData=tG.sndData
        self.sndKeys=tG.sndKeys

        self.diagKeys=tG.diagKeys
        self.diagFilenames=tG.diagFilenames
        self.diagVals=tG.diagVals
        self.diagTypes=tG.diagTypes
        self.diaguRls=tG.diaguRls
        self.urlData=tG.urlData

        if(hasattr(tG,'trkploturl')):
            self.trkploturl=tG.trkploturl



    def makeDiagFile(self):


        def cleankey(key):
            key=key.lower()
            key=key.strip()
            key=key.replace(' ','')
            key=key.replace('(hr)','')
            key=key.replace('(c)','')
            key=key.replace('(kt)','')
            key=key.replace('(10kt)','')
            key=key.replace('(10c)','')
            key=key.replace('(10c)','')
            key=key.replace('(%)','')
            key=key.replace('(deg)','')
            key=key.replace('(dm)','')
            key=key.replace('(kj/cm2)','')
            key=key.replace('(10m/s)','')
            key=key.replace('(/s)','')
            key=key.replace('(mm)','')
            key=key.replace('(mb)','')
            key=key.replace('(km)','')
            key=key.replace('(10mm/d)','')
            return(key)

        def printtaus():

            # -- print taus
            #
            card= "%s  "%(stmkeys[0].upper()[3:])
            for tau in self.taus:
                card=card+"%s "%(self.stmData[tau][stmkeys[0]])
            cards.append(card)


        if(not(hasattr(self,'tD'))): self.tD=TcData(stmopt=self.stmid)

        (smt3id,stmname)=self.tD.getStmName3id(self.stmid)        

        cards=[]
        stm2id=stm1idTostm2id(self.stmid).split('.')[0]

        # -- use adeck name if there
        aidname=self.model
        if(hasattr(self,'aidname')): aidname=self.aidname

        card="     *   %-6s   %10s    *"%(aidname,self.dtg)
        cards.append(card.upper())
        card="     *   %-6s   %10s    *"%(stm2id,stmname)
        cards.append(card.upper())

        card="\n     ---------------------------------------- storm data ----------------------------------------\n".upper()
        cards.append(card)
        card="ntimes %03d"%(len(self.taus))
        card=card.upper()
        cards.append(card)

        stmkeys=self.stmData[self.taus[0]].keys()
        stmkeys.sort()
        for stmkey in stmkeys:
            cstmkey=stmkey.upper()[3:]
            card= "%s  "%(cstmkey)

            for tau in self.taus:

                if(tau == self.taus[0] or len(self.taus) == 1):
                    if(not(cstmkey in self.diagKeys)):
                        self.diagKeys.append(cstmkey)
                    self.diagFilenames[cstmkey]="%s.%s"%(cleankey(cstmkey),self.stmid)

                cdata=self.stmData[tau][stmkey]
                card=card+"%s "%(cdata)
                self.diagVals[tau][cstmkey]=cdata
                self.diagTypes[tau][cstmkey]='storm'
                try:
                    self.diaguRls[tau][cstmkey]=self.urlData[tau][stmkey]
                except:
                    self.diaguRls[tau][cstmkey]='None'

            cards.append(card)

        card="\n     ---------------------------------------- custom data ----------------------------------------".upper()
        cards.append(card)

        customkeys=self.customData[self.taus[0]].keys()
        customkeys.sort()

        card="nvar %03d"%(len(customkeys))
        card=card.upper()
        cards.append(card)

        rc=printtaus()

        for customkey in customkeys:
            ctmkey=customkey.upper()[3:]
            card= "%s  "%(ctmkey)
            for tau in self.taus:

                if(tau == self.taus[0] or len(self.taus) == 1):
                    if(not(ctmkey in self.diagKeys)):
                        self.diagKeys.append(ctmkey)
                    self.diagFilenames[ctmkey]="%s.%s"%(cleankey(ctmkey),self.stmid)

                cdata=self.customData[tau][customkey]
                self.diagVals[tau][ctmkey]=cdata
                self.diagTypes[tau][ctmkey]='custom'

                try:
                    self.diaguRls[tau][ctmkey]=self.urlData[tau][customkey]
                except:
                    self.diaguRls[tau][ctmkey]='None'


                card=card+"%s "%(cdata)
            cards.append(card)

        card="\n     ---------------------------------------- sounding data ----------------------------------------\n".upper()
        cards.append(card)


        card=self.clevels
        cards.append(card)

        # -- print taus
        #
        card= "%s  "%(stmkeys[0].upper()[3:])
        for tau in self.taus:
            cdata=self.stmData[tau][stmkeys[0]]
            card=card+"%s "%(cdata)
        cards.append(card)

        sndkeys=self.sndKeys
        for sndkey in sndkeys:
            csndkey=sndkey.upper()
            card= "%s  "%(csndkey)

            for tau in self.taus:

                cdata=self.sndData[tau][sndkey]
                self.diagVals[tau][csndkey]=cdata
                self.diagTypes[tau][csndkey]='sounding'

                try:
                    self.diaguRls[tau][csndkey]=self.urlData[tau][sndkey]
                except:
                    self.diaguRls[tau][csndkey]='None'

                if(tau == self.taus[0] or len(self.taus) == 1 ):

                    if(not(csndkey in self.diagKeys)):
                        self.diagKeys.append(csndkey)

                    #if(self.diaguRls[tau][csndkey] != 'None'):
                    #    self.diagFilenames[csndkey]="%s.%s"%(cleankey(csndkey),self.stmid)
                    #else:
                    #    self.diagFilenames[csndkey]='None'

                    self.diagFilenames[csndkey]="%s.%s"%(cleankey(csndkey),self.stmid)

                card=card+"%s "%(cdata)
            cards.append(card)


        if(self.verb):
            print
            for card in cards:
                print card


        MF.WriteList2File(cards,self.diagpath,verb=1)
        if(hasattr(self,'diagpathWebALL')):
            MF.WriteList2File(cards,self.diagpathWebALL,verb=1)

    def doPyp(self,verb=0):

        del self.tD
        try: del self.tGtrk
        except: None
        if(verb or self.verb): print 'III writing html pyp: ',self.pyppathHtml
        self.putPyp(pyppath=self.pyppathHtml,verb=verb)


class TcTrkPlot(DataSet):
    """plot tc trk
    """

    def __init__(self,tG,stmid,zoomfact=None,verb=1,otau=48,override=0,
                 doveribt=1,
                 dobt=0,
                 Quiet=1,
                 Bin='grads',
                 ctlpath=None):

        self.year=tG.year
        self.dtg=tG.dtg
        self.model=tG.model
        self.pltdir=tG.pltdir
        self.doveribt=doveribt
        self.dobt=dobt
        self.ctlpath=ctlpath
        self.btcs=tG.btcs
        self.inputAD=tG.aD
        self.pngmethod=tG.printMethod

        self.stmid=stmid
        self.verb=verb
        self.aidtrk=tG.aidtrk
        self.aidtaus=tG.aidtaus
        self.zoomfact=zoomfact
        self.otau=otau
        self.Bin=Bin

        self.pltfile="trkplt.%s.%s.png"%(self.stmid,self.model)
        self.pltpath="%s/%s"%(self.pltdir,self.pltfile)

        self.trkplotpath=self.pltpath
        self.trkploturl="../../../%s/%s/%s/%s"%(self.year,self.dtg,self.model,self.pltfile)

        doplot=0
        if(not(MF.ChkPath(self.pltpath)) or override): doplot=1

        if(not(doplot)):
            print 'WWW.TcTrkPlot.doplot: ',doplot,' override: ',override
            return

        if(not(override) and MF.ChkPath(self.trkplotpath)):
            print 'III trkplotpath: ',self.trkplotpath,' already there and override=0...'
            return

        # -- make separate ga object for tracker and put on tG -- irrespective of override... 
        # -- if you got to this point, you want to make the plot
        #
        #if((not(hasattr(tG,'ga2')) and not(override)) or override):
        if( not(hasattr(tG,'ga2')) ):
            gaP=GaProc(ctlpath="%s/dum.ctl"%(w2.GradsGslibDir),Quiet=Quiet,Bin=self.Bin)
            gaP.initGA(doreinit=1)
            tG.ga2=gaP.ga
            tG.ge2=tG.ga2.ge

        self.trkSource=tG.trkSource
        if(hasattr(tG,'FtrkSource')): self.FtrkSource=tG.FtrkSource

        self.ga=tG.ga2
        self.ge=tG.ge2

        self.ga('q dims')

        self.ge.pareaxl=0.50
        self.ge.pareaxr=9.75
        self.ge.pareayb=0.25
        self.ge.pareayt=8.25
        self.ge.setParea()


        self.curgxout=self.ga.getGxout()
        self.setInitialGA()

        # -- get TC info and best track
        #
        if(not(hasattr(tG,'tD'))):  
            print 'III-TCdiag.TcTrkPlot() -- making tD...'
            tD=TcData(dtgopt=self.dtg)
        else:                       
            tD=tG.tD

        self.bts=tD.getBtcs4Stmid(self.stmid,dtg=self.dtg,dobt=self.dobt)

        if(len(self.bts) == 0):
            print 'WWW TcTrkPlot no bts for stmid: ',self.stmid,' dtg: ',self.dtg
            return


        (self.stm3id,self.stmname)=tD.getStmName3id(self.stmid)

        self.PlotTrk()


    def setInitialGA(self,overrideRT=1):

        ga=self.ga
        ge=self.ge
        try:
            btc=self.btcs[self.stmid]
        except:
            btc=None

        # -- override the reftrk for case when tceps doesn't get a good one...????
        #
        (alats,alons,refaid,reftau,reftrk)=GetOpsRefTrk(self.dtg,self.stmid,override=overrideRT,
                                                        verb=self.verb,btc=btc,inputAD=self.inputAD)

        self.alats=alats
        self.alons=alons
        self.refaid=refaid
        self.reftau=reftau
        self.reftrk=reftrk

        (lat1,lat2,lon1,lon2)=LatLonOpsPlotBounds(alats,alons,verb=self.verb)

        if(self.zoomfact != None):

            zoom=float(self.zoomfact)

            dlon=30.0/zoom
            dlat=20.0/zoom
            dint=2.5

            rlat=self.aidtrk[self.otau][0]
            rlon=self.aidtrk[self.otau][1]
            if(rlat == None):
                vdtg=mf.dtginc(self.dtg,self.otau)
                try:
                    bt=self.bts[vdtg]
                except:
                    bt=self.bts[self.dtg]
                rlat=bt[0]
                rlon=bt[1]

            lat1=rlat-dlat*0.65
            lat1=int(lat1/dint+1)*dint
            lat2=lat1+dlat

            lon1=rlon-dlon*0.35
            lon1=int(lon1/dint+1)*dint
            lon2=lon1+dlon



        ge.lat1=lat1
        ge.lat2=lat2
        ge.lon1=lon1
        ge.lon2=lon2

        ge.mapdset='mres'
        #ge.xlint=xlint
        #ge.ylint=ylint
        ge.clear()
        ge.mapcol=0
        ge.setMap()
        ge.grid='off'
        ge.setGrid()
        ge.setLatLon()
        ge.setXylint()
        ge.setParea()
        ge.setPlotScale()


        if(self.stmid in self.btcs.keys()):
            self.tau0stmvmax=self.btcs[self.stmid][2]
            self.tau0stmdir=self.btcs[self.stmid][4]
            self.tau0stmspd=self.btcs[self.stmid][5]
        else:
            self.tau0stmvmax=999
            self.tau0stmdir=270.0
            self.tau0stmspd=10.0            




    def PlotTrk(self,doalltaus=1,otau=48,etau=168,dtau=12):

        ga=self.ga
        ge=self.ge

        self.etau=etau
        self.dtau=dtau
        self.otau=otau

        mktaus=[0,24,48,72,120]
        mkcols={0:1,24:1,48:1,72:2,120:2}

        ftlcol=modelTrkPlotProps[self.model][0]
        modeltitle=modelOname[self.model]

        (btau,etau,dtau)=(0,etau,dtau)
        itaus=range(btau,etau+1,dtau)

        taus=[]
        for itau in itaus:
            for ttau in self.aidtaus:
                if(itau == ttau):
                    taus.append(itau)


        pbt=ga.gp.plotTcBt
        if(self.doveribt):
            pbt.set(self.bts,self.dtg,nhbak=72,nhfor=etau,ddtg=dtau)
        else:
            pbt.set(self.bts,self.dtg,nhbak=72,nhfor=0,ddtg=dtau)

        bm=ga.gp.basemap2
        bm.draw()
        ge.setPlotScale()

        pbt.dline(times=pbt.otimesbak,lcol=7,lthk=7)
        pbt.dwxsym(times=pbt.otimesbak)


        if(self.doveribt):
            pbt.dline(times=pbt.otimesfor,lsty=1,lcol=1,lthk=10)
            pbt.dwxsym(times=pbt.otimesfor)
            pbt.legend(ge,times=pbt.otimesbak+pbt.otimesfor,ystart=7.9)

        else:
            pbt.legend(ge,times=pbt.otimesbak,ystart=7.9)


        pft=ga.gp.plotTcFt
        pft.set(self.aidtrk,lcol=ftlcol,doland=1)

        if(ftlcol == -2):
            pft.dline(lcol=15)
            try:     vmcol=pft.lineprop[otau][0]
            except:  None

            if(vmcol != 75):
                pft.dmark(times=[otau],mkcol=vmcol,mksiz=0.20)
                pft.dmark(times=[otau],mksiz=0.05)
            else:
                pft.dmark(times=[otau])
        else:
            pft.dline(times=taus,lsty=3)
            pft.dmark(times=taus,mksiz=0.050)
            for mktau in mktaus:
                if(mktau in taus):
                    pft.dmark(times=[mktau],mksiz=0.100)
                    pft.dmark(times=[mktau],mkcol=0,mksiz=0.070)
                    pft.dmark(times=[mktau],mkcol=mkcols[mktau],mksiz=0.040)




        ttl=ga.gp.title
        ttl.set(scale=0.85)
        t1='%s TC: %s[%s] V`bmax`n: %3dkt bdtg: %s'%(modeltitle,self.stmid,self.stmname,int(self.bts[self.dtg][2]),self.dtg)
        t2='TCDiag track plot'
        if(hasattr(self,'FtrkSource')):
            ts=self.FtrkSource[self.stmid]
        else:
            ts=self.trkSource
            

        if(mf.find(ts,'best')): ots='BEST'
        if(mf.find(ts,'mftrk')): ots='ESRL MF'
        if(mf.find(ts,'tmtrk')): ots='GFDL TM'
        t2="%s tracker: %s"%(t2,ots)

        ttl.top(t1,t2)

        ga('q pos')

        #ge.pngmethod='gxyat'
        ge.makePng(self.pltpath,verb=1)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# basic html for hfip -- only used in TcDiagHtml
#
class MFhtml(MFutils):

    webroot='hfip'
    webserver='ruc.noaa.gov'
    webdirbase=w2.HfipProducts
    weburlbase="http://%s/%s"%(webserver,webroot)

    def __init__(self,webdir=webdirbase,webroot=webroot):

        self.webdir=webdirbase

        self.initTopLine()


    def initTCs(self,stmdtg=None,stmid=None):

        from tcbase import TcData
        self.tD=TcData(dtgopt=stmdtg)
        if(stmid == None and hasattr(self,'stmid')): stmid=self.stmid
        self.bts=self.tD.getBtLatLonVmax(stmid,stmdtg=self.dtg)
        try:    self.tcvmax=self.bts[self.dtg][2]
        except: self.tcvmax=-999

        (self.stm3id,self.stmname)=self.tD.getStmName3id(self.stmid)



    def initTopLine(self):

        self.html="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">"""


    def initHead(self,
                 bdir='../../..',
                 pagetitle=None,
                 cssdir=None,
                 jsdir=None,
                 icondir=None,
                 cssfile='tcdiag.css',
                 xsize=830,
                 ysize=630,
                 dourltxt=1,
                 ):


        if(pagetitle == None and hasattr(self,'pagetitle')):  pagetitle=self.pagetitle
        else:                                                 self.pagetitle=pagetitle

        self.cssdir=cssdir
        self.jsdir=jsdir
        self.icondir=icondir
        self.cssfile=cssfile
        if(cssdir == None):   self.cssdir="%s/css"%(bdir)
        if(jsdir == None):    self.jsdir="%s/js"%(bdir)
        if(icondir == None):  self.icondir="%s/icon"%(bdir)


        self.html='''%s
<html>
<head>

<title>
%s
</title>

<link rel="shortcut icon" href="%s/favicon.ico">
<link rel="stylesheet"  type="text/css" href="%s/%s">
<link rel="stylesheet"  type="text/css" href="%s/lightbox.css">

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da >
'''%(self.html,self.pagetitle,self.icondir,self.cssdir,self.cssfile,self.cssdir)

        ustmid=None
        umodel=None
        if(hasattr(self,'stmid')): ustmid=self.stmid.upper()
        if(hasattr(self,'model')): umodel=self.model
        if(ustmid != None and umodel != None):
            urltxt="diag.all.%s.%s.txt"%(ustmid,umodel)
        else:
            urltxt='text.txt'

        self.html='''%s
<script language="javascript" type="text/javascript">

<!-- Idea by:  Nic Wolfe -->
<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->
<!-- Begin
function popUp(URL) {

URL='%s'

day = new Date();
id = day.getTime();
eval("page" + id + " = window.open(URL, '" + id + "', 'toolbar=1,scrollbars=1,location=1,statusbar=1,menubar=1,resizable=1,width=1024,height=768');");
}

var newwindow;
function poptastic(url)
{
	newwindow=window.open(url,'name','height=%d,width=%d');
	if (window.focus) {newwindow.focus()}
}

function lightboxhtm(url) {
    parent.location.href=url;
    parent.location.rel='lightbox';
alert(url);
}


</script>

</head>'''%(self.html,urltxt,ysize,xsize)


        self.html='''%s
<script language="javascript" src="%s/wxmain.js"   type="text/javascript"></script>
<script language="javascript" src="%s/lightbox.js" type="text/javascript"></script>
'''%(self.html,self.jsdir,self.jsdir)



    def setTitle(self,htmltitle=None,width=1024):

        if(htmltitle == None): htmltitle=self.htmltitle

        self.html='''%s
<table class='title'>
<tr>
<td width=%d>
%s
</td>
</tr>
</table>'''%(self.html,width,htmltitle)


    def initTail(self):

        self.html='''%s
</body>
</html>'''%(self.html)



    def writeHtml(self,verb=0):

        if(verb):
            print 'III(M.MFhtml) writing html path: ',self.htmlpath
            print 'III(M.MFhtml)          html url: ',self.htmlurl

        rc=self.WriteString2File(self.html,self.htmlpath)


class TcDiagHtml(MFhtml):

    def __init__(self,tG=None,tGtrk=None,verb=0):

        self.tG=tG
        self.tGtrk=tGtrk

        self.verb=verb
        self.name='tcdiag'
        self.pagename='TCdiag'

        self.rctG=1
        if(not(hasattr(tG,'year'))):
            self.rctG=0
            return

        self.year=self.tG.year
        self.dtg=self.tG.dtg
        self.model=self.tG.model.lower()
        self.umodel=self.tG.model.upper()
        self.stmid=self.tG.stmid.lower()
        self.basename=self.tG.basename
        if(hasattr(tG,'aidtrk')): self.aidtrk=self.tG.aidtrk

        self.urlbase="../../../%s/%s/%s"%(self.year,self.dtg,self.model)
        self.trkploturl=self.tGtrk.trkploturl

        if(hasattr(tG,'webdir')):
            self.webdir=self.tG.webdir
        else:
            print 'EEE(TcDiagHtml) webdir not set in tG object'
            sys.exit()

        self.weburldir="%s/%s/%s/%s"%(self.name,self.year,self.dtg,self.model)
        self.webdir="%s/%s"%(self.webdir,self.weburldir)
        MF.ChkDir(self.webdir,'mk')

        self.htmlfile="%s.%s.%s.htm"%(self.model,self.dtg,self.stmid)
        self.htmlurl="%s/%s/%s"%(self.weburlbase,self.weburldir,self.htmlfile)
        self.htmlpath="%s/%s"%(self.webdir,self.htmlfile)

        self.pagetitle="%s :: %s %s  %s"%(self.basename,self.dtg,self.model,self.stmid)

        print
        print 'HHH making MODEL html for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid
        print


        (dir,file)=os.path.split(self.tG.finalDiagPath)
        diagurl="%s/%s"%(self.urlbase,file)

        self.databutton='''
<input type='button' class='databutton'
onMouseOver="className='databuttonOVER';"
onMouseOut="className='databutton';"
value='%s.file' name=taub
onClick="url='%s',poptastic(url);">
'''%(self.basename,diagurl)

        self.trkbutton='''
<input type='button' class='databutton'
onMouseOver="className='databuttonOVER';"
onMouseOut="className='databutton';"
value='%s.TRKplot' name=taub
onClick="url='%s',poptastic(url);">
'''%(self.basename,self.trkploturl)

        self.htmldiag={}

        self.taus=self.tG.taus
        # -- check if taus reduced because of going to far poleward
        #
        if( hasattr(tG,'stmTaus') and (len(self.taus) > len(tG.stmTaus)) ):
            self.taus=tG.stmTaus

        self.diagKeys=self.tG.diagKeys
        self.diagVals=self.tG.diagVals
        self.diagTypes=self.tG.diagTypes
        self.diaguRls=self.tG.diaguRls
        self.diagFilenames=self.tG.diagFilenames
        self.pyppathHtml=self.tG.pyppathHtml

        # -- get tc info from tG object
        #

        tG.getTCinfo(self.stmid.upper())
        if(hasattr(self.tG,'bts')):
            self.bts=self.tG.bts
            self.stm3id=self.tG.stm3id
            self.stmname=self.tG.stmname
            self.tcvmax=self.tG.tcvmax
        else:
            print "III(TcDiagHmtl): getting TC info from MFhtml.initTCs"
            self.initTCs(stmdtg=self.dtg)

        datatrkhtm='''
<table border=0 cellpadding=0 cellspacing=0 width=1000 style='table-layout:fixed' >
<col width=100>
<col width=100>
<col width=800>
<tr>
<td>
%s
</td>
<td>
%s
</td>
 '''%(self.databutton,self.trkbutton)

        self.htmltitle='''
 %s <td>
<table border=0 cellpadding=0 cellspacing=0 width=800 class='title'  >
<tr>
<col width=800>
<td>
&nbsp;&nbsp;
 Model: <font color=blue>%s</font> Dtg: <font color=blue>%s</font>
 TC: <font color=red>%s [%s]</font>  TCVmax: <font color=red>%d</font>
<a href="%s" rel="lightbox" title="trkplot" >TRKplot</a>
</td>
</tr>
</table>
</td>
</tr>
</table>

'''%(datatrkhtm,modelOname[self.model],self.dtg,self.stmid.upper(),self.stmname,int(self.tcvmax),self.trkploturl)




    def doHtml(self):

        self.initTopLine()
        self.initHead()
        if(self.verb): self.printStats()
        self.setTitleLocal()
        self.setplotTable()
        self.initTail()
        self.writeHtml(verb=self.verb)

        # -- copy diag file to webdir
        #
        cmd="cp %s %s"%(self.tG.finalDiagPath,self.webdir)
        mf.runcmd(cmd)


    def setTitleLocal(self,htmltitle=None):

        if(htmltitle == None): htmltitle=self.htmltitle

        self.html='''%s
%s
'''%(self.html,htmltitle)



    def doPyp(self,verb=0):

        try: del self.tD
        except: None

        # -- a good idea?
        del self.tG

        try: del self.tGtrk
        except: None

        if(verb or self.verb): print 'III writing html pyp: ',self.pyppathHtml
        self.putPyp(pyppath=self.pyppathHtml,verb=verb)



    def taulabel(self,taus=None):

        if(taus != None):
            ltaus=taus
        else:
            ltaus=self.taus

        cstyle=''
        htm='''<td class="tauHead" %s >%s</td>'''%(cstyle,'tau:')
        self.html='''%s\n%s'''%(self.html,htm)

        for tau in ltaus:
            cstyle='''style="background-color: #FFFF33; color: #000000"'''
            cval=tau
            htm='''<td class="tauVal" %s >%s</td>'''%(cstyle,cval)
            self.html='''%s\n%s'''%(self.html,htm)

        self.html='''%s\n</tr>'''%(self.html)




    def setplotTable(self):


        self.html='''%s\n<table class="stats" cellspacing="0"><tr>'''%(self.html)

        rc=self.taulabel()

        didTauCustom=0
        didTauSounding=0

        dkeys=self.diagKeys

        # -- for case when there is no tau 0 in tracker?  happenend for tmtrkN 2015070712
        #    did a ttc -O and it cleared -- maybe a problem with dccs1?
        #
        for dkey in dkeys:
            try:
                ctype=self.diagTypes[0][dkey]
            except:
                try:
                    ctype=self.diagTypes[6][dkey]
                except:
                    print 'WWW - no tau 0 or tau 0 for TcDiagHtml.setplotTable() dkey: ',dkey
                    continue

            if(ctype == 'custom' and didTauCustom == 0):
                rc=self.taulabel()
                didTauCustom=1

            if(ctype == 'sounding' and didTauSounding == 0):
                rc=self.taulabel()
                didTauSounding=1



            self.htmldiag[dkey]=''

            cstyle=''
            if(mf.find(dkey,'TIME')):  cstyle='''style="background-color: #B0C4DE; color: #000000"'''


            #if(self.diagFilenames[dkey] != 'None'):
            #    curl="../%s.htm"%(self.diagFilenames[dkey])
            #    cval=dkey
            #    cval='''<a href="%s" >%s</a>'''%(curl,cval)
            #else:
            #    cval=dkey

            if(not(mf.find(dkey,'TIME'))):
                curl="../%s.htm"%(self.diagFilenames[dkey])
                cval=dkey
                cval='''<a class="linkTextb" href="%s" >%s</a>'''%(curl,cval)
            else:
                cstyle='''style="background-color: #B0C4DE; color: #000000"'''
                cval=dkey

            htm='''<td class="field" %s >%s</td>'''%(cstyle,cval)
            self.html='''%s\n%s'''%(self.html,htm)
            self.htmldiag[dkey]=self.htmldiag[dkey]+htm

            for tau in self.taus:

                cval=self.diagVals[tau][dkey]
                if(float(cval) == -9999.): cval=' 9999'

                # -- in case a bad number gets to this point
                #
                if(len(cval) > 5):  cval='9999'

                ctype=self.diagTypes[tau][dkey]
                if(self.diaguRls[tau][dkey] != 'None'):
                    curl=self.diaguRls[tau][dkey]
                    curl="../../../%s"%(curl)
                    ###cval='''<a href="javascript:poptastic('%s');">%s</a>'''%(curl,cval)
                    cval='''<a class="linkText" href="%s" rel="lightbox" title="%s" >%s</a>'''%(curl,cval,cval)

                cstyle=''
                if(ctype == 'storm'):                           cstyle='''style="background-color: #FFB6C1; color: #000000"'''
                if(ctype == 'custom'):                          cstyle='''style="background-color: #FFFFF0; color: #000000"'''
                if(ctype == 'sounding'):                        cstyle='''style="background-color: #87CEFA; color: #000000"'''
                if(mf.find(self.diagVals[tau][dkey],'9999')):   cstyle='''style="background-color: #888; color: #fff"'''
                if(mf.find(dkey,'TIME')):                       cstyle='''style="background-color: #B0C4DE; color: #000000"'''

                htm='''<td class="val" %s >%s</td>'''%(cstyle,cval)
                self.html='''%s\n%s'''%(self.html,htm)

            self.html='''%s\n</tr>'''%(self.html)

        self.html='''%s\n</table>'''%(self.html)


    def printStats(self):

        for tau in self.taus:
            for dkey in self.diagKeys:
                print tau,dkey,self.diagVals[tau][dkey],self.diaguRls[tau][dkey]





class TcDiagHtmlVars(TcDiagHtml):


    def __init__(self,tG=None,
                 keepmodels=None,
                 verb=0):


        self.tG=tG

        self.verb=verb
        self.keepmodels=keepmodels
        self.name='tcdiag'
        self.pagename='TCdiagVars'

        self.year=self.tG.year
        self.dtg=self.tG.dtg
        self.model=self.tG.model.lower()
        self.umodel=self.tG.model.upper()
        self.basename=self.tG.basename
        self.stmid=self.tG.stmid

        self.weburldir="%s/%s/%s"%(self.name,self.year,self.dtg)
        if(hasattr(tG,'webdir')):
            self.webdir=self.tG.webdir
        else:
            print 'EEE(TcDiagHtmlVars) webdir not set in tG object'
            sys.exit()

        self.webdir="%s/%s"%(self.webdir,self.weburldir)

        self.inittGhPyps()

        # -- tcinfo
        #
        rc=self.tG.getTCinfo(self.stmid.upper())
        (self.bts,self.tcvmax,self.stm3id,self.stmname)=rc

        print
        print 'HHH making VAR   html for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid
        print


    def sortVmodels(self):

        omodels=[]

        for smodel in tcdiagModelOrderVar:
            for vmodel in self.vmodels:
                if(vmodel == smodel):
                    omodels.append(vmodel)
                    break

        return(omodels)




    def inittGhPyps(self):

        verb=self.verb

        vkeys=[]
        vtaus=[]
        vmodels=[]
        vmodelurls={}

        vvals={}
        vurls={}
        vctypes={}

        hmask="%s/*/*htm*pyp"%(self.webdir)
        htmlpyps=glob.glob(hmask)

        gotvkeys=0
        for pyp in htmlpyps:
            (dir,file)=os.path.split(pyp)
            tgH=self.getPyp(pyppath=pyp)
            ss=file.split('.')
            stmid="%s.%s"%(ss[1],ss[2])
            if(stmid == self.stmid):
                model=dir.split('/')[len(dir.split('/'))-1]
                # -- use keepmodels to restrict which models go into the table
                #
                if(self.keepmodels != None  and not(model in self.keepmodels) ):
                    print 'SSSSSSSSSSSSSSSSSSSSkipping ',model,'in ',self.keepmodels
                    continue

                vmodels.append(model)
                try:
                    vmodelurls[model]=tgH.htmlfile
                except:
                    print 'WWWW unable to read pyp: ',pyp

                if(gotvkeys == 0):
                    vkeys=tgH.diagKeys
                    vfilenames=tgH.diagFilenames
                    gotvkeys=1

                # -- find max vtaus
                #
                if(len(tgH.taus) > len(vtaus)): vtaus=tgH.taus

                vvals[model]=tgH.diagVals
                vurls[model]=tgH.diaguRls
                vctypes[model]=tgH.diagTypes

                if(verb == 1):
                    kks=tgH.diagFilenames.keys()
                    kks.sort()
                    for kk in kks:
                        print kk,tgH.diagFilenames[kk]
                        for tau in tgH.taus:
                            print tgH.diagVals[tau][kk],tgH.diaguRls[tau][kk]


        # -- no diags for stmid
        #
        if(len(vkeys) == 0):
            print 'WWW initGhPyps len(vkeys) = 0'
            self.vkeys=vkeys
            return(0)

        if(verb):
            print '     vkeys: ',vkeys
            print '     vtaus: ',vtaus
            print '   vmodels: ',vmodels
            if(verb > 1): print 'vfilenames: ',vfilenames
            for vmodel in vmodels:
                print 'vvvvv ',vmodel,len(vurls[model][0].keys())
                print 'vvvvv ',vmodel,len(vvals[model][0].keys())


        self.vkeys=vkeys
        self.vmodels=vmodels
        self.vtaus=vtaus
        self.vfilenames=vfilenames
        self.vvals=vvals
        self.vurls=vurls
        self.vmodelurls=vmodelurls
        self.vctypes=vctypes



    def doHtml(self):


        rc=1
        if(len(self.vkeys) == 0):
            rc=0
            return(rc)

        for vkey in self.vkeys:

            if(mf.find(vkey,'TIME')): continue
            self.pagetitle="%s %s"%(vkey,self.dtg)
            self.htmltitle="%s for models at dtg:<font color=blue>%s</font> TC: <font color=red>%s</font>  TCVmax: <font color=red>%d</font>"%(vkey,self.dtg,self.stmid,int(self.tcvmax))
            self.htmlfile="%s.htm"%(self.vfilenames[vkey])
            self.htmlpath="%s/%s"%(self.webdir,self.htmlfile)
            self.htmlurl="%s/%s/%s"%(self.weburlbase,self.weburldir,self.htmlfile)

            self.initTopLine()
            self.initHead(bdir='../..')
            self.setTitle()
            self.setplotTable(vkey)
            self.initTail()
            self.writeHtml(verb=self.verb)

        return(rc)



    def setplotTable(self,tvkey):

        self.html='''%s\n<table class="stats" cellspacing="0"><tr>'''%(self.html)

        rc=self.taulabel(taus=self.vtaus)

        for vkey in self.vkeys:

            if( not(mf.find(vkey,'TIME') or vkey == tvkey) ):continue


            if(mf.find(vkey,'TIME')):

                cstyle=''
                if(mf.find(vkey,'TIME')):  cstyle='''style="background-color: #B0C4DE; color: #000000"'''
                htm='''<td class="field" %s >%s</td>'''%(cstyle,vkey)
                self.html='''%s\n%s'''%(self.html,htm)

                for vtau in self.vtaus:
                    cval=vtau
                    cstyle=''
                    cstyle='''style="background-color: #B0C4DE; color: #000000"'''
                    htm='''<td class="val" %s >%s</td>'''%(cstyle,cval)
                    self.html='''%s\n%s'''%(self.html,htm)

                self.html='''%s\n</tr>'''%(self.html)


            else:


                omodels=self.sortVmodels()
                for vmodel in omodels:

                    cstyle=''

                    curl="%s/%s"%(vmodel,self.vmodelurls[vmodel])
                    cval=vmodel.upper()
                    cval=modelTagOname[vmodel]

                    curltrk="../../%s/%s/%s/trkplt.%s.%s.png"%(self.year,self.dtg,vmodel,self.stmid,vmodel)
                    cvaltrk='TRK'

                    cval='''<a class="linkTextb" href="%s" >%s</a>&nbsp;<a class="linkTextb" href="%s" rel="lightbox" >%s</a>'''%(curl,cval,curltrk,cvaltrk)

                    htm='''<td class="field" %s >%s</td>'''%(cstyle,cval)
                    self.html='''%s\n%s'''%(self.html,htm)

                    for vtau in self.vtaus:

                        try:
                            cval=self.vvals[vmodel][vtau][tvkey]
                        except:
                            cval='9999'

                        # -- in case a bad number gets to this point
                        #
                        if(len(cval) > 5):  cval='9999'

                        try:
                            curl=self.vurls[vmodel][vtau][tvkey]
                        except:
                            curl='None'

                        try:
                            ctype=self.vctypes[vmodel][vtau][tvkey]
                        except:
                            ctype='None'

                        if(curl != 'None'):
                            curl="../../%s"%(curl)
                            cval='''<a class="linkText" href="%s" rel="lightbox" title="%s" >%s</a>'''%(curl,cval,cval)

                        cstyle=''
                        if(ctype == 'storm'):                           cstyle='''style="background-color: #FFB6C1; color: #000000"'''
                        if(ctype == 'custom'):                          cstyle='''style="background-color: #FFFFF0; color: #000000"'''
                        if(ctype == 'sounding'):                        cstyle='''style="background-color: #87CEFA; color: #000000"'''
                        if(mf.find(cval,'9999')):                       cstyle='''style="background-color: #888; color: #fff"'''
                        #if(mf.find(tvkey,'TIME')):                       cstyle='''style="background-color: #B0C4DE; color: #000000"'''

                        htm='''<td class="val" %s >%s</td>'''%(cstyle,cval)
                        self.html='''%s\n%s'''%(self.html,htm)

                    self.html='''%s\n</tr>'''%(self.html)


        self.html='''%s\n</table>'''%(self.html)






#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods
#

def getModels4Dtg(dtg,modelopt):

    models=modelopt.split(',')

    if(modelopt == 'all'):
        models=tcdiagModels
        if(MF.is0618Z(dtg)): models=tcdiagModels0618

    elif(modelopt == 'alljt'):
        models=jtdiagModels
        if(MF.is0618Z(dtg)): models=jtdiagModels0618

    elif(modelopt == 'allgen'): models=tcdiagGenModels

    return(models)

def getDtgsModels(CL,dtgopt,modelopt,dtgs=None,
                  stmopt=None,dtginc=12):

    if(stmopt != None):
        tD=TcData(stmopt=stmopt)
        stmids=MakeStmList(stmopt,verb=0)
        dtgs=[]
        for stmid in stmids:
            dtgs=dtgs+tD.getStmDtgs(stmid)

        odtgs=[]
        for dtg in dtgs:
            hh=int(dtg[8:10])
            if(hh%dtginc == 0):
                odtgs.append(dtg)

        dtgs=odtgs

    elif(dtgs == None):
        dtgs=mf.dtg_dtgopt_prc(dtgopt)

    modelsDiag={}
    for dtg in dtgs:
        modelsDiag[dtg]=getModels4Dtg(dtg,modelopt)

    return(dtgs,modelsDiag)


def cycleByDtgsModels(CL,dtgs,models,stmopt=None):

    # -- check for when doing a single model
    if((len(dtgs) == 1 and len(models) == 1) or CL.doinventory):
        dtg=dtgs[0]
        model=models[0]
        return(dtg,model)

    if(CL.dohtmlvars): models=['gfs2']

    for dtg in dtgs:

        for model in models:

            cmd="%s %s %s"%(CL.pypath,dtg,model)
            for o,a in CL.opts:

                if(stmopt == None and o != '-S'):
                    cmd="%s %s %s"%(cmd,o,a)

            mf.runcmd(cmd,CL.ropt)

    sys.exit()



def getStmids(dtg,allstmids,aDstm2ids=None,stmopt=None,dols=0,tD=None):

    aDstm1ids=[]

    if(stmopt != None): tstmids=MakeStmList(stmopt,verb=0)
    else: tstmids=None

    # -- check if in existing tc list:
    #
    if(tstmids == None):
        tstmids=allstmids

    elif(len(tstmids) > 0):
        newtstmids=[]
        for allstmid in allstmids:
            for tstmid in tstmids:
                if(allstmid == tstmid): newtstmids.append(allstmid)

    if(aDstm2ids != None):

        for stm2id in aDstm2ids:
            bnum=stm2id[2:4]
            b2id=stm2id[0:2].lower()

            stm1id=None

            if(not(b2id == 'io' or b2id == 'sh')):
                stm1id=stm2idTostm1id(stm2id)
            else:
                for allstmid in allstmids:
                    abnum=allstmid[0:2]
                    b1id=allstmid[2].lower()
                    astm2id=stm1idTostm2id(allstmid)
                    ab2id=astm2id[0:2]

                    if(bnum == abnum and (ab2id == 'io' or ab2id == 'sh') ):
                        stm1id=None
                        # -- case where tracker does not identify the subbasin but uses 'i'
                        if(ab2id == 'io' and (b1id == 'a' or b1id == 'b' or b1id == 'i') ):
                            stm1id=allstmid
                        elif(ab2id == 'sh' and (b1id == 's' or b1id == 'p') ):
                            stm1id=allstmid
                            
                        break

                    # -- storm from adecks no longer in mdeck tcvitals
                    #
                    else:

                        if(ab2id == 'io' and (b1id == 'a' or b1id == 'b') ):
                            stm1id=allstmid
                        elif(ab2id == 'sh' and (b1id == 's' or b1id == 'p') ):
                            stm1id=allstmid

            if(stm1id == None):
                # -- cases in io where model run with 9X but went to NN, depends on when the tracker was run
                stm1id=stm2idTostm1id(stm2id)
                print 'WWW(TCdiag.getStmids): unable to match stm2id: ',stm2id,' in IO/SHEM 9X adeck with one in TCdata() setting to: ',stm1id
                        
            if(stm1id != None):
                aDstm1ids.append(stm1id)

        aDstm1ids=MF.uniq(aDstm1ids)


    # if going for all tcs add in ones from the tracker
    #
    if(tstmids == allstmids):
        tstmids=MF.uniq(allstmids+aDstm1ids)


    if(tstmids == None): tstmids=[]

    # -- find storms that are NOT tracked in the model
    #
    if(tD != None):
        
        # -- first find NOT adstorms
        #
        aDstm1idsNot=[]
        noADstmids=[]
        
        for tstmid in tstmids:
            if(not(tstmid in aDstm1ids)): noADstmids.append(tstmid)

        rstmids=tD.getRawStm1idDtg(dtg)

        for rstmid in rstmids:
            (snum,b1id,year,b2id,stm2id,rstmid9)=getStmParams(rstmid,convert9x=1)
            if(rstmid9 in noADstmids):
                aDstm1idsNot.append(rstmid)


    if(dols):
        if(len(allstmids) == 0):
            print 'NO Current stmids...'
            return(0,tstmids)
        else:
            print
            print 'Current stmids: '
            for stmid in allstmids:
                print stmid

        print
        print 'Current stmids in AD: '
        for stmid in aDstm1ids:
            print stmid
            
        if(tD != None and len(aDstm1idsNot) > 0):
            print
            print 'Current stmids NOT in AD:'
            for stmid in aDstm1idsNot:
                print stmid
            print

    rc=(0,tstmids)
    if(tD != None): rc=(1,tstmids,aDstm1idsNot)
    return(rc)

def runLsDiag(mfT,tG,ropt='',override=0,doAdeckOut=1):
    """ run the fortran using the TcFldsDiag and TcDiag objects
    """
    if(not(mfT.sstDone and mfT.meteoDone)):
        print '''EEE(runLsDiag):  mfT.sstDone:''',mfT.sstDone,'''and mfT.meteoDone:''',mfT.meteoDone,''' != 1'''
        return(0)

    sstpath=mfT.sstdpath
    metapath=mfT.mpath
    tcmetapath=tG.mpath
    outpath=tG.finalDiagPath
    prcdir=tG.prcdir

    # -- dump adeck used in making the diag file to same place as diagfile
    #    also done in TcDiag.putAdeckCards
    #
    if(hasattr(tG,'oadeck') and doAdeckOut):
        oadeckPath=outpath.replace('tcdiag','oadeck')
        MF.WriteList2File(tG.oadeck,oadeckPath,verb=0)
    cmd="%s/lsdiag.x %s %s %s %s"%(prcdir,metapath,tcmetapath,sstpath,outpath)
    MF.runcmd(cmd,ropt)
    return(1)



def runLgem(diagpath,tG,tD,dtg,model,stmid,
            prcdir='/w21/prc/tcdiag',
            prcdirIships='/w21/src/tclgem',
            verb=0,icarqvmax=1,ropt=''):


    # -- check if nhc storm...
    #

    if(not(IsNhcBasin(stmid))):
        print """WWW can't run lgem for non nhc basin; stmid: """,stmid
        return

    if(hasattr(tG,'shipstxt')):
        shipstxt=tG.shipstxt
        shipsadk=tG.shipsadk
        shipslog=tG.shipslog
        shipscrq=tG.shipscrq

    if(verb):
        print 'diagpath: ',diagpath
        print 'shipstxt: ',shipstxt
        print 'shipsadk: ',shipsadk
        print 'shipslog: ',shipslog
        print 'shipscrq: ',shipscrq

    MF.ChangeDir(prcdir)

    atrk={}

##    # -- old version using mdecks.pybdb
##    #
##    aDcarq=AD.getCarqFromDss(stmid,verb=verb)
##    if(aDcarq == None):
##        print 'WWW(aDcarq): not available for stmid: ',stmid,' dtg: ',dtg,' model: ',model
##        pass
##    else:
##        try:
##            print 'III getting carq from aDcarq'
##            atrk=aDcarq.ats[dtg]
##        except:
##            atrk={}

    # -- use mdecks2 -- no BT
    #
    if(len(atrk) == 0):
        atrk=getAtrkFromStmid(tD,stmid,dtg)

    # -- if no luck; bail
    #
    if(len(atrk) == 0):
        print 'WWW(atrk): no posits in atrk for stmid: ',stmid,' dtg: ',dtg,' model: ',model
        return

    ocard=Atrk2Icarq(atrk,dtg)
    MF.WriteString2File(ocard,shipscrq,verb=1)

    cmd="ln -s -f %s modeldiag.dat"%(diagpath)
    MF.runcmd(cmd,ropt)

    cmd="ln -s -f %s ships.txt"%(shipstxt)
    MF.runcmd(cmd,ropt)

    cmd="ln -s -f %s ships.dat"%(shipsadk)
    MF.runcmd(cmd,ropt)

    cmd="ln -s -f %s ships.log"%(shipslog)
    MF.runcmd(cmd,ropt)

    if(len(atrk) > 0):
        ocard=Atrk2Icarq(atrk,dtg)
        MF.WriteString2File(ocard,shipscrq)

    cmd="ln -s -f %s icarq.dat"%(shipscrq)
    MF.runcmd(cmd,ropt)

    # -- run the model
    #
    if(icarqvmax == 0):
        cmd="%s/iships.x -i"%(prcdirIships)
    else:
        cmd="%s/iships.x"%(prcdirIships)

    MF.runcmd(cmd,ropt)


def getAtrkFromStmid(tD,stmid,dtg):

    atrk={}
    ttrk=None

    btcs=tD.getBtcs4Stmid(stmid,dtg)

    if(len(btcs) == 0):
        return(atrk)
    else:
        ttrk=btcs
        tdtgs=btcs.keys()

    if(ttrk != None):
        dtg0=dtg
        dtgm12=mf.dtginc(dtg,-12)

        try:
            trk0=ttrk[dtg0]
        except:
            print 'WWW getAtrkFromStmid failed...stmid: ',stmid,' dtg: ',dtg
            return(atrk)


        try:
            trkm12=ttrk[dtgm12]
            type=1
        except:
            trkm12=None

        if(trkm12 == None):
            try:
                trkm12 = ttrk[mf.dtginc(dtg0,-6)]
                trk0   = ttrk[mf.dtginc(dtg0,+6)]
                type=2
            except:
                trk0=None
                trkm12=None

        if(trk0 == None):
            try:
                trkm12 = ttrk[mf.dtginc(dtg0,+0)]
                trk0   = ttrk[mf.dtginc(dtg0,+6)]
                type=3

            except:
                print 'WWW(getAtrkFromStmid) -- perverse case of single posit bt for stmid: ',stmid,' dtg: ',dtg
                return(atrk)


        atrk[0]   =trk0[0:4]
        atrk[-12] =trkm12[0:4]

        print '000 getAtrkFromStmid ',type,atrk[0]
        print '111 getAtrkFromStmid ',type,atrk[-12]


    return(atrk)



def Atrk2Icarq(atrk,dtg):

    (rlat0,rlon0,rvmax0,rpmin0)=atrk[0]
    (rlatm12,rlonm12,rvmaxm12,rpminm12)=atrk[-12]

    (course,speed,eiu,eiv)=rumhdsp(rlatm12,rlonm12,rlat0,rlon0,12)

    ihead=int(course+0.5)
    ispeed=int(speed+0.5)

    if(rlon0 >= 180.0): rlon0 = rlon0-360.0
    if(rlonm12 >= 180.0): rlonm12 = rlonm12-360.0

    print '000000',rlat0,rlon0,rvmax0,rpmin0
    print '121212',rlatm12,rlonm12,rvmaxm12,rpminm12

    ilat0=int("%5.0f"%(rlat0*10.0))
    ilon0=int("%5.0f"%(rlon0*10.0))
    ivmx0=int("%5.0f"%(rvmax0))

    ilatm12=int("%5.0f"%(rlatm12*10.0))
    ilonm12=int("%5.0f"%(rlonm12*10.0))
    ivmxm12=int("%5.0f"%(rvmaxm12))

    iper=ivmx0-ivmxm12

    print 'FFFFFF: %5.1f %6.1f  %5.1f %6.1f'%(rlat0,rlon0,rlatm12,rlonm12)

    ocard="%10s %5d %5d %5d %5d %5d %5d %5d %5d %5d"%(dtg,ilat0,ilon0,ilatm12,ilonm12,ivmx0,ivmxm12,ihead,ispeed,iper)
    print ocard
    return(ocard)



if (__name__ == "__main__"):

    curdtg=mf.dtg()
    print 'cccccccccccc ',curdtg
    model='gfs2'
    td=TcDiag(curdtg,model)
    td.ls()
    sys.exit()
