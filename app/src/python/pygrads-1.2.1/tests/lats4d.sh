#!/bin/sh
#
# Simple sh(1) script to start GrADS and LATS4D, exiting from GrADS
# upon completion.
#
# Revision history:
#
# 29dec1999   da Silva  First crack. 
# 05jan1999   da Silva  Minor mod.
# 04oct2005   Todling   Added pointer for lats4d.gs in the build
#

gradsbin="../src/grads"
#lats4dgs="$FVROOT/lib/grads/lats4d.gs"
lats4dgs="./lats4d.gs"

if [ $#0 -lt 1 ]; then
	echo "          "
	echo "NAME"
	echo "     lats4d - file conversion and subsetting utility"
	echo "          "
        echo "SYNOPSIS"
        echo "     lats4d [-dap]  option(s)"
	echo "          "
	echo "DESCRIPTION"
	echo "     lats4d is a command line interface to GrADS"
        echo "     and the lats4d.gs script. It starts either"
        echo "     grads or gradsdap depending on the options"
        echo "     specified, runs lats4d.gs, and exits"
	echo "     from GrADS upon completion.     "
	echo "          "
	echo "     For additional information on LATS4D enter: lats4d -h"
	echo "          "
	echo "OPTIONS"
	echo " -dap       starts 'gradsdap' instead of 'grads"
	echo "          "
	echo " option(s)  are passed to lats4d.gs; for a list of lats4d "
        echo "            options enter: lats4d -h"
	echo "          "
	echo "IMPORTANT"
	echo "     You must specify the input file name with "
        echo "     the \"-i\" option."
	echo "          "
        echo "SEE ALSO  "
        echo "     http://dao.gsfc.nasa.gov/software/grads/lats4d"
	echo "          "
	exit 1
fi

if [ "$1" = "-nc" ];  then
	gradsbin="gradsnc"
	shift
elif [ "$1" = "-hdf" ]; then
	gradsbin="gradshdf"
	shift
elif [ "$1" = "-dods" ]; then
	gradsbin="../src/gradsdap"
	shift
fi

echo $gradsbin -blc \'run $lats4dgs -q $@ \'
eval $gradsbin -blc \'run $lats4dgs -q $@ \'
