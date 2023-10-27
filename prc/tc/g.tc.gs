function main(args)

rc=gsfallow('on')
rc=const()
rc=jaecol2()


_docp=0

_xsizepng=1024
_ysizepng=768

_xsizepng=1200
_ysizepng=900

_xsizepng=800
_ysizepng=600

_verb=0
#
# _dofcplot handles case where no fc; just plot bt
# set to 0 in trkrd
#
_dofcplot=1
#oooooooooooooooooooooooooooooooooooooooooooooo


#
# use only bt for setting lat/lon to keep size fixed 
#
_ltlnmax='fc'
_ltlnmax='bt'
#
# if 1 then plot script ack
#
_misctle=0
_dobasemap=1
_doeps=1
_dormgm=1

#oooooooooooooooooooooooooooooooooooooooooooooo

n=1
_ptype=subwrd(args,n) ; n=n+1
_btpath=subwrd(args,n) ; n=n+1
_ftpath=subwrd(args,n) ; n=n+1
_vpath=subwrd(args,n) ; n=n+1
_pltdir=subwrd(args,n) ; n=n+1
_plot=subwrd(args,n) ; n=n+1
_model=subwrd(args,n) ; n=n+1
_sn=subwrd(args,n) ; n=n+1
nstorm=subwrd(args,n) ; n=n+1
nbasin=subwrd(args,n) ; n=n+1
dtg=subwrd(args,n) ; n=n+1
_vtype=subwrd(args,n) ; n=n+1
_bname=subwrd(args,n) ; n=n+1
_year=subwrd(args,n) ; n=n+1
_opt1=subwrd(args,n) ; n=n+1


_imodel=_model
print 'ppppppppppppp '_model
print 'ppppppppppppp '_sn
print 'ppppppppppppp '_btpath
print 'ppppppppppppp '_ftpath
print 'ppppppppppppp '_vpath
print 'ppppppppppppp '_pltdir

if(_opt1 = 'll')
_ilat1=subwrd(args,n) ; n=n+1
_ilat2=subwrd(args,n) ; n=n+1
_ilon1=subwrd(args,n) ; n=n+1
_ilon2=subwrd(args,n) ; n=n+1
endif

_tcname='NULL'
_tctype='NULL'
if(_opt1 = 'name')
  _tctype=subwrd(args,n) ; n=n+1
  _tcname=subwrd(args,n) ; n=n+1
endif

_opt2=subwrd(args,n) ; n=n+1
_opt3=subwrd(args,n) ; n=n+1




_script='g.tc.gs'
_author='CDR M. Fiorino, USNR, NRL Monterey NR S&T 114 TC Analysis Project'

#
# set printer
#
#_printer='ps_vax_c_t'

_printer='ps_oa_c_t'
_printer='ps_oa_c'
_printer='hpcolor'
_printer='tek'
_printer='file'

_gifgeom=_xsizepng'x'_ysizepng

_gifmethod='convert'
_gifmethod='wi'

# 20021121
# -- turn off eps and wi gif

_gifmethod='png'


_sthk=6
_lthk=6

#
#  set how often the BT are plot
#
_hh='12'
_hh='00and12'

#_opt2='syn06_18'
if(_opt2 = 'syn06_18')
  _hh='06and18'
endif

if(_opt2 = 'syn00_12')
  _hh='00and12'
endif


_hh='all'
_jinc=2

'set rgb 90 100 100 100'
'set rgb 91  50 50 50 '
'set rgb 92 200 200 200'
'set button 1 90 91 92 1'

narg=n-1

if(_verb=1)
print 'args:'
print args

n=1
while(n<=narg) 
  print 'n = 'n' arg = 'subwrd(args,n)
 n=n+1
endwhile
endif

_script='~fiorino/era/tc/grf/g.tc.gs sig args: '_year' '_sn' '_model' '_vtype

if(_vtype = 'homo')
  nvtype=2
endif

if(_vtype = 'hetero')
  nvtype=1
endif

'open dum'

if(_plot='') ; _plot=n ; endif

_int=y
_mode='single'
_mode='int'

rc=setup()

*********************************************************
*
*	graphics set up
*
*********************************************************

rc=plotdims()
if(_misctle = 1) ; rc=scrptle() ; endif

*
*	options
*

ppx=0.90
ppy=0.90
pytoff=0.35
pyboff=0.35
pytoff=0.00
pyboff=0.00
_stlscl=0.8

laydir=1
np=4
np=2
asymx=0.8
asymy=0.5

if(_opt1 = '2plot') 
pytoff=0.35
endif

rc=plotarea(np,ppx,ppy,laydir,pytoff,pyboff,asymx,asymy)

*
*	basic setup
*

_dtau=12
_ntau=(144/12) + 1
_undef=-999.0
_ltmn=90
_ltmx=-90
_ltmxtl=60
_ltmntl=-60


_mc1=2
_mc2=4
_mm1=1
_mm2=5

rc=trkrd()
if(rc=999) ; print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTT'; 'quit' ; endif

if(_ptype = 'batch' | _ptype = 'batchint' ) 
  rc=trkbch(0)
  if(rc=999 & _ptype='batch') ; 'quit' ; endif
  return
endif

if(_opt1 = '2plot')
rc=trk2p(0)
return
endif

rc=trkall(0)

while(1)
rc=trkgui()
if(rc=999) ; 'quit' ; endif
endwhile

return



function trkbch(rescale)

rc=setbackground(1)
rc=setgrads()

i=1
'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i

if(_opt1=ll)
_ltmn=_ilat1
_ltmx=_ilat2
_lnmn=_ilon1
_lnmx=_ilon2
_ltmno=_ilat1
_ltmxo=_ilat2
_lnmno=_ilon1
_lnmxo=_ilon2
print 'LLLLLL force set : _ilat1 _ilat2 _ilon1 _ilon2'
endif


rc=trkmap(rescale)
rc=trk2xy()
_model=_models.1

rc=trktle()
rc=trkset()
rc=trklgd()
rc=lgndstat()
rc=trkplt()



ii=_nt.1

gname=setgname()

model1=_model

_gmpath1=gname'.gm'
_pspath1=gname'.ps'
_pngpath1=gname'.png'
_epspath1=gname'.eps'
_epsipath1=gname'.epsi'

if(_verb=1)
print 'PPPPPPPPPPPPPPPPPP 1111111111111111111'
print 'epspath1  la '_epspath1
print 'pngpath1  '_pngpath1
print ' '
endif
tack1=_author
tack2=_pspath1
if(_misctle = 1)
rc=bottitle(tack1,tack2,0.8,1,1)
endif



if(_doeps=1)
'set grid on 3 1'
'd d'
'enable print '_gmpath1
'print'
'disable print'
'!gxeps -c -i '_gmpath1' -o '_epspath1
if(_dormgm=1) ; '!rm '_gmpath1 ; endif

#'!convert -crop 0x0 -density 144 -rotate 90 -geometry '_gifgeom' 'pspath1
#'!convert -rotate 90  700x560+40+30 'pspath1' 'gifpath1
endif

print 'pngpath1  '_pngpath1
'printim '_pngpath1' x'_xsizepng' y'_ysizepng' white'


if(_nmod >= 2) 
rc=setbackground(1)
rc=setgrads()
_model=_models.2
model2=_model

rc=trkmap(rescale)
rc=trktle()
rc=trkplt()
rc=trklgd()

gname=setgname()

_gmpath2=gname'.gm'
_pspath2=gname'.ps'
_pngpath2=gname'.png'
_epspath2=gname'.eps'
_epsipath2=gname'.epsi'

tack1=_author
tack2=_pspath2
rc=bottitle(tack1,tack2,0.8,1,1)

if(_verb = 1)
print 'PPPPPPPPPPPPPPPPPP 22222222222222222222222'
print 'pspath2   '_pspath2
print 'pngpath2  '_pngpath2
print ' '
endif

if(_doeps=1)
'enable print '_gmpath2
'print'
'disable print'
'!gxeps -c -i '_gmpath2' -o '_epspath2
if(_dormgm=1) ; '!rm '_gmpath2 ; endif

#'!convert -crop 0x0 -density 144 -rotate 90 -geometry '_gifgeom' 'pspath2
#'!convert -rotate 90 -crop 700x560+50+30 'pspath2
endif

#  always do printim
print 'pngpath2  '_pngpath2
'printim '_pngpath2' x'_xsizepng' y'_ysizepng' white'


if(_docp & _ptype = 'batch')

  _gmpath=_gmpath1
  _pspath=_pspath1
  _pngpath=_pngpath1
  _epspath=_epspath1
  _epsipath=_epsipath1

  rc=cpplots()

  _gmpath=_gmpath2
  _pspath=_pspath2
  _pngpath=_pngpath2
  _epspath=_epspath2
  _epsipath=_epsipath2

  rc=cpplots()

endif

# do merging in p.tc.ops.update.pl vice here....

domerge=0
if(domerge)
  gname=_pltdir'/tc.trk.'model1'.'model2'.'_year'.'_sn'.'dtg
  gifpath=gname'.gif'
  print 'merge: 'gifpath
  '!gifmerge -l0 -150 'gifpath1' 'gifpath2' > 'gifpath
endif

endif
return(999)

function trk2p(rescale)

'c'
i=1
print 'parea i = 'i' '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i
'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i

rc=setgrads()

rc=trkmap(rescale)
rc=trk2xy()
rc=trktle()
rc=trkplt()
rc=trklgd()

sscl=0.7
s1=modtle(_model)
rc=stitle(s1,_stlscl)

i=2
'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i
print 'parea i = 'i' '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i
_model=_models.2
rc=trkmap(rescale)
rc=trk2xy()
rc=trkplt()
rc=trklgd()

s1=modtle(_model)
rc=stitle(s1,_stlscl)
rc=trkgui()
return

#------------------------------------------------------------------------------
#
#  cp plots for web  and create a log
#
#------------------------------------------------------------------------------

function cpplots(tdir)

if(_curseason = '' | _curseason='_curseason')

  csfile='/tmp/zy0x1s2.tc'

  '!echo $WXMAP_TC_CURRENT_SEASON > 'csfile
  '!echo $WXMAP_TC_SITREP_DIR >> 'csfile
  rc=read(csfile)
  _curseason=subwrd(rc,2)

  rc=read(csfile)
  _sitrepdir=subwrd(rc,2)
  '!rm 'csfile

endif

tdir=_sitrepdir'/'_curseason'/plt'

if(tdir != '')
  '!cp '_pngpath' 'tdir
  '!cp '_pspath' 'tdir
  '!cp '_gmpath' 'tdir
endif

logfile='/tmp/plot.log_g.tc.bt.climo.ll.gs_.txt'

rc=write(logfile,_gmpath)
rc=write(logfile,_pngpath,append)
rc=write(logfile,_pspath,append)
rc=write(logfile,_epspath,append)
rc=write(logfile,_epsipath,append)

return




function setbackground(opt)

if(opt = 1)
  'set display color white'
  'set rgb 99 254 254 254'
  'set background 99'
endif

return


function trkall(rescale)

rc=setbackground(1)

i=1
'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i

rc=setgrads()

if(_opt1 = 'll')
_ltmn=_ilat1
_ltmx=_ilat2
_lnmn=_ilon1
_lnmx=_ilon2
_ltmno=_ilat1
_ltmxo=_ilat2
_lnmno=_ilon1
_lnmxo=_ilon2
print 'LLLLLL force set : _ilat1 _ilat2 _ilon1 _ilon2'
endif

rc=trkmap(rescale)
rc=trk2xy()
rc=trktle()
rc=trkplt()
rc=trklgd()
rc=trkgui()
return



function trkgui

#----------------------------------------------------------------------
#
#	buttons
#
#----------------------------------------------------------------------

if(_nmod = 3)
if(_model=_models.1) ; bmodel=_models.2 ; endif
if(_model=_models.2) ; bmodel=_models.3 ; endif
if(_model=_models.3) ; bmodel=_models.1 ; endif
else
if(_model=_models.1) ; bmodel=_models.2 ; endif
if(_model=_models.2) ; bmodel=_models.1 ; endif
endif


'draw button 1 0.60 0.30 0.6 0.20 zoom'
'draw button 2 1.30 0.30 0.6 0.20 eps'
'draw button 7 1.90 0.30 0.6 0.20 png'
'draw button 3 2.60 0.30 0.6 0.20 'bmodel
'draw button 4 3.30 0.30 0.6 0.20 break'
'draw button 5 3.90 0.30 0.6 0.20 Redo'
'draw button 6 4.60 0.30 0.6 0.20 QUIT'

#----------------------------------------------------------------------
#
#	set up a rubber band widget and do a q pos
#
#----------------------------------------------------------------------

'set rband 10 box '_xlplot' '_ybplot' '_xrplot' '_ytplot

'q pos'
print 'trkgui ---- result 'result

x1=subwrd(result,3)
y1=subwrd(result,4)

btype=subwrd(result,5)
wtype=subwrd(result,6)
bnum=subwrd(result,7)


#----------------------------------------------------------------------
#
#	process rubber band
#
#----------------------------------------------------------------------

if(wtype=2)

  x2=subwrd(result,8)
  y2=subwrd(result,9)   

  if(x2 < x1) ; xx=x1 ; x1=x2 ; x2=xx ; endif
  if(y2 < y1) ; yy=y1 ; y1=y2 ; y2=yy ; endif


  'set line 0 1 20'
  'draw rec 'x1' 'y1' 'x2' 'y2
  'set line 1 1 5'
  'draw rec 'x1' 'y1' 'x2' 'y2


  'q xy2w 'x1' 'y1
  ln1=subwrd(result,3)
  lt1=subwrd(result,6)

  ln1=nint(ln1)
  lt1=nint(lt1)

  'q xy2w 'x2' 'y2
  ln2=subwrd(result,3)
  lt2=subwrd(result,6)
  ln2=nint(ln2)
  lt2=nint(lt2)


  if(lt1 < lt2)  
    _ltmn=lt1
    _ltmx=lt2
  else 
    _ltmn=lt2
    _ltmx=lt1
  endif

  if(ln1 < ln2)
    _lnmn=ln1
    _lnmx=ln2
  else
    _lnmn=ln2
    _lnmx=ln1
  endif

  lndist=abs(_lnmx-_lnmn)
  if(lndist  >  0 & lndist <=  5)  ; _lnint=0.5 ; endif
  if(lndist  >  5 & lndist <= 10)  ; _lnint=  1 ; endif
  if(lndist  > 10 & lndist <= 20)  ; _lnint=  2 ; endif

  ltdist=abs(_ltmx-_ltmn)
  if(ltdist  >  0 & ltdist <=  5)  ; _ltint=0.5 ; endif
  if(ltdist  >  5 & ltdist <= 10)  ; _ltint=  1 ; endif
  if(ltdist  > 10 & ltdist <= 20)  ; _ltint=  2 ; endif

endif

#----------------------------------------------------------------------
#
#	process buttons
#
#----------------------------------------------------------------------

if(wtype = 1) 

  if(bnum = 1)

    rc=setgrads()
    rc=trkmap()
    rc=trk2xy()
    rc=trktle()
    rc=trkplt()
    rc=trklgd()
    return(bnum)
  endif

  if(bnum=2 | bnum=7)
#    'q dialog type file name'
#    say result
    if(_ltmn>=0)
      latbndmn=_ltmn'N'
    else
      latbndmn=abs(_ltmn)
      latbndmn=latbndmn'S'
    endif
  
    if(_ltmx>=0)
      latbndmx=_ltmx'N'
    else
      latbndmx=abs(_ltmx)
      latbndmx=latbndmx'S'
    endif
  
    latbnd=latbndmn'-'latbndmx

    if(_lnmn > 180) 
      ll=360-_lnmn
      latbnd=latbnd'-'ll'W'
    endif

    if(_lnmn <= 180)
      latbnd=latbnd'-'_lnmn'E'
    endif

    if(_lnmx > 180)
      ll=360-_lnmx
      latbnd=latbnd'-'ll'W'
    endif
    if(_lnmx <= 180)
      latbnd=latbnd'-'_lnmx'E'
    endif

    print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP'
###    print gifpath' '_ltmn' '_ltmx' '_lnmn' '_lnmx' 'latbnd


    gname=setgname()
    if(_opt1 != 'll')
      gname=gname'.'latbnd
    endif

    pngpath=gname'.png'
    gmpath=gname'.gm'
    epspath=gname'.eps'
    pspath=gname'.ps'

    if(bnum = 2 | bnum = 7) 

      if(bnum = 2)
      'enable print 'gmpath
      'print'
      'disable print'
      print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP gxeps'
      '!gxeps -c -i 'gmpath
      if(_dormgm=1) ; '!rm '_gmpath ; endif

#      print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP gxps'
#      '!gxps -b 0.0 -c -i 'gmpath' -o 'pspath
#
#  do png using printim
#  
      endif
      print 'PPPPPPPPPPPPPPPPPPPPP (trkgui) - png : 'pngpath
      'printim 'pngpath' x'_xsizepng' y'_ysizepng' white'

      if(_gifmethod = 'wi')     
        rc=replot(pspath)
        print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP wi'
        print 'gifpath = 'gifpath
        'wi 'gifpath
      else
###    '!convert -crop 0x0 -density 144 -rotate 90 -geometry '_gifgeom' 'pspath
#    '!convert -density 144 -rotate 90 -geometry '_gifgeom' 'pspath
#        print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP convert'
#        print 'gifpath = 'gifpath
      endif


if(bnum = 2)
if(_printer = 'tek' | _printer = 'hpcolor') 
      '!lpr -P'_printer' 'epspath
      print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP lpr'
      '!lpstat -p'_printer
      print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP all done'

else

if(_printer != 'file')
      '!lpr -s -P'_printer' 'epspath
      print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP lpr'
      '!lpq -P'_printer
      print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP all done'
endif
endif
endif
 

      return(bnum)
    endif
  endif

  if(bnum=3)
    print '3333333333333333333 '_model
    if(_nmod = 3)
    if(_model = _models.1) ; nmodel=_models.2 ; endif
    if(_model = _models.2) ; nmodel=_models.3 ; endif
    if(_model = _models.3) ; nmodel=_models.1 ; endif
    else
    if(_model = _models.1) ; nmodel=_models.2 ; endif
    if(_model = _models.2) ; nmodel=_models.1 ; endif
    endif
    _model=nmodel
    rc=trkall(0)
  endif


  if(bnum=5)
    rc=trkall(1)
  endif

  if(bnum=6)
    return(999)
  endif

  return(bnum)

endif

return


function setgname()
if(_tcname != 'NULL')
  if(_tctype != 'NULL')
    gname=_pltdir'/tc.trk.'_model'.'_year'.'_sn'.'_tcname'.'_tctype
  else
    gname=_pltdir'/tc.trk.'_model'.'_year'.'_sn'.'_tcname
  endif
else
  gname=_pltdir'/tc.trk.'_model'.'_year'.'_sn
endif
return(gname)

function setgrads()

  'c'
  'set grads off'
###  'set timelab on'
  'set xlopts 1 '_lthk
  'set ylopts 1 '_lthk 

return


#
#------------- replot
#

function replot(pspath)

   rc=setgrads()
   rc=trkmap()
   rc=trk2xy()
   rc=trktle()
   rc=trkplt()
   rc=trklgd()

   tack1=_author
   tack2=pspath
   rc=bottitle(tack1,tack2,0.7,1,1)

return


*
*-------------------  trkrd -----------------
*
function trkrd()

lnmnw=999
lnmxw=-999
lnmne=999
lnmxe=-999

_ltmx=-999
_ltmn=999

_btpath='/tmp/g.tc.btgcards.txt'

rc=read(_btpath)
card=sublin(rc,2)
iok=sublin(rc,1)
if(iok != 0 ) ; print 'unable to read _btpath '_btpath ; 'quit' ; endif

nbt=subwrd(card,3)

i=1
while(i<=nbt) 
  rc=read(_btpath)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  if(iok != 0 ) ; print 'eof reading '_btpath ; 'quit' ; endif
  if(_verb) ; print 'BT card = 'card' '_ptype ; endif

  _dtg.i.1=subwrd(card,1)
  _lt.i.1.1=subwrd(card,2)
  _ln.i.1.1=subwrd(card,3)
  _mw.i.1.1=subwrd(card,4)
  _tau.i.1.1=000
  _btvflg.i.1.1=subwrd(card,5)
  _nt.i.1=1

  if(_verb) ; print 'BTTTTTT: '_dtg.i.1' '_lt.i.1.1' '_ln.i.1.1' '_mw.i.1.1 ; endif
  i=i+1 
endwhile

_nt.1=nbt*1

print 'qqqqqqqqqqqqq '_btpath' 'nbt
modelnew='asfdasdfasdf'
nmodel=0
imodel1=0
imodel2=0
imodel3=0
iok=0
jmax=_ntau

#
# read in forecast track
#

_ftpath='/tmp/g.tc.fcgcards.txt'
nread=0
while(iok=0)

  rc=read(_ftpath)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  if(_verb);  print '0000000 ft iok = 'iok' 'card' '_ftpath ; endif
  if(iok=2)
    _ntau=0
  endif

  model=subwrd(card,1)
  if(model != modelnew & _ntau != 0)
    nmodel=nmodel+1
    if(_verb)
       print 'MMM new model 'model' nmodel = 'nmodel
    endif

    _models.nmodel=model
    modelnew=model
  endif

  dtg=subwrd(card,2)

  if(model = _models.1) ; kmod=2 ; imodel1=imodel1+1 ; i=imodel1 ; endif
  if(model = _models.2) ; kmod=3 ; imodel2=imodel2+1 ; i=imodel2 ; endif
  if(model = _models.3) ; kmod=4 ; imodel3=imodel3+1 ; i=imodel3 ; endif
  
  if(_ntau != 0) 
  j=1
  k=4
  while(j<=_ntau)
    tau=subwrd(card,k)
    if(tau = '') ; break ; endif
    lat=subwrd(card,k+1)
    lon=subwrd(card,k+2)
    mw=subwrd(card,k+3)
    fe=subwrd(card,k+4)

#
# check if model crossing GM ; cliper bug
#
docorr=1

if(docorr=1 & lat > 0 & j > 1)
    lntest=_ln.i.1.kmod
    if(lntest > 180 & lon < 50)
print 'CCCGGGMMM crossing GM 'lntest' 'lon
       lon=360+lon
    endif
#
# cliper bug
#
    if(lntest > 300 & (lon > 50 & lon <= 200) )
print 'CCCGGGMMM cliper bug 'lntest' 'lon
       lon=180+lon
    endif
endif

    _tau.i.j.kmod=tau
    _lt.i.j.kmod=lat
    _ln.i.j.kmod=lon
    _mw.i.j.kmod=mw
    _fe.i.j.kmod=fe

    k=k+6
    if(_verb)
      print 'model dtg 'i' 'j' 'kmod' : 'model' 'dtg' 'tau' 'lat' 'lon' 'mw' fe: 'fe
    endif

    j=j+1

  endwhile

  j=j-1

  if(_verb)
     print '111111111111111 i = 'i' kmod = 'kmod' j = 'j' 'dtg
  endif

  _nt.i.kmod=j
  _nt.kmod=i
  _dtg.i.kmod=dtg

  endif
 
  nread=nread+1 
endwhile

#
# detect if any fc cards read...
# if nread = 1 then none
#

if(nread = 1)
  _dofcplot=0
  _models.1=_imodel
  _models.2=_imodel
  _models.3=_imodel
  _model=_imodel
endif

_nmod=nmodel
#_nmod=2
#if(nmodel = 1 & _model = 'mrf') ; _nmod=1 ; endif
#if(nmodel = 1 & _model = 'ifs') ; _nmod=1 ; endif
#if(nmodel = 1 & _model = 'ngp') ; _nmod=1 ; endif

if(_verb = 1)
print 'NNNMMMOOODDD '_nmod' 'nmodel
k=1
while(k <= _nmod)
  
  print 'MMMMMMMMMMMMMMMM 'k' : '_models.k
  k=k+1
endwhile

endif

k=1
kend=_nmod+1
if(_opt1 = '2plot') 
  kend=1
endif


if(_ltlnmax = 'bt') ; kend=1 ; endif
while(k<=kend)

  i=1
  if(_nt.k = '') ; _nt.k = 0 ; endif

  while(i<=_nt.k) 

    j=1

if(_nt.i.k = '' | _nt.i.k > 150)
return(999)
endif

    ne=_nt.i.k
    if(_ltlnmax = 'bt') ; ne=1 ;endif
    while(j<=ne)

      if(_lt.i.j.k > _ltmx ) ; _ltmx=_lt.i.j.k ; endif
      if(_lt.i.j.k < _ltmn ) ; _ltmn=_lt.i.j.k ; endif

      lne=_ln.i.j.k

#print '----------lne 'i' 'j' 'k' 'lne' '_lt.i.j.k

      if(lne >= 0 & lne <180)
        if(lne < lnmne) ; lnmne=lne ; endif
        if(lne > lnmxe) ; lnmxe=lne ; endif
      else
        if(lne < lnmnw) ; lnmnw=lne ; endif
        if(lne > lnmxw) ; lnmxw=lne ; endif
      endif

      j=j+1
    endwhile

    i=i+1
  endwhile

  k=k+1
endwhile

_verb=1
*
*	lat/lon bounds
*
*	check for crossing W to E
*
t1=360-lnmnw
t2=360-lnmxw

if(_verb=1)
print 'ln www  't1' 't2
print 'ln eee  'lnmne' 'lnmx
endif
*
*	check if crossing the dl or gm
*
if(lnmne=999 | lnmnw=999)
  _lnmn=lnmnw
  _lnmx=lnmxw
  if(lnmnw=999)
    _lnmn=lnmne
    _lnmx=lnmxe
  endif
else
print 'inside 'lnmnw' 'lnmxe
  dln=lnmnw-lnmxe
  if(dln > 180)
    _lnmn=lnmnw
    _lnmx=360+lnmxe
  else
    _lnmn=lnmne
    _lnmx=lnmxw
  endif
endif


if(_verb = 1)
print 'qqq lnmn and mx '_lnmn' '_lnmx 
print 'qqq ltmn and mx '_ltmn' '_ltmx
endif

*
*	tolerance on latitude
*
if(_ltmx > _ltmxtl) ; _ltmx=_ltmxtl ; endif 
if(_ltmn < _ltmntl) ; _ltmn=_ltmntl ; endif 

if(_verb=1)
print 'qqq ltmn and mx 11111  '_ltmn' '_ltmx
endif

lttol=5
lntol=10

_lnint=lntol
_ltint=lttol

ltdist=_ltmx - _ltmn

if(_bname = 'sio' & ltdist < 5)
  lttol=12.5
  lntol=lttol*2
  _lnint=10
  _ltint=10
endif


_ltmn=int(_ltmn)
_ltmx=int(_ltmx)
_lnmn=int(_lnmn)
_lnmx=int(_lnmx)

if(_ltmn < 0) 
_ltmn=nint(_ltmn/lttol)-1
_ltmx=nint(_ltmx/lttol)-1
else
_ltmn=nint(_ltmn/lttol)
_ltmx=nint(_ltmx/lttol)
endif

_lnmn=nint(_lnmn/lttol)
_lnmx=nint(_lnmx/lttol)

_ltmn=_ltmn*lttol-lttol
_ltmx=_ltmx*lttol+lttol

_lnmn=_lnmn*lttol-lntol
_lnmx=_lnmx*lttol+lntol

aspect=(_ltmx-_ltmn)/(_lnmx-_lnmn)

if(_verb=1)
  print 'AAA before aspect 'aspect' '_ltmx' '_ltmn' '_lnmx' '_lnmn
endif

maxiter=10
iter=1
while(aspect < 0.5 & iter <= maxiter) 
  _ltmx=_ltmx+lttol
  _ltmn=_ltmn-lttol
  aspect=(_ltmx-_ltmn)/(_lnmx-_lnmn)
  if(_verb=1)
  print 'YYY ASPECT  adjust 'aspect
  endif
  iter=iter+1
endwhile

iter=1
while(aspect > 0.9 & iter <= maxiter) 
  _lnmx=_lnmx+lntol
  _lnmn=_lnmn-lntol
  aspect=(_ltmx-_ltmn)/(_lnmx-_lnmn)
  if(_verb=1)
  print 'XXX ASPECT  adjust 'aspect
  endif
  iter=iter+1
endwhile

if(_verb=1)
  print 'AAA AFTER aspect 'aspect' '_ltmx' '_ltmn' '_lnmx' '_lnmn
endif

_lnmn=265.0
_lnmx=290.0
_ltmn=20.0
_ltmx=40.0


if(iter >= maxiter)
 return(999)
endif


*
*	store for later use
*
_lnmno=_lnmn
_lnmxo=_lnmx
_ltmno=_ltmn
_ltmxo=_ltmx
_lninto=_lnint
_ltinto=_ltint

return


function trkzm()
return
*
*-------------------  trkmap -----------------
*

function trkmap(rescale)
#'set rgb 50 175 175 175'
#'set background 50'
#'c'

if(rescale=1) 
  'set lat '_ltmno' '_ltmxo
  'set lon '_lnmno' '_lnmxo
  _ltmn=_ltmno
  _ltmx=_ltmxo
  _lnmn=_lnmno
  _lnmx=_lnmxo
  _lnint=_lninto
  _ltint=_ltinto
else
  'set lat '_ltmn' '_ltmx
  'set lon '_lnmn' '_lnmx
endif

'set map 15 0 6'
hreslim=25
if((abs(_ltmx-_ltmn) < hreslim) | (abs(_lnmx-_lnmn) < hreslim ))

#  print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS hires'
  _mapres='H'
  'set mpdset hires'
  'set mpdset mres'
else 
#  print 'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM mres'
  'set mpdset mres'
  _mapres='M'
endif

'set xlint '_lnint
'set ylint '_ltint
'define d=const(d,0,-a)'
'set cmax -1'
'set gxout fgrid'
'set fgvals 1 1'
'd d'

#
# now that we have an plot env; do the basemap
#

if(_dobasemap = 1)
  'set rgb 41 245 255 255'
  'basemap L 72 1 M'
  'basemap O 41 1 M'
#'basemap L 85 1 H'
endif

'set grid on 3 1'
'd d'

rc=plotdims()
return


*
*-------------------  trklgd -----------------
*
function trklgd()
i=1
if(_opt1 = '2plot') 
'set clip 0 8.5 0 11'
else
'set clip 0 11 0 8.5'
endif
lscl=1.0
lscl=0.9
x=_xpr.1+(0.50)*(1.5/lscl)
xs=x+(0.25)*lscl
y=_ytplot
y=8.0
dy=0.165*lscl
yss=dy*0.60*lscl

while(i<=_btlgd.n)

 'draw wxsym '_btlgd.sym.i' 'x' 'y' '_btlgd.siz.i' '_btlgd.col.i' 8'

  'set string 1 l '_sthk
  'set strsiz 'yss
  dddd=_btlgd.dtg.i
  d4=substr(dddd,5,6)
  d4=dddd
  lmw=_btlgd.mw.i
  if(lmw < 100) ; lmw=' 'lmw ; endif
  lgd='- 'd4' 'lmw
  'draw string 'xs' 'y' 'lgd
  y=y-dy
  i=i+1
endwhile
return
*
*-------------------  trktlte -----------------
*
function trktle()
*
*	titles
*
nbt=_nt.1
ttlscl=1.0
t1col=1
t2col=2
if(_model = 'ifs') 
  mname='ECMWF IFS CY22R3 (T`bL`n319L60)'
  mname='ECMWF IFS CY23R4 (T`bL`n511L60)'
  mname='ECMWF IFS (ops)'
endif

if(_model = 'mrf') 
  mname='NCEP MRF (T170L40)'
endif

if(_model = 'avn') 
  mname='NCEP GFS (AVN) (T170L40)'
  mname='NCEP GFS (AVN) (T254L68)'
endif

if(_model = 'eco') 
  mname='ECMWF IFS (ops) (T`bL`n511L60)'
endif
if(_model = 'ece') 
  mname='ECMWF IFS (EPS) (T`bL`n255L40)'
endif

if(_model = 'ukm') 
  mname='UKMO UM (0.83x0.55L38)'
endif

if(_model = 'fv4') 
  mname='NASA GOES4 (0.36x0.25L??)'
endif

if(_model = 'fv5') 
  mname='NASA GOES5 (0.36x0.25L??)'
endif

if(_model = 'btk') 
  mname='Best Track'
endif

if(_model = 'clp') 
  mname='CLIPER (no-skill)'
endif

if(_model = 'ofc') 
  mname='Official (JTWC|NHC)'
endif

if(_model = 'esuite') 
  mname='ECMWF IFS **ESUITE** CY22R3 (T`bL`n319L60)'
endif

if(_model = 'ifc') 
  mname='ECMWF IFS CY22R3 (T`bL`n319L60) CORR'
endif

if(_model = 'ngp')
  mname='FNMOC NOGAPS4.0 (T159L23)'
  mname='FNMOC NOGAPS4.0 (T239L30)'
endif

if(_model = 'clp')
  mname='CLIPER'
endif

if(_model = 'e40')
  mname='ERA-40'
endif

lmodel=strlen(_model)

if(lmodel > 3 & _model != 'esuite') 
  mname='IFS EXP ('_model')'
endif

if(_opt1='2plot') ; mname='' ; endif

if(_tcname != 'NULL')
  t1=mname' Forecasts for `4'_year' '_sn' `0'_tctype' `2'_tcname
  if(_model = 'btk')
    t1=mname' for `4'_year' '_sn' `0'_tctype' `2'_tcname
  endif
else
  t1=mname' Forecasts for `4'_year'`0 TC '_sn
  if(_model = 'btk')
    t1=mname' for `4'_year'`0 TC '_sn
  endif
endif

if(nbt<4)
  t2='period '_dtg.1.1
else
  t2='period '_dtg.1.1' to '_dtg.nbt.1
endif
rc=toptitle(t1,t2,ttlscl,t1col,t2col)

return


function modtle(model)

if(model = 'ifs') 
  mname='ECMWF IFS CY22R3 (T`bL`n319L60)'
endif

if(model = 'ifc') 
  mname='ECMWF IFS CY22R3 (T`bL`n319L60) CORR'
endif

if(model = 'ngp')
  mname='FNMOC NOGAPS4.0 (T159L23)'
endif

lmodel=strlen(model)

if(lmodel > 3) 
  mname='IFS EXP ('model')'
endif

return(mname)

*
*-------------------  trk2xy -----------------
*
function trk2xy()
*
*	convert track to plot coord
*
k=1
while(k<=_nmod+1)
i=1
while(i<=_nt.k)
  j=1
  while(j<=_nt.i.k)
    'q w2xy '_ln.i.j.k' '_lt.i.j.k
###print    'q w2xy 'i' 'j' 'k' 'ln.i.j.k' '_lt.i.j.k
    _x.i.j.k=subwrd(result,3)
    _y.i.j.k=subwrd(result,6)
    _d.i.j.k=1
    j=j+1
  endwhile
  i=i+1
endwhile
  k=k+1
endwhile

*
*------------------ trkplt
*
function trkplt()

#
#	clip the area for draw commands to the plot area
#

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

rc=trkset()
k=0
if(_model = _models.1) ; k=2 ; endif
if(_model = _models.2) ; k=3 ; endif
if(_model = _models.3) ; k=4 ; endif

if(k=0) ; print 'improper model: '_model' '_models.1' '_models.2' '_models.3 ; 'quit' ; endif

#print 'before plotbt ...'
#'q pos'
rc=plotbt()
if(_dofcplot = 1)
  rc=plotfc(k)
endif


return


#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#  setup trk plot parms
#
#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

function trkset()

*
*	draw the initial positions as a working best track
*
col12='29 27 25 23 49 47 45 43 39 37 35 33 69 67 65 63'
col12='2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 2 3 4 5 6 7 8 9 10 11 12 13 14'
col12='2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 '
col12='2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 4 '
col12='2 1 3 4 8'
col12=col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12


#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
#  set up bt plotting parameters
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp

i=1
n12=0
while(i<=_nt.1)

  hh=substr(_dtg.i.1,9,2)

  btc=1
  btlc=12
  btc=btlc
  btls=1

  if(_hh = '00and12') 
    htest=(hh='12' | hh='00')
  endif

  if(_hh = '06and18')
    htest=(hh='06' | hh='18')
  endif

  if(htest)

    n12=n12+1
    btc=subwrd(col12,n12)
    bdtg=_dtg.i.1
    _tcl.bdtg=btc

    btsizmx=0.25
    btsizmn=0.15
    btsiz=btsizmx*( _mw.i.1.1/135)
    if(btsiz<btsizmn) ; btsiz=btsizmn ; endif
    btsym=41
    if(_mw.i.1.1 < 65) ; btsym=40 ; endif

    _btlgd.siz.n12=btsiz
    _btlgd.sym.n12=btsym
    _btlgd.col.n12=btc
    _btlgd.dtg.n12=bdtg
    _btlgd.mw.n12=_mw.i.1.1
    _btlgd.n=n12

  endif

  i=i+1

endwhile

return





#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# plot forecast track
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp

function plotfc(k)

_plotfe=1
didtmrk=1

i=1
while(i<=_nt.k)

  ip1=i+1
  bdtg=_dtg.i.k
  bdtg48=dtginc(bdtg,48)
  bdtg72=dtginc(bdtg,72)

#
#  find bt point
#

  n=1
  while(n<=_nt.1)
    if(_dtg.n.1 = bdtg48)
      lt48=_lt.n.1
      ln48=_ln.n.1
      n48=n
    endif
    if(_dtg.n.1 = bdtg72)
      lt72=_lt.n.1
      ln72=_ln.n.1
      n72=n
    endif
    n=n+1
  endwhile

#  print 'BBBBBBBBBBQQQQQQQQQQQ 'bdtg48' 'lt48' 'ln48' '_x.n48.1.1' '_y.n48.1.1
#  print 'ASDF222  i = 'i' bdtg = 'bdtg' k = 'k'  _nt.k '_nt.k' '_nt.i.k'  bdtg48 'bdtg48
#  'q pos'
  j=1
  fm=2
  sm=0.05
  cm=_tcl.bdtg
#
# new logic -- handle case where the fc tau inc is not constant, e.g., ofc
#

_plttaus='00 24 48 72 96 120'

jj=1
jt=1

#
# 20050322 - bug, forgot to initialize plttau
#
plttau=subwrd(_plttaus,1)

while(jj<=_nt.i.k)
  ctau=_tau.i.jj.k
  if(ctau = plttau)
    jtaus.jt=jj
    jt=jt+1
    plttau=subwrd(_plttaus,jt)
  endif
  jj=jj+1
endwhile


jts=jt-1

jjp1=jts+1
jtaus.jtp1=jtaus.jts

#jt=1
#while(jt<=jts)
#  print 'jjjjjjj_________ 'i' 'jtaus.jt
#  jt=jt+1
#endwhile

plttau=subwrd(_plttaus,1)


  jt=1
  while(jt<=jts)

    j=jtaus.jt
    jtp1=jt+1
    jjp1=jtaus.jtp1
    jp1=jjp1
    ctau=_tau.i.j.k

#  while(j<=_nt.i.k)
#    jp1=j+_jinc

    fm=2
    sm=0.05
    cm=_tcl.bdtg

    'set line 'cm' 3 4'

#print 'DDDDDDD i,j,k 'i' 'j' 'k' '_nt.i.k' 'ctau
   
    if(jp1<=_nt.i.k)
    'draw line '_x.i.j.k' '_y.i.j.k' '_x.i.jp1.k' '_y.i.jp1.k
    endif

    if(j=1)
      fm0=3
      sm0=0.075
      cm0=_tcl.bdtg
      fm=fm0
      sm=sm0
      cm=cm0
    endif

#    if(mod(j,2)=1 & j != 7 & ( jp1 != _nt.i.k ) & j>1 )
#      fm=3
#      sm=sm*1.25
#    endif

#-----------
#mark VERIFYING 72 hour position with bt colour; other wise use current colour
#-----------

    cm48=_tcl.bdtg48
    cm72=_tcl.bdtg72
    

#######    if(j=7) 


    if(_opt3 = '48veri')
      tauend=48
      cmend=cm48
      fmend=3
      smend=0.10
      nend=n48
    endif

    if(_opt3 = '72veri')
      tauend=72
      tauendp=120
      cmend=cm72
      fmend=3
      smend=0.10
      nend=n72
    endif

    if(ctau = tauend)

    if(cmend < 127)



      'set line 'cmend
      'draw mark 'fmend' '_x.i.j.k' '_y.i.j.k' 'smend

#
# 200503 draw line between 48(72) h verifying and forecast position
#
if(_plotfe=1 & _fe.i.j.k > 0)

#
# 20050425 - draw error rose and title with FE error
#

fehr=substr(_opt3,1,2)

x1=_x.i.j.k
x2=_x.nend.1.1
y1=_y.i.j.k
y2=_y.nend.1.1

fescl=0.50

fedx=1.0
fedy=1.0

fedx=fedx*fescl
fedy=fedy*fescl

feoff=0.25

x0=_xlplot+fedx
y0=_ytplot-fedy

x0=_xlplot+fedx+feoff
y0=_ybplot+fedy+feoff

#
# calculate diameter of circle according to PACOM error goals of 100 nm at 48 and 150 at 72 h
#

'q xy2w 'x0' 'y0
lon0=subwrd(result,3)
lat0=subwrd(result,6)
#####print 'ppppppppppppp 'result' 'lon0' 'lat0

if(fehr = 48); dlatcp=100.0/60.0 ; endif
if(fehr = 72); dlatcp=150.0/60.0 ; endif

latcp1=lat0+dlatcp
latcp2=lat0-dlatcp

'q w2xy 'lon0' 'latcp1
ycp1=subwrd(result,6)
####print 'ppppppppppp 'result' 'ycp1

'q w2xy 'lon0' 'latcp2
ycp2=subwrd(result,6)

dycp=ycp1-ycp2
####print 'ppppppppppp 'result' 'ycp2' 'dycp



#
# draw cross hair + CINCPAC goal for FE (circle)
#

if(didtmrk=1)
  crshrsiz=1.25
  crshrsiz=crshrsiz*fescl
  'set line 1'
  'draw mark 1 'x0' 'y0' 'crshrsiz
  'draw mark 2 'x0' 'y0' 'dycp*fescl
  didtmrk=0
endif

###print 'pppppppppppppppp 'x0' 'y0' 'fedx' 'fedy
dxa=x2-x1
dya=y2-y1

dxa=dxa*fescl
dya=dya*fescl

x1a=x0
x2a=x0-dxa
y1a=y0
y2a=y0-dya

'set line 'cmend' 1 16'
'draw line 'x1a' 'y1a' 'x2a' 'y2a

        'set line 'cmend' 1 16'
        'draw line 'x1' 'y1' 'x2' 'y2

#
# 20050425 - draw FE title
#

'set clip 0 '_pagex' 0 '_pagey

xtoff=0.15
ytoff=0.15

x1t=_xlplot+xtoff
y1t=_ytplot+ytoff

dxt=6.0
dyt=0.10
x1tb=x1t-xtoff
x2tb=x1tb+dxt
y1tb=y1t-dyt
y2tb=y1t+dyt

'set line 0'
'draw recf 'x1tb' 'y1tb' 'x2tb' 'y2tb

'set string 1 l 6'
'set strsiz 0.125'

if(_fe.i.j.k > 0)
fetle=_model' 'bdtg' 'fehr'-h FE:  '_fe.i.j.k' nm'
'draw string 'x1t' 'y1t' 'fetle
endif

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

####'q pos'

      endif

      'set line 0'
      sm=sm0*0.8
      'draw mark 'fm0' '_x.i.j.k' '_y.i.j.k' 'sm

      fm=fm0
      sm=sm0*0.5
      cm=cm0

     else

     'set line 'cm
      smend=sm0*1.15
     'draw mark 'fm0' '_x.i.j.k' '_y.i.j.k' 'smend

     endif


    endif

    'set line 'cm
    'draw mark 'fm' '_x.i.j.k' '_y.i.j.k' 'sm
    'draw mark 'fm' '_x.i.j.k' '_y.i.j.k' 'sm


####    j=j+_jinc
    jt=jt+1

  endwhile 

  if(j = _nt.i.k)
    if(j=2)
      fm=2
      sm=0.05
    endif
    'set line 'cm
    'draw mark 'fm' '_x.i.j.k' '_y.i.j.k' 'sm
    'draw mark 'fm' '_x.i.j.k' '_y.i.j.k' 'sm
  endif

#
# 200503 save tmp files for animated gif
#

  if(i<=9) ; plotcnt='0'i ; endif
  if(i>=10) ; plotcnt=i   ; endif
   pngpath='/tmp/tc.fc.'plotcnt'.png'
  'printim 'pngpath' x'_xsizepng' y'_ysizepng' white'

  i=i+1

endwhile

return


#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# plot BT
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp

function plotbt()

i=1
n12=0
while(i<=_nt.1)

  hh=substr(_dtg.i.1,9,2)
  btc=1
  btlc=12
  btc=btlc
  btls=1

  if(_hh = '00and12') 
    htest=(hh='12' | hh='00')
  endif

  if(_hh = '06and18') 
    htest=(hh='06' | hh='18')
  endif

  if(htest)
    n12=n12+1
    btsiz=_btlgd.siz.n12
    btsym=_btlgd.sym.n12
    btc=_btlgd.col.n12
    bdtg=_btlgd.dtg.n12
    'draw wxsym 'btsym' '_x.i.1.1' '_y.i.1.1' 'btsiz' 'btc' 6'
  else

    btsiz=0.050
    'set line 'btc
    if(hh='00') ; btsym=3 ; endif
    if(hh='06') ; btsym=2 ; endif
    if(hh='18') ; btsym=4 ; endif

    btsym=3
    'draw mark 'btsym' '_x.i.1.1' '_y.i.1.1' 'btsiz

  endif
  ip1=i+1 
  if(i != _nt.1)
    'set line 'btlc' 'btls' 6'
    'draw line '_x.i.1.1' '_y.i.1.1' '_x.ip1.1.1' '_y.ip1.1.1
  endif
  i=i+1
endwhile

return



*
*-------------------- utility script functions
*

*
*-------------------------- ofile ------------------
*
function ofile (fname)
'query files'
i = 0
while (1)  
  if (subwrd(result,1)='No')       
    ret = 0
    break;
  endif
  rec = sublin(result,i*3+2)
  if (rec='') 
    ret = 0;
    break; 
  endif
  if (subwrd(rec,2)=fname)
    rec = sublin(result,i*3+1)
    ret = subwrd(rec,2)
    break;
  endif
  i = i + 1
endwhile
if (ret=0) 
  'open 'fname
  if (rc>0) 
    say "Error opening "fname
    return (0)
  endif
  rec = sublin(result,2)
  ret = subwrd(rec,8)
endif
return (ret)
*
*-------------------------- strlen ------------------
*
function strlen(arg)

i=1
while(substr(arg,i,1) != '' & i<250)
  i=i+1
endwhile
return(i-1)

*
*-------------------------- mod ------------------
*
function mod(i0,inc)
  if(inc!=0)
    imod=int(i0/inc)
  else
    imod=int(i0/1)
  endif
  imod=i0-imod*inc
return(imod)

*
*-------------------------- int ------------------
*
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

*
*-------------------------- stitle ------------------
*
function stitle(t1,scale)

  rc=plotdims()
  dxs=_xlplot
  dyt=_pagey-_ytplot

  tsiz=0.15
  xoff=0.75
  yoff=0.10

  xs=_xlplot-xoff-tsiz/2
  xm=(_xlplot+_xrplot)/2
  ys=(_ybplot+_ytplot)/2

  if(scale != 'scale')
    tsiz = tsiz * scale
    xs=_xlplot-xoff-tsiz/2
  endif

  angle=90
  tt=tsiz+yoff

  if(tt < dyt) 
    xs=xm
    ys=_ytplot+yoff+tsiz/2 
    angle=0
  endif
  
  'set line 0 '
  x1b=_xlplot
  x2b=_xrplot
  y1b=_ytplot+yoff-tsiz*0.6
  y2b=y1b+tsiz+tsiz*0.6

  'draw recf 'x1b' 'y1b' 'x2b' 'y2b
  'set strsiz 'tsiz
  'set string 1 c 6 'angle
  'draw string 'xs' 'ys' 't1
  'set string 1 c 6 0'



return


*
*-------------------------- scrptle ------------------
*
function scrptle(scale,type)

  rc=plotdims()

  tsiz=0.06
  if(scale != 'scale')
    tsiz = tsiz * scale
  endif

  xoff=0.15
  yoff=0.06
  
  if(type != 'type') 

    xb=0

    if(type=top)
      yb=_pagey
      yoff=-yoff
    endif
 
    if(type=bottom)
      yb=0
    endif
   
     xe=_pagex
     ye=_pagey
  
     x1=xb+xoff
     y1=yb+yoff+tsiz/2

     x2=xe-xoff
     y2=y1

  else

    x1=_xlplot+xoff
    y1=_ybplot+yoff+tsiz/2

    x2=_xrplot-xoff
    y2=y1
  endif

  'set strsiz 'tsiz

  'set string 1 l 4' 
  'draw string 'x1' 'y1' '_script


return

*
*-------------------------- bottitle ------------------
*
function bottitle(t1,t2,scale,t1col,t2col)

  'q gxinfo'
  card=sublin(result,2)

  pagex=subwrd(card,4)
  pagey=subwrd(card,6)

  xr=pagex
  xl=0
  y1=0.22
  y2=0.08

  xoff=0.20
  yoff=0.06
  x2=xr-xoff

  xs=xl+(xr-xl)*0.5
*  xs=0.2


  tsiz=0.09
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif

  'set strsiz 'tsiz
  'set string 't1col' c 4'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 4'
    'draw string 'xs' 'y2' 't2
  endif

return

*
*-------------------------- plotdims ------------------
*

function plotdims()
*
*	get the dimensions of the plot
*
*	do a dummy plot go the dimension
*
  'q gxinfo'
  card=sublin(result,2)
  _pagex=subwrd(card,4)
  _pagey=subwrd(card,6)
  if(_pagex>_pagey) ; _orient='land' ; endif
  if(_pagey>_pagex) ; _orient='port' ; endif

  card=sublin(result,3)
  _xlplot=subwrd(card,4)
  _xrplot=subwrd(card,6)

  card=sublin(result,4)
  _ybplot=subwrd(card,4)
  _ytplot=subwrd(card,6)

return
*
*-------------------------- toptitle ------------------
*

function toptitle(t1,t2,scale,t1col,t2col)

  rc=plotdims()

  xr=_pagex
  xl=0
  y1=_pagey-0.15
  xs=(xr-xl)*0.5
  tsiz=0.15
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif
  if(t1col='') ; t1col=1 ; endif
  if(t2col='') ; t2col=1 ; endif
  t2siz=tsiz*0.85
  y2=_pagey-0.15-tsiz*1.5

  'set strsiz 'tsiz
  'set string 't1col' c 6'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 5'
    'set strsiz 't2siz
    'draw string 'xs' 'y2' 't2
  endif

return
*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------
function metadata(j,varo)

'set dfile 'j
'q file'

card=sublin(result,5)
_nx.j=subwrd(card,3)
_ny.j=subwrd(card,6)
_nz.j=subwrd(card,9)
_nt.j=subwrd(card,12)
card=sublin(result,6)
_nv.j=subwrd(card,5)

if(varo='y') 
  i=1
  while(i<=_nv.j)
    ii=6+i
    card=sublin(result,ii)
    _vr.i.j=subwrd(card,1)
    _nl.i.j=subwrd(card,2)
    _un.i.j=subwrd(card,3)
    bd=wrdpos(card,4)
say 'bd = 'bd' 'card
    _ds.i.j=substr(card,bd,120)
    i=i+1
  endwhile
endif

return


*-----------------------------------------------------------
*
*	function setup
*
*-----------------------------------------------------------
function setup(rcfg)
*
*	dtg global variables
*
_monamel='jan feb mar apr may jun jul aug sep oct nov dec'
_monameu='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
_monday='31 28 31 30 31 30 31 31 30 31 30 31'

return

function openfile()
*
*	open the files
*
nf=_cc.1
n=1
while(n<=nf)
  nn=n+1 
  _f.n=ofile(_cc.nn)
  if(_f.n=0) ; say 'unable to open '_cc.nn ; 'quit' ; endif
  n=n+1
endwhile

return(nn)


function plotarea(np,ppx,ppy,laydir,pytoff,pyboff,asymx,asymy)
*
*	switch the sense of the layout direction if portrait
*
if(_orient='port')
  if(laydir=1)
    laydir=0 
  else
    laydir=1
  endif
endif

dpagex=_pagex
dpagey=_pagey-(pytoff+pyboff)

nbl1="1 2 3 2 2 2 2 2 2 2 3 3"
nbl0="1 1 1 2 3 3 4 4 5 5 4 4"

npx=subwrd(nbl1,np)
npy=subwrd(nbl0,np)

if(laydir=0)
  npx=subwrd(nbl0,np)
  npy=subwrd(nbl1,np)
endif

dpx=dpagex/npx
dpy=dpagey/npy
dxb=(1.0-ppx)*dpx
dyb=(1.0-ppy)*dpy

l=1
j=npy
while(j>=1)

  y0=pyboff+(j-1)*dpy
  y1=pyboff+j*dpy

  i=1
  while(i<=npx & l<=np)

    if(i=1)
      x0=0
      x1=dpagex*asymx
     _xpl.l=x0+dxb*1.25
if(_opt1 = '2plot') 
     _xpl.l=x0+dxb*0.5
endif
     _xpr.l=x1-dxb*0.5

    endif

    if(i=2) 
      x0=x1
      x1=x0+dpagex*(1-asymx)
      _xpl.l=x0+dxb*0.75
      _xpr.l=x1-dxb*0.5
    endif

    _ypt.l=y1-dyb
    _ypb.l=y0+dyb

    i=i+1
    l=l+1
  endwhile
  j=j-1
endwhile

return

function linelgd(nm,dxoff,xlsft,xlsz,yln,ylg,dyl)
xlen=_pagex-2*dxoff
ylg=yln+dyl
dx=xlen/nm
xloff=(dx-xlsz*dx)*0.5-xlsft
j=1
while(j<=nm)
  xb=dxoff+(j-1)*dx+xloff
  xe=xb+xlsz*dx
  xm=(xb+xe)*0.5

  'set line '_lc.j' '_ls.j' '_lt.j
  'draw line 'xb' 'yln' 'xe' 'yln
  'set string 1 bc 6'
  'set strsiz 0.125'
  'draw string  'xm' 'ylg' '_s.j
  j=j+1
endwhile



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
*
*	different output format?
*
  if(subwrd(dum,3)="Window" & subwrd(dum,4) = "id:") 
    _winid=subwrd(dum,5)
    gotid=1
    break
  endif

  if(subwrd(dum,2)="Window" & subwrd(dum,3) = "id:") 
    _winid=subwrd(dum,4)
    gotid=1
    break
  endif

endwhile
rc=close(wininfo)
'!rm wininfo'
return(gotid)

*
*-------------------------- abs ------------------
*
function abs(i0)
  siz=strlen(i0)
  if(substr(i0,1,1)='-') 
    iabs=substr(i0,2,siz)
  else
    iabs=i0
  endif
return(iabs)

*
*-------------------------- nint ------------------
*
function nint(i0)
  i0=i0+0.5
  i=0
  while(i<12)
    i=i+1
    if(substr(i0,i,1)='.')
      i0=substr(i0,1,i-1)
      break
    endif
  endwhile
return(i0)


*
*-------------------------- mod ------------------
*
function mod(i0,inc)
  if(inc!=0)
    imod=int(i0/inc)
  else
    imod=int(i0/1)
  endif
  imod=i0-imod*inc
return(imod)

*
*-------------------------- int ------------------
*
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

*
*-------------------------- plotdims ------------------
*

function plotdims()
*
*	get the dimensions of the plot
*
*	do a dummy plot go the dimension
*
  'q gxinfo'
  card=sublin(result,2)
  _pagex=subwrd(card,4)
  _pagey=subwrd(card,6)

  card=sublin(result,3)
  _xlplot=subwrd(card,4)
  _xrplot=subwrd(card,6)

  card=sublin(result,4)
  _ybplot=subwrd(card,4)
  _ytplot=subwrd(card,6)

return

*
*-------------------------- nint ------------------
*
function nint(i0)
  i0=i0+0.5
  i=0
  while(i<12)
    i=i+1
    if(substr(i0,i,1)='.')
      i0=substr(i0,1,i-1)
      break
    endif
  endwhile
return(i0)

*
*-------------------------- curdtgh ------------------
*
function curdtgh(ctime)
*
*  convert current time to dtg 
*
  iyr=substr(ctime,11,2)
  nmo=substr(ctime,6,3)
  ida=substr(ctime,4,2)
  ihr=substr(ctime,1,2)
  i=1
  while (nmo!=subwrd(_monameu,i));i=i+1;endwhile
  imo=i
  if(imo < 10); imo='0'imo; endif
  if(ihr = 0); ihr='00';endif
  if(ihr < 10 & ihr != '00'); ihr='0'ihr; endif

  idtg=iyr%imo%ida%ihr

return (idtg)
*
*-------------------------- dtghcur ------------------
*
function dtghcur(dtgh)
*
*  convert FNMOC DTG to GrADS time
*
  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
  nmo=subwrd(_monamel,imo)
  imo=i
return (ihr%'Z'ida%nmo%iyr)

function tcstat(nvtype,nbasin,nstorm,dtg)

fo=ofile(_vpath)
if(fo = 0) ; 'quit' ;endif

if(nvtype = 2) ; nstorm=nstorm+30 ; endif
'set dfile 'fo
'set x 6'
'set y 'nstorm
'set z 'nbasin

ntmax=0

t=1
te=4
while(t<=te) 
  'set t 't
  'd const(i(x=1),0,-u)'
  nti=subwrd(result,4)
  if(nti > ntmax) ; ntmax=nti ; endif
  t=t+1
endwhile

return(ntmax' 'fo)

function trkpstat(nbasin,nvtype)

#
#  dim env already set up
#
#'set dfile 'fo
#'set x 6'
#'set y 'nstorm
#'set z 'nbasin

ntmax=0
mwmax=0
femax=0
lsiz=0.125
lsiz=0.1

t=1
te=4
while(t<=te) 
  'set t 't
  'd const(i(x=1),0,-u)'
  nti=subwrd(result,4)
  if(nti > ntmax) ; ntmax=nti ; endif
  print 'nti 't' 'nti.t
  'd const(i(x=5),0,-u)'
  mwi=subwrd(result,4)
  if(mwi > mwmax) ; mwmax=mwi ; endif
  'd const(n(x=5),0,-u)'
  mwn=subwrd(result,4)
  if(mwn > mwmax) ; mwmax=mwn ; endif

  'd const(i(x=6),0,-u)'
  fei=subwrd(result,4)
  if(fei > femax) ; femax=fei ; endif
  'd const(n(x=6),0,-u)'
  fen=subwrd(result,4)
  if(fen > femax) ; femax=fen ; endif

  t=t+1
endwhile

'set warn off'
print 'femax = 'femax
print 'mwmax = 'mwmax
print 'ntmax = 'ntmax

feinc=100
femax=(int(femax/feinc)+1)*feinc
mwinc=10
mwmax=(int(mwmax/mwinc)+1)*mwinc
ntinc=2
ntmax=(int(ntmax/ntinc)+1)*ntinc

print 'femax = 'femax
print 'mwmax = 'mwmax
print 'ntmax = 'ntmax

'set t 1 last'

'pmi=((i(x=1)-i(x=2))/(i(x=1)))*100'
'pmn=((n(x=1)-n(x=2))/(n(x=1)))*100'

'set mproj off'
'set mpdraw off'
'set gxout bar'
'set bargap 50'
'set ccolor 3'
'set t 0.5 'te'.5'
'set vrange 0 'femax
'set yaxis 0 'femax' 'feinc
'set ylopts 1 4 'lsiz
'set xlopts 1 5 'lsiz
if(te=4)
'set xaxis -12 84 24'
'set xlabs  0h | 24h | 48h | 72h '
endif

if(te=6)
'set xaxis -12 132 24'
'set xlabs  0h | 24h | 48h | 72h | 96h | 120h '
endif

'd i'
'set bargap 75'
'set ccolor 4'
'd n'
'set ccolor 0'
'set cthick 10' 
'set baropts outline'
'd n'

rc=plotdims()

if(nbasin = 1)
  bname='LANT'
endif

if(nbasin = 2)
  bname='EASTPAC'
endif

if(nbasin = 3)
  bname='WESTPAC'
endif

if(nvtype = 1)
  vname='HETERO'
endif

if(nvtype = 2)
  vname='HOMO'
endif

t1=vname
rc=stitle(t1,0.5)

xyl=_xlplot-0.3
yyl=_ytplot+0.2
'set string 1 l 5'
'set strsiz 'lsiz
'draw string 'xyl' 'yyl' FE (nm)'

xyl=_xlplot-0.45

'set string 1 c 5'
'set strsiz 'lsiz
'draw string 'xyl' 'yyl' N '

xyl=_xrplot+0.2

'set string 1 r 5'
'set strsiz 'lsiz
'draw string 'xyl' 'yyl' V`bmax`n (kts)'


'set gxout line'
'set ylpos 0 r'
'set ylopts 1 4 'lsiz
'set xlopts 1 4 'lsiz
'set vrange 0 'mwmax
'set yaxis 0 'mwmax' 'mwinc
'set grid off'

'set ccolor 0'
'set cthick 15'
'set ylopts 1 4 'lsiz
'set xlopts 1 4 'lsiz
'd i(x=5)'
'set ccolor 3'
'set cthick 4'
'd i(x=5)'

'set ccolor 0'
'set cthick 15'
'set ylopts 1 4 'lsiz
'set xlopts 1 4 'lsiz
'd n(x=5)'
'set ccolor 4'
'set cthick 4'
'd n(x=5)'

'set ylpos -0.40 l'
'set vrange 0 'ntmax
'set ylopts 1 4 'lsiz
'set yaxis 0 'ntmax' 'ntinc
'set grid off'

'set baropts fill'
'set bargap 90'
'set gxout errbar'

'set ccolor 0'
'set cthick 15'
'd i(x=1);i(x=2)'
'set ccolor 3'
'set cthick 6'
'd i(x=1);i(x=2)'

'set ccolor 0'
'set cthick 15'
'd n(x=1);n(x=2)'
'set ccolor 2'
'set cthick 6'
'd n(x=1);n(x=2)'

'set ccolor 0'
'set cthick 15'
'd n(x=1);n(x=1)'
'set ccolor 1'
'set cthick 6'
'd n(x=1);n(x=1)'


return

*
*-------------------- utility script functions
*

*
*-------------------------- ofile ------------------
*
function ofile (fname)
'query files'
i = 0
while (1)  
  if (subwrd(result,1)='No')       
    ret = 0
    break;
  endif
  rec = sublin(result,i*3+2)
  if (rec='') 
    ret = 0;
    break; 
  endif
  if (subwrd(rec,2)=fname)
    rec = sublin(result,i*3+1)
    ret = subwrd(rec,2)
    break;
  endif
  i = i + 1
endwhile
if (ret=0) 
  'open 'fname
  if (rc>0) 
    say "Error opening "fname
    return (0)
  endif
  rec = sublin(result,2)
  ret = subwrd(rec,8)
endif
return (ret)
*
*-------------------------- strlen ------------------
*
function strlen(arg)

i=1
while(substr(arg,i,1) != '' & i<250)
  i=i+1
endwhile
return(i-1)

*
*-------------------------- mod ------------------
*
function mod(i0,inc)
  if(inc!=0)
    imod=int(i0/inc)
  else
    imod=int(i0/1)
  endif
  imod=i0-imod*inc
return(imod)

*
*-------------------------- int ------------------
*
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

*
*-------------------------- stitle ------------------
*
function stitle(t1,scale)

  rc=plotdims()

  dxs=_xlplot
  dyt=_pagey-_ytplot

  tsiz=0.15
  xoff=0.75
  yoff=0.10

  xs=_xlplot-xoff-tsiz/2
  xm=(_xlplot+_xrplot)/2
  ys=(_ybplot+_ytplot)/2

  if(scale != 'scale')
    tsiz = tsiz * scale
    xs=_xlplot-xoff-tsiz/2
  endif

  angle=90
  tt=tsiz+yoff

  if(tt < dyt) 
    xs=xm
    ys=_ytplot+yoff+tsiz/2 
    angle=0
  endif
  
  'set line 0 '
  x1b=_xlplot
  x2b=_xrplot
  y1b=_ytplot+yoff-tsiz*0.6
  y2b=y1b+tsiz+tsiz*0.6

  'draw recf 'x1b' 'y1b' 'x2b' 'y2b
  'set strsiz 'tsiz
  'set string 1 c 6 'angle
  'draw string 'xs' 'ys' 't1
  'set string 1 c 6 0'



return

*
*-------------------------- scrptle ------------------
*
function scrptle(scale)
 
  rc=plotdims()
  '!dtg > dtg.cur'
  rc=read(dtg.cur)
  dtg=sublin(rc,2)
  rc=close(dtg.cur)

  tsiz=0.06
  if(scale != 'scale')
    tsiz = tsiz * scale
  endif

  dx1=_pagex

  xoff=0.15
  yoff=0.06

  x1=xoff
  y1=yoff+tsiz/2

  x2=_pagex-xoff
  y2=y1

  x3=_pagex/2
  y3=y1

  'set strsiz 'tsiz
  'set string 1 l 4' 
  'draw string 'x1' 'y1' GrADS Script: '_script
  'set strsiz 'tsiz
  'set string 1 r 4' 
  'draw string 'x2' 'y2' 'dtg
  'set string 1 c 4 0'
  'draw string 'x3' 'y3' PCMDI (M. Fiorino)'

return

*
*-------------------------- plotdims ------------------
*

function plotdims()
*
*	get the dimensions of the plot
*
*	do a dummy plot go the dimension
*
  'q gxinfo'
  card=sublin(result,2)
  _pagex=subwrd(card,4)
  _pagey=subwrd(card,6)
  if(_pagex>_pagey) ; _orient='land' ; endif
  if(_pagey>_pagex) ; _orient='port' ; endif

  card=sublin(result,3)
  _xlplot=subwrd(card,4)
  _xrplot=subwrd(card,6)

  card=sublin(result,4)
  _ybplot=subwrd(card,4)
  _ytplot=subwrd(card,6)

return
*
*-------------------------- toptitle ------------------
*

function toptitle(t1,t2,scale,t1col,t2col)

  rc=plotdims()

  xr=_pagex
  xl=0
  y1=_pagey-0.15
  y2=_pagey-0.35
  xs=(xr-xl)*0.5
  tsiz=0.15
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif
  if(t1col='') ; t1col=1 ; endif
  if(t2col='') ; t2col=1 ; endif

  'set strsiz 'tsiz
  'set string 't1col' c 6'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 5'
    'set strsiz 0.10'
    'draw string 'xs' 'y2' 't2
  endif

return
*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------
function metadata(j,varo)

'set dfile 'j
'q file'

card=sublin(result,5)
_nx.j=subwrd(card,3)
_ny.j=subwrd(card,6)
_nz.j=subwrd(card,9)
_nt.j=subwrd(card,12)
card=sublin(result,6)
_nv.j=subwrd(card,5)

if(varo='y') 
  i=1
  while(i<=_nv.j)
    ii=6+i
    card=sublin(result,ii)
    _vr.i.j=subwrd(card,1)
    _nl.i.j=subwrd(card,2)
    _un.i.j=subwrd(card,3)
    bd=wrdpos(card,4)
say 'bd = 'bd' 'card
    _ds.i.j=substr(card,bd,120)
    i=i+1
  endwhile
endif

return

*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------

function cbarn (args,lab,labstr)
*
*  Script to plot a colorbar
*
*  The script will assume a colorbar is wanted even if there is 
*  not room -- it will plot on the side or the bottom if there is
*  room in either place, otherwise it will plot along the bottom and
*  overlay labels there if any.  This can be dealt with via 
*  the 'set parea' command.  In version 2 the default parea will
*  be changed, but we want to guarantee upward compatibility in
*  sub-releases.
*
*
*	modifications by mike fiorino 940614
*
*	- the extreme colors are plotted as triangles
*	- the colors are boxed in white
*	- input arguments in during a run execution:
* 
*	run cbarn sf vert xmid ymid
*
*	sf   - scale the whole bar 1.0 = original 0.5 half the size, etc.
*	vert - 0 FORCES a horizontal bar = 1 a vertical bar
*	xmid - the x position on the virtual page the center the bar
*	ymid - the x position on the virtual page the center the bar
*
*	if vert,xmid,ymid are not specified, they are selected
*	as in the original algorithm
*  


sf=subwrd(args,1)
vert=subwrd(args,2)
xmid=subwrd(args,3)
ymid=subwrd(args,4)
force=subwrd(args,5)
if(sf='');sf=1.0;endif


*
*  Check shading information
*
  
  if(force!='y') 
    'query shades'
    shdinfo = result
    if (subwrd(shdinfo,1)='None') 
     say 'Cannot plot color bar: No shading information'
     return
    endif
  else
    if (subwrd(_shdinfo.1,1)='None') 
     say 'Cannot plot color bar: No shading information'
     return
    endif
  endif
* 
*  Get plot size info
*
  'query gxinfo'
  rec2 = sublin(result,2)
  rec3 = sublin(result,3)
  rec4 = sublin(result,4)
  xsiz = subwrd(rec2,4)
  ysiz = subwrd(rec2,6)
  ylo = subwrd(rec4,4)
  xhi = subwrd(rec3,6)
  xd = xsiz - xhi

  ylolim=0.6*sf
  xdlim1=1.0*sf
  xdlim2=1.5*sf  
  barsf=0.8*sf
  yoffset=0.2*sf
  stroff=0.05*sf
  strxsiz=0.11*sf
  strysiz=0.12*sf
*
*  Decide if horizontal or vertical color bar
*  and set up constants.
*
  if (ylo<ylolim & xd<xdlim1) 
    say "Not enough room in plot for a colorbar"
    return
  endif

  if(force=y) 
    cnum = subwrd(_shdinfo.1,5)
  else
    cnum = subwrd(shdinfo,5)
  endif

*
*	logic for setting the bar orientation with user overides
*
  if (ylo<ylolim | xd>xdlim1)
    vchk = 1
    if(vert = 0) ; vchk = 0 ; endif
  else
    vchk = 0
    if(vert = 1) ; vchk = 1 ; endif
  endif
*
*	vertical bar
*

  if (vchk = 1 )

    if(xmid = '') ; xmid = xhi+xd/2 ; endif
    xwid = 0.2*sf
    ywid = 0.5*sf
    
    xl = xmid-xwid/2
    xr = xl + xwid
    if (ywid*cnum > ysiz*barsf) 
      ywid = ysiz*barsf/cnum
    endif
    if(ymid = '') ; ymid = ysiz/2 ; endif
    yb = ymid - ywid*cnum/2
    'set string 1 l 5'
    vert = 1

  else

*
*	horizontal bar
*

    ywid = 0.4
    xwid = 0.8

    if(ymid = '') ; ymid = ylo/2-ywid/2 ; endif
    yt = ymid + yoffset
    yb = ymid
    if(xmid = '') ; xmid = xsiz/2 ; endif
    if (xwid*cnum > xsiz*barsf)
      xwid = xsiz*barsf/cnum
    endif
    xl = xmid - xwid*cnum/2
    'set string 1 tc 5'
    vert = 0
  endif


*
*  Plot colorbar
*


  'set strsiz 'strxsiz' 'strysiz
  num = 0
  while (num<cnum) 

    if(force = y)
      ii=num+2 
      rec=_shdinfo.ii
      col = subwrd(rec,1)
      hi = subwrd(rec,3)
    else
      rec = sublin(shdinfo,num+2)
      col = subwrd(rec,1)
      hi = subwrd(rec,3)
    endif
    if (vert) 
      yt = yb + ywid
    else 
      xr = xl + xwid
    endif

    if(num!=0 & num!= cnum-1)
    'set line 1 1 10'
    'draw rec 'xl' 'yb' 'xr' 'yt
    'set line 'col
    'draw recf 'xl' 'yb' 'xr' 'yt
    if (num<cnum-1)
      if (vert) 
        xp=xr+stroff
        'draw string 'xp' 'yt' 'hi
      else
        yp=yb-stroff
        'draw string 'xr' 'yp' 'hi
      endif
    endif
    endif

    if(num = 0 )

      if(vert = 1)

        xm=(xl+xr)*0.5
        'set line 1 1 10'
        'draw line 'xl' 'yt' 'xm' 'yb
        'draw line 'xm' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'yt

        'set line 'col
        'draw polyf 'xl' 'yt' 'xm' 'yb' 'xr' 'yt' 'xl' 'yt

      else

        xm=(xl+xr)*0.5
        ym=(yb+yt)*0.5
        'set line 1 1 10'
        'draw line 'xl' 'ym' 'xr' 'yb
        'draw line 'xr' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'ym

        'set line 'col
       'draw polyf 'xl' 'ym' 'xr' 'yb' 'xr' 'yt' 'xl' 'ym

      endif

    endif

    if (num<cnum-1)
      if (vert)
         xp=xr+stroff 
        'draw string 'xp' 'yt' 'hi
      else
         yp=yb-stroff
        'draw string 'xr' 'yp' 'hi
      endif
    endif

    if(num = cnum-1 )

      if( vert = 1)
        'set line 1 1 10'
        'draw line 'xl' 'yb' 'xm' 'yt
        'draw line 'xm' 'yt' 'xr' 'yb
        'draw line 'xr' 'yb' 'xl' 'yb

        'set line 'col
        'draw polyf 'xl' 'yb' 'xm' 'yt' 'xr' 'yb' 'xl' 'yb
        if(lab=y) 
          ylb=yt+0.25
          strxsizl=strxsiz*1.75
          strysizl=strysiz*1.75
          'set string 1 c 6'
          'set strsiz 'strxsizl' 'strysizl
          'draw string 'xm' 'ylb' 'labstr
          'set string 1 tc 5'
        endif
      else

        'set line 1 1 10'
        'draw line 'xr' 'ym' 'xl' 'yb
        'draw line 'xl' 'yb' 'xl' 'yt
        'draw line 'xl' 'yt' 'xr' 'ym

        'set line 'col
        'draw polyf 'xr' 'ym' 'xl' 'yb' 'xl' 'yt' 'xr' 'ym
        if(lab=y) 
          ylb=yt+0.15
          strxsizl=strxsiz*2.0
          strysizl=strysiz*2.0
          'set string 1 c 6'
          'set strsiz 'strxsizl' 'strysizl
          'draw string 'xmid' 'ylb' 'labstr
          'set string 1 tc 5'
        endif

      endif

    endif

    if (num<cnum-1)
      if (vert) 
        xp=xr+stroff
        'draw string 'xp' 'yt' 'hi
      else
        yp=yb-stroff
       'draw string 'xr' 'yp' 'hi
      endif
    endif

    num = num + 1
    if (vert); yb = yt;
    else; xl = xr; endif;
  endwhile
return

*----------------------------------------------------------
*
*	jaecol
*
*	color table by Jae Schemm of CPC, NCEP
*
*----------------------------------------------------------

function jaecol()

*light yellow to dark red
'set rgb 21 255 250 170'
'set rgb 22 255 232 120'
'set rgb 23 255 192  60'
'set rgb 24 255 160   0'
'set rgb 25 255  96   0'
'set rgb 26 255  50   0'
'set rgb 27 225  20   0'
'set rgb 28 192   0   0'
'set rgb 29 165   0   0'
*
*light green to dark green
'set rgb 31 230 255 225'
'set rgb 32 200 255 190'
'set rgb 33 180 250 170'
'set rgb 34 150 245 140'
'set rgb 35 120 245 115'
'set rgb 36  80 240  80'
'set rgb 37  55 210  60'
'set rgb 38  30 180  30'
'set rgb 39  15 160  15'
*set rgb 39   5 150   5
*
*light blue to dark blue
'set rgb 41 200 255 255'
'set rgb 42 175 240 255'
'set rgb 43 130 210 255'
'set rgb 44  95 190 250'
'set rgb 45  75 180 240'
'set rgb 46  60 170 230'
'set rgb 47  40 150 210'
'set rgb 48  30 140 200'
'set rgb 49  20 130 190'
*
*light purple to dark purple
'set rgb 51 220 220 255'
'set rgb 52 192 180 255'
'set rgb 53 160 140 255'
'set rgb 54 128 112 235'
'set rgb 55 112  96 220'   
'set rgb 56  72  60 200'   
'set rgb 57  60  40 180'
'set rgb 58  45  30 165'
'set rgb 59  40   0 160'
*
*light pink to dark rose  
'set rgb 61 255 230 230'
'set rgb 62 255 200 200'
'set rgb 63 248 160 160'
'set rgb 64 230 140 140'
'set rgb 65 230 112 112'
'set rgb 66 230  80  80'   
'set rgb 67 200  60  60'   
'set rgb 68 180  40  40'
'set rgb 69 164  32  32'
*
* black to light grey
'set rgb 71 250 250 250'
'set rgb 72 225 225 225'
'set rgb 73 200 200 200'
'set rgb 74 180 180 180'
'set rgb 75 160 160 160'
'set rgb 76 150 150 150'
'set rgb 77 140 140 140'
'set rgb 78 124 124 124'
'set rgb 79 112 112 112'
'set rgb 80  92  92  92'
'set rgb 81  80  80  80'   
'set rgb 82  70  70  70'   
'set rgb 83  60  60  60'   
'set rgb 84  50  50  50'   
'set rgb 85  40  40  40'
'set rgb 86  36  36  36'
'set rgb 87  32  32  32'

return
*
*-------------------------- curdtgh ------------------
*
function curdtgh(ctime)
*
*  convert current time to dtg 
*
  iyr=substr(ctime,11,2)
  nmo=substr(ctime,6,3)
  ida=substr(ctime,4,2)
  ihr=substr(ctime,1,2)
  i=1
  while (nmo!=subwrd(_monameu,i));i=i+1;endwhile
  imo=i
  if(imo < 10); imo='0'imo; endif
  if(ihr = 0); ihr='00';endif
  if(ihr < 10 & ihr != '00'); ihr='0'ihr; endif

  idtg=iyr%imo%ida%ihr

return (idtg)
*
*-------------------------- dtghcur ------------------
*
function dtghcur(dtgh)
*
*  convert FNMOC DTG to GrADS time
*
  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
  nmo=subwrd(_monamel,imo)
  imo=i
return (ihr%'Z'ida%nmo%iyr)


function efscol(cmap)

if(cmap=efs_1)
'set rgb 20    0  29  29'
'set rgb 21    0  49  49'
'set rgb 22    0  69  69'
'set rgb 23    0  89  89'
'set rgb 24    0 109 109'
'set rgb 25    0 129 129'
'set rgb 26    0 149 149'
'set rgb 27    0 169 169'
'set rgb 28    0 189 189'
'set rgb 29    0 209 209'
'set rgb 30    0 229 229'
'set rgb 31    0 249 249'
'set rgb 32    0 209 255'
'set rgb 33    0 169 255'
'set rgb 34    0 129 255'
'set rgb 35    0  89 255'
'set rgb 36    0  49 255'
'set rgb 37   49   0 255'
'set rgb 38   89   0 255'
'set rgb 39  109   0 255'
'set rgb 40  149   0 255'
'set rgb 41  189   0 255'
'set rgb 42  209   0 255'
'set rgb 43  249   0 255'
'set rgb 44  255   0 209'
'set rgb 45  255   0 169'
'set rgb 46  255   0 129'
'set rgb 47  255   0  89'
'set rgb 48  255   0  49'

endif

if(cmap='efs_2')
'set rgb 20  99   0  99'
'set rgb 21 159   0 159'
'set rgb 22 255   0 255'
'set rgb 23 205   0 255'
'set rgb 24 169   0 255'
'set rgb 25  99   0 255'
'set rgb 26   0   0 255'
'set rgb 27   0  79 255'
'set rgb 28   0 192 255'
'set rgb 29   0 255 255'
'set rgb 30   0 255 205'
'set rgb 31   0 255 179'
'set rgb 32   0 255  79'
'set rgb 33   0 255   0'
'set rgb 34 165 255   0'
'set rgb 35 205 255   0'
'set rgb 36 255 255   0'
'set rgb 37 255 205   0'
'set rgb 38 255 154   0'
'set rgb 39 255 102   0'
'set rgb 40 255   0   0'
'set rgb 41 205   0   0'
'set rgb 42 165   0   0'
endif

if(cmap='efs_3')

'set rgb 20   0   0   0'
'set rgb 21   0  55  55'
'set rgb 22   0  65  65'
'set rgb 23   0  75  75'
'set rgb 24   0  85  85'
'set rgb 25   0  95  95'
'set rgb 26   0 105 105'
'set rgb 27   0 115 115'
'set rgb 28   0 125 125'
'set rgb 29   0 135 135'
'set rgb 30   0 145 145'
'set rgb 31   0 155 155'
'set rgb 32   0 165 165'
'set rgb 33   0 175 175'
'set rgb 34   0 185 185'
'set rgb 35   0 195 195'
'set rgb 36   0 205 205'
'set rgb 37   0 215 215'
'set rgb 38   0 225 225'
'set rgb 39   0 235 235'
'set rgb 40   0 245 245'
'set rgb 41 255 255 255'
'set rgb 42 255 255 255'

endif

if(cmap=efs_4)
'set rgb 50   0 100   0'
'set rgb 51   0 120   0'
'set rgb 52   0 140   0'
'set rgb 53   0 160   0'
'set rgb 54   0 180   0'
'set rgb 55   0 200   0'
'set rgb 56   0 220   0'
'set rgb 57   0 230   0'
'set rgb 58   0 240   0'
'set rgb 59   0 255   0'
'set rgb 60  85 255   0'
'set rgb 61 125 255   0'
'set rgb 62 165 255   0'
'set rgb 63 205 255   0'
'set rgb 64 255 225   0'
'set rgb 65 255 205   0'
'set rgb 66 225 185   0'
'set rgb 67 205 165   0'
'set rgb 68 185 120   0'
'set rgb 69 165 120   0'
'set rgb 70 145 100   0'
'set rgb 71  85  45   0'
'set rgb 72   0   0  55'
endif

return


*-----------------------------------------------------------
*
*	function setup
*
*-----------------------------------------------------------
function setup(rcfg)
*
*	dtg global variables
*
_monamel='jan feb mar apr may jun jul aug sep oct nov dec'
_monameu='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
_monday='31 28 31 30 31 30 31 31 30 31 30 31'

if(rcfg='y')
*
*	ensemble name cfg
*
ecfg='g.generic.cfg'
iok=0
i=0
imax=1000
while(1)
  rc=read(ecfg)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  if(iok != 0 & i = 0) 
    say 'Unable to read configuration file!!!'
    say 'BYE'
    'quit'
  endif
  if(iok=2) ; _ne=i ; break ; endif
  i=i+1
  _en.i=subwrd(card,1)
  if(i=imax) ; break ; endif
endwhile

endif

return


function plotarea(np,pp,laydir,pytoff,pyboff)
*
*	switch the sense of the layout direction if portrait
*
if(_orient='port')
  if(laydir=1)
    laydir=0 
  else
    laydir=1
  endif
endif

dpagex=_pagex
dpagey=_pagey-(pytoff+pyboff)

nbl1="1 2 3 2 2 2 2 2 2 2 3 3"
nbl0="1 1 1 2 3 3 4 4 5 5 4 4"

npx=subwrd(nbl1,np)
npy=subwrd(nbl0,np)

if(laydir=0)
  npx=subwrd(nbl0,np)
  npy=subwrd(nbl1,np)
endif

dpx=dpagex/npx
dpy=dpagey/npy
dxb=(1.0-pp)*dpx*0.5
dyb=(1.0-pp)*dpy*0.5
say 'qqq kk = 'np' 'npx' 'npy' 'dpx' 'dpy' 'dxb' 'dyb

l=1
j=npy
while(j>=1)

  y0=pyboff+(j-1)*dpy
  y1=pyboff+j*dpy

  i=1
  while(i<=npx & l<=np)
    x0=(i-1)*dpx
    x1=i*dpx

    _xpl.l=x0+dxb
    _xpr.l=x1-dxb
    _ypt.l=y1-dyb
    _ypb.l=y0+dyb

    i=i+1
    l=l+1
  endwhile
  j=j-1
endwhile

return

function linelgd(nm,dxoff,xlsft,xlsz,yln,ylg,dyl)
xlen=_pagex-2*dxoff
ylg=yln+dyl
dx=xlen/nm
xloff=(dx-xlsz*dx)*0.5-xlsft
j=1
while(j<=nm)
  xb=dxoff+(j-1)*dx+xloff
  xe=xb+xlsz*dx
  xm=(xb+xe)*0.5

  'set line '_lc.j' '_ls.j' '_lt.j
  'draw line 'xb' 'yln' 'xe' 'yln

  'set string 1 bc 6'
  'set strsiz 0.125'
  'draw string  'xm' 'ylg' '_s.j
  j=j+1
endwhile



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
*
*	different output format?
*
  if(subwrd(dum,3)="Window" & subwrd(dum,4) = "id:") 
    _winid=subwrd(dum,5)
    gotid=1
    break
  endif

  if(subwrd(dum,2)="Window" & subwrd(dum,3) = "id:") 
    _winid=subwrd(dum,4)
    gotid=1
    break
  endif

endwhile
rc=close(wininfo)
'!rm wininfo'
return(gotid)


