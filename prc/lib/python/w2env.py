from M import *
import mf
MF=MFutils()

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# env
#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

class W2env(MFbase):

    W2_OPS=1
    W2_CLEAN_NDAY=10
    W2_CLEAN_NDAY_DAT=5

    W2_USE_NGP_LDM=1

    W2_USE_RSYNC=1
    W2_USE_RSYNC=0

    curdtg=mf.dtg()

    W2_CUR_YEAR=curdtg[0:4]
    # 20070507 -- change over to nhem
    CurTcSeason='NHEM'
    # 20071204 -- switch to shem season
    CurTcSeason='SHEM'

    # 20080524 -- switch to nhem season
    CurTcSeason='NHEM'

    # 20090326 -- switch to nhem season
    CurTcSeason='SHEM'

    # 20090503 -- switch to nhem season
    CurTcSeason='NHEM'

    # 20091227 -- switch to shem season
    CurTcSeason='SHEM'

    W2_BDIR=os.getenv("W2_BDIR")
    W2_BDIRDAT=os.getenv("W2_BDIRDAT")
    W2_BDIRPLT=os.getenv("W2_BDIRPLT")
    W2_BDIRWEB=os.getenv("W2_BDIRWEB")
    W2_BDIRWEBA=os.getenv("W2_BDIRWEBA")
    W2_PERL_DIR=os.getenv("W2_PERL_DIR")
    W2_PRC_W2_DIR=os.getenv("W2_PRC_W2_DIR")
    W2_PRC_TC_DIR=os.getenv("W2_PRC_TC_DIR")

    W2_PROD_CENTER="NPMOC/JTWC"
    W2_PROD_CENTER="FNMOC"

    W2_NWP_DATA_DIR="/dat/nwp/dat"
    W2_FTP_BDIR="/dat/nwp/wxmap/ftp"

    W2_FTP_INCOMING_FNMOC_REMOTE_DIR="/comms_dir/ddn/fnoc"
    W2_FTP_INCOMING_FNMOC_REMOTE_SPRITE_DIR="/pub/fiorino/tmp"
    W2_FTP_INCOMING_NCEP_REMOTE_DIR="/comms_dir/ddn/fnoc/ncep"
    W2_FTP_INCOMING_LLNL_NGTRP_REMOTE_DIR="/comms_dir/llnl/ngtrp"
    W2_FTP_INCOMING_LLNL_NGP_REMOTE_DIR="/comms_dir/llnl/ngp"
    W2_FTP_INCOMING_JTWC_REMOTE_DIR="/opt/DEVELOPMENT/atcf/fnmocin"
    W2_FTP_INCOMING_JTWC_REMOTE_ARCHIVE_DIR="/opt/DEVELOPMENT/atcf/archives"

    W2_FTP_INCOMING_BDIR=W2_FTP_BDIR+'/incoming'
    W2_LDM_INCOMING_BDIR="/dat/ldmincoming"
    W2_DAT_BDIR="/dat/nwp"



    W2_METGRAM_PRC_DIR=W2_BDIR+'/prc/metgram'
    W2_METGRAM_PLT_DIR=W2_BDIR+'/plt/metgram'

    W2_FTPDIR_FNMOC="/pub/fiorino/fnmoc/dat"
    W2_FTPDIR_NCEP="/pub/fiorino/ncep/dat"

    W2_GEODIR=W2_BDIRDAT+'/geog'
    W2_CLIMOSST=W2_BDIRDAT+'/climo/sst'
    W2_CLIMODAT=W2_BDIRDAT+'/nwp/climo'

    W2_PRC_HTML_DIR=W2_BDIR+'/prc/html'
    W2_PRC_DAT_DIR=W2_BDIR+'/prc/dat'
    W2_JUNK_FILE='/tmp/wxmap.zy0x1w2.tmp'

    W2_BASEMAP_GDIR=W2_BDIRPLT+'/basemap'

    ##################################################
    #
    #	HTML
    #
    ##################################################

    W2_HTML_BASE= "wxmap"                   # 970707 change to the op dirs

    W2_HTML_BASE_DOC= "wxmap/doc"

    W2_HTML_BASE_CLASSES= "wxmap/classes"

    W2_HTML_BASE_GRF= "fiorino/wxmap/grf"

    W2_HTML_BASE_HREF= 'http://wxmap2'

    W2_HTML_BASE_ICON= 'icon'

    W2_HTML_BASE= '../..'

    W2_HTML_BASE_TOP= '.'

    W2_HTML_BASE_DOC= '../../doc'
    W2_HTML_BASE_CLASSES= '../../classes'
    W2_HTML_BASE_GRF= '../../grf'
    W2_HTML_BASE_ICON= '../../icon'

    W2_HTML_BASE_DOC_TOP= 'doc'
    W2_HTML_BASE_CLASSES_TOP= 'classes'
    W2_HTML_BASE_GRF_TOP= 'grf'
    W2_HTML_BASE_ICON_TOP= 'icon'

    W2_WEB_DIR="/dat/nwp/wxmap/web"  # 970707 change to the op dirs
    W2_WEB_DIR="/data/rapb/projects/wxmap2"  # 20130418 -- real dir to server 
    W2_ICON_DIR=W2_WEB_DIR+'/icon'

    W2_PLOT_XSIZE=900

    ###################################################
    #
    #	AREA PROPERTIES
    #	JTWC
    #
    ###################################################

    #----------------------------------------------------------------------
    #  shem TC season
    #----------------------------------------------------------------------

    #
    # mf 20061202: added shem 2007 areas on
    # mf 20080123: put asia back
    #
    W2_AREAS = [
        'asia',
        #'wconus',   # -- 20170225 - turn off plotting since tropical ENSO on main page
        'conus',
    #    'europe',
        'nhem',
        'tropwpac',
        'tropnio',
        'tropepac',
        'troplant',
        'tropsio',
        'tropoz',
    #    'tropenso',
        'tropswpac',
        ]
    # -- 20200321 -- reduce for wxmap2.com
    #
    W2_AREAS = [
         'asia',      # -- 20200723 -- turn on with JMA GSM
         #'wconus',   # -- 20170225 - turn off plotting since tropical ENSO on main page
         'conus',
         #'europe',
         #'nhem',
         'tropwpac',
         #'tropnio',
         'tropepac',
         'troplant',
         #'tropsio',
         #'tropoz',
         #'tropenso',
         #'tropswpac',
         ]

    W2_AREAS_TYPES = {
        'asia':'midlat',
        'wconus':'midlat',
        'conus':'midlat',
        'europe':'midlat',
        'nhem':'midlat',
        'bigaus':'special',
        'tropwpac':'tropic',
        'tropnio':'tropic',
        'tropsio':'tropic',
        'tropoz':'tropic',
        'tropenso':'tropic',
        'tropswpac':'tropic',
        'tropepac':'tropic',
        'troplant':'tropic',
        }

    W2_AREAS_DESC = {
        'asia':'East Asia',
        'wconus':'WConus',
        'conus':'Conus',
        'europe':'Europe',
        'nhem':'NHEM',
        'bigaus':'Big Aus',
        'tropwpac':'Tropical WPAC',
        'tropnio':'Tropic NIO',
        'tropsio':'Tropical SIO',
        'tropoz':'Tropical Oz',
        'tropswpac':'Tropical SWPAC',
        'tropepac':'Tropical EPAC',
        'troplant':'Tropical LANT',
        }

    W2_AREAS_CLIMO = [
        'jtwcaor',
        'nhcaor',
        ]

    W2_PLOT_TYPES="midlat:special:tropic"
    W2_PLOT_TYPES_PLOTS="500 prp:uas shr u50 prp:uas prp 500"
    W2_PLOT_TYPES_TAUS="default:default:default:0 240 24"


    ###################################################
    #
    #	MODEL PROPERTIES
    #       JTWC
    #
    ###################################################


    W2_MODELS_CURRENT_GRFDIR={

        'gfs':"%s/plt_ncep_gfs"%(W2_BDIRWEB),
        'fim':"%s/plt_esrl_fim"%(W2_BDIRWEB),
       
        'fv3e':"%s/plt_esrl_fv3e"%(W2_BDIRWEB),
        'fv3g':"%s/plt_esrl_fv3g"%(W2_BDIRWEB),
  
        'ngp':"%s/plt_fnmoc_ngp"%(W2_BDIRWEB),
        'ngp05':"%s/plt_fnmoc_ngp"%(W2_BDIRWEB),
        'ukm':"%s/plt_ukmo_ukm"%(W2_BDIRWEB),
        'ocn':"%s/plt_fnmoc_ocn"%(W2_BDIRWEB),
        'ecm':"%s/plt_ecmwf_ecm"%(W2_BDIRWEB),
        'cmc':"%s/plt_cmc_cmc"%(W2_BDIRWEB),
        'cgd2':"%s/plt_cmc_cmc"%(W2_BDIRWEB),

        'gfs2':"%s/plt_ncep_gfs"%(W2_BDIRWEB),
        'fim8':"%s/plt_esrl_fim"%(W2_BDIRWEB),
        'fimx':"%s/plt_esrl_fimx"%(W2_BDIRWEB),
        'ukm2':"%s/plt_ukmo_ukm"%(W2_BDIRWEB),
        'ecm2':"%s/plt_ecmwf_ecm"%(W2_BDIRWEB),
        'ecm4':"%s/plt_ecmwf_ecm"%(W2_BDIRWEB),
        'ecm5':"%s/plt_ecmwf_ecm"%(W2_BDIRWEB),
        'jgsm':"%s/plt_jma_gsm"%(W2_BDIRWEB),

        'cgd2':"%s/plt_cmc_cmc"%(W2_BDIRWEB),
        
        'ecmt':"%s/plt_ecmwf_ecm"%(W2_BDIRWEB),
        'gfsk':"%s/plt_esrl_gfsk"%(W2_BDIRWEB),
        'ecmn':"%s/plt_ecmwf_ecm"%(W2_BDIRWEB),
        'ecmg':"%s/plt_ecmwf_ecmg"%(W2_BDIRWEB),
        'ngp2':"%s/plt_fnmoc_ngp"%(W2_BDIRWEB),
        'ngpc':"%s/plt_fnmoc_ngpc"%(W2_BDIRWEB),
        'navg':"%s/plt_fnmoc_navg"%(W2_BDIRWEB),
        'cmc2':"%s/plt_cmc_cmc"%(W2_BDIRWEB),

        'gfsc':"%s/plt_ncep_gfsc"%(W2_BDIRWEB),
        'ngpj':"%s/plt_fnmoc_ngpj"%(W2_BDIRWEB),
        'ukmc':"%s/plt_ukmo_ukmc"%(W2_BDIRWEB),
        'jmac':"%s/plt_jma_jmac"%(W2_BDIRWEB),
        
        }

    W2_MODELS=[
        'gfs',
        'ngp',
        'ngp05',
        'ukm',
        'ocn',
        'ecm',
        'cmc',
        ]

    W2_MODELS2=[
        'gfs2',
        'gfsc',
        'fim8',
        'fimx',
        'ngp2',
        'ngpc',
        'navg',
        'ukm2',
        'ecm2',
        'ecm4',
        'ecm5',
        'jgsm',
        'cgd2',
        
        'fv3e',
        'fv3g',
        
        'ecmt',
        'gfsk',
        'ecmn',
        'ecmg',
        ]

    W2_MODELS_RES={
        'gfs':'10',
        'gfs.jtwc':'10',
        'ngp':'10',
        'ngp05':'05',
        'ukm':'10',
        'ukm.jtwc':'12',
        'gsm':'12',
        'ocn':'10',
        'ecm':'10',
        'cmc':'10',
        
        'ecm2':'10',
        'ecm2':'05',
        'ecm4':'025',
        #
        
        'fv3e':'05',
        'fv3g':'05',
        
        'ecmt':'05',
        'ecmn':'10',
        'ecmg':'25',
        'ngp2':'10',
        'ngpc':'05',

        # -- 20200323 current model models
        #
        'gfs2':'025',
        'ecm5':'025',
        'jgsm':'125',
        'cgd2':'025',
        'navg':'05',

        }

    W2_MODELS_CENTER={
        'gfs':'ncep',
        'gfs.jtwc':'ncep',
        'ngp':'fnmoc',
        'ngp05':'fnmoc',
        'ukm':'ukmo',
        'ukm.jtwc':'ukmo',
        'gsm':'jma',
        'ocn':'fnmoc',
        'ecm':'ecmwf',
        'cmc':'cmc',

        'ecm2':'ecmwf',
        'ecm4':'ecmwf',
        'ecm5':'ecmwf',
        'jgsm':'jma',
        'cgd2':'cmc',

        'fv3e':'esrl',
        'fv3g':'esrl',
        
        'ecmt':'ecmwf',
        'ecmn':'ecmwf',
        'ecmg':'ecmwf',
        'ngp2':'fnmoc',
        'ngpc':'fnmoc',
        'navg':'fnmoc',

        }


    W2_MODELS_GRF_EXT='10'

    W2_MODELS_HTTP_GDIR={
        'gfs':'plt_ncep_gfs',
        'fim':'plt_esrl_fim',

        'fv3e':'plt_esrl_fv3e',
        'fv3g':'plt_esrl_fv3g',

        'ngp':'plt_fnmoc_ngp',
        'ngp05':'plt_fnmoc_ngp',
        'ukm':'plt_ukmo_ukm',
        'ocn':'plt_fnmoc_ocn',
        'gsm':'plt_jma_gsm',
        'ecm':'plt_ecmwf_ecm',
        'cmc':'plt_cmc_cmc',

        'ecm2':'plt_ecmwf_ecm',
        'ecmt':'plt_ecmwf_ecm',
        'ecmn':'plt_ecmwf_ecm',
        'ecmg':'plt_ecmwf_ecmg',
        'ecm4':'plt_ecmwf_ecm',
        'ecm5':'plt_ecmwf_ecm',
        'jgsm':'plt_jma_gsm',
        'cgd2':'plt_cmc_cmc',
        'ngp2':'plt_fnmoc_ngp',
        'ngpc':'plt_fnmoc_ngpc',
        'navg':'plt_fnmoc_navg',


        }

    W2_MODELS_DESC={
        'gfs':'NCEP GFS',
        'ngp':'FNMOC NOGAPS',
        'ngp05':'FNMOC NOGAPS(0.5d)',
        'ukm':'UKMO',
        'gsm':'JMA GSM',
        'ocn':'FNMOC OCN',
        
        'ecm':'ECMWF IFS',
        'ecm2':'ECMWF IFS',
        'ecm4':'ECMWF HRES',
        'ecm5':'ECMWF HRES',
        'jgsm':'JMA GSM',
        'cgd2':'CMC CGD',
        'ecmt':'ECMWF IFS',
        'ecmn':'ECMWF IFS',
        'ecmg':'ECMWF IFS',

        'fv3e':'ESRL FV3 NCEP',
        'fv3g':'ESRL FV3 GF',

        'ngp2':'FNMOC NOGAPS',
        'ngpc':'FNMOC NOGAPS',
        'navg':'FNMOC NAVGEM',


        }

    W2_MODELS_BKG={
        'gfs':'bkgred.gif',
        'fim':'bkgyello.gif',
        
        'fv3e':'bkgred.gif',
        'fv3g':'bkggreen.gif',
        
        'ngp':'bkgblue.gif',
        'ngp05':'bkgblue.gif',
        'ukm':'bkggreen.gif',
        'gsm':'bkgyello.gif',
        'ocn':'bkgyello.gif',
        'ocn':'bkgyello.gif',
        'ecm':'bkgyello.gif',
        'cmc':'bkgyello.gif',

        'ecm2':'bkgyello.gif',
        'ecm4':'bkgyello.gif',
        'ecm5':'bkgyello.gif',
        'jgsm':'bkgblue.gif',
        'cgd2':'bkgyello.gif',
        'ecmt':'bkgyello.gif',
        'ecmn':'bkgyello.gif',
        'ecmg':'bkgyello.gif',
        'ngp2':'bkgblue.gif',
        'ngpc':'bkgblue.gif',
        'navg':'bkgblue.gif',

        }

    W2_MODELS_Run00={
        'gfs':1,
        'ngp':1,
        'ngp05':1,
        'ukm':1,
        'gsm':1,
        'ocn':1,
        'ecm':1,
        'cmc':1,

        'fim8':1,
        'fimx':1,
        
        'rtfim':1,
        'rtfimx':1,
        'rtfimy':1,

        'gfs2':1,
        'ngp2':1,
        'ngpc':1,
        'navg':1,
        'ukm2':1,
        'ecm2':1,
        'ecm4':1,
        'era5':1,
        'ecm5':1,
        'jgsm':1,
        'cgd2':1,
        'ecmt':1,
        'ecmn':1,
        'ecmg':1,
        
        'cmc2':1,
        'cgd6':1,
        'cgd2':1,

        'gfsc':1,
        'ngpj':1,
        'ukmc':1,
        'jmac':1,

        'goes':1,
        
         'ocn':0,
         'ohc':1,
         'ww3':1,
        'mpas':1,
        'mpsg':1,
        
        'fv3e':1,
        'fv3g':1,

        'fv7e':1,
        'fv7g':1,

        'hwrf':1,
        
        }

    W2_MODELS_Run06={
        'gfs':1,
        'ngp':1,
        'ngp05':1,
        'ukm':0,
        'gsm':0,
        'ocn':0,
        'ecm':0,
        'cmc':0,

        'fim8':0,
        'fimx':0,

        'rtfim':0,
        'rtfimx':0,
        'rtfimy':0,

        'gfs2':1,
        'gfsc':1,
        'ngp2':0,
        'ngpc':1,
        'navg':1,
        'ukm2':1,
        'ecm2':0,
        'ecm4':0,
        'ecm5':0,
        'jgsm':1,
        'cgd2':1,
        'ecmt':0,
        'ecmn':0,
        'ecmg':0,
        
        'cmc2':0,
        'cgd6':0,
        'cgd2':0,

        'gfsc':1,
        'ngpj':1,
        'ukmc':0,
        'jmac':0,

        'goes':1,

         'ocn':0,
         'ohc':0,
         'ww3':0,
        'mpas':0,
        'mpsg':0,

        'fv3e':0,
        'fv3g':0,

        'fv7e':0,
        'fv7g':0,
        
        'hwrf':1,
    

        }

    W2_MODELS_Run12={
        'gfs':1,
        'ngp':1,
        'ngp05':1,
        'ukm':1,
        'gsm':1,
        'ocn':1,
        'ecm':1,
        'cmc':1,

        'gfs2':1,

        'fim8':1,
        'fimx':1,
        
        'rtfim':1,
        'rtfimx':1,
        'rtfimy':1,
        
        'ukm2':1,
        'ecm2':1,
        'ecm4':1,
        'era5':1,
        'ecm5':1,
        'jgsm':1,
        'cgd2':1,
        'ecmt':1,
        'ecmn':1,
        'ecmg':1,
        'ngp2':1,
        'ngpc':1,
        'navg':1,
        
        'cmc2':1,
        'cgd6':1,
        'cgd2':1,
        
        'gfsc':1,
        'ngpj':1,
        'ukmc':1,
        'jmac':1,

        'goes':1,
        
         'ocn':1,
         'ohc':1,
         'ww3':1,
        'mpas':1,
        'mpsg':1,

        'fv3e':1,
        'fv3g':1,

        'fv7e':1,
        'fv7g':1,
        
        'hwrf':1,
        

        }

    W2_MODELS_Run18={
        'gfs':1,
        'ngp':1,
        'ukm':0,
        'gsm':0,
        'ocn':0,
        'ecm':0,
        'cmc':0,

        'gfs2':1,
        
        'fim8':0,
        'fimx':0,
        'rtfim':0,
        'rtfimx':0,
        'rtfimy':0,

        'ukm2':1,
        'ecm2':0,
        'ecm4':0,
        'era5':0,
        'ecm5':0,
        'jgsm':1,
        'cgd2':0,
        'ecmt':0,
        'ecmn':0,
        'ecmg':0,
        'ngp2':0,
        'ngpc':1,
        'navg':1,
        
        'cmc2':0,
        'cgd6':0,
        'cgd2':0,

        'gfsc':1,
        'ngpj':1,
        'ukmc':0,
        'jmac':0,

        'goes':1,
        
         'ocn':0,
         'ohc':0,
         'ww3':0,
        'mpas':0,
        'mpsg':0,

        'fv3e':0,
        'fv3g':0,

        'fv7e':0,
        'fv7g':0,
        
        'hwrf':1,

        }

    W2_MODELS_NTAU={
        'gfs':144,
        'gfs.jtwc':144,
        'ngp':144,
        'ngp05':144,
        'ukm':144,
        'ukm.jtwc':72,
        'gsm':72,
        'ocn':144,
        'wav':144,
        'ecm':144,
        'cmc':144,

        'gfs2':144,
        'fim8':144,
        'fimx':144,
        'ukm2':144,
        'ecm2':144,
        'ecm4':144,
        'ecm5':144,
        'jgsm':132,
        'cgd2':144,
        'era5':144,
        
        'fv3e':168,
        'fv3g':168,
        
        'ecmt':144,
        'ecmn':144,
        'ecmg':144,
        'ngp2':144,
        'ngpc':168,
        'navg':168,
        'cmc2':144,

        }

    W2_MODELS_DATA_NTAU={
        'gfs':144,
        'ngp':144,
        'ngp05':144,
        'ukm':144,
        'ocn':0,
        'wav':144,
        'ecm':144,
        'cmc':144,

        'gfs2':144,
        'fim8':144,
        'fimx':144,
        'ukm2':144,
        
        'cmc2':144,
         
        'ecm2':240,
        'ecm4':240,
        'ecm5':240,
        'jgsm':132,
        'cgd2':240,
        'era5':240,
        'ecmt':240,
        'ecmn':240,
        'ecmg':240,
        
        'fv3e':168,
        'fv3g':168,
        
        'ngp2':144,
        'ngpc':168,
        'navg':168,
        
        'hwrf':126,

        }

    #
    # used in w2.status.py and w2-plot.py
    #
    W2_MODELS_TauInc={
        'gfs':12,
        'ngp':12,
        'ngp05':12,
        'ukm':12,
        'gsm':12,
        'ocn':12,
        'wav':12,
        'ecm':12,
        'cmc':12,

        'gfs2':12,
        'fim8':12,
        'fimx':12,
        'ukm2':12,
        'ecm2':12,
        'ecm4':12,
        'ecm5':12,
        'jgsm':12,
        'cgd2':12,
        'era5':12,
        'ecmt':12,
        'ecmn':12,
        'ecmg':12,
        
        'fv3e':12,
        'fv3g':12,
        
        'ngp2':12,
        'ngpc':12,
        'navg':12,
        'cmc2':12,

        }


    W2_MODELS_HTML_DIR={
        'gfs':'gfs/archive',
        'ngp':'ngp/archive',
        'ngp05':'ngp/archive',
        'ukm':'ukm/archive',
        'gsm':'gsm/archive',
        'ocn':'ngp/archive',
        'ecm':'ecm/archive',
        'ecm4':'ecm/archive',
        'ecm5':'ecm/archive',
        'jgsm':'gsm/archive',
        'cmc':'cmc/archive',
        'cgd2':'cmc/archive',
        
        'fv3e':'fv3e/archive',
        'fv3g':'fv3g/archive',
        
        }

    W2_MODELS_ADD_MAPS={

        'gfs':1,
        'ngp':0,
        'ngp05':0,
        'ukm':0,
        'gsm':0,
        'ocn':0,
        'ecm':0,
        'cmc':0,

        'ecm2':0,
        'ecm4':0,
        'ecm5':0,
        'jgsm':0,
        'cgd2':0,
        'ecmt':0,
        'ecmn':0,
        'ecmg':0,
        'ngp2':0,
        'ngpc':0,
        'navg':0,
        
        'fv3e':0,
        'fveg':0,
        
        }

    W2_MODELS_COLOR={
        'gfs':'red',
        'fim':'orange',
        
        'fv3e':'red',
        'fv3g':'green',
        
        'fimx':'orange',
        'ngp':'navy',
        'ngp05':'navy',
        'ukm':'green',
        'gsm':'yellow',
        'ocn':'yellow',
        'ecm':'yellow',
        'cmc':'yellow',

        'ecm2':'yellow',
        'ecm4':'yellow',
        'ecm5':'yellow',
        'jgsm':'blue',
        'cgd2':'yellow',
        
        'ecmt':'yellow',
        'ecmn':'yellow',
        'ecmg':'yellow',
        'ngp2':'navy',
        'ngpc':'navy',
        'navg':'navy',
        }

    W2_MODELS_UCASE={
        'gfs':'GFS',
        'fim':'FIM',
        
        'fv3e':'FV3N',
        'fv3g':'FV3G',

        'fimx':'FIMX',
        'ngp':'NGP',
        'ngp05':'NGP',
        'ukm':'UKM',
        'gsm':'GSM',
        'ocn':'OCN',
        'ecm':'ECM',
        'cmc':'CMC',

        'ecm2':'ECM2',
        'ecm4':'ECM4',
        'ecm5':'ECM5',
        'jgsm':'JGSM',
        'cgd2':'CMC',
        
        'ecmt':'ECMT',
        'ecmn':'ECMN',
        'ecmg':'ECMG',
        'ngp2':'NGP2',
        'ngpc':'NGPC',
        'navg':'NAVG',
        }

    ###################################################
    #
    #	TC PROPERTIES
    #
    ###################################################

    W2_TC_NGTRP_OPS_DIR=W2_DAT_BDIR+'/dat/tc'
    W2_TC_ATCF_OPS_DIR=W2_DAT_BDIR+'/dat/tc/atcf'
    W2_TC_JTWC_DIR=W2_TC_NGTRP_OPS_DIR+'/jtwc'
    W2_TC_NHC_DIR=W2_TC_NGTRP_OPS_DIR+'/bdeck/nhc'
    W2_TC_BT_OPS_DIR=W2_TC_NGTRP_OPS_DIR
    W2_TC_BT_EXP_DIR=W2_TC_BT_OPS_DIR+'/bt_neumann'
    W2_TC_FT_OPS_DIR=W2_TC_NGTRP_OPS_DIR+'/ft_ops'
    W2_TC_REPORT_OPS_DIR=W2_TC_NGTRP_OPS_DIR+'/report'
    W2_TC_REPORT_EXP_DIR=W2_TC_NGTRP_OPS_DIR+'/report'

    W2_TC_VERI_OPS_DIR=W2_TC_NGTRP_OPS_DIR+'/veri_ops'
    W2_TC_TRACK_IFS_OPS_INCOMING_DIR="/pcmdi/ftp_incoming/fiorino"
    W2_TC_SITREP_DIR="/dat/www/tc/sitrep"

    W2_TC_STRUCT_PZAL_DIR="/tdocommon/wxmap/dat/tc/tcstruct"
    W2_TC_ECMWF_PLT_DIR="/dat/nwp/dat/tc/plt/ecmwf"
    W2_TC_ECMWF_PLT_PZAL_DIR="/tdocommon/wxmap/web/ecmwf"


    W2_MODELS_ARCHIVE_GRFDIR=W2_MODELS_CURRENT_GRFDIR


    ###################################################
    #
    #	WXMAP Subroutines
    #
    ###################################################

    narea=len(W2_AREAS)

    #
    # ncep r1 daily wind climo  as model nr1
    #

    plot_control={}

    plot_control['wconus','tmx','units']="F"
    plot_control['wconus','tmn','units']="F"

    plot_control['conus','tmx','units']="F"
    plot_control['conus','tmn','units']="F"

    plot_control['europe','tmx','units']="C"
    plot_control['europe','tmn','units']="C"

    plot_control['nhem','tmx','units']="C"
    plot_control['nhem','tmn','units']="C"

    plot_control['ausnz','tmx','units']="C"
    plot_control['ausnz','tmn','units']="C"

    plot_control['bigaus','tmx','units']="C"
    plot_control['bigaus','tmn','units']="C"

    plot_control['aoe1','tmx','units']="F"
    plot_control['aoe1','tmn','units']="F"

    plot_control['wconus','tas','units']="F"
    plot_control['conus','tas','units']="F"

    plot_control['europe','tas','units']="C"
    plot_control['nhem','tas','units']="C"
    plot_control['asia','tas','units']="F"

    plot_control['tropepac','tas','units']="C"
    plot_control['tropwpac','tas','units']="C"
    plot_control['tropswpac','tas','units']="C"

    plot_control['uk','tas','units']="C"
    plot_control['africa','tas','units']="C"

    #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    #
    #  mid-lat
    #
    #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

    PlotsMidLatFull="500 prp w20 850 uas psl"
    PlotsMidLatFullTmaxTmin="500 prp w20 850 uas psl tas tmx tmn"
    PlotsMidLatFullTas="500 prp w20 850 uas psl tas"

    PlotsMidLatFull="500 prp w20 850"
    PlotsMidLatFullTmaxTmin="500 prp w20 850 tas tmx tmn"
    PlotsMidLatFullTas="500 prp w20 850 tas"

    PlotsMidLat="500 prp w20"
    PlotsMidLatTas="500 prp w20 tas"
    PlotsMidLatTmaxTmin="500 prp w20 tas tmx tmn"
    PlotsMidLatReduced="500 psl w20"

    # -- asia
    
    plot_control['gfs','asia','plots']=PlotsMidLat
    plot_control['gfs','asia','taus']="default"
    plot_control['fim','asia','plots']=PlotsMidLat
    plot_control['fim','asia','taus']="default"

    plot_control['fv3e','asia','plots']=PlotsMidLat
    plot_control['fv3e','asia','taus']="default"
    plot_control['fv3g','asia','plots']=PlotsMidLat
    plot_control['fv3g','asia','taus']="default"

    plot_control['fimx','asia','plots']=PlotsMidLat
    plot_control['fimx','asia','taus']="default"
    plot_control['ecmn','asia','plots']=PlotsMidLat
    plot_control['ecmn','asia','taus']="default"
    plot_control['ecmg','asia','plots']=PlotsMidLatReduced
    plot_control['ecmg','asia','taus']="default"
    plot_control['ngp2','asia','plots']=PlotsMidLat
    plot_control['ngp2','asia','taus']="default"
    plot_control['ngpc','asia','plots']=PlotsMidLat
    plot_control['ngpc','asia','taus']="default"
    plot_control['navg','asia','plots']=PlotsMidLat
    plot_control['navg','asia','taus']="default"

    plot_control['ecmt','asia','plots']=PlotsMidLat
    plot_control['ecmt','asia','taus']="default"
    plot_control['ukm','asia','plots']=PlotsMidLat
    plot_control['ukm','asia','taus']="default"

    plot_control['ecm','asia','plots']=PlotsMidLat
    plot_control['ecm','asia','taus']="default"
    
    plot_control['gsm','asia','plots']=PlotsMidLat
    plot_control['gsm','asia','taus']="default"
    
    plot_control['cmc','asia','plots']=PlotsMidLat
    plot_control['cmc','asia','taus']="default"
    plot_control['gfsc','asia','plots']=PlotsMidLat
    plot_control['gfsc','asia','taus']="default"
    plot_control['ngpj','asia','plots']=PlotsMidLat
    plot_control['ngpj','asia','taus']="default"

    # -- wconus
    
    plot_control['gfs','wconus','plots']=PlotsMidLat
    plot_control['gfs','wconus','taus']="default"
    plot_control['fim','wconus','plots']=PlotsMidLat
    plot_control['fim','wconus','taus']="default"

    plot_control['fv3e','wconus','plots']=PlotsMidLat
    plot_control['fv3e','wconus','taus']="default"
    plot_control['fv3g','wconus','plots']=PlotsMidLat
    plot_control['fv3g','wconus','taus']="default"


    plot_control['fimx','wconus','plots']=PlotsMidLat
    plot_control['fimx','wconus','taus']="default"
    plot_control['ecmn','wconus','plots']=PlotsMidLat
    plot_control['ecmn','wconus','taus']="default"
    plot_control['ecmg','wconus','plots']=PlotsMidLatReduced
    plot_control['ecmg','wconus','taus']="default"
    plot_control['ngp2','wconus','plots']=PlotsMidLat
    plot_control['ngp2','wconus','taus']="default"
    plot_control['ngpc','wconus','plots']=PlotsMidLat
    plot_control['ngpc','wconus','taus']="default"
    plot_control['navg','wconus','plots']=PlotsMidLat
    plot_control['navg','wconus','taus']="default"
    plot_control['ecm','wconus','plots']=PlotsMidLat
    plot_control['ecm','wconus','taus']="default"
    plot_control['gsm','wconus','plots']=PlotsMidLat
    plot_control['gsm','wconus','taus']="default"
    plot_control['ecmt','wconus','plots']=PlotsMidLat
    plot_control['ecmt','wconus','taus']="default"
    plot_control['ukm','wconus','plots']=PlotsMidLat
    plot_control['ukm','wconus','taus']="default"

    plot_control['cmc','wconus','plots']=PlotsMidLat
    plot_control['cmc','wconus','taus']="default"

    plot_control['gfsc','wconus','plots']=PlotsMidLat
    plot_control['gfsc','wconus','taus']="default"
    plot_control['ngpj','wconus','plots']=PlotsMidLat
    plot_control['ngpj','wconus','taus']="default"


    # -- conus
    
    plot_control['gfs','conus','plots']=PlotsMidLatFullTmaxTmin
    plot_control['gfs','conus','taus']="default"
    plot_control['fim','conus','plots']=PlotsMidLatFull
    plot_control['fim','conus','taus']="default"

    plot_control['fv3e','conus','plots']=PlotsMidLatFull
    plot_control['fv3e','conus','taus']="default"
    plot_control['fv3g','conus','plots']=PlotsMidLatFull
    plot_control['fv3g','conus','taus']="default"

    plot_control['fimx','conus','plots']=PlotsMidLatFull
    plot_control['fimx','conus','taus']="default"
    plot_control['ecmn','conus','plots']=PlotsMidLatFull
    plot_control['ecmn','conus','taus']="default"
    plot_control['ecmg','conus','plots']=PlotsMidLatReduced
    plot_control['ecmg','conus','taus']="default"
    plot_control['ngp2','conus','plots']=PlotsMidLatFull
    plot_control['ngp2','conus','taus']="default"
    plot_control['ngpc','conus','plots']=PlotsMidLatFull
    plot_control['ngpc','conus','taus']="default"
    plot_control['navg','conus','plots']=PlotsMidLatFull
    plot_control['navg','conus','taus']="default"
    plot_control['ecm','conus','plots']=PlotsMidLatFull
    plot_control['ecm','conus','taus']="default"
    plot_control['gsm','conus','plots']=PlotsMidLatFull
    plot_control['gsm','conus','taus']="default"
    plot_control['ecmt','conus','plots']=PlotsMidLatFull
    plot_control['ecmt','conus','taus']="default"
    plot_control['ukm','conus','plots']=PlotsMidLatFull
    plot_control['ukm','conus','taus']="default"

    plot_control['cmc','conus','plots']=PlotsMidLatFull
    plot_control['cmc','conus','taus']="default"

    plot_control['gfsc','conus','plots']=PlotsMidLatFull
    plot_control['gfsc','conus','taus']="default"
    plot_control['ngpj','conus','plots']=PlotsMidLatFull
    plot_control['ngpj','conus','taus']="default"

    # -- europe
    
    plot_control['gfs','europe','plots']=PlotsMidLat
    plot_control['gfs','europe','taus']="default"
    plot_control['fim','europe','plots']=PlotsMidLat
    plot_control['fim','europe','taus']="default"

    plot_control['fv3e','europe','plots']=PlotsMidLat
    plot_control['fv3e','europe','taus']="default"
    plot_control['fv3g','europe','plots']=PlotsMidLat
    plot_control['fv3g','europe','taus']="default"

    plot_control['fimx','europe','plots']=PlotsMidLat
    plot_control['fimx','europe','taus']="default"
    plot_control['ecmn','europe','plots']=PlotsMidLat
    plot_control['ecmn','europe','taus']="default"
    plot_control['ecmg','europe','plots']=PlotsMidLatReduced
    plot_control['ecmg','europe','taus']="default"
    plot_control['ngp2','europe','plots']=PlotsMidLat
    plot_control['ngp2','europe','taus']="default"
    plot_control['ngpc','europe','plots']=PlotsMidLat
    plot_control['ngpc','europe','taus']="default"
    plot_control['navg','europe','plots']=PlotsMidLat
    plot_control['navg','europe','taus']="default"
    plot_control['ecm','europe','plots']=PlotsMidLat
    plot_control['ecm','europe','taus']="default"
    plot_control['gsm','europe','plots']=PlotsMidLat
    plot_control['gsm','europe','taus']="default"
    plot_control['ecmt','europe','plots']=PlotsMidLat
    plot_control['ecmt','europe','taus']="default"
    plot_control['ukm','europe','plots']=PlotsMidLat
    plot_control['ukm','europe','taus']="default"

    plot_control['cmc','europe','plots']=PlotsMidLat
    plot_control['cmc','europe','taus']="default"

    plot_control['gfsc','europe','plots']=PlotsMidLat
    plot_control['gfsc','europe','taus']="default"
    plot_control['ngpj','europe','plots']=PlotsMidLat
    plot_control['ngpj','europe','taus']="default"
    

    # -- nhem
    
    plot_control['gfs','nhem','plots']=PlotsMidLat
    plot_control['gfs','nhem','taus']="default"
    plot_control['fim','nhem','plots']=PlotsMidLat
    plot_control['fim','nhem','taus']="default"

    plot_control['fv3e','nhem','plots']=PlotsMidLat
    plot_control['fv3e','nhem','taus']="default"
    plot_control['fv3g','nhem','plots']=PlotsMidLat
    plot_control['fv3g','nhem','taus']="default"

    plot_control['fimx','nhem','plots']=PlotsMidLat
    plot_control['fimx','nhem','taus']="default"
    plot_control['ecmn','nhem','plots']=PlotsMidLat
    plot_control['ecmn','nhem','taus']="default"
    plot_control['ecmg','nhem','plots']=PlotsMidLatReduced
    plot_control['ecmg','nhem','taus']="default"
    plot_control['ngp2','nhem','plots']=PlotsMidLat
    plot_control['ngp2','nhem','taus']="default"
    plot_control['ngpc','nhem','plots']=PlotsMidLat
    plot_control['ngpc','nhem','taus']="default"
    plot_control['navg','nhem','plots']=PlotsMidLat
    plot_control['navg','nhem','taus']="default"
    plot_control['ecm','nhem','plots']=PlotsMidLat
    plot_control['ecm','nhem','taus']="default"
    plot_control['gsm','nhem','plots']=PlotsMidLat
    plot_control['gsm','nhem','taus']="default"
    plot_control['ecmt','nhem','plots']=PlotsMidLat
    plot_control['ecmt','nhem','taus']="default"
    plot_control['ukm','nhem','plots']=PlotsMidLat
    plot_control['ukm','nhem','taus']="default"

    plot_control['cmc','nhem','plots']=PlotsMidLat
    plot_control['cmc','nhem','taus']="default"

    plot_control['gfsc','nhem','plots']=PlotsMidLat
    plot_control['gfsc','nhem','taus']="default"
    plot_control['ngpj','nhem','plots']=PlotsMidLat
    plot_control['ngpj','nhem','taus']="default"



    ##################################################
    #
    #   tropics
    #
    ##################################################


    # -- reorder so most sig plots are to the left
    #

    PlotsNhemTropfull="n850 uas shr prp w20 mhq wdl hhq lmq 500 u50 u70 w70 850 psl"
    PlotsShemTropfull="n850 uas shr prp w20 mhq wdl 850"
    PlotsTropMonitor="uas prp shr n850 w20 mhq psl"
    
    # -- set/reduce here and in wxmap.env.pl
    #
    PlotsNhemTropfull="uas shr n850 prp 500 w20 wdl lmq mhq hhq"
    PlotsShemTropfull="uas shr n850 prp 500 w20 wdl lmq mhq hhq"
    PlotsTropMonitor="uas shr prp w20"
    
    PlotsTropAllNhem=PlotsNhemTropfull
    PlotsTropAllShem=PlotsShemTropfull
    
    # -- reduce because /w3/rapb too full
    #
    PlotsTropAllLant=PlotsNhemTropfull
    PlotsTropAllEpac=PlotsNhemTropfull
    PlotsTropAllWpac=PlotsNhemTropfull
    
    PlotsTropReduced="n850 shr w20 psl"
    
    # -- ENSO eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

    plot_control['gfs','tropenso','plots']=PlotsTropAllLant
    plot_control['gfs','tropenso','taus']="default"
    plot_control['fim','tropenso','plots']=PlotsTropAllLant
    plot_control['fim','tropenso','taus']="default"

    plot_control['fv3e','tropenso','plots']=PlotsTropAllLant
    plot_control['fv3e','tropenso','taus']="default"
    plot_control['fv3g','tropenso','plots']=PlotsTropAllLant
    plot_control['fv3g','tropenso','taus']="default"

    plot_control['navg','tropenso','plots']=PlotsTropAllLant
    plot_control['navg','tropenso','taus']="default"
    plot_control['ecm','tropenso','plots']=PlotsTropAllLant
    plot_control['ecm','tropenso','taus']="default"
    plot_control['gsm','tropenso','plots']=PlotsTropAllLant
    plot_control['gsm','tropenso','taus']="default"
    plot_control['ukm','tropenso','plots']=PlotsTropAllLant
    plot_control['ukm','tropenso','taus']="default"

    plot_control['cmc','tropenso','plots']=PlotsTropAllLant
    plot_control['cmc','tropenso','taus']="default"


    # -- LANT llllllllllllllllllllllllllllllll
    
    plot_control['gfs','troplant','plots']=PlotsTropAllLant
    plot_control['gfs','troplant','taus']="default"
    plot_control['fim','troplant','plots']=PlotsTropAllLant
    plot_control['fim','troplant','taus']="default"

    plot_control['fv3e','troplant','plots']=PlotsTropAllLant
    plot_control['fv3e','troplant','taus']="default"
    plot_control['fv3g','troplant','plots']=PlotsTropAllLant
    plot_control['fv3g','troplant','taus']="default"

    plot_control['fimx','troplant','plots']=PlotsTropAllLant
    plot_control['fimx','troplant','taus']="default"
    plot_control['ecmn','troplant','plots']=PlotsTropAllLant
    plot_control['ecmn','troplant','taus']="default"
    plot_control['ecmg','troplant','plots']=PlotsTropReduced
    plot_control['ecmg','troplant','taus']="default"
    plot_control['ngp2','troplant','plots']=PlotsTropAllLant
    plot_control['ngp2','troplant','taus']="default"
    plot_control['ngpc','troplant','plots']=PlotsTropAllLant
    plot_control['ngpc','troplant','taus']="default"
    plot_control['navg','troplant','plots']=PlotsTropAllLant
    plot_control['navg','troplant','taus']="default"
    plot_control['ecm','troplant','plots']=PlotsTropAllLant
    plot_control['ecm','troplant','taus']="default"
    plot_control['gsm','troplant','plots']=PlotsTropAllLant
    plot_control['gsm','troplant','taus']="default"
    plot_control['ecmt','troplant','plots']=PlotsTropAllLant
    plot_control['ecmt','troplant','taus']="default"
    plot_control['ukm','troplant','plots']=PlotsTropAllLant
    plot_control['ukm','troplant','taus']="default"

    plot_control['cmc','troplant','plots']=PlotsTropAllLant
    plot_control['cmc','troplant','taus']="default"

    plot_control['gfsc','troplant','plots']=PlotsTropAllLant
    plot_control['gfsc','troplant','taus']="default"
    plot_control['ngpj','troplant','plots']=PlotsTropAllLant
    plot_control['ngpj','troplant','taus']="default"


    # -- EPAC eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

    plot_control['gfs','tropepac','plots']=PlotsTropAllEpac
    plot_control['gfs','tropepac','taus']="default"
    plot_control['fim','tropepac','plots']=PlotsTropAllEpac
    plot_control['fim','tropepac','taus']="default"

    plot_control['fv3e','tropepac','plots']=PlotsTropAllEpac
    plot_control['fv3e','tropepac','taus']="default"
    plot_control['fv3g','tropepac','plots']=PlotsTropAllEpac
    plot_control['fv3g','tropepac','taus']="default"

    plot_control['fimx','tropepac','plots']=PlotsTropAllEpac
    plot_control['fimx','tropepac','taus']="default"
    plot_control['ecmn','tropepac','plots']=PlotsTropAllEpac
    plot_control['ecmn','tropepac','taus']="default"
    plot_control['ecmg','tropepac','plots']=PlotsTropReduced
    plot_control['ecmg','tropepac','taus']="default"
    plot_control['ngp2','tropepac','plots']=PlotsTropAllEpac
    plot_control['ngp2','tropepac','taus']="default"
    plot_control['ngpc','tropepac','plots']=PlotsTropAllEpac
    plot_control['ngpc','tropepac','taus']="default"
    plot_control['navg','tropepac','plots']=PlotsTropAllEpac
    plot_control['navg','tropepac','taus']="default"
    plot_control['ecm','tropepac','plots']=PlotsTropAllEpac
    plot_control['ecm','tropepac','taus']="default"
    plot_control['gsm','tropepac','plots']=PlotsTropAllEpac
    plot_control['gsm','tropepac','taus']="default"
    plot_control['ecmt','tropepac','plots']=PlotsTropAllEpac
    plot_control['ecmt','tropepac','taus']="default"
    plot_control['ukm','tropepac','plots']=PlotsTropAllEpac
    plot_control['ukm','tropepac','taus']="default"

    plot_control['cmc','tropepac','plots']=PlotsTropAllEpac
    plot_control['cmc','tropepac','taus']="default"

    plot_control['gfsc','tropepac','plots']=PlotsTropAllEpac
    plot_control['gfsc','tropepac','taus']="default"
    plot_control['ngpj','tropepac','plots']=PlotsTropAllEpac
    plot_control['ngpj','tropepac','taus']="default"


    # -- WPAC wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    
    plot_control['gfs','tropwpac','plots']=PlotsTropAllWpac
    plot_control['gfs','tropwpac','taus']="default"
    plot_control['fim','tropwpac','plots']=PlotsTropAllWpac
    plot_control['fim','tropwpac','taus']="default"

    plot_control['fv3e','tropwpac','plots']=PlotsTropAllWpac
    plot_control['fv3e','tropwpac','taus']="default"
    plot_control['fv3g','tropwpac','plots']=PlotsTropAllWpac
    plot_control['fv3g','tropwpac','taus']="default"

    plot_control['fimx','tropwpac','plots']=PlotsTropAllWpac
    plot_control['fimx','tropwpac','taus']="default"
    plot_control['ecmn','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ecmn','tropwpac','taus']="default"
    plot_control['ecmg','tropwpac','plots']=PlotsTropReduced
    plot_control['ecmg','tropwpac','taus']="default"
    plot_control['ngp2','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ngp2','tropwpac','taus']="default"
    plot_control['ngpc','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ngpc','tropwpac','taus']="default"
    plot_control['navg','tropwpac','plots']=PlotsTropAllWpac
    plot_control['navg','tropwpac','taus']="default"
    plot_control['ecm','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ecm','tropwpac','taus']="default"
    plot_control['gsm','tropwpac','plots']=PlotsTropAllWpac
    plot_control['gsm','tropwpac','taus']="default"
    plot_control['ecmt','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ecmt','tropwpac','taus']="default"
    plot_control['ukm','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ukm','tropwpac','taus']="default"

    plot_control['cmc','tropwpac','plots']=PlotsTropAllWpac
    plot_control['cmc','tropwpac','taus']="default"

    plot_control['gfsc','tropwpac','plots']=PlotsTropAllWpac
    plot_control['gfsc','tropwpac','taus']="default"
    plot_control['ngpj','tropwpac','plots']=PlotsTropAllWpac
    plot_control['ngpj','tropwpac','taus']="default"
    

    # -- NIO oooooooooooooooooooooooooooooooooooo
    
    plot_control['gfs','tropnio','plots']=PlotsTropAllNhem
    plot_control['gfs','tropnio','taus']="default"
    plot_control['gfsc','tropnio','plots']=PlotsTropAllNhem
    plot_control['gfsc','tropnio','taus']="default"
    
    plot_control['fim','tropnio','plots']=PlotsTropAllNhem
    plot_control['fim','tropnio','taus']="default"

    plot_control['fv3e','tropnio','plots']=PlotsTropAllNhem
    plot_control['fv3e','tropnio','taus']="default"
    plot_control['fv3g','tropnio','plots']=PlotsTropAllNhem
    plot_control['fv3g','tropnio','taus']="default"

    plot_control['fimx','tropnio','plots']=PlotsTropAllNhem
    plot_control['fimx','tropnio','taus']="default"
    plot_control['ecmn','tropnio','plots']=PlotsTropAllNhem
    plot_control['ecmn','tropnio','taus']="default"
    plot_control['ecmg','tropnio','plots']=PlotsTropReduced
    plot_control['ecmg','tropnio','taus']="default"
    plot_control['ngp2','tropnio','plots']=PlotsTropAllNhem
    plot_control['ngp2','tropnio','taus']="default"
    plot_control['ngpc','tropnio','plots']=PlotsTropAllNhem
    plot_control['ngpc','tropnio','taus']="default"
    plot_control['navg','tropnio','plots']=PlotsTropAllNhem
    plot_control['navg','tropnio','taus']="default"
    plot_control['ecm','tropnio','plots']=PlotsTropAllNhem
    plot_control['ecm','tropnio','taus']="default"
    plot_control['gsm','tropnio','plots']=PlotsTropAllNhem
    plot_control['gsm','tropnio','taus']="default"
    plot_control['ecmt','tropnio','plots']=PlotsTropAllNhem
    plot_control['ecmt','tropnio','taus']="default"
    plot_control['ukm','tropnio','plots']=PlotsTropAllNhem
    plot_control['ukm','tropnio','taus']="default"

    plot_control['cmc','tropnio','plots']=PlotsTropAllNhem
    plot_control['cmc','tropnio','taus']="default"

    #SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
    #
    # SHEM
    #
    #SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

    # -- swpac

    plot_control['gfs','tropswpac','plots']=PlotsTropAllShem
    plot_control['gfs','tropswpac','taus']="default"
    plot_control['fim','tropswpac','plots']=PlotsTropAllShem
    plot_control['fim','tropswpac','taus']="default"

    plot_control['fv3e','tropswpac','plots']=PlotsTropAllShem
    plot_control['fv3e','tropswpac','taus']="default"
    plot_control['fv3g','tropswpac','plots']=PlotsTropAllShem
    plot_control['fv3g','tropswpac','taus']="default"

    plot_control['fimx','tropswpac','plots']=PlotsTropAllShem
    plot_control['fimx','tropswpac','taus']="default"
    plot_control['ngp2','tropswpac','plots']=PlotsTropAllShem
    plot_control['ngp2','tropswpac','taus']="default"
    plot_control['ngpc','tropswpac','plots']=PlotsTropAllShem
    plot_control['ngpc','tropswpac','taus']="default"
    plot_control['navg','tropswpac','plots']=PlotsTropAllShem
    plot_control['navg','tropswpac','taus']="default"
    plot_control['ecm','tropswpac','plots']=PlotsTropAllShem
    plot_control['ecm','tropswpac','taus']="default"
    plot_control['gsm','tropswpac','plots']=PlotsTropAllShem
    plot_control['gsm','tropswpac','taus']="default"
    plot_control['ecmt','tropswpac','plots']=PlotsTropAllShem
    plot_control['ecmt','tropswpac','taus']="default"
    plot_control['ecmg','tropswpac','plots']=PlotsTropReduced
    plot_control['ecmg','tropswpac','taus']="default"
    plot_control['ukm','tropswpac','plots']=PlotsTropAllShem
    plot_control['ukm','tropswpac','taus']="default"

    plot_control['cmc','tropswpac','plots']=PlotsTropAllShem
    plot_control['cmc','tropswpac','taus']="default"

    plot_control['gfsc','tropswpac','plots']=PlotsTropAllShem
    plot_control['gfsc','tropswpac','taus']="default"
    plot_control['ngpj','tropswpac','plots']=PlotsTropAllShem
    plot_control['ngpj','tropswpac','taus']="default"


    # -- tropio
    
    plot_control['gfs','tropio','plots']=PlotsTropAllShem
    plot_control['gfs','tropio','taus']="default"
    plot_control['fim','tropio','plots']=PlotsTropAllShem
    plot_control['fim','tropio','taus']="default"

    plot_control['fv3e','tropio','plots']=PlotsTropAllShem
    plot_control['fv3e','tropio','taus']="default"
    plot_control['fv3g','tropio','plots']=PlotsTropAllShem
    plot_control['fv3g','tropio','taus']="default"

    plot_control['fimx','tropio','plots']=PlotsTropAllShem
    plot_control['fimx','tropio','taus']="default"
    plot_control['ngp2','tropio','plots']=PlotsTropAllShem
    plot_control['ngp2','tropio','taus']="default"
    plot_control['ngpc','tropio','plots']=PlotsTropAllShem
    plot_control['ngpc','tropio','taus']="default"
    plot_control['navg','tropio','plots']=PlotsTropAllShem
    plot_control['navg','tropio','taus']="default"
    plot_control['ecm','tropio','plots']=PlotsTropAllShem
    plot_control['ecm','tropio','taus']="default"
    plot_control['gsm','tropio','plots']=PlotsTropAllShem
    plot_control['gsm','tropio','taus']="default"
    plot_control['ecmt','tropio','plots']=PlotsTropAllShem
    plot_control['ecmt','tropio','taus']="default"
    plot_control['ecmg','tropio','plots']=PlotsTropReduced
    plot_control['ecmg','tropio','taus']="default"
    plot_control['ukm','tropio','plots']=PlotsTropAllShem
    plot_control['ukm','tropio','taus']="default"

    plot_control['cmc','tropio','plots']=PlotsTropAllShem
    plot_control['cmc','tropio','taus']="default"

    plot_control['gfsc','tropio','plots']=PlotsTropAllShem
    plot_control['gfsc','tropio','taus']="default"
    plot_control['ngpj','tropio','plots']=PlotsTropAllShem
    plot_control['ngpj','tropio','taus']="default"
    

    # -- tropsio

    plot_control['gfs','tropsio','plots']=PlotsTropAllShem
    plot_control['gfs','tropsio','taus']="default"
    plot_control['fim','tropsio','plots']=PlotsTropAllShem
    plot_control['fim','tropsio','taus']="default"

    plot_control['fv3e','tropsio','plots']=PlotsTropAllShem
    plot_control['fv3e','tropsio','taus']="default"
    plot_control['fv3g','tropsio','plots']=PlotsTropAllShem
    plot_control['fv3g','tropsio','taus']="default"

    plot_control['fimx','tropsio','plots']=PlotsTropAllShem
    plot_control['fimx','tropsio','taus']="default"
    plot_control['ngp2','tropsio','plots']=PlotsTropAllShem
    plot_control['ngp2','tropsio','taus']="default"
    plot_control['ngpc','tropsio','plots']=PlotsTropAllShem
    plot_control['ngpc','tropsio','taus']="default"
    plot_control['navg','tropsio','plots']=PlotsTropAllShem
    plot_control['navg','tropsio','taus']="default"
    plot_control['ecm','tropsio','plots']=PlotsTropAllShem
    plot_control['ecm','tropsio','taus']="default"
    plot_control['gsm','tropsio','plots']=PlotsTropAllShem
    plot_control['gsm','tropsio','taus']="default"
    plot_control['ecmt','tropsio','plots']=PlotsTropAllShem
    plot_control['ecmt','tropsio','taus']="default"
    plot_control['ecmg','tropsio','plots']=PlotsTropReduced
    plot_control['ecmg','tropsio','taus']="default"
    plot_control['ukm','tropsio','plots']=PlotsTropAllShem
    plot_control['ukm','tropsio','taus']="default"

    plot_control['cmc','tropsio','plots']=PlotsTropAllShem
    plot_control['cmc','tropsio','taus']="default"

    plot_control['gfsc','tropsio','plots']=PlotsTropAllShem
    plot_control['gfsc','tropsio','taus']="default"
    plot_control['ngpj','tropsio','plots']=PlotsTropAllShem
    plot_control['ngpj','tropsio','taus']="default"
    

    # -- tropoz

    plot_control['gfs','tropoz','plots']=PlotsTropAllShem
    plot_control['gfs','tropoz','taus']="default"
    plot_control['fim','tropoz','plots']=PlotsTropAllShem
    plot_control['fim','tropoz','taus']="default"

    plot_control['fv3e','tropoz','plots']=PlotsTropAllShem
    plot_control['fv3e','tropoz','taus']="default"
    plot_control['fv3g','tropoz','plots']=PlotsTropAllShem
    plot_control['fv3g','tropoz','taus']="default"

    plot_control['fimx','tropoz','plots']=PlotsTropAllShem
    plot_control['fimx','tropoz','taus']="default"
    plot_control['ngp2','tropoz','plots']=PlotsTropAllShem
    plot_control['ngp2','tropoz','taus']="default"
    plot_control['ngpc','tropoz','plots']=PlotsTropAllShem
    plot_control['ngpc','tropoz','taus']="default"
    plot_control['navg','tropoz','plots']=PlotsTropAllShem
    plot_control['navg','tropoz','taus']="default"
    plot_control['ecm','tropoz','plots']=PlotsTropAllShem
    plot_control['ecm','tropoz','taus']="default"
    plot_control['gsm','tropoz','plots']=PlotsTropAllShem
    plot_control['gsm','tropoz','taus']="default"
    plot_control['ecmt','tropoz','plots']=PlotsTropAllShem
    plot_control['ecmt','tropoz','taus']="default"
    plot_control['ecmg','tropoz','plots']=PlotsTropReduced
    plot_control['ecmg','tropoz','taus']="default"
    plot_control['ukm','tropoz','plots']=PlotsTropAllShem
    plot_control['ukm','tropoz','taus']="default"

    plot_control['cmc','tropoz','plots']=PlotsTropAllShem
    plot_control['cmc','tropoz','taus']="default"

    plot_control['gfsc','tropoz','plots']=PlotsTropAllShem
    plot_control['gfsc','tropoz','taus']="default"
    plot_control['ngpj','tropoz','plots']=PlotsTropAllShem
    plot_control['ngpj','tropoz','taus']="default"
    plot_control['ukmc','tropoz','plots']=PlotsTropAllShem
    plot_control['ukmc','tropoz','taus']="default"
    

    ##################################################
    #
    #   special
    #
    ##################################################

    aoeplot="w20 lmq mhq 500 850 uas prp psl"
    aoeplot_ukm="w20 lmq 500 850 uas psl"

    plot_control['gfs','aoe1','plots']=aoeplot+' '
    plot_control['gfs','aoe1','taus']="default"
    plot_control['fim','aoe1','plots']=aoeplot+' '
    plot_control['fim','aoe1','taus']="default"

    plot_control['fv3e','aoe1','plots']=aoeplot+' '
    plot_control['fv3e','aoe1','taus']="default"
    plot_control['fv3g','aoe1','plots']=aoeplot+' '
    plot_control['fv3g','aoe1','taus']="default"

    plot_control['fimx','aoe1','plots']=aoeplot+' '
    plot_control['fimx','aoe1','taus']="default"
    plot_control['ngp2','aoe1','plots']=aoeplot+' '
    plot_control['ngp2','aoe1','taus']="default"
    plot_control['ngpc','aoe1','plots']=aoeplot+' '
    plot_control['ngpc','aoe1','taus']="default"
    plot_control['navg','aoe1','plots']=aoeplot+' '
    plot_control['navg','aoe1','taus']="default"
    plot_control['ecm','aoe1','plots']=aoeplot+' '
    plot_control['ecm','aoe1','taus']="default"
    plot_control['gsm','aoe1','plots']=aoeplot+' '
    plot_control['gsm','aoe1','taus']="default"
    plot_control['ecmt','aoe1','plots']=aoeplot+' '
    plot_control['ecmt','aoe1','taus']="default"

    plot_control['gfs','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['gfs','bigaus','taus']="default"
    plot_control['fim','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['fim','bigaus','taus']="default"

    plot_control['fv3e','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['fv3e','bigaus','taus']="default"
    plot_control['fv3g','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['fv3g','bigaus','taus']="default"

    plot_control['fimx','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['fimx','bigaus','taus']="default"
    plot_control['ngp2','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['ngp2','bigaus','taus']="default"
    plot_control['ngpc','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['ngpc','bigaus','taus']="default"
    plot_control['navg','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['navg','bigaus','taus']="default"
    plot_control['ecm','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['ecm','bigaus','taus']="default"
    plot_control['gsm','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['gsm','bigaus','taus']="default"
    plot_control['ecmt','bigaus','plots']="shr w20 lmq mhq 500 850 psl prp"
    plot_control['ecmt','bigaus','taus']="default"

    ##################################################
    #
    #   special/misc
    #
    ##################################################

    plot_control['ngp','uk','plots']="500 psl 850 prp uas"
    plot_control['ngp','uk','taus']="default"


    wxmap_maxplot_area={}

    wxmap_maxplot_area['ngp']=999
    wxmap_maxplot_area['ngp05']=999
    wxmap_maxplot_area['gfs']=999
    wxmap_maxplot_area['fim']=999

    wxmap_maxplot_area['fv3e']=999
    wxmap_maxplot_area['fv3g']=999

    wxmap_maxplot_area['fimx']=999
    wxmap_maxplot_area['gsm']=999
    wxmap_maxplot_area['ukm']=999
    wxmap_maxplot_area['ngp2']=999
    wxmap_maxplot_area['ngpc']=999
    wxmap_maxplot_area['navg']=999
    wxmap_maxplot_area['ecm']=999
    wxmap_maxplot_area['ecmt']=999
    wxmap_maxplot_area['era15']=999

    ##################################################
    #
    #   archive machine
    #
    ##################################################

    wxmap_archive_server="ecfs"
    wxmap_archive_server="bitbank.nersc.gov"
    wxmap_archive_server="hpss.nersc.gov"
    wxmap_archive_server="wxmap"
    wxmap_archive_server="pzal.npmoc.navy.mil"

    ###################################################
    #
    #  971205 - virtual frame buffer controls on stargate (sparc ultra)
    #  971228 - lock file controls
    #
    #   d - directory
    #   l - lock file
    #   n - number of display
    #   X - X display
    #
    #  wxmap_lockfile_maxage_min - max allowed age of a lock file in mins (3 hr)
    #
    ###################################################

    wxmap_lockfile_maxage_min=180    
    wxmap_tmpdir="/tmp/.fiorino"
    MF.ChkDir(wxmap_tmpdir,'mk')

    wxmap_xvfb={}

    wxmap_xvfb['gfs','d']="%sdir/xvfb.gfs"
    wxmap_xvfb['ngp','d']="wxmap_tmpdir/xvfb.ngp"
    wxmap_xvfb['Xvfb4','d']="wxmap_tmpdir/xvfb.4"

    wxmap_xvfb['gfs','l']="wxmap_tmpdir/lock.gfs"
    wxmap_xvfb['ngp','l']="wxmap_tmpdir/lock.ngp"

    wxmap_xvfb['gfs','n']="1"
    wxmap_xvfb['ngp','n']="3"
    wxmap_xvfb['Xvfb4','n']="4"

    wxmap_xvfb['gfs','X']="stargate:wxmap_xvfb['gfs','n'}.0"
    wxmap_xvfb['ngp','X']="stargate:wxmap_xvfb['ngp','n'}.0"
    wxmap_xvfb['Xvfb4','X']="stargate:wxmap_xvfb['Xvfb4','n'}.0"


    ##################################################
    #
    #   associative array between plot number and name on graphics file 
    #
    ##################################################


    pnam={}

    pnam={
        '1':'500',
        '2':'psl',
        '3':'prp',
        '4':'850',
        '5':'tas',
        '6':'uas',
        '7':'u50',
        '8':'shr',
        '9':'u70',
        '10':'sst',
        '11':'wav',
        '12':'w20',
        '13':'wdl',
        '14':'lmq',
        '15':'mhq',
        '16':'hhq',
        '20':'tmx',
        '21':'tmn',
        '22':'thk',
        '23':'w70',
        '30':'basemap',
        '50':'clm',
        '60':'stg',
        '61':'st2',

        '101':'n850',
        '102':'op06',
        '103':'op12',


        }

    pns=pnam.keys()

    pnum={}

    for pn in pns:
        pnum[pnam[pn]]=pn


    numplot_delta={
        '500':0,
        'psl':0,
        'prp':-1,
        '850':0,
        'tas':0,
        'uas':0,
        'u50':0,
        'shr':0,
        'sst':0,
        'wav':0,
        'w20':0,
        'wdl':0,
        'lmq':0,
        'mhq':0,
        'hhq':0,
        'tmx':-1,
        'tmn':-1,
        'thk':0,
        'w70':0,
        'basemap':-999,
        'clm':0,

        'n850':0,
        'op06':0,
        'op12':0,

        }


    maptitle={
        '500':'500 hPa Heights [m] and Rel. Vort [10<sup>-5</sup> s<sup>-1</sup>]',
        '850':'850 hPa Temperature [C], winds [kts] and Rel. Hum. [%]',
        'prp':'SLP [hPa] / 540 line / Prev 6-h Prcp Rate [mm/day]', 
        'psl':'SLP [hPa] & 500-1000 Thkns [m] & 700 hPa Vert. Vel [Pa s<sup>-1</sup>]',
        'u50':'500 hPa Strmlns & Istchs [kt] ; Wind Barbs',
        'u70':'700 hPa Strmlns ; N-S wind componment ; Wind Barbs',
        'shr':'|850-200 Shear| ; 200 hPa Strmlns ; 850(R)/200(G) Barbs',
        'sst':'SST [C] ; SST Anomaly from AMIP II SST Climatology (1979-96)',
        'uas':'Over Ocean Sfc Winds [kt]',
        'wav':'Sig Wave Heights [ft] ; Over Ocean Sfc Winds [kt]',
        'w20':'200 hPa Streamlines and Isotachs [kt]',
        'wdl':'Deep Layer Mean Streamlines/Isotachs [kt]',
        'lmq':'Low-Mid Trop (850/700/500) PW [mm] & Flow',
        'mhq':'Mid-High Trop (500/300) PW [mm] & Flow',
        'hhq':'High-High Trop (300/200) PW [mm] & Flow',
        'tmx':'Max Sfc Air Temperature [F] ; GFS Previous 24-h',
        'tmn':'Min Sfc Air Temperature [F] ; GFS Previous 24-h',
        'tas':'Sfc Air Temperature Change [F]',
        'thk':'1000-500 Thickness [dm] and Sea Level Pressure [mb]',
        'w70':'700 hPa Strmlns and Istchs [kt] ; Wind Barbs',
        'clm':'0-5 day mean climo',

        'n850':'850 Rel Vort [10^-5] Wind Barbs ; 200 Strmlns [kt]',
        'op06':'SLP [hPa] / 540 line / 6-h accum QMPORPH Prcp Rate [mm/day]', 
        'op12':'SLP [hPa] / 540 line / 12-h accum QMPORPH Prcp Rate [mm/day]', 
    }


    def getW2_MODELS_CURRENT_GRFDIR(self,model):

        if(model == 'gfs'):
            gdir="%s/plt_ncep_gfs"%(self.W2_BDIRWEB)
        elif(model == 'fim'):
            gdir="%s/plt_esrl_fim"%(self.W2_BDIRWEB)

        elif(model == 'fv3e'):
            gdir="%s/plt_esrl_fv3e"%(self.W2_BDIRWEB)
        elif(model == 'fv3g'):
            gdir="%s/plt_esrl_fv3g"%(self.W2_BDIRWEB)

        elif(model == 'ngp'):
            gdir="%s/plt_fnmoc_ngp"%(self.W2_BDIRWEB)
        elif(model == 'ngp05'):
            gdir="%s/plt_fnmoc_ngp"%(self.W2_BDIRWEB)
        elif(model =='ukm'):
            gdir="%s/plt_ukmo_ukm"%(self.W2_BDIRWEB)
        elif(model =='ocn'):
            gdir="%s/plt_fnmoc_ocn"%(self.W2_BDIRWEB)
        elif(model =='ecm'):
            gdir="%s/plt_ecmwf_ecm"%(self.W2_BDIRWEB)
        elif(model =='gsm'):
            gdir="%s/plt_jma_gsm"%(self.W2_BDIRWEB)
        elif(model =='ecmt'):
            gdir="%s/plt_ecmwf_ecmt"%(self.W2_BDIRWEB)
        elif(model =='cmc'):
            gdir="%s/plt_cmc_cmc"%(self.W2_BDIRWEB)

        elif(model =='gfs2'):
            gdir="%s/plt_ncep_gfs"%(self.W2_BDIRWEB)
        elif(model =='fim8'):
            gdir="%s/plt_esrl_fim"%(self.W2_BDIRWEB)
        elif(model =='fimx'):
            gdir="%s/plt_esrl_fimx"%(self.W2_BDIRWEB)
        elif(model =='ngp2'):
            gdir="%s/plt_fnmoc_ngp"%(self.W2_BDIRWEB)
        elif(model =='ngpc'):
            gdir="%s/plt_fnmoc_ngpc"%(self.W2_BDIRWEB)
        elif(model =='navg'):
            gdir="%s/plt_fnmoc_navg"%(self.W2_BDIRWEB)
        elif(model =='ukm2'):
            gdir="%s/plt_ukmo_ukm"%(self.W2_BDIRWEB)
        elif(model =='ecm2'):
            gdir="%s/plt_ecmwf_ecm"%(self.W2_BDIRWEB)
        elif(model =='ecm4'):
            gdir="%s/plt_ecmwf_ecm"%(self.W2_BDIRWEB)
        elif(model =='ecm5'):
            gdir="%s/plt_ecmwf_ecm"%(self.W2_BDIRWEB)
        elif(model =='jgsm'):
            gdir="%s/plt_jma_gsm"%(self.W2_BDIRWEB)
        elif(model =='cgd2'):
            gdir="%s/plt_cmc_cmc"%(self.W2_BDIRWEB)
        elif(model =='ecmt'):
            gdir="%s/plt_ecmwf_ecm"%(self.W2_BDIRWEB)
        elif(model =='gfsk'):
            gdir="%s/plt_esrl_gfsk"%(self.W2_BDIRWEB)
        elif(model =='ecmn'):
            gdir="%s/plt_ecmwf_ecm"%(self.W2_BDIRWEB)
        elif(model =='ecmg'):
            gdir="%s/plt_ecmwf_ecmg"%(self.W2_BDIRWEB)
        elif(model =='cmc2'):
            gdir="%s/plt_cmc_cmc"%(self.W2_BDIRWEB)

        elif(model =='gfsc'):
            gdir="%s/plt_ncep_gfsc"%(self.W2_BDIRWEB)
        elif(model =='ngpj'):
            gdir="%s/plt_fnmoc_ngpj"%(self.W2_BDIRWEB)
        elif(model =='ukmc'):
            gdir="%s/plt_ukmo_ukmc"%(self.W2_BDIRWEB)
        elif(model =='jmac'):
            gdir="%s/plt_jmac_jmac"%(self.W2_BDIRWEB)

        return(gdir)

    def TitleAck(self,model):

        myname="Dr. Mike Fiorino (fiorino@ecmwf.int) ECMWF, Reading, UK"
        myname="Dr. Mike Fiorino (fiorino@llnl.gov), PCMDI, LLNL, Livermore CA"
        myname="CDR Mike Fiorino, USN (RC), COMPACFLT Det 520, Sacramento CA"
        myname="CDR Mike Fiorino, USN (RC), CNE-C6F Det 802, Atlanta GA"
        myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) TechDevAppUnit NHC, Miami, FL"
        myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) ESRL/GSD/ADB, Boulder, CO"
        myname="Dr. Mike Fiorino (mike@wxmap2.com) WxMAP2 Ave Maria, FL"

        tack2="GrADS (http://grads.iges.org/grads) Graphics by "+myname
        tack2="Diagnostics/graphics by "+myname
        tack2=myname
        if(model == 'ifs'):
            tack1="ECMWF Data Courtesy of ERA-40 Project"
            fullmod="ECM(IFS)"

        if(model == 'ecm' or model == 'ecm2'):
            tack1="ECMWF Data Courtesy of NCEP/NCO"
            fullmod="ECMWF(IFS)"

        if(model == 'ecm4'):
            tack1="ECMWF Data Courtesy of NCEP/NCO"
            fullmod="ECMWF(HRES)"

        if(model == 'ecm5'):
            tack1="ECMWF Data Courtesy of ECMWF ERA"
            fullmod="ECMWF(HRES)"

        if(model == 'jgsm'):
            tack1="GSM Data Courtesy of JMA"
            fullmod="JMA(GSM)"

        if(model == 'cgd2'):
            tack1="CMC Data Courtesy of CMC"
            fullmod="CMC(CGD)"

        if(model == 'ecmt'):
            tack1="ECMWF Data Courtesy of ECMWF TIGGE Server"
            fullmod="ECMWF(IFS)"

        if(model == 'ecmn'):
            tack1="ECMWF Data Courtesy of NWS/AWIPS"
            fullmod="ECMWF(IFS)"

        if(model == 'ecmg'):
            tack1="ECMWF Data Courtesy of ECMWF"
            fullmod="ECMWF(IFS)"

        if(model == 'ngp2'):
            tack1="NOGAPS Data Courtesy of NCEP/NCO"
            fullmod="NOGAPS"

        if(model == 'ngpc'):
            tack1="NOGAPS Data Courtesy of FNMOC/CAGIPS"
            fullmod="NOGAPS"

        if(model == 'navg'):
            tack1="NAVGEM Data Courtesy of NCEP/NCO"
            fullmod="NAVGEM"

        if(model == 'gfsc'):
            tack1="GFS Data Courtesy of FNMOC/CAGIPS"
            fullmod="GFS"

        if(model == 'ngpj'):
            tack1="NOGAPS Data Courtesy of FNMOC/CAGIPS"
            fullmod="NOGAPS"

        if(model == 'ukmc'):
            tack1="UKMO 1.0 deg Data Courtesy of FNMOC/CAGIPS"
            fullmod="UKMO"

        if(model  ==  'jmac'):
            tack1="JMA GSM 1.0 deg Data Courtesy of FNMOC/CAGIPS"
            fullmod="JMA(GSM)"

        if(model == 'cmc' or model == 'cmc2'):
            tack1="CMC Data Courtesy of NCEP/NCO"
            fullmod="CMC(CEM)"

        if(model == 'ngp' or model == 'ngp2'):
            tack1="NOGAPS Data Courtesy of FNMOC, Monterey, CA"
            fullmod="NOGAPS"

        if(model == 'ngp05'):
            tack1="NOGAPS Data Courtesy of FNMOC, Monterey, CA"
            fullmod="NOGAPS05"

        if(model == 'era15'):
            tack1="ECMWF ReAnalysis (ERA-15) Courtesy of ECMWF and PCMDI, LLNL"
            fullmod="ECM(ERA15)"

        if(model == 'gfs' or model == 'gfs2'):
            tack1="NCEP GFS courtesy NCEP/NCO"
            fullmod="NCEP(GFS)"

        if(mf.find(model,'fim')):
            tack1="ESRL FIM courtesy ESRL/GSD/FRD"
            fullmod="ESRL(FIM)"

        if(model == 'fv3e'):
            tack1="ESRL FV3 GFS courtesy ESRL/GSD/FRD"
            fullmod="ESRL(FV3-GFS)"
        if(model == 'fv3g'):
            tack1="ESRL FV3 GF Physics courtesy ESRL/GSD/FRD"
            fullmod="ESRL(FV3-GF)"

        if(mf.find(model,'fimx')):
            tack1="ESRL FIMX courtesy ESRL/GSD/FRD"
            fullmod="ESRL(FIMX)"

        if(model == 'nr1'):
            tack1="NCEP/NCAR R1 Global Reanalysis Data courtesy NOAA CDC"
            fullmod="NCEP(R1)"

        if(model  ==  'ukm' or model == 'ukm2'):
            tack1="UKMO 0.8 deg data courtesy of NCEP/NCO"
            fullmod="UKMO"

        if(model  ==  'ocn'):
            tack1="0 h FNMOC 1.0 deg files courtesy of FNMOC"
            fullmod="UKMO"

        if(model  ==  'gsm'):
            tack1="0-72 hr GSM 1.25 deg files courtesy of JMA (ftp://ddb.kishou.go.jp/pub/DATA/jp034/g02YYMMDDHH)"
            fullmod="JMA(GSM)"

        return(myname,tack1,tack2,fullmod)

    def PlotXsYs(self,model,area):

        xs=self.W2_PLOT_XSIZE

        if(model == 'nr1' or area == 'jtwcaor' or area == 'nhcaor'):
            xs=900

        ys=int(xs*3.0/4.0)

        return(xs,ys)


    def SetWxmapurls(self):

        url={}

        url['tc','tropwpac']="http://grads.iges.org/pix/allwpac.html"
        url['tc','tropwpac']="http://weather.unisys.com/hurricane/w_pacific/W2_CUR_YEAR/index.html"

        url['tc','tropepac']="http://grads.iges.org/pix/allepac.html"
        url['tc','tropepac']="http://weather.unisys.com/hurricane/e_pacific/W2_CUR_YEAR/index.html"

        url['tc','troplant']="http://grads.iges.org/pix/allatla.html"
        url['tc','troplant']="http://weather.unisys.com/hurricane/atlantic/W2_CUR_YEAR/index.html"

        url['tc','tropswpac']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"
        url['tc','tropio']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"
        url['tc','tropnio']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"
        url['tc','tropsio']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"
        url['tc','tropsoz']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"


        url['tc','aor']="http://grads.iges.org/pix/allatla.html"

        url['tc','global']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"

        #
        # TC struct cgi
        #
        url['tcstruct']="/cgi-bin/wxmap2/tcstruct.cgi"

        nrlpacbase='http://www.nrlmry.navy.mil/sat-bin/display10?PHOT=yes&AREA=pacific'
        nrllantbase='http://www.nrlmry.navy.mil/sat-bin/display10?PHOT=yes&AREA=atlantic'
        url['sat','tropwpac']=nrlpacbase+'/western/tropics&PROD=ir&NAV=tropics&CGI=tropics.cgi&ARCHIVE=Latest&MOSAIC_SCALE=15&CURRENT=LATEST.jpg'

        url['sat','global']="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html"

        url['sat','tropepac']=nrlpacbase+'/eastern/tropics&PROD=ir&NAV=tropics&CGI=tropics.cgi&ARCHIVE=Latest&MOSAIC_SCALE=15%&CURRENT=LATEST.jpg'

        url['sat','troplant']=nrllantbase+'/stiched&PROD=ir&NAV=tropics&ARCHIVE=Latest&CGI=tropics.cgi&MOSAIC_SCALE=15%'

        url['sat','troplant']=nrllantbase+'/stitched&PROD=ir&NAV=tropics&CGI=tropics.cgi&ARCHIVE=Latest&MOSAIC_SCALE=15&CURRENT=LATEST.jpg'

        url['sat','aor']="http://www.nrlmry.navy.mil/sat-bin/display3?phot=yes&dir=goes8_images/trop_atlantic_ir&type=jpeg"

        url['sat','conus']='http://www.weather.com/weather/sat/ussat_720x486.html'
        url['sat','conus']='http://maps.weather.com/images/sat/ussat_720x486.jpg'
        url['sat','ausnz']="http://208.134.241.135/images/sat/aussiesat_720x486.jpg"
        url['sat','europe']="http://208.134.241.135/images/sat/europesat_720x486.jpg"
        url['sat','europe']="http://208.134.241.135/images/sat/europesat_720x486.jpg"
        url['sat','europe']="http://www.meto.gov.uk/satpics/latest_vis.jpg"
        url['sat2','europe']="http://www.meto.gov.uk/satpics/latest_ir.jpg"

        url['sat','nhem']="http://www.meto.gov.uk/satpics/latest_vis.jpg"
        url['sat2','nhem']="http://www.meto.gov.uk/satpics/latest_ir.jpg"

        url['sat','africa']="http://maps.weather.com/images/sat/africasat_720x486.jpg"
        url['sat','asia']='http://www.npmoc.navy.mil/satimages/gmsa.jpg'

        url['sat','sam']="http://maps.weather.com/images/sat/sasat_720x486.jpg"
        url['sat','ausnz']="http://maps.weather.com/images/sat/aussiesat_720x486.jpg"
        url['sat','swasia']="http://maps.weather.com/images/sat/mideastsat_720x486.jpg"
        url['sat','whitbread']="http://maps.weather.com/images/sat/pacglobsat_720x486.jpg"

        cimssbase='http://cimss.ssec.wisc.edu/tropic/real-time'

        url['sat_v_hi','troplant']=cimssbase+'/atlantic/winds/wg8wvir.gif'
        url['sat_v_lo','troplant']=cimssbase+'/atlantic/winds/wg8ir.gif'
        url['sat_v_sh','troplant']=cimssbase+'/atlantic/winds/wg8shr.gif'

        url['sat_v_hi','tropwpac']=cimssbase+'/westpac/winds/wgmswv.gif'
        url['sat_v_lo','tropwpac']=cimssbase+'/westpac/winds/wgmsir.gif'
        url['sat_v_sh','tropwpac']=cimssbase+'/westpac/winds/wgmsshr.gif'

        url['sat_v_hi','tropepac']=cimssbase+'/eastpac/winds/wg9wvir.gif'
        url['sat_v_lo','tropepac']=cimssbase+'/eastpac/winds/wg9ir.gif'
        url['sat_v_sh','tropepac']=cimssbase+'/eastpac/winds/wg9shr.gif'

        url['sat_v_hi','tropnio']=cimssbase+'/indian/winds/wm5wv.gif'
        url['sat_v_lo','tropnio']=cimssbase+'/indian/winds/wm5ir.gif'
        url['sat_v_sh','tropnio']=cimssbase+'/indian/winds/wm5shr.gif'

        url['sat_v_hi','tropsio']=cimssbase+'/indian/winds/wm5wv.gif'
        url['sat_v_lo','tropsio']=cimssbase+'/indian/winds/wm5ir.gif'
        url['sat_v_sh','tropsio']=cimssbase+'/indian/winds/wm5shr.gif'

        url['sat_v_hi','tropoz']=cimssbase+'/shemi/winds/wgmswvs1.gif'
        url['sat_v_lo','tropoz']=cimssbase+'/shemi/winds/wgmsirs1.gif'
        url['sat_v_sh','tropoz']=cimssbase+'/shemi/winds/wgmsshSW.gif'

        url['sat_v_hi','tropswpac']=cimssbase+'/seastpac/winds/wg10swvir.gif'
        url['sat_v_lo','tropswpac']=cimssbase+'/seastpac/winds/wg10sir.gif'
        url['sat_v_sh','tropswpac']=cimssbase+'/seastpac/winds/wg10sshr.gif'

        url['wxmap','nlmoc']="http://www1.nlmoc.navy.mil:83/wxmap/web/wx.htm"
        url['wxmap','pcmdi']="http://www-pcmdi.llnl.gov/fiorino/wxmap"

        url['whitbread','whitbread']="http://www.whitbread.org"

        return(url)

    def tc_plot_area(self,lat,lon):

        areas=[]
        if( (lat <= 20) and (lon >= 60 and lon <=220 ) ):
            areas.append('bigaus')

        if( (lat < 10 ) and (lon>30 and lon <130) ): 
            areas.append('tropsio')

        if(lat < 0 and (lon>=90 and lon<180)):
            areas.append('tropoz')

        if( (lat < 50 and lat > -10) and (lon>30 and lon <100)):
            areas.append('tropnio')

        if(lat < 20 and (lon>=130 and lon<360)):
            areas.append('tropswpac')

        if(lat > -10 and (lon>=100 and lon<180)):
            areas.append('tropwpac')

        epac=( (lon>=276 and lon<=282 and lat<9 )
               or (lon>=273 and lon<276 and lat<12 )
               or (lon>=267 and lon<273 and lat<15 )
               or (lon>=261 and lon<267 and lat<17 )
               )

        lant=( (lon>=276 and lon<=282 and lat>=9 )
               or (lon>=273 and lon<276 and lat>=12 )
               or (lon>=267 and lon<273 and lat>=15 )
               or (lon>=261 and lon<267 and lat>=17 )
               )

        if( ( (lat > 0) and (lon>=180 and lon<261)) or epac):
            areas.append('tropepac')

        if( ( (lat > 0) and (lon>=276 and lon<=360) ) or lant):
            areas.append('troplant')

        return(areas)


    def TcstructDb(self,dtg,dbdir):

        stms=[]
        stmareas={}

        verb=1
        dbpath="%s/tc.db.%s.txt"%(dbdir,dtg)

        try:
            cards=open(dbpath).readlines()
        except:
            cards=None

        if(cards == None):
            return(None)

        for card in cards:

            tt=card.split()
            stm=tt[0]
            rlat=float(tt[1])
            rlon=float(tt[2])
            vmax=tt[3]
            rmax=tt[4]
            r34=tt[5]
            areastc=self.tc_plot_area(rlat,rlon)
            stmareas[stm]=areastc
            stms.append(stm)

        return(stmareas)


    def ModelRunSyn(self,dtg):

        hmodels=[]

        curhh=dtg[8:10]
        for model in W2_MODELS:

            if(curhh == '00' and W2_MODELS_Run00):
                hmodels.append(model)
            elif(curhh == '06' and W2_MODELS_Run06):
                hmodels.append(model)
            elif(curhh == '12' and W2_MODELS_Run12):
                hmodels.append(model)
            elif(curhh == '18' and W2_MODELS_Run18):
                hmodels.append(model)


        return(hmodels)




    def ModelPlotDb(self,hmodels,dtg,dotau=0):

        verb=0

        modelplots={}
        modelpareas={}
        modelptypes={}

        pdirbase=w2.W2BaseDirWeb

        for model in hmodels:

            pareas=[]
            ptypes=[]

            pdir="%s/%s/%s"%(pdirbase,w2.W2ModelPltDir(model),dtg)
            pmask="%s/*.png"%(pdir)


            paths=glob.glob(pmask)

            for path in paths:

                (dir,file)=os.path.split(path)

                tt=file.split('.')
                ptype=tt[1]
                ptau=tt[2]
                parea=tt[3]

                if(ptype != 'clm'):
                    modelplots[model,ptype,ptau,parea]=1
                    ptypes.append(ptype)
                    pareas.append(parea)



            if(pareas):
                upareas=mf.uniq(pareas)
            else:
                upareas=pareas

            if(ptypes):
                uptypes=mf.uniq(ptypes)
            else:
                uptypes=ptypes

            modelpareas[model]=upareas
            modelptypes[model]=uptypes


        return(modelplots,modelpareas,modelptypes)


    def SetHtmlProp(self,baseicon,baseicontop):

        width={}

        width['maptitle']=300
        width['mapname']=50
        width['tau']=32
        width['movie']=40

        width['c1']=125
        width['c1b']=200
        width['c2']=650
        width['vbb']=64
        width['vbbs']=50
        width['vplot']=900

        #
        #  inside buttons
        #

        button={}

        button['tc','img']="%stc.info.small.gif"%(baseicon)
        button['tc','alt']="tcinfo"
        button['tcstruct','img']="%stcstruct.gif"%(baseicon)
        button['tcstruct','alt']="tcstruct"
        button['allmap','img']="%sall.maps.gif"%(baseicon)
        button['allmap','alt']="all maps"
        button['alltimes','img']="%sall.times.gif"%(baseicon)
        button['alltimes','alt']="all times"
        button['fnmoc_sst','img']="%sfnmoc.sst.gif"%(baseicon)
        button['fnmoc_sst','alt']="SST"

        button['sat','img']="%ssatpix.gif"%(baseicon)
        button['sat','alt']="sat pix"

        button['sat_v_hi','img']="%ssatwind.vapor.gif"%(baseicon)
        button['sat_v_hi','alt']="V vapor"

        button['sat_v_lo','img']="%ssatwind.vis.gif"%(baseicon)
        button['sat_v_lo','alt']="V vis"

        button['sat_v_ir','img']="%ssatwind.ir.gif"%(baseicon)
        button['sat_v_ir','alt']="V IR"

        button['wxmap','nlmoc']="%snlmoc.wxmap.big.gif"%(baseicon)
        button['wxmap','nlmoc']="Navy WXMAP"
        button['wxmap','pcmdi']="%spcmdi.wxmap.big.gif"%(baseicon)
        button['wxmap','pcmdi']="PCMDI WXMAP"


        buttontop={}

        buttontop['tc','img']="%stc.info.small.gif"%(baseicontop)
        buttontop['tc','alt']="tcinfo"
        buttontop['tcstruct','img']="%stcstruct.gif"%(baseicontop)
        buttontop['tcstruct','alt']="tcstruct"
        buttontop['allmap','img']="%sall.maps.gif"%(baseicontop)
        buttontop['allmap','alt']="all maps"
        buttontop['alltimes','img']="%sall.times.gif"%(baseicontop)
        buttontop['alltimes','alt']="all times"
        buttontop['fnmoc_sst','img']="%sfnmoc.sst.gif"%(baseicontop)
        buttontop['fnmoc_sst','alt']="SST"
        buttontop['sat','img']="%ssatpix.gif"%(baseicontop)
        buttontop['sat','alt']="sat pix"
        buttontop['sat_v_hi','img']="%ssatwind.vapor.gif"%(baseicontop)
        buttontop['sat_v_hi','alt']="V vapor"
        buttontop['sat_v_lo','img']="%ssatwind.vis.gif"%(baseicontop)
        buttontop['sat_v_lo','alt']="V vis"
        buttontop['sat_v_ir','img']="%ssatwind.ir.gif"%(baseicontop)
        buttontop['sat_v_ir','alt']="V IR"
        buttontop['wxmap','nlmoc']="%snlmoc.wxmap.big.gif"%(baseicontop)
        buttontop['wxmap','nlmoc']="Navy WXMAP"
        buttontop['wxmap','pcmdi']="%spcmdi.wxmap.big.gif"%(baseicontop)
        buttontop['wxmap','pcmdi']="PCMDI WXMAP"

        return(width,button,buttontop)


    def PlotTaus(self,ptaus,model):

        if(ptaus == 'default'):
            taubeg=0
            tauend=W2_MODELS_NTAU[model]
            tauinc=W2_MODELS_TauInc[model]
        else:
            tt=ptaus.split()
            taubeg=int(tt[0])
            tauend=int(tt[1])
            tauinc=int(tt[2])

        taus=range(taubeg,tauend+1,tauinc)
        return(taus)

        
    def IsPltFileThere(self,modelplots,model,modelplot,ctau,area):

        try:
            there=modelplots[model,modelplot,ctau,area]
        except:
            there=0
        return(there)


    def PltHtmFiles(self,basewxmap,hfilehead,gfilehead,gfilehttp,
                    modelplots,model,modelplot,ctau,area):                    
                    
        hfile="%s/%s.%s.%s.%s.htm"%(hfilehead,model,modelplot,ctau,area)
        hfile2="%s.%s.%s.%s.htm"%(model,modelplot,ctau,area)
        gfile="%s.%s.%s.%s.png"%(gfilehead,modelplot,ctau,area)

        urlhfile="%s/%s/%s.%s.%s.%s.htm"%(basewxmap,hfilehead,model,
                                          modelplot,
                                          ctau,
                                          area)

        urlgfile="%s/%s/%s%s.%s.%s.%s.png"%(basewxmap,gfilehttp,
                                            model,W2_MODELS_GRF_EXT,
                                            modelplot,
                                            ctau,
                                            area)

        #print gfile,hfile
        #print urlhfile
        #print urlgfile

        return(hfile,hfile2,gfile,urlhfile,urlgfile)

    def PltHtmHead(self,modeldesc,dtg,tau,plotdesc):
        
        web1="""
<html>
<head>

<link rel=\"shortcut icon\" href=\"favicon.ico\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/wxmain.css\">
<title>%s %s %d h </title>

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da>
<script language=\"javascript\" src=\"../../js/wxmain.js\" type=\"text/javascript\"></script>

<table class='title'>
<tr><td width=900>
%s <font color=red><i>%s</font></i> <font color=blue>t = %d h</font> forecast of %s</td>
</tr>
</table>

<table border=1 cellpadding=0 cellspacing=0>
<tr>"""%(modeldesc,dtg,tau,
         modeldesc,dtg,tau,plotdesc)
        return(web1)


    def ModelHtmProps(self,model,dtg,
                      baseicon,
                      model_grf_ext):

        bgmodel="%s/%s"%(baseicon,W2_MODELS_BKG[model])
        webmodeldir="web_%s"%(model)
        hfilehead="%s/%s"%(webmodeldir,dtg)
        gfilehead="%s%s"%(model,model_grf_ext)
        gfilehttp="%s/%s"%(self.W2_MODELS_HTTP_GDIR[model],dtg)

        center=W2_MODELS_CENTER[model]
        modeldesc=W2_MODELS_DESC[model]
        praccum=W2_MODELS_PRaccum[model]

        return(bgmodel,webmodeldir,
               hfilehead,gfilehead,gfilehttp,
               center,modeldesc,praccum)


    def ModelHtmLink(self,urlfile,baseicon,model,modelplot):

        htm="""<td>
<a href=\"%s\">
<img src=\"%s/%s.fcst.gif\" img border=\"0\">
</a>
</td>"""%(urlfile,baseicon,model)


        htm2="""<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(modelplot,urlfile)


        return(htm2)


    def OtherModelHtmLink(self,urlfile,baseicon,omodel,modelplot):

        modbutton="btnsml%s"%(omodel)
    
        htm2="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(modbutton,modbutton,modbutton,
          omodel.upper(),urlfile)

        return(htm2)



    def TcstructHtmLink(self,w2urls):

        htm="""<td>
<input type='button' class='btn75'
onMouseOver=\"className='btn75over';\" onMouseOut=\"className='btn75';\"
value='TCstruct' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>"""%(w2urls['tcstruct'])

        return(htm)

    def AllMapsTausHtmLink(self,model,modelplot,ctau,area):

        urlamfile="%s.allmap.%s.%s.htm"%(model,ctau,area)
        urlatfile="%s.alltau.%s.%s.htm"%(model,modelplot,area)

        htm="""<td>
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='Allmaps' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>

<td>
<input type='button' class='btn50'
onMouseOver=\"className='btn50over';\" onMouseOut=\"className='btn50';\"
value='Alltaus' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>"""%(urlamfile,urlatfile)

        return(htm)

    def SatHtmLinks(self,url,area):

        satbutton="btn60sat"
        htm=''
        htmadd=''

        try:
            if(url['sat',area]):
                htmadd="""
<td class=button><a href=\"%s\" >SatPix</td>
    """%(url['sat',area])

                htmadd="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(satbutton,satbutton,satbutton,
              'SatPix',url['sat',area])

        except:
            htmadd=''

        htm=htm+htmadd



        try:
            if(url['sat_v_hi',area]):
                htmadd="""
<td class=button><a href=\"%s\" >SatVhi</td>
"""%(url['sat_v_hi',area])
            htmadd="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(satbutton,satbutton,satbutton,
          'SatVhi',url['sat_v_hi',area])
        except:
            htmadd=''

        htm=htm+htmadd

        
        try:     
            if(url['sat_v_lo',area]):
                htmadd="""
<td class=button><a href=\"%s\" >SatVlo</td>
"""%(url['sat_v_lo',area])
                htmadd="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(satbutton,satbutton,satbutton,
          'SatVlo',url['sat_v_lo',area])

        except:
            htmadd=''

        htm=htm+htmadd

        try:
            if(url['sat_v_sh',area]):
                htmadd="""
<td class=button><a href=\"%s\" >SatVSh</td>
"""%(url['sat_v_sh',area])

                htmadd="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(satbutton,satbutton,satbutton,
              'SatVSh',url['sat_v_sh',area])

        except:
            htmadd=''

        htm=htm+htmadd

        return(htm)
         

    def TcstructCarqStmsHtmLinks(self,stmareas,dtg,area,model):

        htm=''
        tcs=[]
        for carqstm in stmareas.keys():
            careas=stmareas[carqstm]
            for carea in careas:
                if(carea == area):
                    tcfull=carqstm
                    tc=tcfull.split('.')[0]
                    tcs.append(tc)
                    cgiurl='/cgi-bin/wxmap2/tcstruct.cgi'
                    cgiopt="dtg=%s&storm=%s&model=%s&tau=undef"%(dtg,tcfull,model)
                    htmadd="""<td class=button2>
<a href=\"%s?%s\"><b><i>%s</i></b></a></td>"""%(cgiurl,cgiopt,tc)

                    htmadd2="""<td>
<input type='button' class='btn50b'
onMouseOver=\"className='btn50bover';\" onMouseOut=\"className='btn50b';\"
value='%s' name=tctrk
onClick=\"cvalue=\'%s?%s\';opentype='page',swaphtm();\">
</td>"""%(tc,cgiurl,cgiopt)

                    htm=htm+htmadd2


        return(htm,tcs)

    def SstHtmLinks(self,ocnplotsm00,ocnplotsm12,ocnplotsm24,
                    dtg,area):


        basewxmap=W2_HTML_BASE
        baseicon=W2_HTML_BASE_ICON
        model_grf_ext=W2_MODELS_GRF_EXT
        ocnplot='sst'
        ocnmodel='ocn'
        octau='000'

        if(len(ocnplotsm00) > 0):
            ocnplots=ocnplotsm00
        elif(len(ocnplotsm12) > 0):
            ocnplots=ocnplotsm12
        elif(len(ocnplotsm24) > 0):
            ocnplots=ocnplotsm24


        if(IsPltFileThere(ocnplots,ocnmodel,ocnplot,octau,area)):

            rc=ModelHtmProps(ocnmodel,dtg,baseicon,model_grf_ext)
            (bgmodel,webmodeldir,
             hfilehead,gfilehead,gfilehttp,
             center,modeldesc,praccum)=rc
            rc=PltHtmFiles(basewxmap,hfilehead,gfilehead,gfilehttp,
                                 ocnplots,ocnmodel,ocnplot,octau,area)
            (hfile,hfile2,gfile,urlhfile,urlgfile)=rc


            htm2="""<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='%s' name=tctrk
onClick=\"cvalue='%s';opentype='page',swaphtm();\">
</td>"""%(ocnplot,urlhfile)

        return(htm2)


    def ModelHomeHtmLinks(self,hmodels,area,dtg):

        htm=''
        htmadd=''

        basewxmap=W2_HTML_BASE
        for hmodel in hmodels:
            modbutton="btn75%s"%(hmodel)
            if(hmodel != 'ocn'):
                htmadd="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s home' name=tctrk
onClick=\"cvalue=\'%s/%s.%s.%s.htm\';opentype='page',swaphtm();\">
</td>"""%(modbutton,modbutton,modbutton,
          hmodel.upper(),basewxmap,hmodel,area,dtg)
            
            htm=htm+htmadd

        return(htm)


    def Wxmap2HomeHtmLinks(self):
    
        basewxmap=W2_HTML_BASE
        htm="""<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2 Home' name=tctrk
onClick=\"cvalue=\'%s/wx.htm\';opentype='page',swaphtm();\">
</td>"""%(basewxmap)

        return(htm)

    def Wxmap2HelpHtmLinks(self):
    
        basewxmap=W2_HTML_BASE
        htm="""<td>
<input type='button' class='btn75a'
onMouseOver=\"className='btn75aover';\" onMouseOut=\"className='btn75a';\"
value='Help' name=tctrk
onClick=\"cvalue=\'%s/wx.help.htm\';opentype='page',swaphtm();\">
</td>"""%(basewxmap)

        return(htm)


    def LoopModeHtmLinks(self,model,dtg,modelplot,area):

        basewxmap=W2_HTML_BASE
        urlmoviefile="%s/web_%s/%s/%s.movie.%s.%s.htm"%(basewxmap,model,
                                                    dtg,model,modelplot,area)
        htm="""<td>
<input type='button' class='btn125'
onMouseOver=\"className='btn125over';\" onMouseOut=\"className='btn125';\"
value='Loop Mode' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>"""%(urlmoviefile)

        return(htm)

    def SingleModeHtmLinks(self,model,dtg,modelplot,area):

        basewxmap=W2_HTML_BASE
        urltau000file="%s/web_%s/%s/%s.%s.000.%s.htm"%(basewxmap,model,
                                                   dtg,model,modelplot,area)
        htm="""<td>
<input type='button' class='btn125a'
onMouseOver=\"className='btn125aover';\" onMouseOut=\"className='btn125a';\"
value='Single Tau' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>"""%(urltau000file)

        return(htm)


    def TauButtonsHtmLinks(self,modelplots,model,modelplot,area,dtg,
                           curtau,taus):

        basewxmap=W2_HTML_BASE
        baseicon=W2_HTML_BASE_ICON
        model_grf_ext=W2_MODELS_GRF_EXT

        htm=''
    
        for tau in taus:
            ctau="%03d"%(tau)

            if(IsPltFileThere(modelplots,model,
                              modelplot,ctau,area)):

                urltaufile="%s/web_%s/%s/%s.%s.%s.%s.htm"%(basewxmap,model,
                                                           dtg,model,modelplot,ctau,area)

                taubutton="%s/tau.%s.gif"%(baseicon,ctau)
                if(curtau == ctau): taubutton="%s/tau.%s.display.gif"%(baseicon,ctau)

                htmadd="""
<td><a href=\"%s\"><img src=\"%s\" img border=\"0\"></a></td>"""%(urltaufile,taubutton)
                htm=htm+htmadd

        #
        # do not bother implementing +/-12 h buttons...
        #


        return(htm)


    def ImageHtmLinks(self,urlgfile):
    
        htm="""
<table border=1 cellpadding=0 cellspacing=0>
<tr>
<td width=%d>
<img src=\"%s\">"""%(self.W2_PLOT_XSIZE,urlgfile)

        return(htm)


    def PrevRunsHtmLinks(self,modelplots,model,modelplot,area,dtg,
                         curtau,taus,width):

        baseicon=W2_HTML_BASE_ICON

        htm="""</td>
<td valign=top align=left width=%d >
"""%(width['vbbs'])

        taus=[12,24,36,48,72,96,120]
        taus.reverse()

        for tau in taus:

            ntau=-tau
            pdtg=mf.dtginc(dtg,ntau)

            ctau="%03d"%(tau)
            basewxmap=W2_HTML_BASE
            urlfile="%s/web_%s/%s/%s.%s.%s.%s.htm"%(basewxmap,model,pdtg,
                                                     model,modelplot,
                                                     ctau,area)
            htmadd="<a href=\"%s\"><img src=\"%s/prevrun.m%dh.gif\" img border=\"0\" alt=\"%d\"></a>\n"%(urlfile,baseicon,tau,tau)

            htm=htm+htmadd

        taus.reverse()

        for tau in taus:

            ptau=tau
            ntau=int(curtau)-tau

            if(ntau > 0): 
                ndtg=mf.dtginc(dtg,ptau)
                cntau="%03d"%(ntau)
                basewxmap=W2_HTML_BASE
                urlfile="%s/web_%s/%s/%s.%s.%s.%s.htm"%(basewxmap,model,ndtg,
                                                     model,modelplot,
                                                     cntau,area)

                htmadd="<a href=\"%s\"><img src=\"%s/nextrun.p%dh.gif\" img border=\"0\" alt=\"%s\"></a>\n"%(urlfile,baseicon,tau,tau)

                #print 'uuu pppp',htmadd

                htm=htm+htmadd

        htm=htm+"""</td>
 """
        #
        # previous analyses
        #


        if(curtau == '000'):

            htm=htm+"""<td valign=top align=left width=%d >
"""%(width['vbbs'])

            taus=[12,24,36,48,72]
            taus.reverse()

            for tau in taus:

                ntau=-tau
                pdtg=mf.dtginc(dtg,ntau)

                basewxmap=W2_HTML_BASE
                urlfile="%s/web_%s/%s/%s.%s.000.%s.htm"%(basewxmap,model,pdtg,
                                                        model,modelplot,
                                                        area)
                htmadd="""<a href=\"%s\">
<img src=\"%s/prevanal.m%dh.gif\" img border=\"0\" alt=\"%d\">
</a>\n"""%(urlfile,baseicon,tau,tau)

            ###print 'uuu nnnn',htmadd
                htm=htm+htmadd

            taus.reverse()

            for tau in taus:

                ptau=tau
                ndtg=mf.dtginc(dtg,ptau)
                basewxmap=W2_HTML_BASE
                urlfile="%s/web_%s/%s/%s.%s.000.%s.htm"%(basewxmap,model,ndtg,
                                                        model,modelplot,
                                                        area)

                htmadd="""<a href=\"%s\">
<img src=\"%s/nextanal.p%dh.gif\" img border=\"0\" alt=\"%s\">
</a>\n"""%(urlfile,baseicon,tau,tau)


                htm=htm+htmadd


        htmadd="""</td>
</tr>
</table>

</body>
</html>
"""
        htm=htm+htmadd


        return(htm)

    def AllmapHtmHead(self,model,dtg,curtau,area,modeldesc):
    
        ampath="%s/web_%s/%s/%s.allmap.%s.%s.htm"%(self.W2_BDIRWEB,model,dtg,model,curtau,area)
    
        htm="""<html>
<head>
<link rel=\"shortcut icon\" href=\"favicon.ico\">
<title>All Maps for %s t= %d h</title>
</head>
<body>
<b>%s <font color=red><i>$tdtg</font></i> <font color=blue>All Maps</font></b><br>
</body>
Click on the map to return to that individual map<br>"""%(modeldesc,int(curtau),modeldesc)

        return(htm,ampath)


    def AllmapHtmLink(self,modeldesc,dtg,tau,plotdesc,
                      urlhfile,urlgfile):

        htm="""
<br><b>%s t = %d forecast of %s</b><br>
<a href=\"%s\">
<img src=\"%s\" img border=\"0\">
</a>"""%(modeldesc,tau,plotdesc,urlhfile,urlgfile)

        return(htm)


    def AlltauHtmHead(self,model,dtg,curtau,area,modeldesc,
                      modelplot,plotdesc):

        atpath="%s/web_%s/%s/%s.alltau.%s.%s.htm"%(self.W2_BDIRWEB,model,dtg,model,modelplot,area)

        htm="""<html>
<head>
<link rel=\"shortcut icon\" href=\"favicon.ico\">
<title>All Taus for: %s</title>
</head>
<br><b>%s <font color=red><i>%s</font></i> %s maps for
<font color=blue>All Times</font> </b><br>
<body>
Click on the map to return to that individual map<br>"""%(modeldesc,modeldesc,dtg,plotdesc)

        return(htm,atpath)


    def AlltauHtmLink(self,modeldesc,dtg,tau,plotdesc,
                      urlhfile,urlgfile):

        htm="""
<br><b>%s t = $%d h forecast </b><br>
<a href=\"%s\"><img src=\"%s\">
</a>"""%(modeldesc,tau,urlhfile,urlgfile)

        return(htm)


    def MovieHtmHead(self,model,dtg,curtau,area,modeldesc,
                     modelplot,plotdesc):

        moviepath="%s/web_%s/%s/%s.movie.%s.%s.htm"%(self.W2_BDIRWEB,model,dtg,model,modelplot,area)

        htm="""<html>
    <head>
    <link rel=\"shortcut icon\" href=\"favicon.ico\">
    <link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/wxmain.css\">
    <title>%s %s Movie</title>
    </head>
    <body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad="launch()">
    <script language=\"javascript\" src=\"../../js/wxmain.js\" type=\"text/javascript\"></script>

    <table class=title>
    <tr><td width=900>
    %s <font color=red><i>%s</font></i> <b>Loop</b> of %s
    </td>
    </tr>
    </table>
    <table border=1 cellpadding=0 cellspacing=0>
    <tr>"""%(modeldesc,modelplot,modeldesc,dtg,plotdesc)

        return(htm,moviepath)
    

    def MovieOtherModelHtmLink(self,omodel,dtg,curtau,area,modeldesc,
                               modelplot,plotdesc):

        omodelmoviepath="%s/web_%s/%s/%s.movie.%s.%s.htm"%(self.W2_BDIRWEB,
                                                           omodel,dtg,
                                                           omodel,modelplot,area)

        modbutton="btn75%s"%(omodel)
    
        htm="""<td>
<input type='button' class='%s'
onMouseOver=\"className='%sover';\" onMouseOut=\"className='%s';\"
value='%s loop' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>"""%(modbutton,modbutton,modbutton,
          omodel.upper(),omodelmoviepath)

        return(htm)


    def MovieBreakRow(self,nbutton,nbreak):

        htm=None
        if(nbutton%nbreak == 0):
            htm="""
</tr><tr>
</table><table border=1 cellpadding=0 cellspacing=0>
"""
        return(htm)


    def MovieOtherPlotHtmLink(self,model,dtg,curtau,area,modeldesc,
                              modelplot,plotdesc):
    
        oplotmoviepath="%s/web_%s/%s/%s.movie.%s.%s.htm"%(self.W2_BDIRWEB,
                                                          model,dtg,
                                                          model,modelplot,area)

        htm="""<td>
<input type='button' class='btn75'
onMouseOver=\"className='btn75over';\" onMouseOut=\"className='btn75';\"
value='%s loop' name=tctrk
onClick=\"cvalue=\'%s\';opentype='page',swaphtm();\">
</td>"""%(modelplot,oplotmoviepath)

        return(htm)


    def MovieHtmLink(self,modeldesc,dtg,tau,plotdesc,
                     urlhfile,urlgfile):

        htm="""
<br><b>%s t = $%d h forecast </b><br>
<a href=\"%s\"><img src=\"%s\">
</a>"""%(modeldesc,tau,urlhfile,urlgfile)

        return(htm)


    def MovieJsHead(self,model,area,dtg,taus,modelplot):

        basewxmap=W2_HTML_BASE
        baseicon=W2_HTML_BASE_ICON
        model_grf_ext=W2_MODELS_GRF_EXT

        gfilehttp="%s/%s/"%(basewxmap,W2_MODELS_HTTP_GDIR[model])

        taubeg=taus[0]
        tauend=taus[-1]
        tauinc=W2_MODELS_TauInc[model]

        beg_tau_count=(taubeg/tauinc)+1
        last_tau_count=(tauend/tauinc)+1

        #
        # mf 20010523 -- last_tau_count is really number of images in loop
        #
        last_tau_count=last_tau_count - beg_tau_count + 1

        image_beg_tau="%03d"%(taubeg)
        fcst_begin=taubeg

        jshead="""
<SCRIPT LANGUAGE=\"JavaScript\">
// <!--
//
// step 1: define above the location of the images
//
//============================================================
//                >> jsImagePlayer 1.0 <<
//            for Netscape3.0+, September 1996
//============================================================
//                  by (c)BASTaRT 1996
//             Praha, Czech Republic, Europe
//
// feel free to copy and use as long as the credits are given
//          by having this header in the code
//
//          contact: xholecko\@sgi.felk.cvut.cz
//          http://sgi.felk.cvut.cz/~xholecko
//
//============================================================
// Thanx to Karel & Martin for beta testing and suggestions!
//============================================================
//
//     modified by D. Watson and A. Earnhart (CIRA/CSU), 7/30/97
//     and Greg Thompson (NCAR/RAP) Dec. 11 1997
//
//============================================================

//********* SET UP THESE VARIABLES - MUST BE CORRECT!!!*********************

//
// step 2: define variables used to determine images
//
image_plot=\"%s\";
image_area=\"%s\";
image_dtg=\"%s\";
image_href=\"%s\";
image_model_type=\"%s\";
image_model_res=\"%s\";
image_model = image_href + image_dtg + \"/\" + image_model_type + image_model_res ;
image_beg_tau= \"%s\";

first_image = %s;
last_image = %s;
fcst_begin = %s;

fcst_increment = %d;
image_type = \"png\";
"""%(modelplot,area,dtg,gfilehttp,model,
         model_grf_ext,
         image_beg_tau,beg_tau_count,last_tau_count,
         fcst_begin,tauinc)


        return(jshead)


    def MovieJsBody(self,model,area,dtg,taus,modelplot):

        jsbody="""
//
// step 3: define dimensions of image (would be nice if this were interactively done)
//         Presently these ARE NOT used below. See step 9
//

animation_height  = 743;
animation_width  = 1225;

//**************************************************************************

//=== THE CODE STARTS HERE - no need to change anything below ===

//=== global variables ====
theImages = new Array();      //holds the images
imageNum = new Array();       //keeps track of which images to omit from loop
normal_delay = 500;
delay = normal_delay;         //delay between frames in 1/100 seconds
delay_step = 50;
delay_max = 4000;
delay_min = 50;
dwell_multipler = 3;
dwell_step = 1;
end_dwell_multipler   = dwell_multipler;
start_dwell_multipler = dwell_multipler;
current_image = first_image;     //number of the current image
timeID = null;
status = 0;                      // 0-stopped, 1-playing
play_mode = 0;                   // 0-normal, 1-loop, 2-sweep
size_valid = 0;

//===> Make sure the first image number is not bigger than the last image number
if (first_image > last_image)
{
   var help = last_image;
   last_image = first_image;
   first_image = help;
}

//===> Preload the first image (while page is downloading)
   theImages[0] = new Image();
//
// step 4: construct filename of first image
//
   theImages[0].src = image_model + \".\" + image_plot + \".\" + 
                      image_beg_tau + \".\" + image_area + \".\" + image_type;
   imageNum[0] = true;

//==============================================================
//== All previous statements are performed as the page loads. ==
//== The following functions are also defined at this time.   ==
//==============================================================

//===> Stop the animation
function stop()
{
//== cancel animation (timeID holds the expression which calls the fwd or bkwd function) ==
  if (status == 1)
    clearTimeout (timeID);
  status = 0;
}


//===> Display animation in fwd direction in either loop or sweep mode
function animate_fwd()
{
   current_image++;                      //increment image number

  //== check if current image has exceeded loop bound ==
  if (current_image > last_image) {
    if (play_mode == 1) {              //fwd loop mode - skip to first image
      current_image = first_image;
    }
    if (play_mode == 2) {              //sweep mode - change directions (go bkwd)
      current_image = last_image;
      animate_rev();
      return;
    }
  }

  //== check to ensure that current image has not been deselected from the loop ==
  //== if it has, then find the next image that hasn't been ==
  while (imageNum[current_image-first_image] == false) {
    current_image++;
    if (current_image > last_image) {
      if (play_mode == 1)
        current_image = first_image;
      if (play_mode == 2) {
        current_image = last_image;
        animate_rev();
        return;
      }
    }
  }

  document.animation.src = theImages[current_image-first_image].src;   //display image onto screen
  document.control_form.frame_nr.value = current_image;                //display image number

  delay_time = delay;
  if ( current_image == first_image) delay_time = start_dwell_multipler*delay;
  if (current_image == last_image)   delay_time = end_dwell_multipler*delay;

  //== call \"animate_fwd()\" again after a set time (delay_time) has elapsed ==
  timeID = setTimeout(\"animate_fwd()\", delay_time);
}


//===> Display animation in reverse direction
function animate_rev()
{
  current_image--;                      //decrement image number

  //== check if image number is before lower loop bound ==
  if (current_image < first_image) {
    if (play_mode == 1) {               //rev loop mode - skip to last image
       current_image = last_image;
    }
    if (play_mode == 2) {
      current_image = first_image;     //sweep mode - change directions (go fwd)
      animate_fwd();
      return;
    }
  }

  //== check to ensure that current image has not been deselected from the loop ==
  //== if it has, then find the next image that hasn't been ==
  while (imageNum[current_image-first_image] == false) {
    current_image--;
    if (current_image < first_image) {
      if (play_mode == 1)
        current_image = last_image;
      if (play_mode == 2) {
        current_image = first_image;
        animate_fwd();
        return;
      }
    }
  }

  document.animation.src = theImages[current_image-first_image].src;   //display image onto screen
  document.control_form.frame_nr.value = current_image;                //display image number

  delay_time = delay;

  if ( current_image == first_image) delay_time = start_dwell_multipler*delay;
  if (current_image == last_image)   delay_time = end_dwell_multipler*delay;

  //== call \"animate_rev()\" again after a set amount of time (delay_time) has elapsed ==
  timeID = setTimeout(\"animate_rev()\", delay_time);
}


//===> Changes playing speed by adding to or substracting from the delay between frames
function change_speed(dv)
{
  delay+=dv;
  //== check to ensure max and min delay constraints have not been crossed ==
  if(delay > delay_max) delay = delay_max;
  if(delay < delay_min) delay = delay_min;
}

//===> functions that changed the dwell rates.
function change_end_dwell(dv) {
  end_dwell_multipler+=dv;
  if ( end_dwell_multipler < 1 ) end_dwell_multipler = 0;
}

function change_start_dwell(dv) {
  start_dwell_multipler+=dv;
  if ( start_dwell_multipler < 1 ) start_dwell_multipler = 0;
}

//===> Increment to next image
function incrementImage(number)
{
  stop();

  //== if image is last in loop, increment to first image ==
  if (number > last_image) number = first_image;

  //== check to ensure that image has not been deselected from loop ==
  while (imageNum[number-first_image] == false) {
    number++;
   if (number > last_image) number = first_image;
  }

  current_image = number;
  document.animation.src = theImages[current_image-first_image].src;   //display image
  document.control_form.frame_nr.value = current_image;                //display image number
}

//===> Decrement to next image
function decrementImage(number)
{
  stop();

  //== if image is first in loop, decrement to last image ==
  if (number < first_image) number = last_image;

  //== check to ensure that image has not been deselected from loop ==
  while (imageNum[number-first_image] == false) {
    number--;
   if (number < first_image) number = last_image;
  }

  current_image = number;
  document.animation.src = theImages[current_image-first_image].src;   //display image
  document.control_form.frame_nr.value = current_image;                //display image number
}

//===> \"Play forward\"
function fwd()
{
  stop();
  status = 1;
  play_mode = 1;
  animate_fwd();
}

//===> \"Play reverse\"

function rrev()
{
  stop();
  status = 1;
  play_mode = 1;
  animate_rev();
}

//===> \"play sweep\"
function sweep() {
  stop();
  status = 1;
  play_mode = 2;
  animate_fwd();
}

//===> Change play mode (normal, loop, swing)
function change_mode(mode)
{
   play_mode = mode;
}

//===> Load and initialize everything once page is downloaded (called from 'onLoad' in <BODY>)
function launch()
{
  for (var i = first_image + 1; i <= last_image; i++)
  {
    if ( fcst_begin > 0)
      var fcst_length = fcst_begin+(i-1)*fcst_increment;
    else var fcst_length = (i-1)*fcst_increment;

    theImages[i-first_image] = new Image();

//
// step 5: construct filenames of rest of images (conditional adds '0' to numbers less than 10)
//

    if ( fcst_length < 10)
      theImages[i-first_image].src = 
         image_model + \".\" + image_plot + \".\" + 
         \"00\" + fcst_length + \".\" + image_area + \".\" + image_type;
    else if( fcst_length < 100) 
      theImages[i-first_image].src = 
         image_model + \".\" + image_plot + \".\" + 
         \"0\" + fcst_length + \".\" + image_area + \".\" + image_type;
    else 
      theImages[i-first_image].src = 
         image_model + \".\" + image_plot + \".\" + 
               fcst_length + \".\" + image_area + \".\" + image_type;

      imageNum[i-first_image] = true;
      document.animation.src = theImages[i-first_image].src;
      document.control_form.frame_nr.value = i;

  }

  // this needs to be done to set the right mode when the page is manually reloaded
  change_mode (1);
  fwd();
}

//===> Check selection status of image in animation loop
function checkImage(status,i)
{
  if (status == true)
    imageNum[i] = false;
  else imageNum[i] = true;
}

//==> Empty function - used to deal with image buttons rather than HTML buttons
function func()
{
}

//===> Sets up interface - this is the one function called from the HTML body
function animation()
{
  count = first_image;
}

// -->

</SCRIPT>


<NOSCRIPT>
<P ALIGN=LEFT>
<BR>
<H1>
This requires Javascript for an animation of the model forecast plots.
You will need Netscape version 3.0 or higher or Internet Explorer 3.0
or higher and Javascript enabled to view this.
</H1>
</P>
</NOSCRIPT>
<!-- Write javascript code --------------------------------------->



<SCRIPT>
//--------------------------------------------------------------
//Javascript slider code
//--------------------------------------------------------------

versionButton = 1

var browser = new Object();

if (navigator.appName.substring(0,8) == \"Netscape\")
{
browser.name = \"NN\";
}

if (navigator.appName.substring(0,9) == \"Microsoft\")
{
browser.name = \"MSIE\";
}


browser.version = Math.round(parseFloat(navigator.appVersion) * 1000);

if ((browser.name == \"MSIE\" && browser.version >= 4000) || (browser.name == \"NN\" && browser.version >= 3000)) versionButton = 3; 
if (versionButton == 3)
{"""

        basewxmap=W2_HTML_BASE
        baseicon=W2_HTML_BASE_ICON
        model_grf_ext=W2_MODELS_GRF_EXT
        gfilehttp="%s/%s/"%(basewxmap,W2_MODELS_HTTP_GDIR[model])
        taubeg=taus[0]
        tauend=taus[-1]
        tauinc=W2_MODELS_TauInc[model]
        beg_tau_count=(taubeg/tauinc)+1
        last_tau_count=(tauend/tauinc)+1
        baseicon=W2_HTML_BASE_ICON

        for i in range(beg_tau_count,last_tau_count+1):
            hh="""
      toc%don = new Image(60, 20);
      toc%don.src = \"%s/on.slider.gif\";
"""%(i,i,baseicon)
            jsbody=jsbody+hh

        for i in range(beg_tau_count,last_tau_count+1):
            hh="""
      toc%doff = new Image(60, 20);
      toc%doff.src = \"%s/off.slider.gif\";
"""%(i,i,baseicon)
            jsbody=jsbody+hh

        hh="""
}

function img_act(imgName,imgNum)
{
  if (versionButton == 3)
  {
   stop();
   current_image = imgNum;
   //display image
   document.animation.src = theImages[current_image-first_image].src;
   //display image number
   document.control_form.frame_nr.value = current_image;
    imgOn = eval(imgName + \"on.src\");
    document [imgName].src = imgOn;
  }
}


function img_inact(imgName)
{
  if (versionButton == 3)
  {
    imgOff = eval(imgName + \"off.src\");
    document [imgName].src = imgOff;
  }
}

// -->

</script>

<!-- End of Write javascript code ------------------------------------->
"""
        jsbody=jsbody+hh

        hh="""
<! //
<! // step 8: define location of buttons
<! //

<P ALIGN=left>
<TABLE ALIGN=left BORDER=1 CELLPADDING=0 CELLSPACING=0>
  <TR>
  <TD ALIGN=CENTER VALIGN=MIDDLE>
    <IMG NAME=\"animation\" width=720 height=540 BORDER=0 ALT=\"image\">
  </TD>
    <TD BGCOLOR=\"#9FC1FF\" WIDTH=100 ALIGN=CENTER VALIGN=MIDDLE>
      <FONT SIZE=-1 COLOR=\"#3300CC\"> Loop Mode:</FONT><BR>
      <A HREF=\"JavaScript: func()\" onClick=\"change_mode(1);fwd()\">
      <IMG BORDER=0 SRC=\"%s/nrm_button.gif\" ALT=\"Normal\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"sweep()\">
      <IMG BORDER=0 SRC=\"%s/swp_button.gif\" ALT=\"Back and Forth\"></A>
      <BR> <HR WIDTH=\"70%%\" SIZE=2>
      <FONT SIZE=-1 COLOR=\"#3300CC\">Animate Frames:</FONT><BR>
      <A HREF=\"JavaScript: func()\" onClick=\"change_mode(1);rrev()\">
      <IMG BORDER=0 SRC=\"%s/rev_button.gif\" ALT=\"REV\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"stop()\">
      <IMG BORDER=0 SRC=\"%s/stp_button.gif\" ALT=\"STOP\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"change_mode(1);fwd()\">
      <IMG BORDER=0 SRC=\"%s/fwd_button.gif\" ALT=\"FWD\"></A>
      <BR> <HR WIDTH=\"70%%\" SIZE=2>
      <FONT SIZE=-1 COLOR=\"#3300CC\"> Dwell First:</FONT><BR>
      <A HREF=\"JavaScript: func()\" onClick=\"change_start_dwell(-dwell_step)\">
      <IMG BORDER=0 SRC=\"%s/dw1_minus.gif\" ALT=\"dec start dwell\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"change_start_dwell(dwell_step)\">
      <IMG BORDER=0 SRC=\"%s/dw1_plus.gif\" ALT=\"inc start dwell\"></A><BR>
      <FONT SIZE=-1 COLOR=\"#3300CC\"> Dwell Last:</FONT><BR>
      <A HREF=\"JavaScript: func()\" onClick=\"change_end_dwell(-dwell_step)\">
      <IMG BORDER=0 SRC=\"%s/dw2_minus.gif\" ALT=\"dec end dwell\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"change_end_dwell(dwell_step)\">
      <IMG BORDER=0 SRC=\"%s/dw2_plus.gif\" ALT=\"inc end dwell\"></A>
      <BR> <HR WIDTH=\"70%%\" SIZE=2>
      <FONT SIZE=-1 COLOR=\"#3300CC\">Adjust Speed:</FONT><BR>
      <A HREF=\"JavaScript: func()\" onClick=\"change_speed(delay_step)\">
      <IMG BORDER=0 SRC=\"%s/slw_button.gif\" ALT=\"--\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"change_speed(-delay_step)\">
      <IMG BORDER=0 SRC=\"%s/fst_button.gif\" ALT=\"++\"></A>
      <BR> <HR WIDTH=\"70%%\" SIZE=2>
      <FONT SIZE=-1 COLOR=\"#3300CC\">Advance One:</FONT><BR>
      <A HREF=\"JavaScript: func()\" onClick=\"decrementImage(--current_image)\">
      <IMG BORDER=0 SRC=\"%s/mns_button.gif\" ALT=\"-1\"></A>
      <A HREF=\"JavaScript: func()\" onClick=\"incrementImage(++current_image)\">
      <IMG BORDER=0 SRC=\"%s/pls_button.gif\" ALT=\"+1\"></A>
      <HR WIDTH=\"70%%\" SIZE=2>
      <FORM METHOD=\"POST\" NAME=\"control_form\">
      <FONT SIZE=-1 COLOR=\"#3300CC\">Frame No:</FONT>
        <FONT SIZE=-1>
          <INPUT TYPE=\"text\" NAME=\"frame_nr\" VALUE=9 SIZE=\"1\" onFocus=\"this.select()\" 
            onChange=\"go2image(this.value)\">
          </INPUT>
        </FONT>
      </FORM>
<font SIZE=-1 COLOR=#3300CC>Frame Slider</font>
<table BORDER=0 CELLSPACING=0 CELLPADDING=0 BGCOLOR=\"#999999\">
<tr>

"""%(baseicon,baseicon,baseicon,baseicon,baseicon,
     baseicon,baseicon,baseicon,baseicon,baseicon,
     baseicon,baseicon,baseicon)

        jsbody=jsbody+hh


        sliderwidth=6
        sliderheight=20
        for i in range(beg_tau_count,last_tau_count+1):
            hh="""<td>
<a href=JavaScript:func() 
onMouseover = img_act(\'toc%d\',%d) onMouseout = img_inact(\'toc%d\')>
<img src=\' %s/off.slider.gif\' width=%d height=%d border=0 name=\'toc%d\'></a>
</td>"""%(i,i,i,baseicon,sliderwidth,sliderheight,i)
            jsbody=jsbody+hh


        hh="""
     </tr>
   </table>
  </TD>
</TR>
</TABLE>
</P>
</body>
</html>
"""
        
        jsbody=jsbody+hh

        return(jsbody)


    def ModelHomeHtmHead(self,model,dtg,taus,width,
                         modeldesc,
                         baseicon,baseicontop,
                         basewxmap,basewxmaptop,
                         prodcenter,area,areadesc):

        htm1="""<html>
<head>
<link rel=\"shortcut icon\" href=\"favicon.ico\">
<title>%s %s WxMaps -- %s</title>

<style type=\"text/css\">
table {
	font-family : Verdana, Geneva, Arial, Helvetica, sans-serif;
	font-size :9pt;
	font-style : normal;
	font-weight : normal;
	vertical-align : middle;
/*background-color: gold*/
}
</style>
</head>
<body background=\"icon/bkgred.gif\" TEXT=\"#000000\" LINK=\"#0000FF\" VLINK=\"#006030\">
<h2><font face=\"arial\"><i>%s WxMaps</i></font><br>
<font face=\"arial\"color=red>%s Home Page for: %s</font><br>
<font face=\"arial\"color=blue><i>%s</i></font></h2>
<table border=1 cellpadding=0 cellspacing=0>
<caption align=center>
</caption>
"""%(prodcenter,modeldesc,areadesc,
     prodcenter,modeldesc,dtg,areadesc)

        htm2="""
<tr>
<td align=right colspan=3>Forecast Time [h]</td>"""

        for tau in taus:
            htm2=htm2+"""
<th width=%s align=center >%d</th>"""%(width['tau'],tau)

        htm2=htm2+"""
</tr>

<tr>
<th width=300 align=center > Weather Map</th>
<th width=50 align=center>Name</th>
<td width=32 align=center>All &tau;</td>
<td width=32 align=center >"""

        for tau in taus:
            htm2=htm2+"""
<a href=\"web_gfs/%s/gfs.allmap.%03d.%s.htm\">
<img src=\"icon/all.maps.button.gif\" ALT=\"All Maps\" img border=\"0\">
</a></th>"""%(dtg,tau,area)


        htm=htm1+htm2
    
        return(htm)

    
    def ModelHomeHtmRowTitle(self,model,dtg,taus,
                             modelplot,plotdesc,
                             width,
                             modeldesc,
                             baseicon,baseicontop,
                             basewxmap,basewxmaptop,
                             prodcenter,area,areadesc):



        return(htm)


