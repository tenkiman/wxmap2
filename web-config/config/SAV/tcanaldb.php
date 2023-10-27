<?php

error_reporting(E_ERROR | E_WARNING | E_PARSE);



function findcurdtgibie($tdtg,$dtgs,$ndtgs,$ndtgsmax) {

  $dtt=1;
  if($ndtgsmax >= 5) $dtt=2;
  if($ndtgsmax >= 7) $dtt=3;

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

