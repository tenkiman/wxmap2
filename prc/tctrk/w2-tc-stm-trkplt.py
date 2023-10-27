#!/usr/bin/env python

from tcbase import *

stmDZModels={}

stmDZ05ls={
    '05la':('2019082400.2019090612.12',' 5,-95,45,-30'),
    '05lb':('2019082800.2019090312.12','10,-95,40,-45'),
    '05lc':('2019090200.2019090612.12','20,-90,45,-40'),

}


def getmodelOpt(stmid):
    
    # -- model opt
    # 
    rc=getStmParams(stmid)
    iyear=int(rc[2])
    
    if(iyear == 2019):
        fmodelOpt=modelOpt2019
        # -- do JGSM for wpac only
        if(rc[1] == 'W'): fmodelOpt=modelOptWPAC2019
    
    else:
        
        fmodelOpt=modelOpt
        # -- do JGSM for wpac only
        if(rc[1] == 'W'): fmodelOpt=modelOptWPAC

    if(doOps): 
        if(IsNhcBasin(stmid)):
            fmodelOpt=modelOpt06Nhc
        elif(IsJtwcBasin(stmid)):
            fmodelOpt=modelOpt06Jtwc
    
    
    return(fmodelOpt)    
     

def setSdtgOpt(endDtg,sdtgopt):

    (bdtg,edtg,ddtg)=sdtgopt.split('.')
    nbdtg=bdtg
    nedtg=edtg
    
    if(mf.find(endDtg,'cur')):
        bdtgs=mf.dtg_dtgopt_prc(endDtg)
        nbdtg=bdtgs[0]
        nedtg=edtg
    else:
        if(len(endDtg) == 10):
            nbdtg=endDtg
        else:
            
            try:
                tauinc=int(endDtg)
                nbdtg=mf.dtginc(edtg,-tauinc)
                if(tauinc < 0):
                    nedtg=nbdtg
            except:
                nbdtg=bdtg
                nedtg=edtg
                None
    
    sdtgopt="%s.%s.%s"%(nbdtg,nedtg,ddtg)
    
    return(sdtgopt)
    

def getZoomLatLonBounds(tD,stmid,dobt,cur12dtg=None,endDtg=None,doOps=0,unZoom=0,
                        ddtg=12,aspectMin=1.33,aspectMax=1.67,verb=0):

    def getLatLonOcard(ocard):
        bb=ocard.split()
        clat=bb[4]
        clon=bb[5]
        bvmax=int(bb[2])
        (blat,blon)=Clatlon2Rlatlon(clat,clon)
        return (blat,blon,bvmax)
    
    def setBElatlon(blat,elat,blon,elon,bdy,edy,bdx,edx,verb=0):

        # -- SHEM check...push the poleward boundary
        #
        if(blat < 0.0 and elat < 0.0):
            zblat=(int(blat+0.5)/5 + edy)*5
            zelat=(int(elat+0.5)/5 - bdy)*5
        else:
            zblat=(int(blat+0.5)/5 - bdy)*5
            zelat=(int(elat+0.5)/5 + edy)*5
            
        zblon=(int(blon+0.5)/5 - bdx)*5
        zelon=(int(elon+0.5)/5 + edx)*5
        
        
        # -- not sure why... for case of lant/epac?  make sure both are in W hemi
        # -- doesn't work for SWPAC storms crossing 180E
        #
        if(zblon > 180 and zelon > 180): 
            zblon=zblon-360
            zelon=zelon-360
        
        zlatLen=float(zelat-zblat)
        zlonLen=float(zblon-zelon)
        
        zaspect=abs(zlonLen)/abs(zlatLen)

        # -- really a SHEM check...for grads want the blat to be the smallest
        #
        if(zelat < zblat):
            ee=zelat
            zelat=zblat
            zblat=ee

        if(verb):
            print 'BElat: ',zblat,zelat,'BElon: ',zblon,zelon
            print 'Zlen: ',zlatLen,zlonLen,'aspect: ',zaspect
        
            
        return(zblat,zelat,zblon,zelon,zaspect)

    ocards=tD.lsDSsStmCards(stmid,dobt=dobt)
    ocards9X=tD.lsDSsStmCards(stmid,dobt=0)

    sumcard=tD.lsDSsStmCards(stmid,dobt=dobt,sumonly=1)
    sumcard9X=tD.lsDSsStmCards(stmid,dobt=0,sumonly=1)

    odtgs=ocards.keys()
    odtgs.sort()
    
    odtgs9X=ocards9X.keys()
    odtgs9X.sort()

    stmodtgs=odtgs
    tcdtgs=[]
    gdtgs=[]
    for odtg in stmodtgs:
        if(mf.find(odtg,'summ')): continue
        tt=ocards[odtg].split()
        sdtg=tt[0]
        if( mf.find(sdtg,'*') and MF.is0012Z(sdtg)): gdtgs.append(sdtg)
        if(MF.is0012Z(sdtg)): tcdtgs.append(sdtg[0:10])
        if(doOps and MF.is0618Z(sdtg)): tcdtgs.append(sdtg[0:10])
    
    # -- if no gen dtgs then get cards with dobt=0
    #
    doBT=2
    if(len(gdtgs) == 0):
        
        print 'WWW-getZoomLatLonBounds:  no genesis dtgs for stmid: ',stmid,' and dobt=1 ... try dobt=0'
        stmodtgs=odtgs9X
        tcdtgs=[]
        gdtgs=[]
        for odtg in stmodtgs:
            if(mf.find(odtg,'summ')): continue
            tt=ocards9X[odtg].split()
            sdtg=tt[0]
            if( mf.find(sdtg,'*') and MF.is0012Z(sdtg)): gdtgs.append(sdtg)
            if(MF.is0012Z(sdtg)): tcdtgs.append(sdtg[0:10])
            if(doOps and MF.is0618Z(sdtg)): tcdtgs.append(sdtg[0:10])
        
        ocards=ocards9X
        odtgs=odtgs9X
        doBT=0
    
    sNameMD2=tD.getStmNameMD2(stmid)
    sNamePY=GetTCName(stmid)
    
    if(sNameMD2 != None):
        sName=sNameMD2
    else:
        sName=sNamePY

    if(len(gdtgs) == 1):
        bdtg=gdtgs[0][0:10]
    elif(len(gdtgs) > 1):
        bdtg=gdtgs[-2][0:10]
    else:
        print 'WWW-no genesis dtgs...return None'
        return(None,None,None)
    
    # -- ops bdtg
    #
    if(doOps): bdtg=mf.dtginc(bdtg,6)

    # -- scan tcdtgs for last TC dtg
    #
    tcdtgs.reverse()
    edtg=None
    for tcdtg in tcdtgs:
        tt=ocards[tcdtg].split()
        tcstate=tt[11]
        tcstate=tcstate[-2:]
        istc=IsTc(tcstate)
        if(istc >= 1 and istc <=2):
            edtg=tcdtg
            break
        
    # -- ops edtg -- don't need since pulling 06/18Z tcdtgs
    #
    #if(doOps): edtg=mf.dtginc(edtg,6)
        
    if(cur12dtg != None):
        c12dtgs=mf.dtg_dtgopt_prc(cur12dtg)
        icur12dtg=c12dtgs[0]
        if(doOps): cur12dtg=mf.dtginc(icur12dtg,6)
        
        if(cur12dtg in tcdtgs):
            print 'III-getZoomLatLonbounds-cur12dtg: ',cur12dtg,' in tcdtgs...using edtg: ',cur12dtg
            edtg=cur12dtg
        else:
            print 'WWW-getZoomLatLonbounds-cur12dtg: ',cur12dtg,' NOT in tcdtgs...using edtg: ',edtg
            if(edtg == None):
                print 'WWW-not enough dtgs to plot...return None'
                return(None,None,None)
        
    sdtgopt="%s.%s.%s"%(bdtg,edtg,ddtg)
    
    if(endDtg != None):
        sdtgopt=setSdtgOpt(endDtg, sdtgopt)
        (bdtg,edtg,ddtg)=sdtgopt.split('.')
        
    fmodelOpt=getmodelOpt(stmid)

    if(doOps): 
        if(IsNhcBasin(stmid)):
            fmodelOpt=modelOpt06Nhc
        elif(IsJtwcBasin(stmid)):
            fmodelOpt=modelOpt06Jtwc
        

    # -- check ending dtg
    #
    edtgdiff=mf.dtgdiff(curdtg,edtg)
    
    # -- check if going hot
    #
    actualCur12dtg=mf.dtg_dtgopt_prc('cur12')[0]
    
    if(doOps and edtgdiff > -6):
        edtg=mf.dtginc(edtg,-6)
    elif(not(doOps) and edtgdiff > -12 and edtg != actualCur12dtg):
        edtg=mf.dtginc(edtg,-12)
     
     
    if(edtg == actualCur12dtg):
        print 'III-getZoomLatLonbounds-cur12dtg on command line using -e -- edtg = real-time cur12: ',actualCur12dtg
        
        
    ocardB=ocards[bdtg]
    ocardE=ocards[edtg]

    (blat,blon,bvmax)=getLatLonOcard(ocardB)
    (elat,elon,evmax)=getLatLonOcard(ocardE)
    
    # -- shem
    #
    isShem=0

    mvEast2West=1
    if(blon > elon): mvEast2West=0
    
    if(blat < 0):
        isShem=1
        if(elat < -20.0 or blat < -20.0):
            edy=3 ; bdy=1
        else:
            edy=3 ; bdy=2
        
    # -- nhem
    #
    else:
        if(elat > 20.0):
            edy=4 ; bdy=1
        else:
            edy=3 ; bdy=2
    
    mvEq2Pole=1
    if(isShem and elat > blat): mvEq2Pole=0
    elif(blat < elat): mvEq2Pole=0
    
    if(mvEq2Pole): 
        if(isShem):
            bdx=5
            edx=4
        else:
            bdx=4
            edx=3
    else:
        bdx=4
        edx=3
        
    # -- make sure  blon < elon for grads dim env
    #
    if(blon > elon):
        ee=elon
        bb=blon
        blon=ee
        elon=bb
        
    # -- make sure blat < elat for grads dim env
    #
    if(blat > elat):
        ee=elat
        bb=blat
        blat=ee
        elat=bb
        
    if(verb): print 'eeelllaaattt',blat,elat,blon,elon,'bbyyy',bdy,'e',edy,'bbbxxxx',bdx,edx
    (zblat,zelat,zblon,zelon,zaspect)=setBElatlon(blat,elat,blon,elon,bdy,edy,bdx,edx,verb=verb)

    # -- adjust longitude for bigger plot for 'tall' TCs
    #
    if(verb): print '000000',zaspect,aspectMin,'zzzz',zblat,zelat,'lll',zblon,zelon

    while(zaspect <= aspectMin):
        
        bdx=bdx+0
        edx=edx+1
        
        (zblat,zelat,zblon,zelon,zaspect)=setBElatlon(blat,elat,blon,elon,bdy,edy,bdx,edx,verb=verb)
        if(verb): print '------',zaspect,zblat,zelat,'lll',zblon,zelon,'bdx: ',bdx,'edx: ',edx

    # -- adjust latitude for 'wide' TCs
    #
    while(zaspect >= aspectMax):
        if(verb): print '++++++',zaspect,aspectMax,zblat,zelat,'lll',zblon,zelon,'bbee',bdx,edx,bdy,edy
        if(isShem):
            #bdx=bdx-1
            #edx=edx-0
            bdy=bdy+1
            edy=edy+0
        else:
            bdy=bdy-0
            edy=edy+1
            
        if(verb): print '+++bbee',bdx,edx,bdy,edy
        (zblat,zelat,zblon,zelon,zaspect)=setBElatlon(blat,elat,blon,elon,bdy,edy,bdx,edx,verb=verb)
        if(verb): print '++++++',zaspect,aspectMax,zblat,zelat,'lll',zblon,zelon

    zoomopt="%d,%d,%d,%d"%(zblat,zblon,zelat,zelon)
    
    if(unZoom): zoomopt=''

    stmDZ=("%s.%s.%s"%(bdtg,edtg,ddtg),zoomopt,fmodelOpt)

    sNamePY=GetTCName(stmid)
    
    if(sName != sNamePY):
        print 'WWW-storm name from adecks != from storms*.txt'

    if(verb):
        print '  STMID: ',stmid
        print '  sName: ',sName,' sNamePY: ',sNamePY,' sNameMD2: ',sNameMD2
        print 'BBBBDTG: ',bdtg
        print 'EEEEDTG: ',edtg
        print 'DDDDDTG: ',ddtg
        print 'BBBBLAT: ',blat,blon
        print 'EEEELON: ',elat,elon
        print 'ZZZZBBB: ',zblat,zelat,zblon,zelon
        print 'ZASPECT: ',zaspect
        print 'ZOOMOPT: ',zoomopt
        print 'stmDDZZ: ',stmDZ

    sNameT=(sName,sNameMD2,sNamePY)
    return(stmDZ,doBT,sNameT)


def makeFOFjsHtm(stmid,sName,doOps,unZoom,
                 TrkPltDirs,FOFpaths,FOFpathJSs,HtmPaths,
                 xWsize=xsizeTcTrk,ropt=''):
    
    rc=getStmParams(stmid)
    s3id=rc[0]+rc[1].upper()
    syear=rc[2]
    
    yWsize=int(xWsize*0.75)

    TrkPltDir=TrkPltDirs[stmid]
    FOFpath=FOFpaths[stmid]
    FOFpathJS=FOFpathJSs[stmid]
    (HtmPath,HtmPathCur)=HtmPaths[stmid]

    rc=getStmParams(stmid)
    syear=rc[2]
    
    (fdir,ffile)=os.path.split(FOFpath)
    FF=open(FOFpath,'w')

    if(unZoom):
        pmask="%s/trkplt-*-UNZOOM-*.png"%(TrkPltDir)
    else:
        pmask="%s/trkplt-*png"%(TrkPltDir)
    pltPaths=glob.glob(pmask)
    pltPathsDict={}
    pdtgs=[]

    bdtg=None
    omodels=None
    pnum=None
    
    for ppath in pltPaths:
        (pdir,pfile)=os.path.split(ppath)
        pp=pdir.split('/')
        if(bdtg == None): 
            pnum=pp[-2]
            bdtg=pp[-1]
            
        pp=pfile.split('.')[0].split('-')
        pdtg=pp[1]
        if(omodels == None):
            pmodels=pp[2:]
            omodels='%s'%(pmodels[0])
            for pmodel in pmodels[1:-2]:
                omodels="%s, %s"%(omodels,pmodel)
            omodels="%s, %s"%(omodels,pmodels[-2])
                
        pdtgs.append(pdtg)
        odtg=mf.dtg2gtime(pdtg)
        odtg=odtg[0:3]+ ' ' + odtg[3:-4]+ ' ' + odtg[-4:]
        
        pcard='''./%s/%s/%s/%s "%s"\n'''%(syear,s3id,bdtg,pfile,odtg)
        
        pltPathsDict[pdtg]=pcard
        
    pdtgs.sort()
    for pdtg in pdtgs:
        pcard=pltPathsDict[pdtg]
        FF.writelines(pcard)
    FF.close()
    
    
    FF=open(FOFpathJS,'w')
    (jdir,jfile)=os.path.split(FOFpathJS)
    jcard="""var fof_file = './%s/%s/%s/%s'\n
var win_size = '%d,%d'\n
"""%(syear,s3id,bdtg,ffile,xWsize,yWsize)
    FF.writelines(jcard)
    FF.close()
    
    if(pnum == None):
        print 'EEE -- no plots to make...sayounara...'
        return(None)

    omodels='''<span style="color:red"> %s </span>'''%(omodels)
    hcard="%s.%s - MODels"%(pnum,syear)
    if(doOps): hcard="%s.%s - OPS"%(pnum,syear)
    tcard="TCtrk: %s.%s [%s] models: %s end DTG: %s"%(pnum,syear,sName,omodels,bdtg)
    jcard="./%s/%s/%s/%s"%(syear,s3id,bdtg,jfile)
    
    # -- html
    #
    
    dirh="../.."
    dirh='.'
    dirjs="%s/js"%(dirh)
    dircss="%s/css"%(dirh)
    dirfavicon=dirh
    
    htmjs="""
<!DOCTYPE html>
<html>
<head>

  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=Edge"/>
  <title>%s</title>
 
  <script type="text/javascript" src="%s"> </script>
  <script type="text/javascript" src="%s/hanis_min.js"> </script>
  <script type="text/javascript" src="%s/hanconfig.js"> </script>
"""%(hcard,jcard,dirjs,dirjs)
    
    htmcss="""
  <link rel="shortcut icon" href="%s/favicon.ico">
  <link rel="stylesheet" href="%s/wxmain.css" type="text/css">
  <link rel="stylesheet" href="%s/wxmain2.css" type="text/css">
  <link rel="stylesheet" href="%s/dropdown.css" type="text/css">
</head>
"""%(dirfavicon,dircss,dircss,dircss)
    
    htmbody="""

<body text="black" link="blue" vlink="purple" bgcolor="#fcf1da" style="width:%dpx;" onload="HAniS.setup(hancon,'handiv') ">

<!--
<p>
%s
</p>
-->
  <div id="handiv" style="background-color:#808080;">
  </div>

</body>
</html>
"""%(xWsize,tcard)
    
    htm=htmjs+htmcss+htmbody
    
    HH=open(HtmPath,'w')
    HH.writelines(htm)
    HH.close()
    
    # -- now make ln -s to current
    #
    cmd="ln -f -s %s %s"%(HtmPath,HtmPathCur)
    mf.runcmd(cmd,ropt)
    
def VeriFy(stmid,modelOpt,override=0,
           doVeriInt=0,doVeriHomo=0,doVeriLand=0,
           doX=0):    

    veriType='pe'
    if(doVeriInt): veriType='vbias'
        
    rc=getStmParams(stmid)
    b1id=rc[1]
    vmodelOpt=modelOpt
    filtOpt='z0012'
    title1="PE for %s models"%(stmid)
    vcase="%s-model"%(stmid)
    
    if(doOps): 
        if(IsNhcBasin(b1id)):
            vmodelOpt=modelOpt06Nhc
            if(veriType == 'vbias'): vmodelOpt=modelOpt06NhcInt
            filtOpt='z0618'
            vcase='%s-nhc'%(stmid)
            title1="PE for %s NHC ops"%(stmid)
        elif(IsJtwcBasin(b1id)):
            vmodelOpt=modelOpt06Jtwc
            filtOpt='z0618'
            vcase='%s-jtwc'%(stmid)
            title1="PE for %s JTWCops"%(stmid)


    hOpt='-H'
    if(doVeriHomo): 
        hOpt=''
        vcase="%s-homo"%(vcase)
    
    vdir=TrkVeriDirs[stmid]
    MF.ChangeDir(vdir)
    
    oOpt=''
    if(override): oOpt='-O'
    xOpt='-X -x'
    if(doX): xOpt='-X'
    
    # -- run twice, 1st with no land points; then with all BT
    #
    # -- 20201004 -- pyplot crashing? try doing a sleep?
    sleep(1)
    vlOpt='-L'
    cmd='''%s -T %s -S %s -f %s -1 "%s" -c %s -p %s %s %s %s %s'''%(pycmdV,vmodelOpt,
                                                                    stmid,filtOpt,title1,vcase,veriType,
                                                                    hOpt,xOpt,oOpt,vlOpt)
    mf.runcmd(cmd,ropt)

    sleep(1)
    vlOpt=''
    cmd='''%s -T %s -S %s -f %s -1 "%s" -c %s -p %s %s %s %s %s'''%(pycmdV,vmodelOpt,
                                                                    stmid,filtOpt,title1,vcase,veriType,
                                                                    hOpt,xOpt,oOpt,vlOpt)
    mf.runcmd(cmd,ropt)

    MF.ChangeDir(curdir)
    
    
    

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'dtgs'],
            #2:['modelopt',  """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
            }

        self.options={
            'doOps':           ['P',0,1,'do ad2 and and p06'],
            'override':        ['O',0,1,'override'],
            'overrideHtm':     ['H',0,1,'override making the .js .txt and .htm'],
            'stmopt':          ['S:',None,'a','stmopt for any storm'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'useReftrkOpt':    ['R:',None,'a','use reftrk based on BT and FC for storms set'],
            'doVeri':          ['v',1,0,'do NOT verfication -- pe'],
            'doVeriHomo':      ['h',0,1,'do homo verfication'],
            'doX':             ['X',0,1,' do X after plot made'],
            'ropt':            ['N','','norun',' norun is norun'],
            'unZoom':          ['U',0,1,"""don't do zoom"""],
            'doAll':           ['A',0,1,"""run all four version"""],
            'do9X':            ['9',0,1,"""do 9X storms"""],
            'endDtg':          ['E:',None,'a',' set ending dtg'],
            'maxTauOpt':       ['t:',120,'i',""" set maxtau plot [120]"""],
            'modOpt':          ['M:',None,'a',""" set models: None | 'waf' (2021 paper)"""],
            'modOpt6':         ['6:',None,'a',""" set models at tau6: None | 'waf' (2021 paper)"""],
            'cur12dtg':        ['e:',None,'a',' set cur12dtg to set ending dtg'],
            }

        self.purpose='''
plot trks for active and other storms'''
        
        self.examples='''
%s -S cur-e cur12 -O -R 09l     # model version with edtg=cur12 and reftrk for 09l
%s -S cur -O                    # model version use autoset of edtg
%s -S cur -P -O                 # operational version'''

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

modelOpt2019='hwrf,tecm4,emdt,avno' # - use new pull from ecmwf -- add cmc
modelOptWPAC2019='hwrf,tecm4,emdt,jgsm,avno' # - use new pull from ecmwf -- add cmc
modelOpt062019='hwrf06,tecm406,emdt06,avno06'
modelOpt06WPAC2019='hwrf06,tecm406,emdt06,jgsm06,avno06'

# -- 20200724 add tjgsm
#
modelOpt='hwrf,tecm5,emdt,tcgd2,tjgsm,avno' # - use new pull from ecmwf -- add cmc
modelOptWPAC='hwrf,tecm5,emdt,tcgd2,tjgsm,avno' # - use new pull from ecmwf -- add cmc
modelOpt06='hwrf06,tecm506,emdt06,tcgd206,tjgsm06,avno06'
modelOpt06WPAC='hwrf06,tecm506,emdt06,tcgd206,tjgsm06,avno06'

modelOpt06Nhc='%s,tvcn,ofcl'%(modelOpt06)
modelOpt06NhcInt='%s,ivcn,ofcl'%(modelOpt06)
modelOpt06NhcAll='%s,tvcn,ivcn,ofcl'%(modelOpt06)
modelOpt06Jtwc='%s,conw,jtwc'%(modelOpt06)

modelOpt06Nhc2019='%s,tvcn,ofcl'%(modelOpt062019)
modelOpt06NhcInt2019='%s,ivcn,ofcl'%(modelOpt062019)
modelOpt06NhcAll2019='%s,tvcn,ivcn,ofcl'%(modelOpt062019)
modelOpt06Jtwc2019='%s,conw,jtwc'%(modelOpt062019)

# -- 20210102 -- for WAF paper 2020 lant
# -- 20200724 add tjgsm
#
if(modOpt != None):
    if( modOpt == 'waf'):
        modelOpt='hwrf,avno,tecm5' # - use new pull from ecmwf -- add cmc
        modelOptWPAC='hwrf,avno,tecm5' # - use new pull from ecmwf -- add cmc
    else:
        modelOpt=modOpt
        modelOptWPAC=modOpt
        
if(modOpt6 != None):
    modelOpt06Nhc=modOpt6
    modelOpt06Jtwc=modOpt6
        

MF.sTimer('ALL-%s'%(CL.pyfile))                

if(doAll):
    
    MF.sTimer("%s-ALL"%(pyfile))
    allOpts=['','-U','-P','-P -U']
    
    for aopt in allOpts:
        cmd="%s "%(pypath)
        for o,a in CL.opts:
            if(o != '-A'):
                cmd="%s %s %s"%(cmd,o,a)
                
        cmd="%s %s"%(cmd,aopt)
        mf.runcmd(cmd,ropt)
    MF.dTimer("%s-ALL"%(pyfile))
    sys.exit()
        
        

# -- basic setup
#
pycmdT="/w21/prc/tctrk/w2-tc-trkplt.py"
pycmdV="/w21/prc/tcdat/w2-tc-dss-vd2-anl.py"

# -- max tau to plot...
#
maxTau=maxTauOpt

#if(mf.find(stmopt,'cur') or override): override=1

if(stmopt == None):
    print 'EEE -- must set...typically cur'
    sys.exit()
    

do05l=0
doI=1
if(do05l): doI=1


if(do05l): pyStms=['05lc']

Xopt=''
if(doX): Xopt='-X'
Iopt=''
if(doI): Iopt='-I 0.70'


# -- find the storms and set the dtg and zoom ranges
#
dobt=1
if(do9X): dobt=0

if(cur12dtg == None):
    cur12dtg=mf.dtg_dtgopt_prc('cur12-12')[0]
    
elif(cur12dtg == 'cur12'):
    cur12dtg=mf.dtg_dtgopt_prc('cur12')[0]
    

if(mf.find(stmopt,'cur')):
    dtgopt='cur12-12'
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    tD=TcData(dtgopt=dtgopt)
    sdtg=dtgs[0]
    activeStorms=tD.getStmidDtg(sdtg,dobt=dobt)
    
elif(stmopt != None):
    (activeStorms,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt=stmopt,dobt=dobt)


# -- get dtgs for aids
#
MF.sTimer('tcA-aidDtgs')
aidDtgs={}
for tstmid in activeStorms:

    fmodelOpt=getmodelOpt(tstmid)
    print
    print 'aidDtgs for tstmid: ',tstmid
    tcA=TcAidTrkAd2Bd2(stmopt=tstmid, dtgopt=None, do9Xonly=0, dobt=0, 
                      source='tmtrkN', dsbdir=None, 
                      quiet=1, verb=0)

    
    taids=fmodelOpt.split(',')
    for taid in taids:
        try:
            adtgs=tcA.getAidStatus(taid, tstmid)
        except:
            print 'WWW--in tcA...no dtgs...set to zero length'
            adtgs=[]
        
        if(len(adtgs) == 0):
            print 'WWW-- no dtgs for tstmid: ',tstmid,' taid: ',taid
            
        aidDtgs[taid,tstmid]=adtgs
    
    print
    
MF.sTimer('tcA-aidDtgs')
    
pyStms=activeStorms

# -- set up output dirs and calc zoom lat/lon bounds
#
TrkVeriDirs={}
TrkPltDirs={}
FOFpaths={}
FOFpathJSs={}
HtmPaths={}
chkHtmPaths={}

chkFOFpaths={}
chkFOFpathJSs={}

doBTs={}
sNames={}

# -- first check if enough dtgs
#
opyStms=[]
for stmid in pyStms:
    (zoomDZ,doBT,sNameT)=getZoomLatLonBounds(tD,stmid,dobt,cur12dtg,endDtg,doOps,unZoom,verb=verb)
    if(zoomDZ != None): opyStms.append(stmid)
    
pyStms=opyStms
    


# -- set up stmDZ and paths by stmid
#
for stmid in pyStms:
    
    (zoomDZ,doBT,sNameT)=getZoomLatLonBounds(tD,stmid,dobt,cur12dtg,endDtg,doOps,unZoom,verb=verb)
    
    # -- check if enought dtgs to plot
    #
    if(zoomDZ == None): break
        
    
    (sName,sNameMD2,sNamePY)=sNameT
    stmDZModels[stmid]=zoomDZ
    
    # -- set doBT for 01W.19
    #
    
    doBTs[stmid]=doBT
    sNames[stmid]=sName
    
    finaldtg=zoomDZ[0].split('.')[1]
    zoomopt=zoomDZ[-2]
    fmodelOpt=zoomDZ[-1]
    
    rc=getStmParams(stmid)
    s3id=rc[0]+rc[1].upper()
    syear=rc[2]
    
    BaseDirRoot='%s/tctrkveriDAT/%s/%s'%(w2.HfipProducts,syear,s3id)
    BaseDirRootW2='%s/tctrkveri'%(w2.HfipProducts)
    
    HtmDir=BaseDirRootW2
    HtmRoot="%s/%s/%s"%(syear,s3id,finaldtg)
    
    TrkPltDirRoot=BaseDirRoot
    TrkPltDir="%s/%s"%(TrkPltDirRoot,finaldtg)

    TrkVeriDir="%s/veri"%(TrkPltDirRoot)

    TrkVeriDirs[stmid]=TrkVeriDir
        
    print 'TV dirs stmid: ',stmid
    print '        sName: ',sName
    print '     sNameMD2: ',sNameMD2
    print '      sNamePY: ',sNamePY
    print '     finaldtg: ',finaldtg
    print '      zoomopt: ',zoomopt
    print '    fmodelOpt: ',fmodelOpt
    print '       HtmDir: ',HtmDir
    print '      HtmRoot: ',HtmRoot
    print '   TrkVeriDir: ',TrkVeriDir
    print '    TrkpltDir: ',TrkPltDir

    if(ropt != 'norun'):
        MF.ChkDir(TrkVeriDir,'mk')
        MF.ChkDir(TrkPltDir,'mk')
        
    if(ropt == 'norun'): continue
        
    fofmodel=fmodelOpt.replace(',','-')

    # -- set htm
    #
    
    if(unZoom): 
        HtmMask="trk-%s-%s-MOD-*-%s.UNZOOM.htm"%(s3id,syear,fofmodel)
        Htmfile="trk-%s-%s-MOD-%s-%s.UNZOOM.htm"%(s3id,syear,finaldtg,fofmodel)
        HtmfileCur="trk-%s-%s-MOD-CUR.UNZOOM.htm"%(s3id,syear)
    else:       
        HtmMask="trk-%s-%s-MOD-*-%s.htm"%(s3id,syear,fofmodel)
        Htmfile="trk-%s-%s-MOD-%s-%s.htm"%(s3id,syear,finaldtg,fofmodel)
        HtmfileCur="trk-%s-%s-MOD-CUR.htm"%(s3id,syear)
    if(doOps): 
        if(unZoom): 
            HtmMask="trk-%s-%s-OPS-*-%s.UNZOOM.htm"%(s3id,syear,fofmodel)
            Htmfile="trk-%s-%s-OPS-%s-%s.UNZOOM.htm"%(s3id,syear,finaldtg,fofmodel)
            HtmfileCur="trk-%s-%s-OPS-CUR.UNZOOM.htm"%(s3id,syear)
        else:       
            HtmMask="trk-%s-%s-OPS-*-%s.htm"%(s3id,syear,fofmodel)
            Htmfile="trk-%s-%s-OPS-%s-%s.htm"%(s3id,syear,finaldtg,fofmodel)
            HtmfileCur="trk-%s-%s-OPS-CUR.htm"%(s3id,syear)
            
    HtmPath="%s/%s"%(HtmDir,Htmfile)
    HtmPathCur="%s/%s"%(HtmDir,HtmfileCur)
    #HtmPathCur="%s/%s"%('.',HtmfileCur)

    if(unZoom):
        FOFfile="fof-%s-unzoom.txt"%(fofmodel)
        FOFfileJS="fof-%s-unzoom.js"%(fofmodel)
        FOFpath="%s/%s"%(TrkPltDir,FOFfile)
        FOFpathJS="%s/%s"%(TrkPltDir,FOFfileJS)
    else:
        FOFfile="fof-%s.txt"%(fofmodel)
        FOFfileJS="fof-%s.js"%(fofmodel)
        FOFpath="%s/%s"%(TrkPltDir,FOFfile)
        FOFpathJS="%s/%s"%(TrkPltDir,FOFfileJS)

    chkHtmPath=MF.ChkPath(HtmPath)
    chkFOFpath=MF.ChkPath(FOFpath)
    chkFOFpathJS=MF.ChkPath(FOFpathJS)

    if(ropt != 'norun'):
        if(chkFOFpath):
            if(override):
                print 'FFF-OOO killing: ',FOFpath
                os.unlink(FOFpath)
            else:
                print 'FFF-AALLRREEAADDYY: ',FOFpath,' already done...'
        else:
            print 'FFF-MAKE FOFpath: ',FOFpath,'...'
            
            
    print '   HtmPathCur: ',HtmPathCur
    print '      HtmPath: ',HtmPath,'  chkHtmPath: ',chkHtmPath
    print '      FOFpath: ',FOFpath,'  chkFOFpath: ',chkFOFpath
    print '    FOFpathJS: ',FOFpathJS,' chkFOFpathJS: ',chkFOFpathJS

    # -- if override...blow off everything
    #
    if(override):
        print
        print 'III -- killing all files in TrkPltDir: ',TrkPltDirRoot
        if(doOps):
            if(unZoom):
                cmd="rm %s/????????06/*UNZOOM*"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
                cmd="rm %s/????????18/*UNZOOM*"%(TrkPltDirRoot)
            else:
                cmd="rm -r %s/????????06"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
                cmd="rm -r %s/????????18"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
        else:
            if(unZoom):
                cmd="rm %s/????????00/*UNZOOM*"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
                cmd="rm %s/????????12/*UNZOOM*"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
            else:
                cmd="rm -r %s/????????00"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
                cmd="rm -r %s/????????12"%(TrkPltDirRoot)
                mf.runcmd(cmd,ropt)
                
        cmd="rm %s/%s"%(HtmDir,HtmMask)
        mf.runcmd(cmd,ropt)
        print
    
        
    chkHtmPaths[stmid]=chkHtmPath
    chkFOFpaths[stmid]=chkFOFpath
    chkFOFpathJSs[stmid]=chkFOFpathJS
    HtmPaths[stmid]=(HtmPath,HtmPathCur)    
    FOFpaths[stmid]=FOFpath
    FOFpathJSs[stmid]=FOFpathJS
    TrkPltDirs[stmid]=TrkPltDir
    
    if(overrideHtm):
        rc=makeFOFjsHtm(stmid,sName,doOps,unZoom,
                        TrkPltDirs,FOFpaths,FOFpathJSs,HtmPaths)
        
        sys.exit()

# -- make the ad2 for ops comps
#
if(doOps):
    
    for stmid in pyStms:

        (sdtgopt,zoomopt,fmodelOpt)=stmDZModels[stmid]
        fmodelOptAD2=modelOpt
        
        amodelOpt=fmodelOptAD2
        adtgs=mf.dtg_dtgopt_prc(sdtgopt)
        adtgTouch="%s_%s"%(adtgs[0],adtgs[-1])
        
        touchFile="ad2_06_%s_%s"%(stmid,amodelOpt)
        touchFile=touchFile.replace(',','_')
        touchFile="%s_%s"%(touchFile,adtgTouch)
        touchDir=TrkVeriDirs[stmid]
        touchPath="%s/%s"%(TrkVeriDir,touchFile)
        tsiz=MF.getPathSiz(touchPath)
        
        if(tsiz < 0 or override):
        
            cmd='w2-tc-dss-ad2.py -S %s -T %s -h 6'%(stmid,amodelOpt)
            mf.runcmd(cmd,ropt)
            cmd="touch %s"%(touchPath)
            mf.runcmd(cmd,ropt)
 

# -- cycle storms
#

for stmid in pyStms:

    pstm=stmid
    (sdtgopt,zoomopt,fmodelOpt)=stmDZModels[stmid]
    finaldtg=sdtgopt.split('.')[1]

    vmodelOpt=getmodelOpt(stmid)
    
    doBT=doBTs[stmid]

    if(doOps): Iopt='-I 0.70'
    
    if(zoomopt != ''): szoomopt='-Z %s'%(zoomopt)
    else: szoomopt=''
    
    if(unZoom):
        szoomopt=''
    
    # -- use reftrk for storms set by the useReftrkOpt
    #
    useReftrk=0
    if(useReftrkOpt == None): useReftrk=0
    if(useReftrkOpt != None):
        try:
            urStms=useReftrkOpt.split(',')
        except:
            urStms=[]
            
        for urStm in urStms:
            if(stmid[0:3] == urStm.upper()): useReftrk=1
    
    if(useReftrk):
        szoomopt='-R'
    
    cOpt='-1 %s'%(finaldtg)

    oOpt=''
    if(override): oOpt='-O -Q'
    
    bTOpt=''
    if(doBT == 0): bTOpt='-b'

    if(pstm == '09L.2022'):
        szoomopt="-Z 10,-90,35,-65"
        
    print 'sss',szoomopt

    if(not(overrideHtm)):
        cmd="%s %s %s -S %s %s %s -M %d -C %s %s %s %s"%(pycmdT,sdtgopt,fmodelOpt,pstm,cOpt,szoomopt,maxTau,bTOpt,oOpt,Xopt,Iopt)
        mf.runcmd(cmd,ropt)

    dohtm=(ropt != 'norun' and (override or overrideHtm or not(chkFOFpaths[stmid])) ) 
    if(dohtm and ropt != 'norun'):
        rc=makeFOFjsHtm(stmid,sName,doOps,unZoom,
                        TrkPltDirs,FOFpaths,FOFpathJSs,HtmPaths)
        
        if(rc == None):
            print 'WWW -- no runs to plot...for stmid: ',stmid
            #continue

    # -- verification
    #
    if(doVeri or doVeriHomo and ropt != 'norun'): 
        rc=VeriFy(stmid, vmodelOpt,override=override)
        rc=VeriFy(stmid, vmodelOpt,doVeriInt=1,override=override)
        
# -- rsync to wxmap2.com
#
web='tctrkveri'
rc=rsync2Wxmap2(web,stmid=stmid,ropt=ropt,doBail=0)


MF.dTimer('ALL-%s'%(CL.pyfile))                
        
        
