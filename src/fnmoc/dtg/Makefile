#
#

CPP_COMPILER=g++
#CPP_COMPILER=pgCC
#CC=gcc34

TARGETS = dtgops dtgdiff
OBJECTS = cxclock.o 

SYSDEF = 

# CFLAGS = -DVERBOSE -g
#CFLAGS = -O2

all : $(TARGETS)

dtgops : dtgops.C cxclock.o
	$(CPP_COMPILER) $(SYSDEF) $(CFLAGS) dtgops.C $(OBJECTS) -o $@

dtgdiff : dtgdiff.C  
	$(CPP_COMPILER) $(SYSDEF) $(CFLAGS) dtgdiff.C -o $@
        
cxclock.o :  cxclock.C cxclock.h
	$(CPP_COMPILER) $(SYSDEF) $(CFLAGS) -c cxclock.C

clean :
	rm -f core $(TARGETS) *.o 
