#!/usr/bin/env python

# -- new tc module with everything needed...
#
from WxMAP2 import *
w2=W2()

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['source',    'no default'],
            }

        self.options={
            'override':        ['O',0,1,'override'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'ropt':            ['N','','norun',' norun is norun'],
            }

        self.purpose='''
purpose -- parset techlist.dat files and make .py dictionary'''

        self.examples='''
%s nhc'''

def getAidDocs(sdir,tdmask):
    aidDocs={}
    tds=glob.glob("%s/*%s"%(sdir,tdmask))
    tdpath=tds[0]
    cards=open(tdpath).readlines()
    for card in cards[1:]:
        tt=card[1:68].split()
        desc=card[68:-1]
        aid=tt[1]
        retired=tt[-5]
        color=tt[-4]
        intVmax=tt[-3]
        raddef=tt[-2]
        default=tt[-1]
        aidDocs[aid]=(desc,default,retired,color,raddef,intVmax)
    return(aidDocs)

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

sdirJ=w2.TcStormsJtwcDir
sdirN=w2.TcStormsNhcDir

tdmask="20160601"

aidDocsJtwc=getAidDocs(sdirJ,tdmask)
aidDocsNhc=getAidDocs(sdirN,tdmask)


dicPath='aidDesc.py'
dicCardsJtwc=[]
dicCardsNhc=[]
    
dicCardsJtwc.append('aidDescJtwc={')
aids=aidDocsJtwc.keys()
aids.sort()
for aid in aids:
    desc=aidDocsJtwc[aid][0]
    card=''''%s':"""%s""",'''%(str(aid),desc)
    dicCardsJtwc.append(card)
dicCardsJtwc.append('}')
dicCardsJtwc.append(' ')

dicCardsNhc.append('aidDescNhc={')
aids=aidDocsNhc.keys()
aids.sort()
for aid in aids:
    desc=aidDocsNhc[aid][0]
    card=''''%s':"""%s""",'''%(str(aid),desc)
    dicCardsNhc.append(card)
dicCardsNhc.append('}')
dicCardsNhc.append(' ')
    
MF.WriteList2Path(dicCardsJtwc,dicPath,verb=1)
MF.WriteList2Path(dicCardsNhc,dicPath,verb=1,append=1)
    
    
MF.dTimer('all')

    
