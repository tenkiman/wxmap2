#!/usr/bin/env python

"""%s

purpose:

  convert ukmo tigge xml to wxmap adeck

-O override find list
-G dogepsanal=0 -- don't do graphics
-C  :: incrontab=0 -- tell it to avoid crontab processing

usages:


examples:

%s cur all
"""

from tcbase import *

from xml.dom import minidom


#
#  defaults
#

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]
narg=len(sys.argv)-1

ropt=''
verb=0
override=0
dogepsanal=w2.W2doTcepsAnl
incrontab=1
useAdeck=0


#
# options using getopt
#

if(narg >= 2):

    dtgopt=sys.argv[1]
    model=sys.argv[2]
    
    if(model == 'all'):
        nb=3
    else:
        nb=4
        taid=sys.argv[3]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[nb:], "VNOGCA")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-V",""): verb=1
        if o in ("-N",""): ropt='norun'
        if o in ("-O",""): override=1
        if o in ("-G",""): dogepsanal=0
        if o in ("-C",""): incrontab=0
        if o in ("-A",""): useAdeck=1
        
else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


def openXML(xmlpath,gzip=0):

    # -- first check if there's data...
    #
    xsiz=MF.getPathSiz(xmlpath)
    if(xsiz <= 0):
        print 'EEE-openXML xmlpath: ',xmlpath,' is 0 sized or None...sayounara...'
        return(None)
    
    if(gzip):

        import gzip as GZ

        try:
            XML=GZ.open(xmlpath)
            return(XML)
        except:
            print 'EEE unable to open ',xmlpath,' sayoonara'
            return(None)
    else:
        
        try:
            XML=open(xmlpath)
            return(XML)
        except:
            print 'EEE unable to open ',xmlpath,' sayoonara'
            return(None)
        
    

import tigge as TG
import gzip as GZ


if(model == 'all'):

    models=['ecmwf','ukmo','ncep','cmc']
    
    modeltaids={
        'ecmwf':['ecmt','all'],
        'ukmo':['det','all'],
        'ncep':['gfst','all'],
        'cmc':['cmct','all'],
        }
                
    for model in models:
        for taid in modeltaids[model]:
            cmd="%s %s %s %s"%(pyfile,dtgopt,model,taid)
            for o,a in opts:
                cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)

    sys.exit()



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer('all')
prcdir=w2.PrcDirTcdatW2
mf.ChangeDir(prcdir)

sbdir=w2.TcDatDir


dtgs=mf.dtg_dtgopt_prc(dtgopt)

# -- how many times to try before giving up...
#
ntries=10

tcD=TcData(dtgopt=dtgopt)

for dtg in dtgs:

    yyyy=dtg[0:4]

    (bstmids,btcs)=tcD.getDtg(dtg,renameSubbasin=1)    

    if(verb):
        for bstmid in bstmids:
            print 'TC: %s %5.1f %6.1f %3.0f'%(bstmid,btcs[bstmid][0],btcs[bstmid][1],btcs[bstmid][2])

    if(model == 'ncep'):
        tbdir=w2.TcAdecksNcepDir
        mf.ChkDir(tbdir,'mk')
        if(w2.W2doW3RapbXmlAdecks):
            w3dir=w2.TcAdecksNcepDirW3
            mf.ChkDir(w3dir,'mk')
        
        xmldir="%s/ncep/tigge/%s"%(sbdir,yyyy)
        dogzip=1
        xmlfile="kwbc_%s0000_GEFS_glob_prod_esttr_glo.xml.gz"%(dtg)
        dogzip=0
        xmlfile="kwbc_%s0000_GEFS_glob_prod_esttr_glo.xml"%(dtg)
        if(not(os.path.exists("%s/%s"%(xmldir,xmlfile)))): xmlfile="kwbc_%s0000_GEFS_glob_prod_esttr_glo.xml.gz"%(dtg)

        
        if(taid == 'gfst'):
            #xmlfile="kwbc_%s0000_GFS_glob_prod_tctr_glo.xml.gz"%(dtg)
            dogzip=1
            xmlfile="kwbc_%s0000_GFS_glob_prod_sttr_glo.xml.gz"%(dtg)
            dogzip=0
            xmlfile="kwbc_%s0000_GFS_glob_prod_sttr_glo.xml"%(dtg)

        xmlpath="%s/%s"%(xmldir,xmlfile)
        XML=openXML(xmlpath,gzip=dogzip)

    elif(model == 'jma'):
        tbdir=w2.TcAdecksJmaDir
        mf.ChkDir(tbdir,'mk')
        if(w2.W2doW3RapbXmlAdecks):
            w3dir=w2.TcAdecksNcepDirW3
            mf.ChkDir(w3dir,'mk')
#-rw-r--r--  1 fiorino  frdrapb    1605 Oct 18  2009 z_tigge_c_RJTD_20091016120000_GSM_glob_prod_tctr_nwp.xml.gz
#-rw-r--r--  1 fiorino  frdrapb    4834 Oct 18  2009 z_tigge_c_RJTD_20091016120000_TEM_glob_prod_etctr_nwp.xml.gz
#-rw-r--r--  1 fiorino  frdrapb   28581 Oct 18  2009 z_tigge_c_RJTD_20091016120000_WFM_glob_prod_etctr_nwp.xml.gz
        
        xmldir="%s/jma/tigge/%s"%(sbdir,yyyy)
        xmlfile="z_tigge_c_RJTD_%s0000_WFM_glob_prod_etctr_nwp.xml.gz"%(dtg)
        if(taid == 'gsm'):
            xmlfile="z_tigge_c_RJTD_%s0000_GSM_glob_prod_tctr_nwp.xml.gz"%(dtg)
        if(taid == 'tem'):
            xmlfile="z_tigge_c_RJTD_%s0000_TEM_glob_prod_etctr_nwp.xml.gz"%(dtg)
        xmlpath="%s/%s"%(xmldir,xmlfile)
        XML=openXML(xmlpath,gzip=1)

    elif(model == 'cmc'):
        tbdir=w2.TcAdecksCmcDir
        mf.ChkDir(tbdir,'mk')
        if(w2.W2doW3RapbXmlAdecks):
            w3dir=w2.TcAdecksCmcDirW3
            mf.ChkDir(w3dir,'mk')

        dogzip=1
        xmldir="%s/cmc/tigge/%s"%(sbdir,yyyy)
        xmlfile="kwbc_%s0000_CENS_glob_prod_etctr_glo.xml.gz"%(dtg)
        dogzip=0
        xmlfile="kwbc_%s0000_CENS_glob_prod_esttr_glo.xml"%(dtg)
        if(taid == 'cmct'):
            xmlfile="kwbc_%s0000_CMC_glob_prod_tctr_glo.xml.gz"%(dtg)
            xmlfile="kwbc_%s0000_CMC_glob_prod_sttr_glo.xml"%(dtg)
        xmlpath="%s/%s"%(xmldir,xmlfile)
        XML=openXML(xmlpath,gzip=dogzip)

    elif(model == 'ecmwf'):
        tbdir=w2.TcAdecksEcmwfDir
        mf.ChkDir(tbdir,'mk')
        if(w2.W2doW3RapbXmlAdecks):
            w3dir=w2.TcAdecksEcmwfDirW3
            mf.ChkDir(w3dir,'mk')

        xmldir="%s/ecmwf/tigge/%s"%(sbdir,yyyy)
        xmlfile="z_tigge_c_ecmf_%s0000_ifs_glob_prod_all_glo.xml"%(dtg)
        xmlpath="%s/%s"%(xmldir,xmlfile)
        XML=openXML(xmlpath)

    elif(model == 'ukmo'):

        tbdir=w2.TcAdecksuKmoDir
        mf.ChkDir(tbdir,'mk')
        if(w2.W2doW3RapbXmlAdecks):
            w3dir=w2.TcAdecksuKmoDirW3
            mf.ChkDir(w3dir,'mk')
            
        xmldir="%s/ukmo/tigge/%s"%(sbdir,yyyy)
        if(taid == 'det'):
            xmlfile="z_tigge_c_egrr_%s0000_mogm_glob_prod_tctr_glo.xml"%(dtg)
            xmlpath="%s/%s"%(xmldir,xmlfile)
            XML=openXML(xmlpath,gzip=0)
            
        else:
            xmlfile="z_tigge_c_egrr_%s0000_mogreps_glob_prod_etctr_glo.xml.gz"%(dtg)
            xmlpath="%s/%s"%(xmldir,xmlfile)
            XML=openXML(xmlpath,gzip=1)
        
        
    else:
        print 'EEE invalid model: ',model
        sys.exit()

    useXML=1
    if(XML == None):
        print 'WWW no XML press..'
        if(useAdeck):
            useXML=0
        else:
            continue

    if(useXML):
    
        logdir="%s/%s/tigge/%s/%s"%(w2.TcDatDir,model,yyyy,dtg)
        mf.ChkDir(logdir,diropt='mk')
        logmask="%s/db.xml2adeck.%s.%s.%s.*.txt"%(logdir,model,taid,dtg)
        nlog=len(glob.glob(logmask))

        # -- 20120525 keep try until we've done it ntries times...
        #
        if(nlog > ntries and not(override)):
            print 'WWW already processed... sayoonara because override=0...nlog: ',nlog
            if(len(dtgs) == 1):
                sys.exit()
            else:
                continue


        print "XXXXX-%s-tigge: %s %s"%(model,dtg,xmlpath)
        print

        try:
            xmldoc=minidom.parse(XML)
        except:
            'EEE---BBBAAADD XML xmlpath: ',xmlpath
            continue
        h=xmldoc.getElementsByTagName('header')
        d=xmldoc.getElementsByTagName('data')

        try:
            (bdtg,cdtg,pcenter,product,genapp)=TG.ParseHeader(h)
        except:
            print 'EEE in ParseHeader for dtg: ',dtg
            continue

        adecks={}
        adtaus={}
        adstmids={}
        adaids=[]

        trkdataAnl={}
        for i in range(0,d.length):
            TG.ParseData(d[i],trkdataAnl,bdtg,btcs,adecks,adtaus,adstmids,adaids,verb=verb)

        adaids=mf.uniq(adaids)
        
        MF.uniqDictList(adtaus)

        #
        #  put out individual wxmap adecks based on taid
        #

        if(taid == 'all' or taid == 'tem'):

            adeckall={}
            allstmids=[]
            allb2s={}
            for adaid in adaids:
                stmids=adstmids[adaid]
                stmids=mf.uniq(stmids)
                for stmid in stmids:
                    allstmids.append(stmid)
                    
                    for itau in adtaus[stmid,adaid]:
                        card=adecks[stmid,adaid,itau]
                        MF.appendDictList(adeckall,stmid,card)
                        
                        #adeckall[stmid]=[]
                        #print 'EEE(%s): bad adeck for: %s aid: %s -- setting adeckall to []'%(pyfile,stmid,adaid)

            allstmids=mf.uniq(allstmids)
            for stmid in allstmids:

                gotrealstorm=0
                if(stmid == '99X.9999'):
                    print 'WWWW----WWWW(%s): got 99X.9999 in all...press...'%(pyfile)
                    continue


                if(mf.find(stmid,'.')):
                    stmyear=stmid.split('.')[1]
                    b2stmid=ConvertB1Stmid2B2Stmid(stmid).lower()
                    if(taid == 'tem'):
                        oadeck="a%s.%s.%s.%s_tem_eps_tigge.txt"%(b2stmid,dtg,stmid,model)
                    else:
                        if(model == 'jma'):  oadeck="a%s.%s.%s.%s_eps_tigge.txt"%(b2stmid,dtg,stmid,model)
                        else:                oadeck="a%s.%s.%s.%s_tigge.txt"%(b2stmid,dtg,stmid,model)

                    gotrealstorm=1

                else:
                    stmyear=dtg[0:4]
                    clat=stmid.split('_')[0]
                    clon=stmid.split('_')[1]
                    (rlat,rlon)=Clatlon2Rlatlon(clat,clon)
                    b1id=tcbasinb1id(rlat,rlon,b3id='')
                    b2id=Basin1toBasin2[b1id]

                    for card in adeckall[stmid]:
                        try:
                            allb2s[b2id].append(card)
                        except:
                            allb2s[b2id]=[]
                            allb2s[b2id].append(card)


                tdir="%s/%s"%(tbdir,stmyear)
                if(mf.ChkDir(tdir,'mk') == 0):
                    print 'tdir error',tdir
                    sys.exit()

                if(gotrealstorm):
                    oadeckpath="%s/%s"%(tdir,oadeck)
                    print 'ooooooooooooooooo(all): ',oadeckpath
                    mf.WriteList(adeckall[stmid],oadeckpath)
                    if(w2.W2doW3RapbXmlAdecks):
                        oadeckpathw3="%s/%s"%(w3dir,oadeck)
                        print 'wwwwwwwwwwwwwwwww(all): ',oadeckpathw3
                        cmd="cp %s %s"%(oadeckpath,oadeckpathw3)
                        mf.runcmd(cmd,ropt)


            if(len(allb2s) > 0):
                b2s=allb2s.keys()
                b2s.sort()
                for b2 in b2s:
                    oadeck="ae_%s_%s.%s_tigge.txt"%(b2,dtg,model)
                    oadeckpath="%s/%s"%(tdir,oadeck)
                    print 'ooooooooooooooooo(gen): ',oadeckpath
                    mf.WriteList(allb2s[b2],oadeckpath)
                    if(w2.W2doW3RapbXmlAdecks):
                        oadeckpathw3="%s/%s"%(w3dir,oadeck)
                        print 'wwwwwwwwwwwwwwwww(gen): ',oadeckpathw3
                        cmd="cp %s %s"%(oadeckpath,oadeckpathw3)
                        mf.runcmd(cmd,ropt)



        else:

            # -- xml parser always puts 'forecast' to 'EDET' and ensembles to 'EP00 -- EPNN'
            #
            itaid=taid
            if(taid.lower() == 'ecmt' or 
               taid.lower() == 'det' or 
               taid.lower() == 'gfst' or 
               taid.lower() == 'cmct' or 
               taid.lower() == 'gsm'):
                itaid='EDET'
            

            for adaid in adaids:

                if(adaid == itaid):
                    stmids=adstmids[itaid]
                    stmids=mf.uniq(stmids)

                    got99x=0
                    for stmid in stmids:
                        if(len(stmid.split('_')) == 2):
                            stm3id='99X'
                        else:
                            stm3id=stmid.split('.')[0]
                            stmyear=stmid.split('.')[1]

                        if(stm3id == '99X'):
                            stmyear=dtg[0:4]

                        tdira="%s/%s"%(tbdir,stmyear)
                        tdir="%s/wxmap"%(tdira)

                        mf.ChkDir(tdir,'mk')
                        otaid=taid.lower()
                        # -- old wxfile
                        #wxfile="wxmap.%s.%s.%s"%(otaid,dtg,stm3id)
                        #wxpath="%s/%s"%(tdir,wxfile)

                        if(not(mf.find(stmid,'.'))): continue
                        stmyear=stmid.split('.')[1]
                        b2stmid=ConvertB1Stmid2B2Stmid(stmid).lower()
                        oadeck="a%s.%s.%s.%s_%s_tigge.txt"%(b2stmid,dtg,stmid,model,taid)
                        oadeckpath="%s/%s"%(tdira,oadeck)

                        if(verb):
                            print 'sssssssssss ',stm3id,stmyear,' for itaid: ',itaid,tdir
                            for itau in adtaus[stmid,itaid]:
                                card=adecks[stmid,itaid,itau]
                                print 'AAA final ',card 


                        #wmode='w'
                        #if(stm3id == '99X'):
                            #if(os.path.exists(wxpath)):
                                #if(override and got99x == 0):
                                    #os.unlink(wxpath)
                                    #got99x=1
                                    #wmode='w'
                                    #if(verb): print "W2 99X.9999 adeck override: %s"%(wxpath)
                                #else:
                                    #wmode='a'
                            #else:
                                #if(got99x == 0): print "W2 99X.9999 adeck         : %s"%(wxpath)
                                #wmode='a'
                                #got99x=1
                        #else:
                            #if(verb): print "W2 %s RRRReal adeck : %s"%(stmid,wxpath)

                        adlist=[]
                        for itau in adtaus[stmid,itaid]:
                            card=adecks[stmid,itaid,itau]
                            adlist.append(card)
                            
                        mf.WriteList(adlist,oadeckpath)
                        print 'oooooooooooooooooo(det): ',oadeckpath
                        if(w2.W2doW3RapbXmlAdecks):
                            oadeckpathw3="%s/%s"%(w3dir,oadeck)
                            print 'wwwwwwwwwwwwwwwwww(det): ',oadeckpathw3
                            cmd="cp %s %s"%(oadeckpath,oadeckpathw3)

                        #mf.WriteList(adlist,wxpath,wmode=wmode)


        curdtgms=mf.dtg('dtg_ms')
        logpath="%s/db.xml2adeck.%s.%s.%s.%s.txt"%(logdir,model,taid,dtg,curdtgms)
        print
        print 'llll ',logpath
        cmd="touch %s"%(logpath)
        mf.runcmd(cmd,ropt)

    #gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
    # 
    # graphics...

    if(dogepsanal and taid == 'all' and incrontab):

        # -- if useAdeck then opt is properly set for w2-tc-g-epsanal.py
        #
        cmd="w2-tc-g-epsanal.py %s %s %s"%(dtg,model,taid)
        for o,a in opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
        
##         # -- put in crontab
##         cmd="w2-tc-g-epsanal.py %s %s -A"%(dtg,model)
##         for o,a in opts:
##             cmd="%s %s %s"%(cmd,o,a)
##         mf.runcmd(cmd,ropt)

        #
        # always inventory from current dtg
        #
        cmd="w2-tc-inventory-epsanal.py %s"%(curdtg)
        mf.runcmd(cmd,ropt)

        
        
    
MF.dTimer('all')

sys.exit()

