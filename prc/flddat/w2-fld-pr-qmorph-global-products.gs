function main(args)

rc=gsfallow(on)
rc=const()

i=1

dtg=subwrd(args,i)     ; i=i+1
ibase=subwrd(args,i)   ; i=i+1
obase=subwrd(args,i)   ; i=i+1
acp=subwrd(args,i)     ; i=i+1
setyear=subwrd(args,i) ; i=i+1

outconv='grads_grib'
outconv='grib_only'

dvar='pr'
dvarchk='pr'

#
# global 0.5 deg grid
#
_nxg=720
_nyg=361
_dlong=0.5
_dlatg=0.5


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

if(acp < 10)
  lipath=ibase'_a0'acp'h.ctl'
  if(setyear != 'None') ; lipath=ibase'_a0'acp'h-'setyear'.ctl' ; endif
  lobase=obase'_a0'acp'h_global_'dtg
endif

if(acp > 10 & acp < 100)
  lipath=ibase'_a'acp'h.ctl'
  if(setyear != 'None') ; lipath=ibase'_a'acp'h-'setyear'.ctl' ; endif
  lobase=obase'_a'acp'h_global_'dtg
endif

print 'IIII--- 'lipath
fd=ofile (lipath)
if(fd<=0) ; say 'no data file' ; 'quit' ; endif

#
# set up output grid using a dummy file
#

fdg=ofile('dum05.ctl')

rc=metadata(fdg,'y')

'set dfile 'fdg
nxg=_nx.fd
nyg=_ny.fd

'set_lats parmtab lats.pr.table.txt'

'set_lats convention 'outconv
'set_lats calendar standard'
'set_lats frequency hourly'
'set_lats model "'lmodel'"'
'set_lats center 'lcenter
'set_lats comment "qmorph pr"'

'set_lats gridtype linear'
'set x 1 '_nxg
'set y 1 '_nyg

'set_lats timeoption dim_env'
'set t 1'

'lats_grid d'
id_grid=subwrd(result,5)
if(!id_grid) ; say 'unable to define the LATS GRID; sayoonara, baby' ; 'quit' ; endif

'set dfile 'fd


gtime=dtg2gtime(dtg)
'set time 'gtime

rc=datachk(dvarchk)

if(rc = -999)
  print 'WWWWWWWWWWWWWW no data for 'dtg
  'quit'
endif

rc=praccum(acp,lvar.acp,lvrts.6,id_grid,lobase,dtg)

'quit'

return



function praccum(acp,lvar,lvrts,id_grid,lobase,dtg)

'set_lats deltat '0

'set_lats create 'lobase

id_file=subwrd(result,5)
if(id_file<=0) ; say 'unable to create LATS output file 'lobase' sayoonara, baby ' ; 'quit' ; endif
'set_lats var 'id_file' 'lvar' 'lvrts' 'id_grid' 0'
id_var=subwrd(result,5)
if(!id_var) ; print 'unable to define the LATS VAR 'acp'; sayoonara, baby' ; 'quit' ; endif

'pra=re(pr,'_nxg',linear,0.0,'_dlong','_nyg',linear,-90.0,'_dlatg',ba)'

'set_lats write 'id_file' 'id_var
id_write=subwrd(result,5)
if(id_write>0) 
  'lats_data pra'
  id_output=subwrd(result,5)
else
  print 'unable to set up write for VAR 'acp'; sayoonara, baby'
 'quit'
endif
'set_lats close 'id_file

return


