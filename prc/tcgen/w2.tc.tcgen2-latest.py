#!/usr/bin/env python
from WxMAP2 import *
from M import MFutils
MFd=MFutils()
w2=W2()

sdir="%s/tcgenDAT"%(w2.HfipWebBdir)
tdir="%s/tcgen/latest"%(w2.HfipWebBdir)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class AdgenCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv is None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['dtgopt',  'run dtgs'],
        }

        self.defaults={
            'doupdate':0,
            'BMoverride':0,
        }

        self.options={
            'override':      ['O',0,1,'override'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doit':          ['X',1,0,'execute'],
        }



        self.purpose='''
purpose -- set latest .png to to latest/*latest.png '''
        self.examples='''
%s cur
'''
#w2.ls()
#sys.exit()

argv=sys.argv
CL=AdgenCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

print 'CCC',curdtg,curyear

if(doit): ropt=''

mask="%s/%s/??????????"%(sdir,curyear)
print mask
gdtgs=glob.glob(mask)
adtgs=[]
for gdtg in gdtgs:
    dtg=gdtg[-10:]
    adtgs.append(dtg)
    
    
adtgs.sort()
latestDtg=adtgs[-1]
mask="%s/%s/%s/*.png"%(sdir,curyear,latestDtg)
curPngs=glob.glob(mask)

for png in curPngs:
    (fdir,ffile)=os.path.split(png)
    fdtg=ffile.split('.')[1]
    lpng=ffile.replace(fdtg,'latest')
    lpng="%s/%s"%(tdir,lpng)
    cmd="ln -s -f %s %s"%(png,lpng)
    mf.runcmd(cmd,ropt)


sys.exit()
