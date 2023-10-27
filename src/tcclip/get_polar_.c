/**********************************************************************
 *
 * IDENTIFICATION:
 *    get_polar_.c - Gets a NOGAPS file from the TEDS database (2.5 deg)
 *
 *    Grid is a polar stereographic one, as defined in JTWC92.
 *
 *
 * REVISION/MODIFICATION HISTORY:
 * Sampson, NRL      - original code                    
 *
 * RESPONSIBLE ORGANIZATION:
 * Sampson, NRL   Sep, 1998
 *
 * DESCRIPTION:
 *    See description of individual functions.
 *
 * LANGUAGE:
 *    C
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
 *    None
 *
 *********************************************************************/

/* INCLUDE STATEMENTS */

#include <stdio.h>
#include <time.h>
#include <varargs.h>
#include <malloc.h>

#include "MAGRIDAPI.h"

#include "date.h"
#include "tedutils.h"
#include "tedgrid.h"
#include "tdTime.h"
#include "GeomReg.h"

/*  TEDS Debugging variable */
/* int nMAGRIDdebug = 1; */

/********************************************************************
 *FUNCTION :
 *    function 

 * DESCRIPTION:
 *    function routine to retrieve a NOGAPS field from the TEDS database

 * INPUTS:
 *    icentury - integer; contains century
 *    IDATE - Array; contains year, month, day, and symoptic time
 *    presl - requested pressure level (lower)    
 *    presu - requested pressure level (upper)
 *    parm  - requested parameter 
 *    itau  - requested forecast hour
 * OUTPUTS:
 *    gfield - array containing field returned to calling program (FORTRAN) 
 *    sflag  - status flag returned to calling program
 **********************************************************************/

   get_polar(icentury,idate, presl, presu, parm, itau, gfield, sflag) 

int    *icentury;       /* century                                  */ 
int    idate[4];        /* Array containing date/time               */ 
int    *presl;		/* array of pressure levels to analyze      */
int    *presu;		/* array of pressure levels to analyze      */
int    *parm;           /* Index of parameter type                  */ 
int    *itau;           /* Forecast hour                            */
float  *gfield;         /* Array for request field                  */
int    *sflag;          /* Status flag                              */

{

/* DEFINE STATEMENTS */

#define  ATCF_VAPORPRESSURE 55
#define  ATCF_GEOPOTENTIAL_MN  134
#define  ATCF_GEOPOTENTIAL  7
#define  ATCF_TEMPERATURE   11
#define  ATCF_U_COMPONENT   33
#define  ATCF_V_COMPONENT   34
#define  ATCF_PRESSURE      2

#define  ATCF_MILLIBARS     870
#define  ATCF_GPM           710
#define  ATCF_KELVIN        440
#define  ATCF_MPS           860

#define  ATCF_PRES_LEVEL    100
#define  ATCF_MSL           102
#define  ATCF_LAYER         101

   struct tm        tmStruct;
   int              pindex = 0, n = 0;
   int              row = 0;
   time_t           theTime; 
   MAGRIDRET        magridRet;
   MAGRIDQUERY      GridQuery;
   MAGRIDFORMAT     stGridFormat;
   long             lNumFound = 0;
   MAGRIDLINKEDLIST GridDataLL, *pGridDataLL = 0;
   MAGRIDDATA       *pGridData = 0;
   
   float parsFbuffA[42048];     /* Array for request field                    */
   float parsFbuffB[42048];     /* Array for request field                    */
   GEOMREGISTRATION  GeomRegA;  /* Registration struc for input to GridMap    */
   GEOMREGISTRATION  GeomRegB;  /* Registration struc for output from GridMap */
   
#if 0   
   printf("in get_polar,presl=%d,presu=%d,parm=%d,itau=%d \n",*presl,*presu,*parm,*itau);
   printf("in get_polar,icentury,date=%d %d %d %d %d\n",*icentury,idate[0],idate[1],idate[2],idate[3]);
#endif

/* figure out date from idate(4) */

   memset ( &magridRet, 0, sizeof ( MAGRIDRET ) );
   memset ( &tmStruct, 0, sizeof ( struct tm ) );
   tmStruct.tm_year = idate[0] + *icentury*100 - 1900;
   tmStruct.tm_mon =  idate[1] - 1;
   tmStruct.tm_mday = idate[2];
   tmStruct.tm_hour = idate[3];

   theTime = mktime ( &tmStruct );
#if 0
   printf ( "BaseTime is (%d:%s)\n", theTime, ( char * ) ctime ( &theTime ) ); 
#endif

   memset ( &stGridFormat, 0, sizeof ( MAGRIDFORMAT ) );

   pindex = *parm;
    
/****************************************/
/* Populate the catalog query structure */
/****************************************/

   memset(&GridQuery, 0, sizeof(MAGRIDQUERY));
   memset(&GridDataLL, 0, sizeof(MAGRIDLINKEDLIST));
   GridQuery.lProductionCenterId = 58;       /* US Navy               */
   GridQuery.lSubCenterId        = 0;        /* FNMOC                 */
   GridQuery.lGridId             = 240;
   
   if (*presu == 0)
       {
       GridQuery.lGeneratingProcId   = 58;       /* NOGAPS                */
       }
   else
       {
       GridQuery.lGeneratingProcId   = 83;       /* GOXM - special grids  */
       }
          
   GridQuery.lParameterId        = MAGRID_QUERY_WILDCARD;
   GridQuery.lBeginBaseTime      = ( long ) theTime;
   GridQuery.lEndBaseTime        = ( long ) theTime;
   GridQuery.lBeginTau           = ( long ) *itau * 60;     /* TAU in minutes        */
   GridQuery.lEndTau             = ( long ) *itau * 60;     /* TAU in minutes (24hr) */
   GridQuery.rsBeginLevel        = *presl;
   GridQuery.rsEndLevel          = *presu;
   GridQuery.lLevelType          = MAGRID_QUERY_WILDCARD;
   GridQuery.stGeoArea.rsNLat    =   90.0;
   GridQuery.stGeoArea.rsSLat    =  -90.0;
   GridQuery.stGeoArea.rsELon    =  180.0; 
   GridQuery.stGeoArea.rsWLon    = -180.0;

/**************************************/     
/* Populate the grid format structure */
/**************************************/
   
   stGridFormat.eOutputFormat      = MAGRID_GET_AS_SPECIFIED;
   stGridFormat.lMaxXPoint         = 144;
   stGridFormat.lMaxYPoint         = 73;
   stGridFormat.eScanMode          = MAGRID_pXinpY;
/* stGridFormat.eProjection        = MAGRID_SPHERICAL;*/
   stGridFormat.stProjectionDesc.eProjection = MAGRID_SPHERICAL;
   stGridFormat.lUnitId            = MAGRID_QUERY_WILDCARD;
      

    switch(pindex)
    {
/*******************************************************************/
/*    Case 1 gets geopotential height field                        */
/*******************************************************************/
       case 1:
              stGridFormat.lUnitId =   ATCF_GPM; /*geopotential meters*/
              GridQuery.lParameterId = ATCF_GEOPOTENTIAL_MN;/*gpm*/
	      GridQuery.lLevelType =   ATCF_PRES_LEVEL; /*pressure level*/
	      if (*presu > 0) GridQuery.lLevelType = ATCF_LAYER; 
              break;
/*******************************************************************/
/*    Case 2 gets temperature field                                */
/*******************************************************************/
       case 2:
              stGridFormat.lUnitId =   ATCF_KELVIN;
              GridQuery.lParameterId = ATCF_TEMPERATURE;             
	      GridQuery.lLevelType =   ATCF_PRES_LEVEL;
              break;
/*******************************************************************/
/*    Case 3 gets vapor pressure                                   */
/*******************************************************************/
       case 3:
              stGridFormat.lUnitId =   ATCF_MILLIBARS;               
              GridQuery.lParameterId = ATCF_VAPORPRESSURE;
	      GridQuery.lLevelType =   ATCF_PRES_LEVEL; 
              break;
/*******************************************************************/
/*    Case 4 gets u component of wind                              */
/*******************************************************************/
       case 4:  
              stGridFormat.lUnitId =   ATCF_MPS;
              GridQuery.lParameterId = ATCF_U_COMPONENT;
	      GridQuery.lLevelType =   ATCF_PRES_LEVEL; 
	      /* special case for dlm fields */
	      if (*presu > 0) GridQuery.lLevelType = ATCF_LAYER; 
	      /*printf ( "GridQuery.lParameterId = %d\n", GridQuery.lParameterId );*/
              break;
/*******************************************************************/
/*       case 5 gets v component of wind                           */
/*******************************************************************/ 
       case 5:
              stGridFormat.lUnitId =   ATCF_MPS;              
              GridQuery.lParameterId = ATCF_V_COMPONENT;
	      GridQuery.lLevelType =   ATCF_PRES_LEVEL; 
	      /* special case for dlm fields */
	      if (*presu > 0) GridQuery.lLevelType = ATCF_LAYER; 
              break;
/*******************************************************************/
/*       case 6 gets sfc pressure                                  */
/*******************************************************************/ 
       case 6:
              stGridFormat.lUnitId =   ATCF_MILLIBARS;
              GridQuery.lParameterId = ATCF_PRESSURE;
	      GridQuery.lLevelType =   ATCF_MSL; 
              break;
   } 


/**************************************************************/
/* Call the API MAGRIDGet2DByQuery to retrieve multiple Grids */
/**************************************************************/

   magridRet = MAGRIDGet2DByQuery ( &GridQuery, &stGridFormat,
                            &lNumFound, &GridDataLL );
                         
   if ( magridRet.nStatus )
   {
      printf( "Error in MAGRIDGet2DByQuery (%d) (%s) (%s)\n", magridRet.nStatus,
                          magridRet.szSQLState, magridRet.szErrorMessage );
      printf( "ErrorMessage (%s)\n", magridRet.szErrorMessage);
   }
   else
   {         
      /**************************/
      /* Can't find it          */
      /**************************/
      if (lNumFound < 1)
      {
         *sflag = 1; 
         /* printf("\nNo grids were found.\n"); */
      }
      /**************************/
      /* Found it               */
      /**************************/
      else
      {
         n = 1;
         pGridDataLL = &GridDataLL;
         while (n <= lNumFound)
         {
            pGridData = ( PMAGRIDDATA ) pGridDataLL->data;
            n++;
            pGridDataLL = pGridDataLL->next;
            /* copy grid data to gfield array to pass back to calling routine */
            memcpy ( parsFbuffA, pGridData->pGridFieldData, pGridData->ulSize );
            *sflag = 0; 

         }
         MAGRIDFreeLL( &GridDataLL );
      } /* end Found it */

    }  /* end no error in database query */
#if 0
for (row = 0; row < 10512 ; row++) 
   { 
	if (parsFbuffA[row] < 5000.0 )printf(" %f \n ", parsFbuffA[row]);
   } 
#endif

 if (lNumFound > 0)
 {

 /*  Start conversion to polar stereographic projection  */  
 /******************************************************************************
 * INPUTS:
 *      GeomRegA.rdRegLat      latitude of origin (degrees)
 *      GeomRegA.rdRegLon      longitude of origin (degrees, west is -ve)
 *      GeomRegA.rsRegXx       column number defining origin (top left is 1,1)
 *      GeomRegA.rsRegY        row number defining origin (top left is 1,1)
 *      GeomRegA.nNumXPnts     count of columns in grid
 *      GeomRegA.nNumYPnts     count of rows in grid
 *      GeomRegA.eProjection   enumerated projection name
 *      GeomRegA.eStorDsc      enumerated storage description
 *      GeomRegA.rsParm1       geometry parameter 1 value defined for
 *                                 each projection in table projection
 *      GeomRegA.rsParm2       geometry parameter 2 value defined for
 *                                 each projection in table projection
 *      GeomRegA.rsParm3       geometry parameter 3 value defined for
 *                                 each projection in table projection
 *      GeomRegA.rsParm4       geometry parameter 4 value defined for
 *                                 each projection in table projection
 *      GeomRegA.rsParm5       geometry parameter 5 value defined for
 *                                 columns, left column is number 1
 *      GeomRegB.lRefNum
 *      GeomRegB.rdRegLat      latitude of origin (degrees)
 *      GeomRegB.rdRegLon      longitude of origin (degrees, west is -ve)
 *      GeomRegB.rsRegX        column number defining origin (top left is 1,1)
 *      GeomRegB.rsRegY        row number defining origin (top left is 1,1)
 *      GeomRegB.nNumXPnts     count of columns in grid
 *      GeomRegB.nNumYPnts     count of rows in grid
 *      GeomRegB.eProjection   enumerated projection name
 *      GeomRegB.eStorDsc      enumerated storage description
 *      GeomRegB.rsParm1       geometry parameter 1 value defined for
 *                                 each projection in table projection
 *      GeomRegB.rsParm2       geometry parameter 2 value defined for
 *                                 each projection in table projection
 *      GeomRegB.rsParm3       geometry parameter 3 value defined for
 *                                 each projection in table projection
 *      GeomRegB.rsParm4       geometry parameter 4 value defined for
 *                                 each projection in table projection
 *      GeomRegB.rsParm5       geometry parameter 5 value defined for
 *                                 each projection in table projection
 *      parsFbuffA             array of floating-point parameter values for
 *                                 each point of the grid; storage order
 *                                 each point of the grid; storage order
 *                                 depends on the enumerated data type
 *                                 pGeomRegA.eStorDsc
 *
 * OUTPUTS:
 *      parsFbuffB              array of floating-point parameter values for
 *                                 each point of the grid; storage order
 *                                 depends on the enumerated data type
 *                                 pGeomRegB.eStorDsc
 *
 *      nStatus                 returns 0 on success, -1 if prdXcoord or
 *                                 prdYcoord is outside the grid, if prdLat
 *                                 or prdLon is invalid, or if prdXcoord and
 *                                 prdYcoord is the grid origin
 *****************************************************************************/
  
#if 0

   GeomRegA.rdRegLat   = -90.0;
   GeomRegA.rdRegLon   =   0.0;
   GeomRegA.rsRegX     =  1;
   GeomRegA.rsRegY     =  1;
 above is what i wanted to set to, but underlying routines demand otherwise
 I had to register the grid at the center, use -180 instead of 180.
#endif
   GeomRegA.rdRegLat   =   0.0;
   GeomRegA.rdRegLon   =  -180.0;
   GeomRegA.rsRegX     =  72;
   GeomRegA.rsRegY     =  37;
   GeomRegA.rsXDistance=  277.997;
   GeomRegA.rsYDistance=  277.997;
   GeomRegA.rsParm1    =  2.5;
   GeomRegA.rsParm2    =  2.5;
   GeomRegA.rsParm3    = -1.0;
   GeomRegA.rsParm4    = -1.0;
   GeomRegA.rsParm5    = -1.0;
   GeomRegA.nNumXPnts  =  144;
   GeomRegA.nNumYPnts  =  73;
   GeomRegA.eProjection=  RWS_SPHERICAL;
   GeomRegA.eStorDsc   =  pXinpY;
   GeomRegB.rdRegLat   =  90.0;
   GeomRegB.rdRegLon   = -80.0;
   GeomRegB.rsRegX     =  32.205;
   GeomRegB.rsRegY     =  32.205;
   GeomRegB.rsXDistance=  381.;
   GeomRegB.rsYDistance=  381.;
   GeomRegB.rsParm1    =  60.0;
   GeomRegB.rsParm2    = -80.0; 
   GeomRegB.rsParm3    = -1.0;
   GeomRegB.rsParm4    = -1.0;
   GeomRegB.rsParm5    = -1.0;
   GeomRegB.nNumXPnts  =  65;
   GeomRegB.nNumYPnts  =  65;
   GeomRegB.eProjection=  RWS_POLAR;
   GeomRegB.eStorDsc   =  pXinnY;
#if 0
   printf ("before GridMap \n");
   printf ("parsFbuffA : %f  %f  \n", parsFbuffA[1],parsFbuffA[1000]);
#endif

   if ( *sflag = GridMap( &GeomRegA, &GeomRegB, parsFbuffA, parsFbuffB ))
        {
         printf("Error from GridMap (%d)\n", *sflag );
        }
        memcpy ( gfield, parsFbuffB, 16900 );
 }


}
