#!/usr/bin/env python

"""
%s

purpose:

  generate flat-file inventory database for epsanal plots

usages:

  %s dtgopt (bdtg.edtg[.ddtg])

  -R :: dorsync=0 (don't do it!)
  -n :: ndaybackopt
  
examples:

  %s cur 

(c) 2008 by Michael Fiorino, NHC
"""


from WxMAP2 import *
w2=W2()
import tcbase as TC

from w2switches import *

import M

MF=M.MFutils()


#
#  defaults
#
ropt=''
verb=0
dorsync=1
doretro=0
ndayback=30
ndaybackopt=None
override=0
doKlean=0

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "RNVn:r:OK")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-n",""): ndaybackopt=a
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-R",""): dorsync=0
        if o in ("-r",""): doretro=1
        if o in ("-O",""): override=1
        if o in ("-K",""): doKlean=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)



#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local routines


def PrintHash(hash,name='hash'):

    cards=[]
    kk=hash.keys()
    kk.sort()
    nh=len(hash)
    if(isinstance(kk[0],tuple)):
        nk=len(kk[0])
    else:
        nk=1


    card="%s %d %d"%(name,nk,nh)
    cards.append(card)

    for k in kk:
        card=''
        if(isinstance(k,tuple)):
            for n in k:
                card=card+' '+n
        else:
            card=card+' '+k
        card=card+' : '
        for n in hash[k]:
            card=card+' '+n
        cards.append(card)

    return(cards)


def getTcEpsInventory(webdir,dtgopt,ndayback):

    if(len(dtgopt.split('.')) > 1):
        tdtgs=mf.dtg_dtgopt_prc(dtgopt)

    elif(not(mf.find(dtgopt,'cur'))):
        edtg=mf.dtg_command_prc(dtgopt)
        bdtg=mf.dtginc(edtg,-24*ndayback)
        tdtgopt="%s.%s"%(bdtg,edtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    else:
        bdtg="cur-d%d"%(ndayback)
        tdtgopt="%s.cur"%(bdtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    allstmsDtg={}
    stmsDtg={}
    dtgsStm={}
    dtgsModel={}
    
    modelsDtgStm={}
    ptypesDtgStmModel={}
    pltsDtgStmModel={}
    pltfilesDtgStmModelTau={}
    tausDtgStmModel={}

    mf.ChangeDir(webdir)

    for dtg in tdtgs:
        year=dtg[0:4]
        maskpngec="%s/%s/ec.eps.*png"%(year,dtg)
        maskpng="%s/%s/esrl.eps.*png"%(year,dtg)
        maskgif="%s/%s/esrl.eps.*gif"%(year,dtg)

        plts=glob.glob(maskgif)+glob.glob(maskpngec)+glob.glob(maskpng)

        (allstms,stmopt)=TC.GetStmidsByDtg(dtg)
        
        # -- stms <- dtg

        for stm in allstms:
            try:
                allstmsDtg[dtg].append(stm)
            except:
                allstmsDtg[dtg]=[]
                allstmsDtg[dtg].append(stm)
                
        for plt in plts:
            
            if(mf.find(plt,'.veri.')): continue

            (dir,file)=os.path.split(plt)
            (base,ext)=os.path.splitext(file)

            tt=file.split('.')

            if(tt[0] == 'ec'):
                
                model='ecm_eps'
                ptype=tt[2]

                if(ext == '.png'):
                    stm="%s.%s"%(tt[3],tt[4])
                    #stm="%s"%(tt[3])
                    tau='single'

            else:
                
                model=tt[2]
                ptype=tt[3]
                
                if(ext == '.png'):
                    stm="%s.%s"%(tt[4],tt[5])
                    #stm="%s"%(tt[4])
                    tau=tt[6]
                elif(ext == '.gif'):
                    stm="%s.%s"%(tt[5],tt[6])
                    #stm="%s"%(tt[5])
                    tau='loop.gif'

            if(verb):
                print 'plt:   ',plt,' model: ',model,' ptype: ',ptype,' stm: ',stm,' tau: ',tau
            
            try:
                dtgsModel[model].append(dtg)
            except:
                dtgsModel[model]=[]
                dtgsModel[model].append(dtg)


            # -- stms <- dtg
            try:
                stmsDtg[dtg].append(stm)
            except:
                stmsDtg[dtg]=[]
                stmsDtg[dtg].append(stm)

            # -- dtgs <- stm
            try:
                dtgsStm[stm].append(dtg)
            except:
                dtgsStm[stm]=[]
                dtgsStm[stm].append(dtg)

            # -- models <- dtg,stm
            try:
                modelsDtgStm[dtg,stm].append(model)
            except:
                modelsDtgStm[dtg,stm]=[]
                modelsDtgStm[dtg,stm].append(model)
                
            # -- taus <- dtg,stm,model

            try:
                tausDtgStmModel[dtg,stm,model].append(tau)
            except:
                tausDtgStmModel[dtg,stm,model]=[]
                tausDtgStmModel[dtg,stm,model].append(tau)

            #-- ptypes <- dtg,stm,model
            
            try:
                ptypesDtgStmModel[dtg,stm,model].append(ptype)
            except:
                ptypesDtgStmModel[dtg,stm,model]=[]
                ptypesDtgStmModel[dtg,stm,model].append(ptype)

            # -- plts <- dtg,stm,model
            try:
                pltsDtgStmModel[dtg,stm,model].append(plt)
            except:
                pltsDtgStmModel[dtg,stm,model]=[]
                pltsDtgStmModel[dtg,stm,model].append(plt)
                
            if(dopltfiles):
                try:
                    pltfilesDtgStmModelTau[dtg,stm,model,tau].append(plt)
                except:
                    pltfilesDtgStmModelTau[dtg,stm,model,tau]=[]
                    pltfilesDtgStmModelTau[dtg,stm,model,tau].append(plt)



    def uNiqHash(hash):
        tt={}
        for kk in hash.keys():
            dd=hash[kk]
            dd=mf.uniq(dd)
            tt[kk]=dd
            
        return(tt)

    #
    # special handling for taus -- put loop.gif in front for tceps.php
    #
    def uNiqHashTaus(hash):
        tt={}
        for kk in hash.keys():
            dd=hash[kk]
            dd=mf.uniq(dd)
            dd.sort()
            if(dd[-1] == 'loop.gif'):
                odd=[]
                odd.append(dd[-1])
                for d in dd[0:-1]:
                    odd.append(d)
                tt[kk]=odd
            else:
                tt[kk]=dd
            
        return(tt)

    # uniq the dtgs by stm
    #
    dtgsStm=uNiqHash(dtgsStm)
        
    # uniq the dtgs by model
    #
    dtgsModel=uNiqHash(dtgsModel)

    stmsDtg=uNiqHash(stmsDtg)
    allstmsDtg=uNiqHash(allstmsDtg)
    modelsDtgStm=uNiqHash(modelsDtgStm)
    ptypesDtgStmModel=uNiqHash(ptypesDtgStmModel)
    tausDtgStmModel=uNiqHashTaus(tausDtgStmModel)
    pltsDtgStmModel=uNiqHash(pltsDtgStmModel)
    
    cards=[]
    if(len(stmsDtg) == 0):
        return(cards)
    cards=cards+PrintHash(stmsDtg)
    cards=cards+PrintHash(allstmsDtg)
    cards=cards+PrintHash(dtgsStm)
    cards=cards+PrintHash(dtgsModel)
    cards=cards+PrintHash(modelsDtgStm)
    cards=cards+PrintHash(tausDtgStmModel)
    cards=cards+PrintHash(ptypesDtgStmModel)
    if(dopltfiles):
        cards=cards+PrintHash(pltfilesDtgStmModelTau)

    return(cards)
            
        

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#



if(w2.W2doTcepsAnl == 0):
    print 'WWWWWWWWWWWWWWWWWW - turned off in w2switches.py'
    sys.exit()

    
MF.sTimer()

if(ndaybackopt != None): ndayback=int(ndaybackopt)
    
dopltfiles=0
print 'NNNN ndayback: ',ndayback,w2.W2doW3RapbRsync

webdir=w2.TcTcepsWebDir

# set the dtg range for inventory for season...why?
#
#if(dtgopt == 'cur' or dtgopt == 'ops'):
#    dtgoptinv='2009080100.cur'
#else:

dtgoptinv=dtgopt


# original dependence on switches:  if((dorsync and w2.W2doW3RapbRsync) and not(doretro) ):
if(dorsync and not(doretro) or override or doKlean):
    
    if(len(dtgopt.split('.')) > 1 or ndayback == 0):
        tdtgopt=dtgopt
    elif(ndaybackopt != None):
        nd=ndayback+2
        tdtgopt="cur-d%d.cur"%(nd)
    else:
        tdtgopt='cur-d5.cur'

    tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    # 20100319 -- turn off since we cp from /data/amb/project/hfip/tceps directly and
    # i svn co from to wxmap.sf.net
    #
    # rsync plots from local web -> ruc web by dtgs
    #for tdtg in tdtgs:
    #    year=tdtg[0:4]
    #    cmd="rsync -alv /%s/tceps/%s/%s %s/tceps/%s"%(w2.HfipBaseDir,year,tdtg,w2.HfipProducts,year)
    #    mf.runcmd(cmd,ropt)

    #
    # rsync the basic web stuff from local web (svn co web/config; make.ln.sh)
    #
    #
    #cmd="rsync --exclude \"*/20??/*\" --exclude \"inv.*\" --exclude-from=/w21/etc/ex-w21.txt -alv %s/ %s/"%(w2.HfipBaseDir,w2.HfipProducts)
    #mf.runcmd(cmd,ropt)

if(doKlean):
    
    keepdtg=tdtgs[0]
    curdtgs=glob.glob("%s/????/*"%(webdir))
    for curdtg in curdtgs:
        cc=curdtg.split('/')
        year=cc[len(cc)-2]
        cdtg=cc[len(cc)-1]
        dtime=mf.dtgdiff(keepdtg,cdtg)
        if(dtime < 0.0):
            cmd="rm -r %s/%s/%s"%(webdir,year,cdtg)
            mf.runcmd(cmd,ropt)
    sys.exit()

if(ndayback != 0):
    invcards=getTcEpsInventory(webdir,dtgopt=dtgoptinv,ndayback=ndayback)
    invpath="%s/inv.tceps.txt"%(webdir)
    rc=mf.WriteList(invcards,invpath,1)
    
MF.dTimer()

sys.exit()
