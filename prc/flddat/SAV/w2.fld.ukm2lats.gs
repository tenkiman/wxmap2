function main(args)

rc=gsfallow(on)
rc=const()

i=1
dtg=subwrd(args,i)     ; i=i+1
tau=subwrd(args,i)     ; i=i+1
dpathW=subwrd(args,i)   ; i=i+1
dpathM=subwrd(args,i)   ; i=i+1
opath=subwrd(args,i)   ; i=i+1
ptable=subwrd(args,i)   ; i=i+1

# -- assume dtau is 6
#
dtau=6
nt=(tau/dtau)+1

yyyy=substr(dtg,1,4)
mm=substr(dtg,5,2)
dd=substr(dtg,7,2)
hh=substr(dtg,9,2)

outconv='grads_grib'
outconv='grib_only'
dvar='uas'

fdW=ofile (dpathW)
fdM=ofile (dpathM)

rc=metadata(fdW,'y')

# -- sfc vars
#
nvs=6

lvar.1='pr'       ; lvart.1='m'
lvrts.1='accum'

lvar.2='prc'      ; lvart.2='m'
lvrts.2='accum'

lvar.3='psl'      ; lvart.3='m'
lvrts.3='instant' 

lvar.4='tas'     ; lvart.4='m'
lvrts.4='accum'

lvar.5='uas'     ; lvart.5='w'
lvrts.5='instant'

lvar.6='vas'     ; lvart.6='w'
lvrts.6='instant'



# -- UA vars
#
nvu=5

uvars.1='zg'      ; uvart.1='m'
uvrts.1='instant'

uvars.2='ta'      ; uvart.2='m'
uvrts.2='instant'

uvars.3='hur'     ; uvart.3='m'
uvrts.3='instant'

uvars.4='ua'      ; uvart.4='w'
uvrts.4='instant'

uvars.5='va'      ; uvart.5='w'
uvrts.5='instant'


# -- vert dimension

ulevs=_plevs.fdW
nz=_nz.fdW

i=1
while(i<=nz)
  plev.i=subwrd(ulevs,i)
  i=i+1
endwhile

lcenter='UKMO'
lmodel='ukm2'

'set_lats parmtab 'ptable

'set_lats convention 'outconv
'set_lats calendar standard'
'set_lats frequency hourly'
'set_lats model "'lmodel'"'
'set_lats center 'lcenter
'set_lats comment "destagger mass to wind points"'

'set_lats timeoption dim_env'
'set_lats frequency forecast_hourly'
'set_lats deltat 'tau

'set_lats create 'opath
idf=subwrd(result,5)
print 'idf 'idf
if(idf<=0) ; say 'unable to create LATS output file 'opath' sayoonara, baby ' ; 'quit' ; endif

'set_lats basetime 'idf' 'yyyy' 'mm' 'dd' 'hh' 0 0'

'set_lats gridtype linear'
'set x 1 '_nx.fdW
'set y 1 '_ny.fdW

'set t 'nt
'set_lats fhour 'tau

'lats_grid 'dvar
idg=subwrd(result,5)
if(idg = 0) ; say 'unable to define the LATS GRID; sayoonara, baby' ; 'quit' ; endif

print 'idf 'idf' idg 'idg

# -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV -- setup lats vars

# -- ua vars
#
'set_lats vertdim plev 'ulevs
idz=subwrd(result,5)
print 'idz 'idz

l=1
while(l<=nvu)
  uvar=uvars.l
  uvrt=uvrts.l
  'set_lats var 'idf' 'uvar' 'uvrt' 'idg' 'idz
  idvu.l=subwrd(result,5)
  print 'UUU idvu 'idvu.l
  l=l+1
endwhile

# -- sfc vars
#
l=1
while(l<=nvs)
  lvar=lvar.l
  lvrts=lvrts.l
  'set_lats var 'idf' 'lvar' 'lvrts' 'idg' 0'
  idvs.l=subwrd(result,5)
  print 'SSS idvs 'idvs.l
  l=l+1
endwhile


# -- UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU output upper air
#
l=1
while(l<=nvu)
uvar=uvars.l
uvrt=uvart.l
k=1
while(k<=nz)

  p=plev.k
  'set_lats write 'idf' 'idvu.l' 'p
  idw=subwrd(result,5)
  
  'set lev 'p

  if(uvrt = 'm')
     lexpr=mkexpr(uvar,fdM,fdW)
  endif
  
  if(uvrt = 'w')
     lexpr=mkexprw(uvar,fdM,fdW)
  endif

  'lats_data 'lexpr
  ido=subwrd(result,5)
  print 'UUU 'uvar' 'p' idw 'idw' ido 'ido

  k=k+1
endwhile

l=l+1
endwhile

# -- SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS output sfc
#
l=1
while(l<=nvs)
  lvar=lvar.l
  lvrts=lvrts.l
  lvrt=lvart.l

  'set_lats write 'idf' 'idvs.l' 0'
  idw=subwrd(result,5)

  if(lvrt = 'm')
     lexpr=mkexpr(lvar.l,fdM,fdW)
  endif
  
  if(lvrt = 'w')
     lexpr=mkexprw(lvar.l,fdM,fdW)
  endif
  
  'lats_data 'lexpr

  ido=subwrd(result,5)
  print 'SSS 'lvar' idw 'idw ' ido 'ido' lvrt: 'lvrt
l=l+1
endwhile

# -- CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC - close file
#
'set_lats close 'idf

'quit'

return

function mkexpr(var,fdM,fdW)
  expr='re('var'.'fdM','_nx.1',linear,'_x0.fdW','_dx.fdW','_ny.fdW',linear,'_y0.fdW','_dy.fdW')'
return(expr)

function mkexprw(var,fdM,fdW)
  expr='re('var'.'fdM','_nx.1',linear,'_x0.fdW','_dx.fdW','_ny.fdW',linear,'_y0.fdW','_dy.fdW')'
  expr=var
return(expr)


