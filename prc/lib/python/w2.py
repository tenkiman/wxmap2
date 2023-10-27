from M import *

from w2local import *
from w2switches import *

W2TmpPrcDirPrefix='/tmp/PRC.W2PLOT'


#from w2html import *

#
# w2env 
#

W2_MODELS_GRF_EXT='10'


#
# wxmap1
#

Wxmap1Center='ESRL/GSD'

Wxmap1BaseDir='/dat/nwp/wxmap'
WebBdirWxmap1='/dat/nwp/wxmap/web'
NwpDataBdirWxmap1='/dat/nwp/dat'
PzalWxmap1BaseDir='/tdocommon/wxmap'
GeoDir='/dat/nwp/dat/geog'
NwpDataBdirWxmap1Hpss='/home/xaw/u9508'

wxpdWxmap1="%s/prc/wxmap"%(Wxmap1BaseDir)
wxpdDat1="%s/prc/dat"%(Wxmap1BaseDir)
wxpdHtml1="%s/prc/html"%(Wxmap1BaseDir)
wxdFtp1="%s/ftp"%(Wxmap1BaseDir)
wxhWeb1="%s/web"%(Wxmap1BaseDir)
wxhWebClm1="%s/clm"%(wxhWeb1)

W1DatLocalDir='/dat/nwp/dat'

#
# templates
#
htmMainTemplate="%s/template/main.template.txt"%(wxhWeb1)


#22222222222222222222222222222222222222222222222222222222222222222222222222222222222

W2Center=os.getenv('W2CENTER')
W2CenterFullName=W2Center

W2Dir=os.getenv('W2')
W2BaseDir=os.getenv('W2_BDIR')
W2BaseDirDat=os.getenv('W2_BDIRDAT')
W2BaseDirApp=os.getenv('W2_BDIRAPP')
W2BaseDirBin=os.getenv('W2_BDIRBIN')
W2BaseDirPlt=os.getenv('W2_BDIRPLT')
W2BaseDirWeb=os.getenv('W2_BDIRWEB')
W2BaseDirEvt=os.getenv('W2_BDIREVT')
W2BaseDirLog=os.getenv('W2_BDIRLOG')


#
# w2 web regen
#
W2RegenDir='/data/amb/projects/wxmap2a'
W2RegenBaseDirWeb="%s/web"%(W2RegenDir)

AppBdirW2=W2BaseDirApp
BinBdirW2=W2BaseDirBin
SrcBdirW2=W2BaseDir+'/src'
PrcBdirW2=W2BaseDir+'/prc'
PrcCfgBdirW2=PrcBdirW2+'/cfg'
DatBdirW2=W2BaseDirDat
EvtBdirW2=W2BaseDirEvt

W2BaseDirDat2='/data/wxmap2/dat'
W2BaseDirDat2='/storage2/kishou/wxmap2/dat'
##### 20080831 - shift to storage2; usb2 disk failed
W2BaseDirDat2='/storage4/kishou/wxmap2/dat'
W2BaseDirDat2='/wxmap2/dat2'
W2BaseDirDat2='/dat2'

DatBdirW2data=W2BaseDirDat2

LogBdirW2='/ptmp'
PrwLoopTmpDir='/ptmp/prw'

GradsBdirW2=AppBdirW2+'/grads'
GradsGslibDir=GradsBdirW2+'/gslib'

NwpDataBdirW2=DatBdirW2


#pppppppppppppppppppppppppppppppppppppppppppp
# /public/ - esrl

EsrlPublicDirFim='/public/data/fsl/fim/tracker'
EsrlPublicDirFim9='/public/data/fsl/fim/tracker'


#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# wjet

WjetScpServer='jetscp.rdhpcs.noaa.gov'
####WjetQmorphDir='/lfs2/projects/fim/fiorino/dat/qmorph'
####WjetRtfim='/lfs2/projects/rtfim'
WjetQmorphDir='/lfs1/projects/fim/fiorino/dat/qmorph'
WjetRtfim='/lfs1/projects/rtfim'

#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
# ranger.tacc.utexas.edu

TaccUser='mfiorino'
TaccServer='ranger.tacc.utexas.edu'
TaccFim9Gfs='/scratch/01033/harrop/FIM/FIMrun'
TaccFim9EnKF='/scratch/01033/harrop/FIM_ens/FIMrun'
TaccFim8EnKF='/scratch/01033/harrop/FIM_ens/FIMrun'
TaccFim10kmEnKF='/scratch/01033/harrop/FIM_10km/FIMrun'
TaccTcvitals='/work/01233/mfiorino/w21/dat/tc/tcvitals'
TaccMfAdecks='/work/01233/mfiorino/w21/dat/tc/adeck/tacc/2009'


Nwp2DataBdir='/storage2/nwp2'
Nwp2DataBdir='/storage3/nwp2'
Nwp2DataBdir="%s/nwp2"%(W2BaseDirDat)

Nwp2DataArchiveBdirLocal='/storage0/nwp2'
Nwp2DataArchiveBdirLocal10='/storage10/nwp2'
Nwp2DataArchiveBdirLocal11='/storage11/nwp2'
Nwp2DataArchiveBdirSnap='/storage4/nwp2'

Nwp2DataMassStore='/mss/jet/projects/fim/fiorino/nwp2'
NwpDataMassStore='/mss/jet/projects/fim/fiorino/nwp'
RtfimDataMassStore='/mss/jet/projects/fim/fiorino/rtfim'


GeogDatDirW2="%s/geog"%(DatBdirW2)

PrcDirTcdatW2="%s/tcdat"%(PrcBdirW2)
PrcDirTcbogW2="%s/tcbog"%(PrcBdirW2)
PrcDirTcpltW2="%s/tcplt"%(PrcBdirW2)
PrcDirTcww3W2="%s/tcww3"%(PrcBdirW2)
PrcDirWebW2="%s/web"%(PrcBdirW2)
PrcDirWxmap2W2="%s/wxmap2"%(PrcBdirW2)
PrcDirTcanalW2="%s/tcanal"%(PrcBdirW2)
PrcDirTctrkW2="%s/tctrk"%(PrcBdirW2)
PrcDirTcepsW2="%s/tcdat"%(PrcBdirW2)
PrcDirTcfiltW2="%s/tcfilt"%(PrcBdirW2)
PrcDirTcclimoW2="%s/tcclimo"%(PrcBdirW2)

PrcDirWebW2="%s/web"%(PrcBdirW2)

PrcDirFlddatW2="%s/flddat"%(PrcBdirW2)
PrcDirFlddatHwrfW2="%s/hwrf"%(PrcBdirW2)
PrcDirFldanalW2="%s/fldanal"%(PrcBdirW2)

FtpIncomingDir='/pcmdi/ftp_incoming/fiorino'

AtcfFtpserver='198.97.80.42'
AtcfLogin='atcfp1'
AtcfPasswd='atcfp112'
AtcfArchiveDir='/opt/DEVELOPMENT/atcf/archives'
AtcfStormDir='/opt/DEVELOPMENT/atcf/storms'


TcDatDir="%s/tc"%(W2BaseDirDat)
TcDatDir2="%s/tc"%(W2BaseDirDat2)


WdriveFtpBaseDir='/wdrive/FTP/users/fiorino'

TcAdecksXfr2AtcfDir="%s/adeck/xfr2atcf"%(TcDatDir)

TcRefTrkDatDir="%s/reftrk"%(TcDatDir)

TcAdecksNhcDir="%s/adeck/nhc"%(TcDatDir)
TcAdecksJtwcNhcDir="%s/adeckjtwc/nhc"%(TcDatDir)
TcBdecksNhcDir="%s/bdeck/nhc"%(TcDatDir)
TcStormsNhcDir="%s/nhc"%(TcDatDir)
TcComNhcDir="%s/com/nhc"%(TcDatDir)
TcStextNhcDir="%s/stext/nhc"%(TcDatDir)

TcABdecksJtwcDir="%s/jtwc"%(TcDatDir)
TcAdecksJtwcDir="%s/adeck/jtwc"%(TcDatDir)
TcBdecksJtwcDir="%s/bdeck/jtwc"%(TcDatDir)
TcStormsJtwcDir="%s/jtwc"%(TcDatDir)
TcComJtwcDir="%s/com/jtwc"%(TcDatDir)

TcBdecksNeumannDir="%s/bdeck/neumann"%(TcDatDir)
TcStormsNeumannDir="%s/neumann"%(TcDatDir)

TcBdecksHurdatDir="%s/bdeck/hurdat"%(TcDatDir)
TcStormsHurdatDir="%s/hurdat"%(TcDatDir)

TcAdecksLocalDir="%s/adeck/local"%(TcDatDir)
TcAdecksEcmwfDir="%s/adeck/ecmwf"%(TcDatDir)
TcAdecksMitDir="%s/adeck/mit"%(TcDatDir)
TcAdecksTcepsDir="%s/adeck/tceps"%(TcDatDir)
TcAdecksuKmoDir="%s/adeck/ukmo"%(TcDatDir)
TcAdecksNcepDir="%s/adeck/ncep"%(TcDatDir)
TcAdecksCmcDir="%s/adeck/cmc"%(TcDatDir)
TcAdecksEsrlDir="%s/adeck/esrl"%(TcDatDir)
TcAdecksGfsenkfDir="%s/adeck/esrl"%(TcDatDir)
TcAdecksTaccDir="%s/adeck/tacc"%(TcDatDir)
TcAdecksJmaDir="%s/adeck/jma"%(TcDatDir)
TcAdecksFnmocDir="%s/adeck/jtwc"%(TcDatDir)

HfipBaseDir="/dat2/hfip/web"
HfipHttpInternetDocRoot=os.getenv('W2_HFIP')
HfipProducts=os.getenv('W2_HFIP')



#tttttttccccccc
# tceps
#


TcBaseDirPltTc=W2BaseDirPlt+"/tc"

TcPltEcmwfDir=TcBaseDirPltTc+"/ecmwf"
TcPltEcmwfEpsDir=TcBaseDirPltTc+"/ecmwf_eps"

TcTcepsEcmwfDir="%s/tceps/ecmwf"%(TcDatDir)
TcTcepsuKmoDir="%s/tceps/ukmo"%(TcDatDir)
TcTcepsNcepDir="%s/tceps/ncep"%(TcDatDir)
TcTcepsCmcDir="%s/tceps/cmc"%(TcDatDir)
TcTcepsEsrlDir="%s/tceps/esrl"%(TcDatDir)
TcTcepsGfsenkfDir="%s/tceps/gfsenkf"%(TcDatDir)
TcTcepsFnmocDir="%s/tceps/fnmoc"%(TcDatDir)

TcTcepsEcmwfNmembers=51
TcTcepsuKmoNmembers=24
# -- 20220925 now 31 vice 21
TcTcepsNcepNmembers=31
TcTcepsCmcNmembers=21
TcTcepsEsrlNmembers=21
TcTcepsGfsenkfNmembers=20
TcTcepsFimensNmembers=20
TcTcepsFnmocNmembers=20

TcTcepsDatDirRT="%s/tceps"%(TcDatDir)
TcTcepsDatDir="%s/tceps"%(TcDatDir2)
TcTcepsDatDirTail="dat/tc/tceps"
TcTcepsWebDir="%s/tceps"%(HfipBaseDir)

# direct write to webserver dir
if(W2doW3RapbRsync == 0): TcTcepsWebDir="%s/tceps"%(HfipProducts)

TcTcepsWebDirKishou="%s/tceps"%(HfipBaseDir)

TcTcanalDatDirRT="%s/tcanal"%(TcDatDir)
TcTcanalDatDir="%s/tcanal"%(TcDatDir2)
TcTcanalDatDirTail="dat/tc/tcanal"
TcTcanalWebDir="%s/tc/tcanal"%(W2BaseDirWeb)


TcAtcfDatDir="%s/atcf"%(TcDatDir)
TcBtDatDir="%s/bt"%(TcDatDir)
TcBtNeumannDatDir="%s/btn"%(TcDatDir)
TcBtHurdatDatDir="%s/bth"%(TcDatDir)
TcBtOpsDatDir="%s/bto"%(TcDatDir)

TcTcfiltDatDirRT="%s/tcfilt"%(TcDatDir)
TcTcfiltDatDir="%s/tcfilt"%(TcDatDir2)
TcTcfiltDatDirTail="dat/tc/tcfilt"
TcTcfiltWebDir="%s/tc/tcfilt"%(W2BaseDirWeb)
TcTcfiltWdriveWebDir="%s/tc/tcfilt"%(W2BaseDirWeb)

TcTcWW3WebDir="%s/tc/tcww3"%(W2BaseDirWeb)

TceBtCsuDatDir="%s/ebt"%(TcDatDir)

TcCimssWindRadiiDir="%s/cimss"%(TcDatDir)
TccBtCimssDatDir="%s/cbt"%(TcDatDir)

TcClimoDatDir="%s/climo"%(TcDatDir)
TcCarqDatDir="%s/carq"%(TcDatDir)
TcNamesDatDir="%s/names"%(TcDatDir)

TcAdecksFinalDir="%s/adeck"%(TcDatDir)
TcBdecksFinalDir="%s/bdeck"%(TcDatDir)
TcMdecksFinalDir="%s/mdeck"%(TcDatDir)

TcStatusLogDir="%s/tcstatus"%(W2BaseDirLog)
TcAdeckLogDir="%s/adeck"%(W2BaseDirLog)
TcBdeckLogDir="%s/bdeck"%(W2BaseDirLog)
TcMdeckLogDir="%s/mdeck"%(W2BaseDirLog)

TcTcbogDatDir="%s/tcbog"%(TcDatDir)

TcTiggeDatDir="%s"%(TcDatDir)

#cccccccccccccccccccccccccccccccccccccccccccccccccc
# cira MTCSWA -- multi-platform tropical cyclone surface wind analysis
#
TcMtcswaFtpServer='satepsanone.nesdis.noaa.gov'
TcMtcswaFtpDatDir='MTCSWA'
TcMtcswaFtpLogin='ftp'
TcMtcswaFtpPasswd="michael.fiorino"
TcMtcswaDatDir="%s/cira/mtcswa"%(TcDatDir)

TcMtcswaLateFtpServer='rammftp.cira.colostate.edu'
TcMtcswaLateFtpDatDir='knaff/MPSW_LATE'
TcMtcswaLateFtpLogin='ftp'
TcMtcswaLateFtpPasswd="michael.fiorino"
TcMtcswaLateDatDir="%s/cira/mtcswa_Late"%(TcDatDir)

#
#  nhc web
#

NhcHttpIntranetServerSkate='skate.nhc.noaa.gov'
NhcHttpIntranetDocRootSkate='/www/mfiorino/public_html'
NhcHttpuserSkate='mfiorino'

DoDogfishRsync=1
NhcHttpIntranetServerDogfish='dogfish.nhc.noaa.gov'
NhcHttpIntranetDocRootDogfish='/data/www/html/mfiorino'
NhcHttpuserDogfish='mfiorino'

#
#  jtwc web
#

JtwcHttpIntranetServer='138.163.146.36'
JtwcHttpIntranetDocRoot='/dat/nwp'
JtwcHttpuser='fiorino'

#
#  esrl web
#

EsrlHttpInTranetserver='brain.fsl.noaa.gov'
EsrlHttpIntranetDocRoot='/w3/rapb/wxmap2/'
EsrlHttpIntranetDocRoot='%s/wxmap2/'%(HfipProducts)
EsrlHttpIntranetDocRootFiorino='/w3/rapb/fiorino'
EsrlHttpuser='fiorino'

EsrlHttpInternetHfipDocRoot='/w3/rapb/hfip'
EsrlHttpInternetHfipEnkfDocRoot='/w3/rapb/hfip/enkf'
EsrlHttpInternetHfipEnkfDocRoot='%s/hfip/enkf'%(HfipProducts)
EsrlHttpInternetHfipFimadecksDocRoot='/w3/rapb/hfip/fimadecks'

EsrlHttpInTranetserver='brain.fsl.noaa.gov'
EsrlHttpIntranetDocRoot='%s/wxmap2/'%(HfipProducts)
EsrlHttpIntranetDocRoot='%s/wxmap2/'%(HfipProducts)
EsrlHttpIntranetDocRootFiorino='%s/hfip/fiorino'%(HfipProducts)
EsrlHttpuser='fiorino'

EsrlHttpInternetHfipDocRoot='%s/hfip'%(HfipProducts)
EsrlHttpInternetHfipEnkfDocRoot='%s/hfip/enkf'%(HfipProducts)
EsrlHttpInternetHfipEnkfDocRoot='%s/hfip/enkf'%(HfipProducts)
EsrlHttpInternetHfipFimadecksDocRoot='%s/hfip/fimadecks'%(HfipProducts)


LocalHttpDocRoot='/Library/WebServer/Documents/'

TcAdecksEcmwfDirW3="%s/tc/tceps/ecmwf"%(EsrlHttpIntranetDocRootFiorino)
TcAdecksuKmoDirW3="%s/tc/tceps/ukmo"%(EsrlHttpIntranetDocRootFiorino)
TcAdecksNcepDirW3="%s/tc/tceps/ncep"%(EsrlHttpIntranetDocRootFiorino)
TcAdecksJmaDirW3="%s/tc/tceps/jma"%(EsrlHttpIntranetDocRootFiorino)
TcAdecksCmcDirW3="%s/tc/tceps/cmc"%(EsrlHttpIntranetDocRootFiorino)
TcbogDirW3="%s/tc/tcvitals"%(EsrlHttpIntranetDocRootFiorino)
TcvitalsDirW3="%s/tc/tcvitals"%(EsrlHttpIntranetDocRootFiorino)
TcBdecksDirW3="%s/tc/bdecks"%(EsrlHttpIntranetDocRootFiorino)
TcAdecksDirW3="%s/tc/adecks"%(EsrlHttpIntranetDocRootFiorino)

wxhWebClm="%s/web_clm"%(W2BaseDirWeb)


#
# llnl
#
LlnlFtpServer='tenki.llnl.gov'

#
# jtwc
#
JtwcFtpserver='198.97.80.64'
#
# 20050126 - .64 turned off (wxamp0) on 20050124; change the new wxmap machine .60 (wxmap2)
#
JtwcFtpserver='198.97.80.60'

#
# 200604 - use atcfarch@ftp://pzal  vice wxmap2
#
JtwcFtpserver='pzal.npmoc.navy.mil'
JtwcFtpserver='pzal.ndbc.noaa.gov'

JtwcLogin='atcfarch'
JtwcPasswd='HAwA1150'
JtwcDatDir='/storms'


JtwcPzalAtcfServer='205.85.40.24'
JtwcPzalAtcfLogin='nhc'
JtwcPzalAtcfPasswd="Hurricane2**4"

#JtwcPzalAtcfServer='pzal.npmoc.navy.mil'
#JtwcPzalAtcfLogin='fnmoc'
#JtwcPzalatcfPasswd='8tcf5t0rmZ'

#
# 20060215 -- reconfig firewall
# 20060411 -- go with wxmap2 until pzal sorted
#
jtserv='https'
#jtserv='ftp'

if(jtserv == 'ftp'):

    JtwcFtpserver='pzal.npmoc.navy.mil'
    JtwcLogin='atcfarch'
    JtwcPasswd='HAwA1150'
    JtwcDatDir='/storms'

    JtwcService='ftp'
    JtwcFtpserver='199.10.200.62'
    JtwcLogin='fiorino'
    JtwcPasswd='tcad94'
    JtwcDatDir='/dat/nwp/dat/tc/jtwc'

else:

    JtwcService='https'
    JtwcFtpserver='pzal.ndbc.noaa.gov'
    JtwcLogin='fnmoc'
    JtwcPasswd='8tcf5t0rmZ'
    JtwcDatDir='/atcf_storms/storms'

    
PushTcstruct2Pzal=0

# -- kerry emanuel chips model

MitFtpserver='texmex.mit.edu'
MitLogin='ftp'
MitPasswd='michael.fiorino@noaa.gov'
MitDatDir='/pub/emanuel/JTWC'


#
# nhc
#

NhcFtpserver='ftp.nhc.noaa.gov'
NhcFtpserver='ftp.tpc.ncep.noaa.gov'

NhcLogin='ftp'
NhcPasswd='michael.fiorino@noaa.gov'
NhcDatDir='/pub/atcf'
NhcDatDir='/atcf'
NhcLocalAtcfDatDir='/mnt/users/atcf'

#-- ucar
#

HfipFtpserver='ftp.rap.ucar.edu'
HfipLogin='ftp'
HfipPasswd='michael.fiorino@noaa.gov'
HfipDatDir='/incoming/irap/hfip'

#-- final demo data
HfipFtpserver='www.rap.ucar.edu'
HfipLogin='hfipteam'
HfipPasswd='hfipteam'
HfipDatDir='/data/tcmt'


HfipLocalAtcfDatDir='/mnt/users/atcf'

HrdFtpserver='ftp.aoml.noaa.gov'
HrdLogin='ftp'
HrdPasswd='fiorino@llnl.gov'
HrdDatDir='/pub/hrd/gopal/tracks'
HrdHwindDatDir='/pub/hrd/hwind/carq/Operational'

EcmwfTiggeFtpserver='tigge-ldm.ecmwf.int'
EcmwfTiggeLogin='tigge'
EcmwfTiggePasswd='tigge'
EcmwfTiggeDatDir='/cxml'

uKmoTiggeFtpserver='ftp.metoffice.gov.uk'
uKmoTiggeLogin='nhc_tropc'
uKmoTiggePasswd='du7etexe'
uKmoTiggeDatDir='.'

NcepTiggeFtpserver='ftp.emc.ncep.noaa.gov'
NcepTiggeLogin='ftp'
NcepTiggePasswd='michael.fiorino@noaa.gov'
NcepTiggePasswd='mike'
NcepTiggeDatDir='/gmb/rwobus/tigge/beta/cxml'

CmcTiggeFtpserver='ftp.emc.ncep.noaa.gov'
CmcTiggeLogin='ftp'
CmcTiggePasswd='michael.fiorino@noaa.gov'
CmcTiggePasswd='mike'
CmcTiggeDatDir=NcepTiggeDatDir

#
# set on kishou by su
#
NhcLocalAtcfDatDir='/atcf'

NhcLocalAtcfOpsDatDir='/home/mfiorino/databases/atcf/storms'
NhcLocalAtcfOpsDatabaseDir='/home/mfiorino/databases/atcf/atcfdatabase'
NhcLocalAtcfOpsDatArchiveDir='/home/mfiorino/databases/atcf/archive'

# jtwc -- rsync mech to do a/b decks vice wget to pzal.nmci.navy.mil
#

JtwcWxmap2AtcfDatDir='/dat/nwp/dat/tc/jtwc'
# 20110713 -- nfs from wxmap1 -> 2 machine

JtwcWxmap2AtcfDatDir='/dat/rdata/tc/jtwc'
JtwcWxmap2AtcfEcmwfDatDir='/dat/nwp/dat/tc/ecmwf'

#
# jma
#

JmaFtpserver='ddb.kishou.go.jp'
JmaIdir='/dat/nwp/dat'


#
#  fnmoc
#

FnmocCagipsGridCacheDir='/gpfs6/cagips/cache/fnmoc/grid'
FnmocCagipsGridLocalDir='/home/dlaws/cagips_data'

#
#  nhc - cagips
#
NhcCagipsGridCacheDir='/gpfs6/cagips/cache/fnmoc/grid'
NhcCagipsGridLocalDir='/home/mfiorino/dat/cagips'

#
#  nhc - nawips
#
NhcNawipsGridCacheDir='/gpfs6/cagips/cache/fnmoc/grid'
NhcNawipsGridLocalDir='/mnt/model'
NhcNawipsGridLocalDir='/model'
NhcNawipsGridArchDir='/mnt/data_arch'
NhcNawipsGridArchTmpDir='/storage/data_arch'


#
# nhc -- model flds
#
NhcFldArchiveBase='/storage/dat/nwp'
#
# 20081202 -- shift to snap drives to disconnect local usb2 drives...
#
NhcFldArchiveBase='/storage3/dat/nwp'
NhcFldLiveBase='/storage2/nwp2'
#--------- 20070823 -- cut over to new snap drive
NhcFldLiveBase="%s/nwp2"%(W2BaseDirDat)

#
# nhc - ftp dirs
#

#
#  nhc - nco
#
NcoDcomDir='/dcom/us007003'
NcoGridLocalDir='/mnt/model'
NcoGridArchDir='/mnt/data_arch'


#
#  nhc - ukmo 
#
NhcFtpIncominguKmo='/users/naprod/model/ukmet_hr/downloads'
NhcFtpIncominguKmo='mfiorino@compute1:/home/naprod/model/ukmet_hr/downloads'
NhcTargetuKmo=NhcFldLiveBase+'/ukmo/ukm'

#
#  nhc - cpc qmorph rain 
#
PrDatRoot='/dat1/dat/pr'
CpcFtpQmorphServer='ftp.cpc.ncep.noaa.gov'
CpcFtpSourceDirQmorph='/precip/qmorph/30min_025deg/'

NhcFtpTargetDirQmorph='%s/qmorph/30min_025deg/incoming/'%(PrDatRoot)
NhcQmorphFinalLocal='%s/qmorph/30min_025deg/grib/'%(PrDatRoot)

NhcQmorphFinalSnap='/storage3/dat/qmorph/30min_025deg/grib/'
NhcQmorphProductsGrib='/dat1/model/pr_qmorph/grib'
NhcQmorphProductsGempak='/dat1/model/pr_qmorph/'
NhcQmorphProductsGempakNawips='/model/pr_qmorph/'

CpcFtpCmorphServer=CpcFtpQmorphServer
CpcFtpSourceDirCmorph='/precip/global_CMORPH/30min_025deg/'
#
# 20090605 -- tmp location for recovered cmorph gap 200905007-20090521
#
#CpcFtpSourceDirCmorph='/precip/qmorph/30min_025deg/'

NhcFtpTargetDirCmorph='/%s/cmorph/30min_025deg/incoming/'%(PrDatRoot)
NhcCmorphFinalLocal='/%s/cmorph/30min_025deg/grib/'%(PrDatRoot)

NhcCmorphFinalSnap='/storage3/dat/cmorph/30min_025deg/grib/'
NhcCmorphProductsGrib='/dat1/model/pr_cmorph/grib'
NhcCmorphProductsGempak='/dat1/model/pr_cmorph/'

#
# ncep
#


def GetNcepBaseInOutDat(center=W2Center.lower()):

    if(center == 'esrl'):
        NcepBaseOutDat=NhcFldLiveBase+'/ncep/OUTDAT'
        NcepBaseInDat=NhcFldLiveBase+'/ncep/com'
        NcepBaseFlddb="%s/FLDDB/ncep"%(W2BaseDirDat)
        NcepFldLiveBase=NhcFldLiveBase

    elif(center == 'ncep'):
        NcepBaseOutDat='/tpc/noscrub/OUTDAT'
        NcepBaseInDat='/com'
        NcepBaseFlddb="/tpc/noscrub/FLDDB/ncep"
        NcepFldLiveBase=NcepBaseOutDat+'/nwp2'

    return(NcepBaseInDat,NcepBaseOutDat,NcepBaseFlddb,NcepFldLiveBase)



def CagipsModelDir(model,center=W2Center.lower()):
    icodes=[]

    if(center == 'fnmoc'):

        if(model == 'ngp'):
            cdir=FnmocCagipsGridLocalDir
            icode='0058_0240'
            icodes.append(icode)
        elif(model == 'gfs'):
            cdir=FnmocCagipsGridLocalDir
            icode='0012_0240'
            icodes.append(icode)
        elif(model == 'ukm'):
            cdir=FnmocCagipsGridLocalDir
            icode='0118_0240'
            icodes.append(icode)
        elif(model == 'ocn'):
            cdir=FnmocCagipsGridLocalDir
            icode='0037_0240'
            icodes.append(icode)
            icode='0110_0240'
            icodes.append(icode)
        elif(model == 'ecm'):
            cdir=FnmocCagipsGridLocalDir
            icode='0048_0240'
            icodes.append(icode)
        elif(model == 'all'):
            cdir=FnmocCagipsGridLocalDir
            icode='_0240'
            icodes.append(icode)
        else:
            print 'EEEE invalid model: ',model,' for center: ',center,' sayoonara, o genki de!'
            sys.exit()

    elif(center == 'esrl'):

        if(model == 'ngp'):
            cdir=NhcCagipsGridLocalDir
            icode='0058_0240'
            icodes.append(icode)
        elif(model == 'ngp05'):
            cdir=NhcCagipsGridLocalDir
            icode='0058_0056'
            icodes.append(icode)
        elif(model == 'gfs'):
            cdir=NhcCagipsGridLocalDir
            icode='0012_0240'
            icodes.append(icode)
        elif(model == 'ukm'):
            cdir=NhcCagipsGridLocalDir
            icode='0118_0240'
            icodes.append(icode)
        elif(model == 'ocn'):
            cdir=NhcCagipsGridLocalDir
            icode='0037_0240'
            icodes.append(icode)
            icode='0110_0240'
            icodes.append(icode)
        elif(model == 'ecm'):
            cdir=NhcCagipsGridLocalDir
            icode='0048_0240'
            icodes.append(icode)
        elif(model == 'all'):
            cdir=NhcCagipsGridLocalDir
            icode='_0240'
            icodes.append(icode)
        else:
            print 'EEEE invalid model: ',model,' for center: ',center,' sayoonara, o genki de!'
            sys.exit()


    else:
        print 'EEEE invalid center: ',center,' sayoonara, o genki de!'
        sys.exit()

    return(cdir,icodes)



#
# nasa
#

NasaFtpserver='gmaoftp.gsfc.nasa.gov'
NasaLogin='ftp'
NasaPasswd='fiorino@llnl.gov'

NasaDatDir='/pub/data/dao_ops/map05'
W2DatNasaDir='/pcmdi/chico_dat/nwp/dat'

NasaFldFtpserver='sprite.llnl.gov'
NasaFldIdir='/var/ftp/incoming/fiorino'
NasaFldIdirPcmdi='/pcmdi/ftp_incoming/fiorino'

NcdcGdasFtpserver='nomads6.ncdc.noaa.gov'
NcdcGdasIdir='/pub/raid1a/gfs/amip'
NcdcGdasPcmdi='/dat/nwp/ncep/gdas'

NcepJtwcFtpserver='ftpprd.ncep.noaa.gov'
NcepJtwcIdir='/dat/nwp/dat'
NcepJtwcIdir='/dat/nwp/dat'
LdmQueueDir="%s/ldmqueue"%(NcepJtwcIdir)

FtpAlarmMins=45      # max number of minutes to wait before killing (hung) ftp
TimeSleepMaxHours=5  # max hours to sleep in hours
TimeSleepSecs=120    # time to sleep in sec


R1ClimoDatDir="%s/%s"%(W2BaseDirDat,'climo/ncepr1_daily_wind/ac')
R1ClimoByear=1970
R1ClimoEyear=2000
R1ClimoNday=6



MandatoryPressureLevels=[1000,925,850,700,500,400,300,250,200,150,100,70,50,30,20,10]
SynopticTimes=['00','06','12','18']

ClimoPlots=['200','500','700','850','sfc','shr','lmt']

wxModels=['gfs','ngp','ukm','ecm','cmc','ocn']
wxModels=['gfs','ngp','ukm','ecm','cmc']

Nwp2ModelsAll=['gfs2','fim8','ecm2','ukm2','ngp2','ecmn','cmc2','fimx','ngpc']
Nwp2ModelsAll=['gfs2','fim8','ecm2','ukm2','ngp2','ecmn','cmc2','ngpc','gfsk','ohc','ocn','ww3']
Nwp2Models=['gfs2','fim8','ecm2','ngp2','ukm2']
Nwp2Models=['gfs2','fim8','ecm2','fimx','ukm2','ngpc']
Nwp2Models=['gfs2','fim8','ecm2','ukm2','ngpc']
Nwp2Models=['gfs2','fim8','ecm4','ukm2','navg']  # -- 20170315 -- switch to ecm4 0.25 deg fields
Nwp2Models=['gfs2','fim8','ecm4','ukm2','navg','fv3e','fv3g']  # -- 20180111 -- deprecate fim8 and add two fv3 runs
#ch to ecm4 0.25 deg fields

if(NgpModel == 'ngp2'):
    Nwp2Models=['gfs2','fim8','ecm2','ukm2','ngp2']
    w2TcAnalModels=['gfs2','fim8','ecm2','ngp2','ukm2']
if(NgpModel == 'ngpc'):
    Nwp2Models=['gfs2','fim8','ecm2','ukm2','ngpc']
    w2TcAnalModels=['gfs2','fim8','ecm2','ngpc','ukm2']

wxModels2=Nwp2Models
wxModels2offtimes=['gfs2','ukm2','navg']

w2DatCagipsModels=['ngp','ocn','ohc','ww3','ngp05']
w2DatCagipsOnlyModels=['ocn','ohc','ww3','ngp05']
w2DatModels=wxModels+['ngp05']
w2DatModels=wxModels
w2PlotModels=copy.copy(wxModels)

w2PlotClmModels=['gfs2','fim8','ngpc','ecm2','ukm2']


def IsOffTime(dtg):
    dtghh=int(dtg[8:10])
    if(dtghh == 6 or dtghh == 18):
        return(1)
    else:
        return(0)


def ModelArchiveDirs(model,dtg,center='esrl'):

    yyyymm=dtg[0:6]
    ftpserver='hpss.nersc.gov'
    ftpserver='kishou.nhc.noaa.gov'
    ftpserver='share2'

    renmask=None
    modelrename=None
    modres=ModelRes(model)


    if(IsModel2(model)):

        localarchbase=Model2ArchiveDir(yyyymm)
        localarchdir=Nwp2DataBdirModel(model,bdir2=localarchbase)
        remotedir=localarchdir

        Model2DataPathsStatus(model,dtg)
        localdir=Nwp2DataBdirModel(model)
        modres=Model2Res(model)

        if(model == 'gfs2'):
            mask="gfs2.%s.*"%(dtg)

        elif(model == 'fim8'):
            mask="fim8.%s.*"%(dtg)

        elif(model == 'fimx'):
            mask="fimx.%s.*"%(dtg)

        elif(model == 'ngp2'):
            mask="ngp2.*%s.*"%(dtg)

        elif(model == 'ngpc'):
            mask="ngpc.*%s.*"%(dtg)

        elif(model == 'ukm2'):
            mask="ukm2.%s.*"%(dtg)

        elif(model == 'ecm2'):
            mask="ecmo.%s.*"%(dtg)

        elif(model == 'gfs2'):
            mask="gfs2.%s.*"%(dtg)

        elif(model == 'ecmn'):
            mask="ecmn.%s.*"%(dtg)

        elif(model == 'cmc2'):
            mask="cmc.%s.*"%(dtg)


    else:

        if(model == 'gfs'):
            remotedir="ncep/gfs/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="gfs.10.%s.*"%(dtg)

        elif(model == 'avn'):
            remotedir="ncep/avn/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="avn.10.%s.*"%(dtg)
            modelrename='gfs'
            renmask="%s.10.%s.*"%(modelrename,dtg)

        elif(model == 'gfs.jtwc'):
            remotedir="ncep/gfs/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="gfs.jtwc.10.%s.*"%(dtg)

        elif(model == 'ngp'):
            remotedir="fnmoc/ngp/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="ngp.10.*%s.*"%(dtg)

        elif(model == 'ngp05'):
            remotedir="fnmoc/ngp/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="%s.05.*%s.*"%(model,dtg)

        elif(model == 'ukm'):
            remotedir="ukmo/ukm/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="ukm.10.%s.*"%(dtg)

        elif(model == 'ocn'):
            remotedir="fnmoc/ocn/sst/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="ocn.10.*%s.*"%(dtg)

        elif(model == 'ww3'):
            remotedir="fnmoc/ocn/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="ocn.10.*%s.*"%(dtg)

        elif(model == 'ecm'):
            remotedir="ecmwf/ecm/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="ecm.10.%s.*"%(dtg)

        elif(model == 'cmc'):
            remotedir="cmc/cmc/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="cmc.10.%s.*"%(dtg)
#
# 20080908 -- fim global model from gsd and tacc 
#
        elif(model == 'fim8'):
            remotedir="esrl/fim8/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="fim8.%s.%s.*"%(modres,dtg)

        elif(model == 'fim9'):
            remotedir="gsd/fim8/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            mask="fim9.%s.%s.*"%(modres,dtg)

        elif(model == 'all'):
            remotedir="*/*/%s"%(yyyymm)
            localdir=NwpDataBdir(model)
            localarchbase=NhcFldArchiveBase
            localarchdir="%s/%s"%(localarchbase,remotedir)
            mask="*.%s.*"%(dtg)

        else:
            print 'EEEE invalid model in w2.ModelArchiveDir: ',model
            sys.exit()

        if(model != 'all'):
            localarchbase=NhcFldArchiveBase
            localarchdir="%s/%s"%(localarchbase,remotedir)


    if(ftpserver == 'share2'):
        remotedir="root/nwp/%s/%s"%(dtg[0:6],remotedir)

    return(ftpserver,remotedir,localdir,localarchdir,
           mask,renmask,modelrename)


def Dtg2Timei(dtg):
    timei=time.strptime(dtg,"%Y%m%d%H")
    return(timei)


def DeltaTimei(timei1,timei2):

    t1=time.mktime(timei1)
    t2=time.mktime(timei2)
    dt=(t1-t2)/3600.0
    return(dt)

def PathCreateTimeDtgdiff(dtg,path):

    timei=os.path.getctime(path)
    ctimei=time.gmtime(timei)
    dtimei=Dtg2Timei(dtg)

    dt=DeltaTimei(ctimei,dtimei)

    return(dt)

def PathModifyTimeDtgdiff(dtg,path,tzoff=0):

    timei=os.path.getmtime(path)
    ctimei=time.gmtime(timei)
    dtimei=Dtg2Timei(dtg)

    dt=DeltaTimei(ctimei,dtimei)+tzoff

    return(dt)

def PathModifyTimeCurdiff(path,tzoff=0):

    timei=os.path.getmtime(path)
    ptimei=time.gmtime(timei)
    ctimei=time.gmtime(time.time())

    dt=DeltaTimei(ptimei,ctimei)+tzoff

    return(dt)

def PathCreateTimeCurdiff(path,tzoff=0):

    timei=os.path.getctime(path)
    ptimei=time.gmtime(timei)
    ctimei=time.gmtime(time.time())

    dt=DeltaTimei(ptimei,ctimei)+tzoff

    return(dt)

#
# event logging
#

def EventPath(type,model,dtg,area):
    bdir="%s/%s"%(EvtBdirW2,dtg[0:6])
    mf.ChkDir(bdir,'mk')
    epath="%s/%s.%s.%s.%s.txt"%(bdir,type,model,dtg,area)
    return(epath)

def PutEvent(pyfile,type,tag,model,dtg,areaopt,area=None):

    dtgmn=dtg+'00'
    cdtgmn=mf.dtg('dtgmn')
    phr=mf.dtgmndiff(dtgmn,cdtgmn)
    eventtime=mf.dtg('dtg.hms')
    epath=EventPath(type,model,dtg,areaopt)

    oareaopt=areaopt
    if(area != None): oareaopt=area

    eventcard="%s %-15s dtg: %s model: %-5s areaopt: %-10s  time: %s phr: %6.2f"%(pyfile,tag,dtg,model,oareaopt,eventtime,phr)

    E=open(epath,'a')
    E.writelines(eventcard+'\n')
    E.close()

def GetEvent(type,model,dtg,area):
    epath=EventPath(type,model,dtg,area)
    try:
        cards=open(epath).readlines()
    except:
        cards=[]
    return(cards)


def ModelPlotTaus(model,dtg,center=W2Center.lower()):

    dtghh=int(dtg[8:10])

    taus=None
    if(center == 'esrl'):

        if(model == 'gfs2' or model == 'gfs' or model == 'ecm2' or model == 'gfsk'):
            etau=144
            dtau=12
            etau=None
            taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

        elif(mf.find(model,'fim')):
            etau=144
            dtau=12
            etau=None
            taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

        elif(model == 'ngp2' or model == 'ngp'):
            dtau=6
            etau=None
            taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144]

        elif(model == 'ngpc'):
            dtau=6
            etau=None
            taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

        elif(model == 'ecm' or model == 'ecmn'):
            etau=144
            dtau=12
            etau=None
            taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144]


        elif(model == 'ukm2' or model == 'ukm'):

            dtau=12
            etau=None
            if(dtghh == 0 or dtghh == 12):
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144]
            elif(dtghh == 6 or dtghh == 18):
                taus=[0,6,12,18,24,30,36,42,48,60]

        elif(model == 'cmc2' or model == 'cmc'):
            etau=144
            dtau=12

        else:
            print 'EEE invalid model plotmintau: ',model
            sys.exit()

    else:

        print 'EEEEEEEEEEEEEEEEEEE invalid center: ',center
        sys.exit()

    if(etau != None):
        taus=range(0,etau+1,dtau)

    return(taus)

def Model2DataTaus(model,dtg,center=W2Center.lower()):

    dtghh=int(dtg[8:10])

    taus=None
    if(center == 'esrl' or mf.find(center,'wxmap')):

        if(model == 'gfs2' or model == 'fim8' or model == 'fimx' or
           model == 'ecm2' or model == 'gfsk' or 
           model == 'cmc2' or model == 'cgd6' or model == 'cgd2' or
           model == 'ocn' or model == 'ohc' or model == 'ww3' or
           model == 'ecmn' or model == 'ngpc'):
            etau=Model2EtauData(model,dtghh)
            dtau=Model2DtauData(model,dtghh)
            if(etau != None):
                taus=range(0,etau+1,dtau)
            else:
                taus=[]

        elif(model == 'ukm2' or model == 'ngp2' ):
            if(dtghh == 0 or dtghh == 12):
                taus=range(0,72+1,6)+range(84,144+1,12)
            elif(dtghh == 6 or dtghh == 18):
                taus=range(0,60+1,6)

        else:
            print 'EEE invalid model DataTaus: ',model
            sys.exit()

    else:
        print 'EEEEEEEEEEEEEEEEEEE invalid center: ',center
        sys.exit()


    return(taus)


def IsModel2(model):

    for m2 in Nwp2ModelsAll:
        if(m2 == model):
            return(1)
    return(0)

def Model2CenterModel(model):

    centermodel=None

    if(model == 'gfs2'): centermodel='ncep/gfs2'
    if(model == 'fim8'): centermodel='esrl/fim8'
    if(model == 'fimx'): centermodel='esrl/fimx'
    if(model == 'ngp2'): centermodel='fnmoc/nogaps'
    if(model == 'ngpc'): centermodel='fnmoc/ngp05cagips'
    if(model == 'ocn'): centermodel='fnmoc/ocean/sst'
    if(model == 'ohc'): centermodel='fnmoc/ocean/ohc'
    if(model == 'ww3'): centermodel='fnmoc/ocean/ww3'
    if(model == 'ukm2'): centermodel='ukmo/ukm2'
    if(model == 'ecm1'): centermodel='ecmwf/ecm1'
    if(model == 'ecm2'): centermodel='ecmwf/ecmo'
    if(model == 'gfsk'): centermodel='esrl/gfsk'
    if(model == 'ecmn'): centermodel='ecmwf/ecmo_nws'
    if(model == 'cmc2'): centermodel='cmc/cmc'
    if(model == 'gfdl'): centermodel='ncep/gfdl'
    if(model == 'hwrf'): centermodel='ncep/gfdl'
    if(model == 'tctrk'): centermodel='tctrk'

    return(centermodel)


def getModelBaseName(imodel):

    ttp=imodel.split('.')
    ttd=imodel.split('_')
    if(len(ttp) > 1):
        model=ttp[0]
    elif(len(ttd) > 1):
        model=ttd[0]
    else:
        model=imodel

    lm=len(model)
    try:
        nm=int(model[lm-2:lm])
    except:
        nm=-999

    if(model[-1] == 'j' or model[-1] == 'k'):
        mbase=model[0:-1]
    elif(lm == 5 and nm >= 0):
        mbase=model[0:3]
    elif(lm == 4):
        mbase=model[0:4]
    elif(lm >= 5 and nm != -999):
        mbase=model[0:4]
    elif(lm >= 5 and nm == -999):
        mbase=model
    else:
        mbase=model[0:3]

    return(mbase)




def Model2LocalArchivePaths(model,dtg):

    yyyymm=dtg[0:6]

    localpaths=[]
    localarchpaths=[]

    if(model == 'gfs2'):
        ctlfile="gfs2.%s.ctl"%(dtg)

    elif(model == 'fim8'):
        ctlfile="fim8.*%s.ctl"%(dtg)

    elif(model == 'fimx'):
        ctlfile="%s/fim8.FIMX.grb2.ctl"%(dtg)

    elif(model == 'ngp2'):
        ctlfile="ngp.*%s.ctl"%(dtg)

    elif(model == 'ngpc'):
        ctlfile="ngpc.*%s.ctl"%(dtg)

    elif(model == 'ukm2'):
        ctlfile="ukm.%s.ctl"%(dtg)

    elif(model == 'ecm2'):
        ctlfile="ecmo.%s.*"%(dtg)

    elif(model == 'gfsk'):
        ctlfile="gfsk.%s.*"%(dtg)

    elif(model == 'ecmn'):
        ctlfile="ecmn.%s.*"%(dtg)

    elif(model == 'cmc2'):
        ctlfile="cmc.%s.*"%(dtg)


    localdir=Nwp2DataBdirModel(model)
    localpath="%s/%s/%s"%(localdir,dtg,ctlfile)
    print 'llll ',localpath
    localpaths.append(localpath)

    archsources=['local','local10','snap']
    for archsource in archsources:
        localarchbase=Model2ArchiveDir(yyyymm,source=archsource)
        localarchdir=Nwp2DataBdirModel(model,bdir2=localarchbase)
        localarchpath="%s/%s/%s"%(localarchdir,dtg,ctlfile)
        localarchpaths.append(localarchpath)

    return(localpaths,localarchpaths)



def Model2PlotMinTau(model,dtg,center='esrl'):

    dtghh=int(dtg[8:10])

    if(center == 'pcmdi'):
        pass

    elif(center == 'esrl'):

        if(model == 'gfs2'):
            taumin=144

        elif(mf.find(model,'fim8')):
            taumin=144

        elif(mf.find(model,'fimx')):
            taumin=144

        elif(model == 'ngp2'):
            taumin=144

        elif(model == 'ngpc'):
            taumin=144

        elif(model == 'ecm2'):
            taumin=144

        elif(model == 'gfsk'):
            taumin=144

        elif(model == 'ecmn'):
            taumin=144

        elif(model == 'ukm2'):
            #
            # taumin and tau forced to be the same because grib from ukmo is in one file...
            #
            if(dtghh == 0 or dtghh == 12):
                taumin=144
            elif(dtghh == 6 or dtghh == 18):
                taumin=60

        elif(model == 'cmc2'):
            taumin=144

        else:
            print 'EEE invalid model plotmintau: ',model
            sys.exit()

    tauend=Model2EtauData(model,dtghh)
    dtau=Model2DtauPlot(model)

    if(tauend != None and dtau != None):
        alltaus=range(0,tauend+1,dtau)
    else:
        print 'EEE invalid model in plotmintau',model,dtg
        sys.exit()

    return(taumin,alltaus)


def Model2ArchiveDir(yyyymm,source='local',dtg=None):

    if(source == 'local'):
        archdir=Nwp2DataArchiveBdirLocal
    elif(source == 'local10'):
        archdir=Nwp2DataArchiveBdirLocal10
    elif(source == 'snap'):
        archdir=Nwp2DataArchiveBdirSnap
    else:
        print 'EEE invalid (w2.py) model2 archive source: ',source
        sys.exit()

    archdir="%s/%s"%(archdir,yyyymm)

    return(archdir)


def Model2DataPaths(model,dtg,doreport=0,center='esrl',cagips=0):

    if(center == 'pcmdi'):
        pass

    elif(center == 'esrl'):

        yyyy=dtg[0:4]
        mm=dtg[4:6]
        yyyymm=dtg[0:6]
        mmddhh=dtg[4:10]

        ftpserver='hpss.nersc.gov'
        ftpserver='kishou.nhc.noaa.gov'
        ftpserver='share2'

        renmask=None
        modelrename=None

        localdir="%s/%s"%(Nwp2DataBdirModel(model),dtg)

        if(model == 'gfs2'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'fim8'):
            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'fimx'):

            localdir='/w21/dat/nwp2/rtfim/dat/FIMX/%s'%(dtg)
            dmask="*fim8.FIMX.f???.grb2"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'ngp2'):

            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'ngpc'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)


        elif(model == 'ukm2'):

            dmask="ukm.%s.t???.grb"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)


        elif(model == 'ecm2'):

            dmask="*DCD%s*"%(mmddhh)
            dmask="ecm2.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'gfsk'):

            dmask="gfsk.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'ecmn'):

            dmask="ecmo.*%s*"%(mmddhh)
            ldmask="%s/%s"%(localdir,dmask)

        elif(model == 'cmc2'):

            dmask="*cmc_%sf???"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

        else:
            print 'EEEE invalid model in w2.ModelArchiveDir: ',model
            sys.exit()



    elif(center == 'jtwc'):

        pass

    else:

        print 'EEEE invalid center: ',center,' in: ModelDirsPathsStatus'
        sys.exit()


    return(rc,latesttau)




def Model2DataPathsStatus(model,dtg,doreport=0,center='esrl',cagips=0,dowgribinv=1):


    printall=0
    if(doreport == 2): printall=1

    if(center == 'pcmdi'):

        pass

    elif(center == 'esrl'):

        yyyy=dtg[0:4]
        mm=dtg[4:6]
        yyyymm=dtg[0:6]
        mmddhh=dtg[4:10]

        ftpserver='hpss.nersc.gov'
        ftpserver='kishou.nhc.noaa.gov'
        ftpserver='share2'

        renmask=None
        modelrename=None

        localdir="%s/%s"%(Nwp2DataBdirModel(model),dtg)

        xwgrib='wgrib'

        if(model == 'gfs2'):

            xwgrib='wgrib2'
            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)


        elif(model == 'ngp2'):

            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)

        elif(model == 'ngpc'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)

        elif(model == 'fim8'):

            remotedir="%s/%s"%(Model2CenterModel(model),yyyymm)
            dmask="fim8.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)


        elif(model == 'fimx'):

            localdir='/w21/dat/nwp2/rtfim/dat/FIMX/%s'%(dtg)
            remotedir="%s/%s"%(Model2CenterModel(model),yyyymm)
            dmask="*fim8.FIMX.f???.grb2"
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)



        elif(model == 'ukm2'):

            dmask="ukm2.%s.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)
            hh=dtg[8:10]
            def name2tau(file):
                hh=dtg[8:10]
                if(hh == '00' or hh == '12'):
                    tau=144
                else:
                    tau=60

                return(tau)


        elif(model == 'ecm2'):

            dmask="ecmo.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):

                lf=len(file)
                lfe=lf-3
                lfb=lfe-6
                vmmddhh=file[lfb:lfe]
                vmm=vmmddhh[0:2]
                if(vmm == '01' and mm == '12'):
                    vdtg=str(int(yyyy+1))+vmmddhh
                else:
                    vdtg=yyyy+vmmddhh
                tau=mf.dtgdiff(dtg,vdtg)
                tau=int(tau)

                return(tau)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)

        elif(model == 'gfsk'):

            dmask="gfsk.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)


            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)



        elif(model == 'ecmn'):

            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)



        elif(model == 'cmc2'):

            remotedir="cmc/cmc/%s"%(yyyymm)
            dmask="*cmc_%sf???"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                lf=len(file)
                lfe=lf
                lfb=lfe-3
                tau=file[lfb:lfe]
                tau=int(tau)

                return(tau)


        else:
            print 'EEEE invalid model in w2.ModelArchiveDir: ',model
            sys.exit()



    elif(center == 'jtwc'):

        pass

    else:

        print 'EEEE invalid center: ',center,' in: ModelDirsPathsStatus'
        sys.exit()


    status={}

    override=0

    dpaths=glob.glob("%s"%(ldmask))
    dpaths.sort()

    report=[]

    if(doreport != 2):
        report.append("model: %s dtg: %s "%(model,dtg))

    np=len(dpaths)

    if(np == 0):
        rc=-1
        print 'WWW:  NO DATA model: ',model,dtg,' localdir: ',localdir
        return(rc,-999)


    report.append(" ")
    report.append("model   dtg       tau(h)  age(h)  nf")
    report.append("===== ==========  ======  ======  ==")
    report.append(" ")

    for dpath in dpaths:

        (dir,file)=os.path.split(dpath)
        (base,ext)=os.path.splitext(dpath)
        gribver=int(ext[-1])

        if(model == 'ukm2'):
            hh=dtg[8:10]
            if(hh == '00' or hh == '12'):
                tau=144
            else:
                tau=60
            wgribpath="%s.wgrib%1d.txt"%(base,gribver)

        else:
            tau=name2tau(file)
            wgribpath="%s.wgrib%1d.txt"%(base,gribver)

        if(dowgribinv):
            if(not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0) or override):
                cmd="%s %s > %s"%(xwgrib,dpath,wgribpath)
                mf.runcmd(cmd)

        if(os.path.exists(wgribpath)):
            (dir,file)=os.path.split(wgribpath)
            age=PathCreateTimeDtgdiff(dtg,wgribpath)
            nf=len(open(wgribpath).readlines())
            report.append("%s  %s   %03d   %5.2f  %4d"%(model,dtg,tau,age,nf))
            status[tau]=(age,nf)



    nmiss=-999
    curtaus=status.keys()
    curtaus.sort()

    (taumin,alltaus)=Model2PlotMinTau(model,dtg)

    if(len(curtaus) > 0):
        latesttau=curtaus[-1]
    else:
        latesttau=-999


    #
    # see if minimum taus is available
    #
    try:
        (agedone,nfdone)=status[taumin]
        iok=1
    except:
        (agedone,nfdone)=(-999.9,-99)
        iok=0


    if(iok):

        #
        # test for completeness
        #

        cmask={}

        for atau in alltaus:

            if(atau <= taumin):
                cmask[atau]=0
                for ctau in curtaus:
                    if(ctau == atau):
                        cmask[ctau]=1

        mtaus=cmask.keys()
        mtaus.sort()
        nmiss=0
        for mtau in mtaus:
            if(cmask[mtau] == 0): nmiss=nmiss+1


        rc=1

    else:

        #print 'WWW2: ',report[0],' insufficient DATA...'
        rc=0


    if(doreport):
        if(printall):
            for line in report:
                print line
        else:
            print report[-1]

    return(rc,latesttau)



def Model2IsReady2Plot(model,dtg):
    minfracreq=0.0
    if(model == 'ecmn'):
        rc=1
    else:
        (rc,latesttau)=Model2DataPathsStatus(model,dtg)

    return(rc,minfracreq)


def IsModel2PlotRunning(model,dtg):
    prcs="%s.%s.%s.*"%(W2TmpPrcDirPrefix,model,dtg)
    prcs=glob.glob(prcs)
    return(len(prcs))


def ModelMinGrbSiz(model,dtghh='',center=W2Center.lower()):

    #
    # actual #
    #
    if(model == 'gfs'): siz=61465404
    if(model == 'ngp'): siz=243116456
    if(model == 'ngp05'): siz=243116456
    if(model == 'ukm'): siz=12883332
    if(model == 'ocn'): siz=12883332
    if(model == 'ww3'): siz=12883332
    if(model == 'fg4'): siz=96552288

    #
    # mins
    #
    if(model == 'gfs'): siz=59000000
    if(model == 'gfs.jtwc'): siz=59000000
    if(model == 'ngp'): siz=80000000
    if(model == 'ngp05'): siz=80000000
    if(model == 'ocn'): siz= 7700000
    if(model == 'ww3'): siz= 7700000
    if(model == 'ukm'): siz=10000000
    if(model == 'ukm.jtwc'): siz= 1200000
    if(model == 'fg4'): siz= 7700000

    if(center == 'esrl'):
        if(model == 'gfs'): siz=25000000

        # cagips
        if(model == 'ngp'): siz=30000000
        if(model == 'ngp05'): siz=30000000

        # nawips
        if(model == 'ngp'): siz=12000000

        if(model == 'ukm'):
            if(dtghh == '06' or dtghh == '18'):
                siz=16000000
            else:
                siz=30000000

        if(model == 'ecm'): siz=28000000

        if(model == 'cmc'): siz=15000000
        if(model == 'ocn'): siz= 2000000
        if(model == 'ww3'): siz= 2000000

        if(model == 'fim8'): siz=25000000
        if(model == 'fimx'): siz=25000000
        if(model == 'fim9'): siz=25000000

        if(model == 'ecm2'): siz=28000000

        if(model == 'gfsk'): siz=28000000



    return(siz)

def ModelMaxNFlds(model,dtghh='',cagips=0,center=W2Center.lower()):

    if(center == 'esrl'):
        if(model == 'gfs'): nf=448

        # cagips
        if(model == 'ngp'):
            if(cagips):
                if(dtghh == '06' or dtghh == '18'):
                    nf=615
                else:
                    nf=614
            else:
                if(dtghh == '06' or dtghh == '18'):
                    nf=209
                else:
                    nf=209

        elif(model == 'ngp05'):
            if(cagips):
                if(dtghh == '06' or dtghh == '18'):
                    nf=615
                else:
                    nf=614
            else:
                if(dtghh == '06' or dtghh == '18'):
                    nf=209
                else:
                    nf=209

        if(model == 'ukm'):
            if(dtghh == '06' or dtghh == '18'):
                nf=210
            else:
                nf=406

        if(model == 'ecm'): nf=376

        if(model == 'cmc'): nf=272
        if(model == 'ocn'): nf= 3
        if(model == 'ww3'): nf= 1

        if(model == 'ecm2'): nf=376
        if(model == 'gfsk'): nf=376



    return(nf)

def Model2Model2TcModel(model):

    if(model == 'gfs2'):
        tcmodel='gfs2'
    elif(model == 'fim8'):
        tcmodel='fim8'

    elif(model == 'fimx'):
        tcmodel='fimx'

    elif(model == 'ngp2'):
        tcmodel='ngp2'

    elif(model == 'ngpc'):
        tcmodel='ngpc'

    elif(model == 'ecm2'):
        tcmodel='ecm2'

    elif(model == 'gfsk'):
        tcmodel='gfsk'

    elif(model == 'ecmn'):
        tcmodel='ecmn'
    elif(model == 'ukm2'):
        tcmodel='ukm2'

    elif(model == 'cmc2'):
        tcmodel='cmc'

    else:
        tcmodel=model

    return(tcmodel)

def Model2Model2PlotModel(model):

    if(model == 'gfs2'):
        pmodel='gfs'
    elif(model == 'fim8'):
        pmodel='fim'
    elif(model == 'fimx'):
        pmodel='fimx'
    elif(model == 'ngp2'):
        pmodel='ngp2'
    elif(model == 'ngpc'):
        pmodel='ngpc'

    elif(model == 'ecm2'):
        pmodel='ecm'

    elif(model == 'gfsk'):
        pmodel='gfsk'

    elif(model == 'ecmn'):
        pmodel='ecmn'
    elif(model == 'ukm2'):
        pmodel='ukm'

    elif(model == 'cmc2'):
        pmodel='cmc'

    else:
        pmodel=model

    return(pmodel)


def ModeltoGrfModel(model):


    if(model == 'gfs2'):
        gmodname='gfs05'
    elif(model == 'fim8'):
        gmodname='fim05'
    elif(model == 'fimx'):
        gmodname='fimx05'
    elif(model == 'ngp2'):
        gmodname='ngp10'
    elif(model == 'ngpc'):
        gmodname='ngp05'
        gmodname='ngpc'
    elif(model == 'ecmn'):
        gmodname='ecmn10'
    elif(model == 'ecm2'):
        gmodname='ecm10'

    elif(model == 'gfsk'):
        gmodname='gfs05'

    elif(model == 'ukm2'):
        gmodname='ukm07'
    elif(model == 'cmc2'):
        gmodname='cmc10'
    else:
        gmodname="%s%s"%(model,W2_MODELS_GRF_EXT)

    #ffffffffffffffffffffffffffffffffffffff
    #
    # force standard extenion -- disable
    #
    #gmodname="%s%s"%(model[0:3],W2_MODELS_GRF_EXT)

    return(gmodname)



def Model2CtlPath(model,dtg,ctltype=0,doarchive=0):

    if(doarchive == 1):
        ctldir="%s/w2flds/dat/%s/%s"%(Nwp2DataBdir,model,dtg)
    else:
        ctldir="%s/%s"%(Nwp2DataBdirModel(model),dtg)

    if(ctltype != 0 and doarchive != 1):
        ctlmask="%s/*.%s.%s.ctl"%(ctldir,dtg,ctltype)
    else:
        ctlmask="%s/*.%s.ctl"%(ctldir,dtg)

    if( (doarchive > 0) and (model == 'fim8' or model == 'gfs2') ):
        ctlmask="%s/*%s*.%s.ctl"%(ctldir,model,dtg)

    if(model == 'fimx' ):
        ctldir='/w21/dat/nwp2/rtfim/dat/FIMX/%s'%(dtg)
        ctlmask="%s/fim8.FIMX.grb2.ctl"%(ctldir)

    ctlpaths=glob.glob(ctlmask)


    if(len(ctlpaths) == 0):
        ctlpath=None
    else:
        ctlpath=ctlpaths[0]

    return(ctlpath)


def ModelDdtgData(model,dtghh='',center=W2Center.lower()):

    ddtg=None

    if(center == 'esrl'):

        if(model == 'gfs'): ddtg=6
        if(model == 'ngp'): ddtg=6
        if(model == 'ecm'): ddtg=12
        if(model == 'ukm'): ddtg=6
        if(model == 'cmc'): ddtg=12
        if(model == 'fim8' or model == 'fim9' or model == 'fimx'): ddtg=12

    return(ddtg)

def Model2DdtgData(model,dtghh='',center=W2Center.lower()):

    ddtg=None

    if(center == 'esrl'):

        if(model == 'gfs2'): ddtg=6
        if(model == 'fim8'): ddtg=12
        if(model == 'fimx'): ddtg=12
        if(model == 'ngp2'): ddtg=12
        if(model == 'ngpc'): ddtg=12
        if(model == 'ecm2'): ddtg=12
        if(model == 'gfsk'): ddtg=6
        if(model == 'ecmn'): ddtg=12
        if(model == 'ukm2'): ddtg=6
        if(model == 'cmc2'): ddtg=12

    return(ddtg)


def Model2DtauData(model,dtghh='',center=W2Center.lower()):

    dtau=None
    if(center == 'esrl'):

        if(model == 'gfs2'): dtau=6
        if(model == 'fim8'): dtau=6
        if(model == 'fimx'): dtau=6
        if(model == 'ngp2'): dtau=6
        if(model == 'ngpc'): dtau=6
        if(model == 'ocn'):  dtau=6
        if(model == 'ohc'):  dtau=6
        if(model == 'ww3'):  dtau=6
        if(model == 'ecm2'): dtau=6
        if(model == 'gfsk'): dtau=6
        if(model == 'ecmn'): dtau=12
        if(model == 'ukm2'): dtau=6
        if(model == 'cmc2'): dtau=6

    return(dtau)

def ModelDtauData(model,dtghh='',center=W2Center.lower()):

    dtau=None
    if(center == 'esrl'):

        if(model == 'gfs'): dtau=12
        if(model == 'ngp'): dtau=12
        if(model == 'ecm'): dtau=12
        if(model == 'ukm'): dtau=12
        if(model == 'cmc'): dtau=12
        if(model == 'fim8' or model == 'fim9' or model == 'fimx'): dtau=6

    return(dtau)


def Model2DtauPlot(model,dtghh='',center=W2Center.lower()):

    dtau=None
    if(center == 'esrl'):

        if(model == 'gfs'): dtau=6
        if(model == 'ngp'): dtau=6
        if(model == 'ngp05'): dtau=6
        if(model == 'ukm'): dtau=6
        if(model == 'ecm'): dtau=12
        if(model == 'cmc'): dtau=12
        if(model == 'ocn'): dtau=12
        if(model == 'ohc'): dtau=12
        if(model == 'ww3'): dtau=6

        if(model == 'gfs2'): dtau=12
        if(model == 'fim8'): dtau=12
        if(model == 'fimx'): dtau=12
        if(model == 'ngp2'): dtau=12
        if(model == 'ngpc'): dtau=6
        if(model == 'ecm2'): dtau=12
        if(model == 'gfsk'): dtau=6
        if(model == 'ecmn'): dtau=12
        if(model == 'ukm2'): dtau=6
        if(model == 'cmc2'): dtau=12

    return(dtau)




def Model2EtauData(model,dtghh=999,center=W2Center.lower()):

    etau=None

    dtghh=int(dtghh)

    if(center == 'esrl'):

        if(model == 'gfs'): etau=144
        if(model == 'ngp'): etau=144
        if(model == 'ngp05'): etau=144

        if(model == 'ecm'): etau=144
        if(model == 'cmc'): etau=144
        if(model == 'ocn'): etau=0
        if(model == 'ohc'): etau=0
        if(model == 'ww3'): etau=180

        if(model == 'gfs2'): etau=180
        if(model == 'ngp2'): etau=144
        if(model == 'ngpc'): etau=180
        if(model == 'ecm2'): etau=240
        if(model == 'gfsk'): etau=168
        if(model == 'ecmn'): etau=240

        if(model == 'ukm2' or model == 'ukm'):
            if(dtghh == 0 or dtghh == 12):
                etau=144
            elif(dtghh == 6 or dtghh == 18):
                etau=60

        if(model == 'cmc2'):
            if(dtghh == 0):
                etau=180
            elif(dtghh == 12):
                etau=144
            else:
                etau=None

        if(model == 'cgd2'):
            if(dtghh == 0):
                etau=240
            elif(dtghh == 12):
                etau=144
            else:
                etau=None

        if(model == 'cgd2'):
            if(dtghh == 0):
                etau=240
            elif(dtghh == 12):
                etau=144
            else:
                etau=None


        if(model == 'fim8' or model == 'fim9' or model == 'fimx'):
            etau=168

    return(etau)



def Model2Res(model):

    if(model == 'gfs2'): res=''
    if(model == 'fim8'): res=''
    if(model == 'fimx'): res=''
    if(model == 'ngp2'): res=''
    if(model == 'ngpc'): res=''
    if(model == 'ukm2'): res=''
    if(model == 'cmc2'): res=''
    if(model == 'ecm2'): res=''
    if(model == 'gfsk'): res=''
    if(model == 'ecmn'): res=''
    if(model == 'ecm1'): res=''

    return(res)

def ModelRes(model):

    if(IsModel2(model)):
        res=Model2Res(model)
        return(res)

    if(model == 'gfs'): res='10'
    if(model == 'gfs.jtwc'): res='10'
    if(model == 'ngp'): res='10'
    if(model == 'ngp05'): res='05'
    if(model == 'ocn'): res='02'
    if(model == 'ww3'): res='02'
    if(model == 'clm'): res='25'
    if(model == 'ukm'): res='10'
    if(model == 'ukm.jtwc'): res='12'
    if(model == 'fg4'): res='10'
    if(model == 'gsm'): res='12'
    if(model == 'ecm'): res='10'
    if(model == 'cmc'): res='10'
    if(model == 'fim8'): res='05'
    if(model == 'fim9'): res='05'
    if(model == 'fimx'): res='05'

    if(model == 'ecm1'): res='10'
    if(model == 'ecm2'): res='10'
    if(model == 'gfsk'): res='05'
    if(model == 'ecmn'): res='10'

    return(res)


def ModelResGrf(model):

    if(model == 'gfs'): res='10'
    if(model == 'ngp'): res='10'
    if(model == 'ngp05'): res='05'
    if(model == 'ukm'): res='10'
    if(model == 'ocn'): res='10'
    if(model == 'ww3'): res='02'
    if(model == 'clm'): res='25'
    if(model == 'fg4'): res='10'
    if(model == 'gsm'): res='10'
    if(model == 'ecm'): res='10'
    if(model == 'cmc'): res='10'

    if(model == 'ecm1'): res='10'
    if(model == 'ecm2'): res='10'
    if(model == 'gfsk'): res='05'
    if(model == 'ecmn'): res='10'

    return(res)

def ModelWxmap1GrfDir(model):

    if(model == 'gfs'): gdir=WebBdirWxmap1+'/ncep.gfs.grf'
    if(model == 'ukm'): gdir=WebBdirWxmap1+'/ncep.ukm.grf'
    if(model == 'ocn'): gdir=WebBdirWxmap1+'/fnmoc.ocn.grf'
    if(model == 'ww3'): gdir=WebBdirWxmap1+'/fnmoc.ww3.grf'
    if(model == 'ngp'): gdir=WebBdirWxmap1+'/fnmoc.nogaps.grf'
    if(model == 'ngp05'): gdir=WebBdirWxmap1+'/fnmoc.nogaps.grf'
    if(model == 'ecm'): gdir=WebBdirWxmap1+'/ecmwf.ifs.grf'
    if(model == 'cmc'): gdir=WebBdirWxmap1+'/cmc.cmc.grf'

    if(model == 'ecm2'): gdir=WebBdirWxmap1+'/ecmwf.ifs.grf'
    if(model == 'gfsk'): gdir=WebBdirWxmap1+'/ecmwf.gfsk.grf'

    return(gdir)

def W2ModelPltDir(model,dtype='local'):

    if(model == 'gfs'): gdir='plt_ncep_gfs'
    if(model == 'fim'): gdir='plt_esrl_fim'
    if(model == 'ukm'): gdir='plt_ukmo_ukm'
    if(model == 'ocn'): gdir='plt_fnmoc_ocn'
    if(model == 'ww3'): gdir='plt_fnmoc_ocn'
    if(model == 'ngp'): gdir='plt_fnmoc_ngp'
    if(model == 'ngp2'): gdir='plt_fnmoc_ngp'
    if(model == 'ngpc'): gdir='plt_fnmoc_ngpc'
    if(model == 'ngp05'): gdir='plt_fnmoc_ngp'
    if(model == 'ecm'): gdir='plt_ecmwf_ecm'
    if(model == 'cmc'): gdir='plt_cmc_cmc'

    if(dtype == 'full'):
        gdir="%s/%s"%(W2BaseDirWeb,gdir)

    if(model == 'ecm2'): gdir='plt_ecmwf_ecm'
    if(model == 'ecm2'): gdir='plt_esrl_gfsk'
    if(model == 'ecmn'): gdir='plt_ecmwf_ecm'

    return(gdir)

def W2LoopPltDir(ltype,dtype='full',doarchive=0):

    gdir='plt_loop'
    if(ltype == 'prw'): gdir='plt_loop'

    if(dtype == 'full'):

        if(doarchive == 3):
            gdir="%s/%s"%(EsrlHttpIntranetDocRoot,gdir)
        elif(doarchive > 0 and doarchive != 3):
            gdir="%sa/%s"%(W2BaseDirWeb,gdir)
        else:
            gdir="%s/%s"%(W2BaseDirWeb,gdir)

    return(gdir)


def NwpDataBdir(model):
    #
    # do not put in argument list, set bdir by
    # setting in the w2 object, e.g.,
    # w2.W2BaseDirDat=w2.W2RegenBaseDirDat
    #
    bdir=W2BaseDirDat

    if(model == 'ngp'):
        ddir="%s/nwp/fnmoc"%(bdir)
    elif(model == 'ngp05'):
        ddir="%s/nwp/fnmoc"%(bdir)
    elif(model == 'ocn'):
        ddir="%s/nwp/fnmoc"%(bdir)
    elif(model == 'ww3'):
        ddir="%s/nwp/fnmoc"%(bdir)
    elif(model == 'gfs' or model == 'gfs.jtwc' or model == 'avn'):
        ddir="%s/nwp/ncep"%(bdir)
    elif(model == 'ukm' or model == 'ukm.jtwc'):
        ddir="%s/nwp/ukmo"%(bdir)
    elif(model == 'gsm'):
        ddir="%s/nwp/jma"%(bdir)
    elif(model == 'ecm'):
        ddir="%s/nwp/ecmwf"%(bdir)
    elif(model == 'cmc'):
        ddir="%s/nwp/cmc"%(bdir)
    elif(model == 'fim8' or model == 'fim9' or model == 'fimx'):
        ddir="%s/nwp/gsd/%s"%(bdir,model)
    elif(model == 'all'):
        ddir="%s/nwp/*"%(bdir)

    elif(model == 'cqpr'):
        ddir=NhcQmorphProductsGrib
    else:
        ddir=0

    if(bdir == ''):
        ddir=ddir[1:]

    return(ddir)

def Nwp2DataBdirModel(model,bdir2=Nwp2DataBdir):

    ddir=None
    if(bdir2 == ''):
        ddir=ddir[1:]

    centermodel=Model2CenterModel(model)
    ddir="%s/%s"%(bdir2,centermodel)

    if(model == 'fimx'):
        ddir='/w21/dat/nwp2/rtfim/dat/FIMX'


    if(model == 'all2'):
        ddir="%s/*/*"%(bdir2)

    return(ddir)

def CagipsNwpCtlFile(model,dtg,ctlfile,grbfile,gmpfile,dogribmap=1):

    bdir=NwpDataBdir(model)
    gtime=mf.dtg2gtime(dtg)

    ctl=None

    if(model == 'ngp'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
#
#dtype grib 3
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef  8 levels
1000 925 850 700 500 400 300 200
tdef  13 linear %s 12hr
vars  11
prm     0 62,1,0     ** misc precipitation [kg/m^2]
pr      0 61,1,0     ** Total precipitation [kg/m^2]
psl     0  2,102,0   ** Pressure reduced to MSL [Pa]
tas     0 11,105,2   ** sfc air T [K]
uas     0 33,105,10  ** u wind [m/s]
vas     0 34,105,10  ** v wind [m/s]
zg      8  7,100,0   ** Geopotential height [gpm]
hur     8 52,100,0   ** Relative humidity [%%]
ta      8 11,100,0   ** Temp. [K]
ua      8 33,100,0   ** u wind [m/s]
va      8 34,100,0   ** v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    if(model == 'ngp05'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
#
#dtype grib 3
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef  8 levels
1000 925 850 700 500 400 300 200
tdef  13 linear %s 12hr
vars  11
prm     0 62,1,0     ** misc precipitation [kg/m^2]
pr      0 61,1,0     ** Total precipitation [kg/m^2]
psl     0  2,102,0   ** Pressure reduced to MSL [Pa]
tas     0 11,105,2   ** sfc air T [K]
uas     0 33,105,10  ** u wind [m/s]
vas     0 34,105,10  ** v wind [m/s]
zg      8  7,100,0   ** Geopotential height [gpm]
hur     8 52,100,0   ** Relative humidity [%%]
ta      8 11,100,0   ** Temp. [K]
ua      8 33,100,0   ** u wind [m/s]
va      8 34,100,0   ** v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    if(model == 'ocn'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
#
#dtype grib 3
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef  8 levels
1000 925 850 700 500 400 300 200
tdef  13 linear %s 12hr
vars 4
htsgw 0 100,1,0  ** Sig height of wind waves and swell [m]
sic   0  91,1,0  ** Ice concentration (ice=1;no ice=0) [fraction]
tosa  0  25,1,0  ** Temp. anomaly [K]
tos   0  80,1,0  ** Water temp. [K]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'ecm' or model == 'ukm' or model == 'cmc'):
        ddir="%s/nwp/cmc"%(bdir)
    else:
        ddir=0

    if(bdir == ''):
        ddir=ddir[1:]

    ctlpath="%s/%s"%(bdir,ctlfile)
    mf.WriteCtl(ctl,ctlpath)

    ropt=''
    if(dogribmap):
        cmd="gribmap -s100000 -E -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)

    return(ctlpath)



def NwpCtlFile(model,dtg,ctlfile,grbfile,gmpfile,dogribmap=1):

    bdir=NwpDataBdir(model)
    gtime=mf.dtg2gtime(dtg)

    if(model == 'ngp' or model == 'gfs'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
ydef 181 linear -90.0 1.0
xdef 360 linear   0.0 1.0
zdef  11 levels
1000 925 850 700 500 400 300 250 200 150 100 
tdef  13 linear %s 12hr
vars  16
prc    0  63,1  ,0   Convective precipitation [kg/m^2]
pr     0  61,1  ,0   Total precipitation [kg/m^2]
zg    11   7,100,0   Geopotential height [gpm]
psl    0   1,102,0   Pressure [Pa]
hur   11  52,100,0   Relative humidity [%%]
hurs   0  52,105,2   Relative humidity [%%]
cll    0  71,212,0   Total cloud cover [%%]
clm    0  71,222,0   Total cloud cover [%%]
clh    0  71,232,0   Total cloud cover [%%]
ta    11  11,100,0   Temp. [K]
tas    0  11,105,2   Temp. [K]
ua    11  33,100,0   u wind [m/s]
uas    0  33,105,10  u wind [m/s]
va    11  34,100,0   v wind [m/s]
vas    0  34,105,10  v wind [m/s]
wap   11  39,100,0   v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'ngp05'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
xdef 720 linear   0.0 1.0
ydef 361 linear -90.0 1.0
zdef  11 levels
1000 925 850 700 500 400 300 250 200 150 100 
tdef  13 linear %s 12hr
vars  16
prc    0  63,1  ,0   Convective precipitation [kg/m^2]
pr     0  61,1  ,0   Total precipitation [kg/m^2]
zg    11   7,100,0   Geopotential height [gpm]
psl    0   1,102,0   Pressure [Pa]
hur   11  52,100,0   Relative humidity [%%]
hurs   0  52,105,2   Relative humidity [%%]
cll    0  71,212,0   Total cloud cover [%%]
clm    0  71,222,0   Total cloud cover [%%]
clh    0  71,232,0   Total cloud cover [%%]
ta    11  11,100,0   Temp. [K]
tas    0  11,105,2   Temp. [K]
ua    11  33,100,0   u wind [m/s]
uas    0  33,105,10  u wind [m/s]
va    11  34,100,0   v wind [m/s]
vas    0  34,105,10  v wind [m/s]
wap   11  39,100,0   v wind [m/s]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'ocn'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
ydef 181 linear -90.0 1.0
xdef 360 linear   0.0 1.0
zdef  1 levels 1013
tdef 13 linear %s 12hr
vars  4
tos     0  80,1,0  SST from OCN model [K]
wavdir  0 107,1,0  ** Primary wave direction [deg]
htsgw   0 100,1,0  ** Sig height of wind waves and swell [m]
wavper  0 108,1,0  ** Primary wave mean period [s]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'ecm'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
ydef 181 linear -90.0 1.0
xdef 360 linear   0.0 1.0
zdef  1 levels 500
tdef  7 linear %s 24hr
vars 2
psl      0    1,102, 0  Pressure [Pa]
zg       0    7,100,500     Geopotential height [gpm]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'ukm.jtwc'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
xdef 288 linear   0 1.25
ydef 145 linear -90 1.25
zdef   6 levels 1000 850 700 500 300 200
tdef   7 linear %s 12hr
vars 9
psl      0    2,102, 0  Pressure [Pa]
uas      0   33,  1, 0  10  u sfc wind (10m) [m/s]
vas      0   34,  1, 0  10  v sfc wind (10m) [m/s]
zg       6    7,100     Geopotential height [gpm]
ta       6   11,100     Temperature [K]
ua       6   33,100     u wind [m/s]
va       6   34,100     v wind [m/s]
hur      6   52,100     Relative humidity [percent]
wap      6   39,100     Veritcal velocity [Pa/s]
endvars"""%(grbfile,gmpfile,gtime)

    elif(model == 'gfs.jtwc'):
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title fnmoc cagips data for wxmap2
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev
xdef 360 linear   0 1.0
ydef 181 linear -90 1.0
zdef  6 levels 1000 850 700 500 300 200
tdef  12 linear %s 12hr
vars 13
psl      0    2,102,  0  Pressure [Pa]
uas      0   33,105, 10  u sfc wind (10m) [m/s]
vas      0   34,105, 10  v sfc wind (10m) [m/s]
tas      0   11,105,  2  tas sfc Temperature (2m) [K]
pr       0   61,  1,  0  precip accumulated [mm/6 h]
tasmax   0   15,105,  2  max tas sfc Temperature (2m) [K]
tasmin   0   16,105,  2  min tas sfc Temperature (2m) [K]
zg       6    7,100  Geopotential height [gpm]
ta       6   11,100  Temperature [K]
ua       6   33,100  u wind [m/s]
va       6   34,100  v wind [m/s]
hur      6   52,100  Relative humidity [percent]
wap      4   39,100  Veritcal velocity [Pa/s]
endvars"""%(grbfile,gmpfile,gtime)

    print ctl
    ctlpath="%s/%s"%(bdir,ctlfile)
    mf.WriteCtl(ctl,ctlpath)

    ropt=''
    if(dogribmap):
        cmd="gribmap -s100000 -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)

    return(ctlpath)



def NwpDataFile(model,dtg,iscagips=0):

    res=ModelRes(model)
    if(iscagips):
        bfile="%s.%s.cagips.%s"%(model,res,dtg)
    else:
        bfile="%s.%s.%s"%(model,res,dtg)

    ctlfile="%s.ctl"%(bfile)
    grbfile="%s.grb"%(bfile)
    gmpfile="%s.gmp"%(bfile)

    return(ctlfile,grbfile,gmpfile)


def NcepGfsNomadsPath(dtg,model,archivetype='archive'):

    NomadsServer="nomad2.ncep.noaa.gov:9090"
    NomadsServer="nomad3.ncep.noaa.gov"
    yyyymm=str(dtg[0:8])
    hh=str(dtg[8:10])

    if(archivetype == 'archive'):
        url="http://%s/dods/%s/archive/%s%s/%s_%sz"%(NomadsServer,model,model,yyyymm,model,hh)
    else:
        url="http://%s/dods/%s/rotating/%s%s/%s_%sz"%(NomadsServer,model,model,yyyymm,model,hh)
    return(url)

#
#  see http://www.calle.com/world for lat/long of an
#
StationLonLat={
    'Reading_UK':[-1.0,51.43],
    'willits_ca':[-123.30,39.70],
    'dublin_ca':[-121.93,37.70],
    'boulder_co':[-105.20,40.00],
    'ocala_fl':[-82.1,29.2],
    'pinnacles_ca':[-121.00,36.50],
    'point_reyes_ca':[-122.87,38.11],
    'DCA':[-77.0,38.9],
    'IAD':[-77.5,38.9],
    'ATL':[-88.4,33.6],
    'AVL':[-82.5,35.4],
    'MIA':[-80.3,25.8],
    'OKC':[-97.6,35.4],
    'patrick_afb':[-80.6,28.2],
    'bsa_losmochos':[-121.53,37.55],
    'yosemite':[-119.59,37.74],
    'llnl':[-121.70,37.70],
    'Indian_GR_SP':[-120.65,38.43],
    'san_diego_ca':[-117.15,32.71],
    'special':[-110.1,37.6],
    'green_valley_az':[-111.0,31.86],
    'nice_france':[7.2,43.7],
    'firenze_italia':[11.2,43.8],
}

def MeteogramGs(model):
    gsdir=os.getenv('GASCRP')
    if(model == 'gfs' or model == 'gfs05'):
        gspath=gsdir+'/meteogram_%s.gs'%(model)
    elif(model == 'gfsb'):
        gspath=gsdir+'/meteogram_%s.gs'%(model)
    elif(model == 'nam'):
        gspath=gsdir+'/meteogram_%s.gs'%(model)

    return(gspath)


def MeteogramNomadsCtl(model,dtg,modelopt='nam3hr',source='ncep',archivetype='archive'):

    yyyymm=dtg[0:6]
    yyyymmdd=dtg[0:8]
    hh=dtg[8:10]
    hh4="%04d"%(int(hh))
    print 'ssss', source

    nomadsmodel=model
    modeldtg=model
    modelhh=model

    if(model == 'nam'):

        if(modelopt == 'nam1hr'):
            nomadsmodel='nam'
            modelhh='nam1hr'

        if(modelopt == 'nam3hr'):  nomadsmodel='nam'

    elif(model == 'gfs05'):

        if(source == 'cola'):
            nomadsmodel='gfs2'
            modeldtg='gfs'
            modelhh=nomadsmodel
        else:
            nomadsmodel='gfs_master'
            modeldtg='gfs'
            modelhh=nomadsmodel



#http://www.monsoondata.org:9090/dods/gfs2/gfs.2008020500
    if(source == 'cola'):

        server='www.monsoondata.org:9090'
        dsetcardgfs="http://%s/dods/%s/%s.%s"%(server,nomadsmodel,modeldtg,dtg)
        dsetcardnam=''

    elif(source == 'ncep1'):
        server='nomad1.ncep.noaa.gov:9090'
        if(archivetype == 'archive'):
            dsetcardgfs="http://%s/dods/%s/archive/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)
            dsetcardnam=dsetcardgfs
        elif(archivetype == 'realtime'):
            dsetcardgfs="http://%s/dods/%s/archive/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)
            dsetcardnam=dsetcardgfs
        else:
            dsetcardgfs="http://%s/dods/%s/rotating/gfs_%sz"%(server,model,hh)
            dsetcardnam="http://%s/dods/%s/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)

    elif(source == 'ncep' or source == 'ncep5'):
        server='nomad6.ncep.noaa.gov:9090'
        server='nomad5.ncep.noaa.gov:9090'
        server='nomads.ncep.noaa.gov:80'
        #http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs20170517/gfs_0p25_12z
        model='gfs_0p25'
        model='gfs'
        if(model == 'gfs05'): model='gfs'
        model='gfs_0p25'
        model='gfs'

        if(archivetype == 'archive'):
            dsetcardgfs="http://%s/dods/%s/archive/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)
            dsetcardnam=dsetcardgfs
        elif(archivetype == 'realtime'):
            #http://nomad5.ncep.noaa.gov:9090/dods/gfs/rh20070724/gfs_00z.rh20070724
            #http://nomad5.ncep.noaa.gov:9090/dods/gfs/gfs20071225/gfs_00z
            #http://nomad5.ncep.noaa.gov:9090/dods/nomad1-raid1/gfs_master/gfs20080620/gfs_master_06z
            dsetcardgfs="http://%s/dods/nomad1-raid1/%s_master/%s%s/%s_master_%sz"%(server,model,model,yyyymmdd,model,hh)
            #http://nomad5.ncep.noaa.gov:9090/dods/nam/nam20080620/nam_06z
            dsetcardnam="http://%s/dods/%s/%s%s/%s_%sz"%(server,model,model,yyyymmdd,model,hh)


        else:
            dsetcardgfs="http://%s/dods/%s/rotating/gfs_%sz"%(server,model,hh)
            dsetcardnam="http://%s/dods/%s/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)
            
        dsetcardgfs="http://%s/dods/%s_0p25/%s%s/%s_0p25_%sz"%(server,model,model,yyyymmdd,model,hh)

    elif(source == 'ncep3'):
        server='nomads6.ncdc.noaa.gov:9090'
        server='nomad3.ncep.noaa.gov:9090'
        if(model == 'gfs05'):
            server='nomads6.ncdc.noaa.gov:9090'
            server='nomad3.ncep.noaa.gov:9090'

        #http://nomad3.ncep.noaa.gov:9090/dods/gfs/gfs20061228/gfs_06z
        if(archivetype == 'archive'):
            dsetcardgfs="http://%s/dods/%s/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)
            dsetcardnam=dsetcardgfs
        elif(archivetype == 'realtime'):
            dsetcardgfs="http://%s/dods/%s/%s%s/%s_%sz"%(server,nomadsmodel,modeldtg,yyyymmdd,modelhh,hh)
            dsetcardnam=dsetcardgfs
        elif(archivetype == 'rotating'):
            #http://nomad3.ncep.noaa.gov:9090/dods/gfs/rotating/gfs_06z
            dsetcardgfs="http://%s/dods/%s/rotating/%s_%sz"%(server,nomadsmodel,nomadsmodel,hh)
            dsetcardnam=dsetcardgfs
        else:
            dsetcardgfs="http://%s/dods/%s/%s%s/%s_%sz"%(server,nomadsmodel,nomadsmodel,yyyymmdd,modelhh,hh)
            dsetcardnam="http://%s/dods/%s/%s%s/%s_%sz"%(server,model,model,yyyymmdd,modelhh,hh)

    elif(source == 'ncdc'):
        #http://nomads.ncdc.noaa.gov:9090/dods/_NCEP_HIRES_GFSAVN/200404/20040428/gfs-avn-hi_3_20040428_0000_fff
        #http://nomads6.ncdc.noaa.gov:9090/dods/gfs_master/gfs20061228/gfs_master_12z

        if(model == 'gfs05'):
            server='nomads6.ncdc.noaa.gov:9090'
        else:
            server='nomads.ncdc.noaa.gov:9091'

        if(model == 'gfs'):
            ncdcmodelgrid='gfs_3'
            ncdcmodel='NCEP_GFS'
        elif(model == 'nam'):
            ncdcmodelgrid='nam_218'
            ncdcmodel='NCEP_NAM'

        #http://nomads.ncdc.noaa.gov:9091/dods/NCEP_NAM/200612/20061228/nam_218_20061228_0600_fff
        if(model == 'gfs' or model == 'nam'):

            server='nomads6.ncdc.noaa.gov:9090'
            #http://nomads6.ncdc.noaa.gov:9090/dods/gfs_master/gfs20080620/gfs_master_12z
            dsetcardgfs="http://%s/dods/%s_master/%s%s/%s_master_%sz"%(server,model,model,yyyymmdd,model,hh)
            #http://nomads6.ncdc.noaa.gov:9090/dods/nam/nam20080620/nam_12z
            dsetcardnam="http://%s/dods/%s/%s%s/%s_%sz"%(server,model,model,yyyymmdd,model,hh)


        else:
            if(archivetype == 'realtime'):
                dsetcardgfs="http://%s/dods/%s/%s%s/%s_%sz"%(server,nomadsmodel,modeldtg,yyyymmdd,nomadsmodel,hh)
                dsetcardnam=dsetcardgfs


    if(model == 'gfs'):

        nlev=26
        nlev=47
        nfc=61
        dtau=3
        
        nlev=31
        nfc=41
        dtau=3
        btime=mf.dtg2gtime(dtg)
        ctl="""dset %s
title GFS %s run
tdef time %d linear %s %shr
vars 22
ugrdprs=>u           %d -999 ** u wind [m/s] 
vgrdprs=>v           %d -999 ** u wind [m/s] 
tmpprs=>t            %d -999 ** temp. [k] 
rhprs=>rh            %d -999 ** relative humidity [%%] 
hgtprs=>z            %d -999 ** geopotential height [gpm] 
pressfc=>ps        0 -999 ** surface pressure [pa] 
prmslmsl=>slp         0 -999 ** pressure reduced to msl [pa] 
no4lftxsfc=>li4       0 -999 ** surface best (4-layer) lifted index [k] 
lftxsfc=>li           0 -999 ** surface surface lifted index [k] 
ugrd10m=>u10m      0 -999 ** 10 m u wind [m/s] 
vgrd10m=>v10m      0 -999 ** 10 m u wind [m/s] 
rh2m=>rh2m         0 -999 ** 2 m relative humidity [%%] 
tmp2m=>t2m         0 -999 ** 2 m temp. [k] 
owatrsfc=>runoff      0 -999 ** surface water runoff [kg/m^2] (hidden) 
soill0_10cm=>soilm2    0 -999 ** 0-10cm undergnd volumetric soil moisture [fraction] 
soill0_10cm=>soilm2    0 -999 ** 0-10cm undergnd volumetric soil moisture [fraction] 
opratesfc=>op         0 -999 ** surface precipitation rate [kg/m^2/s] (hidden) 
oapcpsfc=>p            0 -999 ** surface total precipitation [kg/m^2] (hidden) 
oacpcpsfc=>pc          0 -999 ** surface convective precipitation [kg/m^2] (hidden) 
ocsnowsfc=>csnow      0 -999 ** surface categorical snow [yes=1;no=0] (hidden) 
ocfrzrsfc=>cfrzr      0 -999 ** surface categorical freezing rain [yes=1;no=0] (hidden) 
ocicepsfc=>cicep      0 -999 ** surface categorical ice pellets [yes=1;no=0] (hidden) 
endvars"""%(dsetcardgfs,dtg,nfc,btime,dtau,
            nlev,nlev,nlev,nlev,nlev)

    elif(model == 'gfs05' and source != 'cola'):

        nlev=47
        nfc=61
        dtau=3
        btime=mf.dtg2gtime(dtg)
        ctl="""dset %s
title GFS %s run
tdef time %d linear %s %shr
vars 21
ugrdprs=>u           %d -999 ** u wind [m/s] 
vgrdprs=>v           %d -999 ** u wind [m/s] 
tmpprs=>t            %d -999 ** temp. [k] 
rhprs=>rh            %d -999 ** relative humidity [%%] 
hgtprs=>z            %d -999 ** geopotential height [gpm] 
pressfc=>ps            0 -999 ** surface pressure [pa] 
prmslmsl=>slp          0 -999 ** pressure reduced to msl [pa] 
no4lftxsfc=>li4        0 -999 ** surface best (4-layer) lifted index [k] 
lftxsfc=>li            0 -999 ** surface surface lifted index [k] 
ugrd10m=>u10m          0 -999 ** 10 m u wind [m/s] 
vgrd10m=>v10m          0 -999 ** 10 m u wind [m/s] 
rh2m=>rh2m             0 -999 ** 2 m relative humidity [%%] 
tmp2m=>t2m             0 -999 ** 2 m temp. [k] 
owatrsfc=>runoff       0 -999 ** surface water runoff [kg/m^2] (hidden) 
soilw0_10cm=>soilm2    0 -999 ** 0-10cm undergnd volumetric soil moisture [fraction] 
opratesfc=>op          0 -999 ** surface precipitation rate [kg/m^2/s] (hidden) 
oapcpsfc=>p            0 -999 ** surface total precipitation [kg/m^2] (hidden) 
oacpcpsfc=>pc          0 -999 ** surface convective precipitation [kg/m^2] (hidden) 
ocsnowsfc=>csnow       0 -999 ** surface categorical snow [yes=1;no=0] (hidden) 
ocfrzrsfc=>cfrzr       0 -999 ** surface categorical freezing rain [yes=1;no=0] (hidden) 
ocicepsfc=>cicep       0 -999 ** surface categorical ice pellets [yes=1;no=0] (hidden) 
endvars"""%(dsetcardgfs,dtg,nfc,btime,dtau,
            nlev,nlev,nlev,nlev,nlev)

    elif(model == 'gfs05' and source == 'cola'):

        nlev=47
        nfc=61
        dtau=3
        btime=mf.dtg2gtime(dtg)
        ctl="""dset %s
title GFS %s run
"""%(dsetcardgfs,dtg)


    elif(model == 'nam'):


        ctl="""dset %s
title NAM %s run
vars 16
hgtprs=>z          39 -999 ** geopotential height [gpm] 
rhprs=>rh          39 -999 ** relative humidity [%%] 
tmpprs=>t          39 -999 ** temp. [k] 
ugrdprs=>u         39 -999 ** u wind [m/s] (hidden) 
vgrdprs=>v         39 -999 ** v wind [m/s] (hidden) 
no4lftx180_0mb=>li  0 -999 ** 180-0 mb above gnd best (4-layer) lifted index [k] 
acpcpsfc=>pc        0 -999 ** surface convective precipitation [kg/m^2] 
apcpsfc=>p          0 -999 ** surface total precipitation [kg/m^2] 
pressfc=>ps         0 -999 ** surface pressure [pa] 
prmslmsl=>slp       0 -999 ** pressure reduced to msl [pa] 
rh2m=>rh2m          0 -999 ** 2 m relative humidity [%%] 
soilwsoilt=>soilm2  0 -999 ** 0-10cm undergnd volumetric soil moisture [fraction] 
tmp2m=>t2m          0 -999 ** 2 m temp. [k] 
ugrd10m=>u10m       0 -999 ** 10 m u wind [m/s] (hidden) 
vgrd10m=>v10m       0 -999 ** 10 m v wind [m/s] (hidden) 
msletmsl=>slpe      0 -999 ** mean sea level pressure (nam model) [pa] 
endvars"""%(dsetcardnam,dtg)


    return(ctl)


def AnalNgpGrbLog(srcopt,dtg,ipath,opath):

    def utc2plustime(synhour,utc):
        utchh=utc.split(':')[0]
        utcmm=utc.split(':')[1]
        plustime=(float(utchh)+float(utcmm)/60.0)-float(synhour)

        return(plustime)

    def grbfile2vars(grbfile):
        prodtype=grbfile[6:9]
        prodsrc=grbfile[17:21]
        grid=grbfile[22:26]
        tau=int(grbfile[27:32])/100
        ltype=grbfile[47:51]
        level=grbfile[52:58]
        level=int(level)*0.1
        var=grbfile[65:]

        rc=(prodtype,prodsrc,grid,tau,ltype,level,var)
        return(rc)


    def DefineGrid(ni,nj,wi0,wj0,dwi,dwj,undef):
        """
        1,1 based grid with ni,nj points
        starting at wi0,wj0 with delta w (world coordinate, e.g, lat/lon) dwi,dwj
        """
        grid={}
        nij=ni*nj
        for j in range(1,nj+1):
            for i in range(1,ni+1):
                grid[i,j]=undef

        return(grid)

    def w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj):

        i=(wi-wi0)/dwi + 0.5
        j=(wj-wj0)/dwj + 0.5

        #
        # cyclic continuity in x
        #

        if(i <  0.0): i=float(ni)+i
        if(i >   ni): i=i-float(ni)

        i=int(i+1.0)
        j=int(j+1.0)

        return(i,j)


    card1="%s DPSR feed analysis by tau / plus hour for dtg: %s"%(srcopt,dtg)
    report=card1 + '\n' + (len(card1)*'=') + '\n\n'


    try:
        O=open(opath,'w')
    except:
        print "EEE unable to open: %s"%(opath)
        sys.exit()

    verb=0

    #
    # i-> tau
    # j-> + h
    #

    dtau=6.0
    etau=144.0

    dphr=0.5
    ephr=15.0

    ni=int((etau/dtau)+1.0)
    nj=int((ephr/dphr)+1.0)

    wi0=0.0
    wj0=0.0
    dwi=dtau
    dwj=dphr
    g0=0.0
    undef=-999.0

    grid=DefineGrid(ni,nj,wi0,wj0,dwi,dwj,g0)

    print 'ni,nj ',ni,nj

    synhour=dtg[8:]
    print synhour
    cards=open(ipath).readlines()

    nfiles=0
    for card in cards:
        utc=card.split()[0]
        grbfile=card.split()[1]
        nfiles=nfiles+1
        plustime=utc2plustime(synhour,utc)
        rc=grbfile2vars(grbfile)
        #print utc,grbfile,"%5.2f"%(plustime),rc
        tau=rc[3]

        wi=float(tau)
        wj=plustime

        (i,j)=w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj)
        #print 'ggg ',wi,wj,ni,nj,wi0,wj0,dwi,dwj,i,j
        if(verb): print nfiles,wi,i,wj,j,grbfile

        grid[i,j]=grid[i,j]+1



    pcards=[]

    doall=1
    if(doall):
        otaus=range(0,int(etau)+1,int(dtau))
    else:
        otaus=range(0,72,6)+range(72,144+1,6)

    itaus=[]

    for otau in otaus:
        (i,j)=w2ij(otau,0,ni,nj,wi0,wj0,dwi,dwj)
        itaus.append(i)


    tcard='phr/tau  TOT'
    for i in itaus:
        tau=wi0+dwi*(i-1)
        tcard=tcard+" %03.0f"%(tau)

    pcards.append(tcard)

    tautot={}
    for i in range(1,ni+1):
        tautot[i]=0
        for j in range(1,nj+1):
            tautot[i]=tautot[i]+grid[i,j]


    for j in range(1,nj+1):
        tot=0
        for i in itaus:
            tot=tot+grid[i,j]

        card="%5d"%(tot)

        for i in itaus:
            if(grid[i,j] == 0):
                ogrid=' ---'
            else:
                ogrid=' %3d'%(grid[i,j])
            card=card+ogrid

        phr=wj0+dwj*(j-1)
        card="%05.2f  %s"%(phr,card)
        pcards.append(card)

    card="total: %5d"%(nfiles)

    for i in itaus:
        if(tautot[i] == 0):
            ogrid=' ---'
        else:
            ogrid=' %3d'%(tautot[i])
        card=card+ogrid

    pcards.append(card)

    for pcard in pcards:
        report=report+pcard+'\n'

    print report
    O.writelines(report)
    O.close()



def ModelGrfDir(model,dtg):
    if(model == 'ngp'):
        gdir="%s/fnmoc/nogaps/grf/archive/%s"%(wxdFtp,dtg)
    elif(model == 'ngp05'):
        gdir="%s/fnmoc/nogaps/grf/archive/%s"%(wxdFtp,dtg)
    elif(model == 'gfs'):
        gdir="%s/ncep/gfs/grf/archive/%s"%(wxdFtp,dtg)
    elif(model == 'ocn'):
        gdir="%s/ncep/ukm/grf/archive/%s"%(wxdFtp,dtg)
    elif(model == 'ukm'):
        gdir="%s/ncep/ukm/grf/archive/%s"%(wxdFtp,dtg)
    elif(model == 'gsm'):
        gdir="%s/jma/gsm/grf/archive/%s"%(wxdFtp,dtg)

    return(gdir)

def ModelHtmDir(model,dtg):
    if(model == 'ngp'):
        hdir="%s/ngp/archive/%s"%(wxhWeb,dtg)
    elif(model == 'ngp05'):
        hdir="%s/ngp/archive/%s"%(wxhWeb,dtg)
    elif(model == 'ocn'):
        hdir="%s/ngp/archive/%s"%(wxhWeb,dtg)
    elif(model == 'gfs'):
        hdir="%s/gfs/archive/%s"%(wxhWeb,dtg)
    elif(model == 'ukm'):
        hdir="%s/ukm/archive/%s"%(wxhWeb,dtg)
    elif(model == 'gsm'):
        hdir="%s/gsm/archive/%s"%(wxhWeb,dtg)
    elif(model == 'sst'):
        hdir="%s/ngp/archive/%s/ngp.sst.000.tropwpac.htm"%(wxhWeb,dtg)

    return(hdir)



def R1ClimoPrc(bdtg,edtg,uapath,vapath,verb=0,ndy=R1ClimoNday,override=0):

    cdir=R1ClimoDatDir
    byr=R1ClimoByear
    eyr=R1ClimoEyear

    odir="%s/%s/%s"%(W2BaseDirDat,'nwp','climo')

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
    dpath=odir+"/%s"%(dfile)

    if(not(override) and MF.ChkPath(dpath)):
        print 'WWW dpath: ',dpath,' already there...'
        return(0)

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


def SetNcdcGdasData(dtg,model='gdas',source='ncdc'):

    hh=dtg[8:]
    yymmdd=dtg[0:8]
    yymm=dtg[0:6]

    if(source == 'ncdc'):
        ftpserver=NcdcGdasFtpserver

    idir=NcdcGdasIdir
    if(model == 'gdas'):
        if(source == 'ncdc'):
            doclean=0
            sdir="%s/rh%s"%(idir,yymmdd)
            grbsiz=100700000
            imask="%s1.t%sz.rh%s.*"%(model,hh,yymmdd)
            tdir="%s/%s"%(NcdcGdasPcmdi,yymm)
            mf.ChkDir(tdir,'mk')


    return(ftpserver,tdir,sdir,imask,grbsiz,doclean)

def SetNasaFldData(dtg,model,source='pcmdi'):

    hh=dtg[8:]
    yymmddhh=dtg[2:]

    if(source == 'pcmdi'):
        ftpserver=NasaFldFtpserver
    elif(source == 'nasa'):
        ftpserver='sprite.llnl.gov'

    idir=NasaFldIdir
    if(model == 'fg4'):
        if(source == 'pcmdi'):
            doclean=1
            sdir=idir
            grbsiz=96552288
            imask="%s.*.%s.*"%(model,dtg)
            tdir=NwpDataBdir(model)

        elif(source == 'nasa'):
            doclean=0
            sdir='unknown'
            grbsiz=0
            imask="%s.*.%s.*"%(model,dtg)
            tdir=W2DatNasaDir

        dfile="%s.12.%s.grb"%(model,dtg)
        alldonepath="%s/alldone/alldone.%s.12.%s"%(idir,model,dtg)

    fipath="/tmp/f.jma.%s.%s.txt"%(model,dtg)
    fipathchk="/tmp/f.check.jma.%s.%s.txt"%(model,dtg)

    return(ftpserver,tdir,sdir,imask,grbsiz,doclean)


def SetNcepJtwcData(dtg,model,source='ncep'):

    ftpserver=NcepJtwcFtpserver

    if(source == 'pcmdi'):
        ftpserver='sprite.llnl.gov'

    idir=NwpDataBdir(model)

    if(model == 'gfs'):

        if(source == 'ncep'):
            sdir='/pub/data2/JTWC/gfs'
            ifile="gfs.10.%s.jtwc_grb"%(dtg)
        else:
            sdir='/pub/fiorino/jtwc'
            ifile="gfs.10.%s.grb"%(dtg)
            ifile="gfs.10.%s.jtwc_grb"%(dtg)

        dfile="%s.jtwc.10.%s.grb"%(model,dtg)
        alldonepath="%s/alldone/alldone.%s.10.%s"%(idir,model,dtg)

    elif(model == 'ukm'):
        if(source == 'ncep'):
            sdir='/pub/data2/JTWC/ukmet'
            ifile="ukmet.12.%s.jtwc_grb"%(dtg)
        else:
            sdir='/pub/fiorino/jtwc'
            ifile="ukm.12.%s.grb"%(dtg)
            ifile="ukmet.12.%s.jtwc_grb"%(dtg)
        dfile="%s.jtwc.12.%s.grb"%(model,dtg)
        alldonepath="%s/alldone/alldone.%s.12.%s"%(idir,model,dtg)

    else:
        print "EEE invalid model: %"%(model)
        sys.exit()

    fipath="/tmp/f.ncep.jtwc.%s.%s.txt"%(model,dtg)
    fipathchk="/tmp/f.check.ncep.jtwc.%s.%s.txt"%(model,dtg)

    return(ftpserver,idir,sdir,ifile,dfile,fipath,fipathchk,alldonepath)


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



def GetW2Dtgs(curdtg,verb=0):

    dtgs={}
    models=wxModels
    models.append('sst')

    for model in wxModels:

        tdtg=curdtg
        ok=0
        n=0
        nmax=8
        while(ok == 0 and n <= nmax):
            tdir=ModelHtmDir(model,tdtg)
            tdir=ModelGrfDir(model,tdtg)
            chkmethod=os.path.isdir
            if(model == 'sst'): chkmethod=os.path.exists

            if(chkmethod(tdir)):
                if(verb): print 'YYYY ',tdir,tdtg,n
                dtgs[model]=tdtg
                ok=1
            else:
                tdtg=mf.dtginc(tdtg,-6)
                n=n+1

        if(n >= nmax):
            dtgs[model]=curdtg
            print 'eeeeeeeee ',n,tdtg

    return(dtgs)


def w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj):

    i=(wi-wi0)/dwi + 0.5
    j=(wj-wj0)/dwj + 0.5

    #
    # cyclic continuity in x
    #

    if(i <  0.0): i=float(ni)+i
    if(i >   ni): i=i-float(ni)

    i=int(i+1.0)
    j=int(j+1.0)

    return(i,j)

#ggggggggggggggggggggggggggggggggggggggggggggggggggggggg
#
#  land-frac binary data array created by p.lf.navy.geog.dat.gs
#
#lllllllllllllllllllllllllllllllllllllllllllllllllllllll


def SetLandFrac(lfres='1deg',ni=720,nj=361):

    lf=array.array('f')
    gdir=GeogDatDirW2
    lfres='1deg'

    lfpath="%s/lf.%s.dat"%(gdir,lfres)

    LF=open(lfpath,'rb')
    nij=ni*nj

    lf.fromfile(LF,nij)

    return(lf)

#
#  return land frac given lat/lon; note defaults; same as used by .gs
#

def GetLandFrac(lf,tlat,tlon,ni=720,nj=361,blat=-90.0,blon=0.0,dlat=0.5,dlon=0.5):

    (i,j)=w2ij(tlon,tlat,ni,nj,blon,blat,dlon,dlat)
    ij=(j-1)*ni+i-1
    #print 'ij ',ij,lf[ij]
    return(lf[ij])


def IsFldDataThere(model,dtg,tdiropt=None,cagips=0,verb=0):


    if(IsModel2(model)):
        (rc,minfracreq)=Model2IsReady2Plot(model,dtg)
        return(rc)

    print 'ddddddddddddd------------ ',W2BaseDirDat

    def getlocaldir(tdiropt=None):

        (ftpserver,remotedir,localdir,localarchdir,
         mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

        if(tdiropt != None):
            localdir="%s/%s"%(tdiropt,dtg)
            mf.ChkDir(localdir,'mk')

        return(localdir)


    def getdatpath(tdiropt=None):

        sdir=getlocaldir(tdiropt)

        res=ModelRes(model)

        if(cagips):
            datpath="%s/%s.%s.cagips.%s.grb"%(sdir,model,res,dtg)
        else:
            datpath="%s/%s.%s.%s.grb"%(sdir,model,res,dtg)

        return(datpath)



    dtghh=dtg[8:10]
    datpath=getdatpath(tdiropt)

    if(os.path.exists(datpath)):
        siz=os.path.getsize(datpath)
        sizmin=ModelMinGrbSiz(model,dtghh)
        if(verb): print 'IsFldDataThere: siz,sizmin: ',siz,sizmin
        if(siz > sizmin):
            return(1)
        else:
            return(999)

    else:
        if(tdiropt != None):
            rc=IsFldDataThere(model,dtg)
            #
            # copy over from local, real-time to target dir
            #
            if(rc == 1):
                datpath=getdatpath()
                cmd="cp %s %s/%s/."%(datpath,tdiropt,dtg)
                mf.runcmd(cmd)
                rc=2
            else:
                rc=0
        else:
            rc=0
        return(rc)


def IsFldDataArchive(model,dtg,tdiropt=None,cagips=0,verb=0):

    dtghh=dtg[8:10]

    if(IsModel2(model)):
        rc=0
        (localpaths,localarchpaths)=Model2LocalArchivePaths(model,dtg)
        for path in localarchpaths:
            if(os.path.exists(path)): rc=1
        return(rc)



    (ftpserver,remotedir,ocaldir,localarchdir,
     mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

    if(tdiropt != None):
        localdir="%s/%s"%(tdiropt,dtg)
        mf.ChkDir(localdir,'mk')


    res=ModelRes(model)
    if(cagips):
        datpath="%s/%s.%s.cagips.%s.grb"%(localarchdir,model,res,dtg)
    else:
        datpath="%s/%s.%s.%s.grb"%(localarchdir,model,res,dtg)
        datmask="%s/%s.%s.%s.*"%(localarchdir,model,res,dtg)

    if(verb):
        print 'IsFldDataArchive datpath ',datpath

    if(os.path.exists(datpath)):
        siz=os.path.getsize(datpath)
        sizmin=ModelMinGrbSiz(model,dtghh)
        if(verb): print siz,sizmin
        if(siz > sizmin):
            return(1)
        else:
            return(999)

    else:
        return(0)

def RecoverFldDataArchive2Local(model,dtg,tdiropt=None,cagips=0,verb=0):

    if(IsModel2(model)):
        (localpaths,localarchpaths)=Model2LocalArchivePaths(model,dtg)
        return(rc)


    dtghh=dtg[8:10]

    (ftpserver,remotedir,localdir,localarchdir,
     mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

    if(tdiropt != None):
        localdir="%s/%s"%(tdiropt,dtg)
        mf.ChkDir(localdir,'mk')

    cmd="cp %s/%s %s"%(localarchdir,mask,localdir)
    mf.runcmd(cmd)

    return(1)

def RecoverFldDataRemote2Local(model,dtg,tdiropt=None,cagips=0,verb=0):

    (ftpserver,remotedir,localdir,localarchdir,
     mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

    if(tdiropt != None):
        localdir="%s/%s"%(tdiropt,dtg)
        mf.ChkDir(localdir,'mk')

    rc=mf.doFTPsimple(ftpserver,localdir,remotedir,mask,'ftp.get',doitout=0)

    return(1)



def RemoveRecoveredFldDataLocal(model,dtg,cagips=0,verb=0):

    dtghh=dtg[8:10]

    (ftpserver,remotedir,localdir,localarchdir,
     mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

    cmd="rm %s/%s"%(localdir,mask)
    mf.runcmd(cmd)

    return(1)



def IsFldDataRemote(model,dtg,tdiropt=None,verb=0):


    if(IsModel2(model)):
        rc=0
        return(rc)

    (ftpserver,remotedir,localdir,localarchdir,
     mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

    dtghh=dtg[8:10]
    grbsizmin=ModelMinGrbSiz(model,dtghh)

    if(tdiropt != None):
        localdir="%s/%s"%(tdiropt,dtg)
        mf.ChkDir(localdir,'mk')


    rc=mf.doFTPsimple(ftpserver,localdir,remotedir,mask,'ftp.ls',doitout=1)
    nrc=len(rc)
    isthere=-1
    isrightsiz=-1
    iok=0

    siz=-999
    if(nrc >= 3):
        for r in rc:
            if(verb): print 'rrrrrrrrrrrrrr ',r[:-1]
            if(mf.find(r,'.grb')):
                tt=r.split()
                siz=int(tt[4])
                isthere=1
            elif(mf.find(r,'No such file')):
                isthere=0
    else:
        isthere=-1

    if(siz >= grbsizmin): isrightsiz=1

    if(isthere == 1 and isrightsiz == 1): iok=1

    if(verb): print 'nrc ',nrc,iok,isthere,isrightsiz,siz,grbsizmin
    return(iok)


def IsFldDataLocal(model,dtg,verb=0):

    (ftpserver,remotedir,localdir,localarchdir,
     mask,renmask,modelrename)=ModelArchiveDirs(model,dtg)

    dtghh=dtg[8:10]
    grbsizmin=ModelMinGrbSiz(model,dtghh)

    rc=mf.doFTPsimple(ftpserver,localdir,remotedir,mask,'local.ls',doitout=1)

    nrc=len(rc)
    isthere=-1
    isrightsiz=-1
    iok=0

    siz=-999
    if(nrc >= 3):
        for r in rc:
            if(verb): print 'llllllllllll ',r[:-1]
            if(mf.find(r,'.grb')):
                tt=r.split()
                siz=int(tt[4])
                isthere=1
            elif(mf.find(r,'No such file')):
                isthere=0
    else:
        isthere=-1

    if(siz >= grbsizmin): isrightsiz=1

    if(isthere == 1 and isrightsiz == 1): iok=1
    if(verb): print 'nrc ',nrc,iok,isthere,isrightsiz,siz,grbsizmin
    return(iok)

def IsCagipsOnlyModel(model):

    rc=0
    for cmodel in w2DatCagipsOnlyModels:
        if(model == cmodel): rc=1

    return(rc)


def IsNogapsCagips(model,dtg):

    ddirs=ModelArchiveDirs(model,dtg)
    ddir=ddirs[2]
    dmask="%s*%s*%s*.grb"%(model,ModelRes(model),dtg)
    dfiles=glob.glob("%s/%s"%(ddir,dmask))
    rc=0
    for dfile in dfiles:
        if(mf.find(dfile,'cagips')): rc=1

    return(rc)


def WriteList2File(path,list):

    O=open(path,'w')
    for l in list:
        O.writelines(l+'\n')
    O.close()

def AppendList2File(path,list):

    try:
        O=open(path,'a')
    except:
        print 'Appendlist2File: unable to open: ',path
        return

    for l in list:
        O.writelines(l+'\n')
    O.close()

def WriteString2File(path,string):

    O=open(path,'w')
    O.writelines(string)
    O.close()

def WriteHash2File(path,hash):

    keys=hash.keys()
    keys.sort()

    O=open(path,'w')
    for key in keys:
        O.writelines(hash[key]+'\n')
    O.close()


def GetKeys(hash,title='keys',verb=0):
    ks=hash.keys()
    if(verb):
        print "keys ",title
        for k in ks:
            print k
    return(ks)

def PrintFirstListHash(ks,listhash):
    k=ks[0]
    print 'k0: ',k
    for card in listhash[k]:
        print card
    return

def PrintFirstHash(ks,hash):
    k=ks[0]
    print 'k1 ',k
    print hash[k]
    return

def GetModelsFromModopt(modopt):

    tt=modopt.split('.')
    if(len(tt) >= 2):
        models=tt
        nmodels=len(tt)
    elif(len(tt) == 1):
        models=[modopt]
        nmodels=1
    else:
        print 'EEEE w2.GetModelsFromModopt :: invalid modopt: ',modopt
        sys.exit()

    return(models)


def GetLogLatest(type,dtg):

    masktype=type
    if(type == 'tcstatus'):
        masktype='tc'

    logdir="%s/%s/%s"%(W2BaseDirLog,type,dtg)
    logs=glob.glob("%s/%s.*"%(logdir,masktype))
    ocards={}
    cards=[]

    if(len(logs) == 0):
        #
        # go back -6 h
        #
        dtgm6=mf.dtginc(dtg,-6)
        print 'LLLLL going back -6 h from: ',dtg,' to ',dtgm6
        logdir="%s/%s/%s"%(W2BaseDirLog,type,dtgm6)
        logs=glob.glob("%s/%s.*"%(logdir,masktype))

    if(len(logs) > 0):
        logs.sort()
        for log in logs:
            cards=open(log).readlines()
            for card in cards:
                file=card.split()[0]
                ocards[file]=card

        files=ocards.keys()
        files.sort()

        for file in files:
            cards.append(ocards[file])

    else:
        cards=None

    return(cards)


def GetLatestTcStatusLog(dtg):

    type='tcstatus'
    masktype='tc'

    logdir="%s/%s/%s"%(W2BaseDirLog,type,dtg)
    logs=glob.glob("%s/%s.*"%(logdir,masktype))
    ocards={}
    cards=[]

    if(len(logs) == 0):
        #
        # go back -6 h
        #
        dtgm6=mf.dtginc(dtg,-6)
        print 'LLLLL going back -6 h from: ',dtg,' to ',dtgm6
        logdir="%s/%s/%s"%(W2BaseDirLog,type,dtgm6)
        logs=glob.glob("%s/%s.*"%(logdir,masktype))

    if(len(logs) > 0):
        logs.sort()
        logfile=logs[-1]
        print 'lllll ',logfile
        cards=open(logfile).readlines()

    else:
        cards=None

    return(cards)


def GetSynHour(dtg):
    hh=synhour=dtg[8:]
    ihh=int(hh)
    return(hh,ihh)


def cpTcvitals(dtgs,ropt='',verb=0):

    from types import ListType

    tvdir="%s/tc/tcvitals"%(W2BaseDirDat)
    tdssdir="%s/tc/DSs"%(W2BaseDirDat)

    w3tdir=TcvitalsDirW3

    #
    # tcvitals -- local and then scp to jet
    #

    if( not(type(dtgs) is ListType) ):
        dtgs=[dtgs]

    for dtg in dtgs:
        year=dtg[0:4]
        tvpath="%s/tcvitals.%s.txt"%(tvdir,dtg)
        cmd="w2-tc-posit.py %s -v %s"%(dtg,tvpath)
        mf.runcmd(cmd,ropt)

        if(W2doWjet):
            cmd="scp %s fiorino@%s:/lfs0/projects/fim/tcvitals/."%(tvpath,WjetScpServer)
            mf.runcmd(cmd,ropt)

            cmd="scp %s fiorino@%s:/lfs0/projects/rtfim/tcvitals/."%(tvpath,WjetScpServer)
            mf.runcmd(cmd,ropt)

        if(W2doW3Rapb):
            cmd="cp %s  %s/."%(tvpath,w3tdir)
            mf.runcmd(cmd,ropt)


    return

def cpReftrk2W3(dtgs,ropt='',verb=0):

    from types import ListType

    w3tdir=TcvitalsDirW3
    if( not(type(dtgs) is ListType) ):
        dtgs=[dtgs]

    for dtg in dtgs:
        year=dtg[0:4]
        sdir="%s/%s"%(TcRefTrkDatDir,year)
        if(W2doW3Rapb):
            cmd="cp -p %s/*%s* %s/."%(sdir,dtg,w3tdir)
            mf.runcmd(cmd,ropt)
        if(W2doWjet):
####            cmd="scp %s/*%s* fiorino@%s:/lfs2/projects/rtfim/tcvitals/."%(sdir,dtg,WjetScpServer)
            cmd="scp %s/*%s* fiorino@%s:/lfs1/projects/rtfim/tcvitals/."%(sdir,dtg,WjetScpServer)
            mf.runcmd(cmd,ropt)

    return

def cpBdecks2W3(dtgopt,ropt='',verb=1):

    #if(not(W2doW3Rapb)): return

    from BD import Bdeck
    #
    # put bdecks to /w3/rapb/fiorino/bdeck
    # put bdecks to $W2_HFIP/fiorino/bdeck
    #
    b=Bdeck(dtgopt=dtgopt,verb=verb)
    w3tdir=TcBdecksDirW3

    bdtgs=b.dtgs
    stmids=b.curbdecks.keys()

    bdtgs.sort()
    stmids.sort()

    for bdtg in bdtgs:
        for stmid in stmids:
            bdeck=b.curbdecks[stmid]
            (dir,file)=os.path.split(bdeck)
            tpath="%s/%s.%s"%(w3tdir,bdtg,file)

            cmd="cp -p %s %s"%(bdeck,tpath)
            mf.runcmd(cmd,ropt)

            cmd="cp -p %s %s/."%(bdeck,w3tdir)
            mf.runcmd(cmd,ropt)

    return


if (__name__ == "__main__"):

    narg=len(sys.argv)-1


    if(narg == 2):
        dtgopt=sys.argv[1]
        model=sys.argv[2]
    else:
        print 'invoke w2.py dtg model'
        sys.exit()

    dtgs=mf.dtg_dtgopt_prc(dtgopt)

    if(model == 'all'):
        models=wxModels2
    else:
        models=[model]

    for dtg in dtgs:
        for model in models:
            (rc,latesttau)=Model2DataPathsStatus(model,dtg,doreport=1)
            print 'llll latesttau ',latesttau
