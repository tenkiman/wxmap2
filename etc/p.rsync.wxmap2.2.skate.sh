#!/bin/sh

cd $W2
pwd
rsync -alv --delete --exclude-from=ex.rsync.skate.txt trunk/prc/ "mfiorino@skate.nhc.noaa.gov:/www/mfiorino/public_html/wxmap2/trunk/prc"
#rsync -alvn trunk/prc "mfiorino@skate.nhc.noaa.gov:/www/mfiorino/public_html/wxmap2/trunk/"

