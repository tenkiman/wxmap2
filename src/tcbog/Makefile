SHELL=/bin/sh

OBJS=	ngtcbog.o gettrp.o getspc.o spcgto.o \
        bcubvs.o bicub2.o daynum.o nfopen.o noday.o \
        bcubiy.o chlen.o dtgfix.o gausl3.o geostd.o \
        gathij.o gathv.o setupv.o stupiy.o tpose.o \
        trdih.o tpotri.o trdiph.o trdivv.o zilch.o \
        lgndr.o nfread.o nfwrit.o qpnh.o qprnth.o \
        s2ptrp.o sortml.o tranrs.o transr.o tranuv.o \
        gautrp.o gausgr.o glogau.o dftouv.o uvtodf.o mftcbog.o \
	smthrad.o qprntn.o \
	rumdirdist.o rumlatlon.o 

ISRC=	
		
#
# CF		Name of the fortran compiling system to use
# LDFLAGS	Flags to the loader
# LIBS		List of libraries
# CMD		Name of the executable
# PROFLIB	Library needed for profiling
#

CF =		cf77
LD=             $(MSPATH)/bin/empesqlcc
LDFLAGS =   -Wl,"-D map=brief;preset=indef"	
LIBS =		-l /usr/local/fnoc/lib/libfnoc.a 
CMD =   ngtrk
FFLAGS =    -Wf"-ei -o aggress"

CF =		f77 
LD=             f77

CF=		pgf77 
LD=             pgf77

CF =		pgf90
LD=             pgf90
FFLAGS = -fast -Mextend -byteswapio -Bstatic

CF =		g77
LD=             g77

# -- doesn't work for some reason...on kishou...but g95 does...
#
CF	= gfortran
#FFLAGS  = -gdwarf-2 -O  -frecord-marker=4  -fno-range-check -ffixed-line-length-132
# 20161220 -- seems to work
FFLAGS  =  -ffixed-line-length-132
LD      = gfortran

#CF =		g95
#LD =		g95
#FFLAGS =  -ffixed-line-length-132

LDFLAGS =  -Bstatic
LIBS    =
CMD     = ngtcbog.x



# Lines from here on down should not need to be changed.  They are the
# actual rules which make uses to build a.out.
#

$(CMD):		$(OBJS) $(ISRC)
	$(LD) -o $(CMD) $(OBJS) $(LIBS) $(LDFLAGS)

clean:
	rm *.o $(CMD)

install:
	mv $(CMD) ../../../prc/tctrack



.f.o:
	$(CF) $(FFLAGS) -c $*.f -o $@ 

