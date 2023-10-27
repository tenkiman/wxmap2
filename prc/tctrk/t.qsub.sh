#!/bin/ksh
#$ -S /bin/ksh
#$ -N tctrk
#$ -cwd
#$ -r y
#$ -pe serial 1
#$ -l h_rt=00:30:00,h_vmem=1.0G
#$ -A fim 
#$ -j y
#$ -o /lfs1/projects/fim/fiorino/w21/prc/tctrk/wjet_tmtrk.log

# Set up paths to unix commands

RM=/bin/rm
CP=/bin/cp
MV=/bin/mv
LN=/bin/ln
MKDIR=/bin/mkdir
CAT=/bin/cat
ECHO=/bin/echo
CUT=/bin/cut
WC=/usr/bin/wc
DATE=/bin/date
AWK="/bin/awk --posix"
SED=/bin/sed
TAIL=/usr/bin/tail

# Executable script and path
RUNCMD='/lfs1/projects/fim/fiorino/w21/run.cron.tcsh'
PYDIR="/lfs1/projects/fim/fiorino/w21/prc/tctrk"
PYCMD="$PYDIR/p.gfsenkf.tmtrk.py"

# Set CWD to script location and execute redirecting stdout/stderr
cd $PYDIR
$RM -f tctrkout.txt
$RUNCMD "$PYCMD cur12-12" > tctrkout.txt 2>&1

# Check for exit status of script
error=$?
if [ ${error} -ne 0 ]; then
  ${ECHO} "ERROR: ${PYCMD} crashed  Exit status=${error}"
  exit ${error}
fi

# Sucessful exit
exit 0

