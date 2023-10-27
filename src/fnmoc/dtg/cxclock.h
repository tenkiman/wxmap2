#include <iostream.h>
#
#ifndef _CX_CLOCK_
#define _CX_CLOCK_

#include <time.h>

class cxclock {

private:
	/* int year ;
	int month ;
	int date ;
	int hour ;
	int minute ;
	int second ; */

	time_t year ;
	time_t month ;
	time_t date ;
	time_t hour ;
	time_t minute ;
	time_t second ; 
	char timezone[32] ;

        char clockenv[64] ;

	int julian_day ;
	time_t epoch_time_in_sec ;

	// Private functions
	void dtg_parser(const char*) ;
	void sys_time() ;
	void set_user_time(const char*) ;
	void get_tm_struct(time_t) ;

public:
	cxclock() ;
	cxclock(const char*) ; // Set clock time to DTG string
	~cxclock() { } ;
	void reset(const char*) ;
	void advance(const int) ;
	void reset(void) ;
	int update() ;

	// Utility functions
	int yr() { return year ; }
	int mon() { return month ; }
	int dd() { return date ; }
	int hr() { return hour ; }
	int min() { return minute ; }
	int sec() { return second ; }
	int julian() { return julian_day ; }

	friend ostream& operator<<(ostream&, cxclock&) ;	
} ;

#endif // _CX_CLOCK_

