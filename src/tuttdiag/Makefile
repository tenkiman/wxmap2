SHELL=/bin/sh

OBJS=	mf.modules.o readFldMeta.o ngtrk.o avgddt.o bogread.o calcntr.o calddto.o \
	calint.o chkcir.o chkfcir.o cirloc.o clltxy.o cxytll.o evaliso.o \
	fldread.o isocnt.o isofnd.o isotrc.o isovzm.o numchk.o outgdat.o \
	rcalhdst.o rcaltln.o selcyc.o sortem2.o trackem.o valinp.o \
	chlen.o glclrd.o xieee.o verify.o \
	mf.routines.o mf.track.o mf.grhilo.o \
	mf.trackem.o mf.grhilo.vrt925.o mf.grhilo.psl.o rumdirdist.o rumlatlon.o 

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

CF =		g95
LD =		g95

CF =		gfortran
LD =             gfortran

FFLAGS =  -ffixed-line-length-132

LDFLAGS =  -Bstatic
LIBS =	
CMD =   ngtrkN.x



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

