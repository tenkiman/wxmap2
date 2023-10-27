function main(args)
*
*	plot H/L using the NCEP user-defined function clhilo
*
*	clhilo.f modified by LCDR Mike Fiorino on 960214
*	philo2.gs created by LCDR Mike Fiorino on 960214
*
*	input args:
*
*	varo = GrADS expression to plot H/L
*	ptype = 
*		maxmin	- plot both H and L
*		max	- plot only H
*		min	- plot only H
*
*	fmt = fortran-style format for the H/L value
*	clint = contour level parameter of the clhilo.f alogorithm
*	clrad = radius parameter (km) of the clhilo.f alogorithm
*		as clrad decrease the number of H/L increases
*
*	current defaults:
*	
*	fmt=i4 or I4 output (e.g., slp is displayed as 1024)
*	clint = '' use the  GrADS contour interval
*	clrad = 1000 km or synotpic scale H/L
*
varo=subwrd(args,1)
clrad=subwrd(args,2)
clint=subwrd(args,3)
ptype=subwrd(args,4)
fmt=subwrd(args,5)
*
*	set defaults
*
if(ptype='') ; ptype=maxmin ; endif
if(fmt='') ; fmt=i4 ; endif
if(clrad='') ; clrad=1000 ;endif
*
*	run the clhilo function
*
rc=clhilo(varo,ptype,fmt,clint,clrad)

return

*
*-------------------------- clhilo ------------------
*
function clhilo(var,maxmin,fmt,cint,rad)

  if(maxmin = "maxmin" | maxmin = "MAXMIN")
    mm=0.0
  endif

  if(maxmin = "max" | maxmin = "MAX")
    mm=1.0
  endif

  if(maxmin = "min" | maxmin = "MIN")
    mm=-1.0
  endif
*
*	set gxout to stat to find the GrADS contour interval
*
  if(cint = -999 | cint='') 
    'set gxout stat'
    'd 'var
    dum=sublin(result,9)
    say "dum="dum
    cint=subwrd(dum,7)
    say "cint set to "cint
    'set gxout contour'
  endif
*
*	the output of clhilo.f goes to the udfile file
*
  udfile="udf.clhilo.vals"
  '!rm 'udfile

  'd clhilo('var','mm','rad','cint','fmt')'
*
*	parse the udfile 
*
  while (1)
    res=read(udfile)
    rc=sublin(res,1)
    if (rc != 0)
      if(rc = 1); say "open error for file "udfile; return; endif
      if(rc = 2); say "end of file for file "udfile; break; endif
      if(rc = 9); say "I/O error for file "udfile; return; endif
    endif
    dum=sublin(res,2)
    maxormin=subwrd(dum,1)
    lon=subwrd(dum,2)
    lat=subwrd(dum,3)
    val=subwrd(dum,4)

    'q w2xy 'lon' 'lat
    x=subwrd(result,3)
    y=subwrd(result,6)
    if(maxormin = "max"); str="H"; 'set string 4 c 6'; endif
    if(maxormin = "min"); str="L"; 'set string 2 c 6'; endif
    'set font 5'
    'set strsiz 0.1'
    'draw string 'x' 'y' 'str
    'set font 0'
    'set strsiz 0.07'
    'set string 1 tc 4'
    ytop=y-0.1
    'draw string 'x' 'ytop' 'val
    
  endwhile
  rc=close(udfile)

return





