   159	20:20	rsync -alvn NO_NAME1/kishou/. usbdisk/.
   160	20:35	rsync -alv NO_NAME1/kishou/. usbdisk/.
   200	11:42	rsync -alv NO_NAME1/kishou/. usbdisk/kishou/.
   201	11:43	rsync -alv NO_NAME1/kishou/. usbdisk/kishou/.
   213	11:40	g rsync *py
   214	11:40	g rsync ../*/*py
   215	11:40	g rsync ../*/*py | g ss
   216	11:41	rsync -e ssh -alvn "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/lib/python"
   217	11:41	rsync -e ssh -alvn . "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/lib/python"
   219	11:42	rsync -e ssh -alvn trunk/. "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/."
   220	11:42	rsync -e ssh -alvn trunk/prc/hwrf/. "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/."
   221	11:42	rsync -e ssh -alvn trunk/prc/hwrf/. "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/trunk/prc/hwrf/."
   222	11:43	rsync -e ssh -alv trunk/prc/hwrf/. "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/trunk/prc/hwrf/."
   223	11:43	rsync -e ssh -alv trunk/prc/hwrf/. "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/trunk/prc/hwrf/."
   224	11:43	rsync -e ssh -alv trunk/prc/hwrf/. "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/trunk/prc/hwrf/."
   225	11:43	rsync -e ssh -alv trunk/prc/hwrf/ "wx80mf@devccs.ncep.noaa.gov/gpfs/d/tpc/save/wx80mf/wxmap2/trunk/prc/hwrf/"
   226	11:44	rsync -e ssh -alv trunk/prc/hwrf/ "wx80mf@devccs.ncep.noaa.gov:/gpfs/d/tpc/save/wx80mf/wxmap2/trunk/prc/hwrf/"
   247	16:52	rsync -alvn -e ssh --rsync-path=/usrx/local/bin/rsync * 'wx80mf@devccs.ncep.noaa.gov:/gpfs/tpc/save/wx80mf/wxmap2/trunk'
   248	16:53	rsync -alvn --rsh ssh --rsync-path=/usrx/local/bin/rsync . 'wx80mf@devccs.ncep.noaa.gov:/gpfs/tpc/save/wx80mf/wxmap2/trunk/.'
   249	16:54	rsync -alvn -e ssh --rsync-path=/usrx/local/bin/rsync * 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
   250	16:54	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync * 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
   259	16:56	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync /home/work/wxmap2/trunk 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
   262	16:56	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync * 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
   263	16:56	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync * 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk' | l
   264	16:57	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync .* 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk' | l
   266	16:58	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync trunk/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk' | l
   269	16:59	rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync trunk/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk' | l
   270	16:59	rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync trunk/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
   275	17:10	rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync app/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/trunk'
   278	17:11	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync app/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app'
   279	17:12	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync app/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app'
   288	17:37	h | g rsync
   289	17:37	h | g rsync > ../../p.rsync.wxmap2.2.devccs.sh
   292	17:38	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync data/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads'
   293	17:38	rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync data/ 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads'
   294	17:40	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync udf 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads/udf'
   295	17:40	rsync -alvn -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync udf 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads/'
   296	17:40	rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync udf 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads/'
   297	17:41	rsync -alv -e ssh --ignore-existing --rsync-path=/usrx/local/bin/rsync gslib 'wx80mf@devccs.ncep.noaa.gov:/tpc/save/wx80mf/wxmap2/app/grads/'
   299	17:51	h | g rsync > ../../p.rsync.wxmap2.2.devccs.sh
