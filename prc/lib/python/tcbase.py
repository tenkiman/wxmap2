from WxMAP2 import *
w2=W2()

#from ATCF import IsWindRadii,WindRadiiCode2Normal,TrkModeltoBattributes


TcCarqDatDir=w2.TcCarqDatDir
TcDataBdir=w2.TcDatDir
W2BaseDirDat=w2.W2BaseDirDat
TcNamesDatDir=w2.TcNamesDatDir
SetLandFrac=w2.SetLandFrac
GetLandFrac=w2.GetLandFrac
WjetScpServer=w2.WjetScpServer
WjetScpServerLogin=w2.WjetScpServerLogin
ZeusScpServer=w2.ZeusScpServer
W2doW3Rapb=w2.W2doW3Rapb
TcvitalsDirW3=w2.TcvitalsDirW3
TcCarqDatDir=w2.TcCarqDatDir
SetLandFrac=w2.SetLandFrac
TcBtNeumannDatDir=w2.TcBtNeumannDatDir
TcBtOpsDatDir=w2.TcBtOpsDatDir
TcBtDatDir=w2.TcBtDatDir
TcMdecksFinalDir=w2.TcMdecksFinalDir
GetLandFrac=w2.GetLandFrac
TcBtDatDir=w2.TcBtDatDir
TcAdecksFinalDir=w2.TcAdecksFinalDir
PrcDirTctrkW2=w2.PrcDirTctrkW2
PrcBdirW2=w2.PrcBdirW2

Nhc2JtwcFtpServer='moonfish.nhc.noaa.gov'

icharA=97
undef=-999
maxNNnum=60
maxNNnum=49


#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# vars

# -- 
BaseDirWWW=w2.W2BaseDirWeb
BaseDirWWWTcSitrep=BaseDirWWW+'/tc/sitrep'
BaseDirWWWTcSitrep='/w3/rapb/hfip/tcact'
BaseDirWWWTcSitrep='%s/tcact'%(w2.HfipProducts)

BaseDirPltTc=w2.TcBaseDirPltTc
PltTcOpsDir="%s/ops"%(BaseDirPltTc)
RptDir=w2.W2BaseDir + "/rpt"

TrkModels=['ofc','clp','gfs','ngp','ukm','eco','ece','btk','fv4','fv5','con','fg4','fd5',
           'egr','ofi','cn3','cn4','cne','cnf','pne','gfd']


BaseDirDataTc=TcDataBdir
BaseDirPrcTcDat=w2.PrcDirTcdatW2
JtwcBaseDir="%s/jtwc"%(TcDataBdir)
NhcBaseDir="%s/nhc"%(TcDataBdir)
TcAdecksNhcDir="%s/adeck/nhc"%(TcDataBdir)
TcAdecksLocalDir="%s/adeck/local"%(TcDataBdir)
TcAdecksJtwcDir="%s/adeck/jtwc"%(TcDataBdir)
TcBdecksNhcDir="%s/bdeck/nhc"%(TcDataBdir)
TcBdecksJtwcDir="%s/bdeck/jtwc"%(TcDataBdir)
TcBdecksNhcDir2="%s/bdeck2/nhc"%(TcDataBdir)
TcBdecksJtwcDir2="%s/bdeck2/jtwc"%(TcDataBdir)
TcAdecksEsrlDir="%s/adeck/esrl"%(TcDataBdir)
TcAdecksEcmwfDir="%s/adeck/ecmwf"%(TcDataBdir)
TcAdecksCmcDir="%s/adeck/cmc"%(TcDataBdir)
TcAdecksClipDir="%s/adeck/clip"%(TcDataBdir)
TcAdecksUkmoDir="%s/adeck/ukmo"%(TcDataBdir)
TcAdecksAtcfFormDir="%s/adeck/atcf-form"%(TcDataBdir)
TcAdecksNcepDir="%s/adeck/ncep"%(TcDataBdir)
TcAdecksHrdDir="%s/adeck/hrd"%(TcDataBdir)
TcAdecksMftrkNDir="%s/adeck/mftrkN"%(TcDataBdir)
TcAdecksTmtrkNDir="%s/adeck/tmtrkN"%(TcDataBdir)
TcAdecksPsdRR2Dir="%s/adeck/psdRR2"%(TcDataBdir)
TcAdecksEraiDir="%s/adeck/erai/adeck-stm"%(TcDataBdir)
TcAdecksEra5Dir="%s/adeck/era5/adeck-stm"%(TcDataBdir)
TcRefTrkDatDir="%s/reftrk"%(TcDataBdir)
TcTmtrkNDir="%s/tmtrkN"%(TcDataBdir)
TcVitalsDatDir="%s/tcvitals"%(TcDataBdir)
TcGenDatDir="%s/tcgen"%(TcDataBdir)
TcDiagDatDir="%s/tcdiag"%(TcDataBdir)
TcDiagDatDir0="%s/tcdiag0"%(TcDataBdir)



TcEcmwfBaseDir="%s/ecmwf"%(TcDataBdir)
EcmwfBufrLocalDir=TcEcmwfBaseDir + '/ecbufr'
EcmwfWmoBufrLocalDir=TcEcmwfBaseDir + '/wmo-essential'
EcmwfBufrJetDir=W2BaseDirDat + '/ecnogaps/ecbufr'

TcObsMtcswaSourceDir="%s/cira/mtcswa"%(TcDataBdir)
TcObsSatWindsDir="%s/obs/satwinds"%(TcDataBdir)

TcDssbdir="%s/DSs"%(TcDataBdir)

MdeckBaseDir="%s/mdeck"%(TcDataBdir)
AdeckBaseDir="%s/adeck"%(TcDataBdir)
VdeckBaseDir="%s/adeck"%(TcDataBdir)

W2fldsBaseDir="%s/nwp2/w2flds"%(W2BaseDirDat)

MdeckDir=MdeckBaseDir
VdeckDir=VdeckBaseDir

eBdeckDir=TcDataBdir + "/ebt"

Md2Dbname='mdecks2a'
Md2Dbname='mdecks2'
MdDbname='mdecks'

BD2dbname='bd2'
AD2dbname='ad2'
MD2dbname='md2'
VD2dbname='vd2'

xsizeTcTrk=1200

# -- import here because vars above are needed below
#
from tcCL import * # imports tcVM
from adCL import * # import adVM which imports tcVM
