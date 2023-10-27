<?php


$pt='';

function dtginc($idtg,$inc) {

  $mday=array(31,28,31,30,31,30,31,31,30,31,30,31);
  $mdayleap=array(31,29,31,30,31,30,31,31,30,31,30,31);
  $aday=array(1,32,60,91,121,152,182,213,244,274,305,335);
  $adayleap=array(1,32,61,92,122,153,183,214,245,275,306,336);
  
  $ndyyr=365;
  $bleap=0;

  $yr=substr($idtg,0,4)*1;
  $mo=substr($idtg,4,2)*1;
  $dy=substr($idtg,6,2)*1;
  $hr=substr($idtg,8,2)*1;
  
  $hr=$hr+$inc;
  if($yr%4==0) $bleap=1;
  
  if($bleap) $ndyyr=366;
 

  $jdy=$dy-1;
  if($bleap) {
    $jdy=$jdy+$adayleap[$mo-1];
  } else {
    $jdy=$jdy+$aday[$mo-1];
  }

#print "start jdy = $mo $jdy $hr\n";

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
    if($yr%4==0) $leap=1;
    //if($bleap == 1 && $leap == 0) $leap=1;
    $ndyyr=365;
    if($leap) $ndyyr=366;
    $jdy=$jdy+$ndyyr;
  }

  if($jdy > $ndyyr) {
    $jdy-=$ndyyr;
    $yr++;
    $leap=0;
    if($yr%4==0) $leap=1;
    $ndyyr=365;
    if($leap) $ndyyr=366;
  }
  
#print"yyy $jdy $yr\n";

  $leap=0;
  if($yr%4==0) $leap=1;

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
  
  $ndtg=sprintf("%04d%02d%02d%02d",$yr,$mo,$dy,$hr);
  
  return($ndtg);

}


function uniq($list) {
  sort($list);
  $olist=array();
  $mnew="${list[0]}ASDFASDFASDF";
  foreach ($list as $m) {
    if($m != $mnew) {
      array_push($olist,$m);
      $mnew=$m;
    }
  }
  return $olist;
}


function pysplit($str,$delimiter) {
  $nw=0;
  $tt=explode($delimiter,$str);
  foreach ($tt as $ww) {
    $lenww=strlen($ww);
    if($lenww > 0) {
      $list[$nw]=$ww;
      $nw++;
    }
  }

  return $list;
}

function getplot($model,$dtg,$area,$tau,$plot) {

  $itau=$tau*1;
  $tau=sprintf("%03d",$itau);
  if($model == 'gfs') {
    $path="plt_ncep_$model/$dtg/${model}05.$plot.$tau.$area.png";

  } elseif($model == 'fim' || $model == 'fimx') {
    $path="plt_esrl_$model/$dtg/${model}05.$plot.$tau.$area.png";

  } elseif($model == 'fv3e' || $model == 'fv3g') {
    $path="plt_esrl_$model/$dtg/${model}05.$plot.$tau.$area.png";

  } elseif($model == 'ecmn') {
    $path="plt_ecmwf_ecm/$dtg/${model}10.$plot.$tau.$area.png";

  } elseif($model == 'ecmg') {
    $path="plt_ecmwf_ecmg/$dtg/${model}05.$plot.$tau.$area.png";

  } elseif($model == 'ngp') {
    $path="plt_fnmoc_$model/$dtg/${model}10.$plot.$tau.$area.png";

  } elseif($model == 'ngpc') {
    $path="plt_fnmoc_$model/$dtg/ngp05.$plot.$tau.$area.png";

  } elseif($model == 'navg') {
    $path="plt_fnmoc_$model/$dtg/nav05.$plot.$tau.$area.png";

  } elseif($model == 'ukm') {
    $path="plt_ukmo_$model/$dtg/${model}07.$plot.$tau.$area.png";

  } elseif($model == 'cmc') {
    $path="plt_cmc_$model/$dtg/${model}025.$plot.$tau.$area.png";

  } elseif($model == 'ecm') {
    $path10="plt_ecmwf_$model/$dtg/${model}10.$plot.$tau.$area.png";
    $path025="plt_ecmwf_$model/$dtg/${model}025.$plot.$tau.$area.png";
    if(file_exists($path025)) {
      $path=$path025;
    } elseif(file_exists($path10)) {
      $path=$path10;
    }


  } else {


    $path="";

  }


  return($path);



}


function MorphLoop($paths,$looppath,$veri) {
  // get the bind here, there is no global scope in php
  require 'w2local.php';

  $verb=0;

  $cwd=getcwd();

  $dissdelay=25;
  $dissdelay=15;
  $begloopdelay=100;
  $loopdelay=100;

  // increase for looping models
  $loopdelay=200;

  if($veri == 1 || $veri == 2) {
    $dissdelay=12;
    $begloopdelay=80;
    $loopdelay=120;
  }

  $loopcmd="$bindir/convert -loop 0 ";

  $ndiss=2;
  $ndiss=0; // turn off morphing -- a LOT faster
  $npaths=count($paths);

  // use tmp hanging off the web root vice system tmp for better control
  //$tdir=$cwd."/tmp";
  // -- 20201231 -- wxmap2.com use system tmp
  $tdir="/tmp";
  
  // clear the plot cache

  $cmd="/bin/rm -f $tdir/p??.png";
  $rc=system($cmd);
  if($verb) {
      print "CCC(int): $cmd\n";
      print "rc: $rc\n";
    }

  $tpaths=array();

  $n=0;

  for ($i=0  ; $i<$npaths ; $i++) { 
    
    $ldelay=$loopdelay;
    
    if($i==0) $ldelay=$begloopdelay;

    $tpath=sprintf('%s/p%02d.png',$tdir,$n);
    $loopcmd="$loopcmd -delay $ldelay $tpath";

    array_push($tpaths,$tpath);

    $cmd="/bin/cp -f $paths[$i] $tpath";
    $rc=system($cmd);
    if($verb) {
      print "CCC(int): $cmd\n";
      print "rc: $rc\n";
    }

    for ($j=0 ; $j<$ndiss ; $j++) {
      $n++;
      $pdiss=100.0-(($j+1)/($ndiss+1))*100.0;
      $pdiss=round($pdiss,0);
      $tpath=sprintf('%s/p%02d.png',$tdir,$n);
      $loopcmd="$loopcmd -delay $dissdelay $tpath";

      array_push($tpaths,$tpath);
      $plot1=$paths[$i];
      $ip1=$i+1;
      if($i == $npaths-1) {
	$ip1=0;
      }
      $plot2=$paths[$ip1];

      $cmd="$bindir/composite -dissolve $pdiss  $plot1 $plot2 $tpath";
      $rc=system($cmd);
      if($verb) {
	print "CCC(int): $cmd\n";
	print "rc: $rc\n";
      }

    }

    $n++;
    
  }


  $loopcmd="$loopcmd -delay $ldelay $tpaths[0] $looppath";
  $rc=system($loopcmd);
  if($verb) {
    print "CCC(loop): $loopcmd\n";
    print "rc(loop): $rc\n";
  }


}




function LatLonMouseOver($area,$ptype) {

    $llmohtm='';
    
    $doit=0;

    if($ptype == 'prw') {

      if($area == 'lant') {

	$doit=1;
	$arealatT=40.0;
	$arealatB=-10.0;
	$arealonL=-100.0;
	$arealonR=-10.0;

	$xL=39;
	$xR=859;
	$yTb=73;
	$yBb=605;
	$ycorr=0;

      } elseif($area == 'epac') {

	$doit=1;
	$arealatT=40.0;
	$arealatB=-10.0;
	$arealonL=-160.0;
	$arealonR=-70.0;

	$xL=39;
	$xR=859;
	$yTb=73;
	$yBb=604;
	$ycorr=0;

      } elseif($area == 'wpac') {

	$doit=1;

	$arealatT=45.0;
	$arealatB=-10.0;
	$arealonR=200.0;
	$arealonL=100.0;

#
# adjust by hand by having showlatlon display pixel
#
	$xL=39;
	$xR=859;
	$yTb=77;
	$yBb=602;
	$ycorr=0;

      } elseif($area == 'io') {

	$doit=1;

	$arealatT=30.0;
	$arealatB=-40.0;
	$arealonR=140.0;
	$arealonL=20.0;

#
# adjust by hand by having showlatlon display pixel
#
	$xL=39;
	$xR=859;
	$yTb=75;
	$yBb=616;
	$ycorr=0;

      } elseif($area == 'spac') {

	$doit=1;

	$arealatT=10.0;
	$arealatB=-50.0;
	$arealonR=210.0;
	$arealonL=100.0;

#
# adjust by hand by having showlatlon display pixel
#
	$xL=39;
	$xR=859;
	$yTb=77;
	$yBb=599;
	$ycorr=0;

      }


    } else {


      if($area == 'troplant') {

	$doit=1;
	$arealatT=60.0;
	$arealatB=-10.0;
	$arealonL=-120.0;
	$arealonR=0.0;
	
      } elseif($area == 'tropepac') {

	$doit=1;
	$arealatT=60.0;
	$arealatB=-10.0;
	$arealonL=160.0;
	$arealonR=280.0;

      } elseif($area == 'tropwpac') {
	$doit=1;
	$arealatT=60.0;
	$arealatB=-10.0;
	$arealonR=200.0;
	$arealonL=80.0;
      }

    }

    if($ptype != 'prw') {

      $xL=40;
      $xR=876;
      $yTb=36;
      $yBb=604;
      $ycorr=3;

    }

    if($doit) {
	

$llmohtm="

<!-- show lat/lon code as doc going on end of preceeding doc -->

<script language=\"Javascript1.2\" src=\"js/numberformat.js\" type=\"text/javascript\"></script>
<script language=\"Javascript1.2\" src=\"js/showlatlon.js\" type=\"text/javascript\"></script>


<form name=\"Show\">
<input type=\"text\" name=\"MouseY\" value=\"0\" size=\"5\">
<input type=\"text\" name=\"MouseX\" value=\"0\" size=\"5\"> Lat/Lon<br>
</form>

<script language=\"JavaScript1.2\">

var tempX = 0
var tempY = 0

// offset that makes upper righthand corner (0,0)

var offsetxL=tp[0]
var offsetyT=tp[1]

var IEoffsetX=-3
var IEoffsetY=-3


// calc from parea and size of image in area.trop*.cfg

var xL=${xL}
var xR=${xR}

var lonL=${arealonL}
var lonR=${arealonR}

var yT=${yTb}+${ycorr}
var yB=${yBb}+${ycorr}

var latT=${arealatT}
var latB=${arealatB}

var dX=xR-xL
var dlonP=(lonR-lonL)/dX

var dY=yB-yT
var dlatP=(latT-latB)/dY
</script>

";

    }

    return($llmohtm);

}



$PlotTitle= array(
'500' => '500 hPa Heights [m] and Rel. Vort [10^-5 s^-1]',
'850' => '850 hPa Temperature [C], winds [kts] and Rel. Hum. [%]',
'prp',$pt,
'psl' => 'SLP [hPa] & 500-1000 Thkns [m] & 700 hPa Vert. Vel [Pa s^-1]',
'u50' => '500 hPa Strmlns & Istchs [kt] ; Wind Barbs',
'u70' => '700 hPa Strmlns ; N-S wind componment ; Wind Barbs',
'shr' => '|850-200 Shear| ; 200 hPa Strmlns 850(R)/200(G) Barbs',
'sst' => 'SST [C] ; SST Anomaly from AMIP II SST Climatology (1979-96)',
'uas' => '10 m Sfc Winds [kt]',
'wav' => 'Sig Wave Heights [ft] ; Over Ocean Sfc Winds [kt]',
'w20' => '200 hPa Streamlines and Isotachs [kt]',
'wdl' => 'Deep Layer Mean Streamlines/Isotachs [kt]',
'lmq' => 'Low-Mid Trop (850/700/500) PW [mm] & Flow',
'mhq' => 'Mid-High Trop (500/300) PW [mm] & Flow',
'hhq' => 'High-High Trop (300/200) PW [mm] & Flow',
'tmx' => 'Max Sfc Air Temperature [F] ; GFS Previous 24-h',
'tmn' => 'Min Sfc Air Temperature [F] ; GFS Previous 24-h',
'tas' => 'Sfc Air Temperature Change [F]',
'thk' => '1000-500 Thickness [dm] and Sea Level Pressure [mb]',
'w70' => '700 hPa Strmlns and Istchs [kt] ; Wind Barbs',
'clm' => '0-5 day mean climo',
'n850' => 'McAdie Plot: 850 Rel Vort [10^-5] Wind Barbs ; 200 Strmlns [kt]',
);



function findexts ($filename)
{
  $filename = strtolower($filename) ;
  $exts = split("[/\\.]", $filename) ;
  $n = count($exts)-1;
  $exts = $exts[$n];
  return $exts;
}

function gethost ()
{

  $card=php_uname();
  $tt=pysplit($card,' ');
  $host=$tt[1];
  $tt=pysplit($host,'.');
  $firstname=$tt[0];
  return $host;
}

?>
