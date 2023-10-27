#!/usr/local/bin/perl

$ifile="ua.txt";
$sfile="ua.obs";

$cnt=0;

open(I,"cat $ifile | ")  || die "unable to open $ifile\n";
open(S,">$sfile") || die "unable to open $sfile_new\n";

$undef=1e20;
$d2r=3.141592654/180.0;

while(<I>) {
  $card=$_;
  chomp($card);
  next if(!($card =~ /\w/)) ;  # whitspace only (blank card)
  $id=substr($card,17,5) if(substr($card,0,7) eq "METXUAR");
  if(substr($card,1,3) eq "LOC") {
    $lat=substr($card,10,4);
    $hemns=substr($card,14,1);
    $lon=substr($card,15,5);
    $hemew=substr($card,20,1);
  }  



}
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


close(I);
close(S);

exit;


