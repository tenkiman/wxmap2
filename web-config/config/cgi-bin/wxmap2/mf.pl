$century=20;
#
#     utility routines
#
%mname=(
'01','January',
'02','February',
'03','March',
'04','April',
'05','May',
'06','June',
'07','July',
'08','August',
'09','September',
'10','October',
'11','November',
'12','December'
);

%mname3=(
'01','Jan',
'02','Feb',
'03','Mar',
'04','Apr',
'05','May',
'06','Jun',
'07','Jul',
'08','Aug',
'09','Sep',
'10','Oct',
'11','Nov',
'12','Dec'
);

sub dtg000 {
  local ($i)=@_;
  if($i<10) {
    $tauTTT="00$i";
  } elsif($i<100) {
    $tauTTT="0$i";
  } else { 
    $tauTTT=$i;
  } 
  return $tauTTT;
}
#-------------------------------------------------------
#
#     dtg routines
#
#-------------------------------------------------------

sub dtginc {

@mday=(31,28,31,30,31,30,31,31,30,31,30,31);
@mdayleap=(31,29,31,30,31,30,31,31,30,31,30,31);
@aday=(1,32,60,91,121,152,182,213,244,274,305,335);
@adayleap=(1,32,61,92,122,153,183,214,245,275,306,336);
@adayleap=(1,32,61,92,122,153,183,214,245,275,306,336);


my ($idtg,$off)=@_;
my ($i,$yr,$mo,$dy,$hr,$leap,$ndyyr,$jdy);

$ndyyr=365;
$leap=0;

$yr=substr($idtg,0,2)*1;
$mo=substr($idtg,2,2)*1;
$dy=substr($idtg,4,2)*1;
$hr=substr($idtg,6,2)*1;

$hr=$hr+$off;
$leap=1 if($yr%4==0);

$ndyyr=366 if($leap);

$jdy=$dy-1;
if($leap) {
  $jdy=$jdy+$adayleap[$mo-1];
} else {
  $jdy=$jdy+$aday[$mo-1];
}

#print "start jdy = $jdy $hr\n";

while($hr>=24) {
  $hr=$hr-24;
  $jdy++;
}

while($hr<0) {
  $hr=$hr+24;
  $jdy--;
}

#print "end jdy = $jdy $ndyyr\n";

#
#  year adjustment (only one for now)
#

if($jdy <= 0) {
  $yr--;
  $leap=0;
  $leap=1 if($yr%4==0);
  $ndyyr=366 if($leap);
  $jdy=$jdy+$ndyyr;
}

if($jdy > $ndyyr) {
  $jdy-=$ndyyr;
  $yr++;
  $leap=0;
  $leap=1 if($yr%4==0);
  $ndyyr=366 if($leap);
}

#print"yyy $jdy $yr\n";

$leap=0;
$leap=1 if($yr%4==0);

#
# find the month and day of month
#

if($leap) {
  $i=11;
  while($jdy < $adayleap[$i]) {
    $i--;
  }
  $ndy=$jdy-$adayleap[$i]+1;
} else {
  $i=11;
  while($jdy < $aday[$i]) {
    $i--;
  }
  $ndy=$jdy-$aday[$i]+1;
}

$mo=$i+1;
$dy=$ndy;

$ndtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$hr);

return $ndtg;

}


#-------------------------------------------------------
#
#     dtg routines
#
#-------------------------------------------------------

sub dtg4inc {

@mday=(31,28,31,30,31,30,31,31,30,31,30,31);
@mdayleap=(31,29,31,30,31,30,31,31,30,31,30,31);
@aday=(1,32,60,91,121,152,182,213,244,274,305,335);
@adayleap=(1,32,61,92,122,153,183,214,245,275,306,336);
@adayleap=(1,32,61,92,122,153,183,214,245,275,306,336);


my ($idtg,$off)=@_;
my ($i,$yr,$mo,$dy,$hr,$leap,$ndyyr,$jdy,$ct);
 my ($verb);

 $verb=0;


$ndyyr=365;
$leap=0;

$ct=substr($idtg,0,2)*1;
$yr=substr($idtg,2,2)*1;
$mo=substr($idtg,4,2)*1;
$dy=substr($idtg,6,2)*1;
$hr=substr($idtg,8,2)*1;


$hr=$hr+$off;
$leap=1 if($yr%4==0);

$ndyyr=366 if($leap);

$jdy=$dy-1;
if($leap) {
  $jdy=$jdy+$adayleap[$mo-1];
} else {
  $jdy=$jdy+$aday[$mo-1];
}

print "start jdy = $jdy $hr\n" if($verb) ;

while($hr>=24) {
  $hr=$hr-24;
  $jdy++;
}

while($hr<0) {
  $hr=$hr+24;
  $jdy--;
}

#print "end jdy = $jdy $ndyyr\n";

#
#  year adjustment (only one for now)
#

if($jdy <= 0) {
  $yr--;
  if($yr < 0) {
    $yr=100+$yr;
    $ct--;
  }
  $leap=0;
  $leap=1 if($yr%4==0);
  $ndyyr=366 if($leap);
  $jdy=$jdy+$ndyyr;
}

if($jdy > $ndyyr) {
  $jdy-=$ndyyr;
  $yr++;
  if($yr == 100) {
    $yr=0;
    $ct++;
  }
  $leap=0;
  $leap=1 if($yr%4==0);
  $ndyyr=366 if($leap);
}

#print"yyy $jdy $yr\n";

$leap=0;
$leap=1 if($yr%4==0);

#
# find the month and day of month
#

if($leap) {
  $i=11;
  while($jdy < $adayleap[$i]) {
    $i--;
  }
  $ndy=$jdy-$adayleap[$i]+1;
} else {
  $i=11;
  while($jdy < $aday[$i]) {
    $i--;
  }
  $ndy=$jdy-$aday[$i]+1;
}

$mo=$i+1;
$dy=$ndy;

$ndtg=sprintf("%02d%02d%02d%02d%02d",$ct,$yr,$mo,$dy,$hr);

return $ndtg;

}


sub ndaymo {

@mday=(31,28,31,30,31,30,31,31,30,31,30,31);
@mdayleap=(31,29,31,30,31,30,31,31,30,31,30,31);

my($idtg)=@_;
my($i,$yr,$mo,$ndymo);
#my(@mday,@mdayleap);
 
$leap=0;

$yr=substr($idtg,0,4)*1;
$mo=substr($idtg,4,2)*1;

$leap=1 if($yr%4==0);
$mo--;

$ndymo=$mday[$mo];
$ndymo=$mdayleap[$mo] if($leap);

return $ndymo;

}



sub dtg {


my ($opt)=$_[0];
my ($year,$chr,$curdtg);

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);

$yr=$year;
$mo=$mon+1;
$dy=$mday;
$mn=$min+1;
$sc=$sec;
$fhr=$hour+1;
$yr=00 if($yr == 100);
$yr=$yr-100 if($yr >= 100);

$phr=$hour%12;
$hr=int($hour/12)*12;

$hour00=sprintf("%02d",$hour) ;
$hr00=sprintf("%02d",$hr) ;
$mo00=sprintf("%02d",$mo) ;
$dy00=sprintf("%02d",$dy) ;
$mn00=sprintf("%02d",$mn) ;
$sc00=sprintf("%02d",$sc) ;
$yr00=sprintf("%02d",$yr) ;

if($opt eq 'ph') {
  $curdtg=sprintf("%02d%02d%02d%02d %02d\:%02d",$yr,$mo,$dy,$hr,$phr,$mn);
} elsif($opt eq 'time') {
  $curdtg="$hour00\:$mn00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'timesec') {
  $curdtg="$hour00\:$mn00\:$sc00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'watchtime') {
  $curdtg="$hr00\:00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'full' || $opt eq 'dtg4') {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$hr);
} elsif($opt eq 'fullhm') {
  $curdtg=sprintf("%02d%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$fhr,$mn);
} elsif($opt eq 'fullph') {
  $curdtg=sprintf("%02%02d%02d%02d%02d +%02d\:%02d",$century,$yr,$mo,$dy,$hr,$phr,$mn);
} elsif($opt eq 'eccurdtg') {
#$yr=98;$mo=4;$dy=5;$fhr=3;  ecmwf DTG change calculator assumig 12Z run comes in +15Z
  $curdtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$fhr);
  $curdtg=dtginc($curdtg,-27);
  $curdtg=substr($curdtg,0,6).'12';
} elsif($opt eq 'eccurdtg4') {
#$yr=98;$mo=4;$dy=5;$fhr=3;  ecmwf DTG change calculator assumig 12Z run comes in +15Z
  $curdtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$fhr);
  $curdtg=dtginc($curdtg,-27);
  $curdtg=$century.substr($curdtg,0,6).'12';
} else {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$hr);
}
return $curdtg;

}

sub dtg6 {

my ($opt)=$_[0];
my ($year,$chr,$curdtg);

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);

$yr=$year;
$mo=$mon+1;
$dy=$mday;
$mn=$min+1;
$sc=$sec;
$fhr=$hour+1;
$yr=00 if($yr == 100);
$yr=$yr-100 if($yr >= 100);

$phr=$hour%6;
$hr=int($hour/6)*6;

$hour00=sprintf("%02d",$hour) ;
$hr00=sprintf("%02d",$hr) ;
$mo00=sprintf("%02d",$mo) ;
$dy00=sprintf("%02d",$dy) ;
$mn00=sprintf("%02d",$mn) ;
$sc00=sprintf("%02d",$sc) ;
$yr00=sprintf("%02d",$yr) ;

if($opt eq 'ph') {
  $curdtg=sprintf("%02d%02d%02d%02d +%02d\:%02d",$yr,$mo,$dy,$hr,$phr,$mn);
} elsif($opt eq 'time') {
  $curdtg="$hour00\:$mn00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'timesec') {
  $curdtg="$hour00\:$mn00\:$sc00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'watchtime') {
  $curdtg="$hr00\:00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'full' || $opt eq 'dtg4') {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$hr);
} elsif($opt eq 'fullhm') {
  $curdtg=sprintf("%02d%02d%02d%02d %02d:%02d",$century,$yr,$mo,$dy,$fhr,$mn);
} elsif($opt eq 'fullph') {
  $curdtg=sprintf("%02%02d%02d%02d%02d +%02d\:%02d",$century,$yr,$mo,$dy,$hr,$phr,$mn);
} elsif($opt eq 'eccurdtg') {
 #$yr=98;$mo=4;$dy=5;$fhr=3;  ecmwf DTG change calculator assumig 12Z run comes in +15Z
  $curdtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$fhr);
  $curdtg=dtginc($curdtg,-27);
  $curdtg=substr($curdtg,0,6).'12';
} elsif($opt eq 'eccurdtg4') {
 #$yr=98;$mo=4;$dy=5;$fhr=3;  ecmwf DTG change calculator assumig 12Z run comes in +15Z
  $curdtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$fhr);
  $curdtg=dtginc($curdtg,-27);
  $curdtg=$century.substr($curdtg,0,6).'12';
} else {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$hr);
}
return $curdtg;

}

#
# - classic 12 h dtg
#

sub dtg12 {


my ($opt)=$_[0];
my ($year,$chr,$curdtg);

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);

$yr=$year;
$mo=$mon+1;
$dy=$mday;
$mn=$min+1;
$sc=$sec;
$fhr=$hour+1;
$yr=00 if($yr == 100);
$yr=$yr-100 if($yr >= 100);

$phr=$hour%12;
$hr=int($hour/12)*12;

$hour00=sprintf("%02d",$hour) ;
$hr00=sprintf("%02d",$hr) ;
$mo00=sprintf("%02d",$mo) ;
$dy00=sprintf("%02d",$dy) ;
$mn00=sprintf("%02d",$mn) ;
$sc00=sprintf("%02d",$sc) ;
$yr00=sprintf("%02d",$yr) ;

if($opt eq 'ph') {
  $curdtg=sprintf("%02d%02d%02d%02d %02d\:%02d",$yr,$mo,$dy,$hr,$phr,$mn);
} elsif($opt eq 'time') {
  $curdtg="$hour00\:$mn00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'timesec') {
  $curdtg="$hour00\:$mn00\:$sc00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'watchtime') {
  $curdtg="$hr00\:00 UTC $dy $mname{$mo00}, ${century}${yr00}" ;
} elsif($opt eq 'full' || $opt eq 'dtg4') {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$hr);
} elsif($opt eq 'fullhm') {
  $curdtg=sprintf("%02d%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$fhr,$mn);
} elsif($opt eq 'fullph') {
  $curdtg=sprintf("%02%02d%02d%02d%02d +%02d\:%02d",$century,$yr,$mo,$dy,$hr,$phr,$mn);
} elsif($opt eq 'eccurdtg') {
#$yr=98;$mo=4;$dy=5;$fhr=3;  ecmwf DTG change calculator assumig 12Z run comes in +15Z
  $curdtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$fhr);
  $curdtg=dtginc($curdtg,-27);
  $curdtg=substr($curdtg,0,6).'12';
} elsif($opt eq 'eccurdtg4') {
#$yr=98;$mo=4;$dy=5;$fhr=3;  ecmwf DTG change calculator assumig 12Z run comes in +15Z
  $curdtg=sprintf("%02d%02d%02d%02d",$yr,$mo,$dy,$fhr);
  $curdtg=dtginc($curdtg,-27);
  $curdtg=$century.substr($curdtg,0,6).'12';
} else {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$hr);
}
return $curdtg;

}

sub localdtg {
local $opt=$_[0];
local $year;

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
my ($yr,$mo,$dy,$mn,$sc,$fhr,$phr,$hr);
my ($hour00,$hr00,$mo00,$dy00,$mn00,$sc00);
my ($curdtg);

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

 $yr=$year;
 $yr=00 if($yr == 100);
 $yr=$yr-100 if($yr > 100);
 $yr=sprintf("%02d",$yr) ;

$mo=$mon+1;
$dy=$mday;
$mn=$min+1;
$sc=$sec;
$fhr=$hour;
$phr=$hour%12;
$hr=int($hour/12)*12;

$hour00=sprintf("%02d",$hour) ;
$hr00=sprintf("%02d",$hr) ;
$mo00=sprintf("%02d",$mo) ;
$dy00=sprintf("%02d",$dy) ;
$mn00=sprintf("%02d",$mn) ;
$sc00=sprintf("%02d",$sc) ;

if($opt eq "time") {
  $curdtg="$hour00\:$mn00 Local $dy $mname{$mo00}, 20$yr" ;
} elsif($opt eq "timesec") {
  $curdtg="$hour00\:$mn00\:$sc00 HST $dy $mname{$mo00}, 20$yr" ;
} elsif($opt eq "watchtime") {
  $curdtg="$hr00\:00 Local $dy $mname{$mo00}, 20$yr" ;
} elsif($opt eq "full") {
  $curdtg=sprintf("20%02d%02d%02d%02d",$yr,$mo,$dy,$hr);
} elsif($opt eq "fullhm") {
  $curdtg=sprintf("%02d%02d%02d%02d %02d:%02d",$century,$yr,$mo,$dy,$fhr,$mn);
} else {
  $curdtg=sprintf("%02d%02d%02d%02d%02d",$century,$yr,$mo,$dy,$fhr);
}
return $curdtg;

}

sub dtg2time {
local $dtg=$_[0];
my($yr,$mo,$dy,$hr,$yyyy);

if(length($dtg) == 10) {
  $yyyy=substr($dtg,0,4);
  $mo=substr($dtg,4,2)*1;
  $dy=substr($dtg,6,2)*1;
  $hr=substr($dtg,8,2);
} else {
  $ct='20';
  $yr=substr($dtg,0,2)*1;
  $mo=substr($dtg,2,2)*1;
  $dy=substr($dtg,4,2)*1;
  $hr=substr($dtg,6,2);
  $yyyy=$ct.$yr;
}

$curdtg="$hr:00 UTC $dy $mname{$mo},$yyyy" ;
return $curdtg;

}

sub dtg2gtime {
my($dtg)=$_[0];
my($yr,$mo,$dy,$hr,$yyyy);

if(length($dtg) == 10) {
  $yyyy=substr($dtg,0,4);
  $mo=substr($dtg,4,2);
  $dy=substr($dtg,6,2)*1;
  $hr=substr($dtg,8,2)*1;
} else {
  $ct='20';
  $yr=substr($dtg,0,2);
  $mo=substr($dtg,2,2);
  $dy=substr($dtg,4,2)*1;
  $hr=substr($dtg,6,2)*1;
  $yyyy=$ct.$yr;
}

$monname=substr($mname{$mo},0,3);
$gtime="${hr}Z${dy}${monname}${yyyy}" ;
return $gtime;

}

sub ecp{
  my(@d)=@_;
  my($r,@rc);
  @rc=`set noglob ; $ENV{"ECFS_SYS_PATH"}/ecp.p @d`;
  if($? ne 0) {
    print "ECP error for \"@d\"\n"; 
    foreach $r (@rc) {
      chomp($r);
      print "ECP output: $r\n";
    }
    return(1);
  } else {
    foreach $r (@rc) {
      chomp($r);
      print "ECP output: $r\n";
    }
    return(0);
  }
}

sub els{
  my(@d)=@_;
  my($r,@rc);
  @rc=`$ENV{"ECFS_SYS_PATH"}/els.p @d`;
  foreach $r (@rc) {
    chomp($r);
    print "ELS output: $r\n";
  }
}

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

sub yyyymminc{

  ($yyyymm)=@_;

  my($yyyy,$mm);
  $yyyy=substr($yyyymm,0,4);
  $mm=substr($yyyymm,4,2)*1;
  $mm++;
  if($mm > 12) {
    $yyyy++;
      $mm=1;
  }
    
  $yyyymm=sprintf("%04d%02d",$yyyy,$mm);

}


sub dtgdiff($bdtg,$edtg) {

  my($bdtg,$edtg)=@_;
  my($t1,$t2,$dt);

  $t1=dtg2timesec($bdtg);
  $t2=dtg2timesec($edtg);
  if($t1 < 0 || $t2 < 0) {
    return(1e20);
  } else {
    $dt=($t2-$t1)/3600.0;
  }

  return($dt);

}

sub dtg2timesec($idtg) {

  use Time::Local;

  my($idtg)=@_;
  my($yr,$mo,$dy,$hr,$min,$sec,$time);
  

  $yr=substr($idtg,0,4)*1;
  $mo=substr($idtg,4,2)*1;
  $dy=substr($idtg,6,2)*1;
  $hr=substr($idtg,8,2)*1;
  $min=0;
  $sec=0;
#
# C struc tm ; a bug before! worked in dtgdiff only for short shifts
#
  $mo=$mo-1;

  if($yr < 1973 || $yr > 2038) {
    return(-1.0);
  }

  $time=timelocal($sec,$min,$hr,$dy,$mo,$yr);

  return($time);

}


1;

