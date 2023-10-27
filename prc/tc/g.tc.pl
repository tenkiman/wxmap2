#!/usr/bin/env perl

$perldir=$ENV{"WXMAP_PERL_DIR"};
require("$perldir/lib/mf.pl");

$wxdir=$ENV{"WXMAP_PRC_WXMAP_DIR"};
require("$wxdir/wxmap.env.pl");
wxmap_env();

$tcprcdir=$ENV{"WXMAP_PRC_TC_DIR"};

$tcprcdir="$tcprcdir/tctrack";
require("$tcprcdir/p.tc.func.pl");

tc_setup();
$plot='y';
$vtype='hetero';
$ptype='ops';
$opt1='NULL';
$mfilt='ASDFASDFASDF';
$bttype='ops.jtwc';

$verb=0;

$curdir=`pwd`;
chop($curdir);

#
# make 2-D stats from yearly .ctl file 
#

$narg=$#ARGV+1;

if($narg >= 5 ) {

  $i=0;
  $yyyy=$ARGV[$i]; $i++;
  $vvvv=$ARGV[$i]; $i++;
  $stmid=$ARGV[$i]; $i++;
  $vmodel=$ARGV[$i]; $i++;
  $ptype=$ARGV[$i]; $i++;
  $opt1=$ARGV[$i] if($ARGV[$i] ne '') ; $i++;
  if($i>=7) { $vtype=$ARGV[$i] ; $i++ }
  $mfilt=$ARGV[$i] if($ARGV[$i] ne '') ; $i++;

} else {

  print "$0:\n\n";
  print "Plots TC positions from the ERA and NCEP reanals with statistics\n";
  print "Uses the GrADS script g.tc.gs to do the plotting\n\n";
  print "\nThe argument list is:\n";
  print "        yyyy : YYYY | YYYYMM\n";
  print "       vvvv  : tmp | VVVV in  tc.veri.VVVV.txt file (e.g., drops.new)\n";
  print "       stmid : NNL where L = basin parameter\n";
  print "      vmodel : ifs | mmm1,mm2 -- verify model(s)\n";
  print "       ptype : [ops] | era40.batch | exp | rd | exp.ifs (current cases) | ops.batch\n";
  print "        opt1 : [NULL] | 2plot | ll.lat1.lat2.lon1.lon2\n";
  print "     [vtype] : [hetero] | homo\n";
  print "     [mfilt] : [] | models to filter out\n";
  print "\n";
  exit;
}


if(length($stmid) != 3) {
  print "EEE: invalid stmid: $stmid\n";
  exit(1);
}


$xsize='600x800';
$gmode="pbc";
$gmode="pc" if($plot eq "y");
$xsize="800x600";
$xsize="1024x768";
$gmode="lbc" if($ptype =~ 'batch');
$gmode="lc" if($plot eq "y" && !($ptype =~ 'batch') );
$gcmd='grads';


if($opt1 eq '2plot') {

  $xsize="600x800";
  $gmode="pbc";
  $gmode="pc" if($plot eq 'y');

}

if($ptype eq 'ops.batch' || $ptype eq 'era40.batch') {
  $gcmd='vgrads';
  $gcmd='grads';
}

if($opt1 =~ 'll') {
  @tt=split('\.',$opt1);
  $lat1=$tt[1];
  $lat2=$tt[2];
  $lon1=$tt[3]*1;
  $lon2=$tt[4]*1;
  $lon1=360+$lon1 if($lon1<0);
  $lon2=360+$lon2 if($lon2<0);

  $opt1="ll $lat1 $lat2 $lon1 $lon2";
}

#
# pass TC name to g.tc.gs
#
if($opt1 =~ 'name') {
  @tt=split('\.',$opt1);
  $tctype=$tt[1];
  $tcname=$tt[2];
  $opt1="name $tctype $tcname";
}

$bname=substr($stmid,2,1);
$bname=$basin{$bname};
$nbasin=$basin{substr($stmid,2,1),'num'};
$nstorm=substr($stmid,0,2)*1;

##################################################
#
# file setup
#
##################################################

$pltdir='/tmp';
$pltdir=$WXMAP{"WXMAP_TC_TRACK_PLOT_DIR"};


if($ptype =~ 'ops') {
  $btdir=$WXMAP{"WXMAP_TC_BT_OPS_DIR"};
  $ftdir=$WXMAP{"WXMAP_TC_FT_OPS_DIR"};
  $veridir="$WXMAP{'WXMAP_TC_VERI_OPS_DIR'}";
} elsif($ptype =~ 'exp' || $ptype =~ 'era40') {
  $btdir=$WXMAP{"WXMAP_TC_BT_EXP_DIR"};
  $ftdir=$WXMAP{"WXMAP_TC_FT_EXP_DIR"};
  $veridir="$WXMAP{'WXMAP_TC_VERI_EXP_DIR'}";


} else {
  $btdir=$WXMAP{"WXMAP_TC_BT_DIR"};
  $ftdir=$WXMAP{"WXMAP_TC_FT_DIR"};
  $veridir="$WXMAP{'WXMAP_TC_VERI_DIR'}";
}

if($vvvv =~ 'tmp') {
  $veridir="/tmp";
}

#ooooooooooooooooooooooooooooooooooooooooooooooooooo
#
# direct overide
#
#ooooooooooooooooooooooooooooooooooooooooooooooooooo

if($ptype eq 'era40' || $ptype eq 'era40.batch') {
  $btdir="/pcmdi/chico_dat/wxmap2/dat/tc/bt";
  $ftdir="/pcmdi/chico_dat/wxmap2/dat/tc/fc/era40";
  $veridir="/pcmdi/chico_dat/wxmap2/dat/tc/veri";
  $pltdir="/pcmdi/chico_dat/wxmap2/plt/tc/era40/trk";
}

if($ptype eq 'ops.batch') {
  $btdir="/pcmdi/chico_dat/wxmap2/dat/tc/bt";
  $ftdir="/pcmdi/tenki_dat/nwp/dat/tc/ft_ops";
  $veridir="/pcmdi/chico_dat/wxmap2/dat/tc/veri";
  $pltdir="/pcmdi/chico_dat/wxmap2/plt/tc/era40/trk";
}

print "PPPPPPPPPPPPPPP   btdir: $btdir\n";
print "PPPPPPPPPPPPPPP   ftdir: $ftdir\n";
print "PPPPPPPPPPPPPPP veridir: $veridir\n";

$grepyyyy=$yyyy;

if(length($yyyy) == 6) {

  $yyyymm=$yyyy;
  $yyyy=substr($yyyy,0,4);
  $grepyyyy=$yyyymm;

}

$btyyyy=2002;
$btyyyy=$yyyy;

if($btyyyy <= 2000 && !($ptype =~ 'era40')) {
    $bttype='neumann';
    $btdir="$btdir/bt_neumann";
}

if($bttype eq 'ops.jtwc') {
  $btpath="$btdir/$btyyyy/bt.jtwc.$bname.$btyyyy.$stmid.txt";
  $btpath="$btdir/$btyyyy/bt.local.jtwc.$bname.$yyyy.$stmid.txt";
} elsif($bttype eq 'neumann') {
  $btpath="$btdir/$btyyyy/bt.neumann.$bname.$btyyyy.$stmid.txt";
} else {
  $btpath="$btdir/$btyyyy/bt.ngtrp.$bname.$btyyyy.$stmid.txt";
}

if($ptype =~ 'exp' || $ptype =~ 'era40' ) {
  $ftipath="$veridir/tc.veri.$vvvv.ctat.txt";
  $vpath="$veridir/tc.veri.$vvvv.tc.ctl";
  $bname=substr($stmid,2,1);
  $bname=$basin_neumann{$bname};
  $btpath="$btdir/$yyyy/bt.neumann.$bname.$yyyy.$stmid.txt";
  if($yyyy > 2001) {
    $btdir=$WXMAP{"WXMAP_TC_BT_OPS_DIR"};
    $btpath="$btdir/$yyyy/bt.ngtrp.$bname.$yyyy.$stmid.txt";
  }

} else {
  $ftipath="$veridir/tc.veri.$vvvv.txt";
  $vpath="$veridir/tc.veri.$vvvv.tc.ctl";
}

#ooooooooooooooooooooooooooooooooooooooooooooooooooo
#
# direct overide
#
#ooooooooooooooooooooooooooooooooooooooooooooooooooo

if($ptype eq 'era40' || $ptype eq 'era40.batch' || $ptype eq 'ops.batch') {
    if($btyyyy >= 2001) {
	$bname=substr($stmid,2,1);
	$bname=$basin{$bname};
	$btpath="$btdir/$btyyyy/bt.local.jtwc.$bname.$btyyyy.$stmid.txt";
    } else {
	$btpath="$btdir/$btyyyy/bt.neumann.$bname.$btyyyy.$stmid.txt";
    }
    $ftipath="$veridir/tc.veri.$vvvv.txt";
}

if($ptype eq 'ops.w2') {

    $btdir="/pcmdi/chico_dat/wxmap2/dat/tc/bt";
    $ftdir="/pcmdi/chico_dat/wxmap2/dat/tc/fc/era40";
    $veridir="/pcmdi/chico_dat/wxmap2/dat/tc/veri";
    $pltdir="/pcmdi/chico_dat/wxmap2/plt/tc/era40/trk";
    $btpath="$btdir/$btyyyy/BT.$bname.$btyyyy.$stmid.txt";
    $ftipath="$veridir/tc.veri.$vvvv.txt";
}

$ftopath="/tmp/g.tc.ft.input.$yyyy.$stmid.txt";
$ftgpath='/tmp/g.tc.ft.txt';

print "nbtpath: $btpath\nftipath: $ftipath \nftopath: $ftopath\nftgpath: $ftgpath\n";

$overide=1;
$sizgft=(-s $ftopath);
if($sizgft eq '' || $sizgft == 0 || $overide) {
  $cmd="grep $grepyyyy $ftipath | grep $stmid | grep -v $mfilt > $ftopath";
  $cmd="grep $stmid $ftipath |  grep -v $mfilt > $ftopath";
  print "CCC($0): $cmd\n";
  system($cmd);
  $sizgft=(-s $ftopath);
#
# if SHEM look to previous year
#

  if($sizgft == 0 && ($bname eq 'sio' || $basin eq 'swp') ) {
    $grepyyyy=$grepyyyy-1;
    print "EEE: no forecast track cards to process\n";
    $cmd="grep $grepyyyy $ftipath | grep $stmid | grep -v $mfilt > $ftopath";
    $cmd="grep $stmid $ftipath |  grep -v $mfilt > $ftopath";
    print "CCC($0): $cmd\n";
    system($cmd);
    $sizgft=(-s $ftopath);
  }

}

$sizgft=(-s $ftopath);

if($sizgft == 0) {
  print "EEE: no forecast track cards to process\n";
  exit(1);
}

open(FI,$ftopath) || die "unable to open $ftopath";
open(FO,"> $ftgpath") || die "unable to open $ftgpath";


$dtgnew='00000000';
$modelnew='asdfasdf';
undef(@models);
@cards=<FI>;
foreach $card (@cards) {

  chomp($card);
  @tt=split(' ',$card);

  $model=$tt[0];
  $tau=$tt[1];
  $lat=$tt[6];
  $lon=$tt[7];
  $mw=$tt[16];
  $dtg=$tt[3];
  $hh=substr($dtg,8,2);

  $all{$model,$dtg,$tau,'lat'}=$lat;
  $all{$model,$dtg,$tau,'lon'}=$lon;
  $all{$model,$dtg,$tau,'mw'}=$mw;
  $all{$model,$dtg,'ntau'}++;

  push @models, $model;

# not really necessary ............... since the fc in the veri deck only has 12Z....
# plot only the 12Z forecast
#
#  print "ddddddddddddd $dtg\n";
#  if($ptype =~ 'era40' && $hh eq '12') {
#      push @dtgs, $dtg;
#  }  

  push @dtgs, $dtg;

  push @taus, $tau;

###  print "II: $model :: $dtg :: $tau :: $lat :: $lon :: $mw :: $hh\n";
  
}

@models=uniq(@models);
@dtgs=uniq(@dtgs);
@taus=uniq(@taus);

@tt=split(',',$vmodel);

if($#tt >= 1) {
  @models=@tt;
  $vmodel=$tt[0];
} 

if($#tt == 0) {
    undef(@models);
    push @models,$vmodel;
}


if($verb) {
    foreach $dtg (@dtgs) {
	print "DDD $dtg\n";
    }
}

foreach $model (@models) {
  foreach $dtg (@dtgs) {
    $fcard{$model,$dtg}='';

    foreach $tau (@taus) {
      $lat=$all{$model,$dtg,$tau,'lat'};
      $lon=$all{$model,$dtg,$tau,'lon'};
      $mw=$all{$model,$dtg,$tau,'mw'};
      if($tau eq '000' && $lon > 0) {
	$fcard{$model,$dtg}="$tau $lat $lon $mw";
      } elsif($lon > 0 && $lon < 360.0 && $tau gt '000' ) {
	$fcard{$model,$dtg}="$fcard{$model,$dtg} : $tau $lat $lon $mw "; 
      }
    }
  }
}

foreach $model (@models) {
  foreach $dtg (@dtgs) {
    if($fcard{$model,$dtg} ne '') {
      print "OO: $model $dtg :: $fcard{$model,$dtg}\n" if($verb);
      print FO "$model $dtg :: $fcard{$model,$dtg}\n";
    }
  }
}


close(FI);
close(FO);

$siz=(-s $ftgpath) if(-e $ftgpath) ;
print "dddddddddddddddddddddddd $ftopath\n";
print "DDDDDDDDDDDDDDDDDDDDDDDD $ftgpath :: $siz\n";

#sssssssssssssssssssssssssssssssssssssssssssss
#
#  sayoonara out if no fc tracks
#
#sssssssssssssssssssssssssssssssssssssssssssss

if($siz == 0) {
    print "EEEEEEEEEEEEEEEEEE no fc for: $vmodel\n";
    exit;
}

$gclinput="$ptype $btpath $ftgpath $vpath $pltdir $plot $vmodel $stmid $nstorm $nbasin $vvvv $vtype $bname $yyyy $opt1 $xsize";


$cmd="$gcmd -${gmode} \"run g.tc.gs $gclinput\" -g ${xsize}-0+0";
print "CCC(g.tc.gs) : $cmd\n";
#system($cmd);

exit;
 
system("rm $ftopath");
system("rm $ftgpath");
    
exit;

sub uniq (@list) {
  my(@mm,$m,$mnew);
  @list=@_;
  @mm=sort @list;
  undef(@list);
  $mnew="${mm[0]}ASDFASDFASDF";
  foreach $m (@mm) {
    if($m ne $mnew) {
      push @list,$m;
      $mnew=$m;
    }
  }
  return(@list);
}


