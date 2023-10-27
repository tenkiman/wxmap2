#!/usr/bin/env tcsh
#
#       96110100 -- changed this to tcsh after all the mucking around with .cshrc
#
#       set the environment
#
#setenv W2 /dat1/w21/ -- had to set it here on tenki7-ssd on mike2
echo $W2
cd "$W2"
source .w2rc 
echo "Executing run.crontab.tcsh"
echo "************************************"
echo "*"
echo "QQQQQ: START $1 at "`date`" on "`hostname`
echo "*"
echo "************************************"
time $1
echo "************************************"
echo "*"
echo "QQQQQ:  END $1 at "`date`" on "`hostname`
echo "*"
echo "************************************"
exit

