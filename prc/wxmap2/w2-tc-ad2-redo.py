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
            1:['year',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'quiet':               ['q',0,1,'1 - turn off all diag messages'],
            'ropt':                ['N','','norun',' norun is norun'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            'do9Xonly':            ['9',0,1,'just do 9X'],
            'basinOpt':            ['b:',None,'a','set basin'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
redo ad2 decks if .pypdb goes south
sources: %s'''%(w2.TCsourcesActive)
        self.examples='''
%s cur -9  # redo all 9x for cur year'''

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

print 'yyy',year
if(year == None or type(year) != StringType):
    print 'EEE -- must set year as 1st plain opt'
    sys.exit()


if(year == 'cur'): year=curyear

# -- first clean off the ad2 
#

ad2s=glob.glob("%s/ad2*%s*.pypdb"%(dssdir,year))
bd2s=glob.glob("%s/bd2*%s*.pypdb"%(dssdir,year))

ad2Basins9X={}
ad2BasinsNN={}

for ad2 in ad2s:
    (ddir,dfile)=os.path.split(ad2)
    tt=dfile.split('.')[0].split('-')
    basin=tt[-2]
    if(mf.find(dfile,'9X')):
        basin=tt[-2]
        ad2Basins9X[basin]=ad2
        if(verb): print '9Xtt',tt,basin
    else:
        basin=tt[1]
        ad2BasinsNN[basin]=ad2
        if(verb): print 'NNtt',tt,basin
        
if(do9Xonly):
    ad2Basins=ad2Basins9X
    ad2Opt='-9'
else:
    ad2Basins=ad2BasinsNN
    ad2Opt=''
    
basins=ad2Basins.keys()
basins.sort()

if(basinOpt != None):
    if(basinOpt == 'all'):
        basins=['i','w','e','c','l','h']
        
    else:
        basins=basinOpt.split(',')
    
bopt='-S '
do9X=0
for basin in basins:
    if(len(basin) == 1):
        b1id=basin
        basin=Basin1toBasin2[b1id.upper()]
        basin=basin.lower()
    else:
        b1id=Basin2toBasin1[basin.upper()].lower()
        
    if(b1id == 's'): b1id='h'
    if(b1id == 'a' or b1id == 'b'): b1id='i'
    
    ad2=bd2=None
    bopt="%s%s.%s,"%(bopt,b1id,year)
    if(basin in (ad2Basins9X.keys())):
        ad2=ad2Basins9X[basin]
        bd2=ad2.replace('ad2','bd2')
        do9X=1
    
    if(basin in (ad2BasinsNN.keys())):
        ad2=ad2BasinsNN[basin]
        bd2=ad2.replace('ad2','bd2')

    if((doIt or ropt == 'norun') and ad2 != None):
        cmd="rm %s"%(ad2)
        mf.runcmd(cmd,ropt)
        cmd="rm %s"%(bd2)
        mf.runcmd(cmd,ropt)
        print
    
bopt=bopt[0:-1]

# -- if previously removed...just nhem & shem
#
if(bopt == '-S' or basinOpt == 'all'):
    bopt='-S i.%s,w.%s,c.%s,e.%s,l.%s,h.%s'%(year,year,year,year,year,year)

MF.sTimer('ad2-redo-ALL')

MF.sTimer('ad2-redo-%s'%(bopt))
ad2src='all'
cmd="time %s/w2-tc-dss-ad2.py %s %s %s -O1"%(prcdir,ad2src,bopt,ad2Opt)
mf.runcmd(cmd,ropt)    
MF.dTimer('ad2-redo-%s'%(bopt))

if(do9X):
    MF.sTimer('ad2-redo-9X-%s'%(bopt))
    ad2src='all'
    if(mf.find(ad2Opt,'-9')):
        ad2Opt=''
    cmd="time %s/w2-tc-dss-ad2.py %s %s %s -9 -O1"%(prcdir,ad2src,bopt,ad2Opt)
    mf.runcmd(cmd,ropt)    
    MF.dTimer('ad2-redo-9X-%s'%(bopt))

MF.dTimer('ad2-redo-ALL')
