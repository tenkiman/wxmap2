/**********************************************************************
 *
 * IDENTIFICATION:
 *    get_grid_tapt.c - Gets a NOGAPS file from the TEDS database 
 *                      specifically for TAPT grid (37x25)
 *
 *               (1)---55N--->(37)
 *                      .
 *                      .
 *                      .
 *                  --------->
 *               90E--------->180W
 *                  ----5S--->(925)
 *
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
 *    presl - requested pressure level    
 *    parm  - requested parameter 
 *    itau  - requested forecast hour
 * OUTPUTS:
 *    gfield - array containing field returned to calling program (FORTRAN) 
 *    sflag  - status flag returned to calling program
 **********************************************************************/

   get_grid_tapt(icentury,idate, presl, parm, itau, gfield, sflag) 

int    *icentury;       /* century               */ 
int    idate[4];        /* Array containing date/time               */ 
int    *presl;		/* array of pressure levels to analyze       */
int    *parm;           /* Index of parameter type                   */ 
int    *itau;           /* Forecast hour                             */
float  *gfield;         /* Array for request field                    */
int    *sflag;          /* Status flag                               */

{

/* DEFINE STATEMENTS */

#define  ATCF_VAPORPRESSURE 55
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

   int            u_comp = ATCF_U_COMPONENT;
   struct tm      tmStruct;
   int            pindex = 0, n = 0;
   time_t         theTime; 
   MAGRIDRET        magridRet;
   MAGRIDQUERY      GridQuery;
   MAGRIDFORMAT     stGridFormat;
   long             lNumFound = 0;
   MAGRIDLINKEDLIST GridDataLL, *pGridDataLL = 0;
   MAGRIDDATA       *pGridData = 0;
   
   
#if 0   
   printf("in get_grid,presl=%d,parm=%d,itau=%d \n",*presl,*parm,*itau);
   printf("in get_grid,date=%d %d %d %d\n",idate[0],idate[1],idate[2],idate[3]);
#endif

/* figure out date from idate(4) */

   memset ( &magridRet, 0, sizeof ( MAGRIDRET ) );
   memset ( &tmStruct, 0, sizeof ( struct tm ) );
   tmStruct.tm_year = idate[0] + *icentury*100 - 1900;
   tmStruct.tm_mon = idate[1] - 1;
   tmStruct.tm_mday = idate[2];
   tmStruct.tm_hour = idate[3];

   theTime = mktime ( &tmStruct );
/* printf ( "BaseTime is (%d:%s)\n", theTime, ( char * ) ctime ( &theTime ) ); */

   memset ( &stGridFormat, 0, sizeof ( MAGRIDFORMAT ) );

   pindex = *parm;
    
   /****************************************/
   /* Populate the catalog query structure */
   /****************************************/
   memset(&GridQuery, 0, sizeof(MAGRIDQUERY));
   memset(&GridDataLL, 0, sizeof(MAGRIDLINKEDLIST));
   GridQuery.lGeneratingProcId   = 58;       /* NOGAPS                */
   GridQuery.lProductionCenterId = 58;       /* US Navy               */
   GridQuery.lSubCenterId        = 0;        /* FNMOC                 */
   GridQuery.lGridId             = 240;
          
   GridQuery.lParameterId        = MAGRID_QUERY_WILDCARD;
   GridQuery.lBeginBaseTime      = ( long ) theTime;
   GridQuery.lEndBaseTime        = ( long ) theTime;
   GridQuery.lBeginTau           = ( long ) *itau * 60;     /* TAU in minutes        */
   GridQuery.lEndTau             = ( long ) *itau * 60;     /* TAU in minutes (24hr) */
   GridQuery.rsBeginLevel        = *presl;
   GridQuery.rsEndLevel          = 0;
   GridQuery.lLevelType          = MAGRID_QUERY_WILDCARD;
   GridQuery.stGeoArea.rsNLat    =  55.0;
   GridQuery.stGeoArea.rsSLat    = - 5.0;
   GridQuery.stGeoArea.rsELon    = -180.0;
   GridQuery.stGeoArea.rsWLon    = - 90.0;
   /**************************************/     
   /* Populate the grid format structure */
   /**************************************/
   stGridFormat.eOutputFormat      = MAGRID_GET_AS_SPECIFIED;
   stGridFormat.lMaxXPoint         = 37;
   stGridFormat.lMaxYPoint         = 25;
   stGridFormat.eScanMode          = MAGRID_pXinpY;
   stGridFormat.stProjectionDesc.eProjection = MAGRID_SPHERICAL;
   stGridFormat.lUnitId            = MAGRID_QUERY_WILDCARD;
      

    switch(pindex)
    {
/*******************************************************************/
/*    Case 1 gets geopotential height field                        */
/*******************************************************************/
       case 1:
              stGridFormat.lUnitId = ATCF_GPM; /*geopotential meters*/
              GridQuery.lParameterId = ATCF_GEOPOTENTIAL;/*gpm*/
	      GridQuery.lLevelType = ATCF_PRES_LEVEL; /*pressure level*/
              break;
/*******************************************************************/
/*    Case 2 gets temperature field                                */
/*******************************************************************/
       case 2:
              stGridFormat.lUnitId = ATCF_KELVIN;
              GridQuery.lParameterId = ATCF_TEMPERATURE;             
	      GridQuery.lLevelType = ATCF_PRES_LEVEL;
              break;
/*******************************************************************/
/*    Case 3 gets vapor pressure                                   */
/*******************************************************************/
       case 3:
              stGridFormat.lUnitId = ATCF_MILLIBARS;               
              GridQuery.lParameterId = ATCF_VAPORPRESSURE;
	      GridQuery.lLevelType = ATCF_PRES_LEVEL; 
              break;
/*******************************************************************/
/*    Case 4 gets u component of wind                              */
/*******************************************************************/
       case 4:  
              stGridFormat.lUnitId = ATCF_MPS;
              GridQuery.lParameterId = ATCF_U_COMPONENT;
	      GridQuery.lLevelType = ATCF_PRES_LEVEL; 
	      /*printf ( "GridQuery.lParameterId = %d\n", GridQuery.lParameterId );*/
              break;
/*******************************************************************/
/*       case 5 gets v component of wind                           */
/*******************************************************************/ 
       case 5:
              stGridFormat.lUnitId = ATCF_MPS;              
              GridQuery.lParameterId = ATCF_V_COMPONENT;
	      GridQuery.lLevelType = ATCF_PRES_LEVEL; 
              break;
/*******************************************************************/
/*       case 6 gets sfc pressure                                  */
/*******************************************************************/ 
       case 6:
              stGridFormat.lUnitId = ATCF_MILLIBARS;
              GridQuery.lParameterId = ATCF_PRESSURE;
	      GridQuery.lLevelType = ATCF_MSL; 
              break;
   } 


   /**************************************************************/
   /* Call the API MAGRIDGet2DByQuery to retrieve multiple Grids */
   /**************************************************************/
   magridRet = MAGRIDGet2DByQuery ( &GridQuery, &stGridFormat,
                            &lNumFound, &GridDataLL );
   sflag = &magridRet.nStatus; 
                         
   if ( magridRet.nStatus )
   {
      printf( "Error in MAGRIDGet2DByQuery (%d) (%s) (%s)\n", magridRet.nStatus,
                          magridRet.szSQLState, magridRet.szErrorMessage );
      printf( "ErrorMessage (%s)\n", magridRet.szErrorMessage);
   }
   else
   {         
      /**************************/
      /* Display output values. */
      /**************************/
      if (lNumFound < 1)
      {
         /* printf("\nNo grids were found.\n"); */
      }
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
            memcpy ( gfield, pGridData->pGridFieldData, pGridData->ulSize );

         }
         MAGRIDFreeLL( &GridDataLL );
      }
   }


}
