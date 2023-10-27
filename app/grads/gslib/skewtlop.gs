From hart@EMS.PSU.EDUMon Oct 21 10:49:58 1996
Date: Mon, 21 Oct 1996 04:01:58 -0400
From: Bob Hart <hart@EMS.PSU.EDU>
Reply to: GRADSUSR@icineca.cineca.it
To: Multiple recipients of list GRADSUSR <GRADSUSR@icineca.cineca.it>
Subject: skewtlogp.gs - GrADS Function to Plot a SkewT/Log P Diagram

Hello Folks,

    I've gotten quite a few requests over the past few weeks for
a script to plot soundings on skewt/logp diagrams.  I've generalized
the script greatly so that it should work for anyone now.   The
fully documented script (nearly 800 lines) follows this brief
description.

Description:

skewtlogp.gs - GrADS function to plot a temperature/dewpoint sounding
on a skewt/logP diagram.   GrADS must be in portrait mode.  The script
will work for either regular pressure levels (LINEAR MAPPING in the
ctl file) or irregular levels (LEVELS MAPPING).  The data must
be continuous, however (no missing data between two levels of valid
data).

Features:

    - Stretchable Skewt diagram.   You can alter the "skewness" of
      the diagram for your needs, as well as the temperature ranges
      of the diagram.  The default parameters are usually sufficient.

    - Wind Profile.

    - Stability Indices including K, TT, LI

    - Surface-based CAPE given.

    - Hodograph

    - Parcel path tracing

    - Extremely flexible options... including contour intervals,
      hodograph location, wind profile location,
      and switching off all the above.

Typical Call to the routine:

skewtlogp(temp,dewp,wspd,wdir)

A sample gif image of the output can be found at:

http://www.ems.psu.edu/wx/gifs/skewtlogp.gif

That's it.  I know there are many out there who were waiting for
this.  I hope it is useful to you...   send any problems or
suggestions you may have.

The script follows.

-Bob Hart
PSU Meteorology

--------------------------- SNIP ---------------------------------------

function skewtlogp(sndtemp,snddewp,sndspd,snddir)
"clear"
*************************************************************************
*
* GrADS Script to Plot a SkewT/LogP Diagram
*
* Bob Hart
* Graduate Student
* Penn State University / Dept of Meteorology
* Last Update:  Oct 21, 1996
*
* Features:
*   - All features of standard skewt/logp plot
*   - LCL location
*   - Parcel trajectory
*   - Stability Indices
*   - CAPE
*   - Wind Profile
*   - Hodograph
*
*
* There are numerous tunable parameters below to change the structure,
* and output for the diagram.
*
* Function Arguments:
*    sndtemp - temperature data as a function of pressure
*    snddewp - dewpoint data as a function of pressure
*    sndspd  - wind speed data as a function of pressure
*    snddir  - wind direction data as a function of pressure
*
* NOTE:  This script expects you to be in portrait mode.
*
* NOTE:  Make sure to set the vertical range before running.
*        I.e., "SET LEV 1050 150", for example.
*
* Please send any problems, comments, or suggestions to
* <hart@ems.psu.edu>
*
**************************************************************************
*
* ------------------- Define Skew-T Diagram Shape/Slope-----------------
*
* (P1,T1) = Pres, Temp of some point on left-most side
* (P2,T2) = Pres, Temp of some point on right-most side
* (P3,T3) = Pres, Temp of some point in diagram which is mid-point
*           in the horizontal between 1 and 2.
*
* P1, P2, P3 are in mb ; T1, T2, T3 are in Celsius
*
* These define the SLOPE and WIDTH of the diagram as you see it but DO NOT
* DEFINE THE HEIGHT of the diagram as you see it.  In other words,
* 1 and 2 do NOT necessarily need to be at the bottom of the diagram and
* 3 does NOT necessarily need to be at the top.  THE VERTICAL PRESSURE RANGE
* OF THE SKEWT AS YOU SEE IT IS DETERMINED BY YOUR 'SET Z ...' COMMAND OR THE
* 'SET LEV ...' COMMAND BEFORE RUNNING THIS SCRIPT.
*
*    _______________________
*   |                       |
*   |                       |
*   |           3           |
*   |                       |
*   |                       |
*   |                       |
*   |                       |
*   |                       |
*   |                       |
*   |                       |
*   |                       |
*   |1                     2|
*   |                       |
*   |_______________________|
*
*
* A good set of defining points are given below.   Feel free
* to experiment to your liking.


P1 = 1000
T1 = -40

P2 = 1000
T2 = 40

P3 = 200
T3 = -50

* ------------------- Contour Intervals / Levels --------------------------
*
* All variables below are contour intervals/levels for diagram
*
* Thetaint = interval for potential temperature lines
* Thetwint = interval for moist pseudo adiabats
* tempint  = interval for temperature lines
* wsclevs  = contour LEVELS for mixing ratio lines
*
*
thetaint = 10
thetwint = 5
tempint = 10
wsclevs = "1 1.5 2 3 5 7 9 12 16 20 24 28 32 36 40"
*
*
* ------------------------ Output Options --------------------------------
*
* All variables below are logical .. 1=yes, 0=no
*
* DrawBarb = Draw wind barbs along right side of plot
* DrawThet = Draw dry adiabats
* DrawThtw = Draw moist pseudo-adiabats
* DrawTemp = Draw temperature lines
* DrawMix  = Draw mixing ratio lines
* DrawTSnd = Draw temperature sounding
* DrawDSnd = Draw dewpoint sounding
* DrawPrcl = Draw parcel path from LCL upward
* DrawIndx = Display stability indices & CAPE
* DrawHodo = Draw hodograph

DrawBarb = 1
DrawThet = 1
DrawThtw = 1
DrawTemp = 1
DrawMix  = 1
DrawTSnd = 1
DrawDSnd = 1
DrawPrcl = 1
DrawIndx = 1
DrawHodo = 1

*
* ----------------- Wind Barb Profile Options ----------------------------
*
* All variables here are in units of inches, unless otherwise specified
*
*  barbint = Interval for plotting barbs (in units of levels)
*  Polelen = Length of wind-barb pole
*  Poleloc = Horizontal Location of each wind-barb pole
*  Len05   = Length of each 5-knot barb
*  Len10   = Length of each 10-knot barb
*  Len50   = Length of each 50-knot flag
*  Wid50   = Width of base of 50-knot flag
*  Spac50  = Spacing between 50-knot flag and next barb/flag
*  Spac10  = Spacing between 10-knot flag and next flag
*  Spac05  = Spacing between 5-knot flag and next flag
*  Flagbase= Draw flagbase (filled circle) for each windbarb [1=yes, 0 =no]
*  Fill50  = Solid-fill 50-knot flag [1=yes, 0=no]
*
barbint= 1
polelen= 0.35
poleloc= 8.0
len05  = 0.07
len10  = 0.15
len50  = 0.15
wid50  = 0.06
spac50 = 0.10
spac10 = 0.05
spac05 = 0.05
Fill50 = 1
flagbase = 1
*
*
*---------------- Hodograph Options -------------------------------------
*
* All variables here are in units of inches, unless otherwise specified
*
* HodL = Leftmost limit of hodograph box
* HodR = RIghtmost limit of hodograph box
* HodT = Topmost limit of hodograph box
* HodB = Bottom limit of hodograph box
*
*
*
*
* !!!!! YOU SHOULD NOT NEED TO CHANGE ANYTHING BELOW HERE !!!!!
****************************************************************************
*
*------------------------------------------------------
* calculate constants determining slope/shape of diagram
* based on temp/pressure values given by user
*-------------------------------------------------------

"define m1 = ("T1"+"T2"-2*"T3") / (2*log10("P2"/"P3"))"
"define m2 = ("T2"-"T3"-m1*log10("P2"/"P3"))/50"
"define m3 = ("T1"-m1*log10("P1"))"

*-------------------------------------------
* grab user-specified pressure range to plot
*-------------------------------------------

"q dims"
rec=sublin(result,4)
zmin=subwrd(rec,11)
zmax=subwrd(rec,13)

"set z "zmin" "zmax
"set lon 0 100"
"set zlog on"
"set xlab off"

*-------------------------------------------------
* perform coordinate transformation to Skew-T/LogP
*-------------------------------------------------

"define tgrid=m1*log10(lev)+m2*lon+m3"
"define thet=(tgrid+273.15)*pow(1000/lev,0.286)-273.15"
"define es=6.112*exp(17.67*tgrid/(tgrid+243.5))"
"define ws=622*es/lev"
"define tempx=("sndtemp"-m1*log10(lev)-m3)/m2"
"define dewpx=("snddewp"-m1*log10(lev)-m3)/m2"
"set x 1"
"set parea 0.5 7 0.75 10.5"
"set axlim 0 100"
"set lon 0 100"
"set grid on 1 1"

*-----------------------
* Plot temperature lines
*-----------------------

If (DrawTemp = 1)
   "set gxout contour"
   "set ccolor 4"
   "set cint "tempint
   "set clopts 1 1 .15"
   "set clab forced"
   "d tgrid"
Endif

*------------------
* Plot dry adiabats
*------------------

If (DrawThet = 1)
   "set gxout contour"
   "set ccolor 2"
   "set cstyle 1"
   "set cint "thetaint
   "set clab off"
   "d thet"
Endif

*------------------------
* Plot mixing ratio lines
*------------------------

If (DrawMix = 1)
   "set gxout contour"
   "set cint 1"
   "set ccolor 7"
   "set clevs "wsclevs
   "set cstyle 5"
   "set clopts 3 1 .15"
   "set cthick 5"
   "set clab forced"
   "d ws"
Endif

*-----------------------------
* Plot moist (pseudo) adiabats
*-----------------------------

If (DrawThtw = 1)
   "set x 1"
   "set lon 0 100"
   "set y 1"
   "set z 1"
   "set gxout stat"
   tloop=80
   "q gr2w 50 "zmax
   rec=sublin(result,1)
   Pmin=subwrd(rec,6)
   If (Pmin < 200)
      Pmin = 200
   Endif
   While (tloop > -80)
     "set line 3 1 1"
     PTemp=Lift(tloop,1000,Pmin,m1,m2,m3,1)
     tloop=tloop-thetwint
   Endwhile
Endif

*-----------------------------------------------------
* Plot transformed user-specified temperature sounding
*-----------------------------------------------------

If (DrawTSnd = 1)
   "set gxout line"
   "set x 1"
   "set z "zmin" "zmax
   "set ccolor 1"
   "set cmark 0"
   "set cthick 10"
   "d tempx"
Endif

*---------------------------------------------------
* Plot transformed user-specified dewpoint sounding
*---------------------------------------------------

If (DrawDSnd = 1)
   "set gxout line"
   "set x 1"
   "set z "zmin" "zmax
   "set cmark 0"
   "set ccolor 1"
   "set cthick 10"
   "d dewpx"
Endif

*----------------------------------------
* Determine lowest level of reported data
*----------------------------------------

zz=1
temp=-999
While (temp < -50 & zz <= zmax)
   "set z "zz
   "d "sndtemp
   rec=sublin(result,1)
   temp=subwrd(rec,4)
   if (temp < -50)
     zz=zz+1
   endif
Endwhile
"q gr2w 50 "zz
rec=sublin(result,1)
Plev=subwrd(rec,6)
"d "snddewp
rec=sublin(result,1)
dewp=subwrd(rec,4)

*------------------------------------------
* Calculate temperature and pressure of LCL
*------------------------------------------

TLcl=Templcl(temp,dewp)
Plcl=Preslcl(temp,dewp,Plev)

*---------------------------
* Plot parcel path from LCL
*---------------------------

If (DrawPrcl = 1)
   "q w2xy 1 "Plcl
   rec=sublin(result,1)
   yloc=subwrd(rec,6)
   "set strsiz 0.1"
   "set string 7"
   "draw string 7.15 "yloc" LCL"
   "set line 1"
   "draw line 7.0 "yloc" 7.1 "yloc
   "set x 1"
   "set lon 0 100"
   "set y 1"
   "set z 1"
   "set gxout stat"
   "set line 5 3 5"
   Ptemp=Lift(TLcl,Plcl,200,m1,m2,m3,1)
Endif

*--------------------------------
* Draw stability indices and CAPE
*--------------------------------

If (DrawIndx = 1)
   Temp850=interp(sndtemp,sndtemp,850,zmax)
   Temp700=interp(sndtemp,sndtemp,700,zmax)
   Temp500=interp(sndtemp,sndtemp,500,zmax)
   Dewp850=interp(snddewp,sndtemp,850,zmax)
   Dewp700=interp(snddewp,sndtemp,700,zmax)
   Dewp500=interp(snddewp,sndtemp,500,zmax)
   K=Temp850+Dewp850+Dewp700-Temp700-Temp500
   "draw string 0.5 10.8 K  = "substr(K,1,4)
   tt=Temp850+Dewp850-2*Temp500
   "draw string 0.5 10.6 TT = " substr(tt,1,4)
   PTemp=Lift(TLcl,Plcl,500,m1,m2,m3,0)
   "define SLI="Temp500"-"PTemp""
   "d SLI"
   rec=sublin(result,8)
   SLI=subwrd(rec,4)
   "draw string 1.5 10.8 SLI = "substr(SLI,1,4)
   say TLcl " "Plcl
   Pos=CAPE(TLcl,Plcl,200,sndtemp,zmax)
   "draw string 1.5 10.6 CAPE= "substr(Pos,1,5)
Endif

*-----------------------------
* Draw wind profile along side
*-----------------------------

If (DrawBarb = 1)
   "set z "zmin" "zmax
   "set x 1"
   "set gxout stat"
   "set line 1 1 1"
   zz=1
   wspd=-999
   While (wspd < 0 & zz <= zmax)
      "set z "zz
      "d "sndspd
      rec=sublin(result,8)
      wspd=subwrd(rec,4)
      if (wspd < 0)
          zz=zz+1
      endif
   Endwhile
   While (zz < zmax)
      "set z "zz
      "d "sndspd
      rec=sublin(result,8)
      wspd=subwrd(rec,4)
      "d "snddir
      rec=sublin(result,8)
      wdir=subwrd(rec,4)
      xwind=GetUWnd(wspd,wdir)
      ywind=GetVWnd(wspd,wdir)
      "query gr2xy 5 "zz
      rec=sublin(result,1)
      y1=subwrd(rec,6)
      "set x 1"
      "set y 1"
      "define cc = "polelen"/wspd"
      "define xendpole= "poleloc"-xwind*cc"
      "define yendpole= "y1 "-ywind*cc"
      "set gxout stat"
      "d xendpole"
      rec=sublin(result,8)
      xendpole=subwrd(rec,4)
      "d yendpole"
      rec=sublin(result,8)
      yendpole=subwrd(rec,4)
      if (xendpole>0 & wspd >= 0.5)
        if (flagbase = 1)
           "draw mark 3 "poleloc " " y1 " 0.05"
        endif
        "draw line " poleloc " " y1 "  " xendpole " " yendpole
        flagloop=wspd/10
        windcount=wspd
        flagcount=0
        xflagstart=xendpole
        yflagstart=yendpole
        vect2=180-wdir
        "define dx= cos(" vect2 "*3.1415/180.0)"
        "define dy= sin(" vect2 "*3.1415/180.0)"
        "d dx"
        rec=sublin(result,8)
        dx=subwrd(rec,4)
        "d dy"
        rec=sublin(result,8)
        dy=subwrd(rec,4)
        while (windcount > 47.5)
           flagcount=flagcount+1
           dxflag=-len50*dx
           dyflag=-len50*dy
           xflagend=xflagstart+dxflag
           yflagend=yflagstart+dyflag
           windcount=windcount-50
           x1=xflagstart+0.5*wid50*xwind/wspd
           y1=yflagstart+0.5*wid50*ywind/wspd
           x2=xflagstart-0.5*wid50*xwind/wspd
           y2=yflagstart-0.5*wid50*ywind/wspd
           If (Fill50 = 1)
              "draw polyf "x1" "y1" "x2" "y2" "xflagend" "yflagend" "x1" "y1
           Else
              "draw polyd "x1" "y1" "x2" "y2" "xflagend" "yflagend" "x1" "y1
           Endif
           xflagstart=xflagstart+spac50*xwind/wspd
           yflagstart=yflagstart+spac50*ywind/wspd
        endwhile
        while (windcount > 7.5 )
           flagcount=flagcount+1
           dxflag=-len10*dx
           dyflag=-len10*dy
           xflagend=xflagstart+dxflag
           yflagend=yflagstart+dyflag
           windcount=windcount-10
           "draw line " xflagstart " " yflagstart " " xflagend " " yflagend
           xflagstart=xflagstart+spac10*xwind/wspd
           yflagstart=yflagstart+spac10*ywind/wspd
        endwhile
        if (windcount > 2.5)
           flagcount=flagcount+1
           if (flagcount = 1)
              xflagstart=xflagstart+spac05*xwind/wspd
              yflagstart=yflagstart+spac05*ywind/wspd
           endif
           dxflag=-len05*dx
           dyflag=-len05*dy
           xflagend=xflagstart+dxflag
           yflagend=yflagstart+dyflag
           windcount=windcount-5
           "draw line " xflagstart " " yflagstart " " xflagend " " yflagend
        endif
      else
        if (wspd < 0.5 & wspd >= 0)
           "draw mark 2 " x1 " " y1 " 0.08"
        endif
      endif
      zz=zz+barbint
   endwhile
Endif

*----------------
* Draw Hodograph
*----------------

If (DrawHodo = 1)
   HodL=4.5
   HodR=7.5
   xcent=0.5*HodL+0.5*HodR
   HodT=10.5
   HodB=7.5
   ycent=0.5*HodT+0.5*HodB
   "set line 0"
   "draw recf "HodL" "HodB" "HodR" "HodT
   "set line 1"
   "draw rec "HodL" "HodB" "HodR" "HodT
   "set line 7"
   "set string 1"
   "draw mark 1 "xcent " "ycent " " 3
   "draw mark 2 "xcent " "ycent " " 3
   "draw string "xcent-1.5" "ycent-0.1 " 75"
   "draw mark 2 "xcent " "ycent " " 2
   "draw string "xcent-1.0" "ycent-0.1 " 50"
   "draw mark 2 "xcent " "ycent " " 1
   "draw string "xcent-0.5" "ycent-0.1 " 25"
   "set line 1 1 5"
   zloop=zmin
   While (zloop < zmax)
      "set z "zloop
      "d "sndspd
      rec=sublin(result,8)
      wspd=subwrd(rec,4)
      "d "snddir
      rec=sublin(result,8)
      wdir=subwrd(rec,4)
      uwnd=GetUWnd(wspd,wdir)
      vwnd=GetVWnd(wspd,wdir)
      If (wspd >= 0 & zloop > zmin)
         xloc=xcent+uwnd*0.5/25
         yloc=ycent+vwnd*0.5/25
         "draw line "xold" "yold" "xloc" "yloc
      Endif
      If (wspd >= 0)
         xold=xloc
         yold=yloc
      Endif
      zloop=zloop+1
   EndWhile
Endif
Return

*************************************************************************

function Templcl(temp,dewp)

*------------------------------------------------------
* Calculate the temp at the LCL given temp & dewp in C
*------------------------------------------------------

tempk=temp+273.15
dewpk=dewp+273.15
Parta=1/(dewpk-56)
"define Partb=log("tempk"/"dewpk")/800"
"d Partb"
rec=sublin(result,1)
Partb=subwrd(rec,4)
Tlcl=1/(Parta+Partb)+56
return(Tlcl-273.15)

**************************************************************************

function Preslcl(temp,dewp,pres)

*-------------------------------------------------------
* Calculate press of LCL given temp & dewp in C and pressure
*-------------------------------------------------------

Tlcl=Templcl(temp,dewp)
Tlclk=Tlcl+273.15
tempk=temp+273.15
"define theta="tempk"*pow(1000.0/"pres",0.286)"
"d theta"
rec=sublin(result,1)
theta=subwrd(rec,4)
"define plcl=1000.0*pow("Tlclk"/"theta",3.48)"
"d plcl"
rec=sublin(result,1)
plcl=subwrd(rec,4)
return(plcl)

**************************************************************************
function Lift(startt,startp,endp,m1,m2,m3,display)

*--------------------------------------------------------------------
* Lift a parcel moist adiabatically from startp to endp.
* Init temp is startt in C.  If you wish to see the parcel's
* path plotted, display should be 1.  Returns temp of parcel at endp.
*--------------------------------------------------------------------

temp=startt
pres=startp
cont = 1
delp=10
While (pres >= endp & cont = 1)
    If (display = 1)
       "define xtemp=("temp"-m1*log10("pres")-m3)/m2"
       "d xtemp"
       rec=sublin(result,8)
       xtemp=subwrd(rec,4)
       "q w2xy "xtemp" "pres
       rec=sublin(result,1)
       xloc=subwrd(rec,3)
       yloc=subwrd(rec,6)
    Endif
    If (display = 1 & (xtemp < 0 | xtemp > 100))
       cont=0
    Else
       If (pres < startp & display = 1)
          "draw line "xold" "yold" "xloc" "yloc
       Endif
       pres=pres-delp
       xold=xloc
       yold=yloc
       lapse=gammaw(temp,pres,100)
       temp=temp-100*delp*lapse
    Endif
EndWhile
return(temp)


**************************************************************************
function CAPE(startt,startp,endp,sndtemp,zmax)

*---------------------------------------------------------------------
* Returns all postive area above LCL.
* parcel is lifted from LCL at startt,startp and is halted
* at endp.
*---------------------------------------------------------------------

Pcltemp=startt
pres=startp
cont = 1
delp=10
Pos=0
Neg=0

While (pres >= endp & cont = 1)
   EnvTemp=interp(sndtemp,sndtemp,pres-delp,zmax)
   Pcltemp=Pcltemp-100*delp*gammaw(Pcltemp,pres,100)
   "define Val=(287*log("pres"/("pres"-"delp"))*("Pcltemp"-"EnvTemp"))"
   "d Val"
   rec=sublin(result,8)
   Val=subwrd(rec,4)
   If (EnvTemp > -200 & Pcltemp > -200)
      If (Val > 0)
         Pos=Pos+Val
      Else
         Neg=Neg+Val
      Endif
   Endif
   pres=pres-delp
Endwhile

return(Pos)

***************************************************************************
function gammaw(tempc,pres,rh)

*-----------------------------------------------------------------------
* Function to calculate the moist adiabatic lapse rate based
* on the temperature, pressure, and rh of the environment.
*----------------------------------------------------------------------

tempk=tempc+273.15
"define es=6.112*exp(17.67*"tempc"/("tempc"+243.5))"
"d es"
rec=sublin(result,8)
es=subwrd(rec,4)
ws=0.622*es/(pres-es)
w=rh*ws/100
tempv=tempk*(1.0+0.6*w)

A=1.0+2.5e6*ws/(287*tempk)
B=1.0+0.622*2.5e6*2.5e6*ws/(1004*287*tempk*tempk)
Density=100*pres/(287*tempv)
lapse=(A/B)/(1004*Density)
return(lapse)

*************************************************************************
function interp(array,temparr,pres,zmax)

*------------------------------------------------------------------------
* Interpolate inside array for pressure level pres.
* Returns estimated value of array at pressure pres.
*------------------------------------------------------------------------

"set lev "pres
altpres=subwrd(result,4)
"q dims"
rec=sublin(result,4)
zlev=subwrd(rec,9)

If (altpres > pres)
   zmin=zlev+1
Else
   zmin=zlev
Endif

"set z "zmin
rec=sublin(result,1)
PAbove=subwrd(rec,4)
"d "array"(lev="PAbove")"
rec=sublin(result,8)
VAbove=subwrd(rec,4)
"d "temparr"(lev="PAbove")"
rec=sublin(result,8)
TAbove=subwrd(rec,4)
"set z "zmin-1
rec=sublin(result,1)
PBelow=subwrd(rec,4)
"d "array"(lev="PBelow")"
rec=sublin(result,8)
VBelow=subwrd(rec,4)
"d "temparr"(lev="PBelow")"
rec=sublin(result,8)
TBelow=subwrd(rec,4)

If (TAbove > -100 & TBelow > -100 & zmin < zmax)
    found = 1
Else
    found = 0
Endif

If (found = 1)
   "define
 MeanT=(log10("PAbove")*"TAbove"+log10("PBelow")*"TBelow")/(log10("PAbove"*"PBel
 ow"))"
   "d MeanT"
   rec=sublin(result,8)
   MeanT=subwrd(rec,4)+273.15
   "define LayerD=287*"MeanT"*log("PBelow"/"PAbove")/9.8"
   "d LayerD"
   rec=sublin(result,8)
   LayerD=subwrd(rec,4)
   "define DZ=287*"MeanT"*log("PBelow"/"pres")/9.8"
   "d DZ"
   rec=sublin(result,8)
   DZ=subwrd(rec,4)
   DelV=VAbove-VBelow
   Vest=VBelow+DZ*DelV/LayerD
Else
   Vest=-9999.0
Endif

Return(Vest)

****************************************************************************

function GetUWnd(wspd,wdir)

*------------------------
* Get x-component of wind.
*------------------------


If (wspd > 0)
   convdir=270.0-wdir
   "define xwind = " wspd "*cos(" convdir "*3.1415/180.0)"
   "d xwind"
   rec=sublin(result,8)
   xwind=subwrd(rec,4)
Else
   xwind = -9999.0
Endif
return(xwind)

**************************************************************************

function GetVWnd(wspd,wdir)

*-----------------------
* Get y-component of wind
*------------------------

If (wspd > 0)
   convdir=270.0-wdir
   "define ywind = " wspd "*sin(" convdir "*3.1415/180.0)"
   "d ywind"
   rec=sublin(result,8)
   ywind=subwrd(rec,4)
Else
   ywind=-9999.0
Endif

return(ywind)
