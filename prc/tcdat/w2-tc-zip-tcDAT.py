#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
MF=MFutils()
            

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['sourceOpt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'yearOpt':       ['Y:',None,'a','yearopt'],
            'DATopt':        ['D:',None,'a','DATopt'],
            }

        self.purpose='''
convert tmtrkN adecks to zip archive'''
        
        self.examples='''
%s cmc -Y 2013'''


MF.sTimer(tag='all')

argv=sys.argv
CL=MssCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

sbdir=w2.HfipProducts
tdir='/dat12/data/hfip/fiorino/products/hfip'

year=yearOpt

DATdirs=[
    'jtdiagDAT',
    'tcactDAT',
    'tcdiagDAT',
    'tcepsDAT',
    'tcgenDAT',
]


if(DATopt != None):
    DATdirs=[DATopt]
    
MF.sTimer('ALL-zip-tcDAT')



for ddir in DATdirs:

    rc=MF.ChangeDir('%s/%s/%s'%(sbdir,ddir,year),verb=-1)
    if(rc == 0):
        print """WWW -- can't zip ddir: %s for year: %s ... press ..."""%(ddir,year)
        continue
    else:
        mf.runcmd('pwd')
        dfiles=glob.glob("??????????")
        dfiles.sort()
        if(len(dfiles) == 0):
            print 'EEE - no dirs to zip'
            sys.exit()
        else:
            print 'III'
            print 'III -- there are %d directories in %s for year: %s'%(len(dfiles),ddir,year)
            print 'III'
            print 'III -- current zip files in %s'%(ddir)
            print 'III'
            
    zdir="%s/%s"%(tdir,ddir)
    MF.sTimer('YYY-%s-zip-%s'%(year,ddir))
    zipfile='%s/%s-%s.zip'%(zdir,ddir,year)
    curZfiles=glob.glob("%s/*zip"%(zdir))
    curZfiles.sort()
    for cz in curZfiles:
        print cz
    
    print 'III'
    zipcmd="zip %s -u -m -r %s??????"%(zipfile,year)
    mf.runcmd(zipcmd,ropt)
    MF.dTimer('YYY-%s-zip-%s'%(year,ddir))

MF.dTimer('ALL-zip-tcDAT')
