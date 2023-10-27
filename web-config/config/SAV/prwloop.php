<?php

// Report simple running errors
error_reporting(E_ALL | E_WARNING | E_PARSE);

require 'wxmap.php';
require 'tcanaldb.php';
require 'phpglobal.php';

$bdir="plt_loop";
$cwd=getcwd();
$bdir=$cwd."/$bdir";

$mask="prw.*.*.*.loop.gif";
$sbtmask="gfs.goes.chn03.*.*.loop.gif";

chdir($bdir);

$giffiles=glob($mask);
rsort($giffiles);

$sbtgiffiles=glob($sbtmask);
rsort($sbtgiffiles);

#print_r($sbtgiffiles);

$models=array();
$dtgs=array();
$areadtgs=array();
$modeldtgs=array();


foreach ($giffiles as $giffile) {
  $rc=pysplit($giffile,'.');
  $model=$rc[1];
  $dtg=$rc[2];
  $area=$rc[3];
  array_push($dtgs,$dtg);
  array_push($models,$model);
  $areadtgs[$dtg]=$areadtgs[$dtg]." $area ";
  $modeldtgs[$dtg]=$modeldtgs[$dtg]." $model ";
  //print_r($rc);
}

$dtgs=uniq($dtgs);
$models=uniq($models);
$dtgs=array_reverse($dtgs);
$ndtgs=count($dtgs);

foreach ($dtgs as $dtg) {
  $areadtgs[$dtg]=pysplit($areadtgs[$dtg],' ');
  $areadtgs[$dtg]=uniq($areadtgs[$dtg]);
  //print "QQQ $dtg\n";
  //print_r($areadtgs[$dtg]);

}

foreach ($dtgs as $dtg) {
  $modeldtgs[$dtg]=pysplit($modeldtgs[$dtg],' ');
  $modeldtgs[$dtg]=uniq($modeldtgs[$dtg]);
//  print "QQQ $dtg\n";
//  print_r($modeldtgs[$dtg]);

}

$xszs=900;
$yszs=$xszs*(3/4);

#
# input that comes in from the link
#

$tdtg=$_GET['dtg'];
$tarea = $_GET['area'];
$tmodel = $_GET['model'];
$tptau = $_GET['ptau'];

# naked input
#

if($tdtg == '') {
  $tdtg=$dtgs[0];
} 


if($tarea == '') {
  $tarea=$areadtgs[$tdtg][0];
}

if($tmodel == '') {
  $curmodels=sortmodel($modeldtgs[$tdtg]);
  $tmodel=$curmodels[0];
}


if($tmodel == 'goes') {
  $sbtarea=$sbtAreaNames[$tarea];
  $looppath="plt_loop/gfs.goes.chn03.$sbtarea.$tdtg.loop.gif";
  if($tptau != '') {
    $looppath="plt_prw_goes/$tdtg/gfs.goes.chn03.$sbtarea.$tdtg.$tptau.png";
    $tptau='';

  }
} else {
  $looppath="plt_loop/prw.$tmodel.$tdtg.$tarea.loop.gif";
  if($tptau != '') {
    $looppath="plt_prw_goes/$tdtg/prw.$tmodel.$tdtg.$tarea.$tptau.png";
    $tptau='';
  }
}


# -- make the html
#
$lctmodel=strtolower($tmodel);

$yyyy=substr($tdtg,0,4);

$modeltitle=strtoupper($tmodel);
$areatitle=strtoupper($tarea);
$toptitle="PRW $tmodel BDTG: $tdtg";

$pagetitle="WxMAP2 $tmodel PRW <font color=red>$tdtg</font> Area: <font
color=red>$areatitle</font> Model: <font color=red>$modeltitle<font>";

$htmlhead="
<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
<html>
<head>

<title>
$toptitle
</title>
<link rel=\"shortcut icon\" href=\"favicon.ico\">
<link rel=\"stylesheet\" href=\"css/wxmain.css\" type=\"text/css\">

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da>
<script language=\"javascript\" src=\"js/wxmain.js\" type=\"text/javascript\"></script>
";


print $htmlhead;

print "
<table class='title'>
<tr>

<td width=800>
$pagetitle
</td>

</tr>
</table>

";



//----------------------------------- button row 1 ---- storms for this dtg 
$stmtable="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$curmodels=$modeldtgs[$tdtg];
$curmodels=sortmodel($curmodels);

foreach ($curmodels as $model) {
  $omodel=strtoupper($model);
  $stmtable="$stmtable
<td>
<input type='button' class='btnmod'
onMouseOver=\"className='btnmodover';\" onMouseOut=\"className='btnmod';\"
value='$omodel' name=tctrk
onClick=\"cvalue='prwloop.php?dtg=$tdtg&area=$tarea&model=$model'; opentype='page',swaphtm();\">
</td>
";

}


$stmtable="$stmtable
<td>
<input type='button' class='btnmod'
onMouseOver=\"className='btnmodover';\" onMouseOut=\"className='btnmod';\"
value='GOES' name=tctrk
onClick=\"cvalue='prwloop.php?dtg=$tdtg&area=$tarea&model=goes'; opentype='page',swaphtm();\">
</td>
";




$curareas=$areadtgs[$tdtg];
$curareas=sortarea($curareas);

foreach ($curareas as $area) {
  $oarea=strtoupper($area);
  $stmtable="$stmtable
<td>
<input type='button' class='btntd'
onMouseOver=\"className='btntdover';\" onMouseOut=\"className='btntd';\"
value='$oarea' name=tctrk
onClick=\"cvalue='prwloop.php?dtg=$tdtg&area=$area&model=$tmodel'; opentype='page',swaphtm();\">
</td>
";

}





$stmtable="$stmtable


</tr>
</table>
";
print $stmtable;
//eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee button row 1 eeeeeeeeeeeeeeeeeeeeeeeeeeee



//--------------------------- button row 2 --- dtgs -- 
$menutable1="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue='wx.htm';opentype='page',swaphtm();\">
</td>
";


$ndtgsmax=5;
$rc=findcurdtgibie($tdtg,$dtgs,$ndtgs,$ndtgsmax);

$idtgb=$rc[0];
$idtge=$rc[1];
$icurdtg=$rc[2];


for ($i=$idtgb ; $i<$idtge ; $i++) { 
  $dtg=$dtgs[$i];

  if($i == $icurdtg) {
    $btnclass='btndtgcur';
  } else {
    $btnclass='btndtg';
  }

  $menutable1="
$menutable1
<td>
<input type='button' class='${btnclass}'
onMouseOver=\"className='${btnclass}over';\" onMouseOut=\"className='${btnclass}';\"
value='$dtg' name=tctrk
onClick=\"cvalue='prwloop.php?dtg=$dtg&area=$tarea';opentype='page',swaphtm();\">
</td>


";  
}

//------------------- tau buttons

$btntau='btntaudtg';

$taubuttons="";

foreach ($sbtTaus as $sbttau) {

  $tau=intval(substr($sbttau,1,4));
  if(substr($sbttau,0,1) == 'm') {
    $otau=sprintf("%+d",$tau*-1);
  } else {
    $otau=sprintf("%+d",$tau);
  }

	$taubuttons= "
$taubuttons
<td>
<input type='button' class='${btntau}'
onMouseOver=\"className='${btntau}over';\"
onMouseOut=\"className='${btntau}';\"
value='${otau}' name=taub
onClick=\"cvalue='prwloop.php?dtg=$tdtg&model=$tmodel&area=$tarea&ptau=$sbttau';opentype='page',swaphtm();\">
</td>
";


}



    $menutable1="
$menutable1
$taubuttons


</tr>
</table>
";
print $menutable1;
//eeeeeeeeeeeeeeeeeeeeeeeeeee button row 2 eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee




$plthtml="
<table border=1 cellpadding=0 cellspacing=0>
<tr>
<td>
<img name='myImage' src=\"$looppath\">
</td>
</tr>
</table>
";

print $plthtml;

//--------------------------------------- plot ---------------------------------------

$ptype='prw';
$llhtml=LatLonMouseOver($tarea,$ptype);
print $llhtml;

print "
</body>
</html>
";

function sortmodel($models) {

  //print_r($models);
  $omodels=array();
  $stdorder=array('gfs2','fim8');
  foreach ($stdorder as $smodel) {
    foreach ($models as $model) {
      if($model == $smodel) {
	array_push($omodels,$model);
      }

    }

  } 
  //print_r($stndorder);
  //print_r($omodels);

  return($omodels);

}

function sortarea($areas) {

  //print_r($areas);
  $oareas=array();
  $stdorder=array('wpac','epac','lant','io','spac');
  foreach ($stdorder as $sarea) {
    foreach ($areas as $area) {
      if($area == $sarea) {
	array_push($oareas,$area);
      }

    }

  } 
  //print_r($stndorder);
  //print_r($oareas);

  return($oareas);

}


?>

