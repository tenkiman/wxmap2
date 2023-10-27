SHELL=/bin/sh

OBJS=	tcsanal.o clltxy.o cxytll.o \
	qprntn.o readfld.o bssl5.o ofiles.o \
	cmdline.o readadeck.o readtcstruct.o analtc.o rumltlg.o \
	const.o load32.o ngptcbog.o

CF =		pgf90
LD=             pgf90

CF =		gfortran
LD=             gfortran

LDFLAGS =   
LIBS =	
CMD =   tcsanal.x

FFLAGS = -col120
FFLAGS = -Mextend -g -O0
FFLAGS = -fast -Mextend -byteswapio
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


