#!/bin/sh

runcmd='/data/w22/run.cron.bash'
w2pdir='/data/w22/prc'
w2prjdir='/data/w22/prj'
ptmpdir="/ptmp"

sdate=`date`
echo 'START: '$sdate

# -- run monitor and throw in background
#
$runcmd "$w2pdir/wxmap2/w2-ps-monitor.py -X -S 15"             >> $ptmpdir/log-w2-ps-monitor.py.tenki.PS-MONITOR 2>&1 &
$runcmd "$w2pdir/tcdat/w2-tc-ops-dat.py ops -o -V"             >> $ptmpdir/log-w2-tc-ops-dat.py.TENKILF 2>&1

# -- ad2

$runcmd "$w2pdir/tcdat/w2-tc-dss-ad2.py jt -d cur-24.cur"                          >> $ptmpdir/log-w2.tc.dss.ad2.py.wxmap2.AD2-jt-nhc-hourly-AD2 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-dss-ad2.py jt,gefs,ukmo -d cur-24.cur -9"             >> $ptmpdir/log-w2.tc.dss.ad2.py.wxmap2.AD2-jt-nhc-tm-mftrkN-hourly-AD2-9X 2>&1

# -- TC push to wxmap2.com
#
#$runcmd "$w2pdir/tcdat/w2-tc-rsync-mirror-TC-names-DSs-tcvitals-wxmap2.py -X"                 >> $ptmpdir/log-w2-tc-rsync-mirror-TC-names-DSs-tcvitals-wxmap2.py.TC2WXMAP2 2>&1
#$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 1 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P1 2>&1
#$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 2 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P2 2>&1
#$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 3 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P3 2>&1
#$runcmd "$w2pdir/tcdat/w2-tc-active.py -C -W -P 4 -X"                                         >> $ptmpdir/log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P4 2>&1


# -- goes
#

$runcmd "$w2pdir/flddat/w2-fld-wget-mirror-gfs-stbgoes.py cur-48.cur"              >> $ptmpdir/log-w2-fld-wget-mirror-gfs-stbgoes.py.GFS2 2>&1

# -- oisst
#
$runcmd "$w2pdir/flddat/w2-fld-wget-mirror-cpc-oisst.py"                           >> $ptmpdir/log-w2-fld-wget-mirror-cpc-oisst.py.CPC.OISST 2>&1

# -- pr
#
"$w2pdir/flddat/w2-fld-pr-qmorph.py cur-24.cur.24  -S qmorph -n 6"                 >> $ptmpdir/log-w2-fld-qmorph.py.CPC-QMORPH 2>&1
"$w2pdir/flddat/w2-fld-pr-qmorph.py cur-48.cur-24 -S cmorph -n 6"                  >> $ptmpdir/log-w2-fld-qmorph.py.CPC-CMORPH 2>&1
"$w2pdir/flddat/w2-fld-pr-qmorph-products.py ops6 -S qmorph -n 6"                  >> $ptmpdir/log-w2-fld-qmorph-products.py.qmorph.CPC 2>&1
"$w2pdir/flddat/w2-fld-pr-qmorph-products.py cur-36.cur-24 -S cmorph -n 6"         >> $ptmpdir/log-w2-fld-qmorph-products.py.cmorph.CPC 2>&1
"$w2pdir/flddat/w2-fld-pr-qmorph-global-products.py ops6 -S qmorph -n 6"           >> $ptmpdir/log-w2-fld-qmorph-global-products.py.qmorph.CPC 2>&1
"$w2pdir/flddat/w2-fld-pr-qmorph-global-products.py cur-36.cur-24 -S cmorph -n 6"  >> $ptmpdir/log-w2-fld-qmorph-global-products.py.cmorph.CPC 2>&1

# -- eps
#
$runcmd "$w2pdir/tcdat/w2-tc-ecmwf-wmo-essential-bufr-json.py cur-48.cur-6"      >> $ptmpdir/log-w2-tc-ecmwf-wmo-essential-bufr-json.py-EPS 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-all-eps.py cur-48.cur-6 -2"                         >> $ptmpdir/log-w2-tc-all-eps.py.EPSPLOTTIGGENCEP 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-all-eps.py cur-48.cur-6 -T -m ncep"                 >> $ptmpdir/log-w2-tc-all-eps.py.TIGGE-NCEP 2>&1
$runcmd "$w2pdir/tcdat/w2-tc-all-eps.py cur-48.cur-6 -T -m cmc"                  >> $ptmpdir/log-w2-tc-all-eps.py.TIGGE-CMC 2>&1

exit;
# -- also do goes loops
#
dtg='2021102918'
#$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
#$runcmd "$w2pdir/fldanal/w2-gfs-goes-loop.py $dtg all -A"              >> $ptmpdir/log-w2-gfs-goes-loop-py.GOES 2>&1
$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg -O"                             >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

dtg='2021103000'
$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
$runcmd "$w2pdir/fldanal/w2-gfs-goes-loop.py $dtg all -A"               >> $ptmpdir/log-w2-gfs-goes-loop-py.GOES 2>&1

$runcmd "$w2pdir/wxmap2/do-navg.py $dtg"                                >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
$runcmd "$w2pdir/wxmap2/do-ecm5.py $dtg"                                >> $ptmpdir/log-w2-do-ecm5.py.ECM5 2>&1
$runcmd "$w2pdir/wxmap2/do-cgd2.py $dtg"                                >> $ptmpdir/log-w2-do-cgd2.py.CGD2 2>&1
$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

# -- jtdiag
#
$runcmd "$w2pdir/tcdiag/w2-tc-jtdiag-cp-png-2-tcdiag.py cur-12.cur "    >> $ptmpdir/log-w2-tc-jtdiag.py-JTdiag-ph2-3 2>&1

dtg='2021103006'
$runcmd "$w2pdir/wxmap2/do-gfs2.py $dtg"                                >> $ptmpdir/log.do-gfs2.py.GFS2_p505 2>&1
$runcmd "$w2pdir/fldanal/w2-gfs-goes-loop.py $dtg all -A"               >> $ptmpdir/log-w2-gfs-goes-loop-py.GOES 2>&1

$runcmd "$w2pdir/wxmap2/do-navg.py $dtg "                               >> $ptmpdir/log.do-navg.py.NAVG_p605 2>&1
$runcmd "$w2pdir/wxmap2/do-jgsm.py $dtg"                                >> $ptmpdir/log-w2-do-jgsm.py.JGSM 2>&1

edate=`date`
echo 'EEEND: '$edate

