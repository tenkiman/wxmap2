<?php

//ini_set('session.gc_maxlifetime',1800);
//ini_set('session.gc_probability',100);
//session_start();

// Report simple running errors

error_reporting(E_ALL | E_WARNING | E_PARSE);

require 'tc.php';
require 'wxmap.php';
require 'tcanaldb.php';

function TCww3DB ( $inventory ) {

  $dtgs=array();
  $dtgstms=array();
  $dtgstmplts=array();
  $dtgstmplttaus=array();

  $verb=1;

  $cards=file_get_contents($inventory);
  $cards=explode("\n",$cards);
  $lines=array();

#-------------- parse file into array of lines

  foreach ($cards as $card) {
    $tt=explode(' ',$card);
    array_push($lines,$tt);
  }

#--------------- get the dtgs...

  foreach ($lines as $tt) {

    $dtg=$tt[0];
    if(strlen($dtg) == 10) {
      $stm=$tt[1];
      $n=count($tt);
      $tlast=$tt[$n-1];
      $plts=array_slice($tt,3,$n-1);
      $nplts=count($plts);
      if($nplts > 1) {
	array_push($dtgs,$dtg);
	$dtgstms[$dtg]=array();
      }
    }
    
  }


#---------------- get storms by dtg

  foreach ($lines as $tt) {

    $dtg=$tt[0];
    if(strlen($dtg) == 10) {
      $stm=$tt[1];
      $n=count($tt);
      $tlast=$tt[$n-1];
      $plts=array_slice($tt,3,$n-1);
      $nplts=count($plts);
      if($nplts > 1) {
	array_push($dtgstms[$dtg],$stm);
	$dtgstmplttaus[$dtg][$stm]=array();
      }
    }
  }

#---------------- get plts by dtg, stm

  foreach ($lines as $tt) {

    $dtg=$tt[0];
    if(strlen($dtg) == 10) {
      $stm=$tt[1];
      $n=count($tt);
      $tlast=$tt[$n-1];
      $plts=array_slice($tt,3,$n-1);
      $nplts=count($plts);
      if($nplts > 1) {
	$dtgstmplts[$dtg][$stm]=$plts;
	$taus=array();
	foreach ($plts as $plt) {
	  $tt=pysplit($plt,'.');
	  $tau=$tt[2];
	  if(strlen($tau) == 3) {
	    array_push($taus,$tau);
	  }
	}
	array_push($dtgstmplttaus[$dtg][$stm],$taus);
      }
    }
  }



  //print_r($ncards);
  //$dtgs=uniq($dtgs);
  //print_r($dtgs);
  //print_r($dtgstms);
  //print_r($dtgstmplts);
  //print_r($dtgstmplttaus);

  $dtgs=uniq($dtgs);

  $rc=array($dtgs,$dtgstms,$dtgstmplts,$dtgstmplttaus);
  return $rc;

}


#------------------------------------------------------------------------------------------
#
# main
#


#
# input that comes in from the link
#

$tdtg = $_GET['dtg'];
$tstm = $_GET['stm'];
$ttau = $_GET['tau'];
$ptype = $_GET['ptype'];

$phpfile='tcww3.php';

$baseurl="http://www.nrlmry.navy.mil/atcf_web/wavewatch/";

$idir="tc/tcww3";
$cwd=getcwd();
$inventory="$cwd/$idir/db.tcww3.txt";

$rc=TCww3DB($inventory);

//$rc=array($dtgs,$dtgstms,$dtgstmplts,$dtgstmplttaus);
$i=0;
$dtgs=$rc[$i]; $i++;
$dtgstms=$rc[$i]; $i++;
$dtgstmplts=$rc[$i]; $i++;
$dtgstmplttaus=$rc[$i]; $i++;
  

$nd=count($dtgs);
$lastdtg=$dtgs[$nd-1];
$lstms=$dtgstms[$lastdtg];
$firststm=$lstms[0];


$xszs=900;
$yszs=$xszs*(3/4);




#
# naked input
#

if($tdtg == '') {
  $tdtg=$lastdtg;
} 

if($tstm == '') {
  $lstms=$dtgstms[$tdtg];
  sort($lstms);
  $tstm=$lstms[0];
}

if($ptype == '') {
  $ptype='ww3.anim';
}


$plts=$dtgstmplts[$tdtg][$tstm];
$taus=$dtgstmplttaus[$tdtg][$tstm];

if( $ttau == '') {
    $ttau=$taus[0];
}


#
# make the html
#

$yyyy=substr($tdtg,0,4);

$stmtitle=strtoupper($tstm);
$toptitle="NRL TC WW3 Analysis :: $tdtg";

$pagetitle="NRL TC WW3 for: <font color=red>$tdtg</font> Current TC: <font color=red>$stmtitle</font>";

$htmlhead="
<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
<html>
<head>

<title>
$toptitle
</title>
<link rel=\"stylesheet\" href=\"css/wxmain.css\" type=\"text/css\">

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad=pswap()>
<script language=\"javascript\" src=\"js/wxmain.js\" type=\"text/javascript\"></script>
";

//     [0] => Array
//         (
//             [0] => ep922008.per.2008080612_animation.gif
//             [1] => ep922008.uv.2008080612_animation.gif
//             [2] => ep922008.ww3.000.gif
//             [3] => ep922008.ww3.012.gif
//             [4] => ep922008.ww3.2008080612_animation.gif
//         )

//------------------------------------------- pswap -------------------------------------
$jspswap="
<script language=\"javascript\" type=\"text/javascript\">

plotdir='$baseurl';
ptype='$ptype';
tdtg='$tdtg';
tstm='$tstm';
ttau='$ttau';

function pswap() 
{

    if(ptype == 'tau') {
	value=plotdir + '/' + tstm + '/' + tdtg + '/' + tstm + '.ww3.' + ttau + '.gif';
    } else if(ptype == 'ww3.anim') {
	value=plotdir + '/' + tstm + '/' + tdtg + '/' + tstm + '.ww3.' + tdtg + '_animation.gif';
    } else if(ptype == 'uv.anim') {
	value=plotdir + '/' + tstm + '/' + tdtg + '/' + tstm + '.uv.' + tdtg + '_animation.gif';
    } else if(ptype == 'per.anim') {
	value=plotdir + '/' + tstm + '/' + tdtg + '/' + tstm + '.per.' + tdtg + '_animation.gif';
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

  $plts=$dtgstmplts[$tdtg][$stm];
  $nplts=count($plts);

  $stmtable="$stmtable
<td>
<input type='button' class='btntd'
onMouseOver=\"className='btntdover';\" onMouseOut=\"className='btntd';\"
value='$stm' name=tctrk
onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$stm'; opentype='page',swaphtm();\">
</td>
";

}

$stmtable="$stmtable
</td>
</tr>
</table>
";
print $stmtable;
//eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee button row 1 eeeeeeeeeeeeeeeeeeeeeeeeeeee



//--------------------------- button row 2 --- dtgs -- home
$menutable1="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='NRL TCww3' name=tctrk
onClick=\"cvalue='$baseurl';opentype='page',swaphtm();\">
</td>
";

$dtgs=array_reverse($dtgs);

$ndtgs=count($dtgs);
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
onClick=\"cvalue='$phpfile?dtg=$dtg';opentype='page',swaphtm();\">
</td>


";  
}

    $menutable1="
$menutable1

</tr>
</table>
";
print $menutable1;
//eeeeeeeeeeeeeeeeeeeeeeeeeee button row 2 eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee


//---------------------------- plot tau buttons-------------------------------

$taubuttons="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";


$plts=$dtgstmplts[$tdtg][$tstm];
$taus=$dtgstmplttaus[$tdtg][$tstm];

$ploops=array();
$ptaus=array();

foreach ($plts as $plt) {
  if(strstr($plt,'anim')) {
    array_push($ploops,$plt);
  } else {
    array_push($ptaus,$plt);
  }
}

//print_r($ploops);
//print_r($ptaus);

$btnanim='btn75';
$btnprof='btn75';
$btntau='btnsmltau';

if(count($ploops) > 0) {

  foreach ($ploops as $ploop) {
    
    if(strstr($ploop,'ww3')) {
      $ptype='ww3.anim';

    } elseif(strstr($ploop,'per')) {
      $ptype='per.anim';

    } elseif(strstr($ploop,'uv')) {
      $ptype='uv.anim';
    }


    $taubuttons="
$taubuttons
<td>
<input type='button' class='${btnanim}'
onMouseOver=\"className='${btnanim}over';\"
onMouseOut=\"className='${btnanim}';\"
value='$ptype' name=taub
onClick=\"ptype='$ptype',pswap();\">
</td>
";
  }

}


if(count($ptaus) > 0) {

  foreach ($ptaus as $ptau) {
    
    $tau=pysplit($ptau,'.');
    $tau=$tau[2];

    $taubuttons="
$taubuttons
<td>
<input type='button' class='${btntau}'
onMouseOver=\"className='${btntau}over';\"
onMouseOut=\"className='${btntau}';\"
value='$tau' name=taub
onClick=\"ptype='tau';ttau='$tau';pswap();\">
</td>
";
  }

}


$taubuttons="
$taubuttons
</tr>";

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

