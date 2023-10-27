import os,sys,glob,time,getopt

import mf


def CmdLine():

    __doc__="""%s

purpose:

usages:

  %s bdtg[.edtg[.ddtg]] model -p 'all'|plot -t 'all'|tau -O
  %s cur-24.cur-6 all -O   -- redo all plots for a dtgrange, overwrite
  %s cur-6 gfs -a europe -p basemap  :: make basemap for europe
models:
  ecm | ngp | gfs | ukm | cmc | all

-N  -- norun
-O  -- override=1 (force plot)
-I  -- interact
-T  -- test (no rm of .gs)
-A  0|1|2 doarchive=int(a) ; make plots in /w21/weba
    1 -- use /dat/nwp2/w2flds (i.e., for gfs2 and fim8 if data not on /public)
    2 -- use /dat/nwp2

-F :: dow2flds=1 :: use wgrib filtered fields

-c ctltype  :: ctltype = 'mand' | 'pr' | 'hl'

examples:

 %s cur-12 ngp -t 0 -a tropsio -p prp -O -I  | interactively create tau0 prp plot for tropsio and overwrite (-O disable exist check)
 
(c) 2006-2010 Michael Fiorino, NOAA ESRL
"""

    curdtg=mf.dtg()
    curphr=mf.dtg('phr')
    curyear=curdtg[0:4]
    curtime=mf.dtg('curtime')
    curdir=os.getcwd()
    pypath=sys.argv[0]
    (pydir,pyfile)=os.path.split(pypath)

    #
    #  defaults
    #
    ropt=''
    verb=0

    plotopt='all'
    tauopt='all'
    areaopt='all'

    override=0
    interact=0
    dotest=0
    dow2flds=0
    #
    # use the mandatory level version
    #
    ctltype='mand'
    docleanplt=0
    doarchive=0

    narg=len(sys.argv)-1

    if(narg >= 2):

        dtgopt=sys.argv[1]
        areaopt=sys.argv[2]

        try:
            (opts, args) = getopt.getopt(sys.argv[3:], "NVO")

        except getopt.GetoptError:
            mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
            sys.exit(2)

        for o, a in opts:
            if o in ("-N",""): ropt='norun'
            if o in ("-V",""): verb=1
            if o in ("-O",""): override=1
    else:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(1)

    rc=(
        curdtg,curphr,curyear,curtime,curdir,pypath,pydir,pyfile,ropt,verb,override,
        dtgopt,areaopt,
        )

    return(rc)




