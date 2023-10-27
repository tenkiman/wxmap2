# Makefile for diagnostic file generation. 
# 
# Version 1.1, last modified 02/11/2011
# This version (v1.0) is for HWRF reruns.
#
# make/make all   - compile all associated fortran programs
# make clean      - removes all intermediate files (does not remove *.x)
# make lstest.exe - makes only test program for diagnostic calculation

# Fortran compiler/linker 
FC	= pgf90

# Fortran compiler options

# quiet options (OPTIMIZATION LEVEL #2) 
FFLAGS	= -C -Minform=inform

OBJS=	mf.modules.o gbland.o tcdiag.o lsdiags.o  ctorh.o wndspd.o qprntn.o readgrid.o writeparams.o lsdiagDriver.o
CMD =   lsdiag.x

# -gdwarf-2 removes these warnings paricular to gfortran on macos leopard
# ld warning: can't find atom for N_GSYM stabs rnm2km:G(0,8) in mf.modules.o
# ld warning: can't find atom for N_GSYM stabs omega:G(0,8) in mf.modules.o

FC	= gfortran
FFLAGS= -gdwarf-2 -O  -frecord-marker=4  -fno-range-check -ffixed-line-length-132

#FC	= g95
#FFLAGS= -g -O -ftrace=full -ffixed-line-length-132

LD      = gfortran
LDFLAGS = -Bstatic
LIBS =	

$(CMD):		$(OBJS) 
	$(LD) -o $(CMD) $(OBJS) $(LIBS) $(LDFLAGS)


.f.o:
	$(FC) $(FFLAGS) -c $*.f -o $@ 



## lsdiag.x: lsdiagDriver.f 
## 	$(FC) $(FFLAGS) lsdiagDriver.f lsdiags.o gbland.o ctorh.o tcdiag.o wndspd.o qprntn.o readgrid.o writeparams.o -o lsdiag.x


## tcdiag.x: tcdiagdriver.f tcdiag.o lsdiags.o gbland.o ctorh.o wndspd.o qprntn.o diag_util.mod diag_util.o dataio.o
## 	$(FC) $(FFLAGS) tcdiagdriver.f lsdiags.o gbland.o ctorh.o tcdiag.o wndspd.o qprntn.o diag_util.o dataio.o -o tcdiag.x


## ## (all)
## all: nameparse.x gridparse.x getcenter.x inddiag.x inddiagnull.x totaldiag.x

## ## (nameparse.x) 
## nameparse.x: nameparse.f
## 	$(FC) $(FFLAGS) nameparse.f -o nameparse.x

## ## (gridparse.x) 
## gridparse.x: gridparse.f
## 	$(FC) $(FFLAGS) gridparse.f -o gridparse.x

## ## (totaldiag.x)
## totaldiag.x: totaldiag.f diag_util.mod diag_util.o dataio.o upcase.o
## 	$(FC) $(FFLAGS) totaldiag.f diag_util.o dataio.o upcase.o -o totaldiag.x

## ## (inddiag.x)
## inddiag.x: inddiag.f diag_util.mod diag_util.o dataio.o upcase.o lsdiags.o gbland.o
## 	$(FC) $(FFLAGS) inddiag.f diag_util.o dataio.o upcase.o lsdiags.o gbland.o -o inddiag.x

## ## (inddiagnull.x)
## inddiagnull.x: inddiagnull.f diag_util.mod diag_util.o dataio.o upcase.o
## 	$(FC) $(FFLAGS) inddiagnull.f diag_util.o dataio.o upcase.o -o inddiagnull.x

## ## (getcenter.x)
## getcenter.x: getcenter.f diag_util.mod diag_util.o dataio.o upcase.o
## 	$(FC) $(FFLAGS) getcenter.f diag_util.o dataio.o upcase.o -o getcenter.x

## lsdiags.o: lsdiags.f 
## 	$(FC) $(FFLAGS) -c lsdiags.f 

## diag_util.mod: diag_util.f 
## 	$(FC) $(FFLAGS) -c diag_util.f 

## diag_util.o: diag_util.f
## 	$(FC) $(FFLAGS) -c diag_util.f 

## dataio.o: dataformats.inc dataioparms.inc dataio.f
## 	$(FC) $(FFLAGS) -c dataio.f

## gbland.o: gbland.f
## 	$(FC) $(FFLAGS) -c gbland.f

## wndspd.o: wndspd.f
## 	$(FC) $(FFLAGS) -c wndspd.f

## upcase.o: upcase.f
## 	$(FC) $(FFLAGS) -c upcase.f

## ctorh.o: ctorh.f
## 	$(FC) $(FFLAGS) -c ctorh.f

## tcdiag.o: tcdiag.f
## 	$(FC) $(FFLAGS) -c tcdiag.f

## qprntn.o: qprntn.f
## 	$(FC) $(FFLAGS) -c qprntn.f

## readgrid.o: readgrid.f
## 	$(FC) $(FFLAGS) -c readgrid.f

## writeparams.o: writeparams.f
## 	$(FC) $(FFLAGS) -c writeparams.f

## ## (lstest.exe)
## #lstest.exe: lstest.f lsdiags.f stndz.f gbland.f ctorh.f
## #	$(FC) $(FFLAGS) lstest.f lsdiags.f stndz.f gbland.f ctorh.f -o lstest.exe

clean:
	rm -rf *.o *~ *.mod *.x
