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
            'nlev':          ['n:',1,'i', ' norun is norun'],
            'dodirs':        ['d',0,1,'do by dirs'],
            'doTotOnly':      ['T',0,1,'only output totals'],
            'help':          ['h',0,1,'pring help'],
            }

        self.purpose='''
purpose -- recursive du -s to list usage
%s [path] :: default = '.'
'''
        self.examples='''
%s ../tmp
'''




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='all')
argv=sys.argv
CL=MssCmdLine(argv=argv)
#CL.CmdLine(blankPlainArgs=1)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
ns=54
nd=16

if(path == '.'):
    opath=curdir
else:
    opath=path

if(dodirs):
    opaths=[]
    dirs=os.listdir('.')
    for dir in dirs:
        if(os.path.isdir(dir) and not(mf.find(dir,'.'))): opaths.append(dir)
    opaths.sort()
    
else:
    opaths=[opath]

tt=os.uname()
osname=tt[0]
if(mf.find(osname,'arwin')):
    excludeOpt='''-I "*snapshot*"'''
else:
    excludeOpt='''--exclude "*snapshot*"'''

opaths.sort()

for opath in opaths:

    opath=os.path.realpath(opath)
    print "%s%s"%(opath,((ns+nd-len(opath))*'.'))
    print "%s"%((ns+nd)*'-')
    if(dodirs): continue

    n0=path.replace('./','').count('/')
    os.chdir(path)
    rc=os.popen('''du -k %s'''%(excludeOpt)).readlines()

    rc.sort() 

    format="%%-%ds :: %%10d"%(ns)
    n0=0
    ntot=0
    ndir=0

    ofiles={}

    for r in rc:
        rr=r.split('\t')
        siz=rr[0]
        try:
            file=rr[1]
        except:
            continue
        #file=file.replace('./','')
        file=file.replace('\n','')
        siz=int(siz)
        nl=file.count('/')
        nl=nl-n0
        #print 'nnnnnnnnnnn',n0,nl,nlev,file
        if(nl<=nlev):

            if(file == '.'):
                ntot=siz
            elif(nl==1):
                ndir=ndir+siz

            if(len(file)>=ns):
                ofile=file[0:ns-3]+'...'
            else:
                ofile=file[0:ns]

            if(file != '.'):
                ofiles[ofile]=(ns,siz)
                #mf.PrintCurrency(ofile,ns,siz)


    files=ofiles.keys()
    files.sort()

    for file in files:
        oo=file
        (ns,siz)=ofiles[file]
        mf.PrintCurrency(oo,ns,siz)


    nfile=ntot-ndir

    if(len(files) > 1): print "%s"%((ns+nd)*'-')
    mf.PrintCurrency('Total..................',ns,ntot)
    if(not(doTotOnly) and len(files) >= 1 ): mf.PrintCurrency('Files..................',ns,nfile)
    if(not(doTotOnly) and len(files) > 1 ): mf.PrintCurrency('Dirs...................',ns,ndir)


if(not(doTotOnly)): MF.dTimer(tag='all')

