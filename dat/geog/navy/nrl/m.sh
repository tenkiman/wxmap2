#!/bin/sh

#f77 sgeo.f -o sgeo geo.util.o -L/usr/local/lats/lib -llats -L/usr/local/lib -lnetcdf
#f77 sgeo.f -o sgeo geo.util.o -L/d1/lats -llats -L/usr/local/lib -lnetcdf
pgf77 geo.util.f -c
pgf77 sgeo.f -o sgeo geo.util.o -L/usr/local/lib -llats -L/usr/local/lib -lnetcdf

exit
