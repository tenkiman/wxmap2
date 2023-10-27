<?php

ini_set('session.gc_maxlifetime',1800);
ini_set('session.gc_probability',100);
session_start();
// Report simple running errors
//error_reporting(E_ALL | E_WARNING | E_PARSE);
error_reporting(E_ERROR);

require 'tc.php';
require 'wxmap.php';
require 'tcanaldb.php';

function LoadHash($lines,$ib,$ie,$nk) {

  $hash=array();

  for ($i=$ib; $i<$ie; $i++) {
    $tt=$lines[$i];
    //print_r($tt);
    if($nk == 1) {
      $key1=$tt[0];
      $hash[$key1]=array_slice($tt,2);

    } elseif($nk == 2) {

      $key1=$tt[0];
      $key2=$tt[1];
      $hash[$key1][$key2]=array_slice($tt,3);

    } elseif($nk == 3) {

      $key1=$tt[0];
      $key2=$tt[1];
      $key3=$tt[2];
      $hash[$key1][$key2][$key3]=array_slice($tt,4);

    } elseif($nk == 4) {

      $key1=$tt[0];
      $key2=$tt[1];
      $key3=$tt[2];
      $key4=$tt[3];
      $hash[$key1][$key2][$key3][$key4]=array_slice($tt,5);

    } else {
      print "EEEEEEEEE key too big\n"; 
    }
  }

  return($hash);
  //print_r($hash);

}



function TCepsDB ( $inventory ) {

  $stmsDtgE=array();
  $dtgsStmE=array();

  $verb=1;

  $cards=file_get_contents($inventory);
  $cards=explode("\n",$cards);
  $lines=array();


#-------------- parse file into array of lines

  foreach ($cards as $card) {
    //$tt=explode(' ',$card);
    $tt=pysplit($card,' ');
    array_push($lines,$tt);
  }

  $n=0;
  $nhash=0;
  $ncards=count($lines);

  while($n < $ncards-1) {
    //print_r($lines[$n]);
    $keyword=$lines[$n][0];
    //print "kkk $keyword $n $ncards\n";
    if($keyword == 'hash') {
      $nl=$lines[$n][2];
      $nk=$lines[$n][1];
      $ib=$n+1;
      $ie=$ib+$nl;
      $hash=LoadHash($lines,$ib,$ie,$nk);
      $n=$n+$nl+1;
      $nhash++;
      if($nhash == 1) $stmsDtgE=$hash;
      if($nhash == 2) $dtgsStmE=$hash;
    }
    
    //print "NNNNNNNNN $nhash\n";
  }

  $rc=array($stmsDtgE,$dtgsStmE);
  return($rc);
  
}


function getInitial() {

  global $stmsDtgE,$dtgsStmE;
  global $ptypesE;
  global $tdtgE,$tstmE,$tptypeE,$reset;

  $nd=count($stmsDtgE);
  $dtgs=array_keys($stmsDtgE);
  
  $tdtgE=$dtgs[$nd-1];
  
  $laststmEs=$stmsDtgE[$tdtgE];
  sort($laststmEs);
  $tstmE=$laststmEs[0];
  
  $tptypeE=$ptypesE[0];
  
}


#------------------------------------------------------------------------------------------
#
# main
#

$xsize=1024;
$ysize=$xsize*(3/4);

$xsizefl=$xsize+24;
$ysizefl=$ysize+128;

$phpfile='tceps.php';

#
# input that comes in from the link
#


$tdtgE = $_GET['dtg'];
$tstmE = $_GET['stm'];
$tptypeE = $_GET['ptype'];

$reset = $_GET['reset'];
$interact = $_GET['interact'];

if( $reset == 1 ) {
  error_reporting(E_ERROR);
  session_destroy();
  session_start();
}

if($interact == '') {
  $interact=0;
} 

$_SESSION['countE']=$_SESSION['countE']+1;

$viewcount=$_SESSION['countE'] ;

if($viewcount <= 1 || $reset == 1) {

  $cwd=getcwd();
  $tcfiltinventory="$cwd/tc/tceps/inv.tceps.txt";
  $rc=TCepsDB($tcfiltinventory);
  
  $i=0;
  
  $stmsDtgE=$rc[$i]; $i++;
  $dtgsStmE=$rc[$i]; $i++;
  $ptypesE=array('strike','plumes');

  
  $_SESSION['stmsDtgE']=$stmsDtgE;
  $_SESSION['dtgsStmE']=$dtgsStmE;
  $_SESSION['ptypesE']=$ptypesE;
  
} else {
  
  $stmsDtgE=$_SESSION['stmsDtgE'];
  $dtgsStmE=$_SESSION['dtgsStmE'];
  $ptypesE=$_SESSION['ptypesE'];
  
}


if($tdtgE == '') {
  getInitial();
}

# 
# check if tstmE is in the stms by dtg, if not use first
#
$gotstmE=0;
foreach($stmsDtgE[$tdtgE] as $dstm) {
  if($dstm == $tstmE) $gotstmE=1;
}

if($gotstmE == 0) $tstmE=$stmsDtgE[$tdtgE][0];


#
# make the html
#

$yyyy=substr($tdtgE,0,4);

$stmtitle=strtoupper($tstmE);
$toptitle="TCeps :: $tdtgE";

$pagetitle="TCeps for: <font color=red>$tdtgE</font> Current TC: <font color=red>$stmtitle</font>";

$htmlhead="
<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
<html>
<head>

<title>
$toptitle
</title>

<link rel=\"shortcut icon\" href=\"favicon.ico\">
<link rel=\"stylesheet\"  type=\"text/css\" href=\"css/wxmain.css\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"css/dropdown.css\">

</head>

<body text=black link=blue vlink=purple bgcolor=#fcf1da onLoad=pswap()>

<script language=\"javascript\" src=\"js/wz_tooltip.js\"    type=\"text/javascript\"></script>
<script language=\"javascript\" src=\"js/wxmain.js\"        type=\"text/javascript\"></script>
<script language=\"javascript\" src=\"js/dropdown.js\"      type=\"text/javascript\"></script>

";


//------------------------------------------- pswap -------------------------------------
$jspswap="

<script language=\"javascript\" type=\"text/javascript\">

plotdir='tc/tceps';
tdtgE='$tdtgE';
tstmE='$tstmE';
tptypeE='$tptypeE';
tyear=tdtgE.substr(0,4);

function pswap() 
{

value=plotdir + '/' + tyear + '/' + tdtgE + '/ec.eps.' + tptypeE + '.'  + tstmE + '.' + tyear + '.' + tdtgE + '.png';
myUrl=value;

altvalue='NO PLOT FOR.... Dtg: ' + ' Stm: ' + tstmE  + ' TptypeE: ' + tptypeE + ' ...try another Model/Dtg/Ptype button';

if (value != '') if (document.images) {
  document.images.myImage.src = value;
  document.images.myImage.alt = altvalue;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
//alert(value);
}

}


function loadDivHtml(value)
{
  newInnerHtml=\"<object id='test' data='\" + value+ \"' width=$xsizefl height=$ysizefl align=center valign=top>\";
  newInnerHtml=newInnerHtml.concat(\"</object>\");
  document.getElementById('div1').innerHTML = newInnerHtml;
}


var menulinks=new Array()

menulinks[0]='<a href=\"javascript:cvalue=\'doc/wxmap.help.htm\',loadDivHtml(cvalue);\" >wxmap help</a>'
menulinks[1]='<a href=\"javascript:cvalue=getW2Url(\'nrl.tc\'),loadW2Html(cvalue,\'window\');\">nrl tc page</a>'

</script>

";

//eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee pswap


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




//111111111111111111111111111111111111111 button row 1 ---- storms for this dtg 


$Bbtni='btn75b';
$Bbtnloop='btn75c';
$Bbtnsingle='btn75d';
$Bbtnsingle=$Bbtnloop;

$Bbtnreset='breset';

$Bbtnphpmode='btn75b';
$Bbtnjsmode='btn75d';
$Bbtnjsmode=$Bbtnphpmode;
$Bbtndrop='btnsmldrop';

$BbptypesE='btn75e';

$stmmisc=600;
$stmwidth=$xsizefl-$stmmisc;

$linksdropwidth=200;
$dtgwidth=$xsize-$linksdropwidth;

$row3ptypeWidth=200;
$row3miscWidth=$xsizefl - $row3ptypeWidth;


$stmtable="

<table  border=0 cellpadding=0 cellspacing=0>
<tr>
<td width=$stmwidth valign=middle align=left>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$curstms=$stmsDtgE[$tdtgE];
sort($curstms);

foreach ($curstms as $stm) {

  $plts=$dtgstmplts[$tdtgE][$stm];
  $nplts=count($plts);

  if($interact) {
    $onclick="onClick=\"tstmE='${stm}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtgE&stm=$stm&ptype=$tptypeE'; opentype='page',swaphtm();\">";
  }

  $stmtable="$stmtable
<td>
<input type='button' class='btn50red'
onMouseOver=\"className='btn50redover';\" onMouseOut=\"className='btn50red';\"
value='$stm' name=tctrk
$onclick
</td>
";


}

$stmtable="$stmtable
</tr>
</table>
</td>

<td width=$stmmisc valign=middle align=right>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='TcW2filt' name=tctrk
onClick=\"cvalue='tcfilt.php';opentype='window',loadW2Html(cvalue,opentype);\">
</td>

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue='wx.htm';opentype='page',swaphtm();\">
</td>

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='doc...' name=tctrk
onClick=\"cvalue='doc/wxmap.help.htm',loadDivHtml(cvalue);\">
</td>

</tr>
</table>
</td>

</tr>
</table>



";

print $stmtable;


//222222222222222222222222222222222222- button row 2 --- dtgs


$dtgtable="
<table border=0 cellpadding=0 cellspacing=0>

<tr>
<td width=$dtgwidth valign=middle align=left>

<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>

";

$dtgs=$dtgsStmE[$tstmE];
rsort($dtgs);

$ndtgs=count($dtgs);
$ndtgsmax=7;
$rc=findcurdtgibie($tdtgE,$dtgs,$ndtgs,$ndtgsmax);

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
  
  if($interact) {
    $onclick="onClick=\"tdtgE='${dtg}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$dtg&stm=$tstmE&ptype=$tptypeE'; opentype='page',swaphtm();\">";
  }

  $dtgtable="
$dtgtable
<td>
<input type='button' class='${btnclass}'
onMouseOver=\"className='${btnclass}over';\" onMouseOut=\"className='${btnclass}';\"
value='$dtg' name=tctrk
$onclick
</td>

";  
}

    $dtgtable="
$dtgtable
</tr>
</table>
</td>

<td width=$linksdropwidth valign=middle align=right>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>

</tr>
</table>
</td>

";
print $dtgtable;



//333333333333333333333333333333333333333333333333333333 button row 3 ---- eps plot types

$modeltable="
<table  border=0 cellpadding=0 cellspacing=0>

<tr>
<td width=$row3ptypeWidth valign=middle align=left>

<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$onclickinteract="onClick=\"cvalue='$phpfile?dtg=$tdtgE&stm=$tstmE&ptype=$tptypeE&interact=1';opentype='page',swaphtm();\">";
$onclickphpmode="onClick=\"cvalue='$phpfile?dtg=$tdtgE&stm=$tstmE&ptype=$tptypeE&interact=0';opentype='page',swaphtm();\">";
$onclickreset="onClick=\"cvalue='$phpfile?reset=1'; opentype='page',swaphtm();\">";

foreach ($ptypesE as $ptype) {

  if($interact) {
    $onclick="onClick=\"tptypeE='${ptype}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtgE&stm=$tstmE&ptype=$ptype'; opentype='page',swaphtm();\">";
  }

  $modeltable="$modeltable
<td>
<input type='button' class='${BbptypesE}'
onMouseOver=\"className='${BbptypesE}over';\" onMouseOut=\"className='${BbptypesE}';\"
value='$ptype' name=tctrk
$onclick
</td>
";

}


if($interact == 1) {

$webmodhtml="
<td>
<input type='button' class=${Bbtnphpmode}
onMouseOver=\"className='${Bbtnphpmode}over';\" onMouseOut=\"className=${Bbtnphpmode};\"
value='PHP mode' name=tctrk
$onclickphpmode
</td>
";

} elseif($interact == 0) {

$webmodhtml="
<td>
<input type='button' class='${Bbtnjsmode}'
onMouseOver=\"className='${Bbtnjsmode}over';\" onMouseOut=\"className='${Bbtnjsmode}';\"
value='JS mode' name=tctrk
$onclickinteract
</td>
";
}


//onMouseOver=\"className='${Bbtnreset}over';\" onMouseOut=\"className='${Bbtnreset}';\"

$modeltable="$modeltable
</tr>
</table>
</td>

<td width=$row3miscWidth valign=middle align=right>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>

<td>
<input type='button' class='${Bbtnreset}'
onMouseOver=\"className='${Bbtnreset}over';\" onMouseOut=\"className='${Bbtnreset}';\"
value='RESET' name=tctrk
$onclickreset
</td>

$webmodhtml

$loopmodehtml

<td>
<input type='button' class='${Bbtndrop}'
onMouseover=\"dropdownmenu(this, event, menulinks, '250px')\" ;
onMouseout=\"delayhidemenu()\";
value='Links...' name='tctrk'\">
</td>

</tr>
</table>

</tr>
</table>
";


print $modeltable;


//44444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444

//---------------------------- plot-------------------------------


$plthtml="
<tr>

<td> <!-- plot column  -->
<table border=0 cellpadding=1 cellspacing=1>
<tr>
<td>
<table border=0 cellpadding=0 cellspacing=0>
<tr>
<td width=$xsizefl align=center>

<div id='div1'>
<a name='link' href='myUrl' target='_blank'><img name='myImage' width='$xsize'></a>
</div>
</td>

</tr>
</table>
</td>

";

print $plthtml;



$bottombuttons="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>


</tr>
</table>
";

print $bottombuttons;

print "
</body>
</html>
";

?>

