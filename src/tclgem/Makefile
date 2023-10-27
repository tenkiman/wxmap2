# Makefile for SHIPS intensity model. 
# 
# This version is for the iships.f stand-alone code
#
# make       - compile the model

# Fortran compiler/linker 
#FC	= pgf90

# Fortran compiler options

# quiet options (OPTIMIZATION LEVEL #2) 
#FFLAGS	= -C -Minform=inform

#FC      = g95
#FFLAGS= -g -O -ftrace=full -ffixed-line-length-132

FC      = gfortran
FFLAGS= -g -O -ffixed-line-length-132

## (iships.x) 
iships.x: iships.f ships_util.mod ships_util.o ships_input.mod ships_input.o decay.o rapidga.o rapidge.o aland.o dataio.o upcase.o PrSEFoNe.o
	$(FC) $(FFLAGS) iships.f ships_util.o ships_input.o decay.o rapidga.o rapidge.o aland.o dataio.o upcase.o PrSEFoNe.o -o iships.x

ships_util.mod: ships_util.f
	$(FC) $(FFLAGS) -c ships_util.f

ships_util.o: ships_util.f
	$(FC) $(FFLAGS) -c ships_util.f

ships_input.mod: ships_input.f ships_util.mod ships_util.o dataio.o
	$(FC) $(FFLAGS) -c ships_input.f ships_util.o dataio.o

ships_input.o: ships_input.f ships_util.mod ships_util.o dataio.o
	$(FC) $(FFLAGS) -c ships_input.f ships_util.o dataio.o

decay.o: decay.f
	$(FC) $(FFLAGS) -c decay.f

rapidga.o: rapidga.f
	$(FC) $(FFLAGS) -c rapidga.f

rapidge.o: rapidge.f
	$(FC) $(FFLAGS) -c rapidge.f

aland.o: aland.f
	$(FC) $(FFLAGS) -c aland.f
 
#stndz.o: stndz.f
#	$(FC) $(FFLAGS) -c stndz.f

dataio.o: dataformats.inc dataioparms.inc dataio.f
	$(FC) $(FFLAGS) -c dataio.f

upcase.o: upcase.f
	$(FC) $(FFLAGS) -c upcase.f

#llintp.o: llintp.f
#	$(FC) $(FFLAGS) -c llintp.f

PrSEFoNe.o: PrSEFoNe.f
	$(FC) $(FFLAGS) -c PrSEFoNe.f

clean:
	rm -rf *.o *~ *.mod
