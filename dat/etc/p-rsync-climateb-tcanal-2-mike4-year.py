#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):
        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yearopt',  'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            }

        self.options={
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            }

        self.purpose='''
rsync TO mike4:dat120 FROM climateb tc/tcanal/*grb2
'''
        self.examples='''
%s 2000-2005  # cycle through years 2000-2005'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='mdeck')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

yy=yearopt.split('-')

if(len(yy) == 2):
    byear=yy[0]
    eyear=yy[1]

    years=MF.YearRange(byear,eyear)
else:
    years=yy

rsyncOpt='-alv'

MF.sTimer('climate-mike4-ALL')

for year in years:
    MF.sTimer('climate-mike4 %s'%(year))
    cmd="rsync %s mfiorino@climateb:/braid1/mfiorino/w22/dat/tc/tcanal/%s/ /dat21/dat/tc/tcanal/%s/"%(rsyncOpt,year,year)
    mf.runcmd(cmd,ropt)
    MF.dTimer('climate-mike4 %s'%(year))

MF.dTimer('climate-mike4-ALL')
