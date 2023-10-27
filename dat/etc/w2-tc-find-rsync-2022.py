#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


bdir="/data/w22/dat"
tdir="/ssd4/dat/tc"

rdirs=[
    'adeck',
    'archive',
    'bdeck',
    'bt',
    'carq',
    'cimss',
    'cira',
    'climo',
    'cmc',
    'com',
    'dis',
    'DSs',
    'DSs-VD2',
    'ecmwf',
    'edeck',
    'etc',
    'fdeck',
    'jtwc',
    'mdeck',
    'names',
    'ncep',
    'nhc',
    'ptcanl',
    'ptmp',
    'reftrk',
    'stext',
    'tcanal',
    'tcdiag',
    'tceps',
    'tcgen',
    'tcvcip',
    'tcvitals',
    'tdeck',
    'tmtrkN',
    'ukmo',

    ]

bdate='2022-01-01'

ropt='norun'
ropt=''
MF.ChangeDir(bdir,verb=1)
MF.sTimer('tc-rsync')

for rdir in rdirs:

    if(rdir == 'climo'):
        cmd='''rsync -alv ./%s "%s/%s'''%(rdir,tdir,rdir)
    else:
        cmd='''time find tc-dat2/%s/. -newermt "%s" -type f -print0 | rsync -ar -iv --files-from - --from0 ./ "%s/%s"'''%(rdir,bdate,tdir,rdir)
        
    mf.runcmd(cmd,ropt)
    continue
    
MF.dTimer('tc-rsync')
