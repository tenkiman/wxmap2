#!/bin/sh

ngtcbog.x tcbog.posits.txt tcbog.test.fgge.txt tcbog.test.txt tcbog.obs

# -- compare fgge output to run on kishou.fsl.noaa.gov:
# Linux kishou.fsl.noaa.gov 2.6.18-308.20.1.el5 #1 SMP Tue Nov 13 10:15:12 EST 2012 x86_64 x86_64 x86_64 GNU/Linux

#Kishou(LINUX)[W2:ESRL]: /mnt/hgfs/dat1/w21/prc/tcbog 226 > pg /etc/redhat-release 
#CentOS release 5.8 (Final)

echo
echo "diff fgge output: "
diff tcbog.test.fgge.txt tcbog.test.fgge.CUR.txt
echo
echo "diff text output: "
diff tcbog.test.txt tcbog.test.CUR.txt

