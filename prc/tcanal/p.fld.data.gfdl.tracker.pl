#!/usr/bin/env perl

$perldir=$ENV{"WXMAP_PERL_DIR"};
require("$perldir/lib/mf.pl");

$wxdir=$ENV{"WXMAP_PRC_WXMAP_DIR"};
require("$wxdir/wxmap.env.pl");
wxmap_env();

$model='ngp';
$analonly='NULL';
$cpath='NULL';

$curdtg=dtg(); 

$narg=$#ARGV+1;

$i=0;

if($narg >= 2) {

  $dtg4=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;
  $model=$ARGV[$i] if($narg >$i); $i++;
  $cpath=$ARGV[$i] if($narg >$i); $i++;
  $lspath=$ARGV[$i]  if($narg >$i); $i++;
  $analonly=$ARGV[$i] if($narg >$i); $i++;
  $regrid=$ARGV[$i] if($narg >$i); $i++;

} else {

  print "\n$0 - create field data (sfc wind) for FNMOC TC tracker\n\nArguments:\n\n";
  print "The Current DTG: $curdtg\n\n";
  print "       dtg4 : cur | cur-12 (ditto) | cur+12 | YYYYmmddhh\n";
  print "      model : avn | ukm | ngp";
  print "      cpath : data ctl file path\n";
  print "     lspath : ls ctl file path\n";
  print " [analonly] : [0] | 1 \n";
  print "   [regrid] : [0] | 1 \n\n";
  print "Try again...\n";
  exit(0);
}


$dtg2=substr($dtg4,2,8);

$ddir=$model_archive_datdir{$model};
if($cpath eq 'NULL') {
  $cpath="$ddir/$model.10.$dtg4.ctl";
  if($dtg4 < 1999070700) {
    $cpath="$ddir/$model.10.$dtg2.ctl";
  }
}

$lspath="$WXMAP{'WXMAP_GEODIR'}/ls.1deg.ctl";
$cmd="grads -lbc \"run p.fld.data.gfdl.tracker.gs $dtg4 $model $cpath $lspath $analonly\"";
print "CCC: $cmd\n";
system($cmd);



exit(0);


