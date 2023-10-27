cajs  Parameter file for ddeck.f.  Separated from the main routine
cajs  to allow one time maintenance of the values.  This whole file is
cajs  included in any subroutine that needs any of these parameters.


cajs    naids   is  the maximum number of objective aids processed per
cajs                run.  This number should accomodate the total number 
cajs                of legal objective aids names.
cajs                Possibly changes to "naids" should correspond to
cajs                changes in "taids" in triparms.inc.

      parameter(naids=100)

cajs    kmax    is  the forecast periods, 0, 12, 24, 36, 48, 72, 96, 120

      parameter(kmax=8)

cajs    jmax    is  the forecast types, FTE, XTC w/respect to CLIP, 
cajs                ATC w/respect to CLIP, TKE, SPE, TME, XTE, ATE

      parameter(jmax=8)

