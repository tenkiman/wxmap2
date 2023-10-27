#!/usr/bin/env python

"""%s

purpose:

 list nwp fld files

  -A add to list in spinning archive
  -d dtgopt
  -V verb for lsopt='arch'

examples:

%s dat ngp                  # model data
%s grf ngp -d cur-12        # plots model data cur-12 dtg
%s dat all                  # all model data for curdtg
%s dat all-24|all-d1,2,3,4  # all model data from -d1,2,3,4 dtg
%s dat.in ngp               # all dtgs in cagips dir
%s arch all -d 2005      # looking for missing/bad all model fields in archive for 2005
%s arch avn -d 200501    # looking for missing/bad avn fields in archive for 200501

%s wgrib all -O             # create *wgrib.txt



"""

import os,sys,time
import getopt,glob

import mf
import w2
import TCw2 as TC
import nawips

lsopt='dat'
model=''
verb=0

ropt=''

curdtg=mf.dtg()
(tttdtg,curphr)=mf.dtg_phr_command_prc(curdtg) 
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

dtgopt='cur'
doarch=0
dostatus=0
dooverride=0
doregen=0

mbfact=1.0/(1024.0*1024.0)

narg=len(sys.argv)-1


if(narg >= 1):

    lsopt=sys.argv[1]
    if(narg > 1): model=sys.argv[2]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "OSACDGVd:R")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-S",""): dostatus=1
        if o in ("-A",""): doarch=1
        if o in ("-C",""): prcopt='Cfiles'
        if o in ("-D",""): prcopt='dat'
        if o in ("-G",""): prcopt='grib'
        if o in ("-O",""): dooverride=1
        if o in ("-d",""): dtgopt=a
        if o in ("-V",""): verb=1
        if o in ("-R",""): doregen=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

#LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
#
#  local
#



def PrintFileStatus(file,ptype,nfields=None):
    
    tt=file.split('.')
    dtg=tt[(len(tt)-2)]
    siz=os.path.getsize(file)
    ctime=os.path.getctime(file)
    utctime=time.gmtime(ctime)

    cyr=utctime[0]
    cmo=utctime[1]
    cda=utctime[2]
    chr=utctime[3]
    cmn=utctime[4]

    cdtgmn="%04d%02d%02d%02d%02d"%(cyr,cmo,cda,chr,cmn)
    dtgmn="%s%02d"%(dtg,0)
    phr=mf.dtgmndiff(dtgmn,cdtgmn)

    ftime="%H:%M %Y%m%d%H"
    ptime=time.strftime(ftime,utctime)
    rsiz=float(siz)*mbfact
    csiz="%6.2f"%(rsiz)
    if(len(tt) == 5):
        cfile="%s.%s.%s"%(tt[0],tt[1],tt[2])
    else:
        cfile="%s.%s"%(tt[0],tt[1])


    if(phr > 100.0):
        phr=-99.
        
    cdtg="%s % +5.1f %s:00"%(dtg[0:10],phr,dtg[8:10])
    if(len(cfile) > 10 or ptype == 'all'):
        if(nfields != None):
            pstatus="%-14s %s Mb % 4d %s <-> %s"%(cfile,csiz,nfields,cdtg,ptime)
        else:
            pstatus="%-14s %s Mb %s <-> %s"%(cfile,csiz,cdtg,ptime)
            
    else:
        if(nfields != None):
            pstatus="%-7s %s Mb % 4d %s <-> %s"%(cfile,csiz,nfields,cdtg,ptime)
        else:
            pstatus="%-7s %s Mb %s <-> %s"%(cfile,csiz,cdtg,ptime)
    return(pstatus)


def ParseGribParms(tt):
    card1=tt[0]
    ttt=card1.split()
    var=ttt[3]
    tau=ttt[len(ttt)-2]

    if(ttt[len(ttt)-1] == 'anl:'):
        tau='000hr'
        
    card2=tt[1][:-1]
    ttt=card2.split('=')
    vardesc=ttt[1]

    card3=tt[2]
    ttt=card3.split()
    ni=ttt[9]
    nj=ttt[11]

    card4=tt[4]
    ttt=card4.split()
    blat=ttt[2]
    elat=ttt[4]
    dlat=ttt[6]
    nij=ttt[8]

    card5=tt[5]
    ttt=card5.split()
    blon=ttt[1]
    elon=ttt[3]
    dlon=ttt[5]
    grid=ttt[6]+" "+ttt[7]+" "+ttt[8]


    rc=((
        (var,tau),
        (vardesc),
        (ni,nj),
        (blat,elat,dlat,nij),
        (blon,elon,dlon,grid),
        ),

        (
        card1,
        card2,
        card3,
        card4,
        card5
        )
        
        )
    
    return(rc)

#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
#
# main
#
    
if(lsopt != 'arch'):
    (dtg,phr)=mf.dtg_phr_command_prc(dtgopt) 

if(doregen):
    w2.W2BaseDirDat=w2.W2RegenBaseDirDat

if(lsopt == 'wgrib'):

    maskdtg=''
    ptype='single'
    if(model=='all'):
        models=w2.wxModels
        maskdtg=curdtg[0:8]
        ptype='all'
    elif(model=='all-24' or model=='all-d1'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-24)
        maskdtg=odtg[0:8]
        ptype='all'
    elif(model=='all-48' or model=='all-d2'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-48)
        maskdtg=odtg[0:8]
        ptype='all'
    elif(model=='all-72' or model=='all-d3'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-72)
        maskdtg=odtg[0:8]
        ptype='all'
    elif(model=='all-96' or model=='all-d4'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-96)
        maskdtg=odtg[0:8]
        ptype='all'
    elif(model=='all-120' or model=='all-d5'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-120)
        maskdtg=odtg[0:8]
        ptype='all'
    else:
        models=[model]

    for model in models:
        print
        ddir=w2.NwpDataBdir(model)
        os.chdir(ddir)
        grbfiles=glob.glob("*%s*%s*grb"%(model,maskdtg))
        grbfiles.sort()
        for grbfile in grbfiles:
            (file,ext)=os.path.splitext(grbfile)
            wgribfile="%s.wgrib.txt"%(file)
            nfields=0
            if(not(os.path.exists(wgribfile))):
                cmd="wgrib %s > %s"%(grbfile,wgribfile)
                mf.runcmd(cmd,ropt)

            if(dooverride):
                cmd="wgrib %s > %s"%(grbfile,wgribfile)
                mf.runcmd(cmd,ropt)

            cmd="wc -l %s"%(wgribfile)
            rc=os.popen(cmd).readlines()
            rc=rc[0].split()
            nfields=int(rc[0])
                
            pstatus=PrintFileStatus(grbfile,ptype,nfields)
            print pstatus
            

    print
    print 'CCCCC=====> curdtg: ',curdtg,' curphr: ',curphr,' <=====CCCCC'
    print


if(mf.find(lsopt,'cur') or len(lsopt)==10):

    models=w2.wxModels2

    for model in models:

        if(w2.IsModel2(model)):
            ddtg=w2.Model2DdtgData(model)
            if(ddtg == 12):
                bdtg=mf.dtg_command_prc(lsopt,curdtg12=0)
            else:
                bdtg=mf.dtg_command_prc(lsopt,curdtg12=0)
                
            dtgs=mf.dtgrange(mf.dtginc(bdtg,0),bdtg,ddtg)

            for dtg in dtgs:
                (rc,latesttau)=w2.Model2DataPathsStatus(model,dtg,doreport=2,dowgribinv=0)

if(lsopt == 'dat'):

    maskdtg=''
    ptype='single'
    if(model=='all'):
        models=w2.wxModels
        maskdtg=curdtg[0:8]
        ptype='all'
    elif(model=='all-24' or model == 'all-d1'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-24)
        maskdtg=odtg[0:8]
        ptype='all'
    elif(model=='all-48'or model == 'all-d2'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-48)
        maskdtg=odtg[0:8]
        ptype='all'
    elif(model == ''):
        models=w2.Nwp2Models
        ptype='all'
    else:
        models=[model]

    for model in models:

        if(w2.IsModel2(model)):
            ddtg=w2.Model2DdtgData(model)
            if(ddtg == 12):
                bdtg=mf.dtg12()
            else:
                bdtg=curdtg
                
            dtgs=mf.dtgrange(mf.dtginc(bdtg,-72),bdtg,ddtg)

            print
            for dtg in dtgs:
                (rc,latesttau)=w2.Model2DataPathsStatus(model,dtg,doreport=1)

        else:
            print "WWW dat dtg command not available for non-nwp2 models, use l.py cur???"
	    sys.exit() 
            if(doarch):
                (ddir,ddira,ddirat,fmask)=nawips.NawipsModelDir(model,dtg)
                os.chdir(ddira)
                datfiles=glob.glob("%s*f120"%(fmask))
                datfiles.sort()
                for datfile in datfiles:
                    print datfile

            else:
                ddir=w2.NwpDataBdir(model)
                mf.ChkDir(ddir,'mk')

                os.chdir(ddir)
                datfiles=glob.glob("%s.*%s*grb"%(model,maskdtg))
                datfiles.sort()
                if(ptype == 'all'): print 
                for datfile in datfiles:
                    pstatus=PrintFileStatus(datfile,ptype)
                    print pstatus

    print
    print 'CCCCC=====> curdtg: ',curdtg,' curphr: ',curphr,' <=====CCCCC'
    print

elif(lsopt == 'grf'):

    maskdtg=''
    ptype='single'
    if(model=='all'):
        models=w2.wxModels
        maskdtg=curdtg[0:8]
        ptype='all'
    elif(model=='all-24'):
        models=w2.wxModels
        odtg=mf.dtginc(curdtg,-24)
        maskdtg=odtg[0:8]
        ptype='all'
    else:
        models=[model]
        maskdtg=dtg

    for model in models:
        gdir="%s/%s"%(w2.W2ModelPltDir(model,'full'),dtg)
        print 'gdir: ',gdir
        os.chdir(gdir)
        datfiles=glob.glob("%s??.???.*png"%(model))
        datfiles.sort()
        if(ptype == 'all'): print 
        for datfile in datfiles:
            print datfile

        
            
elif(lsopt == 'dat.in'):

    dowgrib=0
    if(model == 'fg4'):
        ddir=w2.NasaFldIdirPcmdi
    else:
        ddir=w2.NwpDataBdir(model)
        (cdir,icode)=w2.CagipsModelDir(model)
    os.chdir(cdir)
    ficode=icode[len(icode)-1]
    print 'qqq ',cdir,ficode,dtg
    fmask="*%s*%s*"%(ficode,dtg)
    fmask="*%s*%s*"%(ficode,dtg[0:4])
    if(model == 'all'): fmask="*%s*"%(dtg)
    cmd="find . -name \"%s\" -print | cut -c0-120"%(fmask)
    files=os.popen(cmd).readlines()
    fields=[]
    for file in files:
        file=file[2:-1]
        if(dowgrib):
            cmd="wgrib -V %s"%(file)
            wgribout=os.popen(cmd).readlines()
            siz=os.path.getsize(file)
            rc=ParseGribParms(wgribout)
            nij=rc[0][3][3]
            card4=rc[1][3]
            card2=rc[1][1]
            var=rc[0][1]
            field="%-12d %s :: %s : %s :: %s"%(siz,file,nij,var,card2)
            fields.append(field)
        else:
            #US058GMET-GR1mdl.0058_0240_14400F0RL2006091200_0105_000100-000000wnd_vcmp
            #14400F0RL2006091200_0105_000100-000000wnd_vcmp
            tt=file.split('_')[2]
            tau=tt[0:5]
            type1=tt[5:7]
            type2=tt[7:9]
            basedtg=tt[9:19]
            #print 'tau... ',tau,type1,type2,basedtg
            fields.append(basedtg)

    if(len(fields) > 0):
        maxprint=160
        fields.sort()
        fields=mf.uniq(fields)
        for field in fields:
            print field[0:maxprint]
    #mf.runcmd(cmd,ropt)

elif(lsopt == 'arch'):

    if(model == 'all'):
        models=['gfs','ngp','ukm','ecm','cmc']
    else:
        models=[model]

    dtg=dtgopt
    
    if(len(dtg) == 4):
        byyyymm="%s01"%(dtg)
        eyyyymm="%s12"%(dtg)
    elif(len(dtg) == 6):
        byyyymm="%s"%(dtg)
        eyyyymm="%s"%(dtg)
    
    yyyymms=mf.yyyymmrange(byyyymm,eyyyymm)

    for model in models:
        print
        print 'AAAMMMMMM model: ',model,' <-------'
        
        
        for yyyymm in yyyymms:

            byyyymm=yyyymm
            eyyyymm=mf.yyyymminc(byyyymm,1)

            bdtg="%s0100"%(byyyymm)
            edtg="%s0100"%(eyyyymm)


            mdtau=w2.ModelDdtgData(model)

            (ftpserver,remotedir,localdir,localarchdir,
             mask,renmask,modelrename)=w2.ModelArchiveDirs(model,dtg)

            mask="%s*%s*grb"%(model,yyyymm)

            tdtgs=mf.dtgrange(bdtg,edtg,mdtau)

            nmissing=0
            missingdtgs=[]

            for tdtg in tdtgs[:-1]:
                grbsizmin=w2.ModelMinGrbSiz(model,tdtg[8:10])
                paths=glob.glob("%s/%s*%s*grb"%(localarchdir,model,tdtg))

                if(len(paths) > 0):
                    for path in paths:
                        siz=os.path.getsize(path)
                        if(verb):
                            print 'AAA --------:    ',tdtg,siz,path
                        if(siz < grbsizmin):
                            print 'AAA low size:    ',tdtg,siz,path
                else:
                    missingdtgs.append(tdtg)
                    nmissing=nmissing+1


            if(nmissing > 0):
                print
                print "AAA: %s  yyyymm: %s  nmissing: %d"%(model,yyyymm,nmissing)
                if(verb):
                    for missingdtg in missingdtgs:
                        print "AAA: %s  missing dtgs: %s"%(model,missingdtg)


    sys.exit()
                    



