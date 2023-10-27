#!/usr/local/bin/perl

$ifile="s.txt";
$sfile="s.obs";

$cnt=0;

open(I,"cat $ifile | ")  || die "unable to open $ifile\n";
open(S,">$sfile") || die "unable to open $sfile_new\n";

#
#      end of time record
#

$nlev=0;
$id=9999;
$lat=0;
$lon=0;
$rt=0;
$iflag=0;

$bend=pack("a8fffii",$id,$lat,$lon,$rt,$nlev,$iflag);

#
#	read the text data and write out the binary data
#

while(<I>) {
  $card=$_;
  chop($card);
#  print "qqq $card cnt = $cnt\n";

  if($cnt == 0)  {

    $yy=substr($card,5,2);
    $mm=substr($card,8,2);
    $dd=substr($card,11,2);
    $hh=substr($card,14,2);
#    print "$yy $mm $dd $hh\n";
    $cnt++;


  } else {

    $cnt++;

    $nlev=1;
    $rt=0;
    $iflag=1;

    @t=split(' ',$card);
    $lat=$t[0]*0.1;
    $lon=$t[1]*0.1;
    $u=$t[2]*0.1;
    $v=$t[3]*0.1;

    $bhead=pack("a8fffii" ,$cnt,$lat,$lon,$rt,$nlev,$iflag);
    $bdata=pack("f" x 2 ,$u,$v);
    print S $bhead;
    print S $bdata;

  }

}


print S $bend;

close(I);
close(S);

exit;

