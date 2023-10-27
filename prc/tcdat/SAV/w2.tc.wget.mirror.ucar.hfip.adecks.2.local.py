#!/usr/bin/env python

from tcbase import *

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
purpose -- mirror adecks from hfip stream15 to local
%s cur
'''
        self.examples='''
%s cur
'''




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

decks=['adeck','adeck.jtwc']

# 2012
decks=['adeck']

sbdir=w2.HfipDatDir
tbdir=w2.TcDatDir

for deck in decks:

    af=w2.HfipFtpserver
    al=w2.HfipLogin
    ap=w2.HfipPasswd
    ad=w2.HfipDatDir

    if(mf.find(deck,'adeck')): dtype='a'

    if(deck == 'adeck'):
        sdir="%s/stream15"%(sbdir)
        deckdir='adeck'
        sdir='data/tcmt/h2012/'
        sdir='%s/d%s/'%(ad,yyyy)

    elif(deck == 'adeck.jtwc'):
        sdir="%s/jtwc"%(sbdir)
        deckdir='adeck'

        

    tdir="%s/%s/%s/%s/"%(tbdir,deckdir,'hfip',yyyy)
    if(mf.ChkDir(tdir,diropt='mk') != 0): os.chdir(tdir)
    print 'CCC: working in: ',os.getcwd()

    #wgetopt='-m -nd -T 180 -t 2 -nv'
    #cmd="wget %s \"ftp://%s/%s/%s??*%s*.dat*\""%(wgetopt,af,sdir,dtype,yyyy)
    #mf.runcmd(cmd,ropt)

    wgeturl='''"http://www.ral.ucar.edu/%s"'''%(sdir)
    wgetopt=" --user=%s --password=%s --mirror -nd -np -T 60 -t 1"%(al,ap)
    wgetmask='''-A "a????%s*"'''%(yyyy)
    wgettarget="-P %s"%(tdir)
    cmd="wget %s %s %s %s"%(wgetopt,wgetmask,wgettarget,wgeturl)
    mf.runcmd(cmd,ropt)

    


sys.exit()

