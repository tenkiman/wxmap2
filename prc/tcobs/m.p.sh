#!/bin/sh

# -- make application that prints out winds from 'diag' file from gfsenkf, e.g.,
#lfs1/projects/fim/ppegion/gfsenkf/t254/cira_winds/diag/2010062000/diag_conv_ges.2010062000_ensmean

#ifort -c readconvobs.f90
#ifort print_omf.gfsenkf.f90 readconvobs.enkf.o -o p.x
ifort -c kinds.f90
ifort -c readconvobs.enkf.f90
#ifort print_omf.gfsenkf.cira.f90 readconvobs.enkf.o -o p.x
ifort print_omf.gfsenkf.f90 readconvobs.enkf.o -o p.x

