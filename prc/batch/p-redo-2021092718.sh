#!/bin/sh

runcmd='/data/w22/run.cron.bash'
w2pdir='/data/w22/prc'
w2prjdir='/data/w22/prj'
ptmpdir="/ptmp"

sdate=`date`
echo 'START: '$sdate
 
# -- goes eps

$runcmd "$w2pdir/flddat/w2-fld-wget-mirror-gfs-stbgoes.py cur-18.cur"            >> $ptmpdir/log-w2-fld-wget-mirror-gfs-stbgoes.py.GFS2 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-ecmwf-wmo-essential-bufr-json.py cur-18.cur-6"      >> $ptmpdir/log-w2-tc-ecmwf-wmo-essential-bufr-json.py-EPS 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-all-eps.py cur-18.cur-6 -2"                         >> $ptmpdir/log-w2-tc-all-eps.py.EPSPLOTTIGGENCEP 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-all-eps.py cur-24.cur-6 -T -m ncep"                 >> $ptmpdir/log-w2-tc-all-eps.py.TIGGE-NCEP 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-all-eps.py cur-24.cur-6 -T -m cmc"                  >> $ptmpdir/log-w2-tc-all-eps.py.TIGGE-CMC 2>&1

dtg='2021092718'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
#$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
#$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg2"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
#$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

dtg='2021092800'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
#$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
#$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
#$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

dtg='2021092806'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/wxmap2/do-navg.py $dtg"                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
#$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
#$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
#$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

dtg='2021092812'
$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1


edate=`date`
echo 'EEEND: '$edate

