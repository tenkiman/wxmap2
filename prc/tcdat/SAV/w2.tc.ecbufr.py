#!/usr/bin/env python

"""%s

purpose:

  cp and crack ecmwf bufr file

examples:

%s cur

  -O override and force reprocess
  -J do NOT do ftp for jtwc
  
"""

from tcbase import *
import ATCF


def CleanAdeck(dtg,iapath,taumax=18,maxdist=300.0,doDtgFiltOnly=1,verb=0):

    ocards=[]

    adecks={}

    good={}
    n0s=[]

    # -- filter out the dtg
    #
    
    tcards=[]

    icards=open(iapath).readlines()
    for card in icards:
        tt=card.split(',')
        idtg=tt[2].strip()
        if(dtg == idtg):
            tcards.append(card)


    if(doDtgFiltOnly): return(tcards)

    icards=tcards

    # -- now do clean up
    ncards=len(icards)
    for n in range(0,ncards):
        icard=icards[n]
        aid=tt[4]
        tau=int(tt[5])
        if(tau == 0): n0s.append(n)


    n0s.append(ncards-1)
    good={}
    
    for nn in range(0,len(n0s)-1):
        nbeg=n0s[nn]
        nend=n0s[nn+1]
        n0len=nend-nbeg

        if(n0len > 1):
            tt0=icards[nbeg].split(',')
            tau0=int(tt0[5])
            clat0=tt0[6]
            clon0=tt0[7]
            (rlat0,rlon0)=Clatlon2Rlatlon(clat0,clon0)
            

            tt1=icards[nbeg+1].split(',')
            tau1=int(tt1[5])
            clat1=tt1[6]
            clon1=tt1[7]
            (rlat1,rlon1)=Clatlon2Rlatlon(clat1,clon1)

            distp1=gc_dist(rlat0,rlon0,rlat1,rlon1)
        dtg=tt[2].strip()
        aid=tt[4]
        tau=int(tt[5])
        if(tau == 0): n0s.append(n)


    n0s.append(ncards-1)
    good={}
    
    for nn in range(0,len(n0s)-1):
        nbeg=n0s[nn]
        nend=n0s[nn+1]
        n0len=nend-nbeg

        if(n0len > 1):
            tt0=icards[nbeg].split(',')
            tau0=int(tt0[5])
            clat0=tt0[6]
            clon0=tt0[7]
            (rlat0,rlon0)=Clatlon2Rlatlon(clat0,clon0)
            

            tt1=icards[nbeg+1].split(',')
            tau1=int(tt1[5])
            clat1=tt1[6]
            clon1=tt1[7]
            (rlat1,rlon1)=Clatlon2Rlatlon(clat1,clon1)

            distp1=gc_dist(rlat0,rlon0,rlat1,rlon1)

            if(tau1 >= taumax or distp1 > maxdist):
                good[nn]=0
            else:
                good[nn]=1


        else:
            good[nn]=1

            
        for n in range(nbeg,nend):
            tt=icards[n].split(',')
            aid=tt[4]
            tau=int(tt[5])
            if(good[nn] == 0): continue
            
            ocards.append(icards[n])
            if(verb): print "%5d %3d"%(n,tau),good[nn],icards[n].split(',')[0:8]

        if(verb): print
        

    return(ocards)



lsopt='dat'
model='ngp'

ropt=''

curdtg=mf.dtg()
(tttdtg,curphr)=mf.dtg_phr_command_prc(curdtg) 
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)


doftp4jtwc=0

dtgopt='cur'
doarch=0
dosleep=0
dooverride=0
docleanDtg=0
verb=0

mbfact=1.0/(1024.0*1024.0)

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "OSACDGNVJ")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-S",""): dosleep=1
        if o in ("-A",""): doarch=1
        if o in ("-C",""): docleanDtg=1
        if o in ("-D",""): prcopt='dat'
        if o in ("-G",""): prcopt='grib'
        if o in ("-O",""): dooverride=1
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-J",""): doftp4jtwc=0

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


dtgs=mf.dtg_dtgopt_prc(dtgopt)

def GetTcIds(dtg,ddir):

    dtg1=dtg[0:8]+'00'
    dtg2=dtg[0:8]+'12'

    (stmids1,tcs1)=tD.getDtg(dtg1)
    (stmids2,tcs2)=tD.getDtg(dtg2)

    tcs=tcs1

    otcs=[]
    
    for stmid in stmids1:
        tt=tcs1[stmid]
        tcdtg=dtg1
        tcid=stmid.split('.')[0]
        tcvmax=int(tt[2])
        tcrlat=tt[0]
        tcrlon=tt[1]
        if(tcrlon > 180.0): tcrlon=tcrlon-360.0
        tccard="%s %3s % 7.2f % 7.2f %3i"%(tcdtg,tcid,tcrlat,tcrlon,tcvmax)
        otcs.append(tccard)

    for stmid in stmids2:
        tt=tcs2[stmid]
        tcdtg=dtg2
        tcid=stmid.split('.')[0]
        tcvmax=int(tt[2])
        tcrlat=tt[0]
        tcrlon=tt[1]
        if(tcrlon > 180.0): tcrlon=tcrlon-360.0
        tccard="%s %3s % 7.2f % 7.2f %3i"%(tcdtg,tcid,tcrlat,tcrlon,tcvmax)
        otcs.append(tccard)

    otc="%2i"%(len(otcs))
    otccards="""%s"""%(otc)

    for otc in otcs:
        otccards="""%s
%s"""%(otccards,otc)

    otcpath="%s/tcposit.%s.txt"%(ddir,dtg[0:8])

    mf.WriteCtl(otccards,otcpath)

    return(otcpath)


doadeck=1
server='moonfish.nhc.noaa.gov'

if(onWjet):
    sdir=EcmwfBufrJetDir
    print 'sssssssssssssssss',sdir
else:
    sdir=EcmwfBufrLocalDir

####oadir="/lfs2/projects/fim/fiorino/tmp/adeck/ecbufr"
oadir="/lfs1/projects/fim/fiorino/tmp/adeck/ecbufr"

bufrcracker='ectcbufr2adeck.x'

tD=TcData(dtgopt=dtgopt)

for dtg in dtgs:

    curdtghms=mf.dtg('dtg_hms')
    
    yyyy=dtg[0:4]
    yyyymmdd=dtg[0:8]

    adir="%s/%s"%(TcAdecksEcmwfDir,yyyy)
    mf.ChkDir(adir,'mk')

    tdir=adir

    bmask="%s/ec*%s*"%(sdir,yyyymmdd)
    bpaths=glob.glob(bmask)

    doClean=1
    if(verb): print bmask

    if(len(bpaths) > 0):

        nf=0
        for bpath in bpaths:


            (dir,file)=os.path.split(bpath)

            oafile="adeck.ecmwf.tcbufr.%s_%s.txt"%(dtg,curdtghms)
            oapath="%s/%s"%(oadir,oafile)
            oamask="adeck.ecmwf.tcbufr.%s*.txt"%(dtg)

            iapath="/tmp/adeck.ecmwf.txt"

            #efile="ectc.tcbufr.%s_%s.txt"%(dtg,curdtghms)
            #oepath="%s/%s"%(oadir,efile)
            
            tpath="%s/%s"%(tdir,file)

            bsiz=MF.GetPathSiz(bpath)
            tsiz=MF.GetPathSiz(tpath)
            print ' BBB: %100s'%(bpath),' siz: ',bsiz
            print ' TTT: %100s'%(tpath),' siz: ',tsiz
            print 'IAAA: %100s'%(iapath)
            print 'OAAA: %100s'%(oapath)
            #print 'OEEE: ',oepath

            if(docleanDtg):
                kfiles=glob.glob("%s/%s"%(oadir,oamask))
                for kfile in kfiles:
                    print 'KKKilling: ',kfile
                    os.unlink(kfile)
                                 

            if(tsiz == None or bsiz > tsiz or dooverride):

                tcpath=GetTcIds(dtg,adir)

                print 'PPP tccpath: ',tcpath
                print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPP process bufr file ',bpath
                cmd="cp %s %s"%(bpath,tpath)
                mf.runcmd(cmd,ropt)

                if(verb):
                    #cmd="%s -i %s -t %s -o %s -e %s -v"%(bufrcracker,tpath,tcpath,oapath,oepath)
                    if(doClean):
                        cmd="%s -i %s -t %s -o %s -v"%(bufrcracker,tpath,tcpath,iapath)
                    else:
                        cmd="%s -i %s -t %s -o %s -v"%(bufrcracker,tpath,tcpath,oapath)
                else:
                    #cmd="%s -i %s -t %s -o %s -e %s"%(bufrcracker,tpath,tcpath,oapath,oepath)
                    if(doClean):
                        cmd="%s -i %s -t %s -o %s"%(bufrcracker,tpath,tcpath,iapath)
                    else:
                        cmd="%s -i %s -t %s -o %s"%(bufrcracker,tpath,tcpath,oapath)
                    
                mf.runcmd(cmd,ropt)

                # -- clean up the adeck from the cracker
                #
                if(doClean):
                    oacards=CleanAdeck(dtg,iapath,verb=verb)
                    MF.WriteList2Path(oacards,oapath)

                if(doftp4jtwc and ropt != 'norun'):

                    localdir="%s/%s/wxmap"%(TcAdecksEcmwfDir,yyyy)
                    remotedir='ecmwf'
                    mask="wx*%s*"%(dtg)
                    mf.doFTPsimple(server,localdir,remotedir,mask,opt='ftp.put')

                    mask="a*%s*.dat"%(dtg[0:4])
                    mf.doFTPsimple(server,localdir,remotedir,mask,opt='ftp.put')

                print 'OAAA: %100s'%(oapath)


            nf=nf+1
            
        else:
            print
            print '00000000 bufr file: ',bpath,""" hasn't changed size curdtghms: """,curdtghms
            print
        


sys.exit()

clean
