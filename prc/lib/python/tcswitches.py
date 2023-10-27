from w2switches import W2doPublicAdecks,W2doWjet,W2doMirrorWjet

domirrornhc=1

# -- 20110418 cnmoc turned off access? just for me?
# someone thought i had root access...jtwc is checking
# use pzal, which does work...
domirrorjtwc=1

domirrormit=1

# -- turn off on 20121206
domirrorhfip=0

domirrorwjet=W2doWjet
# -- turn off for testing
domirrorwjet=W2doMirrorWjet

domirrortacc=0
doucarput=0
override=0

dotcposits=1
dopostmdeck=1
doforceall=0
dobdecksonly=0
doreftrkonly=0
dogrepnceponly=0
dotcstatus=0
dorsync2jet=0

dovdeck=0

docuradeck=1
doadeck=0
# -- in crontab
#
doadeckdss=0
dovdeckdss=0

#
# 20080207 -- this was causing problems at ncep added with hung processes, added --timeout, seems to have fixed
# 20080221 -- big switch that overrides in w2.py:
#
#    W2RsyncTCAtcfNcepOff=1 -- do both noaa and navy atcf files
#    W2RsyncTCAdeckNcepOff=0 -- just do the adecks
#
donceprsync=1
#
# 20080709 -- wxmap.npmoc broke
#
dojtwcrsync=1

dotcvitalsonly=0
#
# 20090622 -- don't do ww3 inventory here ... in crontab
doww3inv=0

# -- 20110714 -- turn on/off mtcswa
#
domtcswa=0
# -- 20110715 -- turned back on -- ok now
domtcswa=1

# 20111209 -- md2 inside otc on kaze
#
doTCmdecks2=1

# 20120821 -- control of wget.mirror.nhc
#
dodisNHC=1
docomNHC=1
dostextNHC=1

# 20120829 -- whether to gunzip .gz from nhc; if 0, then only gunzip if .dat NOT there
# -- 20160709 -- use gzip -d to preserve time-stamp -- now only gunzip of .gz updated; applies to nhc adecks and nhc archive a/bdecks
#
alwaysGunzip=0
