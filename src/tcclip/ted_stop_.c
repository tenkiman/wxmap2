
/**********************************************************************
 *
 * IDENTIFICATION:
 *    ted_stop_.c - Closes TEDS database
 *
 * REVISION/MODIFICATION HISTORY:
 *
 * RESPONSIBLE ORGANIZATION:
 * Roland E. Nagle CSC
 *
 * DESCRIPTION:
 *    See description of individual functions.
 *
 * LANGUAGE:
 *    MASSCOMP C
 *
 * INPUTS:
 *    None
 *
 * OUTPUTS:
 *    None
 *
 * ERROR MESSAGES:
 *    None
 *
 * EXTERNAL ROUTINES:
 *   ted_stop() 
 *
 *********************************************************************/

/* INCLUDE STATEMENTS */
#include <stdio.h>

#include "MAGRIDAPI.h"

/********************************************************************
 *FUNCTION :
 *    function 

 * DESCRIPTION:
 *    function routine to open teds database

 * INPUTS:
 *    None
     
 * OUTPUTS:
 *    None
 **********************************************************************/
/*
 *CALLING INTERFACE:
*/
   ted_stop(sflag)
   
   int   *sflag;
/*
 *EXTERNAL SUBROUTINE:
*/
 {
/*
 *LOCAL VARIABLES:
*/
   MAGRIDRET magridRet;

   memset ( &magridRet, 0, sizeof ( MAGRIDRET ) );

   magridRet = MAGRIDConnect ( );
   *sflag  = magridRet.nStatus;
 }
