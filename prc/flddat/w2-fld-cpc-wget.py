#!/usr/bin/env python

"""
%s

purpose:

wget mirror cpc qmorph data to nhc

usages:

  %s cur|dtg -S qmorph|cmorph [-N]
  
dtg: "date time group" = YYYYMMDDHH
  YYYY is year
  MM is month
  DD is day
  HH synoptic hour (UTC = 00,06,12,18)

(c) 2008 by Michael Fiorino, NHC
"""

from WxMAP2 import *
w2=W2()

#
#  defaults
#
ropt=''
source='qmorph'

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyyyy=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

if(narg > 0):

    dtgopt=sys.argv[1]
    (dtg,phr)=mf.dtg_phr_command_prc(dtgopt) 

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "NVS:")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-S",""): source=a

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


i=1
if(narg >= 1):
    dtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit()


service='ftp'
login='ftp'

dtgswitch='2015110800'
dtgdiff=mf.dtgdiff(dtgswitch,dtg)

usenew=0
if(dtgdiff >= 0.0): usenew=1

if(source == 'qmorph'):
    server=w2.CpcFtpQmorphServer
    tbdir=w2.NhcFtpTargetDirQmorph
    if(usenew):
        sbdir=w2.CpcFtpSourceDirQmorph
        sbdir="/precip/CMORPH_V0.x_RT/RAW/0.25deg-30min"
        mask='\"CMORPH_V0.x_RAW_0.25deg-30min_*.RT2.gz\"'
        
        # -- 20180124 - new location for qmorph
        #
        sbdir="/precip/CMORPH_RT/GLOBE/data"
        sdir="%s/%s/%s"%(sbdir,dtg[0:4],dtg[0:6])
        tdir="%s/%s"%(tbdir,dtg[0:4])
        MF.ChkDir(tdir,'mk')
        mask='\"CMORPH_V0.x_RT_8km-30min_%s*.gz\"'%(dtg[0:8])
        
        
elif(source == 'cmorph'):
    server=w2.CpcFtpCmorphServer
    sdir=w2.CpcFtpSourceDirCmorph
    tbdir=w2.NhcFtpTargetDirCmorph
    mask='\"C*%s*Z\"'%(dtg[0:6])
    if(usenew):
        sbdir=w2.CpcFtpSourceDirQmorph
        sbdir="/precip/CMORPH_V0.x/RAW/8km-30min"
        sdir="%s/%s/%s"%(sbdir,dtg[0:4],dtg[0:6])
        tdir="%s/%s"%(tbdir,dtg[0:4])
        MF.ChkDir(tdir,'mk')
        mask='\"CMORPH_V0.x_RAW_8km-30min_%s*.gz\"'%(dtg[0:8])

mf.ChkDir(tdir,'mk')
cmd="wget --mirror -T 480 -nv -nd -np -l1 -A %s -P %s \"%s://%s@%s/%s/\""%(mask,tdir,service,login,server,sdir)
mf.runcmd(cmd,ropt)

sys.exit()
