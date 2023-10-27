function main(args)

rc=gsfallow(on)
dpath=subwrd(args,1)
opath=subwrd(args,2)
d025path='dum.qmorph.ctl'

outconv='grads_grib'
outconv='grib_only'
_gvar.1='grid'

*
*	OUTPUT -- set up, use standard AMIP II names
*

_lofile=opath

_nv=1

_lvar.1='pr'

_lnm.1='msl'

_lvrts.1='accum'

_cnm.1='NHC'


*************************
*
*11111111111111 open the GrADS grid data file -- a dummy data set which provides grid information
*
*************************

_fd=ofile (dpath)
if(_fd<=0) ; say 'no data file' ; 'quit' ; endif
rc=metadata(_fd,'y')

_fd025=ofile(d025path)

*	get the meta data for 0.25 grid
*
rc=metadata(_fd025,'y')

'set_lats parmtab lats.pr.table.txt'

'set_lats convention 'outconv
'set_lats calendar standard'

'set_lats frequency minutes'
'set_lats deltat 30'

'set_lats model "CPC"'
'set_lats center '_cnm.1
'set_lats comment "qmorph pr"'
'set_lats create '_lofile

id_file=subwrd(result,5)

if(id_file<=0) ; say 'unable to create LATS output file '_lofile' sayoonara, baby ' ; 'quit' ; endif

#'set_lats basetime 'id_file' 2008 3 14 18'

'set_lats gridtype linear'

'set x 1 '_nx._fd025
'set y 1 '_ny._fd025

'lats_grid pr.'_fd025'(t=1)'
id_grid=subwrd(result,5)
if(id_grid = 0 ) ; say 'unable to define the LATS GRID; sayoonara, baby' ; 'quit' ; endif

'set dfile '_fd
'set x 1 '_nx._fd
'set y 1 '_ny._fd

'set_lats timeoption dim_env'
'set t 1'
*
'set_lats var 'id_file' '_lvar.1' '_lvrts.1' 'id_grid' 0'
id_var.1=subwrd(result,5)
if(id_var.1 = 0) ; print 'unable to define the LATS VAR 1; sayoonara, baby' ; 'quit' ; endif

*************************
*
*	output section
*
*	loop through time, levels and variables
*
*************************

nt=2
t=1
while(t<=nt)

'set t 't

'set_lats write 'id_file' 'id_var.1
id_write=subwrd(result,5)
if(id_write = 0) ; say 'unable to set up write for VAR 1; sayoonara, baby' ; 'quit' ; endif

var=_lvar.1
lexpr='re('var'.'_fd','_nx._fd025',linear,'_x0._fd025','_dx._fd025','_ny._fd025',linear,'_y0._fd025','_dy._fd025')'

'lats_data 'lexpr
id_data=subwrd(result,5)
if(id_data = 0) ; say 'unable to set up write for VAR 1; sayoonara, baby' ; 'quit' ; endif

t=t+1

endwhile

'set_lats close 'id_file

'quit'

return
