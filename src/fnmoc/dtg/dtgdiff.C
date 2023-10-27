#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdio.h>
#include <errno.h>
#include <iostream.h>

#define BUFSIZE 256

/* Pedro Tsai : Retrun difference in hours btwn 2 dtg values 
   To compile: g++ dtgdiff.C -o dtgdiff 
*/

struct date
{
long year,month,date,hours ;
} ;

date* parser(char* dtg_input)
{
        static date x ;
	char tmpstr[10] ;

	tmpstr[0]=dtg_input[0] ;
	tmpstr[1]=dtg_input[1] ;
	tmpstr[2]=dtg_input[2] ;
	tmpstr[3]=dtg_input[3] ;
	tmpstr[4]='\0' ;
	x.year=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[4] ;
	tmpstr[1]=dtg_input[5] ;
	tmpstr[2]='\0' ;
	x.month=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[6] ;
	tmpstr[1]=dtg_input[7] ;
	tmpstr[2]='\0' ;
	x.date=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[8] ;
	tmpstr[1]=dtg_input[9] ;
	tmpstr[3]='\0';   
	x.hours=atoi(tmpstr) ;

   return &x ;
}

int getsec(char* s)
{
  time_t seconds ;
  struct tm *ptr_tm , dtg ;
  date *x ; 

  /* get the GMT offset from the local machine */
  time(&seconds) ;
  if (seconds == -1 ) 
  {
     fprintf(stderr,"error in time function,errno = %d \n",errno) ;
     return 1 ; 
  }

#ifdef SunOS
     ptr_tm=gmtime(&seconds) ;
#else
     ptr_tm=localtime(&seconds) ;
#endif
     
  x=parser(s) ;

/* convert first DTG date to seconds */
     dtg.tm_sec=0 ;
     dtg.tm_min=0 ;
     dtg.tm_hour=(int) x->hours ; 
     dtg.tm_mday=(int) x->date  ; 
     dtg.tm_mon=(int) (x->month) -1  ; 
     dtg.tm_year=(int) (x->year)- 1900 ;  
     dtg.tm_wday=0 ;
     dtg.tm_yday=0 ;
     dtg.tm_isdst=ptr_tm->tm_isdst ; 
/*   dtg.tm_zone="PSD" ; */

#ifdef SunOS
     seconds=timegm(&dtg) ;
#else 
     seconds=mktime(&dtg) ;
#endif

  return seconds ;
} 

float dtgdiff(char *dtg1, char *dtg2)
{
  time_t  seconds_1, seconds_2 ; 
  const time_t sec_in_hour=3600 ;
  float diffhours ;

  seconds_1 = getsec(dtg1) ;
  seconds_2 = getsec(dtg2) ;

/* Subtract or add a specified number of hours from the DTG time */
   seconds_1 -= seconds_2 ;
   diffhours =  (seconds_1 / sec_in_hour ) ;
     cout <<  diffhours << '\n' ;

  return diffhours ;
}


int main(int argc,char* argv[]) 
{
  if ( argc <= 2 )
  {
     cerr << "Usage: " << argv[0] 
          << " dtg_1<YYYYMMDDHH> dtg_2<YYYYMMDDHH>\n" ;
  } 
  else
  {
     dtgdiff(argv[1],argv[2]) ;
  }
  return 0 ;
}



