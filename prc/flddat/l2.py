#!/usr/bin/env python

"""%s

purpose:

 list nwp2 fld files ++

  dtgopt -- nwp2 data
  fim    -- fim data/trackers

  qpr    -- qmorph precip

  goes   -- gfs goes

  tceps    -- tigge cxml
  tcepsxml -- xml from ecmwf/ukmo
  genstrk  -- ncep/cmc eps trackers from ncep:/com
  reftrk   -- reference tracker for setting area dimensions

  ecbufr   -- GTS bufr tracker from ncep

examples:

  %s cur-12,cur-6 gfs2
  %s reftrk 2014091712.cur12.12  # display reftrk files from 2014091712 to curdtg
  %s tceps 2014091712.cur12.12   # display tceps files from 2014091712 to curdtg
  %s ecbufr 2014091712.cur12.12  # display ecbufr files from 2014091712 to curdtg

-V :: verbose
-l :: list every tau
-A :: lsadeck=doarchve=1
-D :: dmodelType=a
-W :: dmodelType='w2flds'
-O :: override=1 for making grib inventory
-I :: doinv=1
-K :: unlink=1 for nwp2Inv-w2flds.pypdb
-R :: noRunChk=1 -- bypass chkIfRunning

"""

diag=0
from M import MFutils
mf2=MFutils()

mf2.sTimer('all')
if(diag): mf2.sTimer('w2')
from WxMAP2 import *
w2=W2()

from M2 import setModel2,FimModel,Model2
from tcbase import CurShemOverlap
if(diag): mf2.dTimer('w2')

# defaults
#
longls=0
models=None
verb=0
dmodelType=None
lsadeck=0
doarchive=0
override=0
nmaxTceps=3
nmaxReftrk=3
nmaxEcbufr=6
doinv=0
unlink=0
noRunChk=0

curdtg=mf.dtg()
curphr=mf.dtg('phr')
(tttdtg,curphr)=mf.dtg_phr_command_prc(curdtg) 
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

narg=len(sys.argv)-1

if(narg >= 1):

    lsopt=sys.argv[1]
    istart=2

    if(narg > 1):

        if(mf.find(sys.argv[1],'tceps')):
            dtgs=mf.dtg_dtgopt_prc(sys.argv[2])
            nmaxTceps=len(dtgs)

        elif(mf.find(sys.argv[1],'reftrk')):
            dtgs=mf.dtg_dtgopt_prc(sys.argv[2])
            nmaxReftrk=len(dtgs)

        elif(mf.find(sys.argv[1],'ecbufr')):
            dtgs=mf.dtg_dtgopt_prc(sys.argv[2])
            nmaxEcbufr=len(dtgs)

        elif(mf.find(sys.argv[2],'cur') or not(mf.find(sys.argv[2],'-')) ):
            models=sys.argv[2].split(',')
            istart=3
    try:
        (opts, args) = getopt.getopt(sys.argv[istart:], "VlAD:WOIKR")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-V",""): verb=1
        if o in ("-l",""): longls=1
        if o in ("-A",""): lsadeck=1 ; doarchive=1
        if o in ("-D",""): dmodelType=a
        if o in ("-W",""): dmodelType='w2flds'
        if o in ("-O",""): override=1
        if o in ("-K",""): unlink=1
        if o in ("-R",""): noRunChk=1
        if o in ("-I",""): doinv=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#


year=curdtg[0:4]

emodels=['cmc','ncep','ukmo','ecmwf']

MF.sTimer(tag='chkifrunning')
rc=w2.ChkIfRunningNWP(dtg=None,pyfile=pyfile,model=None)
if(rc > 1 and not(noRunChk)):
    print 'AAA allready running...'
    sys.exit()
if(diag): MF.dTimer(tag='chkifrunning')

llsopt=len(lsopt.split('.'))

if(
    (mf.find(lsopt,'cur') or mf.find(lsopt,'ops') or
     (len(lsopt)==10)  or (len(lsopt)==6 and llsopt == 1 and lsopt != 'reftrk' and lsopt != 'ecbufr') or
     len(lsopt)==13 or
     len(lsopt)>=21 or llsopt >= 2)
    ):

    if(diag): mf2.sTimer('dat')
    dtgopt=lsopt
    dtgs=mf.dtg_dtgopt_prc(dtgopt)

    if(models == None):
        models=Model2.models
        if(dmodelType == 'w2flds'): models=Model2.modelsW2

        #if(dmodelType == 'w2flds'):
            #models.remove('fim8')
            #if('ecmn' in models): models.remove('ecmn')


    elif(mf.find(models[0],'rtfim') and onWjet):
        #
        # handle real-time fim here with a subclassed Model2
        #

        domachine=0

        rf=FimModel()
        if(model == 'rtfim'): rf.version='FIM'
        if(model == 'rtfimx'): rf.version='FIMX'
        if(model == 'rtfimy'): rf.version='FIMY'

        for dtg in dtgs:
            rf.getNATfiles(dtg)

            if(rf.natdir == None):
                print "No %s data for %s"%(model,dtg)
                continue

            taus=rf.fimtaus
            if(len(taus) == 0):
                print 'WWW no taus for :',model,' at: ',dtg
                continue

            if(len(taus) < 3):
                otaus=taus
            else:
                otaus=[taus[0],taus[-2],taus[-1]]

            if(longls == 1):
                otaus=taus

            for tau in otaus:
                age=rf.fimages[tau]
                cage=MF.rhh2hhmm(age)
                print "%s  %s   %03d   %s"%(model,dtg,tau,cage)

            if(domachine):
                print 'MACHINE file: ',rf.machinefile
                cmd="uniq %s > /tmp/%s.nodes.txt"%(rf.machinefile,model)
                mf.runcmd(cmd)

            print

        sys.exit()


    else:
        #models=[model]
        models=models

    ms={}


    unlinkDone=0
    setinvDone=0
    for model in models:
        m=setModel2(model)
        if(m == None): sys.exit()
        if(doinv):
            if(unlink and not(unlinkDone)):
                mi=setModel2(model)
                mi.setInventory(override=override,unlink=unlink)
                unlinkDone=1
                setinvDone=1
            elif(not(setinvDone)):
                mi=setModel2(model)
                mi.setInventory(override=override)
                setinvDone=1

            m.iV=mi.iV

        ms[model]=m


    for dtg in dtgs: 

        if(len(models) > 1): print
        for model in models:

            lsext=''
            m=ms[model]
            #m.tryarch=0 -- too brutal


            hh=dtg[8:10]

            if(hh == '00'): runflg=w2.W2_MODELS_Run00
            if(hh == '06'): runflg=w2.W2_MODELS_Run06
            if(hh == '12'): runflg=w2.W2_MODELS_Run12
            if(hh == '18'): runflg=w2.W2_MODELS_Run18

            if(m == None): continue

            if(runflg[model]):

                if(diag > 1): mf2.sTimer('datapaths %s %s'%(model,dtg))

                m=ms[model]

                if(m == None): continue

                if(dmodelType != None):

                    m.dmodelType=dmodelType
                    m.dtype=dmodelType
                    if(dmodelType == 'w2flds'):
                        m.bddir="%s/%s/dat/%s"%(w2.Nwp2DataBdir,dmodelType,model)
                    else:
                        m.bddir="%s/%s"%(w2.Nwp2DataBdir,dmodelType)

                    if(hasattr(m,'setxwgribNwp2')): m.setxwgrib=m.setxwgribNwp2
                    fm=m.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,doDATage=1)

                elif(doarchive):
                    m.bddir="%s/%s"%(m.archdir,m.modelcenter)
                    fm=m.DataPath(dtg,dowgribinv=1,override=override,doDATage=1)

                else:
                    # -- special case -- Ecmg()
                    #
                    if(hasattr(m,'setxwgribNwp2')): m.setxwgrib=m.setxwgribNwp2
                    fm=m.DataPath(dtg,dowgribinv=1,override=override,doDATage=1)


                if(diag > 1): mf2.dTimer('datapaths %s %s'%(model,dtg))

                # -- always show the data dir
                #
                lsext="%s/%s"%(m.bddir,dtg)

                fd=fm.GetDataStatus(dtg)
                badage=0
                didprint=0
                if(len(fm.datpaths) > 0):
                    itaus=fm.dsitaus
                    ntaus=len(itaus)

                    if(fd.dslatestCompleteTauBackward > 0):
                        tau=fd.dslatestCompleteTauBackward
                    else:
                        tau=fd.dslatestCompleteTau

                    taus=[tau]
                    if(longls == 1):
                        taus=itaus

                    # -- logic for handling 'alltau' models, e.g., ukm2
                    #
                    statussTaus=fm.statuss[dtg].keys()

                    otau=tau
                    itaus=taus

                    if(len(statussTaus) == 1):  itaus=[statussTaus[0]]
                    if(len(statussTaus) == 0):  
                        itaus=[]                        
                        tau=999
                        age=999.9
                        nf=0
                        prefix='Z-'
                        print "%-6s %s%s  %03d   %7.2f  %4d <--- NO/ZERO DATA localdir: %s"%(model,prefix,dtg,tau,age,nf,fd.dstdir)
                        didprint=1

                    for itau in itaus:
                        prefix='  '

                        (age,nf)=fm.statuss[dtg][itau]
                        if(age == None):

                            tau=999
                            age=999.9
                            nf=0
                            if(not(doarchive)):
                                prefix='0-'
                                print "%-6s %s%s   %03d   %7.2f  %4d <--- NOOOO DATA because data are ln -s localdir: %s"%\
                                      (model,prefix,dtg,tau,age,nf,fd.dstdir)
                                didprint=1
                                continue
                        # -- use the tau from above unless more than 1 tau
                        #
                        if(len(itaus) > 1): otau=itau
                        olsext=lsext
                        if(nf < fm.nfields): 
                            prefix='L-'
                            olsext="%s <--- low data count nfields: %d"%(lsext,fm.nfields)
                        print "%-6s %s%s  %03d   %7.2f  %4d  nt:%3d  %s"%(model,prefix,dtg,otau,age,nf,ntaus,olsext)
                        didprint=1

                else:
                    tau=999
                    age=999.9
                    nf=0

                if((not(doarchive) and nf == 0 and not(didprint)) or badage):
                    if(badage): age=-888.8
                    print "%-6s N-%s  %03d   %7.2f  %4d <--- NO DATA localdir: %s"%(model,dtg,tau,age,nf,fd.dstdir)
                ##MF.dTimer('load1 %s %s'%(model,dtg))

    if(diag >= 1): mf2.dTimer('dat')


elif(lsopt == 'reftrk'):


    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    sdir="%s/%s"%(w2.TcRefTrkDatDir,year)
    rpaths=glob.glob("%s/*%s*"%(sdir,yyyymmm1))+glob.glob("%s/*%s*"%(sdir,yyyymm))

    rdtgs={}
    for rpath in rpaths:
        (dir,file)=os.path.split(rpath)
        tt=file.split('.')
        rdtg=tt[len(tt)-2]
        try:
            rdtgs[rdtg].append(rpath)
        except:
            rdtgs[rdtg]=[]
            rdtgs[rdtg].append(rpath)


    kk=rdtgs.keys()
    kk.sort()
    nfr=len(kk)
    nfr=min([nfr,nmaxReftrk])

    ne=len(kk)
    nb=ne-nfr
    if(nb<0):nb=0

    print
    print 'reftrks:'
    for n in range(nb,ne):
        rdtg=kk[n]
        rpaths=rdtgs[rdtg]
        for rpath in rpaths:
            age=MF.PathCreateTimeDtgdiff(rdtg,rpath)
            print "%-80s  age: %6.1f"%(rpath,age)




elif(lsopt == 'ecbufr'):


    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    sdir="%s/%s/ecbufr"%(w2.TcAdecksEcmwfDir,year)
    rpaths=glob.glob("%s/adec*%s*"%(sdir,yyyymmm1))+glob.glob("%s/adec*%s*"%(sdir,yyyymm))

    rpaths.reverse()
    rdtgs={}
    for rpath in rpaths:
        (dir,file)=os.path.split(rpath)
        tt=file.split('.')
        tt1=tt[len(tt)-2].split('_')
        rdtg=tt1[0]
        rtime="%s:%s:%s"%(tt1[2],tt1[3],tt1[4])
#        print rpath,rdtg,rtime
#        continue
        try:
            rdtgs[rdtg].append((rtime,rpath))
        except:
            rdtgs[rdtg]=[]
            rdtgs[rdtg].append((rtime,rpath))


    kk=rdtgs.keys()
    kk.sort()
    nfr=len(kk)
    nfr=min([nfr,nmaxEcbufr])

    ne=len(kk)
    nb=ne-nfr
    if(nb<0):nb=0

    rdtg1=kk[0]
    print
    print 'ecbufr:'
    for n in range(ne-1,nb,-1):
        rdtg=kk[n]
        rrs=rdtgs[rdtg]
        if(rdtg != rdtg1):
            rdtg1=rdtg
            print
        for rr in rrs:
            (rtime,rpath)=rr
            age=MF.PathCreateTimeDtgdiff(rdtg,rpath)
            print "%-80s  dtg: %s  phr: %s  age: %6.1f"%(rpath,rdtg,rtime,age)

    print



elif(lsopt == 'qpr'):


    def GetQprFiles(source,dtype):

        if(source == 'qmorph'):
            sdir=w2.NhcQmorphFinalLocal
            sdirp=w2.NhcQmorphProductsGrib
        elif(source == 'cmorph'):
            sdir=w2.NhcCmorphFinalLocal
            sdirp=w2.NhcCmorphProductsGrib

        stitle=source.upper()

        sfiles={}
        if(dtype == 'input'):
            mask="%s/*%s*"%(sdir,yyyymm)
            maskm1="%s/*%s*"%(sdir,yyyymmm1)

            files=glob.glob(maskm1)+glob.glob(mask)
            for sfile in files:
                dtg=long(sfile.split(".")[-2])
                sfiles[dtg]=sfile
            title='hourly:'
            maxfiles=10

        elif(dtype == 'prod'):
            mask="%s/*h_%s????.grb"%(sdirp,yyyymm)
            maskm1="%s/*h_%s????.grb"%(sdirp,yyyymmm1)
            files=glob.glob(maskm1)+glob.glob(mask)
            for sfile in files:
                dtg=long(sfile.split("_")[-1].split('.')[0])
                sfiles[dtg]=sfile            
            title='6-h products'
            maxfiles=5

        elif(dtype == 'globalprod'):
            mask="%s/*h_global_%s????.grb"%(sdirp,yyyymm)
            maskm1="%s/*h_global_%s????.grb"%(sdirp,yyyymmm1)
            files=glob.glob(maskm1)+glob.glob(mask)
            for sfile in files:
                dtg=long(sfile.split("_")[-1].split('.')[0])
                sfiles[dtg]=sfile
            title='6-h GLOBAL products'
            maxfiles=5

        sdtgs=sfiles.keys()
        sdtgs.sort(key=int)
        nsdtgs=len(sdtgs)

        if(nsdtgs == 0):
            print 'WWW-l2.GetQprFiles no files for dtype: ',dtype
        else:
            files=[]
            for n in range(nsdtgs-1,nsdtgs-maxfiles,-1):
                files.append(sfiles[sdtgs[n]])

        return(files,stitle,title)


    def PrintQprFiles(files,stitle,title):

        print
        print "%s %s"%(stitle,title)
        for file in files:
            print file


    sources=['qmorph','cmorph']
    dtypes=['input','prod','globalprod']

    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    for source in sources:
        for dtype in dtypes:
            (files,stitle,title)=GetQprFiles(source,dtype)
            PrintQprFiles(files,stitle,title)

    print
    print 'Curdtg: ',curdtg,' curphr: ',curphr


    #ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    #
    # fim files
    #

elif(lsopt == 'fim'):

    bfimpub=w2.EsrlPublicDirFim
    bfim9pub=w2.EsrlPublicDirFim9

    bfim="%s/FIM/FIMrun"%(w2.WjetRtfim)
    bfimx="%s/FIMX/FIMrun"%(w2.WjetRtfim)

    bfim9gwjet="%s/TACC"%(w2.WjetRtfim)
    bfim10kmewjet="%s/TACC_10km"%(w2.WjetRtfim)
    bfim9ewjet="%s/TACC_ens"%(w2.WjetRtfim)
    bfim8ewjet="%s/TACC_ens8"%(w2.WjetRtfim)

    bfim9gtacc=w2.TaccFim9Gfs
    bfim8etacc=w2.TaccFim8EnKF
    bfim9etacc=w2.TaccFim9EnKF
    bfim10kmetacc=w2.TaccFim10kmEnKF

    def GetTrackers(basedir):

        dtgs=[]
        trackers={}

        if(model != None):
            chkdtgs=mf.dtg_dtgopt_prc(model)
        else:
            chkdtgs=None


        if(chkdtgs == None):
            if(mf.find(basedir,'public')):
                mask="%s/*%s*"%(basedir,curdtg[0:6])
            else:
                mask="%s/fim_*%s*/tracker*/*"%(basedir,curdtg[0:4])
            try:
                paths=glob.glob(mask)
            except:
                paths=[]
        else:
            paths=[]
            for chkdtg in chkdtgs:
                if(mf.find(basedir,'public')):
                    mask="%s/*%s*"%(basedir,chkdtg)
                else:
                    mask="%s/fim_*%s*/tracker*/*"%(basedir,chkdtg)

                paths=paths+glob.glob(mask)

        paths.sort()
        paths=mf.uniq(paths)

        for path in paths:

            (dir,file)=os.path.split(path)


            if(not(mf.find(file,'fort.')) and
               not(mf.find(file,'namelist')) and
               not(mf.find(file,'tcvital')) and
               not(mf.find(file,'.ix')) ):

                tt=dir.split('/')
                tt=tt[len(tt)-2].split('_')
                ff=file.split('.')

                if(ff[0] == 'fim'):
                    dtg=tt[len(tt)-1][0:10]
                else:
                    if(ff[0] == 'track'):
                        dtg=ff[1]
                    elif(ff[1] == 'grib'):
                        dtg=ff[0]
                    elif(ff[1] == 'tracker'):
                        dtg=ff[0].split('-')[1]


                dtg=dtg[0:10]

                try:
                    trackers[dtg].append((file,dir,path))
                except:
                    trackers[dtg]=[]
                    trackers[dtg].append((file,dir,path))

                dtgs.append(dtg)

            dtgs=mf.uniq(dtgs)

        rc=(dtgs,trackers)
        return(rc)



    def PrintTrackers(rc,title='',lsadeck=0):

        (dtgs,trackers)=rc

        if(len(dtgs) == 0):
            return
        print
        print 'FIM tracker for: ',title,' dtgs= ',dtgs[0],' to ',dtgs[-1],' ffffffffffffffffffffffff '

        for dtg in dtgs:
            rcs=mf.uniq(trackers[dtg])
            if(not(lsadeck)):
                print
                print "DDDDD- %s -DDDDD"%(dtg)
                print "Dir: %s"%(rcs[0][1])
                print "File:",58*' ','dtg age:'


            for i in range(0,len(rcs)):
                rc=rcs[i]
                if(not(lsadeck)):
                    print "%-60s  %6.1f"%(rc[0],MF.PathCreateTimeDtgdiff(dtg,rc[2]))
                else:
                    if(mf.find(rc[0],'track.')):
                        print "%-60s  %6.1f"%(rc[2],MF.PathCreateTimeDtgdiff(dtg,rc[2]))


    if(not(onTacc)):
        rc=GetTrackers(bfimpub)
        PrintTrackers(rc,title='FIM  (/public/) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim9pub)
        PrintTrackers(rc,title='FIM9 (/public/) ',lsadeck=lsadeck)

    if(onWjet):
        rc=GetTrackers(bfim)
        PrintTrackers(rc,title='FIM     (rtfim) ',lsadeck=lsadeck)

        rc=GetTrackers(bfimx)
        PrintTrackers(rc,title='FIMX    (rtfim) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim9gwjet)
        PrintTrackers(rc,title='FIM9     (wjet) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim9ewjet)
        PrintTrackers(rc,title='FIM9EnKF (wjet) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim10kmewjet)
        PrintTrackers(rc,title='FIM10kmEnKF (wjet) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim8ewjet)
        PrintTrackers(rc,title='FIM8EnKF (wjet) ',lsadeck=lsadeck)



    if(onTacc):

        rc=GetTrackers(bfim9gtacc)
        PrintTrackers(rc,title='FIM9     (tacc) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim9etacc)
        PrintTrackers(rc,title='FIM9EnKF (tacc) ',lsadeck=lsadeck)

        rc=GetTrackers(bfim10kmetacc)
        PrintTrackers(rc,title='FIM10kmEnKF (tacc) ',lsadeck=lsadeck)




    print
    print 'Curdtg: ',curdtg,' curphr: ',curphr

    #gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
    # genstrk
    #

elif(lsopt == 'genstrk'):

    def PrintStormAdecks(model,tdtgs):

        if(mf.find(model,'ncep')):
            edir=w2.TcAdecksNcepDir
            modeltag='NCEP GEFS storm adecks from NCEP:/com --'
            emask="%s/%s/%s*/ap01*unix"%(edir,yyyy,yyyymm)
            emaskp1="%s/%s/%s*/ap01*unix"%(edir,yyyy,yyyymmm1)

        elif(mf.find(model,'cmc')):
            edir=w2.TcAdecksCmcDir
            modeltag='CMC eps storm adecks from NCEP:/com --'
            emask="%s/%s/%s*/cp01*unix"%(edir,yyyy,yyyymm)
            emaskp1="%s/%s/%s*/cp01*unix"%(edir,yyyy,yyyymmm1)


        efiles=glob.glob(emaskp1)+glob.glob(emask)
        nfe=len(efiles)
        edtgs={}

        for efile in efiles:

            edtg=efile.split('/')[7]

            if(tdtgs != None):

                for tdtg in tdtgs:
                    if(edtg == tdtg):
                        try:
                            edtgs[edtg].append(efile)
                        except:
                            edtgs[edtg]=[]
                            edtgs[edtg].append(efile)

            else:
                try:
                    edtgs[edtg].append(efile)
                except:
                    edtgs[edtg]=[]
                    edtgs[edtg].append(efile)



        kk=edtgs.keys()
        kk.sort()

        print modeltag
        ne=len(kk)
        nb=ne-nfe
        if(nb<0):nb=0

        np=ne-nb

        nmax=20
        if(np > nmax):
            nb=ne-nmax


        for n in range(nb,ne):
            edtg=kk[n]
            efiles=edtgs[edtg]
            for efile in efiles:
                (dir,file)=os.path.split(efile)
                print "%-80s  age: %6.1f"%(efile,MF.PathCreateTimeDtgdiff(edtg,efile))

        print


    yyyy=curdtg[0:4]
    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    if(model != None):
        tdtgs=mf.dtg_dtgopt_prc(model)
    else:
        tdtgs=mf.dtg_dtgopt_prc('cur-d3.cur')

    models=['ncep','cmc']
    for model in models:
        PrintStormAdecks(model,tdtgs)

    print 'Curdtg: ',curdtg,' curphr: ',curphr


    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # tcepsxml

elif(lsopt == 'tcepsxml'):


    def parselog(cards):
        datetimegots=[]
        for card in cards:

            ecmwfthere=    (mf.find(card,'z_tigge_c_ecmf_') and (mf.find(card,'glo.xml')) )
            ukmothere=     (mf.find(card,'z_tigge_c_egrr_') and (mf.find(card,'glo.xml')) )
            ncepDetthere=  (mf.find(card,'kwbc_') and ( mf.find(card,'GFS_glob_prod')) )
            ncepEpsthere=  (mf.find(card,'kwbc_') and (mf.find(card,'GEFS_glob_prod')) )
            cmcEpsthere=   (mf.find(card,'kwbc_') and (mf.find(card,'CENS_glob_prod')) )
            cmcDetthere=   (mf.find(card,'kwbc_') and (mf.find(card,'CMC_glob_prod')) )


            if(ecmwfthere or
               ukmothere or
               ncepEpsthere or
               ncepDetthere or
               cmcEpsthere or
               cmcDetthere
               ):
                tt=card.split()
                date=tt[0]
                time=tt[1]

                if(ukmothere): tag='ukmo eps'
                if(ecmwfthere): tag='ecmwf DET + eps'
                if(ncepEpsthere): tag='ncep eps'
                if(ncepDetthere): tag='ncep DET'
                if(cmcEpsthere): tag='cmc eps'
                if(cmcDetthere): tag='cmc DET'

                datetimegot="%s %s :: %s"%(date,time,tag)
                datetimegot="%s :: %s"%(time,tag)
                datetimegots.append(datetimegot)

        return(datetimegots)

    yyyy=curdtg[0:4]
    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    tbdir=w2.TcDatDir

    for model in emodels:

        lmask="%s/%s/tigge/%s/%s*/db.wget*.txt"%(tbdir,model,yyyy,yyyymm)
        lmaskp1="%s/%s/tigge/%s/%s*/db.wget*.txt"%(tbdir,model,yyyy,yyyymmm1)

        lpaths=glob.glob(lmaskp1)+glob.glob(lmask)

        print
        pcards=[]
        for lpath in lpaths:
            (dir,file)=os.path.split(lpath)

            tt=file.split('.')
            dtg=tt[len(tt)-2]
            cards=open(lpath).readlines()
            datetimegots=parselog(cards)
            for datetimegot in datetimegots:
                pcard="%-80s %s %s"%(lpath,dtg,datetimegot)
                pcards.append(pcard)


        nc=len(pcards)
        ncmax=12
        nb=nc-ncmax
        ne=nc
        if(nb < 0): nb=0
        for n in range(nb,ne):
            print pcards[n]





elif(lsopt == 'tceps'):


    def PrintStormXml(model,curdtg):

        if(mf.find(model,'ncep')):
            edir=w2.TcAdecksNcepDir
            modeltag='NCEP GEFS storm adecks:'

        elif(mf.find(model,'cmc')):
            edir=w2.TcAdecksCmcDir
            modeltag='CMC eps storm adecks:'

        elif(mf.find(model,'ukm')):
            edir=w2.TcAdecksuKmoDir
            modeltag='uKMO MOGREPS storm adecks:'

        elif(mf.find(model,'ecm')):
            edir=w2.TcAdecksEcmwfDir
            modeltag='ECMWF EPS storm adecks:'


        yearp1=str(int(year)+1)
        emask="%s/%s/*.%s????.*"%(edir,year,yyyymm)
        emaskp1="%s/%s/*.%s????.*"%(edir,year,yyyymmm1)
        (shemoverlap,cy,cyp1)=CurShemOverlap(curdtg)

        if(model == 'cmc'):
            emask="%s/%s/%s????/[c]p01*unix"%(edir,year,yyyymm)
            emaskp1="%s/%s/%s????/[c]p01*unix"%(edir,year,yyyymmm1)

        if(model == 'ncep'):
            emask="%s/%s/%s????/[a]p01*unix"%(edir,year,yyyymm)
            emaskp1="%s/%s/%s????/[a]p01*unix"%(edir,year,yyyymmm1)

        # shem
        if(shemoverlap):
            emaskyp1="%s/%s/*.%s????.*"%(edir,yearp1,yyyymm)
            emaskyp1p1="%s/%s/*.%s????.*"%(edir,yearp1,yyyymmm1)
            efiles=glob.glob(emaskyp1p1)+glob.glob(emaskyp1)+glob.glob(emaskp1)+glob.glob(emask)
        else:
            efiles=glob.glob(emaskp1)+glob.glob(emask)

        nfe=len(efiles)
        edtgs={}

        #print 'eee ',shemoverlap,emask,emaskp1,nfe
        for efile in efiles:
            (dir,file)=os.path.split(efile)
            edtg=file.split('.')[1]
            if(model == 'ncep' or model == 'cmc'):
                edir=dir.split('/')
                edtg=edir[-1]
            try:
                edtgs[edtg].append(efile)
            except:
                edtgs[edtg]=[]
                edtgs[edtg].append(efile)


        kk=edtgs.keys()
        kk.sort()

        print modeltag
        ne=len(kk)
        nb=ne-nfe
        if(nb<0):nb=0

        np=ne-nb

        nmax=nmaxTceps
        if(np > nmax):
            nb=ne-nmax


        for n in range(nb,ne):
            edtg=kk[n]
            efiles=edtgs[edtg]
            for efile in efiles:
                (dir,file)=os.path.split(efile)
                print "%-80s  age: %6.1f"%(efile,MF.PathCreateTimeDtgdiff(edtg,efile))

        print



    nmaxw=3

    year=curdtg[0:4]
    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    wdtgs={}

    twdir=w2.TcTcepsWebDir
    wmask="%s/%s/%s????/*hit*.gif"%(twdir,year,yyyymm)
    wmaskp1="%s/%s/%s????/*hit*.gif"%(twdir,year,yyyymmm1)
    wfiles=glob.glob(wmaskp1)+glob.glob(wmask)

    for wfile in wfiles:
        (dir,file)=os.path.split(wfile)
        wdtg=dir.split('/')
        wdtg=wdtg[-1]
        try:
            wdtgs[wdtg].append(wfile)
        except:
            wdtgs[wdtg]=[]
            wdtgs[wdtg].append(wfile)



    nfw=len(wfiles)
    nfw=min([nfw,nmaxw])

    kk=wdtgs.keys()
    kk.sort()

    print
    print 'Web plots -- local:'
    ne=len(kk)
    nb=ne-nfw
    if(nb<0):nb=0
    for n in range(nb,ne):
        wdtg=kk[n]
        wfiles=wdtgs[wdtg]
        for wfile in wfiles:
            (dir,file)=os.path.split(wfile)
            print "%-80s  age: %6.1f"%(wfile,MF.PathCreateTimeDtgdiff(wdtg,wfile))


    print

    wdtgs={}

    twdir=w2.TcTcepsWebDir

    wmask="%s/%s/%s????/ec.eps*strike*png"%(twdir,year,yyyymm)
    wfiles=glob.glob(wmask)

    for wfile in wfiles:
        (dir,file)=os.path.split(wfile)
        wdtg=dir.split('/')
        wdtg=wdtg[-1]
        try:
            wdtgs[wdtg].append(wfile)
        except:
            wdtgs[wdtg]=[]
            wdtgs[wdtg].append(wfile)



    nfw=len(wfiles)
    nfw=min([nfw,nmaxw])

    kk=wdtgs.keys()
    kk.sort()

    print
    print 'Web plots -- ecmwf:'
    ne=len(kk)
    nb=ne-nfw
    if(nb<0):nb=0
    for n in range(nb,ne):
        wdtg=kk[n]
        wfiles=wdtgs[wdtg]
        for wfile in wfiles:
            (dir,file)=os.path.split(wfile)
            print "%-80s  age: %6.1f"%(wfile,MF.PathCreateTimeDtgdiff(wdtg,wfile))


    print

    for model in emodels:
        PrintStormXml(model,curdtg)

else:
    print 'WWW lsopt: ',lsopt

if(diag): mf2.dTimer('all')
sys.exit()

