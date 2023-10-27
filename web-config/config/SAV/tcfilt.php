<?php

$dosession=1;

if($dosession) {
  ini_set('session.gc_maxlifetime',1800);
  ini_set('session.gc_probability',100);
  session_start();
}

// Report simple running errors
// error_reporting(E_ALL | E_WARNING | E_PARSE);
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



function TCfiltDB ( $inventory ) {

  $stmsDtg=array();
  $dtgsStm=array();
  $dtgsModel=array();

  $modelsDtgStm=array();
  $tausDtgStmModel=array();
  $pltsDtgStmModel=array();
  //$pltfilesDtgStmModel=array();


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
      if($nhash == 1) $stmsDtg=$hash;
      if($nhash == 2) $dtgsStm=$hash;
      if($nhash == 3) $dtgsModel=$hash;
      if($nhash == 4) $modelsDtgStm=$hash;
      if($nhash == 5) $tausDtgStmModel=$hash;
      if($nhash == 6) $pltsDtgStmModel=$hash;
      //if($nhash == 7) $pltfilesDtgStmModel=$hash;
       

    }
    
    //print "NNNNNNNNN $nhash\n";
  }

  //print_r($tausDtgStmModel);
  
  //$rc=array($stmsDtg,$dtgsStm,$dtgsModel,$modelsDtgStm,$tausDtgStmModel,$pltsDtgStmModel,$pltfilesDtgStmModel);
  $rc=array($stmsDtg,$dtgsStm,$dtgsModel,$modelsDtgStm,$tausDtgStmModel,$pltsDtgStmModel);
  return($rc);
  
}


function sortplts($plts) {
  $oplts=array();
  $pltorder=array('vt850','psl','sh200');
  foreach($pltorder as $splt) {
    foreach ($plts as $plt) {
      if($splt == $plt) {
	array_push($oplts,$plt);
      }
    }
  }
  return($oplts);
}


function sortTCfiltModels($models) {

  //print_r($models);
  $omodels=array();
  $stdorder=array('gfs','ecm','ukm','ngp','fim8','fim9');
  $stdorder=array('gfs2','fim8','ngp2','ecm2','ukm2');
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

function model2button($model) {

  $bmodel=$model;
  if($model == 'gfs2') $bmodel='gfs2';
  if($model == 'fim8') $bmodel='fim8';
  if($model == 'fim9') $bmodel='fim9';
  if($model == 'ecmn') $bmodel='ecmn';
  if($model == 'ecm2') $bmodel='ecm2';
  if($model == 'ngp2') $bmodel='ngp2';
  if($model == 'ukm2') $bmodel='ukm2';

  return($bmodel);
}


//function getInitial($tdtg,$tmodel,$tstm) {
function getInitial() {

  //global $stmsDtg,$dtgsStm,$dtgsModel,$modelsDtgStm,$tausDtgStmModel,$pltsDtgStmModel,$pltfilesDtgStmModel;
  global $stmsDtg,$dtgsStm,$dtgsModel,$modelsDtgStm,$tausDtgStmModel,$pltsDtgStmModel;
  global $ptypes;
  global $tdtg,$tstm,$ttau,$tplt,$tmodel,$tptype,$tpmode,$reset;

  $nd=count($stmsDtg);
  $dtgs=array_keys($stmsDtg);
  
  $tdtg=$dtgs[$nd-1];

#  if($tdtg == '') {
#    $tdtg=$dtgs[$nd-1];
#  }

  $laststms=$stmsDtg[$tdtg];

#  if($tstm == '') {
#    $tstm=$laststms[0];
#  }

  $tstm=$laststms[0];

  
  $models=$modelsDtgStm[$tdtg][$tstm];
  $models=sortTCfiltModels($models);

#  if($tmodel == '') {  
#    $tmodel=$models[0];
#  }

  $tmodel=$models[0];

  
  $plts=$pltsDtgStmModel[$tdtg][$tstm][$tmodel];
  $plts=sortplts($plts);
  $tplt=$plts[0];
  
  $taus=$tausDtgStmModel[$tdtg][$tstm][$tmodel];
  
  $ttau=$taus[0];

  for ($i=0; $i <= count($taus); $i++ ) {
    if($taus[$i] == '000') {
      $ttau=$taus[$i];
      break;
    }
  }
  
  $ncards=count($lines);

  $tptype=$ptypes[0];
  
  $tpmode='single';

// session saved between sessions, even if browser closed out

   $reset=1;
  
  }



#------------------------------------------------------------------------------------------
#
# main
#

$xsize=1024;
$ysize=$xsize*(3/4);

$xsizefl=$xsize+24;
$ysizefl=$ysize+128;

#
# input that comes in from the link
#


$tdtg = $_GET['dtg'];
$tstm = $_GET['stm'];
$ttau = $_GET['tau'];
$tplt = $_GET['plt'];
$tmodel = $_GET['model'];
$tptype = $_GET['ptype'];
$tpmode = $_GET['pmode'];

$reset = $_GET['reset'];
$interact = $_GET['interact'];

error_reporting(E_ERROR);

#if( $reset == 1 ) {
#  session_destroy();
#  session_start();
#}

if($interact == '') {
  $interact=0;
} 

$_SESSION['TCFcount']=$_SESSION['TCFcount']+1;
$viewcount=$_SESSION['TCFcount'] ;

//print "qqqqqqqqqqqqqqqffffffffffffffffffffffffff $viewcount\n";

if($viewcount <= 1 || $reset == 1) {

  $ptypes=array('full','vrtm');

  $cwd=getcwd();
  $tcfiltinventory="$cwd/tc/tcfilt/inv.tcfilt.txt";
  
  $rc=TCfiltDB($tcfiltinventory);
  
  $i=0;
  
  $stmsDtg=$rc[$i]; $i++;
  $dtgsStm=$rc[$i]; $i++;
  $dtgsModel=$rc[$i]; $i++;
  $modelsDtgStm=$rc[$i]; $i++;
  $tausDtgStmModel=$rc[$i]; $i++;
  $pltsDtgStmModel=$rc[$i]; $i++;
  //$pltfilesDtgStmModel=$rc[$i]; $i++;
  
  $_SESSION['stmsDtg']=$stmsDtg;
  $_SESSION['dtgsStm']=$dtgsStm;
  $_SESSION['dtgsModel']=$dtgsModel;
  $_SESSION['modelsDtgStm']=$modelsDtgStm;
  $_SESSION['tausDtgStmModel']=$tausDtgStmModel;
  $_SESSION['pltsDtgStmModel']=$pltsDtgStmModel;
  //$_SESSION['pltfilesDtgStmModel']=$pltfilesDtgStmModel;
  $_SESSION['ptypes']=$ptypes;

  getInitial();
  
} else {
  
  $stmsDtg=$_SESSION['stmsDtg'];
  $dtgsStm=$_SESSION['dtgsStm'];
  $dtgsModel=$_SESSION['dtgsModel'];
  $modelsDtgStm=$_SESSION['modelsDtgStm'];
  $tausDtgStmModel=$_SESSION['tausDtgStmModel'];
  $pltsDtgStmModel=$_SESSION['pltsDtgStmModel'];
  //$pltfilesDtgStmModel=$_SESSION['pltfilesDtgStmModel'];
  $ptypes=$_SESSION['ptypes'];

}


//getInitial($tdtg,$tmodel,$tstm);
//  getInitial();


# 
# check if tstm is in the stms by dtg, if not use first
#
  $gotstm=0;
  foreach($stmsDtg[$tdtg] as $dstm) {
    if($dstm == $tstm) $gotstm=1;
  }

  if($gotstm == 0) $tstm=$stmsDtg[$tdtg][0];


$ptaus=$tausDtgStmModel[$tdtg][$tstm][$tmodel];

//print "BBBBBBBBBBBBBBBBBBBB $viewcount $gotstm $tstm\n";
//print "TTTTTTTTTTTTTTTTT  $tdtg $tstm $tmodel\n";
//print_r($ptaus);


#
# make the html
#

$yyyy=substr($tdtg,0,4);

$stmtitle=strtoupper($tstm);
$modeltitle=strtoupper($tmodel);
$toptitle="TCfilt :: $tdtg";

$pagetitle="TCfilt for: <font color=red>$tdtg</font> Current TC: <font color=red>$stmtitle</font> Current Model: <font color=red>$modeltitle</font>";

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


$ptaus=$tausDtgStmModel[$tdtg][$tstm][$tmodel];

$jstaus="ptaus = new Array(";

$nt=count($ptaus);

for ($n=0; $n < $nt; $n++) {

  $ptau=$ptaus[$n];
  $jstaus="$jstaus'$ptau'";

  if($n < $nt-1) {
    $jstaus="$jstaus,";
  }
}
$jstaus="$jstaus );" ;


//------------------------------------------- pswap -------------------------------------
$jspswap="
<script language=\"javascript\" type=\"text/javascript\">

$jstaus

plotdir='tc/tcfilt';
tptype='$tptype';
tdtg='$tdtg';
tstm='$tstm';
ttau='$ttau';
tmodel='$tmodel';
tplt='$tplt';
tyear=tdtg.substr(0,4)
tpmode='$tpmode';
tauinc=0;

function getcurtaundx(ttau,ptaus) {
  for (n in ptaus) {
    if(ptaus[n] == ttau) {
    return(n);
  } 
}




}

function pswap() 
{

if(tauinc == 'ptauinc') {
  nttau=getcurtaundx(ttau,ptaus);
  ntmax=ptaus.length
  nttau++;
  if(nttau > ntmax-1) nttau=0;
  if(nttau < 0) nttau=ntmax-1;
  ttau=ptaus[nttau]
  tauinc=0

//alert(ttau);
}

if(tauinc == 'mtauinc') {
  nttau=getcurtaundx(ttau,ptaus);
  ntmax=ptaus.length
  nttau--;
  if(nttau > ntmax-1) nttau=0;
  if(nttau < 0) nttau=ntmax-1;
  ttau=ptaus[nttau]
  tauinc=0;
}

value=plotdir + '/' + tyear + '/' + tdtg + '/' + tstm + '/' + tmodel + '.' + tdtg + '.' + ttau + '.' + tstm + '.' + tplt + '.' + tptype + '.maxr0.png';
myUrl=value;

/*
if(tpmode == 'loop') {
newInnerHtml=\"<object id='test' data='\" + value+ \"' width=$xsize height=$ysize>\";
newInnerHtml=newInnerHtml.concat(\"</object>\");
newInnerHtml=\"<a name='link' href='myUrl' target='_blank'><img name='myImage' width='$xsize'></a>\";
document.getElementById('div1').innerHTML = newInnerHtml;
tpmode='single';
}
*/

altvalue='NO PLOT FOR.... Model: ' + tmodel + ' Dtg: ' + tdtg + ' Stm: ' + tstm + ' Ttau: ' + ttau + ' Tplt: ' + tplt + ' ...try another Model/Dtg/Stm/Tau/Plt button';

if (value != '') if (document.images) {
  document.images.myImage.src = value;
  document.images.myImage.alt = altvalue;
  var el=document.images.myImage;
  while(el.nodeName.toLowerCase() != 'a') {
    el=el.parentNode;
    el.setAttribute('href',myUrl);
  }
//alert(value)
}

if(tpmode == 'loop') {
  value=plotdir + '/' + tyear + '/' + tdtg + '/' + tstm + '/flanis.' + tmodel + '.' + tplt + '.' + tptype + '.htm';
  newInnerHtml=\"<object id='test' data='\" + value+ \"' width=$xsizefl height=$ysizefl align=center valign=top>\";
  newInnerHtml=newInnerHtml.concat(\"</object>\");
  document.getElementById('div1').innerHTML = newInnerHtml;
//  tpmode='single';
}

}

function loopDivHtml()
{

  value=plotdir + '/' + tyear + '/' + tdtg + '/' + tstm + '/flanis.' + tmodel + '.' + tplt + '.' + tptype + '.htm';

  newInnerHtml=\"<object id='test' data='\" + value+ \"' width=$xsizefl height=$ysizefl align=center valign=top>\";
  newInnerHtml=newInnerHtml.concat(\"</object>\");
  document.getElementById('div1').innerHTML = newInnerHtml;
  //  tpmode='loop';

}

function loadDivHtml(value)
{

  newInnerHtml=\"<object id='test' data='\" + value+ \"' width=$xsizefl height=$ysizefl align=center valign=top>\";
  newInnerHtml=newInnerHtml.concat(\"</object>\");
  document.getElementById('div1').innerHTML = newInnerHtml;

}


var menulinks=new Array()

menulinks[0]='<a href=\"javascript:cvalue=\'doc/wxmap.help.htm\',loadDivHtml(cvalue);\">wxmap help</a>'
menulinks[1]='<a href=\"javascript:cvalue=getW2Url(\'nrl.tc\'),loadW2Html(cvalue,\'window\');\">nrl tc page</a>'
menulinks[2]='<a href=\"javascript:cvalue=\'http://ruc.noaa.gov/hfip/tceps\',loadDivHtml(cvalue);\" >TCeps</a>'
menulinks[3]='<a href=\"https://metocph.nmci.navy.mil/animator.php\">nmfc-jtwc</a>'

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

$Bbptypes='btn75e';

$stmmisc=600;
$stmwidth=$xsizefl-$stmmisc;

$linksdropwidth=200;
$dtgwidth=$xsize-$linksdropwidth;

$row3modelWidth=200;
$row3pltWidth=200;
$row3ptypeWidth=200;
$row3miscWidth=$xsizefl - $row3modelWidth - $row3pltWidth - $row3ptypeWidth;


$stmtable="

<table  border=0 cellpadding=0 cellspacing=0>
<tr>
<td width=$stmwidth valign=middle align=left>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$curstms=$stmsDtg[$tdtg];
sort($curstms);

foreach ($curstms as $stm) {

  $plts=$dtgstmplts[$tdtg][$stm];
  $nplts=count($plts);

  if($interact) {
    $onclick="onClick=\"tstm='${stm}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$stm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
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

$yyyy=substr($tdtg,0,4);
$tstmyyyy="$tstm.$yyyy";

$stmtable="$stmtable

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='TcStruct' name=tctrk
onClick=\"cvalue='tcstruct.php?dtg=$tdtg&storm=$tstm';opentype='page',loadW2Html(cvalue,opentype);\">
</td>

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='TcEps' name=tctrk
onClick=\"cvalue='http://ruc.noaa.gov/hfip/tceps/tceps.php?dtg=$tdtg&stm=$tstmyyyy';opentype='page',loadW2Html(cvalue,opentype);\">
</td>

</tr>
</table>
</td>

<td width=$stmmisc valign=middle align=right>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>


<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue='wx.htm';opentype='window',loadW2Html(cvalue,opentype);\">
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

//$dtgs=$dtgsStm[$tstm];
$dtgs=$dtgsModel[$tmodel];
rsort($dtgs);

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
  
  if($interact) {
    $onclick="onClick=\"tdtg='${dtg}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$dtg&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
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

<!---
<td>
<input type='button' class='btndrop'
onMouseover=\"dropdownmenu(this, event, menulinks, '150px')\" ;
onMouseout=\"delayhidemenu()\";
value='Links...' name='tctrk'\">
</td>
--->

</tr>
</table>
</td>

";
print $dtgtable;




//333333333333333333333333333333333333333333333333333333 button row 3 ---- models ...

$modeltable="
<table  border=0 cellpadding=0 cellspacing=0>

<tr>
<td width=$row3modelWidth valign=middle align=left>

<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$curmodels=$modelsDtgStm[$tdtg][$tstm];
$curmodels=sortTCfiltModels($curmodels);


foreach ($curmodels as $model) {

$bmodel=model2button($model);

  if($interact) {
    $onclick="onClick=\"tmodel='${model}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$model&plt=$tplt&tau=$ttau&ptype=$tptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
  }

  $modeltable="$modeltable
<td>
<input type='button' class='btnsmlmod'
onMouseOver=\"className='btnsmlmodover';\" onMouseOut=\"className='btnsmlmod';\"
value='$bmodel' name=tctrk
$onclick
</td>
";

}

#pppppppppppppppp --  plot bttons

$modeltable="$modeltable
</tr>
</table>
</td>

<td width=$row3pltWidth valign=middle align=right>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$curplts=$pltsDtgStmModel[$tdtg][$tstm][$tmodel];
$curplts=sortplts($curplts);

foreach ($curplts as $plt) {

  $nplts=count($curplts);

  if($interact) {
    $onclick="onClick=\"tplt='${plt}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$plt&ptype=$tptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
  }


  $modeltable="$modeltable
<td>
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='$plt' name=tctrk
$onclick
</td>

";

}


#ppppppppppppppp -- plot type buttons

$modeltable="$modeltable
</tr>
</table>
</td>

<td width=$row3ptypeWidth valign=middle align=left>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";



$onclickinteract="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=$tpmode&interact=1';opentype='page',swaphtm();\">";
$onclickphpmode="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=$tpmode&interact=0';opentype='page',swaphtm();\">";
//$onclickphpmode="onClick=\"cvalue='$phpfile?dtg=$tdtg&interact=0'; opentype='page',swaphtm();\">";
$onclickreset="onClick=\"cvalue='$phpfile?reset=1'; opentype='page',swaphtm();\">";
$onclickloop="onclick=\"tpmode='loop';loopDivHtml()\"/>";
$onclickloop="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=loop'; opentype='page',swaphtm();\">";
$onclicksingle="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=single'; opentype='page',swaphtm();\">";


foreach ($ptypes as $ptype) {

  if($interact) {
    $onclick="onClick=\"tptype='${ptype}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$ptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
  }

//

  $modeltable="$modeltable
<td>
<input type='button' class='${Bbptypes}'
onMouseOver=\"className='${Bbptypes}over';\" onMouseOut=\"className='${Bbptypes}';\"
value='$ptype' name=tctrk
$onclick
</td>
";

}

if($tpmode == 'single') {
$loopmodehtml="
<td>
<input type='button' class='${Bbtnloop}'
onMouseOver=\"className='${Bbtnloop}over';\" onMouseOut=\"className='${Bbtnloop}';\"
value='LOOP' name=tctrk
$onclickloop
</td>
";

} elseif ($tpmode == 'loop') {

$loopmodehtml="
<td>
<input type='button' class='${Bbtnsingle}'
onMouseOver=\"className='${Bbtnsingle}over';\" onMouseOut=\"className='${Bbtnsingle}';\"
value='Single' name=tctrk
$onclicksingle
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


$taubuttons="
<td valign=top align=center width=50> <!-- button  -->
";

if(count($ptaus) > 0) {

  foreach ($ptaus as $tau) {

  if($interact) {
    $onclick="onClick=\"ttau='${tau}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$tau&plt=$tplt&ptype=$tptype&pmode=single'; opentype='page',swaphtm();\">";
  }

    $taubuttons="
$taubuttons
<input type='button' class='btnsmltau'
onMouseOver=\"className='btnsmltauover';\"
onMouseOut=\"className='btnsmltau';\"
value='$tau' name=taub
$onclick
";
  }

// + - tau buttons
    $onclick="onClick=\"tauinc='mtauinc',pswap();\">";
    $taubuttons="
$taubuttons
<input type='button' class='btnsmltau2'
onMouseOver=\"className='btnsmltau2over';\"
onMouseOut=\"className='btnsmltau2';\"
value='<' name=taub
$onclick
";

    $onclick="onClick=\"tauinc='ptauinc',pswap();\">";
    $taubuttons="
$taubuttons
<input type='button' class='btnsmltau2'
onMouseOver=\"className='btnsmltau2over';\"
onMouseOut=\"className='btnsmltau2';\"
value='>' name=taub
$onclick
";


$curmodels=$modelsDtgStm[$tdtg][$tstm];
$curmodels=sortTCfiltModels($curmodels);

foreach ($curmodels as $model) {

$bmodel=model2button($model);

  if($interact) {
    $onclick="onClick=\"tmodel='${model}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$model&plt=$tplt&tau=$ttau&ptype=$tptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
  }

    $taubuttons="
$taubuttons
<input type='button' class='btnsmlmod'
onMouseOver=\"className='btnsmlmodover';\" onMouseOut=\"className='btnsmlmod';\"
value='$bmodel' name=tctrk
$onclick
";

}



#pppppppppppppppp --  plot bttons

$taubuttons="$taubuttons
";

$curplts=$pltsDtgStmModel[$tdtg][$tstm][$tmodel];
$curplts=sortplts($curplts);

foreach ($curplts as $plt) {

  $nplts=count($curplts);

  if($interact) {
    $onclick="onClick=\"tplt='${plt}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$plt&ptype=$tptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
  }

  $taubuttons="$taubuttons
<input type='button' class='btnsml'
onMouseOver=\"className='btnsmlover';\" onMouseOut=\"className='btnsml';\"
value='$plt' name=tctrk
$onclick

";

}



$BbptypesSml='btn40e';

foreach ($ptypes as $ptype) {

  if($interact) {
    $onclick="onClick=\"tptype='${ptype}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$ptype&pmode=$tpmode'; opentype='page',swaphtm();\">";
  }

//

    $taubuttons="
$taubuttons
<input type='button' class='${BbptypesSml}'
onMouseOver=\"className='${BbptypesSml}over';\" onMouseOut=\"className='${BbptypesSml}';\"
value='$ptype' name=tctrk
$onclick
";

}



}


$taubuttons="
$taubuttons
</td>
</tr>
</table>
</tr>
";

print $taubuttons;


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

