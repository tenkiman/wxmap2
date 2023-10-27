#!/bin/sh

testplatform="kishou.macosx.gfortran"

diagfile="ngtrk.diag.txt"
mfdiagfile="ngtrk.mfdiag.txt"
outfile="ngtrk.out.txt"
metafile="gfs2.2012071812.meta.txt"
nlfile="ngtrk.nl"
ngtrpfile="ngtrk.ngtrp.txt"
trackfile="ngtrk.gfs2.track.txt"

comptrackfile="$testplatform.$trackfile"

cmd="time ../ngtrkN.x $nlfile $ngtrpfile $metafile $outfile $diagfile $mfdiagfile"

echo $cmd
#$cmd 
$cmd > $trackfile

#-- comp

cmd="/Applications/xxdiff.app/Contents/MacOS/xxdiff $comptrackfile $trackfile"
echo $cmd
$cmd


exit;




