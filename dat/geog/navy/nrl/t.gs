function main(args)
dset='navyh20'
dset='rosmond'



if(dset=rosmond)
'open t.ctl'
gname='rosmond.ls.gif'
'set lat 40 50'
'set lon -90 -70'
'set mpdset hires'
'set gxout fgrid'
'set fgvals 0 2'
'd w'
'draw title Rosmond land-set data set ilsfil on 10 min grid'
'!xtof /scratch/ftp/pub/fiorino/tmp/'gname' GIF'
endif

if(dset=navyh20)
'open ../navyh2o.ctl'
gname='navyh2o.gif'
'set lat 40 50'
'set lon -90 -70'
'set mpdset hires'
'set gxout grfill'
'set clevs 80 90 95'
'set ccols 0 3 4 2'
'd w'
'cbarn'
'draw title % water data base from Navy(?) on 10 min grid'
'!xtof /scratch/ftp/pub/fiorino/tmp/'gname' GIF'
endif

