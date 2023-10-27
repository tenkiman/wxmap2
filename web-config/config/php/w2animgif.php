<?php


// Report simple running errors
//error_reporting(E_ALL | E_WARNING | E_PARSE);

require 'wxmap.php';

$dtg = $_GET['dtg'];
$area = $_GET['area'];
$tau = $_GET['tau'];
$plot = $_GET['plot'];
$reset = $_GET['reset'];
$veri = $_GET['veri'];
$model = $_GET['model'];


$test=0;

if($test) {
  $reset=0;
  $dtg=2008081312;
  $area='troplant';
  $tau='072';
  $plot='uas';
  $veri=2;
  $model='gfs';

  $reset=1;
  $dtg=2008120306;
  $area='troplant';
  $tau='072';
  $plot='uas';
  $veri=0;
  $model='ecm';

  $reset=0;
  $dtg=2009032312;
  $area='troplant';
  $tau='072';
  $plot='uas';
  $veri=0;
  $model='fim';

}


if($dtg == '' || $area == '' || $tau == '' || $plot == '') {
  print 'oops...';
  exit;
}

#
# exclude cmc from model loops
#
$allmodels=array('gfs','ngp','ukm','ecm');
$allmodels=array('gfs','fim','ecmn','ngp');
$allmodels=array('gfs','fim','ecm','ecmn','ngp','ukm');
$allmodels=array('gfs','fim','fimx','ecm','ukm');
$allmodels=array('gfs','fim','ngpc','ecmg','ukm');
# -- ecmn now works
$allmodels=array('gfs','fim','ngpc','ecmn','ukm');
# -- ecm2
$allmodels=array('gfs','fim','ngpc','navg','ecm','ukm');
# -- no more nogaps
$allmodels=array('gfs','fim','navg','ecm','ukm');
# -- just the 'good' models
$allmodels=array('gfs','ecm','cmc','navg');
$modelsthere=array();
$loopmodels=$allmodels;
$basedtg=$dtg;

$paths=array();

#
# get the verification analysis and go back for the forecasts
#
if($veri == 1) {

  $analdtg=$dtg;
  $analtau=0;

#
# set the bdtg of the model runs back...
#
  $tauinc=-1*$tau;
  $dtg=dtginc($dtg,$tauinc);
  $loopmodels=array($model);
  $models=array($model);

  $veribttle='Veri_Tau';

} elseif($veri == 2) {

#
#  R-R consistency
#

  $loopmodels=array($model);
  $models=array($model);

  $veribttle='R2R_Con';

  $contaus=array(0,12,24,36);
  $condtgs=array();

  for ($n=0 ; $n<count($contaus) ; $n++) {
    
    $tauinc=-1*($contaus[$n]);
    $cdtg=dtginc($basedtg,$tauinc);
    array_push($condtgs,$cdtg);
    $vtau=$tau+$contaus[$n];
    $contaus[$n]=$vtau;

  }
  
}

foreach ($allmodels as $lmodel) {

  $therean[$lmodel]=0;

  if($veri == 1) {
    $vplot=$plot;
if($plot == 'prp') $vplot='op06';
    $pathan=getplot($lmodel,$analdtg,$area,$analtau,$vplot);
    if(file_exists($pathan)) {
      $therean[$lmodel]=1;
    }


  } elseif($veri == 2) {

    $gotem=0;

    for($n=0 ; $n<count($condtgs) ; $n++) {
      
      $pathfc=getplot($lmodel,$condtgs[$n],$area,$contaus[$n],$plot);
      if(file_exists($pathfc)) {
	$therefc[$lmodel]=1;
	$gotem=1;
      }

    }
    
    if($gotem) {
      $therefc[$lmodel]=1;
      array_push($modelsthere,$lmodel);
    }


  } else {

    $therefc[$lmodel]=0;
    $pathfc=getplot($lmodel,$dtg,$area,$tau,$plot);
    if(file_exists($pathfc)) {
      $therefc[$lmodel]=1;
    }

  }
}


if($veri != 2) {

  foreach ($allmodels	 as $lmodel) {

    if($veri == 1 && $therean[$lmodel] && $therefc[$lmodel]) {
      array_push($modelsthere,$lmodel);
    } else {
      array_push($modelsthere,$lmodel);
    }
  }
}


foreach ($loopmodels as $loopmodel) {

  if($veri == 1) {
    $pathan=getplot($loopmodel,$analdtg,$area,$analtau,$vplot);
    if(file_exists($pathan)) {
      array_push($paths,$pathan);
    }

    $path=getplot($loopmodel,$dtg,$area,$tau,$plot);
    if(file_exists($path)) {
      array_push($paths,$path);
    }

  } elseif($veri == 2) {

    for($n=0 ; $n<count($condtgs) ; $n++) {

      $pathfc=getplot($loopmodel,$condtgs[$n],$area,$contaus[$n],$plot);
      if(file_exists($pathfc)) {
	array_push($paths,$pathfc);
      }

    }

  } else {
#
# loop models
#
    $path=getplot($loopmodel,$dtg,$area,$tau,$plot);
    if(file_exists($path)) {
      array_push($paths,$path);
    }
  }

}


if($veri == 1) {
  $looppath="plt_loop/w2loop.veri.$model.$plot.$dtg.$area.$tau.gif";
} elseif($veri == 2) {
  $looppath="plt_loop/w2loop.contau.$model.$plot.$dtg.$area.$tau.gif";
} else {
  $looppath="plt_loop/w2loop.$plot.$dtg.$area.$tau.gif";
}



if(file_exists($looppath) && $reset != 1 ) {


} else {

  MorphLoop($paths,$looppath,$veri);

}


$ptitle=$PlotTitle[$plot];

$mtitle='';
if($veri == 1) {
  $mm=strtoupper($model);
  $ptitle="VERI: Tau: $tau Model: $mm :: $ptitle";
  
} elseif($veri == 2) {
  $mm=strtoupper($model);
  $ptitle="Run-Run Consistency: Tau: $tau Model: $mm :: $ptitle";
  
} else {
  foreach ($modelsthere as $pmodel) {
    $mm=strtoupper($pmodel);
    $mtitle="$mtitle $mm";
  }
  $ptitle="Tau: $tau Models: $mtitle :: $ptitle";

}


$html="
<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">
<html>
<head>

<link rel=\"shortcut icon\" href=\"favicon.ico\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"css/wxmain.css\">

<title>
$ptitle
</title>

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad=initLoop('image1')>
<script language=\"javascript\" src=\"js/wxmain.js\" type=\"text/javascript\"></script>

<table class='title'>
<tr><td width=900>
$ptitle
</td></tr></table>

<table border=1 cellpadding=0 cellspacing=0>
<tr>

<table border=1 cellpadding=0 cellspacing=0>
</tr>
";

if($veri == 1 or $veri == 2) {


  
  $html="$html
<td>
<input type='button' class='btn150a'
onMouseOver=\"className='btn150a';\" onMouseOut=\"className='btn150a';\"
value='$veribttle Tau: $tau' name=tctrk
onClick=\"cvalue='';opentype='page';\">
</td>
";

  foreach ($modelsthere as $pmodel) {

    $mm=strtoupper($pmodel);

    if($veri == 1) {
      $link="w2animgif.php?dtg=$analdtg&model=$pmodel&area=$area&tau=$tau&plot=$plot&veri=1";
    } elseif($veri == 2) {
      $link="w2animgif.php?dtg=$basedtg&model=$pmodel&area=$area&tau=$tau&plot=$plot&veri=2";
    } else {
      $link="web_$pmodel/$dtg/$pmodel.$plot.$tau.$area.htm";
    }

    $html="$html
<td>
<input type='button' class='btnsmlmod'
onMouseOver=\"className='btnsmlmodover';model='ngp',pswap();\"
onMouseOut=\"className='btnsmlmod';\"
value='$pmodel' name=tctrk
onClick=\"cvalue='$link';opentype='page',swaphtm();\">
</td>";

  }

}


$html="$html
<tr>
<table border=1 cellpadding=0 cellspacing=0>
<tr>
";


$html="$html
<td>
<input type='button' class='btn150a'
onMouseOver=\"className='btn150a';\" onMouseOut=\"className='btn150a';\"
value='Single Taus:' name=tctrk
onClick=\"cvalue='';opentype='page';\">
</td>
";

foreach ($modelsthere as $pmodel) {

  $mm=strtoupper($pmodel);
    $link="web_$pmodel/$basedtg/$pmodel.$plot.$tau.$area.htm";
  $html="$html
<td>
<input type='button' class='btnsmlmod'
onMouseOver=\"className='btnsmlmodover';model='ngp,pswap();\"
onMouseOut=\"className='btnsmlmod';\"
value='$pmodel' name=tctrk
onClick=\"cvalue='$link';opentype='page',swaphtm();\">
</td>";

}



$html="$html

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue='wx.htm';opentype='page',swaphtm();\">
</td>
<td>


</tr>
</table>
</tr>

";



$html="$html
</tr>
</table>

<tr><td>

<img name='myImage' src=\"$looppath\">

</td></tr>
</table>
";



$ptype='anigif';

$llhtml=LatLonMouseOver($area,$ptype);

print $html;
print $llhtml;

print "
</body>
</html>
";


exit;
