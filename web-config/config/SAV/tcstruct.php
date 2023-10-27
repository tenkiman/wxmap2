<?php

ini_set('session.gc_maxlifetime',1800);
ini_set('session.gc_probability',100);

session_start();

// Report simple running errors
//error_reporting(E_ALL | E_WARNING | E_PARSE);
error_reporting(E_ERROR);

require 'wxmap.php';
require 'tcanaldb.php';

$host=gethost();

#
# get web server from superglobal $_SERVER
#
$webserver=$_SERVER['SERVER_NAME'];

function sortmodels($models) {

  //print_r($models);
  $omodels=array();
  $stdorder=array('gfs','ecm','ukm','ngp','cmc');
  $stdorder=array('ecm2','ukm2','gfs2','fim8','ngp2');
  $stdorder=array('gfs2','fim8','ukm2','ecm2','ngp2');
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

function TCstructDB ( $tcfiles ) {

  $dtgs=array();
  $dtgmodels=array();
  $dtgstms=array();

  $verb=0;

  foreach ( $tcfiles as $tcfile) {

    $tcsiz=filesize($tcfile);
    $tcatime=filectime($tcfile);
    $tcdtg=strftime("%Y%m%d%H",$tcatime);
    if($verb) {
      echo "fffffff $tcfile siz: $tcsiz $tcatime $tcdtg\n";
    }
    $tt1=explode(".",$tcfile);
    $dtg=$tt1[2];
    array_push($dtgs,$dtg);

    $cards=file_get_contents($tcfile);
    $cards=explode("\n",$cards);
  
    $taus=array();
    $stms=array();
    $models=array();

    foreach ($cards as $card) {
      //print "$card\n";
      //$tt=explode(" ",$card);
      if(strlen($card) <= 1) {
	break;
      }
      $tt=pysplit($card,' ');
      if(count($tt) > 6) {
	$stm=$tt[0];
	array_push($stms,$stm);
      }
    }


    //$taumodels=settaumodels($taus,$stms);
    //$modeltaus=setmodeltaus($models,$stms);
    //print_r($modeltaus);

    foreach ($cards as $card) {
      //print "$card\n";
      //$tt=explode(" ",$card);
      if(strlen($card) <= 1) {
	break;
      }
      $tt=pysplit($card,' ');
      if(count($tt) > 6) {
	$stm=$tt[0];
	$stm=$stm;
	$rlat=$tt[1];
	$rlon=$tt[2];
	$vmax=$tt[3];
	$rmax=$tt[4];
	$r34=$tt[5];
      
	//echo "ttttt--------- $stm $rlat $rlon $vmax $rmax $r34\n";
	for ($i=6; $i < count($tt); $i++) {
	  $tttt=explode(".",$tt[$i]);
	  $model=$tttt[0];
	  array_push($models,$model);
	  $tau=$tttt[1];
	  array_push($taus,$tau);

	  //print "$i $tt[$i] $model $stm $tau\n";
	  $modeltaus[$dtg][$model][$stm]=$modeltaus[$dtg][$model][$stm]." $tau";
	  $taumodels[$dtg][$tau][$stm]=$taumodels[$dtg][$tau][$stm]." $model";
	}
      }

    }

    $models=uniq($models);

#
# sort models into better order
#
    $smodels=sortmodels($models);
    $dtgmodels[$dtg]=$smodels;
    $dtgstms[$dtg]=$stms;

  }
  
  $dtgs=uniq($dtgs);
  
  $rc=array($dtgs,$dtgmodels,$dtgstms,$modeltaus,$taumodels);
  return $rc;

}

function model2button($model) {

  $bmodel=$model;
  if($model == 'gfs2') $bmodel='GFS';
  if($model == 'fim8') $bmodel='FIM';
  if($model == 'ukm2') $bmodel='UKM';
  if($model == 'ecm2') $bmodel='ECM';
  if($model == 'ngp2') $bmodel='NGP';

  return($bmodel);
}


$bdir="tc/tcanal";
$cwd=getcwd();
$tcdir=$cwd."/$bdir";

$ndtgs=0;
$mask="$tcdir/tc.db*.txt";
$mask="tc.db.*.txt";

chdir($tcdir);

$tcfiles=glob($mask);
rsort($tcfiles);

$xszs=900;
$xszs=1024;
$yszs=$xszs*(3/4);

$reset = $_GET['reset'];
//$reset=1;

if( $reset == 1 ) {
  error_reporting(E_ERROR);
  session_destroy();
  session_start();
}

$_SESSION['TCScount']=$_SESSION['TCScount']+1;
$viewcount=$_SESSION['TCScount'] ;

if($viewcount <= 1 || $reset == 1) {

  $rc = TCstructDB($tcfiles);

  //error_reporting(E_ALL | E_WARNING | E_PARSE);

  $i=0;
  $dtgs=$rc[$i]; $i++;
  $dtgmodels=$rc[$i]; $i++;
  $dtgstms=$rc[$i]; $i++;
  $modeltaus=$rc[$i]; $i++;
  $taumodels=$rc[$i]; $i++;
  
  $dtgs=array_reverse($dtgs);
  $ndtgs=count($dtgs);

  $_SESSION['TCSdtgs']=$dtgs;
  $_SESSION['TCSdtgmodels']=$dtgmodels;
  $_SESSION['TCSdtgstms']=$dtgstms;
  $_SESSION['TCSmodeltaus']=$modeltaus;
  $_SESSION['TCStaumodels']=$taumodels;

} else {

  $dtgs=$_SESSION['TCSdtgs'];
  $dtgmodels=$_SESSION['TCSdtgmodels'];
  $dtgstms=$_SESSION['TCSdtgstms'];
  $modeltaus=$_SESSION['TCSmodeltaus'];
  $taumodels=$_SESSION['TCStaumodels'];
  $ndtgs=count($dtgs);


}

$verb=0;
if($verb) {
  foreach ($dtgs as $dtg) {
    foreach ($dtgmodels[$dtg] as $model) {
      foreach ($dtgstms[$dtg] as $stm) {
	$mtaus= $modeltaus[$dtg][$model][$stm];
	print "qqqqqqqqqq $dtg $model $stm taus: $mtaus\n";
      } 
    }
  }
}

#
# input that comes in from the link
#

error_reporting(E_ERROR);

$tdtg=$_GET['dtg'];
$tstm = $_GET['storm'];
$tmodel = $_GET['model'];
$ttau = $_GET['tau'];
$ptype = $_GET['ptype'];


#
# naked input
#


if($tdtg == '') {
  $tdtg=$dtgs[0];
} 

$curstms=$dtgstms[$tdtg];
sort($curstms);

#
# handle 3 char stmid from tcfilt.php
#
if($tstm == '') {
  $tstm=$curstms[0];
} else {
  $lc=strlen($tstm);
  if($lc == 3) {
    foreach ($curstms as $curstm) {
      $tt=pysplit($curstm,'.');
      if($tt[0] == $tstm) {
	$tstm=$curstm;
      }
    }
  }
}

if($ptype == '') {
  $ptype='tau';
}

if($tmodel == '') {
  $tmodel=$dtgmodels[$tdtg][0];
}

$taus=pysplit($modeltaus[$tdtg][$tmodel][$tstm],' ');

if( $ttau == '') {
    $ttau=$taus[0];
}

if( $ttau == '') {
  $rc=findtau000($tdtg,$tstm,$ttau,$dtgmodels,$dtgstms,$modeltaus);
  $ttau=$rc[0];
  $tmodel=$rc[1];
  $tstm=$rc[2];
  if($ttau == -999 && $tmodel == -999 && $tstm == -999) {
    $tdtg=$dtgs[1];
    $rc=findtau000($tdtg,$tstm,$ttau,$dtgmodels,$dtgstms,$modeltaus);
    $ttau=$rc[0];
    $tmodel=$rc[1];
    $tstm=$rc[2];
    if($ttau == -999 && $tmodel == -999 && $tstm == -999) {
      print 'sorry we have a problem...';
      exit;
    }
  }
}

#
# make the html
#
$lctmodel=strtolower($tmodel);

$yyyy=substr($tdtg,0,4);

$modeltitle=strtoupper($tmodel);
$stormtitle=strtoupper($tstm);
$toptitle="WxMAP2 TC Structure Analysis :: $tdtg";

$pagetitle="WxMAP2 TC Structure Analysis: <font color=red>$tdtg</font> Current TC: <font color=red>$stormtitle</font>  Model: <font color=red>$modeltitle<font>";

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

<body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad=pswap()>
<script language=\"javascript\" src=\"js/wxmain.js\" type=\"text/javascript\"></script>
";



//------------------------------------------- pswap -------------------------------------
$jspswap="
<script language=\"javascript\" type=\"text/javascript\">

plotdir='$bdir';
ptype='$ptype';
yyyy='$yyyy';
tdtg='$tdtg';
lctmodel='$lctmodel';
tstm='$tstm';
ttau='$ttau';

function pswap() 
{

    if(ptype == 'tau') {
	value=plotdir + '/' + yyyy + '/' + tdtg + '/plt/plt'     + '.' + lctmodel + '.' + tstm + '.' + ttau + '.png';
    } else if(ptype == 'animate') {
	value=plotdir + '/' + yyyy + '/' + tdtg + '/plt/animate' + '.' + lctmodel + '.' + tstm + '.' + tdtg + '.gif';
    } else if(ptype == 'profile') {
	value=plotdir + '/' + yyyy + '/' + tdtg + '/plt/profile' + '.' + lctmodel + '.' + tstm + '.' + tdtg + '.png';
    }

myUrl=value;
if (value != '') if (document.images) {
  document.images.myImage.src = value;
  document.images.myImage.alt = value;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
//alert(value)
}

}

</script>

";
//------------------------------------------- pswap -------------------------------------


print $htmlhead;
print $jspswap;

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

$curstms=$dtgstms[$tdtg];
sort($curstms);

foreach ($curstms as $stm) {

  $ttstm=pysplit($stm,'.');
  $stm3=$ttstm[0];

  $stmtable="$stmtable
<td>
<input type='button' class='btn50red'
onMouseOver=\"className='btn50redover';\" onMouseOut=\"className='btn50red';\"
value='$stm3' name=tctrk
onClick=\"cvalue='tcstruct.php?dtg=$tdtg&storm=$stm'; opentype='page',swaphtm();\">
</td>
";

}

$ttstm=pysplit($tstm,'.');
$tstm3=$ttstm[0];

$stmtable="$stmtable

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='TcFilt' name=tctrk
//http://kishou.fsl.noaa.gov/wxmap2/tcfilt.php?dtg=2009042718&stm=27S&model=gfs2&tau=000&plt=vt850&ptype=full&pmode=single
onClick=\"cvalue='tcfilt.php?dtg=$tdtg&stm=$tstm3&model=$tmodel&tau=000&plt=vt850&ptype=full&pmode=single&interact=0'; opentype='page',swaphtm();\">
</td>

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='TcEps' name=tctrk
onClick=\"cvalue='http://$webserver/hfip/tceps/tceps.php?dtg=$tdtg&stm=$tstm';opentype='page',loadW2Html(cvalue,opentype);\">
</td>


</tr>
</table>
";
print $stmtable;
//eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee button row 1 eeeeeeeeeeeeeeeeeeeeeeeeeeee

$ttstm=pysplit($tstm,'.');
$tstm3=$ttstm[0];


//--------------------------- button row 2 --- dtgs -- home
$menutable1="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
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
onClick=\"cvalue='tcstruct.php?dtg=$dtg&storm=$tstm';opentype='page',swaphtm();\">
</td>


";  
}

    $menutable1="
$menutable1

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue='wx.${tdtg}.htm';opentype='page',swaphtm();\">
</td>

<td>
<input type='button' class='bhelp'
onMouseOver=\"className='bhelpover';\" onMouseOut=\"className='bhelp';\"
value='RESET' name=tctrk
onClick=\"cvalue='tcstruct.php?reset=1'; opentype='page',swaphtm();\">
</td>

</tr>
</table>
";
print $menutable1;
//eeeeeeeeeeeeeeeeeeeeeeeeeee button row 2 eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee


//---------------------------- model, plot tau buttons-------------------------------
$taubuttons="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$model000s=pysplit($taumodels[$tdtg]['000'][$tstm],' ');
$model000s=$dtgmodels[$tdtg];

foreach ($model000s as $model) {
  
  $bmodel=model2button($model);
  $taus=pysplit($modeltaus[$tdtg][$model][$tstm],' ');

  $taubuttons="
$taubuttons

<td>
<input type='button' class='btn50grnr'
onMouseOver=\"className='btn50grnrover';\"
onMouseOut=\"className='btn50grnr';\"
value='${bmodel}' name=taub
onClick=\"cvalue='tcstruct.php?dtg=$tdtg&storm=$tstm&model=$model&ptype=$ptype';opentype='page',swaphtm();\">
</td>
";
  
  $btnanim='btn50';
  $btnprof='btn50';
  $btntau='btnsmltau';

  if(count($taus) > 0) {

  $taubuttons="
$taubuttons
<td>
<input type='button' class='${btnanim}'
onMouseOver=\"className='${btnanim}over';\"
onMouseOut=\"className='${btnanim}';\"
value='anim' name=taub
onClick=\"ptype='animate';lctmodel='${model}',pswap();\">
</td>

<td>
<input type='button' class='${btnprof}'
onMouseOver=\"className='${btnprof}over';\"
onMouseOut=\"className='${btnprof}';\"
value='prf' name=taub
onClick=\"ptype='profile';lctmodel='${model}',pswap();\">
</td>
";


    foreach ($taus as $tau) {

      $urltaufile="tcstruct.php?dtg=$tdtg&storm=$tstm&model=$model&ptype='tau'&tau=$tau";
    
      $taubuttons= "
$taubuttons
<td>
<input type='button' class='${btntau}'
onMouseOver=\"className='${btntau}over';\"
onMouseOut=\"className='${btntau}';\"
value='${tau}' name=taub
onClick=\"ttau='${tau}';ptype='tau';lctmodel='${model}',pswap();\">
</td>
";
    }

  }
    $taubuttons="
$taubuttons
</tr>";
}

$taubuttons="
$taubuttons
</table>
";

print $taubuttons;
//---------------------------- model, plot tau buttons-------------------------------


$plthtml="
<table border=1 cellpadding=0 cellspacing=0>
<tr>
<td width=$xszs>
<a name='link' href='myUrl' target='_blank'><img name='myImage' width='$xszs'></a>
</td>
</tr>
</table>
";

print $plthtml;

//--------------------------------------- plot ---------------------------------------


print "
</body>
</html>
";

?>

