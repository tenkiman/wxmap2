#!/usr/bin/env python
from WxMAP2 import *
w2=W2()


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
            'doit':                 ['X',0,1,' do it...'],
        }


        self.purpose='''wget mirror tc/names and tc/DSs locally
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
    
ddirs=['names','DSs','tcvitals','carq/%s'%(curyear)]    
sbDir='https://ruc.noaa.gov/hfip/fiorino/tc'
sbDir='http://tcdat.wxmap2.com'
tbDir="%s/tc"%(w2.DatBdirW2)

for ddir in ddirs:

    tdir="%s/%s"%(tbDir,ddir)
    sdir="%s/%s"%(sbDir,ddir)
    
    if(ropt != 'norun'):
        MF.ChkDir(tdir, 'mk')
    else:
        print 'target Dir: ',tdir
    
    MF.ChangeDir(tdir)
        
    cmd='wget -nv -nd -m -nH -np %s/'%(sdir)
    mf.runcmd(cmd,ropt)
    

