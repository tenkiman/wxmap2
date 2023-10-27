#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");
wxmap_env();
#
# mod of t.wxmap.pl to do clm plot
#

$okchk="n";
$area="tropaor";

$opt1='ops.wxmap';
$opt2='npmoc.ldm';

$model_grf_ext=$WXMAP{"WXMAP_MODELS_GRF_EXT"};

$narg=$#ARGV+1;
$curdtg=dtg6();

$i=0;
if( $narg >=2 )  {

    $dtg=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;
    $model=$ARGV[$i] if($narg >$i); $i++;
    $area=$ARGV[$i] if($narg >$i); $i++;

} else {

  print "\n$0 arguments:\n\n";
  print "The current dtg: $curdtg\n\n";
  print "        dtg : YYYYmddhh | cur | cur-12 | cur+12 \n";
  print "      model : basemap | ngp | avn | ukm | gsm\n";
  print"\n\n";
  exit;
}

$tua=0;

$xs=800;
$ys=600;

if($model eq 'nr1' | ($area eq 'tropaor') | ($area eq 'tropnhcaor') ) {
    $xs=1024;
    $xs=900;
    $ys=int($xs*3.0/4.0);
}

$gmode="-lbc";
$gcmd="run g.wxmap.base.gs";

$gdir="$model_archive_grfdir{$model}/$dtg";
$gcdir="$model_current_grfdir{$model}";

if($model eq 'nr1') {
    $gdir="$WXMAP{'WXMAP_WEB_DIR'}/clm/monthly";
    $gcdir=$gdir;
}

print "QQQ $gdir\n";

$grfprc='printim';
$bmapdir=$WXMAP{'WXMAP_BASEMAP_GDIR'};
$bmapgif="$bmapdir/basemap.$area.gif";

$cmd="wxmap.make.g.wxmap.gs.cfg.pl $dtg $model";
print "CCC: $cmd\n";
system($cmd);

$wxifile="g.wxmap.test.input.txt";
open(I,"> $wxifile" ) || die "unable to open $wxifile\n";

#
# defaults
#
$plot='clm';
$tau='000';
$specopt='npmocldm';


$gradsrun="$dtg $model $tau $area $pnum{$plot} y $gdir $gcdir $grfprc $xs $ys $mopt1";

$dtg4=$dtg;
$tcopt="ops";
#tc_posits($tau);

print "DDDDDD $gradsrun\n" ;
print "BBBBBposits: $btposits\n";
print "FFFFFposits: $ftposits\n";

print I "$gradsrun\n";
print I "$btposits\n";
print I "$ftposits\n";

close(I);

$gradscmd='grads';

$doit=1;
$cmd="$gradscmd $gmode \"$gcmd $wxifile $specopt\" -g ${xs}x${ys}";
print "CCCC: $cmd\n"; 
system($cmd) if($doit);

exit;

