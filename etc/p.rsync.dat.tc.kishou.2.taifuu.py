#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


def doRsync(sdir,ropt='',dosizonly=0,doupdate=0,dodelete=0,reverse=0):

    tbdir="/Volumes/USB2M03/kishou"
    tbdir=''
    tdir="%s/%s"%(tbdir,sdir)
    tdir=tdir.replace('//','/')
    sdir=sdir.replace('//','/')
    if(mf.find(tdir,'-BAK')): tdir=tdir.replace('-BAK','')

    if(ropt == ''): MF.ChkDir(tdir,'mk')
    
    if(reverse):
        sdirin=sdir
        sdir=tdir
        tdir=sdirin

    if(reverse):
        tdir="fiorino@kishou.fsl.noaa.gov:/%s"%(tdir)
    else:
        sdir="fiorino@kishou.fsl.noaa.gov:/%s"%(sdir)
        
    tdir=tdir.replace('//','/')
    sdir=sdir.replace('//','/')
    pdir='/w21/etc'

    rupopt=''
    if(doupdate): rupopt='-u'

    sizonly=''
    if(dosizonly):  sizonly='--size-only'

    delopt=''
    if(dodelete): delopt='--delete'

    rsyncopt="--timeout=100 %s %s %s %s -alv --exclude-from=%s/ex-w21.txt"%(sizonly,delopt,rupopt,sizonly,pdir)

    if(reverse):
        cmd="rsync %s %50s/ %50s/"%(rsyncopt,sdir,tdir)
    else:
        MF.ChkDir(tdir,'mk')
        cmd="rsync %s %s %s"%(rsyncopt,sdir+'/',tdir+'/')
        
    mf.runcmd(cmd,ropt)

tcdasdirs=[
    '/w21/dat/tc/DSs',
    '/w21/dat/tc/names',

    '/w21/dat/tc/nhc',
    '/w21/dat/tc/jtwc',
#    '/w21/dat/tc/ecmwf',
#    '/w21/dat/tc/cira',

    '/w21/dat/tc/adeck',
    '/w21/dat/tc/bdeck',
    '/w21/dat/tc/mdeck',
    '/w21/dat/tc/edeck',
    '/w21/dat/tc/fdeck',

    '/w21/dat/tc/carq',
    '/w21/dat/tc/hrd',
    '/w21/dat/tc/jma',
    '/w21/dat/tc/ncdc',
#    '/w21/dat/tc/ncep',
    '/w21/dat/tc/nrl',
#    '/w21/dat/tc/ukmo',

    '/w21/dat/tc/carq',
    '/w21/dat/tc/com',
    '/w21/dat/tc/bt',
    '/w21/dat/tc/stext',
    '/w21/dat/tc/tcvitals',

    '/w21/dat/tc/climo',

#    '/w21/dat/tc/ebt',
#    '/w21/dat/tc/fst',
#    '/w21/dat/tc/hurdat',
#    '/w21/dat/tc/obs',
    '/w21/dat/tc/reftrk',
#    '/w21/dat/tc/sgp',
#    '/w21/dat/tc/tcbog',
#    '/w21/dat/tc/tcc',
#    '/w21/dat/tc/tcdiag',
#    '/w21/dat/tc/tceps',
#    '/w21/dat/tc/tcfilt',
#    '/w21/dat/tc/tcgen',
    ]

tcdasdirsKishou2Kaze=[
    '/w21/dat/tc/DSs',
    '/w21/dat/tc/names',
    '/w21/dat/tc/climo',
    '/w21/dat/tc/carq',
    '/w21/dat/tc/tmtrkN',
]


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            }

        self.options={
            'verb':       ['V',0,1,'verb=1 is verbose'],
            'ropt':       ['N','','norun',' norun is norun'],
            'doit':       ['X',0,1,' run...'],
            'dodelete':   ['D',0,1,' delete options...'],
            'dosizonly':  ['S',0,1,' do --size-only...'],
            'reverse':    ['R',0,1,' reverse direction from local (sdir) to remote (tdir)'],
            'doupdate':   ['u',0,1,' update in rsync'],
            'adyear':     ['y:',None,'a','adyear'],
            }

        self.purpose='''
purpose -- rsync from kaze-kishou tc data sets'''

        self.examples='''
%s -V -N'''
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

rc=w2.ChkIfRunning(dtg=None,pyfile=pyfile,model=None)
if(rc > 1):
    print 'AAA allready running...'
    sys.exit()

tcadeckDirsKishou2Kaze=[
    '/w21/dat/tc/bdeck/jtwc/%s'%(adyear),
    '/w21/dat/tc/bdeck/nhc/%s'%(adyear),
    '/w21/dat/tc/bdeck/nhc/store_invest',
    '/w21/dat/tc/nrl',
    '/w21/dat/tc/adeck/jtwc/%s'%(adyear),
    '/w21/dat/tc/adeck/nhc/%s'%(adyear),
#    '/w21/dat/tc/adeck/cmc/%s'%(adyear),
#    '/w21/dat/tc/adeck/ecmwf/%s'%(adyear),
#    '/w21/dat/tc/adeck/esrl/%s'%(adyear),
#    '/w21/dat/tc/adeck/local/%s'%(adyear),
#    '/w21/dat/tc/adeck/mit/%s'%(adyear),
#    '/w21/dat/tc/adeck/ncep/%s'%(adyear),
#    '/w21/dat/tc/adeck/ukmo/%s'%(adyear),
#    '/w21/dat/tc/adeck/wxmap2/%s'%(adyear),
    ]


MF.sTimer('tc.rsync.kaze')
if(reverse):
    for sdir in tcdasdirsKishou2Kaze:
        doRsync(sdir,dosizonly=dosizonly,doupdate=doupdate,dodelete=dodelete,ropt=ropt,reverse=reverse)
        
else:
    for sdir in tcdasdirs:
        doRsync(sdir,dosizonly=dosizonly,doupdate=doupdate,dodelete=dodelete,ropt=ropt,reverse=reverse)

if(adyear != None):
    for sdir in tcadeckDirsKishou2Kaze:
        doRsync(sdir,dosizonly=dosizonly,doupdate=doupdate,dodelete=dodelete,ropt=ropt,reverse=reverse)

    MF.dTimer('tc.rsync.kaze')
    sys.exit()


MF.dTimer('tc.rsync.kaze')

sys.exit()

