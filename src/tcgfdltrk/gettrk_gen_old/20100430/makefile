SHELL=  /bin/sh
ISIZE = 4
RSIZE = 8
COMP=   xlf
LIBS=   -L/nwprod/lib -lw3_d -lbacio_4
LDFLAGS= -bloadmap:loadmap -bnoquiet
#FFLAGS= -O -qcheck -qintsize=$(ISIZE) -qrealsize=$(RSIZE)
###FFLAGS= -O -qcheck -qextchk -qarch=auto -qflttrap=ov:zero:inv:enable -qintsize=$(ISIZE) -qrealsize=$(RSIZE)
#FFLAGS= -O -qcheck -qextchk -qwarn64 -qarch=auto -qflttrap=ov:zero:inv:enable -qintsize=$(ISIZE) -qrealsize=$(RSIZE)
FFLAGS= -g -O0 -qcheck -qextchk -qwarn64 -qarch=auto -qflttrap=ov:zero:inv:enable -qintsize=$(ISIZE) -qrealsize=$(RSIZE)

gettrk_gen:      gettrk_main.gen.f gettrk_modules.gen.o
	@echo " "
	@echo "  Compiling the tracking program....."
	$(COMP) $(FFLAGS) $(LDFLAGS) gettrk_modules.gen.o gettrk_main.gen.f $(LIBS) -o gettrk_gen
	@echo " "

gettrk_modules.gen.o:    gettrk_modules.gen.f
	@echo " "
	@echo "  Compiling the modules....."
	$(COMP) $(FFLAGS) -c gettrk_modules.gen.f -o gettrk_modules.gen.o
	@echo " "
