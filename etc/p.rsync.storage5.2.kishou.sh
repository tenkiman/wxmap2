#!/bin/sh

base5='/storage5/kishou'
#
# first do update only rsync from source (kishou) to target (storage5) in case i've changed files on kishou
#
prcdir='/wxmap2/bin'
prcdir='/wxmap2'
b5prcdir="$base5$prcdir"

# ------------------ storarge5 -> kishou
cd $b5prcdir
#rsync -avn --exclude-from=$base5/ex-wxmap2.txt . $prcdir
rsync -av --exclude-from=$base5/ex-wxmap2.txt . $prcdir

#cd $prcdir
#rsync -u -avn --exclude-from=$base5/ex-wxmap2.txt . $b5prcdir

exit;

cd /home/mfiorino/
rsync -alv  . $base5/home/mfiorino/


