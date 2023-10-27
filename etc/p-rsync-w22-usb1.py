#!/usr/bin/env python

from WxMAP2 import *

ropt=''
#ropt='norun'
brOpt='-alv '

# -- web-config
#

wdirs=['config','configa','tceps','jtdiag','tcact','tcdiag','tceps','tcgen']

wsdir='/data/w22/web-config'
usdir='/usb1/w22/web-config'


for wdir in wdirs:

    Source='%s/%s/'%(wsdir,wdir)
    Target='%s/%s/'%(usdir,wdir)
    
    exOpt='''%s --exclude "*2021*" --exclude "*2020*" --exclude "*2019*"'''%(brOpt)
    if(mf.find(wdir,'tcact')): exOpt=brOpt
    
    cmd="rsync %s %s %s "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)


# -- dotfiles
#
cmd="cp -n /home/fiorino/dotfiles.tar /usb1/."
mf.runcmd(cmd,ropt)


exOpt=brOpt
Source='/usb1/ptmp/'
Target='/dat1/ptmp/'

# -- ptmp first
#
cmd="rsync %s %s %s "%(exOpt,Source,Target)
mf.runcmd(cmd,ropt)

sdirs={
    '/data/w22':'/usb1/w22',
    '/dat1/w21-git':'/usb1/w21-git',
    }


for sdir in sdirs.keys():

    Source=sdir
    Target=sdirs[sdir]
        
    exOpt=brOpt
    if(mf.find(sdir,'w22')):
        exOpt="%s --exclude web-config"%(brOpt)
        
    cmd="rsync %s  %s/ %s/ "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)

    
