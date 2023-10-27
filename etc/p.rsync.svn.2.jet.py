#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dir',        'directoy to rsync to jet'],
            2:['machine',    'machine= jet|zeus'],
            }
            
        self.options={
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'override':       ['O',0,1,'1 - '],
            'dryrun':         ['d',0,1,'1 - '],
            'reverse':        ['R',0,1,'1 - remote-local '],
            'delete':         ['D',0,1,'delete'],
            'sizeonly':       ['S',0,1,'size-only'],
            'doit':           ['X',0,1,'size-only'],
            'bypath':         ['P',0,1,"""no '/' in local/remote dirs"""],
            'jetsubdir':      ['J',0,1,"""put into subdir if going from jet to zeus"""],
            }

        self.defaults={
            }

        self.purpose='''
rsync svn-managed dir to jet
(c) 2009-2012 Michael Fiorino,NOAA ESRL'''
        
        self.examples='''
%s prec'''


        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

expath="./ex-svn.rsync.jet.txt"
localw2base=w2.W2BaseDir
if(machine == 'jet'):
    remotew2base='/lfs1/projects/fim/fiorino/w21'
    remoteurl='fiorino@jetscp.rdhpcs.noaa.gov'

if(machine == 'zeus'):
    remotew2base='/scratch1/portfolios/BMC/fim/fiorino/w21'
    remoteurl='Michael.Fiorino@dtn1.fairmont.rdhpcs.noaa.gov'

local="%s/%s/"%(localw2base,dir)
remote="%s:%s/%s/"%(remoteurl,remotew2base,dir)

if(bypath):
    local="%s/%s"%(localw2base,dir)
    remote="%s:%s/%s"%(remoteurl,remotew2base,dir)

if(jetsubdir):
    remote="%s"%(remote)
    local="%s/%s"%(local,machine)
        

if(reverse):
    remote="%s/%s/"%(localw2base,dir)
    local="%s:%s/%s/"%(remoteurl,remotew2base,dir)

    if(bypath):
        remote="%s/%s"%(localw2base,dir)
        local="%s:%s/%s"%(remoteurl,remotew2base,dir)

    if(jetsubdir):
        remote="%s/%s"%(remote,machine)
        local="%s"%(local)
        


dopt=''
if(delete): dopt='--delete'

sopt=''
if(sizeonly): sopt='--size-only'

rsyncopt='-alvn'
if(doit): rsyncopt='-alv'

if(dryrun):
    ropt=''
    rsyncopt='-alvn'
    

cmd="rsync %s %s %s --protocol=29 --exclude-from=%s %s %s"%(rsyncopt,dopt,sopt,expath,local,remote)
mf.runcmd(cmd,ropt)
