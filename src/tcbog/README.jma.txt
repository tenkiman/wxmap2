       TCBOG -- TC wind profile retrievals using TC observations

			      Mike Fiorino
			    fiorino@llnl.gov

			      7 July 2004



Intro
=====

TCBOG is an adaptation of the FNMOC bogussing scheme for the NOGAPS
global models developed for ERA-40 and used in JRA-25.  The scheme
generates 5 wind profiles 1000-400 mb around a TC based only on:

position
motion
max wind
R30 - radius of 30(4) kt winds
R50 - radius of 50 kt winds

if R30 and R50 are not available the a lookup table based on max wind and
basin is used.


Application
===========

TCBOG is a F90 application that is run with three command line options:

ngtcbog.x tcbog.posits.txt tcbog.fgge.2.txt tcbog.obs
			    
ngtcbog.x		    application built using Makefile

tcbog.posits.txt	    input file with TC obs
tcbog.fgge.2.txt	    output file with TC wind retrivals in FGGE format
tcbog.obs		    output in grads station format



Input
=====

tcbog.posits.txt:

1987090700 15W 130 9999  20.0 110.0  080  150 304.0 04.55 -03.74 002.57
1987090700 15W 130 9999  20.0 140.0  120  225 304.0 04.55 -03.74 002.57
1987090700 15W 130 9999  20.0 170.0  -99  -99 304.0 04.55 -03.74 002.57
1987090700 15W 080 9999  40.0 110.0  060  110 304.0 04.55 -03.74 002.57
1987090700 15W 080 9999  40.0 140.0  090  175 304.0 04.55 -03.74 002.57
1987090700 15W 080 9999  40.0 170.0  -99  -99 304.0 04.55 -03.74 002.57

one line / TC

1987090700 15W 130 9999  20.0 110.0  080  150 304.0 04.55 -03.74 002.57

1987090700  = yyyymmddhh
15W	    = 3-char storm id
130	    = vmax (kts)
9999	    = pmin (mb) 9999 = undefined
20.0	    = latitude in deg N
110.0	    = longitude in deg E
080	    = R50 (nm)
150	    = R30 (nm)
304.0	    = direction of motion
04.55	    = speed (kts)
-03.74	    = u of motion (kts)
002.57	    = v of motion (kts)


Output -- FGGE
==============

this is the native output format used at FNMOC; have application that
converts to bufr

*15TC15W   0 220011000 0         0  7   
1010000-999999-99999-99999 75 1911  2    1010000 = 1000 mb  75: wind direction=75 deg 1911: 19 m/s speed   
10 9250-999999-99999-99999 84 2011  3    10 9250 = 925 mb 20 m/s at 85 deg   
10 8500-999999-99999-99999 93 2011  4   
10 7000-999999-99999-99999 93 1911  5   
10 5000-999999-99999-99999 94 1711  6   
10 4000-999999-99999-99999 95 1311  7   

Output -- GrADS station
=======================

station data form that allows plotting of all winds


Testing
=======

1) make # build 

2) ngtcbog.x tcbog.posits.txt tcbog.fgge.2.txt tcbog.obs  # run app

3) stnmap -v -i tcbog.ctl # make grads station map file



tcbog.ctl:
----------

dset ^tcbog.obs
#
#  new comment
#
title five TCBOG wind profile retrievals
dtype station
stnmap ^tcbog.smp
options sequential
undef 1e20
tdef 1 linear 00Z7Sep1987 6hr
vars  13
z     1 0 1000 h z [m]
uf    1 0 u fg [m/s]
vf    1 0 v fg [m/s]
ufb   1 0 u bias correction factor [m/s]
vfb   1 0 v bias correction factor [m/s]
ufc   1 0 u corrected fg [m/s]
vfc   1 0 v corrected fg [m/s]
um    1 0 u tc motion [m/s]
vm    1 0 v tc motion [m/s]
utr   1 0 u tc rankine [m/s]
vtr   1 0 v tc rankine [m/s]
u     1 0 u final [m/s]
v     1 0 v final [m/s]
endvars


Key Files
=========


Makefile			make the ngtcbog.x application set the compiler and flags
				CF =		pgf90  # portland group
				FFLAGS =	  -c -Mextend  # allows lines > 80 columns


ngtcbog.f			main program

gettrp.f			input TC obs




tcbog.radii.v.maxwind.pl	table (in perl) that relates maxwind (knots)
				to R30 (nm) and R50 (nm) as a function of basint


				basins LANT = atlantic; EPAC = eastern North Pacific ;
				WPAC = western North Pacifi; NIO = North Indian Ocean;
				SIO = South Indian Ocean (to 135E); SPAC = South Pacific (> 135E) 



tcbog.obs.png			500 winds using grads station data

tcbog.output.txt		stdout from running test program