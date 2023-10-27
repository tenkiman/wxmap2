#!/bin/sh
# -- set the redo env
#
. ~/.redorc

dtg=$1  
model=$2
overopt=$3
runbg=$4
ropt=$5

#model='jgsm'
#model='navg'

if [ "$model" = 'jgsm' ] 
then
logfile=$logjgsm

elif [ "$model" = 'navg' ] 
then
logfile=$lognavg

elif [ "$model" = 'gfs2' ] 
then
logfile=$loggfs2

elif [ "$model" = 'ecm5' ] 
then
logfile=$logecm5

elif [ "$model" = 'cgd2' ] 
then
logfile=$logcgd2

else
logfile=''

fi

if [ "$dtg" = '' ]
then
echo "p-redo-model.sh dtg model overopt runbg ropt"
echo "#1: dtg"
echo "#2: model: jgsm | navg | gfs2 | ecm5 | cgd2"
echo "#3: overopt (-O) | runbg: -b | -f"
echo "#4: runbg='-b' | -f | run in background"
echo "#5: ropt = -N no run"
echo "  example: "
echo "  p-redo-model.sh cur12-12 gfs2 -b # run in background"

exit;

fi


if [ "$model" = '' ]
then
echo "must set model as second command line arg"
exit;
fi

if [ "$logfile" = '' ]
then
echo "invalid model: $model"
exit;
fi

if [ "$3" = '' ]
then
echo "must set either overopt as 3rd arg..."
exit;

elif  [ "$3" = '-b' ] || [ "$3" =  '-B' ] || [ "$3" = '-f' ] || [ "$3" = '-F' ] 
then
runbg=$3
echo "setting runbg using 3rd arg: $runbg"
overopt=''

elif [ "$3" = '-O' ] || [ "$3" = '-o' ]
then
overopt=$3

if [ "$4" = '' ] 
then
echo "if using arg 3 as overopt, then must set arg 4 as runbg..."
exit;

elif [ "$4" = '-O' ] || [ "$4" = '-o' ]
then
overopt=$4
fi

fi

if  [ "$ropt" = '-N' ] || [ "$dtg" = '' ]
then
  echo "IIIIIIEEE"
  echo "$runcmd \"$w2pdir/wxmap2/do-$model.py $dtg $overopt\"                          >> $ptmpdir/$logfile 2>&1 &"
else
  sdate=`date`
  echo "START-$model: $sdate"

  if [ "$runbg" = '-b' ] || [ "$runbg" = '-B' ]
  then
    echo "HHHAAAIII BBBBB == doing model: $model dtg: $dtg overopt: $overopt in BACKGROUND" 
    $runcmd "$w2pdir/wxmap2/do-$model.py $dtg $overopt"                     >> $ptmpdir/$logfile 2>&1 &
  else
    echo "HHHAAAIII FFFFF == doing model: $model dtg: $dtg overopt: $overopt in foreground"
    $runcmd "$w2pdir/wxmap2/do-$model.py $dtg $overopt"                     >> $ptmpdir/$logfile 2>&1
  fi

  edate=`date`
  echo "EEEND-$model: $edate"
fi

