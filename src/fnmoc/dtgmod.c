#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdio.h>
#include <errno.h>

#define BUFSIZE 256
/* Pedro Tsai : Add/subtract hours on a given dtg value.
   To compile: gcc dtgmod.c -o dtgmod
*/


void parser(char* dtg_input) ;
char filetype[2],buffer[BUFSIZE],incre[BUFSIZE],decre[BUFSIZE] ;
long year,month,date,hours ;

int main(int argc, char *argv[])
{
  time_t  seconds, sec , *ptr_seconds ;
  struct tm *ptr_tm, dtg , *ptr_dtg ;
  const time_t sec_in_hour=3600 ;
  int nlen , index ;

#define FIELDWIDTH 9  /* Fieldwidth is 11 -> YYMMDDHH plus Null terminating char */
  char s[FIELDWIDTH] ;

  ptr_seconds=&seconds ;
	

if ( argc != 3 ) 
{
   fprintf(stderr, "Usage: argv[0] DTG +hour|-hours \n" );
   fprintf(stderr, "\twhere DTG is a character string (YYMMDDHH) and +|- \n" ); 
   fprintf(stderr, "\thours increases/decreases DTG by the specified hours\n" ) ;
   fprintf(stderr, "\nExample: \"dtgmod 94070403 +12\" will return 94070415\n") ;
   fprintf(stderr, "\nExample: \"dtgmod 94070403 -12\" will return 94070315\n") ;
   exit(1) ; 
}

	strncpy(s,argv[1],FIELDWIDTH-1) ;
	s[FIELDWIDTH]='\0' ;
       /*  fprintf(stderr,"Input dtg: %s\n", s ) ; */
	parser(s) ;

time(&seconds) ; /* get the GMT offset from the local machine */
if (seconds == -1 ) {
   fprintf(stderr,"error in time function,errno = %d \n",errno) ;
   return 1 ; }
ptr_tm=gmtime(&seconds) ;

/* convert the DTG date to seconds */
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


/* Subtract or add a specified number of hours from the DTG time */
     strcpy(buffer,argv[2]) ;
     nlen=strlen(buffer) ;
     index=0 ;

	switch( buffer[0] )
	{
	case '+' :	/* increment */
		for ( index=1; index < nlen ; index++)
			incre[(index-1)]=buffer[index] ;
		incre[index] = '\0' ;
			
		seconds=seconds+sec_in_hour*(atoi(incre)) ; 
		break ;
	case '-' :	/*  decrement */
		for ( index=1; index < nlen ; index++ )
			decre[(index-1)]=buffer[index] ; 
		decre[index] = '\0' ;
	
		seconds=seconds-sec_in_hour*(atoi(decre)) ;
		break ;
	default :
		seconds=seconds+sec_in_hour*(atoi(buffer)) ;
	} ;

ptr_dtg=gmtime(&seconds) ;

/* Out put the new DTG string */

printf("%s",filetype) ;
printf("%02d%02d",ptr_dtg->tm_year,(ptr_dtg->tm_mon + 1 )) ;
printf("%02d%02d\n",ptr_dtg->tm_mday,ptr_dtg->tm_hour) ;
 
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
