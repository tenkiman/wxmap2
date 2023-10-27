#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


class AoriCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):


        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yearOpt',  '''years to push from mike4 -> climateb'''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','norun','norun','must use -X to run'],
            'doit':                ['X',0,1,'''do it'''],
            }

        self.purpose='''
push era5 fc from mike4 -> aori.climateb'''
        
        self.examples='''
%s 2000.2001 -N'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=AoriCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tt=yearOpt.split('.')
tt1=yearOpt.split(',')

if(len(tt1) > 1):
    years=[]
    for tt in tt1:
        years.append(int(tt))
        
elif(len(tt) == 2):
    years=MF.YearRange(int(tt[0]),int(tt[1]))
else:
    years=[int(yearOpt)]

if(doit): ropt=''
tdirAori='''mfiorino@climateb:/braid1/mfiorino/w22/dat/nwp2/w2flds/dat'''

model='era5'

for year in years:

    sdir='/w21/dat/nwp2/w2flds/dat/%s/%s'%(model,year)
    tdir="%s/%s/%s"%(tdirAori,model,year)
    
    print 'ssss',sdir,ropt
    print 'tttt',tdir

    MF.sTimer('era4-xfr-%s'%(year))
    cmd="rsync -alv %s/ %s/"%(sdir,tdir)
    mf.runcmd(cmd,ropt)
    MF.dTimer('era4-xfr-%s'%(year))


            
