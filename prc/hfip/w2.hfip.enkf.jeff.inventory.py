#!/usr/bin/env python

"""
%s

purpose:

  generate hfip enkf jeff web

usages:

  %s dtgopt (bdtg.edtg[.ddtg])

  -I :: doinventory=1 or user geturl go get inventory from nrl
  -R :: dorsync=1

examples:

  %s cur -I

(c) 2008 by Michael Fiorino, NHC
"""


import w2
import TCw2 as TC

import cPickle as pickle

import BeautifulSoup
import urllib2

from M import *

MF=MFutils()


#
#  defaults
#
ropt=''
verb=0
update=0
areaopt='all'
doinventory=0
dorsync=0


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
        (opts, args) = getopt.getopt(sys.argv[2:], "NVIR")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-I",""): doinventory=1
        if o in ("-R",""): dorsync=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local routines

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



def getHfipEnkfWW3Inventory(baseurl,PW,dtgopt,verb=0):


    b2stmids=[]
    
    if(dtgopt == 'cur' or dtgopt == 'ops'):
        tstmids=[]
        dtgs=mf.dtg_dtgopt_prc('cur-36.cur')
        for dtg in dtgs:
            (stmids,stmopt)=TC.GetStmidsByDtg(dtg)
            tstmids=tstmids+stmids


        tstmids=mf.uniq(tstmids)

        for tstmid in tstmids:
            b2stmid=TC.ConvertB1Stmid2B2Stmid(tstmid).lower()
            b2stmids.append(b2stmid)

        
    dtgs=[]
    stms=[]
    models=[]
    areas=[]
    
    Dtgstms={}
    Dtgmodels={}
    Prdmodelstms={}
    Taumodelstms={}

    Verivars={}
    Veritaus={}

    #
    # get dtgs
    #
    html=urllib2.urlopen(baseurl)
    soup=BeautifulSoup.BeautifulSoup(html)
    aas=soup.findAll('a')
    for aa in aas:
        cc=str(aa.contents[0])
        dtg=cc.strip()
        if(len(dtg) != 10):
            continue
        dtgs.append(dtg)

    #
    # get veri plots
    #
    veriurl="%s/verif"%(baseurl)
    html=urllib2.urlopen(veriurl)
    stmsoup=BeautifulSoup.BeautifulSoup(html)
    aas=stmsoup.findAll('a')
    for aa in aas:
        plt=str(aa.contents[0]).strip()
        (dir,file)=os.path.split(plt)
        (file,ext)=os.path.splitext(file)
        tt=file.split('_')
        area=tt[0][0:2]
        var=tt[0][2:]
        tau=tt[1][0:-2]

        try:
            Verivars[area].append(var)
        except:
            Verivars[area]=[]
            Verivars[area].append(var)
            

        try:
            Veritaus[area,var].append(tau)
        except:
            Veritaus[area,var]=[]
            Veritaus[area,var].append(tau)

    kks=Verivars.keys()
    kks=mf.uniq(kks)

    for kk in kks:
        vars=mf.uniq(Verivars[kk])
        Verivars[kk]=vars


    for dtg in dtgs:
        dtgurl="%s/%s"%(baseurl,dtg)
        if(verb): print 'DDDDDD ',dtg,dtgurl,len(dtg)
        html=urllib2.urlopen(dtgurl)
        stmsoup=BeautifulSoup.BeautifulSoup(html)
        aas=stmsoup.findAll('a')
        for aa in aas:
            plt=str(aa.contents[0]).strip()
            if(mf.find(plt,'test')): continue
            (dir,file)=os.path.split(plt)
            (file,ext)=os.path.splitext(file)
            tt=file.split('_')
            prd=tt[0]
            stm=tt[1]
            model=tt[2]
            tau=tt[3][1:]
            
            stms.append(stm)
            models.append(model)
            
            try:
                Dtgstms[dtg].append(stm)
            except:
                Dtgstms[dtg]=[]
                Dtgstms[dtg].append(stm)

            try:
                Dtgmodels[dtg].append(model)
            except:
                Dtgmodels[dtg]=[]
                Dtgmodels[dtg].append(model)

            try:
                Prdmodelstms[dtg,stm,model].append(prd)
            except:
                Prdmodelstms[dtg,stm,model]=[]
                Prdmodelstms[dtg,stm,model].append(prd)

            try:
                Taumodelstms[dtg,stm,model].append(tau)
            except:
                Taumodelstms[dtg,stm,model]=[]
                Taumodelstms[dtg,stm,model].append(tau)

            if(verb): print 'ccccc ',dtg,plt,prd,len(prd),stm,model,tau


    stms=mf.uniq(stms)
    models=mf.uniq(models)

    for dtg in dtgs:
        stms=mf.uniq(Dtgstms[dtg])
        Dtgstms[dtg]=stms

    for dtg in dtgs:
        models=mf.uniq(Dtgmodels[dtg])
        Dtgmodels[dtg]=models

    for dtg in dtgs:
        stms=Dtgstms[dtg]
        models=Dtgmodels[dtg]
        for stm in stms:
            for model in models:
                try:
                    prds=mf.uniq(Prdmodelstms[dtg,stm,model])
                except:
                    prds=[]
                Prdmodelstms[dtg,stm,model]=prds
                
                try:
                    taus=mf.uniq(Taumodelstms[dtg,stm,model])
                except:
                    taus=[]
                Taumodelstms[dtg,stm,model]=taus
                    

    if(verb):
        
        print stms
        print models

        for dtg in dtgs:
            stms=Dtgstms[dtg]
            models=Dtgmodels[dtg]
            print 'Stmdtgs ',dtg,stms,models
            for stm in stms:
                for model in models:
                    print 'ssss ',stm,model,Taumodelstms[dtg,stm,model]

                    
    pickle.dump(stms,PW)
    pickle.dump(dtgs,PW)
    pickle.dump(Dtgstms,PW)
    pickle.dump(Dtgmodels,PW)
    pickle.dump(Taumodelstms,PW)
    pickle.dump(Prdmodelstms,PW)
    pickle.dump(Verivars,PW)
    pickle.dump(Veritaus,PW)
    PW.close()



def getHfipGfsEnkfWW3Inventory(w3dir,invpath,PW,dtgopt,verb=0):


    b2stmids=[]
    
    if(dtgopt == 'cur' or dtgopt == 'ops'):
        tstmids=[]
        dtgs=mf.dtg_dtgopt_prc('cur-36.cur')
        for dtg in dtgs:
            (stmids,stmopt)=TC.GetStmidsByDtg(dtg)
            tstmids=tstmids+stmids


        tstmids=mf.uniq(tstmids)

        for tstmid in tstmids:
            b2stmid=TC.ConvertB1Stmid2B2Stmid(tstmid).lower()
            b2stmids.append(b2stmid)


    print 'vvvvvvv ',tstmids,b2stmids
        
    dtgs=[]
    areaStms=[]
    
    DtgStms={}
    DtgStmPrds={}
    DtgStmPrdTaus={}

    ppaths=glob.glob("%s/*.png"%(w3dir))
    for ppath in ppaths:
        (dir,file)=os.path.split(ppath)
        (base,ext)=os.path.splitext(file)
        tt=base.split('_')
        if(tt[0] == 'ellipses'):
            prod=tt[0]
            dtg=tt[1]
            b2id=tt[2]
            stm2id=tt[3]
            b1id=TC.Basin2toBasin1[b2id]
            stm=stm2id+b1id
            tau='00'
            itau=int(tau)
            print 'pppp ',file,dtg,prod,stm,eps,tau

        else:
            prod=tt[0][0:len(tt[0])-10]
            dtg=tt[0][len(tt[0])-10:]
            stm=tt[1]
            eps=tt[2]
            tau=tt[3].split('.')[0][1:]
            itau=int(tau)
            

        MF.appendDictList(DtgStms,stm,dtg)
        MF.append2TupleKeyDictList(DtgStmPrds,dtg,stm,prod)
        MF.append3TupleKeyDictList(DtgStmPrdTaus,dtg,stm,prod,itau)


    DtgStms=MF.uniqDict(DtgStms)
    DtgStmPrds=MF.uniqDict(DtgStmPrds)
    DtgStmPrdTaus=MF.uniqDict(DtgStmPrdTaus)
    cards=[]
    cards=cards+MF.PrintDict(DtgStms)
    cards=cards+MF.PrintDict(DtgStmPrds)
    cards=cards+MF.PrintDict(DtgStmPrdTaus)

    MF.WriteList2File(cards,invpath,verb=1)
    
    sys.exit()


                    
    pickle.dump(stms,PW)
    pickle.dump(dtgs,PW)
    pickle.dump(Dtgstms,PW)
    pickle.dump(Dtgmodels,PW)
    pickle.dump(Taumodelstms,PW)
    pickle.dump(Prdmodelstms,PW)
    pickle.dump(Verivars,PW)
    pickle.dump(Veritaus,PW)
    PW.close()





def getInventoryFromPickle(pyppath):
    
    try:

        PW=open(pyppath)
        dtgs=pickle.load(PW)
        stms=pickle.load(PW)
        Dtgstms=pickle.load(PW)
        Dtgmodels=pickle.load(PW)
        Taumodelstms=pickle.load(PW)
        Prdmodelstms=pickle.load(PW)
        Verivars=pickle.load(PW)
        Veritaus=pickle.load(PW)
        
    except:
        
        dtgs=[]
        stms=[]
        Dtgstms={}
        Dtgmodels={}
        Taumodelstms={}
        Prdmodelstms={}
        Verivars={}
        Veritaus={}


    rc=(dtgs,stms,Dtgstms,Dtgmodels,Taumodelstms,Prdmodelstms,Verivars,Veritaus)
    
    return(rc)

def putHfipEnkfWW3Inventory(hashes,dtgopt=None,ndayback=15):

    if(dtgopt != None):
        if(not(mf.find(dtgopt,'cur'))):
            edtg=mf.dtg_command_prc(dtgopt)
            bdtg=mf.dtginc(edtg,-24*ndayback)
            tdtgopt="%s.%s"%(bdtg,edtg)
        else:
            bdtg="cur-d%d"%(ndayback)
            tdtgopt="%s.cur"%(bdtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    cards=[]
    for hash in hashes:
        cards=cards+PrintHash(hash)

    return(cards)

def makeIndexHtml(w3dir):

    #
    # main page
    #
    dtgs=[]

    index="""<html>
<title>HFIP Global Ensemble Forecast Plots</title>
<body>
<h1>HFIP Global Ensemble Forecast Plots</h1>"""

    paths=glob.glob("%s/veri*"%(w3dir)) + glob.glob("%s/2009??????"%(w3dir))
    paths.sort()
    for path in paths:
        (dir,file)=os.path.split(path)
        if(len(file) == 10): dtgs.append(file)
        index=index+"<a href=%s> %s</a><br>\n"%(file,file)

    index=index+"""</body></html>
"""

    indexpath="%s/index.html"%(w3dir)
    rc=mf.WriteCtl(index,indexpath)

    #
    # dtgs
    #

    dtgs.sort()
    for dtg in dtgs:
        indexdtg="""
<html>
<title>HFIP Global Ensemble Forecast Plots from %s</title>
<body>
<h1>HFIP Global Ensemble Forecast Plots %s</h1>"""%(dtg,dtg)

        wdir="%s/%s"%(w3dir,dtg)
        plts=glob.glob("%s/*.png"%(wdir))
        for plt in plts:
            (path,file)=os.path.split(plt)
            indexdtg=indexdtg+"<a href=%s> %s</a><br>\n"%(file,file)

        indexdtg=indexdtg+"""</body></html>
"""
        indexdtgpath="%s/index.html"%(wdir)
        print 'making indexdtg: ',indexdtgpath
        rc=mf.WriteCtl(indexdtg,indexdtgpath)
                       
        

    #
    # veri
    #

    indexverif="""
<html>
<title>HFIP Global Forecast Verification Statistics</title>
<body>
<h1>HFIP Global Forecast Verification Statistics</h1>"""

    wdir="%s/verif"%(w3dir)
    plts=glob.glob("%s/*.png"%(wdir))
    for plt in plts:
        (path,file)=os.path.split(plt)
        indexverif=indexverif+"<a href=%s> %s</a><br>\n"%(file,file)


    indexverif=indexverif+"""</body></html>
"""
    indexverifpath="%s/index.html"%(wdir)
    print 'making indexverif: ',indexverifpath
    rc=mf.WriteCtl(indexverif,indexverifpath)
                       
    
    return(1)
    


def rsyncTaccEnkf2Rapb(tdir):

    sdir="/work/01217/whitaker/ensplots/"
    sdir="/lfs1/projects/fim/whitaker/gfsenkf/hurrplots/"
    mf.ChangeDir(tdir)
    server='mfiorino@ranger.tacc.utexas.edu'
    server=w2.WjetScpServer
    cmd="rsync -avz %s:%s %s"%(server,sdir,tdir)
    mf.runcmd(cmd,ropt)

    


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

dowebupdate=w2.W2doW3Rapb

webdirext=w2.EsrlHttpInternetHfipEnkfDocRoot
webdir="%s/hfip/enkf"%(w2.W2BaseDirWeb)

pypfile="hfip.enkf.pyp"
pyppath="%s/%s"%(webdirext,pypfile)
invpath="%s/inv.hfip.enkf.txt"%(webdirext)
invpath="%s/inv.hfip.gfsenkf.txt"%(webdirext)

baseurl='http://www.cdc.noaa.gov/people/jeffrey.s.whitaker/hfip/'
baseurl='http://ruc.noaa.gov/hfip/enkf/ensplots/'
w3dir="%s/ensplots"%(webdirext)
w3dir="%s/../gfsenkfDAT"%(webdirext)

#
# first rsync over the plots...
#
if(dorsync):
    rc=rsyncTaccEnkf2Rapb(w3dir)

#
# make the index.html
#
#rc=makeIndexHtml(w3dir)

#
# make the inventory
#
if(doinventory):
    PW=open(pyppath,'w')
    #getHfipEnkfWW3Inventory(baseurl,PW,dtgopt,verb=verb)
    getHfipGfsEnkfWW3Inventory(w3dir,invpath,PW,dtgopt,verb=verb)


#
# and/or get from pickle
#
rc=getInventoryFromPickle(pyppath)
(dtgs,stms,Dtgstms,Dtgmodels,Taumodelstms,Prdmodelstms,Verivars,Veritaus)=rc

hashes=[Dtgstms,Dtgmodels,Taumodelstms,Prdmodelstms,Verivars,Veritaus]

invcards=putHfipEnkfWW3Inventory(hashes)
rc=mf.WriteList(invcards,invpath,1)

if(dowebupdate and dorsync):
    cmd="rsync -alvn --exclude \"*~\"  --exclude \"ensplots*\" --exclude \"*.pyp\" %s/ %s/"%(webdirext,webdir)
    mf.runcmd(cmd,ropt)



sys.exit()
