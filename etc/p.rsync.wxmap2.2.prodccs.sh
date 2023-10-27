#!/bin/sh

cd $W2
pwd

rsync -alv -n -u -e ssh --delete --exclude-from=ex.rsync.prodccs.txt --rsync-path=/usrx/local/bin/rsync trunk/ 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wxmap2/trunk'

#rsync -alv -u -n -e ssh --delete --exclude-from=ex.rsync.prodccs.txt --rsync-path=/usrx/local/bin/rsync 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wxmap2/trunk/prc/lib/python/.' trunk/prc/lib/python/. 

#rsync -alv -n -u -e ssh --exclude-from=ex.rsync.prodccs.txt --rsync-path=/usrx/local/bin/rsync 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wxmap2/trunk/prc/flddat/.' trunk/prc/flddat/. 


exit;

#rsync -alvn -e ssh --delete --exclude-from=ex.rsync.prodccs.txt --rsync-path=/usrx/local/bin/rsync app/ 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wxmap2/app'
#rsync -alvn -e ssh --delete --exclude-from=ex.rsync.prodccs.txt --rsync-path=/usrx/local/bin/rsync bin/ 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wxmap2/bin'

#rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync app/ 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
#rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync data/ 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads'
#rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync udf 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads/'
#rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync gslib 'tpcprd1@prodccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads/'
