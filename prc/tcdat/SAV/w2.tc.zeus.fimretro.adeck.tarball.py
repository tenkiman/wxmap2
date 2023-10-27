#!/usr/bin/env python

from M import *
MF=MFutils()

retroruns=[
    'FIMRETRO2517a',
    'FIMRETRO2517b',
    'FIMRETRO2517c',
    'FIMRETRO2517d',
    'FIMRETRO2517e',
    'FIMRETRO2517f',
    'FIMRETRO2517g',
    ]
bdir='/scratch1/portfolios/BMC/fim'


retroruns=[
    'FIM9RETRO',
    ]
bdir='/scratch1/portfolios/BMC/fim/fiorino/rtfim/dat'


retroruns=[
    'FIMRETRO_janjic_pgf',
    ]
bdir='/scratch2/portfolios/BMC/rtfim'

retroruns=[
    'FIMRETRO_r2972_jan0',
    'FIMRETRO_r2972_jan1',
    'FIMRETRO_r2972_jan2',
    ]

retroruns=[
    'FIMRETRO_r2972_jan0_RED_DIFF3',
    'FIMRETRO_r2972_jan1_RED_DIFF3',
    'FIMRETRO_r2972_jan2_RED_DIFF3',
    ]

retroruns=[
    'FIMRETRO_r2972_jan0_RED_DIFF3',
    ]
bdir='/scratch2/portfolios/BMC/fim'
retroruns=[
    'FIMRETRO_r2972_jan0_intsm50',
    ]

# -- 2013 hfip demo retro
#
bdir='/scratch2/portfolios/BMC/fim'
retroruns=[
    'FIMRETRO_r3162_g9',
    ]
# -- redone with reanal using hybrid 2010-11 -- same as used in hwrf
#
bdir='/scratch2/portfolios/BMC/fim'
retroruns=[
    'FIMRETRO_r3162_g9_V',
    ]


# -- 20140101 -- may 2012 physics
#
bdir='/scratch2/portfolios/BMC/fim'
retroruns=[
    'FIMRETRO_r3585_v3',
    'FIMRETRO_r3585_v4',
    ]


# -- 20140422 -- hfip 2014 retro
#
bdir='/scratch2/portfolios/BMC/fim'
retroruns=[
    'FIM9RETRO_HFIP_2014',
    ]

# -- 20140 -- hfip 2014 retro
#
bdir='/scratch2/portfolios/BMC/fim'
retroruns=[
#    'FIM9RETRO_new_interp',
    'FIMRETRO_new_interp',
    ]

tdir='/scratch1/portfolios/BMC/fim/fiorino/tmp/adeck/retro'
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

        print 'qqqqqqqq ',trkdir

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

    
    # --rerun of 3162
    tarball="%s.new.trackers.tgz"%(run)

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



