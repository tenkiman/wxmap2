#!/usr/bin/env python

from WxMAP2 import *

ropt="norun"
ropt=''

rsyncOpt='-alv'

cmd="rsync %s /dat1/tc/ /dat2/dat/tc/"%(rsyncOpt)
mf.runcmd(cmd,ropt)
