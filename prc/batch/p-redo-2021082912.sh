#!/bin/sh

runcmd='/data/w22/run.cron.bash'
w2pdir='/data/w22/prc'
w2prjdir='/data/w22/prj'
ptmpdir="/ptmp"

#dtg='2021082818'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
#$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
#$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg2"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
#$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1


dtg='2021082900'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
#$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
#$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

dtg='2021082906'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/wxmap2/do-navg.py $dtg"                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
#$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
#$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg"                               >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1


