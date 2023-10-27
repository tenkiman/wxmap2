#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
MF=MFutils()
            
sources= [
    'cmc',
    'ecmwf',
    'esrl',
    'fimens',
    'fnmoc',
    'gfsenkf',
    'ncep',
    'ukmo',
]

sbdir='/data/tc/dat/tc/tceps'
sbdir='/dat16/dat/tc/tceps'

def getSyears(doprint=0):
    
    # -- get years by source
    #
    srcYears={}
    
    if(doprint): print
    for source in sources:
        
        sdir="%s/%s"%(sbdir,source)
        MF.ChangeDir(sdir,'quiet')
        years=glob.glob("????")
        years.sort()
        if(doprint): print 'source: %-10s'%(source),'years: ',years
        srcYears[source]=years

        MF.ChangeDir('..','quiet')
    
    if(doprint): print

    return(srcYears)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['sourceOpt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'yearOpt':       ['Y:',None,'a',"""source: %s"""%(str(sources))],
            'moOpt':         ['M:',None,'a','month Opt'],
            }

        self.purpose='''
convert tmtrkN adecks to zip archive'''
        
        self.examples='''
%s cmc -Y 2013'''


    def printSyear(self,doprint=0):
        srcYears=getSyears(doprint=doprint)
        return(srcYears)

MF.sTimer(tag='all')

argv=sys.argv
CL=MssCmdLine(argv=argv)
dop=0
if(len(argv) == 1): dop=1
srcYears=CL.printSyear(doprint=dop)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


months=range(1,13)

if(moOpt != None):
    tt=moOpt.split('.')
    if(len(tt) == 2):
        bmo=int(tt[0])
        emo=int(tt[1])
        months=range(bmo,emo+1)
    elif(len(tt) == 1):
        if(mf.find(moOpt,'cur')):
            CL.ls()
        else:
            months=[int(moOpt)]


if(sourceOpt != None):
    osources=sourceOpt.split(',')
else:
    print 'EEEE must set sourceOpt...'
    sys.exit()
    
    
MF.sTimer('ALL-zip-tceps')
for osource in osources:

    syears=srcYears[osource]
    if(yearOpt == 'all'):
        tyears=syears
    else:
        tyears=yearOpt.split(',')

    zyears=[]
    
    if(len(tyears) > 0):
        for tyear in tyears:
            if(tyear in syears): zyears.append(tyear)
    
    for year in zyears:


        MF.sTimer('YYY-zip-%s'%(year))
        sdir="%s/%s/%s"%(sbdir,osource,year)
        tdir="%s/%s"%(sbdir,osource)
            
        rc=MF.ChangeDir(sdir)
    
        for mo in months:

            MF.sTimer('YYY-MMM-zip-%s-%02d'%(year,int(mo)))
            zipfile='%s/%s-%s%02d.zip'%(tdir,osource,year,mo)
            zipcmd="zip %s -u -m -r %s%02d????"%(zipfile,year,mo)
            mf.runcmd(zipcmd,ropt)
            MF.dTimer('YYY-MMM-zip-%s-%02d'%(year,int(mo)))

        MF.dTimer('YYY-zip-%s'%(year))


MF.dTimer('ALL-zip-tceps')
