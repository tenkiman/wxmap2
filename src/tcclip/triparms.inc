ckpd  Parameter file for triangle.for.  Separated from the main routine
ckpd  to allow one time maintenance of the values.  This whole file is
ckpd  included in any subroutine that needs any of these parameters.

ckpd  Going along with Mike Fiorino's good start, added many parameters
ckpd  to replace undocumented "magic number" integer constants in the
ckpd  source text with documented named constants, to ease program
ckpd  maintenance.

ckpd    nodata  is  the value expected and presented when either no data
ckpd                exists for an entry or no value can be computed for
ckpd                an entry.

                        parameter(nodata=-9999)

ckpd  MAINTENANCE WARNING:  Changes to the value of naids must be
ckpd                        reflected where marked in prttri.for with
ckpd                        parallel changes to the print format
ckpd                        constants there.  Both these changes should
ckpd                        reflect changes to the maximum number of
ckpd                        aids used in any one basin, and to the
ckpd                        various editions of "techlist.dat".

ckpd    naids   is  the maximum number of objective aids processed per
ckpd                run.  This is severely limited by cpu executable
ckpd                file memory space limitations, since several large
ckpd                in-memory multidimensional arrays have this as one
ckpd                dimension.

      parameter(naids=20)

ckpd    taids   is  a number somewhat larger than the total number of
ckpd                legal objective aids names, to allow for growth. It
ckpd                helps size some modest sized arrays.
cajs  MAINTENANCE WARNING:  The "data" statement for "taids" should be
cajs                        modified to correspond to a change in
cajs                        parameter "naids" in ddeckparms, and vice versa.

cx    parameter(taids=60)
      integer taids
      parameter(taids=100)

ckpd    nerror  is  the maximum number of forecast synoptic periods for
ckpd                which errors are to be processed for a single storm.
ckpd                Like naids, it is severely limited by available cpu
ckpd                memory for executable files.  This parameter limits
ckpd                the number or size of individual storm d-deck files
ckpd                that can be combined into a single dcombo.dat file
ckpd                and run through this program to create triangle
ckpd                statistics tables for a basin's whole season.

cx -fortran comment, not c!   /* changed from 500 to 1000, 4/2/97, ajs */
      parameter(nerror=1000)    

ckpd  MAINTENANCE WARNING:  The "data" statement for "stdtau" must be
ckpd                        modified to correspond to a change in
ckpd                        parameter "ntau", and vice versa.

ckpd    ntau    is  the number of synoptic periods ahead for which
ckpd                tropical cyclone position forecasts are done at a
ckpd                single forecast time, at this writing, five (12, 24,
ckpd                36, 48, 72, 96 and 120 hour forecasts are standard).

      parameter(ntau=7)

ckpd    ntdata  is the number of fourth subscript entries in array tri.

      parameter(ntdata=3)

ckpd    n1data  is the number of fourth subscript entries in array tri1.

      parameter(n1data=2)

ckpd    nwrad   is  the number of wind radii forecast per position
ckpd                forecast.  It is unused as this is written, but
ckpd                included in case the ability to do error statistics
ckpd                on wind forecasts is added later to this program and
ckpd                to ddeck.for when some reliable measure of "true
ckpd                winds" for all storms is found to compare against
ckpd                the forecast winds.

      parameter(nwrad=4)

ckpd  MAINTENANCE WARNING:  The "data" statement for the "nerr" array of
ckpd                        error name character strings must be
ckpd                        modified to correspond to a change in
ckpd                        parameter "nkinds", and vice versa.

ckpd    nkinds  is  the number of kinds of forecast errors computed by
ckpd                this routine.

      parameter(nkinds=8)

ckpd    nstats  is  the number of kinds of statistics computable for
ckpd                each forecast error kind, by this routine; now: mean
ckpd                absolute value of forecast errors, standard
ckpd                deviation of signed forecast errors and Student's T
ckpd                confidence measure that paired techniques'
ckpd                simultaneous signed forecast errors differ
ckpd                significantly as a set, and gamma median (a low
ckpd                budget approximation of the arithmetic median) of
ckpd                signed forecast errors.  Arithmetic median of signed
ckpd                values of forecast errors and arithmetic median of
ckpd                absolute values of forecast errors are planned but
ckpd                not implemented yet due to speed versus computer
ckpd                memory limitations problems.

      parameter(nstats=5)

ckpd    lstmid  is  the length of a storm id character string.

      parameter(lstmid=6)

ckpd    laidln  is  the length of the buffer needed to hold a d-deck or
ckpd                a-deck data line.  It is unused currently but
ckpd                included for documentation in case this set of
ckpd                routines is being rewritten into some even
ckpd                moderately maintainable computer language.  Fortran
ckpd                '77 does allows it to be used neither as part of the
ckpd                "character*80" declaration term, nor as part of the
ckpd                "a80" format term, its only current uses in these
ckpd                routines.  It is used nowhere in the current code
ckpd                either as an index limit, or as a substring
ckpd                delimiter, for example.

      parameter(laidln=80)

ckpd    pstmid  is  the position (counting from 1) of the first
ckpd                character of the storm id in an input data line.

      parameter(pstmid=59)

ckpd    lutech  is  the logical unit number of the techlist (objective
ckpd                aids identifiers and error and statistics processing
ckpd                controls) input file.

      parameter(lutech=1)

ckpd    luinpt  is  the logical unit number of the d-deck forecast
ckpd                errors input file, the primary program input data.

      parameter(luinpt=3)

ckpd    lucont  is  the logical unit number of the program control input
ckpd                file that captures the users decisions (entered
ckpd                there with a text editor) about what kind of errors
ckpd                and what kind of statistics for them will be
ckpd                generated by this program.

      parameter(lucont=5)

ckpd    ludiag  is  the logical unit number of the (optional) diagnostic
ckpd                program trace output file, an option chosen with the
ckpd                control input file.

      parameter(ludiag=6)

ckpd    lutria  is  the logical unit number of the triangle table output
ckpd                file, the primary data output from this program.

      parameter(lutria=10)

ckpd    gamoff  is  the limit at or below whose negative data values
ckpd                must be discarded to avoid taking a natural
ckpd                logarithm of a number whose value is zero or
ckpd                negative, because we offset all other gamma median
ckpd                input values by GAMOFF before taking their natural
ckpd                logarithm.

cx    parameter(gamoff=2000)
      integer gamoff
      parameter(gamoff=2000)

ckpd    meanab  is  the index value of the Mean Absolute Error statistic
ckpd                in the statistics control parameter array.

      parameter(meanab=1)

ckpd    studev  is  the index value of the Student's T and Standard
ckpd                Deviation statistic in the statistics control
ckpd                parameter array.

cx    parameter(studev=2)
      integer  studev
      parameter(studev=2)

ckpd    medgam  is  the index value of the Gamma Median statistic in the
ckpd                statistics control parameter array.

      parameter(medgam=3)

ckpd    medsgn  is  the index value of the Arithmetic Median of Signed
ckpd                Errors statistic in the statistics control parameter
ckpd                array.

      parameter(medsgn=4)

ckpd    medabs  is  the index value of the Arithmetic Median of Absolute
ckpd                Errors statistic in the statistics control parameter
ckpd                array.

      parameter(medabs=5)

ckpd    iself   is  the index value for the fourth subscript of the tri
ckpd                and tri1 arrays that corresponds to the position
ckpd                into which the error's own value is accumulated.

      parameter(iself=1)

ckpd    iother  is  the index value for the fourth subscript of the tri
ckpd                and tri1 arrays that corresponds to the position
ckpd                into which the other (matching) error's value is
ckpd                accumulated.

      parameter(iother=2)

ckpd    koccur  is  the index value for the fourth subscript of the tri
ckpd                array that corresponds to the position into which
ckpd                the number of occurrences of accumulated errors (or
ckpd                matching pairs) is counted.

      parameter(koccur=3)

ckpd    isumer  is  (for the posit() calculation) the index of poserr
ckpd                for the array elements into which the sum of the
ckpd                position errors is accumulated.

      parameter(isumer=1)

ckpd    issqer  is  (for the posit() calculation) the index of poserr
ckpd                for the array elements into which the sum of the
ckpd                squares of the position errors is accumulated.

      parameter(issqer=2)

ckpd    kpoccu  is  (for the posit() calculation) the index of poserr
ckpd                for the array elements into which the count of
ckpd                occurrences of the valid position errors for this
ckpd                combination of technique type and retrospective tau
ckpd                offset is accumulated.

      parameter(kpoccu=3)

ckpd    icarq   is  (for the posit() calculation) the value of the first
ckpd                index into array poserr that corresponds to the
ckpd                array positions into which CARQ card position errors
ckpd                are accumulated.

      parameter(icarq=1)

ckpd    iwrng   is  (for the posit() calculation) the value of the first
ckpd                index into array poserr that corresponds to the
ckpd                array positions into which WRNG card position errors
ckpd                are accumulated.

      parameter(iwrng=2)

ckpd    npcard  is  (for the posit() calculation) the number of data
ckpd                card types interesting to this routine.

      parameter(npcard=2)

ckpd  MAINTENANCE WARNING:  There are print formats in routine posit()
ckpd                        which require maintenance if the value of
ckpd                        nptaus is changed in the program parameters
ckpd                        include file.  They are clearly marked in
ckpd                        that subroutine's source code file.

ckpd    nptaus  is  (for the posit() calculation) the number of
ckpd                retrospective taus considered (probably the same as
ckpd                ntau, but why create a maintenance nightmare later
ckpd                if one changes but the other does not?)

      parameter(nptaus=5)

ckpd    npdata  is  (for the posit() calculation) the number of kinds of
ckpd                data accumulated for each card type and tau index
ckpd                value.

      parameter(npdata=3)

ckpd    bigerr  is  (for the posit() calculation) the limiting size of
ckpd                an input position error above which we warn the user
ckpd                of possible problems with the input data.  These
ckpd                occur fairly often over the course of a season, but
ckpd                the end user wants to be told about them all.

      parameter(bigerr=100.0)
