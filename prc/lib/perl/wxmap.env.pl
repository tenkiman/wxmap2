#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};

$WXMAP2_BDIR=$ENV{"W2"};
$WXMAP{'WXMAP_WEB_DIR'}="$WXMAP2_BDIR/web";  #

$WXMAP_BDIR="";

$WXMAP_PERL_DIR=$ENV{"W2_PERL_DIR"};
$WXMAP_PRC_WXMAP_DIR="$WXMAP2_BDIR/trunk/prc/fldanal";
$WXMAP_PRC_TC_DIR=$ENV{"WXMAP_PRC_TC_DIR"};

$WXMAP{"WXMAP_PROD_CENTER"}="NHC";
$WXMAP{"WXMAP_PROD_CENTER"}="ESRL/GSD";
$WXMAP{"WXMAP_PROD_CENTER"}="WxMAP2";


#
#  20001220 - turn off ---------- move /d1/nwp/wxmap
#  20001221 - turn off ---------- move /scratch/staff/fiorino
#  20001221 - turn off ---------- move /dat/nwp/wxmap
#

$WXMAP{'WXMAP_NWP_DATA_DIR'}="/dat/nwp/dat";
$WXMAP{'WXMAP_FTP_BDIR'}="/dat/nwp/wxmap/ftp";

$WXMAP{'WXMAP_FTP_INCOMING_FNMOC_REMOTE_DIR'}="/comms_dir/ddn/fnoc";
$WXMAP{'WXMAP_FTP_INCOMING_FNMOC_REMOTE_SPRITE_DIR'}="/pub/fiorino/tmp";
$WXMAP{'WXMAP_FTP_INCOMING_NCEP_REMOTE_DIR'}="/comms_dir/ddn/fnoc/ncep";
$WXMAP{'WXMAP_FTP_INCOMING_LLNL_NGTRP_REMOTE_DIR'}="/comms_dir/llnl/ngtrp";
$WXMAP{'WXMAP_FTP_INCOMING_LLNL_NGP_REMOTE_DIR'}="/comms_dir/llnl/ngp";
$WXMAP{'WXMAP_FTP_INCOMING_JTWC_REMOTE_DIR'}="/opt/DEVELOPMENT/atcf/storms";
$WXMAP{'WXMAP_FTP_INCOMING_JTWC_REMOTE_DIR'}="/opt/DEVELOPMENT/atcf/fnmocin";
$WXMAP{'WXMAP_FTP_INCOMING_JTWC_REMOTE_ARCHIVE_DIR'}="/opt/DEVELOPMENT/atcf/archives";

$WXMAP{'WXMAP_FTP_INCOMING_BDIR'}="$WXMAP{'WXMAP_FTP_BDIR'}/incoming";
$WXMAP{'WXMAP_LDM_INCOMING_BDIR'}="/wxmap_old/dat/ldmincoming";
$WXMAP{'WXMAP_LDM_INCOMING_BDIR'}="/dat/ldmincoming";
$WXMAP{'WXMAP_DAT_BDIR'}="$WXMAP2_BDIR/dat/nwp";
$WXMAP{'WXMAP_METGRAM_PRC_DIR'}="$WXMAP_BDIR/prc/metgram";
$WXMAP{'WXMAP_METGRAM_PLT_DIR'}="$WXMAP_BDIR/plt/metgram";

$WXMAP{'WXMAP_PERL_DIR'}= "$WXMAP_PERL_DIR";

$WXMAP{'WXMAP_FTPDIR_FNMOC'}="/pub/fiorino/fnmoc/dat";
$WXMAP{'WXMAP_FTPDIR_NCEP'}="/pub/fiorino/ncep/dat";

$WXMAP{'WXMAP_GEODIR'}="$WXMAP2_BDIR/dat/geog";
$WXMAP{'WXMAP_CLIMOSST'}="$WXMAP2_BDIR/dat/climo/sst";

$WXMAP{'WXMAP_PRC_WXMAP_DIR'}="$WXMAP_PRC_WXMAP_DIR";
$WXMAP{'WXMAP_PRC_HTML_DIR'}="$WXMAP_BDIR/prc/html";
$WXMAP{'WXMAP_PRC_DAT_DIR'}="$WXMAP_BDIR/prc/dat";
$WXMAP{'WXMAP_JUNK_FILE'}="/tmp/wxmap.zy0x1w2.tmp";

$WXMAP{'WXMAP_BASEMAP_GDIR'}="$WXMAP2_BDIR/plt/basemap";

##################################################
#
#	HTML
#
##################################################


$WXMAP{'WXMAP_HTML_BASE'}= '../../';
$WXMAP{'WXMAP_HTML_BASE_TOP'}= '';
$WXMAP{'WXMAP_HTML_BASE_DOC'}= '../../doc/';
$WXMAP{'WXMAP_HTML_BASE_CLASSES'}= '../../classes/';
$WXMAP{'WXMAP_HTML_BASE_GRF'}= '../../grf/';
$WXMAP{'WXMAP_HTML_BASE_ICON'}= '../../icon/';
$WXMAP{'WXMAP_HTML_BASE_DOC_TOP'}= 'doc/';
$WXMAP{'WXMAP_HTML_BASE_CLASSES_TOP'}= 'classes/';
$WXMAP{'WXMAP_HTML_BASE_GRF_TOP'}= 'grf/';
$WXMAP{'WXMAP_HTML_BASE_ICON_TOP'}= 'icon/';

$WXMAP{'WXMAP_ICON_DIR'}="$WXMAP{'WXMAP_WEB_DIR'}/icon";

$WXMAP{'WXMAP_PLOT_XSIZE'}= '900';
$WXMAP{'WXMAP_PLOT_YSIZE'}= '675';

###################################################
#
#	AREA PROPERTIES
#	JTWC
#
###################################################


$WXMAP{'WXMAP_AREAS'}       ="asia:wconus:conus:nhem:tropwpac:tropnio:tropsio:tropoz:tropenso:tropswpac:tropepac:troplant";
$WXMAP{'WXMAP_AREAS_TYPES'} ="midlat:midlat:midlat:special:tropic:tropic:tropic:tropic:tropic:tropic:tropic:tropic:tropic";
$WXMAP{'WXMAP_AREAS_DESC'}  ="East Asia:W CONUS:CONUS:NHEM:Tropical WPAC:Tropical NIO:Tropical SIO:Tropical Oz:Tropical ENSO:Tropical SWPAC:Tropical EPAC:Tropical LANT";

# -- reduced
# -- 20200723 -- add in asia because we have JMA GSM
#
$WXMAP{'WXMAP_AREAS'}       ="asia:conus:tropwpac:tropepac:troplant";
$WXMAP{'WXMAP_AREAS_TYPES'} ="midlat:midlat:tropic:tropic:tropic";
$WXMAP{'WXMAP_AREAS_DESC'}  ="ASIA:CONUS:Tropical WPAC:Tropical EPAC:Tropical LANT";



$WXMAP{'WXMAP_PLOT_TYPES'}="midlat:special:tropic";
$WXMAP{'WXMAP_PLOT_TYPES_PLOTS'}="500 psl 850 prp:uas shr u50 prp:uas prp 500";
$WXMAP{'WXMAP_PLOT_TYPES_TAUS'}="default:default:default:0 240 24";


##############################################################
#
# 20090323 - model props for esrl
#
##############################################################

$WXMAP{'WXMAP_MODELS'}="gfs:fim:navg:ecm:ukm";
$WXMAP{'WXMAP_MODELS_RES'}="05:05:05:025:07";     
$WXMAP{'WXMAP_MODELS_CENTER'}="ncep:esrl:fnmoc:ecmwf:ukmo";       
$WXMAP{'WXMAP_MODELS_GRF_EXT'}="05:05:05:025:07";    
$WXMAP{'WXMAP_MODELS_GRF_NAME'}="gfs:fim:nav:ecm:ukm";     
$WXMAP{'WXMAP_MODELS_HTTP_GDIR'}="plt_ncep_gfs:plt_esrl_fim:plt_fnmoc_navg:plt_ecmwf_ecm:plt_ukmo_ukm";                
$WXMAP{'WXMAP_MODELS_DESC'}="NCEP GFS:ESRL FIM:FNMOC NAVG:ECMWF HRES:UKMO UM";            

$WXMAP{'WXMAP_MODELS_BKG'}="bkgred.gif:bkgyello.gif:bkgblue.gif:bkggreen.gif:bkgyello.gif";             

$WXMAP{'WXMAP_MODELS_RUN00'}="1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN06'}="1:0:1:0:1";   
$WXMAP{'WXMAP_MODELS_RUN12'}="1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN18'}="1:0:1:0:1";   
$WXMAP{'WXMAP_MODELS_NTAU'}="168:168:168:168:168";
$WXMAP{'WXMAP_MODELS_DATA_NTAU'}="180:168:168:168:168";      
$WXMAP{'WXMAP_MODELS_TAUINC'}="12:12:12:12:12";    
$WXMAP{'WXMAP_MODELS_TAUINC_RUN'}="6:12:6:12:6";   

$WXMAP{'WXMAP_MODELS_PRACCUM'}="12:12:12:12";    

$WXMAP{'WXMAP_MODELS_ADD_MAPS'}="0:0:0:0:0";   
$WXMAP{'WXMAP_MODELS_COLOR'}="red:yellow:blue:green:yellow";      
$WXMAP{'WXMAP_MODELS_UCASE'}="GFS:FIM:NAVG:ECM:UKM";       
$WXMAP{'WXMAP_MODELS_GRID_RES'}="05:05:05:025:07";    
$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_ukmo_ukm";                                  

$WXMAP{'WXMAP_MODELS_ARCHIVE_GRFDIR'}=$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'};
$WXMAP{'WXMAP_MODELS_ARCHIVE_MOVIEDIR'}=\
"$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs/movie:\
$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim/movie";
$WXMAP{'WXMAP_MODELS_GDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_ukmo_ukm";                                

# -- 20170214 - reorder models
#
$WXMAP{'WXMAP_MODELS'}="gfs:ecm:ukm:fim:navg";
$WXMAP{'WXMAP_MODELS_RES'}="05:025:07:05:05";     
$WXMAP{'WXMAP_MODELS_CENTER'}="ncep:ecmwf:ukmo:esrl:fnmoc";       
$WXMAP{'WXMAP_MODELS_GRF_EXT'}="05:025:07:05:05";    
$WXMAP{'WXMAP_MODELS_GRF_NAME'}="gfs:ecm:ukm:fim:nav";     
$WXMAP{'WXMAP_MODELS_HTTP_GDIR'}="plt_ncep_gfs:plt_ecmwf_ecm:plt_ukmo_ukm:plt_esrl_fim:plt_fnmoc_navg";                
$WXMAP{'WXMAP_MODELS_DESC'}="NCEP GFS:ECMWF HRES:UKMO UM:ESRL FIM:FNMOC NAVG";            

$WXMAP{'WXMAP_MODELS_BKG'}="bkgred.gif:bkggreen.gif:bkgyello.gif:bkgyello.gif:bkgblue.gif";             

$WXMAP{'WXMAP_MODELS_RUN00'}="1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN06'}="1:0:1:0:1";   
$WXMAP{'WXMAP_MODELS_RUN12'}="1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN18'}="1:0:1:0:1";   
$WXMAP{'WXMAP_MODELS_NTAU'}="168:168:168:168:168";
$WXMAP{'WXMAP_MODELS_DATA_NTAU'}="180:168:168:168:168";      
$WXMAP{'WXMAP_MODELS_TAUINC'}="12:12:12:12:12";    
$WXMAP{'WXMAP_MODELS_TAUINC_RUN'}="6:12:6:12:6";   

$WXMAP{'WXMAP_MODELS_PRACCUM'}="12:12:12:12";    

$WXMAP{'WXMAP_MODELS_ADD_MAPS'}="0:0:0:0:0";   
$WXMAP{'WXMAP_MODELS_COLOR'}="red:green:yellow:yellow:blue";      
$WXMAP{'WXMAP_MODELS_UCASE'}="GFS:ECM:UKM:FIM:NAVG";       
$WXMAP{'WXMAP_MODELS_GRID_RES'}="05:025:07:05:05";    
$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_ukmo_ukm:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg";                                  

$WXMAP{'WXMAP_MODELS_ARCHIVE_GRFDIR'}=$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'};
$WXMAP{'WXMAP_MODELS_ARCHIVE_MOVIEDIR'}=\
"$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs/movie:\
$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim/movie";
$WXMAP{'WXMAP_MODELS_GDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_ukmo_ukm:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg";                                


# -- 20180113 - deprecate fim add fv3e and g
#
$WXMAP{'WXMAP_MODELS'}="gfs:fv3e:fv3g:ecm:ukm:navg";
$WXMAP{'WXMAP_MODELS_RES'}="05:05:05:025:07:05";     
$WXMAP{'WXMAP_MODELS_CENTER'}="ncep:esrl:esrl:ecmwf:ukmo:fnmoc";       
$WXMAP{'WXMAP_MODELS_GRF_EXT'}="05:05:05:025:07:05";    
$WXMAP{'WXMAP_MODELS_GRF_NAME'}="gfs:fv3e:fv3g:ecm:ukm:nav";     
$WXMAP{'WXMAP_MODELS_HTTP_GDIR'}="plt_ncep_gfs:plt_esrl_fv3e:plt_esrl_fv3g:plt_ecmwf_ecm:plt_ukmo_ukm:plt_fnmoc_navg";                
$WXMAP{'WXMAP_MODELS_DESC'}="NCEP GFS:ESRL FV3 NCEP:ESRL FV3 GF:ECMWF HRES:UKMO UM:FNMOC NAVG";            

$WXMAP{'WXMAP_MODELS_BKG'}="bkgred.gif:bkgred.gif:bkggreen.gif:bkggreen.gif:bkgyello.gif:bkgblue.gif";             

$WXMAP{'WXMAP_MODELS_RUN00'}="1:1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN06'}="1:0:0:0:1:1";   
$WXMAP{'WXMAP_MODELS_RUN12'}="1:1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN18'}="1:0:0:0:1:1";   
$WXMAP{'WXMAP_MODELS_NTAU'}="168:168:168:168:168:168";
$WXMAP{'WXMAP_MODELS_DATA_NTAU'}="180:168:168:168:168:168";      
$WXMAP{'WXMAP_MODELS_TAUINC'}="12:12:12:12:12:12";    
$WXMAP{'WXMAP_MODELS_TAUINC_RUN'}="6:12:12:12:6:6";   

$WXMAP{'WXMAP_MODELS_PRACCUM'}="12:12:12:12:12";    

$WXMAP{'WXMAP_MODELS_ADD_MAPS'}="0:0:0:0:0:0";   
$WXMAP{'WXMAP_MODELS_COLOR'}="red:red:green:yellow:blue";      
$WXMAP{'WXMAP_MODELS_UCASE'}="GFS:FV3N:FV3G:ECM:UKM:NAVG";       
$WXMAP{'WXMAP_MODELS_GRID_RES'}="05:05:05:025:07:05";    
$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fv3e:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fv3g:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_ukmo_ukm:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg";                                  

$WXMAP{'WXMAP_MODELS_ARCHIVE_GRFDIR'}=$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'};
$WXMAP{'WXMAP_MODELS_ARCHIVE_MOVIEDIR'}=\
"$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs/movie:\
$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim/movie";
$WXMAP{'WXMAP_MODELS_GDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fv3e:$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fv3g:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_ukmo_ukm:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg";


# -- 20200301 ------------------------------------- final non esrl
# -- 20200723 add in GSM
#
$WXMAP{'WXMAP_MODELS'}="gfs:ecm:cmc:navg:gsm";
$WXMAP{'WXMAP_MODELS_RES'}="05:025:025:05:125";     
$WXMAP{'WXMAP_MODELS_CENTER'}="ncep:ecmwf:cmc:fnmoc:jma";       
$WXMAP{'WXMAP_MODELS_GRF_EXT'}="05:025:025:05:125";    
$WXMAP{'WXMAP_MODELS_GRF_NAME'}="gfs:ecm:cmc:nav:gsm";     
$WXMAP{'WXMAP_MODELS_HTTP_GDIR'}="plt_ncep_gfs:plt_ecmwf_ecm:plt_cmc_cmc:plt_fnmoc_navg:plt_jma_gsm";                
$WXMAP{'WXMAP_MODELS_DESC'}="NCEP GFS:ECMWF HRES:CMC CGD:FNMOC NAVG:JMA GSM";            

$WXMAP{'WXMAP_MODELS_BKG'}="bkgred.gif:bkgyello.gif:bkgyello.gif:bkgblue.gif:bkgblue.gif";             

$WXMAP{'WXMAP_MODELS_RUN00'}="1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN06'}="1:0:0:1:1";   
$WXMAP{'WXMAP_MODELS_RUN12'}="1:1:1:1:1";   
$WXMAP{'WXMAP_MODELS_RUN18'}="1:0:0:1:1";   
$WXMAP{'WXMAP_MODELS_NTAU'}="168:168:168:168:132";
$WXMAP{'WXMAP_MODELS_DATA_NTAU'}="168:168:168:168:132";      
$WXMAP{'WXMAP_MODELS_TAUINC'}="12:12:12:12:12";    
$WXMAP{'WXMAP_MODELS_TAUINC_RUN'}="6:12:12:6:6";   

$WXMAP{'WXMAP_MODELS_PRACCUM'}="12:12:12:12:12";    

$WXMAP{'WXMAP_MODELS_ADD_MAPS'}="0:0:0:0:0";   
$WXMAP{'WXMAP_MODELS_COLOR'}="red:yellow:yellow:blue:blue";      
$WXMAP{'WXMAP_MODELS_UCASE'}="GFS:ECM:CMC:NAVG:GSM";       
$WXMAP{'WXMAP_MODELS_GRID_RES'}="05:025:025:05:125";    
$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_cmc_cmc:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg:$WXMAP{'WXMAP_WEB_DIR'}/plt_jma_gsm";

$WXMAP{'WXMAP_MODELS_ARCHIVE_GRFDIR'}=$WXMAP{'WXMAP_MODELS_CURRENT_GRFDIR'};
$WXMAP{'WXMAP_MODELS_ARCHIVE_MOVIEDIR'}=\
"$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs/movie:\
$WXMAP{'WXMAP_WEB_DIR'}/plt_esrl_fim/movie";
$WXMAP{'WXMAP_MODELS_GDIR'}="$WXMAP{'WXMAP_WEB_DIR'}/plt_ncep_gfs:$WXMAP{'WXMAP_WEB_DIR'}/plt_ecmwf_ecm:$WXMAP{'WXMAP_WEB_DIR'}/plt_cmc_cmc:$WXMAP{'WXMAP_WEB_DIR'}/plt_fnmoc_navg:$WXMAP{'WXMAP_WEB_DIR'}/plt_jma_gsm";

###################################################
#
#	WXMAP Subroutines
#
###################################################

sub wxmap_env {

my(@a,@am,@m,@p,@t,@apt,@apts,@aptp,
      @d,@tt,@hh,@dd,@mm,@bb,
      @r00,@r06,@r12,@r18,@nn,@ndt,@ntt,@pra,@hhd,@aam,@cc,@uu,@gg,@gt,
      @mc,@ms,@md,@mdc,@mdi,@mda,@mdl,@mga,@mgc,@mgm,$var);
#-------
# load the libraries
#-------

@a=split(/\:/,$WXMAP{"WXMAP_AREAS"});
@am=split(/\:/,$WXMAP{"WXMAP_AREAS_MODELS"});
@p=split(/\:/,$WXMAP{"WXMAP_AREAS_PRC"});
@m=split(/\:/,$WXMAP{"WXMAP_AREAS_MACH"});
@t=split(/\:/,$WXMAP{"WXMAP_AREAS_TYPES"});
@d=split(/\:/,$WXMAP{"WXMAP_AREAS_DESC"});


@apts=split(/\:/,$WXMAP{"WXMAP_PLOT_TYPES"});
@aptp=split(/\:/,$WXMAP{"WXMAP_PLOT_TYPES_PLOTS"});
@aptt=split(/\:/,$WXMAP{"WXMAP_PLOT_TYPES_TAUS"});

$ntype=$#apts+1;
for($i=0;$i<$ntype;$i++) {
  $plot_type[$i]=$apts[$i];
  $plot_type_plots{$plot_type[$i]}=$aptp[$i];
  $plot_type_taus{$plot_type[$i]}=$aptt[$i];
}

$narea=$#a+1;
@areas=@a;
@grfprcs=@p;
@machs=@m;
@areatypes=@t;

$nmid=0;
$ntrop=0;
$nspec=0;
$nlrf=0;

for($i=0;$i<$narea;$i++) {

  $area_desc{$areas[$i]}=$d[$i];
  $area_type{$areas[$i]}=$t[$i];
  $area_model{$areas[$i]}=$am[$i];

  if($t[$i] eq "midlat") {
    $areas_midlat[$nmid]=$areas[$i];
    $nmid++;
  } elsif($t[$i] eq "tropic") {
    $areas_tropic[$ntrop]=$areas[$i];
    $ntrop++;
  } elsif($t[$i] eq "special") {
    $areas_special[$nspec]=$areas[$i];
    $nspec++;
  } elsif($t[$i] eq "longrange") {
    $areas_lrf[$nlrf]=$areas[$i];
    $nlrf++;
  }
}

@models=split(/\:/,$WXMAP{"WXMAP_MODELS"});
@ggr=split(/\:/,$WXMAP{'WXMAP_MODELS_GRF_EXT'});
@ggn=split(/\:/,$WXMAP{'WXMAP_MODELS_GRF_NAME'});
@rr=split(/\:/,$WXMAP{"WXMAP_MODELS_RES"});
@hh=split(/\:/,$WXMAP{"WXMAP_MODELS_HTTP_GDIR"});
@dd=split(/\:/,$WXMAP{"WXMAP_MODELS_DESC"});
@bb=split(/\:/,$WXMAP{"WXMAP_MODELS_BKG"});
@r00=split(/\:/,$WXMAP{"WXMAP_MODELS_RUN00"});
@r06=split(/\:/,$WXMAP{"WXMAP_MODELS_RUN06"});
@r12=split(/\:/,$WXMAP{"WXMAP_MODELS_RUN12"});
@r18=split(/\:/,$WXMAP{"WXMAP_MODELS_RUN18"});
@nn=split(/\:/,$WXMAP{"WXMAP_MODELS_NTAU"});
@ndt=split(/\:/,$WXMAP{"WXMAP_MODELS_DATA_NTAU"});
@ntt=split(/\:/,$WXMAP{"WXMAP_MODELS_TAUINC"});
@nttr=split(/\:/,$WXMAP{"WXMAP_MODELS_TAUINC_RUN"});
@pra=split(/\:/,$WXMAP{"WXMAP_MODELS_PRACCUM"});
@hhd=split(/\:/,$WXMAP{"WXMAP_MODELS_HTML_DIR"});
@aam=split(/\:/,$WXMAP{"WXMAP_MODELS_ADD_MAPS"});
@cc=split(/\:/,$WXMAP{"WXMAP_MODELS_COLOR"});
@uu=split(/\:/,$WXMAP{"WXMAP_MODELS_UCASE"});
@gg=split(/\:/,$WXMAP{"WXMAP_MODELS_GDIR"});
@mgr=split(/\:/,$WXMAP{'WXMAP_MODELS_GRID_RES'});

@gt=split(/\:/,$WXMAP{"WXMAP_MODELS_TAR_GDIR"});
@mc=split(/\:/,$WXMAP{"WXMAP_MODELS_CENTER"});
@ms=split(/\:/,$WXMAP{"WXMAP_MODELS_FTPSERVER"});
@md=split(/\:/,$WXMAP{"WXMAP_MODELS_FTPDIR"});
@mdc=split(/\:/,$WXMAP{"WXMAP_MODELS_CURRENT_DATDIR"});
@mdi=split(/\:/,$WXMAP{"WXMAP_MODELS_INCOMING_FTPDIR"});
@mdldm=split(/\:/,$WXMAP{"WXMAP_MODELS_INCOMING_LDMDIR"});
@mda=split(/\:/,$WXMAP{"WXMAP_MODELS_ARCHIVE_DATDIR"});
@mdl=split(/\:/,$WXMAP{"WXMAP_MODELS_LATEST_DATDIR"});
@mga=split(/\:/,$WXMAP{"WXMAP_MODELS_ARCHIVE_GRFDIR"});
@mgc=split(/\:/,$WXMAP{"WXMAP_MODELS_CURRENT_GRFDIR"});
@mgm=split(/\:/,$WXMAP{"WXMAP_MODELS_ARCHIVE_MOVIEDIR"});


$nmodel=$#models+1;

for($i=0;$i<$nmodel;$i++) {

  $model_http_gdir{$models[$i]}=$hh[$i];
  $model_desc{$models[$i]}=$dd[$i];
  $model_bkg{$models[$i]}=$bb[$i];

  $model_run00{$models[$i]}=$r00[$i];
  $model_run06{$models[$i]}=$r06[$i];
  $model_run12{$models[$i]}=$r12[$i];
  $model_run18{$models[$i]}=$r18[$i];

  $model_run{$models[$i],'00'}=$r00[$i];
  $model_run{$models[$i],'06'}=$r06[$i];
  $model_run{$models[$i],'12'}=$r12[$i];
  $model_run{$models[$i],'18'}=$r18[$i];

  $model_res{$models[$i]}=$rr[$i];
  $model_grf_ext{$models[$i]}=$ggr[$i];
  $model_grf_name{$models[$i]}=$ggn[$i];
  $model_ntau{$models[$i]}=$nn[$i];
  $model_data_ntau{$models[$i]}=$ndt[$i];
  $model_tauinc{$models[$i]}=$ntt[$i];
  $model_tauinc_run{$models[$i]}=$nttr[$i];
  $model_praccum{$models[$i]}=$pra[$i];
  $model_html_dir{$models[$i]}="$WXMAP{'WXMAP_WEB_DIR'}/$hhd[$i]";
  $model_add_maps{$models[$i]}=$aam[$i];
  $model_color{$models[$i]}=$cc[$i];
  $model_ucase{$models[$i]}=$uu[$i];
  $model_gdir{$models[$i]}=$gg[$i];
  $model_gridres{$models[$i]}=$mgr[$i];
  $model_tar_gdir{$models[$i]}=$gt[$i];
  $model_center{$models[$i]}=$mc[$i];
  $model_ftpserver{$models[$i]}=$ms[$i];
  $model_ftpdir{$models[$i]}=$md[$i];
  $model_current_datdir{$models[$i]}=$mdc[$i];
  $model_incoming_ftpdir{$models[$i]}=$mdi[$i];
  $model_incoming_ldmdir{$models[$i]}=$mdldm[$i];
  $model_archive_datdir{$models[$i]}=$mda[$i];
  $model_latest_datdir{$models[$i]}=$mdl[$i];
  $model_archive_grfdir{$models[$i]}=$mga[$i];
  $model_current_grfdir{$models[$i]}=$mgc[$i];
  $model_archive_moviedir{$models[$i]}=$mgm[$i];

}


$plot_control{'wconus','tmx','units'}="F";
$plot_control{'wconus','tmn','units'}="F";

$plot_control{'conus','tmx','units'}="F";
$plot_control{'conus','tmn','units'}="F";

$plot_control{'europe','tmx','units'}="C";
$plot_control{'europe','tmn','units'}="C";

$plot_control{'nhem','tmx','units'}="C";
$plot_control{'nhem','tmn','units'}="C";

$plot_control{'ausnz','tmx','units'}="C";
$plot_control{'ausnz','tmn','units'}="C";

$plot_control{'bigaus','tmx','units'}="C";
$plot_control{'bigaus','tmn','units'}="C";

$plot_control{'aoe1','tmx','units'}="F";
$plot_control{'aoe1','tmn','units'}="F";

$plot_control{'wconus','tas','units'}="F";
$plot_control{'conus','tas','units'}="F";

$plot_control{'europe','tas','units'}="C";
$plot_control{'nhem','tas','units'}="C";
$plot_control{'asia','tas','units'}="F";

$plot_control{'tropepac','tas','units'}="C";
$plot_control{'tropwpac','tas','units'}="C";
$plot_control{'tropswpac','tas','units'}="C";
$plot_control{'uk','tas','units'}="C";
$plot_control{'africa','tas','units'}="C";


##################################################
#
#   specific control over plots by model/area
#
##################################################
#
#   midlats
#
##################################################

$PlotsMidLatFull="500 prp w20 850 uas psl";
$PlotsMidLatFullTas="500 prp w20 850 uas psl tas";
$PlotsMidLatFullTmaxTmin="500 prp w20 850 uas psl tas tmx tmn";

# -- reduce
#
$PlotsMidLatFull="500 prp w20 850";
$PlotsMidLatFullTas="500 prp w20 850 tas";
$PlotsMidLatFullTmaxTmin="500 prp w20 850 tas tmx tmn";

$PlotsMidLat="500 prp w20";
$PlotsMidLatTas="500 prp w20 tas";
$PlotsMidLatTmaxTmin="500 prp w20 tas tmx tmn";
$PlotsMidLatReduced="500 psl w20";

#$plot_control{'gfs','asia','plots'} = $PlotsMidLatTmaxTmin;
$plot_control{'gfs','asia','plots'} = $PlotsMidLat;
$plot_control{'gfs','asia','taus'} = "default";
$plot_control{'fim','asia','plots'} = $PlotsMidLat;
$plot_control{'fim','asia','taus'} = "default";

$plot_control{'fv3e','asia','plots'} = $PlotsMidLat;
$plot_control{'fv3e','asia','taus'} = "default";
$plot_control{'fv3g','asia','plots'} = $PlotsMidLat;
$plot_control{'fv3g','asia','taus'} = "default";

$plot_control{'navg','asia','plots'} = $PlotsMidLat;
$plot_control{'navg','asia','taus'} = "default";
$plot_control{'ecm','asia','plots'} = $PlotsMidLat;
$plot_control{'ecm','asia','taus'} = "default";
$plot_control{'gsm','asia','plots'} = $PlotsMidLat;
$plot_control{'gsm','asia','taus'} = "default";
$plot_control{'ukm','asia','plots'} = $PlotsMidLat;
$plot_control{'ukm','asia','taus'} = "default";

$plot_control{'cmc','asia','plots'} = $PlotsMidLat;
$plot_control{'cmc','asia','taus'} = "default";

$plot_control{'gfs','wconus','plots'} = $PlotsMidLat;
$plot_control{'gfs','wconus','taus'} = "default";
$plot_control{'fim','wconus','plots'} = $PlotsMidLat;
$plot_control{'fim','wconus','taus'} = "default";

$plot_control{'fv3e','wconus','plots'} = $PlotsMidLat;
$plot_control{'fv3e','wconus','taus'} = "default";
$plot_control{'fv3g','wconus','plots'} = $PlotsMidLat;
$plot_control{'fv3g','wconus','taus'} = "default";

$plot_control{'navg','wconus','plots'} = $PlotsMidLat;
$plot_control{'navg','wconus','taus'} = "default";
$plot_control{'ecm','wconus','plots'} = $PlotsMidLat;
$plot_control{'ecm','wconus','taus'} = "default";
$plot_control{'gsm','wconus','plots'} = $PlotsMidLat;
$plot_control{'gsm','wconus','taus'} = "default";
$plot_control{'ukm','wconus','plots'} = $PlotsMidLat;
$plot_control{'ukm','wconus','taus'} = "default";

$plot_control{'cmc','wconus','plots'} = $PlotsMidLat;
$plot_control{'cmc','wconus','taus'} = "default";

$plot_control{'gfs','conus','plots'} = $PlotsMidLatFull;
$plot_control{'gfs','conus','taus'} = "default";
$plot_control{'fim','conus','plots'} = $PlotsMidLatFull;
$plot_control{'fim','conus','taus'} = "default";

$plot_control{'fv3e','conus','plots'} = $PlotsMidLatFull;
$plot_control{'fv3e','conus','taus'} = "default";
$plot_control{'fv3g','conus','plots'} = $PlotsMidLatFull;
$plot_control{'fv3g','conus','taus'} = "default";

$plot_control{'fimx','conus','plots'} = $PlotsMidLatFull;
$plot_control{'fimx','conus','taus'} = "default";
$plot_control{'ecmn','conus','plots'} = $PlotsMidLatFull;
$plot_control{'ecmn','conus','taus'} = "default";
$plot_control{'ecmg','conus','plots'} = $PlotsMidLatReduced;
$plot_control{'ecmg','conus','taus'} = "default";
$plot_control{'ngp','conus','plots'} = $PlotsMidLatFull;
$plot_control{'ngp','conus','taus'} = "default";
$plot_control{'ngpc','conus','plots'} = $PlotsMidLatFull;
$plot_control{'ngpc','conus','taus'} = "default";
$plot_control{'navg','conus','plots'} = $PlotsMidLatFull;
$plot_control{'navg','conus','taus'} = "default";
$plot_control{'ecm','conus','plots'} = $PlotsMidLatFull;
$plot_control{'ecm','conus','taus'} = "default";
$plot_control{'gsm','conus','plots'} = $PlotsMidLatFull;
$plot_control{'gsm','conus','taus'} = "default";
$plot_control{'ecmt','conus','plots'} = $PlotsMidLatFull;
$plot_control{'ecmt','conus','taus'} = "default";
$plot_control{'ukm','conus','plots'} = $PlotsMidLatFull;
$plot_control{'ukm','conus','taus'} = "default";

$plot_control{'cmc','conus','plots'} = $PlotsMidLatFull;
$plot_control{'cmc','conus','taus'} = "default";

$plot_control{'gfs','europe','plots'} = $PlotsMidLat;
$plot_control{'gfs','europe','taus'} = "default";
$plot_control{'fim','europe','plots'} = $PlotsMidLat;
$plot_control{'fim','europe','taus'} = "default";

$plot_control{'fv3e','europe','plots'} = $PlotsMidLat;
$plot_control{'fv3e','europe','taus'} = "default";
$plot_control{'fv3g','europe','plots'} = $PlotsMidLat;
$plot_control{'fv3g','europe','taus'} = "default";

$plot_control{'fimx','europe','plots'} = $PlotsMidLat;
$plot_control{'fimx','europe','taus'} = "default";
$plot_control{'ecmn','europe','plots'} = $PlotsMidLat;
$plot_control{'ecmn','europe','taus'} = "default";
$plot_control{'ecmg','europe','plots'} = $PlotsMidLatReduced;
$plot_control{'ecmg','europe','taus'} = "default";
$plot_control{'ngp','europe','plots'} = $PlotsMidLat;
$plot_control{'ngp','europe','taus'} = "default";
$plot_control{'ngpc','europe','plots'} = $PlotsMidLat;
$plot_control{'ngpc','europe','taus'} = "default";
$plot_control{'navg','europe','plots'} = $PlotsMidLat;
$plot_control{'navg','europe','taus'} = "default";
$plot_control{'ecm','europe','plots'} = $PlotsMidLat;
$plot_control{'ecm','europe','taus'} = "default";
$plot_control{'ecmt','europe','plots'} = $PlotsMidLat;
$plot_control{'ecmt','europe','taus'} = "default";
$plot_control{'ukm','europe','plots'} = $PlotsMidLat;
$plot_control{'ukm','europe','taus'} = "default";

$plot_control{'cmc','europe','plots'} = $PlotsMidLat;
$plot_control{'cmc','europe','taus'} = "default";

$plot_control{'gfs','nhem','plots'} = $PlotsMidLat;
$plot_control{'gfs','nhem','taus'} = "default";
$plot_control{'fim','nhem','plots'} = $PlotsMidLat;
$plot_control{'fim','nhem','taus'} = "default";

$plot_control{'fv3e','nhem','plots'} = $PlotsMidLat;
$plot_control{'fv3e','nhem','taus'} = "default";
$plot_control{'fv3g','nhem','plots'} = $PlotsMidLat;
$plot_control{'fv3g','nhem','taus'} = "default";

$plot_control{'fimx','nhem','plots'} = $PlotsMidLat;
$plot_control{'fimx','nhem','taus'} = "default";
$plot_control{'ecmn','nhem','plots'} = $PlotsMidLat;
$plot_control{'ecmn','nhem','taus'} = "default";
$plot_control{'ecmg','nhem','plots'} = $PlotsMidLatReduced;
$plot_control{'ecmg','nhem','taus'} = "default";
$plot_control{'ngp','nhem','plots'} = $PlotsMidLat;
$plot_control{'ngp','nhem','taus'} = "default";
$plot_control{'ngpc','nhem','plots'} = $PlotsMidLat;
$plot_control{'ngpc','nhem','taus'} = "default";
$plot_control{'navg','nhem','plots'} = $PlotsMidLat;
$plot_control{'navg','nhem','taus'} = "default";
$plot_control{'ecm','nhem','plots'} = $PlotsMidLat;
$plot_control{'ecm','nhem','taus'} = "default";
$plot_control{'ecmt','nhem','plots'} = $PlotsMidLat;
$plot_control{'ecmt','nhem','taus'} = "default";
$plot_control{'ukm','nhem','plots'} = $PlotsMidLat;
$plot_control{'ukm','nhem','taus'} = "default";

$plot_control{'cmc','nhem','plots'} = $PlotsMidLat;
$plot_control{'cmc','nhem','taus'} = "default";

##################################################
#
#   special
#
##################################################

$aoeplot="w20 lmq mhq 500 850 uas prp psl";
$aoeplot_ukm="w20 lmq 500 850 uas psl";

$plot_control{'gfs','aoe1','plots'} = "$aoeplot tmx tmn";
$plot_control{'gfs','aoe1','plots'} = "$aoeplot";

$plot_control{'gfs','bigaus','plots'} = "shr w20 lmq mhq 500 850 psl prp";
$plot_control{'gfs','bigaus','taus'} = "default";

##################################################
#
#   tropics
#
##################################################

# -- reorder so most sig plots are to the left
#

$PlotsNhemTropfull="n850 uas shr prp w20 mhq wdl hhq lmq 500 u50 u70 w70 850 psl";
$PlotsShemTropfull="n850 uas shr prp w20 mhq wdl 850";
$PlotsTropMonitor="uas prp shr n850 w20 mhq psl";

# -- set/reduce here and in w2env.py
#
$PlotsNhemTropfull="uas shr n850 prp 500 w20 wdl lmq mhq hhq";
$PlotsShemTropfull="uas shr n850 prp 500 w20 wdl lmq mhq hhq";
$PlotsTropMonitor="uas shr prp w20";

$PlotsTropAllNhem=$PlotsNhemTropfull;
$PlotsTropAllShem=$PlotsShemTropfull;

# -- reduce because /w3/rapb too full
#
$PlotsTropAllLant=$PlotsNhemTropfull;
$PlotsTropAllEpac=$PlotsNhemTropfull;
$PlotsTropAllWpac=$PlotsNhemTropfull;

$PlotsTropReduced="n850 shr w20 psl";

#nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
#
# NHEM
#
#nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

$plot_control{'gfs','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'gfs','troplant','taus'} = "default";
$plot_control{'fim','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'fim','troplant','taus'} = "default";

$plot_control{'fv3e','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'fv3e','troplant','taus'} = "default";
$plot_control{'fv3g','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'fv3g','troplant','taus'} = "default";

$plot_control{'fimx','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'fimx','troplant','taus'} = "default";
$plot_control{'ecmn','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'ecmn','troplant','taus'} = "default";
$plot_control{'ecmg','troplant','plots'} = $PlotsTropReduced;
$plot_control{'ecmg','troplant','taus'} = "default";
$plot_control{'ngp','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'ngp','troplant','taus'} = "default";
$plot_control{'ngpc','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'ngpc','troplant','taus'} = "default";
$plot_control{'navg','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'navg','troplant','taus'} = "default";
$plot_control{'ecm','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'ecm','troplant','taus'} = "default";
$plot_control{'gsm','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'gsm','troplant','taus'} = "default";
$plot_control{'ecmt','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'ecmt','troplant','taus'} = "default";
$plot_control{'ukm','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'ukm','troplant','taus'} = "default";

$plot_control{'cmc','troplant','plots'} = $PlotsTropAllLant;
$plot_control{'cmc','troplant','taus'} = "default";

$plot_control{'gfs','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'gfs','tropenso','taus'} = "default";
$plot_control{'fim','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'fim','tropenso','taus'} = "default";

$plot_control{'fv3e','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'fv3e','tropenso','taus'} = "default";
$plot_control{'fv3g','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'fv3g','tropenso','taus'} = "default";

$plot_control{'ngp','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'ngp','tropenso','taus'} = "default";
$plot_control{'navg','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'navg','tropenso','taus'} = "default";
$plot_control{'ecm','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'ecm','tropenso','taus'} = "default";
$plot_control{'ukm','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'ukm','tropenso','taus'} = "default";

$plot_control{'cmc','tropenso','plots'} = $PlotsTropAllLant;
$plot_control{'cmc','tropenso','taus'} = "default";

$plot_control{'gfs','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'gfs','tropepac','taus'} = "default";
$plot_control{'fim','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'fim','tropepac','taus'} = "default";

$plot_control{'fv3e','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'fv3e','tropepac','taus'} = "default";
$plot_control{'fv3g','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'fv3g','tropepac','taus'} = "default";


$plot_control{'fimx','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'fimx','tropepac','taus'} = "default";
$plot_control{'ecmn','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'ecmn','tropepac','taus'} = "default";
$plot_control{'ecmg','tropepac','plots'} = $PlotsTropReduced;
$plot_control{'ecmg','tropepac','taus'} = "default";
$plot_control{'ngp','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'ngp','tropepac','taus'} = "default";
$plot_control{'ngpc','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'ngpc','tropepac','taus'} = "default";
$plot_control{'navg','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'navg','tropepac','taus'} = "default";
$plot_control{'ecm','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'ecm','tropepac','taus'} = "default";
$plot_control{'gsm','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'gsm','tropepac','taus'} = "default";
$plot_control{'ecmt','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'ecmt','tropepac','taus'} = "default";
$plot_control{'ukm','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'ukm','tropepac','taus'} = "default";

$plot_control{'cmc','tropepac','plots'} = $PlotsTropAllEpac;
$plot_control{'cmc','tropepac','taus'} = "default";

$plot_control{'gfs','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'gfs','tropwpac','taus'} = "default";
$plot_control{'fim','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'fim','tropwpac','taus'} = "default";

$plot_control{'fv3e','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'fv3e','tropwpac','taus'} = "default";
$plot_control{'fv3g','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'fv3g','tropwpac','taus'} = "default";

$plot_control{'fimx','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'fimx','tropwpac','taus'} = "default";
$plot_control{'ecmn','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'ecmn','tropwpac','taus'} = "default";
$plot_control{'ecmg','tropwpac','plots'} =  $PlotsTropReduced;
$plot_control{'ecmg','tropwpac','taus'} = "default";
$plot_control{'ngp','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'ngp','tropwpac','taus'} = "default";
$plot_control{'ngpc','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'ngpc','tropwpac','taus'} = "default";
$plot_control{'navg','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'navg','tropwpac','taus'} = "default";
$plot_control{'ecm','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'ecm','tropwpac','taus'} = "default";
$plot_control{'gsm','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'gsm','tropwpac','taus'} = "default";
$plot_control{'ecmt','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'ecmt','tropwpac','taus'} = "default";
$plot_control{'ukm','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'ukm','tropwpac','taus'} = "default";

$plot_control{'cmc','tropwpac','plots'} =  $PlotsTropAllWpac;
$plot_control{'cmc','tropwpac','taus'} = "default";

$plot_control{'gfs','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'gfs','tropnio','taus'} = "default";
$plot_control{'fim','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'fim','tropnio','taus'} = "default";

$plot_control{'fv3e','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'fv3e','tropnio','taus'} = "default";
$plot_control{'fv3g','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'fv3g','tropnio','taus'} = "default";

$plot_control{'fimx','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'fimx','tropnio','taus'} = "default";
$plot_control{'ecmn','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'ecmn','tropnio','taus'} = "default";
$plot_control{'ecmg','tropnio','plots'} = $PlotsTropReduced;
$plot_control{'ecmg','tropnio','taus'} = "default";
$plot_control{'ngp','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'ngp','tropnio','taus'} = "default";
$plot_control{'ngpc','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'ngpc','tropnio','taus'} = "default";
$plot_control{'navg','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'navg','tropnio','taus'} = "default";
$plot_control{'ecm','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'ecm','tropnio','taus'} = "default";
$plot_control{'ecmt','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'ecmt','tropnio','taus'} = "default";
$plot_control{'ukm','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'ukm','tropnio','taus'} = "default";

$plot_control{'cmc','tropnio','plots'} = $PlotsTropAllNhem;
$plot_control{'cmc','tropnio','taus'} = "default";

#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
#
# SHEM
#
#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

$plot_control{'gfs','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'gfs','tropsio','taus'} = "default";
$plot_control{'fim','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'fim','tropsio','taus'} = "default";

$plot_control{'fv3e','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'fv3e','tropsio','taus'} = "default";
$plot_control{'fv3g','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'fv3g','tropsio','taus'} = "default";

$plot_control{'fimx','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'fimx','tropsio','taus'} = "default";
$plot_control{'ngp','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'ngp','tropsio','taus'} = "default";
$plot_control{'ngpc','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'ngpc','tropsio','taus'} = "default";
$plot_control{'navg','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'navg','tropsio','taus'} = "default";
$plot_control{'ecm','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'ecm','tropsio','taus'} = "default";
$plot_control{'ecmt','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'ecmt','tropsio','taus'} = "default";
$plot_control{'ecmg','tropsio','plots'} = $PlotsTropReduced;
$plot_control{'ecmg','tropsio','taus'} = "default";
$plot_control{'ukm','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'ukm','tropsio','taus'} = "default";

$plot_control{'cmc','tropsio','plots'} = $PlotsTropAllShem;
$plot_control{'cmc','tropsio','taus'} = "default";


$plot_control{'gfs','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'gfs','tropoz','taus'} = "default";
$plot_control{'fim','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'fim','tropoz','taus'} = "default";

$plot_control{'fv3e','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'fv3e','tropoz','taus'} = "default";
$plot_control{'fv3g','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'fv3g','tropoz','taus'} = "default";

$plot_control{'fimx','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'fimx','tropoz','taus'} = "default";
$plot_control{'ngp','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'ngp','tropoz','taus'} = "default";
$plot_control{'ngpc','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'ngpc','tropoz','taus'} = "default";
$plot_control{'navg','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'navg','tropoz','taus'} = "default";
$plot_control{'ecm','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'ecm','tropoz','taus'} = "default";
$plot_control{'ecmt','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'ecmt','tropoz','taus'} = "default";
$plot_control{'ecmg','tropoz','plots'} = $PlotsTropReduced;
$plot_control{'ecmg','tropoz','taus'} = "default";
$plot_control{'ukm','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'ukm','tropoz','taus'} = "default";

$plot_control{'cmc','tropoz','plots'} = $PlotsTropAllShem;
$plot_control{'cmc','tropoz','taus'} = "default";

$plot_control{'gfs','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'gfs','tropswpac','taus'} = "default";
$plot_control{'fim','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'fim','tropswpac','taus'} = "default";

$plot_control{'fv3e','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'fv3e','tropswpac','taus'} = "default";
$plot_control{'fv3g','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'fv3g','tropswpac','taus'} = "default";

$plot_control{'fimx','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'fimx','tropswpac','taus'} = "default";
$plot_control{'ngp','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'ngp','tropswpac','taus'} = "default";
$plot_control{'ngpc','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'ngpc','tropswpac','taus'} = "default";
$plot_control{'navg','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'navg','tropswpac','taus'} = "default";
$plot_control{'ecm','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'ecm','tropswpac','taus'} = "default";
$plot_control{'ecmt','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'ecmt','tropswpac','taus'} = "default";
$plot_control{'ecmg','tropswpac','plots'} = $PlotsTropReduced;
$plot_control{'ecmg','tropswpac','taus'} = "default";
$plot_control{'ukm','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'ukm','tropswpac','taus'} = "default";

$plot_control{'cmc','tropswpac','plots'} = $PlotsTropAllShem;
$plot_control{'cmc','tropswpac','taus'} = "default";

##################################################
#
#   special/misc
#
##################################################

$plot_control{'ngp','uk','plots'} = "500 psl 850 prp uas wav";
$plot_control{'ngp','uk','taus'} = "default";

$plot_control{'ngp','africa','plots'} = "500 prp wav";
$plot_control{'ngp','africa','taus'} = "default";


# max plots per area

$wxmap_maxplot_area{'gfs'}=999;
$wxmap_maxplot_area{'fim'}=999;
$wxmap_maxplot_area{'fv3e'}=999;
$wxmap_maxplot_area{'fv3g'}=999;
$wxmap_maxplot_area{'fimx'}=999;
$wxmap_maxplot_area{'ecmn'}=999;
$wxmap_maxplot_area{'ecmg'}=999;
$wxmap_maxplot_area{'ecm'}=999;
$wxmap_maxplot_area{'gsm'}=999;
$wxmap_maxplot_area{'cmc'}=999;
$wxmap_maxplot_area{'ngp'}=999;
$wxmap_maxplot_area{'ngpc'}=999;
$wxmap_maxplot_area{'navg'}=999;

##################################################
#
#   archive machine
#
##################################################

$wxmap_archive_server="ecfs";
$wxmap_archive_server="bitbank.nersc.gov";
$wxmap_archive_server="hpss.nersc.gov";
$wxmap_archive_server="wxmap";
$wxmap_archive_server="pzal.npmoc.navy.mil";
$wxmap_archive_server="pzal.ndbc.noaa.gov";

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

$wxmap_lockfile_maxage_min=180;    
$wxmap_tmpdir="/tmp/.fiorino";

$wxmap_xvfb{'gfs','d'} = "$wxmap_tmpdir/xvfb.gfs";
$wxmap_xvfb{'ngp','d'} = "$wxmap_tmpdir/xvfb.ngp";
$wxmap_xvfb{'Xvfb4','d'} = "$wxmap_tmpdir/xvfb.4";

$wxmap_xvfb{'gfs','l'} = "$wxmap_tmpdir/lock.gfs";
$wxmap_xvfb{'ngp','l'} = "$wxmap_tmpdir/lock.ngp";

$wxmap_xvfb{'gfs','n'} = "1";
$wxmap_xvfb{'ngp','n'} = "3";
$wxmap_xvfb{'Xvfb4','n'} = "4";

$wxmap_xvfb{'gfs','X'}="stargate:$wxmap_xvfb{'gfs','n'}.0";
$wxmap_xvfb{'ngp','X'}="stargate:$wxmap_xvfb{'ngp','n'}.0";
$wxmap_xvfb{'Xvfb4','X'}="stargate:$wxmap_xvfb{'Xvfb4','n'}.0";

}

##################################################
#
#   associative array between plot number and name on graphics file 
#
##################################################


%pnam=(
       '1','500',
       '2','psl',
       '3','prp',
       '4','850',
       '5','tas',
       '6','uas',
       '7','u50',
       '8','shr',
       '9','u70',
       '10','sst',
       '11','wav',
       '12','w20',
       '13','wdl',
       '14','lmq',
       '15','mhq',
       '16','hhq',
       '20','tmx',
       '21','tmn',
       '22','thk',
       '23','w70',
       '30','basemap',
       '50','clm',
       '60','stg',
       '61','st2',
       '101','n850',
);


%pnum=(
       '500','1',
       'psl','2',
       'prp','3',
       '850','4',
       'tas','5',
       'uas','6',
       'u50','7',
       'shr','8',
       'u70','9',
       'sst','10',
       'wav','11',
       'w20','12',
       'wdl','13',
       'lmq','14',
       'mhq','15',
       'hhq','16',
       'tmx','20',
       'tmn','21',
       'thk','22',
       'w70','23',
       'basemap','30',
       'clm','50',
       'stg','60',
       'st2','61',
       'n850','101',
);


%numplot_delta=(
       '500',0,
       'psl',0,
       'prp',-1,
       '850',0,
       'tas',0,
       'uas',0,
       'u50',0,
       'shr',0,
       'sst',0,
       'wav',0,
       'w20',0,
       'wdl',0,
       'lmq',0,
       'mhq',0,
       'hhq',0,
       'tmx',-1,
       'tmn',-1,
       'thk',0,
       'w70',0,
       'basemap',-999,
       'clm',0,

       'n850',0,
);


%mapbutton=(

	    '500','Z500',
	    '850','TQV8',
	    'prp','Pcp',
	    'psl','Slp',
	    'u50','V500',
	    'u70','W700',
	    'shr','Vshr',
	    'sst','SST',
	    'uas','Vsfc',
	    'wav','Wav',
	    'w20','V200',
	    'wdl','Vdl',
	    'lmq','QVlm',
	    'mhq','QVmh',
	    'hhq','QVhh',
	    'tmx','Tmax',
	    'tmn','Tmin',
	    'tas','Tsfc-D',
	    'thk','Zthk',
	    'w70','V700',
	    'clm','CLM',

	    'n850','Vrt8',

);


%maptitle=(
'500','500 hPa Heights [m] and Rel. Vort [10^-5 s^-1]',
'850','850 hPa Temperature [C], winds [kts] and Rel. Hum. [%]',
'prp',$pt,
'psl','SLP [hPa] & 500-1000 Thkns [m] & 700 hPa Vert. Vel [Pa s^-1]',
'u50','500 hPa Strmlns & Istchs [kt] ; Wind Barbs',
'u70','700 hPa Strmlns ; N-S wind componment ; Wind Barbs',
'shr','|850-200 Shear| ; 200 hPa Strmlns 850(R)/200(G) Barbs',
'sst','SST [C] ; SST Anomaly from AMIP II SST Climatology (1979-96)',
'uas','Over Ocean Sfc Winds [kt]',
'wav','Sig Wave Heights [ft] ; Over Ocean Sfc Winds [kt]',
'w20','200 hPa Streamlines and Isotachs [kt]',
'wdl','Deep Layer Mean Streamlines/Isotachs [kt]',
'lmq','Low-Mid Trop (925-500) PW [mm] & Flow',
'mhq','Mid-High Trop (600-200) PW [mm] & Flow',
'hhq','High-High Trop (400-200) PW [mm] & Flow',
'tmx','Max Sfc Air Temperature [F] ; GFS Previous 24-h',
'tmn','Min Sfc Air Temperature [F] ; GFS Previous 24-h',
'tas','Sfc Air Temperature Change [F]',
'thk','1000-500 Thickness [dm] and Sea Level Pressure [mb]',
'w70','700 hPa Strmlns and Istchs [kt] ; Wind Barbs',
'clm','0-5 day mean climo',
'n850','850 Rel Vort [10^-5] Wind Barbs ; 200 Strmlns [kt]',

);

%shortmaptitle=(
'500','500 Z / Rel Vort',
'850','850 Winds / RH / T',
'prp',$pt,
'psl','SLP / 500-100 Thk',
'u50','500 V: strm + barbs',
'u70','700 V: v comp + barbs',
'shr','850-200 Shr',
'sst','SST Anomaly',
'uas','V sfc',
'wav','Sig Wave Z',
'w20','200 V: strm + iso',
'wdl','DLM V: strm + iso',
'lmq','L-M PW / V',
'mhq','M-H PW / V',
'hhq','H-H PW / V',
'tmx','Tmax',
'tmn','Tmin',
'tas','Tsfc-Change',
'thk','1000-500 Thk',
'w70','700 V: strm + iso',
'clm','climo',
'n850','McAdie 850 Vrt+ 200 V',

);


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

#
#  webmaster in Miami
#
$wb="Send Comments to Dr. Mike Fiorino <a href=\"mailto:michael.fiorino\@noaa.gov\">michael.fiorino\@noaa.gov</a>, 
<a href=\"http://www.nhc.noaa.gov\">NHC</a><br>
<i>Last updated: $timecdtg</i>";

#
#  webmaster in boulder
#
$wb="Send Comments to Dr. Mike Fiorino <a href=\"mailto:michael.fiorino\@noaa.gov\">michael.fiorino\@noaa.gov</a>, 
<a href=\"http://fim.noaa.gov/amb/\">ESRL/GSD/AMB</a><br>
<i>Last updated: $timecdtg</i>";

$wb="Send Comments to Dr. Mike Fiorino <a href=\"mailto:wxmapster\@gmail.com\">wxmapster\@gmail.com</a>, 
WxMAP2<br>
<i>Last updated: $timecdtg</i>";

$wb="Send Comments to Dr. Mike Fiorino <a href=\"mailto:mike\@wxmap2.com\">mike\@wxmap2.com</a>, 
WxMAP2<br>
<i>Last updated: $timecdtg</i>";

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

  @amodels=@hmodels;
  return(@amodels);
  
}


sub mod_db_latest_htm {

  my($verb,$curdir,$model,$area,@dtgs,$lastdtg,$latesthtm);

  $verb=0;

  $curdir=`pwd`;
  chomp($curdir);

  undef(@latest_model_htm);
  chdir($WXMAP{'WXMAP_WEB_DIR'});
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

      $latest_model_htm{$model,$area}=$latesthtm;

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

    use File::Basename;

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

  $ng{'all'}=0;

  foreach $model (@amodels) {

      $ng{$model}=0 ;
      $dtg{$model}=$tdtg;
      $ddir="$model_gdir{$model}/$data_time";
      print "DDDDDDDDDDDDDDDD ddir: $ddir\n" if($verb);

      if($tdtghh ne "") {
	  $model_chk=$model_run{$model,$tdtghh} ;
	  next if($model_chk == 0);
      }
      
    if($atype ne "") {

      foreach $pt (plot_types($model)) {
	  $taubeg=999;
	  $tauend=-999;

	  $lsmask="${model_grf_name{$model}}${model_grf_ext{$model}}*${pt}*.png";
	  print "TTTTTTTTTTTTTTTTTTTTTTTTT lsmask: $lsmask\n" if($verb);


	  if( ! (-d $ddir) ) {
	      $ng{$model,$pt}=0;
	  } else { 
	      
##	      @files=<"%ddir/$lsmask">;
##	      foreach $tt (@files) {
##		  print "QQQ $tt\n";

	      @gglob=<$ddir/$lsmask>;

	      $tt=$#gglob;

	      if( $tt  > 0 ) {

		  if($dotau) {
##		      @gglob=`(cd $ddir ; ls $lsmask)` ) {
###		      if( @gglob=<"%ddir/$lsmask"> ) {
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
	      }
	      
	      $ng{$model,$pt}=$tt*1;
	  } 

	  print "#plots for $model $pt : $ng{$model,$pt} :: $ng{$model,$pt,'taubeg'} : $ng{$model,$pt,'tauend'}\n" if($verb);
	  $ng{$model}=$ng{$model}+$ng{$model,$pt}; 

	  foreach $gg (@gglob) {
	      ($name,$path,$suffix) = fileparse($gg);
	      $gfile_truth{$name}=1;
	  }
	      
#	  if(open(I,"(cd $ddir ; ls $lsmask) |")) {
#	      while ( <I> ) {
#		  chop ;
#		  $file = $_ ;
#		  print "ffffffffff $file\n";
#		  $gfile_truth{$file}=1;
#	      }
#	  }
#	  close(I);

      }
      
  } else {

      if( ! (-d $ddir) ) {
	  $ng{$model}=0;
      } else { 
	  $gmodel=${model_grf_name{$model}};
	  if($tt=`ls -1 $ddir | grep ".png" | grep $gmodel  | wc -l`) {
	      chop($tt);
	      print "TTTTTTTTTTTTTTTTTTTTTTTTT mod_db for gmodel: $gmodel : tt = $tt : ddir: $ddir\n";
	      $ng{$model}=$tt*1;
	  }
      } 
      
  }

      print "#plots for $model ALL : $ng{$model}\n" if($verb);
      $ng{'all'} += $ng{$model};

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

  @ppp=split(' ',$pp);

  return(@ppp);

}

sub plot_taus {

  local($model,$area,$plot)=@_;
  local($tt,@t,$taubeg,$tauend,$tauinc);

  if($plot_control{$model,$area,'taus'} ne "") {
    $tt=$plot_control{$model,$area,'taus'}  ;
  } elsif($plot_control{$model,$plot,'taus'} ne "") {
    $tt=$plot_control{$model,$plot,'taus'}  ;
  } else {
    $tt="$plot_type_taus{$atype}";
  }

  @t=split(/ /,$tt);

  if($t[0] eq "default") {
    $taubeg=0;
    $tauend=$model_ntau{$model};
    $tauinc=$model_tauinc{$model};
  } else {
    $taubeg=$t[0];
    $tauend=$t[1];
    $tauinc=$t[2];
  }
  
  $plot_taupl{'beg'}=$taubeg*1;
  $plot_tau{'end'}=$tauend*1;
  $plot_tau{'inc'}=$tauinc*1;

  if($model eq 'ecmn') {
      @plottaus=(0,12,24,36,48,60,72,84,96,108,120,132,144,156,168);
  } elsif($model eq 'ecmg') {
      @plottaus=(0,24,48,72,96,120,144,168);
  } elsif($model eq 'ngp') {
      @plottaus=(0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144);
  } else {
      @plottaus=(0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168);
  }

}

sub plot_taus2 {

  local($model)=@_;

  if($model eq 'ecmn') {
      @plottaus=(0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168);
  } elsif($model eq 'ecmg') {
      @plottaus=(0,24,48,72,96,120,144,168);
  } elsif($model eq 'ngp') {
      @plottaus=(0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144);
  } elsif($model eq 'ukm') {
      @plottaus=(0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168);
  } else {
      @plottaus=(0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168);
  }

}

sub write_totalmaps {
  local($tot)=@_;
  open (O,"> $WXMAP{'WXMAP_JUNK_FILE'}");
  print O $tot;
  close(O);
}


sub read_totalmaps {
  local($tot)=@_;
  local($card);
  open (I,"cat $WXMAP{'WXMAP_JUNK_FILE'} |");
  while(<I>) {
    $card=$_;
  }
  close(I);
  $tot=$card*1.0;
  return($tot);
}

sub release_lock {

  ($model)=@_;
  $cmd="rm $wxmap_xvfb{$model,'l'}";
  $localtime=localdtg("time");
  print "LLLL: $cmd\n";
  print "LLLL: releasing the lock at $localtime\n";
  system($cmd);
  
}

sub lock_file_age {

  ($model)=@_;
  my($lockfile);
  $lockfile=$wxmap_xvfb{$model,'l'};
  if( -f $lockfile ) {
    @f=stat($lockfile);
    $ftime=$f[10];
    $ctime=time();
    $lockage=($ctime-$ftime)/60;
    printf("LLLL: the lock for the $model model is %6.2f min old\n",$lockage);
  } else {
    $lockage=-999;
  }
  return $lockage;
}


sub set_url {

#
#  URL
#

$url{'tc','tropwpac'}="http://grads.iges.org/pix/allwpac.html";
$url{'tc','tropwpac'}="http://weather.unisys.com/hurricane/w_pacific/$WXMAP_CUR_YEAR/index.html";

$url{'tc','tropepac'}="http://grads.iges.org/pix/allepac.html";
$url{'tc','tropepac'}="http://weather.unisys.com/hurricane/e_pacific/$WXMAP_CUR_YEAR/index.html";

$url{'tc','troplant'}="http://grads.iges.org/pix/allatla.html";
$url{'tc','troplant'}="http://weather.unisys.com/hurricane/atlantic/$WXMAP_CUR_YEAR/index.html";

$url{'tc','tropswpac'}="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html";
$url{'tc','tropio'}="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html";
$url{'tc','tropnio'}="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html";
$url{'tc','tropsio'}="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html";
$url{'tc','tropsoz'}="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html";


$url{'tc','aor'}="http://grads.iges.org/pix/allatla.html";

$url{'tc','global'}="http://www.solar.ifa.hawaii.edu/Tropical/tropical.html";

#
# TC struct cgi
#
$url{'tcstruct'}="/cgi-bin/wxmap2/tcstruct.cgi";


$url{'sat','tropwpac'}='http://www.nrlmry.navy.mil/sat-bin/display10?PHOT=yes&AREA=pacific/western/tropics&PROD=ir&NAV=tropics&CGI=tropics.cgi&ARCHIVE=Latest&MOSAIC_SCALE=15&CURRENT=LATEST.jpg';
$url{'sat','tropwpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/images/xxirgms5.GIF';


$url{'sat','tropepac'}='http://www.nrlmry.navy.mil/sat-bin/display10?PHOT=yes&AREA=pacific/eastern/tropics&PROD=ir&NAV=tropics&CGI=tropics.cgi&ARCHIVE=Latest&MOSAIC_SCALE=15%&CURRENT=LATEST.jpg';
$url{'sat','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/images/xxirg9.GIF';

$url{'sat','troplant'}='http://www.nrlmry.navy.mil/sat-bin/display10?PHOT=yes&AREA=atlantic/stiched&PROD=ir&NAV=tropics&ARCHIVE=Latest&CGI=tropics.cgi&MOSAIC_SCALE=15%';
$url{'sat','troplant'}='http://www.nrlmry.navy.mil/sat-bin/display10?PHOT=yes&AREA=atlantic/stitched&PROD=ir&NAV=tropics&CGI=tropics.cgi&ARCHIVE=Latest&MOSAIC_SCALE=15&CURRENT=LATEST.jpg';
$url{'sat','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/images/xxirg8.GIF';


$url{'sat','aor'}="http://www.nrlmry.navy.mil/sat-bin/display3?phot=yes&dir=goes8_images/trop_atlantic_ir&type=jpeg";

$url{'sat','conus'}='http://www.intellicast.com/WeatherImages/Satellite/satellite.wsi;hiusa;Satellite;gif;satellite.gif';
$url{'sat','conus'}='http://www.weather.com/weather/sat/ussat_720x486.html';
$url{'sat','conus'}='http://maps.weather.com/images/sat/ussat_720x486.jpg';
$url{'sat','ausnz'}="http://208.134.241.135/images/sat/aussiesat_720x486.jpg";
$url{'sat','europe'}="http://208.134.241.135/images/sat/europesat_720x486.jpg";
$url{'sat','europe'}="http://208.134.241.135/images/sat/europesat_720x486.jpg";
$url{'sat','europe'}="http://www.meto.gov.uk/satpics/latest_vis.jpg";
$url{'sat2','europe'}="http://www.meto.gov.uk/satpics/latest_ir.jpg";

$url{'sat','nhem'}="http://www.meto.gov.uk/satpics/latest_vis.jpg";
$url{'sat2','nhem'}="http://www.meto.gov.uk/satpics/latest_ir.jpg";

$url{'sat','africa'}="http://maps.weather.com/images/sat/africasat_720x486.jpg";
$url{'sat','asia'}='http://www.npmoc.navy.mil/satimages/gmsa.jpg';

$url{'sat','sam'}="http://maps.weather.com/images/sat/sasat_720x486.jpg";
$url{'sat','ausnz'}="http://maps.weather.com/images/sat/aussiesat_720x486.jpg";
$url{'sat','swasia'}="http://maps.weather.com/images/sat/mideastsat_720x486.jpg";
$url{'sat','whitbread'}="http://maps.weather.com/images/sat/pacglobsat_720x486.jpg";


$url{'sat_v_hi','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.html';
$url{'sat_v_hi','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8wvir.GIF';
$url{'sat_v_lo','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8ir.html';
$url{'sat_v_lo','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8ir.GIF';
$url{'sat_v_sh','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8shr.html';
$url{'sat_v_sh','troplant'}='http://cimss.ssec.wisc.edu/tropic/real-time/atlantic/winds/wg8shr.GIF';

$url{'sat_v_hi','tropwpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmswv.GIF';
$url{'sat_v_lo','tropwpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsir.GIF';
$url{'sat_v_sh','tropwpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/westpac/winds/wgmsshr.GIF';

$url{'sat_v_hi','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9wvir.html';
$url{'sat_v_lo','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9ir.html';
$url{'sat_v_sh','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9shr.html';

$url{'sat_v_hi','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9wvir.GIF';
$url{'sat_v_lo','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9ir.GIF';
$url{'sat_v_sh','tropepac'}='http://cimss.ssec.wisc.edu/tropic/real-time/eastpac/winds/wg9shr.GIF';

$url{'sat_v_hi','tropnio'}='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.GIF';
$url{'sat_v_lo','tropnio'}='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5ir.GIF';
$url{'sat_v_sh','tropnio'}='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5shr.GIF';

$url{'sat_v_hi','tropsio'}='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5wv.GIF';
$url{'sat_v_lo','tropsio'}='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5ir.GIF';
$url{'sat_v_sh','tropsio'}='http://cimss.ssec.wisc.edu/tropic/real-time/indian/winds/wm5shr.GIF';

$url{'sat_v_hi','tropoz'}='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmswvs1.GIF';
$url{'sat_v_lo','tropoz'}='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsirs1.GIF';
$url{'sat_v_sh','tropoz'}='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsshSW.GIF';

$url{'sat_v_hi','tropswpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsirs3.GIF';
$url{'sat_v_lo','tropswpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmswvs3.GIF';
$url{'sat_v_sh','tropswpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/shemi/winds/wgmsshSE.GIF';

$url{'sat_v_hi','tropswpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/seastpac/winds/wg10swvir.GIF';
$url{'sat_v_lo','tropswpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/seastpac/winds/wg10sir.GIF';
$url{'sat_v_sh','tropswpac'}='http://cimss.ssec.wisc.edu/tropic/real-time/seastpac/winds/wg10sshr.GIF';


$url{'wxmap','nlmoc'}="http://www1.nlmoc.navy.mil:83/wxmap/web/wx.htm";
$url{'wxmap','pcmdi'}="http://www-pcmdi.llnl.gov/fiorino/wxmap";

$url{'whitbread','whitbread'}="http://www.whitbread.org";

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
$tcbtpath=$WXMAP{"WXMAP_TC_BT_OPS_DIR"};
$tcplotdir=$WXMAP{"WXMAP_TC_PLOT_OPS_DIR"};
$ftdir=$WXMAP{"WXMAP_TC_FT_OPS_DIR"};

$yyyy=substr($tdtg,0,4);
$yyyyp1=$yyyy+1;

$tcbtpath0=$tcbtpath;

$tcbtpath="$tcbtpath0/${yyyy}/BtOps.*.txt";
$tcbtpathyyyyp1="$tcbtpath0/${yyyyp1}/BtOps.*.txt";

$tcbtpath2="$tcbtpath0/${yyyy}/BtOps.*.txt";

 @atlpaths=glob("$tcbtpath2");

 if($#atlpaths < 0) {
   $tcbtpath2="";
 }

 $ntc=`grep $tdtg $tcbtpathyyyyp1 $tcbtpath $tcbtpath2 | grep -v lonbnd | wc -l`;
 $ntc=$ntc*1;

 $btdata=`grep -h $tdtg $tcbtpathyyyyp1 $tcbtpath $tcbtpath2 | grep -v lonbnd`;
## $cmd="grep -h $tdtg $tcbtpathyyyyp1 $tcbtpath $tcbtpath2 | grep -v lonbnd";
##print "CCC: $cmd\n";

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
  $tcbtpath=$WXMAP{"WXMAP_TC_BT_DIR"};
  $tcplotdir=$WXMAP{"WXMAP_TC_PLOT_DIR"};
  $ftdir=$WXMAP{"WXMAP_TC_FT_DIR"};
} elsif($tcopt eq 'ops') { 
  $tcbtpath=$WXMAP{"WXMAP_TC_BT_OPS_DIR"};
  $tcplotdir=$WXMAP{"WXMAP_TC_PLOT_OPS_DIR"};
  $ftdir=$WXMAP{"WXMAP_TC_FT_OPS_DIR"};
}

$ftstructdir=$WXMAP{'WXMAP_TC_STRUCT_DAT_DIR'};

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


sub tc_plot_area($lat,$lon,$area) {

  my($lat,$lon,$area,$lant,$epac)=@_;

  if( ($lat <= 20) && ($lon >= 60 && $lon <=220 ) ) {
    $area="$area bigaus";
  } 

  if( ($lat < 10 ) && ($lon>30 && $lon <130)) {
    $area="$area tropsio";
  }

  if($lat < 0 && ($lon>=90 && $lon<180)) {
      $area="$area tropoz";
  }

  if( ($lat < 50 && $lat > -10) && ($lon>30 && $lon <100)) {
    $area="$area tropnio";
  }

  if($lat < 20 && ($lon>=130 && $lon<360)) {
    $area="$area tropswpac";
  }

  if($lat > -10 && ($lon>=100 && $lon<180)) {
    $area="$area tropwpac";
  }

#
# 20000609 - improved logic for LANT/EPAC
#

  $epac=( ($lon>=276 && $lon<=282 && $lat<9 )
      || ($lon>=273 && $lon<276 && $lat<12 )
      || ($lon>=267 && $lon<273 && $lat<15 )
      || ($lon>=261 && $lon<267 && $lat<17 )
      );

  $lant=( ($lon>=276 && $lon<=282 && $lat>=9 )
      || ($lon>=273 && $lon<276 && $lat>=12 )
      || ($lon>=267 && $lon<273 && $lat>=15 )
      || ($lon>=261 && $lon<267 && $lat>=17 )
      );

  if( ( ($lat > 0) && ($lon>=180 && $lon<261)) || $epac) {
    $area="$area tropepac";
  }

  if( ( ($lat > 0) && ($lon>=276 && $lon<=360) ) || $lant) {
    $area="$area troplant";
  }

  return($area);
}

sub dtg_phr_command_prc($dtg) {
  
  my($dtg)=@_;
  my($odtg,@tt,$curdtgphr,$curdtg,$curphr);
  ($curdtg,$curphr)=dtg6('phr');
  
  $odtg=$dtg;

  $odtg=dtg4inc($curdtg,-144) if ($dtg eq 'cur-d6');
  $odtg=dtg4inc($curdtg,-120) if ($dtg eq 'cur-d5');
  $odtg=dtg4inc($curdtg,-96) if ($dtg eq 'cur-d4');
  $odtg=dtg4inc($curdtg,-24) if ($dtg eq 'cur-24');
  $odtg=dtg4inc($curdtg,-18) if ($dtg eq 'cur-18');
  $odtg=dtg4inc($curdtg,-12) if ($dtg eq 'cur-12');
  $odtg=dtg4inc($curdtg,-6) if ($dtg eq 'cur-6');

  $odtg=$curdtg if ($dtg eq 'cur');

  $odtg=dtg4inc($curdtg,+6) if ($dtg eq 'cur+6');
  $odtg=dtg4inc($curdtg,+12) if ($dtg eq 'cur+12');
  $odtg=dtg4inc($curdtg,+18) if ($dtg eq 'cur+18');

  if(length($odtg) != 10) {
    print "EEE: invalid dtg: $dtg  in dtg_phr_command_prc; length(dtg): ",length($dtg),"\n";
    exit(-999);
  } 

  return($odtg,$curphr);
    

}

sub dtg12_phr_command_prc($dtg) {
  
  my($dtg)=@_;
  my($odtg,@tt,$curdtgphr,$curdtg,$curphr);
  ($curdtg,$curphr)=dtg('phr');
  
  $odtg=$dtg;

  $odtg=dtg4inc($curdtg,-144) if ($dtg eq 'cur-d6');
  $odtg=dtg4inc($curdtg,-120) if ($dtg eq 'cur-d5');
  $odtg=dtg4inc($curdtg,-96) if ($dtg eq 'cur-d4');
  $odtg=dtg4inc($curdtg,-24) if ($dtg eq 'cur-24');
  $odtg=dtg4inc($curdtg,-18) if ($dtg eq 'cur-18');
  $odtg=dtg4inc($curdtg,-12) if ($dtg eq 'cur-12');
  $odtg=dtg4inc($curdtg,-6) if ($dtg eq 'cur-6');

  $odtg=$curdtg if ($dtg eq 'cur');

  $odtg=dtg4inc($curdtg,+6) if ($dtg eq 'cur+6');
  $odtg=dtg4inc($curdtg,+12) if ($dtg eq 'cur+12');
  $odtg=dtg4inc($curdtg,+18) if ($dtg eq 'cur+18');

  if(length($odtg) != 10) {
    print "EEE: invalid dtg: $dtg  in dtg_phr_command_prc; length(dtg): ",length($dtg),"\n";
    exit(-999);
  } 

  return($odtg,$curphr);
    

}

sub dtg_command_prc($dtg) {
  
  $curdtg=dtg6();

  my($dtg)=@_;
  my($odtg);

  $odtg=$dtg;

  $odtg=dtg4inc($curdtg,-144) if ($dtg eq 'cur-d6');
  $odtg=dtg4inc($curdtg,-120) if ($dtg eq 'cur-d5');
  $odtg=dtg4inc($curdtg,-96) if ($dtg eq 'cur-d4');
  $odtg=dtg4inc($curdtg,-24) if ($dtg eq 'cur-24');
  $odtg=dtg4inc($curdtg,-18) if ($dtg eq 'cur-18');
  $odtg=dtg4inc($curdtg,-12) if ($dtg eq 'cur-12');
  $odtg=dtg4inc($curdtg,-6) if ($dtg eq 'cur-6');

  $odtg=$curdtg if ($dtg eq 'cur');

  $odtg=dtg4inc($curdtg,+6) if ($dtg eq 'cur+6');
  $odtg=dtg4inc($curdtg,+12) if ($dtg eq 'cur+12');
  $odtg=dtg4inc($curdtg,+18) if ($dtg eq 'cur+18');

  if(length($odtg) != 10) {
    print "EEE: invalid dtg: $dtg  in dtg_command_prc; length(dtg): ",length($dtg),"\n";
    exit(-999);
  } 

  return($odtg);
    

}

sub dtg_12_command_prc($dtg) {
  
  $curdtg=dtg();

  my($dtg)=@_;
  my($odtg);

  $odtg=$dtg;

  $odtg=dtg4inc($curdtg,-24) if ($dtg eq 'cur-24');
  $odtg=dtg4inc($curdtg,-12) if ($dtg eq 'cur-12');

  $odtg=$curdtg if ($dtg eq 'cur');

  $odtg=dtg4inc($curdtg,+12) if ($dtg eq 'cur+12');

  if(length($odtg) != 10) {
    print "EEE: invalid dtg: $dtg  in dtg_command_prc; length(dtg): ",length($dtg),"\n";
    exit(-999);
  } 

  return($odtg);
    

}



sub LatLonMouseOver($area) {

    $llmohtm='';
    
    $doit=0;

    if($area eq 'troplant') {

	$doit=1;
	$arealatT=70.0;
	$arealatB=-10.0;
	$arealonL=-120.0;
	$arealonR=0.0;
	$areaxL=82;
	$areaxR=820;
	$areayT=36;
	$areayB=608;

    } elsif($area eq 'tropepac') {

	$doit=1;
	$arealatT=60.0;
	$arealatB=-10.0;
	$arealonL=160.0;
	$arealonR=300.0;
	$areaxL=40;
	$areaxR=880;
	$areayT=77;
	$areayB=564;


    } elsif($area eq 'tropwpac') {
	$doit=1;
	$doit=1;
	$arealatT=60.0;
	$arealatB=-10.0;
	$arealonR=200.0;
	$arealonL=80.0;
	$areaxL=43;
	$areaxR=880;
	$areayT=38;
	$areayB=604;

    }

    if($doit) {

$llmohtm="

<!-- show lat/lon code as doc going on end of preceeding doc -->

<script language=\"Javascript1.2\" src=\"../../js/numberformat.js\" type=\"text/javascript\"></script>
<script language=\"Javascript1.2\" src=\"../../js/showlatlon.js\" type=\"text/javascript\"></script>


<form name=\"Show\">
<input type=\"text\" name=\"MouseY\" value=\"0\" size=\"6\">
<input type=\"text\" name=\"MouseX\" value=\"0\" size=\"6\"> Lat/Lon<br>
</form>

<script language=\"JavaScript1.2\">

var tempX = 0
var tempY = 0

// offset that makes upper righthand corner (0,0)

var offsetxL=tp[0]
var offsetyT=tp[1]

//var IEoffsetX=-3
//var IEoffsetY=-3


// calc from parea and size of image in area.trop*.cfg

var xL=${areaxL}
var xR=${areaxR}

var lonL=${arealonL}
var lonR=${arealonR}

var yT=${areayT}
var yB=${areayB}

var latT=${arealatT}
var latB=${arealatB}

var dX=xR-xL
var dlonP=(lonR-lonL)/dX

var dY=yB-yT
var dlatP=(latT-latB)/dY
</script>

";

    }

    return($llmohtm);

}

1;
