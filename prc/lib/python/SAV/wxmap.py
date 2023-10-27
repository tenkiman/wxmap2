import os,sys
import mf
import signal

from w2switches import *

WxmapCenter='NHC'
WxmapCenter='ESRL/GSD/AMB'

PzalWxmapBaseDir='/tdocommon/wxmap'

W2BaseDir=os.getenv('W2')
W2BasePrcDir=os.getenv('W2_PRC_DIR')

wxpdWxmap="%s/fldanal"%(W2BasePrcDir)
wxpdDat="%s/flddat"%(W2BasePrcDir)
wxpdHtml="%s/web"%(W2BasePrcDir)


#
# html
#

wxhWeb="%s/web"%(W2BaseDir)
wxhWeb="%s/web"%(W2BaseDir)
wxhWebPub="%s/wxmap2"%(os.getenv('W2_HFIP'))
wxhWebClm="%s/clm"%(wxhWeb)

#
# templates
#
htmMainTemplatePub="%s/template/wxmap.main.template.Pub.txt"%(wxhWebPub)

if(EcmModel == 'ecmn'):
    htmMainTemplate="%s/template/wxmap.main.template.ecmn.txt"%(wxhWeb)
else:
    htmMainTemplate="%s/template/wxmap.main.template.txt"%(wxhWeb)


TcPrcBaseDir='/home/fiorino/era/tc/prc'
TcStructPrcDir="%s/tcstruct"%(TcPrcBaseDir)

AtcfFtpserver='198.97.80.42'
AtcfLogin='atcfp1'
AtcfPasswd='atcfp112'
AtcfArchiveDir='/opt/DEVELOPMENT/atcfs'
AtcfStormDir='/opt/DEVELOPMENT/atcf/storms'


TcJtwcDatDir='/dat/nwp/dat/tc/jtwc'

TcDatDir='/dat/nwp/dat/tc'


TcAdecksNhcDir="%s/adeck/nhc"%(TcDatDir)
TcBdecksNhcDir="%s/bdeck/nhc"%(TcDatDir)
TcABdecksJtwcDir="%s/jtwc"%(TcDatDir)

TcCarqDir="%s/carq"%(TcDatDir)


#
# nhc
#

NhcFtpserver='ftp.nhc.noaa.gov'
NhcLogin='ftp'
NhcPasswd='fiorino@llnl.gov'

NhcDatDir='/pub/atcf'

#
# jma
#

JmaFtpserver='ddb.kishou.go.jp'
JmaIdir='/dat/nwp/dat'


NcepJtwcFtpserver='ftpprd.ncep.noaa.gov'
NcepJtwcIdir='/pcmdi/tenki_dat/nwp/dat'
NcepJtwcIdir='/dat/nwp/dat'
LdmQueueDir="%s/ldmqueue"%(NcepJtwcIdir)

FtpAlarmMins=45      # max number of minutes to wait before killing (hung) ftp
TimeSleepMaxHours=6  # max hours to sleep in hours
TimeSleepSecs=90     # time to sleep in sec
#TimeSleepSecs=10     # time to sleep in sec

wxmapbdir=os.environ['W2']

R1ClimoDatDir='/dat/windclimo/ac'
R1ClimoByear=1970
R1ClimoEyear=2000
R1ClimoNday=6


ClimoPlots=['200','500','700','850','sfc','shr','lmt']

if(EcmModel == 'ecmn'):
    wxModels=['gfs','fim','ngpc','ecmn','ukm']
elif(EcmModel == 'ecmg'):
    wxModels=['gfs','fim','ngpc','ecmg','ukm']
else:
    wxModels=['gfs','fim','ecm','ngp','ukm']
    wxModels=['gfs','fim','fimx','ecm','ukm']
    if(NgpModel == 'ngpc'): wxModels=['gfs','fim','ngpc','ecm','ukm']
    if(NgpModel == 'ngp2'): wxModels=['gfs','fim','ngp','ecm','ukm']



def ModelGrfDir(model,dtg):
    if(model == 'ngp'):
        gdir="%s/plt_fnmoc_ngp/%s"%(wxhWeb,dtg)
    elif(model == 'ocn'):
        gdir="%s/plt_fnmoc_ocn/%s"%(wxhWeb,dtg)
        gdir="%s/ocn10.sst.000.tropwpac.png"%(gdir)
    elif(model == 'gfs'):
        gdir="%s/plt_ncep_gfs/%s"%(wxhWeb,dtg)
    elif(model == 'fim'):
        gdir="%s/plt_esrl_fim/%s"%(wxhWeb,dtg)
    elif(model == 'fimx'):
        gdir="%s/plt_esrl_fimx/%s"%(wxhWeb,dtg)
    elif(model == 'ngpc'):
        gdir="%s/plt_fnmoc_ngpc/%s"%(wxhWeb,dtg)
    elif(model == 'gdl'):
        gdir="%s/plt_gfdl_gfl/%s"%(wxhWeb,dtg)
    elif(model == 'ukm'):
        gdir="%s/plt_ukmo_ukm/%s"%(wxhWeb,dtg)
    elif(model == 'ecm'):
        gdir="%s/plt_ecmwf_ecm/%s"%(wxhWeb,dtg)
    elif(model == 'ecmg'):
        gdir="%s/plt_ecmwf_ecmg/%s"%(wxhWeb,dtg)
    elif(model == 'ecmn'):
        gdir="%s/plt_ecmwf_ecm/%s"%(wxhWeb,dtg)
    elif(model == 'cmc'):
        gdir="%s/plt_cmc_cmc/%s"%(wxhWeb,dtg)
    elif(model == 'gsm'):
        gdir="%s/plt_jma_gsm/%s"%(wxhWeb,dtg)
    else:
        print 'EEEE invalid model: ',model
        sys.exit()

    return(gdir)

def ModelHtmDir(model,dtg):
    hdir="%s/web_%s/%s"%(wxhWeb,model,dtg)

    return(hdir)

    

def R1ClimoPrc(bdtg,edtg,uapath,vapath,verb=0,ndy=R1ClimoNday):

    cdir=R1ClimoDatDir
    byr=R1ClimoByear
    eyr=R1ClimoEyear

    odir=wxmapbdir+'/dat'
    
    dfile="clm.25.%s.dat"%(bdtg)
    cfile="clm.25.%s.ctl"%(bdtg)

    gtime=mf.dtg2gtime(bdtg)
    dtime=12
    nt=mf.dtgdiff(bdtg,edtg)/dtime + 1
    nt=int(nt)

    nlev=5
    levs="850 700 500 300 200"

    print "nt ",nt
    print "dtime ",dtime
    print "gtime ",gtime

    cpath=odir+"/%s"%(cfile)
    
    gs=[]

    g=gs.append

    g("function main(args)")

    g("rc=gsfallow('on')")
    g("rc=const()")
    g("verb=1")

    g("bdtg=%s"%(bdtg))
    g("edtg=%s"%(edtg))
    
    g("cbdtg='1970'%substr(bdtg,5,6)")
    g("cedtg='1970'%substr(edtg,5,6)")

    g("uapath='%s/ua.%s.%s.ac.365.ctl'"%(cdir,byr,eyr))
    g("vapath='%s/va.%s.%s.ac.365.ctl'"%(cdir,byr,eyr))

    g("uaspath='%s/uas.%s.%s.ac.365.ctl'"%(cdir,byr,eyr))
    g("vaspath='%s/vas.%s.%s.ac.365.ctl'"%(cdir,byr,eyr))

    g("opath='%s/%s'"%(odir,dfile))

    g("fu=ofile(uapath)")
    g("fv=ofile(vapath)")
    
    g("fus=ofile(uaspath)")
    g("fvs=ofile(vaspath)")

    g("levs='%s'"%levs)
    g("nl=%s"%nlev)

#    g("rc=uvclimo(fu,fv,'ua','va',%s,levs,nl,cbdtg,cedtg,opath)"%(ndy))
    g("rc=uvclimos(fu,fv,fus,fvs,'ua','va','uas','vas',%s,levs,nl,cbdtg,cedtg,opath)"%(ndy))

    g("'quit'")


    ctl=[]

    c=ctl.append

    c("dset ^%s"%(dfile))
    c("title 1970-2000 daily climo")
    c("undef 1e20")
    c("options big_endian")
    c("xdef 144 linear   0.0  2.5")
    c("ydef  73 linear -90.0  2.5")
    c("zdef  %s levels %s"%(nlev,levs))
    c("tdef  %s linear %s %shr"%(nt,gtime,dtime))

    c("vars 4")
    c("ua      %s 0 ua"%nlev)
    c("va      %s 0 va"%nlev)
    c("uas     0 0 uas")
    c("vas     0 0 vas")
    c("endvars")


    ctlfile=open(cpath,'w')

    for cc in ctl:
        cc=cc+'\n'
        print cc[:-1]
        ctlfile.write(cc)

    ctlfile.close()


    return(gs)


def SignalHandler(signum,frame):
    print 'Alarm went off'
    raise IOError, 'Host not responding'

def SetJmaData(dtg,model,source='jma'):

    hh=dtg[8:]
    yymmddhh=dtg[2:]
    
    ftpserver=JmaFtpserver
    if(source == 'pcmdi'):
        ftpserver='sprite.llnl.gov'
        
    idir=JmaIdir
    if(model == 'gsm'):
        if(source == 'jma'):
            sdir="/pub/DATA/jp034/g002f%s/%s"%(hh,yymmddhh)
            ifile="h*"
        
        dfile="%s.12.%s.grb"%(model,dtg)
        alldonepath="%s/alldone/alldone.%s.12.%s"%(idir,model,dtg)
        
    fipath="/tmp/f.jma.%s.%s.txt"%(model,dtg)
    fipathchk="/tmp/f.check.jma.%s.%s.txt"%(model,dtg)

    return(ftpserver,JmaIdir,sdir,ifile,dfile,fipath,fipathchk,alldonepath)


def SetNcepJtwcData(dtg,model,source='ncep'):

    ftpserver=NcepJtwcFtpserver
    if(source == 'pcmdi'):
        ftpserver='sprite.llnl.gov'
        
    idir=NcepJtwcIdir
    if(model == 'gfs'):
        if(source == 'ncep'):
            sdir='/pub/data2/JTWC/gfs'
            ifile="gfs.10.%s.jtwc_grb"%(dtg)
        else:
            sdir='/pub/fiorino/tmp'
            ifile="gfs.10.%s.grb"%(dtg)
            
        dfile="%s.10.%s.grb"%(model,dtg)
        alldonepath="%s/alldone/alldone.%s.10.%s"%(idir,model,dtg)
    elif(model == 'ukm'):
        if(source == 'ncep'):
            sdir='/pub/data2/JTWC/ukmet'
            ifile="ukmet.12.%s.jtwc_grb"%(dtg)
        else:
            sdir='/pub/fiorino/tmp'
            ifile="ukm.12.%s.grb"%(dtg)
        dfile="%s.12.%s.grb"%(model,dtg)
        alldonepath="%s/alldone/alldone.%s.12.%s"%(idir,model,dtg)
        
    fipath="/tmp/f.ncep.jtwc.%s.%s.txt"%(model,dtg)
    fipathchk="/tmp/f.check.ncep.jtwc.%s.%s.txt"%(model,dtg)

    return(ftpserver,NcepJtwcIdir,sdir,ifile,dfile,fipath,fipathchk,alldonepath)


def CheckNcepJtwcData(dtg,model,curpid):

    (ftpserver,idir,sdir,dfile,fipath,fipathchk,alldonepath)=SetNcepJtwcData(dtg,model)

    verb=0
    
    ftpcmds="""
cd %s
dir
quit"""%(sdir)

    fi=open(fipathchk,'w')
    fi.writelines(ftpcmds)
    fi.close()

    datathere=0
    
    cmd="ftp %s < %s"%(ftpserver,fipathchk)
    
    try:

        #
        # set alarm (timeout) of 30 s then continue
        #
        signal.signal(signal.SIGALRM,SignalHandler)
        nsecftpcheck=30
        signal.alarm(nsecftpcheck)
    
        cards=os.popen(cmd).readlines()

        
    except:

        signal.alarm(0)
        print 'DDDDDDDDD AAAAAAAAAAAAAAAAAA alarm went off ... ',datathere,dfile

        mf.KillPids(curpid)
        return(datathere)

    for card in cards:
        tt=card.split()
        if(len(tt) == 9):
            siz=tt[4]
            name=tt[8]
            time=tt[7]
            if(verb): print siz,time,name
            if(name.find(dtg) != -1):
                datathere=1


    cmd="rm %s"%(fipathchk) 
    mf.runcmd(cmd,'quiet')

    print 'DDDDDDDDD ',datathere,dfile
    return(datathere)



def CheckNcepJtwcData2(dtg,model,curpid):

    (ftpserver,idir,sdir,dfile,fipath,fipathchk,alldonepath)=SetNcepJtwcData(dtg,model)

    verb=1
    datathere=0
    timeout=0
    
    #cmd="ncftpls -t %s -l ftp://%s/%s/"%(timeout,ftpserver,sdir)
    cmd="t.ftpls.sh"
    rc=mf.getCommandOutput2(cmd)
    print 'rc ',rc
    return(datathere)
    
    cards=os.popen(cmd).readlines()
    rc=os.wait()
    print 'rc ',rc

    for card in cards:
        print card
        tt=card.split()
        if(len(tt) == 9):
            siz=tt[4]
            name=tt[8]
            time=tt[7]
            if(verb): print siz,time,name
            if(name.find(dtg) != -1):
                datathere=1
    
    return(datathere)
    


def ParseWgetOutput(cards):

    rc=-999
    for card in cards:
        if(card.find('No such file') > 0):
            print 'WWGGEETT nojoy: ',card[:-1]
            rc=0
        if(card.find('saved [') > 0):
            tt=card.split('[')
            nbytes=tt[1].split(']')[0]
            print 'WWGGEETT  saved: ',card[:-1]
            print 'WWGGEETT nbytes: ',nbytes
            
            if(int(nbytes) == 0):
                rc=-1
            else:
                rc=1

    return(rc)



def GetWxmapDtgs(curdtg,verb=1):

    dtgs={}
    models=wxModels
    models.append('gsm')
    print models

    for model in models:

        tdtg=curdtg
        ok=0
        n=0
        nmax=8
        while(ok == 0 and n < nmax):
            tdir=ModelHtmDir(model,tdtg)
            tdir=ModelGrfDir(model,tdtg)
            chkmethod=os.path.isdir
            if(model == 'ocn'): chkmethod=os.path.exists

            if(verb): print 'eeeeeeeeeeee ',model,tdir,tdtg
            if(chkmethod(tdir)):
                if(verb): print 'YYYY ',tdir,tdtg,n
                dtgs[model]=tdtg
                ok=1
            else:
                tdtg=mf.dtginc(tdtg,-6)
                n=n+1

            if(n >= nmax):
                dtgs[model]='----------'


    return(dtgs)


def HtmlWxmapMain(tdtg,curdtg,curphr,template,verb=0,dopublic=0):

    try:
        htm2=open(template,'r').read()
    except:
        print "EEEE unable to open template: %s"%(template)
        sys.exit()


    wxdtgs=GetWxmapDtgs(tdtg)

    if(EcmModel == 'ecmn'):
        dtgecm=wxdtgs['ecmn']
    elif(EcmModel == 'ecmg'):
        dtgecm=wxdtgs['ecmg']
    else:
        dtgecm=wxdtgs['ecm']


    if(verb):
        for d in wxdtgs.keys():
            print d,wxdtgs[d]



        
##     dtggfs=wxdtgs['gfs']
##     dtgngp=wxdtgs['ngp']
##     dtgukm=wxdtgs['ukm']
##     dtgecm=wxdtgs['ecm']
##     dtgcmc=wxdtgs['cmc']
##     dtgocn=wxdtgs['ocn']
##     dtggsm=wxdtgs['gsm']

##     createTxt="<b>Created: %s %s h</b>  GFS:%s  NGP:%s  UKM:%s  ECM:%s  CMC:%s  OCN:%s  "%(curdtg,curphr,
##                                                                                            dtggfs[6:],
##                                                                                            dtgngp[6:],
##                                                                                            dtgukm[6:],
##                                                                                            dtgecm[6:],
##                                                                                            dtgcmc[6:],
##                                                                                            dtgocn[6:])

    dtggfs=wxdtgs['gfs']
    dtgfim=wxdtgs['fim']
    #dtgfimx=wxdtgs['fimx']
    
    if(NgpModel == 'ngpc'):
        dtgngp=wxdtgs['ngpc']
    if(NgpModel == 'ngp2'):
        dtgngp=wxdtgs['ngp']
        
    dtgukm=wxdtgs['ukm']
    
    #createTxt="<b>Created: %s %s h</b>  GFS:%s  FIM:%s   FIMX:%s  %s:%s UKM:%s "%(curdtg,curphr,
    #                                                                            dtggfs[6:],
    #                                                                            dtgfim[6:],
    #                                                                            dtgfimx[6:],
    #                                                                            EcmModel.upper(),
    #                                                                            dtgecm[6:],
    #                                                                            dtgukm[6:],
    #                                                       )

    if(dopublic):
        createTxt="<b>Created: %s %s h</b>  GFS:%s  FIM:%s  %s:%s "%(curdtg,curphr,
                                                                                      dtggfs[6:],
                                                                                      dtgfim[6:],
                                                                                      NgpModel.upper(),dtgngp[6:],
                                                                                      )

    else:
        createTxt="<b>Created: %s %s h</b>  GFS:%s  FIM:%s  %s:%s  %s:%s UKM:%s "%(curdtg,curphr,
                                                                                      dtggfs[6:],
                                                                                      dtgfim[6:],
                                                                                      NgpModel.upper(),dtgngp[6:],
                                                                                      EcmModel.upper(),
                                                                                      dtgecm[6:],
                                                                                      dtgukm[6:],
                                                                                      )

    
    htm1=""" <html> <head> <title> %s WxMAP2 </title>
<link rel="shortcut icon" href="favicon.ico">
<link rel="stylesheet" type="text/css" href="css/wxmain.css">
<link rel="stylesheet" type="text/css" href="css/dropdown.css">

</head>

<body background="icon/wxmap.bkg.2.gif" TEXT="#000000" LINK="#0000FF" VLINK="#006030">

<script type=\"text/javascript\">
//Contents for menu 1
var menuusnsat=new Array()

menuusnsat[0]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.troplant\\'),loadW2Html(cvalue,\\'window\\');">nrl-troplant</a>'
menuusnsat[1]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.tropepac\\'),loadW2Html(cvalue,\\'window\\');">nrl-tropepac</a>'
menuusnsat[2]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.tropwpac\\'),loadW2Html(cvalue,\\'window\\');">nrl-tropwpac</a>'
menuusnsat[3]='<a href="javascript:cvalue=getW2Url(\\'usn.sat.nfmc-jtwc\\'),loadW2Html(cvalue,\\'window\\');">nmfc-jtwc</a>'

//menuusnsat[2]='<a href="">tropwpac</a>'

var menucira=new Array()
menucira[0]='<a href="javascript:cvalue=getW2Url(\\'cira.tc\\'),loadW2Html(cvalue,\\'window\\');">tc-rammb</a>'
menucira[1]='<a href="javascript:cvalue=getW2Url(\\'cira.tc.vigh\\'),loadW2Html(cvalue,\\'window\\');">tc-vigh</a>'
menucira[2]='<a href="javascript:cvalue=getW2Url(\\'cira.tcfa\\'),loadW2Html(cvalue,\\'window\\');">tcfa</a>'
menucira[3]='<a href="javascript:cvalue=getW2Url(\\'cira.prw\\'),loadW2Html(cvalue,\\'window\\');">prw</a>'

var menussd=new Array()
menussd[0]='<a href="javascript:cvalue=getW2Url(\\'ssd.troplant.vis\\'),loadW2Html(cvalue,\\'window\\');">troplant vis</a>'
menussd[1]='<a href="javascript:cvalue=getW2Url(\\'ssd.troplant.ir\\'),loadW2Html(cvalue,\\'window\\');">troplant ir</a>'
menussd[2]='<a href="javascript:cvalue=getW2Url(\\'ssd.tropepac.vis\\'),loadW2Html(cvalue,\\'window\\');">tropepac vis</a>'
menussd[3]='<a href="javascript:cvalue=getW2Url(\\'ssd.tropepac.ir\\'),loadW2Html(cvalue,\\'window\\');">tropepac ir</a>'

var menucimss=new Array()

menucimss[0]='<a href="http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/global2/main.html">global prw</a>'
menucimss[1]='<a href="http://cimss.ssec.wisc.edu/tropic2/real-time/imagemain.php?&basin=atlantic&prod=irn&sat=g8">images</a>'
menucimss[2]='<a href="http://cimss.ssec.wisc.edu/tropic2/real-time/windmain.php?&basin=atlantic&sat=wg8&prod=wvir&zoom=&time=">winds - lant</a>'
//menucimss[0]='<a href="">troplant vis</a>'

var menucpc=new Array()
menucpc[0]='<a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml">enso</a>'
menucpc[1]='<a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo.shtml">mjo</a>'
menucpc[2]='<a href="http://www.cpc.ncep.noaa.gov/products/hurricane/">hurricanes</a>'
menucpc[3]='<a href="http://www.cpc.ncep.noaa.gov/products/Global_Monsoons/Global-Monsoon.shtml">monsoons</a>'

var menufim=new Array()
menufim[0]='<a href="javascript:cvalue=getW2Url(\\'gsd.fim8.wxmap\\'),loadW2Html(cvalue,\\'window\\');">FIM8 30km (gsd)</a>'
menufim[1]='<a href="javascript:cvalue=getW2Url(\\'gsd.fim9.wxmap\\'),loadW2Html(cvalue,\\'window\\');">FIM9 15km (tacc)</a>'

//menucpc[0]='<a href="">troplant vis</a>'


</script>


<script language="javascript" src="js/dropdown.js" type="text/javascript"></script>
<script language="javascript" src="js/wxmain.js" type="text/javascript"></script>

<script language="javascript">
dtgcur='%s';
dtggfs='%s';
dtgfim='%s';
dtgngp='%s';
dtgecm='%s';
dtgecmn='%s';
dtgecmg='%s';
dtgukm='%s';

</script>





<table class="main" cellspacing=1 cellpadding=1 border=0>
<tr>
<td class='title'>
%s WxMAP2 - %s
</td>
</tr>

<tr>
<td class='status'>
%s
</td>
</tr>"""%(WxmapCenter,tdtg,dtggfs,dtgfim,dtgngp,dtgecm,dtgecm,dtgecmg,dtgukm,WxmapCenter,tdtg,createTxt)



    htm=htm1+htm2


    return(htm)


    


def HtmlCurClimo(dtg,path,area,otherarea):

    htm="""
<html>
<head>
<title>
Current Wind Climo - %s for: %s
</title>

<link rel="stylesheet" type="text/css" href="css/tdo.css">

</head>

<body text="black" link="blue" vlink="purple" onLoad="swap()">

<!--  tc tooltip text -->
<script language="JavaScript1.2" src="js/tdotips.js" type="text/javascript"></script>

<script language="javascript">

mainpage='.';
clmroot=mainpage + '/web_clm';
clmroot='.';
htype='main';
area='%s';
otherarea='%s';

model="gfs";
dtg="%s";

dtype="clm";
plevel="sfc";
ptype="loop";
ctype='chk';

function swap() 
{

if(model == 'gfs') {
  plotdir="../plt_ncep_gfs";
} else if(model == 'fim') {
  plotdir="../plt_esrl_fim";
} else if(model == 'fimx') {
  plotdir="../plt_esrl_fimx";
} else if (model == 'ngpc') {
  plotdir="../plt_fnmoc_ngpc";
} else if (model == 'ukm') {
  plotdir="../plt_ukmo_ukm";
} else if (model == 'ecm') {
  plotdir="../plt_ecmwf_ecm";
} else if (model == 'cmc') {
  plotdir="../plt_cmc_cmc";
}

value=plotdir + "/" + dtg + "/" + model + "." + dtype + "." + plevel + "." + dtg + "." + area + "." + ptype + ".png";
valueloop=value;

if(ptype == 'loop' && ctype != 'mod.chk') {
  valueloop= plotdir + "/" + dtg + "/" + model + "." + dtype + "." + plevel + "." + dtg + "." + area + "." + ptype + ".gif";
  value=valueloop;
} else if(ptype == 'loop' && ctype == 'mod.chk') {
  ptype='mod'
  value=plotdir + "/" + dtg + "/" + model + "." + dtype + "." + plevel + "." + dtg + "." + area + "." + ptype + ".png";
  valueloop=value;
}

myUrl=valueloop;
if (value != '') if (document.images) {
  document.images.myImage.src = valueloop;
  document.images.myImage.alt = valueloop;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
}

}



function swaphtm() 
{
  if(htype == 'main') {
    value='../.';
  } else if (htype == 'cur.clm') {
    value=clmroot + '/' + 'wx.clm.cur.' + area + '.htm';
  } else if (htype == 'area') {
    value=mainpage + '/' + model + '.' + area + '.' + dtg + '.htm';
  } else if (htype == 'mjo.850') {
    value='http://www.bom.gov.au/bmrc/clfor/cfstaff/matw/maproom/RMM/hov.recon.olr.u850.gif'
  } else {
    value=mainpage + '/' + model + '.' + area + '.' + dtg + '.htm';
  }
  parent.location.href=value;
}


</script>

<!-- NNNNNNNNNNNNNNNNNNNN new head -->

<table class="models" cellspacing=0 cellpadding=0 border=0>

<tr>

<td class='title'>
<i>%s</i> Current Wind Climo - %s - Model v NCEP R1
</td>


<td class='btntop' 
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['%s'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['%s'][1])" >
<input type='button' class='btntop' style="background-color: gold ; color: navy"
value='%s' name="tctrk"  onClick="htype='cur.clm';area=otherarea,swaphtm();">
</td>

<td class='btntop' 
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['wxmap'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['wxmap'][1])" >
<input type='button' class='btntop' style="background-color: gold ; color: navy"
value='WxMAP Home' name="tctrk"  onClick="htype='main',swaphtm();">
</td>



<td class='btntop'
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['mo.clm'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['mo.clm'][1])" >
<input type='button' class='btntop' style="background-color: gold ; color: navy"
value='Mon Climo' name="tctrk"  onClick="htype='mo.clm',swaphtm();">
</td>


<td class='btntop'
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['mjo.850'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['mjo.850'][1])" >
<input type='button' class='btntop' style="background-color: navy ; color: gold"
value='BOM MJO' name="tctrk"  onClick="htype='mjo.850',swaphtm();">
</td>

</tr>
</table>

<!-- ***************** table with track and stm buttons -->


<table  cellspacing=0 cellpadding=0 border=0 >

<!-- ***************** col1 -- image -->
<td valign=top>
<a name="link" href="myUrl" target="_blank"><img name="myImage"></a>
</td>



<!-- ***************** col2 -- TCs lant/epac -->
<td valign=top class='khaki'>

<table class="btncolv">

<form>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['clm-mod'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['clm-mod'][1])" >
<input type='button' class='btnsml' style="background-color: #ADD8E6"
value='LOOP' name="tctrk"  onClick="ptype='loop';ctype='chk',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['clm'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['clm'][1])" >
<input type='button' class='btnsml' style="background-color: #ADD8E6"
value='Climo' name="tctrk"  onClick="ptype='clm',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['mod'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['mod'][1])" >
<input type='button' class='btnsml' style="background-color: #ADD8E6"
value='Model' name="tctrk"  onClick="ptype='mod',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['ano'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['ano'][1])" >
<input type='button' class='btnsml' style="background-color: #ADD8E6"
value='Anom' name="tctrk"  onClick="ptype='ano',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['200'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['200'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='200' name="tctrk"  onClick="plevel='200',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['500'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['500'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='500' name="tctrk"  onClick="plevel='500',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['700'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['700'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='700' name="tctrk"  onClick="plevel='700',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['850'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['850'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='850' name="tctrk"  onClick="plevel='850',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['sfc'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['sfc'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='Sfc' name="tctrk"  onClick="plevel='sfc',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['shr'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['shr'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='SHR' name="tctrk"  onClick="plevel='shr',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=CLIMO['lm'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(CLIMO['lm'][1])" >
<input type='button' class='btnsml' style="background-color: Lightgreen"
value='L-M' name="tctrk"  onClick="plevel='lmt',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['gfs'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(MODEL['gfs'][1])" >
<input type='button' class='btnsml' style="background-color: Lightyellow"
value='GFS' name="tctrk"  onClick="ctype='mod.chk';model='gfs',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['gfs'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(MODEL['fim'][1])" >
<input type='button' class='btnsml' style="background-color: Lightyellow"
value='FIM8' name="tctrk"  onClick="ctype='mod.chk';model='fim',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['ngp'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(MODEL['ngp'][1])" >
<input type='button' class='btnsml' style="background-color: Lightyellow"
value='NGP' name="tctrk"  onClick="ctype='mod.chk';model='ngpc',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['ecm'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(MODEL['ecm'][1])" >
<input type='button' class='btnsml' style="background-color: Lightyellow"
value='ECM' name="tctrk"  onClick="ctype='mod.chk';model='ecm',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['ukm'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(MODEL['ukm'][1])" >
<input type='button' class='btnsml' style="background-color: Lightyellow"
value='UKM' name="tctrk"  onClick="ctype='mod.chk';model='ukm',swap();">
</td></tr>

<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=MODEL['cmc'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(MODEL['cmc'][1])" >
<input type='button' class='btnsml' style="background-color: Lightyellow"
value='CMC' name="tctrk"  onClick="ctype='mod.chk';model='cmc',swap();">
</td></tr>





</form>
</table>
</td>

</table>

<script language="JavaScript" type="text/javascript" src="js/wz_tooltip.js"></script>
</body>
</html>"""%(dtg,area.upper(),area,otherarea,dtg,area.upper(),dtg,otherarea,otherarea,otherarea.upper())

    mf.WriteCtl(htm,path)

    



    
