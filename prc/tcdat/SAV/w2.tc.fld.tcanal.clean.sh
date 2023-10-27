#!/bin/sh

bdir="$W2_BDIRDAT/tc/tcanal"
#bdir="$W2_BDIRDAT/tc-dat1/tcanal"
echo $bdir

find $bdir/. -name "*.dat" -exec rm -v {} \;

exit;

# -- /data/tc/ too
#bdir='/data/tc/dat/tc/tcanal/'
echo $bdir
find $bdir/. -name "*.dat" -exec rm -v {} \;
