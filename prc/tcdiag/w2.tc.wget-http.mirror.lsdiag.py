#!/usr/bin/env python

from tcbase import *

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local defs
#

class TcOpsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'doClean':         ['K',0,1,'clean off the tdir before the wget'],
            'doJTdiag':        ['J',1,0,'do NOT pull from jtdiag'],
            'stmopt':          ['S:',None,'a','stmopt'],
            'doDiagOnly':      ['D',0,1,'only do diagfiles'],
            'dochkIfRunning':  ['o',1,0,'do NOT chkifrunning in MFutils.chkIfJobIsRunning'],
            }

        self.purpose='''
mirror ESRL tcdiagDAT to local'''

        self.examples='''
%s cur12-12     : pull from archive dir for 2004'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(ropt == 'norun'): dochkIfRunning=0


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#
# -- turn off Late since John Knaff stopped in 2016...
#

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

if(doJTdiag):
    af=w2.JtDiagHttpServer
    sbdir=w2.JtDiagHttpDatDir
    tbdir=w2.JtDiagHttpLocalDatDir
    timer='wget-mirror-jtdiag'
    
else:
    af=w2.TcDiagHttpServer
    sbdir=w2.TcDiagHttpDatDir
    tbdir=w2.TcDiagHttpLocalDatDir
    timer='wget-mirror-tcdiag'

for dtg in dtgs:

    MF.sTimer('%s-%s'%(timer,dtg))
    yyyy=dtg[0:4]
    sdir="%s/%s/%s"%(sbdir,yyyy,dtg)
    tdir="%s/%s/%s"%(tbdir,yyyy,dtg)

    logdir="%s/log"%(tbdir)
    MF.ChkDir(logdir,'mk')
    logpath="%s/db.wget-http-tcdiag.%s.txt"%(logdir,dtg)
    
    if(doDiagOnly):
        sdir="%s/DIAGFILES"%(sdir)
        tdirrm="%s/DIAGFILES"%(tdir)
        
    
    if(doClean): 
        cmd="rm -r %s"%(tdirrm)
        mf.runcmd(cmd,ropt)
        cmd="rm %s"%(logpath)
        mf.runcmd(cmd,ropt)
        
    MF.ChkDir(tdir,'mk')

    wgetopt=""" -m -np -nH --cut-dirs=4 -nv -T 60 -t 1 -A '*.png','*.txt' -R 'bm.*' """
    cmd="time wget %s -a %s \"http://%s/%s/\" -P %s/"%(wgetopt,logpath,af,sdir,tdir)
    mf.runcmd(cmd,ropt)
    
    MF.dTimer('%s-%s'%(timer,dtg))


sys.exit()
