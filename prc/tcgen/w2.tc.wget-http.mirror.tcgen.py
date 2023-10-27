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
            'stmopt':          ['S:',None,'a','stmopt'],
            'dochkIfRunning':  ['o',1,0,'do NOT chkifrunning in MFutils.chkIfJobIsRunning'],
            }

        self.purpose='''
mirror ESRL tcgenDAT to local'''

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

af=w2.TcGenHttpServer
sbdir=w2.TcGenHttpDatDir
tbdir=w2.TcGenHttpLocalDatDir

for dtg in dtgs:

    MF.sTimer('wget-mirror-tcgen-%s'%(dtg))
    yyyy=dtg[0:4]
    sdir="%s/%s/%s"%(sbdir,yyyy,dtg)
    tdir="%s/%s/%s"%(tbdir,yyyy,dtg)
    MF.ChkDir(tdir,'mk')

    logdir="%s/log"%(tbdir)
    MF.ChkDir(logdir,'mk')
    logpath="%s/db.wget-http-tcgen.%s.txt"%(logdir,dtg)

    cmd="wget -m -np -nH --cut-dirs=4 -nv -T 60 -t 1 -a %s \"http://%s/%s/\" -P %s/"%(logpath,af,sdir,tdir)
    mf.runcmd(cmd,ropt)
    MF.dTimer('wget-mirror-tcgen-%s'%(dtg))

# -- bring over inventory .js
#
cmd="wget -m -np -nH --cut-dirs=4 -nv -T 60 -t 1 \"http://ruc.noaa.gov/hfip/tcgen/inv.tcgen.js\" -P /w21/web/tcgen/"
mf.runcmd(cmd,ropt)

sys.exit()
