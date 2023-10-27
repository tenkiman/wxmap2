function main(args)

rc=gsfallow(on)
rc=const()

i=1

dtg=subwrd(args,i)     ; i=i+1
dpath=subwrd(args,i)   ; i=i+1
opath=subwrd(args,i)   ; i=i+1

outconv='grads_grib'
outconv='grib_only'
minpgood=75.0

if(substr(dtg,5,6) = '010106')
  minpgood=50.0
endif

dvar='pr'
dvarchk06='(sum(pr,t-6*2,t+0))'
dvarchk12='(sum(pr,t-12*2,t+0))'

lvar.1='pr'
lvrts.1='accum'
#lvrts.1='instant'


lvar.3='pr'
lvrts.3='accum'

lvar.6='pr'
lvrts.6='accum'

lvar.12='pr'
lvrts.12='accum'

lcenter='NHC'
lmodel='CPC'
print 'qqqqq 'dpath
print 'ooooo 'opath
fd=ofile (dpath)
if(fd<=0) ; say 'no data file' ; 'quit' ; endif

rc=metadata(fd,'y')

'set_lats parmtab lats.pr.table.txt'

'set_lats convention 'outconv
'set_lats calendar standard'
'set_lats frequency hourly'
'set_lats model "'lmodel'"'
'set_lats center 'lcenter
'set_lats comment "qmorph pr"'

'set_lats gridtype linear'
'set x 1 '_nx.fd
'set y 1 '_ny.fd

'set_lats timeoption dim_env'
'set t 1'

#'set gxout latsgrid'
'lats_grid 'dvar
id_grid=subwrd(result,5)
if(id_grid = 0) ; say 'unable to define the LATS GRID; sayoonara, baby' ; 'quit' ; endif

gtime=dtg2gtime(dtg)
'set time 'gtime


ngood06=chkvar(pr,6*2,dtg)
ngood12=chkvar(pr,12*2,dtg)

pgood06=(ngood06/(6*2))*100.0
pgood12=(ngood12/(12*2))*100.0
pgood06=math_nint(pgood06)
pgood12=math_nint(pgood12)

print 'RRRRRRRCCCCCCC 06h -- 'ngood06' 12: 'ngood12' pgood06: 'pgood06' pgood12: 'pgood12

rc=getdimenv()

#rc=praccum(1,lvar.1,lvrts.1,id_grid,opath,dtg)
#rc=praccum(3,lvar.3,lvrts.3,id_grid,opath,dtg)
if(pgood06 >= minpgood)
  lopath=praccum(6,ngood06,lvar.6,lvrts.6,id_grid,opath,dtg)
  print 'YYYYYYYYYYYYYY 06h -- pgood06: 'pgood06' making: 'lopath'.grb'
else
  print 'NNNNNNNNNNNNNN 06h -- pgood06: 'pgood06
endif

if(pgood12 >= minpgood)
  lopath=praccum(12,ngood12,lvar.12,lvrts.12,id_grid,opath,dtg)
  print 'YYYYYYYYYYYYYY 12h -- pgood12: 'pgood12' making: 'lopath'.grb'
else
  print 'NNNNNNNNNNNNNN 12h -- pgood12: 'pgood12
endif

'quit'
return

# -- only for data processing
#
function chkvar(var,nb,dtg)
goodmaxv=1000.0
ngood=0
'set gxout stat'
ct=nb-1
#print 'asdfasdfasdf'
while (ct >= 0)
  'd 'var'(t-'ct')'
  card=sublin(result,7)
  card8=sublin(result,8)
  nvalid=subwrd(card,8)
  maxv=subwrd(card8,5)
  
#  card9=sublin(result,9)
#  card10=sublin(result,10)
#  meanv=subwrd(card10,2)
#  print 'qqq dtg: 'dtg' ct: 'ct' nvalid: 'nvalid' maxv: 'maxv' meanv: 'meanv
  
  if(nvalid > 0 & maxv < goodmaxv)
    ngood=ngood+1
  endif
  ct=ct-1
endwhile

'set gxout contour'
return(ngood)





function praccum(acp,ngood,lvar,lvrts,id_grid,opath,dtg)

'set_lats deltat '0

if(acp < 10)              ;  lopath=opath'_a0'acp'h_'dtg ; endif
if(acp > 10 & acp < 100)  ;  lopath=opath'_a'acp'h_'dtg ; endif


'set_lats create 'lopath

id_file=subwrd(result,5)
if(id_file<=0) ; say 'unable to create LATS output file 'opath' sayoonara, baby ' ; 'quit' ; endif
'set_lats var 'id_file' 'lvar' 'lvrts' 'id_grid' 0'
id_var=subwrd(result,5)
if(!id_var) ; print 'unable to define the LATS VAR 'acp'; sayoonara, baby' ; 'quit' ; endif

naccum=acp*2-1
#
# convert to mm/day .. units is mm/h hence divide by my # h (acp) vice # time steps
#
sfact=24.0/naccum
sfact=24.0/ngood
'pra=sum(pr,t-'naccum',t+'0')*'sfact

#'set gxout latsdata'
'set_lats write 'id_file' 'id_var
id_write=subwrd(result,5)
if(id_write >0) 
#  'd pra'
  'lats_data pra'
  id_output=subwrd(result,5)
else
  print 'unable to set up write for VAR 'acp'; sayoonara, baby'
 'quit'
endif
'set_lats close 'id_file

return(lopath)

