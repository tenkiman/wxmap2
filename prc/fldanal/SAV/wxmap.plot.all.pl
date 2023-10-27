#!/usr/bin/env perl

$perldir=$ENV{"WXMAP_PERL_DIR"};
require("$perldir/lib/mf.pl");
$wxdir=$ENV{"WXMAP_PRC_WXMAP_DIR"};
require("$wxdir/wxmap.env.pl");
wxmap_env();

###########################################
#
#  defaults and setup
#
###########################################
# 
# 20020622 - deprecate $offline
#
#$offline=0; # limit nogaps plots - set in wxmap.plot.pl

$Xdisplay="NULL";

$narg=$#ARGV+1;
$curdtg=dtg();
$curdtg=dtg6();

$specopt="";

$i=0;
if($narg >= 2) {
  $dtg=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;
  $model=$ARGV[$i] if($narg >$i); $i++;
  $specopt=$ARGV[$i] if($narg >$i); $i++;
} else {

  print "\n";
  print "Current dtg:   $curdtg\n\n";
  print "$0 processing :\n\n";
  print "         dtg  : YYYYmmddhh | curNNN NNN=-24,-18,...,+18\n";
  print "        model : avn | ngp | ukm | gsm\n\n";
  print "       specopt : npmoc.ldm";
  print "  Try again\n\n";
  exit(0);

}


$ldtg=length($dtg);
if($ldtg == 10) {
 $dtg2=substr($dtg,2,8);
} elsif($ldtg == 8) {
  $dtg2=$dtg;
  $yy=substr($dtg,0,2);
  if($yy >0) {
    $dtg='19'.$dtg2;
  } else {
    print "dtg2 problem: $dtg\n";
    exit;
  }
} else {
  print "Y2K problem: $dtg\n";
  exit;
}


##################################################
#
#	do the graphics
#
##################################################

if($model eq 'gsm') {
    @areas=undef;
    push(@areas,'tropwpac');
}


foreach $area (@areas) {
  $cmd="wxmap.plot.pl $dtg $area $model $specopt\n";
  print "CCC($0): $cmd\n";
  system($cmd);
}

exit(0);
