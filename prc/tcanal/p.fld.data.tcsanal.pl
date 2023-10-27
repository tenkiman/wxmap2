#!/usr/bin/env perl

$perldir=$ENV{"WXMAP_PERL_DIR"};
require("$perldir/lib/mf.pl");

$wxdir=$ENV{"WXMAP_PRC_WXMAP_DIR"};
require("$wxdir/wxmap.env.pl");
wxmap_env();

$model='ngp';
$analonly=0;
$cpath='NULL';

$narg=$#ARGV+1;
$curdtg=dtg6();

$i=0;
if($narg >= 2) {

  $tdtg=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;
  $model=$ARGV[$i] if($narg >$i); $i++;
  $cpath=$ARGV[$i]  if($narg >$i); $i++;

} else {

  print "\n$0 - create field data for tcsanal application :: arguments:\n\n";
  print "The current dtg: $curdtg\n\n";
  print "       tdtg  : YYYYmmddhh | curNNN NNN=-24,-18,...,+18\n";
  print "       model : ngp | ifs | XXXX.TT\n";
  print "       cpath : ctl file path\n";
  print "Try again...\n";
  exit(0);

}


if($cpath eq 'NULL') {
  if($model eq 'ukm' || $model eq 'ngp' ||  $model eq 'avn') {
    $ddir=$WXMAP{"WXMAP_DAT_BDIR"};
    $ddir="$ddir/dat";
    if($model eq 'ukm') {
      $cpath="$ddir/$model.12.$tdtg.ctl";
    } else {
      $cpath="$ddir/$model.10.$tdtg.ctl";
    }
  } else {
    print "cpath not set properly\n";
    exit(1);
  }
}

$cmd="grads -lbc \"run p.fld.data.tcsanal.gs $tdtg $model $cpath\"";
print"CCC($0): $cmd\n\n";
system($cmd);



exit(0);


