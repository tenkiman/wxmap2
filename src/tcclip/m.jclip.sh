#!/bin/sh

#
# building for cdat40 python 2.3.3
#
# 20040406
#f2py -c nhc.clipper.lib.f -m nclip
#exit

# this didn't work...
#f2py jtwc.clipper.lib.f -m jclip -h jclip.pyf --overwrite-signature 
#f2py -c jclip.pyf 

# for python 2.1.1
f2py jtwc.clipper.lib.f -m jclip -h jclip.pyf --overwrite-signature --overwrite-makefile
f2py jclip.pyf
make -f Makefile-jclip

