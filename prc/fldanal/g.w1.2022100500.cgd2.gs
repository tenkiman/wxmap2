function main(args)

rc=gsfallow('on')
rc=const()

*************************************************
*
* main function driver for plotting function gwxmap
*  
**************************************************

_verb=0
_newtcfc=0
_fnf=-999
_fnfp=-999
_dotc=1
      
# -- get grads version
#
'q config'
card=sublin(result,2)
version=subwrd(card,8)
_version=substr(version,1,3)


*	read the configuration file
*
rc=loadcfg()

#print 'NNNNNNNNNNNNNNNNNNNNNNNN _nrun:     '_nrun

_areadone='n'
_gravity=9.80665
_doeclogo=0
_test=0
_dobg=1
_dobasemap=0

if(_specopt = 'basemap')
   _dobg=0
endif

_combinecmd='/usr/local/grads/bin/combine'
_combinecmd='/home/fiorino/grads/bin/combine'

_cdelay=150


if(_specopt = 'test') ; _test=1 ; _dobg=0 ; endif

#
#  get xinfo
#

'q xinfo'
card=sublin(result,4)
_xsize=subwrd(card,4)
card=sublin(result,5)
_ysize=subwrd(card,4)

# 
#  tcsetup
#
if(_specopt != 'basemap' & _dotc = 1)
  rc=tcsetup()
endif

irun=1
while(irun<=_nrun)
  args=_args.irun  
  if(_verb=1)
  print 'irun = 'irun' 'args
  endif

  rc=gwxmap(args)
  irun=irun+1
  if(_test = 1) ; irun=9999 ;endif

endwhile

if(_interact = 1) ; 'q pos' ; endif

if((rc = 0 | rc = 2 | rc = 99)  & _test = 0) ; 'quit' ; endif

return



*************************************************
*
*	plotting function gwxmap 
*	same as g.wxmap.gs
*  
**************************************************

function gwxmap (args)

'c'
_script='g.wxmap.gs 'args
_grfprcdef='gif'
_grfprcdef='wi'
_grfprcdef='printim'
_grfprcdef='gxyat'

_cthkt=6

_cthkb=10
_cthk=5

_cthkb=6
_cthk=3

# -- bigger 0 and regular
_cthkbp=10
_cthkp=4

_cthkbb=20
_cthkl=4

_strmspace=0.75
_t1top=''

rc=jaecol()

_nn=1
_bdtg=subwrd(args,_nn); _nn=_nn+1
_model=subwrd(args,_nn); _nn=_nn+1 
_tau=subwrd(args,_nn); _nn=_nn+1
_area=subwrd(args,_nn); _nn=_nn+1

rc=strlen(_bdtg)
if(rc = 8) 
  _bdtg='20'_bdtg
endif

_pn=subwrd(args,_nn); _nn=_nn+1

_batch=subwrd(args,_nn); _nn=_nn+1
if(_batch = '') ; _batch='n' ; endif

_gname=subwrd(args,_nn); _nn=_nn+1

if(_gn='') ; _gname=0 ; endif

#
# 20020622 - deprecate _offline
#
_offline='NULL'

_grfprc=subwrd(args,_nn); _nn=_nn+1
if(_grfprc='') ; _grfprc=_grfprcdef ; endif

if(_grfprc = 'gxgif') 
  _cthkb=6
  _cthkt=5
  _cthk=4
endif

_xsize=subwrd(args,_nn); _nn=_nn+1
_ysize=subwrd(args,_nn); _nn=_nn+1

_mopt1=subwrd(args,_nn); _nn=_nn+1

#
#  now set basemap
#
if(_dobg = 1)
  _bmname=_basemapdir'/basemap.'_area'.png'
else
  _bmname=_basemapdir'/basemap.'_area'.gif'
endif


if(_verb=1)
print 'BBBBBTTTTT: '_btthere
print 'FFFFFTTTTT: '_ftthere
endif

#
#	dtau for calcs
#
_dtau=12

if(dtg = ''); return ; endif

#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
#  define precipitation (pr) and sea-level presuure (psl)
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp

rc=precipvar()
rc=pslvar()
rc=modelvar()

# --------- override from cfg in w2.plot2.py
rc=localvar()
rc=prvar()

#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#
#  open files
#
#  20060418 -- do in loadcfg generated in w2.plot.py
#
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo


_fm=ofile(_geodir'/geo.1deg.ctl')

if(_climosstdir != 'None')
  _fsc=ofile(_climosstdir'/climobs_sst_clim.ctl')
else
  _fsc=0
endif
if(_climodatdir != 'None')
   clmctl=_climodatdir'/clm.25.'_bdtg'.ctl'
print 'ccccccccccccccccccccccc 'clmctl
  _fwc=ofile(clmctl)
else
  _fwc=0
endif


#
#  if doing basemap set _fnf to mask _fm
#

if(_model='basemap')
  _fnf=_fm
endif

tauincp=-1*_dtau
_dtgp=incdtgh(_bdtg,tauincp)

if(_model = 'basemap') 
  _fnf=-999
  _fnfp=-999
endif


*
*	punch out of no data, except for ncep r1 reanal (nr1)
*


if(_fnf=0 | _fnf=-999 ) 
  say 'NO DATA ........... for model: '_model'  specopt: '_specopt' dtg: '_bdtg
  return(3)
endif


*
*	max taus
*
if(substr(_bdtg,9,2)=12) ; _taumax=72  ; _taumin = -72 ; endif
if(substr(_bdtg,9,2)=00) ; _taumax=120 ; _taumin = -72 ; endif

rc=setstau()


'set csmooth on'
'set clopts -1 -1 0.10'
'set clskip 2 1.0'
*
*	set up the area
*
if(_areadone='n')
 rc=setplot(_area)
 _areadone='y'
endif

*
*	do the plots
*

rd=setdraw()
rc=pman(_pn)
*
*	out for testing
* 
if(rc=99) ; return ; endif

*
*	quit if no data
*
if(rc!=0) 
  say 'NO or not enough data for this plot'
  return(99)
endif   

'set vpage off'

#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
#
# bottom title logos
#
#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

if(_specopt != 'basemap')
  rc=bottitle(_tack1,_tack2,1,_t1col,_t2col)
  rc=botcurtime(_curtime)
  if(_doeclogo=1)
    rc=eclogo(9.1,8.26,0.40)
  endif
endif

if(_batch = 'y') 

  m4name='4panels.'_model'.'_area'.'_bdtg'.'_tau'.gm' 
  p4name='4panels.'_model'.'_area'.'_bdtg'.'_tau'.ps'
  g4name='4panels.'_model'.'_area'.'_bdtg'.'_tau'.gif'
  x4name='4panels.'_model'.'_area'.'_bdtg'.'_tau'.xwd'

  if(_grfprc='gxgif')
    xsiz=720
    ysiz=540
    'enable print 'm4name
    'print'
    'disable print'
    '!gxgif -i 'm4name' -o 'g4name' -x 'xsiz' -y 'ysiz
    '!rm 'm4name
  endif

  if(_grfprc='gif')
    rc=getinfo()
    '!xtof 'g4name' GIF '_winid

*    '!giftrans -t 0 'g4name' > 'g4name'.T'
*    '!mv 'g4name'.T 'g4name

  endif

  if(_grfprc='wi')
    'wi '_gname
  endif

  if(_grfprc='printim' | _grfprc = 'gxyat')

    if(_dobg = 1 & _model != 'basemap' )


      cmd=_grfprc' '_gname' -b '_bmname' -t 0 x'_xsize' y'_ysize' png'
      print 'PPPP('_grfprc'): '_gname' 'cmd
      cmd
      
# -- use convert to reduce file size if doing 2.1 graphics; faster than pngquant


      if(_dopngquant)
        cmd='convert '_gname' -colors 64 '_gname
        cmd=_xpngquant' --speed 10 -f 64 '_gname' -o '_gname
        print 'PPPP(convert): 'cmd
        '!'cmd
      endif

    else
      'printim '_gname' x'_xsize' y'_ysize
    endif

  endif

  if(_grfprc='xwd')
    'outxwd 'x4name
    say '!convert xwd:'x4name' gif:'g4name
    '!convert xwd:'x4name' gif:'g4name

  endif

  if(_grfprc='ps')
    m4name=_gname'.gm'
    p4name=_gname'.ps'
    g4name=_gname'.gif'
print 'GGGGGGGGGGGGGGGG 'm4name
print 'GGGGGGGGGGGGGGGG 'p4name
print 'GGGGGGGGGGGGGGGG 'g4name
    'enable print 'm4name
    'print'
    'disable print'
    'reinit'
    '!gxps -c -i 'm4name' -o 'p4name
    '!convert -density 144 -rotate 90 'p4name' 'g4name
    '!rm 'm4name
    '!rm 'p4name
    return(6)
  endif

  if(_gname != 0 & ( _offline = 0 | _offline = 'full') & (_grfprc != 'wi')  & (_grfprc != 'printim') ) 
    '!cp 'g4name' '_gname
    '!rm 'g4name
    return(1)
  endif

  if(_offline = 'test' ) 
    '!mv 'g4name' test.gif'
    'enable print test.gm'
    'print'
    'disable print'
    'reinit'
    return(5)
  endif

#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
#
#  add basemap
#  
#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

if(_dobasemap = 1) 
  cmd=_combinecmd' -compose over '_bmname' '_gname' '_gname
   print 'CCCCCCCCCCCCCCbasemap: 'cmd
  '!'cmd
endif


endif

#
# return 2 if did all plots in loop
#

return(2)




function botcurtime(t1)

'q gxinfo'
card=sublin(result,2)
pagex=subwrd(card,4)
pagey=subwrd(card,6)

y1=0.08
xs=pagex-y1

tsiz=0.08
'set strsiz 'tsiz
'set string  1 r 5'
'draw string 'xs' 'y1' 't1

return



*
*-----------------------------  pman ---------------
*		
function pman(k)

if(_pareabd != '') 
 'set parea '_pareabd
else
 'set parea 0.4 10.8 0.65 8.25'
endif

'c'
'set vpage 0 11 0 8.5'
'set vpage 0.1 10.9 0.1 8.4'

'set time '_time
'q time'

pstat=1

if(k=1) ; rc=gpz500(j) ; endif
if(k=2) ; rc=gppsl(j) ; endif
if(k=3) ; rc=gpprecip(j) ; endif
if(k=4) ; rc=gp850(j) ; endif
if(k=5) ; rc=gptas(j) ; endif
if(k=6) ; rc=gpuas(j) ; endif
if(k=7) ; rc=gpu500(j,500) ; endif
if(k=8) ; rc=gpushr(j) ; endif
if(k=9) ; rc=gpu700(j) ; endif
if(k=23) ; rc=gpu500(j,700) ; endif
if(k=10) ; rc=gpsst(j) ; endif
if(k=11) ; rc=gpwav(j) ; endif
if(k=12) ; rc=gpw200(j) ; endif
if(k=13) ; rc=gpwdlm(j) ; endif
if(k=14) ; rc=gplmq('lm') ; endif
if(k=15) ; rc=gplmq('mh') ; endif
if(k=16) ; rc=gplmq('hh') ; endif
if(k=20) ; rc=gptmax(j) ; endif
if(k=21) ; rc=gptmin(j) ; endif
if(k=22) ; rc=gpthk(j) ; endif
if(k=30) ; rc=gpbasemap(j) ; endif
if(k=50) ; rc=gpclm(j) ; endif
if(k=60) ; rc=gpstm(j) ; endif

if(k=101) ; rc=gpn850(j) ; endif
if(k=102) ; rc=gpcpcpr('op06') ; endif
if(k=103) ; rc=gpcpcpr('op12') ; endif


if((_btthere | _ftthere) & (rc = 0 | rc = 99) & _specopt != 'basemap' & _dotc=1)
  rctc=tcplot()
endif

if(rc = 0) ; pstat=0 ; endif
if(rc = 99 | rc = 98) ; pstat=99 ; endif

return(pstat) 





#
# -------------------------- tcsetup ------------------------------------
#
function tcsetup()

_btautc=0
_dtautc=6

rc=settcbt()

if(_ntcbt.m000 > 0); _btthere=1; endif

return

#
# -------------------------- tcplot  ------------------------------------
#
function tcplot

rc=plotdims()
'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

#
# get ft posits and draw
#
rc=ftposits(_tau,_btautc,_dtautc)
rc=drawtcft()

#
# draw bt
#
rc=drawtcbt()

# get of posits and draw
#
#rc=ofposits(_tau,_btautc,_dtautc)
#rc=drawtcof()


return


*
*-------------------------- readrun ------------------
*
function readrun(runfile)
iok=0
i=0
imax=500
while(1)
  rc=read(runfile)
  card=sublin(rc,2)
  iok=sublin(rc,1)

  if(iok=0)
    i=i+1
    _args.i=card
  endif

  if(iok=2)
    return(i)
  endif

  if(iok != 0 & i <= imax)
    say 'Unable to read configuration file!!!'
    say 'BYE'
    'quit'
  endif

endwhile

return(999)


function newstuff()
    if(_newtcfc = 1)
      _tcft.i.n=subwrd(card,1)
if(_verb) ; print 'FFFF _tcft '_tcft.i.n' 'i ;endif
      j=1
      while(j<=_tcft.i.n)
        rc=read(runfile)
        iok=sublin(rc,1)
        if(iok=0)
          card=sublin(rc,2)
         _tcft.i.j=card
if(_verb) ; print 'FFFF 'i' 'j' '_tcft.i.j ; endif
        else
          print 'EEEE suppose to read '_tcft.i.n' posits for run 'i
           'quit'
        endif
        j=j+1
      endwhile
    endif
return



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
*-------------------------- curdtgh ------------------
*
function curdtgh()
*
*  convert current time to dtg 
*
  moname='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
  'q time'
  t1=subwrd(result,3)
  iyr=substr(t1,11,2)
  nmo=substr(t1,6,3)
  ida=substr(t1,4,2)
  ihr=substr(t1,1,2)
  i=1
  while (nmo!=subwrd(moname,i));i=i+1;endwhile
  imo=i
  if(imo < 10); imo='0'imo; endif
  if(ihr = 0); ihr='00';endif
  if(ihr < 10 & ihr != '00'); ihr='0'ihr; endif

  idtg=iyr%imo%ida%ihr

return (idtg)

*
*-------------------------- incdtgh ------------------
*
function incdtgh(dtgh,inc)
*
***** y2k ******
*  increment a dtg by inc hours
*  RESTRICTIONS!!  
*  (1)  inc > 0
*  (2)  inc < 24
*
  monday.1=31
  monday.2=28
  monday.3=31
  monday.4=30
  monday.5=31
  monday.6=30
  monday.7=31
  monday.8=31
  monday.9=30
  monday.10=31
  monday.11=30
  monday.12=31

  iyr=substr(dtgh,1,4)*1
  imo=substr(dtgh,5,2)*1
  ida=substr(dtgh,7,2)*1
  ihr=substr(dtgh,9,2)*1
*   say 'qqq 'dtgh' 'inc
  if(mod(iyr,4)=0) 
    monday.2=29
  endif

  ihr=ihr+inc
*  say 'ihr = 'ihr' ida = 'ida

  while(ihr>=24)
    ihr=ihr-24
    ida=ida+1
  endwhile

  while(ihr<0)
    ihr=ihr+24
    ida=ida-1
  endwhile

*  say 'new ihr = 'ihr' new ida = 'ida' imo = 'imo

  if(ida > monday.imo)
    ida=ida-monday.imo
*    say 'inside check ida = 'ida' monday = 'monday.imo
    imo=imo+1
  endif

  while(ida < 0)
    imo=imo-1
    ida=monday.imo+ida
  endwhile

  if(ida = 0)
    imo=imo-1
    if(imo<=0)
      imo=imo+12
      iyr=iyr-1
    endif
    ida=monday.imo
  endif

  if(imo<=0)
    imo=imo+12
    iyr=iyr-1
  endif

  if(imo>=13)
    imo=imo-12
    iyr=iyr+1
  endif


if(iyr<10);iyr='0'iyr;endif
if(imo<10);imo='0'imo;endif
if(ida<10);ida='0'ida;endif
if(ihr<10);ihr='0'ihr;endif

return (iyr%imo%ida%ihr)

*
*-------------------------- dtghcur ------------------
*
function dtghcur(dtgh)
###### y2k ######
*
*  convert FNMOC DTG to GrADS time
*
 moname='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
  iyr=substr(dtgh,1,4)*1
  imo=substr(dtgh,5,2)*1
  ida=substr(dtgh,7,2)*1
  ihr=substr(dtgh,9,2)*1
  nmo=subwrd(moname,imo)
  imo=i
return (ihr%'Z'ida%nmo%iyr)

function dtghval(cdtg)
  iyr=substr(cdtg,1,4)*1
  imo=substr(cdtg,5,2)*1
  ida=substr(cdtg,7,2)*1
  ihr=substr(cdtg,9,2)*1
  idtg=iyr*1000000+imo*10000+ida*100+ihr
return(idtg)
*
*----------------- setplot ----------------
*
function setplot(area)
*
*	read an input file for the plot parameters
*
fname=_cfgdir'/area.'_area'.cfg'

iok=0
i=0
ncards=13
while(iok = 0 & i <= ncards)

  rc=read(fname)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  i=i+1

  if(iok != 0 & i = 1) 
    say 'unable to open plot set up data for area= '_area
    say 'BYE'
    'quit'
  endif
 
  if(iok != 0 & i <= ncards)
    say 'premature EOF in area set up file= 'fname
    say 'BYE'
    'quit'
  endif

  if(i=1)  ; _proj    = subwrd(card,1) ; endif
  if(i=2)  ; _geores  = subwrd(card,1) ; endif
  if(i=3)  ; _pareabd = card           ; endif
  if(i=4)  ; _lon1    = subwrd(card,1) ; endif
  if(i=5)  ; _lon2    = subwrd(card,1) ; endif
  if(i=6)  ; _lat1    = subwrd(card,1) ; endif
  if(i=7)  ; _lat2    = subwrd(card,1) ; endif
  if(i=8)  ; _mplon1  = subwrd(card,1) ; endif
  if(i=9)  ; _mplon2  = subwrd(card,1) ; endif
  if(i=10) ; _mplat1  = subwrd(card,1) ; endif
  if(i=11) ; _mplat2  = subwrd(card,1) ; endif
  if(i=12) ; _xlint   = subwrd(card,1) ; endif
  if(i=13) ; _ylint   = subwrd(card,1) ; endif

endwhile

rc=close(fname)

*
*	defaults do the sets
*
  if(_proj    = default ) ; _proj     = latlon  ; endif 
  if(_geores  = default ) ; _geores   = lowres ; endif 
  if(substr(_pareabd,1,3) = def ) 
    _pareabd  = '1 10 1 8'
   endif 
  if(_lon1    = default ) ; _lon1     = 0      ; endif 
  if(_lon2    = default ) ; _lon2     = 360    ; endif 
  if(_lat1    = default ) ; _lat1     = -90    ; endif 
  if(_lat2    = default ) ; _lat2     = 90     ; endif 
  if(_mplon1  = default ) ; _mplon1   = ''     ; endif 
  if(_mplon2  = default ) ; _mplon2   = ''     ; endif 
  if(_mplat1  = default ) ; _mplat1   = ''     ; endif 
  if(_mplat2  = default ) ; _mplat2   = ''     ; endif 
  if(_xlint   = default ) ; _xlint    = ''     ; endif 
  if(_ylint   = default ) ; _ylint    = ''     ; endif 

  'set mproj '_proj
  'set mpdset '_geores
  if(_pareabd != '') ; 'set parea '_pareabd ; endif
  'set lon '_lon1' '_lon2
  'set lat '_lat1' '_lat2
#
# create land-sea mask always for lterp
#  
  pland=50
  'ls=const(const(maskout(sftlf.'_fm'(t=1),sftlf.'_fm'(t=1)-'pland'),-1),0,-u)'


  if( (_proj = 'nps' | _proj = 'sps' | _proj = 'lambert') & mplon1 != '') 
    'set mpvals '_mplon1' '_mplon2' '_mplat1' '_mplat2
  else
    if(_proj = 'nps')
      _mplon1=-90
      _mplon2=270
      _mplat1=0
      _mplat2=90
    endif
    if(_proj = 'sps')
      _mplon1=-90
      _mplon2=270
      _mplat1=-90
      _mplat2=0
    endif
  endif  

#
# do in modelvar.gsf vice here
#

#
# turn off lon fill since using "2" models
#
dollfill=0
_ukfill=0

if(dollfill = 1)

  #
  # 20060814 -- fill accross error in ukm gempak interp
  #


  if(_model = 'ukm')
    if(_lon1< -20 & _lon2 > -20)
      _ukfill=1
    endif
    if(_lon1>=340 & _lon2 <350)
      _ukfill=1
    endif
    if(_lon1>=180 & _lon2 > 370 )
      _ukfill=1
    endif
  endif

  if(_model = 'cmc')
    if(_lon1< -0 & _lon2 > 0)
      _ukfill=1
    endif
    if(_lon1>=360 & _lon2 < 390)
      _ukfill=1
    endif
    if(_lon1>=180 & _lon2 > 360 )
      _ukfill=1
    endif
  endif

  _dlatfill=2.0
  if(_model = 'cmc' & _ukfill=1) ; _dlatfill=4.0 ; endif

endif


return



function setstau
  _dtg=incdtgh(_bdtg,_tau)
  _time=dtghcur(_dtg)
  if(_tau < 0) ; _fn=0 ; else ; _fn=_fnf ; endif
  taup=_tau-_dtau
  if(taup < 0) ; _fnp=0 ; else ; _fnp=_fnf ; endif 
  _dtgp=incdtgh(_bdtg,taup)
  _timep=dtghcur(_dtgp)

return
*
*-------------------------- scrptle ------------------
*
function scrptle(scale,type)

  rc=plotdims()
  '!dtg > dtg.cur'
  rc=read(dtg.cur)
  dtg=sublin(rc,2)
  rc=close(dtg.cur)

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
  'set strsiz 'tsiz
  'set string 1 r 4' 
  'draw string 'x2' 'y2' 'dtg
  'set string 1 c 6 0'


return

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

'set rgb 71 250 250 250'
'set rgb 72 200 200 200'
'set rgb 73 160 160 160'
'set rgb 74 140 140 140'
'set rgb 75 112 112 112'
'set rgb 76  80  80  80'   
'set rgb 77  60  60  60'   
'set rgb 78  40  40  40'
'set rgb 79  32  32  32'

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

  card=sublin(result,3)
  _xlplot=subwrd(card,4)
  _xrplot=subwrd(card,6)

  card=sublin(result,4)
  _ybplot=subwrd(card,4)
  _ytplot=subwrd(card,6)

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

function getinfo()
'q'
card=sublin(result,1)
gradsver=subwrd(card,3)
winname='"GrADS 'gradsver'"'
wfile='wininfo.'_area'.'_model'.'_bdtg
'!xwininfo -int -name 'winname' > 'wfile
i=0; gotid=0
while (1)
  res=read(wfile)
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
rc=close(wfile)
'!rm 'wfile
return(gotid)

function efscol(cmap,offset)

if(cmap=efs_1)

icb=70
ic=icb

'set rgb 'ic'    0  29  29' ; ic=ic+1
'set rgb 'ic'    0  49  49' ; ic=ic+1
'set rgb 'ic'    0  69  69' ; ic=ic+1
'set rgb 'ic'    0  89  89' ; ic=ic+1
'set rgb 'ic'    0 109 109' ; ic=ic+1
'set rgb 'ic'    0 129 129' ; ic=ic+1
'set rgb 'ic'    0 149 149' ; ic=ic+1
'set rgb 'ic'    0 169 169' ; ic=ic+1
'set rgb 'ic'    0 189 189' ; ic=ic+1
'set rgb 'ic'    0 209 209' ; ic=ic+1
'set rgb 'ic'    0 229 229' ; ic=ic+1
'set rgb 'ic'    0 249 249' ; ic=ic+1
'set rgb 'ic'    0 209 255' ; ic=ic+1
'set rgb 'ic'    0 169 255' ; ic=ic+1
'set rgb 'ic'    0 129 255' ; ic=ic+1
'set rgb 'ic'    0  89 255' ; ic=ic+1
'set rgb 'ic'    0  49 255' ; ic=ic+1
'set rgb 'ic'   49   0 255' ; ic=ic+1
'set rgb 'ic'   89   0 255' ; ic=ic+1
'set rgb 'ic'  109   0 255' ; ic=ic+1
'set rgb 'ic'  149   0 255' ; ic=ic+1
'set rgb 'ic'  189   0 255' ; ic=ic+1
'set rgb 'ic'  209   0 255' ; ic=ic+1
'set rgb 'ic'  249   0 255' ; ic=ic+1
'set rgb 'ic'  255   0 209' ; ic=ic+1
'set rgb 'ic'  255   0 169' ; ic=ic+1
'set rgb 'ic'  255   0 129' ; ic=ic+1
'set rgb 'ic'  255   0  89' ; ic=ic+1
'set rgb 'ic'  255   0  49' ; ic=ic+1

return(icb' 'ic)
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
return('20 42')
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

return('20 42')
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
return('50 72')
endif

return



function tyear(dtg)
mo=substr(dtg,5,2)*1.0
hr=substr(dtg,9,2)/24.0
da=substr(dtg,7,2)*1.0+hr

imo=substr(dtg,5,2)
if(substr(imo,1,1) = '0') ; imo=substr(imo,2,1) ; endif
mda=_ndymon.imo*0.5

if(da<mda) 
  nda1=_ndymon.imo
  mda1=nda1*0.5
  imo=imo-1
  if(imo = 0) ; imo=12 ; endif
  nda2=_ndymon.imo
  mda2=nda2*0.5
  ndai=nda1-mda1+mda2
  da=ndai - (mda-da)
  mo=mo-1
  w1=1-(da/ndai)
  w2=1-w1
  imo1=imo
  imo2=imo+1
  if(imo2 > 12) ; imo2 = 1 ; endif
  return(imo1' 'w1' 'imo2' 'w2)
endif

if(da>mda)
  nda1=_ndymon.imo
  mda1=nda1*0.5
  imo1=imo
  imo=imo+1
  if(imo > 12) ;  imo=1 ; endif 
  if(imo = 0) ; imo = 12 ; endif
  nda2=_ndymon.imo
  mda2=nda2*0.5
  ndai=nda1-mda1+mda2
  da=da-mda
  w1=1-(da/ndai)
  w2=1-w1
  imo2=imo
  if(imo2 > 12) ; imo2 = 1 ; endif
  if(imo2 = 0) ; imo2 = 12 ; endif
  return(imo1' 'w1' 'imo2' 'w2)
endif

if(da=mda)
  imo1=imo
  imo2=imo
  w1=1.0
  w2=0.0  
  return(imo1' 'w1' 'imo2' 'w2)
endif

return('error')

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
*
*	rc=cbarn(args,lab,labstr)
*
*	where args="sf vert xmid ymid force"
*
*	sf   - scale the whole bar 1.0 = original 0.5 half the size, etc.
*	vert - 0 FORCES a horizontal bar = 1 a vertical bar
*	xmid - the x position on the virtual page the center the bar
*	ymid - the x position on the virtual page the center the bar
*	force - y - then use color info in _shdinfo.? array
*
*	if vert,xmid,ymid are not specified, they are selected
*	as in the original algorithm
*
*	to specify a color bar, in the calling function
*	
*	cbarg='0.90 0 5.5 0.78 y'  * where y is to force
*
*	and set the global variable _shdinfo 
*
*	_shdinfo.1='Number of levels = 13'
*	_shdinfo.2='9 < -20'
*	_shdinfo.3='14 -20 -15'
*	_shdinfo.4='4 -15 -10'
*	_shdinfo.5='11 -10 -5'
*	_shdinfo.6='5 -5 0'
*	_shdinfo.7='13 0 5'
*	_shdinfo.8='3 5 15'
*	_shdinfo.9='10 15 20'
*	_shdinfo.10='7 20 25'
*	_shdinfo.11='12 25 30'
*	_shdinfo.12='8 30 35'
*	_shdinfo.13='2 35 40'
*	_shdinfo.14='6 40 >'
*
*	where in _shdinfo.2 
*
*	9 = color
*	<	:	low value (< less than ; > greater than)
*	-20	:	high value
*
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
  strxsiz=0.11*sf*0.95
  strysiz=0.12*sf*0.95
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

*say 'cccccc 'xl' 'xr' 'yt' 'yb' 'xwid' 'ywid' 'cnum
*say 'cccccc 'strxsiz' 'strysiz' 'stroff

if(vert=1)
  bb=0.075*sf
  xlbb=xl - bb
  xrbb=xr + stroff + 3*strysiz + bb
  ybbb=yb - bb
  ytbb=yb + ywid*cnum + bb

*say 'cccccc 'xlbb' 'xrbb' 'ytbb' 'ybbb

  'set line 0'
  'draw recf 'xlbb' 'ybbb' 'xrbb' 'ytbb

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
    'set line 'col
    'draw recf 'xl' 'yb' 'xr' 'yt
    'set line 1 1 4'
    'draw rec 'xl' 'yb' 'xr' 'yt
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
        'set line 'col
        'draw polyf 'xl' 'yt' 'xm' 'yb' 'xr' 'yt' 'xl' 'yt

        'set line 1 1 4'
        'draw line 'xl' 'yt' 'xm' 'yb
        'draw line 'xm' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'yt


      else

        xm=(xl+xr)*0.5
        ym=(yb+yt)*0.5

        'set line 'col
       'draw polyf 'xl' 'ym' 'xr' 'yb' 'xr' 'yt' 'xl' 'ym
        'set line 1 1 4'
        'draw line 'xl' 'ym' 'xr' 'yb
        'draw line 'xr' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'ym

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

        'set line 'col
        'draw polyf 'xl' 'yb' 'xm' 'yt' 'xr' 'yb' 'xl' 'yb

        'set line 1 1 4'
        'draw line 'xl' 'yb' 'xm' 'yt
        'draw line 'xm' 'yt' 'xr' 'yb
        'draw line 'xr' 'yb' 'xl' 'yb


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

        'set line 'col
        'draw polyf 'xr' 'ym' 'xl' 'yb' 'xl' 'yt' 'xr' 'ym

        'set line 1 1 4'
        'draw line 'xr' 'ym' 'xl' 'yb
        'draw line 'xl' 'yb' 'xl' 'yt
        'draw line 'xl' 'yt' 'xr' 'ym

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


function col500()

'set rgb 49  00 20 60'
'set rgb 47  00 40 100'
'set rgb 43  00 60 150'
'set rgb 61  00 120 200'

'set rgb 69 20  5 00'
'set rgb 68 50  5 00'
'set rgb 67 100 10 00'
'set rgb 66 120 10 00'
'set rgb 65 130 10 00'
'set rgb 64 150 40 0'
'set rgb 63 170 60 00'
'set rgb 21 200 100 00'
'set rgb 22 255 232 120'
'set rgb 22 255 140 100'

return(0)


*-------------------------- strlen ------------------
*
function strlen(arg)

i=1
while(substr(arg,i,1) != '' & i<250)
  i=i+1
endwhile
return(i-1)

function drawmap(mcol)
if(mcol !='' | mcol ='mcol') ; mcol=1 ; endif
'set map 0 0 12'
'set map 0 0 8'
'draw map'
'set map 'mcol' 0 6'
'set map 'mcol' 0 4'
'draw map'
return

function mfcol(opt)

if(opt=1)
'set rgb 21 255 250 170'
'set rgb 22 255 232 120'
'set rgb 23 255 192  60'
'set rgb 24 255 160   0'
'set rgb 25 255  96   0'
'set rgb 26 255  50   0'
'set rgb 27 225  20   0'
'set rgb 28 192   0   0'
'set rgb 29 165   0   0'

*light blue to dark blue
'set rgb 41 200 255 255'
'set rgb 42 175 240 255'
'set rgb 43 130 210 255'
'set rgb 43 100 190 255'
'set rgb 44  95 190 250'
'set rgb 45  75 180 240'
'set rgb 45  40 160 225'
'set rgb 46  60 170 230'
'set rgb 47  40 150 210'
'set rgb 47  10 80 160'
'set rgb 48  00 65 140'
'set rgb 49  00 50 100'
endif

function settcbt()
_btcoltc=3
_btcol=6
_btszscl=1.0
_bttau=0

_ftszscl=1.0
_ftbcol=1
_ftfcol=2

# load the global data arrays
rc=prwtcbt()
rc=prwtcft()

# -- new bt taus
#
_nbttaus=1


_bttaus.1=0
return
function prwtcbt()
_ntcbt.m000=4
_tcbt.m000.1 ='  17.90  246.20     40 '
_tcbt.m000.2 ='  39.90  163.80     30 '
_tcbt.m000.3 ='  11.30  301.90     30 '
_tcbt.m000.4 ='  -9.60   87.60     30 '
return
function prwtcft()
return

function drawtcbt()

#'set rgb 98   1   1   1'
#'set rgb 99 254 254 254'
# btc=99

nbttimes=_nbttaus


# -- force single bt
#
nbttime=1
nbttimes=1

while(nbttime <= nbttimes)

#bttau=_bttaus.nbttime
# -- set by function main
#
bttau=_bttau

fmt='m%03.0f'
if(substr(bttau,1,1) != 'm')
  if(bttau < 0) ; bttau=-1*bttau ; endif
  pbttau=math_format(fmt,bttau)
else
  pbttau=bttau
endif

if(_ntcbt.pbttau = 0) ; return ; endif

nbt=_ntcbt.pbttau

# -- if no bts, bail
#
if(nbt = 0 | substr(nbt,1,2) = '_n') ; return ; endif

btc=1
n=1
while(n<=nbt) 

  btmw=subwrd(_tcbt.pbttau.n,3)

  btsizmx=0.25
  btsizmn=0.15
  btsiz=btsizmx*(btmw/135)
  btsiz=0.50
  if(btsiz<btsizmn) ; btsiz=btsizmn ; endif
  btsym=41

  if(_btszscl != '' & _btszscl != '_btszscl' & _btszscl != 'reset' )
    if(_btszscl > 0)
       btsiz=btsiz*_btszscl
    else
       btsiz=-1*_btszscl
    endif
  endif

  btstrc=1
  domark=0

  if(btmw >= 65)
    btc=2
    if(_btcoltc != '_btcoltc') ; btc=_btcoltc ; endif
    btsym=41
    btstrc=btc
  endif

  if(btmw >= 35 & btmw < 65)
    btc=6
    if(_btcol != '_btcol') ; btc=_btcol ; endif
    btsym=40
    btstrc=btc
  endif

  if(btmw < 35)
    btc=6
    if(_btcol != '_btcol') ; btc=_btcol ; endif
    btsym=40
    btsym=2
    btstrc=btc
    mksiz=btsiz*0.5
    domark=1
  endif

  btlat=subwrd(_tcbt.pbttau.n,1)
  btlon=subwrd(_tcbt.pbttau.n,2)

#
# check if lon setting is deg w
#
  if(_lon1 < 0)
    btlon=btlon-360.0
  endif

  'q w2xy 'btlon' 'btlat

  x=subwrd(result,3)
  y=subwrd(result,6)
#
# test if a plot has been made...
#
drawtest=substr(result,1,10)
if(drawtest = 'No scaling'); return; endif

  xs=x+0.015
  ys=y-0.015
if(domark = 0)
  'draw wxsym 'btsym' 'xs' 'ys' 'btsiz' '0' 8'
  'draw wxsym 'btsym' 'x' 'y' 'btsiz' 'btc' 6'
endif

if(domark = 1)
  'set line 98 1 8'
  'draw mark 'btsym' 'xs' 'ys' 'mksiz' 98 8'
  'set line 'btc' 1 5'
  'draw mark 'btsym' 'x' 'y' 'mksiz' 'btc' 6'
  'set line 1'
endif

  btstrsiz=btsiz*0.15
  if(btmw >= 100) ;  btstrsiz=btsiz*0.125 ; endif

  'set strsiz 'btstrsiz

  'set string 0 c 10'
  'draw string 'x' 'y' 'btmw
  'set string 'btstrc' c 5'
  'draw string 'x' 'y' 'btmw

  n=n+1
endwhile

nbttime=nbttime+1
endwhile

return
function drawtcft()

ftsiz=0.115
ftsizs=ftsiz+0.025
ftsizi=ftsiz-0.050
if(_ftszscl != '' & _ftszscl!='_ftszscl') ; ftsiz=ftsiz*_ftszscl ; endif

if(_nfcall = 0) ; return ; endif

n=1
while(n<=_ntcftall._tau) 


  ftlat=subwrd(_tcftall.n,1)
  ftlon=subwrd(_tcftall.n,2)
  fttype=subwrd(_tcftall.n,3)
#
# check if lon setting is deg w
#
if(ftlon = '') ; return ; endif
  if(_lon1 < 0)
    ftlon=ftlon-360.0
  endif

ftest=substr(ftlat,1,3)
if(ftest = '_tc') ; return ; endif

  'q w2xy 'ftlon' 'ftlat
if(subwrd(result,1) = 'No' | subwrd(result,1) = 'Query')
  return
endif
  x=subwrd(result,3)
  y=subwrd(result,6)

  xs=x-0.015
  ys=y+0.015

  ftc=3
  ftci=2
  if(fttype = -1); ftci=4; endif

  if(_ftbcol != '' & _ftbcol != '_ftbcol') ; ftc=_ftbcol ; endif
  if(_ftfcol != '' & _ftfcol != '_ftfcol') ; ftci=_ftfcol ; endif

  ftm=3

  'set line 0'
  'draw mark 'ftm' 'x' 'y' 'ftsizs

  'set line 'ftc
  'draw mark 'ftm' 'x' 'y' 'ftsiz

  'set line 'ftci
  'draw mark 'ftm' 'x' 'y' 'ftsizi

  n=n+1
endwhile

return

function ftposits(ttau,btau,dtau)

tau=ttau*1

maxtau=168
# no posits > 168 h so load all that are available
#
if(tau > maxtau)
  tau=maxtau
endif

jmax=400
i=1
while(tau>=btau)

  n=_ntcft.tau

# -- detect undefined n = the variable string
#
  if(n = '_ntcft.'tau)
    _ntcftall.ttau=0
    return(0)
  endif


  if(n >= 1 )
    j=1
    while(j<=n & j<jmax)

      posit=_tcft.tau.j' 'tau

#
# dtau=6 but posits may not be available
#
#print 'PPPPPP 'tau' posit: 'posit

pchk=substr(posit,1,3)
if(pchk = '_tc')
  j=jmax+1
else
  _tcftall.i=posit
  j=j+1
  i=i+1
endif
    endwhile
    if(j = jmax)
      return(999)
    endif
  endif
  tau=tau-dtau
endwhile

np=i-1
if(i=1); np=_ntcft.tau ; endif
_ntcftall.ttau=np
return(0)
function setgtime()
_ugtime.0='Wed 0000 UTC 05 OCT'
_lgtime.0='Tue 2000 EDT 04 OCT'
_ugtime.6='Wed 0600 UTC 05 OCT'
_lgtime.6='Wed 0200 EDT 05 OCT'
_ugtime.12='Wed 1200 UTC 05 OCT'
_lgtime.12='Wed 0800 EDT 05 OCT'
_ugtime.18='Wed 1800 UTC 05 OCT'
_lgtime.18='Wed 1400 EDT 05 OCT'
_ugtime.24='Thu 0000 UTC 06 OCT'
_lgtime.24='Wed 2000 EDT 05 OCT'
_ugtime.30='Thu 0600 UTC 06 OCT'
_lgtime.30='Thu 0200 EDT 06 OCT'
_ugtime.36='Thu 1200 UTC 06 OCT'
_lgtime.36='Thu 0800 EDT 06 OCT'
_ugtime.42='Thu 1800 UTC 06 OCT'
_lgtime.42='Thu 1400 EDT 06 OCT'
_ugtime.48='Fri 0000 UTC 07 OCT'
_lgtime.48='Thu 2000 EDT 06 OCT'
_ugtime.60='Fri 1200 UTC 07 OCT'
_lgtime.60='Fri 0800 EDT 07 OCT'
_ugtime.72='Sat 0000 UTC 08 OCT'
_lgtime.72='Fri 2000 EDT 07 OCT'
_ugtime.84='Sat 1200 UTC 08 OCT'
_lgtime.84='Sat 0800 EDT 08 OCT'
_ugtime.96='Sun 0000 UTC 09 OCT'
_lgtime.96='Sat 2000 EDT 08 OCT'
_ugtime.108='Sun 1200 UTC 09 OCT'
_lgtime.108='Sun 0800 EDT 09 OCT'
_ugtime.120='Mon 0000 UTC 10 OCT'
_lgtime.120='Sun 2000 EDT 09 OCT'
_ugtime.132='Mon 1200 UTC 10 OCT'
_lgtime.132='Mon 0800 EDT 10 OCT'
_ugtime.144='Tue 0000 UTC 11 OCT'
_lgtime.144='Mon 2000 EDT 10 OCT'
_ugtime.156='Tue 1200 UTC 11 OCT'
_lgtime.156='Tue 0800 EDT 11 OCT'
_ugtime.168='Wed 0000 UTC 12 OCT'
_lgtime.168='Tue 2000 EDT 11 OCT'
return
