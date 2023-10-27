#!/bin/sh

runcmd='/data/w22/run.cron.bash'
w2pdir='/data/w22/prc'
w2prjdir='/data/w22/prj'
ptmpdir="/ptmp"

sdate=`date`
echo 'START-tc-push: '$sdate

# -- TC push to wxmap2.com
#
$runcmd "$w2pdir/tcdat/w2-tc-rsync-mirror-TC-names-DSs-tcvitals-wxmap2.py -X"                 >> $ptmpdir/log-w2-tc-rsync-mirror-TC-names-DSs-tcvitals-wxmap2.py.TC2WXMAP2 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 1 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P1 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 2 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P2 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 3 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P3 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 4 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P4 2>&1

edate=`date`
echo 'EEEND-tc-push: '$edate
