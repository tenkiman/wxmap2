#!/usr/bin/env python

from WxMAP2 import *


w2dirs=[
'cgd2',
'ecm5',
'ecmt',
'gfs2',
'jgsm',
'navg',
]

rsyncOpt='-alv'
ropt='norun'
ropt=''

cmd='rsync %s --exclude "cmorph-v10" /dat13/dat/pr/ /ssd2/dat/pr/'%(rsyncOpt)
mf.runcmd(cmd,ropt)

cmd='rsync %s --exclude "era5" /dat13/dat/ocean/ /ssd2/dat/ocean/'%(rsyncOpt)
mf.runcmd(cmd,ropt)

cmd='rsync %s /dat13/nwp2/ncep/ /ssd2/dat/nwp2/ncep/'%(rsyncOpt)
mf.runcmd(cmd,ropt)


sbase='/dat13/nwp2/w2flds/dat'
tbase='/ssd2/dat/nwp2/w2flds/dat'
for w2dir in w2dirs:
    cmd='rsync %s %s/%s/ %s/%s/'%(rsyncOpt,sbase,w2dir,tbase,w2dir)
    mf.runcmd(cmd,ropt)


 
    
