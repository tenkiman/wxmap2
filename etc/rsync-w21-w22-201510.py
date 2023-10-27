#!/usr/bin/env python

from M import *

dirs={
    'app':'',
    'bin':'',
    'dat':'--size-only',
    'doc':'',
    'etc':'--size-only',
    'lib':'',
    'opt':'',
    'prc':'--size-only',
    'prj':'--size-only',
    'src':'--size-only',
    'plt':'',
}

ropt='norun'
ropt=''

rsyncOpt='-alvn'
rsyncOpt='-alv'

pdirs=dirs.keys()
pdirs.sort()
for dir in pdirs:
    cmd="rsync %s %s --exclude-from rsync-exclude.txt /w21/%s/ %s/"%(rsyncOpt,dirs[dir],dir,dir)
    mf.runcmd(cmd,ropt)
