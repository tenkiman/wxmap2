#!/usr/bin/env perl
#   makes a GrADS control file for grib files
#
#   requires wgrib and Perl5
#
#   usage: grib2ctl [options] [grib file] [optional index file] >[control file]
#
#   note: this script does not make the index file .. you have to run gribmap
#
#   Analyses: (using initial time)
#
#      $ grib2ctl.pl example.grib >example.ctl
#      $ gribmap -i example.ctl -0
#
#   Forecasts: (using verifiation time)
#
#      $ grib2ctl.pl -verf example.grib >example.ctl
#      $ gribmap -i example.ctl
#
#   bugs:
#         many
#	  will fail under number of situations
#         finite number of NCEP grids are supported
#
# requires wgrib 1.6.0 or higher 
# wesley ebisuzaki, http://wesley.wwb.noaa.gov/grib2ctl.html

$version="0.9.12.5p16";

$verb=0;
$wflag="";
$file="";
$index="";
$prs="prs";
$suffix="no";
$suffix="";
$z_order="prs";

foreach $_ (@ARGV) {
   SWITCH: {
      /^-verf/ && do { $wflag="$wflag -verf" ; last SWITCH; };
      /^-ncep_opn/ && do { $wflag="$wflag -ncep_opn" ; last SWITCH; };
      /^-ncep_rean/ && do { $wflag="$wflag -ncep_rean" ; last SWITCH; };
      /^-no_prs/ && do { $prs="" ; last SWITCH; };
      /^-no_suffix/ && do { $suffix="no" ; last SWITCH; };
      /^-rev_z/ && do { $z_order="theta"; last SWITCH; };
      /^-/ && do { print STDERR "unknown option: $_\n"; exit 8; };
      if ($file eq "") {
         $file="$_";
      }
      else {
         $index="$_";
      }
   }
}

if ("$file" eq "") {
   if ($#ARGV >= 0) {
      print STDERR "*** missing grib file ***\n\n\n";
   }
   print STDERR "$0 $version  wesley ebisuzaki\n";
   print STDERR " makes a Grads control file for grib files\n";
   print STDERR " usage: $0 [options] [grib file] [optional index file] >[ctl file]\n";
   print STDERR " -ncep_opn       .. use NCEP opn grib table for T62 NCEP fields\n";
   print STDERR " -ncep_rean      .. use NCEP reanalysis grib table for T62 NCEP fields\n";
   print STDERR " -verf           .. use forecast verification times\n";
   print STDERR " -no_prs         .. no prs suffix on variable name\n";
   print STDERR " -no_suffix      .. no suffix on variable name\n";
   print STDERR " -rev_z          .. for reversed vertical coordinates like theta\n";
   exit 8;
}

if (-d "/tmp") {
   $ListA="/tmp/g$$.tmp";
   $TmpFile="/dev/null";
   unlink $ListA;
   $sys="unix";
}
else {
   $ListA="c:\\g$$.tmp";
   $TmpFile="c:\\h$$.tmp";
   unlink ($ListA, $TmpFile);
   $sys="win";
}

# inventory of All records

system "wgrib $wflag -v $file >$ListA";

if ( ! -s $ListA ) {
    print STDERR "Big problem:\n";
    print STDERR "  either $file is missing or not a grib file\n";
    print STDERR "  or wgrib is not on your path\n";
    exit 8;
}

# make table of dates and variables

open (FileDate, "<$ListA");
while (defined($_ = <FileDate>)) {

   # date table

   $_ =~ s/^.*D=//;
   $d=substr($_, 0, 10);
   $dates{$d}="";

   # variable/level list
   @Fld = split(':', $_, 99);
   $kpds=substr($Fld[3],5);
   ($kpds5,$kpds6,$kpds7) = split(/,/,$kpds);
   $varname = "$Fld[1]:$kpds6";
   if (defined $flevels{$varname}) {
      if (!($flevels{$varname} =~ / $kpds7 /)) {
         $flevels{$varname} .= "$kpds7 ";
      }
   }
   else {
      $flevels{$varname} = " $kpds7 ";
      $fcomments{$varname} = "$kpds5:$Fld[$#Fld]";
   }
}
close (FileDate);
@sdates=sort keys(%dates);

$ntime=$#sdates + 1;
$time=$sdates[0];
$year = substr($time,0,4);
$mo = substr($time,4,2);
$day = substr($time,6,2);
$hour = substr($time,8,2);
$month=substr("janfebmaraprmayjunjulaugsepoctnovdec",$mo*3-3,3);

if ($ntime > 1) {
    $year1 = substr($sdates[1],0,4);
    $mo1 = substr($sdates[1],4,2);
    $day1 = substr($sdates[1],6,2);
    $hour1 = substr($sdates[1],8,2);
}

# ---------------intro------------------------------------

if ("$index" eq "" ) {$index="$file.idx";}
if ($sys eq "unix") {
   $caret1 = (substr($file,0,1) eq "/") ? "" : '^';
   $caret2 = (substr($index,0,1) eq "/") ? "" : '^';
}
else {
   $caret1 = (substr($file,1,1) eq ":") ? "" : '^';
   $caret2 = (substr($index,1,1) eq ":") ? "" : '^';
}
print "dset $caret1$file\nindex $caret2$index\n";
print "undef 9.999E+20\ntitle $file\n*  produced by grib2ctl v$version\n";

# ------------------- grid -----------------------
$griddef=`wgrib $wflag -V $file -d 1 -o $TmpFile`;
($grid = $griddef) =~ s/^.*grid=//;
$grid =~ s/ .*//s;

# ------------------- center number -----------------------

@tt=split(' ',$griddef);

for($i=0;$i<=$#tt;$i++) {
  if($tt[$i] eq 'center') {
    $CenterNumber=$tt[$i+1]*1;
    last;
  }
}

# ---------------- if FNMOC (58) disable grid setting by grid number ----

print "CCC $CenterNumber\n" if($verb);

if($CenterNumber == 58) {
  $grid=255;
}

if ($grid != 29 && $grid != 30 && $grid != 33 && $grid != 34 
	&& $grid != 85 && $grid != 86 && $grid != 255) {
    print "options yrev\n";
}
print "dtype grib $grid\n";

if ($grid == 2) {
   # 2.5 x 2.5 lola
   print "xdef 144 linear   0  2.5\n";
   print "ydef  73 linear -90  2.5\n";
}
elsif ($grid == 3) {
   # 1 x 1 lola
   print "xdef 360 linear   0 1\n";
   print "ydef 181 linear -90 1\n";
}
elsif ($grid == 5) {
   print "pdef 53 57 nps 27 49 -105 190.5\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 6) {
   print "pdef 53 45 nps 27 49 -105 190.5\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 29) {
   print "xdef 145 linear 0 2.5\n";
   print "ydef 37  linear 0 2.5\n";
}
elsif ($grid == 30) {
   print "xdef 145 linear   0 2.5\n";
   print "ydef  37 linear -90 2.5\n";
}
elsif ($grid == 33) {
   print "xdef 181 linear 0 2\n";
   print "ydef 46 linear  0 2\n";
}
elsif ($grid == 34) {
   print "xdef 181 linear   0 2\n";
   print "ydef  46 linear -90 2\n";
}
elsif ($grid == 85) {
   print "xdef 360 linear 0.5 1\n";
   print "ydef  90 linear 0.5 1\n";
}
elsif ($grid == 86) {
   print "xdef 360 linear   0.5 1\n";
   print "ydef 90 linear  -89.5 1\n";
}
elsif ($grid == 98) {
   # 192x94 gaussian grid
   print "xdef 192 linear  0 1.875\n";
   print "ydef  94 levels\n";
   print "-88.542 -86.653 -84.753 -82.851 -80.947 -79.043 -77.139 -75.235 -73.331 -71.426\n";
   print "-69.522 -67.617 -65.713 -63.808 -61.903 -59.999 -58.094 -56.189 -54.285 -52.380\n";
   print "-50.475 -48.571 -46.666 -44.761 -42.856 -40.952 -39.047 -37.142 -35.238 -33.333\n";
   print "-31.428 -29.523 -27.619 -25.714 -23.809 -21.904 -20.000 -18.095 -16.190 -14.286\n";
   print "-12.381 -10.476  -8.571  -6.667  -4.762  -2.857  -0.952   0.952   2.857   4.762\n";
   print "  6.667   8.571  10.476  12.381  14.286  16.190  18.095  20.000  21.904  23.809\n";
   print " 25.714  27.619  29.523  31.428  33.333  35.238  37.142  39.047  40.952  42.856\n";
   print " 44.761  46.666  48.571  50.475  52.380  54.285  56.189  58.094  59.999  61.903\n";
   print " 63.808  65.713  67.617  69.522  71.426  73.331  75.235  77.139  79.043  80.947\n";
   print " 82.851  84.753  86.653  88.542\n";
}
elsif ($grid == 87) {
   print "pdef 81 62 nps 31.9 112.53 -105 68.513\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 101) {
   print "pdef 113 91 nps 58.5 92.5 -105 91.452\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 104) {
   print "pdef 147 110 nps 75.5 109.5 -105 90.75464\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 105) {
   print "pdef 83 83 nps 40.5 88.5  -105 90.75464\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 106) {
   print "pdef 165 117 nps 80 176 -105 45.37732\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 107) {
   print "pdef 120 92 nps 46 167  -105 45.37732\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 211) {
   # awips labert conformal;
   print "pdef 93 65 lcc 12.19 -133.459 1 1 25 25 -95 81270.5 81270.5\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 212) {
   # awips labert conformal;
   print "pdef 185 129 lcc 35.0 -95.0 105 49 25 25 -95 40635 40635\n";
   print "xdef 181 linear 220 0.5\n";
   print "ydef  91 linear  15 0.5\n";
}
elsif ($grid == 216) {
   print "pdef 147 110 nps 75.5 109.5 -105 91.452\n";
   print "xdef 181 linear -180 1\n";
   print "ydef 91 linear 0 1\n";
}
elsif ($grid == 218) {
   # awips labert conformal;
   print "pdef 737 513 lcc 12.19 -133.459 1 1 25 25 -95 10.159 10.159\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 240) {
   # nps usa
   print "pdef 1160 880 nps 441 1601 255 4.763\n";
   print "xdef 801 linear -130 0.1\n";
   print "ydef 401 linear 20 0.1\n";
}
elsif ($grid == 241) {
   print "pdef 386 293 nps 147.315 534.0 -105 14.2875\n";
   print "xdef 161 linear -140 0.5\n";
   print "ydef 81 linear 20 0.5\n";
}
elsif ($grid == 126) {
   # 384x190 gaussian grid;
   print "xdef 384 linear 0 0.9375\n";
   print "ydef 190 levels\n";
   print "-89.277 -88.340 -87.397 -86.454 -85.509 -84.565 -83.620 -82.676 -81.731 -80.786\n";
   print "-79.841 -78.897 -77.952 -77.007 -76.062 -75.117 -74.173 -73.228 -72.283 -71.338\n";
   print "-70.393 -69.448 -68.503 -67.559 -66.614 -65.669 -64.724 -63.779 -62.834 -61.889\n";
   print "-60.945 -60.000 -59.055 -58.110 -57.165 -56.220 -55.275 -54.330 -53.386 -52.441\n";
   print "-51.496 -50.551 -49.606 -48.661 -47.716 -46.771 -45.827 -44.882 -43.937 -42.992\n";
   print "-42.047 -41.102 -40.157 -39.212 -38.268 -37.323 -36.378 -35.433 -34.488 -33.543\n";
   print "-32.598 -31.653 -30.709 -29.764 -28.819 -27.874 -26.929 -25.984 -25.039 -24.094\n";
   print "-23.150 -22.205 -21.260 -20.315 -19.370 -18.425 -17.480 -16.535 -15.590 -14.646\n";
   print "-13.701 -12.756 -11.811 -10.866  -9.921  -8.976  -8.031  -7.087  -6.142  -5.197\n";
   print " -4.252  -3.307  -2.362  -1.417  -0.472   0.472   1.417   2.362   3.307   4.252\n";
   print "  5.197   6.142   7.087   8.031   8.976   9.921  10.866  11.811  12.756  13.701\n";
   print " 14.646  15.590  16.535  17.480  18.425  19.370  20.315  21.260  22.205  23.150\n";
   print " 24.094  25.039  25.984  26.929  27.874  28.819  29.764  30.709  31.653  32.598\n";
   print " 33.543  34.488  35.433  36.378  37.323  38.268  39.212  40.157  41.102  42.047\n";
   print " 42.992  43.937  44.882  45.827  46.771  47.716  48.661  49.606  50.551  51.496\n";
   print " 52.441  53.386  54.330  55.275  56.220  57.165  58.110  59.055  60.000  60.945\n";
   print " 61.889  62.834  63.779  64.724  65.669  66.614  67.559  68.503  69.448  70.393\n";
   print " 71.338  72.283  73.228  74.173  75.117  76.062  77.007  77.952  78.897  79.841\n";
   print " 80.786  81.731  82.676  83.620  84.565  85.509  86.454  87.397  88.340  89.277\n";
}
elsif ($grid == 255) {
   # user defined grid
   # very simplistic

   $_ = $griddef;
   GRD: {
      / latlon: / && do {
         / lat  (\S*) to (\S*) by (\S*) /;
         $lat0=$1;
         $lat1=$2;
         $dlat=$3;

         / long (\S*) to (\S*) by (\S*), \((\S*) x (\S*)\)/;
         $lon0=$1;
         # $lon1=$2;
         $dlon=$3;
         $nx =$4;
         $ny =$5;

         if ($lat0 > $lat1) {
            print "options yrev\n";
            print "ydef $ny linear $lat1 ", abs($dlat), "\n"
         }
         else {
            print "ydef $ny linear $lat0 ", abs($dlat), "\n"
         }
         print "xdef $nx linear $lon0 $dlon\n";
         last GRD; };

      / polar stereo: Lat1 16.125000 Long1 234.983000 Orient -100.0/ && do {
         print "options yrev\n";
         print "pdef 129 86 nps 64 136 -100 60\n";
         print "xdef 720 linear  0 0.5\n";
         print "ydef 148 linear 16 0.5\n";
	 last GRD; };

      / polar stereo: Lat1 -4.860000 Long1 -122.614000 Orient -80.000000/ && do {
         print "pdef 49 51 nps 24 26 -80 381\n";
         print "xdef 144 linear 0 2.5\n";
         print "ydef 45 linear -20 2.5\n";
         last GRD; };

      / Lambert Conf:.* Lov 265.*\(151 x 113\)/s && do {
         print "options yrev\n";
         print "pdef 151 113 lcc 16.281 233.8622 1 1 25 25 265 40635 40635\n";
         print "xdef 141 linear -130 0.5\n";
         print "ydef 71 linear 20 0.5\n";
         last GRD; };
      / nx 144 ny 73 / && do {
         # 2.5 x 2.5 lola
         print "options yrev\n";
         print "xdef  144 linear   0 2.5\n";
         print "ydef   73 linear -90 2.5\n";
         last GRD; };
      / nx 360 ny 181 / && do {
         # 1 x 1 lola
         print "options yrev\n";
         print "xdef  360 linear   0 1\n";
         print "ydef  181 linear -90 1\n";
         last GRD; };
      / nx 180 ny 91 / && do {
         # 2 x 2 lola;
         print "options yrev\n";
         print 'xdef  180 linear 0 2';
         print 'ydef  91 linear -90 2';
         last GRD; };
      / nx 192 ny 94 / && do {
         # 192x94 gaussian grid
         print "options yrev\n";
         print "xdef 192 linear  0 1.875\n";
         print "ydef  94 levels\n";
         print "-88.542 -86.653 -84.753 -82.851 -80.947 -79.043 -77.139 -75.235 -73.331 -71.426\n";
         print "-69.522 -67.617 -65.713 -63.808 -61.903 -59.999 -58.094 -56.189 -54.285 -52.380\n";
         print "-50.475 -48.571 -46.666 -44.761 -42.856 -40.952 -39.047 -37.142 -35.238 -33.333\n";
         print "-31.428 -29.523 -27.619 -25.714 -23.809 -21.904 -20.000 -18.095 -16.190 -14.286\n";
         print "-12.381 -10.476  -8.571  -6.667  -4.762  -2.857  -0.952   0.952   2.857   4.762\n";
         print "  6.667   8.571  10.476  12.381  14.286  16.190  18.095  20.000  21.904  23.809\n";
         print " 25.714  27.619  29.523  31.428  33.333  35.238  37.142  39.047  40.952  42.856\n";
         print " 44.761  46.666  48.571  50.475  52.380  54.285  56.189  58.094  59.999  61.903\n";
         print " 63.808  65.713  67.617  69.522  71.426  73.331  75.235  77.139  79.043  80.947\n";
         print " 82.851  84.753  86.653  88.542\n";
         last GRD; };
      / nx 320 ny 160 / && do {
         # 320x160 gaussian grid;
         print "options yrev\n";
         print "xdef 320 linear 0 1.125\n";
         print "ydef 160 levels\n";
         print "-89.142 -88.029 -86.911 -85.791 -84.670 -83.549 -82.428 -81.307 -80.185 -79.064\n";
         print "-77.943 -76.821 -75.700 -74.578 -73.457 -72.336 -71.214 -70.093 -68.971 -67.850\n";
         print "-66.728 -65.607 -64.485 -63.364 -62.242 -61.121 -60.000 -58.878 -57.757 -56.635\n";
         print "-55.514 -54.392 -53.271 -52.149 -51.028 -49.906 -48.785 -47.663 -46.542 -45.420\n";
         print "-44.299 -43.177 -42.056 -40.934 -39.813 -38.691 -37.570 -36.448 -35.327 -34.205\n";
         print "-33.084 -31.962 -30.841 -29.719 -28.598 -27.476 -26.355 -25.234 -24.112 -22.991\n";
         print "-21.869 -20.748 -19.626 -18.505 -17.383 -16.262 -15.140 -14.019 -12.897 -11.776\n";
         print "-10.654  -9.533  -8.411  -7.290  -6.168  -5.047  -3.925  -2.804  -1.682  -0.561\n";
         print "  0.561   1.682   2.804   3.925   5.047   6.168   7.290   8.411   9.533  10.654\n";
         print " 11.776  12.897  14.019  15.140  16.262  17.383  18.505  19.626  20.748  21.869\n";
         print " 22.991  24.112  25.234  26.355  27.476  28.598  29.719  30.841  31.962  33.084\n";
         print " 34.205  35.327  36.448  37.570  38.691  39.813  40.934  42.056  43.177  44.299\n";
         print " 45.420  46.542  47.663  48.785  49.906  51.028  52.149  53.271  54.392  55.514\n";
         print " 56.635  57.757  58.878  60.000  61.121  62.242  63.364  64.485  65.607  66.728\n";
         print " 67.850  68.971  70.093  71.214  72.336  73.457  74.578  75.700  76.821  77.943\n";
         print " 79.064  80.185  81.307  82.428  83.549  84.670  85.791  86.911  88.029  89.142\n";
         last GRD; };
      / nx 640 ny 320 / && do {

# T319(N160)  gaussian grid;
         print "options yrev\n";
$xdef="xdef  640 linear 0 0.5625";
$ydef="ydef  320 levels
 -89.57009 -89.01318 -88.45297 -87.89203 -87.33080 -86.76944 -86.20800 -85.64651
 -85.08499 -84.52345 -83.96190 -83.40034 -82.83876 -82.27718 -81.71559 -81.15400
 -80.59241 -80.03081 -79.46921 -78.90760 -78.34599 -77.78439 -77.22279 -76.66117
 -76.09956 -75.53795 -74.97634 -74.41473 -73.85311 -73.29150 -72.72989 -72.16827
 -71.60666 -71.04504 -70.48342 -69.92181 -69.36019 -68.79858 -68.23695 -67.67534
 -67.11372 -66.55210 -65.99049 -65.42886 -64.86725 -64.30563 -63.74401 -63.18239
 -62.62077 -62.05915 -61.49753 -60.93591 -60.37429 -59.81268 -59.25105 -58.68943
 -58.12782 -57.56620 -57.00457 -56.44296 -55.88133 -55.31971 -54.75809 -54.19647
 -53.63485 -53.07323 -52.51161 -51.94999 -51.38837 -50.82675 -50.26513 -49.70351
 -49.14189 -48.58027 -48.01865 -47.45702 -46.89540 -46.33378 -45.77216 -45.21054
 -44.64892 -44.08730 -43.52568 -42.96406 -42.40244 -41.84081 -41.27919 -40.71757
 -40.15595 -39.59433 -39.03271 -38.47108 -37.90947 -37.34784 -36.78622 -36.22460
 -35.66298 -35.10136 -34.53974 -33.97812 -33.41649 -32.85487 -32.29325 -31.73163
 -31.17001 -30.60839 -30.04676 -29.48514 -28.92352 -28.36190 -27.80028 -27.23866
 -26.67704 -26.11541 -25.55379 -24.99217 -24.43055 -23.86893 -23.30731 -22.74568
 -22.18406 -21.62244 -21.06082 -20.49920 -19.93758 -19.37595 -18.81433 -18.25271
 -17.69109 -17.12947 -16.56785 -16.00622 -15.44460 -14.88298 -14.32136 -13.75974
 -13.19812 -12.63649 -12.07487 -11.51325 -10.95163 -10.39001  -9.82839  -9.26676
  -8.70514  -8.14352  -7.58190  -7.02028  -6.45865  -5.89703  -5.33541  -4.77379
  -4.21217  -3.65055  -3.08892  -2.52730  -1.96568  -1.40406  -0.84244  -0.28082
   0.28081   0.84243   1.40405   1.96567   2.52729   3.08891   3.65054   4.21216
   4.77378   5.33540   5.89702   6.45865   7.02027   7.58189   8.14351   8.70513
   9.26675   9.82838  10.39000  10.95162  11.51324  12.07486  12.63648  13.19811
  13.75973  14.32135  14.88297  15.44459  16.00621  16.56784  17.12946  17.69108
  18.25270  18.81432  19.37594  19.93757  20.49919  21.06081  21.62243  22.18405
  22.74567  23.30730  23.86892  24.43054  24.99216  25.55378  26.11540  26.67702
  27.23865  27.80027  28.36189  28.92351  29.48513  30.04675  30.60838  31.17000
  31.73162  32.29324  32.85486  33.41648  33.97810  34.53973  35.10135  35.66297
  36.22459  36.78621  37.34784  37.90945  38.47108  39.03270  39.59432  40.15594
  40.71756  41.27918  41.84081  42.40242  42.96405  43.52567  44.08729  44.64891
  45.21053  45.77215  46.33377  46.89539  47.45702  48.01863  48.58026  49.14188
  49.70350  50.26512  50.82674  51.38836  51.94998  52.51160  53.07322  53.63484
  54.19646  54.75808  55.31970  55.88132  56.44294  57.00457  57.56618  58.12780
  58.68943  59.25105  59.81266  60.37428  60.93591  61.49752  62.05914  62.62076
  63.18238  63.74400  64.30562  64.86724  65.42886  65.99047  66.55209  67.11371
  67.67533  68.23695  68.79856  69.36018  69.92180  70.48341  71.04503  71.60664
  72.16826  72.72987  73.29149  73.85310  74.41472  74.97633  75.53794  76.09956
  76.66116  77.22277  77.78438  78.34599  78.90759  79.46919  80.03079  80.59239
  81.15399  81.71558  82.27717  82.83875  83.40032  83.96189  84.52345  85.08498
  85.64650  86.20798  86.76942  87.33079  87.89202  88.45296  89.01317  89.57008";
print "$xdef\n";
print "$ydef\n";
         last GRD; };
      print STDERR "*** script needs to be modified ***\n";
      print STDERR "unknown user-defined grid\n";
    }
}
else {
   print STDERR "*** script needs to be modified ***\n";
   print STDERR "unimplimented grid type: $grid\n";
}


# make the tdef statement

&tdef;

# ------------------var-------------------------------------;

%tails =(
   '1' => 'sfc',
   '2' => 'clb',
   '3' => 'clt',
   '4' => 'zdg',
   '5' => 'lcl',
   '6' => 'mwl',
   '7' => 'trp',
   '8' => 'toa',
   '9' => 'bos',
   '10' => 'clm',
   '12' => 'lcb',
   '13' => 'lct',
   '14' => 'loc',
   '22' => 'mcb',
   '23' => 'mct',
   '24' => 'mdc',
   '32' => 'hcb',
   '33' => 'hct',
   '34' => 'hic',
   '100' => 'prs',
   '101' => 'plr',
   '102' => 'msl',
   '103' => 'hml',
   '104' => 'zlr',
   '105' => 'hag',
   '106' => 'hlr',
   '107' => 'sig',
   '108' => 'slr',
   '109' => 'hbl',
   '110' => 'blr',
   '111' => 'dpl',
   '112' => 'dlr',
   '113' => 'tht',
   '114' => 'tlr',
   '116' => 'plg',
   '121' => 'plr',
   '128' => 'slr',
   '141' => 'plr',
   '160' => 'dsl',
   '200' => 'clm',
   '212' => 'lcb',
   '213' => 'lct',
   '214' => 'lcl',
   '222' => 'mcb',
   '223' => 'mct',
   '224' => 'mcl',
   '232' => 'hcb',
   '233' => 'hct',
   '234' => 'hcl',
   );
$tails{'100'} = "$prs";

$nlevelmax=0;
$levelsmax=0;

$nvar=0;
foreach $fname (sort keys(%flevels)) {
   ($name, $kpds6) = split(/:/, $fname);
   ($kpds5, $comment) = split(/:/, $fcomments{$fname});
   $comment = substr($comment,1);

   #
   # find number of levels
   #

   $_=$flevels{$fname};
   $nlev = (tr/ / /) - 1;
   $kpds7s = $_;

   $name =~ tr/_-//d;
   $tail = $suffix eq 'no' ? "" : $tails{$kpds6};

   # tranlate special levels

   if ($kpds6 == 103 && ($kpds7s =~ s/ 1829 / /)) {
      $var_line[$nvar++]="${name}1829m  0 $kpds5,$kpds6,1829 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 103 && ($kpds7s =~ s/ 2743 / /)) {
      $var_line[$nvar++]="${name}2743m  0 $kpds5,$kpds6,2743 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 103 && ($kpds7s =~ s/ 3658 / /)) {
      $var_line[$nvar++]="${name}3658m  0 $kpds5,$kpds6,3658 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 105 && ($kpds7s =~ s/ 2 / /)) {
      $var_line[$nvar++]="${name}2m  0 $kpds5,$kpds6,2 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 105 && ($kpds7s =~ s/ 10 / /)) {
      $var_line[$nvar++]="${name}10m  0 $kpds5,$kpds6,10 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 107 && ($kpds7s =~ s/ 9950 / /) && $nlev < 5) {
      $var_line[$nvar++]="${name}sig995  0 $kpds5,$kpds6,9950 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 111 && ($kpds7s =~ s/ 300 / /)) {
      $var_line[$nvar++]="${name}SoilB  0 $kpds5,$kpds6,300 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 112 && ($kpds7s =~ s/ 10 / /)) {
      $var_line[$nvar++]="${name}SoilT  0 $kpds5,$kpds6,10 ** $comment";
      $nlev--;
   }
   if ($kpds6 == 112 && ($kpds7s =~ s/ 2760 / /)) {
      $var_line[$nvar++]="${name}SoilM  0 $kpds5,$kpds6,2760 ** $comment";
      $nlev--;
   }


   if ($nlev == 1) {
      $kpds7s =~ s/^ //;
      $var_line[$nvar++]="$name$tail  0 $kpds5,$kpds6,$kpds7s ** $comment";
   }
   elsif ($nlev > 1) {
      $var_line[$nvar++]="$name$tail $nlev $kpds5,$kpds6,0 ** $comment";
      if ($nlev > $nlevelmax) {
         $nlevelmax=$nlev;
         $levelsmax=$flevels{$fname};
      }
   }
}

#------------------levels-------------------------;

if ($nlevelmax == 0) {
   print "zdef 1 linear 1 1\n";
}
else {

   ($_ = $levelsmax) =~ s/.//;
   chop($_);

   if ($z_order eq "theta") {
      @levels=sort {$a <=> $b} split(/ /,$_);
   }
   else {
      @levels=sort {$b <=> $a} split(/ /,$_);
   }

   print "zdef $nlevelmax levels\n";
   for ($i = 0; $i < $nlevelmax; $i++) {
      print "$levels[$i] ";
   }
   print "\n";
}

print "vars $nvar\n";
for ($i = 0; $i < $nvar; $i++) {
   print $var_line[$i];
}
print "ENDVARS\n";

if ($sys eq "win") {
   unlink $TmpFile;
}
unlink $ListA;
exit 0;

#------------------ jday --------------------
# jday(year,mo,day) return the julian day relative to jan 0
# mo=1..12
#
sub jday {

   local($n);
   $n=substr(" 000 031 059 090 120 151 181 212 243 273 304 334",($_[1]-1)*4,4);
   $n = $n + $_[2];

   if ($_[1] > 2 && $_[0] % 4 == 0) {
      if ($_[0] % 400 == 0 || $_[0] % 100 != 0) {
         $n++;
      }
   }
   $n;
}


#------------------ write tdef statement ------------------
# still not great but better than before

sub tdef {

   local($tmp);
   $dt="1mo";
   if ($ntime == 1) {
      $dt="1mo";
   }
   elsif ($hour != $hour1) {
      # assume that dt < 24 hours
      $tmp=$hour1-$hour;
      ($tmp < 0) && do {$tmp = $tmp + 24};
      $dt="${tmp}hr";
   }
   elsif ($day != $day1) {
      # assume that dt < 365 days
      $tmp = &jday($year1,$mo1,$day1) - &jday($year,$mo,$day);
      ($tmp < 0) && do {$tmp = $tmp + &jday($year,12,31)};
      $dt="${tmp}dy";
   }
   elsif ($mo != $mo1) {
      # assume that dt < 12 months
      $tmp = $mo1 - $mo;
      ($tmp < 0) && do {$tmp = $tmp + 12};
      $dt="${tmp}mo";
   }
   else {
      $tmp = $year1 - $year;
      $dt="${tmp}yr";
   }
   print "tdef $ntime linear ${hour}Z$day$month$year $dt\n";
}
