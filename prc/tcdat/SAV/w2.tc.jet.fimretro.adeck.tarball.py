#!/usr/bin/env python

from M import *
MF=MFutils()

# -- 20140407 -- 2011-2013 retro
#
bdir='/lfs2/projects/fim-njet'

retroruns=[
#    'FIM9RETRO_HFIP',   -- op gsi for 2011 vice gsi-enkf
    'FIM9RETRO_HFIP_2014',
    ]


tdir='/lfs2/projects/fim/fiorino/tmp/adeck/retro'
MF.ChkDir(tdir,'mk')

dopost2=0

if(dopost2):

    # from post2

    for run in retroruns:

        ddir="%s/%s"%(bdir,run)
        runs=glob.glob("%s/??????????"%ddir)

        otdir="%s/%s"%(tdir,run)
        MF.ChkDir(otdir,'mk')

        for r in runs:

            trkdir="%s/fim*"%(r)
            adeck=glob.glob("%s/track.*"%(trkdir))

            if(len(adeck) == 1):
                cmd="cp -n -v %s %s/."%(adeck[0],otdir)
                mf.runcmd(cmd,'quiet')
            else:
                print 'no data for: ',run

        tarball="%s.trackers.tgz"%(run)
        MF.ChangeDir(tdir)
        cmd="tar -czvf %s %s/."%(tarball,run)
        mf.runcmd(cmd,'')

    sys.exit()



dotar=1
override=1

if(not(dotar)): sys.exit()

# -- directly from retro
#
postfix=None
#postfix='hyb'

for run in retroruns:

    ddir="%s/%s"%(bdir,run)
    runs=glob.glob("%s/FIMrun/fim_*"%ddir)
    if(len(runs) == 0):
        runs=glob.glob("%s/fim_*"%ddir)

    if(postfix != None):
        otdir="%s/%s_%s"%(tdir,run,postfix)
    else:
        otdir="%s/%s"%(tdir,run)
    MF.ChkDir(otdir,'mk')

    for r in runs:

        taus=[]
        trkdir="%s/tracker_C"%(r)
        trackers=glob.glob("%s/*"%(trkdir))

        for t in trackers:
            tau=t.split('/')[-1]
            taus.append(int(tau))

        taus=mf.uniq(taus)

        if(len(taus) == 0): continue

        finaltau=taus[-1]
        latesttracker="%s/%d"%(trkdir,finaltau)

        adeck=glob.glob("%s/track.*"%(latesttracker))

        cpopt='-n -v'
        cpropt='quiet'
        cpropt=''
        if(override): cpopt='-v'
        
        if(len(adeck) == 1):
            cmd="cp -n -v %s %s/."%(adeck[0],otdir)
            #mf.runcmd(cmd,'quiet')
            mf.runcmd(cmd,cpropt)
        else:
            print 'no data for: ',run,latesttracker

    if(postfix != None):
        tarball="%s.%s.trackers.tgz"%(run,postfix)
    else:
        tarball="%s.trackers.tgz"%(run)


    MF.ChangeDir(otdir,verb=1)
    MF.ChangeDir('../..')

    if(postfix != None):
        otrun="%s_%s"%(run,postfix)
    else:
        otrun=run
    cmd="tar -czvf %s retro/%s/."%(tarball,otrun)
    mf.runcmd(cmd,'')
        
sys.exit()



