#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['iyearopt',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'doMdeck1':            ['1',0,1,"""do mdeck1"""],
            'doMdeck2':            ['2',0,1,"""do mdeck2"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','','norun',' norun is norun'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
redo mdeck and mdeck2 by year when .pypdb goes south...'''

        self.examples='''
%s cur # redo curyear'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(not(doIt)): ropt='norun'
if(doIt): ropt=''

prcdir=w2.PrcDirTcdatW2
dssdir=w2.TcDatDirDSs

if(len(iyearopt.split('.')) == 2):
    years=MF.YearRange(iyearopt.split('.')[0],iyearopt.split('.')[1])

elif(len(iyearopt.split(',')) > 1):
    years=iyearopt.split(',')

# -- special case for setting years specifically, used for mftrkN
# -- turn off looping and set the mask...
#
elif(len(iyearopt.split('-')) == 2):
    years=iyearopt.split('-')
    dolooper=0
    setYearMask=1
    yearMasks=years
    
elif(len(iyearopt.split(',')) == 1):
    years=iyearopt.split(',')
    


for year in years:

    if(doMdeck1):

        cmda="%s/w2-tc-bt-adeck-final.py %s -p clean.all"%(prcdir,year)
        cmdb="%s/w2-tc-bt-bdeck-final.py %s -p clean.all"%(prcdir,year)
        cmdm="%s/w2-tc-bt-mdeck-final.py %s -p clean.all"%(prcdir,year)
        cmdMdk="%s/w2-tc-dss-mdeck.py -y %s -O"%(prcdir,year)
    
        mf.runcmd(cmda,ropt)
        mf.runcmd(cmdb,ropt)
        mf.runcmd(cmdm,ropt)
        mf.runcmd(cmdMdk,ropt)

    if(doMdeck2):
        cmdM2="%s/w2-tc-dss-md2.py -y %s -Y -K"%(prcdir,year)
        mf.runcmd(cmdM2,ropt)


