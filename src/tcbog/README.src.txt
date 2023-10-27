			  TCBOG source tarball

			      Mike Fiorino
			michael.fiorino@noaa.gov

			       NOAA ESRL
			    Boulder, CO USA

			    17 December 2012


1. Introduction
---------------

This tarball contains all the source for the 'tcbog' application that
given an input file with TC position data or 'TC vitals', generates or
retrieves TC wind profiles at five points around the TC.  

The scheme originated from the the US Navy and was modified using ideas
from the UKMO TC bogus method for the ECMWF ERA-40 reanalysis project.

see:

Hatsushika H. et al, 2006: Impact of Wind Profile Retrievals on the
Analysis of Tropical Cyclones in the JRA-25 Reanalysis.  Journal of the
Meteorological Society of Japan, Vol. 84, No. 5, pp. 891--905, 2006

for more details.


2. Contents
-----------

# -- uses g95.org compiler
-rwxr-xr-x 5095/10000     1641 2012-12-17 10:38:15 Makefile

# -- fortran source
-rwxr-xr-x 5095/10000     1101 2012-01-30 16:38:39 bcubiy.f
-rwxr-xr-x 5095/10000     2005 2012-01-30 16:38:39 bcubvs.f
-rwxr-xr-x 5095/10000     7810 2012-01-30 16:38:39 bicub2.f
-rwxr-xr-x 5095/10000      227 2012-01-30 16:38:39 chlen.f
-rwxr-xr-x 5095/10000      244 2012-01-30 16:38:39 clokof.f
-rwxr-xr-x 5095/10000      138 2012-01-30 16:38:39 clokon.f
-rwxr-xr-x 5095/10000      547 2012-01-30 16:38:39 daynum.f
-rwxr-xr-x 5095/10000      237 2012-01-30 16:38:39 dftouv.f
-rwxr-xr-x 5095/10000      928 2012-01-30 16:38:39 dtgfix.f
-rwxr-xr-x 5095/10000     1774 2012-01-30 16:38:39 gathij.f
-rwxr-xr-x 5095/10000      455 2012-01-30 16:38:39 gathv.f
-rwxr-xr-x 5095/10000      618 2012-01-30 16:38:39 gausgr.f
-rwxr-xr-x 5095/10000     3605 2012-01-30 16:38:39 gausl3.f
-rwxr-xr-x 5095/10000      732 2012-01-30 16:38:39 gautrp.f
-rwxr-xr-x 5095/10000     3603 2012-01-30 16:38:39 geostd.f
-rwxr-xr-x 5095/10000     1994 2012-01-30 16:38:39 getspc.f
-rwxr-xr-x 5095/10000     5697 2012-01-30 16:38:39 gettrp.f
-rwxr-xr-x 5095/10000     6422 2012-01-30 16:38:39 gettrp.orig.f
-rwxr-xr-x 5095/10000      390 2012-01-30 16:38:39 glogau.f
-rwxr-xr-x 5095/10000     2543 2012-01-30 16:38:39 lgndr.f
-rwxr-xr-x 5095/10000      526 2012-01-30 16:38:39 mftcbog.f
-rwxr-xr-x 5095/10000     1134 2012-01-30 16:38:39 nfopen.f
-rwxr-xr-x 5095/10000     7556 2012-01-30 16:38:39 nfread.f
-rwxr-xr-x 5095/10000     7792 2012-01-30 16:38:39 nfwrit.f
-rwxr-xr-x 5095/10000    36432 2012-06-13 09:12:15 ngtcbog.f  # main program
-rwxr-xr-x 5095/10000      873 2012-01-30 16:38:39 noday.f
-rwxr-xr-x 5095/10000      812 2012-01-30 16:38:39 putobs.f
-rwxr-xr-x 5095/10000      862 2012-01-30 16:38:39 qpnh.f
-rwxr-xr-x 5095/10000     1496 2012-01-30 16:38:39 qprnth.f
-rwxr-xr-x 5095/10000     1746 2012-01-30 16:38:39 qprntn.f
-rw-r--r-- 5095/10000     6318 2012-01-30 16:38:39 rumdirdist.f
-rw-r--r-- 5095/10000     4665 2012-01-30 16:38:39 rumlatlon.f
-rwxr-xr-x 5095/10000      989 2012-01-30 16:38:39 s2ptrp.f
-rwxr-xr-x 5095/10000     2020 2012-01-30 16:38:39 setupv.f
-rwxr-xr-x 5095/10000     2952 2012-01-30 16:38:39 smthrad.f
-rwxr-xr-x 5095/10000      562 2012-01-30 16:38:39 sortml.f
-rwxr-xr-x 5095/10000    17589 2012-01-30 16:38:39 spcgto.f
-rwxr-xr-x 5095/10000     2480 2012-01-30 16:38:39 stupiy.f
-rwxr-xr-x 5095/10000      177 2012-01-30 16:38:39 tpose.f
-rwxr-xr-x 5095/10000      345 2012-01-30 16:38:39 tpotri.f
-rwxr-xr-x 5095/10000     2078 2012-01-30 16:38:39 tranrs.f
-rwxr-xr-x 5095/10000     1522 2012-01-30 16:38:39 transr.f
-rwxr-xr-x 5095/10000     4169 2012-01-30 16:38:39 tranuv.f
-rwxr-xr-x 5095/10000      805 2012-01-30 16:38:39 trdih.f
-rwxr-xr-x 5095/10000     1804 2012-01-30 16:38:39 trdiph.f
-rwxr-xr-x 5095/10000      941 2012-01-30 16:38:39 trdivv.f
-rwxr-xr-x 5095/10000      311 2012-01-30 16:38:39 uvtodf.f
-rwxr-xr-x 5095/10000      115 2012-01-30 16:38:39 zilch.f

# -- header files
-rwxr-xr-x 5095/10000     3624 2012-06-13 09:16:11 cnstnt.h
-rwxr-xr-x 5095/10000       47 2012-01-30 16:38:39 fftcom.h
-rwxr-xr-x 5095/10000       88 2012-01-30 16:38:39 gridg.h
-rwxr-xr-x 5095/10000      990 2012-01-30 16:38:39 ngtcbog.h
-rwxr-xr-x 5095/10000      633 2012-01-30 16:38:39 param.h
-rwxr-xr-x 5095/10000      103 2012-01-30 16:38:39 parmg.h


# -- output files run on kishou.fsl.noaa.gov a CentOS box, test.sh does
     a diff between what the application produces locally and these two
     files

-rw-r--r-- 5095/10000     9891 2012-12-17 10:27:21 tcbog.test.CUR.txt
-rw-r--r-- 5095/10000    12915 2012-12-17 10:27:21 tcbog.test.fgge.CUR.txt

# run this test script after make 
-rwxr-xr-x 5095/10000      520 2012-12-17 10:43:00 test.sh   

# -- input file to test.sh with
-rwxr-xr-x 5095/10000      577 2012-01-30 16:38:39 tcbog.posits.txt



