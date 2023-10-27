function main(args)
dlat=0.5
elon=360.0-dlat

'open navyh2o.ctl'
'lf=regrid2(w,'dlat')'
'm100=const(maskout(lf,lf-98),100)'
'm100=const(m100,0,-u)'
'ml=maskout(lf,-m100)'
'ml=const(ml,0,-u)'
'lff=ml+m100'
'lff=lff*0.01'
'lf=lf*0.01'

'set lon 0 'elon
'set fwrite lf.navy.05deg.dat'
'set gxout fwrite '
'd lff'
print result
'disable fwrite'
'set gxout grfill'
'd lf'
'cbarn'
'q pos'
'c'
'd lff'
'cbarn'



return
