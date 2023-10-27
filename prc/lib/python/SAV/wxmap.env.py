import os

W2_OPS=1
W2_CLEAN_NDAY=10
W2_CLEAN_NDAY_DAT=5

W2_USE_NGP_LDM=1

W2_USE_RSYNC=1
W2_USE_RSYNC=0

W2_CUR_YEAR='2006'

WXMAP2_BDIR="/dat/nwp/wxmap2"

W2_BDIR=os.getenv("W2_BDIR")
W2_PERL_DIR=os.getenv("W2_PERL_DIR")
W2_PRC_W2_DIR=os.getenv("W2_PRC_W2_DIR")
W2_PRC_TC_DIR=os.getenv("W2_PRC_TC_DIR")

W2_PROD_CENTER="NPMOC/JTWC"

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

W2_GEODIR=W2_BDIR+'/dat/geog'
W2_CLIMOSST=W2_BDIR+'/dat/climo/sst'

W2_PRC_HTML_DIR=W2_BDIR+'/prc/html'
W2_PRC_DAT_DIR=W2_BDIR+'/prc/dat'
W2_JUNK_FILE='/tmp/wxmap.zy0x1w2.tmp'

W2_BASEMAP_GDIR=W2_BDIR+'/grf/basemap'

##################################################
#
#	HTML
#
##################################################

W2_HTML_BASE= "wxmap"                   # 970707 change to the op dirs

W2_HTML_BASE_DOC= "wxmap/doc"

W2_HTML_BASE_CLASSES= "wxmap/classes"

W2_HTML_BASE_GRF= "fiorino/wxmap/grf"

W2_HTML_BASE_HREF= 'http://wxmap2/'

W2_HTML_BASE_ICON= 'icon'

W2_HTML_BASE= '../../../'

W2_HTML_BASE_TOP= ''

W2_HTML_BASE_DOC= '../../../doc/'
W2_HTML_BASE_CLASSES= '../../../classes/'
W2_HTML_BASE_GRF= '../../../grf/'
W2_HTML_BASE_ICON= '../../../icon/'

W2_HTML_BASE_DOC_TOP= 'doc/'
W2_HTML_BASE_CLASSES_TOP= 'classes/'
W2_HTML_BASE_GRF_TOP= 'grf/'
W2_HTML_BASE_ICON_TOP= 'icon/'

W2_WEB_DIR="/dat/nwp/wxmap/web"  # 970707 change to the op dirs
W2_ICON_DIR=W2_WEB_DIR+'/icon'

W2_PLOT_XSIZE= '720'
W2_PLOT_YSIZE= '540'

###################################################
#
#	AREA PROPERTIES
#	JTWC
#
###################################################

#----------------------------------------------------------------------
#  shem TC season
#----------------------------------------------------------------------

# -- change to NIO vice whole IO and SIO

W2_AREAS = [
    'asia',
    'wconus',
    'conus',
    'bigaus',
    'tropwpac',
    'tropnio',
    'tropsio',
    'tropoz',
    'tropswpac',
    'tropepac',
    'troplant',
]

W2_AREAS_TYPES = {
    'asia':'midlat',
    'wconus':'midlat',
    'conus':'midlat',
    'bigaus':'special',
    'tropwpac':'tropic',
    'tropnio':'tropic',
    'tropsio':'tropic',
    'tropoz':'tropic',
    'tropswpac':'tropic',
    'tropepac':'tropic',
    'troplant':'tropic',
}

W2_AREAS_DESC = {
    'asia':'East Asia',
    'wconus':'WConus',
    'conus':'Conus',
    'bigaus':'Big Aus',
    'tropwpac':'Tropical WPAC',
    'tropnio':'Tropic NIO',
    'tropsio':'Tropical SIO',
    'tropoz':'Tropical Oz',
    'tropswpac':'Tropical SWPAC',
    'tropepac':'Tropical EPAC',
    'troplant':'Tropical LANT',
}

# -- 20200318 -- reduced
#
W2_AREAS = [
    'conus',
    'tropwpac',
    'tropepac',
    'troplant',
]

W2_AREAS_TYPES = {
    'conus':'midlat',
    'tropwpac':'tropic',
    'tropepac':'tropic',
    'troplant':'tropic',
}

W2_AREAS_DESC = {
    'conus':'Conus',
    'tropwpac':'Tropical WPAC',
    'tropepac':'Tropical EPAC',
    'troplant':'Tropical LANT',
}

W2_PLOT_TYPES="midlat:special:tropic"
W2_PLOT_TYPES_PLOTS="500 psl 850 prp:uas u20 u50 prp:uas prp 500"
W2_PLOT_TYPES_TAUS="default:default:default:0 240 24"


###################################################
#
#	MODEL PROPERTIES
#       JTWC
#
###################################################

# 20020603 - no mrf
# 20020605 - add ukm

W2_MODELS=[
    'avn',
    'ngp',
    'ukm',
    'gsm',
]

W2_MODELS_RES={
    'avn':'10',
    'ngp':'10',
    'ukm':'12',
    'gsm':'12',
}

W2_MODELS_CENTER={
    'avn':'ncep',
    'ngp':'fnmoc',
    'ukm':'ukmo',
    'gsm':'jma',
}

W2_MODELS_ARCHIVE_DATDIR={
    'avn':W2_DAT_BDIR+'/dat',
    'ngp':W2_DAT_BDIR+'/dat',
    'ukm':W2_DAT_BDIR+'/dat',
    'gsm':W2_DAT_BDIR+'/dat',
    'nr1':W2_DAT_BDIR+'/dat',
}


W2_MODELS_GRF_EXT='10'

W2_MODELS_HTTP_GDIR=[
    'ncep.avn.grf',
    'fnmoc.nogaps.grf',
    'ncep.ukm.grf',
    'jma.gsm.grf',
]

W2_MODELS_DESC={
    'avn':'NCEP GFS',
    'ngp':'FNMOC NOGAPS',
    'ukm':'UKMO',
    'gsm':'JMA GSM',
}

W2_MODELS_BKG={
    'avn':'bkgred.gif',
    'ngp':'bkgblue.gif',
    'ukm':'bkggreen.gif',
    'ukm':'bkgyello.gif',
}

W2_MODELS_RUN00={
    'avn':1,
    'ngp':1,
    'ukm':1,
    'gsm':1,
}

W2_MODELS_RUN06={
    'avn':1,
    'ngp':1,
    'ukm':0,
    'gsm':0,
}

W2_MODELS_RUN12={
    'avn':1,
    'ngp':1,
    'ukm':1,
    'gsm':1,
}

W2_MODELS_RUN18={
    'avn':1,
    'ngp':1,
    'ukm':0,
    'gsm':0,
}

W2_MODELS_NTAU={
    'avn':144,
    'ngp':144,
    'ukm':72,
    'gsm':72,
}

W2_MODELS_DATA_NTAU={
    'avn':144,
    'ngp':144,
    'ukm':72,
}

W2_MODELS_TAUINC={
    'avn':12,
    'ngp':12,
    'ukm':12,
    'gsm':12,
}

W2_MODELS_PRACCUM={
    'avn':6,
    'ngp':12,
    'ukm':12,
    'gsm':6,
}

W2_MODELS_HTML_DIR={
    'avn':'avn/archive',
    'ngp':'ngp/archive',
    'ukm':'ukm/archive',
    'gsm':'gsm/archive',
}

W2_MODELS_ADD_MAPS={

    'avn':1,
    'ngp':0,
    'ukm':0,
    'gsm':0,
}

W2_MODELS_COLOR={
    'avn':'red',
    'ngp':'navy',
    'ukm':'green',
    'gsm':'yellow',
}

W2_MODELS_UCASE={
    'avn':'AVN',
    'ngp':'NGP',
    'ukm':'UKM',
    'gsm':'GSM',
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

W2_TC_STRUCT_DAT_DIR="/wxmap_old/dat2/tc/tcstruct"
W2_TC_STRUCT_DAT_DIR="/dat/nwp/dat/tc/tcstruct"
W2_TC_STRUCT_PZAL_DIR="/tdocommon/wxmap/dat/tc/tcstruct"
W2_TC_ECMWF_PLT_DIR="/dat/nwp/dat/tc/plt/ecmwf"
W2_TC_ECMWF_PLT_PZAL_DIR="/tdocommon/wxmap/web/ecmwf"


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

plot_control['ausnz','tmx','units']="C"
plot_control['ausnz','tmn','units']="C"

plot_control['bigaus','tmx','units']="C"
plot_control['bigaus','tmn','units']="C"

plot_control['aoe1','tmx','units']="F"
plot_control['aoe1','tmn','units']="F"

plot_control['wconus','tas','units']="F"
plot_control['conus','tas','units']="F"

plot_control['europe','tas','units']="C"
plot_control['asia','tas','units']="F"

plot_control['tropepac','tas','units']="C"
plot_control['tropwpac','tas','units']="C"
plot_control['tropswpac','tas','units']="C"
plot_control['uk','tas','units']="C"
plot_control['africa','tas','units']="C"


plot_control['ngp','wconus','plots']="w20 500 850 lmq mhq psl prp uas wav"
plot_control['ngp','wconus','taus']="default"
plot_control['avn','wconus','plots']="w20 500 850 lmq mhq psl prp uas tmx tmn"
plot_control['avn','wconus','taus']="default"
plot_control['ukm','wconus','plots']="w20 500 850 lmq mhq psl uas"
plot_control['ukm','wconus','taus']="default"

plot_control['ngp','conus','plots']="w20 500 850 lmq mhq psl prp uas wav"
plot_control['ngp','conus','taus']="default"
plot_control['avn','conus','plots']="w20 500 850 lmq mhq psl prp uas tmx tmn"
plot_control['avn','conus','taus']="default"
plot_control['ukm','conus','plots']="w20 500 850 lmq mhq psl uas"
plot_control['ukm','conus','taus']="default"

plot_control['ngp','asia','plots']="w20 500 850 psl prp wav"
plot_control['ngp','asia','taus']="default"
plot_control['avn','asia','plots']='w20 500 850 psl prp tmx tmn'
plot_control['avn','asia','taus']="default"
plot_control['ukm','asia','plots']='w20 500 850'
plot_control['ukm','asia','taus']="default"

plot_control['ngp','ausnz','plots']="w20 500 850 psl prp uas wav"
plot_control['ngp','ausnz','taus']="default"
plot_control['avn','ausnz','plots']="w20 500 850 prp uas"
plot_control['avn','ausnz','taus']="default"
plot_control['ukm','ausnz','plots']="w20 500 850 uas"
plot_control['ukm','ausnz','taus']="default"

plot_control['ngp','sam','plots']="500 850 psl prp wav"
plot_control['ngp','sam','taus']="default"
plot_control['avn','sam','plots']="500 850 psl prp"
plot_control['avn','sam','taus']="default"
plot_control['ukm','sam','plots']="w20 500 850 uas wav"
plot_control['ukm','sam','taus']="default"

plot_control['ngp','africa','plots']="500 850 psl prp wav"
plot_control['ngp','africa','taus']="default"
plot_control['avn','africa','plots']="500 850 psl prp"
plot_control['avn','africa','taus']="default"
plot_control['ukm','africa','plots']="w20 500 850 uas"
plot_control['ukm','africa','taus']="default"

##################################################
#
#   special
#
##################################################

aoeplot="w20 lmq mhq 500 850 uas prp psl"
aoeplot_ukm="w20 lmq 500 850 uas psl"

plot_control['ngp','aoe1','plots']=aoeplot+'wav'
plot_control['ngp','aoe1','taus']="default"
plot_control['avn','aoe1','plots']=aoeplot+' tmx tmn'
plot_control['avn','aoe1','taus']="default"
plot_control['ukm','aoe1','plots']=aoeplot_ukm
plot_control['ukm','aoe1','taus']="default"

plot_control['ngp','bigaus','plots']="w20 500 850 psl prp wav"
plot_control['ngp','bigaus','taus']="default"
plot_control['avn','bigaus','plots']="u20 w20 lmq mhq 500 850 psl prp tmx tmn"
plot_control['avn','bigaus','taus']="default"
plot_control['ukm','bigaus','plots']="w20 500 850 psl"
plot_control['ukm','bigaus','taus']="default"

##################################################
#
#   tropics
#
##################################################

plots_shem_tropical_season="u20 w20 500 uas prp"
plots_nhem_tropical_season="u20 w20 u50 500 850 uas prp"
plots_nhem_tropical_season_wav="u20 w20 u50 500 850 uas prp wav"
plots_nhem_tropical_season_full="wdl u20 w20 u50 500 u70 w70 850 uas prp"
plots_nhem_tropical_season_full="wdl u20 w20 lmq u50 500 u70 w70 850 uas prp"
plots_nhem_tropical_season_full_wav="plots_nhem_tropical_season_full wav"

plots_nhem_tropical_season_ukm="wdl u20 w20 lmq u50 500 u70 w70 850 uas"
plots_nhem_tropical_season_full_q="wdl u20 w20 lmq mhq u50 500 u70 w70 850 uas prp psl"
plots_nhem_tropical_season_full_wav_q="wdl u20 w20 lmq mhq u50 500 u70 w70 850 uas prp wav psl"

#
# 20000630 - add waves to nhem tropical season
#

plot_control['ngp','tropwpac','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropwpac','taus']="default"
plot_control['avn','tropwpac','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropwpac','taus']="default"
plot_control['ukm','tropwpac','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropwpac','taus']="default"

#
#  20050419 -- add gsm in tropwpac only
#
plot_control['gsm','tropwpac','plots']=plots_nhem_tropical_season_full_q
plot_control['gsm','tropwpac','taus']="default"

plot_control['ngp','tropepac','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropepac','taus']="default"
plot_control['avn','tropepac','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropepac','taus']="default"
plot_control['ukm','tropepac','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropepac','taus']="default"

plot_control['ngp','tropswpac','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropswpac','taus']="default"
plot_control['avn','tropswpac','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropswpac','taus']="default"
plot_control['ukm','tropswpac','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropswpac','taus']="default"

plot_control['ngp','troplant','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','troplant','taus']="default"
plot_control['avn','troplant','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','troplant','taus']="default"
plot_control['ukm','troplant','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','troplant','taus']="default"

plot_control['ngp','tropio','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropio','taus']="default"
plot_control['avn','tropio','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropio','taus']="default"
plot_control['ukm','tropio','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropio','taus']="default"

plot_control['ngp','tropnio','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropnio','taus']="default"
plot_control['avn','tropnio','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropnio','taus']="default"
plot_control['ukm','tropnio','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropnio','taus']="default"

plot_control['ngp','tropsio','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropsio','taus']="default"
plot_control['avn','tropsio','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropsio','taus']="default"
plot_control['ukm','tropsio','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropsio','taus']="default"

plot_control['ngp','tropoz','plots']=plots_nhem_tropical_season_full_wav_q
plot_control['ngp','tropoz','taus']="default"
plot_control['avn','tropoz','plots']=plots_nhem_tropical_season_full_q
plot_control['avn','tropoz','taus']="default"
plot_control['ukm','tropoz','plots']=plots_nhem_tropical_season_ukm
plot_control['ukm','tropoz','taus']="default"

##################################################
#
#   special/misc
#
##################################################

plot_control['ukm','uk','plots']="500 psl 850 uas"
plot_control['ukm','uk','taus']="default"
plot_control['ngp','uk','plots']="500 psl 850 prp uas wav"
plot_control['ngp','uk','taus']="default"

plot_control['ukm','africa','plots']="500 prp wav tas"
plot_control['ukm','africa','taus']="default"
plot_control['ngp','africa','plots']="500 prp wav"
plot_control['ngp','africa','taus']="default"

wxmap_maxplot_area['ngp']=999
wxmap_maxplot_area['avn']=999
wxmap_maxplot_area['gsm']=999
wxmap_maxplot_area['ukm']=999
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
wxmap_archive_server="pzal.ndbc.noaa.gov"

###################################################
#
#  971205 - virtual frame buffe controls on stargate (sparc ultra)
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

wxmap_xvfb['avn','d'} = "wxmap_tmpdir/xvfb.avn"
wxmap_xvfb['ngp','d'} = "wxmap_tmpdir/xvfb.ngp"
wxmap_xvfb['Xvfb4','d'} = "wxmap_tmpdir/xvfb.4"

wxmap_xvfb['avn','l'} = "wxmap_tmpdir/lock.avn"
wxmap_xvfb['ngp','l'} = "wxmap_tmpdir/lock.ngp"

wxmap_xvfb['avn','n'} = "1"
wxmap_xvfb['ngp','n'} = "3"
wxmap_xvfb['Xvfb4','n'} = "4"

wxmap_xvfb['avn','X']="stargate:wxmap_xvfb['avn','n'}.0"
wxmap_xvfb['ngp','X']="stargate:wxmap_xvfb['ngp','n'}.0"
wxmap_xvfb['Xvfb4','X']="stargate:wxmap_xvfb['Xvfb4','n'}.0"

}

##################################################
#
#   associative array between plot number and name on graphics file 
#
##################################################


pnam={
    '1':'500',
    '2':'psl',
    '3':'prp',
    '4':'850',
    '5':'tas',
    '6':'uas',
    '7':'u50',
    '8':'u20',
    '9':'u70',
    '10':'sst',
    '11':'wav',
    '12':'w20',
    '13':'wdl',
    '14':'lmq',
    '15':'mhq',
    '20':'tmx',
    '21':'tmn',
    '22':'thk',
    '23':'w70',
    '30':'basemap',
    '50':'clm',
    '60':'stg',
    '61':'st2',
}


pnum={
    '500':'1',
    'psl':'2',
    'prp':'3',
    '850':'4',
    'tas':'5',
    'uas':'6',
    'u50':'7',
    'u20':'8',
    'u70':'9',
    'sst':'10',
    'wav':'11',
    'w20':'12',
    'wdl':'13',
    'lmq':'14',
    'mhq':'15',
    'tmx':'20',
    'tmn':'21',
    'thk':'22',
    'w70':'23',
    'basemap':'30',
    'clm':'50',
    'stg':'60',
    'st2':'61',
}


numplot_delta={
    '500':0,
    'psl':0,
    'prp':-1,
    '850':0,
    'tas':0,
    'uas':0,
    'u50':0,
    'u20':0,
    'sst':0,
    'wav':0,
    'w20':0,
    'wdl':0,
    'lmq':0,
    'mhq':0,
    'tmx':-1,
    'tmn':-1,
    'thk':0,
    'w70':0,
    'basemap':-999,
    'clm':0,
}


maptitle={
    '500':'500 hPa Heights [m] and Rel. Vort [10<sup>-5</sup> s<sup>-1</sup>]',
    '850':'850 hPa Temperature [C], winds [kts] and Rel. Hum. [%]',
    'prp',$pt,
    'psl':'SLP [hPa] & 500-1000 Thkns [m] & 700 hPa Vert. Vel [Pa s<sup>-1</sup>]',
    'u50':'500 hPa Strmlns & Istchs [kt] ; Wind Barbs',
    'u70':'700 hPa Strmlns ; N-S wind componment ; Wind Barbs',
    'u20':'200 hPa Strmlns ; |850-200 Shear| ; 850(Red) /200(Green) Barbs',
    'sst':'SST [C] ; SST Anomaly from AMIP II SST Climatology (1979-96)',
    'uas':'Over Ocean Sfc Winds [kt]',
    'wav':'Sig Wave Heights [ft] ; Over Ocean Sfc Winds [kt]',
    'w20':'200 hPa Streammlines and Isotachs [kt]',
    'wdl':'Deep Layer Mean Streamlines/Isotachs [kt]',
    'lmq':'Low-Mid Trop (925-500) PW [mm] & Flow',
    'mhq':'Mid-High Trop (600-200) PW [mm] & Flow',
    'hhq':'High-High Trop (400-200) PW [mm] & Flow',
    'tmx':'Max Sfc Air Temperature [F] ; AVN Previous 24-h',
    'tmn':'Min Sfc Air Temperature [F] ; AVN Previous 24-h',
    'tas':'Sfc Air Temperature Change [F]',
    'thk':'1000-500 Thickness [dm] and Sea Level Pressure [mb]',
    'w70':'700 hPa Strmlns and Istchs [kt] ; Wind Barbs',
    'clm':'0-5 day mean climo',
}

#
#  URL
#

def SetWxmapurls():

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
    url['tcstruct']="/cgi-bin/wxmap/tcstruct1.cgi"

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
    url['sat','africa']="http://maps.weather.com/images/sat/africasat_720x486.jpg"
    url['sat','asia']='http://www.npmoc.navy.mil/satimages/gmsa.jpg'

    url['sat','sam']="http://maps.weather.com/images/sat/sasat_720x486.jpg"
    url['sat','ausnz']="http://maps.weather.com/images/sat/aussiesat_720x486.jpg"
    url['sat','swasia']="http://maps.weather.com/images/sat/mideastsat_720x486.jpg"
    url['sat','whitbread']="http://maps.weather.com/images/sat/pacglobsat_720x486.jpg"

    cimssbase='http://cimss.ssec.wisc.edu/tropic/real-time'

    url['sat_v_hi','troplant']=cimssbase+'/atlantic/winds/wg8wvir.html'
    url['sat_v_lo','troplant']=cimssbase+'/atlantic/winds/wg8ir.html'
    url['sat_v_sh','troplant']=cimssbase+'/atlantic/winds/wg8shr.html'

    url['sat_v_hi','tropwpac']=cimssbase+'/westpac/winds/wgmswv.html'
    url['sat_v_lo','tropwpac']=cimssbase+'/westpac/winds/wgmsir.html'
    url['sat_v_sh','tropwpac']=cimssbase+'/westpac/winds/wgmsshr.html'

    url['sat_v_hi','tropepac']=cimssbase+'/eastpac/winds/wg9wvir.html'
    url['sat_v_lo','tropepac']=cimssbase+'/eastpac/winds/wg9ir.html'
    url['sat_v_sh','tropepac']=cimssbase+'/eastpac/winds/wg9shr.html'

    url['sat_v_hi','tropnio']=cimssbase+'/indian/winds/wm5wv.html'
    url['sat_v_lo','tropnio']=cimssbase+'/indian/winds/wm5ir.html'
    url['sat_v_sh','tropnio']=cimssbase+'/indian/winds/wm5shr.html'

    url['sat_v_hi','tropsio']=cimssbase+'/indian/winds/wm5wv.html'
    url['sat_v_lo','tropsio']=cimssbase+'/indian/winds/wm5ir.html'
    url['sat_v_sh','tropsio']=cimssbase+'/indian/winds/wm5shr.html'

    url['sat_v_hi','tropoz']=cimssbase+'/winds/wm5wv.html'
    url['sat_v_lo','tropoz']=cimssbase+'/indian/winds/wm5ir.html'
    url['sat_v_sh','tropoz']=cimssbase+'/real-time/indian/winds/wm5shr.html'

    url['sat_v_hi','tropswpac']=cimssbase+'/winds/wgmsirs3.html'
    url['sat_v_lo','tropswpac']=cimssbase+'/shemi/winds/wgmswvs3.html'
    url['sat_v_sh','tropswpac']=cimssbase+'/shemi/winds/wgmsshSE.html'

    url['wxmap','nlmoc']="http://www1.nlmoc.navy.mil:83/wxmap/web/wx.htm"
    url['wxmap','pcmdi']="http://www-pcmdi.llnl.gov/fiorino/wxmap"

    url['whitbread','whitbread']="http://www.whitbread.org"

    return(url)

def tc_plot_area(lat,lon,area):

    if( (lat <= 20) and (lon >= 60 and lon <=220 ) ):
        area="area bigaus"

    if( (lat < 10 ) and (lon>30 and lon <130) ): 
        area="area tropsio"

    if(lat < 0 and (lon>=90 and lon<180)):
        area="area tropoz"

    if( (lat < 50 and lat > -10) and (lon>30 and lon <100)):
        area="area tropnio"

    if(lat < 20 and (lon>=130 and lon<360)):
        area="area tropswpac"

    if(lat > -10 and (lon>=100 and lon<180)):
        area="area tropwpac"

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
        area="area tropepac"

    if( ( (lat > 0) and (lon>=276 and lon<=360) ) or lant):
        area="area troplant"

    return(area)


sub wxmap_master {

local($wb);
$timecdtg=dtg("time");
#
#  UK webmaster
#

$wb="Send Comments to Dr. Mike Fiorino, ERA-40 Consultant <a href=\"mailto:Mike.Fiorino\@ecmwf.int\">Mike.Fiorino\@ecmwf.int</a>, 
<a href=\"http://www.ecmwf.int\">ECMWF</a><br>
<i>Last updated: $timecdtg</i><br>";

#
#  webmaster in Pearl
#
$wb="Send Comments to CDR Mike Fiorino, USN(RC) <a href=\"mailto:fiorino\@llnl.gov\">fiorino\@llnl.gov</a>, 
<a href=\"http://www.npmoc.navy.mil\">NPMOC</a>, <a
href=\"http://www.npmoc.navy.mil/jtwc.html\">JTWC</a><br>
<i>Last updated: $timecdtg</i><br>";


return($wb);

}

sub mod_db_run($curhh) {

    my($curhh)=@_;

    foreach $m (@models) {

        if($curhh eq "00") {
            $model_run=$model_run00{$m};
            } elsif ($curhh eq "06") {
                $model_run=$model_run06{$m};
                } elsif ($curhh eq "12") {
                    $model_run=$model_run12{$m};
                    } elsif ($curhh eq "18") {
                        $model_run=$model_run18{$m};
                    }

        push(@hmodels,$m) if($model_run) ;

    }

    return(@hmodels);

}


sub mod_db_latest_htm {

    my($verb,$curdir,$model,$area,@dtgs,$lastdtg,$latesthtm);

    $verb=0;

    $curdir=`pwd`;
    chomp($curdir);

    undef(@latest_model_htm);
    chdir(W2_WEB_DIR'});
          system('pwd');

          foreach $model (@models) {
              foreach $area (@areas) {

    @ll=<$model.$area.??????????.htm>;

    undef(@dtgs);
    foreach $l (@ll) {
        @tt=split('\.',$l);
        push @dtgs,$tt[2];
#	if($verb) {
#	  print "ll $area :: $l :: $tt[2]\n";
#	}
    }

    sort(@dtgs);

    $lastdtg=$dtgs[$#dtgs];

                   $latesthtm="$model.$area.$lastdtg.htm";

                   $latest_model_htm{$model,$area]=$latesthtm;

#      if($verb) {
#	print "lastdtg: $model :: $area :: $lastdtg $#dtgs \n";
#	print "latesthtm: $latesthtm \n";
#      }

}

    }

    if($verb) {
        foreach $model (@models) {
            foreach $area (@areas) {
                $h=$latest_model_htm{$model,$area};
        print "LMHTM: $model :: $area :: $h\n";
        }
        }
    }

    chdir($curdir);
}

sub mod_db_plot($dotau=0) {

    my($dotau)=@_;

##################################################
#
#   build plot count data base based on model and plot type   
#
##################################################

my($verb);
$verb=0;

local(@fl,$npall,$index,$tt);
my($gg,@gglob,$tau,$taubeg,$tauend);

$ng['all'}=0;

foreach $model (@hmodels) {

    $ng{$model}=0 ;
    $dtg{$model}=$tdtg;
    $ddir="$model_gdir{$model}/$data_time";

    if($tdtghh ne "") {
        $model_chk=$model_run{$model,$tdtghh} ;
        next if($model_chk == 0);
    }

    if($atype ne "") {

        foreach $pt (plot_types($model)) {
            $taubeg=999;
            $tauend=-999;

            $lsmask="$model*${pt}*.gif";
            $lsmask="$model*${pt}*.png";
            if( ! (-d $ddir) ) {
                $ng{$model,$pt}=0;
                } else { 
                    $tt=`(cd $ddir ; ls $lsmask | wc -l)`;

                    if($dotau) {
    @gglob=`(cd $ddir ; ls $lsmask)`;
    foreach $gg (@gglob) {
        @ttt=split('\.',$gg);
#
# 20050525 -- take out clm plots.......
#
        if($ttt[1] ne 'clm') {
            $tau=$ttt[2]*1;
            $taubeg=$tau if($tau < $taubeg) ;
            $tauend=$tau if($tau > $tauend) ;
            #print "GGG: $model :: pt:$pt :: $tau : $taubeg : $tauend : $gg \n";
        }
    }

    $ng{$model,$pt,'taubeg'} = $taubeg;
    $ng{$model,$pt,'tauend'} = $tauend;
    }

    chop($tt);
    $ng{$model,$pt}=$tt*1;
    } 

    print "#plots for $model $pt : $ng{$model,$pt} :: $ng{$model,$pt,'taubeg'} : $ng{$model,$pt,'tauend'}\n" if($verb);
    $ng{$model}=$ng{$model}+$ng{$model,$pt}; 

    open(I,"(cd $ddir ; ls $lsmask) |") || die "Can't list directory $ddir\n" ;
    while ( <I> ) {
        chop ;
        $file = $_ ;
        $gfile_truth{$file}=1;
    }
    close(I);

    }

    } else {

        $lsmask="$model*.gif";
        $lsmask="$model*.png";

        if( ! (-d $ddir) ) {
            $ng{$model}=0;
            } else { 
###	$tt=`ls -1 $ddir | grep ".gif" | grep $model | wc -l`;
$tt=`ls -1 $ddir | grep ".png" | grep $model | wc -l`;

chop($tt);
            print "TTTTTTTTTTTTTTTTTTTTTTTTT mod_db for: $model : tt = $tt\n";
            $ng{$model}=$tt*1;
        } 

    }

    print "#plots for $model ALL : $ng{$model}\n" if($verb);
    $ng['all'} += $ng{$model};

    }

}

sub plot_types {

    local($model)=@_;
    local($i,$pp,@ppp);

    $pp=$plot_type_plots{$atype};

    if($plot_control{$model,$area,'plots'} ne "") {
        $pp=$plot_control{$model,$area,'plots'}  ;
    }

    if($plot_control{$model,'add','plots'} ne "") {
        $pp="$pp $plot_control{$model,'add','plots'}"  ;
    } 

#  $pp=$plot_type_plots{$atype};
#  if($plot_control{$model,$area,'plots'} ne "") {
#    $pp=$plot_control{$model,$area,'plots'}  ;
#  } elsif($plot_control{$model,'add','plots'} ne "") {
#    $pp="$pp $plot_control{$model,'add','plots'}"  ;
#  } 

    @ppp=split(' ',$pp);

    return(@ppp);

}





sub tc_bt_posits($tcopt) {

    my($tcopt)=@_;
    my($tau,$nbt,$bbbbb,@ttt,@tttt,$tcareas);

##################################################
#
# look for TC positions  
#
##################################################\

#
# add look for year+1 for shem
#
if($tcopt eq 'rd') {
    $tcbtpath=WXMAP{"W2_TC_BT_DIR"};
    $tcplotdir=WXMAP{"W2_TC_PLOT_DIR"};
    $ftdir=WXMAP{"W2_TC_FT_DIR"};
    } elsif($tcopt eq 'ops' || $tcopt eq '' || $tcopt =~ 'jtwc' ) { 
        $tcbtpath=WXMAP{"W2_TC_BT_OPS_DIR"};
        $tcplotdir=WXMAP{"W2_TC_PLOT_OPS_DIR"};
        $ftdir=WXMAP{"W2_TC_FT_OPS_DIR"};
    }

$yyyy=substr($tdtg,0,4);
$yyyyp1=$yyyy+1;

$tcbtpath0=$tcbtpath;

if($prodcenter =~ 'JTWC') {
    $tcbtpath="$tcbtpath0/${yyyy}/bt.jtwc.???.????.???.txt";
    $tcbtpathyyyyp1="$tcbtpath0/${yyyyp1}/bt.jtwc.???.????.???.txt";
    } else {
        $tcbtpath="$tcbtpath0/${yyyy}/bt.jtwc.realtime.*txt";
        $tcbtpathyyyyp1="$tcbtpath0/${yyyyp1}/bt.jtwc.realtime.*txt";
    }

$tcbtpath2="$tcbtpath0/${yyyy}/bt.jtwc.atl.????.???.txt";

    @atlpaths=glob("$tcbtpath2");

    if($#atlpaths < 0) {
       $tcbtpath2="";
       }

    $ntc=`grep $tdtg $tcbtpathyyyyp1 $tcbtpath $tcbtpath2 | grep -v lonbnd | wc -l`;
    $ntc=$ntc*1;

    $btdata=`grep -h $tdtg $tcbtpathyyyyp1 $tcbtpath $tcbtpath2 | grep -v lonbnd`;
## $cmd="grep -h $tdtg $tcbtpathyyyyp1 $tcbtpath $tcbtpath2 | grep -v lonbnd";
##print "CCC: $cmd\n"

        @bt=split(' ',$btdata);

        %bttcareas={};
        $bbbbb='';

    if($ntc > 0) {
        for($n=0;$n<$ntc;$n++) {
            $nlat=4+$n*11;
            $nlon=5+$n*11;
            $nmw=2+$n*11;
            $nstmid=1+$n*11;
            $btiii=$bt[$nstmid];
            $areastc1=tc_plot_area($bt[$nlat],$bt[$nlon],'');
            push @bttcs, $bt[$nstmid];
            $bttcareas{$bt[$nstmid]}=$areastc1;
###     print "TC: $n :: $nstmid :: $bt[$nstmid] : $bt[$nlat] $bt[$nlon] $bt[$nmw] :: $areastc1 \n"; 
$bbbbb=$bbbbb.' '.$areastc1;
        }
    }

        @bttcs=uniq(@bttcs);

###  foreach $bttc (@bttcs) {
###      print "QQQ: $bttc BBAA: $bttcareas{$bttc}\n";
###  }

    @tttt=split(' ',$bbbbb);
    @ttt=uniq(@tttt);
    $tcareas='';
    foreach $tt (@ttt) {
        chomp($tt);
        @t1=split(' ',$tt);
        $t2=$t1[0];
        $tttt=$area_desc{"$t2"};
        $tcareas="$tcareas ($tttt)";
    }

    return($ntc,$tcareas);

}


sub tc_posits {

my($ttau)=@_;
my($tau,$nbt);
my($verb);
$verb=0;

##################################################
#
# look for TC positions  
#
##################################################\

if($tcopt eq 'rd') {
    $tcbtpath=WXMAP{"W2_TC_BT_DIR"};
    $tcplotdir=WXMAP{"W2_TC_PLOT_DIR"};
    $ftdir=WXMAP{"W2_TC_FT_DIR"};
} elsif($tcopt eq 'ops') { 
    $tcbtpath=WXMAP{"W2_TC_BT_OPS_DIR"};
    $tcplotdir=WXMAP{"W2_TC_PLOT_OPS_DIR"};
    $ftdir=WXMAP{"W2_TC_FT_OPS_DIR"};
}

$ftstructdir=W2_TC_STRUCT_DAT_DIR

$yyyy=substr($dtg4,0,4);
$tcbtpath0=$tcbtpath;
$tcbtpath="$tcbtpath0/${yyyy}/bt.jtwc.???.????.???.txt";
$tcbtpath2="$tcbtpath0/${yyyy}/bt.jtwc.atl.????.???.txt";
@atlpaths=glob("$tcbtpath2");

if($#atlpaths < 0) {
   $tcbtpath2="";
}

$fttrkpath="$ftdir/tc.$model.$dtg4.tracks.txt";

if($model eq 'gsm') {
    $fttrkpath="$ftstructdir/$dtg4/trk/ngtrk.track.$model.$dtg4.txt";
    #print "GGGG $fttrkpath\n";
}


$ndtg4=dtg4inc($dtg4,$ttau*1);
$ndtg2=substr($ndtg4,2,8);

$cmd="grep $ndtg4 $tcbtpath | grep -v lonbnd | wc -l";
###print "QQQQQQQ $cmd\n";

$nbt=`grep $ndtg4 $tcbtpath $tcbtpath2 | grep -v lonbnd | wc -l`;

$btdata=`grep $ndtg4 $tcbtpath $tcbtpath2 | grep -v lonbnd`;

if($nbt > 0 && $verb) {
print "BBB $nbt\n";
print "BBB $btdata\n";
}
@bt=split(' ',$btdata);

#
# 20010226 - changed bt format to add time count after TS
# changed parse to use 11 fields between records vice 10 as hard coded
#

    $nfield=11;
    $btposits='0 :';
    $nbtok=0;
    $btpositsnt="$nbt :";
    $btpositsdata='';
if($nbt > 0) {
    for($n=0;$n<$nbt;$n++) {
        $nstmid=1+$n*$nfield;
        $nlat=4+$n*$nfield;
        $nlon=5+$n*$nfield;
        $nmw=2+$n*$nfield;
        $stmid=$bt[$nstmid];
        $stmnum=substr($stmid,0,2)*1;
        if($stmnum >= 80 && $stmnum <= 89) {
###	  print "SSSS skipping stm $stmid\n";
} else {
    $nbtok++;
    $btpositsdata="$btpositsdata ( $bt[$nlat] $bt[$nlon] : $bt[$nmw] )";
}
    }

}

    if($nbtok > 0 ) {
        $btposits="$nbtok : $btpositsdata";
    }


$nft=0;
if (-e $fttrkpath) { 
    open(TT,$fttrkpath) || die "unable to open $fttrkpath";
    @fttrk=<TT>;
    close(TT);
    foreach $t (@fttrk) {
        chomp $t;
        @tt=split(' ',$t);
#    print "TTTT $t\n";
#    for ($ii=0;$ii<=$#tt;$ii++) {
#	print "TTTTT $ii $tt[$ii]\n";
#    }

        $tau=$tt[0];
        $posittype=$tt[6];

        if(defined($tt[2])) {
            $lat=$tt[2]*1;
            } else {
                $lat=9999.9;
            }
        $lon=$tt[3]*1;

        if( ($tau eq '000' ||
             $tau eq '012' || $tau eq '024' ||
             $tau eq '036' || $tau eq '048' || 
             $tau eq '060' || $tau eq '072' ||
             $tau eq '084' || $tau eq '096' ||
             $tau eq '108' || $tau eq '120' )
##### output ALL taus vice just target $ttau
##### original code:
#####       && ($tau eq $ttau) && ($lat < 90.0)) {
&& ($tau <= $ttau) && ($lat < 90.0)) {
    $ftlat[$nft]=$lat;
    $ftlon[$nft]=$lon;
    $fttype[$nft]=$posittype;
    $nft++;
}
    }

    $ftposits="$nft :";

#######  undef(@ftpositscards);
#######  push (@ftpositscards, $ftposits);
#
# 20010507 - reverse order so latest tau plotted first
#

    for($n=0;$n<$nft;$n++) {
        $nn=$nft-$n-1;
###      $ftpositsentry="( $ftlat[$nn] $ftlon[$nn] $fttype[$nn] )";
###      push (@ftpositscards, $ftpositsentry);
#
#  limit the size of the output card...
#
if($n <  100) {
    $ftposits="$ftposits ( $ftlat[$nn] $ftlon[$nn] $fttype[$nn] )";
}
    }

} else {
    $ftposits='';
}

    if($verb) {
        print "BT($0): $btposits\n";
        print "FT($0): $ftposits\n";
    }

}


sub plot_areas {

#
#  use wxmap  configuration file maker to set the areas
#
my(@rc,
   $area,$verb,$testareas,@bt,@ft,$btcard,$ftcard,$nbt,$nft,
   $ilon,$ilat,$latft,$lonft,$latbt,$lonbt,
    @aa,@aaa,$atest);

    $verb=0;
    $testareas=0;

    $btcard=$btposits;
    $ftcard=$ftposits;

    if($testareas) {
        $ftcard="4 : ( -15.5 90.9 ) ( -20 160 ) ( 20 360 ) ( -10 280 )";
        $btcard="2 : ( -16.8 89.1 : 050 ) ( 20 290 : 100 )";
    }

    if($verb) {
        print"btcard: $btcard\n";
        print"ftcard: $ftcard\n";
    }

    @bt=split(' ',$btcard);
    @ft=split(' ',$ftcard);

    if(defined($bt[0])) {
        $nbt=$bt[0];
        } else {
            $nbt=0;
        }
    if(defined($ft[1])) {
        $nft=$ft[0];
        } else {
            $nft=0;
        }

    $ntccheck=$nbt+$nft;

    if($verb) {
        print" nbt: $nbt  nft: $nft\n";
    }

    $area='';
    for($i=0;$i<$nft;$i++) {
        $ilat=3 + $i*5;
        $ilon=$ilat+1;
        $latft=$ft[$ilat];
        $lonft=$ft[$ilon];
        $area=tc_plot_area($latft,$lonft,$area);
        if($verb) {
        print" i latft lonft: $i $ilat $ilon :: $latft $lonft\n";
        print" ft area: $area\n";
        }
    }

    for($i=0;$i<$nbt;$i++) {
        $ilat=3 + $i*6;
        $ilon=$ilat+1;
        $latbt=$bt[$ilat];
        $lonbt=$bt[$ilon];
        $area=tc_plot_area($latbt,$lonbt,$area);
        if($verb) {
        print" $i latbt lonbt: $i $ilat $ilon :: $latbt $lonbt\n";
        print" bt area: $area\n";
        }
    }



    @aa=split(' ',$area);

    @aaa=sort(@aa);
    $atest='asdfasdfasdf';

    foreach $a (@aaa) {
        if($a ne $atest) {
            push @tcareas, $a;
            $atest=$a;
        } 
    }   

}

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#  20020613 -- must change 
#      tc_plot_area
#      tc_title_area 
#
#  when changing wxmap areas with TCs
#
#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

