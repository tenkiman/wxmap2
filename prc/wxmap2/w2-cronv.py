#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            #1:['log',    'ptmpBaseDir log file'],
        }

        self.options={
            'verb':                 ['V',0,1,'verbose'],
            'override':             ['O',0,1,'1 - '],
            'ropt':                 ['N','norun','','ropt'],
            'doit':                 ['X',0,1,'doit'],
            'duration':             ['d:',12,'i','duration of cronv'],
        }


        self.purpose='''
make html of crontab
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s -X -d 24  # 24-h output'''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#
argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(doit):
    hpath='/%s/crontab.html'%(w2.wxhWeb)
    opath='/tmp/crl-reduced.txt'
    ocards=[]
    cards=MF.runcmdLog('crontab -l',quiet=1)
    for card in cards:
        tt=card.split()
        ltt=len(tt)
        if( len(card) > 0 and card[0] != '#' and len(tt) > 5):
            cmm=tt[0]
            chh=tt[1]
            cdd=tt[2]
            cwk=tt[3]
            cyr=tt[4]
            #print 'tt: ',tt
            ttc=tt[6:ltt-3]
            cmd=''
            for t in ttc:
                cmd="%s %s"%(cmd,t)
            cmd=cmd.replace('''"''','')
            cmd=cmd.replace('''$w2pdir/''','')
            
            ocard="%s %s %s %s %s %s"%(cmm,chh,cdd,cwk,cyr,cmd)
            ocards.append(ocard)
            #print len(cmd),ocard
            
    MF.WriteList2Path(ocards, opath)
    cmd="cat %s | cronv -w 130 -d %dh -o %s"%(opath,duration,hpath)
    MF.runcmd(cmd)
        
        
        

