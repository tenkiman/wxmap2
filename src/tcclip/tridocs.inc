ckpd  tridocs.inc, explanations for mftri10.for

ckpd  This program is used as part of the post storm or post season
ckpd  processing for ATCF, to create a table of errors between storm
ckpd  motion forecasts as computed by various meteorological models and
ckpd  passed to ATCF in the form of "objective aids" position (and
ckpd  intensity, rarely) forecasts, and the forecast agency's best
ckpd  estimate of the actual storm motion, smoothed to remove the within
ckpd  storm nutation of the cyclone eye from the more important bulk
ckpd  cyclone motion.  The computed table is used in an end of the
ckpd  season or end of the year published paper report of the agency's
ckpd  relative success in tropical cyclone storm motion and storm
ckpd  intensity forecasting.

ckpd  (From the original triang.for program:)
ckpd  This program computes an error "triangle" from the ddeck. The
ckpd  user is prompted as to which of the four error types to use
ckpd  and what statistic to generate (mean, standard deviation, or
ckpd  median).

c---------------------------------------------------------------------------

ckpd  (Cleaned up Mike's writing here to amend and correct it while
ckpd  keeping the sense of what he wrote.)

ckpd  This is an update to the NEPRF "TRIANGLE" (triang.for) program
ckpd  which: 1) corrects errors in the calculation of the median and the
ckpd  Student's T error statistics; 2) automates the run by eliminating
ckpd  user prompts; 3) speeds up the median calculation; and 4) allows
ckpd  for more than 11 (up to 15, the current maximum available for any
ckpd  one basin) aids to be evaluated simultaneously.  The run is
ckpd  controlled by the input file "mftri10.in" and diagnostic output is
ckpd  written to "mftri10.out."

c      Programmer - Mike Fiorino 6/89 and 2/90
c
c---------------------------------------------------------------------------
c
c  arrays :  error(i,j,k) -- d deck errors for one storm.
c                            i = technique
c                            j = forecast number
c                            k = tau

c            tri(i,j,k,l) -- mean error triangle.
c                            i = x axis
c                            j = y axis
c                            k = tau
c                            l = 1 -- x axis error
c                                2 -- y axis error
c                                3 -- number of errors

c            tri1(i,j,k,l)-- stand. dev. or median

c            ntech(i,k)   -- technique names to be printed.
c                            i = technique
c                            k = tau

ckpd  data files : method.def -- select which techniques ( <= 15)
c                                are to be used.

c                  ddeck      -- d deck data with no blank lines

ckpd  The d-deck file is built by program ddeck.for.  It consists of
ckpd  error offsets between the (usually smoothed) best track data for a
ckpd  storm, and the forecast of each applicable "objective aid", or
ckpd  meteorological model storm motion forecast.  It is fed to this
ckpd  program to develop a publishable reference showing how well each
ckpd  meteorological model is doing in forecasting the storm, and how
ckpd  well ersatz objective aid "JTWC" (or "NWOC" or whatever), the
ckpd  actual emitted forecast by the forecasting agency is doing both
ckpd  absolutely and in comparision with the models' forecasts.

ckpd  Format:   Columns   Contents

ckpd             01-02    Objective aid number, 00 to taids

ckpd             03-06    Objective aid alphanumeric name

ckpd             07-09    Offset of aid's forecast in hours from the
ckpd                      forecast's synoptic time; for real objective
ckpd                      aids this time is positive in six hour
ckpd                      increments from 00 to 72, but a limited set of
ckpd                      up to five of them for any one forecast; CARQ
ckpd                      and WRNG cards contain retrospective best
ckpd                      track position estimate data rather than
ckpd                      position forecast data, so for them the time
ckpd                      offset is negative rather than positive,
ckpd                      thence the extra column for the minus sign.

ckpd             10-17    Date time group in format YYMMDDHH

ckpd             18-57    Eight (now; parameterize with nkinds but fix
ckpd                      format statements independently) sets of
ckpd                      integers, four digits plus a possible closely
ckpd                      set leading minus sign, with no leading zeros,
ckpd                      containing error values for each of the error
ckpd                      kinds identified in "nerr", below.

ckpd             58       Blank space.

ckpd             59-64    The storm ID in format BBNNYY, i.e., basin,
ckpd                      sequence number, and basin season "year"
ckpd                      number.

C****       Tue   2-27-1990  -      modified to bypass median
C****                               and student's t if less than
C****                               2 cases

C****       Programmer       -      Mike Fiorino

ckpd  Updated from Mike Fiorino's source to include 5 tau aids and 4
ckpd  radii winds, effective as of 1 July 1992, instead of previous 3
ckpd  tau aids and 3 radii winds.  The resulting increase in array
ckpd  sizes required that the former "triangles" stored in rectangles
ckpd  be changed to true triangles to save space.  This is done by
ckpd  decreasing the array dimensions by one and doing explicit indexing
ckpd  into the (n+1)*n/2 elements of a triangular subset of a square
ckpd  array that includes the diagonal elements.
ckpd  Kent Paul Dolan, CSC contractor to FNOC, 1992.12.29.

