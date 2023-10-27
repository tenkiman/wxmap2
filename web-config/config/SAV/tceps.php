<?php

$dosession=1;

if($dosession) {
  ini_set('session.gc_maxlifetime',1800);
  ini_set('session.gc_probability',100);
  session_start();
}
// Report simple running errors
//error_reporting(E_ALL | E_WARNING | E_PARSE);
error_reporting(E_ERROR);

require 'tc.php';
require 'phplocal.php';
require 'phpwxmap.php';

$phpfile='tceps.php';

function TCepsDB ( $inventory ) {

  $stmsDtg=array();
  $allstmsDtg=array();
  $dtgsStm=array();
  $dtgsModel=array();

  $modelsDtgStm=array();
  $tausDtgStmModel=array();
  $ptypesDtgStmModel=array();

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
    $keyword=$lines[$n][0];
    if($keyword == 'hash') {
      $nl=$lines[$n][2];
      $nk=$lines[$n][1];
      $ib=$n+1;
      $ie=$ib+$nl;
      $hash=LoadHash($lines,$ib,$ie,$nk);
      $n=$n+$nl+1;
      $nhash++;
      if($nhash == 1) $stmsDtg=$hash;
      if($nhash == 2) $allstmsDtg=$hash;
      if($nhash == 3) $dtgsStm=$hash;
      if($nhash == 4) $dtgsModel=$hash;
      if($nhash == 5) $modelsDtgStm=$hash;
      if($nhash == 6) $tausDtgStmModel=$hash;
      if($nhash == 7) $ptypesDtgStmModel=$hash;

    }
  }

  $rc=array($stmsDtg,$allstmsDtg,$dtgsStm,$dtgsModel,$modelsDtgStm,$tausDtgStmModel,$ptypesDtgStmModel);
  return($rc);
  
}


function GotProductStm($stm,$curstms) {
  
  $rc=0;
  foreach($curstms as $curstm) {
    if($stm == $curstm)  {
      $rc=1;
      break;
    }
  }
  return($rc);

}

function sortplts($plts) {
  $oplts=array();
  $pltorder=array('hit','skp','strike','plumes');
  foreach($pltorder as $splt) {
    foreach ($plts as $plt) {
      if($splt == $plt) {
	array_push($oplts,$plt);
      }
    }
  }
  return($oplts);
}


function sortTCepsModels($models) {
  $stdorder=array('ncep','esrl','cmc','ukmo','ecmt','ecm_eps');
  return($stdorder);

}


function model2button($model) {

  $bmodel=$model;
  if($model == 'ncep') $bmodel='ncep GEFS';
  if($model == 'esrl') $bmodel='esrl FIM8(EnKF)';
  if($model == 'ecmt') $bmodel='ecmwf EPS (TIGGE)';
  if($model == 'ecm_eps') $bmodel='ecmwf EPS (plots)';
  if($model == 'ukmo') $bmodel='ukmo MOGREPS';
  if($model == 'cmc') $bmodel='cmc.ca CEPS)';

  return($bmodel);
}

function model2tcfiltmodel($model) {

  $bmodel=$model;
  if($model == 'ncep') $bmodel='gfs2';
  if($model == 'ecmt') $bmodel='ecm2';
  if($model == 'ecm_eps') $bmodel='ecm2';
  if($model == 'ukmo') $bmodel='ukm2';
  if($model == 'cmc') $bmodel='gfs2';

  return($bmodel);
}


function stm2button($stm) {
  $ostm=substr($stm,0,3);
  return($ostm);
}

function ptype2button($ptype) {
  if($ptype == 'hit') $optype='HIT';
  if($ptype == 'skp') $optype='StkP';
  if($ptype == 'veri') $optype='VERI';
  if($ptype == 'strike') $optype='StkP';
  if($ptype == 'plumes') $optype='IntMgrm';
  return($optype);
}


function tau2button($tau) {
  if($tau == 'single') {
    $otau='5day';
  } else if($tau == 'loop.gif') {
    $otau='AniGif';
  } else {
    $otau=$tau;
  }
  return($otau);
}


function getInitial() {

  require 'phpglobal.php';

  $nd=count($stmsDtg);
  $dtgs=array_keys($stmsDtg);
  
  $tdtg=$dtgs[$nd-1];

  $laststms=$stmsDtg[$tdtg];

  $tstm=$laststms[0];

  $models=$modelsDtgStm[$tdtg][$tstm];
  $models=sortTCepsModels($models);

  if(count($models) > 0) {
    $tmodel=$models[0];
  } else {
    print "WWW no models in getInitial $tdtg $tstm\n";
    exit;
  }
  
  $plts=$ptypesDtgStmModel[$tdtg][$tstm][$tmodel];
  $plts=sortplts($plts);
  $tplt=$plts[0];
  
  $taus=$tausDtgStmModel[$tdtg][$tstm][$tmodel];
  
  $ttau=$taus[0];

  for ($i=0; $i <= count($taus); $i++ ) {
    $gotloop=0;
    if($taus[$i] == 'loop.gif') {
      $ttau=$taus[$i];
      $gotloop=1;
    }
  }
  if($gotloop == 0) {
    if($taus[$i] == '000') {
      $ttau=$taus[$i];
      break;
    }
  }

  
  $ncards=count($lines);
  $tptype=$ptypes[0];
  $tpmode='single';
  $xsize=1024;
  $_SESSION['EPSxsize']=$xsize;
  $_SESSION['EPSmodel']=$tmodel;
  $_SESSION['EPSdtg']=$tdtg;
  $_SESSION['EPSstm']=$tstm;


// session saved between sessions, even if browser closed out

   $reset=0;

//   print "III000 $tdtg, $tstm, $ttau, $tplt, $tmodel, $tptype, $tpmode, $reset, $interact \n";	
//   print "GGG000 M: $gottmodel S: $gottstm D: $gottdtg R: $gotreset\n";

  }


function GetCommandLine() {

  require 'phpglobal.php';
  
  $gottdtg=0;
  if($_GET['dtg'] != '') {
    $gottdtg=1;
    $tdtg = $_GET['dtg'];
    $_SESSION['EPSdtg']=$tdtg;
  } else {
    $tdtg=$_SESSION['EPSdtg'];
  }

  $gottstm=0;
  if($_GET['stm'] != '') {
    $gottstm=1;
    $tstm = $_GET['stm'];
    $_SESSION['EPSstm']=$tstm;
  } else {
    $tstm=$_SESSION['EPSstm'];
  }


  $ttau = $_GET['tau'];
  $tplt = $_GET['plt'];

  $gottmodel=0;
  if($_GET['model'] != '') {
    $gottmodel=1;
    $tmodel = $_GET['model'];
    $_SESSION['EPSmodel']=$tmodel;
  } else {
    $tmodel=$_SESSION['EPSmodel'];
  }
  
  if($_GET['ptype'] != '') {
    $tptype = $_GET['ptype'];
    $_SESSION['EPSptype']=$tptype;
  } else {
    $tptype=$_SESSION['EPSptype'];
  }

  
  if($_GET['pmode'] != '') {
    $tpmode = $_GET['pmode'];
    $_SESSION['EPSpmode']=$tpmode;
  } else {
    $tpmode=$_SESSION['EPSpmode'];
  }
  
  
  if($_GET['xsize'] != '') {
    $xsize = $_GET['xsize'];
    $_SESSION['EPSxsize']=$xsize;
  } else {
    $xsize=$_SESSION['EPSxsize'];
  }

  if($_GET['deltaxsize'] != '') {
    $deltaxsize = $_GET['deltaxsize'];
    $xsize=$_SESSION['EPSxsize'];
    $xsize=$xsize+$deltaxsize;
    $_SESSION['EPSxsize']=$xsize;
    $_SESSION['EPSdeltaxsize']=$deltaxsize;
  }

  $gotreset=0;
  if($_GET['reset'] != '') {
    $gotreset=1;
    $reset = $_GET['reset'];
  } else {
    $reset=0;
  }

  //  print "GetCommandline $gotreset\n";
  

}

function GotStmDtg($stm,$dtg) {

  require 'phpglobal.php';

  $rc=0;
  foreach($stmsDtg[$tdtg] as $dstm) {
    if($dstm == $tstm) {
      $rc=1;
      return(1);
    }
  }
  return($rc);
}


function GotStmDtgModel($stm,$dtg,$model) {

  require 'phpglobal.php';

  $rc=0;
  $emodels=$modelsDtgStm[$dtg][$stm];
  foreach($emodels as $dmodel) {
    if($dmodel == $model) {
      $rc=1;
      return($rc);
    }
  }
  return($rc);
}


// find stm for a $tmodel and $dtg

function FindStmDtgModel($dtg) {

  require 'phpglobal.php';

  $curstms=$stmsDtg[$dtg];
  sort($curstms);
  foreach ($curstms as $stm) {
    $gotstm=GotStmDtgModel($stm,$tdtg,$tmodel);
    if($gotstm) {
      $tstm=$stm;
      return($stm);
    }
  }
  return(0);
}

function FindBestModelDtgStm() {

  require 'phpglobal.php';

  $gotmodel=0;
  $smodels=$modelsDtgStm[$tdtg][$tstm];
  $stdorder=array('ncep','esrl','cmc','ukmo','ecmt','ecm_eps');
  foreach ($stdorder as $stdmodel) {
    foreach ($smodels as $smodel) {
      if($smodel == $stdmodel) {
         $tmodel=$smodel;
	 $gotmodel=1;
         return(0);
      }
    }
  }
  if($gotmodel == 0) {
    print "EEError no models for tdtg: $tdtg  stm: $tstm";
  } 
}


function CmdlineStmDtgModel() {
  require 'phpglobal.php';
  $rc=0;
  if($gottstm && $gottdtg && $gottmodel) $rc=1;
  return($rc);
}

function CmdlineStmDtg() {
  require 'phpglobal.php';
  $rc=0;
  if($gottstm && $gottdtg && $gottmodel == 0) $rc=1;
  return($rc);
}

function CmdlineModel() {
  require 'phpglobal.php';
  $rc=0;
  if($gottstm == 0 && $gottdtg == 0 && $gottmodel) $rc=1;
  return($rc);
}


function GetLLBounds() {
  global $tdtg,$tstm,$ttau,$tplt,$tmodel,$tptype,$tpmode,$reset,$xsize;
  global $lonL,$lonR,$latT,$latB;
   
  $yyyy=substr($tdtg,0,4);
  $dbfile="$yyyy/$tdtg/db.esrl.eps.pagell.$tstm.$tdtg.txt";
  //print "DDD $dbfile\n";
  $cards=file_get_contents($dbfile);
  $cards=explode("\n",$cards);
  foreach ($cards as $card) {
    $tt=pysplit($card,' ');
    //print_r($tt);
    $lonL=$tt[2];
    $lonR=$tt[4];
    $latT=$tt[1];
    $latB=$tt[3];
    $dlon=$lonR-$lonL;
    //print "QQQQQQQ $dlon $lonR $lonL\n";
    if($lonL <= -180.0) {
       $lonL=$lonL+360.0;
       //$lonR=$lonL+$dlon;
    }

    $rc=array($lonL,$lonR,$latT,$latB);
    return($rc);
   
  }

  print "LLL   lonL: $lonL lonR: $lonR latT: $latT latB: $latB\n";

}


function SetDtgsPltsTaus() {

  require 'phpglobal.php';

  $dtgs=$dtgsModel[$tmodel];
  $plts=$ptypesDtgStmModel[$tdtg][$tstm][$tmodel];
  $plts=sortplts($plts);
  $tplt=$plts[0];
  $taus=$tausDtgStmModel[$tdtg][$tstm][$tmodel];
  $ttau=$taus[0];

}


function chkCommandLine() {

  require 'phpglobal.php';

  //print "CCCCIII $tdtg, $tstm, $ttau, $tplt, $tmodel, $tptype, $tpmode, $reset, $interact \n";	
  //print "CCCCGGG M: $gottmodel S: $gottstm D: $gottdtg R: $gotreset\n";

  #
  # MAIN reset
  #

  if($gotreset) {
//    print "RRR: $tdtg, $tstm, $ttau, $tplt, $tmodel, $tptype, $tpmode, $reset, $interact\n";	
    return(1);
  }

  #
  # model reset...
  #
  if( CmdlineModel() ) {
    $dtgs=$dtgsModel[$tmodel];
    $nd=count($dtgs);
    $tdtg=$dtgs[$nd-1];
    
    $gotmodel=0;
    $dstms=$stmsDtg[$tdtg];
    foreach($dstms as $dstm) {
      $emodels=$modelsDtgStm[$tdtg][$dstm];
      foreach($emodels as $dmodel) {
	if($dmodel == $tmodel) {
	  $gotmodel=1;
	  $tstm=$dstm;
	  if($tmodel != 'ecm_eps') {
	    $tptype='hit';
	    $tplt='hit';
	    $ttau='loop.gif';
	  } else {
	    $tplt='strike';
	    $ttau='single';
	  }

	  //print "MMMMMMMMM model reset: tdtg: $tdtg  tstm: $tstm  tmodel: $tmodel tplt: $tplt ttau: $ttau\n";
	  $_SESSION['EPSmodel']=$tmodel;
	  $_SESSION['EPSstm']=$tstm;
	  $_SESSION['EPSdtg']=$tdtg;
	  return($gotmodel);
	}
      }
    }

    if($gotmodel == 0) {
      print "EEE unable to find stm for model: $tmodel  dtg: $tdtg\n";
      print "MMMMMMMMM model reset: tdtg: $tdtg  tstm: $tstm  tmodel: $tmodel\n";
    }
    return(1);
  }
  

  if( CmdlineStmDtg() ) {

    require 'phpglobal.php';

    if( GotStmDtg() ) {
      
      $tmodel=$_SESSION['EPSmodel'];
      // not sure we want to do this here... if($tstm != 0) FindBestModelDtgStm();

      if( GotStmDtgModel($tstm,$tdtg,$tmodel) ) {
	SetDtgsPltsTaus();
	return(1);

      } else {
        FindBestModelDtgStm();	
	      }

    } else {

      $tstm=FindStmDtgModel($tdtg);
      if($tstm == 0) {
	 $tdtg=dtginc($tdtg,-6);
	 $tstm=FindStmDtgModel($tdtg);
	 if($tstm != 0) {
	   FindBestModelDtgStm();	
	 }
	 if($tstm == 0) {
	   $tdtg=dtginc($tdtg,-6);
	   $tstm=FindStmDtgModel($tdtg);
	   if($tstm != 0) FindBestModelDtgStm();
	   if($tstm == 0) {
	     print "EEE unable to find eps for $tdg $tstm; hit the reset button\n";
	     return(0);
	   }
	 }  
      }
    } 


  }


  if(GotStmDtg() && GotStmDtgModel($tstm,$tdtg,$tmodel) ) {

    $dtgs=$dtgsModel[$tmodel];
    $plts=$ptypesDtgStmModel[$tdtg][$tstm][$tmodel];
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
    $ttau='loop.gif';
    $rc=0;
    return($rc);
  } 

  if(GotStmDtg()) {

    $tmodel=$_SESSION['EPSmodel'];

    //print "22222222222222222222222222222 $tdtg $tstm $tmodel";
    $dtgs=$dtgsModel[$tmodel];
    $plts=$ptypesDtgStmModel[$tdtg][$tstm][$tmodel];
    $plts=sortplts($plts);
    $tplt=$plts[0];
    
    $taus=$tausDtgStmModel[$tdtg][$tstm][$tmodel];
    
    $ttau=$taus[0];
    
    for ($i=0; $i <= count($taus); $i++ ) {
      //print "TTTT $taus[$i]\n";
      if($taus[$i] == '000') {
	$ttau=$taus[$i];
	break;
      }
    }
    $rc=0;
    return($rc);

  }


  
  return(0);

# 
# check if tstm is in the stms by dtg, if not use first
#
  $gotstm=0;
  foreach($stmsDtg[$tdtg] as $dstm) {
    if($dstm == $tstm) $gotstm=1;
  }

  if($gotstm == 0){
    $tstm=$stmsDtg[$tdtg][0];
  }


  $gotmodel=0;  
  $dstms=$stmsDtg[$tdtg];
  foreach($dstms as $dstm) {
    $emodels=$modelsDtgStm[$tdtg][$dstm];
    print "EEE $dstm $tdtg $tmodel";
    print_r($emodels);
    foreach($emodels as $dmodel) {
      if($dmodel == $tmodel) {
	$gotmodel=1;
	$tstm=$dstm;
	next;
      }
    }

  }

#print "PPP000 $tstm $tdtg $tmodel $gotmodel PPP\n";

  if($gotmodel == 0) $tmodel=$emodels[0];
  if($gotdtgs == 0) {
      $dtgs=$dtgsModel[$tmodel];
    }  

# print "PPP $tstm $tdtg $tmodel $gotmodel PPP\n";
  $plts=$ptypesDtgStmModel[$tdtg][$tstm][$tmodel];
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


//print "III $tdtg, $tstm, $ttau, $tplt, $tmodel, $tptype, $tpmode, $reset, $interact\n";	


  }



#------------------------------------------------------------------------------------------
#
# main
#


GetCommandLine();


#
# input that comes in from the link
#

$xsizeMenu=1024;
$ysize=$xsize*(3/4);

$xsizefl=$xsizeMenu+24;
$ysizefl=$ysize+128;

error_reporting(E_ERROR);

if( $reset == 1 ) {
  session_destroy();
  session_start();
}

if($interact == '') {
  $interact=0;
} 

$_SESSION['EPScount']=$_SESSION['EPScount']+1;
$viewcount=$_SESSION['EPScount'] ;
//print "VVVV $viewcount\n";

if($viewcount <= 1) {

  $ptypes=array('full','vrtm');

  $cwd=getcwd();
  $tcepsinventory="inv.tceps.txt";
  
  $rc=TCepsDB($tcepsinventory);
  
  $i=0;
  
  $stmsDtg=$rc[$i]; $i++;
  $allstmsDtg=$rc[$i]; $i++;
  $dtgsStm=$rc[$i]; $i++;
  $dtgsModel=$rc[$i]; $i++;
  $modelsDtgStm=$rc[$i]; $i++;
  $tausDtgStmModel=$rc[$i]; $i++;
  $ptypesDtgStmModel=$rc[$i]; $i++;

  //$pltfilesDtgStmModel=$rc[$i]; $i++;
  
  $_SESSION['EPSstmsDtg']=$stmsDtg;
  $_SESSION['EPSallstmsDtg']=$allstmsDtg;
  $_SESSION['EPSdtgsStm']=$dtgsStm;
  $_SESSION['EPSdtgsModel']=$dtgsModel;
  $_SESSION['EPSmodelsDtgStm']=$modelsDtgStm;
  $_SESSION['EPStausDtgStmModel']=$tausDtgStmModel;
  $_SESSION['EPSptypesDtgStmModel']=$ptypesDtgStmModel;
  $_SESSION['EPSptypes']=$ptypes;

  //$_SESSION['pltfilesDtgStmModel']=$pltfilesDtgStmModel;

  getInitial();
  
} else {
  
  $stmsDtg=$_SESSION['EPSstmsDtg'];
  $allstmsDtg=$_SESSION['EPSallstmsDtg'];
  $dtgsStm=$_SESSION['EPSdtgsStm'];
  $dtgsModel=$_SESSION['EPSdtgsModel'];
  $modelsDtgStm=$_SESSION['EPSmodelsDtgStm'];
  $tausDtgStmModel=$_SESSION['EPStausDtgStmModel'];
  $ptypesDtgStmModel=$_SESSION['EPSptypesDtgStmModel'];
  //$pltfilesDtgStmModel=$_SESSION['pltfilesDtgStmModel'];
  $ptypes=$_SESSION['EPSptypes'];

  if($reset == 1) {
    getInitial();
    $_SESSION['EPScount']=1;
    $_SESSION['EPSxsize']=$xsize;
  }


}

chkCommandLine();
$rc=GetLLBounds();
$lonL=$rc[0]; 
$lonR=$rc[1]; 
$latT=$rc[2]; 
$latB=$rc[3]; 


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
$toptitle="Tceps :: $tdtg";

$pagetitle="Tceps for: <font color=red>$tdtg</font> Current TC: <font color=red>$stmtitle</font> Current Model: <font color=red>$modeltitle</font>";

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

//$jstaus

plotdir='.';
tptype='$tptype';
tdtg='$tdtg';
tstm='$tstm';
ttau='$ttau';
tmodel='$tmodel';
tplt='$tplt';
veri=0;
lsdata=0;
setveri=0;
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

if(setveri == 1 && veri == 1) {
  veri=0;
  setveri=0;
}

if(setveri == 1 && veri == 0) {
  veri=1;
  setveri=0;
}



if(tmodel == 'ecm_eps' ) {
//2009/2009070712/ec.eps.plumes.03E.2009.2009070712.png
  value=plotdir + '/' + tyear + '/' + tdtg + '/ec.eps' + '.' + tplt + '.'  + tstm  + '.' + tdtg + '.png';
  tplt='hit';
} else if(ttau == 'loop.gif') {
//2009/2009070712/esrl.eps.ecmt.hit.loop.03E.2009.2009070712.gif
  value=plotdir + '/' + tyear + '/' + tdtg + '/esrl.eps' + '.' + tmodel + '.' + tplt + '.loop.'  + tstm   + '.' + tdtg + '.gif';
  if(veri == 1) {
    value=plotdir + '/' + tyear + '/' + tdtg + '/esrl.eps.veri' + '.' + tmodel + '.' + tplt + '.loop.'  + tstm   + '.' + tdtg + '.gif';
  }

} else {
  value=plotdir + '/' + tyear + '/' + tdtg + '/esrl.eps' + '.' + tmodel + '.' + tplt + '.'  + tstm   + '.' + ttau + '.png';
  if(veri == 1) {
    value=plotdir + '/' + tyear + '/' + tdtg + '/esrl.eps.veri' + '.' + tmodel + '.' + tplt + '.'  + tstm   + '.' + ttau + '.png';
  }
}
//alert(value);
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

menulinks[0]='<a href=\"javascript:cvalue=\'http://ruc.noaa.gov/hfip/enkf\',loadW2Html(cvalue,\'window\');\">HFIP EnKF</a>'
menulinks[2]='<a href=\"javascript:cvalue=\'http://ruc.noaa.gov/tracks\',loadW2Html(cvalue,\'window\');\">Paula\'s TCeps page</a>'
menulinks[1]='<a href=\"javascript:cvalue=getW2Url(\'nrl.tc\'),loadW2Html(cvalue,\'window\');\">NRL TC page</a>'


<!-- Idea by:  Nic Wolfe -->
<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->
<!-- Begin
function popUp(URL) {

tyear=tdtg.substr(0,4)

URL=tyear + '/' + tdtg + '/adeck.' + tmodel + '.' + tstm + '.' + tdtg + '.txt'
 
day = new Date();
id = day.getTime();
eval(\"page\" + id + \" = window.open(URL, '\" + id + \"', 'toolbar=1,scrollbars=1,location=1,statusbar=1,menubar=1,resizable=1,width=1024,height=768');\");
}
// End -->

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
$Bbtnzoom='btn35t';

$stmmisc=600;
$stmwidth=$xsizefl-$stmmisc;

$linksdropwidth=200;
$dtgwidth=$xsize-$linksdropwidth;

$row3modelWidth=200;
$row3pltWidth=200;
$row3ptypeWidth=200;
$row3miscWidth=$xsizefl - $row3modelWidth - $row3pltWidth - $row3ptypeWidth;


$onclickinteract="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=$tpmode&interact=1';opentype='page',swaphtm();\">";
$onclickphpmode="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm';opentype='page',swaphtm();\">";
//$onclickphpmode="onClick=\"cvalue='$phpfile?dtg=$tdtg&interact=0'; opentype='page',swaphtm();\">";
$onclickreset="onClick=\"cvalue='$phpfile?reset=1'; opentype='page',swaphtm();\">";
$onclickloop="onclick=\"tpmode='loop';loopDivHtml()\"/>";
$onclickloop="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=loop'; opentype='page',swaphtm();\">";
$onclicksingle="onClick=\"cvalue='$phpfile?dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype&pmode=single'; opentype='page',swaphtm();\">";
$onclickZoomIn="onClick=\"cvalue='$phpfile?deltaxsize=200&dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype'; opentype='page',swaphtm();\">";
$onclickZoomOut="onClick=\"cvalue='$phpfile?deltaxsize=-200&dtg=$tdtg&stm=$tstm&model=$tmodel&tau=$ttau&plt=$tplt&ptype=$tptype'; opentype='page',swaphtm();\">";

$stmtable="

<table  border=0 cellpadding=0 cellspacing=0>
<tr>
<td width=$stmwidth valign=middle align=left>
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$curstms=$stmsDtg[$tdtg];
$allcurstms=$allstmsDtg[$tdtg];
$allstms=$curstms+$allcurstms;
$allstms=uniq($allstms);

foreach ($allstms as $stm) {

  $bstm=stm2button($stm);
  $plts=$dtgstmplts[$tdtg][$stm];
  $nplts=count($plts);

  $btcol='btn50red';
  $btcolover='btn50redover';

  if($interact) {
    $onclick="onClick=\"tstm='${stm}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?stm=$stm&dtg=$tdtg'; opentype='page',swaphtm();\">";
  }

  $gotstm=GotStmDtgModel($stm,$tdtg,$tmodel);	
  if($gotstm == 0) {
    $btcol='btn50darkorange';
    $btcolover='btn50darkorangeover';
  }

  $gotallstm=GotProductStm($stm,$curstms);
  if($gotallstm == 0) {
    $btcol='btn50grey';
    $btcolover='btn50grey';
    $onclick='';
  }


  $stmtable="$stmtable
<td>
<input type='button' class='$btcol'
onMouseOver=\"className='$btcolover';\" onMouseOut=\"className='$btcol';\"
value='$bstm' name=tctrk
$onclick
</td>
";


}

$tcfiltmodel=model2tcfiltmodel($tmodel);
$tstm3=substr($tstm,0,3);


if($publiconly != 1) {

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
value='TcFilt' name=tctrk
//http://kishou.fsl.noaa.gov/wxmap2/tcfilt.php?dtg=2009042718&stm=27S&model=gfs2&tau=000&plt=vt850&ptype=full&pmode=single
onClick=\"cvalue='tcfilt.php?dtg=$tdtg&stm=$tstm3&model=gfs2&tau=000&plt=vt850&ptype=full&pmode=single'; opentype='page',swaphtm();\">
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

<!--- SSSSSSSSSSSSSSSSSSS size buttons --->

<td>
<input type='button' class='${Bbtnzoom}'
onMouseOver=\"className='${Bbtnzoom}over';\" onMouseOut=\"className='${Bbtnzoom}';\"
value='Zm++' name=tctrk
$onclickZoomIn
</td>

<td>
<input type='button' class='${Bbtnzoom}'
onMouseOver=\"className='${Bbtnzoom}over';\" onMouseOut=\"className='${Bbtnzoom}';\"
value='Zm--' name=tctrk
$onclickZoomOut
</td>

<td>
<input type='button' class='${Bbtnreset}'
onMouseOver=\"className='${Bbtnreset}over';\" onMouseOut=\"className='${Bbtnreset}';\"
value='RESET' name=tctrk
$onclickreset
</td>
";

if($publiconly != 1) {

$stmtable="$stmtable

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='WxMAP2.H' name=tctrk
onClick=\"cvalue='wx.htm';opentype='page',loadW2Html(cvalue,opentype);\">
</td>

";

}

//onClick=\"cvalue='doc/',loadDivHtml(cvalue);\">

$stmtable="$stmtable

<td>
<input type='button' class='btn100'
onMouseOver=\"className='btn100over';\" onMouseOut=\"className='btn100';\"
value='doc...' name=tctrk
onClick=\"cvalue='doc/';opentype='window',loadW2Html(cvalue,opentype);\">
</td>

<td>
<input type='button' class='${Bbtndrop}'
onMouseover=\"dropdownmenu(this, event, menulinks, '250px')\" ;
onMouseout=\"delayhidemenu()\";
value='Links...' name='tctrk'\">
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

rsort($dtgs);

$ndtgs=count($dtgs);
$ndtgsmax=12;
$rc=findcurdtgibie($tdtg,$dtgs,$ndtgs,$ndtgsmax);

$idtgb=$rc[0];
$idtge=$rc[1];
$icurdtg=$rc[2];

for ($i=$idtgb ; $i<$idtge ; $i++) { 
  $dtg=$dtgs[$i];

  if($i == $icurdtg) {
    $btnclass='btndtgacur';
  } else {
    $btnclass='btndtga';
  }
  
  if($interact) {
    $onclick="onClick=\"tdtg='${dtg}',pswap();\">";
  } else {
    $onclick="onClick=\"cvalue='$phpfile?dtg=$dtg&stm=$tstm'; opentype='page',swaphtm();\">";
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



//333333333333333333333333333333333333333333333333333333333333333333  model, plot tau buttons-------------------------------
$taubuttons="
<table border=0 cellpadding=0 cellspacing=0 class='button'>
<tr>
";

$btnanim='btn50a';
$btntauall='btnsmltaua';
$btnmodel='btn90grna';
$btntauloop='btn50loopa';
$btndata='btn50b';
$btnveri='btn50etca';
$btntau5day='btn50taua';

$curmodels=$modelsDtgStm[$tdtg][$tstm];
$curmodels=sortTCepsModels($curmodels);

foreach ($curmodels as $model) {

  $bmodel=model2button($model);

  $taus=$tausDtgStmModel[$tdtg][$tstm][$model];

  $taubuttons="
$taubuttons

<td>
<input type='button' class='$btnmodel'
value='${bmodel}' name=taub
onClick=\"cvalue='$phpfile?model=$model';opentype='page',swaphtm();\">
</td>
";
  

  $curptypes=$ptypesDtgStmModel[$tdtg][$tstm][$model];

  if(count($taus) > 0) {

    if($model != 'ecm_eps') {
// veri button


      $taubuttons="
$taubuttons

<td>
<input type='button' class='${btndata}'
onMouseOver=\"className='${btndata}over';\"
onMouseOut=\"className='${btndata}';\"
value='Data...' name=taub
onClick=\"javascript:popUp('test.txt');\">
</td>

<td>
<input type='button' class='${btnveri}'
onMouseOver=\"className='${btnveri}over';\"
onMouseOut=\"className='${btnveri}';\"
value='VERI' name=taub
onClick=\"setveri='1';tmodel='${model}',pswap();\">
</td>
";

    }
    foreach ($curptypes as $ptype) {

      $bptype=ptype2button($ptype);

      if($ptype == 'strike' || $ptype == 'plumes') {

	if($interact == 1) {
	  $onclick="onClick=\"tdtg='${dtg}',pswap();\">";
	  $onclick="onClick=\"tplt='${ptype}';tmodel='${model}',pswap();\">";
	} else {
	  $urltaufile="$phpfile?dtg=$tdtg&storm=$tstm&model=$model&plt=$ptype";
	  $onclick="onClick=\"cvalue='$urltaufile'; opentype='page',swaphtm();\">";
	}

	$taubuttons="
$taubuttons
<td>
<input type='button' class='${btnanim}'
onMouseOver=\"className='${btnanim}over';\"
onMouseOut=\"className='${btnanim}';\"
value='${bptype}' name=taub
$onclick
</td>
";

      } else {
      $taubuttons="
$taubuttons
<td>
<input type='button' class='${btnanim}'
onMouseOver=\"className='${btnanim}over';\"
onMouseOut=\"className='${btnanim}';\"
value='${bptype}' name=taub
onClick=\"tplt='${ptype}';tmodel='${model}',pswap();\">
</td>
";
      }

    }
    foreach ($taus as $tau) {

      $otau=tau2button($tau);

      $urltaufile="tcstruct.php?dtg=$tdtg&storm=$tstm&model=$model&ptype='tau'&tau=$tau";
    
      if($otau == 'AniGif') {
	$btntau=$btntauloop;
      } else if($otau == '5day') {
	$btntau=$btntau5day;
      } else {
	$btntau=$btntauall;
      }
      if($otau != '5day') {
	$taubuttons= "
$taubuttons
<td>
<input type='button' class='${btntau}'
onMouseOver=\"className='${btntau}over';\"
onMouseOut=\"className='${btntau}';\"
value='${otau}' name=taub
onClick=\"ttau='${tau}';tmodel='${model}',pswap();\">
</td>
";
      }
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

<!-- show lat/lon code as doc going on end of preceeding doc -->

<script language='Javascript1.2' src='js/numberformat.js' type='text/javascript'></script>
<script language='Javascript1.2' src='js/showlatlon.js' type='text/javascript'></script>


<form name='Show'>
<input type='text' name='MouseY' value='0' size='5'>
<input type='text' name='MouseX' value='0' size='5'> Lat/Lon<br>
</form>

<script language='JavaScript1.2'>

var tempX = 0
var tempY = 0

// offset that makes upper righthand corner (0,0)

var offsetxL=tp[0]
var offsetyT=tp[1]

var IEoffsetX=-3
var IEoffsetY=-3


// calc from parea and size of image in area.trop*.cfg

var xL=0
var xR=$xsize

var lonL=$lonL
var lonR=$lonR

var yT=0
var yB=$ysize

var latT=$latT
var latB=$latB

var dX=xR-xL
var dlonP=(lonR-lonL)/dX

var dY=yB-yT
var dlatP=(latT-latB)/dY
</script>


</body>
</html>
";

?>

