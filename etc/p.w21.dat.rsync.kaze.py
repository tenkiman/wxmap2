#!/usr/bin/env python

from M import *
MF=MFutils()

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
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'doit':['X',0,1,' run...'],
            'dodelete':['D',0,1,' delete options...'],
            'reverse':['R',0,1,' reverse direction from local (sdir) to remote (tdir)'],
            'doupdate':['u',0,1,' update in rsync'],
            }

        self.purpose='''
purpose -- rsync from kishou to local tc data sets
%s -N -V -u 
'''
        self.examples='''
%s -V -N
'''
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

argv=sys.argv
CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


kazebdir='/data/amb/hfip/fiorino'
#
#
#

def doRsync(sdir,ropt='',doupdate=0,dodelete=0,reverse=0):

    tdir="%s/%s"%(kazebdir,sdir)
    tdir=tdir.replace('//','/')
    if(mf.find(tdir,'-BAK')): tdir=tdir.replace('-BAK','')

    MF.ChkDir(tdir,'mk')
    
    if(reverse):
        sdirin=sdir
        sdir=tdir
        tdir=sdirin
        
    pdir='/w21/etc'

    rupopt=''
    if(doupdate): rupopt='-u'

    delopt=''
    if(dodelete): delopt='--delete'
    rsyncopt="%s %s --size-only -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,pdir)
    if(reverse):
        cmd="rsync %s %s/ %s/"%(rsyncopt,sdir,tdir)
    else:
        cmd="rsync %s %s/ %s/"%(rsyncopt,sdir,tdir)
        
    mf.runcmd(cmd,ropt)



w2dirs=[
    '/w21/src/opengrads2.0/Grads/extensions',
    '/w21/src/opengrads2.0/Grads/src',
    '/w21/etc',
    '/w21/prc',
    ]

appdirs=[
    '/w21/app/grads',
    ]


tcdasdirs=[
# -- new tcc data from chris hennon
    '/w21/dat/tc/tcc',
    '/w21/dat/tc/DSs',
    '/w21/dat/tc/carq',
    '/w21/dat/tc/mdeck',
    '/w21/dat/tc/bdeck',
    '/w21/dat/tc/climo',
    '/w21/dat/tc/names',
    '/w21/dat/tc/nhc',
    '/w21/dat/tc/jtwc',
    '/w21/dat/tc/bt',
#    '/w21/dat/tc/btn',
#    '/w21/dat/tc/bto',
#    '/w21/dat/tc/tceps',
#    '/w21/dat/tc/tcgen',
#    '/w21/dat/tc/tcdiag',
    '/w21/dat/tc/adeck',
    ]

# -- basics only
tcdasdirs=[
    '/w21/dat/tc/DSs',
    '/w21/dat/tc/names',
    ]


tcdasdirs=[
    '/w21/dat/tc-BAK/DSs',
    '/w21/dat/tc-BAK/names',

    '/w21/dat/tc-BAK/nhc',
    '/w21/dat/tc-BAK/jtwc',

    '/w21/dat/tc-BAK/adeck',
    '/w21/dat/tc-BAK/bdeck',
    '/w21/dat/tc-BAK/mdeck',

    '/w21/dat/tc-BAK/cimss',
    '/w21/dat/tc-BAK/cmc',
    '/w21/dat/tc-BAK/cira',
    '/w21/dat/tc-BAK/ecmwf',
    '/w21/dat/tc-BAK/hrd',
    '/w21/dat/tc-BAK/jma',
    '/w21/dat/tc-BAK/ncdc',
    '/w21/dat/tc-BAK/ncep',
    '/w21/dat/tc-BAK/nrl',
    '/w21/dat/tc-BAK/ukmo',

    '/w21/dat/tc-BAK/carq',
    '/w21/dat/tc-BAK/com',
    '/w21/dat/tc-BAK/bt',

    '/w21/dat/tc-BAK/climo',

    '/w21/dat/tc-BAK/ebt',
    '/w21/dat/tc-BAK/edeck',
    '/w21/dat/tc-BAK/fdeck',
    '/w21/dat/tc-BAK/fst',
    '/w21/dat/tc-BAK/hurdat',
    '/w21/dat/tc-BAK/obs',
    '/w21/dat/tc-BAK/reftrk',
    '/w21/dat/tc-BAK/sgp',
    '/w21/dat/tc-BAK/stext',
    '/w21/dat/tc-BAK/tcbog',
    '/w21/dat/tc-BAK/tcc',
    '/w21/dat/tc-BAK/tcdiag',
    '/w21/dat/tc-BAK/tceps',
#    '/w21/dat/tc-BAK/tcfilt',
    '/w21/dat/tc-BAK/tcgen',
    '/w21/dat/tc-BAK/tcvitals',
    ]



dodata=1
dow2=0
doapp=0

if(dodata):
    for sdir in tcdasdirs:
        doRsync(sdir,doupdate=doupdate,dodelete=dodelete,ropt=ropt,reverse=reverse)


if(dow2):
    for sdir in w2dirs:
        doRsync(sdir,doupdate=1,dodelete=dodelete,ropt=ropt)
    
if(doapp):
    for sdir in appdirs:
        doRsync(sdir,doupdate=0,ropt=ropt)


sys.exit()

