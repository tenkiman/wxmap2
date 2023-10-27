#!/bin/sh

runcmd='/data/w22/run.cron.bash'
w2pdir='/data/w22/prc'
w2prjdir='/data/w22/prj'
ptmpdir="/ptmp"
dtg=$1
overopt=$2
sdate=`date`
echo 'START-ecm5: '$sdate
$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg $overopt"                      >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
edate=`date`
echo 'EEEND-ecm5: '$edate
