#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

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
            'stmopt':          ['s:',None,'a','stmopt'],
            
            }

        self.purpose='''
mirror psd RR2 adecks to plocal'''

        self.examples='''
%s 2004010100     : pull from archive dir for 2004'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

af=w2.TcpsdRR2FtpServer
al=w2.TcpsdRR2FtpLogin
ap=w2.TcpsdRR2FtpPasswd
sbdir=w2.TcpsdRR2FtpDatDir
tbdir=w2.TcpsdRR2DatDir

for dtg in dtgs:

    # -- get the Late data from cira (+3.0h vice +0.5 h)
    #
    year=dtg[0:4]
    sdir="%s/%s/%s"%(sbdir,year,dtg)
    tdir="%s/%s/%s"%(tbdir,year,dtg)
    mf.ChkDir(tdir,diropt='mk')
    mf.ChangeDir(tdir)

    logpath="%s/db.wget.%s.txt"%(tdir,dtg)
    cmd="wget -nv -m -nd -T 180 -t 2 \"ftp://%s:%s@%s/%s/\""%(al,ap,af,sdir)
    mf.runcmd(cmd,ropt)

            

sys.exit()
