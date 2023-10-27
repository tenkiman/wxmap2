#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from TCtmtrkN import TmTrkN,getCtlpathTaus
from tcbase import TcData,TcAidTrkAd2Bd2

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
def cycleDtgsModels(dtgopt,modelopt):

    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    models=modelopt.split(',')

    if(len(models) > 1 or modelopt == 'all' or len(dtgs) > 1):

        for dtg in dtgs:

            if(modelopt == 'all'):
                models=CL.models
                if(MF.is0618Z(dtg)): models=CL.models0618

            for model in models:
                cmd="%s %s %s"%(CL.pypath,dtg,model)
                for o,a in CL.opts:
                    cmd="%s %s %s"%(cmd,o,a)
                mf.runcmd(cmd,ropt,lsopt='')

        sys.exit()

    else:
        model=modelopt
        dtg=dtgs[0]

    return(dtg,model)


def invAnl(dtgopt,modelopt):


    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    models=modelopt.split(',')

    TT=TmTrkN(dtg=None,model=None,ctlpath=None,taus=None,maxtauModel=None,doInvOnly=1)

    inv=TT.invTmtrkN

    kk=inv.keys()

    dtgs=[]
    sumStms={}

    for k in kk:

        if(len(k) <= 2): continue

        if(mf.find(k[2],'sumStm')): 
            dtg=k[0]
            model=k[1]

            tt=inv[k]
            tt=inv[k].split()
            good=tt[2]
            fail=tt[4]
            stop=tt[6]

            dtgs.append(dtg)
            val="%s %s %s %s"%(model,good,fail,stop)
            MF.appendDictList(sumStms,dtg,val)


    dtgs=mf.uniq(dtgs)
    dtgs.sort()

    for dtg in dtgs:
        print dtg,sumStms[dtg]

    sys.exit()

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgs'],
            2:['modelopt',  """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
        }

        self.defaults={
            'doupdate':0,
            'doAdeck2':1,
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'overrideDatChk':   ['D',0,1,'override DataGENoverride'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'dols':             ['l',0,1,'1 - list'],
            'dotrkonly':        ['t',0,1,'1 - run only in tracker mode'],
            'dolsLong':         ['L',0,1,'1 - long list'],
            'doChkIfRunning':   ['r',1,0,'no NOT chk if running'],
            'chkAd2Tracker':    ['C:',-999,'i','check of tracker has been done for NN only (1) or both NN&9X (2)'],

        }

        self.purpose="""
run new version of Tim Marchok's genesis tracker"""

        self.examples='''
%s cur12 gfs2'''

        if(w2.Nwp2ModelsActW20012 != None): self.models=w2.Nwp2ModelsActW20012
        if(w2.Nwp2ModelsActW20618 != None): self.models0618=w2.Nwp2ModelsActW20618

        self.purpose="""
super .py to run new version of Tim Marchok's genesis tracker and MIKE tracker and clean
00/12 Models: %s
06/18 Models: %s"""%(self.models,self.models0618)

        self.examples='''
%s cur12 gfs2'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

# -----------------------------------  default setting of max taus
#
maxtau=168

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

(dtg,model)=cycleDtgsModels(dtgopt,modelopt)

trkonlyOpt=''
doverOptMF=''
if(override):
    if(dotrkonly):
        trkonlyOpt='-t'
        doverOptMF=''
    else:
        doverOptMF='-O'
    

overOpt=''
doverOpt=''
if(override): 
    overOpt='-O'
    doverOpt=overOpt
if(overrideDatChk): doverOpt="%s -D"%(overOpt)

chkAd2Opt=''
#if(chkAd2Tracker != 0):
#    chkAd2Opt='-C%d'%(chkAd2Tracker)
    
chkRunOpt=''
if(not(doChkIfRunning)):
    chkRunOpt='-r'
    
MF.sTimer('ALL-TRACKERS-%s-%s'%(dtg,model))

if(dols or dolsLong):
    overOpt=''
    doverOpt=''
    overrideDatChk=''
    chkAd2Opt='-l'
    if(dolsLong): chkAd2Opt='-L'
    chkAd2Tracker=0
    
    
MF.sTimer('tmtrkN-ALL-%s-%s'%(dtg,model))
cmd="%s/w2-tc-tmtrkN.py %s %s %s %s %s %s"%\
    (w2.PrcDirTctrkW2,dtg,model,doverOpt,trkonlyOpt,chkAd2Opt,chkRunOpt)

# -- really want to do this?
#for o,a in CL.opts:
#    if(o == '-O' or o == '-N'): continue
#    cmd="%s %s %s"%(cmd,o,a)

mf.runcmd(cmd,ropt,lsopt='')
MF.dTimer('tmtrkN-ALL-%s-%s'%(dtg,model))

if(dols or dolsLong):
    sys.exit()


if(chkAd2Tracker < 0):
    MF.sTimer('MFtrkN-ALL-%s-%s'%(dtg,model))
    cmd='%s/w2-tc-mftrkN.py %s %s %s %s'%(w2.PrcDirTctrkW2,dtgopt,model,doverOptMF,trkonlyOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('MFtrkN-ALL-%s-%s'%(dtg,model))
    
# -- clean tmtrkN
#
MF.sTimer('tmtrkN-CLEAN-ALL-%s-%s'%(dtg,model))
cmd="%s/w2-tc-tmtrkN.py %s %s -K"%(w2.PrcDirTctrkW2,dtg,model)
mf.runcmd(cmd,ropt)
MF.dTimer('tmtrkN-CLEAN-ALL-%s-%s'%(dtg,model))

# -- do w2-tc-zip -S trk-tmtrkN
#
MF.sTimer('w2-tc-zip-trk-tmtrkN-%s-%s'%(dtg,model))
cmd="%s/w2-tc-zip-adeck-tmtrkN.py %s -S trk-tmtrkN"%(w2.PrcDirTcdatW2,dtg)
mf.runcmd(cmd,ropt)
MF.dTimer('w2-tc-zip-trk-tmtrkN-%s-%s'%(dtg,model))

MF.dTimer('ALL-TRACKERS-%s-%s'%(dtg,model))

