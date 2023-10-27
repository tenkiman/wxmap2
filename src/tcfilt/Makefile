SHELL=/bin/sh

OBJS=	tcfilt.o \
	amatrix.o bound2.o bound.o calcra.o calcr.o calct.o center.o \
	fdump.o findmx2.o findra.o getfg.o getmq.o h12.o i1mach.o interp.o \
	j4save.o maxmag.o maxth.o phase.o readit.o rodist.o separ.o \
	wnlit.o wnlsm.o wnnls.o xerabt.o xerctl.o xerprt.o xerror.o xerrwv.o \
	xersav.o xgetua.o gfdl_imsl.o ichlen.o tcread.o bsmooth.o

HDRS=	const.h params.h tctype.h 

OBJS=	tcfilt.o \
	amatrix.o bound2.o bound.o calcr.o calct.o center.o \
	findmx2.o findra.o maxth.o phase.o rodist.o separ.o \
	wnlit.o wnlsm.o wnnls.o fdump.o j4save.o h12.o i1mach.o \
	xersav.o xgetua.o xerabt.o xerctl.o xerprt.o xerror.o xerrwv.o \
	gfdl_imsl.o \
	ichlen.o tcread.o bsmooth.o


LDFLAGS =   
LIBS =	
CMD =   tcfilt.x


CF =		pgf90
LD=             pgf90
FFLAGS = -fast -Mextend -byteswapio
FFLAGS = -fast -Mextend

CF =		g95
LD=             g95
FFLAGS = -ffixed-line-length-132

CF =		gfortran
LD=             gfortran
FFLAGS = -ffixed-line-length-132


# Lines from here on down should not need to be changed.  They are the
# actual rules which make uses to build a.out.
#

$(CMD):		$(OBJS)
	$(LD) -o $(CMD) $(OBJS) $(LIBS) $(LDFLAGS)

clean:
	rm *.o $(CMD)

install:
	mv $(CMD) ../../../prc/tctrack


.f.o:
	$(CF) $(FFLAGS) -c $*.f -o $@ 


