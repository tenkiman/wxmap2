#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcbase import *

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'dtgopt'],
            #2:['model',     'model: hwrf|fv7g|fv7e'],
        }

        self.options={
            'verb':                 ['V',0,1,'verbose'],
            'override':             ['O',0,1,'1 - '],
            'ropt':                 ['N','','norun','ropt'],
            'reverse':              ['R',0,1,'reverse direction FROM wxmap2 TO local'],
            'justAdeck':            ['A',0,1,'just do the tmtrkN adecks'],
            'justDSs':              ['D',0,1,'just do DSs, CARQ, names, tcvitals'],
            'adYearOpt':            ['Y:',None,'a','set years to do justAdeck'],
            'doPartN':              ['P:',1,'i','do a group of rsyncs: 1) as before; 2) ops abddecks'],
            'doit':                 ['X',0,1,' do it...'],
        }


        self.purpose='''rsync mirror tc/names and tc/DSs locally
(c) 1992-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s 2019030912 hwrf'''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(not(doit) and ropt != 'norun'): sys.exit()

# -- just get current year and curyear+1 from wxmap2
#

(shemoverlap,curyear,curyearp1)=CurShemOverlap(curdtg)

rsyncOpt='-alv'

# -- adecks
#
zSources=['tmtrkN','mftrkN']
aSources=['ec-wmo','ukmo','tmtrkN']
oaSources=['jtwc','nhc']

onKK=(w2.onKaze or w2.onKishou)

if(w2.onKaze):
    sdirBase='/data/amb/users/fiorino/w21/dat/tc'
elif(w2.onKishou):
    sdirBase=w2.TcDatDir
else:
    # -- auto reverse if NOT onKaze or onKishou
    #
    sdirBase=w2.TcDatDir

tdirBase='/home3/mfiorino/tcdat'

if(adYearOpt != None):
    adYears=[adYearOpt]
    justAdeck=1
    curyear=adYearOpt
else:
    adYears=[curyear]

if(not(justAdeck) and not(onKK) and not(w2.onTenki) ): reverse=1

rsyncOptBase='''--rsh="ssh -p2222" --size-only'''

MF.sTimer('all-rsync-wxmap2')


if(doPartN != None and doPartN == 1):

    # -- dss
    #
    sdirDSs='%s/DSs/'%(sdirBase)
    tdirDSs='''"mfiorino@wxmap2.com:%s/DSs/"'''%(tdirBase)
    
    if(reverse):
        sdir=tdirDSs
        tdir=sdirDSs
    else:
        sdir=sdirDSs
        tdir=tdirDSs
    
    if(adYearOpt != None):
        rsyncOptDSs='''--include="?d2-*%s*" --include="mdecks2*" --exclude="*" %s'''%(adYearOpt,rsyncOptBase)
    else:
        rsyncOptDSs='''--include="?d2-*%s*" --include="?d2-*%s*"  --include="mdecks2*" --exclude="*" %s'''%(curyear,curyearp1,rsyncOptBase)
        
    cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptDSs,sdir,tdir)
    mf.runcmd(cmd,ropt)
    
    # -- names
    #
    sdirNames='%s/names/'%(sdirBase)
    tdirNames='''"mfiorino@wxmap2.com:%s/names/"'''%(tdirBase)
    if(reverse):
        sdir=tdirNames
        tdir=sdirNames
    else:
        sdir=sdirNames
        tdir=tdirNames
    
    rsyncOptNames='''--include="TCstats????.py" --include="TCnames????.py" --exclude="*" %s'''%(rsyncOptBase)
    cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptNames,sdir,tdir)
    mf.runcmd(cmd,ropt)
    
    
    # -- tcvitals
    #
    sdirTCvitals='%s/tcvitals/'%(sdirBase)
    tdirTCvitals='''"mfiorino@wxmap2.com:%s/tcvitals/"'''%(tdirBase)
    
    if(reverse):
        sdir=tdirTCvitals
        tdir=sdirTCvitals
    else:
        sdir=sdirTCvitals
        tdir=tdirTCvitals
    
    rsyncOptTCvitals='''--include "tcvitals.%s??????.txt" --exclude="*" %s'''%(curyear,rsyncOptBase)
    cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCvitals,sdir,tdir)
    mf.runcmd(cmd,ropt)
    
    # -- carq
    #
    sdirTCcarq='%s/carq/%s/'%(sdirBase,curyear)
    tdirTCcarq='''"mfiorino@wxmap2.com:%s/carq/%s/"'''%(tdirBase,curyear)
    
    if(reverse):
        sdir=tdirTCcarq
        tdir=sdirTCcarq
    else:
        sdir=sdirTCcarq
        tdir=tdirTCcarq
    
    rsyncOptTCcarq='''--include "btops*" --exclude="*" %s'''%(rsyncOptBase)
    cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCcarq,sdir,tdir)
    mf.runcmd(cmd,ropt)
    
    if(justDSs):
        MF.dTimer('all-rsync-wxmap2')
        sys.exit()
    
    # -- ATCF-form of adecks from main sources
    #
    for aSource in aSources:
        sdirTCadeck='%s/adeck/atcf-form/%s/%s/'%(sdirBase,curyear,aSource)
        tdirTCadeck='''"mfiorino@wxmap2.com:%s/adeck/%s/%s/"'''%(tdirBase,curyear,aSource)
    
        if(reverse):
            sdir=tdirTCadeck
            tdir=sdirTCadeck
        else:
            sdir=sdirTCadeck
            tdir=tdirTCadeck
    
        rsyncOptTCadeck='''--include "a*.dat" %s'''%(rsyncOptBase)
        cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCadeck,sdir,tdir)
        mf.runcmd(cmd,ropt)
    
    
    # -- zip-form of adecks from main sources
    #
    
    for zSource in zSources:
        sdirTCadeck='%s/adeck/%s/%s/'%(sdirBase,zSource,curyear)
        tdirTCadeck='''"mfiorino@wxmap2.com:%s/adeck/%s/%s/"'''%(tdirBase,zSource,curyear)
    
        if(reverse):
            sdir=tdirTCadeck
            tdir=sdirTCadeck
        else:
            sdir=sdirTCadeck
            tdir=tdirTCadeck
    
        rsyncOptTCadeck='''--include "*.zip" %s'''%(rsyncOptBase)
        cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCadeck,sdir,tdir)
        mf.runcmd(cmd,ropt)
        
    
    # -- tmtrkN runs
    #
    sdirTCadeck='%s/tmtrkN/%s/'%(sdirBase,curyear)
    tdirTCadeck='''"mfiorino@wxmap2.com:%s/tmtrkN/%s/"'''%(tdirBase,curyear)
    
    if(reverse):
        sdir=tdirTCadeck
        tdir=sdirTCadeck
    else:
        sdir=sdirTCadeck
        tdir=tdirTCadeck
    
    rsyncOptTCadeck='''--include "*.zip" %s'''%(rsyncOptBase)
    cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCadeck,sdir,tdir)
    mf.runcmd(cmd,ropt)

if(doPartN != None and doPartN == 2):

    # -- ops adecks 
    #
    for oaSource in oaSources:
        sdirTCadeck='%s/adeck/%s/%s/'%(sdirBase,oaSource,curyear)
        tdirTCadeck='''"mfiorino@wxmap2.com:%s/adeck/%s/%s/"'''%(tdirBase,oaSource,curyear)
    
        if(reverse):
            sdir=tdirTCadeck
            tdir=sdirTCadeck
        else:
            sdir=sdirTCadeck
            tdir=tdirTCadeck
    
        rsyncOptTCadeck='''--include "*" %s'''%(rsyncOptBase)
        cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCadeck,sdir,tdir)
        mf.runcmd(cmd,ropt)
    


    # -- ops bdecks 
    #
    for oaSource in oaSources:
        sdirTCadeck='%s/bdeck/%s/%s/'%(sdirBase,oaSource,curyear)
        tdirTCadeck='''"mfiorino@wxmap2.com:%s/adeck/%s/%s/"'''%(tdirBase,oaSource,curyear)
    
        if(reverse):
            sdir=tdirTCadeck
            tdir=sdirTCadeck
        else:
            sdir=sdirTCadeck
            tdir=tdirTCadeck
    
        rsyncOptTCadeck='''--include "*" %s'''%(rsyncOptBase)
        cmd='''rsync %s %s %s %s'''%(rsyncOpt,rsyncOptTCadeck,sdir,tdir)
        mf.runcmd(cmd,ropt)



 

MF.dTimer('all-rsync-wxmap2')
sys.exit()

