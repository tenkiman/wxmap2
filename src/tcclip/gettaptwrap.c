/* *************************************************************** */
/* This program is a c wrapper around a fortran program to acquire */
/* data for models.                                                */
/* --------- Sampson, NRL  Aug 98                                  */
/* *************************************************************** */

#include "stdio.h"                     /* standard I/O header file */

#if XVT_CC_PROTO
void gettapt( char *stormid  );
#else
void gettapt();
#endif

main(number,name)
int number;                 /* number of arguments on command line */
char *name[];               /* arguments on the command line       */
{
char *stormid;
char *century;

   stormid = name[1];
   century = name[2];
   gettapt(stormid, century);
} 
