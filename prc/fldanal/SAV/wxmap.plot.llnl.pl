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

$test=0;
$grfprc="gif";
$grfprc="wi";
$grfprc="printim";
$minsiz=15000;
$tauinc=12;
$xs=720;
$ys=540;
$res=10;
$res=12 if($model eq "ukm");
$verb=1;

$tcopt='ops';
$model_grf_ext=$WXMAP{"WXMAP_MODELS_GRF_EXT"};

###########################################
#
#	cmd line parsing and setup the dtg
#
###########################################

$curdtg=dtg();

$narg=$#ARGV+1;
$curdtg=dtg6();

$i=0;
if($narg >= 3) {

  $dtg=dtg_command_prc($ARGV[$i]) if($narg >$i); $i++;

  $area=$ARGV[$i] if($narg >$i); $i++;
  $model=$ARGV[$i] if($narg >$i); $i++;
  $tcopt=$ARGV[$i] if($narg > $i); $i++;
  $grfprc=$ARGV[5]  if($narg > $i); $i++;

} else {

  print "\n$0 arguments:\n\n";
  print "The current dtg: $curdtg\n\n";
  print "    dtg  : YYYYmmddhh | curNNN NNN=-24,-18,...,+18\n";
  print "   area  : ";
  foreach $a (@areas) {
    print "$a | ";
  }
  print"\n";
  print "       model : ";
  foreach $m (@models) {
    print "$m | ";
  }
  print "\n";
  print "     [tcopt] : [ops] | rd\n";
  print "    [grfprc] : wi gif | gxgif | xwd | ps\n";
  print "  Try again\n\n";
  exit;

}

#
# 20010124 - set grads by grfprc
#

#$gradsexe="gradsc";
#$gradsexe="vgrads.csh";
#$gradsexe="vgrads.ksh";

if($grfprc eq 'printim'){
  $gradsexe="pgrads";
  $gradsexe="xgrads";
  $gradsexe="grads";
} else {
  $gradsexe="vgrads";
}

#
#  QC user input
#

$iok=0;
for($i=0;$i<$#models;$i++) {
  $iok=1 if($model eq $models[$i]);
}

if(! $iok ) {
  print"EEEEE model = $model\n";
};

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#  yyyymmddhh for tc_posits
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if(length($dtg) == 8) {
  $dtg4="19${dtg}";
} else {
  $dtg4=$dtg;
}

$dtg2=substr($dtg,2,8);

#
#  taus and plots
#

$areatype=$area_type{$area};

#
#  turn off operational number of ngp limits
# 97113000 - force lower max plots if 00Z
#
#$chh=substr($dtg,6,2);
#$wxmap_maxplot_area{'ngp'}=11 if($chh eq "00");

#
# 20020622
# deprecate $offline setting of max plot...
#

$wxmap_maxplot_area{'ngp'}=999 ;

#
# chdir to apps dir
#

chdir($ENV{"WXMAP_PRC_WXMAP_DIR"});

#
#  define the file for grads plotting script will use for intput
#

$wxifile="g.wxmap.$area.$model.$dtg.plot.input.txt";
open(I,"> $wxifile" ) || die "unable to open $wxifile\n";

###########################################
#
#  setup the area including GrADS mode
#
###########################################

$atype="NULL";
for($i=0;$i<$narea;$i++) {
  $atype=$areatypes[$i] if($area eq $areas[$i]);
}

$gmode="-lc";
if( $grfprc eq 'gxgif' || $grfprc eq 'printim' ) {
  $gmode="-lbc";
}

###########################################
#
#  setup the dir for graphics and movie link dir
#
###########################################

$gdir="$model_archive_grfdir{$model}/$dtg";
$gcdir="$model_current_grfdir{$model}";

#$curgdir=$model_gdir{$model}."/current;

$mdir="$gdir/movie";


if ( ! (-d $gdir) ){
  system("mkdir $gdir");
}

if ( ! (-d $mdir) ){
  system("mkdir $mdir");
}


##################################################
#
#  create the configuration file
#
##################################################

$cmd="wxmap.make.g.wxmap.gs.cfg.pl $dtg $model";
print "CCC: $cmd\n";
system($cmd);

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#  get the hour and turn off ngp plots for the 00Z
#  run; only do SST
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

$hh=substr($dtg,6,2);

if(!($hh eq "00" && $model eq "ngp")) { 


###########################################
#
#  set up the GrADS plots
#
###########################################

  $nplot=0;

#  $pp=$plot_type_plots{$atype};
#  if($plot_control{$model,$area,'plots'} ne "") {
#    $pp=$plot_control{$model,$area,'plots'}  ;
#  }
#
#  if($plot_control{$model,'add','plots'} ne "") {
#    $pp="$pp $plot_control{$model,'add','plots'}"  ;
#  } 


@p=plot_types($model);
  foreach $plot (@p) {

###  print"QQQQ $model $area $atype $plot_type_taus{$atype} $plot_control{$model,$area,'taus'} \n";

# 971207 -  full control of taus by model, area and plot
#
    if($plot_control{$model,$area,$plot,'taus'} ne "") { 
      $tt=$plot_control{$model,$area,$plot,'taus'};
    } elsif($plot_control{$model,$area,'taus'} ne "") { 
      $tt=$plot_control{$model,$area,'taus'};
    } elsif($plot_control{$model,$plot,'taus'} ne "") {
      $tt=$plot_control{$model,$plot,'taus'};
    } else {
      $tt="$plot_type_taus{$atype}";
    }

##################################################
#
#  miscellaneous area options
#
##################################################

    $mopt1=$plot_control{$area,$plot,'units'} if($plot_control{$area,$plot,'units'} ne "") ;

####print"MMMM $mopt1\n";

    @t=split(/ /,$tt);

    if($t[0] eq "default") {
      $taubeg=0;
      $tauend=$model_ntau{$model};
      $tauinc=$model_tauinc{$model};
####print "QQQQQQQ $plot $model $tt $taubeg $tauend $tauinc\n";
    } else {
      $taubeg=$t[0];
      $tauend=$t[1];
      $tauinc=$t[2];
    }

    for($tt=$taubeg;$tt<=$tauend;$tt+=$tauinc) {

      $tau=sprintf("%03d",$tt);
      $gname="$gdir/$model${model_grf_ext}.$plot.$tau.$area.gif";
      $gcname="$gcdir/$model${model_grf_ext}.$plot.$tau.$area.gif";

      $gname="$gdir/$model${model_grf_ext}.$plot.$tau.$area.png";
      $gcname="$gcdir/$model${model_grf_ext}.$plot.$tau.$area.png";
      $doit="n";
      $siz=-1;
      $siz=(-s $gname) if(-e $gname) ;

      $doit="y" if($siz < $minsiz) ;

#print "QQQQ $siz $minsiz $doit\n";
#
#  limit number of plots in session
#
#print "qqq $model $wxmap_maxplot_area{$model}\n";

      $doit="n" if($nplot >= $wxmap_maxplot_area{$model});

#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
#
#  TC positions
#
#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

      undef(@tcareas);
      tc_posits($tau);
      
      plot_areas();

      $tcareacheck=0;
      foreach $tcarea (@tcareas) {
        $tcareacheck=1 if($area eq $tcarea);
      }

      if($tcareacheck == 0) { 
        $btposits="0";
        $ftposits="0";
      }

      if ( $doit eq "y" ) {
	$gradsrun="$dtg $model $tau $area $pnum{$plot} y $gname $gcname $grfprc $xs $ys $mopt1";
	print "DDDDDD $gradsrun\n" if($verb);
        #print "DDDDDD $btposits\n";
        #print "DDDDDD $ftposits\n";
	print I "$gradsrun\n";
        print I "$btposits\n";
        print I "$ftposits\n";
	$nplot++;

      }

    }

  }

}

###########################################
#
#  OTIS SST
#
###########################################

if($model eq 'ngp') {

  $plot="sst";
  $tau='000';
  $gname="$gdir/$model${model_grf_ext}.$plot.$tau.$area.gif";
  $gcname="$gcdir/$model${model_grf_ext}.$plot.$tau.$area.gif";

  $gname="$gdir/$model${model_grf_ext}.$plot.$tau.$area.png";
  $gcname="$gcdir/$model${model_grf_ext}.$plot.$tau.$area.png";

  $doit="n";
  $siz=-1;
  $siz=(-s $gname) if(-e $gname) ;
  $doit="y" if($siz < $minsiz) ;
  $doit="n" if($nplot >= $wxmap_maxplot_area{$model});

  print"SSSS $siz $gname $tau $doit\n" if($verb);

#tttttttttttttttttttttttttttttttttttttttttttttttttt
#
#  tc posits
#
#tttttttttttttttttttttttttttttttttttttttttttttttttt

tc_posits($tau);

  if($doit eq "y") {
    $gradsrun="$dtg $model $tau $area $pnum{$plot} y $gname $grfprc";
    $gradsrun="$dtg $model $tau $area $pnum{$plot} y $gname $gcname $grfprc";
    $gradsrun="$dtg $model $tau $area $pnum{$plot} y $gname $gcname $grfprc $xs $ys $mopt1";

    print "$gradsrun\n";
    print I "$gradsrun\n";
    $nplot++;
  }

}

###########################################
#
#  run GrADS
#
###########################################

close(I);

print"NNNNNNNNN nplot = $nplot\n";

if($nplot > 0) {
  $cmd="$gradsexe $gmode \"run g.wxmap.gs $wxifile\" -g ${xs}x${ys}";
  print"QQQ $cmd\n";
  system($cmd) if(! $test);
}

###########################################
#
#  set up movies
#
###########################################

foreach $plot (@p) {

  @t=split(/ /,$taus{$model,'all'});
  @t=split(/ /,$taus{$model,'prp'}) if($plot eq 'prp');

  for($tau=$taubeg;$tau<=$tauend;$tau+=$tauinc) {

    $numtau=$tau/$tauinc+1;

    $gname="$gdir/$model${model_grf_ext}.$plot.$tau.$area.gif";
    $gname_movie="$mdir/$model${model_grf_ext}.$plot.$numtau.$area.gif";

    $gname="$gdir/$model${model_grf_ext}.$plot.$tau.$area.png";
    $gname_movie="$mdir/$model${model_grf_ext}.$plot.$numtau.$area.png";

    $siz=-1;
    $siz=(-s $gname) if(-e $gname) ;

    if ($siz > $minsiz && !(-e $gname_movie) ) {

      $cmd="ln -s $gname $gname_movie";
      system($cmd) if(! $test);
    }  
      
  }

}

#
#  kill off the g.cfg files
#
#system("rm $wxifile");
exit(0);



