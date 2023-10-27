#!/usr/bin/env python 
"""%s:
purpose:

  master script for running TC analysis applications:

usages:

  %s bdtg[.edtg[.ddtg]] gfs;ukm;ngp;gsm;fg4;all -p prcopt
  
  -p prcopt:

     cliper
     tcstruct
     tc.db -- generate db cards for tcstruct
     [all]

  -k :: donocagips -- turn off cagips, e.g., bad data...
  
  -N :: norun
  -R :: realtime=1 --> go to /wxmap2/dat/tc/tcanal vice /storage2/kishou/wxmap2/dat/tc/tcanal
  -L :: keeplocal=1 -- do not rm local copy
  -T :: dotrackeronly
  -P :: dopostprocess=0 -- default is to do all vdeck, adeck, con postprocessing
  -c :: doclip=0
  
examples:

%s cur gfs
%s 2006042300.2006042312.6 gfs.jtwc

"""

import sys
import os
import glob
import string
import getopt

import mf
import w2
import TCw2 as TC

from tcanalsub import * 

#
#  defaults
#

#
# now that we've archived the data off to the nas ftp servers (share2 and share3), chkremote
#

modelopt='all'
prcopt='all'
dtgopt=None
donocagips=0
doclean=0
realtime=0
keeplocal=0
dotrackeronly=0
dopostprocess=0
doclip=0

ropt=''

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()

pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

narg=len(sys.argv)-1

if(narg >= 2):

    dtgopt=sys.argv[1]
    modelopt=sys.argv[2]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "p:VNCkRTLPc")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        print "EEE invalid getopt opt: ",opts,args
        sys.exit(2)

    for o, a in opts:
        if o in ("-p",""): prcopt=a
        if o in ("-V",""): verb=1
        if o in ("-N",""): ropt='norun'
        if o in ("-C",""): doclean=1
        if o in ("-k",""): donocagips=1
        if o in ("-R",""): realtime=1
        if o in ("-L",""): keeplocal=1
        if o in ("-T",""): dotrackeronly=1
        if o in ("-P",""): dopostprocess=0
        if o in ("-c",""): doclip=0

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


if(dtgopt == None):
    print 'EEE must set the dtg opt ...'
    sys.exit()

dd=dtgopt.split('.')
ddtg=6
if(len(dd) == 1):
    bdtg=mf.dtg_command_prc(dtgopt)
    edtg=bdtg

if(len(dd) >= 2):
    bdtg=mf.dtg_command_prc(dd[0])
    edtg=mf.dtg_command_prc(dd[1])

if(len(dd) == 3):
    ddtg=dd[2]

dtgs=mf.dtgrange(bdtg,edtg,ddtg)


fldprcdir=w2.PrcDirFlddatW2
anlprcdir=w2.PrcDirTcanalW2
datprcdir=w2.PrcDirTcdatW2

#
# change to prc dir
#
mf.ChangeDir(anlprcdir)

for dtg in dtgs:

    #
    # check for storms
    #
    tcs=TC.findtcs(dtg)
    #
    # skip if no storms
    #
    if(len(tcs) == 0):
        print 'NNNNNNNNNNN notcs at: ',dtg
        continue

    if(ropt == 'norun'):
        print 'doing: ',dtg,' model: ',modelopt,' len(tcs): ',len(tcs)
        continue
##--------------------------------------------------------------------
##
## - this should not have to be done, but handled by w2.tc.ops.dat.py
##     #
##     # run the adeck convert to get ofci/ofcl
##     #
##     if(prcopt == 'all'):
##         cmd="%s/w2.tc.ops.dat.py %s -F"%(datprcdir,dtg)
##         mf.runcmd(cmd,ropt)


    #
    # set up the directories
    #

    (cdir,bdir,prcddir,\
     odir,ogdir,osdir,otdir,oddir,opdir,\
     oadir,pdir,\
     wpddir,wgddir)=SetTcanalDirs(dtg,realtime)


    #
    # reconstructe tcstruct db
    #


    if(prcopt == 'tc.db'):
        dorealtime=''
        if(realtime): dorealtime='-R'
        cmd="%s/w2.tc.tcstruct.py %s %s %s"%(anlprcdir,dtg,prcopt,dorealtime)
        mf.runcmd(cmd,ropt)
        continue

    #
    # copy of? wxmap adecks to trk dir
    #

    CpOfcAdecks(dtg,otdir)

    #
    # run cliper only once
    #
    if(prcopt == 'cliper' or prcopt == 'all' and not(dotrackeronly) and doclip):
        cmd="%s/w2.tc.cliper.py %s"%(anlprcdir,dtg)
        mf.runcmd(cmd,ropt)


    models=SetModels(dtg,modelopt)

    
    for model in models:

        iokrecoverremote=0
        iokrecoverarchive=0

        #
        # us os.path.exist and ftp to check for local/archive/remote data
        #
        print model,w2.IsModel2(model)
        if(w2.IsModel2(model)):

            ioklocal=w2.IsFldDataThere(model,dtg)
            iokarchive=w2.IsFldDataArchive(model,dtg)
            iokremote=w2.IsFldDataRemote(model,dtg)

        else:

            ioklocal=w2.IsFldDataThere(model,dtg)
            iokarchive=w2.IsFldDataArchive(model,dtg)
            iokremote=w2.IsFldDataRemote(model,dtg)

        print 'iiiiiiiiiiiiiiiiiii ',ioklocal,iokarchive,iokremote

        #
        # not local, but on archive, recover
        #
        if(ioklocal == 0 and iokarchive == 1 and iokremote == 0 ):
            rc=w2.RecoverFldDataArchive2Local(model,dtg)
            ioklocal=w2.IsFldDataThere(model,dtg)
            if(ioklocal):
                iokrecoverarchive=1

        if(ioklocal == 0 and iokarchive == 0 and iokremote == 1 ):
            rc=w2.RecoverFldDataRemote2Local(model,dtg)
            ioklocal=w2.IsFldDataThere(model,dtg)
            if(ioklocal):
                iokrecoverremote=1


            if(ioklocal == 0):

                print 'WWWWWWWWWWWWWWW Sumimasen!!! local/archive/remote data ga arimensen ka, mou ichi dou for: ',dtg
                if(len(dtgs) == 1):
                    sys.exit()
                else:
                    continue

            print "ioklocal: %d  iokarchive: %d  iokremote: %d  iokrecoverremote: %d   iokrecoverarchive: %d"%\
                  (ioklocal,iokarchive,iokremote,iokrecoverremote,iokrecoverarchive)


        if(prcopt == 'tcstruct' or prcopt == 'all'):

            nocagipsopt=''
            docleanopt=''
            dorealtime=''
            dotrackeropt=''
            
            if(donocagips): nocagipsopt='-c'
            if(doclean): docleanopt='-C'
            if(realtime): dorealtime='-R'
            if(dotrackeronly): dotrackeropt='-T'
               
            cmd="%s/w2.tc.tcstruct.py %s %s -p all %s %s %s %s"%(anlprcdir,dtg,model,
                                                                 docleanopt,nocagipsopt,
                                                                 dorealtime,dotrackeropt)
            
            mf.runcmd(cmd,ropt)

        #
        # if did a recovery; blow local away
        #

        if(iokrecoverremote == 1 or iokrecoverarchive == 1):
            #
            # check first... 
            #
            ioklocal=w2.IsFldDataThere(model,dtg)
            if(ioklocal and not(keeplocal)):
                rc=w2.RemoveRecoveredFldDataLocal(model,dtg)

            models=SetModels(dtg,modelopt)


        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #
        # postprocess
        #

        if(dopostprocess):
            TcAnalPost(dtg,model)



    #
    # rsync from real-time to permanent, if realtime
    #

    if(realtime):
        cmd="%s/w2.tc.rsync.realtime.dat.tcanal.2.perm.py cur"%(anlprcdir)
        mf.runcmd(cmd,ropt)

        
sys.exit()




