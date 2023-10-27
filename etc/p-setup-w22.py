#!/usr/bin/env python

from WxMAP2 import *


ropt=''
#ropt='norun'
exOpt=''

sbdir='/w21'
tbdir='/w22'

# -- now fill in the binaries and logs and plts
#

mdirs=['app','bin','evt','log','plt','web-config']

for mdir in mdirs:
    
    Source='%s/%s/'%(sbdir,mdir)
    Target='%s/%s/'%(tbdir,mdir)
    
    exOpt='''--exclude "*2021*" --exclude "*2020*" --exclude "*2019*" --exclude ".svn" '''
    exOpt='''--exclude "*~" --exclude ".git" '''
    
    cmd="rsync -alv %s %s %s "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)

sys.exit()


# -- GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG set up for making w22 repo
#
# -- main dirs
#

mdirs=['app/src/python','app/grads','dat','doc','etc','lib','prc']

for mdir in mdirs:
    
    Source='%s/%s/'%(sbdir,mdir)
    Target='%s/%s/'%(tbdir,mdir)
    
    exOpt='''--exclude "*2021*" --exclude "*2020*" --exclude "*2019*" --exclude ".svn" '''
    exOpt='''--exclude "*~"'''
    
    cmd="rsync -alv %s %s %s "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)


sys.exit()

# -- plt
#
Source="%s/plt/basemap"%(sbdir)
Target="%s/plt/basemap"%(tbdir)


cmd="rsync -alv %s %s %s "%(exOpt,Source,Target)
mf.runcmd(cmd,ropt)


sys.exit()



rdir='web-config'

wdirs=['config','tceps','jtdiag','tcact','tcdiag','tceps','tcgen']

for wdir in wdirs:

    
    Source='%s/%s/%s/'%(sbdir,rdir,wdir)
    Target='%s/%s/%s/'%(tbdir,rdir,wdir)
    
    exOpt='''--exclude "*2021*" --exclude "*2020*" --exclude "*2019*" --exclude ".svn" '''
    
    cmd="rsync -alv %s %s %s "%(exOpt,Source,Target)
    mf.runcmd(cmd,ropt)


sys.exit()



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

