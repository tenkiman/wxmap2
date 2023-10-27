#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");
wxmap_env();
require("$perldir/p.tc.func.pl");
tc_setup();

$pltdir='null';

tc_setup();

$curdtg=dtg();

$narg=$#ARGV+1;

if($narg >= 3 ) {

  $i=0;
  $dtg1=$ARGV[$i]; $i++;
  $dtg2=$ARGV[$i]; $i++;
  $dpath=$ARGV[$i]; $i++;
  $pltdir=$ARGV[$i]; $i++;

} else {

  print "$0:\n\n";
  print "Plot TC Activity\n";
  print "Uses the GrADS script g.tc.activity.gs to do the plotting\n\n";
  print "\nThe argument list is:\n";
  print "        dtg1 : YYYYmmddhh\n";
  print "        dtg2 : YYYYmmddhh\n";
  print "       dpath : ngtrp path\n";
  print "      pltdir : target dir for plots\n";
  print "\n";
  exit;

}

if($pltdir eq 'null') {
    $pltdir=$WXMAP{"WXMAP_TC_TRACK_PLOT_ACTIVITY_DIR"};
    $pltdir="/pcmdi/chico_dat/wxmap2/plt/tc/activity";
} else {
    print "PPPPPPPPPPPPPPPPPPPPPPPPPPPP pltdir: $pltdir\n";
}

$verb=0;


$time1=dtg2gtime($dtg1);
$time2=dtg2gtime($dtg2);

$yyyy=substr($dtg1,0,4);
$yyyy2=substr($dtg2,0,4);
$cccc1=substr($dtg1,0,2);
$cccc2=substr($dtg2,0,2);

$yy1=substr($dtg1,2,2);
$yy2=substr($dtg2,2,2);

print "time :: $time1 :: $time2 :: $yyyy :: $yyyy2\n";

$myearflag=1;

#$dpath="/tmp/ngtrp.test.txt";
#$dpath="/tmp/ngtrp.BT.2003.txt";
#$dpath="/tmp/ngtrp.BT.shem.2004.txt";

$opath="ngtrp.tc.activity.txt";
$spath="ngtrp.tc.activity.summary.txt";

print "dpath: $dpath  opath: $opath\n";

open(T,$dpath) || die "unable to open $dpath";
open(O,">$opath") || die "unable to open $opath";
open(S,">$spath") || die "unable to open $spath";

$j=0;
while(<T>) {
  $card=$_;
  chomp($card);
  @tt=split(' ',$card);
  $ntc=$tt[0];
  $yy=substr($tt[1],0,2);
  if($myearflag == 0) {
    $dtg=$cccc1.$tt[1];
  } else {
    if($yy == $yy1) {
      $dtg=$cccc1.$tt[1];
    } elsif($yy == $yy2) {
      $dtg=$cccc2.$tt[1];
    }
  }
  $j++;

  if(($card =~ 'at') || ($ntc>=1 && $ntc<=10)) {

    if($verb) {
	print "ntc: $ntc dtg: $dtg\n";
    }
    
    if($dtg <= $dtg2 && $dtg >= $dtg1) {  

	if($verb) {
	    print "card: $card :: $ntc :: $dtg\n";
	}

      undef(@stms);
      undef(@cards);

      $ntcfnl=0;
      for($i=0;$i<$ntc;$i++) {
	$card=<T>;
	chomp($card);
	@tt=split(' ',$card);
#
# convert neumman I to A to get in the NIO
#
	$tt[4]='A' if($tt[4] eq 'I') ;
	$sname=$tt[3].$tt[4];
	  if($verb) {
	      print "SSS: $sname\n";
	  }
	$snum=substr($sname,0,2)*1;
	if($snum <= 50) {
	  $ntcfnl++;
	  $vmax=$tt[2];
	  push @snames,$sname;
	  $vmaxs{$sname}=$vmax if($vmaxs{$sname} < $vmax || $vmaxs{$sname} eq '');
	  push @stms,$sname;
	  $cards{$sname}=$card;
	}
    }

      @stms=sort(@stms);
      
      $card="$ntcfnl  $dtg";
      print O "$card\n";

      foreach $stm (@stms) {
###	print "stm: $stm :: $cards{$stm}\n";
	print O "$cards{$stm}\n";
      }

    }

  }

}

@ss=uniq(@snames);

@zones=(1,2,3,4,5,6);
@classes=(all,st,tys,ty,ts,td);


foreach $b (@basins) {
  foreach $c (@classes) {
    $n{$b,$c}=0;
  }
}

foreach $s (@ss) {
  $sn=substr($s,0,2);
  $b=substr($s,2,1);
  $v=$vmaxs{$s};
###  print "$b :: s: $s :: $v\n";
  $n{$b,all}++;
  $n{$b,st}++ if($v >= 130);
  $n{$b,tys}++ if($v >= 100 && $v < 130);
  $n{$b,ty}++ if($v >= 65 && $v < 100);
  $n{$b,ts}++ if($v >= 35 && $v < 65);
  $n{$b,td}++ if($v < 35);
}

foreach $b (@basins) {
  print "NNN: $b :: $n{$b,st} :: $n{$b,tys} :: $n{$b,ty} :: $n{$b,ts} :: $n{$b,td} ALL: $n{$b,all}\n";
}


foreach $c (@classes) {

  $n{1,$c}=$n{L,$c};
  $n{2,$c}=$n{C,$c}+$n{E,$c};
  $n{3,$c}=$n{W,$c};
  $n{4,$c}=$n{A,$c}+$n{B,$c};
  $n{5,$c}=$n{S,$c};
  $n{6,$c}=$n{P,$c};

}

foreach $z (@zones) {
  $card=sprintf("%d %d %d %d %d %d %d",
		$z,$n{$z,all},$n{$z,td},$n{$z,ts},$n{$z,ty},$n{$z,tys},$n{$z,st});
  print "card: $card\n";
  print S "$card\n";
}

close(S);
close(O);

$plot='y';
$xsize="1024x768";
$xsize=1200;
$ysize=$xsize*(3.0/4.0);
$geosize="${xsize}x${ysize}";
$gmode="lc" if($plot eq "y");
$gname="$pltdir/tc.act.spec.$dtg1.$dtg2";
$gname="tc.act.spec.$dtg1.$dtg2";

$gradsexe='grads';
#$gradsexe='/w21/app/opengrads-2.2.1.oga.1/Contents/grads';
$gmode="lc";
$gmode="lbc";

# -- xysize set in .gs
$gclinput="$dtg1 $dtg2 $pltdir $gname $curdtg";

$cmd="$gradsexe -${gmode} \"run g.tc.activity.gs $gclinput\" -g ${geosize}-0+0";
print "CCC: $cmd\n";
system($cmd);
 
exit;

