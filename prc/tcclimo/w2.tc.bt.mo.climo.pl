#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");
wxmap_env();
require("$perldir/p.tc.func.pl");
tc_setup();

$model='ngp';
$opt1='ngtrp';

#def_grid();
#test_ll2i();
#exit;

$verb=1;

$curdtg=dtg(); 

$narg=$#ARGV+1;

if($narg >= 2) {
  $byyyymm=$ARGV[0];
  $eyyyymm=$ARGV[1];
  $opt1=$ARGV[1] if($narg>=3);
} else {
  print "\n$0 - make lat/lon monthly freq filesn\n\nArguments:\n\n";
  print "The Current DTG: $curdtg\n\n";
  print "  byyyymm eyyyymm\n";
  print "   [opt1] : [ngtrp] | neumann | neumann.only\n";

  print "Try again...\n";
  exit(0);
}

$yyyymm=$byyyymm;

while ($yyyymm<=$eyyyymm) {

    print "doing yyyymm: $yyyymm\n";

    $yyyy=substr($yyyymm,0,4);
    $yyyym1=$yyyy-1;
    $yyyyp1=$yyyy+1;

#
#  force setting based on year
#

    $idir="/data/hfip/fiorino/w21/dat/tc/bt";
    $odir="/data/hfip/fiorino/w21/dat/tc/climo";

    $idir="/data/w22/dat/tc/bt";
    $odir="/data/w22/dat/tc/climo";

    $btpath='/tmp/bt.climo.input.txt';

#
# look in previous year because neuman data tries to put all calendar shem storms in the year dir
# wheras the jtwc bt is always one year ahead...
#
    $cmd0="grep -h $yyyymm $idir/$yyyym1/BT.*.txt | grep -v lonbnd | sort > $btpath ";
    $cmd1="grep -h $yyyymm $idir/$yyyy/BT.*.txt | grep -v lonbnd | sort >> $btpath ";
    $cmd2="grep -h $yyyymm $idir/$yyyyp1/BT.*.txt | grep -v lonbnd | sort >> $btpath";
    $cmd="$cmd0 ; $cmd1 ; $cmd2";

    $opath="$odir/bt.climo.$yyyymm.dat";

    print "OOO: $opath\n";
    print "CCC($0): $cmd\n";
    system($cmd);

#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
#
#  define the grids
#
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg


    def_grid();

    open(B,$btpath) || die "unable to open $btpath";
    open(O,">$opath") || die "unable to open $opath";


    while(<B>) {
	$card=$_;
	chomp($card);
#1997090812 02C 065 9999  18.1 159.9 -999 -999  +6h 272.6 10.9  12h 276.3  9.1  23 XX r34:   0   0   0   0 r50:   0   0   0   0
#1996090212 06L 075 0976  23.6 293.3  -99  -99 286.0 10.52 -10.07 003.00
#2007060218 02E 025 1006  15.2 267.7 -999 -999  +6h  17.9  6.3  12h  30.1  5.8  14 TD
#    0       1   2    3     4     5    6    7    8    9     10   11   12   13   14 15
	@tt=split(' ',$card);

	$tcstate=$tt[15];
	$lat=$tt[4];
	$lon=$tt[5];
	$mw=$tt[2]*1.0;
	$stid=$tt[1];
	$dtg=$tt[0];
	$snum=substr($stid,0,2);
#
# exclude 8? 9? ids
#
	next if($snum > 50);
#
# only do TC positions 
#
	$istc=istc();
	if($istc == 0) {
	    #print "NNNNN:  $dtg $mw $lat $lon $stid $tcstate\n";
	    next;
	} else {
	    #print "CCCC: $mw $lat $lon $stid $tcstate\n";
	}

	$ii=ll2i($lat,$lon);
	$ii--;
	if($mw > 130) {
	    print "QQQQ $lat $lon  $mw\n";
	}
	$tsdata[$ii]++ if($mw >= 35);
	$tydata[$ii]++ if($mw >= 65);

	$cat1data[$ii]++ if($mw >= 65 && $mw <= 82);
	$cat2data[$ii]++ if($mw >= 83 && $mw <= 95);
	$cat3data[$ii]++ if($mw >= 96 && $mw <= 113);
	$cat4data[$ii]++ if($mw >= 114 && $mw <= 135);
	$cat5data[$ii]++ if($mw >= 136);

	$acat1data[$ii]++ if($mw >= 65 && $mw <= 82);
	$acat2data[$ii]++ if($mw >= 65 && $mw <= 95);
	$acat3data[$ii]++ if($mw >= 65 && $mw <= 113);
	$acat4data[$ii]++ if($mw >= 65 && $mw <= 135);
	$acat5data[$ii]++ if($mw >= 136);

	$stydata[$ii]++ if($mw >= 130);

	$tcstr=TCscaledTCdays($mw);
	$tcace=TCACE($mw);
	$hurrace=HurrTCACE($mw);
	$tcstrgth[$ii]=$tcstrgth[$ii]+$tcstr;
	$tcACE[$ii]=$tcACE[$ii]+$tcace;
	$HurrACE[$ii]=$HurrACE[$ii]+$hurrace;


###  print "qqq $stid $dtg :: $lat $lon $mw $tcstr :: $ii\n" if($mw >= 35);

    }

#
# scale to TC-days vice TC-6h
#

    for($i=0;$i<$nij;$i++) {

	$tsdata[$i]=$tsdata[$i]*0.25;
	$tydata[$i]=$tydata[$i]*0.25;
	$stydata[$i]=$stydata[$i]*0.25;
	$tcstrgth[$i]=$tcstrgth[$i]*0.25;

	$cat1data[$i]=$cat1data[$i]*0.25;
	$cat2data[$i]=$cat2data[$i]*0.25;
	$cat3data[$i]=$cat3data[$i]*0.25;
	$cat4data[$i]=$cat4data[$i]*0.25;
	$cat5data[$i]=$cat5data[$i]*0.25;

	$acat1data[$i]=$acat1data[$i]*0.25;
	$acat2data[$i]=$acat2data[$i]*0.25;
	$acat3data[$i]=$acat3data[$i]*0.25;
	$acat4data[$i]=$acat4data[$i]*0.25;
	$acat5data[$i]=$acat5data[$i]*0.25;

    }

    print "NNNNNNNN: $#tsdata\n";

    $tsbd=pack("f" x ($#tsdata+1),@tsdata);
    $tybd=pack("f" x ($#tydata+1),@tydata);
    $stybd=pack("f" x ($#stydata+1),@stydata);
    $tcsbd=pack("f" x ($#tcstrgth+1),@tcstrgth);
    $tcacebd=pack("f" x ($#tcACE+1),@tcACE);
    $hurracebd=pack("f" x ($#HurrACE+1),@HurrACE);

    $cat1bd=pack("f" x ($#cat1data+1),@cat1data);
    $cat2bd=pack("f" x ($#cat2data+1),@cat2data);
    $cat3bd=pack("f" x ($#cat3data+1),@cat3data);
    $cat4bd=pack("f" x ($#cat4data+1),@cat4data);
    $cat5bd=pack("f" x ($#cat5data+1),@cat5data);

    $acat1bd=pack("f" x ($#acat1data+1),@acat1data);
    $acat2bd=pack("f" x ($#acat2data+1),@acat2data);
    $acat3bd=pack("f" x ($#acat3data+1),@acat3data);
    $acat4bd=pack("f" x ($#acat4data+1),@acat4data);
    $acat5bd=pack("f" x ($#acat5data+1),@acat5data);

    print O $tsbd;
    print O $tybd;
    print O $stybd;
    print O $tcsbd;
    print O $tcacebd;
	print O $hurracebd;
	

    print O $cat1bd;
    print O $cat2bd;
    print O $cat3bd;
    print O $cat4bd;
    print O $cat5bd;

    print O $acat1bd;
    print O $acat2bd;
    print O $acat3bd;
    print O $acat4bd;
    print O $acat5bd;

    close(O);

    yyyymminc($yyyymm,1);


}

exit;


#
# include subtropical
#
sub istc {

    $tcvmin=25;

    $tc=0;
    if($tcstate eq 'TD' ||
       $tcstate eq 'TS' ||
       $tcstate eq 'TY' ||
       $tcstate eq 'HU' ||
       $tcstate eq 'ST' ||
       $tcstate eq 'TC' &&
       $mw >= $tcvmin
       ) {
	$tc=1;
	
    } elsif($tcstate eq 'SD' ||
	    $tcstate eq 'SS' &&
	    $mw >= $tcvmin) {
	$tc=1;

    } elsif ( ($tcstate eq '' || $tcstate eq 'XX'  || $tcstate eq 'xx') && ($mw >= 25) ) {
	$tc=1;
    }

}

sub test_ll2i {

  for($lat=-90;$lat<=-87.5;$lat+=0.5) {
    for($lon=0;$lon<=10.0;$lon+=0.5) {
     $ii=ll2i($lat,$lon);
    }
  }
}


sub def_grid {
  $ni=144;
  $nj=73;
  $dlon=2.5;
  $lon0=0.0;
  $lat0=-90.0;
  $undef=1e20;
  $nij=$ni*$nj;
  for($i=0;$i<$nij;$i++) {

    $tsdata[$i]=0;
    $tydata[$i]=0;
    $stydata[$i]=0;
    $tcstrgth[$i]=0.0;
    $tcACE[$i]=0.0;
    $HurrACE[$i]=0.0;

    $cat1data[$i]=0.0;
    $cat2data[$i]=0.0;
    $cat3data[$i]=0.0;
    $cat4data[$i]=0.0;
    $cat5data[$i]=0.0;
    $acat1data[$i]=0.0;
    $acat2data[$i]=0.0;
    $acat3data[$i]=0.0;
    $acat4data[$i]=0.0;
    $acat5data[$i]=0.0;
  }

}


sub TCscaledTCdays($mw) {

  my($mw)=@_;
  my($dmw,$tsmin,$tymin,$stymin);

  $mw=$mw*1.0;
  $tdmin=25.0;
  $tsmin=35.0;
  $tymin=65.0;
  $stymin=130.0;

#
# 20070621 - if < TS set to 0.25 vice 0.5
#
# 20070906 - negative mw -> io data set to 0.5 
#
  $tcs=0.0;

  if($mw < 0.0) {
      $tcs=0.50;

  } elsif($mw >= $tdmin && $mw < $tsmin) {
      $tcs=0.25;

  } elsif($mw >= $tsmin && $mw < $tymin) {
      $dmw=($mw-$tsmin)/($tymin-$tsmin);
      $tcs=0.5+$dmw*0.5;

  } elsif($mw >= $tymin && $mw < $stymin) {
      $dmw=($mw-$tymin)/($stymin-$tymin);
      $tcs=1.0+$dmw*1.0;

  } elsif($mw >= $stymin) {
      $tcs=2.0;

  }

  return($tcs);

}


sub TCACE($mw) {

  my($mw)=@_;
  my($dmw,$tsmin,$tymin,$stymin);

  $mw=$mw*1.0;
  $tsmin=35.0;

  $ace=0.0;

  if($mw < 0.0) {
      $ace=0.0;

  } elsif($mw >= $tsmin) {
      $ace=$mw*$mw;
  } else {

      $ace=0.0;
  }
  return($ace);
}

sub HurrTCACE($mw) {

  my($mw)=@_;
  my($dmw,$tsmin,$tymin,$stymin);

  $mw=$mw*1.0;
  $tsmin=65.0;

  $ace=0.0;

  if($mw < 0.0) {
      $ace=0.0;

  } elsif($mw >= $tsmin) {
      $ace=$mw*$mw;
  } else {

      $ace=0.0;
  }
  return($ace);
}

sub ll2i($lat,$lon) {
  my($lat,$lon)=@_;
  my($i,$j,$ii,$verb);
  $verb=0;

  $i=($lon - $lon0)/$dlon + 0.5 ;
  $j=($lat - $lat0)/$dlon + 0.5 ;

  $i=$ni+$i if($i<=0);
  $i=$i-$ni if($i>=$ni);

  $i=int($i+1.0);
  $j=int($j+1.0);

  $ii=($j-1)*$ni + $i;
  if($verb) {
      print "qqq $lat $lon :: $i $j :: $ii\n";
  }

  return($ii);

}
