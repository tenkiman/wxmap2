#!/usr/bin/env python

from M import *
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
            1:['path',    'no default'],
            }

        self.defaults={
            'path':'.',         # -- if blankPlainArgs == 1 in CmdLine()
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'help':          ['h',0,1,'pring help'],
            }

        self.purpose='''
purpose -- kill 0 len files in a dir/
%s [path] :: default = '.'
'''
        self.examples='''
%s ../tmp
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer('all')
argv=sys.argv
CL=MssCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

nfiles0=0
files=glob.glob("%s/*"%(path))
for file in files:
    siz=MF.getPathSiz(file)
    if(siz == 0):
        nfiles0=nfiles0+1
        if(ropt != 'norun'):
            print 'killing: ',file
            os.unlink(file)
        else:
            print 'will kill: ',file

        
if(nfiles0 == 0):
    print 'no 0 len files in: ',path
else:
    print 'killed ',nfiles0
    
MF.dTimer('all')
