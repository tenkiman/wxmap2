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

tbdir=w2.TcDiagHttpLocalDatDir

keepVars=[
    'shr_mag',
    'sst',
    'sstanom',
    '200dvrg',
    '850vort',
    'max_wind',
    'r_700',
]

keepPngs=keepVars  #+ ['trkplt']

for dtg in dtgs:

    MF.sTimer('clean-local-lsdiag-%s'%(dtg))
    yyyy=dtg[0:4]
    tdir="%s/%s/%s"%(tbdir,yyyy,dtg)
    try:
        MF.ChangeDir(tdir)
    except:
        print 'tdir:',tdir,' not there...sayounara'
        sys.exit()
        
    allhtmls=glob.glob("*.htm")
    allhtmls.sort()
    for html in allhtmls:
        thtml=html.split('.')[0]
        if(thtml in keepVars):
            if(verb): print 'keeping(html): ',html
        else:
            print 'KILL-%s-(html): '%(dtg),html
            os.unlink(html)
            
    allpngs=glob.glob("*/*png")
    
    for png in allpngs:
        (tdir,tfile)=os.path.split(png)
        tpng=tfile.split('.')[0]
        if(tpng in keepVars):
            if(verb): print 'keeping(png): ',png   
        else:
            print 'KILL-%s-(png): '%(dtg),png
            os.unlink(png)



sys.exit()
