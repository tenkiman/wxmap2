#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()

import FM
rt=FM.rtfimRuns()


def printLsout(lsout,fimpaths,lspath=0,lstcards=0):

    acards=[]
    tcards=[]
    ocards=[]

    for n in range(0,len(lsout)):
        lso=lsout[n]

        
        if(lso is StringType):
            card=lso[0:-1]
        else:
            card=str(lso)

        card=card.strip()
        if(MF.find(card[0:4],'time')):
            tcards.append(card[0:132])
        elif(MF.find(card,'YYYYY')):
            acards.append(card)
        else:
            ocards.append(card)

    # -- print atcf cards
    #
    if(len(acards) > 0):
        for acard in acards:
            print acard
    
    if(len(acards) > 1): print


    # -- print basic run stats
    #
    ncases=len(ocards)/3
    for i in range(0,ncases):
        ofimpaths=fimpaths[i]
        
        for j in range(0,3):
            ocard=ocards[i*3+j]
            try:
                sumN=int(ocards[i*3+2])
            except:
                print 'something wrong with this card: ',ocard,' and sumN: ',(i*3+2),ocards[i*3+2]
                continue
            tt=ocard.split()
            if(len(tt) == 0): continue
            name=tt[0]
            ln=len(name)
            rp=ocard.rfind(name)
            ln=ln+rp
            c1=ocard[0:ln]
            c1="% 30s"%(name)
            c2=ocard[ln:]
            if(j == 0): nc2=len(ocard[:-1])
            if(j == 0):
                pcard="%s%s"%(c1,c2[:-1])
                pcard="%-90s"%(pcard)
            elif(j == 1 and sumN > 0):
                pcard="%-90s EEEEE!!!!! #fim_C*: %s"%(pcard,ocard)
            elif(j == 2 and sumN > 0):
                if(int(ocard) > 0):
                    ocard="%-8s"%(ocard)
                    pcard="%-90s #NaNs: %s"%(pcard,ocard)

        if(len(ofimpaths) > 0):
            ofimpath=ofimpaths[0]
            if(not(lspath)): ofimpath=''
            print "%s %s"%(pcard,ofimpath)
        else:
            print pcard

    if(lstcards):
        for tcard in tcards:
            print tcard
            


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
from M import CmdLine

class LsFimCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt', 'no default'],
            2:['modelrun', 'no default'],
            }
            
        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'dols':['l',1,0,'do NOT do short list'],
            'doLongls':['L',0,1,'1 - list'],
            'doRsync':['R',0,1,'1 - rsync'],
            'override':['O',0,1,'1 - override'],
            'lspath':['P',0,1,'1 - ls fimpaths'],
            }


        self.purpose='''
purpose: run fp2 to do ls, etc. with rtfimRun properties from FM
rtfimRuns:

%s
'''%(rt.getRunlist())

        
        self.examples='''
  %s cur12-12 rtfimy
'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#
    
argv=sys.argv

CL=LsFimCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)
modelruns1=modelrun.split(',')
modelruns2=modelrun.split('.')

if(len(modelruns1) == 1): modelruns=[modelrun]
if(len(modelruns1) > 1): modelruns=modelruns1
if(len(modelruns1) > 1 and len(modelruns2) >= len(modelruns1)): modelruns=modelruns2
if(modelrun == 'all'): modelruns=FM.models

lsout=[]
fimpaths=[]

for dtg in dtgs:

    for modelrun in modelruns:

        mr=rt.getRun(modelrun)
        if(modelrun == 'rtfimz' and mf.dtgdiff('2010082900',dtg) >= 0): mr.npe='240'

        gopt=npeopt=fimrunopt=expnameopt=''
        if(mr.g != ''): gopt="-g %s"%(mr.g)
        if(mr.npe != ''): npeopt="-n %s"%(mr.npe)
        if(mr.fimrun != ''): fimrunopt="-F %s"%(mr.fimrun)
        if(mr.expname != ''): expnameopt="-E %s"%(mr.expname)

        if(FM.onWjet):
            fe=FM.setFE(dtg,modelrun)
        else:
            fe=FM.setFE(dtg,modelrun,sroot=FM.trootWjet,troot=FM.lrootLocal)

        fr=FM.FimRun(fe,docpalways=0,verb=verb)
        fr.lsSdir(verb=verb)
        fr.LsGrib()

        if(fr.tdatathere == 0):
            print 'WWW no data for modelrun: ',modelrun,' dtg: ',dtg
            continue

        continue
        
        cmd="%s/w2.fim.post2.py %s %s %s %s %s %s"%(CL.pydir,dtg,mr.name,gopt,npeopt,fimrunopt,expnameopt)
        if(dols):     cmd="%s -l"%(cmd)
        if(doRsync):     cmd="%s -R"%(cmd)
        if(doLongls):     cmd="%s -L"%(cmd)
        if(override):     cmd="%s -O"%(cmd)

        if(dols): ropt='quiet'
        rc=MF.runcmd(cmd,ropt)
        if(rc != None and dols):
            lsout=lsout+rc

        lsout=lsout+[fr.nfimruns]+[fr.sumNaNs]
        fimpaths.append(fr.fimpaths)


if(dols and ropt == 'quiet'): printLsout(lsout,fimpaths,lspath=lspath)
    
#    if(len(modelruns) > 1): print


    
