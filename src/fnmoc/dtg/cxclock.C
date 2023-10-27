#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <iostream.h>
#include <iomanip.h>
#include <stdio.h>
#include <errno.h>
#
#include "cxclock.h"

cxclock::cxclock()
{
	cxclock::sys_time() ;
}

cxclock::cxclock(const char* tz)
{  
        sprintf(clockenv,"TZ=%s\0",tz) ;
        putenv(clockenv) ;
	  cout << clockenv << '\n';
//	cxclock::set_user_time(s) ;
        cxclock::sys_time() ;
}

void cxclock::reset(const char* s)
{	
	cxclock::set_user_time(s) ;
}

void cxclock::reset(void)
{
	cxclock::sys_time() ;
}

void cxclock::get_tm_struct(time_t t)
{
	// struct tm *ptr_tm ;
        tm *ptr_tm ; 
	time_t sec ;
	sec=t ;

	// get tm struct from seconds

#ifdef SunOS
	ptr_tm=gmtime(&sec) ;
#else
        ptr_tm=localtime(&sec) ;
#endif

	if ( ! ptr_tm ) {
		cerr << "error in gmtime function,errno = " << errno << endl ;
		exit(-1) ;
	}
	
	// copy tm struct to cxclock private members

	epoch_time_in_sec=sec ;
	year=ptr_tm->tm_year +1900  ;
	month=(ptr_tm->tm_mon) + 1 ;
	date=ptr_tm->tm_mday ;
	hour=ptr_tm->tm_hour ;
	minute=ptr_tm->tm_min ;
	second=ptr_tm->tm_sec ;

#ifdef SunOS
     	strncpy(timezone,ptr_tm->tm_zone,sizeof(timezone)-1) ;   
#else
	// tzname is an external variable which contain timezone 
        // string for SVR5 Unix system (SGI, Solaris,HP,...)
        strncpy(timezone,tzname[0], sizeof(timezone)-1) ;
#endif

	// get julian date
	char buf[10] ;
	strftime(buf, sizeof(buf),"%j", ptr_tm) ;
	julian_day=atoi(buf) ;
}

void cxclock::advance(const int offset_hrs)
{

#define SEC_TO_HR 3600

	// Compute new seconds form epoch
	int offset_sec ;
	
	offset_sec=offset_hrs * SEC_TO_HR ;
	time_t new_epoch_time = epoch_time_in_sec + offset_sec ;   
	
	// Set time using new epoch time
	get_tm_struct(new_epoch_time) ;
}


void cxclock::set_user_time(const char* s)
{
	time_t sec ;
	struct tm *ptr_tm ;
	dtg_parser(s) ;

	time(&sec) ; /* get the GMT offset from the local machine */
	if (sec == -1 ) {
   		cerr << "error in time function,errno = " << errno << endl ;
   		exit(-1) ;
	}
	
	ptr_tm=gmtime(&sec) ;
	if ( ! ptr_tm ) {
		cerr << "error in gmtime function,errno = " << errno << endl ;
		exit(-1) ;
	}

//	convert the DTG date to seconds 
	// ptr_tm->tm_sec=0 ;
	// ptr_tm->tm_min=0 ;
	ptr_tm->tm_hour=(int) hour ; 
	ptr_tm->tm_mday=(int) date  ; 
	ptr_tm->tm_mon=(int) (month-1) ; 
	ptr_tm->tm_year=(int)(year ) -1900;  

	// get julian date
	char buf[10] ;
 
// Convert a tm structure to a calendar time (seconds since 
// 00:00:00 UTC, January 1, 1970).

#ifdef SunOS
        sec=timegm(ptr_tm) ;
#else
	sec=mktime(ptr_tm) ;
#endif

	ptr_tm=gmtime(&sec) ;
	epoch_time_in_sec=sec ;

	strftime(buf, sizeof(buf),"%j", ptr_tm) ;
	julian_day=atoi(buf) ;
	minute=0 ;
	second=0 ;

}

void cxclock::sys_time()
{
	time_t sec ;

	time(&sec) ; /* get the GMT offset from the local machine */
	if (sec == -1 ) {
   		cerr << "error in time function,errno = " << errno << endl ;
   		exit(-1) ;
	}

	// Set tm struct using new epoch time
	get_tm_struct(sec) ;

}

void cxclock::dtg_parser(const char* dtg_input)
{
	char tmpstr[5] ;

        if ( strlen(dtg_input) != 10 )
        {
	  cerr << "Day Time Group format error: \n" 
               << "\tThe correct format is YYYYMMDDHH\n" 
               << "\twhile your input DTG string is " << dtg_input 
               << "\t......aborting\n" ;
          exit(-1) ;
        }

	tmpstr[0]=dtg_input[0] ;
	tmpstr[1]=dtg_input[1] ;
	tmpstr[2]=dtg_input[2] ;
	tmpstr[3]=dtg_input[3] ; 
	tmpstr[4]='\0' ;
	year=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[4] ;
	tmpstr[1]=dtg_input[5] ;
	tmpstr[2]='\0' ;
	month=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[6] ;
	tmpstr[1]=dtg_input[7] ;
	tmpstr[2]='\0' ;
	date=atoi(tmpstr) ;

	tmpstr[0]=dtg_input[8] ;
	tmpstr[1]=dtg_input[9] ;
	tmpstr[3]='\0';   
	hour=atoi(tmpstr) ;
	
}

ostream& operator<<(ostream& os, cxclock& cs)
{
        os << cs.year << ' ' ;
	os << setw(2) << setfill('0') << cs.month << ' ' ;
	os << setw(2) << setfill('0') << cs.date << ' ' ; 
	os << setw(2) << setfill('0') << cs.hour << ' ' ; 
	os << setw(2) << setfill('0') << cs.minute << ' ' ; 
	os << setw(2) << setfill('0') << cs.second << ' ' ;
	os << setw(3) << setfill('0') << cs.julian_day << ' ' ;
	os << cs.timezone ;
        return os ;
}



