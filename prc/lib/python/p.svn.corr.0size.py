#!/usr/bin/env python

from M import *

corr0=['tc2.py','TCtrk.py','TCw2.py','VD.py','VT.py']
corr0=['ATCF.py','ad2.py']

rev=1255
ropt='norun'
ropt=''

for c in corr0:

    cmd="rm -i %s"%(c)
    mf.runcmd(cmd,ropt)
    
    cmd="svn update %s -r %d"%(c,rev)
    mf.runcmd(cmd,ropt)

    cmd="mv %s %s-SAV"%(c,c)
    mf.runcmd(cmd,ropt)

    cmd="svn update %s"%(c)
    mf.runcmd(cmd,ropt)

    cmd="cp %s-SAV %s"%(c,c)
    mf.runcmd(cmd,ropt)


