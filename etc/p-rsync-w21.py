#!/usr/bin/env python

from WxMAP2 import *

Direction='w2u'
#Direction='u2w'

ropt=''
#ropt='norun'

# -- dotfiles
#
if(Direction == 'w2u'):
    cmd="cp -n /home/fiorino/dotfiles.tar /usb1/."
    mf.runcmd(cmd,ropt)


exOpt=''
Source='/usb1/ptmp/'
Target='/dat1/ptmp/'

# -- ptmp first
#
cmd="rsync -alv %s  %s %s "%(exOpt,Source,Target)
mf.runcmd(cmd,ropt)

sdirs=['w21','w21-git']


for sdir in sdirs:

    usbsrc='/usb1/%s/'%(sdir)
    w21src='/dat1/%s/'%(sdir)

    if(Direction == 'w2u'):
        Source=w21src
        Target=usbsrc
    else:
        Source=usbsrc
        Target=w21src
        
    exOpt=''
    if(sdir == 'w21'):
        exOpt="--exclude web-config"
    cmd="rsync -alv %s  %s %s "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)

# -- web-config
#

ropt=''
#ropt='norun'

wdirs=['config','configa','tceps','jtdiag','tcact','tcdiag','tceps','tcgen']

sdir=sdirs[0]+'/web-config'
for wdir in wdirs:

    if(Direction == 'w2u'):
        Source='/%s/%s/'%(sdir,wdir)
        Target='/usb1/%s/%s/'%(sdir,wdir)
    else:
        Source='/usb1/%s/%s/'%(sdir,wdir)
        Target='/%s/%s/'%(sdir,wdir)
    
    exOpt='''--exclude "*2021*" --exclude "*2020*" --exclude "*2019*"'''
    if(wdir == 'tcact'): exOpt=''
    
    cmd="rsync -alv %s %s %s "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)

    
