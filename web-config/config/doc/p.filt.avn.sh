#!/bin/sh
#
#	check of the data file is there
#
shdir="/export/sgi80/wd20mf/grib/wgrib/avn"
addir="/export/sgi80/wd20mf/grib/wgrib/avn/alldone"
xdir="/export/sgi80/wd20mf/bin"
tsleep=300
maxnsleep=60
tsleepftp=60
maxnsleepftp=120
dorsh="n"

if [ $1 = "current" ] ; then
  dtg=`$shdir/dtg.sh`
else 
  dtg=$1
fi

yy=`echo $dtg | awk '{ print substr($1,1,2) }'`
mm=`echo $dtg | awk '{ print substr($1,3,2) }'`
dd=`echo $dtg | awk '{ print substr($1,5,2) }'`
hh=`echo $dtg | awk '{ print substr($1,7,2) }'`

model=$2
dolist=$3
doftp=$4
ftponly=n

vars="zg ua va ta wa hur psl uas vas tas pr"


ddir="/cray3_com/$model/PROD/$model.$yy$mm$dd/"
if [ $model = "avn" ] ; then 
  mname="gblav"
fi

if [ $model = "mrf" -o $model = "mrflrf" ] ; then 
  mname="drfmr"
  ddir="/cray3_com/mrf/PROD/mrf.$yy$mm$dd/"
fi

if [ $model = "ecmwf" ] ; then 
  ddir="/cray3_com/mrf/PROD/$model.$yy$mm$dd/"
  mname="ecmwf"
fi

#
#	model setup
#
#	970619 - experiment with pulling long-range taus -> 2.5 deg at tau=192

if [ $model = "mrf" ] ; then 
  ftau="00 12 24 36 48 60 72 84 96 108 120 132 144 "
  ftau="00 12 24 36 48 60 72 84 96 108 120 132 144 156 168 180 192 204 216 228 240"
  vars="zg ua va ta wa hur psl uas vas tas pr tasmax tasmin"
  res=10
  lasttaufile="$ddir${mname}.T${hh}Z.PGrbF144"
  lasttaufile="$ddir${mname}.T${hh}Z.PGrbF240"
elif [ $model = "mrflrf" ] ; then 
  ftau="00 24 48 72 96 120 144 168 192 216 240"
  ftau="00 12 24 36 48 60 72 84 96 108 120 132 144 156 168 180 192 204 216 228 240"
  vars="zg ua va ta wa hur psl uas vas tas pr tasmax tasmin"
  res=10
  lasttaufile="$ddir${mname}.T${hh}Z.PGrbF240"
elif [ $model = "avn" ] ; then
  ftau="00 12 24 36 48 60 72"
  res=10
  lasttaufile="$ddir${mname}.T${hh}Z.PGrbF72"
elif [ $model = "ecmwf" ] ; then
  ftau="00 12 24 36 48 60 72 84 96 120 144"
  ftau="00"
  res=25
else
  echo "EEEE invalid model"
  exit 99
fi
#
#	file set ups
#

tlfile=$shdir/tmp.wgrib.$model.lst
tgfile=$shdir/tmp.wgrib.$model.grb
ftpfile=$model.$res.$yy$mm$dd$hh.grb
ofile=$shdir/$ftpfile
ftpdonefile=alldone.$model.$res.$yy$mm$dd$hh
donefile=$shdir/$ftpdonefile

if [ $ftponly != "y" ] ; then
#
#	test to see if the last tau is there
#
echo "last tau file : $lasttaufile"

if [ -s $lasttaufile ] ; then
  echo "LLLLL"
  echo "LLLLL its there `date`"
  echo "LLLLL"
else
  nsleep=1
  while [ ! -s $lasttaufile ] ; do
    echo "LLLLL sleeping for $tsleep sec ... `date`"
    echo "LLLLL sleep iteration = $nsleep"
    sleep $tsleep
    nsleep=`expr $nsleep + 1 `
    if [ $nsleep -gt $maxnsleep ] ; then
      echo "XXXXX sleeping too long, bye"
      exit 69
    fi
  done
fi

echo "SSS $model get for $yy$mm$dd$hh STARTED at `date`" > $donefile

#ftau="72"

if [ $dolist = "y" ] ; then
  for tau in `echo $ftau` ; do
    dfile=$ddir"$mname.T"$hh"Z.PGrbF"$tau

    if [ $model = "ecmwf" ] ; then
      dfile=$ddir"ecmwf.$dtg.ecmgrb"
    fi  

    lfile=$shdir/$model.p.$tau.lst
    echo "creating the list file ($lfile) for $dfile..."
    $xdir/wgrib $dfile > $lfile
  done
fi

rm $ofile
touch $ofile

for tau in `echo $ftau` ; do

  lfile=$shdir/$model.p.$tau.lst
  dfile=$ddir"$mname.T"$hh"Z.PGrbF"$tau
  if [ $model = "ecmwf" ] ; then
    dfile=$ddir"ecmwf.$dtg.ecmgrb"
  fi  

  rm $tlfile $tgfile
  touch $tlfile

  for v in `echo $vars`; do

    case $v
    in
	"zg")
	  kpds5=7
	  kpds6=100
	  kpds7="1000 500"
	  var="HGT"
	;; 
	"ua")
	  kpds5=33
	  kpds6=100
	  kpds7="850 700 500 200"
	  var="UGRD"
	;; 
	"va")
	  kpds5=34
	  kpds6=100
	  kpds7="850 700 500 200"
	  var="VGRD"
	;; 
	"ta")
	  kpds5=11
	  kpds6=100
	  kpds7="850 500"
	  var="TMP"
	;;
	"vrta")
	  kpds5=41
	  kpds6=100
	  kpds7="500"
	  kpds7=""
	  var="ABSV"
	;;
	"uas")
	  kpds5=33
	  kpds6=105
	  kpds7=10
	  var="UGRD"
	;;
	"vas")
	  kpds5=34
	  kpds6=105
	  kpds7=10
	  var="VGRD"
	;;
	"tas")
	  kpds5=11
	  kpds6=105
	  kpds7=2
	  var="TMP"
	;;
	"pr")
	  kpds5=61
	  kpds6=1
	  kpds7=0
	  var="APCP"
	;;
	"hur")
	  kpds5=52
	  kpds6=100
	  kpds7="850"
	  var="RH"
	;;
	"wa")
	  kpds5=39
	  kpds6=100
	  kpds7="700"
	  var="VVEL"
	;;
	"psl")
	  kpds5=2
	  kpds6=102
	  kpds7=0
	  var="PRMSL"
	;;
	"tasmax")
	  kpds5=15
	  kpds6=105
	  kpds7=2
	  var="TMAX"
	;;
	"tasmin")
	  kpds5=16
	  kpds6=105
	  kpds7=2
	  var="TMIN"
	;;
    esac

    for lev in `echo $kpds7` ; do
      echo "doing $var at $lev"
      grep "kpds5=$kpds5:kpds6=$kpds6:kpds7=$lev" $lfile >> $tlfile
    done
  done

  echo "extracting the GRIB fields form $dfile"
  cat $tlfile | $xdir/wgrib $dfile -i -grib -o $tgfile
  cat $tgfile  >> $ofile

  rm $tlfile
  rm $tgfile

done

fi

#
#	set up the get and put ftp input files
#

echo "FFF $model get for $yy$mm$dd$hh FINISHED at `date`" 
echo "FFF $model get for $yy$mm$dd$hh FINISHED at `date`" >> $donefile
ftpjob=$shdir/ftp.$model.job
cat > $ftpjob << EOF
verbose
cd /pub/fiorino/ncep
lcd $shdir
pwd
binary
prompt
put $ftpfile
put $ftpdonefile
quit
EOF

if [ $doftp = "y" ] ; then

  nsleep=0
  ftest="Not"

  while [ $ftest = "Not" ] ; do

    echo "TTTTT before ftp"
    ftpstat=`ftp sprite.llnl.gov < $ftpjob`
    ftest=`echo $ftpstat | grep "Not" | awk '{print $1}'`
    echo "TTTTT stat = $? ftest after ftp = fff_${ftset}_fff ftpstat = $ftpstat"

    if [ ${ftest:=OK} = "OK" ] ; then
      echo "TTTTT the ftp worked... `date`"
    else
      echo "LLLLL sleeping for $tsleep sec ... `date`"
      echo "LLLLL sleep iteration = $nsleep"
      sleep $tsleep
      nsleep=`expr $nsleep + 1 `
      if [ $nsleep -gt $maxnsleep ] ; then
        echo "XXXXX sleeping too long, bye"
        exit 99
      fi
    fi

  done

fi

rm $shdir/tmp.*.$model.*
#
#	set up to move to alldone/
#	970118
#
mv $donefile $addir
if [ $dorsh = "y" ] ; then
echo "LLLLL rsh to typhoon and see if it worked....`date`"
#
#	sleep for 10 min to let LLNL take care of things
#
sleep 600
#
#	see what happened before deleteing
#
#there_result=`rsh typhoon.llnl.gov -l fiorino "ls /d1/nwp/dat/$ftpfile"`
#ttest=`grep $ofile $there_result`
echo "LLLLL there_result = $there_result"
echo "LLLLL ttest = $ttest"

if [ ${ttest:=OK} = "OK" ] ; then
  echo "LLLLL LLNL OK ... `date`"
else
  echo "LLLLLLLLL PROBLEM at LLNL `date`"
fi
#
#	everything OK do the rm
#
fi
echo "XXXXXXXX before rm"
echo "ofile = $ofile"
rm $ofile
echo "XXXXXXXX after rm"

exit
