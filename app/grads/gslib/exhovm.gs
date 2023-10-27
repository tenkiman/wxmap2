From wd22sl@sgi39.wwb.noaa.gov Fri Jul 28 06:47:46 1995
Received: Fri, 28 Jul 95 06:47:45 PDT from sun1.wwb.noaa.gov by typhoon.llnl.gov (4.1/1.5)
Received: Fri, 28 Jul 95 09:51:42 EDT from sgi39.wwb.noaa.gov by sun1.wwb.noaa.gov (4.1/1.5)
Received: by sgi39.wwb.noaa.gov (920330.SGI/890607.SGI)
	(for @sun1.wwb.noaa.gov:fiorino@typhoon.llnl.gov) id AA12381; Fri, 28 Jul 95 09:51:41 -0400
Date: Fri, 28 Jul 95 09:51:41 -0400
From: wd22sl@sgi39.wwb.noaa.gov (Steve Lord)
Message-Id: <9507281351.AA12381@sgi39.wwb.noaa.gov>
To: fiorino@typhoon.llnl.gov
Subject: EXTENDED_HOVMOLLER
Status: RO
X-Status: 


Jiang, Naomi, Mark D., Glen W., P. Caplan and Mike F.:

The following is a grads script to do an extended hovmoller consisting of a set of
analyses followed by a model forecast.  The script is self-documenting in that if
you say run exthov without any arguments, the documentation will be printed out.

The input parameters allow you to set the starting time for the analysis, the
end time for the analysis and the length of the forecast.  The typical hovmoller
is longitude/time but lat/time sections can also be made.  Please read the
script and comments for more details.

A complete call of the script might be:

run exthov 00z25jul1995 00z28jul1995 v 850 72 270 370 15 -999 0

NHC users:  the relevant script file is: /tdau/grads/exthov.gs
            the relevant .ctl files are: /tdau/grads/avnuvz.anal.ctl
                                         /tdau/grads/avnuvz.anal.ctl
The user must be in /tdau/grads to run this script.  You can make it more general
with a little work.

Other Users:  the necessary .ctl files are:
              1) a .ctl file for all analyses (the NHC setup uses one for winds and
                 heights, a second one for temperature and rh, but the code for that
                 can be removed
              2) a .ctl file for each forecast time that describes the forecast. Again
                 the script can be modified to suit one's file structure.

The analyses are simple contour lines; the forecasts are shaded and contoured.  You
can fiddle with the displays to suit your taste.

Some things are not completed but are left as exercises for the interested user:

  1) Labels
  2) Averaging over latitude or longitude band (hint: use the define command)
  3) Guarantee of consistency between analyses and forecasts (hint: use gxout stat
     to pull off contouring parameters and set them explicitly for both analysis
     and forecast)

I'm sorry but I don't have time to embelish the script with the above features.

Steve L.

________________________________________________


function main(args)
  stdate=subwrd(args,1)
  endate=subwrd(args,2)
  var=subwrd(args,3)
  level=subwrd(args,4)
  fclen=subwrd(args,5)
  lonmin=subwrd(args,6)
  lonmax=subwrd(args,7)
  latmin=subwrd(args,8)
  latmax=subwrd(args,9)
  avg=subwrd(args,10)
  
  if(stdate = "" | stdate = "?")
    say "exthov.gs requires 10 arguments as follows:"
    say " 1) start date in grads format (e.g. 12z01nov1995)"
    say " 2) end date in grads format"
    say " 3) variable (u, v, t, rh, z etc.)"
    say " 4) level (mb)"
    say " 5) forecast length (hours)"
    say " 6) minimum longitude (for lat/time hovmoller)"
    say " 7) maximum longitude (for lat/time hov. but -999 for lat/time hov.)"
    say " 8) minimum latitude (for lon/time hovmoller)"
    say " 9) maximum latitude (for lon/time hov. but -999 for lat/time hov.)"
    say " 10) average flag (0 for no average, 1 for average over lat,"
    say "    2 for average over lon. for lat/time hov.)" 
    return
  endif

  ymdh=gd2ymdh(endate)
  
  if(var = "z" | var = "V" | var = "u" | var = "U" | var = "v" | var "V")
    analfile="avnuvz.anal.ctl"
    fcfile="avnuvz."%ymdh%".f0072.ctl"
  endif

  if(var = "t" | var = "T" | var = "rh" | var = "RH")
    analfile="avntrh.anal.ctl"
    fcfile="avntrh."%yymmdd%".f0072.ctl"
  endif
  say "analfile="analfile
  say "fcfile="fcfile

*  analfile="d:\grads\modcomp\avnf00.ctl"
*  fcfile="d:\grads\modcomp\avnf24.ctl"  
  'open 'analfile
  'open 'fcfile
    
  'set time 'stdate
  date1=mydate()
  'q dims'
  dum=sublin(result,5)
  tstart=subwrd(dum,9)
  'set time 'endate
  date2=mydate()
  'q dims'
  dum=sublin(result,5)
  tend=subwrd(dum,9)
  textra=int(fclen/12+0.2)
  ttot=tend+textra
  say "tstart="tstart", tend="tend", textra="textra", ttot="ttot
  'set t 'tstart' 'ttot

*  Geometry: if lonmax or latmax are -999, lonmin or latmin are the lon or
*   lat at which the hovmoller is displayed.  If averaging is desired,
*   all of lonmin/max and latmin/max must be given.

  if(lonmax = -999 & latmax = -999); say "ILLEGAL LAT/LON SPECIFICATION"; return; endif
  if(latmax = -999)
    'set lat 'latmin
    'set lon 'lonmin' 'lonmax
    xmin=lonmin
    xmax=lonmax
  endif
  if(lonmax = -999)
    'set lon 'lonmin
    'set lat 'latmin' 'latmax
    xmin=latmin
    xmax=latmax
  endif  
  if(lonmax != -999 & latmax != -999)
    say "AVERAGING IS NOT CURRENTLY SUPPORTED AND IS LEFT AS AN EXERCISE FOR THE INTERESTED STUDENT"
    return
  endif

  'set lev 'level
    
  analvar=var%".1"
  fcvar=var%".2"
  'set yflip on'
  'd 'analvar
  pull zzz
  'set gxout shaded'
  'd 'fcvar
  'set gxout contour'
  'd 'fcvar
  
*  'q w2xy 'xmin' 'endate
*  xl=subwrd(result,3)
*  yl=subwrd(result,6)
*  'q w2xy 'xmax' 'endate
*  xr=subwrd(result,3)
*  'set line 0 1 8'
*  'draw line 'xl' 'yl' 'xr' 'yl
return

function mydate
  'query time'
  sres = subwrd(result,3)
  i = 1
  while (substr(sres,i,1)!='Z')
    i = i + 1
  endwhile
  hour = substr(sres,1,i)
  isav = i
  i = i + 1
  while (substr(sres,i,1)>='0' & substr(sres,i,1)<='9')
    i = i + 1
  endwhile
  day = substr(sres,isav+1,i-isav-1)
  month = substr(sres,i,3)
  year = substr(sres,i+3,4)
  dow=subwrd(sres,6)
  return (hour' 'day' 'month' 'year' 'dow)

function int(stuff)

  res = ''
  i = 1
  c = substr(stuff,i,1)
  while (c!='' & ('x'%c)!='x.') 
    res = res%c
    i = i + 1
    c = substr(stuff,i,1)
  endwhile
return res

function gd2ymdh(gdate)
  ucmon="JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC"
  lcmon="jan feb mar apr may jun jul aug sep oct nov dec"
  i = 1
  while (substr(gdate,i,1)!='Z' & substr(gdate,i,1)!='z')
    i = i + 1
  endwhile
  hour = substr(gdate,1,i-1)
  isav = i
  i = i + 1
  while (substr(gdate,i,1)>='0' & substr(gdate,i,1)<='9')
    i = i + 1
  endwhile
  day = substr(gdate,isav+1,i-isav-1)
  month = substr(gdate,i,3)
  year = substr(gdate,i+5,2)
  im=1
  while (im <= 12)
    ucmo=subwrd(ucmon,im)
    lcmo=subwrd(lcmon,im)
    if(month = ucmo | month = lcmo); imon=im; break; endif
    im=im+1
  endwhile
  if(imon < 10); imon="0"%imon; endif
  ymdh=year%imon%day%hour
return ymdh

________________________________________________


