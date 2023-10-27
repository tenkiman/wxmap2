#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


class W2WebCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            }

        self.defaults={
            }

        self.options={
            'doit':        ['X',0,1,' doit!'],
            'ropt':        ['N','norun','',' norun is norun'],
            'verb':        ['V',0,1,'verb=1 is verbose'],
            'override':    ['O',0,1,'override'],
            }

        self.purpose='''
purpose -- generate home page
%s dtg [-u]
'''
        self.examples='''
%s cur -u
'''

argv=sys.argv
CL=W2WebCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

ropt='norun'
if(doit):
    ropt=''
    
tdir=w2.W2BaseDirWeb
sdir=w2.W2BaseDirWebConfig

lnOpt='-f -s'
lnOpt='-s'
phps=glob.glob("%s/config/php/*.php"%(sdir))

for php in phps:
    cmd="ln %s %s %s/."%(lnOpt,php,tdir)
    mf.runcmd(cmd,ropt)

#sys.exit()

links=[
    '80.htaccess',
    'cgi-bin',
    'classes',
    'css',
#    'diag.php',
    'doc',
    'icon',
    'js',
    'prw2.htm',
    'favicon.ico',
    'template',
#    'php',
]


for link in links:
    cmd="ln %s %s/config/%s %s/%s"%(lnOpt,sdir,link,tdir,link)
    mf.runcmd(cmd,ropt)

    


sys.exit()
