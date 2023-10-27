# Makefile for diagnostic file generation. 
# 
# Version 3.0, last modified 05/14/2015
#
# make/make all   - compile all associated fortran programs
# make clean      - removes all intermediate and executable files

# Fortran compiler/linker 
FC	= pgf90
#FC	= ifort

# Fortran pgf90 compiler options
FFLAGS	= -C -Minform=inform

# Fortran ifort compiler options
#FFLAGS	= -w

## (all)
all: inddiag.x inddiagnull.x totaldiag.x

## (totaldiag.x)
totaldiag.x: totaldiag.f diag_util.mod diag_util.o
	$(FC) $(FFLAGS) totaldiag.f diag_util.o -o totaldiag.x

## (inddiag.x)
inddiag.x: inddiag.f diag_util.mod diag_util.o lsdiags.o gbland.o aland.o shland.o wland.o
	$(FC) $(FFLAGS) inddiag.f diag_util.o lsdiags.o gbland.o aland.o shland.o wland.o -o inddiag.x

## (inddiagnull.x)
inddiagnull.x: inddiagnull.f diag_util.mod diag_util.o
	$(FC) $(FFLAGS) inddiagnull.f diag_util.o -o inddiagnull.x

lsdiags.o: lsdiags.f diag_util.mod diag_util.o gbland.o aland.o shland.o wland.o
	$(FC) $(FFLAGS) -c lsdiags.f diag_util.o gbland.o aland.o shland.o wland.o

diag_util.mod: diag_util.f
	$(FC) $(FFLAGS) -c diag_util.f

diag_util.o: diag_util.f
	$(FC) $(FFLAGS) -c diag_util.f

gbland.o: gbland.f aland.o shland.o wland.o
	$(FC) $(FFLAGS) -c gbland.f aland.o shland.o wland.o

aland.o: aland.f
	$(FC) $(FFLAGS) -c aland.f

shland.o: shland.f
	$(FC) $(FFLAGS) -c shland.f

wland.o: wland.f
	$(FC) $(FFLAGS) -c wland.f

clean:
	rm -rf *.o *~ *.mod *.x
