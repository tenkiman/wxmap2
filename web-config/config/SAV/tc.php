<?php

function GetShemYear($dtg) {
  $yyyy=substr($tdtg,0,4)*1;
  $mmdd=substr($tdtg,4,4)*1;
  if($mmdd >= 701) {
  $yyyy=$yyyy+1;
}
sprintf($yyyy,"%04d",$yyyy);

return($yyyy);

}

function IsShem($b1) {
$rc=0;
if($b1 == 's' || $b1 == 'p') {
  $rc=1;
}
return($rc);


}

function basin2tobasin1($b2) {

  $b1='X';
  if(strtolower($b2) == 'al') {
    $b1='l';

  } elseif( strtolower($b2) == 'io') {
    $b1='i';

  } elseif( strtolower($b2) == 'wp') {
    $b1='w';

  } elseif( strtolower($b2) == 'ep') {
    $b1='e';

  }    
  return($b1);

}

$basin1tobasin2=array();

$basin1tobasin2['l']='al';
$basin1tobasin2['c']='cp';
$basin1tobasin2['w']='wp';
$basin1tobasin2['e']='ep';
$basin1tobasin2['i']='io';



?>