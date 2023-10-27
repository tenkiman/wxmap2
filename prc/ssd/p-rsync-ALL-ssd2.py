#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
ropt='norun'
ropt=''

cmd='p-inv-tc-dat-ops.py'
mf.runcmd(cmd,ropt)

cmd='p-rsync-nwp2-pr-ocean.py'
mf.runcmd(cmd,ropt)

cmd='rsync -alv /dat1/w21-git/ /ssd2/w21-git/'
mf.runcmd(cmd,ropt)

cmd='rsync -alv %s /ssd2/hfip/fiorino/products/'%(w2.HfipProducts)
mf.runcmd(cmd,ropt)

cmd='rsync -alv /data/w22/ /ssd2/w22/'
mf.runcmd(cmd,ropt)
