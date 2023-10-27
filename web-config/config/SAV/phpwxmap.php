<?php


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

  while($hr>=24) {
    $hr=$hr-24;
    $jdy++;
  }

  while($hr<0) {
    $hr=$hr+24;
    $jdy--;
  }

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


function findexts ($filename)
{
  $filename = strtolower($filename) ;
  $exts = split("[/\\.]", $filename) ;
  $n = count($exts)-1;
  $exts = $exts[$n];
  return $exts;
}


function LoadHash($lines,$ib,$ie,$nk) {

  $hash=array();

  for ($i=$ib; $i<$ie; $i++) {
    $tt=$lines[$i];
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

}


function findcurdtgibie($tdtg,$dtgs,$ndtgs,$ndtgsmax) {

  $dtt=1;
  if($ndtgsmax >= 5) $dtt=2;
  if($ndtgsmax >= 7) $dtt=3;
  if($ndtgsmax >= 9) $dtt=4;
  if($ndtgsmax >= 11) $dtt=5;

  for ($i=0 ; $i<$ndtgs ; $i++) {
    if($dtgs[$i] == $tdtg) {
      $ndx=$i;
    }
  }

  if($ndx > 1 && $ndx <= ($ndtgs-$ndtgsmax+$dtt)) {
    $idtgb=$ndx-$dtt;
    $idtge=$idtgb+$ndtgsmax;
  } else {
    $idtgb=$ndx-$dtt;
    $idtge=$idtgb+($ndtgs-$ndtgsmax+$dtt);
  } 

  if($idtge > $ndtgs) {
    $idtge=$ndtgs;
  } elseif($idtgb < 0) {
    $idtgb=0;
    $idtge=$ndtgsmax;
  }


  $rc=array($idtgb,$idtge,$ndx);
  return($rc);
   
}

#
# no taus for the this model storm
#

function findtau000($tdtg,$tstm,$ttau,$dtgmodels,$dtgstms,$modeltaus) {

  $stms=$dtgstms[$tdtg];
  $models=$dtgmodels[$tdtg];

  $ttau=-999;
  $tmodel=-999;

  foreach ($models as $model) {
    $taus=pysplit($modeltaus[$tdtg][$model][$tstm],' ');
    if(count($taus) != 0) {
      $tmodel=$model;
      $ttau=$taus[0];
      $rc=array($ttau,$tmodel,$tstm);
      return($rc);
    }

  }

  $tstm=-999;
#
# no joy for this storm try the next...
#
  if($ttau < 0) {

    foreach ($stms as $stm) {

      foreach ($models as $model) {

	$taus=pysplit($modeltaus[$tdtg][$model][$stm],' ');
	if(count($taus) != 0) {
	  $tstm=$stm;
	  $tmodel=$model;
	  $ttau=$taus[0];
	  $rc=array($ttau,$tmodel,$tstm);
	  return($rc);
	}
	
      }

    }

  }
 
  $rc=array($ttau,$tmodel,$tstm);
  return($rc);
  
}


?>
