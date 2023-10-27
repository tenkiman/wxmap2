#!/usr/bin/env perl

$perldir=$ENV{"W2_PERL_DIR"};
require("$perldir/mf.pl");
require("$perldir/wxmap.env.pl");
wxmap_env();

$okchk="n";
$title2="NULL";

$narg=$#ARGV+1;
$curdtg=dtg();

if($narg >= 2 ) {

  $area=$ARGV[0];
  $title1=$ARGV[1];
  $title2=$ARGV[2] if($narg >=3);

} else {

  print "\nThe argument list is:\n";
  print "       area :  \n";
  print "     title1 : bot title\n";
  print "   [title2] : top title  \n\n";
  exit;

}

#
#  create the configuration file
#

$gmode="-blc";
print "qqqq $area\n";
$cmd="grads $gmode \"run g.button.area.gs $curdtg $area area $title1 $title2 avn\""; 
print "CCC: $cmd\n";
system($cmd);

$gifname="$area.area.button.gif";

#$cmd="cp $gifname $WXMAP{'WXMAP_ICON_DIR'}";
#print "doing cp $cmd\n";
#system($cmd);

exit;




