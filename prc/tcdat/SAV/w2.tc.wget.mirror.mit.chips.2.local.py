#!/usr/bin/env python

from tcbase import *

bddir=None
W2doKazeTcDat=1
if(W2doKazeTcDat): bddir=w2.DATKazeBaseDir
w2=W2(W2BaseDirDat=bddir)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            }

        self.purpose='''
mirror adecks from mit chips intensity model to local'''
        
        self.examples='''
%s cur'''




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='all')

argv=sys.argv
CL=MssCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
MF.dTimer(tag='all')

(dtg,phr)=mf.dtg_phr_command_prc(dtgopt) 

if(dtgopt == 'cur'):
    do9Xstms=0
    yyyy=curdtg[0:4]
    mm=curdtg[4:6]

elif(dtg[0:4] == curyear):
    yyyy=curyear
    mm=dtg[4:6]

else:
    yyyy=dtg[0:4]
    mm=dtg[4:6]


try:
    (yyyy1,yyyy2)=yyyy.split('.')
    print 'qqqq ',yyyy1,yyyy2
    years=range(int(yyyy1),int(yyyy2)+1)
    print 'qqqqq ads',years
except:
    if(yyyy == 'all'):
        years=range(2000,2005)
    else:
        years=[yyyy]

#
# set years to two years to cover shem overlap
#
(shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)

if( (yyyy == curyear) and shemoverlap):
    years=[yyyy1,yyyy2]

#
# do previous year to catch overlap of storms crossing year
#
elif( (yyyy == curyear) and (int(mm) == 1)):
    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    years=[yyyym1,yyyy]

print 'dddddddddddd ',years,yyyy,curyear,int(mm)

decks=['adeck']

sbdir=w2.MitDatDir
tbdir=w2.TcAdecksMitDir

for deck in decks:

    af=w2.MitFtpserver
    al=w2.MitLogin
    ap=w2.MitPasswd

    sdir=sbdir

    tdir="%s/%s"%(tbdir,yyyy)
    if(mf.ChkDir(tdir,diropt='mk') != 0): os.chdir(tdir)
    print 'CCC: working in: ',os.getcwd()

    wgetopt='-m -nd -T 180 -t 2 -nv'

    if(int(yyyy) >= 2002 and int(yyyy) <= 2007):
        cmd="wget %s \"ftp://%s/%s/%s/CHIPS*%s*\""%(wgetopt,af,sdir,yyyy,yyyy)
    else:
        cmd="wget %s \"ftp://%s/%s/CHIPS*%s*\""%(wgetopt,af,sdir,yyyy)
        
    mf.runcmd(cmd,ropt)
    
mf.runcmd(cmd,ropt)



sys.exit()

