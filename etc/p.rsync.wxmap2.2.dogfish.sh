#!/bin/sh

cd $W2
pwd
w2='/data/www/html/mfiorino/wxmap2/trunk/prc'
rsync -alv --exclude-from=ex.rsync.skate.txt trunk/prc/ "mfiorino@dogfish.nhc.noaa.gov:$w2"
#rsync -alvn trunk/prc "mfiorino@skate.nhc.noaa.gov:/www/mfiorino/public_html/wxmap2/trunk/"

