#!/usr/bin/env python

from M import *

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


#
#
#

def doRsync(tdir,ropt='',doupdate=0,dodelete=0,reverse=0):

    server='fiorino@kishou.fsl.noaa.gov'
    sdir='/dat2'+tdir
    if(reverse):
        sdir=tdir
        tdir='/dat2'+tdir
    pdir='/w21/etc'

    rupopt=''
    if(doupdate): rupopt='-u'

    delopt=''
    if(dodelete): delopt='--delete'
    rsyncopt="%s %s --size-only -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,pdir)
    if(reverse):
        cmd="rsync %s %s/ %s:%s/"%(rsyncopt,sdir,server,tdir)
    else:
        cmd="rsync %s %s:%s/ %s/"%(rsyncopt,server,sdir,tdir)
        
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


tcdatdirs=[
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
tcdatdirs=[
    '/w21/dat/tc/DSs',
    '/w21/dat/tc/names',
    ]


dodata=1
dow2=0
doapp=0



if(dow2):
    for tdir in w2dirs:
        doRsync(tdir,doupdate=1,dodelete=dodelete,ropt=ropt)
    
if(doapp):
    for tdir in appdirs:
        doRsync(tdir,doupdate=0,ropt=ropt)

if(dodata):
    for tdir in tcdatdirs:
        doRsync(tdir,doupdate=doupdate,dodelete=dodelete,ropt=ropt,reverse=reverse)


sys.exit()

