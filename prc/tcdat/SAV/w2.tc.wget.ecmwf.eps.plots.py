#!/usr/bin/env python

"""%s

purpose:

  wget ecmwf eps tc graphics

examples:

%s cur

  -O override and force reprocess
  -J do NOT do ftp for jtwc
  -p dopngonly -- make pngs for web
  -D dolp=0
  
"""

from tcbase import *

from BeautifulSoup import BeautifulSoup as BS

import ATCF


lsopt='dat'
model='ngp'

ropt=''

curdtg=mf.dtg()
(tttdtg,curphr)=mf.dtg_phr_command_prc(curdtg) 
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

# -- option to filter out exper storms -- lat/lon must be close to existing storms
#
filtexpStorms=1
convertexe="convert.ksh" # don't need because we'er running grads using opengrads .pl
convertexe="convert"

doftp4jtwc=0

dtgopt='cur'
override=0
verb=0
#
# send pngs to hur_pr
#
dolp=0
dopngonly=1

drmin=2.0

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "ONVJpD")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-O",""): override=1
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-J",""): doftp4jtwc=0
        if o in ("-p",""): dopngonly=1
        if o in ("-D",""): dolp=0

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)



xsiz=1024
ysiz=768

xsizfl=xsiz
ysizfl=ysiz+100

httpbase='http://www.ecmwf.int'
#httpbase='http://old.ecmwf.int'


cookies="%s/cookies.txt"%(w2.W2Dir)

dtgs=mf.dtg_dtgopt_prc(dtgopt)

wgetcookies="--load-cookies=%s"%(cookies)

wgetopts=''
wgetopts='-q'
if(verb): wgetopt='-v'

maxOldAge=240

def GetEcTcIds(dtg,ropt='',verb=0):
    
    year=dtg[0:4]
    yyyymmdd=dtg[0:8]
    ecstms=[]
    htmlpath='/ptmp/ttt.html'
    
    ecurl="%s/products/forecasts/d/tcsearch/?region=00&Year=%s&search=%s&submit=Search"%(httpbase,year,yyyymmdd)
    cmd="wget %s %s  \"%s\" -O %s"%(wgetopts,wgetcookies,ecurl,htmlpath)
    mf.runcmd(cmd,ropt)

    html=open(htmlpath)
    soup=BS(html)

    print htmlpath

    ss=soup.findAll('a')
    
    for s in ss:
        s1=str(s)
        if(mf.find(s1,'dummy') and mf.find(s1,'strike')):
            t1=s.attrs
            for tt in t1:
                if(str(tt[0]) == 'href'):
                    url=str(tt[1])
                    tt=url.split('!')
                    ecstms.append(tt[2])
                    if(verb): print 'sssssssssssssss ',url,tt[1],tt[2]

    return(ecstms)


def GetEcTcIdsNew(dtg,ropt='',verb=0):
    
    year=dtg[0:4]
    yyyymmdd=dtg[0:8]
    ecstms=[]
    htmlpath='/ptmp/ttt.html'

    ecurl="%s/products/forecasts/d/tcsearch/?region=00&Year=%s&search=%s&submit=Search"%(httpbase,year,yyyymmdd)
    ecurl="%s/products/forecasts/d/charts/medium/tropcyclones/Forecast/strike_new!%s!%s!%s!dummy!/"%(httpbase,year,dtg,dtg)
    
    cmd="wget %s %s  \"%s\" -O %s"%(wgetopts,wgetcookies,ecurl,htmlpath)
    mf.runcmd(cmd,ropt)

    html=open(htmlpath)
    soup=BS(html)

    print htmlpath

    ss=soup.findAll('option')
    
    for s in ss:
        s1=str(s)
        if(mf.find(s1,'region')):
            t1=s.attrs
            for tt in t1:
                if(str(tt[0]) == 'value'):
                    url=str(tt[1])
                    tt=url.split('-')
                    nn=str(tt[0]).split()
                    if(len(nn) == 1): 
                        name=nn[0].strip().upper()
                        stmid=name
                    elif(len(nn) == 2):
                        name=nn[0].upper()
                        stmid=nn[1]
                        stmid=stmid.replace('(','')
                        stmid=stmid.replace(')','')
                        
                    rr=str(tt[-1]).split()
                    region=rr[-1].strip()
                    ecstm="%s_%s_%s"%(stmid,name,region)
                    ecstms.append(ecstm)
                    if(verb): print 'sssssssssssssss ',url,tt[1],tt[2]

    return(ecstms)

def GetEcStmDtgs(dtg,ecstms,ropt='',verb=0):

#http://www.ecmwf.int/products/forecasts/d/charts/medium/tropcyclones/Forecast/strike!2008!08S_08S_06!

    year=dtg[0:4]
    htmlpath='/ptmp/ttt.dtg.html'
    ecstmdtgs={}

    for ecstm in ecstms:

        ecstmdtgs[ecstm]=[]

        if(os.path.exists(htmlpath)):
            os.unlink(htmlpath)
        
        ecurl="%s/products/forecasts/d/charts/medium/tropcyclones/Forecast/strike!%s!%s!"%(httpbase,year,ecstm)
        cmd="wget %s %s  \"%s\" -O %s"%(wgetopts,wgetcookies,ecurl,htmlpath)
        mf.runcmd(cmd,ropt)

        html=open(htmlpath)
        soup=BS(html)

        #
        # only 7 dtgs are shown on the page at a time
        # look for utc in the options
        #

        oo=soup.findAll('option')
        for o in oo:
            o1=str(o)
            o2=o.contents[0]
            o2=str(o2)
            if(mf.find(o2,'UTC')):
                tt=o2.split()
                day=int(tt[1])
                dd="%02d"%(day)
                mon=tt[2].upper()
                mm=mf.cname3[mon]
                hh=tt[3][0:2]
                odtg=year+mm+dd+hh
                ecstmdtgs[ecstm].append(odtg)
                

        ss=soup.findAll('a')
        for s in ss:
            s1=str(s)
            
            if(
                (mf.find(s1,'dummy') and mf.find(s1,'charts')) and
                (not(mf.find(s1,'!!'))) or
                 (mf.find(s1,dtg[0:8]))
                ):
                
                t1=s.attrs

                #if(verb): print 'tttttttt ',len(t1),t1

                if(len(t1) == 2):
                    
                    t100=t1[0][0]
                    t101=t1[0][1]
                    
                    t110=t1[1][0]
                    t111=t1[1][1]

                    #if(verb):
                    #    print '00000000000 ',t100,t101
                    #    print '11111111111 ',t110,t111

                    if(t100 == 'class' and t101 == 'menuitem' and t110 == 'href'):
                        tt=t111.split('!')
                        ecdtg=str(tt[3])
                        ecstmdtgs[ecstm].append(ecdtg)

                        if(verb):
                            print 'sssssssssssssss ',ecstm,ecdtg


    
        ecstmdtgs[ecstm]=mf.uniq(ecstmdtgs[ecstm])

    return(ecstmdtgs)


def EcId2uSId(dtg,verb=0):

    etdir="%s/%s"%(TcAdecksEcmwfDir,dtg[0:4])
    etmask="%s/ectc*%s*.txt"%(etdir,dtg)
    etpaths=glob.glob(etmask)

    etcards=[]
    if(len(etpaths) > 0):
        for etpath in etpaths:
            etcards=etcards+open(etpath,'r').readlines()
    else:
        return(etcards)

    etcards=mf.uniq(etcards)
            

    et2us={}
    for etcard in etcards:
        tt=etcard.split()
        etid=tt[0]
        usid=tt[2]
        et2us[etid]=usid


    etids=et2us.keys()
    etids.sort()

    if(verb):
        for etid in etids:
            print 'asdfa ',etid,et2us[etid]

    return(et2us)

    
def GetName2Stmid(year):

    tcnames=GetTCnamesHash(year)

    name2id={}
    stmids=tcnames.keys()
    
    for stmid in stmids:
        name2id[tcnames[stmid]]=stmid[1]


    names=name2id.keys()
    names.sort()

    return(name2id)

def Conver2Png(pspath,usid,ropt='',nhconly=0):

    dopng=( (nhconly and (usid[2] == 'L' or usid[2] == 'E') ) or not(nhconly) )
    if(dopng):
        (base,ext)=os.path.splitext(pspath)
        pngpath="%s.png"%(base)
        tmppath="/ptmp/tt.png"
        cmd="%s -density 150 %s %s"%(convertexe,pspath,pngpath)
        mf.runcmd(cmd,ropt)
        cmd="%s -resize 800x1000 %s %s"%(convertexe,pngpath,pngpath)
        mf.runcmd(cmd,ropt)


def Conver2PngWeb(pspath,wdir,landscape=1,ropt=''):

    (dir,file)=os.path.split(pspath)
    (base,ext)=os.path.splitext(file)
    
    pngpath="%s/%s.png"%(wdir,base)
    tmppath="/ptmp/tt.png"
    cmd="%s -density 150 %s %s"%(convertexe,pspath,pngpath)
    mf.runcmd(cmd,ropt)
    if(landscape):
        cmd="%s -rotate 90 -resize %dx%d %s %s"%(convertexe,xsiz,ysiz,pngpath,pngpath)
    else:
        cmd="%s -resize %dx%d %s %s"%(convertexe,ysiz,xsiz,pngpath,pngpath)
    mf.runcmd(cmd,ropt)



def SendPng2HurPrn(pltdir,dtg,dolp):
    pngs=glob.glob("%s/ec.eps.*%s*.png"%(pltdir,dtg))
    for png in pngs:
        print 'FFFFFFFFFFFFFFF hhhhhhhhhhh 2 hur_prn ',png
        if(dolp):
            cmd="lp -d hur_prn %s"%(png)
            mf.runcmd(cmd,ropt)
    

def getDtgFromPs(pspath):
    cards=open(pspath).readlines()
    dtg=None
    for card in cards:
        if(mf.find(card, 'Date ') and mf.find(card,'@ECMWF')):
            tt=card.split()
            for t in tt:
                if(mf.find(t,'(Date')):
                    n=tt.index(t)
                    dtg="%s%s"%(tt[n+1],tt[n+2])
                    return(dtg)
            
    return(dtg)

# -- new routines for  pulling from new/old site
#

def getB1idFromWMORegion(region):
    b1id=None
    if(region == '01'): b1id='L'
    if(region == '02'): b1id='E'
    if(region == '03'): b1id='C'
    if(region == '04'): b1id='W'
    if(region == '05'): bi1d='I'
    if(region == '06' or region == '07' or region == '08'): b1id='S'
    if(region == '09' or region == '10' or region == '11'): b1id='P'
    return(b1id)


def getStmidFromECstm(ecstm,stmids,year,verb=0):
    
    tt=ecstm.split('_')
    ecnum=tt[0][0:2]
    ecstmid=tt[0]
    ecname=tt[1]
    ecregion=tt[2]
    
    ostmid=None
    for stmid in stmids:
        ostmid=stmid
        (stm3id,sname)=tD.getStmName3id(stmid)
        snum=stmid[0:2]
        sb1id=stmid[2]
        ecb1id=getB1idFromWMORegion(ecregion)
        
        if(snum == ecnum and ecb1id == sb1id):
            if(verb): print 'HHHHHHHHHHHHHHHHH:',ecstmid,stm3id
            return(ostmid)
        elif(mf.find(ecname,sname[0:4]) and ecb1id == sb1id):
            if(verb): print 'HHHHHHHHHHHHHHHHH2222222222222222222nnnnnnnnnnnnnnnnnnnnnn:',ecstmid,stm3id
            return(ostmid)
        elif(ecb1id == sb1id):
            return(ostmid)
        
    # -- no joy with obvious -- match with nearest basin b1id -- use ecstmid
    #

    for stmid in stmids:
        ostmid=stmid
        (stm3id,sname)=tD.getStmName3id(stmid)
        snum=stmid[0:2]
        sb1id=stmid[2]
        ecb1id=getB1idFromWMORegion(ecregion)
        print 'sss',stmid,snum,sb1id,sname[0:4]
        
        if(ecb1id == sb1id and abs((int(snum)-int(ecnum))) <= 3):
            print 'HHHHHHHHHHHHHHHHH3333333333333333333333333:',ecstmid,stm3id
            return(ostmid)
        
    # -- still no joy -- punt
    #
    if(ostmid == None):
        ostmid="%s.%s"%(ecstmid,year)
        print 'MMMMMMMMMMMMMMMMMMMM--punting ostmid:',ostmid
    
    return(ostmid)
    

if(dopngonly):
    dolp=0

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main loop
#
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm


server=Nhc2JtwcFtpServer

didPlots=0
for dtg in dtgs:

    tD=TcData(dtgopt=dtg)
    (stmids,btcs)=tD.getStmidBtcsDtg(dtg)
    year=dtg[0:4]

    if(len(stmids) == 0):
        print 'WWWWW no storms for dtg: ',dtg,'press...'
        continue
        
    print
    print 'SSSSSSSS storms for dtg: ',dtg,stmids
    print
    
    
    
    wdir=w2.TcTcepsWebDir
    wdir="%s/%s/%s"%(wdir,year,dtg)
    mf.ChkDir(wdir,'mk')

    pltdir="%s/%s"%(w2.TcPltEcmwfEpsDir,year)
    MF.ChkDir(pltdir,'mk')

    
    # -- blow away previous plots
    #
    if(override):
        cmd="rm  %s/*%s*"%(pltdir,dtg)
        mf.runcmd(cmd,ropt)

    # -- get ec storms
    #
    ecstms=[]
    ecstmsthere=[]
                  
    ecstms=GetEcTcIdsNew(dtg,ropt,verb=verb)
    #print 'ECstms: ',ecstms
    
    gotEcstms=[]
    
    for ecstm in ecstms:
        
        #http://old.ecmwf.int!2014!18W_FUNG45WONG_04!2014092200!dummy!chart.ps
        
        pspath="/ptmp/ttt.strike.ps"
        ecurlstrike='/products/forecasts/d/getchart/catalog/products/forecasts/medium/tropcyclones/Forecast/strike_new'
        ecurlstrike="%s!%s!%s!%s!dummy!chart.ps"%(ecurlstrike,year,ecstm,dtg)
        ecurlstrike=httpbase+ecurlstrike
        cmd="wget %s %s \"%s\" -O %s"%(wgetopts,wgetcookies,ecurlstrike,pspath)
        mf.runcmd(cmd,ropt)
        ecdtg=getDtgFromPs(pspath)
        ecdtgdiff=-999.
        
        ###print 'EEEEEEEEEEEEEEEEEEE',ecdtg,'target dtg: ',dtg
        
        if(ecdtg == dtg):
            bstmid=getStmidFromECstm(ecstm,stmids,year)
            gotEcstms.append(bstmid)
            
            finalpspath="%s/ec.eps.strike.%s.%s.ps"%(pltdir,bstmid,dtg)
            if(MF.ChkPath(finalpspath) and not(override)): 
                print 'III(finalpapath): ',finalpspath,' already exists...press...'
                continue
            
            didPlots=1
            
            cmd="mv %s %s"%(pspath,finalpspath)
            mf.runcmd(cmd,ropt)
            
            # -- now get plumes
            pspath="/ptmp/ttt.plumes.ps"
            ecurlplume='/products/forecasts/d/getchart/catalog/products/forecasts/medium/tropcyclones/Forecast/plumes_new'
            ecurlplume="%s!%s!%s!%s!dummy!chart.ps"%(ecurlplume,year,ecstm,dtg)
            ecurlplume=httpbase+ecurlplume
            cmd="wget %s %s \"%s\" -O %s"%(wgetopts,wgetcookies,ecurlplume,pspath)
            mf.runcmd(cmd,ropt)
            ecdtg=getDtgFromPs(pspath)
            finalpspath="%s/ec.eps.plumes.%s.%s.ps"%(pltdir,bstmid,dtg)
            cmd="mv %s %s"%(pspath,finalpspath)
            mf.runcmd(cmd,ropt)
            
        else:
            if(ecdtg != None):
                ecdtgdiff=mf.dtgdiff(ecdtg,dtg)
                
        if(ecdtgdiff > maxOldAge):
            print 'III(stop wget...dtg of ec storm: ',ecdtg,'too old compared to target dtg: ',dtg,'...press...'
            break   
        else:   
            continue

    
    pngs=glob.glob("%s/*strike*%s*.png"%(wdir,dtg))
    pss=glob.glob("%s/*strike*%s*.ps"%(pltdir,dtg))
    pps=glob.glob("%s/*plumes*%s*.ps"%(pltdir,dtg))
    
    Necstms=len(gotEcstms)
    Npss=len(pss)
    Npngs=len(pngs)

    # -- special processing of redoing png only
    #
    if( Npss > 0 and Npngs != Npss or override):
        print "PPPPPPPPPPP Nplots: %d  dtg: %s already in: %s"%(Npss,dtg,pltdir)
        for ps in pss:
            Conver2PngWeb(ps,wdir,landscape=1)
        for pp in pps:
            Conver2PngWeb(pp,wdir,landscape=1)

    # -- check if plots done
    #
    if(Npss >= Necstms and not(override) ):
        print
        print "III(ALLDONE) plots: %d  for Necstms: %d  dtg: %s already in: %s ... onward to next dtg ..."%(Npss,Necstms,dtg,pltdir)
        print

# -- do the inventory now
#
if(w2.W2doTcepsAnl and didPlots or override):
    print "III(INVENTORY)................."
    print
    cmd='w2-tc-inventory-epsanal.py cur'
    mf.runcmd(cmd)
    
sys.exit()

    ## -- get ec storms & dtgs
    ##
    #ecstmdtgs=GetEcStmDtgs(dtg,ecstms,ropt,verb=verb)
    #print 'ECstmdtgs: ',ecstmdtgs.keys()


    #if(len(ecstms) > 0):
        
        #for ecstm in ecstms:
            #ecdtgs=ecstmdtgs[ecstm]
            #ecdtgs.sort()
            #if(len(ecdtgs) > 0):
                #for ecdtg in ecdtgs:
                    #if(ecdtg == dtg):
                        #if(verb): print 'got it: ',ecstm,ecdtg
                        #ecstmsthere.append(ecstm)

    #print 'after DTG check -- ecmstmsthere: ',ecstmsthere

    #if(len(ecstmsthere) > 0):

        ##
        ##  sources of id: names database
        ##  from ecbufr cracker
        ##  from metgram .ps
        ##
        
        #name2id=GetName2Stmid(year)
        #et2us=EcId2uSId(dtg)
        #tcs=findtcs(dtg)
        #tcs=DupChkTcs(tcs)
        

        #firstpass=0
        
        #for ecstm in ecstmsthere:

            #ss=ecstm.split('_')
            #etid=ss[0]
            #try:
                #etname=ss[1]
            #except:
                #etname='uuu'

            #try:
                #etwmo=ss[2]
            #except:
                #ecmwo='www'

            #usid=None


            #pspath="/ptmp/ttt.plume.ps"
            #ecurlplume='/products/forecasts/d/getchart/catalog/products/forecasts/medium/tropcyclones/Forecast/plumes'
            #ecurlplume="%s!%s!%s!%s!dummy!chart.ps"%(ecurlplume,year,ecstm,dtg)
            #ecurlplume=httpbase+ecurlplume
            #cmd="wget %s %s \"%s\" -O %s"%(wgetopts,wgetcookies,ecurlplume,pspath)
            #mf.runcmd(cmd,ropt)

            #try:
                #plumes=open(pspath).readlines()
            #except:
                #plumes=[]

            #if(len(plumes) > 0):

                #rlat=None
                #rlon=None

                #for plume in plumes:
                    #if(mf.find(plume,'starting')):
                        #tt=plume.split()
                        #for k in range(0,len(tt)):
                            #if(tt[k] == 'from'):
                                #k1=k+1
                                #rlat=float(tt[k1])
                                #nshem=tt[k1+1]
                                #ewhem=tt[k1+3][0]
                        
                                #if(nshem == 'S'):
                                    #rlat=-rlat
                            
                                #rlon=float(tt[k1+2])
                                #if(ewhem == 'W'):
                                    #rlon=360-rlon

                                #break
                    
                #for tc in tcs:
                    #tc=tc.split()
                    #stmid=tc[1]
                    #blat=float(tc[4])
                    #blon=float(tc[5])

                    #gothit=0
                    #if(rlat != None and rlon != None):
                        #dlat=rlat-blat
                        #dlon=rlon-blon
                        #dr=sqrt(dlat*dlat+dlon*dlon)
                        #if(dr <= drmin):
                            #print 'HHHHHHHHHHHHH ',rlat,rlon,blat,blon,stmid
                            #usid=stmid
                            #gothit=1
                            #break
            
            #if(usid == None):

                #gotecid=0
                #tryname=0
                #gotname=0

                #try:
                    #usid=et2us[etid]
                    #gotecid=1
                #except:
                    #tryname=1
                    #usid=etid

                #if(tryname):
                    
                    #names=name2id.keys()
                    #for name in names:
                        #if(etname == name):
                            #usid=name2id[name]
                            #gotname=1
                            #print 'NNNNNNNN in names: ',name,usid
                        #if(gotname): break

                    #if(gotname == 0):
                        #if(len(etid) == 1):
                            #usid='99'+etid
                        #else:
                            #usid=etid

                    #gothit=2

                #usid="%s.%s"%(usid,year)
                #print 'WWWWWWWWWWW -- alternative sources  tryname: ',tryname,'gotecid: ',gotecid,' gotname: ',gotname,' usid: ',usid

            #if(gothit == 2 and filtexpStorms):
                #print 'WWWWWWWWWWW --  could NOT find real storm for usid: ',usid,' continue...'
                #continue
            

            ## -- processing
            ##
            #didPlots=1
            #pspath="%s/ec.eps.strike.%s.%s.ps"%(pltdir,usid,dtg)
            #ecurlstrike='/products/forecasts/d/getchart/catalog/products/forecasts/medium/tropcyclones/Forecast/strike'
            #ecurlstrike="%s!%s!%s!%s!dummy!chart.ps"%(ecurlstrike,year,ecstm,dtg)
            #ecurlstrike=httpbase+ecurlstrike

            #plotexistbefore=os.path.exists(pspath)
            #cmd="wget %s %s \"%s\" -O %s"%(wgetopts,wgetcookies,ecurlstrike,pspath)
            #mf.runcmd(cmd,ropt)

            #plotexistafter=os.path.exists(pspath)
            #if(not(plotexistbefore) and plotexistafter or override):
                #print 'fffffff SSSSStrike first time got: ',pspath
                #Conver2Png(pspath,usid)
                #Conver2PngWeb(pspath,wdir,landscape=1)
                #firstpass=1

            #pspath="%s/ec.eps.plumes.%s.%s.ps"%(pltdir,usid,dtg)
            #ecurlplumes='/products/forecasts/d/getchart/catalog/products/forecasts/medium/tropcyclones/Forecast/plumes'
            #ecurlplumes="%s!%s!%s!%s!dummy!chart.ps"%(ecurlplumes,year,ecstm,dtg)
            #ecurlplumes=httpbase+ecurlplumes

            #cmd="wget %s %s \"%s\" -O %s"%(wgetopts,wgetcookies,ecurlplumes,pspath)
            #mf.runcmd(cmd)
            #if(firstpass) or override:
                #print 'ffffffff PPPPPPPP plumes first time got: ',pspath
                #Conver2Png(pspath,usid)
                #Conver2PngWeb(pspath,wdir,landscape=0)

    
        #if(firstpass and dolp):
            #print 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF finalize first pass processing'
            #SendPng2HurPrn(pltdir,dtg,dolp)

            
## -- do the inventory now
##
#if(w2.W2doTcepsAnl and didPlots):
    #cmd='w2-tc-inventory-epsanal.py cur'
    #mf.runcmd(cmd)
    
        

#if(doftp4jtwc and ropt != 'norun'):
            
    #localdir=pltdir
    #remotedir='ecmwf/eps'
    #mask="ec.eps.*.*.%s.ps"%(dtg)
    #mf.doFTPsimple(server,localdir,remotedir,mask,opt='ftp.put')

