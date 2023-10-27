<?php

$verb=0;

foreach ($dtgs as $dtg) {

  print 'qqqqqqqqqq '.$dtg."\n";

  $models=$dtgmodels[$dtg];
  $stms=$dtgstms[$dtg];

  if($verb) {
    foreach ($models as $model) {
      echo "\n";
      foreach ($stms as $stm) {
	print "DDD $dtg  MMM $model :: $stm :: ".$modeltaus[$dtg][$model][$stm]."\n";
      }
    }
  }
}


?>