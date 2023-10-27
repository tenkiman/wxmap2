#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
# -- final version of rsync on mike2-tenki7
#

tdirs={
    '/w21/dat/nwp2':'/dat0/dat/nwp2',    # backup to usb3 drive  #-- don't need since on /Mike-D/dat2
    #'/w21/dat/ocean':'/dat0/tenki7-ssd/dat/ocean', # -- relocate to top
    #'/w21/dat/tc':'/dat0/tenki7-ssd/dat/tc',
    #'/w21/dat/pr':'/dat0/tenki7-ssd/dat/pr',
    '/w21/dat/ocean':'/dat0/dat/ocean',
    '/w21/dat/tc':'/dat0/dat/tc',
    '/w21/dat/pr':'/dat0/dat/pr',
    '/w21':'/dat0/tenki7-ssd/w21',           # -- only do once?
    '/w21-git':'/dat0/tenki7-ssd/w21-git',   # -- ditto for w21-git
    '/home/fiorino':'/dat0/tenki7-ssd/home/fiorino',   # -- only once to transition to new 1 Tb SSD
    w2.HfipProducts:'/dat0/%s'%(w2.HfipProducts),
    }


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            }

        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'reverse':      ['R',0,1,' reverse direction'],
            'justDat':      ['d',0,1,' just data'],
            'noDat':        ['D',0,1,' just home /w21'],
            'doDat1':       ['1',0,1,' set of data to tenki7-vb/dat1'],
            'doit':         ['X',0,1,'do it'],
            }


        self.purpose='''
rsync from tenki6 to tenki7 via  to dat0 (usb3 5 TB drive)
(c) 2009-2019 Michael Fiorino,NOAA ESRL'''

        self.examples='''
%s -N '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(ropt == '' and not(doit)):
    print 'WWW -- must set -X flag to execute'
    sys.exit()

sds=tdirs.keys()
sds.sort()

rsopt='-alv'
rsopt="%s --no-group --no-perms "%(rsopt)

if(ropt == 'norun'): rsopt='-alvn'

if(doit and ropt == 'norun'): ropt=''

MF.sTimer('ALL-%s'%(CL.pyfile))
for sd in sds:
    
    isDat=(mf.find(sd,'dat') or mf.find(sd,'hfip'))
    if(doDat1): isDat=(mf.find(sd,'dat') and not(mf.find(sd,'hfip')))
    #print 'qqq',sd,justDat,isDat
    
    orsopt=rsopt
    #if(sd == '/w21'):     orsopt='''%s --exclude dat/'''%(rsopt) # put the basic data dir back...
    if(sd == '/w21/dat'): orsopt='''%s --exclude tc/ --exclude pr/'''%(rsopt)
    td=tdirs[sd]
    
    # -- now reverse since used on FINAL tenki7 -> dat0
    #
    if(reverse):
        if(not(isDat)): continue
        cmd='time rsync %s %s/ %s/'%(orsopt,td,sd)
    else:
        if(justDat and not(isDat) or (isDat and noDat)): continue
        cmd='time rsync %s %s/ %s/'%(orsopt,sd,td)
    mf.runcmd(cmd,ropt)
    
MF.dTimer('ALL-%s'%(CL.pyfile))
