#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdio.h>
#include <errno.h>

#define BUFSIZE 256
/* Pedro Tsai : Retrun difference in hours btwn 2 dtg values 
   To compile: gcc dtgdiff.c -o dtgdiff 
*/

void parser(char* dtg_input) ;
char filetype[2],buffer[BUFSIZE],incre[BUFSIZE],decre[BUFSIZE] ;
long year,month,date,hours ;

int main(int argc, char *argv[])
{
  time_t  seconds, seconds_2 , sec , *ptr_seconds ;
  struct tm *ptr_tm, dtg , *ptr_dtg , dtg2;
  const time_t sec_in_hour=3600 ;
  int nlen , index , diffhours ;

#define FIELDWIDTH 9  /* Fieldwidth is 11 -> YYYYMMDDHH plus Null terminating char */
  char s[FIELDWIDTH] ;
  ptr_seconds=&seconds ;
	
if ( argc != 3 ) 
{
  fprintf(stderr, "Usage: %s DTG1 DTG2 \n",argv[0] );
  fprintf(stderr, "\tReturn DTG1(YYMMDDHH) - DTG2(YYMMDDHH)\n" );
  fprintf(stderr, "\nExample: \"dtgdiff 94070315 94070403\" will return -12\n") ;
  fprintf(stderr, "\nExample: \"dtgdiff 94070423 94070403\" will return  20\n") ;


	exit(1) ; 
}
/* Get first dtg */
        if ( ! argv || ( argv[1] != '\0' ) )
	{
	  strncpy(s,argv[1],FIELDWIDTH-1) ;
	  s[FIELDWIDTH]='\0' ;
	  parser(s) ;
	}

time(&seconds) ; /* get the GMT offset from the local machine */
if (seconds == -1 ) {
   fprintf(stderr,"error in time function,errno = %d \n",errno) ;
   return 1 ; }
ptr_tm=gmtime(&seconds) ;

/* convert first DTG date to seconds */
     dtg.tm_sec=0 ;
     dtg.tm_min=0 ;
     dtg.tm_hour=(int) hours ; 
     dtg.tm_mday=(int) date  ; 
     dtg.tm_mon=(int) (month-1) ; 
     dtg.tm_year=(int) year ;  
     dtg.tm_wday=0 ;
     dtg.tm_yday=0 ;
     dtg.tm_isdst=ptr_tm->tm_isdst ; 
/*   dtg.tm_zone="PSD" ; */
     dtg.tm_gmtoff=ptr_tm->tm_gmtoff ;  
     seconds=timegm(&dtg) ;

/* Get the second dtg */
        if ( ! argv || ( argv[2] != '\0' ) )
	{
	  strncpy(s,argv[2],FIELDWIDTH-1) ;
	  s[FIELDWIDTH]='\0' ;
	  parser(s) ;
	}
/* convert the second DTG date to seconds */
     dtg2.tm_sec=0 ;
     dtg2.tm_min=0 ;
     dtg2.tm_hour=(int) hours ; 
     dtg2.tm_mday=(int) date  ; 
     dtg2.tm_mon=(int) (month-1) ; 
     dtg2.tm_year=(int) year ;  
     dtg2.tm_wday=0 ;
     dtg2.tm_yday=0 ;
     dtg2.tm_isdst=ptr_tm->tm_isdst ; 
/*   dtg2.tm_zone="PSD" ; */
     dtg2.tm_gmtoff=ptr_tm->tm_gmtoff ;  
     seconds_2=timegm(&dtg2) ;

/* Subtract or add a specified number of hours from the DTG time */
     seconds -= seconds_2 ;
     diffhours = (int) (seconds / sec_in_hour ) ;
     printf("%d\n", diffhours) ;

return 0 ;
}

void parser(char* dtg_input)
{
	char tmpstr[3] ;
	int index=0 ;
	
	tmpstr[0]=dtg_input[0] ;
	tmpstr[1]=dtg_input[1] ;
	tmpstr[2]='\0' ;
	year=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[2] ;
	tmpstr[1]=dtg_input[3] ;
	tmpstr[2]='\0' ;
	month=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[4] ;
	tmpstr[1]=dtg_input[5] ;
	tmpstr[2]='\0' ;
	date=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[6] ;
	tmpstr[1]=dtg_input[7] ;
	tmpstr[3]='\0';   
	hours=atoi(tmpstr) ;

}
