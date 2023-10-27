#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};

#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss switches
#
# set ecmwf model
#
$NgpModel='ngp2';
$NgpModel='ngpc';
$NgpModel='navg';

$EcmModel='ecmn';
$EcmModel='ecmt';
$EcmModel='ecm';
$EcmModel='ecm4';

# 19980521 - new variable to turn off WXMAP ################
$WXMAP_OPS=1;

#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss switches


$WXMAP{'WXMAP_CLEAN_NDAY'}=10;
$WXMAP{'WXMAP_CLEAN_NDAY_DAT'}=5;

# 20041115 - use ldm ngp for all basetime
$WXMAP{'WXMAP_USE_NGP_LDM'}=1;

# 20050426 - set rsync v ftp option
$WXMAP{'WXMAP_USE_RSYNC'}=1;
$WXMAP{'WXMAP_USE_RSYNC'}=0;


$WXMAP2_BDIR=$ENV{"W2"};
$WXMAP{'WXMAP_WEB_DIR'}="$WXMAP2_BDIR/web";  #
############ -- $WXMAP{'WXMAP_WEB_DIR'}="$WXMAP2_BDIR/weba";  # 20130522 -- archive

# 19980521 - new variable to turn off WXMAP ################
$WXMAP_OPS=1;

$WXMAP_CUR_YEAR='2013';
$tcseason='NHS';

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

# -- tropics

$PlotsNhemTropfull="n850 uas shr prp w20 mhq wdl hhq lmq 500 u50 u70 w70 850 psl";
$PlotsShemTropfull="n850 uas shr prp w20 mhq wdl 850";
$PlotsTropMonitor="uas prp shr n850 w20 mhq psl";

# -- reduce here and in w2env.py
#
$PlotsNhemTropfull="n850 uas shr prp w20 mhq";
$PlotsShemTropfull="n850 uas shr prp w20 mhq";
$PlotsTropMonitor="n850 uas prp";

$WXMAP{'WXMAP_AREAS'}       ="asia:wconus:conus:nhem:tropwpac:tropnio:tropsio:tropoz:tropswpac:tropepac:troplant";
$WXMAP{'WXMAP_AREAS_TYPES'} ="midlat:midlat:midlat:special:tropic:tropic:tropic:tropic:tropic:tropic:tropic:tropic";
$WXMAP{'WXMAP_AREAS_DESC'}  ="East Asia:W CONUS:CONUS:NHEM:Tropical WPAC:Tropical NIO:Tropical SIO:Tropical Oz:Tropical SWPAC:Tropical EPAC:Tropical LANT";
