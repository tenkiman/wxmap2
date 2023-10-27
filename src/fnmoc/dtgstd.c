/*..................START PROLOGUE......................................
 *
 * SCCS IDENTIFICATION:  %W% %G%
 *
 * CONFIGURATION IDENTIFICATION:
 *
 * FUNCTION NAME:  dtg
 *
 * DESCRIPTION:  Program to access the system date-time-group (DTG) and
 *               write it to standard output in YYYYMMDDHH format or in
 *               any user specified format allowed by UNIX date command.
 *
 * COPYRIGHT:    (c) 1993 FLENUMOCEANCEN
 *               U.S. GOVERNMENT DOMAIN
 *               ALL RIGHTS RESERVED    
 *
 * CONTRACT NUMBER AND TITLE:  
 *
 * REFERENCES:  man pages -- date(1), gmtime(3), strftime(3)
 *
 * CLASSIFICATION:  UNCLASSIFIED
 *
 * RESTRICTIONS:  On Sun workstations, 1901121500 < DTG < 2038011500
 *                due to limited time keeping range of 32 bit word.
 *                No known limits on Cray.
 *
 * COMPUTER/OPERATING SYSTEM DEPENDENCIES:  see restrictions,
 *		beware of dynamic linking on Sun workstations
 *
 * LIBRARIES OF RESIDENCE:  
 *
 * USAGE:  dtg [-h hours] [-d days] [-f opt] [+format]
 *
 * PARAMETERS:
 *     Name       Type      Usage        Description
 *  ---------    -------    ------    --------------------------------------
 *   hours       integer   optional   hours DTG output is incremented
 *   days        integer   optional   days DTG output is incremented
 *   opt         char      optional   "watch" outputs 00 or 12
 *                                    "day" outputs Sun-Sat
 *                                    "month" outputs Jan-Dec
 *                                    "day_of_year" outputs 1-365 
 *   format      char      optional   format string as in 'date' command
 *					see man for date(1) and strftime(3)
 *
 * RETURN CODE:     0    -> normal exit
 *               nonzero -> error in DTGOPS
 *
 * FILES:  standard output (formatted DTG)
 *         standard error (usage message)
 *
 * DATA BASES:  None
 *
 * NON-FILE INPUT/OUTPUT:  (1)  command line switches -d -h -f +
 *                         (2)  environment variable CRDATE (see DTGOPS)
 *
 * ERROR CONDITIONS:
 *     Condition                 Action
 *  -----------------        ----------------------------
 *  DTGOPS error             return nonzero status
 *  bad switch               return nonzero status
 *
 * ADDITIONAL COMMENTS:
 *
 *..................MAINTENANCE SECTION.................................
 *                                
 * FUNCTIONS CALLED:
 *   Name                  Description
 *  -------     ------------------------------------------
 *  DTGOPS      FNOC FORTRAN subroutine that returns system DTG
 *  dtg_to_sec  convert DTG string to seconds
 *  getopt	parse command line switches and arguments
 *  gmtime	convert system seconds to time structure (GMT)
 *  strftime	convert time structure to string under format control
 *  cptofcd	Cray function to convert a c pointer to 
 *              a fortran character descriptor
 * 
 * LOCAL VARIABLES AND		Structures are documented in detail
 *          STRUCTURES:		where they are defined in the code
				within include files
 *  Name	Type	Description
 *  ----	----	-----------
 *  err		int	return status
 *  opt		char	switch variable
 *  format	char	pointer to output format string
 *  dtg_str	char	pointer to DTG string
 *  sec		time_t	DTG in seconds
 *  cdtg	_fcd	Cray fortran character descriptor
 *
 *  argc	int	command line argument count
 *  argv	char	pointer to command line switches
 *  optarg	char	pointer to command arg (see getopt)
 *  optind	int	index of command arg (see getopt)
 *
 *  SIZE	define	maximum output string size
 *  FORMAT	define  standard FNOC DTG format = "%Y%m%d%H"	
 *  HOUR	define	seconds/hour for conversion
 *  DAY		define  seconds/day for conversion
 *  USE		define  usage message
 *
 * METHOD:  Use standard C time keeping conversion functions to
 *          manipulate DTG string returned by DTGOPS subroutine
 *
 * INCLUDE FILES:
 *    Name              Description
 *  -----------    --------------------------------------- 
 *  ctype.h        standard data type definitions
 *  stdio.h        standard i/o definitions
 *  stdlib.h       standard library definitions
 *  string.h       standard string definitions
 *  time.h         standard time definitions
 *  fortran.h      Cray fortran-c linkage definitions
 *
 * COMPILER DEPENDENCIES:  K&R or ANSI C
 *
 * COMPILE OPTIONS:  must link /usr/local/fnoc/lib/libfnoc.a
 *                   and FORTRAN libraries (for DTGOPS)
 *		FNOC=/usr/local/fnoc/lib
 *	Sun:	cc dtg.c -L$FNOC -lfnoc -L/usr/lang/SC0.0 -lF77
 *	Cray:	cc dtg.c -L$FNOC -lfnoc -lf
 *
 * MAKEFILE:
 *
 * RECORD OF CHANGES:
 *			
 * <<CHANGE NOTICE>> version 1.0 (01 Feb 1993) -- May, P.W. (CSC)
 *                   initial coding and installation :)
 *
 *..................END PROLOGUE......................................*/

#include	<ctype.h>
#include	<stdio.h>
#include	<stdlib.h>
#include	<string.h>
#include	<time.h>
#ifdef CRAY
#include	<fortran.h>
#endif

			/* Create format string for the FNOC default
			 * dtg (which is YYYYmmddHH).  Format contains
			 * % = \045 which must be escaped to prevent 
			 * misinterpretation by SCCS.			*/
#define		FORMAT	"\045Y\045m\045d\045H"
#define		HOUR	(long) (60*60)
#define		DAY	(long) (24*HOUR)
#define		SIZE	40		/* maximum output string size	*/
#define		USE	"usage:  dtg [-h hours] [-d days] [-f format]\n"
#define		HELP	"\
	hours	int	optional	hours DTG output is incremented\n\
	days	int	optional	days DTG output is incremented\n\
	opt	char	optional	\"watch\" outputs 00 or 12\n\
					\"day\" outputs Sun-Sat\n\
					\"month\" outputs Jan-Dec\n\
					\"day_of_year\" outputs 1-365\n\
	format	char	optional	format string as in \'date\' command\n\
					see man for date(1) and strftime(3)\n"

main(argc, argv)
int	argc;
char	*argv[];
{
			/* declarations	*/
	extern	char	*optarg;		/*pointer to option arg */
	extern	int	optind;			/*argument index	*/

	int	err=0;
	char	opt, *format=FORMAT, dtg_str[SIZE];
	time_t	sec, dtg_to_sec();

#ifdef CRAY
	void fortran	DTGOPS(_fcd,int*);
	_fcd		cdtg;
#endif

			/* program	*/
#ifdef CRAY
	cdtg = _cptofcd(dtg_str,10L);
        DTGOPS(cdtg,&err);			/* call Cray DTGOPS	*/
#else
	dtgops_(dtg_str,&err,10L);		/* call Sun DTGOPS	*/
#endif
	if (err) return err;
	sec = dtg_to_sec(dtg_str);		/* convert to sec	*/

			/* parse command switches	*/
	while ( (opt = getopt(argc, argv, "d:f:h:UH")) != (char) EOF )
		switch  (opt)
		{
				/* days offset		*/
			case 'd':	sec += DAY*atoi(optarg);
					break;
				/* hours offset		*/
			case 'h':	sec += HOUR*atoi(optarg);
					break;
				/* output format	*/
			case 'f':
				if (strcmp(optarg,"watch") == NULL)
					(void) strcpy(format,"%H");
				else if (strcmp(optarg,"day") == NULL)
					(void) strcpy(format,"%a");
				else if (strcmp(optarg,"month") == NULL)
					(void) strcpy(format,"%b");
				else if (strcmp(optarg,"day_of_year") == NULL)
					(void) strcpy(format,"%j");
				else
					format = optarg;
				break;
			case '?':
			case 'U':	(void) fprintf(stderr,USE);
					return 1;
			case 'H':	(void) fprintf(stderr,USE);
					(void) fprintf(stderr,HELP);
					return 1;
		}

				/* handle a format similar to "date"
				 * e.g. specified as +"%y%m%d"		*/
	if ( (optind < argc) && (*argv[optind] == '+') )
		(void) strcpy(format,argv[optind]+1);

				/* convert seconds to tm structure,
				 * fill dtg string, and display dtg	*/
	(void) strftime(dtg_str,SIZE,format,gmtime(&sec));
	(void) printf("%s\n", dtg_str);
	return err;
}


			/* convert dtg string to tm structure then to secs
			 * use system library functions
			 * mktime (ANSI C) or timegm (Sun/OS) to affect
			 * conversion of tm to seconds			*/
time_t	dtg_to_sec(dtg_str)
char	*dtg_str;
{
	int		year,month,day,hour;
	time_t		sec;
	struct tm	dat;
					/* load tm structure		*/
	(void) sscanf(dtg_str,"%4d%2d%2d%2d", &year,&month,&day,&hour);
	dat.tm_sec = 0;
	dat.tm_min = 0;
	dat.tm_hour = hour;
	dat.tm_mday = day;
	dat.tm_mon = month-1;
	dat.tm_year = year-1900;
	dat.tm_wday = 0;
	dat.tm_yday = 0;
	dat.tm_isdst = 0;
					/* convert tm to seconds	*/
#ifdef __STDC__
	sec = mktime(&dat);
#else
	dat.tm_zone = 0;
	dat.tm_gmtoff = 0L;
	sec = timegm(&dat);
#endif
	return sec;
}

