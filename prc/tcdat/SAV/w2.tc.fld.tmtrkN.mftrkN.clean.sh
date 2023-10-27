#!/bin/sh

bdir="$W2_BDIRDAT/tc/tmtrkN"
# -- on /data/tc

#bdir='/data/tc/dat/tc/tmtrkN/'
bdir='/usb2/dat/tmtrkN'
echo $bdir
find $bdir/. -name "*.grb" -exec rm -v {} \;
find $bdir/. -name "*.dat" -exec rm -v {} \;
