From love@nrlmry.navy.mil Wed Feb 14 08:35:23 1996
Received: Wed, 14 Feb 96 08:35:20 PST from typhoon.llnl.gov by cirrus.llnl.gov (4.1/1.5)
Received: Wed, 14 Feb 96 08:35:16 PST from nrlmry.navy.mil (helium.nrlmry.navy.mil) by typhoon.llnl.gov (4.1/1.5)
Received: from love.nrlmry.navy.mil by nrlmry.navy.mil (4.1/SMI-4.1)
	id AA16531; Wed, 14 Feb 96 08:35:28 PST
Received: by love.nrlmry.navy.mil (940816.SGI.8.6.9/940406.SGI)
	for fiorino@typhoon.llnl.gov id IAA05522; Wed, 14 Feb 1996 08:35:31 -0800
Date: Wed, 14 Feb 1996 08:35:31 -0800
From: love@nrlmry.navy.mil (Gary Love)
Message-Id: <199602141635.IAA05522@love.nrlmry.navy.mil>
Apparently-To: fiorino@typhoon.llnl.gov
Status: RO
X-Status: 

*
* NRL Environmental data Browsing System (NEBS)
*  created by Gary G. Love at NRL Monterey, Dec 93.
*  based on SJLBROWSE.GS developed by Steve J. Lord at NMC.
*  Time clock was obtained from Mike Fiorino at NMC.
*
* Must use with output.gs to print or make video frames.
* Must customize output.gs to use own devices, paths, and programs.
*
* The input files can be specified on the GrADS command line:
*	run nebs.gs gridfile surfacefile upperairfile
*
*    Surfacefile and upperairfile should be specified on the
*    command line only if both are present.
*
*    If surfacefile is specified or input to query,
*    file station.sfc must be present and specify station
*    3-character name, latitude, and longitude:
*		LAX  34.0 -118.4 
*
*    If upperairfile is specified or input to query,
*    file station.ua must be present and specify station
*    3-character name, latitude, longitude, and title:
*		MIR  32.9 -117.1 San Diego
*
function gb(parm)
'reinit'

*  Check for command line input and request file names if missing
_ftype="Grid"
parm1=subwrd(parm,1)
_slat=subwrd(parm,2)
_wlon=subwrd(parm,3)
_nlat=subwrd(parm,4)
_elon=subwrd(parm,5)

if (parm1="")
  '!ls *.ctl'
  say "Enter control file name for GRID data."
  pull _fname.1
else 
  _fname.1=parm1
endif
_gtype=substr(_fname.1,1,2)
if (_gtype="MG")
_wlon=_wlon+360
_elon=_elon+360
_dir=substr(_fname.1,3,8)
endif


* Check if surface and/or upper air data available and desired
* parm2=subwrd(parm,2)
* parm3=subwrd(parm,3)
parm3='1'; parm2='1'
if (parm3="")
  if (parm2="")
    say "Enter control file name for SURFACE data,"
    say "IF available and desired. ELSE {return}"
    pull _fname.2
    say "Enter control file name for UPPER AIR data."
    say "IF available and desired. ELSE {return}"
    if (_fname.2="")
      pull _fname.2
      if (_fname.2!="")
        _ftype="Station"
      endif
    else       
      pull _fname.3
      if (_fname.3="")
        _ftype="Surface"
      else
        _ftype="Both"
      endif
    endif
  else
    _fname.2=parm2
    _ftype="Surface"
    say "Enter control file name for UPPER AIR data."
    say "IF available and desired. ELSE {return}"
    pull _fname.3
    if (_fname.3!="")
      _ftype="Both"
    endif
  endif
else
*  _fname.2=parm2
*  _fname.3=parm3
*  _ftype="Both"
endif 

* Open gridded file
'open '_fname.1
res=result
'q file 1'
_stnnum=0
_sfcnum=0

* Open surface and/or upper air files if requested
if (_ftype="Surface")
  'open '_fname.2
  dum=sublin(result,2)
  res=subwrd(dum,2)
  if(res!="Error:")
    _fn=2
    'q file 2'
    rc=readsfc()
    rc=fnddt(_fname.2)
    _dtime.2=subwrd(rc,1)
  endif
endif
if (_ftype="Station")
  'open '_fname.2
  dum=sublin(result,2)
  res=subwrd(dum,2)
  if(res!="Error:")
   _fn=2
    'q file 2'
    rc=readua()
    rc=fnddt(_fname.2)
    _dtime.2=subwrd(rc,1)
  endif
endif
if (_ftype="Both")
  'open '_fname.3
  dum=sublin(result,2)
  res=subwrd(dum,2)
  if(res!="Error:")
    _fn=2
    'q file 2'
    rc=readua()
    rc=fnddt(_fname.3)
    _dtime.2=subwrd(rc,1)
  endif
  'open '_fname.2
  dum=sublin(result,2)
  res=subwrd(dum,2)
  if(res!="Error:")
    _fn=3
    'q file 3'
    rc=readsfc()
    rc=fnddt(_fname.2)
    _dtime.3=subwrd(rc,1)
  endif
endif

* Setup parameters and create initial display
rc=resetd()
rc=butncons()
rc=colors()
rc=clear()
rc=dobutn()
rc=dodisp()

*  MAIN LOOP  *
*  Warning: it is absolutely necessary that the following
*    functions be called in exactly this order:
gotid=0
while (1)
  if(gotid=0)
   gotid=getinfo()
  endif
  if(_pick!=2)
   rc = qbutton ()
   rc = qbar()
  endif
  if (_btn=99); break; endif
  if (_btn=97); _out=1; endif
  if (_btn=96); rc=resetd(); endif
  _display=0  
  if (_mtyp>0); 'clear'; else; rc = clear(); endif
  if (_mtyp=2); 'enable print gxout'; endif
  rc = monitor()  
  rc = display()
  if (_mtyp=2); 'disable print'; endif
  if (_mtyp>0); rc=output(); _mtyp=0; endif
  rc = dobutn()
  _supp=0
endwhile

say "BROWSE SESSION ENDED."
'quit'

return

function display()
*  Warning: it is absolutely necessary that the following
*    functions be called in exactly this order:
  'set rgb 40 64 64 64'
  'set rgb 41 255 255 0'
  if (_mtyp>0); case=_case; endif
  if (_pick=1&_styp=3); case=1; endif
  if (_pick=2&_styp=3); case=2; endif
  if (_pick=0&_styp=3&_disurf=1&_btnN="2"&_btn<0&_xpos<_timbxll&_xpos>_dimbxur); case=3; endif
  if (_tflag=0&(_btn=98|(_btn<0 & _btnN="3"))); case=4; endif
  if (case=1)
    rc=dosurf()
    _supp=1
    _case=1
  endif
  if (case=2)
    _pick=0
    rc=disurf()
    _display=0
    _supp=1
    _case=2
  endif
  if (case=3)
    rc=disurf()
    _display=0
    _supp=1
    _case=3
  endif
  if (case=4)
    rc = dodisp()
    _supp=1
    _case=4
  endif
  _tflag=0
return

function dobutn()
*  Warning: it is absolutely necessary that the following
*    functions be called in exactly this order:
  rc=vbutton()
  rc=miscbutn() 
  rc=sbutton()
  rc=stbutton()
  rc=gxbutton()
  rc=pbutton()
  rc=tbar()
  rc=dbar()
return 
  
function resetd()
  'reset'
  _clev=1
  _clk=0
  _cvar=1
  _dclick=2
  _dens=5
  _display=0
  _disurf=0
  _disgrp=0
  _entr=0
  _fram=1
  _grid=0
  _gxtp=1
    k=1
    while (k<=7)
      _gxuse.k=0
      k=k+1
    endwhile
  _mtyp=0
  _nchvr=8
  _nfram=0
  _out=0
    k=1
    while (k<=_sfcnum)
      _picked.k=0
      k=k+1
    endwhile
  _pick=0
  _poli=1
  _prj=latlon
  _proj=1
  _sfp=0
  _shad=0
  _skip=1
  _styp=3
    k=1
    while (k<=20)
      _vname.k=""
      _vtyp.k=0
      _vgxt.k=0
      _cint.k=""
      _cmax.k=""
      _cmin.k=""
      _clb.k=1
      _lbl.k=1
      _mrkr.k=0
      _styl.k=1
      k=k+1
    endwhile
  _station=0
  _supp=1
  _surface=0
  _tclick = 2
  _tflag=0
  _trans=0
  _t=1
  _t1=1
  _t2=1
  _wdrupr=0
  _wspupr=0
  _wdrsfc=0
  _wspsfc=0
  _uupr=0
  _vupr=0
 'set dfile 1'
  rc=getbasic()
 return

function getbasic()

* Get info on the file 
  'q file 1'
say result
  res = result
  dum = sublin(res,1)
  _maptitle=subwrd(dum,4)' 'subwrd(dum,5)' 'subwrd(dum,6)' 'subwrd(dum,7)' 'subwrd(dum,8)' 'subwrd(dum,9)
  dum = sublin(res,5)
  _znum = subwrd(dum,9)
  _tnum = subwrd(dum,12)
  _xnum = subwrd(dum,3)
  _ynum = subwrd(dum,6)
  dum = sublin(res,6)
  _vnum = subwrd(dum,5)
  'set x 1 '_xnum
  'set y 1 '_ynum
  'q dims'
say result
  dum = sublin(result,2)
  _lnlo = subwrd(dum,6)
  _lnhi = subwrd(dum,8)
  dum = sublin(result,3)
  _ltlo = subwrd(dum,6)
  _lthi = subwrd(dum,8)
  _x1 = 1
  _y1 = 1

* Get date time group of base time
  dum = sublin(result,5)
  _dtg = subwrd(dum,6)

* Get time limits in character form
  'set t '1
  _tc1 = mydate()
  'set t '_tnum
  _tc2 = mydate()

* Get time interval
  rc=fnddt(_fname.1)
  _dtime.1=subwrd(rc,1)
  _tinc=_dtime.1
  _tdel=_tinc
  _nint=_dtime.1/_tinc
  _tnums=(_tnum-1)*_nint+1

* Set selected domain
  if(_slon!=''&_wlon!=''&_nlat!=''&_elon!='')  
    'set lat '_slat' '_nlat
    'set lon '_wlon' '_elon
    'q dims'
    dummy = sublin(result,2)
    dum = subwrd(dummy,11)
    x1 = int(dum)
    if (x1<0); x1=x1-1; endif
    dum = subwrd(dummy,13)
    x2 = int(dum)
    if (x2>0); x2=x2+1; endif
    _x1=x1
    _xnum = x2 - x1 +1
    _lnlo = subwrd(dummy,6)
    _lnhi = subwrd(dummy,8)
    dummy = sublin(result,3)
    dum = subwrd(dummy,11)
    y1 = int(dum)
    if (y1<0); y1=y1-1; endif
    dum = subwrd(dummy,13)
    y2 = int(dum)
    if (y2>0); y2=y2+1; endif
    _y1=y1
    _ynum = y2 - y1 +1
    _ltlo = subwrd(dummy,6)
    _lthi = subwrd(dummy,8)
  endif
  _x0=_x1
  _x2=_xnum+_x1-1
  _y0=_y1
  _y2=_ynum+_y1-1
  _z1=1
  _z2=1

* Get world values for each lat and lon
  i = 1
  _lons = ''
  while (i<=_xnum) 
    'set x 'i+_x1-1
    lon=subwrd(result,4)
    if (_gtype="MG"); lon=lon-360; endif
    _lons = _lons % ' ' % lon
    i = i + 1
  endwhile
  i = 1
  _lats = ''
  while (i<=_ynum) 
    'set y 'i+_y1-1
    _lats = _lats % ' ' % subwrd(result,4)
    i = i + 1
  endwhile

* Get world values for each level
  i = 1
  _levs = ''
  while (i<=_znum) 
    'set z 'i
     lev=subwrd(result,4)
    _levs = _levs % ' ' % lev
    if(substr(lev,1,4)="1000"); l1=1; endif
    if(substr(lev,1,3)="500"); l2=1; endif
    i = i + 1
  endwhile

* Set labeling of lats, lons, levs, and time
  i = 1
  _xmark=""
  while (i<=_xnum) 
    rng=int(_lnhi-_lnlo)
    lab = subwrd(_lons,i)
    rc=ckinc(lab,rng)
    if (rc=0)
      _xmark=_xmark" "1
    else
      _xmark=_xmark" "0
    endif 
    i = i + 1
  endwhile
  i = 1
  _ymark=""
   while (i<=_ynum) 
    rng=int(_lthi-_ltlo)
    lab = subwrd(_lats,i)
    rc=ckinc(lab,rng)
    if (rc=0)
      _ymark=_ymark" "1
    else
      _ymark=_ymark" "0
    endif
    i = i + 1
  endwhile
  i = 1
  _zmark=""
  while (i<=_znum) 
    rng=_znum
    lab = subwrd(_levs,i)
    rc=ckinc(lab,rng)
    if (rc=0)
      _zmark=_zmark" "1
    else
      _zmark=_zmark" "0
    endif
    i = i + 1
  endwhile
  i = 1
  _tmark=""
  while (i<=(_tnum-1)*_nint+1) 
    rc=mod(i-1,_nint)
    if (rc=0)
      _tmark=_tmark" "1
    else
      if (_tdel<10&_iunit="MN")
        rc=mod(i-1,10)
        if (rc=0)
          _tmark=_tmark" "0
        else
          _tmark=_tmark" "s
        endif
      else
        _tmark=_tmark" "0  
      endif
    endif
    i = i + 1
  endwhile

* Get each upper variable abbreviation and build list
  i = 0
  _varsupr = ''; _upr=0
  while (i<_vnum) 
    dum = sublin(res,i+7)
    var=subwrd(dum,1)
    if(substr(var,4,3)="upr")
      _varsupr = _varsupr % ' ' % var
      _upr = _upr + 1
    endif
    j = i + 1
    if(var="wdrupr")
      _wdrupr=j
    endif
    if(var="wspupr")
      _wspupr=j
    endif
    iw=4
    while (subwrd(dum,iw) !="" & substr(var,4,3)="upr")
      _vname.j = _vname.j%" "%subwrd(dum,iw)
      iw=iw+1
    endwhile
    i = i + 1
  endwhile

*  If upper wsp and wdr present, define u and v components here.
*  Create for selected dimensions in function disp().
  if(_wdrupr!=0&_wspupr!=0)
    _varsupr=_varsupr % " uuuupr vvvupr"
    _upr=_upr+1
    _vname._upr="U COMPONENT OF WIND"
    _uupr=_upr
    _upr=_upr+1
    _vname._upr="V COMPONENT OF WIND"
    _vupr=_upr
    addupr=2
  else
    addupr=0
  endif

* Get each surface variable abbreviation and build list
  i = 0
  _varssfc = ''; _sfc=0
  while (i<_vnum) 
    dum = sublin(res,i+7)
    var=subwrd(dum,1)
    if(substr(var,4,3)="sfc")
      _varssfc = _varssfc % ' ' % var
      _sfc = _sfc + 1
    endif
    j = i + 1 + addupr
    if(var="wdrsfc")
      _wdrsfc=j
    endif
    if(var="wspsfc")
      _wspsfc=j
    endif
    iw=4
    while (subwrd(dum,iw) !="" & substr(var,4,3)="sfc")
      _vname.j = _vname.j%" "%subwrd(dum,iw)
      iw=iw+1
    endwhile
    i = i + 1
  endwhile

*  If surface wsp and wdr present, define u and v components here.
*  Create for selected dimensions in function disp().
  if(_wdrsfc!=0&_wspsfc!=0)
    _varssfc=_varssfc % " uuusfc vvvsfc"
    _sfc=_sfc+1
     num=_upr+_sfc
    _vname.num="U COMPONENT OF WIND"
    _usfc=num
    _sfc=_sfc+1
     num=_upr+_sfc
    _vname.num="V COMPONENT OF WIND"
    _vsfc=num
    addsfc=2
  else
    addsfc=0
  endif

* Get each single level variable abbreviation and build list
  i = 0
  _varsotr = ''; _otr=0; 
  while (i<_vnum) 
    dum = sublin(res,i+7)
    var=subwrd(dum,1)
    if(substr(var,4,3)="otr")
      _varsotr = _varsotr % ' ' % var
      _otr = _otr + 1
    endif
    j = i + 1 + addupr + addsfc
    if(var="slpotr"|var="prsotr")
      _vtyp.j=1
      _vgxt.j=1
    endif
    iw=4
    while (subwrd(dum,iw) !="" & substr(var,4,3)="otr")
      _vname.j = _vname.j%" "%subwrd(dum,iw)
      iw=iw+1
    endwhile
    i = i + 1
  endwhile

*  If u,v winds present, define divergence and curl variables here.
*  Create for selected dimensions in function disp().
  if(_uupr!=0&_vupr!=0)
    _varsotr=_varsotr % " divotr vorotr"
    _otr=_otr+1
     num=_upr+_sfc+_otr
    _vname.num="HORIZONTAL DIVERGENCE"
    _hd = num
    _otr=_otr+1
     num=_upr+_sfc+_otr
    _vname.num="RELATIVE VORTICITY"
    _vt = num
  endif

*  If 1000 and 500 mB levels are present, define thick here
*  Create for selected dimensions in function disp().
  if(l1=1 & l2=1)
    _varsotr=_varsotr % " thkotr"
    _otr=_otr+1
     num=_upr+_sfc+_otr
    _vname.num="1000 to 500 MB THICKNESS"
    _tk = num
  endif

* Set variable list and number
  _vars=_varsupr%_varssfc%_varsotr
  _vnum=_upr+_sfc+_otr

* Set variable contour limits, line styles and markers
  i = 0
  while (i<_vnum)
    i = i + 1
    rc=style(i)
    rc=marker(i)
    var=subwrd(_vars,i)
    rc=getemp(var,_cint.i,_cmax.i,_cmin.i)
    _cint.i=_ci
    _cmax.i=_cmx
    _cmin.i=_cmn
  endwhile

return

function butncons()
'q gxinfo'
  dum=sublin(result,2)
  _xpur=subwrd(dum,4)
  _ypur=subwrd(dum,6)
  _xpll=0.0
  _ypll=0.0

*  Size of Menu Area
  _mwide=1.33
  _mhigh=1.5

*  Height of and width of Graphic Output Boxes (inches)
  _gxbw=_mwide/1
  _gxbh=_mhigh/5

*  Width of time bar display and height of time labels (inches)
  _timbwide=0.50
  _timlhigh=0.2

*  Width of xyz bar display and height of labels (inches)
  _bwide=0.60
  _lhigh=0.2

*  Dimensions of quit, display, reset, and print boxes
  _qbw=1.22
  _qbh=0.5
  _dbw=1.33
  _dbh=0.5
  _pbw=1.22
  _pbh=0.5
  _rbw=1.22
  _rbh=0.5

*  Dimensions of plot, image, and movie buttons
  _mbw=1.22
  _mbh=0.25
  
*  Height and width of section buttons
  _sbw=1.22
  _sbh=0.4

*  Height and width of station buttons
  _stbw=0.8
  _stbh=0.3

*  Height and width of variables boxes
  _vbw=0.55
  _vbh=0.25
  _topbyll=_ypur-_vbh
  if(_ftype="Station"|_ftype="Both")
    _vbh = 0.3
    _topbyll=_ypur-_vbh-_stbh
  endif

*  Border for all buttons
  _bord=1/80

return

function miscbutn()
'set button 0 90 91 92 6'
  if (_out = 0)
    i = 99
    qbx=_qbw/2+_bord*2
    qby=_qbh/2+0.08
    'draw button 'i' 'qbx' 'qby' '_qbw' '_qbh' QUIT'
    i = 97
    pbx=_qbw/2+(_qbw-_pbw)/2+_bord*2
    pby=_qbh/2+0.1+_dbh+_bord
    'draw button 'i' 'pbx' 'pby' '_pbw' '_pbh' OUTPUT' 
  endif
  i = 98
  dbx=_xpur-_dbw/2-4*_bord
  dby=_dbh/2+0.1
  'draw button 'i' 'dbx' 'dby' '_dbw' '_dbh' DISPLAY'
  i = 96
  rbx=_rbw/2+2*_bord
  rby=_ypur-_rbh/2-2*_bord
  'draw button 'i' 'rbx' 'rby' '_rbw' '_rbh' RESET' 
return
  
function gxbutton()
  _gxtype="contour shaded vector barb stream"
  _gxtlab="contour shaded vector barbs stream"
  delx=_gxbw-_bord
  dely=_gxbh-_bord*2
  xbut=_xpur-_gxbw/2-_bord*4
  ybut=_ypur-_gxbh/2-_bord
    nd=5
    ng=1
  while ng <= nd
    str=subwrd(_gxtlab,ng)
    if(_gxtp != ng)
      'set button 0 90 91 92 6'
      'draw button 6'ng' 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 6'ng' 'xbut' 'ybut' 'delx' 'dely' 'str
    endif
    ybut=ybut-_gxbh
    ng=ng+1
  endwhile
return

function pbutton()
 if (_out = 1)
  _prt="PRINT PREVIEW SAVE AUTOMATE"  
  delx=_mbw-_bord
  dely=_mbh-_bord
  xbut=_mbw/2+_bord*3
  ybut=_ypll+3.5*_mbh+_bord+0.1
  i = 1; j = 1
  while (j = 1)
  while (i <= 4)
    str=subwrd(_prt,i)
    if (i != _mtyp)
      'set button 0 90 91 92 6'
      'draw button 'i+55' 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 'i+55' 'xbut' 'ybut' 'delx' 'dely' 'str
    endif
    ybut=ybut-_mbh-_bord
    i = i + 1
  endwhile
  j = 0
  endwhile
 endif
 _out=0
return

function qbutton()
** program waits here for next instruction **
*say 'program waits here for next instruction'
  'q pos'
  _xpos = subwrd(result,3)
  _ypos = subwrd(result,4)
  _btn = subwrd(result,7)
  _event = subwrd(result,6)
  _btnN = subwrd(result,5)
  if (_event=0) 
    _btn = -999
  endif
  n=_btn
  e=0.25
if(_display=1 & _styp=4 & _btnN="1") 
 if(_xpos<=_parxmx+e & _xpos>=_parxmn-e & _ypos<=_parymx+e & _ypos>=_parymn-1.0)
  if(_xpos<=_parxmx-e & _xpos>=_parxmn+e & _ypos<=_parymx-e & _ypos>=_parymn+e)
    rc=zoomin()
  else 
    rc=zoomout()
  endif
  _btn=98
 endif
endif
if(_xpos<=_parxmx & _xpos>=_parxmn & _ypos<=_parymx & _ypos>=_parymn & _display=1)
  if(_ftype="Station"); return; endif
  if(_surface=1)
    if(_btnN="2"); _pick=1; endif
  endif
  if(_ftype="Grid")
    if(_btnN="2"); return; endif
  endif
else
  if(_xpos<_timbxll & _xpos>_dimbxur & _surface=1 & _display=0)
    if (_btn<0 & _btnN="2"); _disurf=1; endif
  endif
* toggle variable button 
  if (n>=1 & n<=20 & _btnN!="3")
    _entr=1
    if (_vtyp.n != 1)
      _vtyp.n=1
    else
      _vtyp.n=0
    endif
  endif
* exclusively set make output button
  if (n=56); _mtyp=1; endif;
  if (n=57); _mtyp=2; endif;
  if (n=58); _mtyp=3; endif;
  if (n=59); _mtyp=4; endif;
* exclusively set graph type button
  if (n>=61 & n<=65)
    _entr=2
  endif
* set contour or fill button
  if (n=61); _gxtp=1; endif;
  if (n=62); _gxtp=2; endif;
* set vect, barb or stream button
  if (n=63); _gxtp=3; endif;
  if (n=64); _gxtp=4; endif;
  if (n=65); _gxtp=5; endif;
* toggle surface
  if (n=70) 
    if(_surface=0)
      _surface=1
    else
      _surface=0
    endif
  endif
* exclusively set station button
  if (n>=71 & n<=89)
    if(n!=_station+70)
      _station=n-70
    else 
      _station=0
    endif
  endif
* n=90 is RETURN button
* exclusively set section button
  if (n=91); _styp=1; endif;
  if (n=92); _styp=2; endif;
  if (n=93); _styp=3; endif;
* n=95 is ENTER button
  if (n=95); _entr=4; endif;
* n=96 is RESET button
* n=97 is OUTPUT button
  if (n=97); _out=1; endif; 
* n=98 is DISPLAY button
* if (_btn<0 & _btnN=3); n=98; endif
* n=99 is QUIT button
endif
return

function sbutton()
  _sec.1="Lon"
  _sec.2="Lat"
  _sec.3="Lev"
  delx=_sbw-_bord
  dely=_sbh-_bord
  xbut=_sbw/2+2*_bord
  ybut=_ypur-_rbh-_sbh/2-_bord-0.05
  i = 1
   while (i <= 3)
    str=_sec.i
    if (i != _styp)
      'set button 0 90 91 92 6'
      'draw button 9'i' 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 9'i' 'xbut' 'ybut' 'delx' 'dely' 'str
    endif
    ybut=ybut-_sbh
    i = i + 1
  endwhile
  return

function stbutton()
if(_ftype!="Grid")
  xmin=_rbw+4*_bord
  xmax=_xpur-_gxbw-4*_bord
  if(_ftype="Station")
    if (_stbw*_stnnum>(xmax-xmin))
      stbw=(xmax-xmin)/_stnnum
    else
      stbw=_stbw
    endif   
    delx=stbw-_bord
    dely=_stbh-_bord
    xbut=(xmax+xmin)/2-stbw*_stnnum/2+stbw/2
    ybut=_ypur-_vbh-_stbh/2-_bord
    i = 1
    while (i<=_stnnum)
      str=_stid.i
      if (i!=_station)
        'set button 0 90 91 92 6'
        'draw button '70+i' 'xbut' 'ybut' 'delx' 'dely' 'str
      else
        'set button 1 90 92 91 6'
        'draw button '70+i' 'xbut' 'ybut' 'delx' 'dely' 'str 
      endif
      xbut=xbut+stbw
      i = i + 1
    endwhile
  endif
  if(_ftype="Surface")
    delx=2*_stbw-_bord
    dely=_stbh-_bord
    xbut=(xmax+xmin)/2
    ybut=_ypur-_vbh-_stbh/2-_bord
    str="SURFACE"
    if (_surface=0)
      'set button 0 90 91 92 6'
      'draw button 70 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 70 'xbut' 'ybut' 'delx' 'dely' 'str 
    endif
  endif
  if(_ftype="Both")
    if (_stbw*(_stnnum+2)>(xmax-xmin))
      stbw=(xmax-xmin)/(_stnnum+2)
    else
      stbw=_stbw
    endif   
    delx=stbw-_bord
    dely=_stbh-_bord
    xbut=(xmax+xmin)/2-stbw*_stnnum/2-_bord
    ybut=_ypur-_vbh-_stbh/2-_bord
    str="SURFACE"
    if (_surface=0)
      'set button 0 90 91 92 6'
      'draw button 70 'xbut' 'ybut' '2*delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 70 'xbut' 'ybut' '2*delx' 'dely' 'str 
    endif
    xbut=xbut+stbw*3/2
    i = 1
    while (i<=_stnnum)
      str=_stid.i
      if (i!=_station)
        'set button 0 90 91 92 6'
        'draw button '70+i' 'xbut' 'ybut' 'delx' 'dely' 'str
      else
        'set button 1 90 92 91 6'
        'draw button '70+i' 'xbut' 'ybut' 'delx' 'dely' 'str 
      endif
      xbut=xbut+stbw
      i = i + 1
    endwhile
  endif
endif
return
  
function vbutton()
  xmin=_rbw+5*_bord
  xmax=_xpur-_gxbw-3*_bord
  xlab=xmin+0.5
  if (_vbw*_vnum>(xmax-xmin))
    vbw=(xmax-xmin)/(_vnum)
  else
    vbw=_vbw
  endif   
  delx=vbw-_bord
  dely=_vbh-_bord
  e=_bord*2
  xbut=(xmax+xmin)/2 -vbw*_vnum/2 +vbw/2-_bord
  ybut=_ypur-_vbh/2-_bord*2
  i = 1
  while (i<=_vnum)
    str=subwrd(_vars,i)
    if(_btn=i & _btnN="3")
      rc=vmenu(i,_xpur/2,ybut,delx+0.3,dely,str)
    endif
    xbut=xbut+vbw
    i = i + 1
  endwhile
  'set line 90'
  'set string 0 l 6'
  'set strsiz 0.15'
  xbut=(xmax+xmin)/2-vbw*_upr/2+vbw/2-_bord
  'draw recf 'xmin+_bord' 'ybut-_vbh*5/2-e' 'xmax-_bord' 'ybut+_vbh/2-e
*  'draw recf 'xmin+_bord' 'ybut-_vbh/2-e' 'xmax-_bord' 'ybut+_vbh/2-e
  'draw string 'xlab' 'ybut' UPPER'
  i = 1
  while (i<=_upr)
    name=subwrd(_vars,i)
    str=substr(name,1,3)
    if (_vtyp.i != 1)
      'set button 0 90 91 92 6'
      'draw button 'i' 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 'i' 'xbut' 'ybut' 'delx' 'dely' 'str 
    endif
    xbut=xbut+vbw
    i = i + 1
  endwhile
  xbut=(xmax+xmin)/2 -vbw*_sfc/2 +vbw/2-_bord
  ybut=ybut -_vbh
*  'draw recf 'xmin+_bord' 'ybut-_vbh/2-e' 'xmax-_bord' 'ybut+_vbh/2-e
  'draw string 'xlab' 'ybut' SURFACE'
  while (i<=_upr+_sfc)
    name=subwrd(_vars,i)
    str=substr(name,1,3)
    if (_vtyp.i != 1)
      'set button 0 90 91 92 6'
      'draw button 'i' 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 'i' 'xbut' 'ybut' 'delx' 'dely' 'str 
    endif
    xbut=xbut+vbw
    i = i + 1
  endwhile
  xbut=(xmax+xmin)/2 -vbw*_otr/2 +vbw/2-_bord
  ybut=ybut -_vbh
*  'draw recf 'xmin+_bord' 'ybut-_vbh/2-e' 'xmax-_bord' 'ybut+_vbh/2-e
  'draw string 'xlab' 'ybut' OTHER'
  while (i<=_vnum)
    name=subwrd(_vars,i)
    str=substr(name,1,3)
    if (_vtyp.i != 1)
      'set button 0 90 91 92 6'
      'draw button 'i' 'xbut' 'ybut' 'delx' 'dely' 'str
    else
      'set button 1 90 92 91 6'
      'draw button 'i' 'xbut' 'ybut' 'delx' 'dely' 'str 
    endif
    xbut=xbut+vbw
    i = i + 1
  endwhile
  return

function tmenu()
  rc= clear()
  y = 0.5*(_timbyll+_timbyur)
  x = 0.5*(_timbxll+_timbxur)-1.5
  c = 0.35
  'set strsiz 0.2'
  'set string 1 r 8'
  'draw string 'x' 'y+2.0*c' Time clock'
  'draw string 'x' 'y' Time interval'
  tinc=_tdel % ' ' % _iunit
  'draw string 'x' 'y-c' is 'tinc
  'set button 0 90 91 92 6'
* Get new time interval
  j=1
  while (j=1)
    'draw button 91 'x+0.5' 'y' 'c' 'c' >'
    'draw button 92 'x+0.5' 'y-c' 'c' 'c' <'
    if(_clk!=1)
      'draw button 93 'x+0.5' 'y+2.0*c' 'c' 'c' Off'
    endif
    if(_clk!=0)
      'set button 1 90 92 91 6'
      'draw button 93 'x+0.5' 'y+2.0*c' 'c' 'c' On'
      'set button 0 90 91 92 6'
    endif
    'set string 95 r 8'
    'q pos'
    btn = subwrd(result,7)
    btnN = subwrd(result,5)
   if(btnN="3")
    if(btn=91)
      'draw string 'x' 'y-c'  is '_tdel % ' ' % _iunit
      rc = timinc(1)
      if(_tinc<_dtime.1); clr=7; else; clr=1; endif
      'set string 'clr' r 8'
      'draw string 'x' 'y-c'  is '_tdel % ' ' % _iunit
    endif
    if(btn=92)
      'draw string 'x' 'y-c'  is '_tdel % ' ' % _iunit
      rc = timinc(-1)
      if(_tinc<_dtime.1); clr=7; else; clr=1; endif
      'set string 'clr' r 8'
      'draw string 'x' 'y-c'  is '_tdel % ' ' % _iunit
    endif
    if(btn=93)
      if(_clk!=0); _clk=0; else; _clk=1; endif
    endif
   else
    j=0
    rc = clear()
   endif
    if(_tinc<_dtime.1)
      'set string 7 r 8'
      'draw string 'x' 'y+c' Interpolated '
    else
      'set string 95 r 8'
      'draw string 'x' 'y+c' Interpolated '
    endif
  endwhile
* Define new _t1 and _t2
  nint=_dtime.1/_tinc
    _t1 = (_t1-1)/_nint+1
    _t2 = (_t2-1)/_nint+1
    _t1 = int((_t1-1)*nint+1)
    _t2 = int((_t2-1)*nint+1)
  _nint=nint
  _tnums=(_tnum-1)*_nint+1
* Create tick mark vector
  i = 1
  _tmark=""
  while (i<=(_tnum-1)*_nint+1) 
    rc=mod(i-1,_nint)
    if (rc=0)
      _tmark=_tmark" "1
    else
      if (_tdel<10&_iunit="MN")
        rc=mod(i-1,10)
        if (rc=0)
          _tmark=_tmark" "0
        else
          _tmark=_tmark" "s
        endif
      else
        _tmark=_tmark" "0  
      endif
    endif
    i = i + 1
  endwhile
return
 
function vmenu(i,xbut,ybut,delx,dely,name)
  _supp=1
  a=0.5; b=0.3; c=0.3; d=0.75
  x=xbut
  y=ybut-0.5
  str=substr(name,1,3)
  'draw button 'i' 'x' 'y+0.5' 'delx' 'dely' 'str
  'set button 0 90 91 92 6'
  'set strsiz 0.2'
  'set string 1 c 8'
  'draw string 'x' 'y-c' CONTOUR'
  'draw string 'x' 'y-5*d-c' LINE'
  if((substr(str,1,1)="u"|substr(str,1,1)="v")&str!="vort")
    'draw string 'x' 'y-7*d-c' VECTOR'
  endif
  rc=style()
  rc=marker()
  rc=getemp(str,_cint.i,_cmax.i,_cmin.i)
  'set strsiz 0.15'
  'set string 1 r 6'
  'draw string 'x+a' 'y-1*d-c' Labels'
  'draw string 'x+a' 'y-2*d' 'str' interval'
  'draw string 'x+b' 'y-2*d-c'  is '_ci
  'draw string 'x+a' 'y-3*d' 'str' maximum'
  'draw string 'x+b' 'y-3*d-c'  is '_cmx
  'draw string 'x+a' 'y-4*d' 'str' minimum'
  'draw string 'x+b' 'y-4*d-c'  is '_cmn
  'draw string 'x+a' 'y-6*d' Style '_sty.i
  'draw string 'x+a' 'y-6*d-c' Marker '_mkr.i
  if((substr(str,1,1)="u"|substr(str,1,1)="v")&str!="vort")
    'draw string 'x+a' 'y-8*d' 'str' grid skip'
    'draw string 'x+b' 'y-8*d-c'  is '_skip-1
    'draw string 'x+a' 'y-9*d' 'str' streamline'
    'draw string 'x+a' 'y-9*d-c' density is '_dens
  endif
  j=1
  while (j=1)
    if(_lbl.i!=1)
      'draw button 80 'x+1.0' 'y-1*d-c' 'c' 'c' Off'
    endif
    if(_lbl.i!=0)
      'set button 1 90 92 91 6'
      'draw button 80 'x+1.0' 'y-1*d-c' 'c' 'c' On'
      'set button 0 90 91 92 6'
    endif
    'draw button 81 'x+1.0' 'y-2*d' 'c' 'c' >'
    'draw button 82 'x+1.0' 'y-2*d-c' 'c' 'c' <'
    'draw button 83 'x+1.0' 'y-3*d' 'c' 'c' >'
    'draw button 84 'x+1.0' 'y-3*d-c' 'c' 'c' <'
    'draw button 85 'x+1.0' 'y-4*d' 'c' 'c' >'
    'draw button 86 'x+1.0' 'y-4*d-c' 'c' 'c' <'
    'draw button 87 'x+1.0' 'y-6*d' 'c' 'c' ?'
    'draw button 88 'x+1.0' 'y-6*d-c' 'c' 'c' ?'
    if((substr(str,1,1)="u"|substr(str,1,1)="v")&str!="vort")
      'draw button 89 'x+1.0' 'y-8*d' 'c' 'c' >'
      'draw button 90 'x+1.0' 'y-8*d-c' 'c' 'c' <'
      'draw button 91 'x+1.0' 'y-9*d' 'c' 'c' >'
      'draw button 92 'x+1.0' 'y-9*d-c' 'c' 'c' <'
    endif
    'set string 95 r 6'
    'q pos'
    btn = subwrd(result,7)
    btnN = subwrd(result,5)
   if(btnN="3")
    if(btn=80)
      if(_lbl.i!=0); _lbl.i=0; else; _lbl.i=1; endif      
    endif
    if(btn=81)
      'draw string 'x+b' 'y-2*d-c'  is '_cint.i
      _cint.i=_cint.i+_cinc
      if(_cint.i>_cmax.i-_cmin.i); _cint.i=_cmax.i-_cmin.i; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-2*d-c'  is '_cint.i
    endif
    if(btn=82)
      'draw string 'x+b' 'y-2*d-c'  is '_cint.i
      _cint.i=_cint.i-_cinc
      if(_cint.i<=0); _cint.i=_cinc; endif
      if((_cmax.i-_cmin.i)/_cint.i>99); _cint.i=_cint.i+_cinc; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-2*d-c'  is '_cint.i
    endif
    if(btn=83)
      'draw string 'x+b' 'y-3*d-c'  is '_cmax.i
      _cmax.i=_cmax.i+5*_cinc
      if((_cmax.i-_cmin.i)/_cint.i>99); _cmax.i=_cmax.i-5*_cinc; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-3*d-c'  is '_cmax.i
    endif
    if(btn=84)
      'draw string 'x+b' 'y-3*d-c'  is '_cmax.i
      _cmax.i=_cmax.i-5*_cinc
      if(_cmax.i<=_cmin.i); _cmax.i=_cmin.i+5*_cinc; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-3*d-c'  is '_cmax.i
    endif
    if(btn=85)
      'draw string 'x+b' 'y-4*d-c'  is '_cmin.i
      _cmin.i=_cmin.i+5*_cinc
      if(_cmax.i<=_cmin.i); _cmin.i=_cmax.i-5*_cinc; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-4*d-c'  is '_cmin.i
    endif
    if(btn=86)
      'draw string 'x+b' 'y-4*d-c'  is '_cmin.i
      _cmin.i=_cmin.i-5*_cinc
      if((_cmax.i-_cmin.i)/_cint.i>99); _cmin.i=_cmin.i+5*_cinc; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-4*d-c'  is '_cmin.i
    endif
    if(btn=87)
      'draw string 'x+a' 'y-6*d' Style '_sty.i
      _styl.i=_styl.i+1
      if(_styl.i=5); _styl.i=1; endif
      rc=style(i)
      'set string 7 r 6'
      'draw string 'x+a' 'y-6*d' Style '_sty.i
    endif
    if(btn=88)
      'draw string 'x+a' 'y-6*d-c' Marker '_mkr.i
      _mrkr.i=_mrkr.i+1
      if(_mrkr.i=6); _mrkr.i=0; endif
      rc=marker(i)
      'set string 7 r 6'
      'draw string 'x+a' 'y-6*d-c' Marker '_mkr.i
    endif
    if(btn=89)
      'draw string 'x+b' 'y-8*d-c'  is '_skip-1
      _skip=_skip+1
      'set string 7 r 6'
      'draw string 'x+b' 'y-8*d-c'  is '_skip-1
    endif
    if(btn=90)
      'draw string 'x+b' 'y-8*d-c'  is '_skip-1
      _skip=_skip-1
      if(_skip<=1); _skip=1; endif
      'set string 7 r 6'
      'draw string 'x+b' 'y-8*d-c'  is '_skip-1
    endif
    if(btn=91)
      'draw string 'x+a' 'y-9*d-c' density is '_dens
      _dens=_dens+1
      if(_dens>=10); _dens=10; endif
      'set string 7 r 6'
      'draw string 'x+a' 'y-9*d-c' density is '_dens
    endif
    if(btn=92)
      'draw string 'x+a' 'y-9*d-c' density is '_dens
      _dens=_dens-1
      if(_dens<=1); _dens=1; endif
      'set string 7 r 6'
      'draw string 'x+a' 'y-9*d-c' density is '_dens
    endif
    if(i=_usfc)
      _cint._vsfc=_cint._usfc
      _cmax._vsfc=_cmax._usfc
      _cmin._vsfc=_cmin._usfc
    endif
    if(i=_vsfc)
      _cint._usfc=_cint._vsfc
      _cmax._usfc=_cmax._vsfc
      _cmin._usfc=_cmin._vsfc
    endif
    if(i=_uupr)
      _cint._vupr=_cint._uupr
      _cmax._vupr=_cmax._uupr
      _cmin._vupr=_cmin._uupr
    endif
    if(i=_vupr)
      _cint._uupr=_cint._vupr
      _cmax._uupr=_cmax._vupr
      _cmin._uupr=_cmin._vupr
    endif
   else
    j=0
    rc= clear()
   endif
  endwhile
  if(_cmax._uupr<_cint._uupr)
    cmax=_cint._uupr
  else
    cmax=_cmax._uupr 
  endif
  if(_cmax._usfc<_cint._usfc)
    cmax=_cint._usfc
  else
    cmax=_cmax._usfc 
  endif
return

function setparea()
  bordlft=0.8
  bordbtm=1.5
  bordrit=0.5
  bordtop=0.2
  if(_plottyp=0)
    bordlft=2.0
    bordbtm=1.2
    bordrit=2.0
    bordtop=0.5
  endif
  if(_plottyp=2)
    bordlft=1.0
    bordbtm=1.2
    bordrit=0.75
    bordtop=0.5
  endif
  if(_plottyp=1|_plottyp=3)
    bordlft=2.0
    bordbtm=1.2
    bordrit=0.5
    bordtop=0.5
  endif
  if(_plottyp=4|_plottyp=5)
    bordlft=1.2
    bordbtm=1.5
    bordrit=0.5
    bordtop=0.5
  endif
  if(_plottyp=6)
    bordlft=2.0
    bordbtm=1.5
    bordrit=0.5
    bordtop=0.5
  endif 
  if(_station!=0)
    bordlft=1.2
    bordbtm=1.0
    bordrit=0.6
    bordtop=0.5
  endif

 _parxmx=_timbxll-bordrit
 _parymx=_topbyll-bordtop-_vbh*3
 _parxmn=_dimbxur+bordlft
 _parymn=_xpll+bordbtm

'set parea '_parxmn' '_parxmx' '_parymn' '_parymx
'set line 0'
'draw recf '_parxmn' '_parymn' '_parxmx' '_parymx

return

function bar(x, y, dx, dy, n, p1, p2, ticks)
  dx2=dx/2
  dx6=dx/6
  dx12=dx/12 
  yd = dy/(n-1)
  ylo = y-dy/2
  yhi = y+dy/2
  'set line 0 1 4'
  'draw line 'x' 'ylo' 'x' 'yhi
  i = 1
  while (i<=n)
    y = ylo + (i-1)*yd
    tk = subwrd(ticks,i)
    if (i>=p1 & i<=p2) 
      'set line 92 1 5.5'
    else
      'set line 0 1 4'
    endif
    if (tk="1")
      'draw line '%(x-dx6)%' 'y' '%(x+dx6)%' 'y
    else
      if (_tinc!=_dtime.1&x>_timbxll)
        'set line 41 1 4'
      endif        
      if (tk="0"); 'draw line '%(x-dx12)%' 'y' '%(x+dx12)%' 'y; endif
    endif 
    i = i + 1
  endwhile
  y1=ylo+(p1-1)*yd
  y2=ylo+(p2-1)*yd   
  'set line 92 1 12'
  'draw line 'x' 'y1' 'x' 'y2
return

function dbar()
  if (_styp=1)
    _nam=_lons
    num=_xnum
    lab1 = "Lon"
    mark=_xmark
    p1=_x1-_x0+1
    p2=_x2-_x0+1
  endif
  if (_styp=2)
    _nam=_lats
    num=_ynum
    lab1 = "Lat"
    mark=_ymark
    p1=_y1-_y0+1
    p2=_y2-_y0+1
  endif
  if (_styp=3)
    _nam=_levs
    num=_znum
    lab1 = "Lev"
    mark=_zmark
    p1=_z1
    p2=_z2
  endif
  _dlev = p1
  nrow=2
  nchr=3
  lh2=0.5*_lhigh
  xhi=_xpll+_bwide
  xlo=_xpll
  ylo = _qbh+_pbh+0.3+nrow*_lhigh
  yhi = _ypur-_rbh-_sbh*3-0.25-nrow*_lhigh
  
  delx=0.35
  dely=0.01
  _dimbxll=xlo+delx
  _dimbxur=xhi+delx
  _dimbyll=ylo-dely
  _dimbyur=yhi-dely
  if(num = 1); return; endif;
  
  x = 0.5*(xhi+xlo)+delx
  dx = _bwide 
  y = 0.5*(ylo+yhi)
  dy = yhi-ylo

  xll=_dimbxll-0.3
  yll=_dimbyll-0.55
  xur=_dimbxur+0.3
  yur=_dimbyur+0.55
  'set line 90'
  'draw recf 'xll' 'yll' 'xur' 'yur
  'set line 92 1 6'
  'draw line 'xll' 'yll' 'xll' 'yur
  'draw line 'xll' 'yur' 'xur' 'yur
  'set line 91 1 6'
  'draw line 'xll' 'yll' 'xur' 'yll
  'draw line 'xur' 'yll' 'xur' 'yur
  rc = bar(x, y, dx, dy, num, p1, p2, mark)

* Label dimension bar
  str=lh2
  if(nchr*str > dx)
    str=dx/nchr
  endif
  'set string 1 c 8'
  'set strsiz 'str
  'draw string 'x' '%(ylo-2.0*_lhigh+lh2)%' 'lab1
  'draw string 'x' '%(yhi+2.0*_lhigh-lh2)%' 'lab1

* Label selected dimension values
  str=0.8*str
  yd = dy/(num-1)
  i = 1
  while (i<=num)
    'set strsiz 'str
    ylab = ylo + (i-1)*yd
    lab2 = subwrd(_nam,i)
    ilab2 = lab2
    mkit = subwrd(mark,i)
    if(mkit="1")
      ilab2=int(lab2)
      'set string 1 l 3'
      xlab = x+dx/4
      'draw string 'xlab' 'ylab' 'ilab2
    endif
    if(i=p1|i=p2)
      if(lab2-int(lab2)!=0); ilab2=int(lab2*100)/100; endif
      'set string 1 r 3'
      xlab = x-dx/4
      'draw string 'xlab' 'ylab' 'ilab2
    endif

* Display current settings
    if(i=_styp)
      'set string 7 l 6'
    else
      'set string 15 l 6'
    endif

   if(_xpur<_ypur)
     'set strsiz 0.12'
     xx=_xpur-7.0
     yy=_ypur-6.0
   else
     'set strsiz 0.15'
     xx=_xpur-9.0
     yy=_ypur-4.5
   endif
   if(_supp!=1)
    if(i=1)
      'draw string 'xx' 'yy+2.0' Lon = 'subwrd(_lons,_x1-_x0+1)
      if(_x1!=_x2)
      'draw string 'xx+0.5' 'yy+1.6' to 'subwrd(_lons,_x2-_x0+1)
      endif
    endif
    if(i=2)
      'draw string 'xx' 'yy' Lat = 'subwrd(_lats,_y1-_y0+1)
      if(_y1!=_y2)
      'draw string 'xx+0.5' 'yy-0.4' to 'subwrd(_lats,_y2-_y0+1)
      endif
    endif
    if(i=3)
      'draw string 'xx' 'yy-2.0' Lev = 'subwrd(_levs,_z1)
      if(_z1!=_z2) 
      'draw string 'xx+0.5' 'yy-2.4' to 'subwrd(_levs,_z2)
      endif
    endif
   endif
   i = i + 1
  endwhile
 return

function qbar()
  bord = 0.1
*  "dimension bar has been chosen"
  if (_xpos<=_dimbxur & _ypos>=_dimbyll-bord & _ypos<=_dimbyur+bord)
* Identify selected dimension
  if (_styp=1)
    num=_xnum
    p1=_x1-_x0+1
    p2=_x2-_x0+1
  endif
  if (_styp=2)
    num=_ynum
    p1=_y1-_y0+1
    p2=_y2-_y0+1
  endif
  if (_styp=3)
    num=_znum
    p1=_z1
    p2=_z2
  endif
  if (num<2); return; endif

*   Get selected dimension index
    td = (_dimbyur-_dimbyll)/(num-1)
    dim = (_ypos-_dimbyll)/td
    dim = int(dim+1.5)
    if (dim<1); dim = 1; endif;
    if (dim>num); dim = num; endif;

*   Set selected dimension
    if (_dclick=1 & _btnN="2") 
      _dclick = 2
      if (p1<dim) 
        p2 = dim
      else
        p1 = dim
      endif
    else
      _dclick = 1
      p1 = dim
      p2 = dim
    endif
    if (_styp=1)
      _x1=p1+_x0-1
      _x2=p2+_x0-1
    endif
    if (_styp=2)
      _y1=p1+_y0-1
      _y2=p2+_y0-1
    endif
    if (_styp=3)
      _z1=p1
      _z2=p2
    endif
  endif

* "time bar has been chosen"
  if (_xpos>=_timbxll & _ypos>=_timbyll-bord & _ypos<=_timbyur+bord)

*   Get tmenu to modify _tinc and _nint
    y = 0.5*(_timbyll+_timbyur)
    x = 0.5*(_timbxll+_timbxur)
    x = x -1.5*_timbwide/8-_timlhigh/4
    if (x>=_xpos-0.1&x<=_xpos+0.3&y>=_ypos-0.5&y<=_ypos+0.5&_btnN="3")
      rc=tmenu()
      rc=tdeflbl(0)
      _tflag = 1
    else

*   Get selected times 
    _tnums=(_tnum-1)*_nint+1
    if (_tnums<2); return; endif
    td = (_timbyur-_timbyll)/(_tnums-1)
    tim = (_ypos-_timbyll)/td
    tim = int(tim+1.5)
    if (tim<1); tim = 1; endif;
    if (tim>_tnums); tim = _tnums; endif;
*   Set _t1 and _t2
    if (_tclick=1 & _btnN="2") 
      _tclick = 2
      if (_t1<tim) 
        _t2 = tim
      else
        _t1 = tim
      endif
    else
      _tclick = 1
      _t1 = tim
      _t2 = tim
    endif
    endif
  endif

 return

function tbar()
* Define tbar  
  nrowtim=3
  nchtim=8
  timlh2=0.5*_timlhigh
  xhi=_xpur
  xlo=_xpur-_timbwide
  ylo = _dbh+0.2+nrowtim*_timlhigh
  yhi = _ypur-_mhigh-0.2-nrowtim*_timlhigh

  delx=0.45
  dely=0.05
  _timbxll=xlo-delx
  _timbxur=xhi-delx
  _timbyll=ylo+dely
  _timbyur=yhi+dely
  if(_tnum = 1); return; endif;
  
  x = 0.5*(xhi+xlo)-delx
  dx = _timbwide 
  y = 0.5*(ylo+yhi)
  dy = yhi-ylo

  xll=_timbxll-0.4
  yll=_timbyll-0.7
  xur=_timbxur+0.4
  yur=_timbyur+0.65
  'set line 90'
  'draw recf 'xll' 'yll' 'xur' 'yur
  'set line 92 1 6'
  'draw line 'xll' 'yll' 'xll' 'yur
  'draw line 'xll' 'yur' 'xur' 'yur
  'set line 91 1 6'
  'draw line 'xll' 'yll' 'xur' 'yll
  'draw line 'xur' 'yll' 'xur' 'yur
  rc = bar(x, y, dx, dy, _tnums, _t1, _t2, _tmark)

* Label first and last times
  timstr=timlh2
  if(nchtim*timstr > 2*dx)
    timstr=2*dx/nchtim
  endif
  'set string 1 c 8'
  'set strsiz 'timstr
  p1 = subwrd(_tc1,1)
  p2 = subwrd(_tc1,2) % ' ' % subwrd(_tc1,3)
  p3 = subwrd(_tc1,4)
  'draw string 'x' '%(ylo-_timlhigh+timlh2)%' 'p1
  'draw string 'x' '%(ylo-2.0*_timlhigh+timlh2)%' 'p2
  'draw string 'x' '%(ylo-3.0*_timlhigh+timlh2)%' 'p3
  p4 = subwrd(_tc2,1)
  p5 = subwrd(_tc2,2) % ' ' % subwrd(_tc2,3)
  p6 = subwrd(_tc2,4)
  'draw string 'x' '%(yhi+_timlhigh-timlh2)%' 'p4
  'draw string 'x' '%(yhi+2.0*_timlhigh-timlh2)%' 'p5
  'draw string 'x' '%(yhi+3.0*_timlhigh-timlh2)%' 'p6
  
* Label selected times
  yd = dy/(_tnums-1)
  i = 1
  'set strsiz 'timstr*0.8
  while (i<=_tnums) 
    if(i=_t1|i=_t2)
      rc=int((i-1)/_nint+1.0)
      'set t 'rc
      tc = mydate()
      p1 = tlabel(i)
      p2 = subwrd(tc,2) % ' ' % subwrd(tc,3)
      ylab = ylo + (i-1)*yd
      xlab=x-dx/3
      'set string 1 r 3'
      'draw string 'xlab' 'ylab' 'p1
      xlab=x+dx/3
      'set string 1 l 3'
      'draw string 'xlab' 'ylab' 'p2
      if(i=_t1); t1=p1' 'p2; endif
      if(i=_t2); t2=p1' 'p2; endif
    endif
    i = i + 1
  endwhile

* Display current settings
   if(i=_styp)
     'set string 7 l 6'
   else
     'set string 15 l 6'
   endif
   if(_xpur<_ypur)
     'set strsiz 0.12'
     xx=_xpur-4.0
     yy=_ypur-6.0
   else
     'set strsiz 0.15'
     xx=_xpur-5.0
     yy=_ypur-4.5
   endif
   if(_supp!=1)
     'draw string 'xx' 'yy' Time = 't1
     if(_t1!=_t2)
     'draw string 'xx+0.5' 'yy-0.4' to 't2
     endif
   endif

*  Add tdef label
   if (_tinc=_dtime.1)
     rc=tdeflbl(1)
   else
     rc=tdeflbl(7)
   endif
 
return

function tdeflbl(clr)
*  Temporary fix for displaying time interval (needs an upgrade)
  y = 0.5*(_timbyll+_timbyur)
  x = 0.5*(_timbxll+_timbxur)
  x = x -1.5*_timbwide/8-_timlhigh/4
  'set strsiz 0.12'
  'set string 'clr' c 3 270'
  tinc=_tdel % ' ' % _iunit
  if(_tinc<_dtime.1); tinc='Interpolated '%tinc; endif
  'draw string 'x' 'y' 'tinc
  'set string 'clr' c 3 0'
  return

function tlabel(val)
  ht = getime(val)
  hr = int(ht)
  hf = ht - hr
  mn = int(60*hf+0.05)
  mf = 60*hf - mn
  sc = int(60*mf+0.45)
  if (hr<10); hr="0"%hr; endif          
  if (mn<10); mn="0"%mn; endif          
  if (sc<10); sc="0"%sc; endif          
  if(_tunit="MN"|_tunit="mn")
    p = hr%':'%mn%':'%sc%'Z'
  endif
  if(_tunit="HR"|_tunit="hr")
    p = hr%':'%mn%'Z'
  endif
  if(_tunit="DY"|_tunit="dy")
    hr = int(24*ht+0.05)
    if (hr<10); hr="0"%hr; endif          
    p = hr%'Z'
  endif 
return p

function fnddt(fname)
while (1)
  res=read(fname)
  dum=sublin(res,2)
  if(subwrd(dum,1)="tdef"|subwrd(dum,1)="TDEF"); break; endif
endwhile
rc=close (fname)
dt=subwrd(dum,5)
i=1
while(substr(dt,i,1)>='0' & substr(dt,i,1)<='9')
  i=i+1
endwhile
num=substr(dt,1,i-1)
_tunit=substr(dt,i,99)
_iunit=_tunit
str=num%" "_tunit
return str

*  Function to reformat the GrADS date/time into something
*  more readable 
function mydate ()
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
return (hour' 'day' 'month' 'year)

function getime(val)
  'query time'
  dtg=subwrd(result,3)
  if(substr(dtg,3,1)=":"); min=substr(dtg,4,2); endif
  if(substr(dtg,3,1)="Z"); min=0; endif
  if(_tunit="DY"|_tunit="dy")
    tp1=substr(dtg,1,2)
    tp2=tp1+_dtime.1
  endif 
  if(_tunit="HR"|_tunit="hr")
    tp1=substr(dtg,1,2)
    tp2=tp1+_dtime.1
  endif 
  if(_tunit="MN"|_tunit="mn")
    tp1=substr(dtg,1,2)+min/60
    tp2=tp1+_dtime.1/60
  endif         
  if (tp2=0); tp2=24; endif 
  b=mod((val-1),_nint)/_nint
  a=1.0-b
  p=a*tp1+b*tp2
return p

function ckinc(val,n)
*---------------
* this is a cluge to handle irregular grid data
  dlon=(_lnhi-_lnlo)/(_xnum-1)
  dlat=(_lthi-_ltlo)/(_ynum-1)
  if (dlon>dlat)
    e = dlat
  else
    e = dlon
  endif
  if (val<0); val=-val; endif
  val = int(val*10+0.5)/10
  ival = int(val)
  if (val-ival>e|ival-val>e); ival=val; endif;
*---------------
  if (n<=10); return(0); endif;
  if (n>10 & n<=20)
    rc=mod(ival,2)
    return(rc)
  endif
  if (n>20 & n<=50)
    rc=mod(ival,5)
    return(rc)
  endif
  if (n>50 & n<=120)
    rc=mod(ival,10)
    return(rc)
  endif
  if (n>120 & n<=360)
    rc=mod(ival,30)
    return(rc)
  endif
  if (n>360)
    rc=mod(ival,50)
    return(rc)
  endif

function mod(i0,inc)
 if(inc!=0)
  imod=int(i0/inc)
 else
  imod=int(i0/1)
 endif
 imod=i0-imod*inc
return(imod)

function int(i0)
 i=0
 while(i<12)
  i=i+1
  if(substr(i0,i,1)='.')
   i0=substr(i0,1,i-1)
   break
  endif
 endwhile
return(i0)

function timinc(val)
 denom=int(1/_tinc+0.5)
 tinc=_tinc
 if(_tunit="MN"|_tunit="mn"); mod=60; endif
 if(_tunit="HR"|_tunit="hr"); mod=60; endif
 if(_tunit="DY"|_tunit="dy"); mod=24; endif
 if(_tunit="MO"|_tunit="mo"); mod=30; endif
 if(_tunit="YR"|_tunit="yr"); mod=12; endif
 i=1
 while (i=1)
   if (val>0) 
     if (tinc<1)
       denom=denom-1
       if(denom<1); denom=1; endif
       if(mod(mod,denom)=0); _tinc=1/denom; break; endif
     else
       tinc = tinc +1
       if (tinc>=_dtime.1); _tinc=_dtime.1; break; endif
       if (mod(_dtime.1,tinc)=0); _tinc=tinc; break; endif
     endif
   endif
   if (val<0) 
     if (tinc<=1)
       denom=denom+1
       if(denom>mod); denom=mod; endif
       if(mod(mod,denom)=0); _tinc=1/denom; break; endif
     else
       tinc = tinc -1
       if(mod(_dtime.1,tinc)=0); _tinc=tinc; break; endif
     endif
   endif
 endwhile
 if(_tinc<1&_tunit="MN"); _tdel=int(_tinc*60+0.5); _iunit="SC"; endif
 if(_tinc>=1&_tunit="MN"); _tdel=_tinc; _iunit="MN"; endif
 if(_tinc<1&_tunit="HR"); _tdel=int(_tinc*60+0.5); _iunit="MN"; endif
 if(_tinc>=1&_tunit="HR"); _tdel=_tinc; _iunit="HR"; endif
 if(_tinc<1&_tunit="DY"); _tdel=int(_tinc*24+0.5); _iunit="HR"; endif
 if(_tinc>=1&_tunit="DY"); _tdel=_tinc; _iunit="DY"; endif
 if(_tinc<1&_tunit="MO"); _tdel=int(_tinc*30+0.5); _iunit="DY"; endif
 if(_tinc>=1&_tunit="MO"); _tdel=_tinc; _iunit="MO"; endif
 if(_tinc<1&_tunit="YR"); _tdel=int(_tinc*12+0.5); _iunit="MO"; endif
 if(_tinc>=1&_tunit="YR"); _tdel=_tinc; _iunit="YR"; endif
 if(_tinc<1&_tunit="mn"); _tdel=int(_tinc*60+0.5); _iunit="sc"; endif
 if(_tinc>=1&_tunit="mn"); _tdel=_tinc; _iunit="mn"; endif
 if(_tinc<1&_tunit="hr"); _tdel=int(_tinc*60+0.5); _iunit="mn"; endif
 if(_tinc>=1&_tunit="hr"); _tdel=_tinc; _iunit="hr"; endif
 if(_tinc<1&_tunit="dy"); _tdel=int(_tinc*24+0.5); _iunit="hr"; endif
 if(_tinc>=1&_tunit="dy"); _tdel=_tinc; _iunit="dy"; endif
 if(_tinc<1&_tunit="mo"); _tdel=int(_tinc*30+0.5); _iunit="dy"; endif
 if(_tinc>=1&_tunit="mo"); _tdel=_tinc; _iunit="mo"; endif
 if(_tinc<1&_tunit="yr"); _tdel=int(_tinc*12+0.5); _iunit="mo"; endif
 if(_tinc>=1&_tunit="yr"); _tdel=_tinc; _iunit="yr"; endif
return

function monitor()
   if(_entr=1 & _vtyp._btn=1)
     if(_gxuse._gxtp=0 | _gxtp=1 | _btn=_uupr | _btn=_vupr | _btn=_usfc | _btn=_vsfc)
       _vgxt._btn=_gxtp
       _gxuse._gxtp=_btn
       if(_gxtp=2); _shad=_btn; endif
     else
       _vtyp._btn=0
       'set string 1 c 6'
       'set strsiz 0.2'
       str1="'"%subwrd(_gxtlab,_gxtp)"'"
       str2=subwrd(_vars,_gxuse._gxtp)
       str=str1%" has been used for "%str2
       'draw string '_xpur/2' '_ypur-2*(_vbh+_stbh)' 'str
       str="SELECT A NEW GRAPH TYPE"
       'draw string '_xpur/2' '_ypur-4*(_vbh+_stbh)' 'str
       _supp=1
     endif
   endif
   if(_entr=1 & _vtyp._btn=0)
     if(_vgxt._btn=2)
        _shad=0
        _gxuse.2=0
      endif
     _vgxt._btn=0 
     _gxuse._gxtp=0
   endif
   _entr=0
 return

function dodisp()
  'set x '_x1' '_x2
  'set y '_y1' '_y2
  'set z '_z1' '_z2
if (_styp=1); _dv="x"; endif
if (_styp=2); _dv="y"; endif
if (_styp=3); _dv="z"; endif
if (_styp=3& _x1<_x2&_y1<_y2)
  'q dims'
  dum = sublin(result,2)
  lnlo = subwrd(dum,6)
  lnhi = subwrd(dum,8)
  dum = sublin(result,3)
  ltlo = subwrd(dum,6)
  lthi = subwrd(dum,8)
  'set mpdset lowres'
  if(lnhi-lnlo<90&lthi-ltlo<45); 'set mpdset mres'; endif
  if(lnhi-lnlo<20&lthi-ltlo<10); 'set mpdset hires'; endif
endif
t1=int((_t1-1)/_nint+1.0)
t2=int((_t2-1)/_nint+1.0)
if(_t1<_t2&_t2<_tnums&mod((_t2-1)*_tinc,_dtime.1)!=0); t2=t2+1; endif
_t = _t1;  _tt1=t1; _tt2=t2
'set t '_tt1' '_tt2
rc=plottype()
rc=setparea()
if (_plottyp=7 & _station=0)
  'set string 1 c 6'
  'set strsiz 0.18'
  'draw string '_xpur/2' '_ypur/2-0.5' Select single level of Lat, Lon, Lev, or Time'
  'draw string '_xpur/2' '_ypur/2-1.0' Click Mouse Button to Continue'
  'q pos'
  rc = clear()
  return
endif
if (_station!=0)
  if (_z1=_z2)
    'set string 1 c 6'
    'set strsiz 0.2'
    'draw string '_xpur/2' '_ypur/2-0.5' Select a range of levels for station data'
    'draw string '_xpur/2' '_ypur/2-1.0' Click Mouse Button to Continue'
    'q pos'
    rc = clear()
    return
  endif
  'set lat '_stlat._station
  'set lon '_stlon._station
  if (_t1<_t2)
    rc = dotime()
  else
    _nfram = 1
    _fram = 0
    rc = disprof()
  endif
else
  if(_plottyp=0|_plottyp=3|_plottyp=4|_plottyp=6)
    _nfram = 1
    _fram = 1
    rc = disp()
  endif
  if (_plottyp=1|_plottyp=2)
    if (_t1=_t2)
      rc = dodims()
    else
      rc = dotime()
    endif
  endif
  if(_plottyp=5)
    rc = dodims()
  endif
endif
_tclick = 2
_dclick = 2
     
return

function dotime()
  if (_t1<_t2) 
    'set dbuff on'
    _t = _t1
    _nfram=_t2-_t1+1
    _fram=1
    while (_t<=_t2)
      'set t 'int((_t-1)/_nint+1.0)
say T' '_t' 'int((_t-1)/_nint+1.0)
      if(_station!=0)
        rc = disprof()
      else
        rc = disp()
      endif
      _fram=_fram+1
      _t = _t + 1
      if (_t>_t2)
        'set string 1 c 6'
        'set strsiz 0.2'
        'draw string '_xpur/2' '_ypur-0.25' Click Mouse Button to Continue'
        _display=0
      endif
      'swap'
    endwhile
    if (_mtyp=0); 'q pos'; rc=clear(); endif
    'set dbuff off'
  else
    _nfram=1
  endif
  _t = _t1
  'set t '_tt1
return

function dodims()
  if (_styp=1)
    p1=_x1
    p2=_x2
  endif
  if (_styp=2)
    p1=_y1
    p2=_y2
  endif
  if (_styp=3)
    p1=_z1
    p2=_z2
  endif
  if (p1<p2) 
    'set dbuff on'
    p = p1
    _nfram=p2-p1+1
    _fram=1
    while (p<=p2) 
      'set '_dv' 'p
      _dlev = p
      rc = disp()
      _fram=_fram+1
      p = p + 1
      if (p>p2)
        'set string 1 c 6'
        'set strsiz 0.2'
        'draw string '_xpur/2' '_ypur-0.25' Click Mouse Button to Continue'
        _display=0
      endif
      'swap'
    endwhile
    if (_mtyp=0); 'q pos'; rc=clear(); endif
    'set dbuff off'
  else
    _nfram = 1
    _fram = 1
    rc = disp()
  endif
  'set '_dv' 'p1
return

function dosurf()
* define interpolation values
  b=mod((_t-1),_nint)/_nint
  a=1.0-b
  tob=int(b*_dtime.1/_dtime._fn)
  d=b*_dtime.1/_dtime._fn-tob
  c=1.0-d
  'set grads off'
  'set ccolor 0'
  'set cthick 6'
  'set gxout model'
*  'd u.'_fn'(t+'tob');v.'_fn'(t+'tob')'
  'set rgb 30 159 255 255'
  'set ccolor 30'
  'set cthick 6'
  'set gxout model'
  if (_t=_tnums)
    'd u.'_fn'(t+'tob');v.'_fn'(t+'tob')'
  else
    'd 'c'*u.'_fn'(t+'tob')+'d'*u.'_fn'(t+'tob+1');'c'*v.'_fn'(t+'tob')+'d'*v.'_fn'(t+'tob+1')'
  endif
  'set rgb 31 255 53 159'
  'set line 31'
  p=0
  while (p<=_sfcnum)
    p=p+1
    if(_picked.p=1)
      'q w2xy '_sfclon.p' '_sfclat.p
      sfx=subwrd(result,3)
      sfy=subwrd(result,6)
      'draw mark 3 'sfx' 'sfy' 0.07'
      'set string 31 bl 2'
      'set strsiz 0.08'
      'draw string 'sfx+0.08' 'sfy+0.08' '_sfcnam.p 
    endif
  endwhile
  while (_pick=1)
    inplot=0
    if(_xpos<=_parxmx & _xpos>=_parxmn & _ypos<=_parymx & _ypos>=_parymn); inplot=1; endif
    if(_btnN="1"); _pick=0; rc=clear(); break; endif
    if(_btnN="2"&inplot=1); rc=picksfc(_xpos,_ypos); endif
    if(_btnN="2"&inplot=0); _pick=2; break; endif
    if(_btnN="3"); _pick=0; break; endif
*   'program waits here for pick instruction'
    'q pos'
    _xpos = subwrd(result,3)
    _ypos = subwrd(result,4)
    _btnN = subwrd(result,5)
  endwhile
return

* Function to display a map
function disp()
  if(_mtyp=1 | _mtyp=3)
    file=filnam()
    'enable print 'file
  endif
* set map parameters
  if (_poli=1)
   'set poli on'
  else
   'set poli off'
  endif
  if (_grid=1)
   'set grid on 5 15'
  else
   'set grid off'
  endif
  'set mproj '_prj
  'set grads off'
  'set csmooth on'
  'set map 1 1 6'
  'set dignum 0'
  'set digsize .08'

* set up to plot shaded variable first
  if(vector=1 & _shad=_vsfc); _shad=_usfc; endif
  if(vector=1 & _shad=_vupr); _shad=_uupr; endif
  if(_shad!=0) 
    didshad=0
  else
    didshad=1
  endif

*** create defined variables here so they can be interpolated ***
'set t '_tt1' '_tt2
if(_vtyp._uupr=1)
  'define uuuupr = wspupr*cos((270-wdrupr)/180*3.1416)'
endif
if(_vtyp._vupr=1)
  'define vvvupr = wspupr*sin((270-wdrupr)/180*3.1416)'
endif
if(_vtyp._uupr=1&_vtyp._vupr=1)
  'define uuuupr = wspupr*cos((270-wdrupr)/180*3.1416)'
  'define vvvupr = wspupr*sin((270-wdrupr)/180*3.1416)'
endif
if(_vtyp._usfc=1)
  'define uuusfc = wspsfc*cos((270-wdrsfc)/180*3.1416)'
endif
if(_vtyp._vsfc=1)
  'define vvvsfc = wspsfc*sin((270-wdrsfc)/180*3.1416)'
endif
if(_vtyp._usfc=1&_vtyp._vsfc=1)
  'define uuusfc = wspsfc*cos((270-wdrsfc)/180*3.1416)'
  'define vvvsfc = wspsfc*sin((270-wdrsfc)/180*3.1416)'
endif
if(_vtyp._hd=1)
  uu='wspupr(lev=500)*cos((270-wdrupr(lev=500))/180*3.1416)'
  vv='wspupr(lev=500)*sin((270-wdrupr(lev=500))/180*3.1416)'
  'define divotr = hdivg('uu','vv')'
endif
if(_vtyp._vt=1)
  uu='wspupr(lev=500)*cos((270-wdrupr(lev=500))/180*3.1416)'
  vv='wspupr(lev=500)*sin((270-wdrupr(lev=500))/180*3.1416)'
  'define vorotr = hcurl('uu','vv')'
endif
if(_vtyp._tk=1)
  'define thkotr = gphupr(lev=500)-gphupr(lev=1000)'
endif
'set t 'int((_t-1)/_nint+1.0)

* Prescan variables
  i=1
  cn=0
  while (i<=_vnum)
    gxtp=_vgxt.i
    if(gxtp=1); cn=cn+1; endif
    i=i+1
  endwhile
  vector=0
  if (_vtyp._uupr=1&_vtyp._vupr=1); vector=1; endif
  if (_vtyp._usfc=1&_vtyp._vsfc=1); vector=1; endif

* Variable plot loop
  a=1; b=0
  i=1; j=0; k=1; l=1
  doit=0
while (i<=_vnum)
  if(i=_shad & didshad=0); doit=1; endif
  if(i!=_shad & didshad=1 & _vtyp.i=1); doit=1; endif
  if(i=_vsfc & _vgxt._vsfc=2 & didshad=1); doit=0; endif
  if(i=_vupr & _vgxt._vupr=2 & didshad=1); doit=0; endif
  if(doit=1)
    j=j+1
    gxtp=_vgxt.i
  zzz=subwrd(_gxtype,gxtp)
  say "graphics type="zzz
  'set gxout 'zzz

* set plot exceptions
  if((_plottyp=4|_plottyp=5)&_z1=_z2)
    'set xyrev on'
  endif
  if(_plottyp=5&_styp=3)
    'set xyrev on'
  endif
  if(_plottyp=1|_plottyp=2)
    'set '_dv' '_dlev
  endif

* set line and symbol type
  if(_plottyp=1|_plottyp=3|_plottyp=6)
    if(_styl.i=4); styl=5; else; styl=_styl.i; endif
    'set cstyle 'styl
    'set cmark '_mrkr.i
  endif

* set labels and y-axis colors
  levlab=subwrd(_nam,_dlev)
  'set grid off'
  if(_plottyp=2|_plottyp>=4)
    'set ylopts 1'
    if(didshad=1&_shad!=0&gxtp<=2)
      k=subwrd(_colors,l)
      'set ccolor 'k
    endif  
    if(cn>1&j>1&gxtp<=2)
      k=subwrd(_colors,j-1)
      'set ccolor 'k
    endif
  endif  
  if(_plottyp=0|_plottyp=1|_plottyp=3|_plottyp=6)
    k=subwrd(_colors,j)
    'set ccolor 'k
    'set ylopts 'k
  endif
*  if(_plottyp=1&_z1!=_z2&_styp!=3); k=1; endif


* define plot variable and settings
  var=subwrd(_vars,i)
  say "buttoned variable="var
  levels=getemp(var,_cint.i,_cmax.i,_cmin.i)
  if(_lbl.i=0)
    'set clab off'
  else
    'set clab on'
  endif
  'set clevs 'levels
  'set cthick 4'
 
* display variable
  if (_plottyp=1|_plottyp=2)  
*     define interpolation values
    b=mod((_t-1),_nint)/_nint
    a=1.0-b
    if ((i=_uupr|i=_usfc) & vector=1)
       vvar=vecvar(var,gxtp,_skip,a,b,t1,t2)
      'd 'vvar
      i = i + 1
    else
     if(_t=_tnums | a=1)
      'd 'var
     else
      'd 'a'*'var'+'b'*'var'(t+1)'
     endif
    endif
  else
    if ((i=_uupr|i=_usfc) & vector=1)
       a=0; b=0
       vvar=vecvar(var,gxtp,_skip,a,b,t1,t2)
      'd 'vvar
      i = i + 1
    else
      'd 'var
    endif
  endif
* add overlays
  if((i=_vsfc|i=_vupr) & (_vgxt._vsfc!=_vgxt._usfc|_vgxt._vupr!=_vgxt._uupr) & vector=1 & didshad=1)
    vgxt=subwrd(_gxtype,_vgxt._vsfc)
    gxtp=_vgxt._vsfc
    'set gxout 'vgxt
    var=subwrd(_vars,i)
    'set clevs 'levels
    if ((_plottyp=1|_plottyp=2)&_t<_tnums&a!=1)  
       post=vecvar(var,gxtp,_skip,a,b,t1,t2)
       'd 'post
    else
       a=0; b=0
       post=vecvar(var,gxtp,_skip,a,b,t1,t2)
       'd 'post
    endif
  endif
  if(_shad!=0 & didshad=0 & (_plottyp=2|_plottyp=4|_plottyp=5))
    'set gxout contour'
    'set clevs 'levels
    'set ccolor 0'
    if (_t<_tnums&a!=1)  
      if((i=_vupr|i=_vsfc) & vector=1)
        'd 'vvar
      else
        'd 'a'*'var'+'b'*'var'(t+1)'
      endif
    else
      if((i=_vupr|i=_vsfc) & vector=1)
        'd 'vvar
      else
        'd 'var
      endif
    endif
  endif
  if(_surface=1&_styp=3& _plottyp=2)
     rc=dosurf()
    _disurf=1
  endif 

* Labels in plots
  res=result
  'set string 'k' c 6'
  'set strsiz 0.15'
  xval=_parxmx - 1.5
  yval=_parymx - 0.5
  if((_plottyp=2|_plottyp=4|_plottyp=5)&_shad!=0)
    'set string 0 c 6'
  endif
  if(_plottyp=1|_plottyp=2|_plottyp=5)
    if (_x1=_x2 & _styp!=1)
      if(_shad=0); 'set string 1 c 6'; endif
      'draw string 'xval' 'yval' lon = 'subwrd(_lons,_x1)
    endif
    if (_y1=_y2 & _styp!=2)
      if(_shad=0); 'set string 1 c 6'; endif
      'draw string 'xval' 'yval' lat = 'subwrd(_lats,_y1)
    endif
    if (_z1=_z2 & _styp!=3)
      if (_nlevs.i = 1|_nlevs.i = 0)
        'draw string 'xval' 'yval' lev = surface'
      else
        'draw string 'xval' '%yval-0.3*j%' lev = 'subwrd(_levs,_z1)
      endif
    endif
  else
   if(_plottyp!=0&_plottyp!=5)
    if(_styp=1)
     if(_plottyp!=4)
      if (_nlevs.i = 1|_nlevs.i = 0)
        'draw string 'xval' '%yval-0.3*j%' lev = surface'
      else
        'draw string 'xval' '%yval-0.3*j%' lev = 'subwrd(_levs,_z1)
      endif
     endif
     if(_shad=0|_plottyp=1|_plottyp=3|_plottyp=6)
       'set string 1 c 6'
      endif
     'draw string 'xval' 'yval' lat = 'subwrd(_lats,_y1)
    endif
    if(_styp=2)
     if(_plottyp!=4)
      if (_nlevs.i = 1|_nlevs.i = 0)
        'draw string 'xval' '%yval-0.3*j%' lev = surface'
      else
        'draw string 'xval' '%yval-0.3*j%' lev = 'subwrd(_levs,_z1)
      endif
     endif
     if(_shad=0|_plottyp=1|_plottyp=3|_plottyp=6)
       'set string 1 c 6'
      endif
     'draw string 'xval' 'yval' lon = 'subwrd(_lons,_x1)
    endif
    if(_styp=3)
      if(_shad=0|_plottyp=1|_plottyp=3|_plottyp=6)
        'set string 1 c 6'
       endif
      'draw string 'xval' 'yval' lon = 'subwrd(_lons,_x1)
      'draw string 'xval' '%yval-0.3%' lat = 'subwrd(_lats,_y1)
    endif
   endif
  endif  

* Print single values (_plottyp=0)
  xval = (_parxmn+_parxmx)/2
  yval = _parymx - 0.5
  if (_plottyp=0)
      'set string 1 c 6'
      'set strsiz 0.15'
      'draw string 'xval' 'yval' lon = 'subwrd(_lons,_x1)
      'draw string 'xval' 'yval-0.3' lat = 'subwrd(_lats,_y1)
      'draw string 'xval' 'yval-0.6' lev = 'subwrd(_levs,_z1)
      yval = 5.5-j*0.2   
      'set string 'k' c 6'
      'draw string 'xval' 'yval' 'subwrd(res,4)
  endif   

*  Title at top of map
  if(_plottyp!=0)
    'draw title '_maptitle
  endif

*  Labels at bottom of plot
  'q gxinfo'
  dum = sublin(result,3)
  xlo = subwrd(dum,4)
  xhi = subwrd(dum,6)
  dum = sublin(result,4)
  ylo = subwrd(dum,4)
  yhi = subwrd(dum,6)
  rc=mydate()
  p1=tlabel(_t)
  verdat=p1 % ' ' % subwrd(rc,2) % ' ' % subwrd(rc,3) % ' ' % subwrd(rc,4)
  varnam=_vname.i
  if (_styp=1)
    levlab = "LON "%levlab
  endif
  if (_styp=2)
    levlab = "LAT "%levlab
  endif
  if (_styp=3)
    levlab = levlab%" MB"
  endif
  if ((_nlevs.i = 1|_nlevs.i = 0)&_styp=3)
    levlab="SURFACE"
  endif
  if (_styp=3 & substr(var,4,3)="sfc")
    levlab="SURFACE"
  endif 
  if (_styp=3 & substr(var,4,3)="otr")
    levlab="OTHER"
  endif 
  if (_styp=3 & (i=_uupr|i=_usfc|i=_vupr|i=_vsfc) & vector=1)
    varnam='WINDS'
  endif
  if(_plottyp=3)
    if (_styp=1)
      levlab = "LON"
    endif
    if (_styp=2)
      levlab = "LAT"
    endif
    if (_styp=3)
      levlab = "LEV"
    endif
  endif
  if(_plottyp=4)
    if (_styp!=3)
      if (_nlevs.i = 1|_nlevs.i = 0)
        levlab = "LEV SURFACE"
      else
        levlab = "LEV "%subwrd(_levs,_z1)
      endif
    endif
    if (_styp=3)
      if (_nlevs.i = 1|_nlevs.i = 0)
        levlab = "LEV SURFACE"
      endif
    endif
  endif
  alllab=varnam%"   "%levlab%"   "%verdat
  if(_plottyp=3)
    levlab=""
  endif
  len=howlong(alllab)
  labsiz=(xhi-xlo)/len
  if(labsiz > 0.12)
    labsiz=0.12
  endif
  lend=howlong(varnam)
  xleft=xlo+lend*labsiz
  rbeg=howlong(verdat)
  xright=xhi-rbeg*labsiz
  xcen=0.5*(xlo+xhi)
  if(xcen < lend)
    xcen=0.5*(xleft+xright)
  endif
  if(_plottyp=0)
    spc=2  
    xlo=2.5
    xhi=8.5
  else
    spc=-0.1
  endif
  if(_plottyp=2&gxtp!=1); k=1; endif
  if(_plottyp>=4)
    spc=-0.4
  endif
  'set strsiz 'labsiz' 0.12'
  'set string 'k' tr 6'
  'draw string 'xhi' '%(ylo-0.18*j+spc)' 'verdat
  'set string 'k' tl 6'
  'draw string 'xlo' '%(ylo-0.18*j+spc)' 'varnam
  'set string 'k' tc 6'
  'draw string 'xcen' '%(ylo-0.18*j+spc)' 'levlab

* add color bar if labels of shaded variable is off
  if (i=_shad & _lbl.i=0)
    'run cbarn.gs 1 1 '_parxmn/4' '_ypur/2
  endif
  if(_shad!=0 & didshad=0)
    didshad=1
    i=0
  endif
  if(gxtp=1&didshad=1); l=l+1; endif
 endif  
 i=i+1
 doit=0
endwhile
  _display=1
*  Add tclock if selected
  if (_clk!=0); rc=tclock(); endif 
*  Print if selected
 if (_mtyp>0&_mtyp<4)
  if(_mtyp=2)
    'print'
  else
    'swap'
    if(_mtyp=3)
     'disable print'
     '!xtof 'file' TIFF '_winid
    else
     'print'
    endif
    'disable print'
  endif
 endif
return 

* Function to display model and raob profiles
function disprof()
if(_mtyp=1 | _mtyp=3)
  file=filnam()
  'enable print 'file
endif
'set grads off'
'set strsiz 0.12'
'set ylopts 1'
* define interpolation values
  b=mod((_t-1),_nint)/_nint
  a=1.0-b 
  if(_t=_tnums); a=0; b=1; endif
* plot grid values
  i=1
  j=0
  while (i<=_vnum)
    if(_vtyp.i=1) 
      j=j+1
      'set grid off'
      'set cthick 4'
      if(_styl.i=4); styl=5; else; styl=_styl.i; endif
      'set cstyle 'styl
      'set cmark '_mrkr.i
      kc=subwrd(_colors,j)
      'set ccolor 'kc
      var=subwrd(_vars,i)
      rc=getemp(var,_cint.i,_cmax.i,_cmin.i)
      if(_t<_tnums)
        'd 'a'*'var'+'b'*'var'(t+1)'
      else
        'd 'var
      endif
      'set string 1 l 6'
      x=_parxmn
      y=_parymn-0.6
      'draw string 'x' 'y' Grid data'
      'set string 'kc' l 6'
      'draw string 'x+0.8*j+1.2' 'y' 'var
    endif
    i=i+1
  endwhile
* invert height and plot station data
  lev2=subwrd(_levs,_z2)
  lev1=subwrd(_levs,_z1)
  'set lev 'lev2' 'lev1
  'set yflip on'
  if(_t=_tnums); b=0; endif
  tob=int(b*_dtime.1/_dtime.2)
  i=1
  k=0
  while (i<=_vnum)
*    if(_vtyp.i=1&b*_dtime.2=0)
    if(_vtyp.i=1&mod(b*_dtime.1,_dtime.2)=0)
      k=k+1
      j=j+1
      'set cthick 6'
      if(_styl.i=4); styl=5; else; styl=_styl.i; endif
      'set cstyle 'styl
      'set cmark '_mrkr.i
      kc=subwrd(_colors,j)
      'set ccolor 'kc
      var=subwrd(_vars,i)
      rc=getemp(var,_cint.i,_cmax.i,_cmin.i)
      'd 'var'.2(t+'tob',stid='_stid._station')'
      res=result
* variable labels
      'set string 1 l 6'
      x=_parxmn
      y=_parymn-0.8
      if(subwrd(res,1)="No")
        'draw string 'x' 'y' No station data'
      else
        'draw string 'x' 'y' Raob data'
        'set string 'kc' l 6'
        'draw string 'x+0.8*k+1.2' 'y' 'var
      endif
    endif
    i=i+1
  endwhile

* Print single values
  xval = 5.5
  yval = _parymx - 1.0
  if (subwrd(res,1)="Result")
      'draw string 'xval' 'yval' lon = 'subwrd(_lons,_x1)
      'draw string 'xval' 'yval-0.3' lat = 'subwrd(_lats,_y1)
      'draw string 'xval' 'yval-0.6' lev = 'subwrd(_levs,_z1)
      yval = 4.5-j*0.3   
      'draw string 'xval' 'yval' 'subwrd(res,4)
  endif   

*  'draw xlab Temperature (C)'
  'draw ylab Height (m)'
  rc = mydate()
  p1 = tlabel(_t)
  tl2 = p1 % ' ' % subwrd(rc,2) % ' ' % subwrd(rc,3) % ' ' % subwrd(rc,4)
  tl3 = (_t-1)*_tinc
  'draw title ' _snam._station '\' tl2'  tau=' tl3 ' hr'
* set yflip off by issuing vpage command and reset levels
* vpage also resets the colors
  'set vpage off'
  'set z '_z1' '_z2
*  Add tclock if selected
  if (_clk!=0); rc=tclock(); endif 
*  Print if selected
 if (_mtyp>0&_mtyp<4)
  if(_mtyp=2)
    'print'
  else
    'swap'
    if(_mtyp=3)
     '!xtof 'file' TIFF '_winid
    else
     'print'
    endif
    'disable print'
  endif
 endif
return

* Function to display surface timelines
function disurf()
if(_mtyp=1 | _mtyp=3)
  file=filnam()
  'enable print 'file
endif
_disurf=0 
rc = clear()
* define time and interpolation values
  t1=int((_t1-1)/_nint+1.0)
  t2=int((_t2-1)/_nint+2.0)
if(_t1=_t2)
  'set t 1 '_tnum
else
  'set t 't1' 't2
endif
'set z '_z1' '_z2
if(_sfp=0)
  'set string 1 c 6'
  'set strsiz 0.18'
  'draw string '_xpur/2' '_ypur/2-1' Select Surface Stations first'
  return
endif

* make plot areas for each selected surface station
  left=_dimbxur+0.5
  right=_timbxll-0.6
  wide=right-left
  ymax=_ypur-_vbh*2-0.25
  ymin=1.0
  'set line 0'
  'draw recf 'left' 'ymin' 'right' 'ymax


* Prescan variables
  i=1; j=1
  cn=0; s=0
  while (i<=_vnum)
    gxtp=_vgxt.i
    if(gxtp=1); cn=cn+1; endif
    if(gxtp=2); s=j; endif
    if(_vtyp.i=1); j=j+1; endif
    i=i+1
  endwhile

* Plot variables
m=1
n=0
while(m<=_sfcnum)
 if(_picked.m=1)
* set up to plot shaded variable first
  if(_z1<_z2&_shad!=0) 
    didshad=0
    doit=0
  else
    didshad=1
    doit=1
  endif
  j=1; k=1; l=0
  base=0.0; delta=0.0
  if(n=_sfp-1); base=0.5; delta=0.08; endif
  top=ymax-n*(ymax-ymin-0.5)/_sfp-(_sfp-1-n)/_sfp*1.03
  botm=top-(ymax-ymin-0.5)/_sfp-base
  high=(ymax-ymin-0.5)/_sfp+base
  'set vpage 'left' 'right' 'botm+delta' 'top+delta
  'set grads off'
  'set parea 0.7 'wide+1.7' 'base' 'high
  'set lon '_sfclon.m
  'set lat '_sfclat.m
  'set xlab off'
  'set grid off'
  if(n=_sfp-1); 'set xlab on'; endif

* plot grid values
  i=1
  while (i<=_vnum)
    if(_vtyp.i=1) 
      if(i=_shad & didshad=0); doit=1; endif
      if(i!=_shad & didshad=1); doit=1; endif
      if(doit=1)
        gxtp=_vgxt.i
        if(gxtp=1&didshad=1); l=l+1; endif
        if(_z1<_z2)
          zzz=subwrd(_gxtype,gxtp)
          say "graphics type="zzz
          'set gxout 'zzz
        endif
        levlab=subwrd(_nam,_dlev)
        if(l>1&didshad=1)
          k=subwrd(_colors,l-1)
          'set ccolor 'k
        endif  
        if(cn>1&j>1)
          k=subwrd(_colors,j-1)
          'set ccolor 'k
        endif  
        'set cthick 4'
        if(_styl.i=4); styl=5; else; styl=_styl.i; endif
        'set cstyle 'styl
        'set cmark '_mrkr.i
        var=subwrd(_vars,i)
        levels=getemp(var,_cint.i,_cmax.i,_cmin.i)
        if (_z1=_z2)
          kc=subwrd(_colors,j)
          'set ccolor 'kc
        else
          'set clevs 'levels
        endif
        'd 'var
        'set string 1 l 9'
        'set strsiz '0.2-_sfp*0.01
        'draw string 1.0 'high-0.25+_sfp*0.02' '_sfcnam.m
        'set string 1 r 9'
        str="Lon = "_sfclon.m"  Lat = "_sfclat.m
        'draw string 'wide-0.5' 'high-0.25+_sfp*0.02' 'str
        j=j+1
        doit=0
      endif
    endif
    if(_z1<_z2 & i=_shad & didshad=0)
      'set gxout contour'
      'set clevs 'levels
      'set ccolor 0'
      'd 'var
      didshad=1
      i=0
    endif
    i=i+1
  endwhile

* plot surface data
  i=1
  while (i<=_vnum)
    if(_vtyp.i=1)
      'set cthick 6'
      if(_styl.i=4); styl=5; else; styl=_styl.i; endif
      'set cstyle 'styl
      'set cmark '_mrkr.i
      var=subwrd(_vars,i)
      rc=getemp(var,_cint.i,_cmax.i,_cmin.i)
      kc=subwrd(_colors,j)
      if (_z1=_z2)
        'set ccolor 'kc
        'd 'var'.'_fn'(stid='_sfcnam.m')'
      endif
      res.i=subwrd(result,3)
      j=j+1
    endif
    i=i+1
  endwhile

* add labels 
  if(n=_sfp-1)
    'set vpage off'
    'set string 1 c 10'
    'set strsiz 0.25'
    if(_z1=_z2)
      'draw string 5.5 '_ypur-_vbh*2-0.5' Surface Time Line'
    else
      'draw string 5.5 '_ypur-_vbh*2-0.5' Model Time Section'
    endif
    x=_parxmn
    y=0.6
    'set string 1 l 6'
    'set strsiz 0.12'
    'draw string 'x' 'y' Grid data'
    i=1; j=1
    while (i<=_vnum)
      if(_vtyp.i=1)
        var=subwrd(_vars,i)
        if (_z1<_z2)
          if(_shad=0)
            if(j=1)
              kc=1
            else
              kc=subwrd(_colors,j-1)
            endif
          else
            if(j<s)
              kc=subwrd(_colors,j)
            endif
            if(j=s)
              kc=1
            endif
            if(j>s)
              kc=subwrd(_colors,j-1)
            endif
          endif
        else
          kc=subwrd(_colors,j)
        endif
        'set string 'kc' l 6'
        'draw string 'x+0.8*j+1.2' 'y' 'var
        j=j+1
      endif
      i=i+1   
    endwhile
    if(_z1=_z2)
       y=0.4
      'set string 1 l 6'
      'draw string 'x' 'y' Surface data'
      i=1; k=1
      while (i<=_vnum)
        if(_vtyp.i=1)
          var=subwrd(_vars,i)
          kc=subwrd(_colors,j)
          'set string 'kc' l 6'
          if(res.i="Error:")
            'set string 1 l 6'
            'draw string 'x+0.8*k+1.2' 'y' none'
          else
            'draw string 'x+0.8*k+1.2' 'y' 'var
          endif
          j=j+1
          k=k+1
        endif
        i=i+1   
      endwhile
    endif
  endif
  n=n+1
 endif
 m=m+1
endwhile
* vpage also resets the colors
  'set vpage off'
  'set x '_x1' '_x2
  'set y '_y1' '_y2
  _t = _t1
 if (_mtyp>0&_mtyp<4)
  if(_mtyp=2)
    'print'
  else
    'swap'
    if(_mtyp=3)
     '!xtof 'file' TIFF '_winid
    else
     'print'
    endif
    'disable print'
  endif
 endif
return

function vecvar(var,gxtp,n,a,b,t1,t2)
nchvar=_nchvr
varz=substr(var,4,nchvar)
  uu='uuu'%varz
  vv='vvv'%varz
* define vecvar
if((b=0)|_t=_tnums)
 if(gxtp=3|gxtp=4)
  vecvar='skip('uu','n');'vv';mag('uu','vv')'
 else
  vecvar='mag('uu','vv')'
 endif
 if(gxtp=5)
  vecvar=uu';'vv';mag('uu','vv')'
 endif
else
  arg1=a'*'uu'+'b'*'uu'(t+1)'
  arg2=a'*'vv'+'b'*'vv'(t+1)'
 if(gxtp=3|gxtp=4)
   vecvar='skip('arg1','n');'arg2';mag('arg1','arg2')'
 else
   vecvar='mag('arg1','arg2')'
 endif
 if(gxtp=5)
   vecvar=arg1';'arg2';mag('arg1','arg2')'
 endif
endif
*set display attributes
 levels=getemp(wspsfc,_cint._wspsfc,_cmax._wspsfc,0.0)
 'set clevs 'levels
 'set arrscl 0.5 '_cmax._wspsfc
 'set strmden '_dens
return vecvar

function howlong(str)
i=1
while (z != "")
z=substr(str,i,1)
i=i+1
endwhile
return i

function plottype()
* set plot type
* plottyp=0 is no plot, print data
* plottyp=1 is line plot, static and animated
* plottyp=2 is 2D section, static and animated
* plottyp=3 is line plot for displayed dimension range
* plottyp=4 is static time section
* plottyp=5 is animated time section
* plottyp=6 is line plot for displayed time range
* plottyp=7 is 4D, no plot
if(_t1=_t2&_x1=_x2&_y1=_y2&_z1=_z2)
  _plottyp=0
endif
if(_t1=_t2&_x1=_x2&_y1=_y2&_z1<_z2)
  if (_styp=3); _plottyp=3; else; _plottyp=1; endif
endif
if(_t1=_t2&_x1=_x2&_y1<_y2&_z1=_z2)
  if (_styp=2); _plottyp=3; else; _plottyp=1; endif
endif
if(_t1=_t2&_x1=_x2&_y1<_y2&_z1<_z2)
  if (_styp=1); _plottyp=2; else; _plottyp=1; endif
endif
if(_t1=_t2&_x1<_x2&_y1=_y2&_z1=_z2)
  if (_styp=1); _plottyp=3; else; _plottyp=1; endif
endif
if(_t1=_t2&_x1<_x2&_y1=_y2&_z1<_z2)
  if (_styp=2); _plottyp=2; else; _plottyp=1; endif
endif
if(_t1=_t2&_x1<_x2&_y1<_y2&_z1=_z2)
  if (_styp=3); _plottyp=2; else; _plottyp=1; endif
endif
if(_t1=_t2&_x1<_x2&_y1<_y2&_z1<_z2)
  _plottyp=2
endif
if(_t1<_t2&_x1=_x2&_y1=_y2&_z1=_z2)
  _plottyp=6
endif
if(_t1<_t2&_x1=_x2&_y1=_y2&_z1<_z2)
  if (_styp=3); _plottyp=4; else; _plottyp=1; endif
endif
if(_t1<_t2&_x1=_x2&_y1<_y2&_z1=_z2)
  if (_styp=2); _plottyp=4; else; _plottyp=1; endif
endif
if(_t1<_t2&_x1=_x2&_y1<_y2&_z1<_z2)
  if (_styp=1); _plottyp=2; else; _plottyp=5; endif
endif
if(_t1<_t2&_x1<_x2&_y1=_y2&_z1=_z2)
  if (_styp=1); _plottyp=4; else; _plottyp=1; endif
endif
if(_t1<_t2&_x1<_x2&_y1=_y2&_z1<_z2)
  if (_styp=2); _plottyp=2; else; _plottyp=5; endif
endif
if(_t1<_t2&_x1<_x2&_y1<_y2&_z1=_z2)
  if (_styp=3); _plottyp=2; else; _plottyp=5; endif
endif
if(_t1<_t2&_x1<_x2&_y1<_y2&_z1<_z2)
  _plottyp=7
endif
return

function style(i)
  if(_styl.i=1); _sty.i='solid'; endif
  if(_styl.i=2); _sty.i='long dash'; endif
  if(_styl.i=3); _sty.i='short dash'; endif
  if(_styl.i=4); _sty.i='dotted'; endif
return

function marker(i)
  if(_mrkr.i=0); _mkr.i='none'; endif
  if(_mrkr.i=1); _mkr.i='cross'; endif
  if(_mrkr.i=2); _mkr.i='open circle'; endif
  if(_mrkr.i=3); _mkr.i='closed circle'; endif
  if(_mrkr.i=4); _mkr.i='open square'; endif
  if(_mrkr.i=5); _mkr.i='closed square'; endif
return

function getemp(tname,cint,cmax,cmin)
***WARNING!!! (ce-co)/ci must be < 99
vname=substr(tname,1,3)
ci=10; co=-100; ce=100; cinc=5
if(vname="dmdz"); ci=40; co=-200; ce=200; cinc=5; endif
if(vname="ee"); ci=50; co=0; ce=1500; cinc=10; endif
if(vname="eh"); ci=50; co=0; ce=1500; cinc=10; endif
if(vname="hdiv"); ci=0.00005; co=-0.001; ce=0.001; cinc=0.00001; endif
if(vname="m"); ci=25; co=250; ce=1000; cinc=5; endif
if(vname="och"); ci=50; co=0; ce=3000; cinc=5; endif
if(vname="p"); ci=50; co=0; ce=1050; cinc=5; endif
if(vname="pc"); ci=0.1; co=0; ce=10; cinc=0.02; endif
if(vname="ps"); ci=5000; co=60000; ce=105000; cinc=500; endif
if(vname="pmsl"); ci=2; co=960; ce=1030; cinc=1; endif
if(vname="q"); ci=1; co=0; ce=30; cinc=0.5; endif
if(vname="qc"); ci=0.000001; co=0; ce=0.00005; cinc=0.0000005; endif
if(vname="qi"); ci=0.000001; co=0; ce=0.00005; cinc=0.0000005; endif
if(vname="qr"); ci=0.000001; co=0; ce=0.00005; cinc=0.0000005; endif
if(vname="rh"); ci=5; co=0; ce=100; cinc=1; endif
if(vname="ri"); ci=0.5; co=-5; ce=1; cinc=0.1; endif
if(vname="slp"); ci=400; co=96000; ce=103000; cinc=100; endif
if(vname="tau"); ci=0.01; co=0; ce=1; cinc=0.002; endif
if(vname="t"); ci=2; co=250; ce=310; cinc=1; endif
if(vname="tc"); ci=2; co=-50; ce=40; cinc=1; endif
if(vname="td"); ci=2; co=-50; ce=40; cinc=1; endif
if(vname="terr"); ci=200; co=-5000; ce=5000; cinc=10; endif
if(vname="th"); ci=2; co=250; ce=310; cinc=1; endif
if(vname="ts"); ci=2; co=250; ce=310; cinc=1; endif
if(vname="u"); ci=1; co=-30; ce=30; cinc=1; endif
if(vname="v"); ci=1; co=-30; ce=30; cinc=1; endif
if(vname="vort"); ci=0.00005; co=-0.001; ce=0.001; cinc=0.00001; endif
if(vname="vv"); ci=1; co=0; ce=10; cinc=0.5; endif
if(vname="z"); ci=500; co=-5000; ce=5000; cinc=10; endif
if(vname="z5"); ci=500; co=4500; ce=6500; cinc=10; endif
*** TESS parameters ***
if(vname="btt"); ci=5; co=-5; ce=41; cinc=5; endif
if(vname="csd"); ci=5; co=0; ce=360; cinc=5; endif
if(vname="csh"); ci=5; co=0; ce=160; cinc=5; endif
if(vname="cta"); ci=0.5; co=0; ce=9; cinc=0.5; endif
if(vname="cuu"); ci=5; co=-15; ce=15; cinc=5; endif
if(vname="cvv"); ci=5; co=-15; ce=15; cinc=5; endif
if(vname="div"); ci=0.00005; co=-0.001; ce=0.001; cinc=0.00001; endif
if(vname="dpt"); ci=5; co=-90; ce=60; cinc=5; endif
if(vname="fdp"); ci=5; co=-180; ce=180; cinc=5; endif
if(vname="fpp"); ci=5; co=0; ce=100; cinc=5; endif
if(vname="fzl"); ci=100; co=100; ce=9900; cinc=50; endif
if(vname="gph"); ci=100; co=-400; ce=9000; cinc=100; endif
if(vname="mco"); ci=5; co=-200; ce=200; cinc=5; endif
if(vname="prs"); ci=4; co=876; ce=1094; cinc=2; endif
if(vname="qpf"); ci=1; co=0; ce=20; cinc=1; endif
if(vname="sdr"); ci=5; co=0; ce=360; cinc=5; endif
if(vname="sse"); ci=5; co=0; ce=160; cinc=5; endif
if(vname="ssp"); ci=10; co=0; ce=900; cinc=5; endif
if(vname="swh"); ci=5; co=0; ce=160; cinc=5; endif
if(vname="thk"); ci=100; co=-400; ce=9000; cinc=100; endif
if(vname="tmp"); ci=5; co=-90; ce=60; cinc=5; endif
if(vname="uuu"); ci=5; co=-15; ce=15; cinc=5; endif
if(vname="vvv"); ci=5; co=-15; ce=15; cinc=5; endif
if(vname="vor"); ci=0.00005; co=-0.001; ce=0.001; cinc=0.00001; endif
if(vname="wdr"); ci=5; co=0; ce=360; cinc=5; endif
if(vname="wsp"); ci=5; co=0; ce=100; cinc=5; endif
if(vname="wuu"); ci=10; co=-400; ce=400; cinc=5; endif
if(vname="wvp"); ci=5; co=0; ce=360; cinc=5; endif
if(vname="wvv"); ci=10; co=-400; ce=400; cinc=5; endif
if(vname="wwh"); ci=5; co=0; ce=160; cinc=5; endif
***

if(cint!="")
  ci=cint
endif
_ci=ci
_cinc=cinc
if(cmax!="")
  ce=cmax
endif
_cmx=ce
if(cmin!="")
  co=cmin
endif
_cmn=co
i = 0
levels=co
cc = co
while (cc < ce)
  i = i + 1
  cc=co + i*ci
  levels=levels % ' ' % cc
endwhile
if(_plottyp=1|_plottyp=2|_plottyp=4|_plottyp=5|_station!=0)
  'set vrange 'co' 'ce
endif
return levels

function readsfc()
i=0
while (1)
  res=read(stations.sfc)
  dum=sublin(res,1)
  cod=subwrd(dum,1)
  if(cod!=0)
    if(cod=1); say "Error opening file"; endif
    if(cod=8); say "File open for write"; endif
    if(cod=9); say "I/O error"; endif
    break
  endif
  i=i+1
  dum=sublin(res,2)
  _sfcnam.i=subwrd(dum,1)
  _sfclat.i=subwrd(dum,2)
  _sfclon.i=subwrd(dum,3)
endwhile
_sfcnum=i
rc=close (stations.sfc)
return

function readua()
i=0
while (1)
  res=read(stations.ua)
  dum=sublin(res,1)
  cod=subwrd(dum,1)
  if(cod!=0)
    if(cod=1); say "Error opening file"; endif
    if(cod=8); say "File open for write"; endif
    if(cod=9); say "I/O error"; endif
    break
  endif
  i=i+1
  dum=sublin(res,2)
  _stid.i=subwrd(dum,1)
  _stlat.i=subwrd(dum,2)
  _stlon.i=subwrd(dum,3)
  _snam.i=subwrd(dum,4)
  _snam.i=_snam.i %' '% subwrd(dum,5)
  _snam.i=_snam.i %' '% subwrd(dum,6)
endwhile
_stnnum=i
rc=close (stations.ua)
return

function getloc(lat,lon)
test=1
pick=0
i=0
while(i<_sfcnum)
  i=i+1
  lat2=(_sfclat.i-lat)*(_sfclat.i-lat)
  lon2=(_sfclon.i-lon)*(_sfclon.i-lon)
  sum2=lat2+lon2
  if(sum2<test)
    test=sum2
    pick=i
  endif
endwhile
return pick

function picksfc(x,y)
'q xy2w 'x' 'y
lon=subwrd(result,3)
lat=subwrd(result,6)
n=getloc(lat,lon)
if(n=0); return; endif
if(_picked.n!=1); i=1; endif
if(_picked.n=1); i=0; endif
if(i=1)
  'q w2xy '_sfclon.n' '_sfclat.n
  _sfx.n=subwrd(result,3)
  _sfy.n=subwrd(result,6)
  'set line 31'
  'draw mark 3 '_sfx.n' '_sfy.n' 0.08'
  'set string 31 bl 1'
  'set strsiz 0.08'
  'draw string '_sfx.n+0.08' '_sfy.n+0.08' '_sfcnam.n 
  _picked.n=1
  _sfp=_sfp+1
endif
if(i=0 & _sfp!=0)
  'set line 0'
  'draw mark 3 '_sfx.n' '_sfy.n' 0.08'
  'set line 30'
  'draw mark 2 '_sfx.n' '_sfy.n' 0.08'
  'set string 0 bl 1'
  'set strsiz 0.08'
  'draw string '_sfx.n+0.08' '_sfy.n+0.08' '_sfcnam.n 
  _picked.n=0
  _sfp=_sfp-1
endif
return

function output()
  rc = clear()
  'set strsiz 0.18'
  'set string 2 c 12'
if(_nfram>1&_mtyp=1)
  'set strsiz 0.225'
  'draw string '_xpur/2' '_ypur/2' ONLY ONE PLOT CAN BE PRINTED'  
  'set strsiz 0.18'
  'draw string '_xpur/2' '_ypur/2-1' Eliminate any animations and reprint'  
  'draw string '_xpur/2' '_ypur/2-3' Click any mouse button to continue'
  'q pos'
else
  if (_mtyp=4)
    rc=automate()
    rc=clear()
    return
  endif
*  if (_mtyp=3)
*say X1' '_x1' 'Y1' '_y1' 'Z1' '_z1' 'T1' '_t1
*    return
*  endif
  if (_mtyp=2)
    'run xwwout.gs gxout 1 2'
  else
    'run xwwout.gs '_name' '_nfram' '_mtyp' '_dir
  endif
  rc = clear()
endif
return

function zoomin()
  'q xy2gr '_xpos' '_ypos
  xcen=subwrd(result,3)
  ycen=subwrd(result,6)
  xrng=_x2-_x1
  yrng=_y2-_y1
  xmid=(_x2+_x1)/2
  ymid=(_y2+_y1)/2
  xfrac=(xcen-xmid)/xrng
  yfrac=(ycen-ymid)/yrng
  if(xfrac<0); xfrac=-xfrac; endif
  if(yfrac<0); yfrac=-yfrac; endif
  if ((xfrac<0.1&yfrac<0.1)|(_x1=1&_x2=_xnum&_y1=1&_y2=_ynum))
    _x2=int(xcen+xrng/4+0.51)
    _y2=int(ycen+yrng/4+0.51)
    _x1=int(xcen-xrng/4+0.49)
    _y1=int(ycen-yrng/4+0.49)
  else
    _x2=int(xcen+xrng/2+0.51)
    _y2=int(ycen+yrng/2+0.51)
    _x1=int(xcen-xrng/2+0.49)
    _y1=int(ycen-yrng/2+0.49)
  endif
  if(_x2>_xnum); _x2=_xnum; endif
  if(_y2>_ynum); _y2=_ynum; endif
  if(_x1<1); _x1=1; endif
  if(_y1<1); _y1=1; endif
return

function zoomout()
  xrng=_x2-_x1
  yrng=_y2-_y1
  xmid=(_x2+_x1)/2
  ymid=(_y2+_y1)/2
  _x2=int(xmid+xrng+0.51)
  _y2=int(ymid+yrng+0.51)
  _x1=int(xmid-xrng+0.49)
  _y1=int(ymid-yrng+0.49)
  if(_x2>_xnum); _x2=_xnum; endif
  if(_y2>_ynum); _y2=_ynum; endif
  if(_x1<1); _x1=1; endif
  if(_y1<1); _y1=1; endif
return

function clear()
  'clear'
  'set line 95'
  'draw recf 0.0 0.0 '_xpur' '_ypur
  _display=0
return

function colors()
*  Set factor
  fac=1.1; add=31

*  Set colors
  cn = (255-add)*100*fac/255+add
  tl = (255-add)*50*fac/255+add
  br = (255-add)*200*fac/255+add
  bg = (255-add)*25*fac/255+add

*  Button colors: 90-center; 91-top,left; 92-bottom,right
  'set rgb 90 'cn' 'cn' 'cn
  'set rgb 91 'tl' 'tl' 'tl
  'set rgb 92 'br' 'br' 'br

*  Background color
  'set rgb 95 0 0 'bg

*  Set plot, label, and other colors 
   _colors="8 5 6 14 3 11 12 9 7 13 15 10 8 5 6 14 3 11 12 9 7 13 15 10"

return

function tclock()
  x0 = (_timbxll+_timbxur)/2-0.15
  y0 = (_timbyll+_timbyur)/2
  csize = 2*(_timbxur-_timbxll)
* get greenwich time
  rc = mydate()
  day=subwrd(rc,2) % ' ' % subwrd(rc,3)
  rc = tlabel(_t)
  time=subwrd(rc,1)
  hour=substr(time,1,2)
  if (substr(time,3,1)=":");
    min=substr(time,4,2)
    if(substr(time,6,1)=":"); min=min+substr(time,7,2)/60; endif
  else
    min=0
  endif
* correct to local
  xmid=int((_x2+_x1)/2)
  'set x 'xmid
  'q dims'
  xdef=sublin(result,2)
  lmid=subwrd(xdef,6)
say LMID' 'lmid' 'XMID' 'xmid
  if(lmid<0)
    gmoffset=int(lmid/15-0.5) 
  else
    gmoffset=int(lmid/15+0.5) 
  endif 
  hour=hour+gmoffset
  if(hour<0); hour= hour+24; endif
  if(hour>=24); hour=hour-24; endif
  if(hour>=6&hour<=19)
    cfacecol=7
  else
    cfacecol=0
  endif
  if(hour<12)
    ampm='AM'
  else
    ampm='PM'
  endif
  rc=clock(x0,y0,csize,hour,min,cfacecol,ampm,day)
return

function clock(x0,y0,csize,hour,min,cfacecol,ampm,day)
*
*     function to draw a clock with hour and min hands
*
pi2=2*3.14159
radius=csize*0.5
hourhand=radius*0.6
minhand=radius*0.8
handcol=1
if(cfacecol!=0);handcol=0;endif
'set line 'cfacecol
'draw mark 3 'x0' 'y0' 'csize

'set line 1 1 8'
'draw mark 2 'x0' 'y0' 'csize
*
*     draw the min and hour hands
*
thetamin=(min/60)*pi2
thetahour=((hour+min/60)/12)*pi2

'd sin('thetamin')'
xm=subwrd(result,4)
xm=xm*minhand
'd cos('thetamin')'
ym=subwrd(result,4)
ym=ym*minhand

'd sin('thetahour')'
xh=subwrd(result,4)
xh=xh*hourhand
'd cos('thetahour')'
yh=subwrd(result,4)
yh=yh*hourhand

x1=x0+xm
y1=y0+ym
'set line 'handcol' 1 5'
'draw line 'x0' 'y0' 'x1' 'y1

x1=x0+xh
y1=y0+yh
'set line 'handcol' 1 6'
'draw line 'x0' 'y0' 'x1' 'y1

ys=y0-radius-0.1

'set strsiz 0.10'
'set string 3 c 4'
'draw string 'x0' 'ys' 'ampm' 'day
'draw string 'x0' 'ys-0.175' LOCAL'

return

function filnam1 ()
  i=1; j=0
  while (i<=_vnum)
    if (_vtyp.i=1)
      j=j+1
      var.j=subwrd(_vars,i)
    endif
    i=i+1
  endwhile
  if (j=1); vnam=substr(var.1,1,3); endif
  if (j=2); vnam=substr(var.1,1,2)%substr(var.2,1,1); endif
  if(j>=3); vnam=substr(var.1,1,1)%substr(var.2,1,1)%substr(var.3,1,1); endif
say 'j = 'j' and vnam is >'vnam'<'
say 'DTG is '_dtg
  month=substr(_dtg,6,3)
say 'month is 'month
  if (month='JAN'); month='01'; endif
  if (month='FEB'); month='02'; endif
  if (month='MAR'); month='03'; endif
  if (month='APR'); month='04'; endif
  if (month='MAY'); month='05'; endif
  if (month='JUN'); month='06'; endif
  if (month='JUL'); month='07'; endif
  if (month='AUG'); month='08'; endif
  if (month='SEP'); month='09'; endif
  if (month='OCT'); month='10'; endif
  if (month='NOV'); month='11'; endif
  if (month='DEC'); month='12'; endif
say 'month = 'month
  day=substr(_dtg,4,2)
  zulu=substr(_dtg,1,1)
say 'day = 'day' and zulu is 'zulu
  if (_nfram>1)
    if (_styp=1); mode="x"; endif
    if (_styp=2); mode="y"; endif
    if (_styp=3); mode="z"; endif
    if (_t2>_t1); mode="t"; endif
  endif
  if (_nfram=1); mode="s"; endif
say 'nfram = '_nfram' and styp is '_styp' and mode is 'mode
  framchar = '0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z'
  fram = subwrd(framchar,_fram)
say 'frame = '_fram' and frame is 'fram 
  _name = vnam%month%day%zulu%mode
say 'name is '_name
  file = _name%fram
say "file is "file
return(file)

function filnam ()
  i=1; j=0
  file=""
  while (i<=_vnum&j<=4)
    if(_vtyp.i=1)
      var=subwrd(_vars,i)
      file=file%substr(var,1,2)
      j=j+1
    endif
    i=i+1
  endwhile
  if(j=0); return; endif
  if(j=1); file=file%"000000"; endif
  if(j=2); file=file%"0000"; endif
  if(j=3); file=file%"00"; endif
  if (_styp=1); mode="x"; lv=_x1; endif
  if (_styp=2); mode="y"; lv=_y1; endif
  if (_styp=3); mode="z"; lv=_z1; endif
  if (_t2>_t1); mode="t"; endif
  ta=_t1
  if (strlen(lv)=1); lv="0"%lv; endif
  if (strlen(ta)=1); ta="0"%ta; endif
  if (_nfram=1); mode=_styp; endif
  framchar = '0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z'
  fram = subwrd(framchar,_fram)
  _name = file%lv%ta%mode
  file = _name%fram
  _autofile = _name%'A'
return(file) 

function automate()
* Save plot settings in auto update file
  rc=filnam()
  autofile=_autofile
  record='DFIL '_fname.1
  rc=write(autofile, record)
  record='TITLE '_maptitle
  rc=write(autofile, record, append)
  if(_styp=1); 'set x '_x1' '_x2; endif
  if(_styp=2); 'set y '_y1' '_y2; endif
  if(_styp=3); 'set z '_z1' '_z2; endif
  if(_t2>_t1); 'set t '_t1' '_t2; endif
  'q dims'
  xdef=sublin(result,2)
  wlon=subwrd(xdef,6)
  elon=subwrd(xdef,8)
  if(elon="="); elon=''; endif
  record='XDEF 'wlon' 'elon
  rc=write(autofile, record, append)
  ydef=sublin(result,3)
  slat=subwrd(ydef,6)
  nlat=subwrd(ydef,8)
  if(nlat="="); nlat=''; endif
  record='YDEF 'slat' 'nlat
  rc=write(autofile, record, append)
  zdef=sublin(result,4)
  blev=subwrd(zdef,6)
  tlev=subwrd(zdef,8)
  if(tlev="="); tlev=''; endif
  record='ZDEF 'blev' 'tlev
  rc=write(autofile, record, append)
  tdef=sublin(result,5)
  tbeg=subwrd(tdef,6)
  tend=subwrd(tdef,8)
  if(tend="=") 
    record='TDEF '_tinc' '_t1' 'tbeg
  else
    record='TDEF '_tinc' '_t1' 'tbeg' '_t2' 'tend
  endif
  rc=write(autofile, record, append)
  record='PLOT '_case' '_plottyp' '_styp' '_grid' '_poli' '_prj' '_clk' '_skip' '_dens
  rc=write(autofile, record, append)
  i=1; num=0
  while (i<=_vnum)
   if(_vtyp.i=1)
     num=num+1
   endif
   i = i + 1
  endwhile
  record='VARS 'num
  rc=write(autofile, record, append)
  i=1
  while (i<=_vnum)
   if(_vtyp.i=1)
    record=subwrd(_vars,i)' '_vgxt.i' '_cmin.i' '_cmax.i' '_cint.i' '_lbl.i' '_clb.i' '_styl.i' '_mrkr.i
    rc=write(autofile, record, append)
   endif
   i = i + 1
  endwhile
  rc=write(autofile, 'ENDVARS', append)   
  rc=close(autofile)
  '!mv 'autofile' AUTO'
  if(_styp=1); 'set x '_x1; endif
  if(_styp=2); 'set y '_y1; endif
  if(_styp=3); 'set z '_z1; endif
  if(_t2>_t1); 'set t '_t1; endif
return

function strlen(str)
 i=1
 while (chr != "")
   chr=substr(str,i,1)
   i=i+1
 endwhile
return i-2

function getinfo()
'!xwininfo -int -name GrADS > wininfo'
i=0; gotid=0
while (1)
  res=read(wininfo)
  dum=sublin(res,1)
  cod=subwrd(dum,1)
  if(cod!=0)
    if(cod=1); say "Error opening file"; endif
    if(cod=8); say "File open for write"; endif
    if(cod=9); say "I/O error"; endif
    break
  endif
  i=i+1
  dum=sublin(res,2)
  if(subwrd(dum,2)="Window"&subwrd(dum,5)='"GrADS"')
    _winid=subwrd(dum,4)
    gotid=1
    break
  endif
endwhile
rc=close(wininfo)
'!rm wininfo'
return gotid

function hex2dec(str)
say STR' 'str
i=strlen(str)
say I' 'i
j=1; dec=0
while (i>0)
  chr=substr(str,i,1)
  if(chr="x"|chr="X"); break; endif
  digit = chr
  if(chr="a"|chr="A"); digit=10; endif
  if(chr="b"|chr="B"); digit=11; endif
  if(chr="c"|chr="C"); digit=12; endif
  if(chr="d"|chr="D"); digit=13; endif
  if(chr="e"|chr="E"); digit=14; endif
  if(chr="f"|chr="F"); digit=15; endif
  if(chr="0"|chr="O"); digit=0; endif
  k=1; pwr=1
  while (k<j)
   pwr=pwr*16
   k=k+1
  endwhile
  dec=dec+digit*pwr
  i=i-1
  j=j+1
endwhile
return dec

  
  

